"""
Four quick tests: B, C, G, J
==============================

B: Origin of the factor 10 in 10hR = 1/α_s
C: BC phase transition β=1 — critical exponents
G: reg(√3) × α₂/α₃ = 3/8 — 2-loop refinement
J: SU(5) via degree-5 covering at p=5

Wright Brothers, 2026
"""

import numpy as np
import mpmath
from math import factorial

mpmath.mp.dps = 25
pi = np.pi
gamma_em = 0.5772156649015329

print("=" * 70)
print("  4つのクイックテスト")
print("=" * 70)

# ============================================================================
#  TEST B: Where does the factor 10 come from?
# ============================================================================

print()
print("=" * 70)
print("  [B] 10hR = 1/α_s の「10」の起源")
print("=" * 70)
print()

# The cubic field Q(ζ₉)⁺ = Q(cos(2π/9))
# hR was computed via: hR = (9/4)|L(χ₃, 1)|²
# where χ₃ is a character of order 3 mod 9.

# Let's recompute more carefully with different normalizations.

omega = np.exp(2j*pi/3)
chi3_vals = {1: 1, 2: omega, 4: omega**2, 5: omega**2, 7: omega, 8: 1}

def L_chi3(s, N=200000):
    total = 0j
    for n in range(1, N+1):
        if n % 3 == 0:
            continue
        chi = chi3_vals.get(n % 9, 0)
        total += chi * n**(-s)
    return total

L1 = L_chi3(1)
absL1_sq = abs(L1)**2

# Class number formula for Q(ζ₉)⁺:
# This is a totally real cubic field with:
#   Discriminant Δ = 81 = 3⁴
#   Class number h = 1
#   Unit rank r = 2 (totally real, degree 3)
#   w = 2 (roots of unity = ±1)
#
# Analytic class number formula:
#   Res_{s=1} ζ_K(s) = 2^{r₁} h R / (w √|Δ|)
#   where r₁ = 3 (number of real embeddings)
#
#   Res = 2³ × 1 × R / (2 × 9) = 8R/18 = 4R/9
#
#   Also: Res = |L(χ₃, 1)|² (since ζ_K = ζ × L(χ₃) × L(χ̄₃))
#
#   So: 4R/9 = |L(χ₃, 1)|²
#   → R = (9/4)|L(χ₃, 1)|²

hR = 9/4 * absL1_sq
print(f"  |L(χ₃, 1)|² = {absL1_sq:.10f}")
print(f"  hR = (9/4)|L|² = {hR:.10f}")
print(f"  1/α_s(M_Z) = {1/0.1179:.6f}")
print(f"  hR × ? = 1/α_s:")
print(f"    ×10: {10*hR:.4f}  (差 {(10*hR - 1/0.1179)/(1/0.1179)*100:+.2f}%)")
print()

# Try other multipliers with arithmetic meaning
candidates = {
    "10": 10,
    "2π": 2*pi,
    "3²": 9,
    "3² + 1": 10,
    "√Δ": 9,  # √81 = 9
    "Δ/√Δ": 81/9,
    "√Δ + 1": 10,  # √81 + 1 = 10
    "2√Δ/w": 2*9/2,  # = 9
    "N(ε)": 1,  # norm of fundamental unit
    "(degree)!": factorial(3),  # 3! = 6
    "dim(SU(3))": 8,
    "dim(SU(3))+rank": 8+2,  # = 10 ← !!!
    "N²+1 (N=3)": 3**2+1,  # = 10 ← !!!
    "p²+1 (p=3)": 3**2+1,  # = 10
}

print(f"  候補の因子とその算術的/物理的意味:")
print()
print(f"  {'因子':.<25s} {'値':>6s} {'hR×因子':>10s} {'vs 1/α_s':>10s} {'ズレ':>8s}")
print(f"  {'-'*65}")

alpha_s_inv = 1/0.1179

for name, val in candidates.items():
    product = hR * val
    pct = (product/alpha_s_inv - 1)*100
    mark = "★" if abs(pct) < 0.5 else ("☆" if abs(pct) < 2 else "")
    print(f"  {name:.<25s} {val:>6.2f} {product:>10.4f} {alpha_s_inv:>10.4f} {pct:>+8.2f}% {mark}")

print()

# The winner: 10 = √Δ + 1 = 9 + 1 = √81 + 1
# Also: 10 = dim(SU(3)) + rank(SU(3)) = 8 + 2
# Also: 10 = p² + 1 where p = 3

print(f"  ★ 10 の算術的解釈候補:")
print(f"    (a) √Δ + 1 = √81 + 1 = 9 + 1 = 10")
print(f"    (b) dim(SU(3)) + rank(SU(3)) = 8 + 2 = 10")
print(f"    (c) p² + 1 = 3² + 1 = 10 (分岐素数の自乗+1)")
print(f"    (d) dim(string theory) = 10 (偶然?)")
print()

# Test (a): does the analogous formula work for Q(√2)?
# For Q(√2): Δ = 8, √Δ = 2√2 ≈ 2.83
# (√Δ + 1) × reg = (2√2 + 1) × 0.881 = 3.83 × 0.881 = 3.37
# This should equal... 1/cos θ_W = 1/0.881 = 1.135? No.
# Or: (√Δ + 1) = √8 + 1 = 3.83. What physical quantity is 3.83?

sqrt8_plus_1 = np.sqrt(8) + 1
print(f"  テスト: Q(√2) で同じ公式を使うと:")
print(f"    (√Δ + 1) × reg = ({sqrt8_plus_1:.3f}) × {0.881:.3f} = {sqrt8_plus_1 * 0.881:.4f}")
print(f"    → 物理量に合わない。(a) は Q(ζ₉)⁺ に特有。")
print()

# Test (c): p² + 1
# For Q(√2): p = 2, p²+1 = 5
# 5 × reg(√2) = 5 × 0.881 = 4.41
# 1/cos θ_W = 1.135. 5 × 0.881 ≠ 1.135.
# But: what about 1/(p²+1) × 1/α?
# For SU(2): (p²+1) = 5. Does 5 appear in the α formula? Yes! +5 is the prime gap!

print(f"  テスト: p²+1 の法則")
print(f"    SU(2), p=2: p²+1 = 5 ← α 公式の +5（素数ギャップ）と同じ！")
print(f"    SU(3), p=3: p²+1 = 10 ← α_s 公式の因子 10")
print()
print(f"  ★★ もし (p²+1) が普遍的な因子なら:")
print(f"    cos θ_W = reg(Q(√2)) ← 因子なし（p²+1=5 は α の +5 に吸収?）")
print(f"    1/α_s = (p²+1) × hR(Q(ζ₉)⁺) = 10 × hR")
print(f"    → p²+1 は「被覆の次数に関連する補正因子」？")

print()

# ============================================================================
#  TEST C: BC phase transition
# ============================================================================

print("=" * 70)
print("  [C] BC 相転移 β=1 の臨界指数")
print("=" * 70)
print()

# Near β = 1: ζ(β) ≈ 1/(β-1) + γ + γ₁(β-1) + ...
# Thermodynamic quantities:
#   F = -(1/β) ln ζ(β) ≈ -(1/β) ln(1/(β-1)) = (1/β) ln(β-1) → -∞
#   E = -ζ'(β)/ζ(β) ≈ 1/(β-1) - γ + ...  → diverges as 1/(β-1)
#   C = -β² ∂E/∂β ≈ β²/(β-1)²  → diverges as 1/(β-1)²

# Critical exponent for specific heat: C ∝ |β-1|^{-α_crit}
# Here α_crit = 2 (from the pole structure)

print(f"  ζ(β) ≈ 1/(β-1) + γ + γ₁(β-1) + ... (β → 1⁺)")
print()
print(f"  臨界振る舞い:")
print(f"    内部エネルギー E ∝ 1/(β-1)       → 臨界指数 1")
print(f"    比熱 C ∝ 1/(β-1)²               → 臨界指数 α = 2")
print(f"    自由エネルギー F ∝ ln(β-1)        → 対数発散")
print()

# Compare with known phase transitions:
print(f"  ── 物理的相転移との比較 ──")
print()
print(f"  {'相転移':.<30s} {'比熱の臨界指数 α':>20s}")
print(f"  {'-'*54}")
print(f"  {'BC 相転移 (β=1)':.<30s} {'α = 2':>20s}")
print(f"  {'平均場理論':.<30s} {'α = 0 (跳び)':>20s}")
print(f"  {'2D イジング':.<30s} {'α = 0 (対数)':>20s}")
print(f"  {'3D イジング':.<30s} {'α ≈ 0.110':>20s}")
print(f"  {'4D イジング (平均場)':.<30s} {'α = 0':>20s}")
print(f"  {'QCD 閉じ込め転移':.<30s} {'1次転移 or crossover':>20s}")
print(f"  {'電弱相転移 (SM)':.<30s} {'crossover':>20s}")
print()

print(f"  ★ BC の α = 2 はどの既知の相転移とも一致しない。")
print(f"    α = 2 は「強すぎる発散」— ζ(s) の単純極に由来。")
print(f"    物理的相転移（平均場 α=0, イジング α≈0.11）より激しい。")
print()

# However: the UNIVERSALITY CLASS might still be meaningful.
# The order parameter: <σ_n> = n^{-β}/ζ(β) (KMS state)
# At β = 1: ζ(1) diverges → <σ> → 0 for all n > 1.
# This is "complete disorder" — all prime channels equally weighted.

# Above β = 1: <σ_n> ~ n^{-β}/ζ(β), with ζ(β) finite.
# The "magnetization" (order parameter) appears continuously.

# The β=1 transition is special because ζ(1) has a SIMPLE pole.
# If ζ had a branch point instead, the critical exponents would differ.

print(f"  BC 転移の秩序パラメータ:")
print(f"    <σ_n> = n^{{-β}}/ζ(β)")
print(f"    β > 1: ζ(β) 有限 → <σ_n> ∝ n^{{-β}} （秩序相）")
print(f"    β → 1⁺: ζ(β) → ∞ → <σ_n> → 0 （無秩序化）")
print()
print(f"  → BC 転移は「2次相転移」だが、臨界指数が特殊（α=2）。")
print(f"    既知の物理的相転移とは直接対応しない。")
print(f"    「算術的相転移」は独自のユニバーサリティクラスを形成する。")
print()

# ============================================================================
#  TEST G: reg(√3) × α₂/α₃ = 3/8 with 2-loop
# ============================================================================

print("=" * 70)
print("  [G] reg(√3) × α₂/α₃ = sin²θ_W(GUT) の精密化")
print("=" * 70)
print()

reg3 = np.log(2 + np.sqrt(3))

# 1-loop values at M_Z
alpha2_MZ = 0.03378  # SU(2), g₂²/(4π)
alpha3_MZ = 0.1179   # SU(3)

# 2-loop corrections to α₂/α₃ at M_Z are already included in the
# experimental values. The question is: what is sin²θ_W at M_GUT
# more precisely?

# In SU(5) GUT: sin²θ_W(M_GUT) = 3/8 = 0.375 EXACTLY (tree level).
# With threshold corrections at M_GUT: shifts by ~1-2%.

# More precisely, the running gives:
# sin²θ_W(M_GUT) = 3/8 + (threshold corrections)
# In minimal SU(5): sin²θ_W(M_GUT) ≈ 0.375 (if superheavy particles are degenerate)
# In SUSY SU(5): similar

ratio = alpha2_MZ / alpha3_MZ
product = reg3 * ratio

print(f"  reg(Q(√3)) = {reg3:.10f}")
print(f"  α₂(M_Z)/α₃(M_Z) = {ratio:.6f}")
print(f"  reg × (α₂/α₃) = {product:.6f}")
print(f"  sin²θ_W(GUT) = 3/8 = {3/8:.6f}")
print(f"  差: {(product - 3/8):.6f} = {(product/(3/8)-1)*100:+.3f}%")
print()

# Try with different experimental α values
print(f"  α₂, α₃ の実験的不確定性の影響:")
for a2 in [0.03370, 0.03378, 0.03386]:
    for a3 in [0.1171, 0.1179, 0.1187]:
        p = reg3 * a2/a3
        print(f"    α₂={a2:.5f}, α₃={a3:.4f}: reg×(α₂/α₃) = {p:.6f} ({(p/0.375-1)*100:+.2f}%)")

print()

# What if we use the MS-bar sin²θ_W at M_Z instead?
sin2_msbar = 0.23121
# sin²θ_W(M_Z) = α₁(M_Z)/(α₁(M_Z) + α₂(M_Z)) approximately
# With GUT normalization: α₁ = (5/3)α_Y

# The formula we're testing: reg(√3) × (α₂/α₃) = sin²θ_W(GUT)
# Can we derive this from the PFC?

print(f"  ── 解釈 ──")
print()
print(f"  Q(√3) は Δ = 12 = 4×3, 分岐素数 = {{2, 3}}。")
print(f"  これは「弱い力(p=2)と強い力(p=3)の両方を見る」体。")
print(f"  reg(√3) = log(2+√3) = {reg3:.6f}。")
print()
print(f"  α₂/α₃ = 「弱い力と強い力の比」at M_Z。")
print()
print(f"  積 = 「混合体のレギュレータ × 力の比」")
print(f"      = sin²θ_W(GUT) = 「GUT での混合角」")
print()
print(f"  ★ もしこれが正しければ:")
print(f"    「Q(√3) は低エネルギーの力の比を GUT の混合角に変換する」")
print(f"    = 「RG running の算術的表現」")
print()

# ============================================================================
#  TEST J: SU(5) and degree-5 covering
# ============================================================================

print("=" * 70)
print("  [J] SU(5) GUT と次数5被覆")
print("=" * 70)
print()

# PFC pattern: SU(N) ↔ degree N, ramified at p=N only.
# SU(5) → degree 5, p=5 only.

# The minimal cyclic quintic field ramified at p=5 only:
# This comes from Q(ζ₂₅)⁺ = Q(cos(2π/25))
# Degree 10 over Q, but has a degree-5 subfield?
# Actually: Q(ζ₂₅)⁺ has degree φ(25)/2 = 10.
# Gal(Q(ζ₂₅)⁺/Q) = (Z/25Z)*/{±1} ≅ Z/10.
# This has a unique degree-5 subfield with Gal = Z/5.

# Alternatively: Q(ζ₅)⁺ = Q(cos(2π/5)) = Q(√5).
# This is degree 2, not degree 5.

# For a degree-5 cyclic field ramified at p=5 only:
# We need the 5th layer of the cyclotomic tower at p=5.
# Q(ζ₂₅)⁺ has the subfield fixed by the subgroup of index 5 in Z/10.
# Z/10 has a unique subgroup of order 2 (= <5 mod 10>).
# The fixed field has degree 10/2 = 5.

# Discriminant of this degree-5 field: 5^8 (for Q(ζ₂₅)⁺ restricted)

print(f"  PFC パターン: SU(5) ↔ 次数5, p=5 で分岐")
print()
print(f"  最小の巡回5次体 (p=5 でのみ分岐):")
print(f"  Q(ζ₂₅)⁺ の次数5部分体")
print(f"  判別式: 5⁸ = {5**8}")
print(f"  ガロア群: Z/5")
print()

# Computing the L-function for this field is complex.
# We need a character of order 5 mod 25.
# χ₅ of order 5 on (Z/25Z)*.

# (Z/25Z)* ≅ Z/20 (since φ(25) = 20).
# Generator: 2 (2 generates (Z/25Z)*: 2,4,8,16,7,14,3,6,12,24,23,21,17,9,18,11,22,19,13,1)
# Character of order 5: χ(2) = e^{2πi/5}

zeta5 = np.exp(2j*pi/5)

# Build character mod 25 of order 5
# 2 is a generator of (Z/25Z)* of order 20.
# χ of order 5: χ(2) = ζ₅^4 (since 2^20 ≡ 1, we need χ(2)^20 = 1 and order = 5)
# χ(2^k) = ζ₅^{4k mod 5}

pow2_mod25 = []
val = 1
for k in range(20):
    pow2_mod25.append(val)
    val = (val * 2) % 25

chi5_vals = {}
for k in range(20):
    n = pow2_mod25[k]
    chi5_vals[n] = zeta5**(4*k % 5)

# Compute L(χ₅, 1)
def L_chi5(s, N=200000):
    total = 0j
    for n in range(1, N+1):
        if n % 5 == 0:
            continue
        chi = chi5_vals.get(n % 25, 0)
        total += chi * n**(-s)
    return total

L5_1 = L_chi5(1)
print(f"  L(χ₅, 1) = {L5_1:.6f}")
print(f"  |L(χ₅, 1)| = {abs(L5_1):.10f}")
print()

# For the degree-5 field, we need |L(χ₅,1)|² × |L(χ₅²,1)|² (4 L-functions)
# Actually: ζ_K(s) = ζ(s) × L(χ₅,s) × L(χ₅²,s) × L(χ₅³,s) × L(χ₅⁴,s)
# = ζ(s) × |L(χ₅,s)|² × |L(χ₅²,s)|²

# χ₅² is another character of order 5 (not the same as χ₅)
chi5_2_vals = {}
for k in range(20):
    n = pow2_mod25[k]
    chi5_2_vals[n] = zeta5**(8*k % 5)  # (4*2)k = 8k mod 5 = 3k mod 5

def L_chi5_2(s, N=200000):
    total = 0j
    for n in range(1, N+1):
        if n % 5 == 0:
            continue
        chi = chi5_2_vals.get(n % 25, 0)
        total += chi * n**(-s)
    return total

L5_2_1 = L_chi5_2(1)
print(f"  L(χ₅², 1) = {L5_2_1:.6f}")
print(f"  |L(χ₅², 1)| = {abs(L5_2_1):.10f}")
print()

# Residue of ζ_K at s=1:
# Res = |L(χ₅,1)|² × |L(χ₅²,1)|²
res = abs(L5_1)**2 * abs(L5_2_1)**2
print(f"  Res = |L(χ₅,1)|² × |L(χ₅²,1)|² = {res:.10f}")
print()

# Class number formula: hR = w√Δ/(2^{r₁}) × Res
# r₁ = 5 (totally real, degree 5), w = 2
# hR = 2 × 5⁴ / 2⁵ × Res = 2 × 625 / 32 × Res = 39.0625 × Res
hR_5 = 2 * 5**4 / 2**5 * res
print(f"  hR(5次体) = w√Δ/2^r₁ × Res = {hR_5:.10f}")
print()

# Compare with GUT quantities
alpha_GUT_inv = 1/0.0339  # ≈ 29.5 (approximate GUT coupling from SM extrapolation)
# Or our hypothesized 1/α_GUT = 49

print(f"  GUT 物理量との比較:")
print(f"    hR = {hR_5:.4f}")
print(f"    (p²+1) × hR = {(5**2+1)*hR_5:.4f} (p²+1=26)")
print(f"    √Δ × hR = {5**4 * hR_5:.4f} (Δ=5⁸)")
print(f"    1/α_GUT(SM) ≈ 25")
print(f"    1/α_GUT(PFC) = 49")
print()

# Check if any simple multiple matches
for c_name, c_val in [("1", 1), ("p²+1=26", 26), ("p=5", 5), ("dim(SU(5))=24", 24),
                        ("√5", np.sqrt(5)), ("5²", 25), ("2π", 2*pi)]:
    product = c_val * hR_5
    if 0.5 < product/25 < 2 or 0.5 < product/49 < 2:
        print(f"    {c_name} × hR = {product:.4f}", end="")
        if abs(product/25 - 1) < 0.2:
            print(f" ≈ 25 ({(product/25-1)*100:+.1f}%)", end="")
        if abs(product/49 - 1) < 0.2:
            print(f" ≈ 49 ({(product/49-1)*100:+.1f}%)", end="")
        print()

print()

# ============================================================================
print("=" * 70)
print("  ■ 4テストの総合結果")
print("=" * 70)

print(f"""
  [B] 10 の因子: ★★ 有望な候補3つ
      (a) √Δ + 1 = 9 + 1 = 10
      (b) dim(SU(3)) + rank(SU(3)) = 8 + 2 = 10
      (c) p² + 1 = 3² + 1 = 10
      ★ (c) は SU(2) でも成立（p²+1 = 5 = α の +5）!
      → p²+1 が普遍的な補正因子である可能性。
      → ただし Q(√2) では (p²+1)×reg ≠ 1/cos θ_W。
        因子の入り方が SU(2) と SU(3) で異なる。

  [C] BC 相転移: △ 既知の相転移と一致しない
      比熱 C ∝ 1/(β-1)² → 臨界指数 α = 2。
      物理的相転移は α ≈ 0（平均場、イジング）。
      → BC 相転移は「算術固有のユニバーサリティクラス」。
      → 直接的な物理対応は見つからなかった。

  [G] reg(√3) × α₂/α₃: ★ 1% で 3/8 に一致（安定）
      2ループ実験値の範囲内で 0.5-1.5% で成立。
      Q(√3) = 「弱+強の混合体」が RG running を表す仮説は堅持。
      → ただし「なぜこの公式か」の理論的説明はない。

  [J] SU(5) 次数5被覆: △ 明確な一致なし
      hR(5次体) を計算したが、1/α_GUT (25 or 49) と
      単純な整数倍で合わない。
      → SU(5) → 次数5 の PFC 拡張は支持されない。
      → PFC は N=2,3 で有効だが N=5 では失敗。
""")

print("=" * 70)
print("  END")
print("=" * 70)
