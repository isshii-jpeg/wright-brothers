/**
 * @file ds_evidence.h
 * @brief Dempster-Shafer Evidence Theory for Excretion Detection
 *
 * Embedded C implementation for STM32F103.
 * Based on: Hu & Chen et al., Healthcare 2023, 11(3), 388
 */

#ifndef DS_EVIDENCE_H
#define DS_EVIDENCE_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/* ---------- Data Types ---------- */

typedef enum {
    STATE_NORMAL = 0,
    STATE_URINE  = 1,
    STATE_FECES  = 2,
    STATE_COUNT  = 3
} ExcretionState;

/**
 * Basic Probability Assignment (BPA) / Mass Function
 * All values are fixed-point Q16 (multiply float by 65536).
 * This avoids floating-point on Cortex-M3.
 */
typedef struct {
    uint16_t normal;      /* m({normal})     */
    uint16_t urine;       /* m({urine})      */
    uint16_t feces;       /* m({feces})      */
    uint16_t uncertainty; /* m(Theta)        */
} MassFunction;

/** Raw sensor reading (integer-scaled for ADC) */
typedef struct {
    int16_t  temperature_x10;  /* Temperature * 10 (e.g., 331 = 33.1°C) */
    uint16_t humidity_x10;     /* Humidity * 10    (e.g., 500 = 50.0%)  */
    uint16_t nh3_ppm_x10;     /* NH3 * 10         (e.g., 20  = 2.0ppm) */
} SensorReading;

/** Actuator command output */
typedef struct {
    uint8_t suction_pump;  /* 0=OFF, 1=ON */
    uint8_t water_pump;    /* 0=OFF, 1=ON */
    uint8_t heater;        /* 0=OFF, 1=ON */
    uint8_t fan;           /* 0=OFF, 1=ON */
    uint16_t duration_sec; /* Recommended cycle duration */
} ActuatorCommand;

/* ---------- Constants ---------- */

#define Q16_ONE       65536U   /* 1.0 in Q16 fixed-point */
#define Q16_HALF      32768U   /* 0.5 in Q16 */
#define CLASSIFY_THRESHOLD  26214U  /* 0.4 in Q16 */

/* Baseline temperature * 10 */
#define TEMP_BASELINE_X10   330

/* ---------- API Functions ---------- */

/**
 * Convert temperature reading to BPA.
 * @param temp_x10 Temperature * 10
 * @return Mass function for temperature evidence
 */
MassFunction ds_temperature_to_bpa(int16_t temp_x10);

/**
 * Convert humidity reading to BPA.
 * @param humidity_x10 Humidity * 10
 * @return Mass function for humidity evidence
 */
MassFunction ds_humidity_to_bpa(uint16_t humidity_x10);

/**
 * Convert NH3 gas reading to BPA.
 * @param nh3_x10 NH3 concentration * 10
 * @return Mass function for gas evidence
 */
MassFunction ds_nh3_to_bpa(uint16_t nh3_x10);

/**
 * Combine two mass functions using Dempster's rule.
 * @param m1 First mass function
 * @param m2 Second mass function
 * @return Combined mass function
 */
MassFunction ds_combine(const MassFunction *m1, const MassFunction *m2);

/**
 * Full classification pipeline: sensor -> BPA -> fusion -> decision.
 * @param reading Sensor data
 * @param out_mass Output: final fused mass function (can be NULL)
 * @return Detected excretion state
 */
ExcretionState ds_classify(const SensorReading *reading, MassFunction *out_mass);

/**
 * Map detected state to actuator commands.
 * @param state Detected state
 * @return Actuator command structure
 */
ActuatorCommand ds_get_action(ExcretionState state);

#ifdef __cplusplus
}
#endif

#endif /* DS_EVIDENCE_H */
