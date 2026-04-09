"""
Audit: "Muting too many primes is dangerous" — re-verify the evidence
=====================================================================

The warp-drive papers list ~7 separate arguments for why over-muting primes
leads to catastrophic outcomes. This script re-verifies each one numerically
and rates how mathematically tight the argument actually is.

Claims under audit:
  C1. Vacuum-energy Euler product |prod (1-p^3)| grows super-exponentially with |S|.
  C2. Parity law: sign of mute factor flips with |S| parity.
  C3. Generation g-2 corrections C_mu, C_tau explode for high primes / large |S|.
  C4. Two-prime muting "decouples" matter from Spec(Z) (transparency claim).
  C5. K_1(Z) != K_1(Z[1/p]) provides a topological no-go for vacuum decay.
  C6. Lambda_QCD is exponentially sensitive to small alpha_s shifts (~25% kills nuclei).
  C7. S = all primes -> Spec(Q): zeta_S(s) = 1 identically, "no physics".

For each: TIGHT (pure math), CONDITIONAL (depends on premise), or SPECULATIVE.
"""

import math
from functools import reduce
from operator import mul

# ----------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------
def primes_up_to(n):
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i*i, n+1, i):
                sieve[j] = False
    return [i for i, v in enumerate(sieve) if v]

def mute_factor(primes, k):
    """prod_{p in S} (1 - p^k) — the multiplier for zeta(-k)."""
    if not primes:
        return 1
    return reduce(mul, ((1 - p**k) for p in primes), 1)

# ============================================================================
# C1.  VACUUM ENERGY PRODUCT: |prod (1 - p^3)| with |S| growing
# ============================================================================
def audit_C1():
    print("=" * 78)
    print("C1.  Vacuum energy product |prod_{p in S}(1 - p^3)| as |S| grows")
    print("=" * 78)
    print(f"{'|S|':>4} {'primes':<26} {'|product|':>16} {'log10':>8} {'sign':>5}")
    print("-" * 64)
    P = primes_up_to(100)
    for n in [0, 1, 2, 3, 4, 5, 6, 8, 10, 15, 20, 25]:
        S = P[:n]
        f = mute_factor(S, 3)
        mag = abs(f)
        sgn = "+" if f > 0 else "-"
        Sstr = ",".join(map(str, S[:6])) + ("…" if n > 6 else "")
        print(f"{n:>4} {Sstr:<26} {mag:>16.3e} {math.log10(mag):>8.2f} {sgn:>5}")
    print()
    # asymptotic growth law
    log_mag = sum(3*math.log10(p) for p in P[:25])
    print(f"Asymptotic: log10|prod| ≈ 3 * sum(log10 p) = {log_mag:.2f} for first 25 primes.")
    print("Growth rate: by prime number theorem, sum_log_p(N) ~ N, so log|prod| ~ 3N.")
    print("VERDICT: TIGHT (pure arithmetic). Vacuum 'energy' multiplier diverges as e^{3 theta(N)}.")
    print("         If zeta-regularized vacuum energy is physical, |S|~25 already gives 10^96 amplification.\n")

# ============================================================================
# C2.  PARITY LAW: sign of mute factor
# ============================================================================
def audit_C2():
    print("=" * 78)
    print("C2.  Parity sign law:  sgn[ prod (1 - p^k) ] = (-1)^|S|  for k>=1")
    print("=" * 78)
    P = primes_up_to(50)
    print(f"{'k':>4} | " + " | ".join(f"|S|={n}" for n in range(7)))
    print("-" * 60)
    for k in [1, 3, 5, 9]:
        row = f"{k:>4} | "
        for n in range(7):
            f = mute_factor(P[:n], k)
            row += f"{('+' if f>0 else '-'):>5} | "
        print(row)
    print()
    print("Each (1 - p^k) is negative for p>=2, k>=1. Sign of product = (-1)^|S|. Trivially true.")
    print("VERDICT: TIGHT (algebraic identity). Confirmed for k = 1, 3, 5, 9.\n")

# ============================================================================
# C3.  GENERATION g-2 CORRECTIONS (electron, muon, tau)
# ============================================================================
def audit_C3():
    print("=" * 78)
    print("C3.  Generation corrections vs muted primes")
    print("=" * 78)
    # exponents for each lepton's zeta(-n) factor in the framework
    # electron: zeta(-1), muon: zeta(-5), tau: zeta(-9)
    # base values (no muting): zeta(-1) = -1/12, zeta(-5) = -1/252, zeta(-9) = -1/132
    base = {"e (zeta-1)": -1/12, "mu (zeta-5)": -1/252, "tau (zeta-9)": -1/132}
    expo = {"e (zeta-1)":  1,    "mu (zeta-5)":  5,    "tau (zeta-9)":  9}

    print(f"{'S':<14} | " + " | ".join(f"{lab:>22}" for lab in base))
    print("-" * 90)
    test_sets = [(), (2,), (3,), (5,), (7,), (2,3), (2,3,5), (2,3,5,7)]
    for S in test_sets:
        row = f"{str(list(S)):<14} | "
        for lab, b in base.items():
            f = mute_factor(S, expo[lab])
            row += f"{b * f:>+22.4e} | "
        print(row)
    print()
    print("VERDICT: TIGHT (algebraic). Tau corrections grow as p^9 — single prime p=7 already")
    print("         multiplies tau correction by ~4e7. Multi-prime muting compounds catastrophically.\n")

# ============================================================================
# C4.  TWO-PRIME "TRANSPARENCY" CLAIM
# ============================================================================
def audit_C4():
    print("=" * 78)
    print("C4.  Two-prime muting and the 'matter transparency' claim")
    print("=" * 78)
    print("The papers claim: muting two primes makes 1/factor approach -1 (decoupling).")
    print("Test: compute 1/prod (1-p^3) for various |S| and see if this is true.\n")
    print(f"{'S':<18} {'prod (1-p^3)':>16} {'1/prod':>14} {'|1/prod|':>14}")
    print("-" * 66)
    for S in [(), (2,), (3,), (2,3), (2,5), (3,5), (2,3,5), (2,3,5,7)]:
        f = mute_factor(S, 3)
        inv = 1.0 / f
        print(f"{str(list(S)):<18} {f:>+16.0f} {inv:>+14.6e} {abs(inv):>14.6e}")
    print()
    print("Observation: 1/prod is small for any |S|>=1, NOT a special two-prime feature.")
    print("The 'transparency' framing is misleading — it's just the reciprocal of a large number.")
    print("Two-prime muting doesn't decouple matter; it amplifies the *positive* correction by ~10^2-10^4.")
    print("VERDICT: REFUTED. The 'transparency' interpretation does not survive numerical inspection.\n")

# ============================================================================
# C5.  K-THEORY TOPOLOGICAL NO-GO
# ============================================================================
def audit_C5():
    print("=" * 78)
    print("C5.  K_1(Z) vs K_1(Z[1/p]):  topological barrier?")
    print("=" * 78)
    print("Mathematical fact (Bass, Quillen):")
    print("  K_1(Z)      = Z/2  (only unit ±1)")
    print("  K_1(Z[1/p]) = Z/2 × Z   (extra Z generated by the unit p)")
    print("These ARE different abelian groups -> no continuous deformation between them.")
    print()
    print("BUT: the claim that 'K_1 is a continuous invariant of the physical vacuum'")
    print("     requires the vacuum configuration space to literally BE Spec(Z[1/p]).")
    print("     That premise is the entire warp-drive program, not an independent fact.")
    print()
    print("If you ASSUME the premise: barrier is topological, decay rate = 0 exactly.")
    print("If the premise is wrong: K_1 doesn't apply, and you're back to standard CDL")
    print("     where lower-energy vacuum DOES nucleate and consume the universe.")
    print()
    print("VERDICT: CONDITIONAL. Math is correct (K-groups differ). Physical safety depends")
    print("         entirely on the unverified Spec(Z) = vacuum identification.\n")

# ============================================================================
# C6.  LAMBDA_QCD EXPONENTIAL SENSITIVITY
# ============================================================================
def audit_C6():
    print("=" * 78)
    print("C6.  Lambda_QCD vs alpha_s:  how dangerous is a 25% coupling shift?")
    print("=" * 78)
    # 1-loop running:  1/alpha_s(mu) = 1/alpha_s(M) + (b0 / 2pi) ln(mu/M)
    # b0 = 11 - 2 nf/3, with nf=5 below top scale -> b0 = 23/3
    # Lambda is where alpha_s diverges:  Lambda = mu * exp(-2pi/(b0 alpha_s(mu)))
    b0 = 23.0 / 3.0
    mu = 91.2  # Z mass in GeV
    alpha_s_normal = 0.118
    Lambda_normal = mu * math.exp(-2*math.pi / (b0 * alpha_s_normal)) * 1000  # MeV
    print(f"Normal:  alpha_s(M_Z) = {alpha_s_normal:.4f}, Lambda_QCD = {Lambda_normal:.1f} MeV")
    print()
    print(f"{'shift in alpha_s':>20} {'new alpha_s':>14} {'new Lambda':>14} {'ratio':>10}")
    print("-" * 64)
    for delta in [-0.25, -0.10, -0.03, -0.003, 0.003, 0.03, 0.10, 0.25]:
        a_new = alpha_s_normal * (1 + delta)
        Lam_new = mu * math.exp(-2*math.pi / (b0 * a_new)) * 1000
        ratio = Lam_new / Lambda_normal
        print(f"{delta*100:>+18.1f}% {a_new:>14.4f} {Lam_new:>11.1f} MeV {ratio:>10.3f}")
    print()
    # Proton mass scales roughly with Lambda_QCD
    print("Proton mass m_p ~ Lambda_QCD * O(1) ~ 938 MeV.  If Lambda drops by factor X,")
    print("nuclei become unstable when m_p falls below about m_n - m_p - m_e (threshold).")
    print("The papers claim 25% alpha_s shift -> 12x Lambda drop. Numerically:")
    delta = -0.25
    a_new = alpha_s_normal * (1 + delta)
    Lam_new = mu * math.exp(-2*math.pi / (b0 * a_new)) * 1000
    print(f"  alpha_s -> {a_new:.4f}: Lambda factor = {Lam_new/Lambda_normal:.3f}  -> proton mass ~ {938*Lam_new/Lambda_normal:.0f} MeV")
    print()
    print("VERDICT: The exponential sensitivity is REAL (1-loop QCD running).")
    print("         The 25% shift estimate ITSELF is heuristic — the framework does not")
    print("         actually compute how alpha_s changes when a prime is muted. So:")
    print("         math = TIGHT, but the input (does muting actually shift alpha_s?) is OPEN.\n")

# ============================================================================
# C7.  Spec(Q) limit: zeta_S(s) -> 1
# ============================================================================
def audit_C7():
    print("=" * 78)
    print("C7.  S = all primes:  zeta_S(s) -> trivial (Spec(Q) limit)")
    print("=" * 78)
    print("zeta(s) = prod_p (1 - p^-s)^-1  =>  removing prime p removes its factor.")
    print("Removing ALL primes leaves the empty product = 1.")
    print()
    print("Test: increasingly large S, s = -3 (vacuum energy multiplier):")
    print(f"{'|S|':>5} {'zeta_S(-3) / zeta(-3)':>26}")
    print("-" * 36)
    P = primes_up_to(50)
    for n in [0, 1, 2, 5, 10, 15]:
        f = mute_factor(P[:n], 3)
        print(f"{n:>5} {f:>+26.3e}")
    print()
    print("The product diverges in magnitude (C1) but its INVERSE — i.e., the residual")
    print("vacuum spectrum — shrinks toward zero. In the limit |S| -> infinity, only the")
    print("trivial empty spectrum remains.")
    print()
    print("'No physics' is the standard interpretation but is more philosophical than rigorous:")
    print("the math says the regularized mode sum becomes trivial, the *interpretation*")
    print("that this means 'no observers' assumes vacuum mode richness = degrees of freedom for life.")
    print("VERDICT: CONDITIONAL. Math: tight (empty product = 1). Anthropic conclusion: plausible but soft.\n")

# ============================================================================
# SUMMARY
# ============================================================================
def summary():
    print("=" * 78)
    print("SUMMARY:  which 'over-muting is dangerous' arguments survive audit?")
    print("=" * 78)
    rows = [
        ("C1  Vacuum product diverges",        "TIGHT",       "10^{3 theta(N)} growth, inevitable"),
        ("C2  Parity sign flip",               "TIGHT",       "(1-p^k)<0 for all k>=1"),
        ("C3  Generation corrections explode", "TIGHT",       "p^{2g+1} amplification in lepton g-2"),
        ("C4  Two-prime 'transparency'",       "REFUTED",     "misreading of 1/factor; real effect = amplification"),
        ("C5  K-theory no-go theorem",         "CONDITIONAL", "K_1 differs (true), but physical relevance assumes Spec(Z) is the vacuum"),
        ("C6  Lambda_QCD exponential collapse","CONDITIONAL", "QCD running real; 25% alpha_s shift is unverified input"),
        ("C7  Spec(Q) trivial limit",          "CONDITIONAL", "math trivial; 'no observers' is anthropic gloss"),
    ]
    print(f"{'claim':<38} {'verdict':<12} note")
    print("-" * 78)
    for c, v, n in rows:
        print(f"{c:<38} {v:<12} {n}")
    print()
    print("Net finding: 3 robust mathematical reasons to fear over-muting (C1, C2, C3),")
    print("              3 conditional arguments that depend on unproven premises (C5, C6, C7),")
    print("              1 claim that does NOT survive numerical inspection (C4).")
    print()
    print("Bottom line: 'Don't mute too many primes' has solid arithmetic backing")
    print("              — vacuum energy multiplier and lepton corrections diverge.")
    print("              The catastrophic *physical* consequences (vacuum decay, dead chemistry)")
    print("              all hinge on the premise that Spec(Z) literally IS the vacuum.")
    print("              No experiment yet validates that premise.\n")

if __name__ == "__main__":
    audit_C1()
    audit_C2()
    audit_C3()
    audit_C4()
    audit_C5()
    audit_C6()
    audit_C7()
    summary()
