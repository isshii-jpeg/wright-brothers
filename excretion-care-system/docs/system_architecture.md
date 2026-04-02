# System Architecture

## High-Level Block Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    PATIENT INTERFACE                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           3D-Printed TPU Receiver                     │   │
│  │  ┌─────────┐  ┌──────────┐  ┌──────────────────┐    │   │
│  │  │  SHT30  │  │  MQ-135  │  │  Suction/Water   │    │   │
│  │  │ Temp/RH │  │ NH3 Gas  │  │  Inlet Ports     │    │   │
│  │  └────┬────┘  └────┬─────┘  └────────┬─────────┘    │   │
│  └───────┼─────────────┼────────────────┼───────────────┘   │
└──────────┼─────────────┼────────────────┼───────────────────┘
           │ I2C         │ ADC            │ Tubing
           ▼             ▼                ▼
┌──────────────────────────────────────────────────────────────┐
│                   CONTROLLER UNIT                             │
│                                                               │
│  ┌────────────────────────────────────────┐                  │
│  │         STM32F103C8T6                  │                  │
│  │                                        │                  │
│  │  ┌──────────────────────────────────┐  │                  │
│  │  │   D-S Evidence Fusion Engine     │  │                  │
│  │  │   (or 1D-CNN via X-CUBE-AI)      │  │                  │
│  │  └──────────────┬───────────────────┘  │                  │
│  │                 │                      │                  │
│  │    ┌────────────┼────────────┐         │                  │
│  │    ▼            ▼            ▼         │                  │
│  │  GPIO_A8    GPIO_A9     GPIO_A10/11    │                  │
│  └────┬────────────┬────────────┬─────────┘                  │
│       │            │            │                             │
│  ┌────▼────┐  ┌────▼────┐  ┌───▼──────┐                     │
│  │  L298N  │  │  L298N  │  │ IRF520x2 │                     │
│  │ Motor   │  │ Motor   │  │ MOSFET   │                     │
│  │ Driver  │  │ Driver  │  │ Modules  │                     │
│  └────┬────┘  └────┬────┘  └──┬────┬──┘                     │
│       │            │           │    │                         │
│  ┌────▼────┐  ┌────▼────┐  ┌──▼─┐ ┌▼──┐                     │
│  │ Suction │  │  Water  │  │Heat│ │Fan│                      │
│  │  Pump   │  │  Pump   │  │ er │ │   │                      │
│  │  12V    │  │  12V    │  │12V │ │12V│                      │
│  └─────────┘  └─────────┘  └────┘ └───┘                     │
│                                                               │
│  ┌────────────┐  ┌─────────────┐  ┌─────────────┐           │
│  │ 12V 5A PSU │  │ AMS1117-3.3 │  │ Thermal Fuse│           │
│  │ (Input)    │  │ (MCU power) │  │ (Safety)    │           │
│  └────────────┘  └─────────────┘  └─────────────┘           │
└──────────────────────────────────────────────────────────────┘
```

## State Machine

```
                    ┌──────────┐
                    │  POWER   │
                    │   ON     │
                    └────┬─────┘
                         │
                         ▼
              ┌──────────────────┐
         ┌───>│   MONITORING     │<──────────────┐
         │    │  (poll sensors   │               │
         │    │   every 1 sec)   │               │
         │    └────────┬─────────┘               │
         │             │                         │
         │     Detection ≥ 3x                    │
         │     consecutive                       │
         │             │                         │
         │             ▼                         │
         │    ┌──────────────────┐               │
         │    │   SUCTION        │               │
         │    │  30s (urine)     │               │
         │    │  60s (feces)     │               │
         │    └────────┬─────────┘               │
         │             │                         │
         │             ▼                         │
         │    ┌──────────────────┐               │
         │    │   WASHING        │               │
         │    │  60s (urine)     │               │
         │    │  120s (feces)    │               │
         │    └────────┬─────────┘               │
         │             │                         │
         │             ▼                         │
         │    ┌──────────────────┐               │
         │    │   DRYING         │      ┌────────┴───────┐
         │    │  90s (urine)     │      │   COMPLETE      │
         │    │  180s (feces)    ├─────>│   (return to    │
         │    └──────────────────┘      │   monitoring)   │
         │                              └────────────────┘
         │
         │    ┌──────────────────┐
         └────┤   ERROR          │
              │  (safety trip    │
              │   all OFF)       │
              └──────────────────┘
                 ↑ Emergency stop
                 ↑ Over-temperature
                 ↑ Over-pressure
```

## D-S Evidence Theory Flow

```
Sensor Data                    BPA Mapping              Fusion              Decision
───────────                    ───────────              ──────              ────────

Temperature ──> temp_to_bpa() ──> m_temp ─┐
                                           ├─ ds_combine() ─> m_12 ─┐
Humidity ────> hum_to_bpa()  ──> m_hum  ─┘                          │
                                                                     ├─ ds_combine() ─> m_final ─> argmax ─> State
NH3 Gas ─────> nh3_to_bpa()  ──> m_nh3  ────────────────────────────┘

m_final = { normal: 0.xx, urine: 0.xx, feces: 0.xx, uncertainty: 0.xx }
                                                                    │
                                                        if max > threshold (0.4)
                                                                    │
                                                              ┌─────┴─────┐
                                                              ▼           ▼
                                                         DETECTED    NORMAL
                                                        (trigger    (continue
                                                         cycle)     monitoring)
```

## AI Extension Path

```
Classical Pipeline (D-S)          AI Pipeline (1D-CNN)
────────────────────               ─────────────────────

Sensor → BPA → Fusion → Decision  Sensor → Window Buffer → CNN → Decision
                                              (60 samples)
Pros:                              Pros:
  - Deterministic                    - Learns temporal patterns
  - Low compute                      - Predictive capability
  - Interpretable                    - Higher potential accuracy
  - No training data needed          - Adapts to individual patients

Cons:                              Cons:
  - Hand-tuned thresholds            - Needs training data
  - No temporal awareness            - Black box
  - Fixed decision boundaries        - More compute / memory
```
