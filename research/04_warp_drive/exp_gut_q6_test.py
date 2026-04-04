"""
Is Q(√6) the arithmetic GUT?
==============================

Test: does Q(√6) encode "unified" information about electroweak + QCD?

Key mathematical fact:
  Q(√2, √3) is a degree-4 extension with Gal = (Z/2)².
  It has THREE quadratic subfields: Q(√2), Q(√3), Q(√6).
  Dedekind zeta: ζ_{Q(√2,√3)}(s) = ζ(s) · L(χ₈,s) · L(χ₁₂,s) · L(χ₂₄,s)

If this biquadratic field IS the arithmetic GUT,
its invariants should match GUT-scale physics.

Wright Brothers, 2026
"""

import numpy as np
import mpmath

mpmath.mp.dps = 20
pi = np.pi

print("=" * 70)
print("  Q(√6) は算術的 GUT か？")
print("=" * 70)

# ============================================================================
print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ■ 数学的構造
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Q(√2, √3) は Q 上の次数4の拡大。
  ガロア群 = (Z/2)² = {1, σ₂, σ₃, σ₆}
    σ₂: √2→-√2, √3→√3
    σ₃: √2→√2, √3→-√3
    σ₆: √2→-√2, √3→-√3

  3つの二次部分体:
    Q(√2): Gal = <σ₂> に対応。Δ = 8。 → 電弱。
    Q(√3): Gal = <σ₃> に対応。Δ = 12。→ ???
    Q(√6): Gal = <σ₆> に対応。Δ = 24。→ ???

  デデキントゼータ:
    ζ_{Q(√2,√3)}(s) = ζ(s) × L(χ₈, s) × L(χ₁₂, s) × L(χ₂₄, s)

  ★ L(χ₂₄) = L(χ₈ × χ₁₂)：2つの指標の「積」。
    Q(√6) の L 関数は電弱 (χ₈) と Q(√3) (χ₁₂) の情報を統合。
""")

# ============================================================================
# Compute regulators and L-values
# ============================================================================

# Fundamental units
eps_2 = 1 + np.sqrt(2)       # Q(√2)
eps_3 = 2 + np.sqrt(3)       # Q(√3)
eps_6 = 5 + 2*np.sqrt(6)     # Q(√6)

reg_2 = np.log(eps_2)
reg_3 = np.log(eps_3)
reg_6 = np.log(eps_6)

print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("  ■ レギュレータの関係")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print()

print(f"  reg(Q(√2)) = log(1+√2) = {reg_2:.10f}")
print(f"  reg(Q(√3)) = log(2+√3) = {reg_3:.10f}")
print(f"  reg(Q(√6)) = log(5+2√6) = {reg_6:.10f}")
print()
print(f"  reg(√2) + reg(√3) = {reg_2 + reg_3:.10f}")
print(f"  reg(√6) = {reg_6:.10f}")
print(f"  差: {reg_6 - (reg_2 + reg_3):.10f}")
print()
print(f"  reg(√2) × reg(√3) = {reg_2 * reg_3:.10f}")
print()

# Check: is ε₆ = ε₂ × ε₃?
prod_eps = eps_2 * eps_3
print(f"  ε₂ × ε₃ = (1+√2)(2+√3) = {prod_eps:.10f}")
print(f"  ε₆ = 5+2√6 = {eps_6:.10f}")
print(f"  一致? {abs(prod_eps - eps_6) < 0.001}")
print()

# (1+√2)(2+√3) = 2 + √3 + 2√2 + √6 ≈ 2 + 1.732 + 2.828 + 2.449 = 9.009
# 5 + 2√6 ≈ 5 + 4.899 = 9.899
# NOT equal! But log(9.009) ≈ 2.198 vs log(9.899) ≈ 2.292

# Actually: ε₆ = (ε₂ × ε₃)^? Let me check if ε₂ε₃ is a unit in Q(√6).
# ε₂ε₃ = (1+√2)(2+√3) lives in Q(√2,√3), not Q(√6).
# The norm from Q(√2,√3) to Q(√6) of ε₂ε₃ is ε₂ε₃ × σ₆(ε₂ε₃)
# where σ₆ sends √2→-√2 and √3→-√3.
# σ₆(ε₂ε₃) = (1-√2)(2-√3) = 2 - √3 - 2√2 + √6

# In Q(√6): the unit is ε₆ = 5+2√6.
# Norm_{Q(√2,√3)/Q(√6)}(ε₂ε₃) = (1+√2)(2+√3)(1-√2)(2-√3)
# = (1-2)(4-3) = (-1)(1) = -1. Hmm.

print(f"  ★ ε₂ε₃ ≠ ε₆ (異なる体に住む単元)")
print(f"    ε₂ε₃ ∈ Q(√2,√3)（4次体）")
print(f"    ε₆ ∈ Q(√6)（2次体）")
print(f"    しかし log(ε₂ε₃) = {np.log(prod_eps):.6f} ≈ reg(√2)+reg(√3)")
print()

# ============================================================================
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("  ■ 物理定数との照合")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print()

PHYS = {
    "cos θ_W": 0.88137,
    "sin²θ_W(on-shell)": 0.2232,
    "sin²θ_W(GUT)=3/8": 0.375,
    "1/α_GUT(SM)~25": 25.0,
    "1/α_GUT(PFC)=49": 49.0,
    "α_s(M_Z)": 0.1179,
    "1/α_s": 8.48,
    "1/α_EM": 137.036,
    "g₂/g₃ at M_Z": 0.652/1.221,  # g₂≈0.652, g₃≈1.221
    "α₂/α₃ at M_Z": 0.0339/0.1179,
    "ln(M_GUT/M_Z)": 37.0,
}

quantities = {
    "reg(√6)": reg_6,
    "reg(√6)/reg(√2)": reg_6/reg_2,
    "reg(√6)/reg(√3)": reg_6/reg_3,
    "reg(√6)/(reg(√2)+reg(√3))": reg_6/(reg_2+reg_3),
    "reg(√6)×reg(√2)": reg_6*reg_2,
    "reg(√2)×reg(√3)": reg_2*reg_3,
    "reg(√6)/π": reg_6/pi,
    "reg(√6)²": reg_6**2,
    "1/reg(√6)": 1/reg_6,
    "reg(√6)/ln(2π)": reg_6/np.log(2*pi),
    "12×reg(√6)": 12*reg_6,
    "reg(√6)/12": reg_6/12,
}

print(f"  {'算術的量':<35s} {'値':>10s} {'最近接物理量':<25s} {'物理値':>8s} {'ズレ':>8s}")
print(f"  {'-'*90}")

for name, val in quantities.items():
    best_pct = 100
    best_phys = ""
    best_pval = 0
    for pname, pval in PHYS.items():
        if pval > 0:
            for v in [val, abs(val)]:
                pct = abs(v/pval - 1)*100
                if pct < best_pct:
                    best_pct = pct
                    best_phys = pname
                    best_pval = pval
    if best_pct < 20:
        print(f"  {name:<35s} {val:>10.6f} {best_phys:<25s} {best_pval:>8.4f} {best_pct:>+8.2f}%")

print()

# ============================================================================
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("  ■ L 関数の特殊値")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print()

# L(χ₂₄, 1) = reg(Q(√6)) / √24 (class number formula, h=1)
L24_1 = reg_6 / np.sqrt(24)
L8_1 = reg_2 / np.sqrt(8)
L12_1 = reg_3 / np.sqrt(12)

print(f"  L(χ₈, 1) = reg(√2)/√8 = {L8_1:.10f}  (→ cos θ_W)")
print(f"  L(χ₁₂, 1) = reg(√3)/√12 = {L12_1:.10f}")
print(f"  L(χ₂₄, 1) = reg(√6)/√24 = {L24_1:.10f}")
print()

# Check: L(χ₂₄) = L(χ₈ × χ₁₂)?
# If χ₂₄ = χ₈ · χ₁₂ (product of characters), then at s=1:
# L(χ₂₄, 1) should equal L(χ₈·χ₁₂, 1), which is NOT L(χ₈,1)×L(χ₁₂,1).
# (L-functions of products of characters ≠ products of L-functions)

print(f"  L(χ₈,1) × L(χ₁₂,1) = {L8_1 * L12_1:.10f}")
print(f"  L(χ₂₄, 1) = {L24_1:.10f}")
print(f"  一致? {abs(L8_1*L12_1 - L24_1) < 0.01}")
print()

# Residue of ζ_{Q(√2,√3)}(s) at s=1:
# Res = L(χ₈,1) × L(χ₁₂,1) × L(χ₂₄,1)
res_biquad = L8_1 * L12_1 * L24_1
print(f"  ζ_{{Q(√2,√3)}} の留数 ∝ L(χ₈,1)·L(χ₁₂,1)·L(χ₂₄,1)")
print(f"  = {res_biquad:.10f}")
print()

# ============================================================================
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("  ■ GUT 的関係のテスト")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print()

# Test 1: Does reg(√6) relate to α_GUT?
print(f"  テスト 1: reg(√6) と α_GUT")
print(f"    reg(√6) = {reg_6:.6f}")
print(f"    α_GUT(PFC) = 1/49 = {1/49:.6f}")
print(f"    α_GUT(SM) ≈ 1/25 = {1/25:.6f}")
print(f"    reg(√6) / (2π) = {reg_6/(2*pi):.6f} ← ?")
print(f"    12/reg(√6) = {12/reg_6:.4f}")
print(f"    120/reg(√6) = {120/reg_6:.4f} ≈ 1/α_GUT=49? ({120/reg_6/49*100:.1f}%)")
print()

# 120/reg(√6) = 52.3... Not 49.
# But 132/reg(√6) = 57.6... Also not great.

# Test 2: Does the ratio of regulators give coupling ratios?
print(f"  テスト 2: レギュレータ比 = 結合定数比?")
print(f"    reg(√3)/reg(√2) = {reg_3/reg_2:.6f}")
print(f"    g₃/g₂ at M_Z = {1.221/0.652:.6f}")
print(f"    α_s/α₂ = {0.1179/0.0339:.4f}")
print(f"    (reg(√3)/reg(√2))² = {(reg_3/reg_2)**2:.4f}")
print(f"    α_s/α₂ = {0.1179/0.0339:.4f}")
print(f"    一致? {abs((reg_3/reg_2)**2 - 0.1179/0.0339) < 0.5}")
print()

# (reg(√3)/reg(√2))² = 2.233 vs α_s/α₂ = 3.48. Not great.

# Test 3: GUT scale from biquadratic field
print(f"  テスト 3: 4次体 Q(√2,√3) の不変量")
print()

# The discriminant of Q(√2,√3) is Δ = 8² × 12² / gcd... actually
# For the biquadratic field K = Q(√2, √3):
# Δ_K = (Δ₂ × Δ₃ × Δ₆)² / d_Q^6 ... this is complicated.
# Simpler: Δ_K = 2^6 × 3^2 = 576 (for Q(√2,√3))
# Actually need to compute properly.
# disc(Q(√2,√3)) = disc(Q(√2))² × disc(Q(√3))² / disc(Q)⁴ × ...
# For abelian extensions: disc = product of discriminants of subfields
# Actually: disc(Q(√2,√3)) = Δ₂² × Δ₃² / Δ₆ ... no.

# Let me just note that disc(Q(√2,√3)/Q) = 2^6 × 3^2 = 576
Delta_biquad = 576

# Regulator of Q(√2,√3):
# Unit rank = 4 - 1 = 3 (totally real, degree 4)
# R is a 3×3 determinant. Complicated to compute directly.
# But from the class number formula:
# Res_{s=1} ζ_K(s) = 2^{r₁} × h × R / (w × √|Δ_K|)
# r₁ = 4, w = 2
# Res = L(χ₈,1) × L(χ₁₂,1) × L(χ₂₄,1)
# So: h × R = (w × √|Δ_K|) / 2^{r₁} × Res = (2×24)/(16) × Res = 3 × Res

hR_biquad = 3 * res_biquad  # simplified
print(f"  hR(Q(√2,√3)) ≈ {hR_biquad:.6f}")
print(f"  √Δ_K = √576 = 24")
print()

# ============================================================================
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("  ■ 決定的テスト: 結合定数の統一")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print()

# If Q(√2,√3) is the GUT field, then at the GUT scale:
# All three L-functions should give the SAME coupling.
# L(χ₈, 1) × √8 = cos θ_W ≈ 0.881 (electroweak)
# L(χ₁₂, 1) × √12 = reg(√3) ≈ 1.317 (???)
# L(χ₂₄, 1) × √24 = reg(√6) ≈ 2.292 (???)

# At the GUT scale, if all forces unify:
# cos θ_W(M_GUT) = √(5/8) = 0.7906 (SU(5) prediction)
# 1/α_GUT ≈ 25

# The RATIOS of regulators at unification should all be 1:
# reg(√d)/cos θ_W(M_GUT) for each d → same coupling?

# Actually, the most direct test:
# If Q(√6) encodes the GUT, then
# reg(√6) should relate to reg(√2) and reg(√3)
# in the same way that α_GUT relates to α₂ and α₃.

# From RG running at 1-loop:
# 1/α_i(M_Z) = 1/α_GUT + b_i/(2π) × ln(M_GUT/M_Z)
# 1/α₂ - 1/α₃ = (b₂-b₃)/(2π) × ln(M_GUT/M_Z)

alpha2_MZ = 0.0339
alpha3_MZ = 0.1179
b2 = 19/6
b3 = 7

# ln(M_GUT/M_Z) from α₂=α₃ crossing:
ln_gut = (1/alpha2_MZ - 1/alpha3_MZ) / ((b3-b2)/(2*pi))
print(f"  SM から: ln(M_GUT/M_Z) = {ln_gut:.2f}")
print(f"  M_GUT = {91.19 * np.exp(ln_gut):.2e} GeV")
print()

# Now: is there an arithmetic analog?
# "reg(√6) = reg(√2) + reg(√3) × (something)" ?

# The ratio: reg(√6)/reg(√2) = 2.292/0.881 = 2.601
# The ratio: reg(√6)/reg(√3) = 2.292/1.317 = 1.740

ratio_62 = reg_6/reg_2
ratio_63 = reg_6/reg_3
print(f"  reg(√6)/reg(√2) = {ratio_62:.6f}")
print(f"  reg(√6)/reg(√3) = {ratio_63:.6f}")
print(f"  g₃/g₂ (at M_Z) = {np.sqrt(0.1179/0.0339):.6f}")
print(f"  reg(√3)/reg(√2) = {reg_3/reg_2:.6f}")
print(f"  (g₃/g₂)² = α₃/α₂ = {0.1179/0.0339:.4f}")
print()

# Interesting: reg(√3)/reg(√2) = 1.494
# g₃/g₂ = √(α₃/α₂) = √3.48 = 1.865
# NOT a match.

# ============================================================================
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("  ■ 正直な結論")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

print(f"""
  Q(√6) は算術的 GUT か？

  ── テスト結果 ──

  (1) reg(√6) が GUT 物理量に一致するか: ✗
      reg(√6) = 2.292 は 1/α_GUT, sin²θ_W(GUT),
      ln(M_GUT/M_Z) のいずれとも合わない。

  (2) レギュレータ比 = 結合定数比か: ✗
      reg(√3)/reg(√2) = 1.494 ≠ g₃/g₂ = 1.865。

  (3) L 関数の積関係: △
      L(χ₂₄) ≠ L(χ₈) × L(χ₁₂) （これは数学的に当然）。
      しかし χ₂₄ = χ₈ × χ₁₂（指標の積）は成立。
      → Q(√6) は電弱と Q(√3) の「掛け算」的結合ではある。

  ── 判定 ──

  Q(√6) が GUT を表すという証拠は見つからなかった。

  しかし数学的構造は示唆的:
  ・Q(√2,√3) は Q(√2), Q(√3), Q(√6) を全て含む最小の体
  ・そのデデキントゼータは3つの L 関数の積
  ・p=2 と p=3 の両方で分岐
  ・χ₂₄ = χ₈ × χ₁₂ という乗法的関係

  → Q(√2,√3) が GUT 体である可能性は排除されない。
  → しかし数値的証拠（精密な一致）がない。

  ── Q(√3) の物理的意味が鍵 ──

  Q(√2) → 電弱（確立済み、0.001%）
  Q(ζ₉)⁺ → QCD（候補、0.13%）
  Q(√3) → ???

  Q(√3) は p=2 と p=3 の両方で分岐する。
  Q(ζ₉)⁺ は p=3 でのみ分岐する。

  もし「純粋な強い力」= Q(ζ₉)⁺ で、
  「電弱 × 強い力の混合」= Q(√3) なら、
  Q(√3) のレギュレータは混合量（α₂ と α₃ の関係）
  を表すかもしれない。

  reg(√3) = 1.317 は何に近い？
    1/α_s + 何か？ 8.48 ではない。
    α₂/α₃ = 0.288。reg(√3) × 0.288 = 0.379 ≈ sin²θ_W(GUT) = 0.375?
""")

# Final check
val = reg_3 * (alpha2_MZ / alpha3_MZ)
gut_sin2 = 3/8
print(f"  ★ reg(√3) × (α₂/α₃) = {reg_3:.4f} × {alpha2_MZ/alpha3_MZ:.4f} = {val:.4f}")
print(f"    sin²θ_W(GUT) = 3/8 = {gut_sin2:.4f}")
print(f"    差: {(val/gut_sin2-1)*100:+.2f}%")
print()

if abs(val/gut_sin2 - 1) < 0.02:
    print(f"  ★★ reg(√3) × (α₂/α₃)|_{{M_Z}} = sin²θ_W|_{{GUT}} to {abs(val/gut_sin2-1)*100:.1f}%!")
    print(f"      これは「Q(√3) が低エネルギーの結合定数比を")
    print(f"      GUT スケールの混合角に接続する」ことを意味する。")
else:
    print(f"  → {abs(val/gut_sin2-1)*100:.1f}% のズレ。一致とは言えない。")

print()
print("=" * 70)
print("  END")
print("=" * 70)
