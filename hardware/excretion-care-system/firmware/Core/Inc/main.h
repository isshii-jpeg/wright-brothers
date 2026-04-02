/**
 * @file main.h
 * @brief Main header - Open Excretion Care System (OECS) Firmware
 *
 * Target: STM32F103C8T6 (Blue Pill)
 * HAL Driver version: STM32Cube HAL
 */

#ifndef __MAIN_H
#define __MAIN_H

#ifdef __cplusplus
extern "C" {
#endif

#include "stm32f1xx_hal.h"

/* ---------- Pin Definitions ---------- */

/* I2C1 - SHT30 Temperature/Humidity Sensor */
#define SENSOR_I2C_SCL_Pin       GPIO_PIN_6
#define SENSOR_I2C_SCL_Port      GPIOB
#define SENSOR_I2C_SDA_Pin       GPIO_PIN_7
#define SENSOR_I2C_SDA_Port      GPIOB

/* ADC1 - MQ-135 Gas Sensor (analog output) */
#define GAS_SENSOR_ADC_Pin       GPIO_PIN_0
#define GAS_SENSOR_ADC_Port      GPIOA
#define GAS_SENSOR_ADC_Channel   ADC_CHANNEL_0

/* GPIO Outputs - Actuators (active high via MOSFET/relay) */
#define SUCTION_PUMP_Pin         GPIO_PIN_8
#define SUCTION_PUMP_Port        GPIOA
#define WATER_PUMP_Pin           GPIO_PIN_9
#define WATER_PUMP_Port          GPIOA
#define HEATER_Pin               GPIO_PIN_10
#define HEATER_Port              GPIOA
#define FAN_Pin                  GPIO_PIN_11
#define FAN_Port                 GPIOA

/* Safety - Thermal Fuse / Emergency Stop */
#define EMERGENCY_STOP_Pin       GPIO_PIN_12
#define EMERGENCY_STOP_Port      GPIOA

/* Status LED */
#define LED_STATUS_Pin           GPIO_PIN_13
#define LED_STATUS_Port          GPIOC

/* UART1 - Debug / Bluetooth communication */
#define DEBUG_UART_TX_Pin        GPIO_PIN_9
#define DEBUG_UART_TX_Port       GPIOA
#define DEBUG_UART_RX_Pin        GPIO_PIN_10
#define DEBUG_UART_RX_Port       GPIOA

/* ---------- Timing Constants ---------- */

#define SENSOR_POLL_INTERVAL_MS     1000   /* Read sensors every 1 second */
#define DEBOUNCE_COUNT              3      /* Require N consecutive detections */
#define SUCTION_DURATION_MS         30000  /* 30 sec suction phase */
#define WASH_DURATION_MS            60000  /* 60 sec wash phase */
#define DRY_DURATION_MS             90000  /* 90 sec dry phase */
#define FECES_MULTIPLIER            2      /* Feces cycle is 2x longer */

/* ---------- Safety Limits ---------- */

#define WATER_TEMP_MAX_X10          380    /* 38.0°C max water temperature */
#define SUCTION_PRESSURE_MAX_KPA    20     /* -20 kPa max suction */

/* ---------- Function Prototypes ---------- */

void SystemClock_Config(void);
void Error_Handler(void);

#ifdef __cplusplus
}
#endif

#endif /* __MAIN_H */
