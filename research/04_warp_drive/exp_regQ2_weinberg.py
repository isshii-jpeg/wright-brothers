"""
Deep dive: reg(Q(√2)) = log(1+√2) ≈ m_W/m_Z = cos(θ_W)
==========================================================

The Arakelov scan found:
  log(1+√2) = 0.88137...
  m_W/m_Z   = 0.88153...
  Agreement: 0.018%

Is this real or coincidence? Stress-test from every angle.

Wright Brothers, 2026
"""

import numpy as np
import mpmath

mpmath.mp.dps = 30
pi = np.pi

# The two numbers
reg_Q2 = np.log(1 + np.sqrt(2))  # = arsinh(1)
mW_over_mZ = 80.3692 / 91.1876  # PDG 2024 values
cos_theta_W = mW_over_mZ
sin2_theta_W = 1 - cos_theta_W**2

print("=" * 70)
print("  reg(Q(√2)) vs m_W/m_Z 深掘り")
print("=" * 70)

# ============================================================================
print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 数値の確認
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  算術側:
    reg(Q(√2)) = log(1+√2) = {reg_Q2:.15f}
    = arsinh(1) = ln(1 + √2)
    これは Q(√2) = Q(銀比) の基本単元 ε = 1+√2 の対数。

  物理側:
    m_W = 80.3692 ± 0.0133 GeV (PDG 2024)
    m_Z = 91.1876 ± 0.0021 GeV (PDG 2024)
    m_W/m_Z = {mW_over_mZ:.15f}
    cos(θ_W) = m_W/m_Z（tree level）

  比較:
    差 = {mW_over_mZ - reg_Q2:.6e}
    相対差 = {(mW_over_mZ/reg_Q2 - 1)*100:.4f}%
""")

# ============================================================================
print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 両者の数学的正体
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ── log(1+√2) の数学 ──

  (1) Q(√2) のレギュレータ
      Q(√2) の整数環 Z[√2] の単元群は <-1, 1+√2> で生成。
      基本単元 ε = 1+√2, ε⁻¹ = √2-1。
      レギュレータ R = log|ε| = log(1+√2)。

  (2) arsinh(1) = 逆双曲線正弦関数
      sinh(x) = (eˣ-e⁻ˣ)/2 = 1 のとき x = arsinh(1) = log(1+√2)。

  (3) 正方形の対角線
      1+√2 は「正方形の辺+対角線」。
      正八角形の内角に関連。
      銀比 δ_S = 1+√2 ≈ 2.414 （黄金比 φ = (1+√5)/2 ≈ 1.618 の「兄弟」）。

  (4) 連分数
      √2 = [1; 2, 2, 2, ...] （最も単純な無限連分数の一つ）。
      1+√2 = [2; 2, 2, 2, ...]。

  ── cos(θ_W) の物理 ──

  (1) ワインバーグ角 θ_W は電弱統一の混合角。
      cos(θ_W) = m_W/m_Z = g₂/√(g₁² + g₂²)
      ここで g₁, g₂ は U(1)_Y, SU(2)_L の結合定数。

  (2) tree level: sin²θ_W = 1 - (m_W/m_Z)²
      = {sin2_theta_W:.6f}
      実測: 0.23121 ± 0.00004 (MS-bar, at M_Z)

  (3) GUT 予測: sin²θ_W = 3/8 = 0.375（統一スケールで）。
      running で低エネルギーでは 0.231 に下がる。
""")

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ テスト 1: 精度は本物か
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

# m_W/m_Z has experimental uncertainty
mW = 80.3692  # GeV
mW_err = 0.0133
mZ = 91.1876
mZ_err = 0.0021

# Error propagation: δ(m_W/m_Z) = (m_W/m_Z) √((δm_W/m_W)² + (δm_Z/m_Z)²)
ratio_err = mW_over_mZ * np.sqrt((mW_err/mW)**2 + (mZ_err/mZ)**2)

z_score = (reg_Q2 - mW_over_mZ) / ratio_err
print(f"  m_W/m_Z = {mW_over_mZ:.6f} ± {ratio_err:.6f}")
print(f"  log(1+√2) = {reg_Q2:.6f}")
print(f"  差 = {reg_Q2 - mW_over_mZ:.6f}")
print(f"  z-score = {z_score:.2f}σ")
print()

if abs(z_score) < 2:
    print(f"  → 実験誤差の {abs(z_score):.1f}σ 以内。統計的に整合。")
elif abs(z_score) < 3:
    print(f"  → {abs(z_score):.1f}σ。微妙。")
else:
    print(f"  → {abs(z_score):.1f}σ。不整合。")

print()

# But: m_W/m_Z at tree level vs with radiative corrections
# The RUNNING of θ_W means the "physical" value depends on scale
# At M_Z (on-shell): sin²θ_W^{on-shell} = 1-(m_W/m_Z)² = 0.2229
# MS-bar at M_Z: sin²θ_W = 0.23121
# These differ by ~3.6%

sin2_onshell = 1 - mW_over_mZ**2
sin2_msbar = 0.23121

print(f"  ── スキーム依存性 ──")
print()
print(f"  sin²θ_W (on-shell) = 1-(m_W/m_Z)² = {sin2_onshell:.6f}")
print(f"  sin²θ_W (MS-bar, M_Z) = {sin2_msbar:.6f}")
print(f"  差 = {sin2_msbar - sin2_onshell:.6f} ({(sin2_msbar/sin2_onshell-1)*100:.1f}%)")
print()

# cos(θ_W) in MS-bar scheme:
cos_msbar = np.sqrt(1 - sin2_msbar)
print(f"  cos θ_W (on-shell) = m_W/m_Z = {mW_over_mZ:.6f}")
print(f"  cos θ_W (MS-bar)   = √(1-0.23121) = {cos_msbar:.6f}")
print(f"  log(1+√2)          = {reg_Q2:.6f}")
print()
print(f"  on-shell との差: {(reg_Q2/mW_over_mZ - 1)*100:+.4f}%")
print(f"  MS-bar との差:   {(reg_Q2/cos_msbar - 1)*100:+.4f}%")
print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ テスト 2: log(1+√2) が出る理論的理由はあるか
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

# In the Standard Model, cos(θ_W) is NOT predicted.
# It's a free parameter (equivalently g₁/g₂ is free).
# So any "prediction" of cos(θ_W) from number theory would be profound.

# In GUT theories:
# At M_GUT: sin²θ_W = 3/8 → cos θ_W = √(5/8) = 0.7906
# RG running to M_Z: cos θ_W → 0.8815
# The running involves α, α_s, and the particle content.

# Question: could the RG running from √(5/8) to 0.8815 give log(1+√2)?

gut_cos = np.sqrt(5/8)
print(f"  GUT 値: cos θ_W(M_GUT) = √(5/8) = {gut_cos:.6f}")
print(f"  低エネルギー: cos θ_W(M_Z) = {mW_over_mZ:.6f}")
print(f"  RG running 量: {mW_over_mZ - gut_cos:.6f}")
print(f"  running / GUT値 = {(mW_over_mZ - gut_cos)/gut_cos:.6f}")
print()

# log(1+√2) / √(5/8) = ?
ratio_gut = reg_Q2 / gut_cos
print(f"  log(1+√2) / √(5/8) = {ratio_gut:.6f}")
print(f"  これは何か？ {ratio_gut:.6f} ≈ ?")
print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ テスト 3: 他のレギュレータと他の物理量
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

# If reg(Q(√2)) = cos θ_W, then do other regulators match other quantities?
regs = {
    2: np.log(1 + np.sqrt(2)),       # 0.8814
    3: np.log(2 + np.sqrt(3)),       # 1.3169
    5: np.log((1+np.sqrt(5))/2),     # 0.4812 = log(φ)
    6: np.log(5 + 2*np.sqrt(6)),     # 2.2924
    7: np.log(8 + 3*np.sqrt(7)),     # 2.7726
    10: np.log(3 + np.sqrt(10)),     # 1.8184
    11: np.log(10 + 3*np.sqrt(11)),  # 2.9932
    13: np.log((3+np.sqrt(13))/2),   # 1.1948
    14: np.log(15 + 4*np.sqrt(14)),  # 3.3844
    15: np.log(4 + np.sqrt(15)),     # 1.9459
    17: np.log(4 + np.sqrt(17)),     # 2.0947
    19: np.log((170+39*np.sqrt(19))/1 if False else 170+39*np.sqrt(19)),
}
# Fix d=19: fundamental unit of Q(√19) is 170+39√19
regs[19] = np.log(170 + 39*np.sqrt(19))  # much larger

PHYS = {
    "cos θ_W": 0.88153,
    "sin²θ_W": 0.23121,
    "sin θ_W": np.sqrt(0.23121),
    "V_us": 0.2243,
    "V_cb": 0.0422,
    "m_u/m_d": 0.474,
    "m_s/m_d": 20.2,
    "m_c/m_s": 11.7,
    "m_b/m_τ": 2.35,
    "m_τ/m_μ": 16.817,
    "m_μ/m_e": 206.768,
    "m_H/v": 0.510,
    "α_s(M_Z)": 0.1179,
    "1/α": 137.036,
}

print(f"  {'d':>4s} {'reg(Q(√d))':>12s}  最近接物理量")
print(f"  {'-'*60}")

for d in sorted(regs.keys()):
    R = regs[d]
    if R > 100:
        continue
    best_name = ""
    best_pct = 100
    best_pval = 0
    for pname, pval in PHYS.items():
        for v in [R, 1/R]:
            if pval > 0:
                pct = abs(v/pval - 1) * 100
                if pct < best_pct:
                    best_pct = pct
                    best_name = pname
                    best_pval = pval
    print(f"  {d:>4d} {R:>12.6f}  {best_name} = {best_pval:.4f} ({best_pct:+.2f}%)")

print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ テスト 4: log(1+√2) の別の書き方で手がかりを探す
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

# log(1+√2) has MANY equivalent representations:
print(f"  log(1+√2) の等価表現:")
print()
print(f"  (1) arsinh(1) = {np.arcsinh(1):.10f}")
print(f"  (2) arcosh(√2) (≠ log(1+√2)? let's check)")
print(f"      arcosh(√2) = {np.arccosh(np.sqrt(2)):.10f}")
print(f"      log(1+√2) = {reg_Q2:.10f}")
print(f"      → 一致: {'✓' if abs(np.arccosh(np.sqrt(2)) - reg_Q2) < 1e-10 else '✗'}")
print()

# arsinh(1) = arcosh(√2)? Check:
# arcosh(x) = log(x + √(x²-1)), so arcosh(√2) = log(√2 + 1) = log(1+√2). YES!

print(f"  (3) ∫₀¹ 1/√(1+t²) dt = arsinh(1)  （楕円積分の特殊ケース）")
print("  (4) Σ (-1)^n (2n)!/(2^{2n}(n!)²(2n+1)) = arsinh(1)")
print()

# Physical interpretation: arsinh appears in special relativity!
# rapidity φ = arsinh(v/c / √(1-v²/c²))
# For v/c = 1/√2: φ = arsinh(1) = log(1+√2)
print(f"  (5) 特殊相対論: v/c = 1/√2 のときのラピディティ")
print(f"      φ = arsinh(γv/c) where γ = 1/√(1-v²/c²)")
print(f"      v = c/√2 → γ = √2 → γv/c = 1")
print(f"      φ = arsinh(1) = log(1+√2)")
print()
print(f"  ★ v = c/√2 は「光速の 1/√2 倍」= 双曲幾何学での特別な速度。")
print(f"    cos(θ_W) = log(1+√2) ≈ 0.8814 が成り立つなら、")
print(f"    ワインバーグ角は「v = c/√2 のラピディティ」。")
print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ テスト 5: 偶然一致の確率
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

# We tested ~15 regulators against ~14 physical constants.
# That's ~15 × 14 × 2 (including reciprocals) ≈ 420 comparisons.
# The precision is 0.018%.
# Probability of one random match within 0.02% out of 420 trials:
# P(one match at 0.02%) ≈ 1 - (1-0.0004)^420 ≈ 0.154 = 15.4%

n_trials = 15 * 14 * 2
p_single = 2 * 0.0002  # prob of being within 0.02% of a target
p_at_least_one = 1 - (1 - p_single)**n_trials

print(f"  比較回数: ~{n_trials}")
print(f"  各比較での 0.02% 以内の確率: {p_single:.5f}")
print(f"  少なくとも1つ当たる確率: {p_at_least_one:.3f} = {p_at_least_one*100:.1f}%")
print()

# More careful: the 0.018% precision
p_single_2 = 2 * 0.00018
p_at_least_one_2 = 1 - (1 - p_single_2)**n_trials
print(f"  0.018% 以内: P(≥1) = {p_at_least_one_2:.3f} = {p_at_least_one_2*100:.1f}%")
print()

# ============================================================================
print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ テスト 6: cos(θ_W) は running する — どのスケールの値？
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  cos(θ_W) はエネルギースケール μ に依存する:
    μ = M_Z:  cos θ_W = {mW_over_mZ:.6f} (on-shell)
                       = {cos_msbar:.6f} (MS-bar)
    μ = M_GUT: cos θ_W = √(5/8) = {gut_cos:.6f}
    μ = M_Pl:  さらに running...

  log(1+√2) = {reg_Q2:.6f}

  もし log(1+√2) が「特定のスケールでの cos θ_W」なら、
  そのスケールは？
""")

# Solve: at which scale μ does cos θ_W(μ) = log(1+√2)?
# 1-loop running: sin²θ_W(μ) = sin²θ_W(M_Z) + (b/2π) ln(μ/M_Z)
# where b depends on the particle content.

# In SM: dsin²θ_W/d(lnμ) ≈ +0.0036 per unit of ln(μ/M_Z)
# (sin²θ increases with energy)

sin2_target = 1 - reg_Q2**2
sin2_MZ = sin2_onshell  # 0.2229 on-shell
delta_sin2 = sin2_target - sin2_MZ
b_sin2 = 0.0036  # approximate SM coefficient

if b_sin2 != 0:
    ln_mu_MZ = delta_sin2 / b_sin2
    mu_scale = 91.19 * np.exp(ln_mu_MZ)
    print(f"  sin²θ_W の目標値: 1 - log(1+√2)² = {sin2_target:.6f}")
    print(f"  sin²θ_W(M_Z, on-shell) = {sin2_MZ:.6f}")
    print(f"  差 = {delta_sin2:.6f}")
    print(f"  必要な running: {delta_sin2/b_sin2:.2f} units of ln(μ/M_Z)")
    print(f"  対応するスケール: μ ≈ {mu_scale:.2e} GeV")
    print()

# ============================================================================
print(f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 正直な判定
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  reg(Q(√2)) = cos(θ_W) は本物か？

  ── 支持する証拠 ──

  (1) 精度 0.018% は印象的
  (2) reg(Q(√2)) はアラケロフ幾何学の「基本不変量」
  (3) cos(θ_W) は標準模型の「基本パラメータ」
  (4) log(1+√2) = arsinh(1) は双曲幾何学で特別
  (5) Q(√2) は最も単純な実二次体の一つ

  ── 反対する証拠 ──

  (1) ~420 回の比較で 0.02% の一致が出る確率は
      {p_at_least_one_2*100:.0f}%。偶然の可能性が無視できない。
  (2) cos(θ_W) はスキーム（on-shell vs MS-bar）に依存。
      on-shell: 0.88153, MS-bar: 0.87689。
      log(1+√2) = 0.88137 は on-shell に近いが MS-bar からは 0.5% ずれる。
  (3) cos(θ_W) は running する。どのスケールの値かが不明確。
  (4) reg(Q(√2)) と cos(θ_W) を結ぶ物理的機構が不明。

  ── 判定 ──

  偶然確率 ~{p_at_least_one_2*100:.0f}%:
  これは「ありえない偶然」ではないが「よくある偶然」でもない。

  比較として:
    12 + 120 = 132 ≈ 137 → 部分集合探索で偶然確率を評価済み
    14π ≈ ln(M_Pl/m_p)  → Bonferroni 後 ~30%

  reg(Q(√2)) = cos(θ_W) の偶然確率 ~{p_at_least_one_2*100:.0f}% は
  これまでの「一致」の中で最も低い確率（＝最も偶然でなさそう）。

  ★ しかし「偶然でなさそう」と「物理的に意味がある」は別。
    意味があるためには、レギュレータとワインバーグ角を
    結ぶ理論的機構が必要。現時点ではない。

  ── 次のステップ ──

  (a) cos(θ_W) = log(1+√2) を仮定して他の予測を出す。
      例: sin²θ_W = 1 - log(1+√2)² = {1-reg_Q2**2:.6f}
      実験値: 0.22290(on-shell), 0.23121(MS-bar)。
      → on-shell 値 0.22290 と {1-reg_Q2**2:.5f} の差は
        {abs(sin2_onshell - (1-reg_Q2**2)):.5f} = {abs(sin2_onshell-(1-reg_Q2**2))/sin2_onshell*100:.2f}%

  (b) 他の実二次体のレギュレータが他の混合角に対応するか。
      reg(Q(√5)) = log(φ) ≈ V_us?
      → {np.log((1+np.sqrt(5))/2):.4f} vs {0.2243} → 115% off. ✗

  (c) 理論的機構の探索:
      アラケロフ幾何学 → 電弱混合 の接続は、
      Spec(Z[√2]) のエタール被覆と SU(2)×U(1) の
      対称性の破れのパターンに関係する可能性。
""")

print("=" * 70)
print("  END")
print("=" * 70)
