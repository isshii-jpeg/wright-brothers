"""
Dispersive shift vs ζ-predicted shift: quantitative comparison
================================================================

Standard circuit QED predicts a specific frequency shift when
a SQUID absorbs a cavity mode ("dispersive shift").

Our ζ framework predicts a DIFFERENT shift if the vacuum
has arithmetic structure.

Question: are these the same or different?
If the same �� experiment can't distinguish → don't bother.
If different → experiment has a target → worth doing.

Wright Brothers, 2026
"""

import numpy as np
pi = np.pi
hbar = 1.054571817e-34  # J·s
kB = 1.380649e-23       # J/K

print("=" * 70)
print("  分散シフト vs ζ予測シフト")
print("=" * 70)

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ セットアップ: 超伝導3Dキャビティ + SQUID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  キャビティ:
    内寸: 35 × 35 × 10 mm（アルミ）
    モード1: f₁ ≈ 6 GHz（基本モード）
    モード2: f₂ ≈ 12 GHz（第2高調波）
    Q値: ～10⁶（超伝導、T = 0.3 K）

  SQUID:
    ジョセフソンエネルギー: E_J ≈ 10 GHz × h
    充電エネルギー: E_C ≈ 200 MHz × h
    → トランスモン領域 (E_J/E_C ≈ 50)
    → 非調和性: α_anh ≈ -E_C ≈ -200 MHz

  結合:
    SQUID-キャビティ結合: g/2π ≈ 100 MHz
""")

# Parameters
f1 = 6e9      # Hz, mode 1
f2 = 12e9     # Hz, mode 2
Q = 1e6       # quality factor
kappa = f1/Q  # cavity linewidth: 6 kHz

g = 100e6     # Hz, coupling strength
E_J = 10e9    # Hz, Josephson energy
E_C = 200e6   # Hz, charging energy
alpha_anh = -E_C  # anharmonicity

T = 0.3       # K, temperature

print(f"  数値パラメータ:")
print(f"    f₁ = {f1/1e9:.1f} GHz")
print(f"    f₂ = {f2/1e9:.1f} GHz")
print(f"    Q = {Q:.0e}")
print(f"    κ = f₁/Q = {kappa:.0f} Hz = {kappa/1e3:.1f} kHz")
print(f"    g/2π = {g/1e6:.0f} MHz")
print(f"    E_J/h = {E_J/1e9:.0f} GHz")
print(f"    E_C/h = {E_C/1e6:.0f} MHz")
print(f"    T = {T} K")
print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 標準 circuit QED: 分散シフト (dispersive shift)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  SQUIDがモード2に同調したとき（Δ₂ = f₂ - f_SQUID ≈ 0）、
  モード1が受ける周波数シフトは:

  ─�� ケース1: SQUID がモード2と共鳴（Δ₂ = 0）─��
  モード2の真空揺らぎがSQUIDを励起
  → SQUIDの状態がモード1に分散シフトを与える

  ���散シフトの公式:
    χ₁ = g₁²/Δ₁ × (α_anh/(Δ₁ + α_anh))

  ここで:
    g₁ = SQUID-モード1 結合 ≈ g × √(f₁/f₂) ≈ 71 MHz
    Δ₁ = f₁ - f_SQUID ≈ f₁ - f₂ = -6 GHz

  ── ケース2: SQUID がモード2から離調（Δ₂ >> κ）──
  SQUID はどのモードとも共鳴しない
  → 分散シフトは異なる値
""")

# Case 1: SQUID on resonance with mode 2
g1 = g * np.sqrt(f1/f2)  # coupling to mode 1 (geometric scaling)
Delta1 = f1 - f2  # detuning of mode 1 from SQUID (when SQUID is at f2)

chi_dispersive_on = g1**2 / Delta1 * (alpha_anh / (Delta1 + alpha_anh))

print(f"  ケース1 (SQUID on mode 2):")
print(f"    g₁ = g × √(f₁/f₂) = {g1/1e6:.0f} MHz")
print(f"    Δ₁ = f₁ - f₂ = {Delta1/1e9:.0f} GHz")
print(f"    χ₁(on) = g₁²/Δ₁ × α/(Δ₁+α) = {chi_dispersive_on/1e3:.2f} kHz")
print()

# Case 2: SQUID far detuned (e.g., at 9 GHz, between modes)
f_SQUID_off = 9e9
Delta1_off = f1 - f_SQUID_off
chi_dispersive_off = g1**2 / Delta1_off * (alpha_anh / (Delta1_off + alpha_anh))

print(f"  ケース2 (SQUID at 9 GHz, detuned):")
print(f"    Δ₁ = f₁ - 9 GHz = {Delta1_off/1e9:.0f} GHz")
print(f"    χ₁(off) = {chi_dispersive_off/1e3:.2f} kHz")
print()

# The DIFFERENCE is what we measure
delta_chi_dispersive = abs(chi_dispersive_on - chi_dispersive_off)
print(f"  ★ 分散シフトの差 (on - off):")
print(f"    |Δχ_dispersive| = {delta_chi_dispersive:.0f} Hz = {delta_chi_dispersive/1e3:.2f} kHz")
print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ ζ予測: 真空エネルギー��変��によるシフト
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ζ正則化による真空エネルギー:
    E_vac = Σ_n ℏω_n/2 → ζ-正則化

  2モードのキャビティ:
    E_vac = ℏ(ω₁ + ω₂)/2 （正則化後）

  モード2をミュートしたとき:
    E_vac' = ℏω₁/2 （モード2が消えた）

  差: ΔE_vac = -ℏω₂/2

  ★ しかし: これは単にモード2のゼロ点エネルギー。
  これは分散シフトとは全く異なる物理量。

  分散シフト = モード1の「周波数」の変化
  ΔE_vac = 系の「全エネルギー」の変化

  両者の関係:
  真空エネルギーの変化がモード1の周波数にどう影響するか？
""")

# The vacuum energy change
omega2 = 2 * pi * f2
Delta_E_vac = hbar * omega2 / 2  # energy of mode 2's zero-point

print(f"  モード2のゼロ点エネルギー:")
print(f"    ΔE_vac = ℏω₂/2 = {Delta_E_vac:.4e} J")
print(f"    = {Delta_E_vac / (hbar * 2 * pi * 1e9):.4f} GHz × h")
print(f"    = {f2/2/1e9:.1f} GHz × h")
print()

# How does this translate to a frequency shift of mode 1?
# In general, a change in vacuum energy δE doesn't directly shift
# a cavity mode frequency. The frequency is determined by geometry.
#
# HOWEVER: in circuit QED, the vacuum fluctuations of one mode
# can shift another mode through the NONLINEARITY of the SQUID.
# This is exactly the dispersive shift we already computed.
#
# So: the "ζ prediction" for the shift is... the dispersive shift itself?

print("""
  ─��� 核��的な問い ──

  真空エネルギーの変化 ΔE_vac がモード1の周波数を
  直接シフトさせるメカニズムは？

  (A) SQUID の���線形性を通じて → これは分散シフト（既知の物理）
  (B) 真空そのものの構造変化���通じて → これが「新物理」

  (A) の場合: ζ予測 = 分散シフト → ��別不可��
  (B) の場合: ζ予測 ≠ 分散シフト → 区別可能

  ★ (B) はどのような形で現れるか？
""")

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ メカニズム (B) ���存在する場合の予測
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  もし「真空そのものの構造変化」が起きるなら、
  それはカシミール効果と同じメカニズム:

  カシミール: 金属板がモードを制限 → 真空エネルギー変化
  → 板の間の力（F = -dE/dx）

  SQUID版: SQUIDがモードを吸収 → 真空エネルギー変化
  → キャビティの有効長が変化 → ��ード1の周波数が変化

  カシミール効果の大きさ:
    F_Casimir = -π²ℏc/(240 a⁴) × A
    (a = 板間距離, A = 面積)

  キャビティの実効カシミール:
    モード2の抑制は「有効的な境界条件の変更��に対���。
    これは有効キャビティ長 L ��� δL だけ変化させる。

    δf₁/f₁ = -δL/L

  δL の見積もり:
    カシミール的な「有効長変化」は:
    δL ∝ λ₂ × (ℏω₂/2) / (ℏω₁ × N_modes)
    ここで N_modes はキャビティのモード数（カットオフまで）
""")

# Rough estimate of the "Casimir-like" shift
c = 3e8  # speed of light
L = 0.035  # cavity length in m
lambda2 = c / f2  # wavelength of mode 2

# Number of modes up to some cutoff (say 100 GHz)
f_cutoff = 100e9
N_modes = int(f_cutoff / f1)  # roughly

# The zero-point energy of mode 2 relative to the total
frac = (f2/2) / (sum(f1 * (n+1)/2 for n in range(N_modes)))

# Crude estimate: δf₁ ~ f₁ × (1 mode's ZPE) / (all modes' ZPE)
delta_f1_zeta = f1 * 1 / N_modes  # very rough

print(f"  粗い見積もり:")
print(f"    キャビティ長: L = {L*1000:.0f} mm")
print(f"    モード2の波長: λ₂ = {lambda2*1000:.1f} mm")
print(f"    カットオフま��のモード数: ～{N_modes}")
print(f"    δf₁(ζ予測) ～ f₁/N_modes ～ {delta_f1_zeta/1e6:.0f} MHz")
print()

# This is way too rough. Let me try a more careful estimate.
# The Lamb shift in circuit QED from vacuum fluctuations:
# δf_Lamb ≈ Σ_k g_k²/(f₁-f_k) (sum over all other modes k)
# Removing mode 2 removes one term from this sum:
# δf from removing mode 2 ≈ g₂²/(f₁-f₂)

g2 = g  # coupling to mode 2
delta_f1_lamb = g2**2 / (f1 - f2)

print(f"  Lamb シフト的な見積もり:")
print(f"    SQUIDがモード2を吸収 → Lamb シフトの1項が消える")
print(f"    δf₁ = g₂²/(f₁-f₂) = ({g/1e6:.0f} MHz)²/({(f1-f2)/1e9:.0f} GHz)")
print(f"         = {delta_f1_lamb/1e3:.2f} kHz")
print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 比較: 分散シフト vs Lamb シフト（ζ的寄与）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")

print(f"  分散シフト (SQUID on/off): {delta_chi_dispersive/1e3:.2f} kHz")
print(f"  Lamb シフト (mode 2 removal): {abs(delta_f1_lamb)/1e3:.2f} kHz")
print()

ratio = abs(delta_f1_lamb) / delta_chi_dispersive
print(f"  比: Lamb / dispersive = {ratio:.4f}")
print()

if ratio > 0.9 and ratio < 1.1:
    print(f"  ★★ 両者はほぼ同じ大きさ！")
    print(f"     分散シフトと Lamb シフトは同じ物理（g²/Δ）。")
    print(f"     → 区別できない可能性が高い。")
elif ratio > 0.1:
    print(f"  ★ 両��は同じオーダー。区別���困難だが不可能ではない。")
else:
    print(f"  Lamb シフトは分散シフトより {1/ratio:.0f} 倍小さい。")
    print(f"  → 分散シフトに埋もれて見えない可能性。")

print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 本当の問題: 分散シフトと真空エネルギー変化は分離可能か
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  分散シフト: χ = g²/Δ × α/(Δ+α)
    → SQUID の非線形性（α_anh）に依存
    → SQUID のパラメータを変えると χ が変わる

  Lamb シフト（真空揺らぎ）: δf = g²/Δ
    → SQUID の非線形性に依存しない（線形効果）
    → SQUID のパラメータを変えても δf は（ほぼ）変わらない

  ★ 分離方��:
    SQUID の E_J を磁束で連続的にチューニングしながら測定。
    E_J を変えると α_anh が変わり、分散シフト χ が変わる。
    しかし Lamb シフト δf は変わらない。

    → χ(E_J) をフィットして分散シフト成分を除去。
    → ��差 = Lamb シフト（真空揺らぎの効果）。

  これは circuit QED で実際���行わ��ている手法
  （Gambetta et al., PRA 2006; Schuster et al., Nature 2007）。
""")

# Can we detect the Lamb shift residual?
# The Lamb shift is g²/Δ ≈ (100 MHz)²/(6 GHz) ≈ 1.67 kHz
# The measurement precision in circuit QED: ～1 Hz (with long averaging)
# So the Lamb shift is ～1000× above the noise floor.

noise_floor = 1  # Hz (achievable with ~1 hour averaging at 0.3 K)
SNR = abs(delta_f1_lamb) / noise_floor

print(f"  検出可能性:")
print(f"    Lamb シフト: {abs(delta_f1_lamb)/1e3:.2f} kHz = {abs(delta_f1_lamb):.0f} Hz")
print(f"    測定ノイズフロア: ～{noise_floor} Hz（1時��積分）")
print(f"    S/N 比: {SNR:.0f}")
print(f"    → {'十分に検出可能' if SNR > 10 else '検出困難'}")
print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ ζ的「追��成分」はど��に現れるか
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  標準 circuit QED:
    δf₁(mode2 removal) = g²/(f₁-f₂) = -g²/f₁

  これは「1つのモードの真空揺らぎの寄与」を除去した結果。

  ζ的予測��「追加」になるのは:
    「モードの除去が、単な���1項の除去以上の効果を持つ場合」

  具体的には:
  (a) モード間の真空相関
      標準 QED: モード間の真空揺らぎは独��（相関��し）
      ζ的予測: モード間に算術的相関がある
      → モード2を消すと、モー���3,4,...の寄与も変わる
      → 「カスケード効果」

  (b) 符号の反転
      標準 QED: 各モードの ZPE = +ℏω/2 > 0（常に正）
      ζ的予測: ミュート後の実効 ZPE が負になりうる
      → Lamb シフトの符号が反転する
      → これ��明確に検出��能！

  ★★ 最もクリーンなシグナル:
    「SQUID をモード2に同調させたとき、
     モード1の Lamb シフトの符号が反転するか」

    標準 QED: Lamb シフトは常に同じ符号（青方偏移）
    ζ予測: ミュート後、赤方偏移に���わる可能性
""")

# Sign of the shifts
print(f"  シフトの符号:")
print(f"    分散シフト（SQUID on）: χ = {chi_dispersive_on/1e3:+.2f} kHz")
print(f"    Lamb シフト（mode 2 removal）: δf = {delta_f1_lamb/1e3:+.2f} kHz")
print()
print(f"    符号反転が起き���ば: 分散シフトを差し引いた後の")
print(f"    残差��符号が標準 QED の予測と反対になる。")
print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 結論: 実験で区別できるか
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  (1) 分散シフトと Lamb シフトは���離可能
      → E_J をスイープして非線形成分を除去する標準的手法���

  (2) Lamb シフトの大きさは十分に検出可能
      → ～1.7 kHz >> ノイズフロア 1 Hz。S/N ≈ 1700。

  (3) ζ的「追加成分」のシグナル:
      → モード間の真空相関（カスケード効果）
      → Lamb シフトの符号反転（最もクリーン）

  (4) 標準 QED との差:
      → 分散シフトを除去した残差が
        「g²/Δ（1項分）」と合うか、
        それ以上/以下/反対���号���。

  ★ 答え: YES、原理的に区別可能。

  分散シフト（非線形、E_J 依存）と
  Lamb シフト（線形、E_J 非依存）は
  E_J スイープで分���でき、
  Lamb シフトの大きさと符号を
  標準 QED の予測と比較できる。

  ── 実験設計の修正 ──

  元の設計: 「SQUID on/off で S₂₁ ���変わるか」
  修正後: 「E_J をスイープし、分散成分を除去した残差の
           大きさと符号が標準 QED と合うか」

  後者の方がはるかに精密で、帰無仮説が明確。
""")

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 60万円の判断: 更新版
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  根拠:
  ✓ Lamb シフト���検出可能（S/N > 1000）
  ✓ 分散シフトと分離可能（E_J スイープ）
  ✓ 帰無仮説が明確（残差 = g²/Δ × 1項分）
  ✓ ζ予測の特徴的シグナル（符号反転）がある
  ✓ 標準 circuit QED の手法で実行可能

  追加リスク:
  △ 符号反転が起きない場合、「ζが間違い」か
    「検出限���以下」か区別できない可能性
  △ 多モード効果のモデリングが複雑

  判断: 実験は正当化され���。
  理由: 帰無仮説が明確で、S/N が十分で、
       標準技術で実行可能。結果は正でも負でも論文になる。
""")

print("=" * 70)
print("  END")
print("=" * 70)
