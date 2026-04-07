#!/usr/bin/env python3
"""ALL five constants from d=4 and cd=3 alone."""
import numpy as np; pi=np.pi; d=4; cd=3
r4=d*cd; r7=cd*(d+1)
print(f"j(i)=(d*cd)^3={r4**3}, |j(-7)|=(cd*(d+1))^3={r7**3}")
print(f"OmL=2pi/cd^2={2*pi/cd**2:.4f} (2.0%)")
print(f"aEM=4pi/(d*cd)^3={4*pi/r4**3:.6f} (0.3%)")
print(f"sin2tW=(cd/(8pi))((d+1)/d)^3={cd/(8*pi)*(r7/r4)**3:.4f} (0.8%)")
print(f"mp/me=d*cd^3*(d^2+1)={d*cd**3*(d**2+1)} (0.008%)")
