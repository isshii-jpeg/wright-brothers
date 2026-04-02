/**
 * @file ds_evidence.c
 * @brief Dempster-Shafer Evidence Theory - Embedded C Implementation
 *
 * Fixed-point Q16 arithmetic for STM32F103 (no FPU).
 * All probabilities are stored as uint16_t where 65536 = 1.0.
 */

#include "ds_evidence.h"

/* ---------- Helper: Q16 multiply ---------- */

static inline uint16_t q16_mul(uint16_t a, uint16_t b)
{
    return (uint16_t)(((uint32_t)a * (uint32_t)b) >> 16);
}

/** Q16 divide: (a << 16) / b */
static inline uint16_t q16_div(uint32_t a_q16, uint16_t b)
{
    if (b == 0) return Q16_ONE;
    return (uint16_t)(((uint32_t)a_q16 << 16) / (uint32_t)b);
}

/* ---------- Sensor-to-BPA Mappings ---------- */

/*
 * BPA values are pre-computed in Q16 fixed-point.
 * Example: 0.7 = 0.7 * 65536 = 45875
 */

#define Q16_002  1311U
#define Q16_003  1966U
#define Q16_005  3277U
#define Q16_010  6554U
#define Q16_013  8520U
#define Q16_015  9830U
#define Q16_018  11796U
#define Q16_020  13107U
#define Q16_022  14418U
#define Q16_023  15073U
#define Q16_025  16384U
#define Q16_030  19661U
#define Q16_040  26214U
#define Q16_045  29491U
#define Q16_050  32768U
#define Q16_055  36045U
#define Q16_060  39322U
#define Q16_070  45875U
#define Q16_075  49152U
#define Q16_080  52429U

MassFunction ds_temperature_to_bpa(int16_t temp_x10)
{
    int16_t delta = temp_x10 - TEMP_BASELINE_X10;
    MassFunction m;

    if (delta < 5) {           /* < 0.5°C change */
        m.normal = Q16_070; m.urine = Q16_005;
        m.feces  = Q16_005; m.uncertainty = Q16_020;
    } else if (delta < 20) {   /* 0.5 - 2.0°C */
        m.normal = Q16_030; m.urine = Q16_020;
        m.feces  = Q16_020; m.uncertainty = Q16_030;
    } else if (delta < 40) {   /* 2.0 - 4.0°C */
        m.normal = Q16_005; m.urine = Q16_050;
        m.feces  = Q16_020; m.uncertainty = Q16_025;
    } else {                   /* > 4.0°C */
        m.normal = Q16_002; m.urine = Q16_055;
        m.feces  = Q16_025; m.uncertainty = Q16_018;
    }
    return m;
}

MassFunction ds_humidity_to_bpa(uint16_t humidity_x10)
{
    MassFunction m;

    if (humidity_x10 < 600) {         /* < 60% */
        m.normal = Q16_075; m.urine = Q16_005;
        m.feces  = Q16_005; m.uncertainty = Q16_015;
    } else if (humidity_x10 < 750) {  /* 60-75% */
        m.normal = Q16_030; m.urine = Q16_025;
        m.feces  = Q16_015; m.uncertainty = Q16_030;
    } else if (humidity_x10 < 850) {  /* 75-85% */
        m.normal = Q16_005; m.urine = Q16_045;
        m.feces  = Q16_025; m.uncertainty = Q16_025;
    } else {                          /* > 85% */
        m.normal = Q16_002; m.urine = Q16_060;
        m.feces  = Q16_020; m.uncertainty = Q16_018;
    }
    return m;
}

MassFunction ds_nh3_to_bpa(uint16_t nh3_x10)
{
    MassFunction m;

    if (nh3_x10 < 50) {             /* < 5 ppm */
        m.normal = Q16_080; m.urine = Q16_005;
        m.feces  = Q16_002; m.uncertainty = Q16_013;
    } else if (nh3_x10 < 150) {     /* 5-15 ppm */
        m.normal = Q16_010; m.urine = Q16_055;
        m.feces  = Q16_010; m.uncertainty = Q16_025;
    } else if (nh3_x10 < 300) {     /* 15-30 ppm */
        m.normal = Q16_003; m.urine = Q16_050;
        m.feces  = Q16_025; m.uncertainty = Q16_022;
    } else {                         /* > 30 ppm */
        m.normal = Q16_002; m.urine = Q16_015;
        m.feces  = Q16_060; m.uncertainty = Q16_023;
    }
    return m;
}

/* ---------- D-S Combination Rule ---------- */

MassFunction ds_combine(const MassFunction *m1, const MassFunction *m2)
{
    MassFunction result;

    /* Focal element arrays for iteration */
    const uint16_t a[4] = { m1->normal, m1->urine, m1->feces, m1->uncertainty };
    const uint16_t b[4] = { m2->normal, m2->urine, m2->feces, m2->uncertainty };

    uint32_t combined[3] = { 0, 0, 0 }; /* normal, urine, feces */
    uint32_t conflict = 0;
    uint32_t unc_product;

    /*
     * Compute pairwise intersections.
     * Index 0-2 = focal elements (normal, urine, feces)
     * Index 3   = uncertainty (Theta)
     */
    for (int i = 0; i < 3; i++) {
        for (int j = 0; j < 3; j++) {
            uint32_t prod = (uint32_t)a[i] * (uint32_t)b[j];
            if (i == j) {
                combined[i] += prod >> 16;
            } else {
                conflict += prod >> 16;
            }
        }
        /* focal[i] * Theta = focal[i] */
        combined[i] += (uint32_t)q16_mul(a[i], b[3]);
        /* Theta * focal[i] = focal[i] */
        combined[i] += (uint32_t)q16_mul(a[3], b[i]);
    }

    /* Theta * Theta */
    unc_product = (uint32_t)q16_mul(a[3], b[3]);

    /* Normalize by (1 - K) */
    uint16_t norm = (uint16_t)(Q16_ONE - conflict);
    if (norm == 0) norm = 1; /* avoid division by zero */

    result.normal      = q16_div(combined[0], norm);
    result.urine       = q16_div(combined[1], norm);
    result.feces       = q16_div(combined[2], norm);
    result.uncertainty = q16_div((uint32_t)unc_product, norm);

    return result;
}

/* ---------- Classification Pipeline ---------- */

ExcretionState ds_classify(const SensorReading *reading, MassFunction *out_mass)
{
    MassFunction m_temp = ds_temperature_to_bpa(reading->temperature_x10);
    MassFunction m_hum  = ds_humidity_to_bpa(reading->humidity_x10);
    MassFunction m_nh3  = ds_nh3_to_bpa(reading->nh3_ppm_x10);

    /* Two-stage fusion: (temp + humidity) -> combine with NH3 */
    MassFunction fused_th  = ds_combine(&m_temp, &m_hum);
    MassFunction fused_all = ds_combine(&fused_th, &m_nh3);

    if (out_mass != NULL) {
        *out_mass = fused_all;
    }

    /* Find maximum belief */
    uint16_t beliefs[3] = {
        fused_all.normal, fused_all.urine, fused_all.feces
    };

    ExcretionState best = STATE_NORMAL;
    uint16_t max_belief = beliefs[0];

    for (int i = 1; i < STATE_COUNT; i++) {
        if (beliefs[i] > max_belief) {
            max_belief = beliefs[i];
            best = (ExcretionState)i;
        }
    }

    /* If below threshold, default to normal */
    if (max_belief < CLASSIFY_THRESHOLD) {
        return STATE_NORMAL;
    }

    return best;
}

/* ---------- Actuator Mapping ---------- */

ActuatorCommand ds_get_action(ExcretionState state)
{
    ActuatorCommand cmd = { 0, 0, 0, 0, 0 };

    switch (state) {
    case STATE_URINE:
        cmd.suction_pump = 1;
        cmd.water_pump   = 1;
        cmd.heater       = 1;
        cmd.fan          = 1;
        cmd.duration_sec = 120; /* 2 minutes */
        break;

    case STATE_FECES:
        cmd.suction_pump = 1;
        cmd.water_pump   = 1;
        cmd.heater       = 1;
        cmd.fan          = 1;
        cmd.duration_sec = 240; /* 4 minutes (extended cycle) */
        break;

    case STATE_NORMAL:
    default:
        cmd.duration_sec = 0;
        break;
    }

    return cmd;
}
