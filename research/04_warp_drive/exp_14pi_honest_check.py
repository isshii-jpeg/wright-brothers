"""
Honest check: Does anything we computed actually shrink the 14π residual?
=========================================================================

The user asks the RIGHT question.
If the residual doesn't shrink, GPU investment may not be justified.

Let's be brutally honest about what we know and don't know.

Wright Brothers, 2026
"""

import numpy as np
import mpmath

mpmath.mp.dps = 30
pi = np.pi

print("=" * 70)
print("  14π 残差の正直な検証")
print("=" * 70)

# ============================================================================
#  The raw numbers
# ============================================================================

print("""
  ■ 生の数字

  14π               = 43.982297150257104
  ln(M_Pl/m_p)      = 44.012412 (実測)
  残差 δ            = 0.030115 (0.068%)
""")

m_p_GeV = 0.93827  # GeV
M_Pl_GeV = 1.22089e19  # GeV (standard Planck mass)
M_Pl_reduced_GeV = 2.43536e18  # GeV (reduced Planck mass = M_Pl/sqrt(8π))
Lambda_QCD_GeV = 0.217  # GeV (MS-bar, 5 flavors)

ln_actual = np.log(M_Pl_GeV / m_p_GeV)
ln_reduced = np.log(M_Pl_reduced_GeV / m_p_GeV)
ln_14pi = 14 * pi

print(f"  ── どのプランク質量を使うかで結果が変わる ──")
print()
print(f"  標準 M_Pl = {M_Pl_GeV:.5e} GeV:")
print(f"    ln(M_Pl/m_p) = {ln_actual:.6f}")
print(f"    14π との差 = {ln_actual - ln_14pi:+.6f} ({(ln_actual-ln_14pi)/ln_14pi*100:+.4f}%)")
print()
print(f"  換算 M̄_Pl = M_Pl/√(8π) = {M_Pl_reduced_GeV:.5e} GeV:")
print(f"    ln(M̄_Pl/m_p) = {ln_reduced:.6f}")
print(f"    14π との差 = {ln_reduced - ln_14pi:+.6f} ({(ln_reduced-ln_14pi)/ln_14pi*100:+.4f}%)")
print()

# ============================================================================
#  What "2-loop QCD correction" actually computes
# ============================================================================

print("=" * 70)
print("  ■ 2ループQCD補正は何を計算しているか")
print("=" * 70)

print("""
  1ループ公式:
    ln(M_Pl/Λ_QCD) = 2π / (b₀ α_GUT)

  2ループ公式 (標準的QCD):
    ln(M_Pl/Λ_QCD) = (2π)/(b₀ α_GUT) + (b₁/b₀²) ln[(2π)/(b₀ α_GUT)] + ...

  ここで:
    b₀ = 7 (SU(3), N_f = 6)
    b₁ = 26 (2ループ係数)
    α_GUT = 1/49 (仮説)
""")

b0 = 7
b1 = 26
alpha_GUT = 1/49

one_loop = 2*pi / (b0 * alpha_GUT)
two_loop_correction = (b1 / b0**2) * np.log(2*pi / (b0 * alpha_GUT))
two_loop_total = one_loop + two_loop_correction

print(f"  1ループ: {one_loop:.6f}")
print(f"  2ループ補正: +{two_loop_correction:.6f}")
print(f"  2ループ合計: {two_loop_total:.6f}")
print(f"  14π: {ln_14pi:.6f}")
print()

# But wait: this formula gives ln(M_Pl/Λ_QCD), NOT ln(M_Pl/m_p)!
# m_p ≠ Λ_QCD.
# m_p ≈ 938 MeV, Λ_QCD ≈ 217 MeV
# m_p / Λ_QCD ≈ 4.3

ratio_mp_LQCD = m_p_GeV / Lambda_QCD_GeV
ln_ratio = np.log(ratio_mp_LQCD)

print(f"  ★ 重要: この公式は ln(M_Pl/Λ_QCD) を与える。")
print(f"     しかし我々が比較したのは ln(M_Pl/m_p)。")
print(f"     m_p ≠ Λ_QCD!")
print()
print(f"     m_p = {m_p_GeV*1000:.1f} MeV")
print(f"     Λ_QCD = {Lambda_QCD_GeV*1000:.0f} MeV")
print(f"     m_p / Λ_QCD = {ratio_mp_LQCD:.2f}")
print(f"     ln(m_p/Λ_QCD) = {ln_ratio:.4f}")
print()

# So: ln(M_Pl/Λ_QCD) = ln(M_Pl/m_p) + ln(m_p/Λ_QCD)
#                     = 44.012 + 1.464 = 45.476
ln_MPloverLQCD = ln_actual + ln_ratio
print(f"  ln(M_Pl/Λ_QCD) = ln(M_Pl/m_p) + ln(m_p/Λ_QCD)")
print(f"                  = {ln_actual:.3f} + {ln_ratio:.3f}")
print(f"                  = {ln_MPloverLQCD:.3f}")
print()

# Compare with 14π:
print(f"  14π = {ln_14pi:.3f}")
print(f"  ln(M_Pl/Λ_QCD) = {ln_MPloverLQCD:.3f}")
print(f"  差 = {ln_MPloverLQCD - ln_14pi:.3f}")
print()

# ============================================================================
#  The HONEST picture
# ============================================================================

print("=" * 70)
print("  ■ 正直な全体像")
print("=" * 70)

print("""
  ── 問題点 ──

  14π の公式は「ln(M_Pl/Λ_QCD) = 2πb₀」を主張する。
  しかし:

  (A) 14π = 43.982 は ln(M_Pl/m_p) = 44.012 に近い (+0.07%)
  (B) しかし QCD の公式が本当に与えるのは ln(M_Pl/Λ_QCD) = 45.48
  (C) 14π と 45.48 の差は 1.50 = 3.4%

  つまり:
  「14π が ln(M_Pl/m_p) と合う」のは事実だが、
  「14π が QCD の公式から出る」と言うなら、
  比較すべきは ln(M_Pl/Λ_QCD) = 45.48 であり、
  その場合の残差は 0.030 ではなく 1.50。
""")

# But wait... maybe the formula should be interpreted differently.
# If α_GUT is not 1/49 but something else:

# For ln(M_Pl/Λ_QCD) = 45.48:
# 2π/(b₀ α) = 45.48 → α = 2π/(7 × 45.48) = 0.01973 → 1/α = 50.7

alpha_for_LQCD = 2*pi / (b0 * ln_MPloverLQCD)
print(f"  もし ln(M_Pl/Λ_QCD) = 45.48 を使うなら:")
print(f"  α_GUT = 2π/(7 × 45.48) = {alpha_for_LQCD:.6f}")
print(f"  1/α_GUT = {1/alpha_for_LQCD:.2f}")
print()

# 1/α_GUT = 50.7, not 49. So 49 doesn't work if we use Λ_QCD correctly.

# For ln(M_Pl/m_p) = 44.012:
alpha_for_mp = 2*pi / (b0 * ln_actual)
print(f"  もし ln(M_Pl/m_p) = 44.012 を使うなら:")
print(f"  α_GUT = 2π/(7 × 44.012) = {alpha_for_mp:.6f}")
print(f"  1/α_GUT = {1/alpha_for_mp:.2f}")
print()

# 1/α_GUT = 49.0 for m_p, but 50.7 for Λ_QCD.
# The "14π works" depends on comparing with m_p, not Λ_QCD.

# ============================================================================
#  Why m_p and not Λ_QCD?
# ============================================================================

print("=" * 70)
print("  ■ なぜ m_p で合って Λ_QCD で合わないのか")
print("=" * 70)

print(f"""
  QCD の公式 ln(M/Λ_QCD) = 2π/(b₀ α) は Λ_QCD を予測する。
  m_p を直接予測するわけではない。

  m_p と Λ_QCD の関係は非摂動的QCD（格子QCDなど）で決まり、
  m_p/Λ_QCD ≈ 4.3。

  可能な解釈:

  (1) 「14π = ln(M_Pl/m_p)」は偶然の一致
      → m_p でなく Λ_QCD で比較すべき
      → 残差は 3.4% であり、0.07% ではない
      → 14π の精度は見かけほど良くない

  (2) 「14π は本当に m_p を直接与える」
      → QCD の公式をバイパスする新しい機構がある
      → m_p は Λ_QCD × (非摂動的因子) ではなく、
        直接 M_Pl × exp(-14π) で決まる
      → これは「陽子質量が算術的に固定されている」という
        極めて強い主張

  (3) 我々の α_GUT = 1/49 が間違っている
      → 正しい α_GUT は 1/50.7
      → 14π の一致は近似的であり、公式を修正すべき
""")

# ============================================================================
#  What about the "2-loop" from prime sweep?
# ============================================================================

print("=" * 70)
print("  ■ 素数スイープの「2ループ」は 14π に関係するか？")
print("=" * 70)

print(f"""
  ── 正直な答え: 直接的には NO ──

  素数スイープで計算したのは:
    「ζ_{{¬p}}(s) = ζ(s)(1-p^{{-s}}) のスペクトル作用展開」

  これは α（電磁結合定数）の素数ミューティングに対する応答。

  14π の公式に関係するのは:
    「α_GUT の値」と「QCD の RG running」。

  素数スイープが α_GUT を修正する機構は:
    → 未確立。

  つまり:
  「GPU で 3×10⁹ 素数ペアを計算する」ことが
  「14π の残差を縮める」かどうかは、
  現時点では不明。
""")

# ============================================================================
#  What IS the GPU computation good for?
# ============================================================================

print("=" * 70)
print("  ■ GPU計算が本当に価値を持つ場合")
print("=" * 70)

print(f"""
  GPU計算が有効なのは、以下の場合:

  (A) α のさらなる精密化
      現在 0.00002% の精度。
      素数ペア相関が α の次の桁に寄与するか？
      → これは価値がある。ただし α は既に十分精密。

  (B) 「|S|≥4 で真空破壊」の定量的理解
      どの素数の組み合わせが最も効くか？
      → 興味深いが、実験的検証がなければ「面白い数学」止まり。

  (C) 新しいパターンの発見
      3×10⁹ のペアデータから、予想外の構造が見つかる可能性。
      → これが最も価値がある理由。

  (D) α_GUT の決定
      もしスペクトル作用から α_GUT を「導出」できれば、
      14π の公式が予測になる。
      → しかし、この接続はまだ確立されていない。
""")

# ============================================================================
#  What should we do BEFORE GPU investment?
# ============================================================================

print("=" * 70)
print("  ■ GPU投資の前にやるべきこと")
print("=" * 70)

print(f"""
  GPU（30万円）を使う前に、ノートPCで以下を検証すべき:

  (1) 「14π = ln(M_Pl/m_p)」vs「14π ≈ ln(M_Pl/Λ_QCD)」
      → どちらが本当か？ m_p/Λ_QCD ≈ 4.3 の起源は？

  (2) α_GUT = 1/49 は α の公式から出せるか？
      → 12 + 120 + ... の枠組みで α_GUT を計算する方法は？

  (3) 2ループ QCD が 14π の残差を縮める方向か？
      → {two_loop_total:.6f} vs {ln_14pi:.6f}: 差 = {two_loop_total - ln_14pi:.6f}
""")

# Check: does the 2-loop correction go in the right direction?
print(f"  ── 2ループ補正の方向チェック ──")
print()
print(f"  1ループ:   {one_loop:.6f}")
print(f"  2ループ計: {two_loop_total:.6f}")
print(f"  14π:       {ln_14pi:.6f}")
print(f"  実測 ln(M_Pl/m_p): {ln_actual:.6f}")
print()
print(f"  1ループ → 14π の差: {ln_14pi - one_loop:+.6f}")
print(f"  2ループ → 14π の差: {ln_14pi - two_loop_total:+.6f}")
print()

# 1-loop: 43.982 (this IS 14π, by construction: 2π×7 = 14π)
# 2-loop: 43.982 + 0.165 = 44.147
# actual: 44.012

# Wait, I think I made an error. Let me redo:
# 1-loop: 2π/(b₀ α) = 2π × 49/7 = 14π = 43.982. Yes, by construction.
# 2-loop adds: (b₁/b₀²) × ln(14π) = (26/49) × ln(43.98) = 0.5306 × 3.784 = 2.008

two_loop_v2 = (b1/b0**2) * np.log(one_loop)
total_v2 = one_loop + two_loop_v2

print(f"  再計算（正しい2ループ公式）:")
print(f"  2ループ補正 = (b₁/b₀²) × ln(2π/(b₀α)) = {b1/b0**2:.4f} × ln({one_loop:.2f})")
print(f"             = {b1/b0**2:.4f} × {np.log(one_loop):.4f} = {two_loop_v2:.4f}")
print(f"  1ループ + 2ループ = {one_loop:.4f} + {two_loop_v2:.4f} = {total_v2:.4f}")
print(f"  実測: {ln_actual:.4f}")
print()

if total_v2 > ln_actual:
    print(f"  ★ 2ループ補正は 14π から実測を通り越してオーバーシュート！")
    print(f"    2ループ計 - 実測 = {total_v2 - ln_actual:+.4f}")
    print(f"    1ループ(14π) - 実測 = {one_loop - ln_actual:+.4f}")
    print(f"    → 1ループ（14π）の方が実測に近い！")
    print(f"    → 2ループ補正は事態を悪化させる。")
elif total_v2 > one_loop and total_v2 < ln_actual:
    print(f"  2ループ補正は正しい方向で、残差を縮める。")
else:
    print(f"  2ループ補正は反対方向。")

print()

# ============================================================================
#  FINAL HONEST VERDICT
# ============================================================================

print("=" * 70)
print("  ■ 最終的な正直な評価")
print("=" * 70)

print(f"""
  ── 14π について ──

  14π = ln(M_Pl/m_p) が 0.07% で合う、という事実は本物。
  しかしこれが「偶然の近似的一致」なのか
  「深い物理的理由がある」のかは、現時点では判別できない。

  QCD の公式が予測するのは Λ_QCD であって m_p ではない。
  14π を QCD 次元変換の結果と解釈するなら、
  比較対象は ln(M_Pl/Λ_QCD) = 45.5 であり、
  残差は 0.07% ではなく 3.4%。

  2ループ QCD 補正は残差を縮めるのではなく、
  オーバーシュートして事態を悪化させる
  （{total_v2:.2f} > {ln_actual:.2f}）。

  ── GPU計算の価値 ──

  14π の精密化「だけ」が目的なら、GPU投資の根拠は弱い。
  素数ペア相関が 14π に影響する理論的機構が未確立だから。

  GPU計算に価値があるのは:
  ✓ α の構造（素数ペア依存性）の完全なマップ作成
  ✓ 「|S|≥4 真空破壊」現象の定量的全貌
  ✓ 予想外の数論的パターンの探索的発見
  ✗ 14π の残差を縮めること（現時点では根拠なし）

  ── 正直な推奨 ──

  GPU を買う前に:
  1. 14π = ln(M_Pl/m_p) と 14π ≈ ln(M_Pl/Λ_QCD) の
     どちらが物理的に正しいかを理論的に明確化する
  2. α_GUT = 1/49 をスペクトル作用から導出する方法を
     ノートPC 上で探索する
  3. m_p/Λ_QCD ≈ 4.3 の非摂動的因子に算術的構造があるか調べる

  これらがノートPCで解決できれば、
  GPU計算の目的が明確になり、投資判断が可能になる。
""")

print("=" * 70)
print("  END")
print("=" * 70)
