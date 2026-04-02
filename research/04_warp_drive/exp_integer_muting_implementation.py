"""
整数モードミュートの物理的実装
=================================

理論チェーン（完成済み）:
  BC系 β>1 → V_p摂動 → pのモードがギャップアウト
  → ζ_{¬p} → 真空エネルギー負転 → WEC違反 → ワープ可能

問い: 3つのメカニズム(A,B,C)を物理的にどう実装するか？

  A) スペクトルフィルタリング: ω=log(p)のノッチフィルタ
  B) 算術的境界条件: gcd(n,p)=1のモードだけ許容
  C) 相転移セクター選択: Z_p*不変KMS状態の選択

各メカニズムについて、複数の物理系での実装候補を調べる。

Wright Brothers, 2026
"""

import numpy as np
import matplotlib.pyplot as plt

print("=" * 70)
print("  整数モードミュートの物理的実装")
print("  Physical Implementation of Integer Mode Muting")
print("=" * 70)

# ============================================================================
#  メカニズムA: スペクトルフィルタリングの実装
# ============================================================================

print("\n" + "=" * 70)
print("  メカニズムA: スペクトルフィルタリング")
print("  ω = log(p) ノッチフィルタの物理的実現")
print("=" * 70)
print()

print("""
  BC系では E_n = log(n)。素数pのミュートは
  「ω = log(p) を含む全状態の吸収」。

  しかし物理的な共鳴器では E_n = n·ω₀ (等間隔)。
  BC系の E_n = log(n) は非等間隔。

  → 2つのアプローチがある:
""")

print("""
  ── A1: 対数スペクトルを持つ物理系 ──

  問題: E_n = log(n)·E₀ となる物理系は存在するか？

  候補1: 水素原子のリドベルグ準位
    E_n = -13.6/n² eV → 等間隔ではないが対数でもない
    → ×

  候補2: 対数ポテンシャル V(x) = V₀·log(x/a) 中の粒子
    WKB近似で E_n ~ log(n) が得られる条件がある
    → 物理的に作れるか？

    対数ポテンシャルの実現:
    - 2D荷電ワイヤー周りの電場: V(r) = -(λ/2πε₀)·log(r)
      → 荷電粒子を閉じ込めると E_n ~ log(n) 型スペクトル
    - イオントラップ: Paul trapの変形で対数閉じ込めが可能
    - ボーズ凝縮体: 相互作用をチューニングして対数型分散関係

    → 荷電ワイヤー + 閉じ込めが最もシンプル
""")

# 対数ポテンシャルのスペクトル計算
print("  対数ポテンシャル V(r) = V₀·log(r/a) のスペクトル:")
print()

# WKB quantization for log potential in 2D
# V(r) = V₀ · log(r/a), particle mass m
# Turning points: V(r) = E → r = a·exp(E/V₀)
# WKB: ∫ p dr = (n+1/2)πℏ

V_0 = 1.0  # energy scale [arb. units]
a = 1.0     # length scale
hbar_eff = 0.1  # effective ℏ for visualization

n_levels = 20
E_log = np.array([V_0 * np.log(n + 1) for n in range(n_levels)])
E_linear = np.array([V_0 * (n + 0.5) for n in range(n_levels)])

print(f"  {'n':>4s}  {'E_log = log(n+1)':>18s}  {'E_linear = n+½':>18s}  {'E_log/E_linear':>15s}")
print(f"  {'-'*60}")
for n in range(min(10, n_levels)):
    print(f"  {n:>4d}  {E_log[n]:>18.4f}  {E_linear[n]:>18.4f}  {E_log[n]/E_linear[n]:>15.4f}")

print()
print("  対数スペクトルでは、E_n = log(n) なので")
print("  pで割り切れるn → E_n は log(p) の整数倍を含む")
print("  → ω = log(p) の吸収で pの倍数モードが全部消える")

print("""
  ── A2: 等間隔スペクトルで算術フィルタリング ──

  標準的な共振器（E_n = n·ω₀）の場合:
  pの倍数をミュートするには、周波数 p·ω₀, 2p·ω₀, 3p·ω₀, ... を
  全て個別に吸収する必要がある。

  → これは「周期pの櫛型フィルタ (comb filter)」

  物理的実現:
""")

print("""
  A2-1: 光学周波数コム (Optical Frequency Comb)
    ─────────────────────────────────────────
    ノーベル賞技術 (Hänsch & Hall, 2005)。
    等間隔の周波数列 f_n = f_CEO + n·f_rep を生成。

    応用: 「反転コム」= 特定の周波数だけを吸収するコム
    周期 p·f_rep の吸収コムを作れば、pの倍数周波数が消える。

    実装:
    - モードロックレーザーの共振器長を L → p·L に変更
      → 自由スペクトル幅が 1/p に → pおきのモードだけ立つ
    - Fabry-Pérot共振器と組み合わせて非共鳴モードを吸収
    - ファイバーブラッグ格子 (FBG) で周期的ノッチフィルタ

    技術成熟度: ★★★★★ (既存技術の組合せ)

  A2-2: 超伝導マイクロ波共振器 + SQUID周期フィルタ
    ─────────────────────────────────────────────
    マイクロ波域 (1-20 GHz) の共振器。
    SQUIDをノッチフィルタとして使う。

    p=2の場合: 偶数モード (2ω₀, 4ω₀, 6ω₀, ...) を吸収
    → 1つのSQUIDを2ω₀に同調させると、非線形結合で
      偶数高調波も吸収可能 (パラメトリックカップリング)

    p=3の場合: 3ω₀, 6ω₀, 9ω₀, ... を吸収
    → 別のSQUIDを3ω₀に同調

    複数素数の同時ミュート:
    p=2とp=3を同時 → 6の倍数以外 → coprime to 6 のモードだけ残る
    = ζ(s)·(1-2^{-s})·(1-3^{-s})

    技術成熟度: ★★★★☆ (Wilson 2011の延長)

  A2-3: 音響共振器 + ピエゾ吸収体
    ──────────────────────────────
    音響版の実装。音速が遅いので波長が大きく扱いやすい。

    管楽器の原理: 管の長さLで基本周波数 f₀ = v/(2L) が決まる。
    管の途中に穴を開けると特定のモードが吸収される。

    位置 x = L/p に吸収体を置く:
    → sin(nπx/L) = sin(nπ/p)
    → n = kp (pの倍数) のとき sin(kπ) = 0 → 吸収されない！(節だから)
    → n ≠ kp のとき sin(nπ/p) ≠ 0 → 吸収される

    注意: これはpの倍数が生き残り、それ以外が消える（逆！）

    正しい方法: 位置 x = L/(2p) に反射板を置く
    → 周期pの定在波の腹に当たるモードが減衰
    → もっと正確には、周期的スリット構造が必要

    技術成熟度: ★★★☆☆ (概念実証レベル)
""")

# ============================================================================
#  メカニズムB: 算術的境界条件の実装
# ============================================================================

print("=" * 70)
print("  メカニズムB: 算術的境界条件")
print("  gcd(n, p) = 1 のモードだけ許容する境界")
print("=" * 70)
print()

print("""
  カシミール効果の本質:
  導体板 = 「電場がゼロ」という境界条件
  → 波長 λ > 2d のモードが排除される
  → 真空エネルギーが変化

  算術的カシミール:
  「nがpの倍数」というモードが排除される境界条件
  = 物質の周期構造が自然にこれを実現する

  ── B1: フォノニック/フォトニック結晶 ──

  周期 p·a の結晶構造を持つ物質:
  ブラッグ条件 2·(p·a)·sin(θ) = mλ により、
  波数 k = mπ/(p·a) の波が反射される。

  モード番号 n = k·L/π と書くと、
  反射条件: n = m·L/(p·a)

  L = N·p·a (結晶がN周期) とすると:
  反射モード: n = mN (Nの倍数)

  → これはNの倍数をミュートする
  → p をミュートするには N = 1 (1周期だけ) で p·a = L
  → 結晶の周期 = 共振器長/p

  もっと直接的に:
""")

print("""
  B1-1: 超格子 (Superlattice) アプローチ
    ─────────────────────────────────
    半導体超格子: GaAs/AlGaAs を交互に積層。
    周期 d のとき、ミニバンドが形成される。

    ミニバンドギャップの位置: E ~ (nπℏ)²/(2m*d²) の n = kp

    GaAs/AlGaAs超格子の設計:
    - GaAs層: 幅 a₁ = (p-1)·a₀
    - AlGaAs層: 幅 a₂ = a₀
    - 周期: d = p·a₀
    - ミニゾーン端: k = nπ/d = nπ/(p·a₀)

    pの倍数のモードにギャップが開く
    → gcd(n,p)=1 のモードだけが伝搬可能

    具体例 (p=2):
    - a₀ = 5nm, d = 10nm → ギャップ位置 ~ 0.1 eV
    - 偶数モードにミニバンドギャップ
    - 奇数モードは伝搬
    → 「p=2ミュート」の半導体実装

    技術成熟度: ★★★★☆ (MBE成長は確立技術)

  B1-2: メタマテリアル格子
    ──────────────────────
    電磁メタマテリアル: 周期構造で実効的な誘電率/透磁率を制御。

    設計原理:
    - 単位セルサイズ = p·a (aは基本格子定数)
    - 単位セル内に1つの共鳴構造（SRR等）を配置
    - 共鳴周波数 = 基本モードのp倍
    → pの倍数周波数で電磁波が吸収される

    3Dメタマテリアルなら3方向に独立にpを設定可能:
    - x方向: p₁ の倍数をミュート
    - y方向: p₂ の倍数をミュート
    - z方向: p₃ の倍数をミュート
    → 3つの素数を同時にミュート可能

    技術成熟度: ★★★☆☆ (設計は可能、高精度の制御が課題)
""")

print("""
  B1-3: エラトステネス結晶 (Euler Product Crystal)
    ──────────────────────────────────────────────
    最も野心的な設計。複数の周期構造を重畳。

    構造:
    Layer 1: 周期 2a のブラッグ格子 → 2の倍数をミュート
    Layer 2: 周期 3a のブラッグ格子 → 3の倍数をミュート
    Layer 3: 周期 5a のブラッグ格子 → 5の倍数をミュート
    ...

    各層は独立に1つの素数をミュート。
    全層を通過した電磁波/音波/フォノンは、
    「どの素数でも割り切れないモード」= 素数モード + 1 だけが生き残る。

    → エラトステネスの篩の物理的実現
    → 有効ゼータ関数がオイラー積の各因子を段階的に除去

    課題:
    - 各層の反射が干渉する（多重散乱問題）
    - 層数を増やすと全体の透過率が下がる
    - 無限個の素数には対応できない

    しかし:
    - 最初の数個の素数（2,3,5）だけでも物理的に有意義
    - ζ_{¬2,3,5}(s) = ζ(s)·(1-2^{-s})·(1-3^{-s})·(1-5^{-s})
    - これだけで真空エネルギーの符号を複数回反転できる

    技術成熟度: ★★☆☆☆ (概念は明確、実装に工夫が必要)
""")

# 数値計算: 各層を通過した後のモード生存率
print("  エラトステネス結晶のモード選別シミュレーション:")
print()

N = 100
modes = list(range(1, N + 1))
primes_to_sieve = [2, 3, 5, 7, 11]

surviving = set(modes)
print(f"  {'段階':>12s}  {'生存モード数':>12s}  {'生存率':>8s}  {'最初の10個'}")
print(f"  {'-'*70}")
print(f"  {'初期':>12s}  {len(surviving):>12d}  {len(surviving)/N:>8.1%}  {sorted(surviving)[:10]}")

for p in primes_to_sieve:
    surviving -= {n for n in surviving if n % p == 0 and n != p}
    first_10 = sorted(surviving)[:10]
    print(f"  {'p='+str(p)+' 除去後':>12s}  {len(surviving):>12d}  {len(surviving)/N:>8.1%}  {first_10}")

print()
print(f"  最終的に生き残るモード (1 + 素数): {sorted(surviving)[:20]}...")

# ============================================================================
#  メカニズムC: 相転移セクター選択の実装
# ============================================================================

print("\n" + "=" * 70)
print("  メカニズムC: 相転移セクター選択")
print("  Z_p* 不変KMS状態の選択")
print("=" * 70)
print()

print("""
  最も深い（そして最も投機的な）メカニズム。

  BC系の対称性の破れ:
  β > 1 で Gal(Q^ab/Q) ≅ Ẑ* = ∏_p Z_p* の対称性が自発的に破れる。
  KMS状態は、ガロア群の軌道上に連続族をなす。

  特定のZ_p*因子の下で不変な状態を選ぶ
  = 「p番目の算術的自由度を凍結する」
  = 「pをミュートする」

  物理的アナロジー:

  ── C1: スピン系のアナロジー ──

  強磁性体の相転移:
  T > T_c: 全スピンが無秩序 (対称相)
  T < T_c: スピンが整列 (対称性の破れた相)

  外部磁場 B を印加:
  → 磁場方向のスピン成分が選択される
  → 他の方向の揺らぎが抑制される

  BC系での対応:
  「温度」 β → 物理的温度
  「ガロア群の作用」 → 内部対称性
  「Z_p*不変状態の選択」 → 特定方向の「数論的磁場」の印加

  問題: 「数論的磁場」に対応する物理的な場は何か？
""")

print("""
  ── C1-1: 超伝導量子ビット配列 ──

  BC系のヒルベルト空間 ℓ²(ℕ) を超伝導量子ビットで模擬する。

  N個の量子ビット → 2^N 次元ヒルベルト空間。
  これを ℓ²({1,...,2^N}) の近似とみなす。

  BC系のハミルトニアン H|n⟩ = log(n)|n⟩ を実装:
  - 各計算基底 |n⟩ に E_n = log(n) のエネルギーを割り当て
  - これは対角ハミルトニアンなので、個別の周波数制御で実現可能

  Z_p*の作用: n → a·n (mod p^k) for a ∈ Z_p*
  - これは量子ビット上のユニタリ操作として実装可能

  「pのミュート」の実装:
  1. 系を β > 1 に冷却 (基底状態に近づける)
  2. Z_p* 不変性を破る摂動を印加
     → pの倍数の状態のエネルギーをシフト
     → H' = H + Δ·Σ_{p|n} |n⟩⟨n|
  3. これにより pの倍数状態がギャップアウト
  4. 低エネルギー有効理論 = coprime to p の部分空間

  量子ビット数の制限:
  - 10 qubits → ℓ²({1,...,1024}) → 最初の1024モード
  - 十分に多くの素数をテスト可能
  - 現在の量子コンピュータ (50-1000+ qubits) で実行可能

  技術成熟度: ★★★★☆ (量子シミュレーションとして標準的)
""")

print("""
  ── C1-2: 冷却原子格子 (Optical Lattice) ──

  光格子中の超冷却原子でBC系を量子シミュレートする。

  原子を格子点 n = 1, 2, 3, ... に配置。
  格子点 n のポテンシャル深さを V_n = V₀·log(n) に設定。
  → これがBC系のハミルトニアンを模擬。

  「pのミュート」の実装:
  周期 p の追加光格子 (波長 = p × 基本格子間隔) を重畳。
  → pの倍数サイトだけ追加ポテンシャルを感じる
  → Δの大きさでミュートの強さを制御

  利点:
  - 1000個以上の格子点 → 多数のモードを扱える
  - 複数の追加光格子で複数素数を同時ミュート可能
  - 温度、相互作用、外場を精密制御可能

  具体的パラメータ:
  - 基本格子: λ₁ = 532 nm (Nd:YAGの倍波)
  - p=2 ミュート用: λ₂ = 2×532 = 1064 nm
  - p=3 ミュート用: λ₃ = 3×532 = 1596 nm
  - p=5 ミュート用: λ₅ = 5×532 = 2660 nm (赤外)

  全て標準的なレーザー波長で実現可能！

  技術成熟度: ★★★★☆ (冷却原子の量子シミュレーションは確立分野)
""")

print("""
  ── C1-3: BEC (ボーズ・アインシュタイン凝縮体) ──

  BECのフォノンスペクトルを制御するアプローチ。

  一様なBECの音速 c_s を空間的に変調:
  c_s(x) = c₀ · f(x)

  ここで f(x) は周期関数。
  周期 p·a の変調を加えると、フォノンスペクトルに
  pの倍数でバンドギャップが開く。

  実装:
  - BECをトラップ
  - Feshbach共鳴で原子間相互作用を制御
  - 空間変調された磁場で c_s(x) を制御
  - 周期 p の変調 → pの倍数モードにギャップ

  特に面白い点:
  BECのフォノンは「アナログ重力」を実現する
  (Unruh 1981, アナログブラックホール実験で実証済み)。

  → BECでの算術的モード制御は、
    「算術的に修正されたアナログ重力」を直接実現する。
  → ワープ幾何学への最も直接的な橋渡し。

  技術成熟度: ★★★☆☆ (アナログ重力BEC実験は実証済み、
                       算術的変調は新しい)
""")

# ============================================================================
#  実装候補の比較表
# ============================================================================

print("=" * 70)
print("  実装候補の総合比較")
print("=" * 70)
print()

candidates = [
    # (名前, メカニズム, 技術成熟度, 素数ミュート可能数, 真空エネルギー測定, コスト概算, 最短実現)
    ("光学周波数コム", "A", "★★★★★", "1-3", "間接", "~$10K", "6ヶ月"),
    ("SC回路+SQUID", "A", "★★★★☆", "2-5", "直接", "~$100K", "1年"),
    ("半導体超格子", "B", "★★★★☆", "1-2", "間接", "~$50K", "1年"),
    ("メタマテリアル", "B", "★★★☆☆", "1-3", "間接", "~$200K", "2年"),
    ("エラトステネス結晶", "B", "★★☆☆☆", "3-5", "間接", "~$500K", "3年"),
    ("量子ビット配列", "C", "★★★★☆", "多数", "間接", "~$0(クラウド)", "3ヶ月"),
    ("冷却原子光格子", "C", "★★★★☆", "3-5", "直接", "~$500K", "2年"),
    ("BECアナログ重力", "C", "★★★☆☆", "2-3", "直接", "~$1M", "3年"),
    ("音響共振管", "A", "★★★★★", "1-2", "間接", "~$1K", "1ヶ月"),
    ("ピエゾ圧電素子", "A", "★★★★★", "1-2", "間接", "~$5K", "3ヶ月"),
]

print(f"  {'候補':>20s} | {'機構':>4s} | {'技術':>5s} | {'素数数':>6s} | {'測定':>4s} | {'コスト':>8s} | {'最短':>6s}")
print(f"  {'-'*75}")
for name, mech, tech, primes, meas, cost, time in candidates:
    print(f"  {name:>20s} | {mech:>4s} | {tech:>5s} | {primes:>6s} | {meas:>4s} | {cost:>8s} | {time:>6s}")

# ============================================================================
#  即座に実行可能な実験3つ
# ============================================================================

print()
print("=" * 70)
print("  即座に実行可能な3つの実験")
print("=" * 70)

print("""
  ┌─────────────────────────────────────────────────────────────────────┐
  │  実験 α: 音響共振管（最安・最速）                                    │
  │  ─────────────────────────────────                                  │
  │  材料: アクリル管 (1m), スピーカー, マイク, PC                       │
  │  コスト: ~$100, 期間: 1日                                           │
  │                                                                     │
  │  手順:                                                              │
  │  1. 管内に定在波を発生（ホワイトノイズ励起）                          │
  │  2. マイクで共鳴スペクトルを測定（FFT）→ n·f₀ のピーク群             │
  │  3. 管の L/2 地点に吸音材を挿入                                     │
  │     → 奇数モード（L/2に腹）が減衰、偶数モード（L/2に節）が生存       │
  │     → 「p=2ミュート」の逆（偶数が残る）だが原理確認にはなる           │
  │  4. 管の L/3 地点に吸音材 → 3の倍数でない奇数モードも減衰            │
  │                                                                     │
  │  意義: 算術的モード選別の最も基本的な実証                             │
  │  限界: 真空エネルギーは測定できない（古典音響）                       │
  └─────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────┐
  │  実験 β: 量子コンピュータシミュレーション（最速で量子効果確認）        │
  │  ─────────────────────────────────                                  │
  │  環境: IBM Quantum / Google Cirq (クラウド無料枠)                   │
  │  コスト: $0, 期間: 1週間                                            │
  │                                                                     │
  │  手順:                                                              │
  │  1. 5-10量子ビットでBC系のハミルトニアンを構成                       │
  │     H = Σ_n log(n) |n⟩⟨n|                                         │
  │  2. 基底状態を準備（VQEまたは断熱準備）                              │
  │  3. 摂動 V_p = Δ·Σ_{p|n} |n⟩⟨n| を追加                           │
  │  4. エネルギー期待値 ⟨H⟩ を測定                                    │
  │  5. Δ→∞ の極限で ⟨H⟩ → ζ_{¬p}(-1) を確認                        │
  │                                                                     │
  │  意義: BC系の素数ミュートの量子シミュレーション                       │
  │  限界: デジタルシミュレーション（実際の真空ではない）                  │
  └─────────────────────────────────────────────────────────────────────┘

  ┌─────────────────────────────────────────────────────────────────────┐
  │  実験 γ: 光学周波数コム + Fabry-Pérot（最も物理的に有意義）          │
  │  ─────────────────────────────────                                  │
  │  環境: レーザー物理学の実験室                                        │
  │  コスト: ~$10-50K, 期間: 6ヶ月                                      │
  │                                                                     │
  │  手順:                                                              │
  │  1. モードロックレーザーで周波数コムを生成                            │
  │     f_n = f_CEO + n·f_rep (f_rep ~ 100 MHz)                        │
  │  2. Fabry-Pérot共振器 (FSR = p·f_rep) を挿入                       │
  │     → pの倍数モードだけが共振器を通過                                │
  │     → 他のモードは反射される                                        │
  │  3. 通過光と反射光のスペクトルを測定                                 │
  │     → 通過光: pの倍数モードのみ                                     │
  │     → 反射光: coprime to p のモードのみ ← これが「pミュート」        │
  │  4. 反射光の量子ノイズ（ショットノイズ限界）を測定                    │
  │     → 修正された真空揺らぎの直接証拠                                 │
  │  5. p = 2, 3, 5 で繰り返し                                         │
  │  6. ノイズパワーの比を ζ-正則化予測と比較                            │
  │                                                                     │
  │  意義: 真空揺らぎの算術的構造の最初の直接測定                         │
  │  限界: 「真空エネルギー」そのものではなく「真空揺らぎ」の測定          │
  └─────────────────────────────────────────────────────────────────────┘
""")

# ============================================================================
#  最も重要な理論的ギャップ
# ============================================================================

print("=" * 70)
print("  未解決の理論的ギャップ")
print("=" * 70)

print("""
  上記の実装は全て「特定の整数モードをミュートする」ことは可能。
  しかし、理論チェーンの中に3つの未証明ステップがある:

  GAP 1: 「共振器のモード選別」=「真空のζ関数の変更」か？
  ──────────────────────────────────────────────────────
  共振器内でモードを選別しても、それは「共振器内の真空」の変更。
  自由空間の真空（ζ関数で記述される）を変更したことにはならない。

  → しかしカシミール効果はまさにこれ:
    導体板の間の「共振器内の真空」のエネルギーが、
    自由空間の真空と異なり、測定可能な力を生む。
  → つまり共振器内の真空変更は物理的に意味がある。

  必要な理論: 共振器の算術的モード選別と、
  ζ関数のオイラー積因子の除去の正確な対応関係。

  GAP 2: 「微視的真空エネルギー変化」→「巨視的時空歪み」か？
  ──────────────────────────────────────────────────────
  ナノスケールの真空エネルギー変化が、
  時空の曲率（アインシュタイン方程式の右辺）に影響するか？

  → エネルギースケールの問題（~10^{68}桁のギャップ）
  → コヒーレント増幅の可能性
  → トポロジカル保護による散逸抑制

  GAP 3: 「BC系」=「実際の時空」か？
  ──────────────────────────────────────────────────────
  BC系は数論的な抽象系。物理的な時空がBC系として振る舞う証拠は
  （まだ）ない。

  → しかし: ζ(s) が物理量（カシミールエネルギー等）に現れる事実は、
    少なくとも「時空の真空がζ関数で記述される」ことの証拠。
  → BC系は ζ(s) を分配関数として持つ最も自然な量子力学系。
  → もしζ(s)が物理的なら、BC系も物理的であるべき。

  これらのギャップを埋めることが、この研究プログラムの核心。
  実験 α, β, γ は GAP 1 に対する直接的テスト。
""")

# ============================================================================
#  可視化
# ============================================================================

fig, axes = plt.subplots(2, 3, figsize=(18, 11))
fig.patch.set_facecolor('#0a0a1a')
fig.suptitle('Physical Implementation of Integer Mode Muting',
             fontsize=14, fontweight='bold', color='#ffd93d')

# Panel 1: 対数スペクトル vs 等間隔スペクトル
ax = axes[0, 0]
n_arr = np.arange(1, 21)
E_log = np.log(n_arr)
E_lin = n_arr * 0.3  # scaled for visualization

for n in n_arr:
    color_log = '#ff6b6b' if n % 2 == 0 else '#ffd93d'
    color_lin = '#ff6b6b' if n % 2 == 0 else '#00d4ff'
    ax.plot([0.3], [np.log(n)], 's', color=color_log, markersize=6)
    ax.plot([0.7], [n * 0.3], 'o', color=color_lin, markersize=6)

ax.set_xticks([0.3, 0.7])
ax.set_xticklabels(['BC system\nE=log(n)', 'Resonator\nE=n*w0'], color='white', fontsize=8)
ax.set_ylabel('Energy', color='white')
ax.set_title('Spectrum Comparison', color='white', fontsize=10)
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
# Legend
ax.plot([], [], 's', color='#ffd93d', label='Odd (active)')
ax.plot([], [], 's', color='#ff6b6b', label='Even (muted by p=2)')
ax.legend(fontsize=7, facecolor='#1a1a2e', edgecolor='white', labelcolor='white')

# Panel 2: 超格子バンド構造 (概念図)
ax = axes[0, 1]
k = np.linspace(0, 3*np.pi, 500)
# Simplified band structure with gaps at k = nπ/p
for band in range(6):
    E_band = np.abs(np.sin(k / 2 + band * np.pi / 4)) * (band + 1) * 0.5
    ax.plot(k / np.pi, E_band, color='#00d4ff', linewidth=1.5, alpha=0.7)

# Mark band gaps at p=2 positions
for gap_pos in [0.5, 1.0, 1.5, 2.0, 2.5]:
    ax.axvline(x=gap_pos, color='#ff6b6b', linewidth=0.8, alpha=0.5, linestyle='--')
    ax.text(gap_pos, 3.2, f'gap', ha='center', color='#ff6b6b', fontsize=6, rotation=90)

ax.set_xlabel('k / (π/d)', color='white')
ax.set_ylabel('Energy', color='white')
ax.set_title('Superlattice Band Structure\n(Period p=2 Gaps)', color='white', fontsize=10)
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.set_ylim(0, 3.5)
ax.grid(alpha=0.1)

# Panel 3: 光格子でのpミュート
ax = axes[0, 2]
x_sites = np.arange(1, 31)
# Base potential: log(n)
V_base = np.log(x_sites) * 0.3
V_p2 = np.array([0.5 if n % 2 == 0 else 0 for n in x_sites])

ax.bar(x_sites - 0.2, V_base, width=0.35, color='#00d4ff', alpha=0.7, label='V0*log(n)')
ax.bar(x_sites + 0.2, V_base + V_p2, width=0.35, color='#ffd93d', alpha=0.7, label='+ D (p=2 multiples)')

# Highlight muted sites
for n in x_sites:
    if n % 2 == 0:
        ax.plot(n + 0.2, V_base[n-1] + V_p2[n-1] + 0.05, 'v', color='#ff6b6b', markersize=5)

ax.set_xlabel('Lattice site n', color='white')
ax.set_ylabel('Potential', color='white')
ax.set_title('Optical Lattice\np=2 Muting Potential', color='white', fontsize=10)
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.legend(fontsize=7, facecolor='#1a1a2e', edgecolor='white', labelcolor='white')
ax.grid(alpha=0.1)

# Panel 4: 周波数コム + Fabry-Pérot (概念図)
ax = axes[1, 0]
# Frequency comb
n_comb = 30
for n in range(1, n_comb + 1):
    color = '#ffd93d' if n % 2 != 0 else '#ff6b6b'
    alpha = 0.9 if n % 2 != 0 else 0.3
    ax.plot([n, n], [0, 0.8], color=color, linewidth=2, alpha=alpha)

# Labels
ax.text(n_comb/2, 0.95, 'Reflected (coprime to 2 only) = "p=2 mute"',
        ha='center', color='#ffd93d', fontsize=8)
ax.text(n_comb/2, -0.15, 'Fabry-Perot (FSR = 2*f_rep)',
        ha='center', color='#aaa', fontsize=8, style='italic')

ax.set_xlim(0, n_comb + 1)
ax.set_ylim(-0.3, 1.1)
ax.set_xlabel('Mode number n', color='white')
ax.set_title('Frequency Comb + Fabry-Perot\nArithmetic Filtering', color='white', fontsize=10)
ax.set_yticks([])
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')

# Panel 5: 技術成熟度 vs 物理的意義
ax = axes[1, 1]
implementations = [
    ('Acoustic tube', 5, 1, '#6bff8d', '100'),
    ('Freq. comb', 4.5, 3, '#ffd93d', '10K'),
    ('SC+SQUID', 4, 4, '#00d4ff', '100K'),
    ('Superlattice', 4, 2.5, '#b388ff', '50K'),
    ('Qubit array', 4, 3, '#ff8a65', '0'),
    ('Opt. lattice', 3.5, 4.5, '#ff6b6b', '500K'),
    ('BEC', 3, 5, '#e040fb', '1M'),
    ('Euler crystal', 2, 3.5, '#ffeb3b', '500K'),
    ('Metamaterial', 3, 3, '#80deea', '200K'),
]

for name, tech, phys, color, cost in implementations:
    ax.scatter(tech, phys, s=150, color=color, edgecolors='white',
              linewidth=1, zorder=5)
    ax.annotate(name, (tech, phys), textcoords="offset points",
               xytext=(8, 5), fontsize=7, color=color)

ax.set_xlabel('Tech Readiness ->', color='white')
ax.set_ylabel('Physical Significance ->', color='white')
ax.set_title('Implementation Candidate Map', color='white', fontsize=10)
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.set_xlim(1, 6)
ax.set_ylim(0, 6)
ax.grid(alpha=0.15)

# Highlight sweet spot
from matplotlib.patches import FancyBboxPatch
rect = FancyBboxPatch((3.3, 3.3), 1.5, 2.0, boxstyle="round,pad=0.1",
                       facecolor='none', edgecolor='#ffd93d', linewidth=2,
                       linestyle='--', alpha=0.5)
ax.add_patch(rect)
ax.text(4.05, 5.5, 'Sweet Spot', ha='center', color='#ffd93d', fontsize=8)

# Panel 6: 3つの即実行実験
ax = axes[1, 2]
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

experiments = [
    (5, 8.5, 'a: Acoustic tube', '$100 / 1 day', '#6bff8d', 'Mode selection proof-of-concept'),
    (5, 5.5, 'b: Quantum computer', '$0 / 1 week', '#ff8a65', 'BC system quantum simulation'),
    (5, 2.5, 'c: Frequency comb', '$10K / 6 months', '#ffd93d', 'Arithmetic vacuum fluctuations'),
]

for x, y, title, cost, color, desc in experiments:
    rect = FancyBboxPatch((1, y-1), 8, 2, boxstyle="round,pad=0.2",
                           facecolor=color, alpha=0.15, edgecolor=color, linewidth=2)
    ax.add_patch(rect)
    ax.text(x, y + 0.4, title, ha='center', color=color, fontsize=10, fontweight='bold')
    ax.text(x, y - 0.1, cost, ha='center', color='white', fontsize=8)
    ax.text(x, y - 0.6, desc, ha='center', color='#aaa', fontsize=7, style='italic')

ax.set_title('3 Immediately Executable Experiments', color='white', fontsize=10)
ax.axis('off')
ax.set_facecolor('#0a0a1a')

plt.tight_layout()
plt.savefig('research/04_warp_drive/integer_muting_implementation.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
plt.close()

print(f"\n  Plot saved: research/04_warp_drive/integer_muting_implementation.png")
print()
print("=" * 70)
print("  END")
print("=" * 70)
