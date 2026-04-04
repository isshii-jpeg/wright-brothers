"""
Deep Prime Scan: vector-valued invariants × multivariate matching
==================================================================

For each prime p ≤ 1000, compute a VECTOR of arithmetic invariants.
Then search for multivariate relationships with physical constants.

This is qualitatively different from our previous "point matching":
we're looking for STRUCTURE in the space of prime invariants.

Wright Brothers, 2026
"""

import numpy as np
import mpmath
from math import gcd
from scipy import stats

mpmath.mp.dps = 15
pi = np.pi

print("=" * 70)
print("  DEEP PRIME SCAN")
print("=" * 70)

# ============================================================================
#  Generate all primes up to 1000
# ============================================================================

def sieve(n):
    is_prime = [True] * (n+1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5)+1):
        if is_prime[i]:
            for j in range(i*i, n+1, i):
                is_prime[j] = False
    return [i for i in range(2, n+1) if is_prime[i]]

primes = sieve(1000)
print(f"\n  素数の数: {len(primes)} (p ≤ 1000)\n")

# ============================================================================
#  Compute invariant vector for each prime
# ============================================================================

def fundamental_unit(d, max_y=100000):
    """Find fundamental unit of Q(√d) via Pell equation."""
    sqrtd = np.sqrt(d)
    for y in range(1, max_y):
        for sign in [1, -1]:
            x2 = d * y*y + sign
            if x2 > 0:
                x = int(np.sqrt(x2) + 0.5)
                if x*x == x2:
                    return x + y * sqrtd, sign
    return None, 0

def kronecker(d, p):
    """Kronecker symbol (d|p) for odd prime p."""
    if p == 2:
        if d % 2 == 0: return 0
        if d % 8 in [1, 7]: return 1
        return -1
    if d % p == 0: return 0
    return pow(d % p, (p-1)//2, p) if pow(d % p, (p-1)//2, p) <= 1 else -1

def cf_period(d):
    """Period length of continued fraction of √d."""
    a0 = int(np.sqrt(d))
    if a0*a0 == d:
        return 0
    m, d_cf, a = 0, 1, a0
    period = 0
    while True:
        m = d_cf * a - m
        d_cf = (d - m*m) // d_cf
        a = (a0 + m) // d_cf
        period += 1
        if a == 2*a0:
            return period

# Build the invariant matrix
print("  不変量ベクトルの計算中...", flush=True)

invariant_names = [
    "reg",          # 0: regulator
    "log_reg",      # 1: log(regulator)
    "disc",         # 2: discriminant
    "log_disc",     # 3: log(discriminant)
    "cf_period",    # 4: continued fraction period
    "unit_norm",    # 5: norm of fundamental unit (±1)
    "reg/sqrt_disc",# 6: L(χ,1) essentially (class number formula)
    "reg²",         # 7: regulator squared
    "1/reg",        # 8: inverse regulator
    "reg/pi",       # 9: reg/π
    "reg/ln2pi",    # 10: reg/ln(2π)
    "p_mod_4",      # 11: p mod 4 (1 or 3)
    "p_mod_8",      # 12: p mod 8
    "p²+1",         # 13: p²+1
    "(p²+1)*reg",   # 14: (p²+1) × reg
]

N_inv = len(invariant_names)
N_primes = len(primes)

data = np.zeros((N_primes, N_inv))

for i, p in enumerate(primes):
    d = p  # Use Q(√p) for each prime
    disc = p if p % 4 == 1 else 4*p

    eps, norm_sign = fundamental_unit(d)
    if eps is None:
        continue

    reg = np.log(eps)
    cf_per = cf_period(d)

    data[i, 0] = reg
    data[i, 1] = np.log(reg) if reg > 0 else 0
    data[i, 2] = disc
    data[i, 3] = np.log(disc)
    data[i, 4] = cf_per
    data[i, 5] = norm_sign
    data[i, 6] = reg / np.sqrt(disc)  # ∝ L(χ, 1)
    data[i, 7] = reg**2
    data[i, 8] = 1/reg if reg > 0 else 0
    data[i, 9] = reg / pi
    data[i, 10] = reg / np.log(2*pi)
    data[i, 11] = p % 4
    data[i, 12] = p % 8
    data[i, 13] = p**2 + 1
    data[i, 14] = (p**2 + 1) * reg

print(f"  完了。行列サイズ: {data.shape}")
print()

# ============================================================================
#  Physical constants
# ============================================================================

phys = {
    "1/α": 137.036,
    "cos_θW": 0.88137,
    "sin²θW": 0.2312,
    "sin_θW": 0.4808,
    "α_s": 0.1179,
    "1/α_s": 8.482,
    "m_μ/m_e": 206.768,
    "m_τ/m_μ": 16.817,
    "m_p/m_e": 1836.15,
    "m_b/m_τ": 2.35,
    "m_c/m_s": 11.7,
    "V_us": 0.2243,
    "V_cb": 0.0408,
    "sin²θ12": 0.307,
    "sin²θ23": 0.546,
    "sin²θ13": 0.022,
    "m_W/m_Z": 0.88153,
    "3/8_GUT": 0.375,
    "G_F*1e5": 1.1664,
    "m_H/v": 0.510,
}

# ============================================================================
#  Single-invariant scan (what we've been doing)
# ============================================================================

print("=" * 70)
print("  ■ Phase 1: 単一不変量マッチング（従来手法）")
print("=" * 70)
print()

single_hits = []

for j in range(N_inv):
    for i in range(N_primes):
        val = data[i, j]
        if val == 0 or abs(val) > 1e6:
            continue
        for pname, pval in phys.items():
            for v in [val, abs(val), 1/abs(val) if abs(val) > 1e-10 else 0]:
                if v > 0 and pval > 0:
                    ratio = v / pval
                    if 0.999 < ratio < 1.001:  # 0.1% threshold
                        pct = (ratio - 1) * 100
                        single_hits.append((abs(pct), primes[i], invariant_names[j], v, pname, pval, pct))

single_hits.sort()
print(f"  0.1% 以内のヒット数: {len(single_hits)}")
print()
if single_hits:
    print(f"  {'p':>5s} {'不変量':>15s} {'値':>12s} {'物理量':>12s} {'物理値':>10s} {'ズレ':>8s}")
    print(f"  {'-'*68}")
    seen = set()
    for _, p, inv, val, pname, pval, pct in single_hits[:15]:
        key = (p, pname)
        if key in seen: continue
        seen.add(key)
        print(f"  {p:>5d} {inv:>15s} {val:>12.6f} {pname:>12s} {pval:>10.6f} {pct:>+8.4f}%")

print()

# ============================================================================
#  TWO-PRIME combinations
# ============================================================================

print("=" * 70)
print("  ■ Phase 2: 2素数の組み合わせ")
print("=" * 70)
print()

# For pairs of primes (p, q), check if
# reg(p) OP reg(q) matches a physical constant
# where OP is +, -, ×, /, harmonic mean, geometric mean

pair_hits = []

# Use only first 25 primes (p ≤ 97) for pairs to keep computation feasible
small_idx = min(25, N_primes)

for i in range(small_idx):
    for j in range(i+1, small_idx):
        r1 = data[i, 0]  # reg of prime i
        r2 = data[j, 0]  # reg of prime j
        if r1 <= 0 or r2 <= 0:
            continue

        combos = {
            "reg(p)+reg(q)": r1 + r2,
            "reg(p)-reg(q)": abs(r1 - r2),
            "reg(p)×reg(q)": r1 * r2,
            "reg(p)/reg(q)": r1 / r2,
            "harmonic": 2*r1*r2/(r1+r2),
            "geometric": np.sqrt(r1*r2),
            "reg(p)²+reg(q)²": r1**2 + r2**2,
            "reg(p)²-reg(q)²": abs(r1**2 - r2**2),
        }

        for cname, cval in combos.items():
            if cval <= 0 or cval > 1e6:
                continue
            for pname, pval in phys.items():
                for v in [cval, 1/cval]:
                    if v > 0 and pval > 0:
                        ratio = v / pval
                        if 0.999 < ratio < 1.001:
                            pct = (ratio - 1) * 100
                            pair_hits.append((abs(pct), primes[i], primes[j], cname, v, pname, pval, pct))

pair_hits.sort()
print(f"  0.1% 以内のヒット数: {len(pair_hits)}")
print()
if pair_hits:
    print(f"  {'(p,q)':>8s} {'操���':>20s} {'値':>12s} {'物理量':>12s} {'物理値':>10s} {'ズレ':>8s}")
    print(f"  {'-'*76}")
    seen = set()
    for _, p, q, op, val, pname, pval, pct in pair_hits[:15]:
        key = (p, q, pname)
        if key in seen: continue
        seen.add(key)
        print(f"  ({p},{q}){'':<{4-len(str(p))-len(str(q))}} {op:>20s} {val:>12.6f} {pname:>12s} {pval:>10.6f} {pct:>+8.4f}%")

print()

# ============================================================================
#  CORRELATION analysis
# ============================================================================

print("=" * 70)
print("  ■ Phase 3: 相関分析")
print("=" * 70)
print()

# Do any invariants correlate across primes in a way that mirrors
# how physical constants relate to each other?

# Compute correlation matrix of invariants
valid_rows = data[:, 0] > 0  # only primes where reg was computed
valid_data = data[valid_rows]

print(f"  不変量間の相関行列（|r| > 0.8 のペア）:")
print()

corr_matrix = np.corrcoef(valid_data.T)
for i in range(N_inv):
    for j in range(i+1, N_inv):
        r = corr_matrix[i, j]
        if abs(r) > 0.8 and not np.isnan(r):
            print(f"    {invariant_names[i]:>15s} × {invariant_names[j]:<15s}: r = {r:+.4f}")

print()

# ============================================================================
#  LINEAR REGRESSION: can a linear combination of invariants
#  reproduce a physical constant?
# ============================================================================

print("=" * 70)
print("  ■ Phase 4: 線形回帰（多変量）")
print("=" * 70)
print()

# For each physical constant, try: phys = a₀ + a₁×inv₁ + a₂×inv₂ + ...
# using the invariants of the FIRST FEW primes as predictors.

# Use the invariants of p=2,3,5,7,11 (5 primes) as input features
# and try to predict each physical constant.

feature_primes = [2, 3, 5, 7, 11]
feature_indices = [primes.index(p) for p in feature_primes]

# Feature vector: [reg(2), reg(3), reg(5), reg(7), reg(11)]
X = np.array([data[i, 0] for i in feature_indices])

print(f"  特徴ベクトル (レギュレータ):")
for p, idx in zip(feature_primes, feature_indices):
    print(f"    reg(Q(√{p})) = {data[idx, 0]:.6f}")
print()

# For each physical constant, find the best linear combination
print(f"  物理定数 = Σ aᵢ × reg(Q(√pᵢ)) の最良フィット:")
print()
print(f"  {'物理量':>12s} {'値':>10s} {'フィット':>10s} {'ズレ':>8s} {'係数 (2,3,5,7,11)':>40s}")
print(f"  {'-'*86}")

# Simple: try all ±1, ±2, 0 coefficient combinations (5^5 = 3125)
import itertools

for pname, pval in phys.items():
    best_err = 1e10
    best_coeffs = None
    best_val = 0

    for coeffs in itertools.product(range(-3, 4), repeat=5):
        if all(c == 0 for c in coeffs):
            continue
        val = sum(c * X[i] for i, c in enumerate(coeffs))
        if val <= 0:
            continue
        err = abs(val / pval - 1)
        if err < best_err:
            best_err = err
            best_coeffs = coeffs
            best_val = val

    if best_err < 0.01:  # 1% threshold
        pct = (best_val/pval - 1) * 100
        coeff_str = ", ".join(f"{c:+d}" for c in best_coeffs)
        print(f"  {pname:>12s} {pval:>10.4f} {best_val:>10.4f} {pct:>+8.3f}% [{coeff_str}]")

print()

# ============================================================================
#  RATIO scan: reg(p)/reg(q) = physical constant?
# ============================================================================

print("=" * 70)
print("  ■ Phase 5: レギュレータ比のスキャン")
print("=" * 70)
print()

ratio_hits = []
for i in range(small_idx):
    for j in range(small_idx):
        if i == j: continue
        r1 = data[i, 0]
        r2 = data[j, 0]
        if r1 <= 0 or r2 <= 0: continue
        ratio = r1 / r2
        for pname, pval in phys.items():
            if pval > 0 and abs(ratio/pval - 1) < 0.005:
                pct = (ratio/pval - 1) * 100
                ratio_hits.append((abs(pct), primes[i], primes[j], ratio, pname, pval, pct))

ratio_hits.sort()
print(f"  reg(p)/reg(q) が物理定数の 0.5% 以内:")
print()
if ratio_hits:
    print(f"  {'p/q':>8s} {'reg比':>12s} {'物理量':>12s} {'物理値':>10s} {'ズレ':>8s}")
    print(f"  {'-'*56}")
    seen = set()
    for _, p, q, ratio, pname, pval, pct in ratio_hits[:20]:
        key = (p, q, pname)
        if key in seen: continue
        seen.add(key)
        print(f"  {p}/{q}{'':<{5-len(str(p))-len(str(q))}} {ratio:>12.6f} {pname:>12s} {pval:>10.6f} {pct:>+8.3f}%")

print()

# ============================================================================
print("=" * 70)
print("  ■ 総合結果")
print("=" * 70)

print(f"""
  Phase 1（単一不変量）: {len(single_hits)} ヒット at 0.1%
  Phase 2（2素数組合せ）: {len(pair_hits)} ヒット at 0.1%
  Phase 4（線形結合）: 1% 以内のフィット（上記参照）
  Phase 5（レギュレータ比）: {len(ratio_hits)} ヒット at 0.5%

  ── 新しい発見はあるか ──
""")

# Identify genuinely NEW hits (not reg(Q(√2)) = cos θ_W which we already know)
print(f"  既知: reg(Q(√2)) = cos θ_W (0.001%)")
print(f"  新規のヒットを上記から抽��...")
print()

# Count truly new discoveries
new_count = 0
for _, p, inv, val, pname, pval, pct in single_hits:
    if not (p == 2 and "cos" in pname):
        new_count += 1
        if new_count <= 5:
            print(f"    NEW: p={p}, {inv}={val:.6f} ≈ {pname}={pval:.6f} ({pct:+.4f}%)")

print()
print("=" * 70)
print("  END")
print("=" * 70)
