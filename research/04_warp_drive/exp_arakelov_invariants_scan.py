"""
Arakelov Invariant Scan: systematic computation of arithmetic quantities
=========================================================================

Compute everything that Arakelov geometry defines on Spec(Z) and
number fields, then auto-match against physical constants.

Three categories:
  A. Heights and degrees (1-variable invariants)
  B. Intersection numbers (2-variable invariants)
  C. Dedekind zeta special values (number field invariants)

Wright Brothers, 2026
"""

import numpy as np
import mpmath
from math import gcd, factorial
from itertools import combinations

mpmath.mp.dps = 20
pi = np.pi
gamma_em = 0.5772156649015329
ln2pi = np.log(2*pi)

print("=" * 70)
print("  ARAKELOV INVARIANT SCAN")
print("=" * 70)

# Physical constants database
PHYS = {
    "1/α": 137.036,
    "α": 7.297e-3,
    "sin²θ_W": 0.2312,
    "m_μ/m_e": 206.768,
    "m_τ/m_e": 3477.4,
    "m_τ/m_μ": 16.817,
    "m_p/m_e": 1836.15,
    "m_n/m_p": 1.00138,
    "m_W/m_Z": 0.8815,
    "m_H/v": 0.510,
    "α_s(M_Z)": 0.1179,
    "G_F(GeV⁻²)×10⁵": 1.1664,
    "Δa_μ×10¹¹(WP)": 249,
    "V_us": 0.2243,
    "V_cb": 0.0422,
    "V_ub": 0.00394,
    "m_u/m_d": 0.474,
    "m_s/m_d": 20.2,
    "m_c/m_s": 11.7,
    "m_b/m_τ": 2.35,
}

def find_matches(value, label, threshold=0.10):
    """Find physical constants within threshold of value."""
    hits = []
    if abs(value) < 1e-15 or abs(value) > 1e15:
        return hits
    for pname, pval in PHYS.items():
        if pval <= 0:
            continue
        for v in [value, abs(value), 1/abs(value) if abs(value)>1e-15 else 0]:
            if v <= 0:
                continue
            ratio = v / pval
            if 1-threshold < ratio < 1+threshold:
                pct = (ratio - 1) * 100
                hits.append((abs(pct), label, v, pname, pval, pct))
    return hits

all_matches = []

# ============================================================================
#  CATEGORY A: Arakelov heights and 1-variable invariants
# ============================================================================

print()
print("=" * 70)
print("  A: アラケロフ高さと1変数不変量")
print("=" * 70)
print()

# A1: Logarithmic Weil height h(n) = log(n)
# This is the eigenvalue of D_BC. The simplest Arakelov invariant.
print("  A1: 対数的ヴェイユ高さ h(n) = log(n)")
print()
for n in range(2, 31):
    h = np.log(n)
    hits = find_matches(h, f"log({n})")
    all_matches.extend(hits)

# A2: Normalized Arakelov height h_Ar(n) = log(n)/log(2π)
# Normalization by the archimedean period
print("  A2: 正規化アラケロフ高さ h(n)/ln(2π)")
print()
for n in range(2, 50):
    h_norm = np.log(n) / ln2pi
    hits = find_matches(h_norm, f"log({n})/ln(2π)")
    all_matches.extend(hits)

# A3: Products of prime heights
print("  A3: 素数高さの積 log(p)×log(q)")
print()
primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47]
for i, p in enumerate(primes):
    for q in primes[i+1:]:
        val = np.log(p) * np.log(q)
        hits = find_matches(val, f"log({p})log({q})")
        all_matches.extend(hits)

# A4: Arakelov self-intersection: log(p)²
print("  A4: アラケロフ自己交点 log(p)²")
print()
for p in primes:
    val = np.log(p)**2
    hits = find_matches(val, f"log({p})²")
    all_matches.extend(hits)

# A5: Sums of prime log-heights: Σ_{p≤x} log(p)
# Chebyshev's θ(x) function
print("  A5: チェビシェフの θ(x) = Σ_{p≤x} log(p)")
print()
theta = 0
for p in primes:
    theta += np.log(p)
    hits = find_matches(theta, f"θ({p})")
    all_matches.extend(hits)
    # Also θ(p)/p, θ(p)/log(p), etc.
    hits = find_matches(theta/p, f"θ({p})/{p}")
    all_matches.extend(hits)
    hits = find_matches(theta/np.log(p), f"θ({p})/log({p})")
    all_matches.extend(hits)

# A6: Mertens-type sums
print("  A6: メルテンス型和")
print()
mertens_sum = 0
mertens_sum2 = 0
for p in primes:
    mertens_sum += 1/p
    mertens_sum2 += np.log(p)/p
    hits = find_matches(mertens_sum, f"Σ1/p (p≤{p})")
    all_matches.extend(hits)
    hits = find_matches(mertens_sum2, f"Σlog(p)/p (p≤{p})")
    all_matches.extend(hits)

# ============================================================================
#  CATEGORY B: Intersection numbers (2-variable)
# ============================================================================

print("=" * 70)
print("  B: 算術的交点数")
print("=" * 70)
print()

# B1: Arithmetic intersection of prime divisors
# In Arakelov geometry on Spec(Z):
# (p) · (q) has local contributions at each prime ℓ plus archimedean
# For distinct primes p ≠ q:
#   (p · q)_Ar = log(gcd(p,q)) at finite places + Green function at ∞
# Since gcd(p,q) = 1 for distinct primes:
#   (p · q)_Ar = 0 + G_∞(p,q)
# The archimedean Green function: G_∞(p,q) = -log|p-q| (simplest version)

print("  B1: アルキメデス的グリーン関数 -log|p-q|")
print()
for i, p in enumerate(primes[:10]):
    for q in primes[i+1:10]:
        G = -np.log(abs(p-q))
        hits = find_matches(G, f"-log|{p}-{q}|")
        all_matches.extend(hits)
        # Also try the "normalized" version
        G_norm = -np.log(abs(p-q)) / ln2pi
        hits = find_matches(G_norm, f"-log|{p}-{q}|/ln(2π)")
        all_matches.extend(hits)

# B2: Arakelov-Green function with logarithmic metric
# G(p,q) = log(max(p,q)/|p-q|) — another natural choice
print("  B2: 代替グリーン関数 log(max(p,q)/|p-q|)")
print()
for i, p in enumerate(primes[:10]):
    for q in primes[i+1:10]:
        G2 = np.log(max(p,q)/abs(p-q))
        hits = find_matches(G2, f"log(max({p},{q})/|{p}-{q}|)")
        all_matches.extend(hits)

# B3: Arithmetic degree of (p)⊗(q)
# deg_Ar((p)⊗(q)) = log(p) + log(q) = log(pq)
print("  B3: 算術的次数 log(p) + log(q)")
print()
for i, p in enumerate(primes[:10]):
    for q in primes[i+1:10]:
        d = np.log(p) + np.log(q)
        hits = find_matches(d, f"log({p})+log({q})")
        all_matches.extend(hits)
        # Also log(p)×log(q)/log(p×q) = harmonic mean type
        hm = np.log(p)*np.log(q)/(np.log(p)+np.log(q))
        hits = find_matches(hm, f"log{p}·log{q}/(log{p}+log{q})")
        all_matches.extend(hits)

# ============================================================================
#  CATEGORY C: Dedekind zeta of number fields
# ============================================================================

print("=" * 70)
print("  C: デデキントゼータ関数の特殊値")
print("=" * 70)
print()

# For a number field K, ζ_K(s) = Σ_{ideals a} N(a)^{-s}
# For quadratic fields K = Q(√d):
#   ζ_K(s) = ζ(s) × L(χ_d, s)

# Special values at negative integers:
# ζ_K(-n) = ζ(-n) × L(χ_d, -n)

# For K = Q(√-1) = Q(i): d = -4
# ζ_{Q(i)}(s) = ζ(s) × L(χ_{-4}, s)

# Generalized Bernoulli numbers for χ_{-4}:
# χ_{-4}(1)=1, χ_{-4}(3)=-1 (the non-trivial character mod 4)
# B_{n,χ_{-4}} for the Kronecker symbol (-4|·)

# Known values:
# L(χ_{-4}, 0) = -B_{1,χ}/1. B_{1,χ_{-4}} = -1/2. L = 1/2.
# L(χ_{-4}, -1) = -B_{2,χ}/2.
# L(χ_{-4}, 1) = π/4.

# For imaginary quadratic field K = Q(√d), d < 0:
# ζ_K(2) = (2π)² h |d|^{-3/2} L(χ_d, 2) / (w² |d|)... complicated.
# Let's just compute numerically.

print("  C1: 虚二次体のデデキントゼータ")
print()

# ζ_{Q(i)}(s) = ζ(s) × L(χ_{-4}, s)
# At s = 2: ζ(2) × L(χ_{-4}, 2) = (π²/6) × G
G_catalan = float(mpmath.catalan)
zeta_Qi_2 = (pi**2/6) * G_catalan
print(f"  ζ_{{Q(i)}}(2) = ζ(2) × L(χ_{{-4}}, 2) = (π²/6) × G = {zeta_Qi_2:.10f}")
hits = find_matches(zeta_Qi_2, "ζ_{Q(i)}(2)")
all_matches.extend(hits)
hits = find_matches(1/zeta_Qi_2, "1/ζ_{Q(i)}(2)")
all_matches.extend(hits)

# At s = -1: ζ(-1) × L(χ_{-4}, -1)
# L(χ_{-4}, -1) = -B_{2,χ}/2. Need to compute B_{2,χ_{-4}}.
# B_{2,χ} = q Σ_{a=1}^{q} χ(a) B_2(a/q) where q=4
# B_2(x) = x² - x + 1/6
def B2_poly(x): return x**2 - x + 1/6
chi_m4 = {1: 1, 3: -1}  # χ_{-4} values at odd residues mod 4
B2_chi = 4 * sum(chi_m4.get(a, 0) * B2_poly(a/4) for a in range(1, 5))
L_chi_m4_neg1 = -B2_chi/2
zeta_Qi_neg1 = (-1/12) * L_chi_m4_neg1
print(f"  B_{{2,χ_{{-4}}}} = {B2_chi:.6f}")
print(f"  L(χ_{{-4}}, -1) = {L_chi_m4_neg1:.6f}")
print(f"  ζ_{{Q(i)}}(-1) = ζ(-1) × L(χ_{{-4}},-1) = {zeta_Qi_neg1:.6f}")
if abs(zeta_Qi_neg1) > 1e-10:
    print(f"  1/|ζ_{{Q(i)}}(-1)| = {1/abs(zeta_Qi_neg1):.4f}")
    hits = find_matches(1/abs(zeta_Qi_neg1), "1/|ζ_{Q(i)}(-1)|")
    all_matches.extend(hits)
print()

# ζ_{Q(√-3)}(s) = ζ(s) × L(χ_{-3}, s)
# L(χ_{-3}, 1) = π/(3√3)
chi_m3 = {1: 1, 2: -1}  # χ_{-3} mod 3
B2_chi3 = 3 * sum(chi_m3.get(a, 0) * B2_poly(a/3) for a in range(1, 4))
L_chi_m3_neg1 = -B2_chi3/2
zeta_eisenstein_neg1 = (-1/12) * L_chi_m3_neg1
print(f"  ζ_{{Q(ω)}}(-1) = ζ(-1) × L(χ_{{-3}},-1) = {zeta_eisenstein_neg1:.6f}")
if abs(zeta_eisenstein_neg1) > 1e-10:
    print(f"  1/|ζ_{{Q(ω)}}(-1)| = {1/abs(zeta_eisenstein_neg1):.4f}")
    hits = find_matches(1/abs(zeta_eisenstein_neg1), "1/|ζ_{Q(ω)}(-1)|")
    all_matches.extend(hits)
print()

# C2: Real quadratic fields
print("  C2: 実二次体のデデキントゼータ")
print()
# Q(√5): d = 5, class number h = 1, fundamental unit ε = (1+√5)/2
# Dirichlet class number formula: L(χ_5, 1) = h log ε / √d
phi_golden = (1 + np.sqrt(5))/2
L_chi5_1 = np.log(phi_golden) / np.sqrt(5)
print(f"  Q(√5): ε = φ = {phi_golden:.6f}")
print(f"  L(χ_5, 1) = log(φ)/√5 = {L_chi5_1:.10f}")
print(f"  ζ_{{Q(√5)}}(2) = ζ(2) × L(χ_5, 2) ≈ {pi**2/6 * float(mpmath.nsum(lambda n: int(n%5 in [1,4])*n**(-2) - int(n%5 in [2,3])*n**(-2), [1, 10000])):.6f}")

# The regulator of Q(√5) is log(φ) = 0.48121...
reg_Q5 = np.log(phi_golden)
print(f"  レギュレータ R = log(φ) = {reg_Q5:.10f}")
print()

# Check: is log(φ)/√5 close to any physical constant?
hits = find_matches(L_chi5_1, "L(χ_5,1)=logφ/√5")
all_matches.extend(hits)
hits = find_matches(reg_Q5, "reg(Q(√5))=logφ")
all_matches.extend(hits)

# C3: Regulators of number fields
print("  C3: レギュレータ")
print()
# Known regulators of real quadratic fields Q(√d):
regulators = {
    2: np.log(1+np.sqrt(2)),        # 0.8814
    3: np.log(2+np.sqrt(3)),        # 1.3169
    5: np.log((1+np.sqrt(5))/2),    # 0.4812
    6: np.log(5+2*np.sqrt(6)),      # 2.2924
    7: np.log(8+3*np.sqrt(7)),      # 2.7726
    10: np.log(3+np.sqrt(10)),      # 1.8184
    11: np.log(10+3*np.sqrt(11)),   # 2.9932
    13: np.log((3+np.sqrt(13))/2),  # 1.1948
}

for d, R in sorted(regulators.items()):
    print(f"  Q(√{d:>2d}): R = {R:.6f}")
    hits = find_matches(R, f"reg(Q(√{d}))")
    all_matches.extend(hits)
    hits = find_matches(R/ln2pi, f"reg(Q(√{d}))/ln(2π)")
    all_matches.extend(hits)

print()

# ============================================================================
#  CATEGORY D: Combined invariants
# ============================================================================

print("=" * 70)
print("  D: 複合不変量")
print("=" * 70)
print()

# D1: ζ'(0)/ζ(0) variations
zp0 = -0.5*ln2pi
z0 = -0.5
print("  D1: ζ'(0)/ζ(0) の変種")
print()
combos_D1 = {
    "ζ'(0)/ζ(0)": zp0/z0,
    "e^{ζ'(0)/ζ(0)}": np.exp(zp0/z0),
    "ζ(0)²": z0**2,
    "ζ'(0)²": zp0**2,
    "|ζ(0)ζ'(0)|": abs(z0*zp0),
    "γ/ζ'(0)": gamma_em/zp0,
    "γ×ζ'(0)": gamma_em*zp0,
    "γ+|ζ'(0)|": gamma_em+abs(zp0),
    "γ×12": gamma_em*12,
    "γ×120": gamma_em*120,
    "γ/ln(2π)": gamma_em/ln2pi,
    "|ζ'(0)|×12": abs(zp0)*12,
    "|ζ'(0)|×120": abs(zp0)*120,
    "12/ln(2π)": 12/ln2pi,
    "120/ln(2π)": 120/ln2pi,
    "12×120/ln(2π)": 12*120/ln2pi,
    "e^γ": np.exp(gamma_em),
    "e^{-γ}": np.exp(-gamma_em),
    "π^γ": pi**gamma_em,
    "2π×γ": 2*pi*gamma_em,
    "12+γ": 12+gamma_em,
    "120×γ": 120*gamma_em,
    "252×γ": 252*gamma_em,
}

for name, val in combos_D1.items():
    hits = find_matches(val, name)
    all_matches.extend(hits)

# D2: Combinations of Bernoulli/zeta special values with Arakelov quantities
print("  D2: ベルヌーイ数 × アラケロフ量")
print()
B_vals = {2: 1/6, 4: -1/30, 6: 1/42, 8: -1/30, 10: 5/66}
ar_vals = {"γ": gamma_em, "ln2π": ln2pi, "h'(0)": 1-0.5*ln2pi,
           "ζ'(0)": zp0, "G_cat": G_catalan, "logφ": reg_Q5,
           "π/4": pi/4, "1/2π": 1/(2*pi)}

for bn, bv in B_vals.items():
    for an, av in ar_vals.items():
        val = bv * av
        name = f"B_{bn}×{an}"
        hits = find_matches(val, name, threshold=0.05)
        all_matches.extend(hits)
        val2 = 1/(abs(bv) * abs(av)) if abs(bv*av) > 1e-15 else 0
        hits = find_matches(val2, f"1/(|B_{bn}|×|{an}|)", threshold=0.05)
        all_matches.extend(hits)

# ============================================================================
#  RESULTS: Top matches
# ============================================================================

print("=" * 70)
print("  ■ 全結果: 物理定数との一致 TOP 30")
print("=" * 70)
print()

# Sort by precision
all_matches.sort(key=lambda x: x[0])

# Remove duplicates
seen = set()
unique = []
for m in all_matches:
    key = (m[1], m[3])
    if key not in seen:
        seen.add(key)
        unique.append(m)

print(f"  {'算術的量':.<40s} {'値':>10s} {'物理量':.<20s} {'物理値':>10s} {'ズレ':>8s}")
print(f"  {'-'*92}")

for pct_abs, label, val, pname, pval, pct in unique[:30]:
    print(f"  {label:.<40s} {val:>10.4f} {pname:.<20s} {pval:>10.4f} {pct:>+8.2f}%")

print()

# ============================================================================
print("=" * 70)
print("  ■ 評価")
print("=" * 70)

# Count matches by precision
n1 = sum(1 for m in unique if m[0] < 1)
n5 = sum(1 for m in unique if m[0] < 5)
n10 = sum(1 for m in unique if m[0] < 10)
total_searched = len(seen)

print(f"""
  探索した算術的量の総数: ~{total_searched}
  物理定数との一致:
    1% 以内: {n1} 個
    5% 以内: {n5} 個
    10% 以内: {n10} 個

  ── 統計的な期待値 ──

  ランダムな正の実数が特定の物理定数の ε% 以内に
  入る確率は約 2ε/100 × (対数的密度)。
  20個の物理定数に対して ~{total_searched} 個の量を試すと、
  10% 以内の偶然一致の期待数 ≈ {total_searched} × 20 × 0.2 / 10:.0f 程度。

  → {n10} 個の一致が {int(total_searched * 20 * 0.2 / 10)} 個の期待値と比べて
    {'多い' if n10 > total_searched * 20 * 0.2 / 10 * 1.5 else '同程度か少ない'}。
""")

# Which matches are NOT expected by chance?
print("  ── 偶然を超える一致はあるか ──")
print()

# The strongest test: find matches where the arithmetic quantity
# has a KNOWN mathematical connection to the physical quantity.
print("  物理的に意味のある可能性がある一致:")
print()

meaningful = []
for pct_abs, label, val, pname, pval, pct in unique[:30]:
    reason = ""
    if "ζ" in label and "α" in pname:
        reason = "ζ値と電磁結合定数"
    elif "reg" in label and "sin" in pname:
        reason = "レギュレータとワインバーグ角？"
    elif "log" in label and "m_" in pname:
        reason = "算術高さと質量比"
    elif "γ" in label:
        reason = "オイラー定数"

    if reason or pct_abs < 2:
        meaningful.append((pct_abs, label, val, pname, pval, pct, reason))

for pct_abs, label, val, pname, pval, pct, reason in meaningful[:10]:
    print(f"    {label} = {val:.4f} ≈ {pname} = {pval:.4f} ({pct:+.2f}%)")
    if reason:
        print(f"      → {reason}")
    print()

print("=" * 70)
print("  END")
print("=" * 70)
