"""
Reanalysis of Casimir Effect Data for Arithmetic Structure
============================================================

Search for prime-correlated signatures in Casimir force measurements.

The standard Casimir force between parallel plates:
  F/A = -π²ℏc/(240 d⁴)

This comes from ζ(-3) = 1/120. If the vacuum has Euler product
structure, there might be CORRECTIONS at specific plate separations
related to primes.

Approach:
  (1) Generate the theoretical Casimir spectrum with mode-by-mode
      contributions (not just the ζ-regularized total)
  (2) Look for deviations when specific modes are enhanced/suppressed
  (3) Check if published experimental residuals show prime patterns
  (4) Predict specific measurable corrections

Wright Brothers, 2026
"""

import numpy as np
import matplotlib.pyplot as plt

pi = np.pi
hbar = 1.054571817e-34
c_light = 2.99792458e8

print("=" * 70)
print("  CASIMIR DATA REANALYSIS FOR ARITHMETIC STRUCTURE")
print("=" * 70)

# ============================================================================
#  PART 1: Mode-by-mode Casimir energy
# ============================================================================

print("""
  ■ PART 1: モードごとのカシミールエネルギー

  平行平板間の真空エネルギー（1D、幅 d）:
  E(d) = (ℏc/2) × Σ_{n=1}^∞ (nπ/d)

  各モード n の寄与: E_n = ℏcnπ/(2d)

  ζ正則化: E_total = (ℏcπ/(2d)) × ζ(-1) = -ℏcπ/(24d)

  ── 素数ミュートの効果 ──

  p=2 をミュートすると偶数モードが消え:
  E_{¬2}(d) = (ℏcπ/(2d)) × ζ_{¬2}(-1) = (ℏcπ/(2d)) × (+1/12)

  差: ΔE = E_{¬2} - E = (ℏcπ/(2d)) × (1/12 - (-1/12)) = ℏcπ/(12d)

  この差は「偶数モードの寄与」そのもの。
""")

# ============================================================================
#  PART 2: Finite-N mode analysis (physical cutoff)
# ============================================================================

print("=" * 70)
print("  ■ PART 2: 有限モードでの解析")
print("=" * 70)
print()

# In a real experiment, there's a physical cutoff:
# modes with λ < λ_min (atomic scale) don't contribute.
# For plate separation d, the relevant modes are n = 1, 2, ..., N_max
# where N_max ~ d / a (a = atomic spacing ~ 0.1 nm)

def casimir_energy_finite(d, N_max):
    """Casimir energy with finite mode cutoff."""
    # E = (ℏcπ/(2d)) × Σ_{n=1}^{N_max} n
    return hbar * c_light * pi / (2 * d) * sum(range(1, N_max + 1))

def casimir_energy_coprime(d, N_max, p=2):
    """Casimir energy with p-muted modes removed."""
    return hbar * c_light * pi / (2 * d) * sum(
        n for n in range(1, N_max + 1) if n % p != 0)

def casimir_energy_zeta(d):
    """ζ-regularized Casimir energy (the physical value)."""
    return -hbar * c_light * pi / (24 * d)

# Plate separations used in actual experiments
d_values = [0.1e-6, 0.5e-6, 1e-6, 5e-6, 10e-6]  # 0.1 to 10 μm

print("  実験で使われる典型的な板間距離:")
print()
print(f"  {'d [μm]':>8s}  {'N_max':>8s}  {'E_ζ [J/m²]':>14s}  {'F_ζ/A [N/m²]':>14s}")
print(f"  {'-'*48}")

a_atomic = 0.1e-9  # atomic scale cutoff

for d in d_values:
    N_max = int(d / a_atomic)
    E_zeta = casimir_energy_zeta(d)
    F_zeta = -pi**2 * hbar * c_light / (240 * d**4)  # force per area
    print(f"  {d*1e6:>8.1f}  {N_max:>8d}  {E_zeta:>14.4e}  {F_zeta:>14.4e}")

# ============================================================================
#  PART 3: Prime-correlated corrections
# ============================================================================

print("\n" + "=" * 70)
print("  ■ PART 3: 素数相関補正の予測")
print("=" * 70)

print("""
  ── 算術的補正のメカニズム ──

  標準カシミール力: 全モードの和 → ζ(-3)
  実際の板: 完全導体ではない → モードごとの反射率 r(n, d) が異なる

  金属板の反射率はプラズマ周波数 ω_p で決まる:
  r(ω) ≈ 1 - 2ω/ω_p  (ω < ω_p)
  r(ω) ≈ 0            (ω > ω_p)

  モード n の周波数: ω_n = nπc/d
  プラズマ周波数: ω_p ~ 10¹⁶ rad/s (金の場合)

  カットオフモード: N_p = ω_p d / (πc)

  このN_pの付近で「不完全反射」によるモード選択が起きる。
  もしN_pが素数に近いとき、素数構造が力に影響する？
""")

omega_p_Au = 1.37e16  # Gold plasma frequency [rad/s]

print("  金の板に対するプラズマカットオフモード N_p:")
print()
for d in [0.1e-6, 0.5e-6, 1e-6, 2e-6, 5e-6]:
    N_p = omega_p_Au * d / (pi * c_light)
    # Is N_p near a prime?
    N_p_int = int(round(N_p))
    # Check primality
    is_prime = N_p_int > 1 and all(N_p_int % i != 0 for i in range(2, min(int(N_p_int**0.5)+1, N_p_int)))
    prime_str = "★ 素数!" if is_prime else ""
    print(f"  d = {d*1e6:.1f} μm: N_p = {N_p:.1f} (≈{N_p_int}) {prime_str}")

# ============================================================================
#  PART 4: Euler product correction to Casimir force
# ============================================================================

print("\n" + "=" * 70)
print("  ■ PART 4: オイラー積補正")
print("=" * 70)

print("""
  ── 理論的予測 ──

  完全導体のカシミール力（ζ正則化）:
    F_0/A = -π²ℏc/(240 d⁴)

  有限伝導率補正（Lifshitz理論）:
    F/A = F_0/A × (1 + δ_cond(d))

  δ_cond は板の材質と間距離に依存する既知の補正。

  ── 新しい予測: 算術的補正 ──

  もしモードの寄与がオイラー積構造を持つなら、
  各素数 p のモード（n = p, 2p, 3p, ...）は
  独立な「チャンネル」として寄与する。

  板の不完全性（有限伝導率）により、
  高次モード（大きい n）は抑制される。
  この抑制パターンが素数構造を持つ場合:

  F/A = F_0/A × ∏_p (1 - ε_p(d))

  ここで ε_p(d) は「素数 p のチャンネルの抑制率」。

  ε_p(d) ≈ exp(-p × d/d_skin)  (d_skin = スキン深さ)
""")

# Compute the arithmetic correction
d_skin_Au = c_light / omega_p_Au  # skin depth of gold

print(f"  金のスキン深さ: d_skin = c/ω_p = {d_skin_Au*1e9:.2f} nm")
print()

# For each plate separation, compute the "prime correction"
print("  素数ごとの抑制率 ε_p(d):")
print()
print(f"  {'d [μm]':>8s}", end="")
for p in [2, 3, 5, 7, 11]:
    print(f"  {'ε_'+str(p):>10s}", end="")
print(f"  {'∏(1-ε_p)':>12s}  {'補正 [%]':>10s}")
print(f"  {'-'*70}")

for d in [0.1e-6, 0.5e-6, 1e-6, 2e-6, 5e-6]:
    product = 1.0
    line = f"  {d*1e6:>8.1f}"
    for p in [2, 3, 5, 7, 11]:
        eps = np.exp(-p * d / d_skin_Au)
        product *= (1 - eps)
        line += f"  {eps:>10.6f}"
    correction_pct = (product - 1) * 100
    line += f"  {product:>12.8f}  {correction_pct:>+10.6f}"
    print(line)

print()

# ============================================================================
#  PART 5: Comparison with actual experimental data
# ============================================================================

print("=" * 70)
print("  ■ PART 5: 実験データとの比較")
print("=" * 70)

print("""
  ── 公開されている精密カシミール測定 ──

  (A) Lamoreaux (1997): 平行平板、d = 0.6-6 μm
      精度: ~5%
      → 算術的補正（~10⁻⁶ %）は検出不可能

  (B) Mohideen & Roy (1998): 球-平板、d = 0.1-0.9 μm
      精度: ~1%
      → まだ検出不可能

  (C) Decca et al. (2003): マイクロ振動子、d = 0.16-0.75 μm
      精度: ~0.5%
      → まだ不十分

  (D) Garrett et al. (2018): 精密平行平板
      精度: ~0.1%
      → まだ不十分

  ── 算術的補正の大きさ ──
""")

# The arithmetic corrections are TINY at accessible separations
# because d >> d_skin for typical experiments

for d in [0.1e-6, 1e-6, 10e-6]:
    product = 1.0
    for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
        eps = np.exp(-p * d / d_skin_Au)
        product *= (1 - eps)
    correction = abs(product - 1)
    print(f"  d = {d*1e6:>5.1f} μm: 補正 = {correction:.2e} ({correction*100:.2e}%)")

print("""
  → 算術的補正は 10⁻⁶ % 以下。
  → 現在の最高精度（~0.1%）より 4 桁以上小さい。
  → 既存データでの検出は不可能。
""")

# ============================================================================
#  PART 6: But there IS something we can look for
# ============================================================================

print("=" * 70)
print("  ■ PART 6: それでも探せるもの")
print("=" * 70)

print("""
  直接的な「素数補正」は小さすぎる。
  しかし、別の角度からカシミールデータに
  算術構造を探すことは可能。

  ── アプローチ: ζ 正則化の「正しさ」の精密検証 ──

  カシミール力の測定値は ζ(-3) = 1/120 を使った計算と一致する。
  もし代わりに ζ(-3) のオイラー積の「部分積」を使ったら？

  ζ(-3) = ∏_p (1-p³)⁻¹ = (1-8)⁻¹(1-27)⁻¹(1-125)⁻¹...

  最初の数個の素数の寄与:
""")

partial_products = []
product = 1.0
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]

print(f"  {'素数まで':>12s}  {'部分積':>16s}  {'1/120との差':>14s}  {'相対誤差':>12s}")
print(f"  {'-'*58}")

target = 1/120

for i, p in enumerate(primes):
    product *= 1.0 / (1 - p**3)
    diff = product - target
    rel_err = abs(diff / target)
    partial_products.append((p, product, diff, rel_err))
    if i < 10 or i == len(primes) - 1:
        print(f"  p ≤ {p:>4d}  {product:>16.10f}  {diff:>+14.6e}  {rel_err:>12.2e}")

print(f"\n  ζ(-3) = 1/120 = {target:.10f}")
print()

# The CONVERGENCE RATE of the Euler product tells us something
# If measurements are precise enough, the NUMBER OF PRIMES
# needed to match the data gives information about the
# arithmetic structure.

print("""
  ── 検証可能な予測 ──

  カシミール力の測定精度が向上すれば、
  「何個の素数で十分な精度が出るか」が分かる。

  現在の精度 (~0.1% = 10⁻³):
    ζ(-3) の部分積が 10⁻³ 以内に入る素数:
""")

for p, prod, diff, rel in partial_products:
    if rel < 1e-3:
        print(f"    p ≤ {p}: 相対誤差 {rel:.2e} < 10⁻³ ✓")
        break

print()
print("  将来の精度 (10⁻⁶) なら:")
for p, prod, diff, rel in partial_products:
    if rel < 1e-6:
        print(f"    p ≤ {p}: 相対誤差 {rel:.2e} < 10⁻⁶ ✓")
        break

print()
print("  → 測定精度が上がると、一致に「何個の素数が必要か」が増える")
print("  → もしオイラー積が物理的なら、精度と必要素数数の関係は")
print("     素数定理 π(N) ~ N/ln(N) に従うはず")
print()

# ============================================================================
#  PART 7: The REAL opportunity — thermal Casimir effect
# ============================================================================

print("=" * 70)
print("  ■ PART 7: 本当のチャンス — 熱カシミール効果")
print("=" * 70)

print("""
  ★ 最も有望な「0円再解析」:

  有限温度のカシミール効果には「マツバラ周波数」が現れる:
    ω_m = 2πm k_B T / ℏ  (m = 0, 1, 2, ...)

  マツバラ周波数の和はまさに離散的なモード和:
    F_thermal = (k_B T / π) Σ'_{m=0}^∞ ∫ ... (m-dependent integrand)

  この和に「素数構造」がないか調べる。

  具体的:
    Σ_m f(m) = f(0)/2 + f(1) + f(2) + f(3) + ...
  から p の倍数を除くと:
    Σ_{p∤m} f(m)

  これは温度依存カシミール力の「算術的補正」。

  ── 決定的な利点 ──

  マツバラ和は有限個（N_max ~ ℏω_p/(2πk_BT)）。
  室温 (T=300K) で金の板:
""")

k_B = 1.380649e-23
T = 300  # room temperature
N_matsubara = hbar * omega_p_Au / (2 * pi * k_B * T)
print(f"  T = {T} K:")
print(f"  N_matsubara = ℏω_p/(2πk_BT) = {N_matsubara:.0f}")
print()

# With N ~ 1700 Matsubara frequencies, the "prime structure"
# of the sum is potentially relevant

# The fraction of Matsubara frequencies that are prime:
N_mat_int = int(N_matsubara)
n_primes_mat = sum(1 for m in range(2, N_mat_int+1)
                   if all(m % i != 0 for i in range(2, min(int(m**0.5)+1, m))))
frac_prime = n_primes_mat / N_mat_int

print(f"  {N_mat_int} 個のマツバラ周波数のうち素数は {n_primes_mat} 個 ({frac_prime*100:.1f}%)")
print()

# Compute the "prime-only" thermal correction
# vs "all m" thermal sum for a specific model
print("  マツバラ和の算術的分解:")
print()

# Simple model: f(m) = 1/(m+1)^3 (simplified thermal kernel)
def thermal_sum(N, exclude_primes_of=None):
    """Sum of 1/(m+1)^3 over Matsubara modes."""
    total = 0.0
    for m in range(1, N+1):
        if exclude_primes_of is not None:
            if m % exclude_primes_of == 0:
                continue
        total += 1.0 / (m)**3
    return total

S_all = thermal_sum(N_mat_int)
S_no2 = thermal_sum(N_mat_int, exclude_primes_of=2)
S_no3 = thermal_sum(N_mat_int, exclude_primes_of=3)

print(f"  Σ_{{m=1}}^{{{N_mat_int}}} 1/m³ = {S_all:.10f}")
print(f"  ζ(3) = {1.2020569031595942:.10f}")
print(f"  差 (有限和の打ち切り誤差): {abs(S_all - 1.2020569031595942):.2e}")
print()
print(f"  p=2 を除外: Σ_{{2∤m}} 1/m³ = {S_no2:.10f}")
print(f"  予測: ζ(3)×(1-2⁻³) = {1.2020569031595942 * (1 - 1/8):.10f}")
print(f"  差: {abs(S_no2 - 1.2020569031595942*(1-1/8)):.2e}")
print()
print(f"  p=3 を除外: Σ_{{3∤m}} 1/m³ = {S_no3:.10f}")
print(f"  予測: ζ(3)×(1-3⁻³) = {1.2020569031595942 * (1 - 1/27):.10f}")
print(f"  差: {abs(S_no3 - 1.2020569031595942*(1-1/27)):.2e}")
print()

print("  → マツバラ和でもオイラー積分解が成立する ✓")
print("  → 有限温度カシミール力の精密測定で「素数チャンネル」の")
print("     個別寄与を検証可能")
print()

# The correction for excluding prime p:
# ΔF_p/F = 1 - (1-p⁻³) = p⁻³
print("  各素数チャンネルの寄与（マツバラ和から除外した場合の補正）:")
print()
for p in [2, 3, 5, 7, 11]:
    correction = 1/p**3
    print(f"  p = {p:>3d}: ΔF_p/F = 1/p³ = {correction:.6f} = {correction*100:.4f}%")

print("""
  ★ p=2 の寄与は 12.5%!
  → 現在の実験精度（0.1%）で十分検出可能
  → しかし「偶数マツバラ周波数を選択的に除外する」
    実験的方法が必要

  ── 提案: 温度変調カシミール測定 ──

  温度 T を変えるとマツバラ間隔が変わる:
    Δω_M = 2πk_BT/ℏ

  T₁ と T₂ = 2T₁ の比較:
  T₁ のマツバラ: ω, 2ω, 3ω, 4ω, 5ω, ...
  T₂ のマツバラ: 2ω, 4ω, 6ω, 8ω, 10ω, ...

  T₂ = 2T₁ では「奇数マツバラ」が消える！
  → 自然に「p=2 ミュート」が実現される！

  F(T₂)/F(T₁) の比が ζ₃×(1-2⁻³)/ζ(3) に従うか確認。
  → 温度の比を正確に制御するだけでオイラー積の検証が可能。
""")

# Compute the prediction
ratio_predicted = (1 - 1/8)  # ζ(3)(1-2⁻³)/ζ(3) for the relevant part
print(f"  予測: F_thermal(2T)/F_thermal(T) の「素数構造」成分:")
print(f"    = (1 - 2⁻³) = {1-1/8:.6f} = 87.5%")
print(f"    → 温度を2倍にすると熱的カシミール力の")
print(f"      「素数チャンネル p=2」寄与が消え、12.5% の差が出る")
print()
print("  これは実験的に測定可能な量か？")
print(f"    精度 0.1% のカシミール測定で: 12.5% の差は 125σ の有意性")
print(f"    → 圧倒的に検出可能!")
print()

print("=" * 70)
print("  ■ CONCLUSION")
print("=" * 70)

print("""
  ── 結果のまとめ ──

  (1) 直接的な「素数補正」(金属板の有限伝導率に起因):
      ~10⁻⁶ % → 現在の精度では検出不可能。

  (2) オイラー積の収束速度:
      精度が上がると必要な素数数が増える → 原理的に検証可能だが、
      現在の精度では区別がつかない。

  (3) ★ 熱カシミール効果のマツバラ周波数:
      温度を2倍にすると奇数マツバラが消える = p=2 ミュート!
      予測: 12.5% の力の差 → 現在の精度で 125σ で検出可能!

  ── 0円で今すぐできること ──

  既存の「温度依存カシミール力」の公開データを探し、
  T と 2T での測定比較で「12.5% のオイラー積構造」が
  見えるか確認する。

  候補データ: Sushkov et al. (2011), Klimchitskaya & Mostepanenko (2020)
  の温度依存カシミール測定。

  ── 正直な注意 ──

  温度を2倍にした時のカシミール力の差は、
  標準の Lifshitz 理論でも計算される。
  差が「ζ(3)×(1-2⁻³)/ζ(3) = 87.5%」に従うことは
  標準理論の帰結でもある（マツバラ和の性質として）。

  つまり: この予測は「Spec(Z) 固有」ではなく、
  標準理論と区別できない可能性がある。

  ★ 真に区別可能な予測:
  温度を T と 3T で比較 → p=3 チャンネルの検証
  T と 5T → p=5 チャンネル
  複数の温度比で同時にオイラー積の乗法構造を検証すれば、
  「個々の予測は標準理論と同じ」だが
  「全体のパターン（乗法性）が一致するか」で区別可能。
""")

# ============================================================================
#  Visualization
# ============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.patch.set_facecolor('#0a0a1a')
fig.suptitle('Casimir Effect Reanalysis for Arithmetic Structure',
             fontsize=14, fontweight='bold', color='#ffd93d')

# Panel 1: Euler product convergence
ax = axes[0, 0]
pp = [x[0] for x in partial_products]
products = [x[1] for x in partial_products]
ax.plot(pp, products, 'o-', color='#ffd93d', markersize=6)
ax.axhline(y=target, color='#6bff8d', linewidth=2, linestyle='--',
           label=f'ζ(-3) = 1/120 = {target:.6f}')
ax.set_xlabel('Largest prime in partial product', color='white')
ax.set_ylabel('Partial Euler product', color='white')
ax.set_title('Euler Product Convergence to ζ(-3)', color='white')
ax.legend(fontsize=8, facecolor='#1a1a2e', edgecolor='white', labelcolor='white')
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.1)

# Panel 2: Prime channel contributions
ax = axes[0, 1]
p_vals = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
contributions = [1/p**3 for p in p_vals]
ax.bar(range(len(p_vals)), [c*100 for c in contributions],
       color='#ff6b6b', alpha=0.8)
ax.set_xticks(range(len(p_vals)))
ax.set_xticklabels([f'p={p}' for p in p_vals], color='white', fontsize=8)
ax.set_ylabel('Channel contribution (%)', color='white')
ax.set_title('Each Prime Channel\'s Contribution to F', color='white')
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.1)
ax.axhline(y=0.1, color='#ffd93d', linewidth=1, linestyle='--',
           label='Current precision (0.1%)')
ax.legend(fontsize=8, facecolor='#1a1a2e', edgecolor='white', labelcolor='white')

# Panel 3: Matsubara sum decomposition
ax = axes[1, 0]
m_values = range(1, 50)
f_all = [1/m**3 for m in m_values]
f_odd = [1/m**3 if m % 2 != 0 else 0 for m in m_values]
f_even = [1/m**3 if m % 2 == 0 else 0 for m in m_values]

ax.bar(m_values, f_all, color='#00d4ff', alpha=0.5, label='All m')
ax.bar(m_values, f_even, color='#ff6b6b', alpha=0.7, label='Even m (p=2)')
ax.set_xlabel('Matsubara index m', color='white')
ax.set_ylabel('1/m³ contribution', color='white')
ax.set_title('Matsubara Sum: All vs Even (p=2 channel)', color='white')
ax.legend(fontsize=8, facecolor='#1a1a2e', edgecolor='white', labelcolor='white')
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')

# Panel 4: Temperature ratio prediction
ax = axes[1, 1]
T_ratios = [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0]
# For each T ratio k, the "removed" Matsubara fraction is
# the fraction of integers ≤ N that are divisible by k
removed_frac = []
for k in T_ratios:
    if k == 1:
        removed_frac.append(0)
    else:
        k_int = int(k)
        # At temperature kT, only multiples of k contribute
        # So non-multiples are "removed"
        frac = 1 - 1/k_int  # fraction of modes removed
        removed_frac.append(frac)

ax.plot(T_ratios, [r*100 for r in removed_frac], 'o-',
        color='#6bff8d', markersize=8)
ax.set_xlabel('Temperature ratio T₂/T₁', color='white')
ax.set_ylabel('Modes "muted" (%)', color='white')
ax.set_title('Temperature Modulation → Natural Prime Muting', color='white')
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.1)

# Annotate
ax.annotate('T₂=2T₁: p=2 mute\n(12.5% in ζ(3))',
            xy=(2, 50), xytext=(3, 60), color='#ffd93d',
            arrowprops=dict(arrowstyle='->', color='#ffd93d'), fontsize=9)

plt.tight_layout()
plt.savefig('research/04_warp_drive/casimir_reanalysis.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
plt.close()

print(f"\n  Plot saved: research/04_warp_drive/casimir_reanalysis.png")
print("=" * 70)
print("  END")
print("=" * 70)
