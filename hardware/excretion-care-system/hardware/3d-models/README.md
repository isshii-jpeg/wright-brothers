# 3D Printable Components

## Receiver (Body-Contact Component)

The receiver is the component that contacts the patient's skin and collects excretions.

### Design Requirements

- **Material**: TPU (Shore 60A) for flexibility and skin comfort
- **Seal**: Lip seal design for leak prevention without excessive pressure
- **Ports**: 
  - Suction inlet (6mm barb fitting)
  - Water inlet (6mm barb fitting)
  - Sensor mounting pocket (SHT30 + MQ-135)
- **Sizes**: Parametric design for S/M/L body types

### Print Settings (TPU)

| Parameter | Value |
|-----------|-------|
| Layer height | 0.2mm |
| Infill | 20% gyroid |
| Walls | 3 |
| Print speed | 25mm/s |
| Retraction | Direct drive recommended |
| Bed temp | 50°C |
| Nozzle temp | 220-230°C |
| Support | Tree supports, easy-release |

## Controller Housing

Houses the STM32 board, motor drivers, and power supply.

### Design Requirements

- **Material**: PLA or PETG
- **Ventilation**: Slots for heater/fan airflow
- **Access**: Removable lid for maintenance
- **Mounting**: Wall-mount bracket or bedside clip

### Print Settings (PLA)

| Parameter | Value |
|-----------|-------|
| Layer height | 0.2mm |
| Infill | 30% cubic |
| Walls | 3 |
| Print speed | 60mm/s |

## Files

STL and STEP files to be added:
- `receiver_medium.stl` - Medium size receiver
- `receiver_medium.step` - Editable STEP format
- `housing_main.stl` - Controller housing body
- `housing_lid.stl` - Controller housing lid
- `housing_bracket.stl` - Wall/bed mount bracket

Parametric source files (FreeCAD/OpenSCAD) will be provided for customization.
