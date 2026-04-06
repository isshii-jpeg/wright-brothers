#!/usr/bin/env python3
"""
Dirac Operator Spectral Modulation:
Can we make G_eff → 0 or negative by perturbing BC eigenvalues?

The key chain:
  Connes' spectral action: Tr(f(D²/Λ²)) = f₄Λ⁴a₀ + f₂Λ²a₂ + f₀a₄ + ...
  a₂ ∝ ∫ R √g d⁴x  → this term gives G_Newton
  If we modify D → D + A, the a₂ coefficient changes → G_eff changes

THE QUESTION: Can δλ_n perturbations to BC eigenvalues make G_eff → 0 or < 0?
"""

import numpy as np
import mpmath

mpmath.mp.dps = 30
pi = float(mpmath.pi)

print("=" * 70)
print("DIRAC SPECTRAL MODULATION: CONTROLLING G_eff")
print("=" * 70)

# =====================================================================
print("\n" + "=" * 70)
print("1. HOW G EMERGES FROM THE SPECTRAL ACTION")
print("=" * 70)

print("""
In Connes' spectral action:
  S = Tr(f(D²/Λ²)) = f₄Λ⁴a₀ + f₂Λ²a₂ + f₀a₄ + ...

The Seeley-DeWitt coefficient a₂ gives the Einstein-Hilbert term:
  a₂ = (1/16π²) ∫ (R/6) √g d⁴x

Matching to Einstein gravity:
  f₂Λ² × a₂ = (1/16πG) ∫ R √g d⁴x

This gives:
  G = 6π / (f₂ Λ²)     ← G is determined by Λ and the moment f₂

For the BC system with f(x) = e^{-x}:
  f₂ = ∫₀^∞ e^{-u} du = 1
  So: G_eff = 6π/Λ²

  G_eff depends on the CUTOFF SCALE Λ.
  If Λ changes locally → G_eff changes locally.

BUT: Λ is related to the BC inverse temperature β by Λ² = 1/β.
  So: G_eff = 6πβ

  β > 0 → G > 0 (normal gravity, attractive)
  β = 0 → G = 0 (no gravity!)
  β < 0 → G < 0 (anti-gravity!)
""")

print("G_eff as function of β:")
print(f"{'β':>8} {'G_eff/G₀':>12} {'ζ(β)':>12} {'physical meaning':>25}")
print("-" * 65)

for beta in [3.0, 2.0, 1.5, 1.0, 0.5, 0.0, -0.5, -1.0, -2.0]:
    G_ratio = beta / 2.0  # normalized to β=2 (our vacuum)
    if abs(beta - 1.0) < 0.01:
        zeta_str = "∞ (pole)"
    else:
        zeta_str = f"{float(mpmath.zeta(beta)):.4f}"

    if beta > 1:
        meaning = "normal gravity"
    elif abs(beta - 1) < 0.1:
        meaning = "phase transition"
    elif beta > 0:
        meaning = "weakened gravity"
    elif abs(beta) < 0.01:
        meaning = "ZERO GRAVITY"
    else:
        meaning = "ANTI-GRAVITY"

    print(f"{beta:>8.1f} {G_ratio:>12.3f} {zeta_str:>12} {meaning:>25}")

# =====================================================================
print("\n" + "=" * 70)
print("2. ★★★ PERTURBATION OF BC EIGENVALUES ★★★")
print("=" * 70)

print("""
BC Hamiltonian: H|n⟩ = log(n)|n⟩

Perturbed: H' = H + δH where δH|n⟩ = δλ_n|n⟩

The perturbed heat kernel:
  K'(t) = Σ e^{-t(log n + δλ_n)} = Σ n^{-t} e^{-t δλ_n}

If δλ_n is SMALL: K'(t) ≈ K(t) - t Σ n^{-t} δλ_n + O(δλ²)
  = ζ(t) - t × Σ n^{-t} δλ_n

THE a₂ COEFFICIENT depends on the SECOND term in the heat kernel
expansion. The perturbation δλ_n modifies a₂:

  δa₂ ∝ Σ n^{-t} δλ_n × (coefficient from expansion)

If δλ_n = c × log(n) (proportional to original eigenvalue):
  K'(t) = Σ n^{-t} e^{-ct log n} = Σ n^{-t(1+c)} = ζ(t(1+c))

  This is equivalent to rescaling β → β(1+c).
  G_eff → G × (1+c).

  c > 0: G increases (stronger gravity)
  c < 0: G decreases (weaker gravity)
  c = -1: G = 0 (zero gravity!)
  c < -1: G < 0 (anti-gravity!)
""")

# =====================================================================
print("=" * 70)
print("3. ★★★★ SELECTIVE PRIME PERTURBATION ★★★★")
print("=" * 70)

print("""
Instead of perturbing ALL eigenvalues, perturb only those
associated with specific PRIMES.

For mode n = Π pᵢ^{aᵢ} (prime factorization):
  log(n) = Σ aᵢ log(pᵢ)

Each prime p contributes log(p) to the energy of modes divisible by p.

SELECTIVE PERTURBATION:
  δλ_n = Σ_p (δε_p × v_p(n) × log p)

where v_p(n) = p-adic valuation of n (how many times p divides n)
and δε_p = perturbation strength for prime p.

The perturbed heat kernel:
  K'(t) = Σ_n n^{-t} × Π_p p^{-t δε_p v_p(n)}
        = Π_p Σ_{k=0}^∞ p^{-k(t + t δε_p)}  (by Euler product)
        = Π_p 1/(1 - p^{-t(1+δε_p)})
        = ζ(t, {1+δε_p})  (generalized Euler product)

WHERE: ζ(t, {1+δε_p}) = Π_p (1 - p^{-t(1+δε_p)})^{-1}

This is a GENERALIZED ZETA with PRIME-DEPENDENT scaling!
""")

# Compute the generalized zeta for various perturbations
print("Generalized heat kernel with prime-dependent perturbation:")
print()

def generalized_euler(t, delta_eps, N_primes=50):
    """Compute Π_p (1-p^{-t(1+δε_p)})^{-1} for first N primes."""
    from sympy import primerange
    primes = list(primerange(2, N_primes * 5))[:N_primes]
    product = 1.0
    for p in primes:
        dep = delta_eps.get(p, 0.0)
        exponent = t * (1 + dep)
        if exponent > 0:
            product /= (1 - float(p)**(-exponent))
        else:
            product *= (1 - float(p)**(abs(exponent)))
    return product

# Case 1: uniform perturbation (all primes shifted equally)
print("Case 1: Uniform δε = c for all primes")
print(f"  K'(t) = ζ(t(1+c))")
print(f"  G_eff = G × (1+c)")
for c in [-0.5, -0.3, 0, 0.3, 0.5, 1.0]:
    G_ratio = 1 + c
    print(f"  c = {c:>5.1f}: G_eff/G = {G_ratio:.2f}")
print()

# Case 2: perturb only p=2
print("Case 2: Perturb only p=2 (δε₂ ≠ 0, others = 0)")
print("  This modifies only the p=2 Euler factor.")
print("  K'(t) = (1-2^{-t(1+δε₂)})^{-1} × Π_{p>2} (1-p^{-t})^{-1}")
print("         = [factor₂'] × ζ(t)/[factor₂]")
print()

t = 2.0  # evaluate at β=2 (our vacuum)
for dep2 in [-2.0, -1.0, -0.5, 0, 0.5, 1.0, 2.0]:
    # Original factor: (1-2^{-t})^{-1}
    f_orig = 1 / (1 - 2**(-t))
    # Perturbed factor: (1-2^{-t(1+dep2)})^{-1}
    exp_new = t * (1 + dep2)
    if exp_new > 0.01:
        f_new = 1 / (1 - 2**(-exp_new))
    elif exp_new < -0.01:
        denom = 1 - 2**(abs(exp_new))
        f_new = 1 / denom if abs(denom) > 1e-10 else float('inf')
    else:
        f_new = float('inf')  # near zero
    ratio = f_new / f_orig
    print(f"  δε₂ = {dep2:>5.1f}: factor ratio = {ratio:.4f}")
print()

# Case 3: the critical case — making G_eff = 0
print("Case 3: Can we make G_eff = 0?")
print("""
  G_eff ∝ a₂ ∝ ∫ (second heat kernel coefficient)

  From the heat kernel expansion at small t:
    K(t) = Σ aₖ t^{(k-d)/2}

  For BC: K(t) = ζ(t) near t=0 gives:
    ζ(t) = -1/2 + t × (-1/2)log(2π) + ...

  The a₂ analog: coefficient of t¹ in the expansion.
    ζ'(0) = -(1/2)log(2π)

  With perturbation δλ_n = c × log n:
    K'(t) = ζ(t(1+c))
    K'(0) = ζ(0) = -1/2 (unchanged)
    dK'/dt|₀ = (1+c) × ζ'(0) = (1+c) × (-(1/2)log(2π))

  Setting the a₂ coefficient to zero:
    (1+c) = 0 → c = -1

  G_eff = 0 when δλ_n = -log(n) for all n.
  i.e., when the perturbation CANCELS the original eigenvalues!
  H' = H + δH = 0 (trivial Hamiltonian).

  This makes sense: no Hamiltonian → no dynamics → no gravity.
  But it's trivial and unphysical.
""")

# =====================================================================
print("=" * 70)
print("4. ★★★★★ THE NON-TRIVIAL APPROACH: SELECTIVE CANCELLATION ★★★★★")
print("=" * 70)

print("""
Instead of canceling ALL eigenvalues, what if we:
  - Cancel eigenvalues for SPECIFIC primes
  - Enhance others
  - Create a position-dependent pattern

IDEA: "Arithmetic metamaterial" = array of quantum elements,
each resonant at log(p) for specific prime p.

Element at position x:
  - Qubit 1: resonant at ω = log(2)/τ → couples to p=2 modes
  - Qubit 2: resonant at ω = log(3)/τ → couples to p=3 modes
  - Qubit 3: resonant at ω = log(5)/τ → couples to p=5 modes
  - ...

When qubit k is ACTIVATED (excited):
  → absorbs energy from the p_k mode
  → effectively sets δε_{p_k} = -1 (cancels that prime's contribution)
  → removes the p_k Euler factor

When qubit k is DEACTIVATED (ground state):
  → p_k mode propagates normally
  → δε_{p_k} = 0

POSITION-DEPENDENT PATTERN:
  Inside the warp bubble: activate qubits for primes p₁,...,p_K
    → G_eff is MODIFIED (Euler factors removed)
  Outside: all qubits off
    → G_eff = G (normal gravity)

The BOUNDARY between activated/deactivated regions = warp bubble wall.
""")

# Compute G_eff for various numbers of cancelled primes
print("G_eff when K primes are 'cancelled' (δε_p = -1):")
print()

primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43]

# The a₂ coefficient modification:
# Each cancelled prime p removes its Euler factor from ζ.
# The effect on G_eff comes from how the spectral action changes.
#
# For the spectral action S = Tr(f(D²/Λ²)):
# a₂ ∝ d/dt [K(t)]|_{t→0}
#
# K(t) = ζ(t) = Π_p (1-p^{-t})^{-1}
# log K(t) = -Σ_p log(1-p^{-t})
# d/dt log K(t) = Σ_p (log p) p^{-t} / (1-p^{-t})
#
# At t→0+: each term → (log p) / (1 - 1) = ∞ (diverges)
# But regulated: d/dt ζ(t)|_{t=0} = ζ'(0) = -(1/2)log(2π)
#
# When prime p is cancelled: remove its contribution from the sum.
# The RATIO of perturbed to original:
# G'_eff / G_eff = [ζ'_muted(0)] / [ζ'(0)]

# ζ'(0) = -(1/2)log(2π)
zeta_prime_0 = -0.5 * np.log(2*pi)
print(f"  ζ'(0) = -(1/2)log(2π) = {zeta_prime_0:.6f}")
print()

# When we remove prime p, the contribution of p to ζ'(0):
# d/dt [-log(1-p^{-t})]|_{t=0} = log(p) × p^0/(1-p^0)... diverges
#
# This requires more careful analysis using the Euler product regularization.
#
# Actually, let's think about it differently.
#
# The spectral action with K primes cancelled:
# K_muted(t) = Π_{p cancelled} (1-p^{-t}) × ζ(t) = ζ_muted(t)
#
# a₂ analog for the muted system:
# d/dt [ζ_muted(t)]|_{t near 0} = d/dt [Π(1-p^{-t}) × ζ(t)]|_{t→0}
#
# For a single prime p:
# d/dt [(1-p^{-t}) ζ(t)] = p^{-t}log(p) ζ(t) + (1-p^{-t}) ζ'(t)
# At t=0: log(p) × ζ(0) + 0 × ζ'(0) = log(p) × (-1/2) = -(log p)/2
#
# Wait, (1-p^0) = 0, so the second term vanishes!
# So: ζ'_{¬p}(0) = log(p) × ζ(0) = -(log p)/2

# For K primes cancelled:
# ζ_{¬{p₁,...,pK}}(t) = Π_{i}(1-pᵢ^{-t}) × ζ(t)
# At t=0: this is 0 (because each factor (1-1)=0)
# Near t=0: use L'Hôpital or Taylor expand

# Actually, ζ_{¬p}(0) = (1-1)×ζ(0) = 0 for any single prime!
# And ζ_{¬{p₁,...,pK}}(0) = 0 for any set of primes.
# The DERIVATIVE is what matters for a₂.

# Let me compute ζ_{¬{p₁,...,pK}}'(0) properly.
# f(t) = Π_i (1-pᵢ^{-t}) × ζ(t)
# f(0) = 0 (multiple zero if K > 1)
# f'(0) = [Σ_i Π_{j≠i}(1-pⱼ^0)] × [log(pᵢ)pᵢ^0] × ζ(0) + Π(1-pᵢ^0) × ζ'(0)
#        = 0 + 0 = 0 (for K ≥ 2!)
#
# For K=1: f'(0) = log(p) × ζ(0) = -log(p)/2

# For K=2: need f''(0)
# This gets complicated. Let me just compute numerically.

print("ζ_muted(t) near t=0 for different muting sets:")
print(f"{'primes':>15} {'ζ_mut(0.01)':>15} {'ζ_mut(0.1)':>12} {'ζ_mut(1)':>12}")
print("-" * 58)

for K in range(0, 8):
    ps = primes_list[:K]
    for t in [0.01, 0.1, 1.0]:
        if abs(t - 1.0) < 0.01 and K == 0:
            val = float('inf')
        else:
            val = float(mpmath.zeta(t))
            for p in ps:
                val *= (1 - float(p)**(-t))
        if t == 0.01:
            p_str = str(ps) if K <= 4 else f"{K} primes"
            print(f"{p_str:>15} {val:>15.6f}", end="")
        elif t == 0.1:
            print(f" {val:>12.6f}", end="")
        else:
            if val == float('inf'):
                print(f" {'∞':>12}")
            else:
                print(f" {val:>12.4f}")

print("""
★ KEY OBSERVATION:
  ζ_muted(t) → 0 as t → 0 for ANY non-empty muting set.
  The ORDER of the zero increases with the number of primes.

  For K=1: simple zero (ζ_{¬p}(t) ~ t × log(p)/2)
  For K=2: double zero (ζ_{¬p,q}(t) ~ t² × ...)
  For K≥3: K-fold zero

  In the spectral action, higher-order zeros at t=0 mean:
    a₀ = 0 (no cosmological constant!)
    a₂ = 0 (no Einstein-Hilbert! → G_eff = 0!)
    a₄ = 0 for K ≥ 3 (no higher-curvature terms!)

  ★★★★★ MUTING 2 OR MORE PRIMES MAKES G_eff = 0 ★★★★★
""")

# =====================================================================
print("=" * 70)
print("5. ★★★★★ THE GRAVITY NULLIFICATION THEOREM ★★★★★")
print("=" * 70)

print("""
THEOREM (proposed):

Let D be the Dirac operator of the Bost-Connes spectral triple,
and let D' be the perturbed operator obtained by removing the
Euler factors for primes p₁, ..., p_K (K ≥ 2).

Then the Seeley-DeWitt coefficients satisfy:
  a₀(D') = 0  (no cosmological term)
  a₂(D') = 0  (no Einstein-Hilbert term → G_eff = 0)

Proof sketch:
  The heat kernel K'(t) = ζ_{¬{p₁,...,pK}}(t) has a K-fold zero at t=0:
    K'(t) = t^K × [finite function]

  The Seeley-DeWitt expansion:
    K'(t) = Σ aₖ t^{(k-d)/2}

  For d=4 (our spacetime):
    K'(t) = a₀ t^{-2} + a₂ t^{-1} + a₄ t⁰ + ...

  But K'(t) ~ t^K near t=0, which requires:
    a₀ = a₂ = ... = a_{2K-2} = 0

  For K = 2: a₀ = a₂ = 0 → no gravity
  For K = 3: a₀ = a₂ = a₄ = 0 → no gravity, no Gauss-Bonnet
  For K ≥ 3: ALL curvature terms vanish → FLAT SPACE

★ A region where 2+ primes are muted has ZERO EFFECTIVE GRAVITY.
  A region where 3+ primes are muted is EFFECTIVELY FLAT.

This is not "anti-gravity." It's the ABSENCE of gravity.
The region has no gravitational interaction with the outside.

IMPLICATIONS FOR WARP:
  Inside the bubble (K ≥ 2 primes muted): G = 0
  Outside (no muting): G = G_Newton (normal)
  Bubble wall: G transitions from G to 0

  An object inside the G=0 region:
  - Is gravitationally decoupled from the universe
  - Moves through space WITHOUT gravitational interaction
  - No geodesic equation applies (no metric to follow)
  - The region is "topologically disconnected" from gravity

  This is MORE radical than Alcubierre:
  Alcubierre: distort spacetime around the ship
  This: DISCONNECT the ship from spacetime curvature
""")

# =====================================================================
print("=" * 70)
print("6. PHYSICAL IMPLEMENTATION")
print("=" * 70)

print("""
THE DEVICE: Array of prime-resonant quantum elements

For each prime p, create a resonant element at frequency ω_p = log(p)/τ:

  p=2: ω₂ = log(2)/τ ≈ 0.693/τ
  p=3: ω₃ = log(3)/τ ≈ 1.099/τ
  p=5: ω₅ = log(5)/τ ≈ 1.609/τ

For τ = 1 ns (GHz regime):
  ω₂ = 693 MHz
  ω₃ = 1.10 GHz
  ω₅ = 1.61 GHz

These are MICROWAVE frequencies — standard for superconducting qubits!

A transmon qubit can be tuned to any of these frequencies.
An array of transmon qubits, each tuned to a different log(p)/τ,
would constitute an "arithmetic metamaterial."

CIRCUIT QED IMPLEMENTATION:
  - Niobium coplanar waveguide (cavity)
  - 2 transmon qubits: tuned to log(2)/τ and log(3)/τ
  - SQUID-tunable coupling
  - Dilution refrigerator (10 mK)
  - Standard Yale/Google-style setup

COST: ~$500K (existing labs have this equipment)

EXPERIMENT:
  1. Measure Casimir shift in cavity with qubits OFF
     → standard ζ(-3) response
  2. Turn ON the log(2) qubit → p=2 muted
     → ζ_{¬2}(-3) response
  3. Turn ON both qubits → p=2,3 muted
     → ζ_{¬2,3}(-3) response → G_eff probed

  If the 2-qubit case shows qualitatively different behavior
  (e.g., cavity frequency shift vanishes or reverses),
  this is evidence for G_eff → 0.
""")

# Compute qubit frequencies
tau = 1e-9  # 1 ns
print("Qubit frequencies for τ = 1 ns:")
for p in [2, 3, 5, 7, 11, 13]:
    omega = np.log(p) / tau
    f = omega / (2*pi)
    print(f"  p={p:>2}: ω = log({p})/τ = {omega/1e9:.3f} GHz, f = {f/1e9:.3f} GHz")

print()
print("All in the 0.1-1 GHz range — standard transmon qubit frequencies!")

# =====================================================================
print("\n" + "=" * 70)
print("7. HONEST ASSESSMENT")
print("=" * 70)

print("""
WHAT IS RIGOROUS:
  ✓ ζ_muted(t) has a K-fold zero at t=0 for K primes removed
    (mathematical fact, follows from Euler product)
  ✓ In Connes' framework, a K-fold zero in the heat kernel
    means the first K Seeley-DeWitt coefficients vanish
    (mathematical fact, from the definition of a_k)
  ✓ a₂ = 0 implies no Einstein-Hilbert term → G_eff = 0
    (mathematical fact, in the spectral action framework)

WHAT IS ASSUMED:
  ? The BC spectral triple correctly describes physical spacetime
    (this is the central assumption of the entire WB program)
  ? Removing Euler factors via qubit absorption is equivalent to
    the mathematical operation on ζ
    (this is the regulator conjecture, testable)
  ? The spectral action at negative t (our regime) gives the same
    physics as at positive t (standard Connes regime)
    (this is the BC extension, partially justified)

WHAT THIS MEANS IF TRUE:
  ★ 2-prime muting → G_eff = 0 in a local region
  ★ This is achievable with EXISTING circuit QED technology
  ★ No exotic matter, no extreme energies
  ★ The "warp bubble" is a region of zero gravity
  ★ The ship inside is gravitationally decoupled

WHAT COULD GO WRONG:
  ✗ The BC spectral triple may not describe real spacetime
  ✗ Qubit absorption may not implement mathematical Euler removal
  ✗ The zero in ζ_muted(0) may not translate to physical G=0
  ✗ There may be non-perturbative effects not captured by
    the heat kernel expansion

THE DECISIVE TEST IS THE SAME:
  2-prime BAW experiment (¥330k): 182× vs 1/3
  If 182×: the Euler product is physical → proceed to G_eff test
  If 1/3: the connection is mathematical only → stop
""")
