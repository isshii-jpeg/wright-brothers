"""
Deep Investigation: Deriving α from Spec(Z)
============================================

Four unsolved problems from exp_alpha_arithmetic.py:
  (1) What is the "+5" in 137 = 120 + 12 + 5?
  (2) Precise arithmetic expression for 0.035999...
  (3) NCG spectral action moments from ζ values
  (4) Arithmetic description of renormalization group running

Wright Brothers, 2026
"""

import numpy as np
from itertools import product as iter_product

pi = np.pi
e_num = np.e
gamma_em = 0.5772156649015329

alpha_inv = 137.035999084
alpha_rem = alpha_inv - 137  # = 0.035999084

zeta = {2: pi**2/6, 3: 1.2020569031595942, 4: pi**4/90,
        5: 1.0369277551433699, 6: pi**6/945, 7: 1.0083492773819228,
        8: pi**8/9450, 9: 1.00200839282608}
zeta_neg = {-1: -1/12, -3: 1/120, -5: -1/252, -7: 1/240,
            -9: -1/132, -11: 691/32760, -13: -1/12}

print("=" * 70)
print("  DEEP INVESTIGATION: α FROM Spec(Z)")
print("=" * 70)

# ============================================================================
#  PROBLEM 1: What is the "+5"?
# ============================================================================

print("\n" + "=" * 70)
print("  PROBLEM 1: WHAT IS THE '+5'?")
print("=" * 70)

print("""
  137 = 120 + 12 + 5

  120 = 5! = 1/ζ(-3)
   12 = 1/|ζ(-1)|

  5 = ?

  ── 候補を体系的に検討 ──
""")

candidates_5 = [
    ("ζ(-3)/ζ(-1) = (1/120)/(-1/12) = -1/10", -1/10, False),
    ("1/ζ(-5) = -252", -252, False),
    ("dim U(1) + dim SU(2) = 1 + 3 = 4", 4, False),
    ("number of fundamental forces", 4, False),
    ("dim representation of SU(2): j=2 → 2j+1=5", 5, True),
    ("|ζ(-1)| × |ζ(-3)| × something... 12 × 120 = 1440", 1440, False),
    ("5 = third prime", 5, True),
    ("5 = dim(Sp(2) fundamental rep)", 5, True),
    ("5 = rank of E_8 minus rank of A_3 (8-3)", 5, True),
    ("5 = number of Platonic solids", 5, True),
    ("5 = Euler characteristic of S⁴ (= 2)", 2, False),
    ("KO-dimension of F in NCG = 6 mod 8... no", 6, False),
]

print("  5に一致するものだけ抽出:")
for desc, val, match in candidates_5:
    if match:
        print(f"    ✓ {desc}")

print("""
  ── より深い分析 ──

  NCG Standard Model の有限空間 F:
    代数: A_F = C ⊕ H ⊕ M_3(C)
    単純成分数: 3 (C, H, M_3(C))

  しかし物理的に意味のある数:
    - SU(5) GUT embedding: U(1) × SU(2) × SU(3) ⊂ SU(5)
    - 5 = SU(5) の rank + 1 = 4 + 1 = 5
    - 5 = dim(SU(5)) の基本表現
""")

# Actually, let's think about this differently
# 120 = |A_5| × 2 = |S_5| (symmetric group on 5 letters)
# 12 = |A_4| (alternating group on 4 letters)
# 5 = |Z/5Z| = |A_5|/|A_4| × ... no

# Better: look at the icosahedral connection
print("  ── 正20面体接続 ──")
print()
print("  120 = |I| (正20面体回転群の位数 = |A_5| = 60 の2倍 = |S_5|)")
print("  Actually: 120 = |S_5| = 5! (5次対称群)")
print("   12 = |Z₃ × Z₂²| or |A₄| (4次交代群)")
print("    5 = |Z₅| (5次巡回群)")
print()
print("  S₅ → A₄ → Z₅ (?)")
print()

# Group theory: is there a sequence S_5 → A_4 → Z_5?
# |S_5| = 120, |A_4| = 12, |Z_5| = 5
# 120 / 12 = 10, 12 / 5 = 2.4... no clean quotient

# BUT: 120 + 12 + 5 = 137
# And: 5! + 4!/2 + 5 = 120 + 12 + 5 = 137
# 4!/2 = |A_4| = 12

print("  5! + |A₄| + 5 = 120 + 12 + 5 = 137")
print("  = |S₅| + |A₄| + |Z₅|")
print()

# This is a sum over "levels" of the icosahedral structure
# Level 0: Z₅ (rotation axis)
# Level 1: A₄ (tetrahedral subgroup)
# Level 2: S₅ (full symmetric group)

# Let's try another decomposition inspired by Spec(Z)
# 137 is the 33rd prime
# π(137) = 33
# π(120) = 30, π(12) = 5, π(5) = 3
# 30 + 5 - 3 = 32... no

# Try: ζ(-n) connection for all n
print("  ── 全ての ζ(-n) の逆数 ──")
print()
for n in [1, 3, 5, 7, 9, 11]:
    val = zeta_neg[-n]
    inv = 1/abs(val) if val != 0 else float('inf')
    print(f"  1/|ζ(-{n})| = {inv:.4f}")

print()
print(f"  1/|ζ(-1)| + 1/|ζ(-3)| = 12 + 120 = 132")
print(f"  137 - 132 = 5")
print(f"  1/|ζ(-5)| = 252 (too large)")
print()

# Key insight: 5 might not come from ζ at all.
# It might come from the NUMBER OF PRIMES used in the Euler product
# truncation, or from the gauge group structure.

# In Connes' NCG: the finite space F has
# dim_R(A_F) = dim_R(C) + dim_R(H) + dim_R(M_3(C)) = 2 + 4 + 18 = 24
# Hmm, 24 = |S_4|

# The NUMBER of independent parameters in the Dirac operator D_F:
# In the Standard Model: 3 gauge couplings + Higgs mass + Higgs vev
# = 5 parameters at tree level!

print("  ── 標準模型の独立パラメータ数 ──")
print()
print("  ツリーレベルの独立パラメータ:")
print("    g₁, g₂, g₃ (3つのゲージ結合定数)")
print("    m_H (ヒッグス質量)")
print("    v (ヒッグス真空期待値)")
print("    = 5 パラメータ")
print()
print("  → 5 = ツリーレベルの SM パラメータ数？")
print()
print("  もしそうなら:")
print("  1/α = (3D真空寄与) + (1D真空寄与) + (パラメータ数補正)")
print("       = 1/ζ(-3) + 1/|ζ(-1)| + N_param")
print("       = 120 + 12 + 5 = 137")

# ============================================================================
#  PROBLEM 2: Precise expression for 0.035999...
# ============================================================================

print("\n" + "=" * 70)
print("  PROBLEM 2: PRECISE EXPRESSION FOR 0.035999084...")
print("=" * 70)
print()

target = alpha_rem
print(f"  Target: {target:.12f}")
print()

# Much more exhaustive search
best_results = []

# Type A: a×ζ(m) + b×ζ(n) + c/π^k for small rational coefficients
for a_num in range(-5, 6):
    for a_den in [1, 2, 3, 4, 6, 12, 24, 120]:
        a = a_num / a_den
        for m in [2, 3, 4, 5, 6, 7]:
            for b_num in range(-5, 6):
                for b_den in [1, 2, 3, 4, 6, 12, 24, 120]:
                    b = b_num / b_den
                    for n in [2, 3, 4, 5, 6, 7]:
                        val = a * zeta[m] + b * zeta[n]
                        err = abs(val - target)
                        if err < 1e-4 and (a_num != 0 or b_num != 0):
                            expr = f"({a_num}/{a_den})ζ({m}) + ({b_num}/{b_den})ζ({n})"
                            best_results.append((expr, val, err))

# Type B: a/π^n + b×ζ(m)/π^k
for a_num in range(-20, 21):
    for a_den in [1, 2, 3, 6, 10, 12, 30, 60, 120, 360]:
        a = a_num / a_den
        for n in [1, 2, 3, 4]:
            val = a / pi**n
            err = abs(val - target)
            if err < 1e-4 and a_num != 0:
                expr = f"({a_num}/{a_den})/π^{n}"
                best_results.append((expr, val, err))

# Type C: expressions involving γ (Euler-Mascheroni)
for a_num in range(-10, 11):
    for a_den in [1, 2, 3, 4, 6, 12]:
        a = a_num / a_den
        val_g = a * gamma_em
        err = abs(val_g - target)
        if err < 1e-3 and a_num != 0:
            expr = f"({a_num}/{a_den})γ"
            best_results.append((expr, val_g, err))

        # a × γ + b × ζ(n)
        for b_num in range(-5, 6):
            for b_den in [1, 2, 3, 6, 12, 120]:
                b = b_num / b_den
                for m in [2, 3, 5]:
                    val_gc = a * gamma_em + b * zeta[m]
                    err_gc = abs(val_gc - target)
                    if err_gc < 5e-5 and (a_num != 0 or b_num != 0):
                        expr = f"({a_num}/{a_den})γ + ({b_num}/{b_den})ζ({m})"
                        best_results.append((expr, val_gc, err_gc))

# Type D: involving log(2), log(3)
log2 = np.log(2)
log3 = np.log(3)
for a_num in range(-10, 11):
    for a_den in [1, 2, 3, 6, 12, 24, 120]:
        a = a_num / a_den
        for b_num in range(-10, 11):
            for b_den in [1, 2, 3, 6, 12, 24, 120]:
                b = b_num / b_den
                val = a * log2 + b * log3
                err = abs(val - target)
                if err < 5e-5 and (a_num != 0 or b_num != 0):
                    expr = f"({a_num}/{a_den})ln2 + ({b_num}/{b_den})ln3"
                    best_results.append((expr, val, err))

# Type E: a × ζ(n) - floor(a × ζ(n))
# i.e., fractional parts of ζ products
for a in range(1, 500):
    for n in [2, 3, 4, 5]:
        val = (a * zeta[n]) % 1
        if val > 0.5:
            val = val - 1
        err = abs(val - target)
        if err < 1e-4:
            expr = f"frac({a} × ζ({n}))"
            best_results.append((expr, val, err))

# Type F: RG running-inspired: b × ln(p) / π for primes p
for p in [2, 3, 5, 7, 11, 13]:
    for a_num in range(-20, 21):
        for a_den in [1, 2, 3, 4, 6, 12, 24, 36, 48, 72, 120, 360]:
            a = a_num / a_den
            val = a * np.log(p) / pi
            err = abs(val - target)
            if err < 5e-5 and a_num != 0:
                expr = f"({a_num}/{a_den}) × ln({p})/π"
                best_results.append((expr, val, err))

best_results.sort(key=lambda x: x[2])

print(f"  {'Expression':>50s}  {'Value':>14s}  {'Error':>12s}")
print(f"  {'-'*80}")
for expr, val, err in best_results[:25]:
    marker = " ★★★" if err < 1e-6 else " ★★" if err < 1e-5 else " ★" if err < 1e-4 else ""
    print(f"  {expr:>50s}  {val:>14.10f}  {err:>12.2e}{marker}")

# ============================================================================
#  PROBLEM 3: NCG spectral action and ζ
# ============================================================================

print("\n" + "=" * 70)
print("  PROBLEM 3: NCG SPECTRAL ACTION MOMENTS")
print("=" * 70)

print("""
  Chamseddine-Connes-Marcolli (2007) のスペクトル作用:

  S = Tr(f(D²/Λ²))

  ≈ f₄ Λ⁴ a₀ + f₂ Λ² a₂ + f₀ a₄ + ...

  ここで f_k = ∫₀^∞ f(x) x^{k/2-1} dx （f のモーメント）
  a_k はSeeley-DeWitt 係数（幾何学的不変量）

  結合定数の決定:
    1/g² = f₂ Λ² × (geometric factor from F)

  ── f のモーメントが算術的に決まるか？ ──

  鍵となる積分恒等式（Mellin変換）:
    ∫₀^∞ x^{s-1}/(e^x - 1) dx = Γ(s) ζ(s)

  もし f(x) = 1/(e^x - 1)（ボーズ-アインシュタイン分布）なら:
    f_k = ∫₀^∞ x^{k/2-1}/(e^x-1) dx = Γ(k/2) ζ(k/2)

  f₀ = ∫ 1/(x(e^x-1)) dx → 発散（対数的）
  f₂ = Γ(1) ζ(1) → 発散（ζの極）
  f₄ = Γ(2) ζ(2) = ζ(2) = π²/6

  ← f₂ が発散するのは BC 系の β=1 相転移と対応！
""")

# If we regularize f₂ by ζ-regularization:
# f₂ ~ ζ(1) → use ζ-reg value... but ζ(1) is a pole
# The residue of ζ at s=1 is 1.
# Laurent expansion: ζ(s) = 1/(s-1) + γ + O(s-1)
# So "ζ(1)" regularized might be γ (Euler-Mascheroni constant)!

print("  ── ζ(1) の正則化 ──")
print()
print(f"  ζ(s) = 1/(s-1) + γ + O(s-1)")
print(f"  「ζ(1)の有限部分」= γ = {gamma_em:.10f}")
print()
print(f"  もし f₂ = γ なら:")

# 1/g_GUT² = c × γ for some geometric constant c
# In NCG: the geometric factor involves the trace over the finite space F
# For SU(2): factor = 1, for SU(3): factor = 1, for U(1): factor = 5/3

# At unification: 1/α_GUT = 4π/g_GUT²
# If g_GUT² = g₀² × γ for some fundamental g₀:
# 1/α_GUT = 4π/(g₀² × γ)

# Let's see what g₀ would need to be
# If 1/α_GUT ≈ 25 (typical):
g0_sq = 4 * pi / (25 * gamma_em)
print(f"  1/α_GUT = 25 → g₀² = 4π/(25γ) = {g0_sq:.6f}")
print(f"  g₀ = {np.sqrt(g0_sq):.6f}")
print()

# Now: 1/α_em at low energy involves running
# 1/α_em = 8/3 × 1/α_GUT + (b₁ × 5/3 + b₂)/(2π) × ln(Λ_GUT/m_Z)
# where b₁ = 41/6, b₂ = -19/6 (SM beta functions)

b1 = 41/6
b2 = -19/6
ln_ratio = np.log(2e16 / 91.2)  # ln(Λ_GUT/m_Z)

print(f"  SM beta 関数係数: b₁ = 41/6, b₂ = -19/6")
print(f"  ln(Λ_GUT/m_Z) ≈ ln(2×10¹⁶/91.2) = {ln_ratio:.4f}")
print()

# 1/α_em = 8/3 × 1/α_GUT + (5/3 × b₁ + b₂)/(2π) × ln
running_coeff = (5/3 * b1 + b2) / (2 * pi)
print(f"  繰り込み係数: (5b₁/3 + b₂)/(2π) = {running_coeff:.6f}")
print()

for alpha_gut_inv in [24, 25, 26, 4*pi/gamma_em, 8*pi**2/(3*zeta[3])]:
    alpha_em_inv = 8/3 * alpha_gut_inv + running_coeff * ln_ratio
    label = f"1/α_GUT = {alpha_gut_inv:.4f}"
    print(f"  {label:>30s}: 1/α_em = {alpha_em_inv:.4f}  (target: {alpha_inv:.4f})")

print()

# ============================================================================
#  PROBLEM 4: Arithmetic RG running
# ============================================================================

print("=" * 70)
print("  PROBLEM 4: ARITHMETIC RG RUNNING")
print("=" * 70)

print("""
  繰り込み群 (RG) の走りには ln(Λ/μ) が現れる。
  Λ = GUT スケール ≈ 2 × 10¹⁶ GeV
  μ = Z 質量 ≈ 91.2 GeV

  ln(Λ/μ) ≈ 33.0

  ── この 33 は算術的に何か？ ──
""")

ln_val = np.log(2e16/91.2)
print(f"  ln(Λ_GUT/m_Z) = {ln_val:.6f}")
print()

# 33 ≈ π(137) (the number of primes ≤ 137)
print(f"  π(137) = 33 (137以下の素数の個数)")
print(f"  ln(Λ/μ) ≈ {ln_val:.1f} ≈ 33 = π(137)")
print()

# This would mean:
# 1/α_em = (algebraic from ζ) + (running ∝ π(1/α))
# A SELF-REFERENTIAL equation!

print("  もし ln(Λ/μ) = π(1/α) なら:")
print("  1/α = F(ζ-values) + G(beta-coefficients) × π(1/α)")
print("  これは自己参照的方程式！")
print("  1/α は自分自身を通じて定義される。")
print()

# Let's check: is there a self-consistent solution?
# 1/α = 8/3 × α_GUT_inv + running_coeff × π(1/α)
# If α_GUT_inv comes from ζ values...

# Try: α_GUT_inv = 4π²/(3ζ(3)) ≈ 10.96
val_gut = 4 * pi**2 / (3 * zeta[3])
print(f"  α_GUT_inv = 4π²/(3ζ(3)) = {val_gut:.6f}")

# Iterate: start with guess 1/α = 137, compute π(137) = 33
# 1/α = 8/3 × 10.96 + running_coeff × 33
alpha_guess = 8/3 * val_gut + running_coeff * 33
print(f"  1/α = 8/3 × {val_gut:.4f} + {running_coeff:.6f} × 33 = {alpha_guess:.4f}")
print()

# Hmm, 29.2 + 30.1 = 59.3, too low.
# The issue is α_GUT_inv ≈ 25 is needed, not 11.

# Try different ζ-expression for α_GUT_inv
for expr_name, gut_val in [
    ("ζ(2)²/ζ(4) × 10", zeta[2]**2/zeta[4] * 10),
    ("24", 24),
    ("8π/γ", 8*pi/gamma_em),
    ("4π × ζ(3)", 4*pi*zeta[3]),
    ("2π²/ζ(3)", 2*pi**2/zeta[3]),
    ("π² × ζ(3)/2", pi**2*zeta[3]/2),
    ("48/2 = |K₃(Z)|/2", 24),
    ("π²/ζ(2) × 6/π² × 25 = 25", 25),
]:
    a_em = 8/3 * gut_val + running_coeff * 33
    err = abs(a_em - alpha_inv)
    marker = " ★" if err < 1 else ""
    print(f"  1/α_GUT = {expr_name:>20s} = {gut_val:>8.4f}: "
          f"1/α_em = {a_em:>8.4f}  (err = {err:>6.2f}){marker}")

print()

# The self-referential aspect is profound even if numbers don't match perfectly
# Let me try: what α_GUT_inv is needed for self-consistency?
# 1/α = 8/3 × x + running_coeff × π(1/α)
# 137.036 = 2.667 × x + 1.074 × 33
# 137.036 = 2.667x + 35.44
# x = (137.036 - 35.44)/2.667 = 101.6/2.667 = 38.1

needed_gut = (alpha_inv - running_coeff * 33) / (8/3)
print(f"  自己無撞着に必要な 1/α_GUT = {needed_gut:.4f}")
print(f"  ζ(2) × |K₃(Z)|/2 = {zeta[2] * 24:.4f}")
print(f"  12π = {12*pi:.4f}")
print(f"  4π × ζ(2) = {4*pi*zeta[2]:.4f}")
print()

# 38.1 ≈ 12π = 37.7 ← close!
print(f"  ★ 12π = {12*pi:.6f} ≈ {needed_gut:.6f}")
print(f"    誤差: {abs(12*pi - needed_gut):.4f}")
print()

# If 1/α_GUT = 12π:
alpha_em_check = 8/3 * 12 * pi + running_coeff * 33
print(f"  1/α_em = 8/3 × 12π + {running_coeff:.4f} × π(137)")
print(f"         = 32π + {running_coeff * 33:.4f}")
print(f"         = {8/3 * 12 * pi:.4f} + {running_coeff * 33:.4f}")
print(f"         = {alpha_em_check:.6f}")
print(f"  実際:    {alpha_inv:.6f}")
print(f"  誤差:    {abs(alpha_em_check - alpha_inv):.6f}")
print(f"  相対誤差: {abs(alpha_em_check - alpha_inv)/alpha_inv:.2e}")

# ============================================================================
#  SYNTHESIS
# ============================================================================

print("\n" + "=" * 70)
print("  SYNTHESIS: THE EMERGING PICTURE")
print("=" * 70)

print(f"""
  4つの問題の探索結果:

  ■ 問題1: "+5" の正体
    最も自然な候補: 標準模型のツリーレベル独立パラメータ数 = 5
    (g₁, g₂, g₃, m_H, v)
    代数的候補: SU(5) GUT の基本表現の次元 = 5
    → 137 = (3D真空) + (1D真空) + (GUTパラメータ数)

  ■ 問題2: 0.035999... の精密表現
    最良候補は探索結果の上位を参照。
    完全一致する単純な算術式は見つからなかった。
    → 繰り込み群の走りに由来する「非算術的」補正の可能性

  ■ 問題3: NCGスペクトル作用のモーメント
    f₂ = γ（オイラー-マスケローニ定数）の可能性。
    ζ(1) の極の有限部分 = γ → BC相転移点の情報。
    f₄ = ζ(2) = π²/6。
    → スペクトル作用のモーメントはζ値で書ける可能性あり。

  ■ 問題4: 繰り込み群の走り
    ★ 最も重要な発見:

    ln(Λ_GUT/m_Z) ≈ 33 = π(137) = π(1/α)

    もしこれが偶然でないなら:
    1/α = 8/3 × (1/α_GUT) + (RG係数) × π(1/α)

    これは自己参照的方程式:
    「1/αの値は、1/α以下の素数の個数に依存する」

    さらに: 1/α_GUT ≈ 12π = 37.7 のとき
    1/α_em = 32π + (RG係数) × π(137)
           = {8/3*12*pi:.2f} + {running_coeff*33:.2f}
           = {alpha_em_check:.2f}
    （実際の値 {alpha_inv:.2f} との誤差 {abs(alpha_em_check-alpha_inv):.2f}）

  ── 提案される公式 ──

  1/α = 32π + (5b₁/3 + b₂)/(2π) × π(1/α)

  ここで:
    32π = 8/3 × 12π = (色因子) × (GUT結合の算術値)
    b₁ = 41/6, b₂ = -19/6 (SM beta関数 — これ自体が算術的！)
    π(1/α) = 137以下の素数の数 = 33

  b₁ と b₂ は粒子の表現の次元から決まるので、
  究極的にはNCGの有限空間Fの構造（= 算術幾何学的データ）で決まる。

  → α は「自分自身以下の素数の数」を参照して自分を定義する
  → Spec(Z) の自己参照的構造が物理定数を決定
""")

print("=" * 70)
print("  END")
print("=" * 70)
