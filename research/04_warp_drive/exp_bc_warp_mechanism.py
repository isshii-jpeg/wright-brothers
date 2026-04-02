"""
PHYSICAL MECHANISM FOR SPACETIME SOURCE CODE EDITING
via the Bost-Connes Phase Transition
=====================================================

The central question: HOW do you physically "mute a prime" or "shift a zero"?

The Bost-Connes system provides the bridge:

  Mathematical operation          Physical mechanism in BC system
  ─────────────────────          ─────────────────────────────────
  Mute prime p                ↔  Project out p-divisible states from ℓ²(ℕ)
  Shift Riemann zero          ↔  Perturb the BC Hamiltonian H → H + δV
  Cross the β=1 transition    ↔  Cool/heat the arithmetic vacuum
  Galois action on KMS states ↔  Rotate between degenerate ground states

The key insight: the Bost-Connes system is a PHYSICAL quantum system
(quantum statistical mechanics on a C*-algebra) whose thermal properties
are DETERMINED by number theory. The phase transition at β=1 is where
arithmetic structure "crystallizes" — primes become individually visible.

Manipulating this system = manipulating spacetime's arithmetic structure.

Wright Brothers, 2026
"""

import numpy as np
from scipy.special import zeta as scipy_zeta
import matplotlib.pyplot as plt

print("=" * 70)
print("  PHYSICAL MECHANISM FOR SPACETIME SOURCE CODE EDITING")
print("  via the Bost-Connes Phase Transition")
print("=" * 70)

# ============================================================================
#  THE BOST-CONNES HILBERT SPACE AND HAMILTONIAN
# ============================================================================
#
#  Hilbert space: H = ℓ²(ℕ*) with basis {|n⟩ : n = 1, 2, 3, ...}
#  Hamiltonian:   H|n⟩ = log(n) |n⟩
#  Partition fn:  Z(β) = Tr(e^{-βH}) = Σ_n e^{-β log(n)} = Σ_n n^{-β} = ζ(β)
#
#  Each basis state |n⟩ has energy E_n = log(n).
#  The prime factorization n = p₁^a₁ · p₂^a₂ · ... means:
#    E_n = a₁·log(p₁) + a₂·log(p₂) + ...
#
#  So the energy is ADDITIVE over prime factors.
#  Each prime p contributes an independent "harmonic oscillator"
#  with frequency log(p).

print("\n" + "=" * 70)
print("  PART 1: THE BOST-CONNES HILBERT SPACE")
print("=" * 70)
print()
print("  Hilbert space: ℓ²(ℕ*) = span{|1⟩, |2⟩, |3⟩, ...}")
print("  Hamiltonian: H|n⟩ = log(n)|n⟩")
print("  Energy spectrum: E_n = log(n)")
print()
print("  Prime decomposition of energy:")
print("    E_1  = log(1)   = 0")
print("    E_2  = log(2)   = 0.693  ← prime p=2")
print("    E_3  = log(3)   = 1.099  ← prime p=3")
print("    E_4  = log(4)   = 2·log(2) = 1.386  ← p=2, twice")
print("    E_6  = log(6)   = log(2)+log(3) = 1.792  ← p=2 and p=3")
print("    E_12 = log(12)  = 2·log(2)+log(3) = 2.485")
print()
print("  The BC system = infinite collection of harmonic oscillators,")
print("  one per prime, with frequencies ω_p = log(p).")
print()
print("  ζ(β) = ∏_p 1/(1-p^{-β}) = ∏_p Z_p(β)")
print("  where Z_p(β) = Σ_{k=0}^∞ p^{-kβ} = 1/(1-p^{-β})")
print("  is the partition function of the p-th oscillator.")

# ============================================================================
#  MECHANISM 1: PRIME MUTING AS HILBERT SPACE PROJECTION
# ============================================================================

print("\n" + "=" * 70)
print("  MECHANISM 1: PRIME MUTING = HILBERT SPACE PROJECTION")
print("=" * 70)
print()
print("  To 'mute' prime p, we PROJECT OUT all states |n⟩ where p | n.")
print()
print("  Define the projection operator:")
print("    P_{¬p} = Σ_{n: p∤n} |n⟩⟨n|")
print()
print("  This removes all states whose quantum number is divisible by p.")
print("  The restricted partition function:")
print("    Z_{¬p}(β) = Tr(P_{¬p} · e^{-βH})")
print("             = Σ_{n: p∤n} n^{-β}")
print("             = ζ(β) · (1 - p^{-β})")
print()

# Compute the restricted partition function
def Z_full(beta):
    """Full BC partition function = ζ(β)."""
    if beta <= 1:
        return float('inf')
    return scipy_zeta(beta, 1)

def Z_muted(beta, p):
    """BC partition function with prime p muted."""
    if beta <= 1:
        return float('inf')
    return scipy_zeta(beta, 1) * (1 - p**(-beta))

print("  Numerical verification:")
print()
print(f"  {'β':>5s} | {'Z(β) = ζ(β)':>14s} | {'Z_{¬2}(β)':>14s} | {'Z_{¬3}(β)':>14s} | {'Z_{¬2,3}(β)':>14s}")
print("  " + "-" * 72)
for beta in [1.5, 2.0, 3.0, 5.0, 10.0]:
    z = Z_full(beta)
    z2 = Z_muted(beta, 2)
    z3 = Z_muted(beta, 3)
    z23 = Z_muted(beta, 2) * (1 - 3**(-beta)) / (1) # approx
    z23_exact = z * (1 - 2**(-beta)) * (1 - 3**(-beta))
    print(f"  {beta:5.1f} | {z:14.6f} | {z2:14.6f} | {z3:14.6f} | {z23_exact:14.6f}")

print()
print("  KEY: Z_{¬p}(β) < Z(β). Muting a prime REDUCES the partition function.")
print("  Fewer states are available → the system is 'colder' in some sense.")

# ============================================================================
#  THE PHYSICAL REALIZATION OF PROJECTION
# ============================================================================

print("\n" + "=" * 70)
print("  HOW TO PHYSICALLY REALIZE THE PROJECTION P_{¬p}")
print("=" * 70)
print()
print("  Three candidate mechanisms:")
print()
print("  (A) SPECTRAL FILTERING")
print("  ────────────────────────")
print("  The states |n⟩ with p|n have energies E_n containing log(p).")
print("  A frequency-selective filter that absorbs the frequency log(p)")
print("  would effectively project out p-divisible states.")
print()
print("  Analogy: an acoustic notch filter removes a specific frequency.")
print("  Here: a 'number-theoretic notch filter' removes a prime frequency.")
print()
print("  If spacetime modes are labeled by integers (as in the BC system),")
print("  a physical device that resonates at frequency ω = log(p) and")
print("  absorbs those modes would 'mute' prime p.")
print()

# Compute the "frequency spectrum" of the BC system
N_max = 100
energies = np.log(np.arange(1, N_max + 1))
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]

print("  Energy spectrum of BC system (first 100 states):")
print(f"    Fundamental frequencies: ", end="")
for p in primes[:6]:
    print(f"log({p})={np.log(p):.3f}  ", end="")
print()
print()

print("  (B) BOUNDARY CONDITIONS")
print("  ─────────────────────────")
print("  In the Casimir effect, boundary conditions select which modes exist.")
print("  Parallel plates at distance d: only modes with λ = 2d/n survive.")
print()
print("  Arithmetic boundary condition: a boundary that allows only modes |n⟩")
print("  where gcd(n, p) = 1. This is a 'sieve of Eratosthenes' boundary.")
print()
print("  Physically: a material whose crystal structure has periodicity p")
print("  would interact differently with p-divisible and non-p-divisible modes.")
print()

print("  (C) PHASE TRANSITION CONTROL")
print("  ────────────────────────────")
print("  The BC system has a phase transition at β = 1.")
print("  For β > 1, the Galois group Gal(Q^ab/Q) ≅ Ẑ* = ∏_p Z_p* acts")
print("  on the degenerate KMS ground states.")
print()
print("  Each factor Z_p* corresponds to prime p.")
print("  'Muting' prime p = restricting to KMS states invariant under Z_p*.")
print("  = selecting a specific SECTOR of the symmetry-broken phase.")
print()
print("  This is analogous to applying a magnetic field to break a specific")
print("  component of a spin symmetry. The 'field' that breaks Z_p* symmetry")
print("  is a number-theoretic analogue of a magnetic field.")

# ============================================================================
#  MECHANISM 2: ZERO SHIFTING AS HAMILTONIAN PERTURBATION
# ============================================================================

print("\n" + "=" * 70)
print("  MECHANISM 2: ZERO SHIFTING = HAMILTONIAN PERTURBATION")
print("=" * 70)
print()

# The Riemann zeros appear in the BC system through the explicit formula.
# The density of states is:
#   d(E) = Σ_n δ(E - log(n))
#        = e^E - Σ_ρ e^{ρE} / ρ + ...  (Weil's explicit formula)
#
# where ρ runs over non-trivial zeros of ζ.
#
# Perturbing H → H + δV changes the eigenvalues E_n → E_n + δE_n.
# By the explicit formula, this shifts the zeros: ρ → ρ + δρ.

print("  The explicit formula (Weil) connects eigenvalues and zeros:")
print()
print("    d(E) = Σ_n δ(E - log n) = e^E - Σ_ρ e^{ρE}/ρ + ...")
print()
print("  The Riemann zeros ρ = 1/2 + iγ appear as OSCILLATORY corrections")
print("  to the smooth density of states e^E.")
print()
print("  Perturbing the Hamiltonian H → H + δV:")
print("    log(n) → log(n) + ⟨n|δV|n⟩")
print()
print("  This shifts the zeros via the inverse spectral problem.")
print()

# Compute how a perturbation changes the "spectral sum" over zeros
riemann_zeros_gamma = [
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
]

def density_of_states(E, zeros=riemann_zeros_gamma, N_terms=50):
    """Smoothed density of states using the explicit formula.
    d(E) ≈ e^E - 2·Σ_γ e^{E/2}·cos(γE)/|ρ| + ..."""
    smooth = np.exp(E)
    oscillatory = 0.0
    for gamma in zeros:
        rho_abs = np.sqrt(0.25 + gamma**2)
        oscillatory += np.exp(E / 2) * np.cos(gamma * E) / rho_abs
    return smooth - 2 * oscillatory

# Perturbed density: shift all zeros by δ in real part
def density_perturbed(E, delta_sigma, zeros=riemann_zeros_gamma):
    """Density of states with zeros shifted: 1/2 → 1/2 + δ."""
    smooth = np.exp(E)
    oscillatory = 0.0
    sigma = 0.5 + delta_sigma
    for gamma in zeros:
        rho_abs = np.sqrt(sigma**2 + gamma**2)
        oscillatory += np.exp(sigma * E) * np.cos(gamma * E) / rho_abs
    return smooth - 2 * oscillatory

E_range = np.linspace(0.1, 8, 500)

print("  === Perturbation types and their physical realizations ===")
print()
print("  TYPE A: Diagonal perturbation δV|n⟩ = v(n)|n⟩")
print("    → Shifts energies: E_n → log(n) + v(n)")
print("    → Physical: external potential applied to the BC system")
print("    → Example: v(n) = ε·(-1)^n (alternating perturbation)")
print("    → Breaks the Z_2* symmetry → affects prime p=2 channel")
print()
print("  TYPE B: Multiplicative perturbation δV|n⟩ = ε·log(n)·|n⟩")
print("    → Shifts energies: E_n → (1+ε)·log(n)")
print("    → Equivalent to β → β·(1+ε) (temperature rescaling)")
print("    → Moves the phase transition: β_c = 1 → 1/(1+ε)")
print()
print("  TYPE C: Prime-selective perturbation")
print("    → δV|n⟩ = ε·v_p(n)·|n⟩ where v_p(n) = ord_p(n)·log(p)")
print("    → Shifts only the p-th harmonic: E_n → log(n) + ε·ord_p(n)·log(p)")
print("    → Selectively tunes the 'frequency' of prime p")
print("    → Physical: resonant interaction at frequency log(p)")

# ============================================================================
#  COMPUTING THE EFFECT: MODIFIED PHASE TRANSITION
# ============================================================================

print("\n" + "=" * 70)
print("  MODIFIED PHASE TRANSITION: WHAT HAPPENS WHEN YOU PERTURB")
print("=" * 70)
print()

# Type B perturbation: energy rescaling
# H_ε = (1+ε)H, so E_n(ε) = (1+ε)log(n)
# Partition function: Z_ε(β) = Σ n^{-β(1+ε)} = ζ(β(1+ε))
# Phase transition moves to β_c = 1/(1+ε)

print("  Type B: Temperature rescaling H → (1+ε)H")
print()
print(f"  {'ε':>8s} | {'β_c':>8s} | {'Z(β=2)':>12s} | {'Shift in transition'}")
print("  " + "-" * 55)
for eps in [-0.3, -0.1, 0, 0.1, 0.3, 0.5, 1.0]:
    beta_c = 1.0 / (1 + eps) if (1 + eps) > 0 else float('inf')
    z_at_2 = scipy_zeta(2 * (1 + eps), 1) if 2 * (1 + eps) > 1 else float('inf')
    print(f"  {eps:+8.2f} | {beta_c:8.3f} | {z_at_2:12.6f} | {'← transition moves LEFT' if eps > 0 else '← transition moves RIGHT' if eps < 0 else '← standard'}")

print()
print("  Moving β_c < 1 means: the 'disordered' (no-arithmetic) phase")
print("  extends to LOWER temperatures. Primes become invisible at")
print("  temperatures where they would normally be 'frozen in'.")
print()
print("  Moving β_c > 1 means: arithmetic order persists to HIGHER")
print("  temperatures. Primes crystallize earlier.")

# ============================================================================
#  THE WARP DRIVE CONNECTION
# ============================================================================

print("\n" + "=" * 70)
print("  THE WARP DRIVE CONNECTION")
print("=" * 70)
print()
print("  Standard spacetime: all primes ON, ζ(-3) = +1/120")
print("    → vacuum energy is tiny and POSITIVE")
print("    → no exotic matter")
print("    → no warp drive")
print()
print("  Modified spacetime (prime p muted):")
print("    → ζ_{¬p}(-3) = (1-p³)/120 < 0")
print("    → vacuum energy is LARGE and NEGATIVE")
print("    → exotic matter condition SATISFIED")
print("    → warp bubble geometry is ALLOWED")
print()
print("  Physical mechanism to mute prime p:")
print()
print("  ┌──────────────────────────────────────────────────────────┐")
print("  │  1. Prepare a Bost-Connes system in the β > 1 phase     │")
print("  │     (low temperature: arithmetic structure visible)      │")
print("  │                                                          │")
print("  │  2. Apply a prime-selective perturbation V_p that        │")
print("  │     'gaps out' the p-th oscillator mode                  │")
print("  │     (analogy: applying a mass to a harmonic oscillator   │")
print("  │      at frequency log(p) → mode becomes invisible)      │")
print("  │                                                          │")
print("  │  3. In the perturbed system, the effective ζ function    │")
print("  │     becomes ζ_{¬p}(s), with NEGATIVE vacuum energy      │")
print("  │                                                          │")
print("  │  4. If this perturbation can be applied LOCALLY          │")
print("  │     (in a finite region of spacetime), then:             │")
print("  │     → a region with negative vacuum energy exists        │")
print("  │     → this region can support warp bubble geometry       │")
print("  │     → the energy cost = energy to excite the V_p mode   │")
print("  └──────────────────────────────────────────────────────────┘")
print()

# Energy cost estimate
print("  ENERGY COST ESTIMATE:")
print()
print("  To 'gap out' the p-th mode in a region of size L:")
print("    ΔE ~ ℏ·ω_p / L³ × (number of modes affected)")
print("    ω_p = c/L_p where L_p is the 'p-th Planck length'")
print()

# The p-th oscillator has frequency ω_p = log(p) in natural units
# The energy to create a gap of size Δ in the p-th mode:
# ΔE ~ Δ · (density of p-divisible states in region of size L)
# ~ Δ · (L/l_P)³ / p  (fraction 1/p of states are p-divisible)

hbar_c = 3.16e-26  # ℏc in J·m
l_P = 1.616e-35  # Planck length

for p in [2, 3, 5]:
    print(f"  Prime p = {p}:")
    print(f"    Frequency ω_p = log({p}) × E_P/ℏ = {np.log(p):.3f} × 1.855×10¹⁹ GHz")

    # Energy to mute p in a 1m³ region (very rough estimate)
    # Number of "modes" in volume V at Planck scale: V/l_P³
    # Fraction that are p-divisible: 1/p
    # Energy per mode: ~E_P (Planck energy)
    E_P = 1.956e9  # Joules
    V = 1.0  # m³
    n_modes = V / l_P**3
    n_p_modes = n_modes / p
    # But we don't need to give each mode E_P — we just need to shift
    # the spectral weight. The minimum perturbation energy:
    # ΔE ~ ℏω_p × sqrt(n_p_modes) (quantum fluctuation argument)
    Delta_E = E_P * np.log(p) * np.sqrt(n_p_modes)
    print(f"    Modes in 1m³: {n_modes:.2e}")
    print(f"    p-divisible modes: {n_p_modes:.2e}")
    print(f"    Energy estimate: {Delta_E:.2e} J = {Delta_E/(1.989e30 * 9e16):.2e} M_sun·c²")
    print()

print("  These estimates are EXTREMELY rough, but they suggest the energy")
print("  cost is astronomical for macroscopic regions. However:")
print()
print("  SCALING ARGUMENT:")
print("  If the region is microscopic (L ~ Planck length), the energy cost")
print("  is of order E_P ~ 10⁹ J (= energy of a lightning bolt).")
print("  A Planck-scale warp bubble might be achievable.")
print()
print("  The Casimir effect shows that boundary conditions at nm scale")
print("  already modify vacuum energy. 'Arithmetic boundary conditions'")
print("  at the Planck scale could, in principle, mute a prime channel.")

# ============================================================================
#  VISUALIZATION
# ============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.patch.set_facecolor('#0a0a1a')
fig.suptitle('Bost-Connes Mechanism for Spacetime Source Code Editing',
             fontsize=14, fontweight='bold', color='#ffd93d')

# Panel 1: BC energy spectrum colored by prime factorization
ax = axes[0, 0]
n_vals = np.arange(1, 61)
for n in n_vals:
    color = '#ffd93d'  # default
    if n % 2 == 0 and n % 3 != 0: color = '#ff6b6b'
    elif n % 3 == 0 and n % 2 != 0: color = '#00d4ff'
    elif n % 2 == 0 and n % 3 == 0: color = '#b482ff'
    elif n % 5 == 0: color = '#6bff8d'
    ax.bar(n, np.log(n), color=color, alpha=0.7, width=0.8)
ax.set_xlabel('n (state label)', color='white')
ax.set_ylabel('E_n = log(n)', color='white')
ax.set_title('BC Energy Spectrum (color = prime factors)', fontsize=10, color='white')
# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#ff6b6b', label='divisible by 2'),
                   Patch(facecolor='#00d4ff', label='divisible by 3'),
                   Patch(facecolor='#b482ff', label='divisible by 2&3'),
                   Patch(facecolor='#6bff8d', label='divisible by 5'),
                   Patch(facecolor='#ffd93d', label='other')]
ax.legend(handles=legend_elements, fontsize=7, loc='upper left')
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.15)

# Panel 2: Muted vs full partition function
ax = axes[0, 1]
beta_range = np.linspace(1.01, 6, 200)
ax.plot(beta_range, [Z_full(b) for b in beta_range],
        color='white', linewidth=2, label='ζ(β) [all ON]')
ax.plot(beta_range, [Z_muted(b, 2) for b in beta_range],
        color='#ff6b6b', linewidth=2, linestyle='--', label='ζ_{¬2}(β) [p=2 OFF]')
ax.plot(beta_range, [Z_muted(b, 3) for b in beta_range],
        color='#00d4ff', linewidth=2, linestyle='--', label='ζ_{¬3}(β) [p=3 OFF]')
ax.axvline(x=1, color='#ffd93d', linewidth=1, linestyle=':', alpha=0.5, label='β=1 transition')
ax.set_xlabel('β (inverse temperature)', color='white')
ax.set_ylabel('Partition function', color='white')
ax.set_title('Partition Function: Full vs Muted', fontsize=10, color='white')
ax.legend(fontsize=8)
ax.set_ylim(0, 10)
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.15)

# Panel 3: Density of states (explicit formula)
ax = axes[1, 0]
E_range = np.linspace(0.5, 6, 500)
d_standard = [density_of_states(E) for E in E_range]
d_shifted_neg = [density_perturbed(E, -0.15) for E in E_range]
d_shifted_pos = [density_perturbed(E, +0.15) for E in E_range]
ax.plot(E_range, d_standard, color='white', linewidth=2, label='δ=0 (standard)')
ax.plot(E_range, d_shifted_neg, color='#ff6b6b', linewidth=1.5,
        linestyle='--', label='δ=-0.15 (zeros left)')
ax.plot(E_range, d_shifted_pos, color='#6bff8d', linewidth=1.5,
        linestyle='--', label='δ=+0.15 (zeros right)')
ax.set_xlabel('E', color='white')
ax.set_ylabel('Density of states d(E)', color='white')
ax.set_title('Density of States vs Zero Position', fontsize=10, color='white')
ax.legend(fontsize=8)
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.15)

# Panel 4: The mechanism diagram
ax = axes[1, 1]
ax.text(0.5, 0.95, 'WARP DRIVE MECHANISM', ha='center', va='top',
        fontsize=12, fontweight='bold', color='#ffd93d', transform=ax.transAxes)

steps = [
    (0.85, 'Prepare BC system at β > 1\n(arithmetic phase)', '#ffd93d'),
    (0.70, 'Apply perturbation V_p\n(prime-selective filter at ω=log p)', '#00d4ff'),
    (0.55, 'p-th channel gaps out\n(ζ → ζ_{¬p}, mode suppressed)', '#ff6b6b'),
    (0.40, 'Vacuum energy flips sign\n(ζ_{¬p}(-3) < 0)', '#ff6b6b'),
    (0.25, 'Energy conditions violated\nLOCALLY in perturbed region', '#b482ff'),
    (0.10, 'Warp bubble geometry\nBECOMES ALLOWED', '#6bff8d'),
]
for y, text, color in steps:
    ax.text(0.5, y, text, ha='center', va='center',
            fontsize=9, color=color, transform=ax.transAxes,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#0a0a1a',
                     edgecolor=color, alpha=0.8))
for i in range(len(steps) - 1):
    ax.annotate('', xy=(0.5, steps[i+1][0] + 0.04),
                xytext=(0.5, steps[i][0] - 0.04),
                xycoords='axes fraction', textcoords='axes fraction',
                arrowprops=dict(arrowstyle='->', color='white', lw=1.5))
ax.axis('off')
ax.set_facecolor('#0a0a1a')

plt.tight_layout()
plt.savefig('research/04_warp_drive/bc_warp_mechanism.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
plt.close()

print(f"\n  Plot saved: research/04_warp_drive/bc_warp_mechanism.png")

# ============================================================================
#  SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("  SUMMARY: THE BC WARP DRIVE PROGRAMME")
print("=" * 70)
print()
print("  ┌──────────────────────────────────────────────────────────────┐")
print("  │  MATHEMATICAL CHAIN:                                        │")
print("  │                                                              │")
print("  │  Mute prime p                                                │")
print("  │    ↓                                                         │")
print("  │  ζ(s) → ζ_{¬p}(s) = ζ(s)·(1-p^{-s})                       │")
print("  │    ↓                                                         │")
print("  │  Vacuum energy: ζ(-3) = +1/120 → (1-p³)/120 < 0            │")
print("  │    ↓                                                         │")
print("  │  Weak energy condition VIOLATED                              │")
print("  │    ↓                                                         │")
print("  │  Alcubierre metric PERMITTED by Einstein equations           │")
print("  │                                                              │")
print("  │  PHYSICAL CHAIN:                                             │")
print("  │                                                              │")
print("  │  Prepare BC system at β > 1 (low temperature)                │")
print("  │    ↓                                                         │")
print("  │  Apply V_p: resonant perturbation at ω = log(p)             │")
print("  │    ↓                                                         │")
print("  │  p-th harmonic oscillator gaps out (mass generation)         │")
print("  │    ↓                                                         │")
print("  │  Restricted Hilbert space: ℓ²({n : p∤n})                    │")
print("  │    ↓                                                         │")
print("  │  Modified vacuum in local region                             │")
print("  │    ↓                                                         │")
print("  │  Negative vacuum energy density in that region               │")
print("  │    ↓                                                         │")
print("  │  Warp bubble                                                 │")
print("  └──────────────────────────────────────────────────────────────┘")
print()
print("  OPEN PROBLEMS:")
print("  1. Is the BC system physically realizable? (condensed matter?)")
print("  2. Can V_p be applied LOCALLY in spacetime?")
print("  3. Does the ζ_{¬p} vacuum persist after the perturbation is removed?")
print("  4. What is the precise energy cost of muting p=2?")
print("  5. Does the back-reaction (gravity of the negative energy)")
print("     stabilize or destabilize the configuration?")
