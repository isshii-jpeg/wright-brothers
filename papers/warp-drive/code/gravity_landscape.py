#!/usr/bin/env python3
"""Gravity rewriting landscape: G_eff = G cos(φ), 6 types, material palette."""
# G_eff(φ) = G × cos(φ). φ = Berry phase.
# φ=0: G, φ=π/3: G/2 (FQHE), φ=π/2: 0, φ=π: -G (TI/π-junction)
# Types: discrete, continuous, spatial, temporal, spectral, Euler product
import numpy as np; pi=np.pi
for deg in range(0, 181, 30):
    print(f"φ={deg:>3}°: G_eff/G = {np.cos(deg*pi/180):>6.3f}")
