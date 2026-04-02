"""
Experiment 1: Zeta-Regularized Vacuum Energy in Warp Geometries
================================================================

The Casimir effect is the ONLY experimentally verified mechanism for
producing negative energy density. Its calculation relies on zeta
function regularization — a technique from analytic number theory.

We compute:
1. Standard Casimir energy between parallel plates (textbook verification)
2. Casimir energy for SPHERICAL geometry (warp bubble prototype)
3. Casimir energy for the Alcubierre warp bubble shape function
4. Comparison with Pfenning-Ford energy requirements

Key insight: The sign of the Casimir energy depends on GEOMETRY and
TOPOLOGY. Some geometries naturally produce negative energy, others
positive. The warp bubble is a specific geometry whose Casimir energy
we can compute.

References:
  [1] Casimir, Proc. K. Ned. Akad. Wet. 51 (1948), 793-795
  [2] Alcubierre, Class. Quantum Grav. 11 (1994), L73-L77
  [3] Pfenning & Ford, Class. Quantum Grav. 14 (1997), 1743-1751
  [4] Boyer, Phys. Rev. 174 (1968), 1764-1774 (spherical Casimir)
  [5] Bordag et al., "Advances in the Casimir Effect" (2009)

Wright Brothers, 2026
"""

import numpy as np
from scipy.special import zeta as scipy_zeta
from scipy.integrate import quad
import matplotlib.pyplot as plt

# Physical constants (SI)
hbar = 1.054571817e-34   # J·s
c = 2.99792458e8          # m/s
G = 6.67430e-11           # m³/(kg·s²)
pi = np.pi

# Planck units
l_P = np.sqrt(hbar * G / c**3)  # ~1.616e-35 m
t_P = l_P / c                   # ~5.391e-44 s
E_P = np.sqrt(hbar * c**5 / G)  # ~1.956e9 J
rho_P = E_P / (l_P**3 * c**2)   # Planck energy density ~4.63e113 J/m³

print("=" * 70)
print("  EXPERIMENT 1: ZETA-REGULARIZED VACUUM ENERGY IN WARP GEOMETRIES")
print("=" * 70)

# ============================================================================
#  PART 1: Parallel Plate Casimir Energy (Textbook Verification)
# ============================================================================

print("\n--- PART 1: Parallel Plate Casimir Energy ---")
print()

def casimir_energy_density_plates(d):
    """Casimir energy density between parallel plates at separation d.
    E/A = -π² ℏc / (720 d³)
    This is NEGATIVE — the standard Casimir effect produces negative energy."""
    return -pi**2 * hbar * c / (720 * d**3)

def casimir_pressure_plates(d):
    """Casimir pressure (force per area) between plates.
    F/A = -π² ℏc / (240 d⁴)"""
    return -pi**2 * hbar * c / (240 * d**4)

# The -1/12 connection:
# The regularized sum Σn = ζ(-1) = -1/12 appears in the derivation:
# E = (ℏc/2) Σ_n (nπ/d) × Area  →  zeta-regularize Σn → -1/12
# This gives E/A = -π²ℏc/(6·(2d)³) × 2 × (-1/12) = ... = -π²ℏc/720d³

print("  The Casimir energy density between parallel plates:")
print(f"  E/A/d = -π²ℏc/(720 d³)")
print()
print(f"  Zeta regularization: Σ n = ζ(-1) = -1/12 = {-1/12:.6f}")
print(f"  (This is the famous  1+2+3+4+... = -1/12)")
print()

for d in [1e-6, 1e-7, 1e-8, 1e-9]:
    E = casimir_energy_density_plates(d)
    print(f"  d = {d:.0e} m:  E/A = {E:.3e} J/m²  ({E/E_P:.3e} E_P/m²)")

# ============================================================================
#  PART 2: Spherical Casimir Energy (Boyer, 1968)
# ============================================================================

print("\n--- PART 2: Spherical Casimir Energy ---")
print()
print("  SURPRISE: The Casimir energy of a spherical shell is POSITIVE!")
print("  (Boyer, 1968). This is the opposite sign from parallel plates.")
print()

def casimir_energy_sphere(R):
    """Casimir energy of a perfectly conducting spherical shell of radius R.
    E = +0.04618 ℏc/R  (Boyer's result)
    POSITIVE — repulsive, opposite to plates!"""
    return 0.04618 * hbar * c / R

for R in [1e-6, 1e-7, 1e-8, 1e-9]:
    E = casimir_energy_sphere(R)
    print(f"  R = {R:.0e} m:  E = {E:+.3e} J  (POSITIVE)")

print()
print("  Lesson: The SIGN of Casimir energy depends on GEOMETRY.")
print("  Parallel plates → negative. Sphere → positive.")
print("  A warp bubble has its own geometry → its own sign.")

# ============================================================================
#  PART 3: Warp Bubble Geometry and Energy
# ============================================================================

print("\n--- PART 3: Alcubierre Warp Bubble ---")
print()

def alcubierre_f(r, R, sigma):
    """Alcubierre shape function.
    f(r) = (tanh(σ(r+R)) - tanh(σ(r-R))) / (2·tanh(σR))
    f ≈ 1 inside bubble (r < R), f ≈ 0 outside (r > R).
    σ controls wall thickness: larger σ = thinner wall."""
    return (np.tanh(sigma * (r + R)) - np.tanh(sigma * (r - R))) / \
           (2 * np.tanh(sigma * R))

def warp_energy_density(r, R, sigma, v_s):
    """Energy density required by Alcubierre metric.
    ρ = -(v_s²)/(32πG) · (df/dr)² · (y²+z²)/r_s²
    For spherical symmetry, averaged over angles:
    <ρ> = -(v_s²)/(32πG) · (df/dr)² · (2/3)

    This is ALWAYS NEGATIVE — violates weak energy condition."""
    dr = R * 1e-4
    dfdr = (alcubierre_f(r + dr, R, sigma) - alcubierre_f(r - dr, R, sigma)) / (2 * dr)
    return -(v_s**2) / (32 * pi * G) * dfdr**2 * (2/3)

# Warp bubble parameters
R_bubble = 50.0       # bubble radius [m] (room for a vehicle)
sigma = 1.0 / 5.0     # wall thickness parameter [1/m] (wall ~ 5m thick)
v_s = 1.0 * c         # bubble velocity = 1c

# Compute energy density profile
r_arr = np.linspace(0.01, 3 * R_bubble, 1000)
rho_arr = np.array([warp_energy_density(r, R_bubble, sigma, v_s) for r in r_arr])
f_arr = np.array([alcubierre_f(r, R_bubble, sigma) for r in r_arr])

# Total energy (volume integral)
# E = ∫ ρ · 4πr² dr  (spherical shell integration)
E_total = np.trapezoid(rho_arr * 4 * pi * r_arr**2, r_arr)

# Convert to solar masses
M_sun = 1.989e30  # kg
E_solar = M_sun * c**2

print(f"  Bubble radius R = {R_bubble} m")
print(f"  Wall thickness ~ {1/sigma:.0f} m")
print(f"  Bubble velocity v_s = {v_s/c:.1f} c")
print()
print(f"  Peak negative energy density: {np.min(rho_arr):.3e} J/m³")
print(f"  Total energy required: {E_total:.3e} J")
print(f"                       = {E_total / E_solar:.3e} solar masses × c²")
print(f"                       = {abs(E_total / E_solar):.1f} solar masses of NEGATIVE energy")

# ============================================================================
#  PART 4: Zeta Regularization Analysis
# ============================================================================

print("\n--- PART 4: Zeta Regularization of Warp Bubble Vacuum ---")
print()

# The Casimir energy in curved spacetime uses the DeWitt-Schwinger expansion.
# For a massless scalar field, the regularized vacuum energy involves:
#
#   E_vac = (ℏc/2) Σ_n ω_n  →  zeta regularized to  (ℏc/2) ζ_bubble(-1)
#
# where ζ_bubble(s) = Σ_n ω_n^{-s} is the spectral zeta function of the
# Laplacian on the warp bubble geometry.
#
# For a general geometry, the zeta function encodes:
#   ζ_bubble(s) = Tr((-Δ_bubble)^{-s})
#
# The heat kernel expansion gives:
#   ζ_bubble(s) ~ (4π)^{-d/2} Σ_k a_k / (s - d/2 + k)
#
# where a_k are the Seeley-DeWitt coefficients that depend on curvature.

# For the warp bubble, the key curvature invariant is the Kretschner scalar:
# K = R_{μνρσ} R^{μνρσ}

def kretschner_warp(r, R, sigma, v_s):
    """Estimate of Kretschner scalar for Alcubierre metric.
    K ~ (v_s/c)^4 · (d²f/dr²)² + lower order terms.
    This is a rough estimate; the full computation needs the Riemann tensor."""
    dr = R * 1e-4
    f_p = alcubierre_f(r + dr, R, sigma)
    f_0 = alcubierre_f(r, R, sigma)
    f_m = alcubierre_f(r - dr, R, sigma)
    d2fdr2 = (f_p - 2 * f_0 + f_m) / dr**2
    return (v_s / c)**4 * d2fdr2**2

K_arr = np.array([kretschner_warp(r, R_bubble, sigma, v_s) for r in r_arr])

# The first Seeley-DeWitt coefficient a_1 ~ ∫ R · √g d⁴x (Ricci scalar)
# The second a_2 ~ ∫ (R² + K) · √g d⁴x (includes Kretschner)

# Casimir energy from Seeley-DeWitt:
# E_Casimir ~ (ℏc)/(16π²) · ∫ K^{1/2} / L³ d³x
# where L is the characteristic length scale (wall thickness ~ 1/σ)

L_wall = 1.0 / sigma
casimir_estimate = (hbar * c) / (16 * pi**2) * \
    np.trapezoid(np.sqrt(np.abs(K_arr)) / L_wall**3 * 4 * pi * r_arr**2, r_arr)

print("  Seeley-DeWitt expansion of vacuum energy:")
print(f"  Kretschner scalar peak: {np.max(K_arr):.3e} m⁻⁴")
print(f"  Wall thickness L = {L_wall:.1f} m")
print(f"  Estimated Casimir energy from curvature: {casimir_estimate:.3e} J")
print()
print(f"  Required negative energy:  {abs(E_total):.3e} J")
print(f"  Casimir contribution:      {casimir_estimate:.3e} J")
print(f"  Ratio (Casimir / Required): {casimir_estimate / abs(E_total):.3e}")
print()

if casimir_estimate / abs(E_total) < 1e-10:
    print("  RESULT: Casimir energy is negligible compared to requirements.")
    print("  Standard zeta regularization does NOT close the gap.")
    print()
    print("  BUT: This calculation uses the REAL zeta function only.")
    print("  The adelic product formula suggests p-adic corrections:")
    print("    E_total = E_∞ · ∏_p E_p")
    print("  If the p-adic factors contribute, the balance changes.")
    print("  → This motivates Experiment 2 (p-adic Alcubierre metric).")

# ============================================================================
#  PART 5: The Key Numbers
# ============================================================================

print("\n--- PART 5: Summary of Key Numbers ---")
print()
print("  Standard Alcubierre requirements (R=50m, v=c, wall=5m):")
print(f"    Negative energy: {abs(E_total/E_solar):.1f} solar masses × c²")
print()
print("  Thinner wall (σ=10, wall=0.1m):")
sigma_thin = 10.0
E_thin = np.trapezoid(
    [warp_energy_density(r, R_bubble, sigma_thin, v_s) * 4*pi*r**2 for r in r_arr], r_arr)
print(f"    Negative energy: {abs(E_thin/E_solar):.1e} solar masses × c²")
print()
print("  Lentz soliton (2021): claims positive energy solutions exist")
print("  Bobrick-Martire (2021): subluminal positive-energy warp possible")
print()
print("  Zeta regularization:")
print(f"    ζ(-1) = -1/12  = {-1/12:.6f}")
print(f"    ζ(-3) = 1/120 = {1/120:.6f}")
print(f"    ζ(0)  = -1/2  = {-1/2:.6f}")
print()
print("  These values appear in ALL vacuum energy calculations.")
print("  They are NOT arbitrary — they are fixed by the Riemann zeta function.")
print("  If spacetime is Spec(Z), these values are determined by")
print("  the arithmetic structure of spacetime itself.")

# ============================================================================
#  PART 6: Visualization
# ============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.patch.set_facecolor('#0a0a1a')
fig.suptitle('Warp Bubble Vacuum Energy Analysis', fontsize=14,
             fontweight='bold', color='white')

# Panel 1: Shape function
ax = axes[0, 0]
for sig, col in [(0.1, '#ffd93d'), (0.2, '#00d4ff'), (1.0, '#ff6b6b')]:
    f_plot = [alcubierre_f(r, R_bubble, sig) for r in r_arr]
    ax.plot(r_arr, f_plot, color=col, linewidth=2,
            label=f'wall ~ {1/sig:.0f}m')
ax.set_xlabel('r [m]', color='white')
ax.set_ylabel('f(r)', color='white')
ax.set_title('Alcubierre Shape Function', color='white')
ax.legend(fontsize=9)
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.15)

# Panel 2: Energy density
ax = axes[0, 1]
ax.plot(r_arr, rho_arr, color='#ff6b6b', linewidth=2)
ax.axhline(y=0, color='white', linewidth=0.5, alpha=0.3)
ax.set_xlabel('r [m]', color='white')
ax.set_ylabel('Energy density [J/m³]', color='white')
ax.set_title('Required Energy Density (NEGATIVE)', color='white')
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.15)

# Panel 3: Kretschner scalar
ax = axes[1, 0]
ax.plot(r_arr, K_arr, color='#ffd93d', linewidth=2)
ax.set_xlabel('r [m]', color='white')
ax.set_ylabel('Kretschner scalar [m⁻⁴]', color='white')
ax.set_title('Curvature of Warp Bubble', color='white')
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.15)

# Panel 4: Energy scale comparison
ax = axes[1, 1]
labels = ['Required\n(Alcubierre)', 'Casimir\n(curvature)', 'Casimir\n(1nm plates)', 'Planck\nenergy']
values = [abs(E_total), casimir_estimate, abs(casimir_energy_density_plates(1e-9) * 1e-9), E_P]
colors = ['#ff6b6b', '#00d4ff', '#6bff8d', '#ffd93d']
ax.bar(range(len(labels)), np.log10(np.array(values) + 1e-300), color=colors, alpha=0.8)
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, fontsize=8, color='white')
ax.set_ylabel('log₁₀(Energy [J])', color='white')
ax.set_title('Energy Scale Comparison', color='white')
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.15)

plt.tight_layout()
plt.savefig('research/04_warp_drive/warp_vacuum_energy.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
plt.close()

print(f"\n  Plot saved: research/04_warp_drive/warp_vacuum_energy.png")
