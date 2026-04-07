#!/usr/bin/env python3
"""
Quantum Critical Enhancement of the Casimir Effect:
Can we detect G_eff = -G without Euler product amplification?

The key: near a quantum critical point (QCP), the Casimir effect
is AMPLIFIED by (ξ/d)^Δ where ξ = correlation length (divergent).
This is PASSIVE (just temperature control) and SAFE (no prime muting).
"""

import numpy as np

hbar = 1.055e-34
c = 3e8
kB = 1.381e-23
G_N = 6.674e-11
pi = np.pi

print("=" * 70)
print("QUANTUM CRITICAL CASIMIR ENHANCEMENT: DEEP DIVE")
print("=" * 70)

# =====================================================================
print("\n" + "=" * 70)
print("1. THE CRITICAL CASIMIR EFFECT — ESTABLISHED PHYSICS")
print("=" * 70)

print("""
The CRITICAL CASIMIR EFFECT is a well-established phenomenon
(predicted: Fisher & de Gennes 1978, observed: Hertlein et al. 2008).

Near a continuous phase transition at T_c:
  Correlation length: ξ(T) = ξ₀ / |1 - T/T_c|^ν
  where ν is the correlation length exponent.

The Casimir force between two surfaces at distance d:
  F_Cas = (kT/d³) × θ(d/ξ)

  Far from T_c (ξ << d): θ → exponentially small
  Near T_c (ξ >> d): θ → universal constant × (ξ/d)^Δ

  Δ = critical exponent for the Casimir amplitude.

THIS IS EXPERIMENTALLY VERIFIED:
  Hertlein et al. (Nature 2008): measured critical Casimir
  force near the demixing transition of a binary liquid.
  Force enhanced by factor ~100 compared to QED Casimir.
""")

# =====================================================================
print("=" * 70)
print("2. APPLICATION TO π-JUNCTION SUPERCONDUCTOR")
print("=" * 70)

print("""
For a superconductor (Nb) near T_c = 9.3 K:
  ξ(T) = ξ₀ / √(1 - T/T_c)    (mean-field, ν = 1/2)
  ξ₀(Nb) ≈ 38 nm (BCS coherence length)

The superconducting transition is mean-field (ν = 1/2, Δ = 3/2):
  Critical Casimir force: F ~ (kT/d²) × (ξ/d)^{3/2}  for ξ >> d

For the π-junction: both the Casimir effect AND the π-Berry
phase are controlled by the same superconducting transition.
  T > T_c: normal state, no π-shift, standard Casimir
  T < T_c: superconducting, π-shift ON, modified Casimir
  T ≈ T_c: ENHANCED Casimir (critical fluctuations)
""")

xi_0 = 38e-9  # Nb coherence length
T_c = 9.3  # K

print("Critical Casimir enhancement near Nb T_c:")
print(f"{'T/T_c':>10} {'1-T/T_c':>10} {'ξ (μm)':>10} {'ξ/d (d=100nm)':>14} "
      f"{'enhancement':>12} {'ΔM/M':>12}")
print("-" * 72)

d = 100e-9  # 100 nm gap
rho_Nb = 8900
base_dM_M = hbar * pi**2 / (720 * c * rho_Nb * d**3 * (d + 300e-9))

for T_frac in [0.9, 0.99, 0.999, 0.9999, 0.99999, 0.999999]:
    xi = xi_0 / np.sqrt(1 - T_frac)
    xi_d = xi / d
    if xi_d > 1:
        # Mean-field critical Casimir: enhancement ~ (ξ/d)^{3/2}
        enh = xi_d ** 1.5
    else:
        enh = 1.0

    dM_M = base_dM_M * enh
    T_actual = T_c * T_frac

    print(f"{T_frac:>10.6f} {1-T_frac:>10.1e} {xi*1e6:>10.2f} "
          f"{xi_d:>14.1f} {enh:>12.0f} {dM_M:>12.2e}")

print()

# =====================================================================
print("=" * 70)
print("3. ★★★ WHAT LIMITS THE ENHANCEMENT? ★★★")
print("=" * 70)

print("""
Three physical limits on the critical enhancement:

LIMIT 1: Temperature stability
  At T/T_c = 0.9999: need ΔT < T_c × 10⁻⁴ = 0.93 mK
  At T/T_c = 0.99999: need ΔT < 0.093 mK
  Modern dilution fridges: stability ~ 0.01 mK → OK to 10⁻⁵
""")

for T_frac in [0.999, 0.9999, 0.99999, 0.999999]:
    dT = T_c * (1 - T_frac)
    print(f"  T/T_c = {T_frac}: need stability < {dT*1e3:.2f} mK")

print("""
LIMIT 2: Finite-size effects
  The sample must be larger than ξ for criticality to hold.
  At T/T_c = 0.9999: ξ ≈ 4 μm → sample must be >> 4 μm
  Typical BAW crystal: mm scale → OK up to ξ ~ 100 μm

LIMIT 3: Time scale of fluctuations
  Critical slowing down: τ_relax ~ ξ^z (z = dynamic exponent)
  For superconductors: z ≈ 2
  At ξ = 4 μm: τ ~ (4×10⁻⁶)² / (D_thermal) ~ μs to ms
  Measurement must average over many fluctuation periods.
  With lock-in amplifier at 1 kHz: OK if τ < 1 ms.
""")

# =====================================================================
print("=" * 70)
print("4. ★★★★ OPTIMIZED DEVICE DESIGN ★★★★")
print("=" * 70)

print("""
THE DEVICE: π-junction cavity at quantum criticality

Structure:
  ┌────────────────────────────┐
  │ Nb upper electrode (150nm) │ ← superconductor
  ├────────────────────────────┤
  │ CuNi barrier (2nm)        │ ← π-shift layer
  ├────────────────────────────┤
  │ Nb lower electrode (150nm) │ ← superconductor
  └────────────────────────────┘

  Gap d = CuNi thickness = 2 nm
  π-junction activates at T < T_c = 9.3 K
  Critical enhancement at T ≈ T_c

KEY INSIGHT: The CuNi barrier IS the Casimir gap.
  d = 2 nm is ALREADY built into the junction.
  No separate "cavity" needed.
  The Josephson junction itself is the experiment.
""")

# Compute for optimized device
d_opt = 2e-9  # 2 nm CuNi barrier
t_wall = 150e-9  # Nb electrode thickness

print("OPTIMIZED: d = 2nm (CuNi barrier), t_wall = 150nm (Nb)")
print()

# Base Casimir energy density at d = 2nm
rho_cas_base = pi**2 * hbar * c / (720 * d_opt**4)
print(f"Base Casimir density: ρ_Cas = {rho_cas_base:.2e} J/m³")

# Base ΔM/M
rho_eff = rho_Nb * 2 * t_wall / d_opt  # effective density per gap volume
base_ratio = 2 * rho_cas_base / (c**2 * rho_eff)
print(f"Base ΔM/M (no enhancement): {base_ratio:.2e}")
print()

# With critical enhancement
print("With critical Casimir enhancement:")
print(f"{'T/T_c':>10} {'ξ/d':>8} {'enhancement':>12} {'ΔM/M':>12} {'detectable':>12}")
print("-" * 60)

for T_frac in [0.99, 0.999, 0.9999, 0.99999, 0.999999]:
    xi = xi_0 / np.sqrt(1 - T_frac)
    xi_d = xi / d_opt
    enh = xi_d ** 1.5 if xi_d > 1 else 1.0
    dM_M = base_ratio * enh
    detect = "★ YES" if dM_M > 1e-13 else "no"
    print(f"{T_frac:>10.6f} {xi_d:>8.0f} {enh:>12.0e} {dM_M:>12.2e} {detect:>12}")

print()

# =====================================================================
print("=" * 70)
print("5. ★★★★★ THE ABSOLUTE FORCE CALCULATION ★★★★★")
print("=" * 70)

print("""
The RATIO ΔM/M exceeds Eöt-Wash precision. But does the ABSOLUTE
FORCE exceed the detection threshold (~10⁻¹⁴ N)?
""")

# For a 1cm² junction at d=2nm, with critical enhancement
A = 1e-4  # 1 cm²
M_test = 0.01  # 10 g test mass
r = 1e-3  # 1 mm distance

print(f"Junction area: {A*1e4:.0f} cm²")
print(f"Test mass: {M_test*1e3:.0f} g at r = {r*1e3:.0f} mm")
print()

print(f"{'T/T_c':>10} {'ρ_Cas×enh':>15} {'M_Cas (1cm²)':>15} {'F_grav':>12} {'detect?':>10}")
print("-" * 70)

for T_frac in [0.999, 0.9999, 0.99999, 0.999999]:
    xi = xi_0 / np.sqrt(1 - T_frac)
    xi_d = xi / d_opt
    enh = xi_d ** 1.5 if xi_d > 1 else 1.0

    rho_enhanced = rho_cas_base * enh
    M_cas = rho_enhanced * A * d_opt / c**2
    F = G_N * M_test * 2 * M_cas / r**2
    detect = "★ YES" if F > 1e-14 else "no"

    print(f"{T_frac:>10.6f} {rho_enhanced:>15.2e} {M_cas:>15.2e} {F:>12.2e} {detect:>10}")

print()

# =====================================================================
print("=" * 70)
print("6. SCALING TO DETECTABLE FORCE")
print("=" * 70)

# Need F > 10⁻¹⁴ N
# F = G × M_test × 2M_Cas / r²
# M_Cas = ρ_cas × enh × A × d / c²
# Need A such that F > 10⁻¹⁴

F_target = 1e-14  # N

print("Area needed for F > 10⁻¹⁴ N:")
print()

for T_frac in [0.999, 0.9999, 0.99999, 0.999999]:
    xi = xi_0 / np.sqrt(1 - T_frac)
    enh = (xi / d_opt) ** 1.5

    rho_enh = rho_cas_base * enh
    M_cas_per_area = rho_enh * d_opt / c**2  # kg/m²

    A_needed = F_target * r**2 / (G_N * M_test * 2 * M_cas_per_area)
    print(f"  T/T_c = {T_frac:.6f}: A = {A_needed:.2e} m² = {A_needed*1e4:.2e} cm²")

print()

# Best case: T/T_c = 0.999999
xi_best = xi_0 / np.sqrt(1 - 0.999999)
enh_best = (xi_best / d_opt) ** 1.5
rho_best = rho_cas_base * enh_best
M_cas_per_area_best = rho_best * d_opt / c**2
A_best = F_target * r**2 / (G_N * M_test * 2 * M_cas_per_area_best)

print(f"At T/T_c = 0.999999:")
print(f"  ξ = {xi_best*1e6:.0f} μm, enhancement = {enh_best:.0e}")
print(f"  A needed = {A_best*1e4:.1f} cm²")
print()

if A_best * 1e4 < 100:
    print(f"  ★ {A_best*1e4:.1f} cm² is a STANDARD Josephson junction size!")
    print(f"  This is a SINGLE CHIP fabrication. Feasible!")
elif A_best * 1e4 < 1e6:
    print(f"  A wafer-scale ({A_best*1e4:.0e} cm²) fabrication. Challenging but possible.")
else:
    print(f"  Not feasible ({A_best*1e4:.0e} cm² needed).")

# =====================================================================
print("\n" + "=" * 70)
print("7. ★★★★★ THE CRITICAL CASIMIR π-JUNCTION EXPERIMENT ★★★★★")
print("=" * 70)

print("""
EXPERIMENT DESIGN (revised Phase 3):

Instead of Euler product amplification (safety issues),
use CRITICAL CASIMIR ENHANCEMENT (safe, passive, established).

Device: Large-area Nb/CuNi/Nb π-Josephson junction
  Area: ~10 cm² (wafer-scale, standard fabrication)
  Gap: d = 2 nm (CuNi barrier, built into junction)
  Temperature: T = 0.999999 T_c = 9.2999907 K (stability: 0.01 mK)

Measurement:
  1. Torsion balance with laser readout (nm precision)
  2. Junction mounted on cryostat cold finger
  3. Test mass (10g brass) at 1mm distance
  4. Temperature sweep across T_c
  5. Record force change at T_c transition

Expected signal:
""")

A_exp = 10e-4  # 10 cm²
T_frac_exp = 0.999999
xi_exp = xi_0 / np.sqrt(1 - T_frac_exp)
enh_exp = (xi_exp / d_opt) ** 1.5
rho_exp = rho_cas_base * enh_exp
M_cas_exp = rho_exp * A_exp * d_opt / c**2
F_exp = G_N * M_test * 2 * M_cas_exp / r**2

print(f"  ξ = {xi_exp*1e6:.0f} μm")
print(f"  Enhancement: {enh_exp:.1e}×")
print(f"  ρ_Cas (enhanced): {rho_exp:.1e} J/m³")
print(f"  M_Cas (10 cm²): {M_cas_exp:.1e} kg")
print(f"  Gravitational force: {F_exp:.1e} N")
print(f"  Detection threshold: 10⁻¹⁴ N")
print(f"  Signal/threshold: {F_exp/1e-14:.0f}×")
print()

if F_exp > 1e-14:
    print("  ★★★ SIGNAL EXCEEDS DETECTION THRESHOLD! ★★★")
    print()
    print("  NO Euler product amplification needed.")
    print("  NO safety concerns.")
    print("  Uses ESTABLISHED physics (critical Casimir effect).")
    print("  STANDARD fabrication (Josephson junction wafer).")
else:
    print("  Signal below threshold. Need larger area or closer distance.")

print(f"""
COST ESTIMATE:
  Large-area π-junction wafer:      ¥300,000 (foundry)
  Dilution fridge (shared/rented):  ¥0-500,000
  Torsion balance + optics:         ¥300,000
  Cryogenic vibration isolation:    ¥200,000
  Total:                            ¥800,000-1,300,000

COMPARED TO:
  Euler product approach: ¥1,130,000 + SAFETY RISK
  QCP approach:           ¥800,000-1,300,000, NO safety risk

TIMELINE:
  Fabrication: 2-3 months
  Setup: 1-2 months
  Measurement: 2-3 months
  Total: 6-8 months
""")

# =====================================================================
print("=" * 70)
print("8. HONEST CAVEATS")
print("=" * 70)

print("""
1. The critical Casimir enhancement (ξ/d)^{3/2} is established
   for CLASSICAL critical points (binary liquids, etc.).
   For SUPERCONDUCTING transitions, the same scaling is expected
   (mean-field universality) but NOT directly measured for the
   π-junction geometry.

2. T/T_c = 0.999999 requires ΔT < 0.01 mK stability.
   This is at the EDGE of dilution fridge capability.
   More realistic: T/T_c = 0.99999 (ΔT < 0.1 mK),
   which gives 10× less enhancement.

3. The π-Berry phase effect on the critical Casimir force
   is a PREDICTION of our framework, not established physics.
   Standard critical Casimir (without π-phase) would give
   an enhanced ATTRACTIVE force, not repulsive.
   The SIGN of the enhanced force is what we need to measure.

4. Vibration isolation at mK temperatures is challenging.
   The torsion balance must be in vacuum AND cooled,
   which creates competing requirements.

5. The 2nm CuNi barrier may not be a clean Casimir cavity.
   Disorder, interdiffusion, and magnetic domains in CuNi
   can modify the effective gap and boundary conditions.

MITIGATION:
  - Start with T/T_c = 0.9999 (easier, ΔT ~ 1 mK)
  - Measure the SIGN of force change at T_c
  - If sign is wrong (attractive enhanced): framework falsified
  - If sign is right (repulsive or reduced attractive): proceed closer to T_c
""")
