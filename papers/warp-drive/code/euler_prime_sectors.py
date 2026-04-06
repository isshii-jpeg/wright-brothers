"""
euler_prime_sectors.py

Exploration of the hypothesis that different primes in the Euler
product correspond to different cosmological sectors:
  p=2 → dark energy (established: Ω_Λ = 2π/9)
  p=3 → dark matter?
  p=5 → baryonic matter?

Systematic computation of all possible single-prime and multi-prime
assignments to cosmological density parameters Ω_Λ, Ω_dm, Ω_b,
testing against observed values and the flatness constraint Σ Ω = 1.
"""

import numpy as np
from fractions import Fraction
from itertools import combinations, permutations
from sympy import bernoulli, pi, Rational, Float, N

print("=" * 70)
print("EULER PRODUCT PRIME SECTORS: COSMOLOGICAL ASSIGNMENT")
print("=" * 70)

# Observed values (Planck 2018)
OBS = {
    'Omega_Lambda': 0.6847,
    'Omega_dm': 0.2645,
    'Omega_b': 0.0493,
    'Omega_m': 0.3153,  # dm + b
}

print(f"\nObserved (Planck 2018):")
for k, v in OBS.items():
    print(f"  {k} = {v}")

# =====================================================================
# 1. Single-prime Ω values: Ω(p) = (8π/3) × (p-1)/12
# =====================================================================

print("\n" + "=" * 70)
print("SECTION 1: Ω(p) = (8π/3)(p-1)/12 for each prime")
print("=" * 70)

def omega_single(p):
    """Ω from single-prime removal at s=-1."""
    return float(Rational(8, 3) * pi * Rational(p - 1, 12))

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23]
print(f"\n{'p':>5} {'Ω(p)':>10} {'Physical?':>10}")
print("-" * 30)
for p in primes:
    o = omega_single(p)
    phys = "✓" if o < 1 else "✗"
    print(f"{p:>5} {o:>10.4f} {phys:>10}")

# =====================================================================
# 2. Alternative: what if sectors use DIFFERENT formulas?
# =====================================================================

print("\n" + "=" * 70)
print("SECTION 2: Alternative sector formulas")
print("=" * 70)
print("Maybe different sectors use different powers of (p-1)/12")

# Try: Ω_sector(p) = c × |(1-p^n) × ζ(-n)| for various n
# At s=-1: (p-1)/12
# At s=-3: (p³-1)/120
# At s=-5: (p⁵-1)/252

def zeta_neg(n):
    B = bernoulli(n + 1)
    return Rational(-B, n + 1)

def sector_value(p, n):
    """|(1-p^n) × ζ(-n)| without the 8π/3 prefactor."""
    return abs((1 - p**n) * zeta_neg(n))

print(f"\n|ζ_{{¬p}}(-n)| values:")
print(f"{'p':>5} {'s=-1':>12} {'s=-3':>12} {'s=-5':>12}")
print("-" * 45)
for p in [2, 3, 5, 7]:
    vals = [float(sector_value(p, n)) for n in [1, 3, 5]]
    print(f"{p:>5} {vals[0]:>12.6f} {vals[1]:>12.6f} {vals[2]:>12.6f}")

# =====================================================================
# 3. CKN-style: Ω = (8π/3) × coefficient
# Try ALL primes at ALL s values, compare to observed Ω values
# =====================================================================

print("\n" + "=" * 70)
print("SECTION 3: Systematic search — which (p, n) matches which Ω?")
print("=" * 70)
print("Computing Ω(p,n) = (8π/3) × |(1-p^n)ζ(-n)| for various p, n")

targets = {
    'Ω_Λ': 0.6847,
    'Ω_dm': 0.2645,
    'Ω_b': 0.0493,
}

results = []
print(f"\n{'p':>3} {'n':>3} {'Ω(p,n)':>12} {'Closest to':>12} {'Error':>10}")
print("-" * 45)

for p in [2, 3, 5, 7, 11]:
    for n in [1, 3, 5, 7]:
        val = float(Rational(8, 3) * pi * sector_value(p, n))
        # Find closest target
        best_target = None
        best_err = float('inf')
        for name, obs in targets.items():
            err = abs(val - obs) / obs
            if err < best_err:
                best_err = err
                best_target = name
        if val < 2:  # only show "reasonable" values
            results.append((p, n, val, best_target, best_err))
            marker = " ★" if best_err < 0.1 else ""
            print(f"{p:>3} {n:>3} {val:>12.4f} {best_target:>12} {best_err:>9.1%}{marker}")

# =====================================================================
# 4. DIFFERENT APPROACH: Ratios between Euler factors
# =====================================================================

print("\n" + "=" * 70)
print("SECTION 4: Ratios approach — Ω_dm/Ω_Λ from prime ratios")
print("=" * 70)
print("If Ω_Λ = (8π/3)(1/12) from p=2, maybe Ω_dm = Ω_Λ × f(p) for some p")

obs_ratio_dm = OBS['Omega_dm'] / OBS['Omega_Lambda']
obs_ratio_b = OBS['Omega_b'] / OBS['Omega_Lambda']
print(f"\nObserved ratios:")
print(f"  Ω_dm/Ω_Λ = {obs_ratio_dm:.4f}")
print(f"  Ω_b/Ω_Λ  = {obs_ratio_b:.4f}")

print(f"\nCandidate arithmetic ratios:")
candidates = [
    ("1/p for p=3", 1/3),
    ("1/p for p=5", 1/5),
    ("(p-1)/(q-1) for 3,2", 2/1),
    ("ln(2)/ln(3)", np.log(2)/np.log(3)),
    ("1/e", 1/np.e),
    ("1/π", 1/np.pi),
    ("2/π²", 2/np.pi**2),
    ("B_2 = 1/6", 1/6),
    ("B_4 = 1/30", 1/30),
    ("|ζ(-3)/ζ(-1)|", (1/120)/(1/12)),
    ("|ζ(-5)/ζ(-1)|", (1/252)/(1/12)),
    ("ln(2)", np.log(2)),
    ("1/(2π)", 1/(2*np.pi)),
    ("3/(8π)", 3/(8*np.pi)),
    ("(3-1)/(8π/3)", 2/(8*np.pi/3)),
    ("1/ζ(2) = 6/π²", 6/np.pi**2),
]

print(f"\n{'Expression':>25} {'Value':>10} {'vs Ω_dm/Ω_Λ':>12} {'vs Ω_b/Ω_Λ':>12}")
print("-" * 65)
for name, val in candidates:
    err_dm = abs(val - obs_ratio_dm) / obs_ratio_dm
    err_b = abs(val - obs_ratio_b) / obs_ratio_b
    dm_marker = " ★" if err_dm < 0.05 else ""
    b_marker = " ★" if err_b < 0.05 else ""
    print(f"{name:>25} {val:>10.4f} {err_dm:>11.1%}{dm_marker} {err_b:>11.1%}{b_marker}")

# =====================================================================
# 5. FLATNESS: Can we find (p_Λ, p_dm, p_b) assignment with Σ Ω = 1?
# =====================================================================

print("\n" + "=" * 70)
print("SECTION 5: Flatness constraint — find 3-prime assignment")
print("=" * 70)
print("Need: Ω(p_Λ, n_Λ) + Ω(p_dm, n_dm) + Ω(p_b, n_b) = 1")
print("With each Ω computed from a (prime, s-value) pair")

# Build a table of all reasonable (p, n) → Ω values
all_omega = {}
for p in [2, 3, 5, 7, 11, 13]:
    for n in [1, 3, 5, 7, 9]:
        val = float(Rational(8, 3) * pi * sector_value(p, n))
        if 0.001 < val < 1.5:
            all_omega[(p, n)] = val

print(f"\nAvailable (p, n) → Ω values (in physical range):")
for (p, n), val in sorted(all_omega.items()):
    print(f"  p={p}, s=-{n}: Ω = {val:.4f}")

# Search for triples that sum to ~1
print(f"\nSearching for triples (Λ, dm, b) summing to 1.000 ± 0.05...")
print(f"{'Λ':>12} {'dm':>12} {'b':>12} {'Sum':>8} {'Error':>8}")
print("-" * 55)

best_combos = []
keys = list(all_omega.keys())
for i in range(len(keys)):
    for j in range(len(keys)):
        for k in range(len(keys)):
            if i == j or j == k or i == k:
                continue
            ki, kj, kk = keys[i], keys[j], keys[k]
            s = all_omega[ki] + all_omega[kj] + all_omega[kk]
            if abs(s - 1.0) < 0.05:
                # Also check if assignments make sense
                vals = sorted([(all_omega[ki], ki), (all_omega[kj], kj), (all_omega[kk], kk)], reverse=True)
                best_combos.append((vals, s))

# Remove duplicates and sort by closeness to 1
seen = set()
unique_combos = []
for vals, s in best_combos:
    key = tuple(sorted([v[1] for v in vals]))
    if key not in seen:
        seen.add(key)
        unique_combos.append((vals, s))

unique_combos.sort(key=lambda x: abs(x[1] - 1.0))

for vals, s in unique_combos[:15]:
    labels = [f"p={v[1][0]},s=-{v[1][1]}" for v in vals]
    omegas = [v[0] for v in vals]
    err = abs(s - 1.0)
    print(f"  {labels[0]:>12} ({omegas[0]:.3f}) + {labels[1]:>12} ({omegas[1]:.3f}) + {labels[2]:>12} ({omegas[2]:.3f}) = {s:.4f} (err={err:.4f})")

# =====================================================================
# 6. MOST INTERESTING: the "p=2 only" universe
# =====================================================================

print("\n" + "=" * 70)
print("SECTION 6: Can ALL sectors come from p=2 at different s?")
print("=" * 70)

print(f"\np=2 Euler factor at various s:")
for n in [1, 3, 5, 7, 9, 11, 13]:
    coeff = sector_value(2, n)
    omega = float(Rational(8, 3) * pi * coeff)
    print(f"  s=-{n}: |ζ_{{¬2}}(-{n})| = {float(coeff):.6f}, Ω = {omega:.4f}")

print(f"\nCan we decompose: Ω_Λ(s=-1) + Ω_dm(s=-?) + Ω_b(s=-?) = 1?")
print(f"  Ω_Λ = (8π/3)(1/12) = {omega_single(2):.4f}")

remaining = 1.0 - omega_single(2)
print(f"  Remaining for matter: 1 - {omega_single(2):.4f} = {remaining:.4f}")
print(f"  Observed Ω_m = {OBS['Omega_m']}")

# Check p=2 at s=-3
omega_2_3 = float(Rational(8, 3) * pi * sector_value(2, 3))
print(f"\n  Ω(p=2, s=-3) = (8π/3)(7/120) = {omega_2_3:.4f}")
print(f"  Observed Ω_dm = {OBS['Omega_dm']}")
print(f"  Difference: {abs(omega_2_3 - OBS['Omega_dm']):.4f} ({abs(omega_2_3 - OBS['Omega_dm'])/OBS['Omega_dm']*100:.1f}%)")

# What about Ω_b?
omega_b_needed = 1.0 - omega_single(2) - omega_2_3
print(f"\n  If Ω_Λ from s=-1 and Ω_dm from s=-3:")
print(f"  Ω_b = 1 - Ω_Λ - Ω_dm = 1 - {omega_single(2):.4f} - {omega_2_3:.4f} = {omega_b_needed:.4f}")
print(f"  Observed Ω_b = {OBS['Omega_b']}")

# =====================================================================
# 7. REFINED: Different normalization for matter sector
# =====================================================================

print("\n" + "=" * 70)
print("SECTION 7: What if matter uses a DIFFERENT normalization?")
print("=" * 70)
print("CKN bound gives (8π/3) for vacuum. Matter might use different prefactor.")

# If Ω_dm = c × |ζ_{¬2}(-3)|, what c is needed?
needed_c_dm = OBS['Omega_dm'] / float(sector_value(2, 3))
print(f"\n  For Ω_dm = c × |ζ_{{¬2}}(-3)| = c × 7/120:")
print(f"  Need c = {needed_c_dm:.4f}")
print(f"  Compare to 8π/3 = {float(8*pi/3):.4f}")
print(f"  Ratio c/(8π/3) = {needed_c_dm/float(8*pi/3):.4f}")

# If Ω_b = c' × |ζ_{¬2}(-5)|, what c' is needed?
needed_c_b = OBS['Omega_b'] / float(sector_value(2, 5))
print(f"\n  For Ω_b = c' × |ζ_{{¬2}}(-5)| = c' × 31/252:")
print(f"  Need c' = {needed_c_b:.4f}")
print(f"  Compare to 8π/3 = {float(8*pi/3):.4f}")
print(f"  Ratio c'/(8π/3) = {needed_c_b/float(8*pi/3):.4f}")

# =====================================================================
# 8. THE RATIO APPROACH
# =====================================================================

print("\n" + "=" * 70)
print("SECTION 8: Ω ratios from ζ ratios (normalization-free)")
print("=" * 70)
print("If all Ω use SAME normalization, ratios cancel the prefactor:")

print(f"\n  Ω_dm/Ω_Λ (observed) = {OBS['Omega_dm']/OBS['Omega_Lambda']:.4f}")
print(f"  |ζ_{{¬2}}(-3)|/|ζ_{{¬2}}(-1)| = (7/120)/(1/12) = 7/10 = {7/10:.4f}")
print(f"  Match: {abs(7/10 - OBS['Omega_dm']/OBS['Omega_Lambda'])/(OBS['Omega_dm']/OBS['Omega_Lambda'])*100:.1f}% off")

print(f"\n  Ω_b/Ω_Λ (observed) = {OBS['Omega_b']/OBS['Omega_Lambda']:.4f}")
print(f"  |ζ_{{¬2}}(-5)|/|ζ_{{¬2}}(-1)| = (31/252)/(1/12) = 31/21 = {31/21:.4f}")
print(f"  Way too large. s=-5 doesn't work for Ω_b.")

# Try s=-3 for dm, s=-7 for b?
r_7 = float(sector_value(2, 7)) / float(sector_value(2, 1))
print(f"\n  |ζ_{{¬2}}(-7)|/|ζ_{{¬2}}(-1)| = (127/240)/(1/12) = 127/20 = {127/20:.4f}")
print(f"  Too large for Ω_b/Ω_Λ.")

# What about using ζ (not ζ_{¬2}) for matter?
print(f"\n  What if MATTER uses full ζ (not truncated)?")
print(f"  |ζ(-3)|/|ζ_{{¬2}}(-1)| = (1/120)/(1/12) = 1/10 = {1/10:.4f}")
print(f"  vs Ω_dm/Ω_Λ = {OBS['Omega_dm']/OBS['Omega_Lambda']:.4f}")
print(f"  Match: {abs(0.1 - OBS['Omega_dm']/OBS['Omega_Lambda'])/(OBS['Omega_dm']/OBS['Omega_Lambda'])*100:.1f}% off")

print(f"\n  |ζ(-5)|/|ζ_{{¬2}}(-1)| = (1/252)/(1/12) = 1/21 = {1/21:.4f}")
print(f"  vs Ω_b/Ω_Λ = {OBS['Omega_b']/OBS['Omega_Lambda']:.4f}")
print(f"  Match: {abs(1/21 - OBS['Omega_b']/OBS['Omega_Lambda'])/(OBS['Omega_b']/OBS['Omega_Lambda'])*100:.1f}% off")

# =====================================================================
# 9. KEY TEST: the "all from p=2, different s" hypothesis
# =====================================================================

print("\n" + "=" * 70)
print("SECTION 9: ALL FROM p=2 HYPOTHESIS")
print("=" * 70)
print("""
Hypothesis: All cosmological densities come from p=2 Euler truncation
at different negative integer arguments:

  Ω_Λ  = (8π/3) × |ζ_{¬2}(-1)| = (8π/3)(1/12)  = 2π/9
  Ω_dm  = (8π/3) × |ζ(-3)|      = (8π/3)(1/120)  = π/45  ?
  Ω_b   = (8π/3) × |ζ(-5)|      = (8π/3)(1/252)  = 4π/189 ?

Note: Ω_dm and Ω_b might use FULL ζ (not truncated), because
matter modes are DD/NN (all harmonics), not DN (odd only).
Only vacuum (dark energy) uses DN → ζ_{¬2}.
""")

omega_L = float(Rational(8,3) * pi / 12)
omega_dm_hyp = float(Rational(8,3) * pi / 120)
omega_b_hyp = float(Rational(8,3) * pi / 252)
total = omega_L + omega_dm_hyp + omega_b_hyp

print(f"  Ω_Λ  = 2π/9     = {omega_L:.4f}  (obs: {OBS['Omega_Lambda']:.4f}, {abs(omega_L-OBS['Omega_Lambda'])/OBS['Omega_Lambda']*100:.1f}%)")
print(f"  Ω_dm = π/45     = {omega_dm_hyp:.4f}  (obs: {OBS['Omega_dm']:.4f}, {abs(omega_dm_hyp-OBS['Omega_dm'])/OBS['Omega_dm']*100:.1f}%)")
print(f"  Ω_b  = 4π/189   = {omega_b_hyp:.4f}  (obs: {OBS['Omega_b']:.4f}, {abs(omega_b_hyp-OBS['Omega_b'])/OBS['Omega_b']*100:.1f}%)")
print(f"  Total            = {total:.4f}  (should be 1.000)")
print(f"  Flatness error   = {abs(total-1.0):.4f}")

print(f"\n  Ω_dm/Ω_Λ predicted = {omega_dm_hyp/omega_L:.4f} = (1/120)/(1/12) = 1/10")
print(f"  Ω_dm/Ω_Λ observed  = {OBS['Omega_dm']/OBS['Omega_Lambda']:.4f}")
print(f"  Agreement: {abs(omega_dm_hyp/omega_L - OBS['Omega_dm']/OBS['Omega_Lambda'])/(OBS['Omega_dm']/OBS['Omega_Lambda'])*100:.1f}%")

# =====================================================================
# 10. SUMMARY
# =====================================================================

print(f"""
{'='*70}
SECTION 10: SUMMARY OF FINDINGS
{'='*70}

HYPOTHESIS TESTED:
  Different primes OR different s-values in the Euler product
  correspond to different cosmological sectors.

RESULTS:

1. SINGLE-PRIME ASSIGNMENT (p_Λ, p_dm, p_b) = (2, 3, 5):
   FAILS. Ω(p=3) = 4π/9 > 1, unphysical.

2. "ALL FROM p=2, DIFFERENT s" HYPOTHESIS:
   Ω_Λ  = (8π/3)|ζ_{{¬2}}(-1)| = 2π/9  = {omega_L:.4f} (obs {OBS['Omega_Lambda']:.4f}, 2% off)
   Ω_dm = (8π/3)|ζ(-3)|       = π/45   = {omega_dm_hyp:.4f} (obs {OBS['Omega_dm']:.4f}, 74% off)  ← BAD
   Ω_b  = (8π/3)|ζ(-5)|       = 4π/189 = {omega_b_hyp:.4f} (obs {OBS['Omega_b']:.4f}, 35% off)  ← BAD

   Flatness: {total:.4f} (should be 1). OFF BY {abs(total-1)*100:.1f}%.

   VERDICT: FAILS for dm and b. Only works for Λ.

3. RATIO APPROACH (normalization-free):
   Ω_dm/Ω_Λ = |ζ(-3)|/|ζ_{{¬2}}(-1)| = 1/10 = 0.100
   Observed = {OBS['Omega_dm']/OBS['Omega_Lambda']:.4f}
   74% off. DOES NOT WORK.

   Ω_dm/Ω_Λ = |ζ_{{¬2}}(-3)|/|ζ_{{¬2}}(-1)| = 7/10 = 0.700
   Observed = {OBS['Omega_dm']/OBS['Omega_Lambda']:.4f}
   81% off. DOES NOT WORK.

4. HONEST CONCLUSION:
   The Euler product prime-sector hypothesis DOES NOT extend
   to dark matter or baryonic matter in any simple form tested.

   Dark energy (Ω_Λ = 2π/9) remains the ONLY cosmological
   quantity successfully predicted by the arithmetic framework.

   Dark matter and baryonic matter densities appear to be
   determined by DYNAMICAL processes (freeze-out, baryogenesis),
   not by vacuum arithmetic structure.

   THIS IS AN HONEST NEGATIVE RESULT that confirms the scope
   limitation of the Wright Brothers framework.
""")
