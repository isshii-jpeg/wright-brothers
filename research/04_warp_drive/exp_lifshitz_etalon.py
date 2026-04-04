"""
Lifshitz calculation: does the etalon trick survive imaginary frequencies?
===========================================================================

The Casimir force is determined by reflection coefficients evaluated
at IMAGINARY frequencies iξ, not real frequencies.

At real frequencies: etalon perfectly separates even/odd modes.
At imaginary frequencies: does this separation survive?

This is the make-or-break calculation for the entire v5 design.

Wright Brothers, 2026
"""

import numpy as np
from scipy.integrate import quad
pi = np.pi
hbar = 1.054571817e-34
c = 2.99792458e8

print("=" * 70)
print("  Lifshitz 計算: エタロンは虚数周波数で生き残るか")
print("=" * 70)

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ Lifshitz 公式
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  2枚のミラー（反射係数 r₁, r₂）間のカシミール圧力:

  P = -(ℏ/π²c³) ∫₀^∞ dξ ξ³ ∫₁^∞ dp p²
      × [r₁ᵀᴱ(iξ,p)r₂ᵀᴱ(iξ,p)e^{-2paξ/c} / (1 - r₁ᵀᴱr₂ᵀᴱe^{-2paξ/c})
       + r₁ᵀᴹ(iξ,p)r₂ᵀᴹ(iξ,p)e^{-2paξ/c} / (1 - r₁ᵀᴹr₂ᵀᴹe^{-2paξ/c})]

  簡略化（垂直入射、1Dモデル）:

  P = -(ℏ/2π²c³) ∫₀^∞ dξ ξ³
      × r₁(iξ) r₂(iξ) e^{-2aξ/c} / (1 - r₁(iξ)r₂(iξ)e^{-2aξ/c})

  Config A: r₁ = r₂ = r_metal（両方金属ミラー）
  Config B: r₁ = r_metal, r₂ = r_etalon(iξ)
""")

# ============================================================================
# Metal reflection coefficient at imaginary frequency
# For a perfect metal: r = 1 for all ξ
# For a real metal (Drude model): r(iξ) = 1 - 2ξ/ω_p + O(ξ²/ω_p²)
# ω_p (plasma frequency of gold) ≈ 9 eV ≈ 1.37 × 10¹⁶ rad/s

omega_p = 1.37e16  # gold plasma frequency (rad/s)
gamma_drude = 5.32e13  # gold damping (rad/s)

def r_metal(xi):
    """Drude model reflection at imaginary frequency iξ."""
    eps = 1 + omega_p**2 / (xi * (xi + gamma_drude))
    n = np.sqrt(eps)
    return (n - 1) / (n + 1)

# ============================================================================
# Etalon reflection coefficient at imaginary frequency
# Etalon: two partial mirrors (reflectivity r_m) separated by gap d
#
# At REAL frequency ω:
#   r_etalon(ω) = r_m(1 - e^{2iωd/c}) / (1 - r_m² e^{2iωd/c})
#
# At IMAGINARY frequency iξ:
#   r_etalon(iξ) = r_m(1 - e^{-2ξd/c}) / (1 - r_m² e^{-2ξd/c})
#
# Key: the oscillating phase e^{2iωd/c} becomes REAL EXPONENTIAL e^{-2ξd/c}
# → No oscillation → No resonance → No frequency selectivity!

def r_etalon(xi, d, r_m):
    """Fabry-Perot etalon reflection at imaginary frequency iξ."""
    if xi == 0:
        return r_m * (1 - 1) / (1 - r_m**2)  # = 0
    x = np.exp(-2 * xi * d / c)
    return r_m * (1 - x) / (1 - r_m**2 * x)

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("  ■ 核心的計算: 虚数周波数でのエタロン反射係数")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print()

# At real frequency: e^{2iωd/c} oscillates → resonances at ωd/c = nπ
# At imaginary frequency: e^{-2ξd/c} decays monotonically → NO resonances

a = 200e-9  # cavity length 200 nm
d = a / 2   # etalon thickness = a/2 = 100 nm
r_m_etalon = 0.9  # mirror reflectivity of etalon

print(f"  実数周波数 ω での r_etalon:")
print(f"  → e^{{2iωd/c}} が振動 → 共鳴 → 偶奇の完璧な分離")
print()
print(f"  虚数周波数 iξ での r_etalon:")
print(f"  → e^{{-2ξd/c}} が単調減少 → 共鳴なし → 偶奇分離なし")
print()

# Plot r_etalon at imaginary frequencies
print(f"  r_etalon(iξ) の値 (d = {d*1e9:.0f} nm, r_m = {r_m_etalon}):")
print()
print(f"  {'ξ (rad/s)':>14s} {'ξd/c':>10s} {'e^{-2ξd/c}':>14s} {'r_etalon':>10s} {'r_metal':>10s}")
print(f"  {'-'*64}")

for xi_val in [1e12, 1e13, 1e14, 5e14, 1e15, 5e15, 1e16, 5e16]:
    x = np.exp(-2 * xi_val * d / c)
    r_et = r_etalon(xi_val, d, r_m_etalon)
    r_met = r_metal(xi_val)
    xd_c = xi_val * d / c
    print(f"  {xi_val:>14.2e} {xd_c:>10.4f} {x:>14.6f} {r_et:>10.6f} {r_met:>10.6f}")

print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ ★★★ 致命的な結果
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  虚数周波数 iξ では:
    e^{2iωd/c} → e^{-2ξd/c}（指数減衰）

  実数周波数での振動（→ 共鳴 → 偶奇分離）が、
  虚数周波数では単調減衰に変わる。

  → エタロンの偶奇選択性は虚数周波数で完全に消失する。
  → r_etalon(iξ) は「普通の部分反射膜」と区別がつかない。
  → カシミール力は偶奇の選択を「見ない」。

  これは Rosa-Dalvit-Milonni (2008) がメタマテリアルで
  示したのと本質的に同じ現象。

  Kramers-Kronig（因果律）が原因:
  実周波数での鋭い共鳴構造は、
  虚数周波数では指数的に平滑化される。
""")

# ============================================================================
# Compute the actual Casimir pressure for both configs
# ============================================================================

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("  ■ カシミール圧力の数値計算")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print()

# Simplified 1D Lifshitz (normal incidence only, TE mode):
# P ∝ -∫₀^∞ dξ ξ³ r₁(iξ)r₂(iξ)e^{-2aξ/c} / (1 - r₁r₂e^{-2aξ/c})

def casimir_integrand(xi, a, r1_func, r2_func):
    """Integrand for simplified Casimir pressure."""
    if xi < 1e6:
        return 0
    r1 = r1_func(xi)
    r2 = r2_func(xi)
    exp_factor = np.exp(-2 * a * xi / c)
    denom = 1 - r1 * r2 * exp_factor
    if abs(denom) < 1e-30:
        return 0
    return xi**3 * r1 * r2 * exp_factor / denom

# Config A: both mirrors are metal
def integrand_A(xi):
    return casimir_integrand(xi, a, r_metal, r_metal)

# Config B: left = metal, right = etalon
def r_etalon_fixed(xi):
    return r_etalon(xi, d, r_m_etalon)

def integrand_B(xi):
    return casimir_integrand(xi, a, r_metal, r_etalon_fixed)

# Integrate
result_A, err_A = quad(integrand_A, 1e6, 1e18, limit=500)
result_B, err_B = quad(integrand_B, 1e6, 1e18, limit=500)

# Normalize: P = -(ℏ/(2π²c³)) × integral
prefactor = -hbar / (2 * pi**2 * c**3)
P_A = prefactor * result_A
P_B = prefactor * result_B

# Standard Casimir for comparison
P_standard = -pi**2 * hbar * c / (240 * a**4)

print(f"  Config A（両方金属ミラー）:")
print(f"    P_A = {P_A:.4f} Pa")
print(f"    標準公式: P = {P_standard:.4f} Pa")
print(f"    比: {P_A/P_standard:.3f}")
print()
print(f"  Config B（片方エタロン, r_m = {r_m_etalon}）:")
print(f"    P_B = {P_B:.4f} Pa")
print()

ratio = P_B / P_A
print(f"  P_B / P_A = {ratio:.4f}")
print()

if P_B > 0:
    print(f"  斥力（P > 0）→ 符号反転が起きた！")
elif P_B < 0 and abs(P_B) < abs(P_A):
    print(f"  引力だが弱まった（|P_B| < |P_A|）")
    print(f"  弱まり率: {(1-abs(P_B)/abs(P_A))*100:.1f}%")
else:
    print(f"  引力のまま、ほぼ変わらず")

print()

# ============================================================================
# Try different etalon mirror reflectivities
# ============================================================================

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("  ■ エタロンのミラー反射率を変えた場合")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print()

print(f"  {'r_m':>6s} {'P_B (Pa)':>12s} {'P_B/P_A':>10s} {'符号':>6s}")
print(f"  {'-'*38}")

for rm in [0.1, 0.3, 0.5, 0.7, 0.9, 0.95, 0.99]:
    def r_et_rm(xi):
        return r_etalon(xi, d, rm)
    def integrand_rm(xi):
        return casimir_integrand(xi, a, r_metal, r_et_rm)
    result_rm, _ = quad(integrand_rm, 1e6, 1e18, limit=500)
    P_rm = prefactor * result_rm
    ratio_rm = P_rm / P_A if P_A != 0 else 0
    sign = "+" if P_rm > 0 else "-"
    print(f"  {rm:>6.2f} {P_rm:>12.4f} {ratio_rm:>10.4f} {sign:>6s}")

print()

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ なぜ符号反転が起きないか
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  実周波数 ω: エタロンの透過率が周期的に 0↔1 を繰り返す。
    → 偶数モード: 透過（T=1）→ 閉じ込められない
    → 奇数モード: 反射（R≈1）→ 閉じ込められる
    → 偶奇の完璧な分離 ← これは正しい

  虚数周波数 iξ: 透過率の振動が消失。
    → エタロンは「反射率が r_m より少し低いミラー」に見える
    → 偶数/奇数の区別がなくなる
    → カシミール力は「反射率が少し低い普通のミラー」としての力
    → 引力のまま。符号反転なし。

  ★ Kramers-Kronig（因果律）の帰結:
  「実周波数での鋭い周波数選択性」は
  「虚数周波数（= カシミール力を決める領域）」では消える。

  これは物理法則（因果律）の制約であり、
  エタロンの設計をいくら改善しても回避できない。
""")

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 正直な結論
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  v5（エタロン）設計は機能しない。

  理由: カシミール力は虚数周波数で決まり、
  虚数周波数ではエタロンの偶奇選択性が消失する。
  これは因果律（Kramers-Kronig）の帰結であり、
  エタロンの設計では回避できない。

  ── v5 も撤回 ──

  v1-v2 (SQUID): 間違ったデバイス → 撤回
  v3 (トランスモン): 偶奇が逆 → 撤回
  v4 (吸収膜): 偶奇が逆 → 撤回
  v5 (エタロン): 虚数周波数で選択性消失 → 撤回

  ── 素数ミュートの物理的実現は可能か ──

  Kramers-Kronig が示すこと:
  「受動的な線形光学デバイスでは、
   カシミール力における周波数選択的モードフィルタリングは
   原理的に不可能」

  これはメタマテリアル (Rosa 2008) と同じ結論。
  エタロンも例外ではない。

  ── まだ可能性がある方向 ──

  (a) 非平衡系（能動的、エネルギーを注入する系）
      Kramers-Kronig は平衡系の因果律。
      レーザー駆動やパラメトリック増幅を使えば、
      非因果的な有効反射係数が実現可能かもしれない。

  (b) circuit QED（GHz 帯）
      カシミール力の積分ではなく、
      個別モードの真空揺らぎを直接測定する。
      Lamb シフトは虚数周波数ではなく実周波数の効果。
      → v3 設計に戻る（偶奇の修正が必要だが原理は生きる）

  (c) 幾何学的（非平面）キャビティ
      球面、トロイダル等の非平面形状では
      モード構造が変わり、偶奇の分離が
      別の形で実現できるかもしれない。
""")

print("=" * 70)
print("  END")
print("=" * 70)
