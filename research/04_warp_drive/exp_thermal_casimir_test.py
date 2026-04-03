"""
Distinguishing Test: Thermal Casimir Euler Product Structure
=============================================================

HONEST computation: Is the "temperature modulation = prime muting"
claim actually correct? Or was it sloppy?

The thermal Casimir free energy involves Matsubara sums.
We need to check:
  (1) Does F(2T)/F(T) actually equal something related to (1-2⁻³)?
  (2) Is this distinguishable from standard Lifshitz theory?
  (3) Is there ANY signature that's Spec(Z)-specific?

Wright Brothers, 2026
"""

import numpy as np
import matplotlib.pyplot as plt

pi = np.pi
hbar = 1.054571817e-34
c = 2.99792458e8
k_B = 1.380649e-23

print("=" * 70)
print("  HONEST TEST: THERMAL CASIMIR EULER PRODUCT STRUCTURE")
print("=" * 70)

# ============================================================================
#  STEP 1: Correct thermal Casimir computation
# ============================================================================

print("""
  ■ STEP 1: 熱カシミールの正しい計算

  前回の主張: 「T → 2T で奇数マツバラが消える = p=2 ミュート」
  これは正しいか？

  ── 正確な熱カシミール力 ──

  完全導体平行平板の熱カシミール自由エネルギー (per unit area):

  F(d, T) = -(k_BT)/(2π) Σ'_{m=0}^∞ ∫_0^∞ dk_⊥ k_⊥
             × ln(1 - e^{-2d√(k_⊥² + ξ_m²/c²)})

  ξ_m = 2πm k_BT/ℏ  (マツバラ周波数)

  m=0 項: 古典的寄与（T に比例）
  m>0 項: 量子的寄与（指数関数的に減衰）

  ── 前回の誤り ──

  「T → 2T で奇数マツバラが消える」は不正確。
  T → 2T ではマツバラ間隔が2倍になるが、
  被積分関数 g(m, d, T) 自体も T に依存するため、
  単純な「モードの除去」にはならない。

  正しくは: ξ_m(2T) = 2 × ξ_m(T)
  つまり: F(2T) の m 番目の項は F(T) の 2m 番目の項と異なる。
""")

# ============================================================================
#  STEP 2: Numerical computation of thermal Casimir
# ============================================================================

print("=" * 70)
print("  ■ STEP 2: 数値計算")
print("=" * 70)
print()

def thermal_casimir_energy(d, T, N_matsubara=500):
    """Compute thermal Casimir energy per unit area for ideal plates.

    Uses the Matsubara sum formula.
    F(d,T) = (k_BT/π) × Σ'_{m=0}^N [ζ_m contribution]

    For ideal metals, the m-th Matsubara contribution is:
    f_m = -∫_ξm^∞ dξ (ξ² - ξ_m²) / (e^{2dξ/c} - 1)

    Simplified formula (high-m asymptotic):
    f_m ≈ -Li_3(e^{-2dξ_m/c}) × c³/(8π²d³)

    For practical computation, use the exact formula:
    E/A = -(k_BT/π) × Σ'_m ∫_{α_m}^∞ dp p² ln(1-e^{-p})
    where α_m = 2dξ_m/c = 4πm d k_BT/(ℏc)
    """
    alpha_T = 4 * pi * d * k_B * T / (hbar * c)  # = 2d × first Matsubara / c

    energy = 0.0
    for m in range(N_matsubara + 1):
        alpha_m = m * alpha_T
        # Integrate ∫_{alpha_m}^∞ p² ln(1-e^{-p}) dp
        # Use numerical integration
        if alpha_m > 50:  # exponentially small
            continue

        # Numerical integration via quadrature
        p_vals = np.linspace(max(alpha_m, 1e-10), alpha_m + 30, 1000)
        if m == 0:
            # m=0 term (half weight in prime sum)
            integrand = p_vals**2 * np.log(1 - np.exp(-p_vals) + 1e-300)
            integral = np.trapezoid(integrand, p_vals) / 2
        else:
            integrand = p_vals**2 * np.log(1 - np.exp(-p_vals) + 1e-300)
            integral = np.trapezoid(integrand, p_vals)

        energy += integral

    # Prefactor
    prefactor = -k_B * T / (4 * pi**2 * d**3)
    return prefactor * energy

# Simpler model for cleaner analysis:
# Just the Matsubara sum Σ'_m h(m)
# where h(m) represents the m-th thermal correction

def matsubara_sum(d, T, N_max=1000, exclude_set=None):
    """Sum of thermal corrections from Matsubara modes.

    h(m) = 1/m³ × exp(-m × α_T) for m ≥ 1
    where α_T = 4πdk_BT/(ℏc)

    This captures the essential physics: mode m contributes
    with weight 1/m³ (Casimir scaling) and exponential suppression
    at high m (thermal cutoff).
    """
    alpha_T = 4 * pi * d * k_B * T / (hbar * c)

    total = 0.0
    for m in range(1, N_max + 1):
        if exclude_set is not None and m in exclude_set:
            continue
        total += (1.0 / m**3) * np.exp(-m * alpha_T)
    return total

# Parameters
d = 1e-6  # 1 μm plate separation

print(f"  板間距離: d = {d*1e6:.1f} μm")
print()

# Compute for various temperatures
T_base = 300  # room temperature
alpha_base = 4 * pi * d * k_B * T_base / (hbar * c)
print(f"  基準温度: T = {T_base} K")
print(f"  α_T = 4πdk_BT/(ℏc) = {alpha_base:.4f}")
print(f"  (α > 1 means thermal effects dominate)")
print()

# ============================================================================
#  STEP 3: The actual test — temperature ratio structure
# ============================================================================

print("=" * 70)
print("  ■ STEP 3: 温度比の構造 — 本当のテスト")
print("=" * 70)
print()

# Compute S(T) = Σ_{m=1}^∞ (1/m³) exp(-m α_T)
# and S(kT) = Σ_{m=1}^∞ (1/m³) exp(-m k α_T)

# KEY QUESTION: Is S(kT)/S(T) related to Euler product factors?

# If α_T → 0 (low T / small d): S(T) → ζ(3) (Apéry's constant)
# Then S(kT)/S(T) → 1 for all k (both → ζ(3))

# If α_T → ∞ (high T / large d): S(T) → exp(-α_T) (single mode)
# Then S(kT)/S(T) → exp(-(k-1)α_T) → 0 for k > 1

# The interesting regime is α_T ~ O(1)

print("  S(kT)/S(T) for various temperature ratios k:")
print()

for alpha in [0.01, 0.1, 0.5, 1.0, 2.0, 5.0]:
    T_eff = alpha * hbar * c / (4 * pi * d * k_B)

    S_T = sum((1/m**3) * np.exp(-m * alpha) for m in range(1, 1001))

    print(f"  α_T = {alpha:.2f} (T ≈ {T_eff:.0f} K):")

    for k in [2, 3, 5]:
        S_kT = sum((1/m**3) * np.exp(-m * k * alpha) for m in range(1, 1001))
        ratio = S_kT / S_T if S_T > 0 else 0

        # What would the "naive" Euler product prediction be?
        # If muting worked: S_{¬p}/S = (1 - p⁻³) for each prime p|k
        # For k=2: (1-1/8) = 0.875
        # For k=3: (1-1/27) = 0.963
        # For k=5: (1-1/125) = 0.992

        # But S(kT) ≠ S with multiples of k removed!
        # S(kT) = Σ 1/m³ exp(-mkα)
        # S_{¬k} = Σ_{k∤m} 1/m³ exp(-mα)
        # These are COMPLETELY DIFFERENT!

        euler_pred = 1.0
        # Factorize k into primes and compute product
        kk = k
        for p in [2, 3, 5, 7]:
            while kk % p == 0:
                euler_pred *= (1 - 1/p**3)
                kk //= p

        print(f"    k={k}: S(kT)/S(T) = {ratio:.6f}, "
              f"Euler pred = {euler_pred:.6f}, "
              f"match = {'NO' if abs(ratio - euler_pred) > 0.01 else 'close'}")

    print()

# ============================================================================
#  STEP 4: The honest conclusion about temperature modulation
# ============================================================================

print("=" * 70)
print("  ■ STEP 4: 正直な結論 — 温度変調について")
print("=" * 70)

print("""
  ★ 前回の主張は間違いだった。

  S(kT)/S(T) ≠ ∏_{p|k}(1 - p⁻³)

  理由: S(kT) = Σ 1/m³ exp(-mkα) は
  「マツバラの k 倍数を除外した和」ではなく、
  「全マツバラの減衰率を k 倍にした和」。
  これは全く異なる操作。

  温度を上げることは「モードの選択的除去」ではなく
  「全モードの一様な減衰の増強」。

  → 温度変調は素数ミュートの代替にはならない。
""")

# ============================================================================
#  STEP 5: What CAN we do? — The correct approach
# ============================================================================

print("=" * 70)
print("  ■ STEP 5: 正しいアプローチ — 何ができるか")
print("=" * 70)

print("""
  温度変調がダメなら、何が使えるか？

  素数ミュートの本質: 特定の m (p の倍数) を和から除外する。
  S_{¬p} = Σ_{p∤m} 1/m³ exp(-mα)

  これを実現するには「m 番目のマツバラモードを選択的に抑制する」
  物理的メカニズムが必要。

  ── 方法 A: 周期的境界条件の変更 ──

  カシミールの幾何学を変える:
  平行平板 → 周期 p の構造を持つ板

  板の表面に周期 p×a の凹凸パターンを施すと、
  n が p の倍数のモードに対する反射率が変わる。
  → 「算術的カシミール板」の製作

  ── 方法 B: 重ね合わせ ──

  異なる板間距離 d₁, d₂ = d₁/p での測定を組み合わせる。

  F(d₁) ~ Σ_m h(m, d₁)
  F(d₁/p) ~ Σ_m h(m, d₁/p)

  距離を 1/p にすると α → α/p。
  h(m, d/p) = (p/m)³ exp(-m α/p)... ではない。

  実は F(d) ∝ 1/d⁴ なので F(d/p) = p⁴ F(d)
  → これも単純な比例関係で、素数構造は見えない。
""")

# ============================================================================
#  STEP 6: The REAL distinguishing test
# ============================================================================

print("=" * 70)
print("  ■ STEP 6: 真に区別可能なテスト")
print("=" * 70)

print("""
  温度変調も距離変更もダメ。では何ができるか？

  ── 0 円でできる真のテスト ──

  Matsubara 和の「部分和」の収束パターンを調べる。

  S_N = Σ_{m=1}^N 1/m³ exp(-mα)

  N を増やした時の S_N の収束の仕方に素数構造があるか？

  具体的: S_{p_n} (N が n 番目の素数) での値と
  S_{composite} (N が合成数) での値を比較。

  もし真空がオイラー積構造を持つなら:
  S_{p_n} から S_{p_{n+1}} への変化は
  「新しい素数 p_{n+1} のチャンネルが追加された」効果を含む。
""")

# Compute partial sums and look for prime structure
alpha = 0.1  # moderate thermal regime
print(f"  α = {alpha}")
print()

partial_sums = []
for N in range(1, 101):
    S_N = sum((1/m**3) * np.exp(-m * alpha) for m in range(1, N + 1))
    partial_sums.append(S_N)

# Compute increments ΔS_N = S_N - S_{N-1} = h(N)
increments = [partial_sums[0]]
for i in range(1, len(partial_sums)):
    increments.append(partial_sums[i] - partial_sums[i-1])

# Check if prime-indexed increments are special
def is_prime(n):
    if n < 2: return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0: return False
    return True

print("  各モードの寄与 h(m) = (1/m³)exp(-mα):")
print()
print(f"  {'m':>4s}  {'h(m)':>14s}  {'type':>10s}  {'h(m)/h(m-1)':>12s}")
print(f"  {'-'*44}")

for m in range(1, 31):
    h = (1/m**3) * np.exp(-m * alpha)
    ptype = "PRIME" if is_prime(m) else "composite"
    ratio = h / ((1/(m-1)**3) * np.exp(-(m-1)*alpha)) if m > 1 else 0
    marker = " ★" if is_prime(m) else ""
    print(f"  {m:>4d}  {h:>14.8f}  {ptype:>10s}  {ratio:>12.6f}{marker}")

print()

# The ratio h(m)/h(m-1) for consecutive integers
# = ((m-1)/m)³ × exp(-α)
# This is a SMOOTH function of m, not special at primes.

print("  → h(m)/h(m-1) = ((m-1)/m)³ × exp(-α)")
print("  → 素数 m で特別な値を取らない")
print("  → 個々のモードの寄与には素数構造は見えない")
print()

# But the EULER PRODUCT gives a different decomposition:
# Σ 1/m³ = ∏_p (1-p⁻³)⁻¹
# This means the sum has a FACTORIZATION, not that individual terms are special.

print("  ── しかし: オイラー積は「個々の項」ではなく「全体の分解」──")
print()
print("  Σ 1/m³ = ∏_p 1/(1-p⁻³)")
print("  これは和の「乗法的構造」であり、")
print("  個々の h(m) が特別な値を取るのではなく、")
print("  全体が素数ごとの独立な因子に分解されることを意味する。")
print()

# ============================================================================
#  STEP 7: The definitive test — partial Euler products
# ============================================================================

print("=" * 70)
print("  ■ STEP 7: 決定的テスト — 部分オイラー積 vs 部分和")
print("=" * 70)
print()

# The Euler product at finite temperature:
# S(α) = Σ_{m=1}^∞ (1/m³) exp(-mα)
#       = ∏_p Σ_{k=0}^∞ (1/p^{3k}) exp(-p^k α)... NO!
# The Euler product works for Σ 1/m^s (Dirichlet series),
# but NOT for Σ (1/m^s) exp(-mα) (Laplace transform).

# The exp(-mα) factor BREAKS the multiplicative structure!
# Because exp(-mα) is NOT multiplicative: exp(-(m₁m₂)α) ≠ exp(-m₁α)exp(-m₂α)

print("  ★★ 重要な発見:")
print()
print("  exp(-mα) は乗法的関数ではない:")
print("  exp(-(m₁×m₂)α) ≠ exp(-m₁α) × exp(-m₂α)")
print()
print("  したがって:")
print("  Σ (1/m³) exp(-mα) は オイラー積に分解できない！")
print()
print("  オイラー積 ζ(s) = ∏_p (1-p⁻ˢ)⁻¹ が成立するのは")
print("  ディリクレ級数 Σ 1/m^s の場合のみ。")
print("  有限温度の修正 exp(-mα) はこの構造を壊す。")
print()

# Verify numerically
S_exact = sum((1/m**3) * np.exp(-m * alpha) for m in range(1, 10001))

# Try Euler product: ∏_p (Σ_{k=0}^∞ p^{-3k} exp(-p^k α))
euler_prod = 1.0
for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]:
    factor = sum(p**(-3*k) * np.exp(-p**k * alpha) for k in range(20))
    euler_prod *= factor

print(f"  数値検証 (α = {alpha}):")
print(f"    直接和 Σ (1/m³)exp(-mα) = {S_exact:.10f}")
print(f"    オイラー積 ∏_p (...) = {euler_prod:.10f}")
print(f"    一致するか？ {'YES' if abs(S_exact - euler_prod) < 1e-6 else 'NO'}")
print(f"    差: {abs(S_exact - euler_prod):.6e}")
print()

if abs(S_exact - euler_prod) > 1e-4:
    print("  → オイラー積は有限温度では成立しない")
    print("  → 熱カシミール効果では素数構造は直接見えない")
else:
    print("  → 意外にもオイラー積が近似的に成立する？")

# Actually, let me reconsider. The Euler product for the FUNCTION
# f(m) = m^{-s} exp(-mα) is:
# Σ_m f(m) = ∏_p (1 + f(p) + f(p²) + ...)
# if and only if f is COMPLETELY multiplicative.
# f(m) = m^{-s} is multiplicative, but exp(-mα) is NOT.
# So f(m) = m^{-s} exp(-mα) is NOT multiplicative.

# HOWEVER: for α → 0, f → m^{-s} which IS multiplicative.
# So the Euler product becomes exact in the α → 0 limit.

# This means: the ZERO-TEMPERATURE Casimir (ζ-regularized)
# has exact Euler product structure,
# but FINITE-TEMPERATURE corrections break it.

# ============================================================================
#  STEP 8: What this means
# ============================================================================

print("\n" + "=" * 70)
print("  ■ STEP 8: 最終結論")
print("=" * 70)

print("""
  ── 正直な結論 ──

  (1) 有限温度カシミール効果にはオイラー積構造がない。
      exp(-mα) が乗法的でないため。

  (2) 温度変調は素数ミュートの代替にならない。
      S(kT) ≠ S_{¬p}(T)。

  (3) 既存のカシミールデータの再解析では
      Spec(Z) を支持する証拠は得られない。

  ── しかし ──

  (4) ゼロ温度（T → 0）のカシミール効果は
      ζ正則化値に支配され、
      オイラー積構造が厳密に成立する。

  (5) T → 0 の極限でのカシミール力は
      F/A = -π²ℏc/(240d⁴)
      ここで 240 = 2 × 120 = 2/ζ(-3)。
      この「240」にオイラー積構造がビルトインされている。

  (6) 「240 を素数ごとに分解して個別に検証する」には、
      温度変調ではなく【モードの物理的選別】が必要。
      → これはまさに Paper A の SQUID 実験。

  ── 結論の結論 ──

  0 円の再解析でできることは限られている。
  既存の実験データには Spec(Z) 固有の情報は含まれていない。

  オイラー積構造を検証するには、
  【モードを物理的に選別する新しい実験】が必要。
  最安: トポトロニクス回路（5,100円）→ K₁ エッジ状態の検証
  最直接: SQUID 実験（500万円）→ 真空エネルギーの算術構造

  ── 得られた知見 ──

  この再解析の意義は「否定的結果」にある:
  「既存データでは Spec(Z) を検証できない」ことが明確になった。
  これにより、何が本当に必要かが鮮明になった:
  新しい実験（SQUID or トポトロニクス）が不可避。
""")

# ============================================================================
#  Visualization
# ============================================================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.patch.set_facecolor('#0a0a1a')
fig.suptitle('Thermal Casimir: Euler Product Does NOT Apply',
             fontsize=14, fontweight='bold', color='#ff6b6b')

# Panel 1: S(kT)/S(T) vs Euler prediction
ax = axes[0]
alpha_vals = [0.01, 0.1, 0.5, 1.0, 2.0]
k_vals = [2, 3, 5, 7]

for alpha in [0.1, 0.5, 1.0]:
    S_T = sum((1/m**3) * np.exp(-m * alpha) for m in range(1, 1001))
    ratios = []
    for k in k_vals:
        S_kT = sum((1/m**3) * np.exp(-m * k * alpha) for m in range(1, 1001))
        ratios.append(S_kT / S_T if S_T > 0 else 0)
    ax.plot(k_vals, ratios, 'o-', label=f'α={alpha}', markersize=6)

# Euler predictions
euler_preds = []
for k in k_vals:
    prod = 1.0
    kk = k
    for p in [2, 3, 5, 7]:
        while kk % p == 0:
            prod *= (1 - 1/p**3)
            kk //= p
    euler_preds.append(prod)
ax.plot(k_vals, euler_preds, 's--', color='#ffd93d', markersize=10,
        label='Euler product prediction', linewidth=2)

ax.set_xlabel('Temperature ratio k', color='white')
ax.set_ylabel('S(kT)/S(T)', color='white')
ax.set_title('S(kT)/S(T) ≠ Euler Product', color='white')
ax.legend(fontsize=8, facecolor='#1a1a2e', edgecolor='white', labelcolor='white')
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.1)

# Panel 2: Direct sum vs Euler product
ax = axes[1]
alphas = np.linspace(0, 2, 100)
S_direct = []
S_euler = []

for alpha in alphas:
    sd = sum((1/m**3) * np.exp(-m * alpha) for m in range(1, 501))
    se = 1.0
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        factor = sum(p**(-3*k) * np.exp(-p**k * alpha) for k in range(10))
        se *= factor
    S_direct.append(sd)
    S_euler.append(se)

ax.plot(alphas, S_direct, color='#00d4ff', linewidth=2, label='Direct sum')
ax.plot(alphas, S_euler, '--', color='#ff6b6b', linewidth=2, label='Euler product attempt')
ax.set_xlabel('α (thermal parameter)', color='white')
ax.set_ylabel('Sum value', color='white')
ax.set_title('Euler Product Breaks at Finite Temperature', color='white')
ax.legend(fontsize=8, facecolor='#1a1a2e', edgecolor='white', labelcolor='white')
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.1)

plt.tight_layout()
plt.savefig('research/04_warp_drive/thermal_casimir_test.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
plt.close()

print(f"\n  Plot saved: research/04_warp_drive/thermal_casimir_test.png")
print("=" * 70)
print("  END")
print("=" * 70)
