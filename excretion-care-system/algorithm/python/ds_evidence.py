"""
Dempster-Shafer Evidence Theory for Excretion Detection
========================================================

Multi-sensor fusion algorithm that combines temperature, humidity, and NH3 gas
sensor data to classify excretion events as: Normal, Urine, or Feces.

Based on: Hu & Chen et al., Healthcare 2023, 11(3), 388

Usage:
    python ds_evidence.py --demo
    python ds_evidence.py --temp 35.2 --humidity 85.0 --nh3 18.0
"""

import argparse
import numpy as np
from dataclasses import dataclass
from enum import Enum
from typing import Dict, Tuple


class State(Enum):
    NORMAL = "normal"
    URINE = "urine"
    FECES = "feces"


@dataclass
class SensorReading:
    temperature: float    # Celsius (skin-surface temperature in diaper)
    humidity: float       # Relative humidity %
    nh3_ppm: float        # Ammonia concentration in ppm


@dataclass
class MassFunction:
    """Basic Probability Assignment (BPA) for D-S evidence theory."""
    normal: float = 0.0
    urine: float = 0.0
    feces: float = 0.0
    uncertainty: float = 1.0  # Theta (frame of discernment)

    def __post_init__(self):
        total = self.normal + self.urine + self.feces + self.uncertainty
        if not np.isclose(total, 1.0, atol=1e-6):
            raise ValueError(f"BPA must sum to 1.0, got {total}")

    def as_dict(self) -> Dict[str, float]:
        return {
            "normal": self.normal,
            "urine": self.urine,
            "feces": self.feces,
            "uncertainty": self.uncertainty,
        }


# --- Sensor-to-BPA Mapping Functions ---

def temperature_to_bpa(temp: float, baseline: float = 33.0) -> MassFunction:
    """
    Convert temperature reading to Basic Probability Assignment.

    Normal skin temp in diaper area: ~33°C
    Urine event: +2-4°C sudden spike
    Feces event: +1-3°C spike (slightly lower due to different thermal mass)
    """
    delta = temp - baseline

    if delta < 0.5:
        return MassFunction(normal=0.7, urine=0.05, feces=0.05, uncertainty=0.2)
    elif delta < 2.0:
        return MassFunction(normal=0.3, urine=0.2, feces=0.2, uncertainty=0.3)
    elif delta < 4.0:
        # Moderate spike - more likely urine
        return MassFunction(normal=0.05, urine=0.5, feces=0.2, uncertainty=0.25)
    else:
        # Large spike
        return MassFunction(normal=0.02, urine=0.55, feces=0.25, uncertainty=0.18)


def humidity_to_bpa(humidity: float) -> MassFunction:
    """
    Convert humidity reading to Basic Probability Assignment.

    Normal: 40-60% RH
    Urine: rapid rise to >80%
    Feces: rise to >75% (slightly less moisture than urine)
    """
    if humidity < 60:
        return MassFunction(normal=0.75, urine=0.05, feces=0.05, uncertainty=0.15)
    elif humidity < 75:
        return MassFunction(normal=0.3, urine=0.25, feces=0.15, uncertainty=0.3)
    elif humidity < 85:
        return MassFunction(normal=0.05, urine=0.45, feces=0.25, uncertainty=0.25)
    else:
        return MassFunction(normal=0.02, urine=0.6, feces=0.2, uncertainty=0.18)


def nh3_to_bpa(nh3_ppm: float) -> MassFunction:
    """
    Convert NH3 gas sensor reading to Basic Probability Assignment.

    Normal: < 5 ppm
    Urine: 10-25 ppm (urea decomposition)
    Feces: > 30 ppm (stronger ammonia + other gases)
    """
    if nh3_ppm < 5:
        return MassFunction(normal=0.8, urine=0.05, feces=0.02, uncertainty=0.13)
    elif nh3_ppm < 15:
        return MassFunction(normal=0.1, urine=0.5, feces=0.15, uncertainty=0.25)
    elif nh3_ppm < 30:
        return MassFunction(normal=0.03, urine=0.5, feces=0.25, uncertainty=0.22)
    else:
        # High NH3 strongly suggests feces
        return MassFunction(normal=0.02, urine=0.1, feces=0.7, uncertainty=0.18)


# --- Dempster-Shafer Combination ---

def ds_combine(m1: MassFunction, m2: MassFunction) -> MassFunction:
    """
    Combine two mass functions using Dempster's rule of combination.

    The combination accounts for conflict between sources and redistributes
    conflicting mass to maintain a valid probability assignment.

    Formula:
        m(A) = (1 / (1-K)) * sum_{B ∩ C = A} m1(B) * m2(C)
        where K = sum_{B ∩ C = ∅} m1(B) * m2(C)  (conflict factor)
    """
    focal_elements = ["normal", "urine", "feces"]

    d1 = m1.as_dict()
    d2 = m2.as_dict()

    # Calculate all pairwise intersections
    combined = {key: 0.0 for key in focal_elements}
    conflict = 0.0

    for key1, val1 in d1.items():
        for key2, val2 in d2.items():
            product = val1 * val2

            if key1 == "uncertainty" and key2 == "uncertainty":
                # Theta ∩ Theta = Theta (contributes to all as uncertainty)
                pass
            elif key1 == "uncertainty":
                # Theta ∩ X = X
                combined[key2] = combined.get(key2, 0) + product
            elif key2 == "uncertainty":
                # X ∩ Theta = X
                combined[key1] = combined.get(key1, 0) + product
            elif key1 == key2:
                # X ∩ X = X
                combined[key1] += product
            else:
                # X ∩ Y = ∅ (conflict)
                conflict += product

    # Uncertainty from Theta ∩ Theta
    uncertainty_product = d1["uncertainty"] * d2["uncertainty"]

    if conflict >= 1.0:
        raise ValueError("Total conflict: evidence sources are completely contradictory")

    # Normalize by (1 - K) to redistribute conflict mass
    normalization = 1.0 - conflict

    result = {}
    for key in focal_elements:
        result[key] = combined[key] / normalization

    result_uncertainty = uncertainty_product / normalization

    return MassFunction(
        normal=result["normal"],
        urine=result["urine"],
        feces=result["feces"],
        uncertainty=result_uncertainty,
    )


def ds_combine_multiple(*mass_functions: MassFunction) -> MassFunction:
    """Combine multiple mass functions sequentially."""
    if len(mass_functions) < 2:
        raise ValueError("Need at least 2 mass functions to combine")

    result = mass_functions[0]
    for mf in mass_functions[1:]:
        result = ds_combine(result, mf)
    return result


# --- Decision Logic ---

def classify(reading: SensorReading, threshold: float = 0.4) -> Tuple[State, MassFunction]:
    """
    Classify a sensor reading using D-S evidence fusion.

    Args:
        reading: Combined sensor data
        threshold: Minimum belief required for positive classification

    Returns:
        Tuple of (classified state, final mass function)
    """
    m_temp = temperature_to_bpa(reading.temperature)
    m_hum = humidity_to_bpa(reading.humidity)
    m_nh3 = nh3_to_bpa(reading.nh3_ppm)

    fused = ds_combine_multiple(m_temp, m_hum, m_nh3)

    # Decision: pick highest belief above threshold
    beliefs = {
        State.NORMAL: fused.normal,
        State.URINE: fused.urine,
        State.FECES: fused.feces,
    }

    best_state = max(beliefs, key=beliefs.get)
    best_belief = beliefs[best_state]

    if best_belief < threshold:
        return State.NORMAL, fused  # Default to normal if uncertain

    return best_state, fused


# --- Control Actions ---

def determine_action(state: State) -> dict:
    """Map detected state to actuator commands."""
    actions = {
        State.NORMAL: {
            "suction_pump": False,
            "water_pump": False,
            "heater": False,
            "fan": False,
            "description": "No action - normal state",
        },
        State.URINE: {
            "suction_pump": True,
            "water_pump": True,
            "heater": True,
            "fan": True,
            "description": "Urine detected: suction -> rinse -> dry",
        },
        State.FECES: {
            "suction_pump": True,
            "water_pump": True,
            "heater": True,
            "fan": True,
            "description": "Feces detected: extended suction -> thorough rinse -> dry",
        },
    }
    return actions[state]


# --- Demo & CLI ---

def run_demo():
    """Run demonstration with sample sensor readings."""
    print("=" * 65)
    print("  Dempster-Shafer Excretion Detection - Demo")
    print("=" * 65)

    test_cases = [
        ("Normal (resting)",        SensorReading(33.1, 50.0, 2.0)),
        ("Slight moisture",         SensorReading(33.5, 65.0, 3.0)),
        ("Urine event",             SensorReading(35.8, 88.0, 18.0)),
        ("Feces event",             SensorReading(35.0, 82.0, 42.0)),
        ("Ambiguous (sweat?)",      SensorReading(34.0, 72.0, 4.0)),
        ("Strong urine",            SensorReading(36.5, 92.0, 22.0)),
    ]

    for name, reading in test_cases:
        state, fused = classify(reading)
        action = determine_action(state)

        print(f"\n--- {name} ---")
        print(f"  Input:  T={reading.temperature}°C  RH={reading.humidity}%  NH3={reading.nh3_ppm}ppm")
        print(f"  Belief: Normal={fused.normal:.3f}  Urine={fused.urine:.3f}  "
              f"Feces={fused.feces:.3f}  Uncertain={fused.uncertainty:.3f}")
        print(f"  Result: {state.value.upper()}")
        print(f"  Action: {action['description']}")

    print("\n" + "=" * 65)


def main():
    parser = argparse.ArgumentParser(
        description="D-S Evidence Theory Excretion Detection"
    )
    parser.add_argument("--demo", action="store_true", help="Run demo with sample data")
    parser.add_argument("--temp", type=float, help="Temperature (°C)")
    parser.add_argument("--humidity", type=float, help="Relative humidity (%%)")
    parser.add_argument("--nh3", type=float, help="NH3 concentration (ppm)")
    parser.add_argument("--threshold", type=float, default=0.4,
                        help="Classification threshold (default: 0.4)")

    args = parser.parse_args()

    if args.demo:
        run_demo()
    elif args.temp is not None and args.humidity is not None and args.nh3 is not None:
        reading = SensorReading(args.temp, args.humidity, args.nh3)
        state, fused = classify(reading, threshold=args.threshold)
        action = determine_action(state)

        print(f"Input:  T={reading.temperature}°C  RH={reading.humidity}%  NH3={reading.nh3_ppm}ppm")
        print(f"Belief: N={fused.normal:.3f}  U={fused.urine:.3f}  "
              f"F={fused.feces:.3f}  Unc={fused.uncertainty:.3f}")
        print(f"Result: {state.value.upper()}")
        print(f"Action: {action['description']}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
