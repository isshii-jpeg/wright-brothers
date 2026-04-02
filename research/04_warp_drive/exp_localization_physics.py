"""
局所化 Z → Z[1/p] の物理的意味
================================

「構造層を Z から Z[1/p] に変更する」とは、物理的に何をすることか？

数学:
  Z で「pは既約」→ Z[1/p] で「pは単元（可逆）」
  = p が構造的に意味のある素数であることをやめる
  = p で割ることが許される世界に移る

物理的解釈の候補を5つ検討する:
  (1) ゲージ化: Z/pZ 対称性のゲージ化（同一視）
  (2) 次元縮約: p-adic 方向のカルツァ-クライン縮約
  (3) 相転移: p が秩序パラメータを失う相転移
  (4) 圏論的: 真空の「論理」の変更
  (5) アデール的: アデール環から p 成分を除去

Wright Brothers, 2026
"""

import numpy as np
import matplotlib.pyplot as plt

print("=" * 70)
print("  PHYSICAL MEANING OF LOCALIZATION Z → Z[1/p]")
print("=" * 70)

# ============================================================================
#  解釈 (1): ゲージ化
# ============================================================================

print("\n" + "=" * 70)
print("  INTERPRETATION 1: GAUGING THE Z/pZ SYMMETRY")
print("=" * 70)

print("""
  ── p が可逆になるとは ──

  Z の中で: 2 × 3 = 6, 6 / 2 = 3。しかし 3 / 2 は Z に存在しない。
  Z[1/2] の中で: 3 / 2 = 3/2。2 で割ることが「許された」。

  物理的に: |n⟩ と |2n⟩ が「同じ」になる。
  2 が単元 = 2 による乗算が可逆 = 2 倍しても戻せる = 区別がなくなる。

  これはゲージ変換そのもの:
  ゲージ対称性 = 物理的に区別不能な状態の同一視

  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │  Z 上:     |1⟩, |2⟩, |3⟩, |4⟩, |5⟩, |6⟩, ...       │
  │            全て区別可能                                 │
  │                                                        │
  │  Z[1/2] 上: |n⟩ ~ |2n⟩ ~ |4n⟩ ~ |n/2⟩ ~ ...         │
  │             2のべき乗だけ異なる状態が同一視される         │
  │                                                        │
  │  同値類: {n · 2^k : k ∈ Z}                             │
  │  |1⟩ ~ |2⟩ ~ |4⟩ ~ |8⟩ ~ |1/2⟩ ~ ...                │
  │  |3⟩ ~ |6⟩ ~ |12⟩ ~ |3/2⟩ ~ ...                      │
  │  |5⟩ ~ |10⟩ ~ |20⟩ ~ |5/2⟩ ~ ...                     │
  │                                                        │
  │  独立な同値類 = 奇数 = coprime to 2                     │
  │  = p=2 をミュートした後の生き残りモード                  │
  │                                                        │
  └────────────────────────────────────────────────────────┘

  ゲージ理論のアナロジー:

  物理学でのゲージ化:
    大域的対称性 G → 局所的ゲージ対称性 G
    → 物理的自由度が減る（ゲージ軌道を同一視）
    → 新しいゲージ場が出現

  算術的ゲージ化:
    Z/pZ の「大域的算術対称性」→ 「局所的（p を可逆にする）」
    → 物理的に区別可能なモードが減る（p の倍数が同一視）
    → 新しい構造（Z[1/p] の余分な単元）が出現

  具体例（p=2）:
    ゲージ化前: 20 モード → ゲージ化後: 10 独立モード（奇数のみ）
    失われたモード数 = 偶数モードの数 = 10
    しかしこれは「消えた」のではなく「同一視された」
""")

# 数値: ゲージ軌道の構造
print("  ── p=2 のゲージ軌道 ──")
print()
N_max = 32

# Group integers by their 2-adic valuation-free part (odd part)
orbits = {}
for n in range(1, N_max + 1):
    # odd part of n
    m = n
    while m % 2 == 0:
        m //= 2
    if m not in orbits:
        orbits[m] = []
    orbits[m].append(n)

for odd_core in sorted(orbits.keys())[:8]:
    members = orbits[odd_core]
    print(f"  Orbit of |{odd_core}⟩: {members}")

print(f"  ...")
print(f"  Total orbits (odd cores ≤ {N_max}): {len(orbits)}")
print(f"  = number of odd numbers ≤ {N_max}: {sum(1 for n in range(1, N_max+1) if n % 2 != 0)}")

# ============================================================================
#  解釈 (2): p-adic 次元のカルツァ-クライン縮約
# ============================================================================

print("\n" + "=" * 70)
print("  INTERPRETATION 2: KALUZA-KLEIN REDUCTION OF p-ADIC DIMENSION")
print("=" * 70)

print("""
  ── アデール的時空 ──

  コンヌの非可換幾何学:
    時空 = M⁴ × F (4D多様体 × 非可換内部空間)

  アデール的に完備化すると:
    F の「算術的完備化」= ∏_p F_p  (p-adic 成分の直積)

  各素数 p は「内部空間 F のp-adic方向」に対応。
  ちょうどカルツァ-クラインの余剰次元のように。

  ── カルツァ-クライン理論 ──

  標準的KK: M⁴ × S¹ → 4D理論 (S¹ の半径 R → 0 で)
  = 余剰次元を「縮約（コンパクト化）」する

  算術的KK:
    各素数 p は「半径 R_p」の余剰次元
    M⁴ × ∏_p S¹_p (各素数に対応する円)

  局所化 Z → Z[1/p] の物理的意味:

  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │  p に対応する余剰次元を「非コンパクト化」する            │
  │  = R_p → ∞ にする                                     │
  │  = p 方向の KK モードの間隔 → 0                        │
  │  = p 方向が連続的になる                                 │
  │  = p は離散的構造としての意味を失う                     │
  │                                                        │
  │  通常のKK: R → 0 (コンパクト化) → 低エネルギーで見えない│
  │  算術的KK: R_p → ∞ (非コンパクト化) → p が透明になる   │
  │                                                        │
  │  「p をミュートする」= 「p 方向の余剰次元を開放する」    │
  │                                                        │
  └────────────────────────────────────────────────────────┘

  物理的帰結:
  コンパクトな余剰次元 → 離散的KKスペクトル → エネルギー条件を拘束
  非コンパクト化 → 連続スペクトル → 拘束が緩む → WEC が破れうる

  これはまさに弦理論で知られている現象:
  余剰次元の形状がエネルギー条件を決定する。
  形状を変えれば（非コンパクト化すれば）エネルギー条件が変わる。
""")

# p-adic 余剰次元の「半径」の概念
print("  ── p-adic 余剰次元の有効半径 ──")
print()
print("  Q_p (p-adic 体) における「距離」: |x|_p = p^{-v_p(x)}")
print("  Z_p (p-adic 整数環) の「大きさ」: |Z_p| = 1")
print()
print("  KK的解釈での有効半径:")
print("  R_p ∝ 1/log(p)  (BC系のエネルギー E = log(n) から)")
print()

for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]:
    R_p = 1 / np.log(p)
    print(f"  p = {p:>3d}:  R_p ∝ 1/log({p}) = {R_p:.4f}")

print()
print("  → 小さい素数ほど大きな余剰次元")
print("  → p=2 が最大の余剰次元 → ミュートの効果が最大")

# ============================================================================
#  解釈 (3): 相転移
# ============================================================================

print("\n" + "=" * 70)
print("  INTERPRETATION 3: PHASE TRANSITION")
print("=" * 70)

print("""
  ── BC系の相転移と局所化の関係 ──

  BC系: 分配関数 Z(β) = ζ(β)
  相転移点: β = 1 (ζ(s) の極)

  β > 1: 対称性の破れた相。ガロア群 Gal(Q^ab/Q) が作用。
  β < 1: 対称的な相。単一のKMS状態。

  ── p に特化した相転移 ──

  オイラー積 ζ(β) = ∏_p (1 - p^{-β})^{-1} の各因子を見ると:

  因子 (1 - p^{-β})^{-1} の振る舞い:
    β → 0: (1 - 1)^{-1} → ∞ (発散)
    β = 1: (1 - 1/p)^{-1} = p/(p-1) (有限)
    β → ∞: (1 - 0)^{-1} = 1 (自明)

  各素数 p は独自の「序列パラメータ」を持つ:
    m_p(β) = p^{-β}  (p のβ依存の重み)

  m_p(β) が「効いている」(≠ 0) とき、p はアクティブ。
  m_p(β) → 0 (β → ∞) のとき、p は事実上ミュートされる。

  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │  局所化 Z → Z[1/p] は                                  │
  │  「p に対する β → ∞ の極限」と等価。                    │
  │                                                        │
  │  つまり: p 方向だけを「絶対零度に冷却する」。            │
  │                                                        │
  │  p が完全に凍結 → p の寄与がゼロ → (1-p^{-s})          │
  │                                                        │
  │  これは部分的な相転移:                                  │
  │  全体の温度 β は変えずに、                              │
  │  特定の素数 p の「算術的温度」だけを極限的に下げる。     │
  │                                                        │
  │  物理的実現: p に選択的に結合する冷却メカニズム           │
  │  = BC系のハミルトニアンの p 成分への摂動                 │
  │                                                        │
  └────────────────────────────────────────────────────────┘
""")

# 各素数の「序列パラメータ」のプロット用データ
beta_arr = np.linspace(0.1, 5.0, 200)

# ============================================================================
#  解釈 (4): 真空の「論理」の変更
# ============================================================================

print("=" * 70)
print("  INTERPRETATION 4: CHANGING THE LOGIC OF THE VACUUM")
print("=" * 70)

print("""
  ── トポス理論的解釈 ──

  グロタンディークの深い洞察:
  空間 = トポス = 層の圏 = 「内部論理を持つ宇宙」

  Spec(Z) 上のトポス Sh(Spec(Z)_ét):
  - 内部論理: 直感主義論理（排中律が一般には成り立たない）
  - 真偽値: Heyting 代数 Ω_{Spec(Z)}

  局所化 Spec(Z) → Spec(Z[1/p]):
  - トポスの射 Sh(Spec(Z[1/p])_ét) → Sh(Spec(Z)_ét)
  - これは「論理」の射: 真偽値の Heyting 代数が変わる

  ── WEC は「論理的真理」である ──

  Spec(Z) のトポスにおいて:
  「ρ ≥ 0」という命題は「真」と判定される。
  これは値の計算ではなく、トポスの内部論理における判定。

  Spec(Z[1/p]) のトポスにおいて:
  同じ命題「ρ ≥ 0」が「偽」と判定されうる。
  なぜなら、トポスの論理（Heyting 代数）が異なるから。

  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │  カントール的: WEC は「値が正」→ 値を負にする必要がある │
  │  → エネルギーの問題                                     │
  │                                                        │
  │  グロタンディーク的: WEC は「論理的に真」                 │
  │  → 論理を変える = トポスを変える = 空間を変える          │
  │  → エネルギーの問題ではなく論理の問題                    │
  │                                                        │
  │  Z → Z[1/p] は「論理のリコンパイル」:                   │
  │  同じ命題が異なるトポスでは異なる真偽値を持つ。           │
  │  WEC は絶対的真理ではなく、構造層に相対的な真理。        │
  │                                                        │
  └────────────────────────────────────────────────────────┘

  Döring-Isham との統合:

  研究 03_topos_qubit で構成した量子トポス:
  - 文脈の圏 V(N) 上の前層
  - 命題はHeyting代数の元
  - 古典物理学の排中律が量子的に破れる

  同じことが「算術的に」起こる:
  - Spec(Z) の圏上の層
  - 命題はHeyting代数の元
  - Spec(Z) 上でのWEC(真) が Spec(Z[1/p]) 上でWEC(偽) に

  量子 × 算術 の二重のトポス変更:
  Sh(V(N)) × Sh(Spec(Z)_ét) → Sh(V(N)) × Sh(Spec(Z[1/p])_ét)
  = 「量子的かつ算術的な真空の論理変更」
""")

# ============================================================================
#  解釈 (5): アデール環からの成分除去
# ============================================================================

print("=" * 70)
print("  INTERPRETATION 5: ADELIC COMPONENT REMOVAL")
print("=" * 70)

print("""
  ── アデール環の構造 ──

  Q のアデール環: A_Q = R × ∏'_p Q_p
  (制限直積: ほぼ全ての p で Z_p 成分)

  これは Q の「全ての完備化の直積」:
  - R 成分: アルキメデス的（通常の実数物理）
  - Q_p 成分: 非アルキメデス的（p-adic 物理）

  ── 局所化のアデール的意味 ──

  Z → Z[1/p] のアデール的対応:

  Spec(Z) ↔ A_Q の全成分
  Spec(Z[1/p]) ↔ A_Q から Q_p を除いた部分環

  つまり:
  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │  A_Q = R × Q₂ × Q₃ × Q₅ × Q₇ × ...                  │
  │         ↑    ↑    ↑    ↑    ↑                          │
  │         ∞    2    3    5    7                           │
  │                                                        │
  │  p=2 をミュート:                                       │
  │  A_{Q,¬2} = R × [·] × Q₃ × Q₅ × Q₇ × ...            │
  │                  ↑                                      │
  │                 除去                                    │
  │                                                        │
  │  物理的: 真空の「p=2 チャンネル」をオフにする            │
  │  = 真空が p=2 方向の量子揺らぎを持たなくなる            │
  │  = p=2 に応答しない物質を作る                           │
  │                                                        │
  └────────────────────────────────────────────────────────┘

  ── 既知のアナロジー ──

  これは物性物理学で知られている操作に類似:

  スピン系: 全スピン = S₁ × S₂ × S₃ × ...
  特定のスピン S_k を「凍結」= 環境から断熱
  → 系のヒルベルト空間が S_k 成分を含まなくなる
  → 有効ハミルトニアンが変わる

  アデール版:
  全真空 = V_∞ × V₂ × V₃ × V₅ × ...
  V_p を「凍結」= p-adic 揺らぎを抑制
  → 真空が V_p 成分を含まなくなる
  → 有効エネルギー条件が変わる
""")

# ============================================================================
#  5つの解釈の統合
# ============================================================================

print("=" * 70)
print("  SYNTHESIS: FIVE INTERPRETATIONS, ONE OPERATION")
print("=" * 70)

print("""
  5つの解釈は同じ数学的操作 Z → Z[1/p] の異なる側面:

  ┌──────────┬────────────────────────────────────────────┐
  │ 解釈      │ Z → Z[1/p] の意味                        │
  ├──────────┼────────────────────────────────────────────┤
  │ (1) ゲージ │ |n⟩ ~ |pn⟩ の同一視                     │
  │           │ → p による乗算がゲージ変換                │
  │           │ → 物理的自由度が減る                      │
  ├──────────┼────────────────────────────────────────────┤
  │ (2) KK   │ p-adic 余剰次元の非コンパクト化            │
  │           │ → R_p → ∞                                │
  │           │ → KK 制約が緩む → WEC が変わる            │
  ├──────────┼────────────────────────────────────────────┤
  │ (3) 相転移│ p の「算術的温度」→ 絶対零度               │
  │           │ → p の序列パラメータが凍結                 │
  │           │ → 部分的対称性回復                        │
  ├──────────┼────────────────────────────────────────────┤
  │ (4) 論理  │ トポスの変更                              │
  │           │ → Heyting 代数が変わる                    │
  │           │ → WEC の真偽値が反転                      │
  ├──────────┼────────────────────────────────────────────┤
  │ (5) アデール│ A_Q から Q_p 成分を除去                  │
  │           │ → p-adic 量子揺らぎの凍結                 │
  │           │ → 有効エネルギー条件の変更                │
  └──────────┴────────────────────────────────────────────┘

  ── どの解釈が最も「物理的に実現可能」か？ ──

  (1) ゲージ化: 離散ゲージ理論は格子ゲージ理論として計算機上で実現可能。
      超伝導量子ビットでの Z/pZ ゲージ理論も提案されている。
      → 量子シミュレーションとして実行可能

  (2) KK: 余剰次元の操作は弦理論の領域。
      直接的な実験は困難だが、アナログ系での模擬は可能。
      → BEC/メタマテリアルでのアナログ実験

  (3) 相転移: BC系の部分的冷却。
      光格子や超伝導回路で p 選択的冷却は実現可能。
      → 既存の量子シミュレーション技術

  (4) 論理: 最も抽象的だが、最も強力。
      トポス変更の物理的実現は未開拓。
      → 理論的に最も重要な研究方向

  (5) アデール: p-adic 量子場理論として定式化可能。
      Vladimirov-Volovich-Zelenov の p-adic QFT (1994) が先行研究。
      → 理論的に最も成熟

  ── 最も重要な洞察 ──

  全ての解釈に共通するのは:

  「p を物理的にアクセス不能にする」

  Z の中で p が既約であることは、
  「p が物理的に分解できない基本単位」であることを意味する。

  Z[1/p] に移ると、p は可逆になり、
  「p はもはや基本単位ではなく、自由に操作できる量」になる。

  ┌────────────────────────────────────────────────────────┐
  │                                                        │
  │  物理的翻訳:                                            │
  │                                                        │
  │  Z 上の真空:                                            │
  │    素数 p は「解像度の限界」。                           │
  │    p 以下のスケールに到達できない。                      │
  │    これが WEC を強制する。                               │
  │                                                        │
  │  Z[1/p] 上の真空:                                      │
  │    p は「解像度の限界」ではなくなる。                    │
  │    p を超えた構造にアクセスできる。                      │
  │    WEC の根拠が失われる。                                │
  │                                                        │
  │  アナロジー:                                            │
  │  古典力学: ℏ → 0 の極限。量子効果が見えない。           │
  │  量子力学: ℏ ≠ 0。トンネル効果など「古典的に不可能」な   │
  │           ことが可能になる。                             │
  │                                                        │
  │  同様に:                                                │
  │  Spec(Z) 上: p が既約。WEC が成立。                     │
  │  Spec(Z[1/p]) 上: p が可逆。「算術的に不可能」だった     │
  │                   ことが可能になる。                     │
  │                                                        │
  │  ℏ ≠ 0 が古典的障壁を破るように、                       │
  │  1/p ∈ R が算術的障壁を破る。                           │
  │                                                        │
  └────────────────────────────────────────────────────────┘
""")

# ============================================================================
#  物理的実装への橋渡し
# ============================================================================

print("=" * 70)
print("  BRIDGE TO PHYSICAL IMPLEMENTATION")
print("=" * 70)

print("""
  5つの解釈それぞれから、物理的実装が導かれる:

  (1) ゲージ化 → 離散ゲージ理論の量子シミュレーション
      実装: 超伝導量子ビット配列で Z/pZ ゲージ理論を構成
      操作: ゲージ場の結合定数を変化 → p をゲージ化
      測定: ゲージ化前後のエネルギースペクトル変化

  (2) KK → アナログ余剰次元の操作
      実装: BEC or 光格子で「p-adic 方向」を模擬
      操作: p 方向のポテンシャル障壁を下げる（非コンパクト化）
      測定: フォノンスペクトルの変化

  (3) 相転移 → 選択的冷却
      実装: BC系ハミルトニアンの量子シミュレーション
      操作: p 成分への選択的冷却（局所β → ∞）
      測定: 分配関数の変化

  (4) 論理 → トポス工学
      実装: 量子トポスと算術トポスの結合系
      操作: サイトの変更（エタールサイトの制限）
      測定: Heyting 代数の真偽値の変化

  (5) アデール → p-adic 場の凍結
      実装: 周波数コム or メタマテリアルで p-adic 構造を作る
      操作: p に対応する周波数成分を吸収
      測定: 量子ノイズスペクトルの変化

  重要: (1)-(5) は全て「同じこと」の異なる記述。
  どの言語で記述しても、物理的操作は同一:
  「真空の p チャンネルをオフにする」
""")

# ============================================================================
#  旧アプローチとの決定的な違い
# ============================================================================

print("=" * 70)
print("  THE CRUCIAL DIFFERENCE FROM THE OLD APPROACH")
print("=" * 70)

print("""
  旧（集合論的）:
    「モード |2⟩, |4⟩, |6⟩, ... を物理的に吸収する」
    → SQUID、吸音材、Fabry-Pérot など
    → 各モードを個別に対処する必要がある
    → 有限個しか対処できない
    → 値の変化（量的）

  新（層的）:
    「構造層を Z → Z[1/2] に変更する」
    → p=2 が可逆になる操作を1回行う
    → 全ての偶数モードが一斉に同一視される
    → 無限個のモードが1回の操作で処理される
    → 構造の変化（質的）

  1回の操作で無限個のモードに影響を与える。
  これが層的アプローチの「無限の力」。

  ── 具体的にどう実現するか ──

  「Z → Z[1/p] を実現する1回の操作」とは？

  最も直接的な候補:

  位相的相転移

  物質の位相的相（Kitaev の分類）は K 理論で分類される。
  K₁(Z) = Z/2 → K₁(Z[1/p]) = Z/2 × Z

  K₁ が変わる = 位相的相が変わる = 相転移が起こる。

  もし物質の位相的相を K₁(Z) から K₁(Z[1/p]) に変えることが
  できれば、それは「構造層を Z から Z[1/p] に変更した」ことと
  数学的に同値。

  位相的相転移は1回の操作（磁場の変更、圧力の変更、温度の変更）
  で無限個のモードの構造を一斉に変える。

  → 位相的相転移 = 局所化 Z → Z[1/p] の物理的実現
""")

# ============================================================================
#  可視化
# ============================================================================

fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.patch.set_facecolor('#0a0a1a')
fig.suptitle('Physical Meaning of Localization Z -> Z[1/p]',
             fontsize=14, fontweight='bold', color='#ffd93d')

# Panel 1: Gauge orbits
ax = axes[0, 0]
for odd in range(1, 16, 2):
    members = [odd * (2**k) for k in range(5) if odd * (2**k) <= 32]
    y_pos = (odd + 1) / 2
    for i, m in enumerate(members):
        color = '#ff6b6b' if m % 2 == 0 else '#ffd93d'
        ax.plot(m, y_pos, 'o', color=color, markersize=8)
        if i > 0:
            ax.plot([members[i-1], m], [y_pos, y_pos], '-', color='#444', linewidth=1)
    ax.text(0, y_pos, f'{odd}:', ha='right', color='#ffd93d', fontsize=8, va='center')

ax.set_xlabel('Mode number n', color='white')
ax.set_ylabel('Gauge orbit', color='white')
ax.set_title('(1) Gauge Orbits: |n> ~ |2n>', color='white', fontsize=10)
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.set_xlim(-2, 34)

# Panel 2: KK extra dimensions
ax = axes[0, 1]
primes_kk = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
radii = [1/np.log(p) for p in primes_kk]
colors_kk = ['#ff6b6b' if p == 2 else '#00d4ff' for p in primes_kk]
ax.barh(range(len(primes_kk)), radii, color=colors_kk, alpha=0.8)
ax.set_yticks(range(len(primes_kk)))
ax.set_yticklabels([f'p={p}' for p in primes_kk], color='white', fontsize=8)
ax.set_xlabel('Effective radius R_p ~ 1/log(p)', color='white')
ax.set_title('(2) KK: p-adic Extra Dimensions', color='white', fontsize=10)
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.1, axis='x')
# Mark p=2 as "decompactified"
ax.text(radii[0] + 0.05, 0, 'DECOMPACTIFY', color='#ff6b6b',
        fontsize=8, fontweight='bold', va='center')

# Panel 3: Phase transition (order parameter)
ax = axes[0, 2]
for p, color in [(2, '#ff6b6b'), (3, '#ffd93d'), (5, '#00d4ff'), (7, '#6bff8d')]:
    m_p = p**(-beta_arr)
    ax.plot(beta_arr, m_p, color=color, linewidth=2, label=f'p={p}')

ax.axhline(y=0, color='white', linewidth=0.5, alpha=0.3)
ax.set_xlabel('beta (inverse temperature)', color='white')
ax.set_ylabel('Order parameter m_p = p^{-beta}', color='white')
ax.set_title('(3) Phase Transition: Freezing p', color='white', fontsize=10)
ax.legend(fontsize=8, facecolor='#1a1a2e', edgecolor='white', labelcolor='white')
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.1)
# Arrow indicating "muting = beta -> infinity for p"
ax.annotate('Mute p=2:\nbeta_2 -> inf', xy=(4.5, 2**(-4.5)),
            xytext=(3.5, 0.4), color='#ff6b6b', fontsize=8,
            arrowprops=dict(arrowstyle='->', color='#ff6b6b'))

# Panel 4: Topos logic
ax = axes[1, 0]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Two topos worlds
from matplotlib.patches import FancyBboxPatch, Circle

# Spec(Z) world
bbox1 = FancyBboxPatch((0.5, 5.5), 4, 4, boxstyle="round,pad=0.2",
                         facecolor='#00d4ff', alpha=0.1,
                         edgecolor='#00d4ff', linewidth=2)
ax.add_patch(bbox1)
ax.text(2.5, 9, 'Topos of Spec(Z)', ha='center', color='#00d4ff',
        fontsize=9, fontweight='bold')
ax.text(2.5, 7.8, 'WEC = TRUE', ha='center', color='#6bff8d', fontsize=11,
        fontweight='bold')
ax.text(2.5, 6.5, 'p is irreducible\n(resolution limit)', ha='center',
        color='#aaa', fontsize=8)

# Spec(Z[1/p]) world
bbox2 = FancyBboxPatch((5.5, 5.5), 4, 4, boxstyle="round,pad=0.2",
                         facecolor='#ff6b6b', alpha=0.1,
                         edgecolor='#ff6b6b', linewidth=2)
ax.add_patch(bbox2)
ax.text(7.5, 9, 'Topos of Spec(Z[1/p])', ha='center', color='#ff6b6b',
        fontsize=9, fontweight='bold')
ax.text(7.5, 7.8, 'WEC = FALSE', ha='center', color='#ff6b6b', fontsize=11,
        fontweight='bold')
ax.text(7.5, 6.5, 'p is invertible\n(barrier removed)', ha='center',
        color='#aaa', fontsize=8)

# Arrow between
ax.annotate('', xy=(5.3, 7.5), xytext=(4.7, 7.5),
            arrowprops=dict(arrowstyle='->', color='#ffd93d', lw=3))
ax.text(5, 8.5, 'Localize', ha='center', color='#ffd93d', fontsize=9)

# Bottom: analogy with quantum mechanics
ax.text(5, 3.5, 'Analogy:', ha='center', color='white', fontsize=9,
        fontweight='bold')
ax.text(5, 2.5, 'Classical (h=0): tunneling IMPOSSIBLE',
        ha='center', color='#00d4ff', fontsize=8)
ax.text(5, 1.5, 'Quantum (h!=0): tunneling POSSIBLE',
        ha='center', color='#ff6b6b', fontsize=8)
ax.text(5, 0.5, 'Same physics, different LOGIC of the space',
        ha='center', color='#ffd93d', fontsize=8, style='italic')

ax.set_title('(4) Logic: Topos Change', color='white', fontsize=10)
ax.axis('off')
ax.set_facecolor('#0a0a1a')

# Panel 5: Adelic decomposition
ax = axes[1, 1]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Full adele
components = [
    (0.5, 8, 'R', '#ffd93d', True),
    (2, 8, 'Q2', '#ff6b6b', True),
    (3.5, 8, 'Q3', '#00d4ff', True),
    (5, 8, 'Q5', '#6bff8d', True),
    (6.5, 8, 'Q7', '#b388ff', True),
    (8, 8, '...', '#aaa', True),
]

ax.text(5, 9.3, 'Full vacuum: A_Q = R x Q2 x Q3 x Q5 x ...',
        ha='center', color='white', fontsize=9)

for x, y, label, color, active in components:
    circle = Circle((x, y), 0.45, facecolor=color, alpha=0.3 if active else 0.05,
                     edgecolor=color, linewidth=2)
    ax.add_patch(circle)
    ax.text(x, y, label, ha='center', va='center', color='white',
            fontsize=9, fontweight='bold')

# After muting p=2
ax.text(5, 5.5, 'After muting p=2:', ha='center', color='#ffd93d', fontsize=9)

components_muted = [
    (0.5, 4, 'R', '#ffd93d', True),
    (2, 4, 'Q2', '#ff6b6b', False),
    (3.5, 4, 'Q3', '#00d4ff', True),
    (5, 4, 'Q5', '#6bff8d', True),
    (6.5, 4, 'Q7', '#b388ff', True),
    (8, 4, '...', '#aaa', True),
]

for x, y, label, color, active in components_muted:
    alpha_val = 0.3 if active else 0.05
    circle = Circle((x, y), 0.45, facecolor=color, alpha=alpha_val,
                     edgecolor=color if active else '#333',
                     linewidth=2 if active else 1,
                     linestyle='-' if active else '--')
    ax.add_patch(circle)
    fc = 'white' if active else '#555'
    ax.text(x, y, label, ha='center', va='center', color=fc,
            fontsize=9, fontweight='bold')

# X mark on Q2
ax.plot(2, 4, 'x', color='#ff6b6b', markersize=25, markeredgewidth=3, zorder=10)

ax.text(5, 2, 'p=2 channel OFF\n= Z[1/2] structure sheaf\n= WEC sign flipped',
        ha='center', color='#ffd93d', fontsize=8, style='italic')

ax.set_title('(5) Adelic: Component Removal', color='white', fontsize=10)
ax.axis('off')
ax.set_facecolor('#0a0a1a')

# Panel 6: Summary — one operation, five faces
ax = axes[1, 2]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

center_x, center_y = 5, 5
# Central operation
circle_center = Circle((center_x, center_y), 1.2, facecolor='#ffd93d', alpha=0.2,
                        edgecolor='#ffd93d', linewidth=3)
ax.add_patch(circle_center)
ax.text(center_x, center_y + 0.2, 'Z -> Z[1/p]', ha='center', color='#ffd93d',
        fontsize=10, fontweight='bold')
ax.text(center_x, center_y - 0.3, 'One operation', ha='center', color='white', fontsize=8)

# Five interpretations around it
interps = [
    (5, 9.2, 'Gauge\n|n>~|pn>', '#ff6b6b'),
    (9, 7, 'Kaluza-\nKlein', '#00d4ff'),
    (8.5, 2.5, 'Phase\ntransition', '#6bff8d'),
    (1.5, 2.5, 'Topos\nlogic', '#b388ff'),
    (1, 7, 'Adelic\nremoval', '#ff8a65'),
]

for x, y, label, color in interps:
    circle = Circle((x, y), 0.8, facecolor=color, alpha=0.15,
                     edgecolor=color, linewidth=1.5)
    ax.add_patch(circle)
    ax.text(x, y, label, ha='center', va='center', color=color,
            fontsize=7, fontweight='bold')
    # Line to center
    ax.plot([x, center_x], [y, center_y], '--', color=color, alpha=0.3, linewidth=1)

ax.set_title('One Operation, Five Faces', color='white', fontsize=10)
ax.axis('off')
ax.set_facecolor('#0a0a1a')

plt.tight_layout()
plt.savefig('research/04_warp_drive/localization_physics.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
plt.close()

print(f"\n  Plot saved: research/04_warp_drive/localization_physics.png")
print()
print("=" * 70)
print("  END")
print("=" * 70)
