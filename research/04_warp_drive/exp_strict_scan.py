"""
Strict scan: more invariants, tighter coefficient constraints
==============================================================

Constraints:
  - Coefficients limited to {-1, 0, +1} only
  - At most 3 nonzero coefficients (sparsity)
  - More invariant types per prime

If a hit survives these constraints, it's much harder to dismiss.
With K variables and coefficients in {-1,0,1}, max 3 nonzero:
  combinations = C(K,1)×2 + C(K,2)×4 + C(K,3)×8

Wright Brothers, 2026
"""

import numpy as np
import mpmath
from itertools import combinations
from math import gcd

mpmath.mp.dps = 15
pi = np.pi

print("=" * 70)
print("  STRICT SCAN: 厳しい係数制約での網羅探索")
print("=" * 70)

# ============================================================================
#  Build enriched invariant set
# ============================================================================

def sieve(n):
    is_prime = [True]*(n+1)
    is_prime[0] = is_prime[1] = False
    for i in range(2, int(n**0.5)+1):
        if is_prime[i]:
            for j in range(i*i, n+1, i): is_prime[j] = False
    return [i for i in range(2, n+1) if is_prime[i]]

def fundamental_unit(d, max_y=200000):
    sqrtd = np.sqrt(d)
    for y in range(1, max_y):
        for sign in [1, -1]:
            x2 = d*y*y + sign
            if x2 > 0:
                x = int(np.sqrt(x2)+0.5)
                if x*x == x2:
                    return x + y*sqrtd
    return None

small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

# For each prime, compute MANY invariants
print(f"\n  不変量の計算中 ({len(small_primes)} 素数)...", flush=True)

invariants = {}  # name → value

for p in small_primes:
    eps = fundamental_unit(p)
    if eps is None:
        continue
    reg = np.log(eps)
    disc = p if p % 4 == 1 else 4*p

    invariants[f"reg({p})"] = reg
    invariants[f"1/reg({p})"] = 1/reg
    invariants[f"reg({p})/pi"] = reg/pi
    invariants[f"reg({p})/ln2pi"] = reg/np.log(2*pi)
    invariants[f"L({p},1)"] = reg / np.sqrt(disc)  # h=1 assumed
    invariants[f"sqrt(disc({p}))"] = np.sqrt(disc)

# Products of pairs of regs
for i, p in enumerate(small_primes[:8]):
    for q in small_primes[i+1:8]:
        ep = fundamental_unit(p)
        eq = fundamental_unit(q)
        if ep and eq:
            rp, rq = np.log(ep), np.log(eq)
            invariants[f"reg({p})*reg({q})"] = rp*rq
            invariants[f"reg({p})/reg({q})"] = rp/rq
            if rp+rq > 0:
                invariants[f"harm({p},{q})"] = 2*rp*rq/(rp+rq)

# Some special values
invariants["gamma"] = 0.5772156649
invariants["ln2pi"] = np.log(2*pi)
invariants["pi"] = pi
invariants["1/pi"] = 1/pi
invariants["sqrt2"] = np.sqrt(2)
invariants["phi"] = (1+np.sqrt(5))/2  # golden ratio
invariants["ln(phi)"] = np.log((1+np.sqrt(5))/2)
invariants["catalan"] = float(mpmath.catalan)

print(f"  不変量の数: {len(invariants)}")

# Physical constants
phys = {
    "1/alpha": 137.036, "cos_tW": 0.88137, "sin2_tW": 0.2312,
    "sin_tW": 0.4808, "alpha_s": 0.1179, "1/alpha_s": 8.482,
    "m_mu/m_e": 206.768, "m_tau/m_mu": 16.817, "m_p/m_e": 1836.15,
    "m_b/m_tau": 2.35, "m_c/m_s": 11.7, "V_us": 0.2243,
    "V_cb": 0.0408, "sin2_t12": 0.307, "sin2_t23": 0.546,
    "sin2_t13": 0.022, "m_W/m_Z": 0.88153, "3/8": 0.375,
    "G_F*1e5": 1.1664, "m_H/v": 0.510,
}

print(f"  物理定数の数: {len(phys)}\n")

# ============================================================================
#  Strict search: coefficients in {-1, 0, +1}, at most 3 nonzero
# ============================================================================

inv_names = list(invariants.keys())
inv_vals = np.array([invariants[n] for n in inv_names])
N = len(inv_names)

print("=" * 70)
print(f"  ■ 厳密探索: 係数 ∈ {{-1, 0, +1}}, 非ゼロ ≤ 3")
print("=" * 70)

# Count combinations
n1 = N * 2  # 1 nonzero
n2 = len(list(combinations(range(N), 2))) * 4  # 2 nonzero
n3 = len(list(combinations(range(N), 3))) * 8  # 3 nonzero
total_combos = n1 + n2 + n3
print(f"\n  探索空間: {n1} + {n2} + {n3} = {total_combos:,d} 組み合わせ")
print(f"  物理定数: {len(phys)} 個")
print(f"  合計比較: {total_combos * len(phys):,d}")
print()

# Expected false positives at 0.1% threshold:
expected_fp = total_combos * len(phys) * 0.002
print(f"  0.1% 閾値での偶然一致の期待数: {expected_fp:.0f}")
print()

hits = []
THRESHOLD = 0.001  # 0.1%

# 1 nonzero
for i in range(N):
    for sign in [+1, -1]:
        val = sign * inv_vals[i]
        if val <= 0 or abs(val) > 1e7:
            continue
        for pname, pval in phys.items():
            ratio = val / pval
            if abs(ratio - 1) < THRESHOLD:
                pct = (ratio-1)*100
                desc = f"{'+' if sign>0 else '-'}{inv_names[i]}"
                hits.append((abs(pct), desc, val, pname, pval, pct, 1))

# 2 nonzero
for i, j in combinations(range(N), 2):
    for s1 in [+1, -1]:
        for s2 in [+1, -1]:
            val = s1*inv_vals[i] + s2*inv_vals[j]
            if val <= 0 or abs(val) > 1e7:
                continue
            for pname, pval in phys.items():
                ratio = val / pval
                if abs(ratio - 1) < THRESHOLD:
                    pct = (ratio-1)*100
                    desc = f"{'+' if s1>0 else '-'}{inv_names[i]} {'+' if s2>0 else '-'}{inv_names[j]}"
                    hits.append((abs(pct), desc, val, pname, pval, pct, 2))

# 3 nonzero
for i, j, k in combinations(range(N), 3):
    for s1 in [+1, -1]:
        for s2 in [+1, -1]:
            for s3 in [+1, -1]:
                val = s1*inv_vals[i] + s2*inv_vals[j] + s3*inv_vals[k]
                if val <= 0 or abs(val) > 1e7:
                    continue
                for pname, pval in phys.items():
                    ratio = val / pval
                    if abs(ratio - 1) < THRESHOLD:
                        pct = (ratio-1)*100
                        desc = (f"{'+' if s1>0 else '-'}{inv_names[i]} "
                                f"{'+' if s2>0 else '-'}{inv_names[j]} "
                                f"{'+' if s3>0 else '-'}{inv_names[k]}")
                        hits.append((abs(pct), desc, val, pname, pval, pct, 3))

hits.sort()

print(f"  ヒット数 (0.1% 以内): {len(hits)}")
print(f"  偶然の期待数との比: {len(hits)/max(expected_fp,1):.2f}×")
print()

# ============================================================================
#  Filter: show only the BEST hit for each physical constant
# ============================================================================

print("=" * 70)
print("  ■ 各物理定数の最良ヒット")
print("=" * 70)
print()

best_per_phys = {}
for h in hits:
    pname = h[4]
    if pname not in best_per_phys or h[0] < best_per_phys[pname][0]:
        best_per_phys[pname] = h

print(f"  {'物理量':>12s} {'値':>10s} {'式':.<50s} {'ズレ':>8s} {'項数':>4s}")
print(f"  {'-'*90}")

for pname in phys:
    if pname in best_per_phys:
        _, desc, val, _, pval, pct, nterms = best_per_phys[pname]
        mark = "★" if abs(pct) < 0.01 else ("☆" if abs(pct) < 0.05 else "")
        print(f"  {pname:>12s} {pval:>10.4f} {desc:.<50s} {pct:>+8.4f}% {nterms:>3d} {mark}")
    else:
        print(f"  {pname:>12s} {phys[pname]:>10.4f} {'(一致なし)':.<50s}")

print()

# ============================================================================
#  Statistical test: are we seeing more hits than expected?
# ============================================================================

print("=" * 70)
print("  ■ 統計的有意性")
print("=" * 70)
print()

n_hits = len(hits)
print(f"  ヒット数: {n_hits}")
print(f"  偶然の期待数: {expected_fp:.0f}")
print(f"  比: {n_hits/max(expected_fp,1):.2f}×")
print()

if n_hits > 2 * expected_fp:
    print(f"  ★ ヒット数が期待値の 2 倍以上。偶然では説明しにくい。")
elif n_hits > expected_fp:
    print(f"  △ ヒット数が期待値を超えるが、決定的ではない。")
else:
    print(f"  ✗ ヒット数が期待値以下。偶然で説明可能。")

print()

# ============================================================================
#  The truly remarkable hits (0.01% or better)
# ============================================================================

print("=" * 70)
print("  ■ 0.01% 以内の一致（最も偶然でなさそうなもの）")
print("=" * 70)
print()

remarkable = [h for h in hits if h[0] < 0.01]
print(f"  0.01% 以内のヒット数: {len(remarkable)}")
print(f"  偶然の期待数 (0.01%): {total_combos * len(phys) * 0.0002:.1f}")
print()

if remarkable:
    for _, desc, val, pname, pval, pct, nt in remarkable:
        print(f"  {pname:>12s} = {desc}")
        print(f"    計算値: {val:.8f}, 実験値: {pval:.8f}, ズレ: {pct:+.5f}%")
        print()

# ============================================================================
#  Focus: hits that DON'T involve reg(2) (to avoid "known" result)
# ============================================================================

print("=" * 70)
print("  ■ reg(2) を含まない新しいヒット")
print("=" * 70)
print()

new_hits = [h for h in hits if "reg(2)" not in h[1] and h[0] < 0.05]
new_hits_unique = {}
for h in new_hits:
    key = h[4]  # physical constant name
    if key not in new_hits_unique or h[0] < new_hits_unique[key][0]:
        new_hits_unique[key] = h

if new_hits_unique:
    print(f"  {'物理量':>12s} {'式':.<55s} {'ズレ':>8s}")
    print(f"  {'-'*80}")
    for pname, (_, desc, val, _, pval, pct, nt) in sorted(new_hits_unique.items(), key=lambda x: x[1][0]):
        print(f"  {pname:>12s} {desc:.<55s} {pct:>+8.4f}%")
else:
    print("  なし。")

print()
print("=" * 70)
print("  END")
print("=" * 70)
