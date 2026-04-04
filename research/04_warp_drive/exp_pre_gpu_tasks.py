"""
Pre-GPU Tasks: Three questions to answer before investing in hardware
=====================================================================

Task 1: Is 14π = ln(M_Pl/m_p) or ln(M_Pl/Λ_QCD)?
Task 2: Can α_GUT = 1/49 be derived from the spectral action?
Task 3: Does m_p/Λ_QCD ≈ 4.3 have arithmetic structure?

Wright Brothers, 2026
"""

import numpy as np
from math import factorial, comb
import mpmath

mpmath.mp.dps = 30
pi = np.pi
gamma_em = 0.5772156649015329

# Physical constants in GeV
m_p = 0.93827  # proton mass
m_n = 0.93957  # neutron mass
m_e = 0.000511  # electron mass
M_Pl = 1.22089e19  # Planck mass (standard)
Lambda_QCD = 0.217  # MS-bar, N_f=5
f_pi = 0.0922  # pion decay constant
m_pi = 0.135  # pion mass

print("=" * 70)
print("  TASK 1: 14π は何に等しいのか？")
print("=" * 70)
print()

# The formula ln(M/Λ) = 2π/(b��� α) comes from 1-loop RG running.
# But WHICH M and WHICH Λ?

# In QCD, the running coupling α_s(μ) satisfies:
# 1/α_s(μ) = 1/α_s(M) + b₀/(2π) ln(M/μ)
# At μ = Λ_QCD: α_s(Λ_QCD) → ∞ (confinement)
# So: 1/α_s(M) = b₀/(2π) ln(M/��_QCD)

# If we set M = M_Pl and α_s(M_Pl) = α_GUT:
# 1/α_GUT = b₀/(2π) ln(M_Pl/Λ_QCD)
# → ln(M_Pl/Λ_QCD) = 2π/(b₀ α_GUT)

# With α_GUT = 1/49: ln(M_Pl/Λ_QCD) = 2π×49/7 = 14π = 43.98

# But ln(M_Pl/Λ_QCD) = ln(M_Pl/m_p) + ln(m_p/Λ_QCD)
#                      = 44.01 + 1.46 = 45.47

# So 14π = 43.98 ≠ 45.47 = ln(M_Pl/Λ_QCD)

# HOWEVER: there's a subtlety. Which Λ_QCD?
# Λ_QCD depends on the renormalization scheme AND the number of active flavors.

# Different values of Λ_QCD:
print("  ── Λ_QCD の定義依存性 ──")
print()

# Λ_QCD^{(N_f)} for different N_f:
# The matching conditions at quark thresholds change Λ.
# At the GUT scale, all 6 quarks are active: N_f = 6
# b₀(N_f=6) = 11 - 2×6/3 = 7
# b₀(N_f=5) = 11 - 2×5/3 = 23/3 ≈ 7.67
# b₀(N_f=4) = 25/3 ≈ 8.33
# b₀(N_f=3) = 9

# The "standard" Λ_QCD ≈ 217 MeV is for N_f=5 (MS-bar).
# For N_f=6 (which is what b₀=7 corresponds to), Λ_QCD is DIFFERENT.

# Matching at m_t = 173 GeV:
# Λ^{(6)} is obtained from Λ^{(5)} by threshold matching.
# Approximately: Λ^{(6)} ≈ Λ^{(5)} × (m_t/Λ^{(5)})^{2/21}
# This gives a LARGER Λ^{(6)}.

m_t = 173.0  # top quark mass in GeV
Lambda_5 = 0.217  # GeV

# Threshold matching (1-loop):
# ln(Λ^{(6)}/Λ^{(5)}) = (b₀^{(5)} - b₀^{(6)})/(2 b₀^{(5)} b₀^{(6)}) × 2π × [something]
# Simpler: at μ = m_t, α_s^{(5)}(m_t) = α_s^{(6)}(m_t)
# 1/α_s(m_t) = b₀^{(5)}/(2π) × ln(m_t/Λ^{(5)})
# = (23/3)/(2π) × ln(173/0.217) = 1.222 × 6.684 = 8.17
# → α_s(m_t) = 0.122 ✓ (matches experiment!)

alpha_s_mt = 1 / ((23/3)/(2*pi) * np.log(m_t/Lambda_5))
print(f"  ��_s(m_t) from Λ^(5) = 217 MeV: {alpha_s_mt:.4f}")
print(f"  実験値: 0.1079 (at M_Z), running to m_t ≈ 0.108")
print()

# Now: 1/α_s(m_t) = b₀^{(6)}/(2π) × ln(m_t/Λ^{(6)})
# → ln(m_t/Λ^{(6)}) = 2π/(7 × α_s(m_t)) = 2π × 8.17/7... wait
# → ln(m_t/Λ^{(6)}) = 2π/(b₀^{(6)} × α_s(m_t)) = 2π/(7 × 0.122) = 7.35
# → Λ^{(6)} = m_t × exp(-7.35) = 173 × 6.4e-4 = 0.111 GeV = 111 MeV

b0_6 = 7
Lambda_6 = m_t * np.exp(-2*pi/(b0_6 * alpha_s_mt))
print(f"  Λ^(6)_QCD = m_t × exp(-2π/(7 α_s(m_t)))")
print(f"           = {m_t} × exp(-{2*pi/(7*alpha_s_mt):.3f})")
print(f"           = {Lambda_6:.4f} GeV = {Lambda_6*1000:.1f} MeV")
print()

# Now check: ln(M_Pl/Λ^{(6)})
ln_MPl_L6 = np.log(M_Pl / Lambda_6)
print(f"  ln(M_Pl/Λ^(6)) = {ln_MPl_L6:.4f}")
print(f"  14π = {14*pi:.4f}")
print(f"  差 = {ln_MPl_L6 - 14*pi:.4f}")
print()

# Hmm, still doesn't match 14π.
# Let's try the other direction: what Λ gives exactly 14π?

Lambda_14pi = M_Pl * np.exp(-14*pi)
print(f"  14π に対応する Λ:")
print(f"  Λ_{{14π}} = M_Pl × exp(-14π) = {Lambda_14pi:.4f} GeV = {Lambda_14pi*1000:.1f} MeV")
print()

# Λ_{14π} ≈ 0.967 GeV ≈ m_p !!!
print(f"  ★ Λ_{{14π}} = {Lambda_14pi*1000:.1f} MeV ≈ m_p = {m_p*1000:.1f} MeV")
print(f"  Λ_{{14π}}/m_p = {Lambda_14pi/m_p:.6f}")
print()

# So 14π gives EXACTLY the proton mass scale, not Λ_QCD!
# This means the formula is NOT the standard QCD formula.
# It's something else: M_Pl × exp(-14π) = m_p (directly).

print("  ┌──────────────────────────────────────────────────────┐")
print("  │                                                      │")
print("  │  Task 1 結論:                                        │")
print("  │                                                      │")
print("  │  14π は Λ_QCD ではなく m_p を直接与える。            │")
print("  │                                                      │")
print("  │  M_Pl × exp(-14π) = 0.967 GeV ≈ m_p = 0.938 GeV    │")
print("  │  精度: 3.1%                                          │")
print("  │                                                      │")
print("  │  これは標準的な QCD 次元変換とは「別の公式」。       │")
print("  │  QCD は Λ_QCD ≈ 0.1-0.2 GeV を予測するが、          │")
print("  │  14π は m_p ≈ 0.94 GeV を直接予測する。              │")
print("  │                                                      │")
print("  │  解釈:                                                │")
print("  │  (A) 偶然の一致（m_p/M_Pl がたまたま exp(-14π)に近い)│")
print("  │  (B) 陽子質量は QCD を経由せず算術的に固定される     │")
print("  │  (C) 14π の背後に QCD + 非摂動効果の組み合わせがある │")
print("  │                                                      │")
print("  └──────────────────────────────────────────────────────┘")
print()

# ============================================================================
print("=" * 70)
print("  TASK 2: α_GUT = 1/49 はスペクトル作用から出るか？")
print("=" * 70)
print()

# In Connes' spectral action:
# 1/g² = f₀/(2π²) × ∫ Tr(F²) × (Seeley-DeWitt factor)
# At unification, all 1/g_i² are equal.
# f₀ = moment of f_BE = related to ζ(0) = -1/2

# In our E-M framework:
# The "coupling at scale Λ" involves the integral term:
# ∫₁^Λ ζ(x) dx = ln(Λ-1) + γΛ + finite

# If we identify α_GUT with the spectral action evaluated at the GUT scale...

# Let's try a direct approach: what does the spectral action give
# when we evaluate it at a specific scale?

# S(Λ) = Σ_m ζ(m/Λ)
# For Λ >> 1: most terms have m/Λ near 0, where ζ has a pole.
# The "coupling" at scale Λ is extracted from the finite part.

# Actually, let me think about this differently.
# The E-M expansion of S = Σ_m ζ(m) gives:
# T₁ = ζ(-1) + ε₁ (j=1 term)
# T₂ = ζ(-3) + ε₂ (j=2 term)
# ...

# These give 1/α = 12 + 120 + ... at LOW energy.
# At GUT energy, all couplings unify. The GUT coupling comes from
# the INTEGRAL of the spectral action, not the finite terms.

# Key insight from Connes' NCG:
# The gauge coupling at unification is:
# 1/g_GUT² = f₀ × a₄ × (normalization)
# where a₄ is the fourth Seeley-DeWitt coefficient.

# In our framework: f₀ relates to ζ(0), and a₄ relates to ζ(-3).
# So: 1/α_GUT ∝ |ζ(0)| × |ζ(-3)|⁻¹ = (1/2) × 120 = 60

ratio_1 = abs(-0.5) * 120
print(f"  候補 1: |ζ(0)| × |ζ(-3)|⁻¹ = (1/2) × 120 = {ratio_1}")
print(f"    → 60 ≠ 49. ✗")
print()

# Try: γ × something?
# γ × |ζ(-3)|⁻¹ = 0.577 × 120 = 69.3
ratio_2 = gamma_em * 120
print(f"  候補 2: γ × |ζ(-3)|⁻¹ = {gamma_em:.4f} × 120 = {ratio_2:.1f}")
print(f"    → 69.3 ≠ 49. ✗")
print()

# Try: 2/|B₂| × 4/|B₄| / (2/|B₂| + 4/|B₄|) = 12×120/132 = harmonic
harmonic = 12 * 120 / (12 + 120)
print(f"  候補 3: 調和平均 12×120/(12+120) = {harmonic:.4f}")
print(f"    → 10.9 ≠ 49. ✗")
print()

# Try: (12+120)/α_corrections = 132/(132-128.964)
# Hmm, this is getting circular.

# Let's try the K-theory route.
# K₁(Z) = Z/2, K₂(Z) = Z/2, K₃(Z) = Z/48
# K₄(Z) = 0, K₅(Z) = Z, K₆(Z) = 0, K₇(Z) = Z/240, K₈(Z) = 0
# K₉(Z) = Z⊕Z/2, ...

# |K₃(Z)| = 48. Our claim: 1/α_GUT = 48 + 1 = 49.
# But WHY +1?

# In Bott periodicity, K-groups repeat with period 8.
# K_{n+8}(Z) ≈ K_n(Z) × (corrections).
# The "+1" could be the "unit" of the ring Z.

# More concretely: K₃(Z) = Z/48 describes the stable homotopy
# of spheres: π₃^s = Z/24 × Z/2... actually no.
# K₃(Z) = Z/48 = Z/16 × Z/3 (this is the correct structure).

# The electron g-2 at 1-loop: α/(2π) ≈ 0.00116.
# Our "48" is Δa_e × 10¹¹ ≈ 48 × 10⁻¹¹.

# Let's try: does the spectral action "see" K₃ directly?

# The index theorem: ind(D) = ∫ Â(M)
# For D_BC on Spec(Z), the relevant index is related to K-theory of Z.
# The algebraic K-theory K₃(Z) = Z/48 is related to ζ(-1) and ζ(-3)
# through the Lichtenbaum conjecture:
# |K_{2n-2}(Z)| × regulator = |ζ(1-n)| × (power of 2)

print(f"  ── K群とゼータ値の関係（リヒテンバウム予想） ──")
print()
print(f"  K₀(Z) = Z       → 単位（「1」の起源）")
print(f"  K₁(Z) = Z/2     → 符号反転（「-1」の起源）")
print(f"  K₂(Z) = Z/2     → 位相的保護")
print(f"  K₃(Z) = Z/48    → |K₃| = 48")
print(f"  K₅(Z) = Z       → 実数の寄与")
print(f"  K₇(Z) = Z/240   → |K₇| = 240 = 8/|B₈|")
print()

# K₇(Z) = Z/240 and 240 = 8/|B₈| = 2j/|B_{2j}| for j=4!
# K₃(Z) = Z/48 and 48 = ???
# 48 = 4!/0.5 = 24/0.5... not obviously a Bernoulli thing.
# But: 48 = 2 × 24 = 2 × 4!
# Or: 48 = 16 × 3

# Actually: |K_{4n-1}(Z)| is related to Bernoulli numbers:
# |K₃(Z)| = 48 (from ζ(-1) = -1/12 and K-theory)
# |K₇(Z)| = 240 (from ζ(-3) = 1/120 and K-theory)
# |K₁₁(Z)| relates to ζ(-5) = -1/252

# The pattern:
# |K₃| = 48 = 4 × 12 = 4 × 2/|B₂|
# |K₇| = 240 = 2 × 120 = 2 × 4/|B₄|
# Check: |K₁₁| should relate to 252?

# Quillen-Lichtenbaum: for odd n ≥ 3,
# |K_{2n-2}(Z)| / |K_{2n-1}(Z)| = |B_n/n| × (power of 2)

# K₃: |B₂/2| × denominator_correction = (1/12) × something = 48?
# (1/12)⁻¹ = 12, 48/12 = 4. So 48 = 4 × |ζ(-1)|⁻¹.
# K₇: |B₄/4| × ... = (1/120) × something = 240?
# (1/120)⁻¹ = 120, 240/120 = 2. So 240 = 2 × |ζ(-3)|⁻¹.

print(f"  ── K群とゼータの定量的関係 ──")
print()
print(f"  |K₃(Z)| = 48 = 4 × |ζ(-1)|⁻¹ = 4 × 12")
print(f"  |K₇(Z)| = 240 = 2 × |ζ(-3)|⁻¹ = 2 × 120")
print()
print(f"  パターン: |K_{{4n-1}}(Z)| = c_n × |ζ(1-2n)|⁻¹")
print(f"    n=1: c₁ = 48/12 = 4")
print(f"    n=2: c₂ = 240/120 = 2")
print()

# So 1/α_GUT = |K₃(Z)| + 1 = 48 + 1 = 49 means:
# 1/α_GUT = 4×|ζ(-1)|⁻¹ + 1 = 4×12 + 1 = 49

# Can we motivate "4×12 + 1" from the spectral action?
# The "4" could be d=4 (spacetime dimension).
# The "+1" could be the j=0 term (a₀ = 1, the "volume" term).

print(f"  ── 1/α_GUT = d × |ζ(-1)|⁻¹ + 1 = 4×12 + 1 = 49 ──")
print()
print(f"  d = 4: 時空次元")
print(f"  |ζ(-1)|⁻¹ = 12: j=1 の結合定数")
print(f"  +1: スペクトル作用の a₀ 項（体積=1の正規化）")
print()

# Check if this formula works for other K-groups:
# |K₇| + 1 = 241? Is this meaningful?
# |K₇| = 240 = 2 × 120. If we apply the same pattern:
# d × |ζ(-3)|⁻¹ + 1 = 4 × 120 + 1 = 481? No, |K₇| = 240.
# Pattern doesn't generalize trivially. The "49 = 48+1" might be specific to GUT.

print("  ┌──────────────────────────────────────────────────────┐")
print("  │                                                      │")
print("  │  Task 2 結論:                                        │")
print("  │                                                      │")
print("  │  1/α_GUT = 49 をスペクトル作用から「導出」することは │")
print("  │  まだできていない。                                  │")
print("  │                                                      │")
print("  │  しかし算術的な文脈は明確になった:                   │")
print("  │  49 = |K₃(Z)| + 1 = 4 �� |ζ(-1)|⁻¹ + 1              │")
print("  │     = d × (j=1結合定数) + (体積の正規化)             │")
print("  │                                                      │")
print("  │  「導出」ではなく「分解」の段階。                    │")
print("  │  導出には d=4 の起源と +1 の正当化が必要。           │")
print("  │                                                      │")
print("  └���─────────────────────────────────────────────────────┘")
print()

# ============================================================================
print("=" * 70)
print("  TASK 3: m_p/Λ_QCD ≈ 4.3 に算術的構造はあるか？")
print("=" * 70)
print()

ratio = m_p / Lambda_QCD
print(f"  m_p/Λ_QCD = {m_p}/{Lambda_QCD} = {ratio:.4f}")
print()

# Is 4.3 close to anything arithmetic?
print(f"  候補:")
print(f"    e^{np.log(ratio):.4f} = {ratio:.4f}")
print(f"    4 + 1/π = {4 + 1/pi:.4f}")
print(f"    (2π)^{1/2} = {np.sqrt(2*pi):.4f}")
print(f"    e^γ × π = {np.exp(gamma_em)*pi:.4f}")
print(f"    Γ(1/4)/√π = ... (complex)")
print()

# Actually, Λ_QCD itself is scheme-dependent.
# Let's check: if 14π = ln(M_Pl/m_p) EXACTLY, what does that imply
# for the "effective Λ" in the formula?
# ln(M_Pl/m_p) = 2π/(b₀ α_eff)
# With 14π: α_eff = 2π/(7 × 14π) = 1/49.
# So α_eff = 1/49 is just the DEFINITION of what makes 14π work.
# It's circular unless we can derive α_eff = 1/49 independently.

print(f"  ── 循環論法の検出 ──")
print()
print(f"  14π = ln(M_Pl/m_p) を仮定")
print(f"  → α_GUT = 1/49 が「必要」（定義から）")
print(f"  → 49 = |K₃(Z)| + 1 と「一致」")
print(f"  → しかしこれは 14π の一致を前提としている")
print()
print(f"  独立な根拠なしには、これは:")
print(f"  「14π ≈ 44.0 が偶然合って、49 ≈ 49.0 は当然合う」")
print(f"  という循環。")
print()

# Is there a NON-circular way to get 49?
# Non-perturbative lattice QCD gives m_p/��_QCD ≈ 4.3.
# If we could predict 4.3 from number theory, that would break the circle.

# m_p ≈ 3 × m_quark + binding energy
# m_quark (up, down) ≈ 2-5 MeV (current mass)
# So m_p is almost entirely binding energy (~99%)!
# m_p ≈ 938 MeV, of which ~930 MeV is QCD binding energy.

# The lattice QCD result: m_p/Λ_MS = 4.1 ± 0.2 (various groups)
# This is a NUMBER that comes out of the strong interactions.

# Is 4.3 ≈ exp(3/2) = 4.48? Or 4.3 ≈ 3 + π/e = 3 + 1.156 = 4.156?

# Let's check: m_p/Λ^(6)_QCD (with N_f=6 Λ, which is the one for b₀=7)
ratio_6 = m_p / Lambda_6
print(f"  m_p/Λ^(6)_QCD = {m_p}/{Lambda_6:.4f} = {ratio_6:.4f}")
print(f"    ln(m_p/Λ^(6)) = {np.log(ratio_6):.4f}")
print()

# m_p/Λ^{(6)} ≈ 8.4. Hmm, 8.4 ≈ 8π/3 = 8.38?
print(f"    8π/3 = {8*pi/3:.4f} (比: {ratio_6/(8*pi/3):.4f})")
print(f"    2e = {2*np.e:.4f} (比: {ratio_6/(2*np.e):.4f})")
print()

# None of these are compelling.

print("  ┌──────────────────────────────────────────────────────┐")
print("  │                                                      │")
print("  │  Task 3 結論:                                        │")
print("  │                                                      │")
print("  │  m_p/Λ_QCD ≈ 4.3 に明確な算術的構造は見つからない。│")
print("  │  この比は非摂動的QCDの結果であり、                  │")
print("  │  格子QCDでしか計算できない。                        │")
print("  │                                                      │")
print("  │  → 14π = ln(M_Pl/m_p) の解釈は                      │")
print("  │    「QCD次元変換」ではなく                           │")
print("  │    「m_p が直接的に算術的に固定される」              │")
print("  │    という仮説に依存する。                            │")
print("  │                                                      │")
print("  └──────────────────────────────────────────────────────┘")
print()

# ============================================================================
print("=" * 70)
print("  ■ 総合判定")
print("=" * 70)

print(f"""
  ── 3つのタスクの結果 ──

  Task 1: 14π は m_p を直接与える（Λ_QCD ではない）
    M_Pl × exp(-14π) = 0.967 GeV ≈ m_p = 0.938 GeV (3.1%)
    標準的QCD とは別の機構を必要とする。
    偶然の一致の可能性を排除できない。

  Task 2: α_GUT = 1/49 はまだ「導出」されていない
    49 = 4 × |ζ(-1)|⁻¹ + 1 = 4×12+1 という分解は見つかった。
    しかし d=4 と +1 の「なぜ」が未解決。
    14π と 49 の関係は循環的な可能性がある。

  Task 3: m_p/Λ_QCD ≈ 4.3 に算術構造なし
    非摂動的QCD の結果。数論とは直接つながらない。

  ── 14π の信頼度（更新後） ──

  以前: 「0.07% の一致、画期的」
  今:   「0.07% で合う事実は変わらないが、
         理論的根拠は循環的であり、
         偶然の一致を排除する手段がない」

  ── GPU投資の判断（更新後） ──

  14π の精密化のため: ✗ 根拠不足
  α の素数ペア構造解明のため: △ 探索的価値あり
  真空破壊閾値の定量化のため: △ 面白いが検証困難

  ── 本当に次にやるべきこと ──

  GPU ではなく:
  1. 14π = ln(M_Pl/m_p) が偶然でないことの独立な証拠を探す
     例: 他の粒子質量にも類似の公式があるか？
     m_n/M_Pl, m_e/M_Pl, m_W/M_Pl, m_H/M_Pl なども
     nπ の形で書けるか？ もし m_p だけなら偶然の疑い強い。
  2. |K₃(Z)| = 48 と α_GUT の関係をリヒテンバウム予想の
     枠組みで厳密に調べる（これは純粋数学の問題）
""")

# ============================================================================
# BONUS: Check if other masses satisfy nπ relations
# ============================================================================

print("=" * 70)
print("  ■ ボーナス: 他の質量比も nπ か？")
print("=" * 70)
print()

masses = {
    'm_e': 0.000511,
    'm_μ': 0.10566,
    'm_τ': 1.777,
    'm_p': 0.938,
    'm_n': 0.9396,
    'm_W': 80.38,
    'm_Z': 91.19,
    'm_H': 125.1,
    'm_t': 173.0,
    'Λ_QCD': 0.217,
}

print(f"  {'粒子':<8s} {'質量 (GeV)':<14s} {'ln(M_Pl/m)':<14s} {'最近い nπ':<12s} {'n':<6s} {'残差%':<10s}")
print(f"  {'-'*68}")

for name, mass in masses.items():
    ln_val = np.log(M_Pl / mass)
    # Find closest nπ
    n_best = round(ln_val / pi)
    npi_best = n_best * pi
    resid = (ln_val - npi_best) / npi_best * 100
    print(f"  {name:<8s} {mass:<14.4f} {ln_val:<14.4f} {n_best}π={npi_best:<10.4f} {n_best:<6d} {resid:>+8.2f}%")

print()

# Check: how special is the 0.07% for m_p?
# If we randomly pick masses, what fraction have |residual| < 0.1%?
# For a random x, the distance to the nearest nπ is uniform on [0, π/2].
# P(|residual/nπ| < 0.001) ≈ 2 × 0.001 × nπ / (π/2) = 4 × 0.001 × n
# For n=14: P ≈ 0.056 = 5.6%. Not that unlikely!

print(f"  ── 統計的有意性 ──")
print()
print(f"  ln(M_Pl/m_p)/π = {np.log(M_Pl/m_p)/pi:.6f}")
print(f"  最近い整数: 14")
print(f"  残差: {(np.log(M_Pl/m_p)/pi - 14):.6f}")
print()
print(f"  ランダムな質量で |残差| < 0.001 (= 0.07% に相当) の確率:")
print(f"  ≈ 2 × 0.001 × n ≈ 2 × 0.001 × 14 = {2*0.001*14:.3f} = {2*0.001*14*100:.1f}%")
print()
print(f"  → 14π の一致が偶然である確率は約 3%。")
print(f"    「統計的に有意」の閾値（5%）は超えるが、")
print(f"    「圧倒的」ではない。")
print(f"    10個の質量で同時にテストしているので、")
print(f"    Bonferroni補正後: 3% × 10 = 30%。")
print(f"    → 偶然の可能性が十分にある。")
print()

# However, let's see if multiple masses give good nπ fits:
good_fits = []
for name, mass in masses.items():
    ln_val = np.log(M_Pl / mass)
    n_best = round(ln_val / pi)
    npi_best = n_best * pi
    resid = abs(ln_val - npi_best) / npi_best * 100
    if resid < 1.0:
        good_fits.append((name, n_best, resid))

print(f"  残差 < 1% のもの:")
for name, n, r in good_fits:
    print(f"    {name}: {n}π, 残差 {r:.2f}%")

print()
print("=" * 70)
print("  END")
print("=" * 70)
