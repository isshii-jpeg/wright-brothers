/**
 * @file main.c
 * @brief Main firmware - Open Excretion Care System (OECS)
 *
 * Target: STM32F103C8T6
 *
 * System flow:
 *   1. Initialize peripherals (I2C, ADC, GPIO, UART)
 *   2. Poll sensors at fixed interval
 *   3. Run D-S evidence fusion to classify state
 *   4. Execute cleaning cycle if excretion detected
 *   5. Return to monitoring
 */

#include "main.h"
#include "../../algorithm/c/ds_evidence.h"
#include <string.h>
#include <stdio.h>

/* ---------- Peripheral Handles ---------- */

I2C_HandleTypeDef  hi2c1;
ADC_HandleTypeDef  hadc1;
UART_HandleTypeDef huart1;
TIM_HandleTypeDef  htim2;

/* ---------- State Machine ---------- */

typedef enum {
    SYSTEM_MONITORING,
    SYSTEM_DETECTED,
    SYSTEM_SUCTION,
    SYSTEM_WASHING,
    SYSTEM_DRYING,
    SYSTEM_COMPLETE,
    SYSTEM_ERROR
} SystemState;

static volatile SystemState system_state = SYSTEM_MONITORING;
static volatile uint32_t    phase_start_tick = 0;
static ExcretionState       detected_type = STATE_NORMAL;
static uint8_t              detection_count = 0;

/* ---------- Forward Declarations ---------- */

static void MX_GPIO_Init(void);
static void MX_I2C1_Init(void);
static void MX_ADC1_Init(void);
static void MX_USART1_UART_Init(void);
static void MX_TIM2_Init(void);

static SensorReading read_sensors(void);
static void set_actuators(const ActuatorCommand *cmd);
static void actuators_off(void);
static void run_cleaning_cycle(ExcretionState type);
static void debug_print(const char *msg);
static uint8_t check_safety(void);

/* ---------- Sensor Drivers ---------- */

/* SHT30 I2C address */
#define SHT30_ADDR  (0x44 << 1)

static SensorReading read_sensors(void)
{
    SensorReading reading = { 0, 0, 0 };
    uint8_t sht30_cmd[2] = { 0x2C, 0x06 }; /* High repeatability, clock stretching */
    uint8_t sht30_data[6];

    /* --- Read SHT30 (Temperature + Humidity) --- */
    if (HAL_I2C_Master_Transmit(&hi2c1, SHT30_ADDR, sht30_cmd, 2, 100) == HAL_OK) {
        HAL_Delay(20); /* Measurement time */
        if (HAL_I2C_Master_Receive(&hi2c1, SHT30_ADDR, sht30_data, 6, 100) == HAL_OK) {
            /* Temperature: -45 + 175 * (raw / 65535) -> scaled x10 */
            uint16_t raw_temp = (sht30_data[0] << 8) | sht30_data[1];
            int32_t temp_x100 = -4500 + (17500 * (int32_t)raw_temp) / 65535;
            reading.temperature_x10 = (int16_t)(temp_x100 / 10);

            /* Humidity: 100 * (raw / 65535) -> scaled x10 */
            uint16_t raw_hum = (sht30_data[3] << 8) | sht30_data[4];
            reading.humidity_x10 = (uint16_t)((1000 * (uint32_t)raw_hum) / 65535);
        }
    }

    /* --- Read MQ-135 (NH3 Gas via ADC) --- */
    HAL_ADC_Start(&hadc1);
    if (HAL_ADC_PollForConversion(&hadc1, 100) == HAL_OK) {
        uint32_t adc_raw = HAL_ADC_GetValue(&hadc1);
        /*
         * MQ-135 calibration (approximate):
         * ADC 12-bit (0-4095) maps to 0-3.3V
         * Sensor resistance ratio Rs/R0 converted to ppm
         * This is a simplified linear mapping; real deployment needs
         * proper calibration curve (see MQ-135 datasheet).
         */
        reading.nh3_ppm_x10 = (uint16_t)((adc_raw * 500) / 4095); /* 0-50.0 ppm range */
    }
    HAL_ADC_Stop(&hadc1);

    return reading;
}

/* ---------- Actuator Control ---------- */

static void set_actuator_pin(GPIO_TypeDef *port, uint16_t pin, uint8_t state)
{
    HAL_GPIO_WritePin(port, pin, state ? GPIO_PIN_SET : GPIO_PIN_RESET);
}

static void set_actuators(const ActuatorCommand *cmd)
{
    set_actuator_pin(SUCTION_PUMP_Port, SUCTION_PUMP_Pin, cmd->suction_pump);
    set_actuator_pin(WATER_PUMP_Port,   WATER_PUMP_Pin,   cmd->water_pump);
    set_actuator_pin(HEATER_Port,       HEATER_Pin,       cmd->heater);
    set_actuator_pin(FAN_Port,          FAN_Pin,          cmd->fan);
}

static void actuators_off(void)
{
    ActuatorCommand off = { 0, 0, 0, 0, 0 };
    set_actuators(&off);
}

/* ---------- Safety Check ---------- */

static uint8_t check_safety(void)
{
    /* Check emergency stop button */
    if (HAL_GPIO_ReadPin(EMERGENCY_STOP_Port, EMERGENCY_STOP_Pin) == GPIO_PIN_SET) {
        return 0; /* UNSAFE */
    }
    /* TODO: Check water temperature sensor feedback */
    /* TODO: Check suction pressure sensor feedback */
    return 1; /* SAFE */
}

/* ---------- Cleaning Cycle State Machine ---------- */

static void run_cleaning_cycle(ExcretionState type)
{
    uint32_t elapsed = HAL_GetTick() - phase_start_tick;
    uint16_t multiplier = (type == STATE_FECES) ? FECES_MULTIPLIER : 1;

    if (!check_safety()) {
        actuators_off();
        system_state = SYSTEM_ERROR;
        debug_print("[ERROR] Safety check failed - all actuators OFF\r\n");
        return;
    }

    switch (system_state) {
    case SYSTEM_SUCTION:
        if (elapsed < SUCTION_DURATION_MS * multiplier) {
            set_actuator_pin(SUCTION_PUMP_Port, SUCTION_PUMP_Pin, 1);
        } else {
            set_actuator_pin(SUCTION_PUMP_Port, SUCTION_PUMP_Pin, 0);
            system_state = SYSTEM_WASHING;
            phase_start_tick = HAL_GetTick();
            debug_print("[PHASE] Suction complete -> Washing\r\n");
        }
        break;

    case SYSTEM_WASHING:
        if (elapsed < WASH_DURATION_MS * multiplier) {
            set_actuator_pin(WATER_PUMP_Port, WATER_PUMP_Pin, 1);
        } else {
            set_actuator_pin(WATER_PUMP_Port, WATER_PUMP_Pin, 0);
            system_state = SYSTEM_DRYING;
            phase_start_tick = HAL_GetTick();
            debug_print("[PHASE] Washing complete -> Drying\r\n");
        }
        break;

    case SYSTEM_DRYING:
        if (elapsed < DRY_DURATION_MS * multiplier) {
            set_actuator_pin(HEATER_Port, HEATER_Pin, 1);
            set_actuator_pin(FAN_Port, FAN_Pin, 1);
        } else {
            actuators_off();
            system_state = SYSTEM_COMPLETE;
            debug_print("[PHASE] Drying complete -> Cycle finished\r\n");
        }
        break;

    default:
        break;
    }
}

/* ---------- Debug Output ---------- */

static void debug_print(const char *msg)
{
    HAL_UART_Transmit(&huart1, (uint8_t *)msg, strlen(msg), 100);
}

/* ---------- Main ---------- */

int main(void)
{
    HAL_Init();
    SystemClock_Config();

    MX_GPIO_Init();
    MX_I2C1_Init();
    MX_ADC1_Init();
    MX_USART1_UART_Init();
    MX_TIM2_Init();

    actuators_off();

    debug_print("\r\n=== OECS Firmware v0.1 ===\r\n");
    debug_print("Open Excretion Care System initialized.\r\n");

    uint32_t last_sensor_tick = 0;
    char debug_buf[128];

    while (1) {
        uint32_t now = HAL_GetTick();

        switch (system_state) {
        case SYSTEM_MONITORING:
            /* Poll sensors at fixed interval */
            if (now - last_sensor_tick >= SENSOR_POLL_INTERVAL_MS) {
                last_sensor_tick = now;

                SensorReading reading = read_sensors();
                MassFunction fused;
                ExcretionState state = ds_classify(&reading, &fused);

                /* Debounce: require consecutive detections */
                if (state != STATE_NORMAL) {
                    detection_count++;
                    if (detection_count >= DEBOUNCE_COUNT) {
                        detected_type = state;
                        system_state = SYSTEM_DETECTED;
                        detection_count = 0;

                        snprintf(debug_buf, sizeof(debug_buf),
                            "[DETECT] %s (T=%d.%d H=%d.%d NH3=%d.%d)\r\n",
                            (state == STATE_URINE) ? "URINE" : "FECES",
                            reading.temperature_x10 / 10,
                            reading.temperature_x10 % 10,
                            reading.humidity_x10 / 10,
                            reading.humidity_x10 % 10,
                            reading.nh3_ppm_x10 / 10,
                            reading.nh3_ppm_x10 % 10);
                        debug_print(debug_buf);
                    }
                } else {
                    detection_count = 0;
                }

                /* Blink LED to show alive */
                HAL_GPIO_TogglePin(LED_STATUS_Port, LED_STATUS_Pin);
            }
            break;

        case SYSTEM_DETECTED:
            /* Start cleaning cycle */
            system_state = SYSTEM_SUCTION;
            phase_start_tick = HAL_GetTick();
            debug_print("[CYCLE] Starting cleaning cycle\r\n");
            break;

        case SYSTEM_SUCTION:
        case SYSTEM_WASHING:
        case SYSTEM_DRYING:
            run_cleaning_cycle(detected_type);
            break;

        case SYSTEM_COMPLETE:
            debug_print("[CYCLE] Returning to monitoring\r\n");
            system_state = SYSTEM_MONITORING;
            detection_count = 0;
            break;

        case SYSTEM_ERROR:
            /* Flash LED rapidly to indicate error */
            HAL_GPIO_TogglePin(LED_STATUS_Port, LED_STATUS_Pin);
            HAL_Delay(200);
            /* Reset after emergency stop released */
            if (check_safety()) {
                debug_print("[RECOVERY] Safety OK - resuming monitoring\r\n");
                system_state = SYSTEM_MONITORING;
            }
            break;
        }
    }
}

/* ---------- Peripheral Initialization ---------- */

void SystemClock_Config(void)
{
    /* Configure HSE (8MHz) -> PLL (72MHz) */
    RCC_OscInitTypeDef osc = { 0 };
    osc.OscillatorType = RCC_OSCILLATORTYPE_HSE;
    osc.HSEState = RCC_HSE_ON;
    osc.PLL.PLLState = RCC_PLL_ON;
    osc.PLL.PLLSource = RCC_PLLSOURCE_HSE;
    osc.PLL.PLLMUL = RCC_PLL_MUL9;
    HAL_RCC_OscConfig(&osc);

    RCC_ClkInitTypeDef clk = { 0 };
    clk.ClockType = RCC_CLOCKTYPE_HCLK | RCC_CLOCKTYPE_SYSCLK |
                    RCC_CLOCKTYPE_PCLK1 | RCC_CLOCKTYPE_PCLK2;
    clk.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
    clk.AHBCLKDivider = RCC_SYSCLK_DIV1;
    clk.APB1CLKDivider = RCC_HCLK_DIV2;
    clk.APB2CLKDivider = RCC_HCLK_DIV1;
    HAL_RCC_ClockConfig(&clk, FLASH_LATENCY_2);
}

static void MX_I2C1_Init(void)
{
    hi2c1.Instance = I2C1;
    hi2c1.Init.ClockSpeed = 100000;    /* 100kHz standard mode */
    hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
    hi2c1.Init.OwnAddress1 = 0;
    hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
    HAL_I2C_Init(&hi2c1);
}

static void MX_ADC1_Init(void)
{
    hadc1.Instance = ADC1;
    hadc1.Init.ScanConvMode = ADC_SCAN_DISABLE;
    hadc1.Init.ContinuousConvMode = DISABLE;
    hadc1.Init.DiscontinuousConvMode = DISABLE;
    hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;
    hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
    hadc1.Init.NbrOfConversion = 1;
    HAL_ADC_Init(&hadc1);

    ADC_ChannelConfTypeDef ch = { 0 };
    ch.Channel = GAS_SENSOR_ADC_Channel;
    ch.Rank = ADC_REGULAR_RANK_1;
    ch.SamplingTime = ADC_SAMPLETIME_239CYCLES_5; /* Slow for stable gas reading */
    HAL_ADC_ConfigChannel(&hadc1, &ch);
}

static void MX_USART1_UART_Init(void)
{
    huart1.Instance = USART1;
    huart1.Init.BaudRate = 115200;
    huart1.Init.WordLength = UART_WORDLENGTH_8B;
    huart1.Init.StopBits = UART_STOPBITS_1;
    huart1.Init.Parity = UART_PARITY_NONE;
    huart1.Init.Mode = UART_MODE_TX_RX;
    huart1.Init.HwFlowCtl = UART_HWCONTROL_NONE;
    HAL_UART_Init(&huart1);
}

static void MX_TIM2_Init(void)
{
    htim2.Instance = TIM2;
    htim2.Init.Prescaler = 7200 - 1;  /* 72MHz / 7200 = 10kHz */
    htim2.Init.CounterMode = TIM_COUNTERMODE_UP;
    htim2.Init.Period = 10000 - 1;     /* 10kHz / 10000 = 1Hz interrupt */
    htim2.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
    HAL_TIM_Base_Init(&htim2);
}

static void MX_GPIO_Init(void)
{
    GPIO_InitTypeDef gpio = { 0 };

    __HAL_RCC_GPIOA_CLK_ENABLE();
    __HAL_RCC_GPIOB_CLK_ENABLE();
    __HAL_RCC_GPIOC_CLK_ENABLE();

    /* Actuator outputs */
    gpio.Mode = GPIO_MODE_OUTPUT_PP;
    gpio.Pull = GPIO_NOPULL;
    gpio.Speed = GPIO_SPEED_FREQ_LOW;

    gpio.Pin = SUCTION_PUMP_Pin | WATER_PUMP_Pin | HEATER_Pin | FAN_Pin;
    HAL_GPIO_Init(GPIOA, &gpio);

    /* Status LED (PC13 on Blue Pill - active low) */
    gpio.Pin = LED_STATUS_Pin;
    HAL_GPIO_Init(LED_STATUS_Port, &gpio);

    /* Emergency stop input (active high with external pull-down) */
    gpio.Mode = GPIO_MODE_INPUT;
    gpio.Pull = GPIO_PULLDOWN;
    gpio.Pin = EMERGENCY_STOP_Pin;
    HAL_GPIO_Init(EMERGENCY_STOP_Port, &gpio);

    /* Ensure all actuators start OFF */
    HAL_GPIO_WritePin(GPIOA, SUCTION_PUMP_Pin | WATER_PUMP_Pin |
                      HEATER_Pin | FAN_Pin, GPIO_PIN_RESET);
}

void Error_Handler(void)
{
    actuators_off();
    while (1) {
        HAL_GPIO_TogglePin(LED_STATUS_Port, LED_STATUS_Pin);
        HAL_Delay(100);
    }
}
