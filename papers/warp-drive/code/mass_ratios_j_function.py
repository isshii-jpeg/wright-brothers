#!/usr/bin/env python3
"""
Mass ratios from j-function CM values.
THE MOST PRECISE PREDICTION: m_p/m_e = 12 × 153 = 1836 (0.008% match!)
"""
import numpy as np
pi = np.pi

r4 = 12   # j(i)^{1/3}
r7 = 15   # |j(-7)|^{1/3}
cd = 3    # cd(Spec(Z))

# m_p/m_e = r_{-4} × (r_{-4}² + cd²)
pred = r4 * (r4**2 + cd**2)  # = 12 × 153 = 1836
obs = 1836.15267343
print(f"m_p/m_e = {r4} × ({r4**2} + {cd**2}) = {r4} × {r4**2+cd**2} = {pred}")
print(f"Observed: {obs:.5f}, Error: {abs(pred-obs)/obs*100:.4f}%")
print()

# Five predictions
preds = [
    ("Omega_L",  "2pi/9",       2*pi/9,      0.6847,     "Planck"),
    ("alpha_EM", "4pi/1728",     4*pi/1728,   1/137.036,  "CODATA"),
    ("sin2tW",   "375/(512pi)",  375/(512*pi), 0.2312,    "PDG"),
    ("m_p/m_e",  "12*153",       1836.0,      1836.153,   "CODATA"),
    ("m_mu/m_e", "9*23",         207.0,       206.768,    "CODATA"),
]
for n, f, p, o, s in preds:
    e = abs(p-o)/o*100
    print(f"  {n:>10} = {f:>12} = {p:.4f} (obs: {o:.4f}, err: {e:.4f}%, {s})")
