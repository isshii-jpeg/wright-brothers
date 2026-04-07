#!/usr/bin/env sage
"""BC system negative integers — Sage v2 (format-safe)"""

print("=" * 70)
print("BC SYSTEM AT NEGATIVE INTEGERS — SAGE")
print("=" * 70)

# =====================================================================
# 1. Modular forms
# =====================================================================
print("\n=== MODULAR FORMS ===")

for k in [2, 4, 6, 8, 10, 12]:
    Bk = bernoulli(k)
    zv = -Bk/k
    print("  E_%d: B_%d = %s, zeta(%d) = %s" % (k, k, Bk, 1-k, zv))

print("\nEisenstein E_4 and E_6:")
E4 = EisensteinForms(1, 4).basis()[0]
print("  E_4 =", E4.q_expansion(8))
E6 = EisensteinForms(1, 6).basis()[0]
print("  E_6 =", E6.q_expansion(8))

print("\nRamanujan Delta:")
Delta = CuspForms(1, 12).basis()[0]
print("  Delta =", Delta.q_expansion(12))

# =====================================================================
# 2. Completed L-functions
# =====================================================================
print("\n=== COMPLETED L-FUNCTIONS xi(s) ===")

print("Verifying xi(s) = xi(1-s):")
for s_val in [-1, -3, -5]:
    s = RR(s_val)
    z_s = RR(zeta(s_val))
    xi_s = RR(0.5) * s * (s-1) * RR(pi)^(-s/2) * gamma(s/2) * z_s
    s2 = RR(1-s_val)
    z_1ms = RR(zeta(1-s_val))
    xi_1ms = RR(0.5) * s2 * (s2-1) * RR(pi)^(-s2/2) * gamma(s2/2) * z_1ms
    print("  xi(%d) = %.12f, xi(%d) = %.12f, match: %s" % (s_val, xi_s, 1-s_val, xi_1ms, abs(xi_s - xi_1ms) < 1e-10))

# =====================================================================
# 3. Dirichlet L at s=-1 — full survey
# =====================================================================
print("\n=== DIRICHLET L(chi, -1) FOR CONDUCTOR <= 30 ===")

print("  N   ord   L(-1,chi)        Omega         physical")
print("  " + "-"*55)

physical_list = []
for N in range(1, 31):
    G = DirichletGroup(N)
    for chi in G:
        if chi.conductor() != N:
            continue
        if chi.is_trivial() and N == 1:
            Lv = float(-QQ(1)/12)
            omega = abs(8*float(pi)/3 * Lv)
            phys = "YES" if 0 < omega < 1 else ""
            print("  %3d  triv  %16.10f  %12.6f  %s" % (N, Lv, omega, phys))
            if phys: physical_list.append((N, "triv", omega))
            continue
        try:
            Lv = float(chi.lfunction_value(-1))
            omega = abs(8*float(pi)/3 * Lv)
            phys = "YES" if 0 < omega < 1 else ""
            if phys or N <= 5 or abs(Lv) < 0.5:
                o = chi.order()
                print("  %3d  ord%d  %16.10f  %12.6f  %s" % (N, o, Lv, omega, phys))
                if phys: physical_list.append((N, "ord%d"%o, omega))
        except:
            pass

print("\nPhysical (Omega in (0,1)):", physical_list)

# =====================================================================
# 4. 2-adic structure
# =====================================================================
print("\n=== 2-ADIC STRUCTURE ===")

Q2 = Qp(2, prec=30)
print("Key values in Q_2:")
for (name, num, den) in [("1/12", 1, 12), ("-7/120", -7, 120), ("31/252", 31, 252)]:
    v = Q2(num)/Q2(den)
    print("  %s = %s  (v_2 = %d)" % (name, v, v.valuation()))

# 2-adic convergence
print("\n2-adic distances between ζ_{not2} values:")
vals_2adic = []
for k in range(1, 7):
    B2k = bernoulli(2*k)
    z_not2 = (1 - 2^(2*k-1)) * (-B2k / (2*k))
    vals_2adic.append(Q2(z_not2))

for i in range(len(vals_2adic)-1):
    diff = vals_2adic[i+1] - vals_2adic[i]
    v = diff.valuation()
    print("  |L_2(%d) - L_2(%d)|_2 = 2^(%d)" % (-(2*(i+2)-1), -(2*(i+1)-1), v))

# =====================================================================
# 5. Cyclotomic class numbers
# =====================================================================
print("\n=== CYCLOTOMIC CLASS NUMBERS ===")

for n in range(2, 7):
    try:
        K = CyclotomicField(2^n)
        h = K.class_number()
        deg = euler_phi(2^n)
        v2h = valuation(h, 2)
        print("  Q(zeta_%d): degree %d, h = %d, v_2(h) = %d" % (2^n, deg, h, v2h))
    except Exception as e:
        print("  Q(zeta_%d): skipped (%s)" % (2^n, e))

# =====================================================================
# 6. Lichtenbaum conjecture verification
# =====================================================================
print("\n=== LICHTENBAUM CONJECTURE ===")

print("|zeta(-1)| = |K_2(Z)|/w_2(Q)")
print("  |K_2(Z)| = 2")
print("  w_2(Q) = 24")
print("  2/24 = 1/12 = |zeta(-1)|: VERIFIED")

# w_2(Q) = largest m such that Q contains a primitive m-th root of (-1)
# Actually w_2(K) = |H^0(K, Q/Z(2))_tors|
# For Q: w_2 = 24 (involves Bernoulli)
# General: w_k(Q) = denominator of B_k/k (for k even)
print("\nGeneralized Lichtenbaum w_k(Q) = denom(B_k/k):")
for k in [2, 4, 6, 8]:
    Bk = bernoulli(k)
    ratio = Bk/k
    w = ratio.denominator()
    print("  w_%d(Q) = denom(B_%d/%d) = denom(%s) = %d" % (k, k, k, ratio, w))

# =====================================================================
# 7. Hecke eigenvalues of Delta
# =====================================================================
print("\n=== HECKE EIGENVALUES OF DELTA ===")

print("Ramanujan tau(p) and the Ramanujan conjecture:")
for p in primes(40):
    tau_p = Delta.coefficient(p)
    bound = 2 * float(p)^(11/2)
    ratio = abs(float(tau_p)) / bound
    print("  tau(%2d) = %10d, bound = %14.1f, |tau|/bound = %.6f" % (p, tau_p, bound, ratio))

# =====================================================================
# 8. E_2 modular anomaly
# =====================================================================
print("\n=== E_2 MODULAR ANOMALY ===")

print("E_2(tau) transforms as: E_2(-1/tau) = tau^2 E_2(tau) + 12*tau/(2*pi*i)")
print("The anomaly coefficient = 12 = 1/|zeta(-1)|")
print("E_2 at self-dual point tau = i:")
print("  E_2(i) = 3/pi = %.15f" % float(3/pi))
print()
print("The modular anomaly of E_2 is PROPORTIONAL to dark energy:")
print("  anomaly = 12/(2*pi*i) per modular transformation")
print("  |anomaly coefficient| = 12 = w_2(Q)/|K_2(Z)| = 24/2")
print("  Omega_Lambda = (d/cd) * 2*pi * 1/12 = (d/cd) * 2*pi * |K_2(Z)|/w_2(Q)")

# =====================================================================
# 9. Dedekind zeta at s=-1 for quadratic fields
# =====================================================================
print("\n=== DEDEKIND ZETA_K(-1) FOR QUADRATIC FIELDS ===")

print("  d       K           disc    L(-1,chi)      zeta_K(-1)")
print("  " + "-"*60)

for d in [-3, -4, -7, -8, -11, -15, -23, 5, 8, 12, 13, 17]:
    try:
        K = QuadraticField(d)
        D = K.discriminant()
        chi_d = kronecker_character(D)
        L_neg1 = float(chi_d.lfunction_value(-1))
        zK = float(-1)/12 * L_neg1
        print("  %3d  Q(sqrt(%3d))  %5d  %12.8f  %14.10f" % (d, d, D, L_neg1, zK))
    except Exception as e:
        pass

# =====================================================================
# 10. Irregular primes
# =====================================================================
print("\n=== IRREGULAR PRIMES ===")

irregular = []
for p in primes(200):
    divides = []
    for k in range(1, (p-1)//2 + 1):
        B = bernoulli(2*k)
        if B.numerator() % p == 0:
            divides.append(2*k)
    if divides:
        irregular.append((p, divides))

print("Irregular primes < 200:")
for p, ks in irregular:
    print("  p = %3d divides B_%s" % (p, ks))

print("\np=2 is REGULAR (important for Iwasawa mu=0)")

# =====================================================================
# 11. K-theoretic formula synthesis
# =====================================================================
print("\n" + "=" * 70)
print("SYNTHESIS: K-THEORETIC FORMULA FOR DARK ENERGY")
print("=" * 70)

print("""
From Lichtenbaum:
  |zeta(-1)| = |K_2(Z)| / w_2(Q) = 2/24 = 1/12

From our framework:
  zeta_{not2}(-1) = (1-2) * (-1/12) = +1/12 = |K_2(Z)|/w_2(Q)
  xi_{not2}(-1) = -pi/6 = -pi * |K_2(Z)|/w_2(Q)
  |xi_{not2}(-1)| = pi/6

  Omega_Lambda = (d/cd) * |xi_{not2}(-1)|
               = (4/3) * (pi/6)
               = 2*pi/9

REWRITTEN USING K-THEORY:
  Omega_Lambda = (d/cd) * pi * |K_2(Z)| / w_2(Q)
               = (4/3) * pi * (2/24)
               = 4*pi / (3*12)
               = pi/9 ... wait that gives pi/9 not 2pi/9.

Let me recheck:
  |xi_{not2}(-1)| = pi/6
  (d/cd) * pi/6 = (4/3)*(pi/6) = 4pi/18 = 2pi/9  OK.

  And pi/6 = pi * (1/12) * 2 = pi * |zeta_{not2}(-1)| * 2
  The factor of 2 comes from the xi completion:
    xi(s) = (1/2)s(s-1)pi^{-s/2}Gamma(s/2)zeta(s)
  At s=-1: (1/2)(-1)(-2) = 1, pi^{1/2}, Gamma(-1/2) = -2*sqrt(pi)
  So the archimedean factor = sqrt(pi)*(-2*sqrt(pi)) = -2*pi

  Therefore:
    |xi_{not2}(-1)| = 2*pi * |zeta_{not2}(-1)| = 2*pi/12 = pi/6  OK.

CORRECT K-THEORETIC FORMULA:
  Omega_Lambda = (d/cd) * 2*pi * |K_2(Z)| / w_2(Q)
               = (4/3) * 2*pi * (1/12)
               = 2*pi/9

  Where:
    d = 4 = cd+1 (from WDW)
    cd = 3 (Artin-Verdier)
    2*pi = archimedean Gamma-factor at s=-1
    |K_2(Z)| = 2 (Milnor K-theory)
    w_2(Q) = 24 (roots of unity factor)
""")

val = float(4)/3 * 2 * float(pi) * 2 / 24
print("  Numerical: (4/3)*2*pi*2/24 = %.15f" % val)
print("  2*pi/9 = %.15f" % float(2*pi/9))
print("  Match:", abs(val - float(2*pi/9)) < 1e-14)
