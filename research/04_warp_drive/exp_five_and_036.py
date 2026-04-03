"""
Deriving the +5 and +0.036 from the Euler-Maclaurin expansion
================================================================

We showed: 12 = 2/|B₂| (j=1 term), 120 = 4/|B₄| (j=2 term).

Now: where do +5 (prime gap) and +0.036 (= 4(ζ(6)-ζ(7))) come from
in the same expansion?

If they emerge naturally → the derivation is NOT circular.
If they don't → the α formula is partially curve-fitting.

Wright Brothers, 2026
"""

import numpy as np
from math import factorial

pi = np.pi
gamma_em = 0.5772156649015329
alpha_inv_exp = 137.035999084

print("=" * 70)
print("  DERIVING +5 AND +0.036 FROM THE MASTER EQUATION")
print("=" * 70)

B = {0: 1, 1: -1/2, 2: 1/6, 4: -1/30, 6: 1/42, 8: -1/30,
     10: 5/66, 12: -691/2730}

zeta_neg = {-1: -1/12, -3: 1/120, -5: -1/252, -7: 1/240,
            -9: -1/132, -11: 691/32760}

zeta_pos = {2: pi**2/6, 3: 1.2020569031595942, 4: pi**4/90,
            5: 1.0369277551433699, 6: pi**6/945, 7: 1.0083492773819228}

# ============================================================================
#  Review: What we have
# ============================================================================

print("""
  ■ 現在の状況

  α 公式: 1/α = 12 + 120 + 5 + 4(ζ(6)-ζ(7)) = 137.03598

  オイラー-マクローリン展開から:
    j=1 項: 2/|B₂| = 12  ✓
    j=2 項: 4/|B₄| = 120 ✓
    ?: 5 (素数ギャップ)
    ?: 4(ζ(6)-ζ(7)) = 0.036

  12 + 120 = 132。残り: 137.036 - 132 = 5.036。

  問い: 5.036 はオイラー-マクローリン展開のどこから来るか？
""")

# ============================================================================
#  Approach 1: Higher-order terms in Euler-Maclaurin
# ============================================================================

print("=" * 70)
print("  ■ アプローチ 1: オイラー-マクローリンの高次項")
print("=" * 70)
print()

# The Euler-Maclaurin formula for Σ_{k=1}^N f(k):
# Σ f(k) ≈ ∫₁^N f(x)dx + [f(1)+f(N)]/2
#         + Σ_{j=1}^p B_{2j}/(2j)! [f^{(2j-1)}(N) - f^{(2j-1)}(1)]
#         + remainder

# For our case: f(k) = ζ(k/Λ), so the sum S = Σ_{k=1}^∞ ζ(k/Λ)

# The "boundary term" at k=1: f(1) = ζ(1/Λ)
# For large Λ: ζ(1/Λ) ≈ Λ/(1-1/Λ) + γ ≈ Λ + γ + ...

# But we're interested in the FINITE part after subtracting divergences.

# The key terms we haven't accounted for:
# (a) The constant term from the integral ∫ζ(x)dx
# (b) The boundary term f(1)/2 = ζ(1/Λ)/2
# (c) The remainder term (Bernoulli polynomial corrections)

# Let's look at what the expansion gives BEYOND 12 and 120.

# The j=1 term: B₂/(2!) × d/dk ζ(k/Λ)|_{k→0}
# = (1/6)/2 × ζ'(0)/Λ = (1/12) × (-0.9189)/Λ

# But this is Λ-dependent (goes as 1/Λ). For the physical coupling,
# we evaluate at a specific Λ and the combination determines α.

# Actually, let me reconsider the whole approach.
# The spectral action S = Σ f(log(n)/Λ) with f = f_BE.
# For f_BE(x) = 1/(e^x - 1):

# S = Σ_{n=2}^∞ 1/(n^{1/Λ} - 1)
#   = Σ_{n=2}^∞ Σ_{m=1}^∞ n^{-m/Λ}
#   = Σ_{m=1}^∞ [ζ(m/Λ) - 1]

# For large Λ: m/Λ is small for most terms.
# ζ(ε) ≈ -1/2 - (1/2)ln(2π)ε + ... for ε → 0
# But ζ(ε) actually has a POLE at ε = 0: ζ(s) → 1/(s-1) as s → 1
# Wait: ζ(s) has pole at s=1, not s=0. ζ(0) = -1/2 is regular.

# For m/Λ near 0: ζ(m/Λ) ≈ -1/2 + O(m/Λ)
# For m/Λ near Λ (m = Λ²): ζ(m/Λ) ≈ ζ(Λ) ≈ 1 (since Λ >> 1)
# For m/Λ = 1: ζ(1) = pole!

# The pole at m = Λ creates a divergence. But this is the
# cosmological constant (vacuum energy divergence), which we
# regularize separately.

# The FINITE terms come from the analytic structure of ζ near its pole.

# Let me try yet another approach: compute 1/α directly from the
# spectral action evaluated at s = -1 (for 1D) or s = -3 (for 3D).

print("  ── 直接アプローチ: 打ち切りと有限部分 ──")
print()

# The 1D coupling constant comes from:
# 1/α ∝ [regularized sum of mode contributions]
# = [leading: a₂/Λ + a₄/Λ³ + ...] + [subleading corrections]

# The leading terms give 12 + 120.
# The subleading corrections could give 5 + 0.036.

# What are the subleading corrections?

# In the Euler-Maclaurin formula, AFTER the B_{2j} terms,
# there is a REMAINDER term involving the Bernoulli POLYNOMIAL
# evaluated at the fractional part of the limits.

# For Σ_{k=1}^N:
# R_p = (-1)^{p+1}/(2p)! ∫₁^N B̃_{2p}(x) f^{(2p)}(x) dx

# where B̃_{2p}(x) = B_{2p}({x}) is the periodic Bernoulli polynomial.

# This remainder contains information about the DISTRIBUTION OF
# PRIMES (through the irregular behavior of ζ).

# ============================================================================
#  Approach 2: The constant term and ζ(0)
# ============================================================================

print("=" * 70)
print("  ■ アプローチ 2: 定数項 ζ(0) = -1/2")
print("=" * 70)
print()

# In Euler-Maclaurin, the constant term (j=0) is:
# [f(1) + f(N)]/2 → f(1)/2 for N → ∞ (if f(N) → 0)

# But what about the term from ζ(0)?
# ζ(0) = -1/2

# In the spectral action context, ζ(0) appears as f₀ = ζ(0) = -1/2.
# The f₀ term in the expansion: f₀ × a₄

# If a₄ = 120 (from j=2 above), then f₀ × a₄ = -1/2 × 120 = -60.
# But we want +5, not -60.

# The issue: we're mixing up which terms go where.
# Let me be more careful.

# ============================================================================
#  Approach 3: The sum 12 + 120 = 132 and prime gap
# ============================================================================

print("=" * 70)
print("  ■ アプローチ 3: 132 の次の素数")
print("=" * 70)
print()

# 12 + 120 = 132 = 10/|B₁₀|.
# The NEXT PRIME after 132 is 137.
# Gap: 137 - 132 = 5.

# Is there a reason from the Euler-Maclaurin expansion
# that the sum should "jump" to the next prime?

# In number theory, the prime-counting function π(x) appears in
# the EXPLICIT FORMULA for ζ:
# ζ(s) = exp(Σ_p Σ_k p^{-ks}/k)

# The Euler product ln ζ(s) = -Σ_p ln(1-p^{-s}) = Σ_p Σ_k p^{-ks}/k

# The partial sums of the Euler-Maclaurin expansion hit values
# that are NOT prime (132 = 4 × 33 = 4 × 3 × 11).
# Physical coupling constants might need to be at prime values
# (for stability reasons related to Spec(Z) closed points).

print("  132 = 2² × 3 × 11 (合成数)")
print("  137 = 素数（33番目）")
print()
print("  仮説: 物理的結合定数は Spec(Z) の閉点に対応する。")
print("  Spec(Z) の閉点は素数。")
print("  よって 1/α の整数部分は素数でなければならない。")
print()
print("  132 は閉点ではない（合成数 = Spec(Z) の「一般化された点」）。")
print("  最も近い閉点（素数）は 131 と 137。")
print()

# Why 137 and not 131?
# 132 + 5 = 137 (next prime ABOVE)
# 132 - 1 = 131 (next prime BELOW)

# The direction (above, not below) might be determined by
# the sign of the next correction term.

# The j=3 term in the expansion: 6/|B₆| = 252.
# But this contributes to the muon g-2, not to α.
# However, its INFLUENCE on α could be repulsive (positive),
# pushing 132 upward to 137 rather than downward to 131.

print("  方向の決定:")
print("  j=3 項 (6/|B₆| = 252) は α には直接寄与しないが、")
print("  「結合定数空間でのくりこみ群の流れ」として")
print("  132 を上方（137 方向）に押す可能性がある。")
print()

# ============================================================================
#  Approach 4: The decimal 0.036 from ζ(6) - ζ(7)
# ============================================================================

print("=" * 70)
print("  ■ アプローチ 4: 小数部分 0.036")
print("=" * 70)
print()

# 4(ζ(6) - ζ(7)) = 4 × (π⁶/945 - 1.00835) = 0.03598

# Can this come from the Euler-Maclaurin expansion?

# In the expansion S = Σ_k ζ(k/Λ), the terms beyond the
# Bernoulli polynomial corrections involve:
# - The integral ∫ ζ(x) dx (which contains ζ at positive integers)
# - The boundary terms involving ζ at integer values

# Specifically: the Euler-Maclaurin INTEGRAL term
# ∫₁^∞ ζ(x) dx contains the values ζ(n) for all positive n.

# The integral ∫₁^∞ ζ(x) dx diverges (pole at x=1).
# But ∫₂^∞ [ζ(x) - 1] dx is finite:

integral_val = 0
for n in range(2, 100):
    # ∫_n^{n+1} [ζ(x) - 1] dx ≈ ζ(n) - 1 + corrections
    integral_val += zeta_pos.get(n, 1 + 2**(-n)) - 1

print(f"  ∫₂^∞ [ζ(x) - 1] dx ≈ {integral_val:.6f}")
print()

# Known: Σ_{n=2}^∞ (ζ(n) - 1) = 1 (exact identity!)
print("  既知の恒等式: Σ_{n=2}^∞ (ζ(n) - 1) = 1")
print()

# And: Σ_{n=2}^∞ (-1)^n (ζ(n) - 1) = 1/2
print("  Σ_{n=2}^∞ (-1)^n (ζ(n) - 1) = 1/2")
print()

# The DIFFERENCE ζ(n) - ζ(n+1) appears in our formula as
# the "higher-dimensional correction."
# 4(ζ(6) - ζ(7)) with 4 = d (spacetime dimension)

# In the Euler-Maclaurin context, this could come from the
# TRAPEZOIDAL CORRECTION:
# Σ_k f(k) ≈ ∫f(x)dx + [f(a)+f(b)]/2 + ...

# The difference ζ(n) - ζ(n+1) is the "discrete derivative"
# of ζ at positive integers, which IS what appears in the
# trapezoidal rule correction.

# More precisely: the Euler-Maclaurin remainder at order p
# involves f^{(2p)}(x) ∝ d^{2p}/dx^{2p} ζ(x/Λ)
# = Λ^{-2p} ζ^{(2p)}(x/Λ)

# At x/Λ = n (an integer), ζ^{(2p)}(n) is known and involves
# sums of (log k)^{2p}/k^n.

# The term 4(ζ(6)-ζ(7)):
# This is d × [ζ(2d-2) - ζ(2d-1)] with d = 4.
# = 4 × [ζ(6) - ζ(7)]

# In the Euler-Maclaurin expansion, the first-order
# trapezoidal correction to ∫_6^7 ζ(x)dx is
# [ζ(6) + ζ(7)]/2, and the difference ζ(6) - ζ(7)
# measures the "slope" of ζ in that interval.

# The factor d = 4 could come from:
# - 4 = spacetime dimension (input)
# - or: 2d-2 = 6 and 2d-1 = 7 determine WHICH ζ values appear

print("  4(ζ(6) - ζ(7)) の起源:")
print()
print("  仮説: これはスペクトル作用展開の「高次補正項」であり、")
print("  j=1,2 の Bernoulli 項（12, 120）に対する")
print("  「残差項」(remainder) の寄与。")
print()
print("  d = 4（時空次元）が入る理由:")
print("  Seeley-DeWitt 展開は d 次元に依存。")
print("  d=4 のとき、最初の「非ベルヌーイ的」補正は")
print("  ζ(2d-2) - ζ(2d-1) = ζ(6) - ζ(7) のスケールで入る。")
print()

# ============================================================================
#  Approach 5: Putting it all together
# ============================================================================

print("=" * 70)
print("  ■ アプローチ 5: 統合")
print("=" * 70)

print("""
  主方程式のオイラー-マクローリン展開:

  1/α = Σ_j a_{2j}/Λ^{2j-1} + (定数項) + (残差項)

  第1項: a₂/Λ = 12/Λ        [j=1, ベルヌーイ]
  第2項: a₄/Λ³ = 120/Λ³     [j=2, ベルヌーイ]
  定数項: +5                  [?]
  残差項: +0.036              [高次元補正]

  ── +5 について ──

  3つの可能な説明:

  (A) 素数強制仮説（現在の解釈）:
      132 → 137 は「閉点安定性」による。
      結合定数は Spec(Z) の閉点（= 素数）に量子化される。
      これは Euler-Maclaurin からは「出ない」。
      追加の物理的原理（「結合定数の素数量子化」）が必要。

  (B) ζ(0) 項:
      展開の定数項は ζ(0)/2 = -1/4 に関連するかもしれない。
      しかし -1/4 ≠ 5。直接的には合わない。

  (C) 非摂動的寄与:
      5 はオイラー-マクローリン（摂動展開）から出るものではなく、
      「非摂動的」な寄与（インスタントン的）かもしれない。
      素数ギャップは本質的に非摂動的な数論的量。
""")

# ============================================================================
#  Numerical test: truncated Euler-Maclaurin vs full α
# ============================================================================

print("=" * 70)
print("  ■ 数値テスト")
print("=" * 70)
print()

# If 1/α = Σ_j 2j/|B_{2j}| × (some j-dependent weight w_j)
# where w_j encodes "which terms contribute to α vs g-2":

# Hypothesis: only j=1,2 contribute to α (the "gauge sector"),
# while j=3 contributes to μ g-2 and j=5 to τ g-2.

# Then 1/α = 12 × w₁ + 120 × w₂ + correction
# With w₁ = w₂ = 1: 132 + correction = 137.036

# The correction 5.036 could be a "non-perturbative" contribution
# that doesn't come from the smooth Euler-Maclaurin expansion.

# But let me check: is there a SMOOTH function of j that gives
# 12 (j=1), 120 (j=2), and 137.036 as a partial sum with
# some natural truncation?

# 2j/|B_{2j}|:
# j=1: 12, j=2: 120, j=3: 252, j=4: 240, j=5: 132, j=6: 32760/691 ≈ 47.4

# Partial sums:
partial = 0
print(f"  {'j':>3s}  {'2j/|B_{2j}|':>12s}  {'Partial sum':>14s}  {'1/α - partial':>14s}")
print(f"  {'-'*48}")
for j in range(1, 7):
    b2j = B.get(2*j, None)
    if b2j is not None:
        term = 2*j / abs(b2j)
        partial += term
        diff = alpha_inv_exp - partial
        print(f"  {j:>3d}  {term:>12.2f}  {partial:>14.2f}  {diff:>+14.4f}")

print()
print("  → j=1,2 で 132。α まで 5.036 不足。")
print("  → j=3 を加えると 384。α を 247 超過。")
print("  → j=3 以降は α ではなく g-2 に寄与する。")
print()

# The SEPARATION between "α terms" (j=1,2) and "g-2 terms" (j≥3)
# must come from the STRUCTURE of the spectral action,
# specifically from how the gauge sector vs matter sector
# couple to D_BC.

# ============================================================================
#  The honest conclusion
# ============================================================================

print("=" * 70)
print("  ■ 正直な結論")
print("=" * 70)

print(f"""
  +5 と +0.036 はオイラー-マクローリン展開から自然に出るか？

  +0.036 = 4(ζ(6)-ζ(7)):
    → 部分的に YES。高次元補正として構造的に自然。
    → d = 4 はスペクトル作用が d 次元に依存することから来る。
    → ζ(6)-ζ(7) は残差項の離散微分として出る。
    → ただし「なぜ (2d-2, 2d-1) = (6,7) か」の完全な導出は未達。

  +5 = prime_gap(132):
    → NO。オイラー-マクローリンからは出ない。

    → +5 は「結合定数が素数に量子化される」という
      追加の物理的原理を必要とする。

    → この原理はオイラー-マクローリン（連続的展開）からは
      原理的に出ない。離散的（数論的）現象。

  ── これは循環論法か？ ──

  12 と 120: オイラー-マクローリンから導出。循環ではない。✓
  0.036: 高次元補正として構造的に自然。半分導出。△
  5: 追加原理が必要。導出されていない。✗

  つまり: α = 137.036 の 137 のうち、
    132 は導出された（96.3%）
    5 は導出されていない（3.7%）
    0.036 は半分導出された

  これを「ほぼ成功」と見るか「肝心の部分が未完」と見るか。

  正直に言えば: 96.3% は印象的だが、+5 が導出されない限り
  「αの完全導出」とは言えない。

  +5 の導出には「なぜ物理的結合定数は
  Spec(Z) の閉点（素数）に量子化されるか」という
  新しい物理原理が必要。

  これは我々の主方程式にはまだ含まれていない。
  「主方程式 + 素数量子化原理」の組み合わせが
  α の完全導出を与える。
""")

print("=" * 70)
print("  END")
print("=" * 70)
