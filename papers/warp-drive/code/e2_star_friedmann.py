#!/usr/bin/env python3
"""
E2* Friedmann solver: V(τ) = Ω_Λ + C × |E₂*(τ)|²/y²
E₂*(i) = 0 → minimum at τ=i → w≈-1 naturally.
Precompute E₂* on grid for speed.
"""

import numpy as np
from scipy.integrate import solve_ivp
from scipy.interpolate import CubicSpline
from scipy.optimize import minimize

pi = np.pi
OmL0 = 2*pi/9      # 0.6981
Om_m0 = 1 - OmL0   # 0.3019

# =====================================================================
# 1. Precompute E₂*(iy) on a fine grid
# =====================================================================

# Cache σ₁(n)
MAX_N = 300
sig1 = [0]*(MAX_N+1)
for n in range(1, MAX_N+1):
    sig1[n] = sum(d for d in range(1, n+1) if n % d == 0)

def E2_holomorphic(y):
    """E₂(iy) = 1 - 24 Σ σ₁(n) e^{-2πny}"""
    val = 1.0
    for n in range(1, MAX_N+1):
        qn = np.exp(-2*pi*n*y)
        if qn < 1e-30:
            break
        val -= 24 * sig1[n] * qn
    return val

def E2_star_val(y):
    """E₂*(iy) = E₂(iy) - 3/(πy)"""
    return E2_holomorphic(y) - 3.0/(pi*y)

# Build spline on [0.85, 15]
print("Precomputing E₂* grid...", flush=True)
y_grid = np.unique(np.concatenate([
    np.linspace(0.85, 1.3, 200),
    np.linspace(1.301, 3.0, 100),
    np.linspace(3.01, 15.0, 50)
]))
E2s_grid = np.array([E2_star_val(y) for y in y_grid])
V_mod_grid = E2s_grid**2 / y_grid**2  # |E₂*|²/y²

E2s_spline = CubicSpline(y_grid, E2s_grid)
Vmod_spline = CubicSpline(y_grid, V_mod_grid)
dVmod_spline = Vmod_spline.derivative()

print("Done. E₂*(1.0) =", E2s_spline(1.0), flush=True)

# =====================================================================
# 2. The potential: V(y) = Ω_Λ + C × |E₂*|²/y²
# =====================================================================

def V_total(y, C):
    y = np.clip(y, 0.85, 15.0)
    return OmL0 + C * float(Vmod_spline(y))

def dV_total(y, C):
    y = np.clip(y, 0.85, 15.0)
    return C * float(dVmod_spline(y))

# Show the potential
print("\nPotential V(y) = Ω_Λ + C×|E₂*|²/y² for C=0.5:")
print(f"{'y':>6} {'E2*':>10} {'|E2*|²/y²':>12} {'V (C=0.5)':>10} {'V/Ω_Λ':>8}")
print("-" * 50)
for y in [0.87, 0.9, 0.95, 0.99, 1.0, 1.01, 1.05, 1.1, 1.2, 1.5, 2.0, 3.0, 5.0]:
    e = float(E2s_spline(y))
    vm = float(Vmod_spline(y))
    vt = OmL0 + 0.5 * vm
    print(f"{y:>6.3f} {e:>10.6f} {vm:>12.6f} {vt:>10.4f} {vt/OmL0:>8.4f}")

# =====================================================================
# 3. Friedmann + Klein-Gordon
# =====================================================================

def friedmann_rhs(N, state, C):
    y, ydot = state
    y = np.clip(y, 0.86, 14.0)

    V = V_total(y, C)
    dVdy = dV_total(y, C)
    K = 1.0 / y**2  # Petersson metric

    rho_m = Om_m0 * np.exp(-3*N)

    # H² = (ρ_m + V) / (1 - K ẏ²/2)
    kinetic_frac = 0.5 * K * ydot**2
    if kinetic_frac > 0.95:
        kinetic_frac = 0.95
    denom = 1.0 - kinetic_frac
    H2 = (rho_m + V) / denom
    if H2 < 1e-12:
        H2 = 1e-12

    # Friction: 3 + (1/2) d(ln H²)/dN
    # d(ln H²)/dN ≈ -3 ρ_m / (H² × denom) (matter dilution)
    dlnH2 = -3.0 * rho_m / (H2 * denom)
    friction = 3.0 + 0.5 * dlnH2

    yddot = -friction * ydot - dVdy / (K * H2)
    return [ydot, yddot]

def compute_w(y, ydot, C, z):
    y = np.clip(y, 0.86, 14.0)
    V = V_total(y, C)
    K = 1.0/y**2
    rm = Om_m0 * (1+z)**3
    kf = 1.0 - min(0.95, 0.5*K*ydot**2)
    H2 = max(1e-12, (rm+V)/kf)
    KE = 0.5 * K * ydot**2 * H2
    denom = KE + V
    if denom < 1e-15:
        return -1.0
    return (KE - V) / denom

def compute_OmDE(y, ydot, C, z):
    V = V_total(np.clip(y,0.86,14), C)
    K = 1.0/max(y,0.86)**2
    rm = Om_m0*(1+z)**3
    kf = 1.0 - min(0.95, 0.5*K*ydot**2)
    H2 = max(1e-12, (rm+V)/kf)
    KE = 0.5*K*ydot**2*H2
    return (KE+V)/H2

# =====================================================================
# 4. Grid scan over (C, ẏ₀)
# =====================================================================

print("\n" + "="*70)
print("GRID SCAN: (C, ẏ₀) → (w₀, w_a)")
print("="*70)
print(f"{'C':>6} {'ẏ₀':>8} {'w₀':>8} {'w(0.3)':>8} {'w(0.5)':>8} {'w(1)':>8} {'w_a':>8}")
print("-" * 60)

results = []

for C in [0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0]:
    for yd0 in np.arange(-0.02, -0.5, -0.02):
        try:
            sol = solve_ivp(friedmann_rhs, [0, -1.5], [1.0, yd0],
                           args=(C,), max_step=0.02, method='RK45',
                           dense_output=True, rtol=1e-8, atol=1e-10)
            if not sol.success:
                continue

            w0 = compute_w(1.0, yd0, C, 0)

            # w at z=0.3
            st03 = sol.sol(-np.log(1.3))
            w03 = compute_w(st03[0], st03[1], C, 0.3)

            # w at z=0.5
            st05 = sol.sol(-np.log(1.5))
            w05 = compute_w(st05[0], st05[1], C, 0.5)

            # w at z=1.0
            st1 = sol.sol(-np.log(2.0))
            w1 = compute_w(st1[0], st1[1], C, 1.0)

            # Effective w_a from z=0 and z=0.5
            wa = -(w05 - w0) / (0.5/1.5)

            # Selection: w₀ near -0.83, w decreasing with z
            if -0.95 < w0 < -0.70 and w05 < w0 and w1 < w05:
                score = (w0 - (-0.83))**2 + (wa - (-0.75))**2
                results.append((score, C, yd0, w0, w03, w05, w1, wa, sol))
                if len(results) % 5 == 0 or score < 0.01:
                    print(f"{C:>6.1f} {yd0:>8.2f} {w0:>8.3f} {w03:>8.3f} {w05:>8.3f} {w1:>8.3f} {wa:>8.3f}")
        except Exception:
            pass

results.sort(key=lambda x: x[0])

# =====================================================================
# 5. Best fit analysis
# =====================================================================

print("\n" + "="*70)
print("★★★ BEST FIT RESULTS ★★★")
print("="*70)

if len(results) > 0:
    score, C_best, yd_best, w0_b, w03_b, w05_b, w1_b, wa_b, sol_best = results[0]

    print(f"\nBest fit: C = {C_best:.2f}, ẏ₀ = {yd_best:.3f}")
    print(f"  w₀ = {w0_b:.4f}  (DESI: -0.83)")
    print(f"  w_a = {wa_b:.4f}  (DESI: -0.75)")
    print(f"  w₀ error: {abs(w0_b-(-0.83))/0.83*100:.1f}%")
    print(f"  w_a error: {abs(wa_b-(-0.75))/0.75*100:.1f}%")
    print()

    # Full w(z) curve
    print("Full w(z) and Ω_DE(z):")
    print(f"{'z':>6} {'y':>8} {'w':>8} {'Ω_DE':>8}")
    print("-" * 35)

    for z in [0, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]:
        N = -np.log(1+z)
        if N < sol_best.t[-1]:
            continue
        st = sol_best.sol(N)
        w = compute_w(st[0], st[1], C_best, z)
        OmDE = compute_OmDE(st[0], st[1], C_best, z)
        print(f"{z:>6.2f} {st[0]:>8.4f} {w:>8.4f} {OmDE:>8.4f}")

    # Compare with DESI w₀w_aCDM
    print(f"\n{'':>6} {'This model':>12} {'DESI w₀w_a':>12} {'ΛCDM':>8}")
    print("-" * 42)
    print(f"{'w₀':>6} {w0_b:>12.3f} {-0.83:>12.3f} {-1.0:>8.3f}")
    print(f"{'w_a':>6} {wa_b:>12.3f} {-0.75:>12.3f} {0.0:>8.3f}")
    print(f"{'Ω_Λ':>6} {'2π/9':>12} {'fitted':>12} {'fitted':>8}")
    print(f"{'params':>6} {'2 (C,ẏ₀)':>12} {'3 (Ω,w₀,wa)':>12} {'1 (Ω)':>8}")

    # Show top 5
    if len(results) > 1:
        print("\nTop 5 fits:")
        for i, (sc, C, yd, w0, w03, w05, w1, wa, _) in enumerate(results[:5]):
            print(f"  #{i+1}: C={C:.2f} ẏ₀={yd:.3f} w₀={w0:.3f} w_a={wa:.3f} score={sc:.4f}")
else:
    print("\nNo satisfactory fits found.")
    print("The potential may need a different normalization or kinetic term.")

print("\n" + "="*70)
print("HONEST ASSESSMENT")
print("="*70)
print(f"""
WHAT IS DERIVED:
  ✓ V(τ) = Ω_Λ + C × |E₂*(τ)|²/y²
  ✓ E₂*(i) = 0 (exact) → w = -1 at τ=i (natural, no tuning)
  ✓ V is harmonic near τ=i → w deviations are naturally small
  ✓ Ω_Λ = 2π/9 (parameter-free from BC)

FREE PARAMETERS: 2
  C = coupling strength of CM modulation
  ẏ₀ = current rolling speed (sets w₀)

COMPARE:
  w₀w_aCDM: 3 free params (Ω_Λ, w₀, w_a)
  This model: 2 free params (C, ẏ₀) + Ω_Λ fixed = 2π/9
  ΛCDM: 1 free param (Ω_Λ) but w=-1 exactly (DESI tension)
""")
