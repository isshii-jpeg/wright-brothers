# Circuit Schematics

## Overview

The system uses a STM32F103C8T6 "Blue Pill" as the central controller.

## Pin Assignment

```
STM32F103C8T6 Pin Map
=====================

PA0  ── ADC1_CH0 ──── MQ-135 analog output
PA8  ── GPIO_OUT ──── Suction pump (via L298N IN1)
PA9  ── USART1_TX ─── Debug UART / Bluetooth TX
PA10 ── USART1_RX ─── Debug UART / Bluetooth RX
PA11 ── GPIO_OUT ──── Fan (via IRF520 MOSFET)
PA12 ── GPIO_IN  ──── Emergency stop button (NC, active high)

PB6  ── I2C1_SCL ──── SHT30 SCL (4.7kΩ pull-up to 3.3V)
PB7  ── I2C1_SDA ──── SHT30 SDA (4.7kΩ pull-up to 3.3V)

PC13 ── GPIO_OUT ──── Status LED (onboard, active low)

PA9  ── GPIO_OUT ──── Water pump (via L298N IN3)  [shared with UART TX - select one]
PA10 ── GPIO_OUT ──── Heater (via IRF520 MOSFET)  [shared with UART RX - select one]
```

> **Note**: PA9/PA10 conflict between UART and actuator control.
> For development, use UART for debugging.
> For production, remap UART to USART2 (PA2/PA3) and free PA9/PA10 for actuators.

## Power Distribution

```
12V 5A PSU
├── L298N motor driver (12V input)
│   ├── Suction pump (OUT1/OUT2)
│   └── Water pump (OUT3/OUT4)
├── IRF520 MOSFET #1
│   └── PTC Heater (12V, max 50W = 4.2A)
│       └── 73°C thermal fuse in series (safety)
├── IRF520 MOSFET #2
│   └── Blower fan (12V, ~0.3A)
└── AMS1117-3.3V regulator
    ├── STM32F103 (3.3V, ~50mA)
    ├── SHT30 sensor (3.3V, ~1mA)
    └── MQ-135 heater powered from 5V (separate regulator or L298N 5V out)
```

## KiCad Project

Full KiCad schematic and PCB layout files will be added in:
- `oecs_schematic.kicad_sch`
- `oecs_pcb.kicad_pcb`

For now, the system can be prototyped on perfboard with the pin assignments above.
