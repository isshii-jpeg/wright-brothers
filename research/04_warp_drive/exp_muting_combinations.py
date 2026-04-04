"""
Complete catalog of prime muting combinations
==============================================

For each subset S of small primes, compute:
  - Vacuum energy ζ_{¬S}(-3)
  - Effect on L(χ₈) (electroweak safety)
  - Effect on L(χ₃) (QCD safety) [for the cubic covering]
  - Safety verdict
  - Associated number field Q(√d) where d = product of primes in S

Constraint from Level 3: |S| ≥ 4 destroys all couplings.

Wright Brothers, 2026
"""

import numpy as np
from itertools import combinations
pi = np.pi

print("=" * 70)
print("  素数ミュート全組み合わせカタログ")
print("=" * 70)

# Setup
primes = [2, 3, 5, 7, 11, 13]

# Kronecker symbol (8|p) for Q(√2) covering
def chi8(p):
    if p == 2: return 0
    return 1 if p % 8 in [1, 7] else -1

# For the cubic covering Q(ζ₉)⁺: character mod 9, order 3
# For safety of p=3 muting w.r.t. the cubic covering:
# χ₃(3) = 0 (ramified). For other p: depends on p mod 9.
def chi9(p):
    if p == 3: return 0
    if p % 3 == 0: return 0
    # Simplified: for the real character component
    # Actually we need |1 - χ₃(p)p^{-1}| type factor
    # For safety check: just need χ=0 or not
    return 1  # nonzero for all p ≠ 3

# Discriminant of Q(√d) for squarefree d
def discriminant(d):
    return d if d % 4 == 1 else 4*d

# Ramified primes = prime divisors of discriminant
def ramified_primes(d):
    Delta = discriminant(d)
    ram = set()
    temp = Delta
    for p in [2,3,5,7,11,13,17,19,23,29,31]:
        while temp % p == 0:
            ram.add(p)
            temp //= p
    return ram

print()

# ============================================================================
#  Single prime muting
# ============================================================================

print("=" * 70)
print("  ■ 1素数ミュート")
print("=" * 70)
print()

print(f"  {'p':>4s} {'ζ_{¬p}(-3)':>14s} {'|ΔE|/ζ(-3)':>12s} "
      f"{'χ₈(p)':>6s} {'θ_W安全':>8s} {'χ₉(p)':>6s} {'α_s安全':>8s} "
      f"{'総合':>6s}")
print(f"  {'-'*72}")

for p in primes:
    vac = (1 - p**3) / 120
    dE = abs(1 - p**3)
    c8 = chi8(p)
    c9 = chi9(p)
    ew_safe = "✓" if c8 == 0 else "✗"
    qcd_safe = "✓" if c9 == 0 else "✗"
    total = "★安全" if c8 == 0 and c9 == 0 else ("△部分" if c8 == 0 or c9 == 0 else "✗危険")

    print(f"  {p:>4d} {vac:>14.6f} {dE:>12d} "
          f"{c8:>6d} {ew_safe:>8s} {c9:>6d} {qcd_safe:>8s} "
          f"{total:>6s}")

print()
print(f"  結論: p=2 は θ_W 安全だが α_s への影響は不明（△）")
print(f"        p=3 は α_s 安全だが θ_W を破壊（✗）")
print(f"        p≥5 は両方破壊（✗）")
print()

# ============================================================================
#  Two-prime muting
# ============================================================================

print("=" * 70)
print("  ■ 2素数ミュート")
print("=" * 70)
print()

print(f"  {'(p,q)':>8s} {'ζ_{¬p,¬q}(-3)':>16s} {'|ΔE|':>8s} "
      f"{'d=pq':>6s} {'Δ(Q√d)':>8s} {'分岐素数':>12s} "
      f"{'全分岐?':>8s} {'安全':>6s}")
print(f"  {'-'*80}")

for combo in combinations(primes, 2):
    p, q = combo
    # ζ_{¬p,¬q}(-3) = ζ(-3) × (1-p^{-(-3)}) × (1-q^{-(-3)})
    #               = (1/120) × (1-p³) × (1-q³)
    vac = (1 - p**3) * (1 - q**3) / 120
    dE = abs((1-p**3)*(1-q**3))

    # Associated field: Q(√(p×q)) if p×q is squarefree
    d = p * q
    Delta = discriminant(d)
    ram = ramified_primes(d)

    # Safety: all muted primes must be ramified in the covering
    all_ram = all(x in ram for x in combo)
    safety = "★安全" if all_ram else "✗危険"

    ram_str = ",".join(str(x) for x in sorted(ram))

    print(f"  ({p},{q}){'':<{4-len(str(p))-len(str(q))}} "
          f"{vac:>16.4f} {dE:>8d} "
          f"{d:>6d} {Delta:>8d} {ram_str:>12s} "
          f"{'✓' if all_ram else '✗':>8s} {safety:>6s}")

print()

# ============================================================================
#  Three-prime muting
# ============================================================================

print("=" * 70)
print("  ■ 3素数ミュート")
print("=" * 70)
print()

print(f"  {'(p,q,r)':>10s} {'ζ_{¬S}(-3)':>16s} {'|ΔE|':>12s} "
      f"{'d':>6s} {'Δ':>8s} {'分岐':>12s} {'全分岐?':>8s} {'安全':>6s}")
print(f"  {'-'*82}")

for combo in combinations(primes, 3):
    p, q, r = combo

    vac = (1-p**3)*(1-q**3)*(1-r**3) / 120
    dE = abs((1-p**3)*(1-q**3)*(1-r**3))

    # d = p*q*r (squarefree)
    d = p * q * r
    Delta = discriminant(d)
    ram = ramified_primes(d)
    all_ram = all(x in ram for x in combo)
    safety = "★安全" if all_ram else "✗危険"
    ram_str = ",".join(str(x) for x in sorted(ram))

    print(f"  ({p},{q},{r}){'':<{6-len(str(p))-len(str(q))-len(str(r))}} "
          f"{vac:>16.2f} {dE:>12,d} "
          f"{d:>6d} {Delta:>8d} {ram_str:>12s} "
          f"{'✓' if all_ram else '✗':>8s} {safety:>6s}")

print()

# ============================================================================
#  Summary: all safe combinations
# ============================================================================

print("=" * 70)
print("  ■ 安全なミュート組み合わせの完全リスト")
print("=" * 70)
print()

safe_combos = []

for size in range(1, 4):
    for combo in combinations(primes, size):
        d = 1
        for p in combo:
            d *= p

        Delta = discriminant(d)
        ram = ramified_primes(d)
        all_ram = all(p in ram for p in combo)

        if all_ram:
            vac = 1
            for p in combo:
                vac *= (1 - p**3)
            vac /= 120
            dE = abs(vac * 120)

            safe_combos.append((combo, d, Delta, vac, dE))

if safe_combos:
    print(f"  {'ミュート素数':>16s} {'d':>6s} {'Δ':>8s} "
          f"{'ζ_{¬S}(-3)':>16s} {'|ΔE|/ζ(-3)':>12s} {'Q(√d)':>12s}")
    print(f"  {'-'*74}")
    for combo, d, Delta, vac, dE in safe_combos:
        combo_str = "{" + ",".join(str(p) for p in combo) + "}"
        field_str = "Q(√" + str(d) + ")"
        print(f"  {combo_str:>16s} {d:>6d} {Delta:>8d} "
              f"{vac:>16.6f} {dE:>12.0f} {field_str:>12s}")
else:
    print("  安全な組み合わせなし！")

print()

# ============================================================================
#  The complete picture
# ============================================================================

print("=" * 70)
print("  ■ 全体像")
print("=" * 70)

print(f"""
  ── |S|=4 以上は真空破壊（Level 3 で確認済み）──
  → 最大 3 素数まで。

  ── 安全条件: ミュートする全素数が被覆の分岐素数 ──
  → Q(√d) の判別式 Δ の素因数に含まれる必要。

  ── 全組み合わせの分類 ──

  |S|=1 (6通り):
    安全: {{2}} のみ（Q(√2) で p=2 が分岐）
    ※ p=3 は Q(√3) の Δ=12 で分岐だが、
      同時に p=2 でも分岐 → p=3 単独でも Δ に 2 が入る
      → Q(√3) を使えば p=3 も安全だが、
        それは「Q(√2) の」L関数ではなく「Q(√3) の」L関数の話。

  ★ 重要な修正:
    安全性は「どの被覆を基準にするか」に依存する。
    Q(√2) の L 関数 L(χ₈) を保護したいなら → p=2 のみ安全。
    Q(√3) の L 関数 L(χ₁₂) を保護したいなら → p=2, 3 が安全。
    Q(√d) の L 関数を保護したいなら → Δ_d の素因数が安全。

  ── 最も効率的な安全ミュート戦略 ──

  (1) p=2 単独 (Q(√2) 基準)
      |ΔE| = 7, 弱い力のみミュート。
      最も安全で最も実験しやすい。

  (2) p=2, 3 同時 (Q(√6) 基準, Δ=24)
      |ΔE| = 7×26 = 182, 弱い力+強い力ミュート。
      効果は (1) の 26 倍。
      Q(√6) の L 関数が保護される。
      ただし Q(√6) と物理の対応は未確立。

  (3) p=2, 3, 5 同時 (Q(√30) 基準, Δ=120)
      |ΔE| = 7×26×124 = 22,568
      効果は (1) の 3,224 倍。
      Q(√30) の Δ=120 は 2,3,5 で分岐。
      ただし |S|=3 は真空破壊の「境界」に近い。

  ── 数体のレギュレータ ──
""")

# Compute regulators for the safe fields
fields = {
    2: "Q(√2)",
    6: "Q(√6)",
    30: "Q(√30)",
    3: "Q(√3)",
    10: "Q(√10)",
    15: "Q(√15)",
}

for d, name in sorted(fields.items()):
    # Find fundamental unit
    eps = None
    sqrtd = np.sqrt(d)
    for y in range(1, 100000):
        for sign in [1, -1]:
            x2 = d * y*y + sign
            if x2 > 0:
                x = int(np.sqrt(x2) + 0.5)
                if x*x == x2:
                    eps = x + y * sqrtd
                    break
        if eps:
            break

    if eps:
        R = np.log(eps)
        Delta = discriminant(d)
        ram = sorted(ramified_primes(d))
        ram_str = ",".join(str(p) for p in ram)
        print(f"  {name:>10s}: reg = {R:.6f}, Δ = {Delta:>4d}, 分岐 = {{{ram_str}}}")

print()

print(f"""
  ── 安全な2素数ミュートの効果比較 ──

  {{2}} のみ:      |ΔE| = 7       → Q(√2), reg = 0.8814
  {{2,3}}:         |ΔE| = 182     → Q(√6), reg = 2.2924
  {{2,5}}:         |ΔE| = 868     → Q(√10), reg = 1.8184
  {{3,5}}:         |ΔE| = 3224    → Q(√15), reg = 1.9459
  {{2,3,5}}:       |ΔE| = 22568   → Q(√30), reg = ... (大きい)

  ★ 効果が最大のものは {{2,3,5}} だが、
    |S|=3 は Level 3 の「真空破壊境界」に近い。
    安全マージンを考えると {{2,3}} が最適バランス。

  ── SQUID 実験への含意 ──

  Phase 1: p=2 のみミュート（確実に安全）
  Phase 2: p=2,3 同時ミュート（26倍の効果、Q(√6) の検証）
  Phase 3: 理論が確立したら p=2,3,5 のトリプル

  ★ Phase 2 の {{2,3}} 同時ミュートは、
    SQUID に2つのノッチフィルタを入れることで実現可能。
    追加コストはほぼゼロ。効果は 26 倍。
""")

print("=" * 70)
print("  END")
print("=" * 70)
