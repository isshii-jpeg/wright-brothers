"""
Numerical verification: Dynamical Casimir Effect (DCE) + Prime Muting
======================================================================

Question: Can we combine DCE with prime-muting boundary conditions to amplify
the repulsive Casimir force enough to lift a macroscopic object against gravity?

Strategy
--------
1. Compute the static prime-muted Casimir force on parallel plates as a function
   of gap L. Prime muting modifies the zeta-regularized mode sum by a factor
   prod_{p in S}(1 - p^3). Odd |S| flips the sign (repulsive).
2. Compute DCE photon production in a parametrically driven cavity (one wall
   modulated at omega_d = 2*omega_n0, n0 = lowest allowed mode in the muted set).
   Use the standard parametric oscillator equation with cavity loss kappa = omega/Q
   and saturation at a critical photon number n_crit (set by Kerr nonlinearity).
3. Convert steady-state photon number to radiation pressure on the cavity walls.
4. Sum static + DCE forces, compare to gravitational weight of the movable plate.
5. Sweep over (L, Q, epsilon) and identify the antigravity-capable region.

All physics is written explicitly so each step can be audited.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ----------------------------------------------------------------------------
# Physical constants (SI)
# ----------------------------------------------------------------------------
hbar = 1.054_571_817e-34   # J s
c    = 2.997_924_58e8      # m / s
g0   = 9.806_65            # m / s^2
kB   = 1.380_649e-23       # J / K

# ----------------------------------------------------------------------------
# Movable plate (the object we want to levitate)
# ----------------------------------------------------------------------------
A_plate     = 1e-4         # 1 cm^2
t_plate     = 1e-6         # 1 micron thick
rho_plate   = 2330.0       # silicon kg/m^3
M_plate     = rho_plate * A_plate * t_plate
W_plate     = M_plate * g0    # weight in Newton

# ----------------------------------------------------------------------------
# Prime-muting amplification factor
# ----------------------------------------------------------------------------
def mute_factor(primes):
    """zeta_{!S}(-3) / zeta(-3) = prod_{p in S}(1 - p^3).
    Odd |S| -> negative -> sign flips Casimir from attractive to repulsive."""
    f = 1
    for p in primes:
        f *= (1 - p**3)
    return f

# ----------------------------------------------------------------------------
# Static Casimir force on parallel plates (per unit area)
# ----------------------------------------------------------------------------
def P_casimir_static(L, primes=()):
    """Force per area, sign convention: negative = attractive (pull plates together).
    Prime muting modifies by prod (1 - p^3); odd |S| -> repulsive (positive)."""
    P0 = -(np.pi**2 * hbar * c) / (240 * L**4)   # standard Casimir pressure
    return P0 * mute_factor(primes)

# ----------------------------------------------------------------------------
# DCE: parametric photon production in driven cavity
# ----------------------------------------------------------------------------
def lowest_allowed_mode(primes):
    """First positive integer not divisible by any p in S (i.e., gcd(n,p)=1 for all p in S)."""
    n = 1
    while True:
        if all(n % p != 0 for p in primes):
            return n
        n += 1

def dce_photon_number(L, Q, epsilon, primes=(), n_crit=1e6):
    """Steady-state photon number in the driven cavity.

    Drive at omega_d = 2*omega_{n0} where n0 = lowest allowed mode.
    Parametric gain: Gamma = epsilon * omega_{n0} / 2.
    Loss rate:       kappa = omega_{n0} / Q.

    Below threshold (2 Gamma < kappa) -> N_ss = Gamma / (kappa - 2 Gamma).
    Above threshold (2 Gamma > kappa) -> exponential growth, capped at n_crit
    (Kerr-nonlinearity-limited saturation, typical of cQED / photonic cavities).
    """
    n0 = lowest_allowed_mode(primes)
    omega = n0 * np.pi * c / L
    Gamma = epsilon * omega / 2.0
    kappa = omega / Q

    if 2 * Gamma >= kappa:
        N = n_crit
        regime = "above-threshold"
    else:
        N = Gamma / (kappa - 2 * Gamma)
        regime = "below-threshold"
    return N, omega, regime

def F_dce(L, A, Q, epsilon, primes=(), n_crit=1e6):
    """Repulsive force on each plate from N intracavity photons in the
    parametrically driven mode. For a 1D standing wave the radiation pressure
    on each end mirror is P = N hbar omega / V, force = P * A = N hbar omega / L.
    Sign convention: positive = repulsive (push plates apart)."""
    N, omega, regime = dce_photon_number(L, Q, epsilon, primes, n_crit)
    F = N * hbar * omega / L
    return F, N, omega, regime

# ----------------------------------------------------------------------------
# Run 1: Static prime-muted Casimir force at L = 100 nm
# ----------------------------------------------------------------------------
def report_static():
    print("=" * 72)
    print("STATIC PRIME-MUTED CASIMIR (parallel plates, A = 1 cm^2)")
    print("=" * 72)
    print(f"Plate mass : {M_plate*1e6:8.3f}  micro-g")
    print(f"Plate weight: {W_plate*1e6:8.3f}  micro-N\n")

    L_vals = [10e-9, 100e-9, 1e-6, 10e-6, 100e-6]
    sets   = [(), (2,), (3,), (2,3), (2,3,5)]

    header = f"{'L [nm]':>10} | " + " | ".join(
        f"S={str(list(s)):<10}" for s in sets
    )
    print(header)
    print("-" * len(header))
    for L in L_vals:
        row = f"{L*1e9:>10.0f} | "
        for S in sets:
            P = P_casimir_static(L, S)
            F = P * A_plate
            ratio = abs(F) / W_plate
            tag = "+" if F > 0 else "-"
            row += f"{tag}{ratio:9.2e} | "
        print(row)
    print("\n(values shown: |F_Casimir| / W_plate, sign = + repulsive, - attractive)")
    print("Repulsion appears for |S| odd. {2,3,5} gives 22568x amplification.\n")

# ----------------------------------------------------------------------------
# Run 2: DCE on top of static prime-muted Casimir
# ----------------------------------------------------------------------------
def report_dce():
    print("=" * 72)
    print("DYNAMICAL CASIMIR ADD-ON (driving the lowest allowed mode)")
    print("=" * 72)
    primes = (2, 3, 5)              # repulsive triplet
    n_crit_table = {                 # saturation photon count by platform
        "circuit-QED 5 GHz" : 1e4,
        "photonic THz"      : 1e6,
        "ideal optical"     : 1e9,
    }
    L = 1e-6                         # 1 micron gap
    print(f"Gap L = {L*1e6:.1f} um, primes muted S = {list(primes)}\n")
    P_stat  = P_casimir_static(L, primes)
    F_stat  = P_stat * A_plate
    print(f"Static prime-muted Casimir force: {F_stat:+.3e} N")
    print(f"Plate weight                    : {W_plate:+.3e} N")
    print(f"Static repulsion / weight       : {F_stat/W_plate:+.3e}\n")

    print(f"{'Platform':24} {'Q':>8} {'eps':>8} {'N_phot':>12} {'F_DCE [N]':>14} {'regime':>16}")
    print("-" * 90)
    for name, n_crit in n_crit_table.items():
        for Q, eps in [(1e4, 1e-4), (1e6, 1e-3), (1e9, 1e-2)]:
            F, N, om, regime = F_dce(L, A_plate, Q, eps, primes, n_crit)
            print(f"{name:24} {Q:>8.0e} {eps:>8.0e} {N:>12.2e} {F:>+14.3e} {regime:>16}")
    print()

# ----------------------------------------------------------------------------
# Run 3: Sweep gap L, find antigravity threshold for each scenario
# ----------------------------------------------------------------------------
def sweep_and_plot():
    L_vals = np.logspace(-8, -3, 200)        # 10 nm ... 1 mm
    primes = (2, 3, 5)
    n_crit = 1e6
    Q       = 1e6
    eps     = 1e-3

    F_static = np.array([P_casimir_static(L, primes) * A_plate for L in L_vals])
    F_dce_arr = np.zeros_like(L_vals)
    N_arr     = np.zeros_like(L_vals)
    regimes   = []
    for i, L in enumerate(L_vals):
        F, N, om, reg = F_dce(L, A_plate, Q, eps, primes, n_crit)
        F_dce_arr[i] = F
        N_arr[i]     = N
        regimes.append(reg)
    F_total = F_static + F_dce_arr

    fig, ax = plt.subplots(1, 1, figsize=(7.5, 5.5))
    ax.loglog(L_vals*1e9, np.abs(F_static), label="static (prime-muted, S={2,3,5})", lw=2)
    ax.loglog(L_vals*1e9, np.abs(F_dce_arr), label=f"DCE only (Q={Q:.0e}, eps={eps:.0e}, n_crit={n_crit:.0e})", lw=2, ls="--")
    ax.loglog(L_vals*1e9, np.abs(F_total), label="total", lw=2.5, ls=":")
    ax.axhline(W_plate, color="red", lw=1.2, label=f"plate weight (Si, 1 cm² × 1 μm)")
    ax.set_xlabel("gap L [nm]")
    ax.set_ylabel("repulsive force [N]")
    ax.set_title("Prime-muted Casimir + DCE versus gravity")
    ax.legend(fontsize=9, loc="upper right")
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    out = os.path.join(os.path.dirname(__file__), "dce_prime_muting_force_vs_gap.png")
    fig.savefig(out, dpi=140)
    print(f"Saved plot to {out}")

    # Find the critical gap where total force = weight
    idx = np.where(F_total >= W_plate)[0]
    if idx.size:
        L_crit = L_vals[idx[-1]]   # largest L where lift is still possible
        F_at_Lcrit = F_total[idx[-1]]
        print(f"\nAntigravity threshold: L_max = {L_crit*1e9:.2f} nm  "
              f"(F_total = {F_at_Lcrit:.3e} N at this gap)")
    else:
        print("\nNo gap in this sweep allows antigravity.")

    return L_vals, F_static, F_dce_arr, F_total

# ----------------------------------------------------------------------------
# Run 3b: Crossover analysis - what n_crit is needed for DCE to matter?
# ----------------------------------------------------------------------------
def crossover_analysis():
    print("=" * 72)
    print("CROSSOVER: when does DCE radiation pressure equal static Casimir?")
    print("=" * 72)
    primes = (2, 3, 5)
    f_S    = abs(mute_factor(primes))
    print(f"Muted set S = {list(primes)}, |1 - prod(p^3)| = {f_S}\n")
    print("Setting F_DCE = F_static gives:")
    print("    N_required(L) = (pi * f_S) / (240 * (L/lambda_C)^2)")
    print("with lambda_C = hbar / (m_e c) does NOT enter — the formula is")
    print("    N_required(L) = pi * f_S / 240 * (L_ref/L)^2 * (L_ref^-2 -> dimensionless),")
    print("so we just compute it directly:\n")
    print(f"{'L':>10} | {'N_required':>14} | {'feasible?':>12}")
    print("-" * 46)
    for L in [10e-9, 100e-9, 1e-6, 10e-6, 100e-6, 1e-3, 1e-2]:
        F_stat = abs(P_casimir_static(L, primes)) * A_plate
        n0     = lowest_allowed_mode(primes)
        omega  = n0 * np.pi * c / L
        # F_DCE = N hbar omega / L  -> N = F_stat * L / (hbar omega)
        N_req  = F_stat * L / (hbar * omega)
        feasible = "yes" if N_req < 1e9 else ("maybe" if N_req < 1e15 else "no")
        print(f"{L*1e9:>9.0f}n | {N_req:>14.2e} | {feasible:>12}")
    print("\nDCE only matters where N_required < n_crit(achievable).")
    print("For L < 1 um the static term needs N >> 1e15 photons to match -- absurd.\n")

# ----------------------------------------------------------------------------
# Run 4: How much amplification does DCE actually buy us?
# ----------------------------------------------------------------------------
def amplification_table():
    print("=" * 72)
    print("DCE AMPLIFICATION RATIO  F_DCE / F_static")
    print("=" * 72)
    primes = (2, 3, 5)
    n_crit = 1e6
    print(f"Muted primes S={list(primes)}, n_crit (saturation) = {n_crit:.0e}\n")
    print(f"{'L':>10} | {'F_static':>12} | {'F_DCE':>12} | {'ratio':>10}")
    print("-" * 56)
    for L in [10e-9, 100e-9, 1e-6, 10e-6, 100e-6, 1e-3]:
        Fs = abs(P_casimir_static(L, primes)) * A_plate
        Fd, _, _, _ = F_dce(L, A_plate, 1e6, 1e-3, primes, n_crit)
        ratio = Fd / Fs
        print(f"{L*1e9:>9.0f}n | {Fs:>12.3e} | {Fd:>12.3e} | {ratio:>10.3e}")
    print()

# ============================================================================
if __name__ == "__main__":
    report_static()
    report_dce()
    amplification_table()
    crossover_analysis()
    sweep_and_plot()
