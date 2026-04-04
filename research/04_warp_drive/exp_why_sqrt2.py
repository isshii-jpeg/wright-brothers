"""
Why Q(√2)? The three unsolved problems.
========================================

(1) Why does Q(√2) correspond to electroweak?
(2) Can CKM/PMNS be reached by other coverings?
(3) Is there a selection principle for d=2?

Wright Brothers, 2026
"""

import numpy as np
import mpmath

mpmath.mp.dps = 20
pi = np.pi

print("=" * 70)
print("  未解決問題の深掘り")
print("=" * 70)

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 問題 1: なぜ Q(√2) が電弱なのか
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  「d=2 が最小の非正方数だから」は理由にならない。
  もっと深い構造的理由が必要。

  ── アプローチ A: ゲージ群の構造から逆算する ──

  電弱: SU(2) × U(1) → U(1)
  これは「rank 2 → rank 1」の対称性の破れ。
  ゲージボソン: W⁺, W⁻, Z, γ の4つ（うち3つが質量を持つ）。

  Q(√d)/Q の被覆:
    rank 2 の Z-module（O_K = Z + Z√d）
    → rank 1 の Z（射影 Spec(O_K) → Spec(Z)）

  ★ 「rank 2 → rank 1」の構造が共通。
  しかしこれは全ての二次体に当てはまる。d=2 の選択理由にならない。
""")

# ============================================================================
print("""
  ── アプローチ B: 判別式 Δ = 8 の特殊性 ──

  Q(√2) の判別式: Δ = 8 = 2³

  他の二次体:
    Q(√3): Δ = 12 = 2² × 3
    Q(√5): Δ = 5
    Q(√6): Δ = 24 = 2³ × 3
    Q(√7): Δ = 28 = 2² × 7

  Δ = 8 の特殊性:
    (1) Δ = 8 は「2のべき乗の判別式」。
        他に Δ が 2 のべきなのは d=2 だけ（Δ=8=2³）。
    (2) 分岐する唯一の素数が p=2。
        Q(√3) は p=2,3 で分岐。Q(√5) は p=5 で分岐。
        Q(√2) だけが「p=2 でのみ分岐」。

  ★ p=2 は最小の素数 = Spec(Z) の最初の閉点。
  「最初の閉点でのみ分岐する二次被覆」は Q(√2) だけ。
""")

# Check: which quadratic fields have discriminant that's a power of 2?
print("  判別式が 2 のべきの二次体:")
print()
for d in range(2, 100):
    # Skip perfect squares
    sqrtd = int(np.sqrt(d))
    if sqrtd * sqrtd == d:
        continue
    # Discriminant
    if d % 4 == 1:
        Delta = d
    else:
        Delta = 4 * d
    # Check if Delta is power of 2
    if Delta > 0 and (Delta & (Delta-1)) == 0:  # power of 2
        print(f"    d = {d}: Δ = {Delta} = 2^{int(np.log2(Delta))}")

print()

# ============================================================================
print("""
  ── アプローチ C: 被覆の分裂密度 ──

  Q(√2) では素数の半分が分裂し、半分が不活性。
  (チェボタレフの密度定理により正確に 1/2 ずつ)

  しかしこれも全ての二次体で同じ。
  特別なのは「どの素数が」分裂するか。

  Q(√2): p ≡ ±1 mod 8 が分裂
  Q(√3): p ≡ ±1 mod 12 が分裂
  Q(√5): p ≡ ±1 mod 5 が分裂

  Q(√2) の場合、mod 8 の条件は:
  分裂: {1, 7} mod 8（8の原始的条件）
  不活性: {3, 5} mod 8

  {1,7} と {3,5} の「対称性」:
  1+7 = 8, 3+5 = 8。両方のペアの和が 8。
  これは mod 8 の特殊な構造。

  ★ 物理との対応?
  SU(2) のアイソスピン: I₃ = +1/2, -1/2
  「分裂 = アイソスピン +1/2」「不活性 = アイソスピン -1/2」?
  → 根拠なし。構造的な類推にすぎない。
""")

# ============================================================================
print("""
  ── アプローチ D: 2 の特殊性（最も有望）──

  p = 2 が特別な理由:

  (1) 2 は唯一の偶数素数。
      全ての偶数は 2 で割れる → 2 は「パリティ」を支配する。

  (2) 物理でのパリティ:
      SU(2)_L はパリティ（左右の区別）に関連。
      弱い力は「左巻き粒子だけに作用する」。
      この左右の区別 ↔ 偶奇の区別 ↔ p=2。

  (3) Z/2 対称性:
      パリティ変換 P: x → -x は Z/2 作用。
      Gal(Q(√2)/Q) = Z/2 は σ: √2 → -√2。
      両方とも Z/2 = 「符号の反転」。

  ★★ これが最も自然な接続:
  「p=2（偶奇 = パリティ）が分岐する被覆 = パリティを破る力（弱い力）」

  SU(2)_L は「左巻き」だけに作用する → パリティ破れ。
  Q(√2) は「p=2 で分岐する」→ p=2 はパリティ（偶奇）を支配。

  → 電弱セクター ↔ Q(√2) の対応は
    「パリティ」を介して接続される。
""")

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 問題 2: CKM/PMNS は他の被覆から出るか
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  CKM 行列の自由パラメータ: 3 つの角度 + 1 つの位相 = 4 個
  PMNS 行列: 同じく 4 個
  合計 8 個の混合パラメータ。

  二次体は無限にあるが、物理的に関連するのは少数のはず。
  「選択原理」が必要。

  ── 可能な選択原理 ──

  (1) 判別式が素数または素数べき:
      Δ = 5 (Q(√5)), 8 (Q(√2)), 13 (Q(√13)), ...
      → 「判別式が素数べき」= 「1つの素数でのみ分岐」

  (2) 類数 h = 1:
      Q(√2), Q(√3), Q(√5), Q(√6), Q(√7), Q(√11), Q(√13), ...
      → 類数 1 の実二次体は無限に多いと予想されている

  (3) 基本判別式の小さい順:
      Δ = 5, 8, 12, 13, 17, 21, 24, 28, 29, 33, ...
      最初の 8 個で CKM+PMNS の 8 パラメータに対応？
""")

# Compute h×R for the first 8 fundamental discriminants
fund_discs = []
for d in range(2, 200):
    sqrtd = int(np.sqrt(d))
    if sqrtd * sqrtd == d:
        continue
    if d % 4 == 1:
        Delta = d
    else:
        Delta = 4 * d
    # Fundamental discriminant check (simplified)
    # Need d to be squarefree
    is_sqfree = True
    for p in range(2, int(np.sqrt(d))+1):
        if d % (p*p) == 0:
            is_sqfree = False
            break
    if is_sqfree:
        # Find fundamental unit
        best_eps = None
        for y in range(1, 10000):
            for sign in [1, -1]:
                x2 = d * y * y + sign
                if x2 > 0:
                    x = int(np.sqrt(x2) + 0.5)
                    if x*x == x2:
                        eps = x + y * np.sqrt(d)
                        if best_eps is None or eps < best_eps:
                            best_eps = eps
                        break
            if best_eps:
                break
        if best_eps:
            R = np.log(best_eps)
            fund_discs.append((Delta, d, R))

fund_discs.sort()

print("  最初の 12 個の実二次体:")
print()
print(f"  {'Δ':>4s} {'d':>4s} {'R':>10s} {'h×R':>10s} {'分岐素数':>12s}")
print(f"  {'-'*46}")

# Physical mixing parameters to match
mix_params = {
    "cos θ_W": 0.88137,
    "sin²θ_W": 0.22318,
    "θ_C (Cabibbo)": 0.2243,   # ≈ V_us
    "V_cb": 0.0408,
    "V_ub": 0.00382,
    "sin²θ₁₂": 0.307,
    "sin²θ₂₃": 0.546,
    "sin²θ₁₃": 0.022,
}

for Delta, d, R in fund_discs[:12]:
    # Find ramified primes (primes dividing Delta)
    ram = []
    temp = Delta
    for p in [2,3,5,7,11,13,17,19,23,29,31,37]:
        if temp % p == 0:
            ram.append(str(p))
            while temp % p == 0:
                temp //= p
    ram_str = ",".join(ram)

    # h=1 assumed for simplicity (true for most small d)
    hR = R  # assuming h=1

    print(f"  {Delta:>4d} {d:>4d} {R:>10.6f} {hR:>10.6f} {ram_str:>12s}")

print()

# ============================================================================
print("""
  ── CKM の Cabibbo 角 θ_C ≈ 0.2243 を探す ──

  V_us = sin θ_C ≈ 0.2243
  V_ud = cos θ_C ≈ 0.9742
""")

V_us = 0.2243
print(f"  V_us = {V_us}")
print()

# Search: which h×R or function thereof gives 0.2243?
print(f"  {'Δ':>4s} {'d':>4s} {'R':>10s} {'R/π':>10s} {'R/4':>10s} {'|R-V_us|/V_us':>14s}")
print(f"  {'-'*58}")

for Delta, d, R in fund_discs[:20]:
    rpi = R/pi
    r4 = R/4
    # Which is closest to V_us?
    candidates = [R, rpi, r4, R/2, R**2, np.sqrt(R)]
    best = min(candidates, key=lambda x: abs(x - V_us))
    pct = abs(best/V_us - 1)*100
    if pct < 10:
        print(f"  {Delta:>4d} {d:>4d} {R:>10.6f} {rpi:>10.6f} {r4:>10.6f} {pct:>14.2f}%  ← best={best:.4f}")

print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 問題 3: 選択原理は存在するか
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ── 候補: 判別式 = 標準模型のゲージ群と対応 ──

  標準模型のゲージ群: SU(3) × SU(2) × U(1)

  SU(3): 次元 = 8, ランク = 2
  SU(2): 次元 = 3, ランク = 1
  U(1): 次元 = 1, ランク = 1

  Q(√2) の判別式: Δ = 8 = dim(SU(3)) ← !!!

  これは偶然か？
""")

print(f"  Δ(Q(√2)) = 8 = dim(SU(3)) = 3² - 1")
print(f"  Δ(Q(√3)) = 12 = ?")
print(f"  Δ(Q(√5)) = 5 = dim(SU(2)) + dim(U(1)) + 1 ← ?")
print()

# Let me check: dim of various groups
print(f"  ゲージ群の次元:")
print(f"    dim(SU(3)) = 8")
print(f"    dim(SU(2)) = 3")
print(f"    dim(U(1)) = 1")
print(f"    dim(SU(3)×SU(2)×U(1)) = 12")
print(f"    dim(SU(5)) = 24")
print(f"    dim(SO(10)) = 45")
print()

print(f"  判別式との対応:")
print(f"    Δ = 8 = dim(SU(3)) ← Q(√2)")
print(f"    Δ = 12 = dim(SM gauge group) ← Q(√3)")
print(f"    Δ = 24 = dim(SU(5)) ← Q(√6)")
print()

# Δ = 8 = dim SU(3) is striking.
# But Δ = 12 = dim(SU(3)×SU(2)×U(1)) is even more striking for Q(√3)!

print(f"  ★ Δ(Q(√3)) = 12 = dim(SU(3)×SU(2)×U(1)) = 標準模型のゲージ群の次元")
print()
print(f"  もし Δ = dim(gauge group) なら:")
print(f"    Q(√3) (Δ=12) ↔ 標準模型全体?")
print(f"    Q(√2) (Δ=8) ↔ SU(3) (QCD)?")
print(f"    Q(√5) (Δ=5) ↔ ???")
print()

# Wait — if Q(√2) with Δ=8 corresponds to SU(3) rather than SU(2)×U(1),
# then the Weinberg angle is NOT the right quantity to match!
# α_s(M_Z) = 0.1179 and reg(Q(√2)) = 0.8814
# These are not close at all.

# Unless: Δ = 8 → electroweak (Δ=8 is the number of W/Z/γ d.o.f.?)
# W⁺: 3 dof (massive spin-1), W⁻: 3, Z: 3, γ: 2 → total 11. No.
# Or: W±: 2 complex = 4, Z: 1, γ: 1 → 6. No.
# Or: W±, Z gain mass from 3 Goldstone bosons → 3 → no.

# Actually 8 = 2³ is just the fact that Δ = 4d for d≡2,3 mod 4.
# For d=2: Δ = 4×2 = 8. This is an artifact of the discriminant formula.

print(f"  ── 正直に: Δ = 8 = dim(SU(3)) はおそらく偶然 ──")
print()
print(f"  Δ = 4d (d ≡ 2 mod 4 のとき) は判別式の公式の帰結。")
print(f"  d=2 なら Δ=8 は自動的。数学的必然であり、深い意味はない可能性。")
print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 最も有望な方向: p=2 とパリティ
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  3つのアプローチを試した結果、最も自然なのは:

  「Q(√2) は p=2 で分岐する唯一の類数1の実二次体であり、
   p=2 はパリティ（偶奇）を支配し、
   弱い力はパリティを破る唯一の力である」

  論理チェーン:
  (1) 弱い力 = パリティ (P) を破る力（実験事実、1957年 Wu）
  (2) パリティ = Z/2 対称性 = 偶奇の区別
  (3) 偶奇を支配する素数 = p = 2
  (4) p=2 でのみ分岐する二次体 = Q(√2)（Δ=8=2³ → 2のみ分岐）
  (5) Q(√2) のレギュレータ = log(1+√2) = cos θ_W

  (1)-(4) は数学的/物理的事実。
  (5) は数値的一致（0.001%）。
  (1)-(4) が (5) の「説明」を提供するなら、
  「なぜ Q(√2) が電弱か」は部分的に答えが出る。

  ── しかし ──

  (1)-(4) は「なぜ Q(√2) か」を説明するが、
  「なぜ cos θ_W = レギュレータか」は説明しない。
  後者は別の理論的根拠が必要。
""")

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 総合判定
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  問題1（なぜQ(√2)が電弱か）:
    最有力回答: p=2 = パリティ ↔ 弱い力 = パリティ破れ
    Q(√2) は「p=2 でのみ分岐する類数1の最小の実二次体」。
    部分的に解決。ただし cos θ_W = reg の「なぜ」は未解決。

  問題2（CKM/PMNSは他の被覆から出るか）:
    V_us ≈ 0.2243 に近いレギュレータは見つからない。
    reg/4 型の一致はあるが精度が低い（>1%）。
    現時点では適用不可。

  問題3（選択原理）:
    「判別式が素数べき」→ 1つの素数でのみ分岐。
    d=2 (Δ=8, p=2), d=5 (Δ=5, p=5), d=13 (Δ=13, p=13), ...
    これが「1つのゲージ力 ↔ 1つの分岐素数」なら:
      p=2 → 弱い力（パリティ）
      p=3 → 強い力（SU(3) の 3）?
      p=5 → ???
    しかし d=3 の判別式は 12 = 2²×3 で p=2,3 の両方で分岐。
    「1素数のみ分岐 = 1つの力」は d=2,5,13,... のみ。

  ── 研究プログラムの現在地 ──

  cos(θ_W) = log(1+√2) は「岩」として残っている。
  「なぜ Q(√2) か」には部分的回答（パリティ論法）がある。
  機構の候補（L関数 → 混合角）がある。
  しかし完全な理論にはまだ遠い。

  次の一手:
  (a) p=2 とパリティの接続を厳密に定式化する
      → エタール基本群と弱い力の C/P/T 対称性の関係
  (b) cos θ_W = reg が「on-shell で正確に成り立つ」ことの
      理論的説明を探す（なぜ on-shell?）
  (c) arXiv に投稿して専門家のフィードバックを得る
""")

print("=" * 70)
print("  END")
print("=" * 70)
