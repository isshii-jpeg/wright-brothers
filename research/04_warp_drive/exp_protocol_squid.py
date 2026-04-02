"""
EXPERIMENTAL PROTOCOL: ARITHMETIC VACUUM ENERGY MEASUREMENT
============================================================

Experiment: Measure the change in Casimir vacuum energy when
"prime channel p=2" is muted in a superconducting microwave circuit.

This is the FIRST proposed test of whether the arithmetic (Euler product)
structure of the Riemann zeta function has a physical counterpart in
the quantum vacuum.

Theoretical prediction:
  The vacuum energy of a cavity with mode spectrum {1,2,3,4,...} is
  proportional to ζ(-1) = -1/12 (zeta-regularized).

  If we suppress all even harmonics (modes divisible by 2), the
  remaining spectrum {1,3,5,7,...} has vacuum energy proportional to
  ζ(-1) × (1 - 2^{-(-1)}) = ζ(-1) × (1 - 2) = (-1/12)×(-1) = +1/12.

  The SIGN FLIPS from negative to positive.
  ΔE = E_{odd} - E_{full} = (+1/12) - (-1/12) = +1/6 (in units of ℏω₀/2).

  This is a QUALITATIVE prediction: the vacuum energy should change sign.

Heritage:
  - Wilson et al., Nature 479, 376-379 (2011): Dynamical Casimir effect
    in superconducting circuit. Proved photon creation from vacuum.
  - Lähteenmäki et al., PNAS 110, 4234-4238 (2013): Dynamical Casimir
    in Josephson metamaterial.
  - Johansson et al., PRL 103, 147003 (2009): Theory of DCE in SC circuit.

Wright Brothers, 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# Physical constants
hbar = 1.054571817e-34   # J·s
c = 2.99792458e8          # m/s
k_B = 1.380649e-23        # J/K
Phi_0 = 2.067833848e-15   # Wb (magnetic flux quantum)
e = 1.602176634e-19        # C
pi = np.pi

print("=" * 70)
print("  EXPERIMENTAL PROTOCOL: ARITHMETIC VACUUM ENERGY MEASUREMENT")
print("  'Does muting prime p=2 flip the sign of vacuum energy?'")
print("=" * 70)

# ============================================================================
#  SECTION 1: CIRCUIT DESIGN
# ============================================================================

print("\n" + "=" * 70)
print("  SECTION 1: CIRCUIT DESIGN")
print("=" * 70)
print()

# The circuit: a coplanar waveguide (CPW) transmission line resonator
# with embedded SQUID-based notch filters.

# CPW resonator parameters
L_res = 10e-3          # resonator length [m] (10 mm)
Z_0 = 50.0             # characteristic impedance [Ω]
c_eff = 1.2e8          # effective speed of light [m/s] (~0.4c in Nb on Si)
epsilon_eff = (c / c_eff)**2  # effective dielectric constant

omega_0 = pi * c_eff / L_res          # fundamental angular frequency
f_0 = omega_0 / (2 * pi)              # fundamental frequency [Hz]
omega_n = lambda n: n * omega_0        # n-th harmonic

print(f"  Coplanar Waveguide Resonator:")
print(f"    Material: Niobium on silicon substrate")
print(f"    Length L = {L_res*1e3:.0f} mm")
print(f"    Impedance Z₀ = {Z_0:.0f} Ω")
print(f"    Effective ε = {epsilon_eff:.1f}")
print(f"    Effective c = {c_eff:.2e} m/s")
print()
print(f"  Mode spectrum:")
print(f"    ω_n = n·π·c_eff/L = n × {omega_0:.3e} rad/s")
print(f"    f_n = n × {f_0/1e9:.3f} GHz")
print()

# List first 10 modes
print(f"  {'Mode n':>8s}  {'Frequency':>12s}  {'Status (with p=2 filter)':>25s}")
print(f"  {'-'*50}")
for n in range(1, 11):
    f_n = n * f_0 / 1e9
    status = "MUTED (even)" if n % 2 == 0 else "ACTIVE (odd)"
    color_hint = "×" if n % 2 == 0 else "✓"
    print(f"  {n:>8d}  {f_n:>10.3f} GHz  {color_hint} {status}")

print()
print(f"  Maximum usable mode (before substrate absorption): n ~ 20")
print(f"    → f_max ~ {20*f_0/1e9:.1f} GHz")

# ============================================================================
#  SECTION 2: SQUID NOTCH FILTER DESIGN
# ============================================================================

print("\n" + "=" * 70)
print("  SECTION 2: SQUID NOTCH FILTER DESIGN")
print("=" * 70)
print()

# Each SQUID acts as a tunable nonlinear resonator.
# We need one SQUID filter per even harmonic to suppress.
# For modes 2,4,6,...,20 → 10 SQUID filters.

# SQUID parameters
I_c = 1.0e-6          # critical current [A] (typical: 0.1-10 μA)
C_J = 1.0e-15          # junction capacitance [F] (typical: 1 fF)
L_J = Phi_0 / (2 * pi * I_c)  # Josephson inductance

# SQUID resonance frequency
omega_SQUID = 1 / np.sqrt(L_J * C_J)
f_SQUID = omega_SQUID / (2 * pi)

print(f"  SQUID Notch Filter Parameters:")
print(f"    Junction critical current I_c = {I_c*1e6:.1f} μA")
print(f"    Junction capacitance C_J = {C_J*1e15:.1f} fF")
print(f"    Josephson inductance L_J = Φ₀/(2πI_c) = {L_J*1e9:.2f} nH")
print(f"    SQUID plasma frequency = {f_SQUID/1e9:.2f} GHz")
print()

# Tuning: Apply external flux Φ_ext to shift SQUID frequency
# ω_SQUID(Φ_ext) = ω_0 × |cos(πΦ_ext/Φ₀)|^{1/2}
# This allows tuning each SQUID to a specific even harmonic.

print(f"  Frequency tuning via external flux:")
print(f"    ω(Φ_ext) = ω_plasma × |cos(πΦ_ext/Φ₀)|^{{1/2}}")
print()

N_even_max = 10  # suppress modes 2,4,...,20
print(f"  Required SQUID filters: {N_even_max}")
print(f"  {'SQUID #':>8s}  {'Target mode':>12s}  {'Target freq':>12s}  {'Φ_ext/Φ₀':>10s}")
print(f"  {'-'*48}")

for i in range(N_even_max):
    n_target = 2 * (i + 1)
    f_target = n_target * f_0
    # Required flux: cos(πΦ/Φ₀) = (f_target/f_SQUID)^2
    cos_val = (f_target / f_SQUID)**2
    if abs(cos_val) <= 1:
        phi_ratio = np.arccos(cos_val) / pi
        print(f"  {i+1:>8d}  {n_target:>12d}  {f_target/1e9:>10.3f} GHz  {phi_ratio:>10.4f}")
    else:
        print(f"  {i+1:>8d}  {n_target:>12d}  {f_target/1e9:>10.3f} GHz  {'OUT OF RANGE':>10s}")

# Check tuning range
print()
f_target_max = 2 * N_even_max * f_0
if f_target_max > f_SQUID:
    print(f"  ⚠ Maximum target frequency ({f_target_max/1e9:.1f} GHz) exceeds")
    print(f"    SQUID plasma frequency ({f_SQUID/1e9:.1f} GHz).")
    print(f"    Options:")
    print(f"      (a) Use higher-I_c junctions (smaller L_J, higher ω_plasma)")
    print(f"      (b) Limit to first few even harmonics (n=2,4,6)")
    print(f"      (c) Use series-array SQUID for wider bandwidth")

    # Recompute with higher I_c
    I_c_new = 5.0e-6
    L_J_new = Phi_0 / (2 * pi * I_c_new)
    f_SQUID_new = 1 / (2 * pi * np.sqrt(L_J_new * C_J))
    print(f"\n    With I_c = {I_c_new*1e6:.0f} μA:")
    print(f"      f_SQUID = {f_SQUID_new/1e9:.1f} GHz (covers up to mode ~{int(f_SQUID_new/f_0)})")

# ============================================================================
#  SECTION 3: QUALITY FACTOR AND SUPPRESSION DEPTH
# ============================================================================

print("\n" + "=" * 70)
print("  SECTION 3: SUPPRESSION QUALITY REQUIREMENTS")
print("=" * 70)
print()

# The SQUID notch filter has a quality factor Q_notch.
# Suppression depth S = 1 - 1/(1 + Q_notch²·(δω/ω)²) for δω off resonance.
# At resonance: S → Q_notch-dependent.
# For effective mode muting, we need suppression > 20 dB (factor 100 in power).

Q_notch_target = 1000  # typical SQUID quality factor at mK temperatures
suppression_dB = 10 * np.log10(1 + Q_notch_target**2)

print(f"  SQUID quality factor Q = {Q_notch_target}")
print(f"  On-resonance suppression: {suppression_dB:.0f} dB")
print(f"  Bandwidth per notch: Δf = f_target/Q = {f_0*2/Q_notch_target/1e6:.1f} MHz")
print()

# Cross-talk: adjacent modes are separated by f_0.
# Need the notch to be narrow enough not to affect odd modes.
print(f"  Mode spacing: Δf_modes = f_0 = {f_0/1e9:.3f} GHz")
print(f"  Notch width: Δf_notch = {f_0*2/(Q_notch_target*1e6):.1f} MHz")
print(f"  Selectivity ratio: Δf_modes/Δf_notch = {f_0/(f_0*2/Q_notch_target):.0f}")
print()

if Q_notch_target > 100:
    print(f"  ✓ Q = {Q_notch_target} provides sufficient selectivity.")
    print(f"    Notch width << mode spacing → minimal cross-talk to odd modes.")
else:
    print(f"  ✗ Q too low. Cross-talk between modes will contaminate measurement.")

# ============================================================================
#  SECTION 4: MEASUREMENT PROTOCOL
# ============================================================================

print("\n" + "=" * 70)
print("  SECTION 4: MEASUREMENT PROTOCOL")
print("=" * 70)
print()

print("""  OVERVIEW:
  We measure the vacuum energy shift by comparing two configurations:
    A) ALL modes active (SQUIDs detuned off-resonance)
    B) Even modes suppressed (SQUIDs tuned to even harmonics)

  The difference reveals the contribution of even-harmonic vacuum
  fluctuations to the total zero-point energy.

  KEY MEASUREMENT: Radiation pressure / Casimir force on a probe.

  STEP-BY-STEP PROTOCOL:

  1. COOL DOWN
     - Cool circuit to T < 20 mK in dilution refrigerator
     - Verify T < ℏω₀/k_B to ensure quantum ground state""")
print(f"       T_quantum = ℏω₀/k_B = {hbar*omega_0/k_B*1e3:.0f} mK")
print(f"       → Need T < {hbar*omega_0/k_B*1e3/5:.0f} mK for ground state occupation > 99%")

print("""
  2. BASELINE MEASUREMENT (Configuration A: all modes)
     - Detune all SQUID filters off-resonance (Φ_ext → 0)
     - Measure:
       (a) Resonator transmission spectrum S₂₁(f)
       (b) Noise power spectral density (thermal + quantum)
       (c) Photon number ⟨n⟩ in each mode via dispersive readout

  3. ARITHMETIC FILTER ON (Configuration B: even modes muted)
     - Tune each SQUID to its target even harmonic
     - Wait for thermalization (τ ~ Q/ω ~ 100 ns per mode)
     - Measure same quantities as step 2

  4. DIFFERENTIAL MEASUREMENT
     ΔS₂₁ = S₂₁(B) - S₂₁(A)  → shows mode suppression profile
     ΔP_noise = P(B) - P(A)    → vacuum energy change
     Δ⟨n⟩ = ⟨n(B)⟩ - ⟨n(A)⟩  → per-mode zero-point shift

  5. CASIMIR FORCE MEASUREMENT (advanced)
     - Use a mechanically compliant element (membrane, nanomechanical
       resonator) coupled to the transmission line
     - Measure frequency shift of mechanical mode
     - ΔΩ_mech ∝ d²E_vac/dx² → direct probe of vacuum energy curvature""")

# ============================================================================
#  SECTION 5: THEORETICAL PREDICTIONS
# ============================================================================

print("\n" + "=" * 70)
print("  SECTION 5: QUANTITATIVE PREDICTIONS")
print("=" * 70)
print()

# Zero-point energy per mode: E_n = ℏω_n/2
E_zp_1 = hbar * omega_0 / 2
print(f"  Zero-point energy of fundamental mode:")
print(f"    E_1 = ℏω₁/2 = {E_zp_1:.3e} J = {E_zp_1/e*1e6:.3f} μeV")
print(f"    = {E_zp_1/(k_B):.3e} K (temperature equivalent)")
print()

# Total zero-point energy (first N modes, hard cutoff)
N_modes = 20
E_total_full = sum(hbar * omega_n(n) / 2 for n in range(1, N_modes + 1))
E_total_odd = sum(hbar * omega_n(n) / 2 for n in range(1, N_modes + 1) if n % 2 != 0)
E_total_even = sum(hbar * omega_n(n) / 2 for n in range(1, N_modes + 1) if n % 2 == 0)

Delta_E = E_total_odd - E_total_full  # = -E_total_even

print(f"  With N = {N_modes} modes (hard cutoff):")
print(f"    E_full  = Σ_{{n=1}}^{{{N_modes}}} ℏω_n/2 = {E_total_full:.3e} J")
print(f"    E_odd   = Σ_{{odd n}} ℏω_n/2     = {E_total_odd:.3e} J")
print(f"    E_even  = Σ_{{even n}} ℏω_n/2    = {E_total_even:.3e} J")
print(f"    ΔE = E_odd - E_full              = {Delta_E:.3e} J")
print(f"       = -{E_total_even:.3e} J  (we remove the even modes)")
print()

# Zeta-regularized prediction
print(f"  Zeta-regularized prediction:")
print(f"    E_full ∝ ζ(-1) = -1/12 = {-1/12:.6f}")
print(f"    E_odd  ∝ ζ(-1) × (1 - 2^{{1}}) = +1/12 = {1/12:.6f}")
print(f"    Ratio: E_odd / E_full = {(1/12) / (-1/12):.1f}")
print(f"    → Sign FLIP from negative to positive")
print()
print(f"    This sign flip is the KEY prediction.")
print(f"    It corresponds to: removing even modes doesn't just")
print(f"    reduce the vacuum energy — it makes it REPULSIVE.")

# ============================================================================
#  SECTION 6: WHAT DOES SUCCESS LOOK LIKE?
# ============================================================================

print("\n" + "=" * 70)
print("  SECTION 6: SUCCESS CRITERIA AND IMPLICATIONS")
print("=" * 70)
print()

print("""  LEVEL 1 SUCCESS (proof of concept):
    Measure ΔE when even harmonics are suppressed.
    Confirm ΔE ≠ 0 to statistical significance.
    → Proves: vacuum energy depends on mode arithmetic.

  LEVEL 2 SUCCESS (quantitative match):
    Measure ΔE/E_full and compare to ζ-regularized prediction.
    Confirm ratio matches (1 - 2^{s+1}) for appropriate s.
    → Proves: zeta function correctly describes vacuum mode structure.

  LEVEL 3 SUCCESS (multi-prime):
    Repeat with p=3 filter (suppress modes divisible by 3).
    Then with p=2 AND p=3 simultaneously.
    Check that ΔE(p=2,3) = ΔE(p=2) × (1 - 3^{s+1})/(1).
    → Proves: Euler product formula is a PHYSICAL LAW.

  LEVEL 4 SUCCESS (sign control):
    Demonstrate controllable sign-flipping of vacuum energy:
    Mute 0 primes: E < 0 (attractive Casimir)
    Mute 1 prime:  E > 0 (repulsive!)
    Mute 2 primes: E < 0 (attractive again)
    → Proves: arithmetic structure controls vacuum energy sign.
    → Direct path to exotic matter engineering.

  IMPLICATIONS OF LEVEL 4:
    If we can flip the sign of vacuum energy at will,
    and if this scales to macroscopic systems,
    then we have a physical mechanism for generating
    the negative energy density required by the Alcubierre metric.

    This would be the first step toward a warp drive.""")

# ============================================================================
#  SECTION 7: ERROR BUDGET AND SYSTEMATICS
# ============================================================================

print("\n" + "=" * 70)
print("  SECTION 7: ERROR BUDGET")
print("=" * 70)
print()

T_base = 15e-3  # base temperature [K]
n_thermal = 1 / (np.exp(hbar * omega_0 / (k_B * T_base)) - 1)

print(f"  Major systematic errors:")
print()
print(f"  1. THERMAL PHOTONS")
print(f"     At T = {T_base*1e3:.0f} mK, ℏω₀/k_BT = {hbar*omega_0/(k_B*T_base):.1f}")
print(f"     Thermal occupation: ⟨n_th⟩ = {n_thermal:.2e}")
print(f"     → {'✓ Negligible' if n_thermal < 0.01 else '✗ Significant'}")
print()

print(f"  2. SQUID BACK-ACTION")
print(f"     Each SQUID adds noise from its own quantum fluctuations.")
print(f"     Estimated back-action photons: ~{1/(2*Q_notch_target):.1e} per mode")
print(f"     → {'✓ Manageable with Q > 1000' if Q_notch_target >= 1000 else '✗ Needs higher Q'}")
print()

print(f"  3. MODE LEAKAGE")
print(f"     Imperfect suppression → residual even-mode contribution.")
print(f"     At {suppression_dB:.0f} dB suppression: residual = {10**(-suppression_dB/10):.1e}")
print(f"     → ✓ {suppression_dB:.0f} dB sufficient for factor-of-2 energy change")
print()

print(f"  4. CROSS-TALK")
print(f"     SQUID tuned to mode 2n may affect mode 2n±1.")
print(f"     At Q = {Q_notch_target}: spillover at ±f_0 = {10*np.log10(1 + Q_notch_target**2*(2*pi*f_0/(omega_0*2/Q_notch_target))**2):.0f} dB down")
print(f"     → ✓ Negligible for Q > 100")

# ============================================================================
#  SECTION 8: RESOURCE ESTIMATES
# ============================================================================

print("\n" + "=" * 70)
print("  SECTION 8: RESOURCES NEEDED")
print("=" * 70)
print()

print("""  FACILITY:
    - Dilution refrigerator (base T < 20 mK)           REQUIRED
    - Microwave measurement setup (VNA, 1-20 GHz)      REQUIRED
    - Nb thin-film deposition & e-beam lithography      REQUIRED
    - SQUID fabrication (Al/AlOx/Al junctions)          REQUIRED

  INSTITUTIONS WITH CAPABILITY:
    - Yale (Schoelkopf lab, Devoret lab)
    - ETH Zurich (Wallraff lab)
    - RIKEN (Nakamura lab, Japan)
    - Chalmers University (Wilson's lab — did the DCE experiment!)
    - Delft (DiCarlo lab)
    - Google Quantum AI, IBM Quantum

  ESTIMATED COST:
    - If using existing lab with dilution fridge: ~$50-100K (fabrication + measurement time)
    - New setup from scratch: ~$2-5M (mostly the dilution fridge)
    - Can be done as student project at equipped lab: ~$20K + labor

  TIMELINE:
    Month 1-2:  Circuit design and simulation (COMSOL, Sonnet)
    Month 3-4:  Fabrication (Nb CPW + SQUID array)
    Month 5-6:  Cooldown + baseline characterization
    Month 7-8:  Prime filter measurements (p=2, then p=3)
    Month 9-10: Data analysis, systematics, repeat
    Month 11-12: Paper writing

  TOTAL: ~12 months from design to publication""")

# ============================================================================
#  SECTION 9: SCALING TO WARP DRIVE
# ============================================================================

print("\n" + "=" * 70)
print("  SECTION 9: FROM CIRCUIT EXPERIMENT TO WARP DRIVE")
print("=" * 70)
print()

# Energy scale comparison
E_circuit = abs(Delta_E)
E_warp = 1e47  # rough Alcubierre energy [J] for 1c bubble

print(f"  Energy in our circuit experiment: {E_circuit:.2e} J")
print(f"  Energy for warp bubble (1c, 50m): ~{E_warp:.0e} J")
print(f"  Gap: {E_warp/E_circuit:.0e} orders of magnitude")
print()

print("""  SCALING PATHWAY (speculative, requires breakthroughs):

  Stage 1: PROOF OF PRINCIPLE (this experiment)
    - Scale: single circuit, ~fJ vacuum energy
    - Prove: arithmetic mode filtering changes vacuum energy
    - Prove: sign flip matches zeta-regularized prediction

  Stage 2: COHERENT AMPLIFICATION
    - Array of N synchronized circuits
    - If vacuum energy effects are COHERENT: E_total ∝ N²
    - 10⁶ circuits → 10¹² × single circuit energy
    - Also explore: longer resonators, higher modes

  Stage 3: MATERIAL IMPLEMENTATION
    - Translate circuit design to bulk metamaterial
    - 3D photonic crystal with arithmetic band structure
    - Potentially: Euler product crystal (sieve of Eratosthenes in material)
    - Energy density scales with material volume

  Stage 4: TOPOLOGICAL PROTECTION
    - Engineer Z/pZ topological invariant in material
    - Arithmetic boundary conditions become robust (topologically protected)
    - Edge states at arithmetic domain walls → concentrated negative energy

  Stage 5: MACROSCOPIC VACUUM ENGINEERING
    - Shape the arithmetic metamaterial into warp bubble geometry
    - Each prime filter layer controls one Euler factor
    - The full Euler product → full vacuum energy control
    - Alcubierre metric as emergent geometry of arithmetic vacuum

  This pathway spans decades and requires multiple breakthroughs.
  But Stage 1 can be done NOW, and it would be a discovery
  regardless of whether it leads to warp drive.""")

# ============================================================================
#  SECTION 10: VISUALIZATION
# ============================================================================

fig = plt.figure(figsize=(16, 20))
fig.patch.set_facecolor('#0a0a1a')
gs = fig.add_gridspec(4, 2, hspace=0.35, wspace=0.3)

# Panel 1: Circuit schematic
ax = fig.add_subplot(gs[0, :])
ax.set_xlim(0, 10)
ax.set_ylim(0, 3)

# Transmission line
ax.plot([0.5, 9.5], [1.8, 1.8], color='#00d4ff', linewidth=4, solid_capstyle='round')
ax.plot([0.5, 9.5], [1.2, 1.2], color='#00d4ff', linewidth=4, solid_capstyle='round')
ax.text(5, 2.1, 'Nb Coplanar Waveguide (L = 10 mm, f₀ = {:.1f} GHz)'.format(f_0/1e9),
        ha='center', color='white', fontsize=10)

# SQUIDs
squid_positions = [1.5, 3.0, 4.5, 6.0, 7.5]
for i, x in enumerate(squid_positions):
    n_target = 2 * (i + 1)
    # Draw SQUID
    rect = plt.Rectangle((x-0.2, 1.2), 0.4, 0.6, fill=True,
                          facecolor='#ff6b6b', edgecolor='white', linewidth=1.5, alpha=0.8)
    ax.add_patch(rect)
    ax.text(x, 0.8, f'SQUID\n@ {n_target}ω₀\n({n_target*f_0/1e9:.1f} GHz)',
            ha='center', va='top', color='#ff6b6b', fontsize=7)

# Input/output
ax.annotate('', xy=(0.5, 1.5), xytext=(-0.3, 1.5),
            arrowprops=dict(arrowstyle='->', color='#ffd93d', lw=2))
ax.text(-0.3, 1.5, 'μW\ninput', ha='right', color='#ffd93d', fontsize=8, va='center')
ax.annotate('', xy=(10.3, 1.5), xytext=(9.5, 1.5),
            arrowprops=dict(arrowstyle='->', color='#6bff8d', lw=2))
ax.text(10.3, 1.5, 'μW\noutput', ha='left', color='#6bff8d', fontsize=8, va='center')

# Temperature label
ax.text(5, 0.2, 'T < 20 mK (dilution refrigerator)',
        ha='center', color='#aaa', fontsize=9, style='italic')

ax.set_title('Circuit Design: CPW Resonator with SQUID Prime Filters',
             color='#ffd93d', fontsize=12, fontweight='bold', pad=10)
ax.axis('off')
ax.set_facecolor('#0a0a1a')

# Panel 2: Mode spectrum (full vs filtered)
ax = fig.add_subplot(gs[1, 0])
n_show = 20

for n in range(1, n_show + 1):
    f_n = n * f_0 / 1e9
    # Full spectrum
    ax.barh(f_n, 0.4, left=0.0, height=f_0/1e9*0.6,
            color='#00d4ff', alpha=0.8)
    # Filtered spectrum
    if n % 2 != 0:
        ax.barh(f_n, 0.4, left=0.6, height=f_0/1e9*0.6,
                color='#ffd93d', alpha=0.8)
    else:
        ax.barh(f_n, 0.4, left=0.6, height=f_0/1e9*0.6,
                color='#ff6b6b', alpha=0.2)
        ax.text(1.15, f_n, '×', color='#ff6b6b', fontsize=12,
                ha='center', va='center', fontweight='bold')

ax.set_xlim(-0.2, 1.4)
ax.set_xticks([0.2, 0.8])
ax.set_xticklabels(['Full\nspectrum', 'p=2\nfiltered'], color='white', fontsize=9)
ax.set_ylabel('Frequency [GHz]', color='white')
ax.set_title('Mode Spectrum', color='white', fontsize=10)
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.1, axis='y')

# Panel 3: Vacuum energy per mode
ax = fig.add_subplot(gs[1, 1])
modes = range(1, N_modes + 1)
E_per_mode = [hbar * omega_n(n) / 2 for n in modes]
colors = ['#ffd93d' if n % 2 != 0 else '#ff6b6b' for n in modes]
labels = ['odd' if n % 2 != 0 else 'even' for n in modes]

ax.bar(modes, [e / E_zp_1 for e in E_per_mode], color=colors, alpha=0.8)
ax.set_xlabel('Mode number n', color='white')
ax.set_ylabel('E_n / E₁', color='white')
ax.set_title('Zero-Point Energy per Mode', color='white', fontsize=10)
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.1)

# Legend
from matplotlib.patches import Patch
legend_elements = [Patch(facecolor='#ffd93d', alpha=0.8, label='Active (odd)'),
                   Patch(facecolor='#ff6b6b', alpha=0.8, label='Muted (even)')]
ax.legend(handles=legend_elements, fontsize=8, loc='upper left',
          facecolor='#1a1a2e', edgecolor='white', labelcolor='white')

# Panel 4: Zeta-regularized prediction
ax = fig.add_subplot(gs[2, 0])

# Show how vacuum energy changes as primes are muted
primes_list = [2, 3, 5, 7, 11, 13]
zeta_m1 = -1/12

# For s = -1 (relevant for 1D vacuum energy)
cumulative_s1 = [zeta_m1]
product = zeta_m1
for p in primes_list:
    product *= (1 - p)
    cumulative_s1.append(product)

x_pos = range(len(cumulative_s1))
x_labels = ['none'] + [str(p) for p in primes_list]
colors_bar = ['#00d4ff'] + ['#ff6b6b' if v < 0 else '#6bff8d' for v in cumulative_s1[1:]]

ax.bar(x_pos, cumulative_s1, color=colors_bar, alpha=0.8, edgecolor='white', linewidth=0.5)
ax.axhline(y=0, color='white', linewidth=1, alpha=0.5)
ax.set_xticks(x_pos)
ax.set_xticklabels(x_labels, color='white', fontsize=9)
ax.set_xlabel('Primes muted (cumulative)', color='white')
ax.set_ylabel('Modified ζ(-1)', color='white')
ax.set_title('Vacuum Energy Sign Oscillation\n(ζ-regularized, s = -1)',
             color='white', fontsize=10)
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')
ax.grid(alpha=0.1)

# Annotate sign flips
for i, val in enumerate(cumulative_s1):
    sign = '+' if val > 0 else '−'
    ax.text(i, val + (0.5 if val > 0 else -0.5), sign,
            ha='center', va='center', color='white', fontsize=14, fontweight='bold')

# Panel 5: Measurement timeline
ax = fig.add_subplot(gs[2, 1])
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)

phases = [
    (0, 2, 'Design\n& Simulate', '#00d4ff'),
    (2, 4, 'Fabricate', '#ffd93d'),
    (4, 6, 'Cooldown &\nBaseline', '#6bff8d'),
    (6, 8, 'Prime Filter\nMeasurements', '#ff6b6b'),
    (8, 10, 'Systematics\n& Repeat', '#b388ff'),
    (10, 12, 'Analysis\n& Paper', '#ff8a65'),
]

for i, (start, end, label, color) in enumerate(phases):
    y = 6 - i
    rect = plt.Rectangle((start, y - 0.35), end - start, 0.7,
                          facecolor=color, alpha=0.7, edgecolor='white', linewidth=1)
    ax.add_patch(rect)
    ax.text((start + end) / 2, y, label, ha='center', va='center',
            color='white', fontsize=8, fontweight='bold')
    ax.text(start - 0.1, y, f'M{start+1}', ha='right', va='center',
            color='#aaa', fontsize=7)

ax.set_xlabel('Months', color='white')
ax.set_title('Experimental Timeline', color='white', fontsize=10)
ax.set_xticks(range(0, 13, 2))
ax.set_xticklabels([f'M{m}' for m in range(0, 13, 2)], color='white', fontsize=8)
ax.set_yticks([])
ax.set_facecolor('#0a0a1a')
ax.tick_params(colors='white')

# Panel 6: Scaling roadmap
ax = fig.add_subplot(gs[3, :])
ax.set_xlim(0, 10)
ax.set_ylim(0, 3)

stages = [
    (1, 2.3, 'Stage 1\nSingle Circuit\n~fJ', '#00d4ff', '2026-27'),
    (3, 2.3, 'Stage 2\nCircuit Array\n~pJ (N²)', '#ffd93d', '2028-30'),
    (5, 2.3, 'Stage 3\nMetamaterial\n~nJ/cm³', '#6bff8d', '2030-35'),
    (7, 2.3, 'Stage 4\nTopological\n~μJ/cm³', '#b388ff', '2035-40'),
    (9, 2.3, 'Stage 5\nWarp Geometry\n~MJ → ???', '#ff6b6b', '2040+'),
]

for x, y, label, color, year in stages:
    circle = plt.Circle((x, y), 0.5, facecolor=color, alpha=0.6,
                         edgecolor='white', linewidth=2)
    ax.add_patch(circle)
    ax.text(x, y, label, ha='center', va='center', color='white',
            fontsize=7, fontweight='bold')
    ax.text(x, 1.5, year, ha='center', color='#aaa', fontsize=8)

# Arrows between stages
for i in range(len(stages) - 1):
    x1 = stages[i][0] + 0.55
    x2 = stages[i+1][0] - 0.55
    ax.annotate('', xy=(x2, 2.3), xytext=(x1, 2.3),
                arrowprops=dict(arrowstyle='->', color='white', lw=1.5))

ax.set_title('Scaling Roadmap: From Proof of Principle to Warp Drive',
             color='#ffd93d', fontsize=12, fontweight='bold', pad=10)
ax.text(5, 0.7, 'Each stage requires fundamental breakthroughs.\n'
        'Stage 1 is achievable with CURRENT technology.',
        ha='center', color='#aaa', fontsize=9, style='italic')
ax.axis('off')
ax.set_facecolor('#0a0a1a')

plt.savefig('research/04_warp_drive/exp_protocol_squid.png',
            dpi=150, bbox_inches='tight', facecolor='#0a0a1a')
plt.close()

print(f"\n  Plot saved: research/04_warp_drive/exp_protocol_squid.png")

# ============================================================================
#  SECTION 11: ONE-PAGE SUMMARY
# ============================================================================

print("\n" + "=" * 70)
print("  ONE-PAGE SUMMARY")
print("=" * 70)
print("""
  TITLE: Arithmetic Vacuum Energy Measurement via Superconducting
         Prime-Filtered Microwave Resonator

  HYPOTHESIS: The quantum vacuum energy of a cavity resonator has
  arithmetic structure described by the Euler product of ζ(s).
  Suppressing modes at multiples of prime p modifies the vacuum
  energy by the factor (1 - p^{-s}), as predicted by ζ-regularization.

  EXPERIMENT: A 10mm Nb coplanar waveguide resonator (f₀ ≈ 6 GHz)
  with SQUID-based notch filters that selectively suppress even
  harmonics. Compare vacuum energy with filters ON vs OFF.

  PREDICTION: Vacuum energy changes sign when even harmonics are
  suppressed. ΔE/E = -2 (sign flip from -1/12 to +1/12).

  SIGNIFICANCE: If confirmed, this proves that the Euler product
  formula ζ(s) = ∏_p (1-p^{-s})^{-1} is not just a mathematical
  identity but a PHYSICAL LAW governing vacuum fluctuations.

  This would open the door to "arithmetic vacuum engineering" —
  controlling the sign and magnitude of vacuum energy by selecting
  which prime channels are active — with ultimate implications
  for generating the exotic matter needed for warp drive.

  REQUIREMENTS: Dilution refrigerator lab with superconducting
  circuit fabrication capability. ~$50-100K, ~12 months.

  COLLABORATORS SOUGHT: Experimental quantum circuits groups
  with Casimir effect measurement experience.
""")

print("=" * 70)
print("  END OF PROTOCOL")
print("=" * 70)
