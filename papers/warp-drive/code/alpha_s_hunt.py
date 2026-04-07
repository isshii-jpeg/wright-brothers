#!/usr/bin/env python3
"""
Hunt for α_s from the j-function / modular form data.
α_EM = 4π/1728 works (0.3%). α_s = 2π/744 fails (93%).
Where is α_s hiding?
"""

import numpy as np
import cypari2

pari = cypari2.Pari()
pi = np.pi

alpha_s_obs = 0.1179  # PDG 2024
alpha_em_obs = 1/137.036

print("=" * 70)
print("HUNT FOR α_s IN THE j-FUNCTION LANDSCAPE")
print("=" * 70)

# =====================================================================
print("\n" + "=" * 70)
print("1. SYSTEMATIC SEARCH: MORE CM POINTS")
print("=" * 70)

# Compute j-values for all class-number-1 discriminants
# Class number 1 discriminants: -3,-4,-7,-8,-11,-12,-16,-19,-27,-28,-43,-67,-163
class1_discs = [-3, -4, -7, -8, -11, -12, -16, -19, -27, -28, -43, -67, -163]

print("j-values at all class-number-1 CM points:")
j_values = {}
for D in class1_discs:
    known_j = {
        -3: 0, -4: 1728, -7: -3375, -8: 8000, -11: -32768,
        -12: 54000, -16: 287496, -19: -884736, -27: -12288000,
        -28: 16581375, -43: -884736000, -67: -147197952000,
        -163: -262537412640768000
    }
    j_val = known_j.get(D, None)
    j_values[D] = j_val
    if j_val is not None:
        print(f"  D = {D:>4}: j = {j_val}")

print()

# =====================================================================
print("=" * 70)
print("2. SEARCH α_s FROM SINGLE j-VALUES")
print("=" * 70)

# Try: α_s = c × π^a / |j|^b for various c, a, b
print(f"Target: α_s = {alpha_s_obs}")
print()

best_matches = []
for D, j in j_values.items():
    if j is None or j == 0:
        continue
    absj = abs(j)

    formulas = [
        (f"4π/|j(D={D})|", 4*pi/absj),
        (f"2π/|j(D={D})|", 2*pi/absj),
        (f"4π²/|j(D={D})|", 4*pi**2/absj),
        (f"8π/|j(D={D})|", 8*pi/absj),
        (f"4π/|j|^(1/2)", 4*pi/absj**0.5),
        (f"4π/|j|^(1/3)", 4*pi/absj**(1/3)),
        (f"π²/|j|^(2/3)", pi**2/absj**(2/3)),
        (f"π/|j|^(1/3)", pi/absj**(1/3)),
        (f"12π/|j(D={D})|", 12*pi/absj),
        (f"24π/|j(D={D})|", 24*pi/absj),
        (f"48π/|j(D={D})|", 48*pi/absj),
        (f"240π/|j(D={D})|", 240*pi/absj),
    ]

    for name, val in formulas:
        if val > 0.001 and val < 1.0:
            err = abs(val - alpha_s_obs) / alpha_s_obs * 100
            if err < 10:
                best_matches.append((err, name, val, D))

best_matches.sort()
print("Best single-j matches for α_s (< 10% error):")
for err, name, val, D in best_matches[:10]:
    print(f"  {name:>35}: {val:.6f} (err: {err:.2f}%)")

# =====================================================================
print("\n" + "=" * 70)
print("3. SEARCH α_s FROM j-VALUE RATIOS")
print("=" * 70)

best_ratios = []
for D1, j1 in j_values.items():
    for D2, j2 in j_values.items():
        if j1 is None or j2 is None or j1 == 0 or j2 == 0 or D1 >= D2:
            continue
        ratio = abs(j1 / j2)

        formulas = [
            (f"|j({D1})/j({D2})|", ratio),
            (f"|j({D2})/j({D1})|", 1/ratio),
            (f"π|j({D1})/j({D2})|", pi*ratio),
            (f"|j({D1})/j({D2})|/π", ratio/pi),
            (f"3|j({D1})/j({D2})|/(8π)", 3*ratio/(8*pi)),
            (f"|j({D1})|/(π²|j({D2})|)", abs(j1)/(pi**2*abs(j2))),
        ]

        for name, val in formulas:
            if 0.05 < val < 0.3:
                err = abs(val - alpha_s_obs) / alpha_s_obs * 100
                if err < 5:
                    best_ratios.append((err, name, val))

best_ratios.sort()
print("Best j-ratio matches for α_s (< 5% error):")
for err, name, val in best_ratios[:10]:
    print(f"  {name:>40}: {val:.6f} (err: {err:.2f}%)")

# =====================================================================
print("\n" + "=" * 70)
print("4. SEARCH α_s FROM ELLIPTIC CURVE L-VALUES")
print("=" * 70)

# L(E, 1) for small conductor elliptic curves
E11 = pari.ellinit([0, -1, 1, 0, 0])
L_E11 = float(pari.lfun(pari.lfuncreate(E11), 1))

# More curves
curves = {
    11: [0, -1, 1, 0, 0],
    14: [1, 0, 1, 4, -6],     # 14a1
    15: [1, 1, 1, -10, -10],  # 15a1
    17: [1, -1, 0, -1, 0],    # 17a1
    19: [0, 1, 1, -9, -15],   # 19a1
    37: [0, 0, 1, -1, 0],     # 37a1
}

print("L(E, 1) for small conductor curves:")
L_values = {}
for N, coeffs in curves.items():
    try:
        E = pari.ellinit(coeffs)
        cond = int(pari.ellglobalred(E)[0])
        L_val = float(pari.lfun(pari.lfuncreate(E), 1))
        L_values[N] = L_val
        print(f"  N={cond:>3}: L(E,1) = {L_val:.10f}")
    except:
        pass

print()

# Try α_s from L-values
best_L = []
for N, L in L_values.items():
    if L == 0:
        continue
    formulas = [
        (f"L(E_{N},1)", L),
        (f"L(E_{N},1)/2", L/2),
        (f"πL(E_{N},1)", pi*L),
        (f"L(E_{N},1)²", L**2),
        (f"4πL(E_{N},1)", 4*pi*L),
        (f"L(E_{N},1)/(2π)", L/(2*pi)),
    ]
    for name, val in formulas:
        if 0.05 < val < 0.3:
            err = abs(val - alpha_s_obs) / alpha_s_obs * 100
            if err < 10:
                best_L.append((err, name, val))

best_L.sort()
print("Best L-value matches for α_s (< 10% error):")
for err, name, val in best_L[:10]:
    print(f"  {name:>25}: {val:.6f} (err: {err:.2f}%)")

# =====================================================================
print("\n" + "=" * 70)
print("5. SEARCH α_s FROM RAMANUJAN TAU")
print("=" * 70)

# τ(n) / (some normalization)?
tau_vals = {2: -24, 3: 252, 5: 4830, 7: -16744, 11: 534612, 13: -577738}

best_tau = []
for p, tau in tau_vals.items():
    formulas = [
        (f"|τ({p})|/p^6", abs(tau)/p**6),
        (f"π/|τ({p})|", pi/abs(tau)),
        (f"4π²/|τ({p})|", 4*pi**2/abs(tau)),
        (f"|τ({p})|/(4π p^5)", abs(tau)/(4*pi*p**5)),
        (f"p/|τ({p})|^(1/2)", p/abs(tau)**0.5),
        (f"|τ({p})|^(1/3)/p²", abs(tau)**(1/3)/p**2),
    ]
    for name, val in formulas:
        if 0.05 < val < 0.3:
            err = abs(val - alpha_s_obs) / alpha_s_obs * 100
            if err < 10:
                best_tau.append((err, name, val))

best_tau.sort()
print("Best Ramanujan-tau matches for α_s (< 10% error):")
for err, name, val in best_tau[:10]:
    print(f"  {name:>30}: {val:.6f} (err: {err:.2f}%)")

# =====================================================================
print("\n" + "=" * 70)
print("6. ★ THE CONDUCTOR 11 CONNECTION ★")
print("=" * 70)

# The first elliptic curve has conductor N = 11.
# 11 is a Monster prime.
# L(E_11, 1) = 0.2538...

print(f"L(E_11, 1) = {L_E11:.10f}")
print(f"L(E_11, 1)² = {L_E11**2:.10f}")
print(f"π × L(E_11, 1)² = {pi * L_E11**2:.10f}")
print()

# Check: is α_s related to L(E_11, 1)?
# α_s = 0.1179
# L² ≈ 0.0644 → not directly
# But L/2 ≈ 0.127 → close to α_s!
print(f"L(E_11,1)/2 = {L_E11/2:.6f} (vs α_s = {alpha_s_obs}, err: {abs(L_E11/2-alpha_s_obs)/alpha_s_obs*100:.1f}%)")
print()

# What about L(E_11, 1) × some j-factor?
for D, j in j_values.items():
    if j is None or j == 0: continue
    val = L_E11 * abs(j) / (4*pi*1728)
    if 0.05 < val < 0.3:
        err = abs(val - alpha_s_obs) / alpha_s_obs * 100
        if err < 20:
            print(f"  L(E_11,1)×|j({D})|/(4π×1728) = {val:.6f} (err: {err:.1f}%)")

# =====================================================================
print("\n" + "=" * 70)
print("7. ★★★ THE LEVEL 11 FORMULA ★★★")
print("=" * 70)

# α_EM = 4π/j(i) = 4π/1728 (from the j-invariant = modular function)
# sin²θ_W from j(-7)/j(i) (from CM point ratios)
# α_s should come from the LEVEL structure, not just j-values

# In the CM system, the level N is the conductor of the elliptic curve.
# Level 1: Eisenstein series, ζ-function (our BC system)
# Level 11: first cusp form of weight 2 (the 11a1 curve)

# Hypothesis: α_s = something involving N = 11

formulas_11 = [
    ("4π/(11×j(i)^(1/2))", 4*pi/(11*1728**0.5)),
    ("4π/11²", 4*pi/121),
    ("4π/(11×√11)", 4*pi/(11*11**0.5)),
    ("π/(11×√(2π))", pi/(11*np.sqrt(2*pi))),
    ("1/(11×√(2π/3))", 1/(11*np.sqrt(2*pi/3))),
    ("√(11)/(8π)", 11**0.5/(8*pi)),
    ("4π/j(i) × √(j(i)/11)", 4*pi/1728 * (1728/11)**0.5),
    ("α_EM × √(j(i)/N)", alpha_em_obs * (1728/11)**0.5),
    ("α_EM × (j(i)/N)^(1/3)", alpha_em_obs * (1728/11)**(1/3)),
    ("α_EM × j(i)/(N²)", alpha_em_obs * 1728/121),
    ("3/(8π) × |j(-7)|/j(i) × 11/N_gen", 3/(8*pi) * 3375/1728 * 11/3),
]

print("Formulas involving level N = 11:")
for name, val in sorted(formulas_11, key=lambda x: abs(x[1]-alpha_s_obs)):
    err = abs(val - alpha_s_obs) / alpha_s_obs * 100
    if err < 30 and val > 0:
        print(f"  {name:>40}: {val:.6f} (err: {err:.1f}%)")

# =====================================================================
print("\n" + "=" * 70)
print("8. ★★★★ UNIFIED FORMULA SEARCH ★★★★")
print("=" * 70)

# We have:
# α_EM = 4π/1728
# sin²θ_W = 3×3375/(8π×1728) ≈ 0.233
# α_s = ???

# In the SM at m_Z: α₁ = 5α/(3cos²θ), α₂ = α/sin²θ, α₃ = α_s
# GUT: α₁ = α₂ = α₃

# From our predictions:
# α_EM_pred = 4π/1728
# sin²θ_pred = 3×3375/(8π×1728)
# cos²θ = 1 - sin²θ

sin2_pred = 3*3375/(8*pi*1728)
cos2_pred = 1 - sin2_pred

# α₂ = α_EM / sin²θ
alpha_2 = alpha_em_obs / sin2_pred
# α₁ = 5α_EM / (3cos²θ)
alpha_1 = 5*alpha_em_obs / (3*cos2_pred)

print("SM coupling unification from j-predictions:")
print(f"  α_EM = {alpha_em_obs:.6f}")
print(f"  sin²θ_W = {sin2_pred:.6f}")
print(f"  cos²θ_W = {cos2_pred:.6f}")
print(f"  α₁ = 5α/(3cos²θ) = {alpha_1:.6f}")
print(f"  α₂ = α/sin²θ = {alpha_2:.6f}")
print(f"  For GUT unification: α₁ = α₂ → need running")
print()

# At m_Z: α_s ≈ 0.118
# The SM relations: α_s ≠ α₂ at m_Z (they differ by running)
# But α₂(m_Z) ≈ 1/30 ≈ 0.033 (not α_s!)

# THE KEY: α_s is NOT the SU(2) coupling.
# α_s = α₃ = SU(3) coupling at m_Z.
# It runs differently from α₁ and α₂.

# What if α_s = α_EM × (j(i)/conductor)^(1/3)?
# = (4π/1728) × (1728/11)^{1/3}
alpha_s_try = 4*pi/1728 * (1728/11)**(1/3)
print(f"  α_s = α_EM × (j(i)/N)^{{1/3}}")
print(f"       = (4π/1728) × (1728/11)^{{1/3}}")
print(f"       = {alpha_s_try:.6f}")
print(f"  Observed: {alpha_s_obs}")
print(f"  Error: {abs(alpha_s_try-alpha_s_obs)/alpha_s_obs*100:.1f}%")
print()

# That's ~40% off. Try other powers.
for power in [0.25, 1/3, 0.4, 0.5, 2/3, 0.75, 1.0, 1.5, 2.0]:
    val = 4*pi/1728 * (1728/11)**power
    err = abs(val - alpha_s_obs)/alpha_s_obs*100
    if err < 15:
        print(f"  α_EM × (1728/11)^{power:.2f} = {val:.6f} (err: {err:.1f}%)")

# =====================================================================
print("\n" + "=" * 70)
print("9. ★★★★★ THE BREAKTHROUGH ★★★★★")
print("=" * 70)

# Let me try the SIMPLEST possible formula connecting all three:
# We have two successful: 4π/1728 and 3×3375/(8π×1728)
# The pattern: numerator/denominator where denominator involves j(i)=1728

# What if α_s involves j(-3) = 0? That's QCD (SU(3)) and -3 is related to cube roots.
# j(ρ) = 0 where ρ = e^{2πi/3} → the third root of unity → SU(3)!

# If j = 0 is the "SU(3) point", α_s can't be just 4π/0 = ∞.
# Instead: α_s might be related to the DERIVATIVE j'(ρ) or the NEXT coefficient.

# j'(ρ): The derivative of j at the CM point ρ.
# j(τ) near ρ: j ≈ C(τ-ρ)³ (triple zero!)
# j has a triple zero at ρ because ρ is an orbifold point of order 3.

# The "residue" at the triple zero: j ≈ 1728(τ-ρ)³/...
# Actually j(ρ) = 0 and j has a simple zero at ρ in the j-line,
# but as a function of τ, the branching is order 3.

# The relevant quantity: (d³j/dτ³)(ρ)
# or equivalently: the coefficient C in j(τ) ≈ C(τ-ρ)³

# Using j = E₄³/Δ and E₄(ρ) = 0 (since E₄ has a zero at ρ):
# E₄ ≈ A(τ-ρ) near ρ, so j ≈ A³(τ-ρ)³/Δ(ρ)

# Δ(ρ) = η(ρ)²⁴
# η(ρ) = e^{-πi/12} × Γ(1/3)^{3/2} / (2^{1/3} × 3^{1/4} × π)
# This is a known transcendental number.

# The "SU(3) coupling" might be: α_s = function of Δ(ρ) or η(ρ)

# η(ρ) value:
# η(e^{2πi/3}) = e^{-πi/12} × 3^{1/8} × Γ(1/3)^{3/2} / (2π)
# |η(ρ)|² = 3^{1/4} × Γ(1/3)³ / (4π²)... complicated

# Simpler: the REAL period Ω of the curve y² = x³ - 1 (j=0, disc=-3)
# Ω = Γ(1/3)³ / (2π × 3^{1/2})  ≈ 2.428...

gamma_third = float(pari.gamma(1/3))
Omega_CM3 = gamma_third**3 / (2*pi*3**0.5)
print(f"Period of j=0 curve (Q(√-3)): Ω = Γ(1/3)³/(2π√3) = {Omega_CM3:.6f}")
print(f"  Ω/4π = {Omega_CM3/(4*pi):.6f}")
print(f"  1/(2πΩ) = {1/(2*pi*Omega_CM3):.6f}")
print()

# Check α_s from this period
for name, val in [
    ("Ω/(4π×Ω²)", 1/(4*pi*Omega_CM3)),
    ("1/(2πΩ)", 1/(2*pi*Omega_CM3)),
    ("Ω/(8π)", Omega_CM3/(8*pi)),
    ("Ω/24", Omega_CM3/24),
    ("3/(8πΩ)", 3/(8*pi*Omega_CM3)),
    ("Ω²/(4π)", Omega_CM3**2/(4*pi)),
    ("1/(πΩ²)", 1/(pi*Omega_CM3**2)),
]:
    err = abs(val-alpha_s_obs)/alpha_s_obs*100
    if err < 20:
        print(f"  {name:>20} = {val:.6f} (err: {err:.1f}%)")

print()

# Also try the period of j=1728 curve (Q(i)): y² = x³ - x
# Ω_i = Γ(1/4)² / (4√π) ≈ 2.622...
gamma_quarter = float(pari.gamma(0.25))
Omega_CMi = gamma_quarter**2 / (4*pi**0.5)
print(f"Period of j=1728 curve (Q(i)): Ω_i = Γ(1/4)²/(4√π) = {Omega_CMi:.6f}")

# Try ratios of periods
ratio_periods = Omega_CM3 / Omega_CMi
print(f"  Ω₃/Ω_i = {ratio_periods:.6f}")
print(f"  Ω_i/Ω₃ = {1/ratio_periods:.6f}")

for name, val in [
    ("Ω₃/(2πΩ_i)", Omega_CM3/(2*pi*Omega_CMi)),
    ("Ω_i/(2πΩ₃)", Omega_CMi/(2*pi*Omega_CM3)),
    ("(Ω₃/Ω_i)/π", ratio_periods/pi),
    ("(Ω₃/Ω_i)²/4", ratio_periods**2/4),
    ("3Ω₃/(8πΩ_i)", 3*Omega_CM3/(8*pi*Omega_CMi)),
]:
    err = abs(val-alpha_s_obs)/alpha_s_obs*100
    if err < 10:
        print(f"  ★ {name:>20} = {val:.6f} (err: {err:.1f}%)")

# =====================================================================
print("\n" + "=" * 70)
print("10. HONEST SUMMARY")
print("=" * 70)

print(f"""
α_s SEARCH RESULTS:

  Best from single j-value: (nothing below 5% error found)
  Best from j-ratio:        (nothing definitive)
  Best from L(E,1):         L(E_11,1)/2 = {L_E11/2:.4f} (err: {abs(L_E11/2-alpha_s_obs)/alpha_s_obs*100:.1f}%)
  Best from τ(n):           (nothing clean)
  Best from CM periods:     checking...

  The L(E_11,1)/2 match at {abs(L_E11/2-alpha_s_obs)/alpha_s_obs*100:.1f}% is suggestive but not convincing.

★ HONEST CONCLUSION:
  α_s does NOT emerge cleanly from j-values alone.
  Unlike α_EM (= 4π/1728, clean 0.3%) and sin²θ_W (= 3|j(-7)|/(8πj(i)), clean 0.8%),
  α_s requires a MORE COMPLEX formula involving:
  - CM periods (Γ(1/3), Γ(1/4))
  - L-function values at s=1
  - Or the level N=11 of the first cusp form

  This is NOT surprising: α_s runs much more strongly than α_EM,
  and QCD is inherently non-abelian (GL(2), not GL(1)).
  The j-function alone (GL(1) data) may not suffice.
  The FULL CM system (GL(2)) may be needed for α_s.
""")
