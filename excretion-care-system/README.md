# Open Excretion Care System (OECS)

An open-source automated excretion detection and cleaning system for nursing care,
based on the design principles described in Hu & Chen et al. (Healthcare 2023, 11(3), 388).

## Overview

This project aims to make automated excretion care technology accessible worldwide
by providing open-source hardware designs, firmware, and detection algorithms that
can be built with affordable, off-the-shelf components.

```
+------------------+     +-------------------+     +------------------+
|  Sensor Layer    | --> |  Detection Logic  | --> |  Actuator Layer  |
|  - Temp/Humidity |     |  - D-S Evidence   |     |  - Suction Pump  |
|  - NH3 Gas       |     |  - 1D-CNN (opt.)  |     |  - Warm Water    |
|  - (extensible)  |     |  - Threshold FB   |     |  - Heater + Fan  |
+------------------+     +-------------------+     +------------------+
        |                        |                         |
        +------------------------+-------------------------+
                                 |
                        STM32F103 MCU
```

## Project Structure

```
excretion-care-system/
├── firmware/           # STM32 HAL-based firmware (C)
│   ├── Core/Inc/       # Header files
│   ├── Core/Src/       # Source files
│   ├── Drivers/        # HAL driver configs
│   └── Middlewares/    # Communication protocols
├── algorithm/          # Detection algorithms
│   ├── python/         # Python reference implementation
│   └── c/              # Embedded C implementation
├── ai/                 # Deep learning extension
│   ├── models/         # Model definitions (1D-CNN)
│   ├── training/       # Training scripts
│   └── data/           # Sample/synthetic datasets
├── hardware/           # Physical design files
│   ├── 3d-models/      # STL/STEP files (TPU receiver, housing)
│   ├── schematics/     # KiCad circuit schematics
│   └── bom/            # Bill of Materials
├── docs/               # Documentation
├── tests/              # Test suites
└── .github/            # CI/CD and templates
```

## Key Features

- **Multi-sensor fusion** using Dempster-Shafer evidence theory (~90% accuracy)
- **Urine vs. feces discrimination** via combined temperature, humidity, and gas analysis
- **Automatic cleaning cycle**: suction -> warm water wash -> hot air dry
- **Modular design**: 3D-printable receiver with TPU flex material
- **AI-ready**: optional 1D-CNN upgrade path for predictive detection

## Hardware Requirements

| Component | Recommended | Alternative | Est. Cost |
|-----------|-------------|-------------|-----------|
| MCU | STM32F103C8T6 (Blue Pill) | STM32F401 | $2-5 |
| Temp/Humidity Sensor | SHT30 (I2C) | DHT22 | $2-8 |
| Gas Sensor | MQ-135 (NH3) | MiCS-6814 | $3-10 |
| Suction Pump | 12V DC diaphragm pump | - | $10-20 |
| Water Pump | 12V peristaltic pump | - | $8-15 |
| Heater | PTC ceramic heater 12V | Nichrome wire | $5-10 |
| Fan | 5015 blower fan 12V | 4010 axial | $3-5 |
| Power Supply | 12V 5A switching PSU | - | $8-12 |
| Motor Driver | L298N or BTS7960 | DRV8871 | $3-8 |

**Estimated total BOM: $45-95 USD**

## Quick Start

### 1. Algorithm Simulation (Python)

```bash
cd algorithm/python
pip install -r requirements.txt
python ds_evidence.py --demo
```

### 2. Firmware Build (STM32)

```bash
# Using STM32CubeIDE or arm-none-eabi-gcc
cd firmware
make
```

### 3. AI Model Training (Optional)

```bash
cd ai/training
pip install -r requirements.txt
python train_1dcnn.py --config config.yaml
```

## Detection Algorithm

The core detection uses Dempster-Shafer (D-S) evidence theory to fuse multiple
sensor readings into a probabilistic classification:

| State | Temperature | Humidity | NH3 Level |
|-------|-------------|----------|-----------|
| Normal | ~33°C | 40-60% | < 5 ppm |
| Urine | +2-4°C spike | > 80% | 10-25 ppm |
| Feces | +1-3°C spike | > 75% | > 30 ppm |

The D-S fusion achieves ~90% detection accuracy compared to ~70% for simple
threshold-based approaches.

## Safety Considerations

- **Skin contact materials**: Use medical-grade TPU (Shore 40A-60A) for receiver
- **Water temperature**: Hardware-limited to max 38°C with thermal fuse backup
- **Suction pressure**: Relief valve limits negative pressure to -20 kPa
- **Electrical isolation**: 12V system with optocoupler isolation from patient contact

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. We especially welcome:
- Translations of documentation
- Clinical validation data
- Alternative sensor integration
- 3D model improvements for different body types

## License

This project is licensed under the CERN Open Hardware Licence v2 - Strongly Reciprocal
(CERN-OHL-S-2.0) for hardware designs, and GPLv3 for software components.

## References

- Hu, B.; Chen, Z.; et al. "Research of System Design and Automatic Detection Method
  for Excretion Nursing Equipment." *Healthcare* 2023, 11(3), 388.
  https://doi.org/10.3390/healthcare11030388
- Dempster, A.P. "A Generalization of Bayesian Inference." *Journal of the Royal
  Statistical Society*, Series B, 1968.
- Shafer, G. *A Mathematical Theory of Evidence*. Princeton University Press, 1976.

## Acknowledgments

This project is inspired by commercial products like the Liberty Himawari (Japan)
and aims to democratize access to automated excretion care technology globally.
