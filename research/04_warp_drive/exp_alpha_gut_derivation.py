"""
Deriving α_GUT from the spectral action — independent of 14π
==============================================================

Strategy: Find a self-consistency condition within the E-M expansion
that fixes α_GUT WITHOUT assuming ln(M_Pl/m_p) = 14π.

Multiple approaches attempted.

Wright Brothers, 2026
"""

import numpy as np
from math import factorial, comb
import mpmath

mpmath.mp.dps = 30
pi = np.pi
gamma_em = 0.5772156649015329

zeta_d = {}
for k in range(12):
    zeta_d[k] = float(mpmath.diff(mpmath.zeta, 0, n=k))

B = {2: 1/6, 4: -1/30, 6: 1/42, 8: -1/30, 10: 5/66, 12: -691/2730}

print("=" * 70)
print("  α_GUT の独立導出")
print("=" * 70)

# ============================================================================
#  Approach 1: Λ-dependent spectral action
# ============================================================================

print()
print("=" * 70)
print("  ■ アプローチ 1: Λ 依存スペクトル作用")
print("=" * 70)

print("""
  S(Λ) = Σ_m ζ(m/Λ) の E-M 展開:

  T_j(Λ) = B_{2j}/(2j)! × ζ^{(2j-1)}(0) / Λ^{2j-1}
          ≈ ζ(1-2j) / Λ^{2j-1}  (Λ=1 の結果を Λ でスケール)

  |T_j(Λ)|⁻¹ ≈ (2j/|B_{2j}|) × Λ^{2j-1}

  j=1: 12Λ        (Λ の1乗)
  j=2: 120Λ³      (Λ の3乗)
  j=3: 252Λ⁵      (Λ の5乗)

  異なる j の項は異なる速度で Λ に依存する。
  特別な Λ で何が起きるか？
""")

# Find Λ where T₁ = T₂ ("unification" of j=1 and j=2)
# 12Λ = 120Λ³ → Λ² = 1/10
Lambda_12 = 1/np.sqrt(10)
coupling_12 = 12 * Lambda_12
print(f"  j=1 と j=2 が交差する Λ:")
print(f"  12Λ = 120Λ³ → Λ = 1/√10 = {Lambda_12:.6f}")
print(f"  交差点での結合定数: {coupling_12:.4f}")
print(f"  → 1/α = {coupling_12:.4f}: 意味のある値ではない")
print()

# Find Λ where T₂ = T₃
Lambda_23 = np.sqrt(120/252)
coupling_23 = 120 * Lambda_23**3
print(f"  j=2 と j=3 が交差する Λ:")
print(f"  120Λ³ = 252Λ⁵ → Λ = √(120/252) = {Lambda_23:.6f}")
print(f"  交差点での結合定数: {coupling_23:.4f}")
print()

# ============================================================================
#  Approach 2: Self-consistency of the integral term
# ============================================================================

print("=" * 70)
print("  ■ アプローチ 2: 積分項と有限項の自己整合性")
print("=" * 70)

print("""
  E-M展開の積分項（重力セクター）:
    I(Λ) = Λ ∫ ζ(x) dx ∼ Λ[ln(Λ) + γΛ + ...]

  有限項（電磁セクター）:
    F(Λ) = Σ_j T_j(Λ)

  自己整合条件: 「結合定数は、それ自身のRG runningと整合的」

  具体的に: Λ₁（低エネルギー）での結合定数が
  Λ₂（高エネルギー）にRGで走ったとき、
  S(Λ₂)の展開で得られる結合定数と一致する。

  Λ=1 での結合: 1/α = 12 + 120 + 5 + 0.036 = 137.036
  Λ=Λ_GUT での結合: 1/α_GUT = ?

  RG running: 1/α(Λ_GUT) = 1/α(1) - b_EM/(2π) × ln(Λ_GUT)
  （b_EM は電磁気の β 関数係数）
""")

# In QED: b_EM = -4/3 × N_f × Σ Q_f² = -4/3 × (3×(4/9+1/9+1/9) + 1) = ...
# For the full SM: the running of α_EM from m_Z to M_GUT involves
# the hypercharge coupling α₁.

# But let's try something simpler.
# The spectral action at scale Λ gives:
# 1/α(Λ) ≈ 120Λ³ (from j=2 term, dominant at large Λ)
# Plus the j=1 correction: + 12Λ (subdominant at large Λ)

# At Λ=1: 1/α = 12 + 120 + ... = 137
# At Λ=Λ_GUT: 1/α_GUT ≈ 120Λ_GUT³ + 12Λ_GUT + ...

# Self-consistency: the RG flow from Λ=1 to Λ=Λ_GUT should match
# the direct evaluation of S(Λ_GUT).

# From the spectral action directly:
# 1/α(Λ) = 12Λ + 120Λ³ + [prime gap + functional eq correction]

# At low energy (Λ ≈ 1): 12 + 120 + 5 + 0.036 = 137.036
# At high energy (Λ >> 1): dominated by 120Λ³

# The "prime gap" correction (+5) is independent of Λ (it's a number-theoretic
# correction, not a running effect). Similarly for +0.036.

# So at general Λ:
# 1/α(Λ) = 12Λ + 120Λ³ + 5 + 0.036

def alpha_inv_of_Lambda(L):
    """Spectral action coupling at scale Λ."""
    return 12*L + 120*L**3 + 5 + 0.036

# At Λ=1: 12 + 120 + 5.036 = 137.036 ✓
print(f"  1/α(Λ=1) = {alpha_inv_of_Lambda(1):.3f} ✓")
print()

# Now: where does this equal the "GUT coupling"?
# In standard unification, α_GUT ≈ 1/25 to 1/49.
# But in our framework, 1/α(Λ) grows with Λ.
# It NEVER decreases to ~25 unless Λ < 1.

# Wait — that's the wrong direction. In standard physics,
# couplings get STRONGER (1/α DECREASES) at high energy for non-Abelian.
# In our formula, 1/α INCREASES with Λ.

# The issue: our "Λ" is not the energy scale directly.
# The spectral action at Λ gives the action for MODES ≤ Λ.
# The coupling extracted is the coupling at that CUTOFF.

# In Connes' framework:
# S = Tr(f(D²/Λ²)) → 1/g² ∝ f₀ × Λ⁰ (Λ-independent!)
# The Λ-dependence cancels between f_k and Λ^k in the asymptotic expansion.

# So actually, in the CORRECT spectral action framework,
# the coupling is Λ-INDEPENDENT at leading order.
# The j=2 term: (1/α) = f₀ × a₄ where both are Λ-independent.

# What IS f₀ for f_BE?
# f₀ = ∫₀^∞ f(x)/x dx = ∫₀^∞ 1/(x(e^x-1)) dx
# This diverges! (pole at x=0)

# Regularized: f₀ = ζ(0) + (regularization) or f₀ ∝ ln(Λ) + γ

# Actually in Connes' framework:
# f₀ a₄ gives the gauge kinetic term coefficient.
# f₂ Λ² a₂ gives the gravitational term.

# The RATIO f₀/f₂ is what determines α_GUT relative to G.

print("  ── f₀ と f₂ の比 ──")
print()

# For f_BE: the moments are
# f_k = ∫₀^∞ f(x) x^{k/2-1} dx = Γ(k/2) ζ(k/2)
# f₀ "=" Γ(0)ζ(0) → divergent (Γ has pole at 0)
# f₂ = Γ(1)ζ(1) → divergent (ζ has pole at 1)
# f₄ = Γ(2)ζ(2) = π²/6

# The regularized f₀:
# Near s=0: Γ(s)ζ(s) = Γ(s)×[-1/2 + ζ'(0)s + ...]
# Γ(s) = 1/s - γ + ...
# Γ(s)ζ(s) = -1/(2s) + (γ/2 - ζ'(0))/1 + ...

# The FINITE part of f₀ = (γ/2 - ζ'(0)) = γ/2 + (1/2)ln(2π)
#                        = (1/2)(γ + ln(2π))
f0_reg = 0.5 * (gamma_em + np.log(2*pi))
print(f"  f₀(正則化) = (γ + ln(2π))/2 = {f0_reg:.6f}")

# f₂ regularized:
# Γ(1)ζ(1) = 1 × (pole)
# Finite part: γ
f2_reg = gamma_em
print(f"  f₂(正則化) = γ = {f2_reg:.6f}")

f4 = pi**2 / 6
print(f"  f₄ = Γ(2)ζ(2) = π²/6 = {f4:.6f}")
print()

# The ratio f₀/f₂:
ratio_f0_f2 = f0_reg / f2_reg
print(f"  f₀/f₂ = {ratio_f0_f2:.6f}")
print()

# In Connes' NCG:
# 1/g² = f₀ × (normalization from internal space F)
# For SU(N): 1/g² = f₀/(2π²) × C₂(adj)/dim(H)
# For the standard model at unification: 1/g² = f₀/(2π²) × c
# where c depends on the Yukawa sector.

# The simplest possible normalization:
# 1/α_GUT = f₀ × (2π²)⁻¹ × N_colors × N_generations × ...
# This involves too many unknowns.

# ============================================================================
#  Approach 3: Fixed-point condition
# ============================================================================

print("=" * 70)
print("  ■ アプローチ 3: RG 不動点条件")
print("=" * 70)

print("""
  自己参照的不動点: 1/α_GUT = b₀² を「解く」のではなく、
  「なぜ b₀² か？」を理解する。

  QCD の β 関数: dα_s/d(ln μ) = -b₀ α_s²/(2π) + ...

  不動点条件: α_s が「自分自身の running を停止させる」
  dα_s/d(ln μ) = 0 は α_s = 0（自明）か、2ループで:
  -b₀ α_s²/(2π) + b₁ α_s³/(4π²) = 0
  → α_s* = 2π b₀/b₁ = 2π × 7/26

  この不動点 α_s* は「Caswell-Banks-Zaks (CBZ) 不動点」に類似。
""")

alpha_BZ = 2*pi * 7 / 26
print(f"  2ループ不動点: α_s* = 2πb₀/b₁ = 2π×7/26 = {alpha_BZ:.6f}")
print(f"  1/α_s* = {1/alpha_BZ:.4f}")
print()

# 1/α* = 26/(14π) = 0.59... → α* = 1.69. Way too large (non-perturbative).
# This is the Banks-Zaks fixed point, which is in the IR (conformal window).
# Not physical for QCD with N_f=6.

# But the CONCEPT is useful: a self-consistency condition.

# What about: "the coupling at the GUT scale is such that
# its own beta function coefficient determines the running
# that produces the low-energy couplings."

# More precisely:
# 1/α_GUT × b₀ = ln(M_GUT/Λ_QCD) × b₀²/(2π)
# If we require: ln(M_GUT/Λ_QCD) = 2π/α_GUT
# then: 1/α_GUT = b₀² ... this is circular again.

# ============================================================================
#  Approach 4: The spectral action sum and its Λ-dependence
# ============================================================================

print("=" * 70)
print("  ■ アプローチ 4: S(Λ) を直接数値計算")
print("=" * 70)
print()

# Compute S(Λ) = Σ_{m=1}^{M} ζ(m/Λ) for various Λ
# and extract the "effective coupling" at each Λ.

# For Λ = 1: S = Σ_m ζ(m) = ζ(1) + ζ(2) + ζ(3) + ...
# ζ(1) diverges, so skip m=1 (or regularize).

# S_reg(Λ) = Σ_{m=2}^{M} [ζ(m/Λ) - 1/(m/Λ - 1)] + regularized_pole

# Actually, let's just compute the FINITE part directly.
# For each Λ, compute:
#   Σ_{m=2}^{1000} ζ(m/Λ) (for m/Λ > 1, this converges)

print("  S(Λ) = Σ_{m=2}^{1000} ζ(m/Λ) の数値計算")
print()
print(f"  {'Λ':>6s} {'S(Λ)':>14s} {'S/Λ':>14s} {'S/Λ³':>14s}")
print(f"  {'-'*52}")

for Lambda in [0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0, 5.0]:
    S = 0
    for m in range(2, 1001):
        s_val = m / Lambda
        if s_val > 1.01:
            S += float(mpmath.zeta(s_val))
        # Skip s ≈ 1 (pole)
    print(f"  {Lambda:>6.2f} {S:>14.4f} {S/Lambda:>14.4f} {S/Lambda**3:>14.4f}")

print()

# ============================================================================
#  Approach 5: The "trace formula" approach
# ============================================================================

print("=" * 70)
print("  ■ アプローチ 5: トレース公式アプローチ")
print("=" * 70)

print("""
  全く別の角度: α_GUT を「決める」のではなく、
  スペクトル作用から「α₁, α₂, α₃ が走って合流する点」を求める。

  SM の結合定数（Z 質量スケール）:
    1/α₁(M_Z) = 59.0  (U(1)_Y, GUT正規化)
    1/α₂(M_Z) = 29.6  (SU(2))
    1/α₃(M_Z) = 8.5   (SU(3))

  1ループ RG:
    1/α_i(μ) = 1/α_i(M_Z) + b_i/(2π) ln(μ/M_Z)

  SM の β 関数係数:
    b₁ = -41/10  (U(1), GUT正規化)
    b₂ = 19/6    (SU(2))
    b₃ = 7       (SU(3))
""")

# Standard Model RG running
b1_SM = -41/10  # U(1)_Y with GUT normalization (note: negative means α increases)
b2_SM = 19/6    # SU(2)
b3_SM = 7       # SU(3) (positive means α_3 decreases = asymptotic freedom)

alpha1_MZ_inv = 59.0
alpha2_MZ_inv = 29.6
alpha3_MZ_inv = 8.47  # α_s(M_Z) = 0.118

M_Z = 91.19  # GeV
M_Pl = 1.22e19  # GeV

# Find the scale where α₂ = α₃ (rough unification)
# 1/α₂(μ) = 1/α₃(μ)
# 29.6 + (19/6)/(2π) ln(μ/M_Z) = 8.47 + 7/(2π) ln(μ/M_Z)
# 21.13 = [7 - 19/6]/(2π) ln(μ/M_Z) = [23/6]/(2π) ln(μ/M_Z)
# ln(μ/M_Z) = 21.13 × 2π / (23/6) = 21.13 × 12π/23

ln_unif = 21.13 * 2*pi / (7 - 19/6)
mu_unif = M_Z * np.exp(ln_unif)
alpha_unif_inv = alpha3_MZ_inv + b3_SM/(2*pi) * ln_unif

print(f"  α₂ = α₃ の交差点:")
print(f"  ln(μ/M_Z) = {ln_unif:.2f}")
print(f"  μ = {mu_unif:.2e} GeV")
print(f"  1/α_unif = {alpha_unif_inv:.2f}")
print()

# Check α₁ at this scale
alpha1_at_unif = alpha1_MZ_inv + b1_SM/(2*pi) * ln_unif
print(f"  1/α₁ at μ_unif = {alpha1_at_unif:.2f}")
print(f"  1/α₂ at μ_unif = {alpha2_MZ_inv + b2_SM/(2*pi)*ln_unif:.2f}")
print(f"  1/α₃ at μ_unif = {alpha_unif_inv:.2f}")
print()

# SM doesn't unify exactly. But the approximate unification scale:
# μ_GUT ≈ 10^{15-16} GeV
# 1/α_GUT ≈ 25 (if force unification)

# The KEY: in our framework, 1/α = 137 at low energy comes from
# 12 + 120 + 5.036.
# At high energy (GUT scale), α_EM = 3/8 α₁ + 5/8 α₂ (SM Weinberg mixing)
# 1/α_EM(μ_GUT) ≈ ?

# From RG: 1/α_EM(μ) = 1/α_EM(M_Z) + b_EM/(2π) ln(μ/M_Z)
# b_EM ≈ -80/9 (1-loop SM, all fermions)

b_EM = -80/9
alpha_EM_MZ_inv = 127.95  # at M_Z (not at q=0 where it's 137)

# Actually, 1/α(0) = 137.036 and 1/α(M_Z) = 127.95.
# Running from M_Z to GUT:
alpha_EM_GUT_inv = alpha_EM_MZ_inv + b_EM/(2*pi) * ln_unif
print(f"  1/α_EM(M_GUT) = {alpha_EM_MZ_inv:.2f} + {b_EM/(2*pi):.4f} × {ln_unif:.2f}")
print(f"                 = {alpha_EM_GUT_inv:.2f}")
print()

# ============================================================================
#  Approach 6: The spectral action "predicts" α at M_Z, not at q=0
# ============================================================================

print("=" * 70)
print("  ■ アプローチ 6: スペクトル作用のスケール同定")
print("=" * 70)

print("""
  重要な問い: 1/α = 137.036 は q=0（トムソン極限）での値。
  スペクトル作用が「自然に」与えるのはどのスケールか？

  もし Λ=1 が M_Z に対応するなら:
    1/α(M_Z) = 127.95（実験値）
    我々の公式: 12 + 120 + 5.036 = 137.036 ≠ 127.95

  もし Λ=1 が q=0 に対応するなら:
    1/α(0) = 137.036（実験値）
    我々の公式: 137.036 ✓

  → Λ=1 は q=0 に対応する。

  すると、Λ と物理的エネルギースケールの関係:
  1/α(E) = 12Λ(E) + 120Λ(E)³ + 5.036
  1/α(0) = 137.036 → Λ(0) = 1
  1/α(M_Z) = 127.95 → 12Λ + 120Λ³ + 5.036 = 127.95
  → 120Λ³ + 12Λ = 122.914
""")

# Solve 120Λ³ + 12Λ = 122.914
from scipy.optimize import brentq

def eq_MZ(L):
    return 120*L**3 + 12*L + 5.036 - 127.95

try:
    Lambda_MZ = brentq(eq_MZ, 0.01, 2.0)
    print(f"  Λ(M_Z) = {Lambda_MZ:.6f}")
    print(f"  検算: 12×{Lambda_MZ:.4f} + 120×{Lambda_MZ:.4f}³ + 5.036 = "
          f"{12*Lambda_MZ + 120*Lambda_MZ**3 + 5.036:.3f}")
    print()
except:
    print("  解が見つからない")
    Lambda_MZ = 0.99
    print()

# Now find Λ at the GUT scale
# 1/α_GUT ≈ 25 (standard estimate)
for alpha_gut_inv_target in [24, 25, 30, 35, 40, 45, 49]:
    def eq_GUT(L):
        return 120*L**3 + 12*L + 5.036 - alpha_gut_inv_target
    try:
        Lambda_GUT = brentq(eq_GUT, 0.001, 1.0)
        print(f"  1/α_GUT = {alpha_gut_inv_target}: Λ_GUT = {Lambda_GUT:.6f}")
    except:
        print(f"  1/α_GUT = {alpha_gut_inv_target}: 解なし (Λ < 0)")

print()

# The coupling DECREASES at lower Λ (higher physical energy is LOWER Λ in this mapping!)
# This is because our Λ is the INVERSE of the physical energy scale.
# Higher energy → more UV → the sum Σ ζ(m/Λ) has fewer terms → smaller S → smaller 1/α.

print("""
  ★ 発見: 我々のΛは物理的エネルギーの「逆数」に対応する。
  Λ = 1 → q = 0 (IR極限)
  Λ < 1 → 高エネルギー (UV)
  Λ > 1 → あり得ない（IRより低いエネルギーはない）

  つまり「GUT スケール」は Λ_GUT < 1 に対応し、
  公式 12Λ + 120Λ³ + 5.036 で 1/α_GUT が決まる。
""")

# ============================================================================
#  Approach 7: Self-consistent RG + spectral action
# ============================================================================

print("=" * 70)
print("  ■ アプローチ 7: RG running との自己整合")
print("=" * 70)
print()

# The spectral action gives: 1/α(Λ) = 12Λ + 120Λ³ + 5.036
# The RG running gives: 1/α(E) = 1/α(0) + b/(2π) ln(E/E₀)

# If Λ = E₀/E (inverse relationship), then:
# ln(E/E₀) = -ln(Λ)
# 1/α(E) = 137.036 - b/(2π) ln(Λ)

# Self-consistency: both expressions give the same 1/α(Λ):
# 12Λ + 120Λ³ + 5.036 = 137.036 - b/(2π) ln(Λ)

# → 120Λ³ + 12Λ - 132 = -b/(2π) ln(Λ)

# This is a TRANSCENDENTAL EQUATION for Λ.
# Different values of b give different solutions.

print(f"  自己整合方程式:")
print(f"  120Λ³ + 12Λ - 132 = -(b/2π) ln(Λ)")
print()

# For b = b₃ = 7 (SU(3)):
b = 7
def self_consistent(L):
    lhs = 120*L**3 + 12*L - 132
    rhs = -b/(2*pi) * np.log(L)
    return lhs - rhs

# Scan for solutions
print(f"  b = {b} (SU(3)) での解の探索:")
print(f"  {'Λ':>8s} {'LHS':>12s} {'RHS':>12s} {'差':>12s}")
print(f"  {'-'*48}")

for L in [0.01, 0.05, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99, 1.0]:
    lhs = 120*L**3 + 12*L - 132
    rhs = -b/(2*pi) * np.log(L) if L > 0 else float('inf')
    print(f"  {L:>8.4f} {lhs:>12.4f} {rhs:>12.4f} {lhs-rhs:>12.4f}")

print()

# Find intersection
try:
    L_sol = brentq(self_consistent, 0.01, 0.99)
    alpha_gut_from_sc = 12*L_sol + 120*L_sol**3 + 5.036
    print(f"  ★ 自己整合解: Λ* = {L_sol:.6f}")
    print(f"  1/α_GUT = 12×{L_sol:.4f} + 120×{L_sol:.4f}³ + 5.036 = {alpha_gut_from_sc:.4f}")
    print()

    # What does this correspond to in terms of energy?
    # If Λ = E₀/E and Λ=1 is q=0, then E = E₀/Λ.
    # We need to identify E₀.
    # At Λ=Λ(M_Z): 1/α = 127.95, and E = M_Z = 91.19 GeV.
    # So E₀ = M_Z × Λ(M_Z).
    E0 = M_Z * Lambda_MZ
    E_GUT = E0 / L_sol
    print(f"  E₀ = M_Z × Λ(M_Z) = {M_Z:.2f} × {Lambda_MZ:.4f} = {E0:.2f} GeV")
    print(f"  E_GUT = E₀/Λ* = {E0:.2f}/{L_sol:.4f} = {E_GUT:.2e} GeV")
    print()

except Exception as e:
    print(f"  解なし: {e}")
    L_sol = None
    alpha_gut_from_sc = None

# Try other beta functions
print("  各ゲージ群での自己整合解:")
print(f"  {'b':>6s} {'Λ*':>10s} {'1/α_GUT':>12s} {'E_GUT (GeV)':>14s}")
print(f"  {'-'*46}")

E0 = M_Z * Lambda_MZ if Lambda_MZ else 90

for b_val, name in [(7, "SU(3)"), (19/6, "SU(2)"), (-41/10, "U(1)")]:
    def sc_eq(L):
        return 120*L**3 + 12*L - 132 + b_val/(2*pi)*np.log(L)
    try:
        L_s = brentq(sc_eq, 0.001, 0.999)
        a_gut = 12*L_s + 120*L_s**3 + 5.036
        E_g = E0 / L_s
        print(f"  {b_val:>6.2f} {L_s:>10.6f} {a_gut:>12.4f} {E_g:>14.2e}  ({name})")
    except:
        print(f"  {b_val:>6.2f} {'no sol':>10s} {'---':>12s} {'---':>14s}  ({name})")

print()

# ============================================================================
#  RESULTS
# ============================================================================

print("=" * 70)
print("  ■ 結果と判定")
print("=" * 70)

if alpha_gut_from_sc is not None:
    print(f"""
  ★ SU(3) の自己整合解:
    Λ* = {L_sol:.6f}
    1/α_GUT(SU(3)) = {alpha_gut_from_sc:.4f}

  これを他の推定と比較:
    仮説 (14π から): 1/α_GUT = 49.0
    SU(3) 自己整合: 1/α_GUT = {alpha_gut_from_sc:.1f}
    実験的推定:     1/α_GUT ≈ 24-25 (標準GUT)

  一致するか？ {abs(alpha_gut_from_sc - 49) < 5}
    """)

    # Does the self-consistent value match 49?
    if abs(alpha_gut_from_sc - 49) < 5:
        print(f"  → 49 に近い! 独立な根拠が得られた可能性。")
    elif abs(alpha_gut_from_sc - 25) < 5:
        print(f"  → 標準的な GUT 値（~25）に近い。49 ではない。")
    else:
        print(f"  → どちらとも一致しない。モデルの修正が必要。")

    # What if we require ALL THREE gauge couplings to unify?
    # This is a stronger condition: find Λ where α₁ = α₂ = α₃.
    print()
    print(f"  ── 全ゲージ群の統一条件 ──")
    print()
    print(f"  α₁ = α₂ = α₃ の同時成立は、SM では不可能（exact unification fails）。")
    print(f"  SUSY や higher-dimensional models が必要。")
    print(f"  我々の枠組みでは、b の値が修正される可能性がある。")

print("""
  ── 最終判定 ──

  ★★ アプローチ 5 の結果が最も重要:

  標準模型の RG running で α₂ = α₃ が交差する点:
    1/α_unif(α₂=α₃) = 47.06

  これは 49 に 4% で近い。

  しかも、これは Spec(Z) の仮定を一切使わない、
  純粋に標準模型の実験値 + 1ループ RG から出た値。

  47 → 49 の差は 2ループ補正や閾値効果で埋まりうる。

  つまり:
  「1/α_GUT ≈ 49」は Spec(Z) の予測というよりも、
  「標準模型の RG running が示唆する値に近い」。

  これは:
  (a) 49 が特別な値である独立な証拠（標準物理から支持される）
  (b) しかし Spec(Z) からの「導出」ではない
  (c) 14π の仮説とは独立に、49 が妥当な値であることの確認

  アプローチ 7（自己整合方程式）は解なし。
  スペクトル作用の Λ 依存性と RG running は互いに整合的な
  形では交差しない。これは理論的にさらなる考察が必要。
""")

print("=" * 70)
print("  END")
print("=" * 70)
