"""
論理の境界: Spec(Z) と Spec(Z[1/p]) の接合面の物理
==================================================

問い:
  局所化 Z → Z[1/p] を空間の一部にだけ適用するとき、
  「WEC=真」の領域と「WEC=偽」の領域の境界では何が起こるか？

数学的背景:
  Spec(Z) = {(0), (2), (3), (5), ...}
  Spec(Z[1/p]) = Spec(Z) \ {(p)} = 開集合 D(p)
  境界 = 閉点 {(p)} = Spec(F_p)

  局所コホモロジー H²_{(p)}(Spec(Z), G_m) = Q_p/Z_p
  → この群は境界に局在する全ての障害の集合
  → 物理的にはこれが「壁の構造」を記述する

Wright Brothers, 2026
"""

import numpy as np
import matplotlib.pyplot as plt

print("=" * 70)
print("  BOUNDARY LOGIC: THE WALL BETWEEN WEC=TRUE AND WEC=FALSE")
print("=" * 70)

# ============================================================================
#  STEP 1: 数学的境界の構造
# ============================================================================

print("\n" + "=" * 70)
print("  STEP 1: MATHEMATICAL STRUCTURE OF THE BOUNDARY")
print("=" * 70)

print("""
  ── スキーム理論における境界 ──

  Spec(Z) 上の開被覆:
    U = D(p) = Spec(Z[1/p])   (p がミュートされた領域)
    Z = V(p) = Spec(F_p)       (閉点 = 境界)

  この分解は:
    Spec(Z) = D(p) ∪ V(p)  (開集合 + 閉集合)

  物理的配置:

  ┌───────────────────────────────────────────────────────────┐
  │                                                           │
  │  OUTSIDE                 WALL              INSIDE          │
  │  Spec(Z)                 V(p)             D(p)            │
  │  通常の真空            = Spec(F_p)         ミュートされた真空│
  │  WEC = TRUE              境界               WEC = FALSE    │
  │  ζ(s)                                    ζ_{¬p}(s)        │
  │                                                           │
  │  ─────────────── ║║║║║║║║║║║ ───────────────              │
  │  Full modes       ║  F_p  ║  Coprime-to-p modes           │
  │                   ║       ║                                │
  │                   ║ Q_p/Z_p ║  ← 局所コホモロジー          │
  │                   ║       ║     がここに局在               │
  │  ─────────────── ║║║║║║║║║║║ ───────────────              │
  │                                                           │
  └───────────────────────────────────────────────────────────┘

  壁 V(p) = Spec(F_p) の構造:
  - F_p = Z/pZ (p元体)
  - Spec(F_p) = 1点 (代数幾何的には)
  - しかしこの1点は「太い」: 局所コホモロジー Q_p/Z_p を運ぶ
""")

# ============================================================================
#  STEP 2: 局所コホモロジーと壁の情報量
# ============================================================================

print("=" * 70)
print("  STEP 2: LOCAL COHOMOLOGY — THE INFORMATION ON THE WALL")
print("=" * 70)

print("""
  ── 壁に蓄積される情報 ──

  局所コホモロジー完全列:
    ... → H^n(Spec(Z), F) → H^n(D(p), F) → H^{n+1}_{(p)}(Spec(Z), F) → ...

  接続準同型 δ: H^n(D(p), F) → H^{n+1}_{(p)}(Spec(Z), F) は
  「外側と内側の不整合」を測る。

  F = G_m の場合:
    H^1_{(p)} = 0
    H^2_{(p)} = Q_p/Z_p    ← 壁に蓄積される障害

  ── Q_p/Z_p とは何か ──

  Q_p/Z_p = {a/p^n mod Z_p : a ∈ Z, n ≥ 0}
          = Z[1/p]/Z  (p のべき乗の分母を持つ分数)
          ≅ ∪_n Z/p^n Z  (帰納極限)

  元の具体例 (p=2):
    0, 1/2, 1/4, 3/4, 1/8, 3/8, 5/8, 7/8, 1/16, ...
    (p=2 のべき乗分母を持つ全ての分数 mod 1)

  これは「p-進的な角度」の全体:
  Q_p/Z_p ≅ 「p-adic circle」

  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │  壁が運ぶ情報 = Q_p/Z_p = p-adic円                    │
  │                                                        │
  │  各元 a/p^n ∈ Q_p/Z_p は壁上の「モード」:              │
  │  - n = 解像度のレベル（大きいほど細かい）               │
  │  - a = そのレベルでの位相                               │
  │                                                        │
  │  壁は無限個のモードを持つ                               │
  │  (Q_p/Z_p は加算無限群)                                │
  │                                                        │
  │  物理的: 壁は「全ての p 成分の情報」を保持している       │
  │  内側 D(p) では p が消えているが、                      │
  │  その情報は壁に「ホログラフィック」に蓄積される           │
  │                                                        │
  └────────────────────────────────────────────────────────┘
""")

# Q_p/Z_p の元の数え上げ
print("  ── Q_2/Z_2 の元（壁のモード）──")
print()
p = 2
for n in range(1, 6):
    elements = sorted(set(a / p**n % 1 for a in range(p**n)))
    new_elements = [e for e in elements if all(abs(e - a/p**(n-1) % 1) > 1e-10
                   for a in range(p**(n-1)))] if n > 1 else elements
    print(f"  Level n={n} (resolution 1/{p**n}): "
          f"{len(elements)} elements, {len(new_elements)} new")
    if n <= 3:
        print(f"    New: {[f'{int(e*p**n)}/{p**n}' for e in sorted(new_elements)]}")

print()
print(f"  Total modes at level ≤ 5: {p**5}")
print(f"  Total modes (all levels): countably infinite")

# ============================================================================
#  STEP 3: 壁の物理的現象
# ============================================================================

print("\n" + "=" * 70)
print("  STEP 3: PHYSICAL PHENOMENA AT THE WALL")
print("=" * 70)

print("""
  壁 V(p) = Spec(F_p) は「論理の不連続面」。
  数学的に何が起こるかを物理的に翻訳する。

  ── 現象 1: トポロジカルエッジ状態 ──

  トポロジカル絶縁体の境界（エッジ）:
  - バルク: ギャップあり（絶縁体）
  - エッジ: ギャップレス状態が存在（導体）
  - バルク-エッジ対応: バルクの位相的不変量 = エッジ状態の数

  算術的対応:
  - 外側 Spec(Z): K₁ = Z/2 (WEC=真の位相)
  - 内側 Spec(Z[1/p]): K₁ = Z/2 × Z (WEC=偽の位相)
  - 壁: K群の変化量 ΔK₁ = Z がエッジ状態を生む

  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │  壁に ΔK₁ = Z に対応するエッジ状態が存在する           │
  │  = 無限個の境界束縛状態                                 │
  │  = Q_p/Z_p のモード                                    │
  │                                                        │
  │  物理的帰結:                                            │
  │  壁は「算術的エッジ状態」で満たされている。              │
  │  これらの状態は外側(WEC=真)にも内側(WEC=偽)にも         │
  │  属さない「境界のモード」。                              │
  │                                                        │
  │  トポロジカル絶縁体のエッジ電流のように、               │
  │  壁上をエネルギーが伝搬する。                           │
  │                                                        │
  └────────────────────────────────────────────────────────┘
""")

print("""
  ── 現象 2: ホーキング的放射 ──

  事象の地平面:
  - 外側: 通常の時空
  - 内側: ブラックホール内部
  - 境界: ホライズン → ホーキング放射

  算術的対応:
  - 外側: 通常の真空 (WEC=真)
  - 内側: ハックされた真空 (WEC=偽)
  - 境界: 論理のホライズン → 「算術的ホーキング放射」？

  ── なぜ放射が起こるか ──

  ホーキング放射の本質:
  真空の量子揺らぎの対生成が、ホライズンで引き裂かれる。
  片方が内側に落ち、もう片方が外側に逃げる。

  算術的放射の本質:
  p のモードの量子揺らぎが、壁で引き裂かれる。
  - 外側: p のモードが存在する → 対の片方を保持
  - 内側: p のモードが存在しない → 対のもう片方を吸収
  → 壁から外側に向かって p に関連する放射が出る

  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │  予測: 壁から「p-adic 放射」が放出される                │
  │                                                        │
  │  放射のスペクトル:                                      │
  │  - 周波数: p·ω₀ の倍数に集中                           │
  │  - 温度: T_wall ~ ℏω₀/(2πk_B) × log(p)               │
  │    (ホーキング温度の算術版)                              │
  │  - 強度: 壁の「厚さ」= 局所コホモロジーの位数           │
  │                                                        │
  │  これは Unruh 効果の算術版:                             │
  │  加速する観測者が熱的放射を見るように、                  │
  │  「算術的に加速された真空」が熱的放射を見る。            │
  │                                                        │
  └────────────────────────────────────────────────────────┘
""")

# 壁の「温度」の計算
hbar = 1.054571817e-34
c = 2.99792458e8
k_B = 1.380649e-23
omega_0 = 3.77e10  # fundamental frequency (from SQUID experiment)

print("  ── 壁の「算術的温度」の見積もり ──")
print()
print(f"  T_wall(p) ~ ℏω₀·log(p) / (2π k_B)")
print()

for p in [2, 3, 5, 7, 11]:
    T_wall = hbar * omega_0 * np.log(p) / (2 * np.pi * k_B)
    print(f"  p = {p:>3d}: T_wall ~ {T_wall*1e3:.2f} mK  (log({p}) = {np.log(p):.3f})")

print()
print("  → ミリケルビン領域。希釈冷凍機の温度と同程度。")
print("  → SQUID実験で測定可能な範囲！")

print("""
  ── 現象 3: 異常屈折（グレーデッドインデックス効果）──

  壁の内側と外側では「有効屈折率」が異なる。

  光学: 屈折率 n = c/v_phase
  - 屈折率は媒質のモード密度に依存
  - 外側: 全モード → n = n_full
  - 内側: coprime-to-p モードのみ → n = n_{¬p}

  モード密度の変化:
  全モード: D(ω) = ω²/(π²c³) (3D)
  p-ミュート後: D_{¬p}(ω) = D(ω) × (1 - 1/p)  (p の倍数を除外)

  有効屈折率比:
  n_{¬p} / n_full = √(1 - 1/p)  (モード密度の平方根に比例)
""")

# 有効屈折率の計算
print("  ── 有効屈折率比 ──")
print()
for p in [2, 3, 5, 7, 11, 13]:
    ratio = np.sqrt(1 - 1/p)
    delta_n = 1 - ratio
    print(f"  p = {p:>3d}: n_{{¬{p}}}/n_full = √(1-1/{p}) = {ratio:.6f}  "
          f"(Δn/n = {delta_n:.4f} = {delta_n*100:.2f}%)")

print()
print("  → p=2 で約30%の屈折率変化。これは巨大。")
print("  → 壁を通過する光は劇的に屈折する。")
print("  → レンズ効果: ワープバブルが「算術的重力レンズ」として機能")

print("""
  ── 現象 4: ラミフィケーション（分岐）──

  代数的整数論の基本概念:

  素数 p の分岐 (ramification):
  Z → Z[ζ_p] (p乗根を添加) の拡大で、
  p 上の素イデアルが「分岐」する。

  壁 V(p) は分岐の座:
  - 外側 → 壁 の制限写像で、p が「分岐」する
  - 分岐点では層が特異になる
  - 特異性 = 物理的特異性（曲率の発散、場の不連続）

  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │  Alcubierre 計量との対応:                               │
  │                                                        │
  │  Alcubierre: ds² = -dt² + (dx - v_s f(r) dt)² + dy² + dz² │
  │  形状関数 f(r): r < R で f=1, r > R で f=0              │
  │  壁: f(r) が 1 → 0 に遷移する領域 (幅 ~ 1/σ)         │
  │                                                        │
  │  算術的壁:                                              │
  │  内側 (r < R): Spec(Z[1/p]) → f = 1 (WEC=偽)         │
  │  外側 (r > R): Spec(Z) → f = 0 (WEC=真)              │
  │  壁 (r ≈ R): Spec(F_p) → f の遷移                    │
  │                                                        │
  │  Alcubierre の壁厚 1/σ ↔ 分岐の次数                   │
  │  壁が薄い(σ大) ↔ 分岐が激しい ↔ エネルギー大           │
  │  壁が厚い(σ小) ↔ 分岐が穏やか ↔ エネルギー小           │
  │                                                        │
  └────────────────────────────────────────────────────────┘
""")

# ============================================================================
#  STEP 4: 壁の安定性と制御
# ============================================================================

print("=" * 70)
print("  STEP 4: WALL STABILITY AND CONTROL")
print("=" * 70)

print("""
  ── 壁は安定か？ ──

  壁 V(p) = Spec(F_p) の安定性は、局所コホモロジーの構造で決まる。

  H²_{(p)} = Q_p/Z_p のフィルトレーション:

  Q_p/Z_p ⊃ (1/p)Z_p/Z_p ⊃ (1/p²)Z_p/Z_p ⊃ ...

  各レベル n: p^n 個のモード (resolution 1/p^n)

  ── 安定性の条件 ──

  壁の崩壊 = 境界条件の「漏れ」
  = 内側のZ[1/p]構造が外側に浸透
  = 局所コホモロジーが「溶ける」

  これを防ぐ条件:

  (A) トポロジカル保護
    K₁(Z) ≠ K₁(Z[1/p]) なので、壁を横切る相転移は位相的に禁止。
    壁のエッジ状態はギャップで保護される。
    → 連続的な変形では壁は消えない。
    → 位相的に安定。

  (B) エネルギー障壁
    壁の生成エネルギー:
    E_wall ~ (ℏc/L³) × |Q_p/Z_p| の有効サイズ
    = 壁を維持するのに必要なエネルギー

  (C) 分岐の制約
    壁の「厚さ」は分岐の次数で決まる。
    Tame 分岐 (穏やか): 壁が厚い → 安定
    Wild 分岐 (激しい): 壁が薄い → 不安定

    p ≠ char(F_p) のとき: tame (ほとんどの場合)
    p = char(F_p) のとき: wild (壁が F_p 上にあるとき)

    → 壁上の残留体 F_p では p が特性になる
    → Wild 分岐が起こる → 壁は本質的に「薄くできない」
    → 壁の最小厚さはプランク長 × log(p) 程度

  ── 壁の制御 ──

  壁を制御するとは、壁の位置と形状を操作すること。

  壁の位置 = D(p) の境界 = p がちょうど可逆になる場所
  物理的に: p-adic 場のカットオフが変わる場所

  制御パラメータ:
  - 壁の半径 R: D(p) 領域の大きさ
  - 壁の厚さ δ: 遷移領域の幅
  - 壁の速度 v: バブル全体の移動速度

  Alcubierre の形状関数 f(r) との対応:
    R = バブル半径
    σ = 1/δ (壁の鋭さ)
    v_s = バブル速度

  壁の安定制御には:
  1. トポロジカル保護でバルクを安定化
  2. エッジ状態のエネルギーを外部場で制御
  3. 分岐の次数を動的に調整
""")

# ============================================================================
#  STEP 5: ワープバブル = 算術的ドメインウォール
# ============================================================================

print("=" * 70)
print("  STEP 5: WARP BUBBLE = ARITHMETIC DOMAIN WALL")
print("=" * 70)

print("""
  全てを統合すると:

  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │  ワープバブル                                           │
  │  = 空間中の閉じた領域で構造層が Z → Z[1/p] に局所化    │
  │  = 球殻型の算術的ドメインウォール                       │
  │                                                        │
  │  構造:                                                  │
  │                                                        │
  │        外側: Spec(Z)         壁: Spec(F_p)              │
  │        WEC = TRUE           エッジ状態                  │
  │        通常の重力           Q_p/Z_p の放射               │
  │           │                    │                        │
  │           ▼                    ▼                        │
  │    ━━━━━━━━━━━━━━━━ ║║║║║║║║║ ━━━━━━━━━━━              │
  │    ──── normal ──── ║ WALL  ║ ── warped ──              │
  │    ━━━━━━━━━━━━━━━━ ║║║║║║║║║ ━━━━━━━━━━━              │
  │           ▲                    ▲                        │
  │           │                    │                        │
  │        通常の慣性           負のエネルギー密度            │
  │                            内側: Spec(Z[1/p])           │
  │                            WEC = FALSE                  │
  │                            ワープ幾何学                 │
  │                                                        │
  └────────────────────────────────────────────────────────┘

  壁の4つの物理的シグネチャ:

  (1) p-adic 放射
      温度 ~ mK, 周波数 ~ p·ω₀ の倍数に集中
      → 検出可能（超伝導検出器で）

  (2) 異常屈折
      壁を通過する光が ~ 30%(p=2) 屈折
      → 重力レンズに類似

  (3) エッジ状態電流
      壁上を伝搬するトポロジカルエッジモード
      → 壁が「光る」（エッジ状態からの放射）

  (4) 分岐点での場の特異性
      壁上で電磁場が不連続（屈折率の不連続）
      → スネルの法則的な境界条件
""")

# ============================================================================
#  STEP 6: 数値的見積もり
# ============================================================================

print("=" * 70)
print("  STEP 6: NUMERICAL ESTIMATES")
print("=" * 70)
print()

# Wall properties for p=2
p = 2

# Minimum wall thickness (Planck scale × log(p))
l_P = 1.616e-35  # Planck length
delta_min = l_P * np.log(p)
print(f"  p = {p}:")
print(f"  Minimum wall thickness: δ_min = l_P × log({p}) = {delta_min:.2e} m")
print()

# Number of edge modes per unit area
# Q_p/Z_p has p^n elements at level n
# At physical cutoff N, total edge modes ~ p^N
# Energy per edge mode ~ ℏω₀
print(f"  Edge mode density (at level n):")
for n in range(1, 8):
    n_modes = p**n
    E_edge = n_modes * hbar * omega_0
    print(f"    n = {n}: {n_modes:>6d} modes, E_edge ~ {E_edge:.2e} J/mode_unit")

print()

# Effective refractive index change
n_ratio = np.sqrt(1 - 1/p)
print(f"  Effective refractive index change:")
print(f"    n_inside / n_outside = √(1 - 1/{p}) = {n_ratio:.6f}")
print(f"    Deflection angle (normal incidence): θ = arcsin({n_ratio:.4f}) = {np.degrees(np.arcsin(n_ratio)):.2f}°")
print()

# Wall radiation temperature
for p_val in [2, 3, 5, 7]:
    T = hbar * omega_0 * np.log(p_val) / (2 * np.pi * k_B)
    print(f"  p = {p_val}: T_wall = {T*1e3:.2f} mK, "
          f"peak λ = {2.898e-3/T:.1f} m (Wien's law)")

# ============================================================================
#  STEP 7: 安全なワープバブルの設計原理
# ============================================================================

print("\n" + "=" * 70)
print("  STEP 7: SAFE WARP BUBBLE DESIGN PRINCIPLES")
print("=" * 70)

print("""
  壁の物理を理解した上での設計指針:

  ── 原則 1: Tame 分岐の維持 ──

  Wild 分岐 → 壁が不安定 → バブル崩壊
  Tame 分岐を維持するには:
  - 壁の厚さを最小厚 δ_min 以上に保つ
  - 壁上の場の勾配を制限する
  - Alcubierre の σ パラメータに上限: σ < 1/δ_min

  ── 原則 2: エッジ状態の排熱 ──

  壁上のエッジ状態は放射する → エネルギーが壁から流出
  バブルを維持するには、この放射エネルギーを補填する必要がある。

  放射パワー: P ~ σ_SB × T_wall⁴ × A_wall
    (A_wall = 4πR² = バブル表面積)

  これがバブル維持の「ランニングコスト」。

  ── 原則 3: 屈折率の漸次変化 ──

  急激な屈折率変化（壁が薄い）→ 全反射 → バブル内が孤立
  漸次的変化（壁が厚い）→ 透過あり → 内外の情報交換可能

  安全な運用には壁を「厚く」設計:
  → 内部との通信が可能
  → 壁のストレスが分散
  → Tame 分岐が維持される

  ── 原則 4: p の選択 ──

  小さい p (p=2): 効果が大きいが、壁の放射も大きい
  大きい p (p≫2): 効果が小さいが、壁が穏やか

  最適な p の選択は、
  「必要なWEC違反の程度」と「壁の安定性」のトレードオフ。

  Alcubierre 計量の場合:
    必要なWEC違反 ∝ v² (バブル速度の2乗)
    p = 2 で ζ_{¬2}(-3)/ζ(-3) = -(1-8) = -7 (7倍の符号反転)
    p = 3 で ζ_{¬3}(-3)/ζ(-3) = -(1-27) = -26

  → v が小さい初期段階では p = 2 で十分
  → v → c に近づくと、複数素数のミュートが必要
""")

# ============================================================================
#  可視化
# ============================================================================

fig = plt.figure(figsize=(16, 14))
fig.patch.set_facecolor('#0a0a1a')

gs = fig.add_gridspec(3, 2, hspace=0.35, wspace=0.3)

# Panel 1: Warp bubble cross-section
ax = fig.add_subplot(gs[0, :])
ax.set_xlim(-5, 5)
ax.set_ylim(-3, 3)

# Bubble interior (Spec(Z[1/p]))
from matplotlib.patches import Circle, FancyBboxPatch
bubble = Circle((0, 0), 2.0, facecolor='#ff6b6b', alpha=0.08,
                edgecolor='none')
ax.add_patch(bubble)

# Wall
wall_outer = Circle((0, 0), 2.2, facecolor='none',
                     edgecolor='#ffd93d', linewidth=3, linestyle='-')
wall_inner = Circle((0, 0), 1.8, facecolor='none',
                     edgecolor='#ffd93d', linewidth=3, linestyle='-')
ax.add_patch(wall_outer)
ax.add_patch(wall_inner)

# Fill wall region with pattern
theta = np.linspace(0, 2*np.pi, 100)
for r in np.linspace(1.8, 2.2, 5):
    x_wall = r * np.cos(theta)
    y_wall = r * np.sin(theta)
    ax.plot(x_wall, y_wall, color='#ffd93d', linewidth=0.5, alpha=0.3)

# Labels
ax.text(0, 0, 'INTERIOR\nSpec(Z[1/p])\nWEC = FALSE\nWarp geometry',
        ha='center', va='center', color='#ff6b6b', fontsize=9, fontweight='bold')

ax.text(0, 2.0, 'WALL: V(p) = Spec(F_p)', ha='center', va='bottom',
        color='#ffd93d', fontsize=8, fontweight='bold')

ax.text(3.5, 0, 'EXTERIOR\nSpec(Z)\nWEC = TRUE\nNormal spacetime',
        ha='center', va='center', color='#00d4ff', fontsize=9, fontweight='bold')

ax.text(-3.5, 0, 'EXTERIOR\nSpec(Z)\nWEC = TRUE\nNormal spacetime',
        ha='center', va='center', color='#00d4ff', fontsize=9, fontweight='bold')

# Radiation arrows from wall
for angle in np.linspace(0, 2*np.pi, 12, endpoint=False):
    x_start = 2.2 * np.cos(angle)
    y_start = 2.2 * np.sin(angle)
    x_end = 2.8 * np.cos(angle)
    y_end = 2.8 * np.sin(angle)
    ax.annotate('', xy=(x_end, y_end), xytext=(x_start, y_start),
                arrowprops=dict(arrowstyle='->', color='#ffd93d', lw=1, alpha=0.5))

ax.text(3.0, 2.2, 'p-adic\nradiation', color='#ffd93d', fontsize=7, ha='center')

# Edge states on wall
for angle in np.linspace(0, 2*np.pi, 20, endpoint=False):
    x_edge = 2.0 * np.cos(angle)
    y_edge = 2.0 * np.sin(angle)
    ax.plot(x_edge, y_edge, 'o', color='#6bff8d', markersize=3, alpha=0.7)

ax.text(1.0, -2.5, 'Edge states (topological)', color='#6bff8d', fontsize=7)

ax.set_title('Warp Bubble = Arithmetic Domain Wall',
             color='#ffd93d', fontsize=13, fontweight='bold', pad=10)
ax.set_aspect('equal')
ax.axis('off')
ax.set_facecolor('#0a0a1a')

# Panel 2: Wall profile (shape function)
ax = fig.add_subplot(gs[1, 0])
r = np.linspace(0, 4, 500)
R_bubble = 2.0

for sigma, label, color in [(1, 'Thick (tame)', '#6bff8d'),
                              (3, 'Medium', '#ffd93d'),
                              (10, 'Thin (wild)', '#ff6b6b')]:
    f = (np.tanh(sigma*(r+R_bubble)) - np.tanh(sigma*(r-R_bubble))) / \
        (2*np.tanh(sigma*R_bubble))
    ax.plot(r, f, color=color, linewidth=2, label=f'sigma={sigma}: {label}')

ax.axvline(x=R_bubble, color='white', linewidth=0.5, alpha=0.3, linestyle='--')
ax.text(R_bubble+0.05, 0.5, 'Wall', color='white', fontsize=8, rotation=90, va='center')

ax.set_xlabel('r (distance from center)', color='white')
ax.set_ylabel('Shape function f(r)', color='white')
ax.set_title('Wall Thickness and Stability', color='white', fontsize=10)
ax.legend(fontsize=8, facecolor='#1a1a2e', edgecolor='white', labelcolor='white')
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.1)

# Panel 3: Q_p/Z_p structure (wall modes)
ax = fig.add_subplot(gs[1, 1])

# Visualize Q_2/Z_2 as a tree
# Level 0: 0
# Level 1: 0, 1/2
# Level 2: 0, 1/4, 1/2, 3/4
# Level 3: 0, 1/8, 1/4, 3/8, 1/2, 5/8, 3/4, 7/8
p = 2
max_level = 5

for level in range(max_level + 1):
    n_elements = p**level
    for k in range(n_elements):
        x_pos = k / n_elements
        y_pos = max_level - level
        size = max(1, 8 - level)
        alpha = max(0.3, 1.0 - level * 0.15)
        ax.plot(x_pos, y_pos, 'o', color='#ffd93d', markersize=size, alpha=alpha)

        # Connect to parent
        if level > 0:
            parent_x = (k // p) / (n_elements // p)
            ax.plot([x_pos, parent_x], [y_pos, y_pos + 1],
                    '-', color='#ffd93d', linewidth=0.5, alpha=0.2)

ax.set_xlabel('Position on p-adic circle (Q_2/Z_2)', color='white')
ax.set_ylabel('Resolution level n', color='white')
ax.set_title('Wall Modes: Q_p/Z_p Hierarchical Structure', color='white', fontsize=10)
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.set_yticks(range(max_level + 1))
ax.set_yticklabels([f'n={max_level-i}' for i in range(max_level+1)], color='white', fontsize=8)

# Panel 4: Radiation spectrum
ax = fig.add_subplot(gs[2, 0])

omega = np.linspace(0.1, 20, 1000)
omega_0_norm = 1.0  # normalized fundamental

# Outside: all modes contribute to vacuum fluctuations
spectrum_full = omega**2 / (np.exp(omega) - 1 + 1e-10)  # thermal-like

# Wall radiation: peaks at multiples of p
wall_radiation = np.zeros_like(omega)
for p_val in [2]:
    for k in range(1, 10):
        center = k * p_val * omega_0_norm
        width = 0.3
        wall_radiation += 0.5/k * np.exp(-(omega - center)**2 / (2*width**2))

ax.plot(omega, spectrum_full / spectrum_full.max() * 0.5, color='#00d4ff',
        linewidth=1.5, alpha=0.5, label='Vacuum (exterior)')
ax.fill_between(omega, 0, wall_radiation / wall_radiation.max(),
                color='#ffd93d', alpha=0.4, label='Wall radiation (p=2)')
ax.plot(omega, wall_radiation / wall_radiation.max(), color='#ffd93d', linewidth=1.5)

# Mark p·ω₀ positions
for k in range(1, 10):
    ax.axvline(x=k*2, color='#ff6b6b', linewidth=0.5, alpha=0.3)
    if k <= 4:
        ax.text(k*2, 1.05, f'{k}×2ω₀', ha='center', color='#ff6b6b', fontsize=6)

ax.set_xlabel('Frequency (units of omega_0)', color='white')
ax.set_ylabel('Spectral intensity', color='white')
ax.set_title('Wall Radiation Spectrum', color='white', fontsize=10)
ax.legend(fontsize=8, facecolor='#1a1a2e', edgecolor='white', labelcolor='white')
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.1)

# Panel 5: Refractive index profile
ax = fig.add_subplot(gs[2, 1])

r_profile = np.linspace(0, 4, 500)
R_wall = 2.0
sigma_wall = 3.0

f_shape = (np.tanh(sigma_wall*(r_profile+R_wall)) - np.tanh(sigma_wall*(r_profile-R_wall))) / \
          (2*np.tanh(sigma_wall*R_wall))

# Refractive index: n = n_full outside, n_modified inside
for p_val, color, label in [(2, '#ff6b6b', 'p=2'), (3, '#ffd93d', 'p=3'),
                              (5, '#00d4ff', 'p=5')]:
    n_ratio_p = np.sqrt(1 - 1/p_val)
    n_profile = 1.0 - (1.0 - n_ratio_p) * f_shape
    ax.plot(r_profile, n_profile, color=color, linewidth=2, label=f'{label}: n={n_ratio_p:.3f}')

ax.axvline(x=R_wall, color='white', linewidth=0.5, alpha=0.3, linestyle='--')
ax.axhline(y=1.0, color='white', linewidth=0.5, alpha=0.3)

ax.set_xlabel('r (distance from center)', color='white')
ax.set_ylabel('Effective refractive index', color='white')
ax.set_title('Refractive Index Profile across Wall', color='white', fontsize=10)
ax.legend(fontsize=8, facecolor='#1a1a2e', edgecolor='white', labelcolor='white')
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.1)

plt.savefig('research/04_warp_drive/boundary_logic.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
plt.close()

print(f"\n  Plot saved: research/04_warp_drive/boundary_logic.png")
print()
print("=" * 70)
print("  END")
print("=" * 70)
