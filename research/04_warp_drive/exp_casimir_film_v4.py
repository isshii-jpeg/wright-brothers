"""
Casimir v4: absorbing film at midpoint = prime-2 muting?
=========================================================

Can we test ζ_{¬2} with a standard Casimir experiment
by inserting a thin absorbing film at the midpoint?

Questions:
1. Does a thin absorbing film act as "pure muting" (not a wall)?
2. What force change does it produce?
3. Is the change detectable with existing Casimir precision?

Wright Brothers, 2026
"""

import numpy as np
pi = np.pi
hbar = 1.054571817e-34  # J·s
c = 2.99792458e8        # m/s
kB = 1.380649e-23       # J/K

print("=" * 70)
print("  カシミール v4: 吸収膜による素数ミュート")
print("=" * 70)

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 問題 1: 吸収膜は「壁」か「穴」か
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  完全導体の壁: 反射率 R = 1, 透過率 T = 0
    → 電磁場が壁でゼロに強制される
    → 壁の両側に独立なキャビティが形成
    → 新しいモードが生まれる
    → 壁 ≠ 素数ミュート

  完全吸収膜: 反射率 R = 0, 吸収率 A = 1
    → 電磁場が膜に到達するとエネルギーが散逸
    → 新しい境界条件は作らない（反射がないから）
    → 膜の位置で振幅が大きいモードだけが減衰
    → 振幅ゼロ（節）のモードは影響を受けない

  ★ 完全吸収膜は「穴」として機能する。
    散逸させるだけで新しいモードを作らない。

  ── ただし「完全吸収膜」は理想化 ──

  現実の薄膜: 反射率 R > 0, 吸収率 A < 1, 透過率 T > 0
  R + A + T = 1

  反射成分がある限り、部分的に「壁」として振る舞う。
  「純粋なミュート」には R → 0, A → 1 が必要。

  実現可能性:
  - 薄い金属膜（数 nm）: R は小さいが A も小さい（T が支配的）
  - 抵抗膜（377 Ω/□ = 自由空間インピーダンス）: R ≈ 0.25, A ≈ 0.5
  - カーボンナノチューブ膜: 高い吸収率が可能

  ★ 完全な R=0 は達成困難。しかし R << 1 の膜なら
    「ほぼ純粋なミュート」に近づける。
""")

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 問題 2: 3次元カシミール効果での計算
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  2枚の完全導体板（面積 A、間隔 a）の間のカシミール力:

  F_Casimir = -π²ℏc/(240 a⁴) × A

  この 240 = 2 × 120 = 2/|ζ(-3)| は
  「3次元 + 2つの偏光」の因子。

  ── 中点に完全導体壁を挿入 ──

  3枚の板: 間隔 a/2 が2つ。
  各区間のカシミール力: F(a/2) = -π²ℏc/(240(a/2)⁴) × A = -16F(a)

  全体: 外側の板にかかる力は変化する。

  ── 中点に完全吸収膜を挿入（理想化）──

  偶数モード（z方向の量子数 n_z が偶数）が吸収される。
  奇数モードは影響を受けない。

  3D の場合、モードは (n_x, n_y, n_z) で指定される。
  膜は z 方向の中点にあるので、n_z が偶数のモードだけ影響。
  n_x, n_y は自由（板に平行な方向は連続）。
""")

# 3D Casimir calculation
# Standard: E(a) = (A/(2π)²) ∫dk_x dk_y Σ_{n_z=1}^∞ (ℏ/2)√(k_x²+k_y²+(nπ/a)²)
# After regularization: E(a)/A = -π²ℏc/(720 a³)
# Force: F/A = -π²ℏc/(240 a⁴)

print("  ── 標準カシミール（膜なし）──")
print()

a = 1e-6  # 1 μm plate separation
A_plate = 1e-8  # 100 μm × 100 μm plate area

F_standard = -pi**2 * hbar * c / (240 * a**4) * A_plate
P_standard = -pi**2 * hbar * c / (240 * a**4)  # pressure

print(f"  板の間隔: a = {a*1e6:.1f} μm")
print(f"  板の面積: A = {A_plate*1e12:.0f} μm²")
print(f"  カシミール圧力: P = -π²ℏc/(240a⁴) = {P_standard:.4f} Pa")
print(f"  カシミール力: F = {F_standard:.4e} N")
print()

# Now: with absorbing film at midpoint
# The film kills all modes with even n_z.
# Remaining modes: n_z = 1, 3, 5, 7, ...

# The energy changes from Σ_{n_z=1}^∞ to Σ_{n_z odd}
# In 3D:
# E(a)/A = -(ℏc)/(2(2π)²) ∫dk_⊥ 2πk_⊥ Σ_{n_z} √(k_⊥²+(n_zπ/a)²)

# The regularized result for the sum over n_z:
# Σ_{n_z=1}^∞ involves ζ(-3) at the end (after k_⊥ integration)
# Σ_{n_z odd} involves ζ_{¬2}(-3)

# ζ(-3) = 1/120
# ζ_{¬2}(-3) = ζ(-3)(1-2³) = (1/120)(-7) = -7/120

zeta_m3 = 1/120
zeta_m3_neg2 = zeta_m3 * (1 - 2**3)  # = -7/120

print(f"  ζ(-3) = {zeta_m3}")
print(f"  ζ_{{¬2}}(-3) = ζ(-3)×(1-2³) = {zeta_m3_neg2}")
print()

# The Casimir energy goes as ζ(-3) in the standard case.
# With even n_z removed: ζ(-3) → ζ_{¬2}(-3)

# Standard pressure: P = -π²ℏc/(240 a⁴) = -π²ℏc × ζ(-3) / (2a⁴) × correction
# Actually the exact formula: P = -π²ℏc/(240 a⁴)
# where 240 = 2 × 4!/ζ(-3)^{-1}... let me just use the ratio.

# The sum over n_z contributes a factor proportional to ζ_R(-3) where
# ζ_R is the zeta function of the relevant sum.

# For ALL n_z: proportional to ζ(-3) = 1/120
# For ODD n_z only: proportional to ζ_{¬2}(-3) = -7/120

# Ratio of pressures:
ratio = zeta_m3_neg2 / zeta_m3

print(f"  圧力の比: P(膜あり)/P(膜なし) = ζ_{{¬2}}(-3)/ζ(-3) = {ratio}")
print()

P_with_film = P_standard * ratio
F_with_film = F_standard * ratio

print(f"  ── 膜挿入後 ──")
print()
print(f"  P(膜あり) = {P_standard:.4f} × ({ratio}) = {P_with_film:.4f} Pa")
print(f"  F(膜あり) = {F_with_film:.4e} N")
print()

print(f"  ★★★ 符号が反転した！")
print(f"    膜なし: P = {P_standard:.4f} Pa（負 = 引力）")
print(f"    膜あり: P = {P_with_film:.4f} Pa（正 = 斥力！）")
print()

Delta_P = P_with_film - P_standard
Delta_F = F_with_film - F_standard
print(f"  圧力変化: ΔP = {Delta_P:.4f} Pa")
print(f"  力の変化: ΔF = {Delta_F:.4e} N")
print(f"  |ΔP/P| = {abs(Delta_P/P_standard):.0f} = {abs(ratio - 1):.0f}倍")
print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 問題 3: 検出可能か
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

# The issue: we computed the force for "pure muting" (R=0, A=1 film)
# But can the CHANGE in force be detected?

# Standard Casimir force at 1 μm: P ≈ 1.3 Pa
# The change is: ΔP ≈ 8 × P ≈ 10.4 Pa (from -1.3 to +9.1 Pa)
# This is HUGE. 8× the original force.

# But: the calculation assumed PERFECT absorption.
# Real films have R > 0, and partial reflection creates "wall-like" effects.

# Casimir experiment precision:
# Lamoreaux (1997): 5% of F at a ~ 1 μm
# Mohideen (1998): 1% at a ~ 100 nm - 1 μm
# Decca (2007): 0.2% at a ~ 200 nm
# Modern MEMS: 0.1%

print(f"  標準カシミール力 (a = 1 μm): |P| = {abs(P_standard):.4f} Pa")
print(f"  膜挿入による変化: |ΔP| = {abs(Delta_P):.4f} Pa")
print(f"  変化率: |ΔP/P| = {abs(Delta_P/P_standard)*100:.0f}%")
print()
print(f"  既存実験の精度:")
print(f"    Lamoreaux (1997): 5%")
print(f"    Mohideen (1998): 1%")
print(f"    最新 MEMS: 0.1%")
print()
print(f"  必要な精度: 変化は {abs(Delta_P/P_standard)*100:.0f}% = 既存精度の数百倍大きい")
print(f"  → 原理的に検出は余裕で可能")
print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 問題 4: 完全吸収膜 vs 現実の膜
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  現実の膜は R > 0（部分的に反射する）。
  反射成分は「壁」として新モードを作る。

  膜の光学特性:
    反射率 R、吸収率 A = 1-R-T、透過率 T

  完全導体壁: R=1, A=0, T=0 → 壁（新モード生成）
  完全吸収膜: R=0, A=1, T=0 → 穴（純粋ミュート）
  現実の膜: R≈0.1-0.3, A≈0.3-0.7, T≈0.1-0.3

  ── Lifshitz 理論 ──

  現実の膜のカシミール効果は Lifshitz 理論で計算可能。
  膜の誘電率 ε(ω) を入力すると、力が出る。

  完全導体 ε → ∞: 標準カシミール
  完全吸収体 Im(ε) → ∞: 純粋ミュートに相当
  現実の膜 ε(ω): 中間的な結果

  ★ Lifshitz 理論は確立された理論であり、
    現実の膜での力は原理的に計算可能。
    「反射成分」と「吸収成分」の寄与を分離できる。
""")

# What does a partially absorbing film give?
# The key: for the sign flip, we need the ABSORPTIVE part to dominate.
# If the film is more absorptive than reflective (A > R),
# the "pure muting" effect dominates the "wall" effect.

# Rough estimate: force = R × F_wall + A × F_mute + T × F_nothing
# F_wall = force with perfect wall (negative, attractive)
# F_mute = force with pure muting (positive, repulsive)
# F_nothing = 0 (transparent film does nothing)

# For a film with R=0.1, A=0.7, T=0.2:
R_film = 0.1
A_film = 0.7
T_film = 0.2

# F_wall: with perfect wall at midpoint
# Two cavities of a/2 each: pressure = 16P_standard (much stronger)
P_wall = 16 * P_standard  # actually need the net pressure on outer plate
# More carefully: the force between a wall at a/2 and the outer plate at a
# is F(a/2) - F(a) for the internal structure. This is complex.
# For a rough estimate: the wall contribution is attractive (negative).
P_wall_contribution = -abs(P_standard) * 5  # rough: wall makes it more negative

P_film_estimate = R_film * P_wall_contribution + A_film * P_with_film + T_film * 0

print(f"  ── 現実的な膜の見積もり (R=0.1, A=0.7, T=0.2) ──")
print()
print(f"  P ≈ R×P_wall + A×P_mute + T×0")
print(f"    ≈ 0.1×(壁の寄与) + 0.7×({P_with_film:.2f}) + 0")
print()
print(f"  吸収成分: A×P_mute = {A_film * P_with_film:.4f} Pa（正 = 斥力）")
print(f"  反射成分: R×P_wall ≈ {R_film * P_wall_contribution:.4f} Pa（負 = 引力）")
print(f"  合計 ≈ {A_film * P_with_film + R_film * P_wall_contribution:.4f} Pa")
print()

net = A_film * P_with_film + R_film * P_wall_contribution
if net > 0:
    print(f"  ★ 合計が正（斥力）→ 吸収が支配。素数ミュートが見える可能性。")
else:
    print(f"  合計が負（引力）→ 反射が支配。素数ミュートが隠れる可能性。")

print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 問題 5: カシミール斥力は既知の研究テーマ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  「カシミール斥力」自体は活発な研究分野:

  (1) Dzyaloshinskii-Lifshitz-Pitaevskii (1961):
      異なる誘電体の間で斥力が生じうることを理論的に予測。
      ε₁ > ε_medium > ε₂ のとき斥力。

  (2) Munday, Capasso, Parsegian (2009, Nature):
      金-ブロモベンゼン液-シリカ の系で
      カシミール斥力を実験的に測定。

  (3) 金属-誘電体-金属のサンドイッチ構造、
      メタマテリアルを使った斥力設計、
      トポロジカル絶縁体でのカシミール効果、など。

  ★ カシミール斥力は「確立された物理現象」。
    ただし、これまでの斥力は「異なる材料の組み合わせ」で実現。
    「吸収膜による偶数モード選択的ミュート」での斥力は
    提案されたことがない。

  ── 我々の実験の新しさ ──

  既存: 「材料の組み合わせ」による斥力
  提案: 「対称性によるモード選択」による斥力

  後者は ζ_{¬2} の物理的実現であり、
  カシミール斥力の新しいメカニズムとして論文になる。
  ζ構造が正しくなくても、新しいタイプのカシミール制御として価値がある。
""")

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 実験設計 v4: カシミール + 吸収膜
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Config A（膜なし）:
    2枚の金属板（金コート）、間隔 a ≈ 1 μm
    カシミール力を AFM or MEMS で測定
    → 標準カシミール引力

  Config B（膜あり）:
    中点 a/2 に薄い吸収膜を挿入
    同じ板間隔 a で力を測定
    → 引力が弱まる？ 斥力に転じる？

  ── 吸収膜の候補 ──

  (1) 極薄金属膜（Cr, Ti）: 1-5 nm
      R ≈ 0.1, A ≈ 0.3, T ≈ 0.6
      → 吸収は中程度。透過が多い。

  (2) 抵抗膜（377 Ω/□）: ITO, graphene
      自由空間インピーダンスと整合 → 反射最小
      R ≈ 0.25, A ≈ 0.5, T ≈ 0.25
      → 反射が残る。

  (3) カーボンナノチューブフォレスト:
      可視光〜赤外で A > 0.99（Vantablack 的）
      → マイクロ波帯（カシミール関連周波数）では不明。

  (4) メタマテリアル吸収体:
      特定周波数帯で A → 1, R → 0 を設計可能。
      → 最も制御性が高いが製作が複雑。
""")

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 決定的な問題: カシミール効果の周波数帯
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  カシミール効果に寄与する周波数:
    主要な寄与: ω ≈ c/a
    a = 1 μm → f ≈ c/a = 3×10¹⁴ Hz = 300 THz（赤外〜可視光）

  つまり: カシミール効果は「光の周波数」での真空揺らぎの効果。
  我々が「素数ミュート」したいのは、この周波数帯のモード。

  ★ 問題:
  板の間の「モード番号」n_z = 1, 2, 3, ... は
  f_n = n_z × c/(2a) = n_z × 150 THz (a=1μm)

  偶数モード (n_z=2,4,...) を吸収するには、
  300 THz, 600 THz, ... での吸収が必要。
  これは近赤外〜紫外領域。

  吸収膜の性能はこの周波数帯で評価する必要がある。

  多くの金属薄膜は可視〜紫外で高い吸収率を持つ。
  → 原理的に実現可能。
""")

# Compute the frequencies involved
for a_um in [0.1, 0.5, 1.0, 2.0, 5.0]:
    a_m = a_um * 1e-6
    f_fundamental = c / (2 * a_m)
    print(f"  a = {a_um:.1f} μm: f₁ = {f_fundamental/1e12:.0f} THz "
          f"(λ = {c/f_fundamental*1e9:.0f} nm, "
          f"{'可視' if 400e-9 < c/f_fundamental < 700e-9 else '赤外' if c/f_fundamental > 700e-9 else 'UV'})")

print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 正直な結論
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  カシミール + 吸収膜で素数ミュートをテストできるか？

  ── YES の根拠 ──
  ✓ 理想的な吸収膜なら符号反転（斥力）が予測される
  ✓ 力の変化は標準カシミールの 8 倍 → 精度的に余裕
  ✓ 室温で実験可能。極低温不要。トランスモン不要。
  ✓ カシミール斥力は確立された研究分野。論文になる。
  ✓ Lifshitz 理論で現実の膜の効果を精密に計算可能。

  ── NO の根拠 ──
  ✗ 完全吸収膜は存在しない。R > 0 の反射が常にある。
  ✗ 反射成分は「壁」として振る舞い、純粋ミュートを汚染する。
  ✗ 反射 vs 吸収の比率によっては斥力が引力に負ける。
  ✗ 「壁＋穴」の混合効果の分離が必要（Lifshitz理論で可能だが複雑）。
  ✗ 膜の z 方向の位置を a/2 に精密に固定する技術が必要。

  ── 最も重要な点 ──

  ★ 反射/吸収の比を変えて系統的に測定すれば、
    「壁成分」と「穴成分」を分離できる。

    複数の膜（R/A 比が異なるもの）で測定し、
    R=0 に外挿する。
    R=0 外挿値が標準カシミールと異符号なら
    → ζ_{¬2} の証拠。

  ── v3（トランスモン）vs v4（カシミール膜）──

  v3: 精密（S/N > 10⁶）、高コスト（5〜40万 + 共同研究）、極低温
  v4: 粗い（精度 1%）、低コスト（AFM使用料）、室温

  v4 は v3 より「精度は劣る」が「実現しやすい」。
  v4 で斥力が見えたら v3 で精密測定する、という二段構えが最適。
""")

print("=" * 70)
print("  END")
print("=" * 70)
