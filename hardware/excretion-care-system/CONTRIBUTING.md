# Contributing to OECS

Thank you for your interest in the Open Excretion Care System.

## How to Contribute

### Bug Reports & Feature Requests
Open an issue with a clear description and, if applicable, sensor data or logs.

### Code Contributions
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-improvement`)
3. Make your changes with clear commit messages
4. Add tests for new functionality
5. Submit a pull request

### Hardware Contributions
- 3D model improvements (STL/STEP + source files)
- PCB layout optimizations
- Alternative component suggestions with test results

### Documentation & Translation
We welcome translations of the README and docs into any language.

## Code Style

- **Python**: Follow PEP 8. Use type hints.
- **C (firmware)**: Follow Linux kernel coding style. Use `snake_case`.
- **Commit messages**: Start with a verb (Add, Fix, Update, Remove).

## Safety-Critical Code

Changes to actuator control, safety limits, or sensor thresholds require:
1. Clear rationale in the PR description
2. Test evidence (simulation or hardware)
3. Review by at least one maintainer

## License

By contributing, you agree that your contributions will be licensed under the same
license as the project (CERN-OHL-S-2.0 for hardware, GPLv3 for software).
