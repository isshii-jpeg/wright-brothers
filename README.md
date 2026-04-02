# Wright Brothers

Research papers, simulations, and experimental plans toward next-generation propulsion and fundamental physics.

## Repository Structure

```
wright-brothers/
├── papers/
│   ├── ehd-propulsion/          # EHD (Electrohydrodynamic) propulsion
│   │   ├── fpga_ghz_feedback_control.pdf   # FPGA GHz feedback control for B-B effect
│   │   ├── paper.tex / paper.pdf           # EHD theory (English)
│   │   ├── paper_japanese.tex / .pdf       # EHD theory (Japanese)
│   │   ├── experiment_plan.tex / .pdf      # Hands-on experiment guide
│   │   └── simulation_plan.tex / .pdf      # Computational simulation plan
│   │
│   ├── plasma-simulator/        # Autonomous multi-scale plasma simulator
│   │   ├── plasma_simulator_proposal.md    # Design proposal v1.0
│   │   └── plasma_simulator_proposal_v2.md # v2.0: Technical challenges & breakthroughs
│   │
│   ├── flying-car/              # EHD flying car roadmap
│   │   └── flying_car_roadmap.tex / .pdf   # 6-phase roadmap with Go/No-Go gates
│   │
│   ├── arithmetic-geometry/     # Arithmetic geometry & spacetime
│   │   ├── arithmetic_geometry_spacetime.tex / .pdf      # Japanese
│   │   └── arithmetic_geometry_spacetime_en.tex / .pdf   # English
│   │
│   └── econoneurodynamics/      # Econo-neurodynamics
│       └── econoneurodynamics.tex / .pdf
│
├── fiction/
│   └── homological-mystery/     # Mathematical mystery fiction
│       ├── homological_mystery.tex / .pdf      # Episode I
│       ├── homological_mystery_II.tex / .pdf   # Episode II
│       ├── murder_over_rings.md                # Episode III draft
│       └── mystery_series_plan.md              # Series plan
│
├── hardware/
│   └── excretion-care-system/   # IoT excretion care system
│       ├── firmware/            # STM32 firmware
│       ├── ai/                  # CNN inference models
│       ├── algorithm/           # Dempster-Shafer evidence fusion
│       └── docs/                # Build guide & architecture
│
├── guides/
│   └── akihabara_build_guide.md # PC build guide for plasma simulation
│
└── README.md
```

## Key Papers

### EHD Propulsion & FPGA Control
Dynamic entropy suppression in EHD propulsion via FPGA-based GHz-rate feedback control, interpreted as a thermodynamically consistent Maxwell's demon. Derives the scaling law Re_max proportional to Pi_ctrl^{2/3}.

### Plasma Simulator (v1.0 & v2.0)
Design proposal for an autonomous, multi-scale, multi-physics plasma simulator combining Adaptive Micro-Macro Coupling (AMMC), Physics-Informed Neural Operators (PINO), and an AI-driven auto-research feedback loop. v2.0 addresses JAX migration, symplectic neural network corrections, and the static-shape vs dynamic-mesh tension.

### Flying Car Roadmap
A 6-phase roadmap from simulation (Phase 0, ~200K JPY) to a flying car (Phase 5, ~100M+ JPY) using micro-electrode arrays with 1mm gaps and FPGA GHz control. Each phase has quantitative Go/No-Go gates.

### Arithmetic Geometry as the Source Code of Spacetime
Explores how topos theory, IUT theory, and noncommutative geometry may provide the "next-generation language" for quantum gravity. 72 references spanning Grothendieck, Mochizuki, Connes, and modern mathematical physics.

## Author

**Wright Brothers** (bsbraveshine777@gmail.com)

## License

All rights reserved unless otherwise noted.
