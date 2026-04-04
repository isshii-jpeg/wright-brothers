"""
BC System: Alternative Physical Interpretations & Expansions
=============================================================

Starting from the ROCK:
  - BC partition function Z(β) = ζ(β) is a theorem
  - E-M expansion gives Bernoulli numbers — theorem
  - 120 ≈ 137 (12%), 252 ≈ 251 (0.4%) — observed

Mission: Find OTHER ways to extract physics from the BC system,
beyond the spectral action + E-M expansion.

Three axes of exploration:
  Axis A: Alternative physical interpretations of the BC system
  Axis B: Alternative expansions (not E-M) of Σζ(m)
  Axis C: Other quantities computable from BC (not just Tr(f(D)))

Wright Brothers, 2026
"""

import numpy as np
from math import factorial, comb
import mpmath
from scipy.special import zeta as sp_zeta

mpmath.mp.dps = 30
pi = np.pi
gamma_em = 0.5772156649015329
alpha_inv_exp = 137.035999084

print("=" * 70)
print("  BC系の代替的物理解釈と展開")
print("=" * 70)

# ============================================================================
#  AXIS A: Alternative physical interpretations
# ============================================================================

print()
print("=" * 70)
print("  AXIS A: BC系の代替的物理解釈")
print("=" * 70)

# ============================================================================
print("""
  ■ A1: BC系 = 素数の統計力学系

  Bost-Connes系の分配関数: Z(β) = ζ(β)
  これは「素数を粒子とする統計力学系」の分配関数。

  各素数 p は「エネルギー ε_p = log(p)」を持つ粒子。
  温度 T = 1/β での分配関数:
    Z(β) = Π_p 1/(1-p^{-β}) = Π_p 1/(1-e^{-β log p})

  これはボソン系の分配関数:
    Z = Π_modes 1/(1-e^{-βε_mode})

  → BC系は「素数をモードとするボソン気体」。

  ★ 物理量の抽出:
  熱力学量 = Z の微分で得られる。
""")

# Thermodynamic quantities from Z(β) = ζ(β)
# Free energy: F = -T ln Z = -(1/β) ln ζ(β)
# Energy: E = -∂/∂β ln Z = -ζ'(β)/ζ(β)
# Entropy: S = β(E - F) = β²∂F/∂β = ...
# Specific heat: C = -β² ∂E/∂β

print("  ── BC 熱力学 ──")
print()

for beta in [1.5, 2.0, 3.0, 4.0, 5.0, 10.0]:
    z_val = float(mpmath.zeta(beta))
    z_prime = float(mpmath.diff(mpmath.zeta, beta))
    z_double = float(mpmath.diff(mpmath.zeta, beta, n=2))

    F = -np.log(z_val) / beta  # Free energy per unit
    E = -z_prime / z_val  # Internal energy
    C = beta**2 * (z_double/z_val - (z_prime/z_val)**2)  # Specific heat

    print(f"  β={beta:>4.1f}: F={F:>8.4f}, E={E:>8.4f}, C={C:>8.4f}, "
          f"ζ'/ζ={z_prime/z_val:>8.4f}")

print()

# The ratio ζ'/ζ is the LOGARITHMIC DERIVATIVE of ζ.
# At β=2: ζ'(2)/ζ(2) = ?

print("  ★ 対数微分 ζ'(β)/ζ(β) の特殊値:")
print()
for beta in [2, 3, 4, 5]:
    ratio = float(mpmath.diff(mpmath.zeta, beta)) / float(mpmath.zeta(beta))
    print(f"    -ζ'({beta})/ζ({beta}) = {-ratio:.6f}")

print()

# ============================================================================
print("""
  ■ A2: BC相転移と物理定数

  BC系は β = 1 で相転移を起こす（ζ(1) の極）。
  β > 1: 秩序相（KMS状態が非自明）
  β < 1: 無秩序相

  相転移点 β_c = 1 の近くでの振る舞い:
    ζ(β) ≈ 1/(β-1) + γ + γ₁(β-1) + ...

  ★ 比熱の発散（相転移のシグネチャ）:
  C ∝ 1/(β-1)² (β → 1⁺)

  物理的解釈: β_c = 1 での相転移は
  「閉じ込め-非閉じ込め転移」に類似。
  β > 1（低温）: 素数が「閉じ込められた」相 → ハドロン的
  β < 1（高温）: 素数が「自由な」相 → クォーク-グルーオン的
""")

# Check: does the BC critical temperature relate to any physical scale?
# β_c = 1 in BC units. What is "1" in physical units?
# If ε_p = log(p), then β = 1 means kT = 1 in units where ε₂ = log 2.
# The "temperature" of the phase transition is kT_c = 1 (in log units).

# In terms of the smallest prime: kT_c/ε₂ = 1/log(2) = 1.443
print(f"  kT_c / ε₂ = 1/ln(2) = {1/np.log(2):.4f}")
print(f"  kT_c / ε₃ = 1/ln(3) = {1/np.log(3):.4f}")
print(f"  kT_c / ε₅ = 1/ln(5) = {1/np.log(5):.4f}")
print()

# ============================================================================
print("""
  ■ A3: BC系の自由エネルギーと α

  自由エネルギー F(β) = -(1/β) ln ζ(β)

  特殊な β での値:
""")

for beta_val in [2, 3, 4, 5, 6, 7]:
    z = float(mpmath.zeta(beta_val))
    F = -np.log(z) / beta_val
    print(f"  β={beta_val}: F = -ln(ζ({beta_val}))/{beta_val} = -ln({z:.6f})/{beta_val} = {F:.6f}")

print()

# Is there a β where F relates to α?
# F(β) = -(1/β) ln ζ(β)
# We want: some function of F to equal 1/137 or 137.

# 1/F(2) = 2/ln(ζ(2)) = 2/ln(π²/6)
val = 2/np.log(pi**2/6)
print(f"  1/F(2) = 2/ln(π²/6) = {val:.6f}")
print(f"  e^{1/val:.4f} = ... not obviously related to α")
print()

# ============================================================================
#  AXIS B: Alternative expansions of Σζ(m)
# ============================================================================

print("=" * 70)
print("  AXIS B: Σζ(m) の代替展開")
print("=" * 70)

# ============================================================================
print("""
  ■ B1: Abel 総和法（E-M の代わりに）

  E-M展開は「離散和 → 積分 + 補正」。
  Abel総和法は「Σ a_n → lim_{x→1⁻} Σ a_n x^n」。

  S = Σ_{m=1}^∞ ζ(m) は発散するが、
  Abel 正則化: S_Abel = lim_{x→1⁻} Σ_{m=1}^∞ ζ(m) x^m
""")

# Compute the Abel sum numerically
print("  Abel 正則化された和:")
print()

for x in [0.5, 0.7, 0.8, 0.9, 0.95, 0.99, 0.999]:
    S_abel = sum(float(mpmath.zeta(m)) * x**m for m in range(2, 200))
    print(f"  x = {x:.3f}: Σ ζ(m) x^m = {S_abel:.6f}")

print()

# The Abel sum diverges as x → 1 (because ζ(1) = ∞).
# But the RATE of divergence may contain physics.
# S_Abel ≈ -ln(1-x) + (finite part) as x → 1

# Extract the finite part:
# S_Abel - (-ln(1-x)) → finite as x → 1
print("  Abel 総和の有限部分 (S - (-1/(1-x))):")
print()
for x in [0.9, 0.95, 0.99, 0.995, 0.999]:
    S_abel = sum(float(mpmath.zeta(m)) * x**m for m in range(2, 500))
    pole = x / (1-x)  # leading divergence from ζ(1) ~ 1/(m-1)... actually ζ(m)→1 for large m
    # For large m: ζ(m) ≈ 1 + 2^{-m} + ..., so Σ ζ(m)x^m ≈ Σ x^m + Σ(ζ(m)-1)x^m
    # Σ x^m = x/(1-x) (divergent), Σ(ζ(m)-1)x^m (convergent)
    finite_part = S_abel - x**2/(1-x)  # subtract Σ_{m≥2} x^m = x²/(1-x)
    print(f"  x = {x:.3f}: S - x²/(1-x) = {finite_part:.6f}")

print()

# The convergent part: Σ_{m=2}^∞ (ζ(m)-1) x^m
# At x=1: Σ(ζ(m)-1) = 1 (known identity!)
print("  収束部分 Σ (ζ(m)-1) x^m:")
print()
for x in [0.5, 0.8, 0.9, 0.95, 1.0]:
    if x < 1:
        conv = sum((float(mpmath.zeta(m))-1) * x**m for m in range(2, 200))
    else:
        conv = sum(float(mpmath.zeta(m))-1 for m in range(2, 200))
    print(f"  x = {x:.2f}: Σ(ζ(m)-1)x^m = {conv:.8f}")

print()
print(f"  ★ x=1 での値: Σ(ζ(m)-1) = 1.000 (厳密)")
print(f"    この「1」は何を意味するか？")
print()

# ============================================================================
print("""
  ■ B2: Dirichlet 級数表現

  Σ_{m=1}^∞ ζ(m) x^m = Σ_{m=1}^∞ Σ_{n=1}^∞ (x/1)^m / n^m...
  ではなく正確に:
  Σ_{m=2}^∞ ζ(m) x^m = Σ_{n=1}^∞ Σ_{m=2}^∞ x^m/n^m
                       = Σ_{n=1}^∞ (x/n)²/(1-x/n)  (|x| < 1)

  n=1 の項: x²/(1-x) → 発散（x→1）
  n≥2 の項: 有限
""")

# Compute for each n separately
print("  各 n の寄与 (x=0.999):")
print()
x = 0.999
for n in range(1, 11):
    if n == 1:
        contrib = (x)**2 / (1 - x)
    else:
        contrib = (x/n)**2 / (1 - x/n)
    print(f"  n = {n:>2d}: (x/n)²/(1-x/n) = {contrib:>12.6f}")

print()

# At x=1:
# n=1: diverges
# n=2: (1/2)²/(1-1/2) = (1/4)/(1/2) = 1/2
# n=3: (1/3)²/(1-1/3) = (1/9)/(2/3) = 1/6
# n=4: (1/4)²/(1-3/4) = (1/16)/(3/4) = 1/12
# General n≥2: (1/n)²/(1-1/n) = 1/(n(n-1)) = 1/(n-1) - 1/n

print("  x=1 での各 n≥2 の寄与:")
print()
total = 0
for n in range(2, 20):
    contrib = 1/(n*(n-1))
    total += contrib
    print(f"  n = {n:>2d}: 1/(n(n-1)) = {contrib:.6f}, 累積 = {total:.6f}")

print(f"  → Σ_{{n≥2}} 1/(n(n-1)) = 1 (テレスコピング和) ✓")
print()

# ============================================================================
print("""
  ■ B3: メリン変換表現

  ζ(s) = (1/Γ(s)) ∫₀^∞ t^{s-1}/(e^t-1) dt  (s > 1)

  したがって:
  Σ_m ζ(m) x^m = Σ_m x^m/(Γ(m)) ∫₀^∞ t^{m-1}/(e^t-1) dt

  和と積分を交換:
  = ∫₀^∞ 1/(e^t-1) × [Σ_m (xt)^{m-1} x/Γ(m)] dt

  Σ_m (xt)^{m-1}/Γ(m) = Σ_m (xt)^{m-1}/(m-1)! = e^{xt}

  → Σ_m ζ(m) x^m = x ∫₀^∞ e^{xt}/(e^t-1) dt

  x < 1 で収束。x → 1 で:
  ∫₀^∞ e^t/(e^t-1) dt = ∫₀^∞ 1/(1-e^{-t}) dt → 発散

  ★ これはボーズ-アインシュタイン積分の変形！
""")

# Compute the Mellin representation numerically
from scipy.integrate import quad

print("  メリン表現の数値計算:")
print()

for x in [0.5, 0.7, 0.9, 0.95]:
    def integrand(t):
        if t < 1e-10:
            return x  # limit as t→0: e^{xt}/(e^t-1) ≈ 1/t → x×1/t, but regulated
        return np.exp(x*t) / (np.exp(t) - 1)

    result, _ = quad(integrand, 0.001, 50, limit=200)
    result *= x
    # Compare with direct sum
    direct = sum(float(mpmath.zeta(m)) * x**m for m in range(2, 200))
    print(f"  x={x:.2f}: Mellin = {result:.6f}, 直接和 = {direct:.6f}, "
          f"差 = {abs(result-direct):.4f}")

print()

# ============================================================================
#  AXIS C: Other quantities from BC system
# ============================================================================

print("=" * 70)
print("  AXIS C: BC系からの他の物理量")
print("=" * 70)

# ============================================================================
print("""
  ■ C1: KMS 状態と真空期待値

  BC系の β > 1 での KMS 状態 φ_β は:
    φ_β(e(r)) = r^{-β}/ζ(β)  (素数のべき r に対して)

  β = 2 での期待値:
    φ₂(e(n)) = n⁻²/ζ(2) = 6n⁻²/π²

  これは「素数 p の占有確率」:
    P(p) = p⁻²/ζ(2) = 6/(π²p²)

  P(2) = 6/(4π²) ≈ 0.152
  P(3) = 6/(9π²) ≈ 0.068
  P(5) = 6/(25π²) ≈ 0.024
""")

print("  素数の占有確率 (β=2):")
print()
for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
    prob = 6 / (pi**2 * p**2)
    print(f"  P({p:>2d}) = 6/(π²×{p}²) = {prob:.6f}")

total_prob = sum(6/(pi**2 * p**2) for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47])
print(f"  Σ P(p) for p≤47 = {total_prob:.6f}")
print(f"  Σ P(p) for all p = (6/π²) × P₂ where P₂ = Σ 1/p² = 0.4522...")
P2 = sum(1/p**2 for p in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97])
print(f"  (6/π²) × P₂ ≈ {6/pi**2 * P2:.6f} (P₂={P2:.4f})")
print()

# ============================================================================
print("""
  ■ C2: BC系のエントロピーと α

  エントロピー S(β) = β E(β) + ln Z(β)
                     = β × (-ζ'(β)/ζ(β)) + ln ζ(β)
""")

print("  BC エントロピー:")
print()
for beta in [1.1, 1.5, 2.0, 3.0, 5.0, 10.0]:
    z = float(mpmath.zeta(beta))
    zp = float(mpmath.diff(mpmath.zeta, beta))
    E = -zp/z
    S = beta * E + np.log(z)
    print(f"  β={beta:>5.1f}: E={E:>10.4f}, S={S:>10.6f}, "
          f"S/ln(2)={S/np.log(2):>10.4f}")

print()

# ============================================================================
print("""
  ■ C3: BC系の相関関数

  2点相関関数: G(m,n) = <e(m) e(n)*> - <e(m)><e(n)*>
  BC系の KMS 状態での2点関数はリーマンゼータの
  比で表される。

  特に: G₂(p,q) = ζ(2β)/(ζ(β))² × (pq)^{-β} (p≠q, 素数)

  β=1 近傍での相関長の発散が「臨界現象」。
""")

# Compute correlation at β=2
print("  2点相関 (β=2):")
print()
z2 = float(mpmath.zeta(2))
z4 = float(mpmath.zeta(4))

for p, q in [(2,3), (2,5), (3,5), (2,7), (5,7)]:
    G = z4/z2**2 * (p*q)**(-2)
    uncorr = (p**(-2)/z2) * (q**(-2)/z2)
    print(f"  G({p},{q}) = {G:.8f}, 非相関部分 = {uncorr:.8f}, "
          f"比 = {G/uncorr:.4f}")

print()

# ============================================================================
print("""
  ■ C4: 素数計数関数 π(x) とスペクトル作用

  リーマンの明示公式:
    π(x) = li(x) - Σ_ρ li(x^ρ) + ...
  ρ はゼータの非自明な零点。

  スペクトル作用 S = Σ_m ζ(m) の中に、
  零点の情報はどのように入っているか？

  ζ(s) = exp(Σ_ρ ln(1-s/ρ) + ...) (Hadamard積)

  → S の中にリーマン零点の情報が暗黙的に含まれる。
  → ゼータ零点は「スペクトル作用のエネルギー準位」に対応？

  ★ もしリーマン零点が物理的スペクトルなら、
    α は零点の分布で決まる可能性がある。
    零点の統計はGUE（ガウス・ユニタリー・アンサンブル）。
    GUE は量子カオスの普遍性クラス。
""")

# Riemann zeros and 137?
# The average spacing of zeros near height T is 2π/ln(T/(2π)).
# The first zero is at ρ₁ = 1/2 + 14.135i
# 14.135 ≈ 14π/π = 14? No, 14.135/π = 4.499 ≈ 4.5 = 9/2

print("  リーマンゼータの最初の零点:")
print()
zeros = [14.1347, 21.0220, 25.0109, 30.4249, 32.9351, 37.5862, 40.9187, 43.3271]
for i, t in enumerate(zeros):
    print(f"  ρ_{i+1} = 1/2 + {t:.4f}i, t/π = {t/pi:.4f}")

print()

# Sum of 1/|ρ|² for the first few zeros
sum_inv_rho2 = sum(1/(0.25 + t**2) for t in zeros)
print(f"  Σ 1/|ρ_k|² (最初の8個) = {sum_inv_rho2:.6f}")
print(f"  × 4π² = {sum_inv_rho2 * 4*pi**2:.4f}")
print()

# ============================================================================
#  AXIS D: Cross-checks — which coincidences survive?
# ============================================================================

print("=" * 70)
print("  AXIS D: 生き残る一致はどれか")
print("=" * 70)
print()

# Collect ALL numerical "coincidences" and rate them
print("  全ての数値的一致の格付け:")
print()
print(f"  {'一致':.<40s} {'精度':>8s} {'足し算?':>8s} {'独立?':>6s} {'評価':>4s}")
print(f"  {'-'*72}")

coincidences = [
    ("4/|B₄| = 120 ≈ 1/α = 137", "12%", "NO", "YES", "★★"),
    ("6/|B₆| = 252 ≈ Δaμ+1 = 252", "0.4%", "NO", "YES", "★★★"),
    ("12+120 = 132 ≈ 137", "3.6%", "YES", "NO", "★"),
    ("132+5+0.036 = 137.036", "0.00002%", "YES++", "NO", "☆"),
    ("ζ(-3)=1/120, dark energy", "2×", "NO", "YES", "★"),
    ("14π ≈ ln(M_Pl/m_p)", "0.07%", "NO", "circ.", "★"),
    ("|K₃(Z)|=48 ≈ Δa_e coeff", "—", "NO", "YES", "★★"),
    ("符号反転定理（全素数）", "exact", "NO", "YES", "★★★"),
    ("K₁ 位相的保護", "exact", "NO", "YES", "★★★"),
]

for name, prec, addition, indep, rating in coincidences:
    print(f"  {name:.<40s} {prec:>8s} {addition:>8s} {indep:>6s} {rating:>4s}")

print()
print("""
  評価基準:
    ★★★ = 数学的定理 or 足し算不要で高精度
    ★★  = 足し算不要で中精度、または定理的
    ★   = 面白いが弱い
    ☆   = 足し算に依存（批判に耐えない）

  ★★★ の一致（揺るがない）:
    (1) 252 ≈ 251 (j=3 単独)
    (2) 符号反転定理
    (3) K₁ 位相的保護

  ★★ の一致（かなり面白い）:
    (4) 120 ≈ 137 (j=2 単独、12%)
    (5) |K₃(Z)| = 48 と電子 g-2
""")

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 方針提案
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  「岩」から広げる研究方針:

  ── 最優先: 252 = 6/|B₆| とミューオン g-2 ──

  これは最も堅固な一致（0.4%、足し算不要、j=3 単独）。
  問いを絞る:
  「なぜ BC 系の j=3 スペクトル作用項が
   ミューオンの異常磁気モーメントに一致するのか？」

  追究すべき方向:
  (a) j=3 の項 = a₆ Seeley-DeWitt 係数。
      コンヌの枠組みでは a₆ は「ヒッグスの自己結合」に関連。
      ミューオン g-2 の先頭ハドロン寄与との接続は？
  (b) 252 = 1/|ζ(-5)|。ζ(-5) の物理的意味は何か？
  (c) |K₇(Z)| = 240 = 2×120。K₇ と j=4 の関係。

  ── 次に: 符号反転定理の物理的実現 ──

  数学的に最も堅固。足し算問題と完全に独立。
  問い:
  「ζ_{¬p}(-3) < 0 は、実際の量子系で実現可能か？」

  これは SQUID 実験の動機であり、
  理論的予測 → 実験的検証 の最短経路。

  ── 並行して: BC 熱力学の探索 ──

  Z(β) = ζ(β) からの熱力学量（E, S, C）に
  物理定数と整合する値がないか系統的に探索。
  特に β_c = 1 近傍の臨界指数。

  ── 保留: α の精密導出 ──

  「足し算問題」が解決するまで、
  1/α = 12 + 120 + 5 + 0.036 は主張しない。
  120 ≈ 137 (12%) のみを控えめに報告。
""")

print("=" * 70)
print("  END")
print("=" * 70)
