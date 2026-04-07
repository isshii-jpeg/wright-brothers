#!/usr/bin/env python3
"""Structural derivation: why 4π, why cubed, why π in couplings.
4π = Vol(S²) from Gauss law in d=4 spacetime.
³ = cd = cohomological dimension (volume forms on 3-manifold).
π in couplings = archimedean Γ-factor in completed ζ.
No π in masses = non-archimedean norms only."""
import numpy as np; pi=np.pi
print("α_EM = Vol(S^{d-2}) / r^{cd} = 4π / 12³ =", 4*pi/1728, "= 1/", 1/(4*pi/1728))
print("Structural: boundary(4π) / bulk(1728) = geometric / arithmetic")
