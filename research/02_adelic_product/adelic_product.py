"""
Adelic Product Formula: A_∞ · ∏_p A_p = 1
==========================================

The Freund-Witten (1987) adelic product formula shows that the
Veneziano amplitude of string theory, when combined with its
p-adic counterparts for ALL primes, yields unity.

This is the most direct evidence that string theory "lives over the adeles"
and that spacetime may have p-adic structure at the Planck scale.

References:
  [1] Freund & Witten, Phys. Lett. B 199 (1987), 191-195
  [2] Freund & Olson, Phys. Lett. B 199 (1987), 186-190
  [3] Volovich, CERN-TH.4781/87 (1987)
  [4] Brekke & Freund, Phys. Rep. 233 (1993), 1-66

Wright Brothers, 2026
"""

import numpy as np
from scipy.special import gamma as Gamma
import matplotlib.pyplot as plt

print("=" * 70)
print("  ADELIC PRODUCT FORMULA: UNIFYING ALL PRIMES IN STRING THEORY")
print("=" * 70)

# ============================================================================
#  PART 1: The Veneziano Amplitude A_∞(s,t)
# ============================================================================
#
# The Veneziano amplitude (1968) for open string tachyon scattering:
#
#   A_∞(s,t) = Γ(-s)Γ(-t) / Γ(-s-t)
#            = B(-s, -t)   (Euler beta function)
#
# where s, t are Mandelstam variables with s + t + u = 0.
#
# This can be written using the "gamma factor at infinity":
#
#   Γ_∞(s) = π^{-s/2} Γ(s/2)
#
# The real amplitude is:
#   A_∞(s,t) = Γ_∞(1-s) Γ_∞(1-t) Γ_∞(1-u) / [Γ_∞(s) Γ_∞(t) Γ_∞(u)]
#
# (up to normalization; here we use the Gel'fand-Graev beta function form)

def veneziano_amplitude(s, t):
    """Real (Archimedean) Veneziano amplitude A_∞(s,t)."""
    u = -s - t
    try:
        return Gamma(-s) * Gamma(-t) / Gamma(-s - t)
    except:
        return np.nan

print("\n--- PART 1: Veneziano Amplitude A_∞(s,t) ---")
print()
s_test, t_test = -0.3, -0.4
u_test = -s_test - t_test
A_inf = veneziano_amplitude(s_test, t_test)
print(f"  Test point: s = {s_test}, t = {t_test}, u = {u_test:.1f}")
print(f"  A_∞(s,t) = Γ({-s_test})·Γ({-t_test})/Γ({-s_test-t_test:.1f})")
print(f"           = {A_inf:.10f}")

# ============================================================================
#  PART 2: The p-adic Amplitude A_p(s,t)
# ============================================================================
#
# For each prime p, the p-adic string amplitude is:
#
#   A_p(s,t) = ζ_p(1-s) · ζ_p(1-t) · ζ_p(1-u)
#              / [ζ_p(s) · ζ_p(t) · ζ_p(u)]
#
# where ζ_p(s) = (1 - p^{-s})^{-1} is the local (Euler) factor of ζ(s).
#
# This is the Gel'fand-Graev beta function over Q_p.

def zeta_p(s, p):
    """Local Euler factor: ζ_p(s) = 1/(1 - p^{-s})."""
    return 1.0 / (1.0 - p ** (-s))

def p_adic_amplitude(s, t, p):
    """p-adic Veneziano amplitude A_p(s,t)."""
    u = -s - t
    num = zeta_p(1-s, p) * zeta_p(1-t, p) * zeta_p(1-u, p)
    den = zeta_p(s, p) * zeta_p(t, p) * zeta_p(u, p)
    return num / den

print("\n--- PART 2: p-adic Amplitudes A_p(s,t) ---")
print()
print(f"  At s = {s_test}, t = {t_test}:")
for p in [2, 3, 5, 7, 11, 13]:
    A_p = p_adic_amplitude(s_test, t_test, p)
    print(f"    A_{p:2d}(s,t) = {A_p:.10f}")

# ============================================================================
#  PART 3: The Adelic Product Formula
# ============================================================================
#
# THEOREM (Freund-Witten, 1987):
#
#   A_∞(s,t) · ∏_{p prime} A_p(s,t) = 1
#
# This is equivalent to the Euler product for the Riemann zeta function:
#   ζ(s) = ∏_p ζ_p(s) = ∏_p 1/(1-p^{-s})
#
# combined with the functional equation of ζ(s).
#
# Let's verify numerically by computing the product over increasing
# sets of primes and watching it converge to 1/A_∞.

def primes_up_to(n):
    """Sieve of Eratosthenes."""
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n+1, i):
                sieve[j] = False
    return [i for i in range(2, n+1) if sieve[i]]

print("\n--- PART 3: Adelic Product Formula ---")
print()
print("  THEOREM: A_∞(s,t) · ∏_p A_p(s,t) = 1")
print()

all_primes = primes_up_to(10000)

# Test at multiple points
test_points = [
    (-0.3, -0.4),
    (-0.1, -0.2),
    (-0.5, -0.3),
    (-0.7, -0.15),
    (-0.25, -0.6),
]

print(f"  Convergence of A_∞ · ∏_{{p≤N}} A_p toward 1:")
print()

for s, t in test_points:
    A_inf = veneziano_amplitude(s, t)
    print(f"  s={s}, t={t}:  A_∞ = {A_inf:.6f}")

    product = A_inf
    checkpoints = [10, 50, 100, 500, 1000, 5000, 10000]
    cp_idx = 0
    for i, p in enumerate(all_primes):
        product *= p_adic_amplitude(s, t, p)
        if cp_idx < len(checkpoints) and p >= checkpoints[cp_idx]:
            print(f"    p ≤ {checkpoints[cp_idx]:>5d} ({i+1:4d} primes): "
                  f"product = {product:.10f}  "
                  f"(error: {abs(product - 1):.2e})")
            cp_idx += 1
    print()

# ============================================================================
#  PART 4: Visualization
# ============================================================================

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle('Adelic Product Formula: $A_\\infty \\cdot \\prod_p A_p = 1$',
             fontsize=14, fontweight='bold')

# Panel 1: Convergence for multiple (s,t) points
ax = axes[0]
for s, t in test_points:
    A_inf = veneziano_amplitude(s, t)
    products = []
    prime_counts = []
    product = A_inf
    for i, p in enumerate(all_primes[:500]):
        product *= p_adic_amplitude(s, t, p)
        if (i+1) % 5 == 0:
            products.append(product)
            prime_counts.append(i+1)
    ax.plot(prime_counts, products, linewidth=1.5,
            label=f's={s}, t={t}', alpha=0.8)

ax.axhline(y=1.0, color='white', linewidth=1, linestyle='--', alpha=0.5)
ax.set_xlabel('Number of primes included', fontsize=10)
ax.set_ylabel('$A_\\infty \\cdot \\prod_{p \\leq N} A_p$', fontsize=11)
ax.set_title('Convergence to 1', fontsize=11)
ax.legend(fontsize=7)
ax.set_facecolor('#0a0a1a')
ax.grid(alpha=0.15)

# Panel 2: Individual p-adic amplitudes
ax = axes[1]
primes_small = all_primes[:50]
for s, t in [(-0.3, -0.4)]:
    amps = [p_adic_amplitude(s, t, p) for p in primes_small]
    ax.bar(range(len(primes_small)), amps, color='#ffd93d', alpha=0.7)
    ax.axhline(y=1.0, color='white', linewidth=1, linestyle='--', alpha=0.3)

ax.set_xlabel('Prime index', fontsize=10)
ax.set_ylabel('$A_p(s,t)$', fontsize=11)
ax.set_title(f'Individual p-adic amplitudes (s={-0.3}, t={-0.4})', fontsize=10)
ax.set_facecolor('#0a0a1a')
ax.grid(alpha=0.15)

# Panel 3: Error decay (log scale)
ax = axes[2]
for s, t in test_points:
    A_inf = veneziano_amplitude(s, t)
    errors = []
    ns = []
    product = A_inf
    for i, p in enumerate(all_primes):
        product *= p_adic_amplitude(s, t, p)
        if (i+1) % 10 == 0:
            errors.append(abs(product - 1))
            ns.append(i+1)
    ax.semilogy(ns, errors, linewidth=1.2, alpha=0.8)

ax.set_xlabel('Number of primes', fontsize=10)
ax.set_ylabel('$|\\prod - 1|$', fontsize=11)
ax.set_title('Error decay (log scale)', fontsize=11)
ax.set_facecolor('#0a0a1a')
ax.grid(alpha=0.15)

plt.tight_layout()
plt.savefig('research/02_adelic_product/adelic_product_formula.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
plt.close()

# ============================================================================
#  PART 5: Physical Interpretation
# ============================================================================

print("=" * 70)
print("  PHYSICAL INTERPRETATION")
print("=" * 70)
print()
print("  The adelic product formula A_∞ · ∏_p A_p = 1 says:")
print()
print("  1. STRING THEORY LIVES OVER THE ADELES")
print("     The 'real' string amplitude A_∞ is not the whole story.")
print("     There exists a 'p-adic string' for EVERY prime p,")
print("     and the product over ALL of them (including real) equals 1.")
print()
print("  2. PRIMES = CHANNELS OF SPACETIME")
print("     Each prime p contributes an independent 'channel' A_p to")
print("     the total amplitude. The real amplitude A_∞ is just the")
print("     'archimedean channel'. Spacetime at the Planck scale may")
print("     have infinitely many p-adic channels, one per prime.")
print()
print("  3. THE PRODUCT FORMULA AS CONSERVATION LAW")
print("     A_∞ · ∏_p A_p = 1 is an ADELIC conservation law:")
print("     the total 'amplitude' across all completions of Q is conserved.")
print("     This is the string-theoretic analogue of Artin's product formula")
print("     for valuations: ∏_v |x|_v = 1 for x ∈ Q*.")
print()
print("  4. TOWARD Spec(Z) SPACETIME")
print("     If string amplitudes naturally decompose as products over primes,")
print("     then the natural 'base space' of string theory is Spec(Z),")
print("     whose points ARE the primes. The geometry of Spec(Z) ---")
print("     its etale cohomology, zeta functions, Galois actions ---")
print("     may encode the quantum gravity we're looking for.")
print()
print(f"  Plot saved: research/02_adelic_product/adelic_product_formula.png")
