"""
Unit tests for D-S Evidence Theory implementation.
"""

import sys
import os
import pytest
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'algorithm', 'python'))
from ds_evidence import (
    MassFunction, SensorReading, State,
    temperature_to_bpa, humidity_to_bpa, nh3_to_bpa,
    ds_combine, ds_combine_multiple, classify, determine_action,
)


class TestMassFunction:
    def test_valid_bpa(self):
        m = MassFunction(normal=0.7, urine=0.1, feces=0.1, uncertainty=0.1)
        assert np.isclose(m.normal + m.urine + m.feces + m.uncertainty, 1.0)

    def test_invalid_bpa_raises(self):
        with pytest.raises(ValueError):
            MassFunction(normal=0.5, urine=0.5, feces=0.5, uncertainty=0.5)

    def test_default_is_full_uncertainty(self):
        m = MassFunction()
        assert m.uncertainty == 1.0
        assert m.normal == 0.0


class TestSensorToBPA:
    def test_normal_temperature(self):
        m = temperature_to_bpa(33.0)
        assert m.normal > 0.5

    def test_elevated_temperature(self):
        m = temperature_to_bpa(36.0)
        assert m.urine > m.normal

    def test_normal_humidity(self):
        m = humidity_to_bpa(50.0)
        assert m.normal > 0.5

    def test_high_humidity(self):
        m = humidity_to_bpa(90.0)
        assert m.urine > m.normal

    def test_low_nh3(self):
        m = nh3_to_bpa(2.0)
        assert m.normal > 0.5

    def test_high_nh3(self):
        m = nh3_to_bpa(40.0)
        assert m.feces > m.urine


class TestDSCombine:
    def test_combine_agreeing_sources(self):
        m1 = MassFunction(normal=0.8, urine=0.1, feces=0.0, uncertainty=0.1)
        m2 = MassFunction(normal=0.7, urine=0.1, feces=0.1, uncertainty=0.1)
        result = ds_combine(m1, m2)
        assert result.normal > 0.8  # Agreement strengthens belief

    def test_combine_conflicting_sources(self):
        m1 = MassFunction(normal=0.8, urine=0.1, feces=0.0, uncertainty=0.1)
        m2 = MassFunction(normal=0.0, urine=0.8, feces=0.1, uncertainty=0.1)
        result = ds_combine(m1, m2)
        # Conflict is normalized away; both beliefs reduced
        assert result.normal + result.urine + result.feces + result.uncertainty == pytest.approx(1.0, abs=0.01)

    def test_combine_preserves_sum(self):
        m1 = MassFunction(normal=0.3, urine=0.3, feces=0.2, uncertainty=0.2)
        m2 = MassFunction(normal=0.4, urine=0.2, feces=0.2, uncertainty=0.2)
        result = ds_combine(m1, m2)
        total = result.normal + result.urine + result.feces + result.uncertainty
        assert total == pytest.approx(1.0, abs=0.01)

    def test_combine_multiple(self):
        m1 = MassFunction(normal=0.1, urine=0.6, feces=0.1, uncertainty=0.2)
        m2 = MassFunction(normal=0.1, urine=0.5, feces=0.1, uncertainty=0.3)
        m3 = MassFunction(normal=0.1, urine=0.4, feces=0.2, uncertainty=0.3)
        result = ds_combine_multiple(m1, m2, m3)
        assert result.urine > result.normal
        assert result.urine > result.feces


class TestClassify:
    def test_normal_reading(self):
        reading = SensorReading(temperature=33.0, humidity=50.0, nh3_ppm=2.0)
        state, _ = classify(reading)
        assert state == State.NORMAL

    def test_urine_reading(self):
        reading = SensorReading(temperature=36.0, humidity=88.0, nh3_ppm=18.0)
        state, _ = classify(reading)
        assert state == State.URINE

    def test_feces_reading(self):
        reading = SensorReading(temperature=35.0, humidity=82.0, nh3_ppm=42.0)
        state, _ = classify(reading)
        assert state == State.FECES

    def test_ambiguous_defaults_to_normal(self):
        reading = SensorReading(temperature=33.5, humidity=55.0, nh3_ppm=3.0)
        state, _ = classify(reading)
        assert state == State.NORMAL


class TestActions:
    def test_normal_no_action(self):
        action = determine_action(State.NORMAL)
        assert not action["suction_pump"]
        assert not action["water_pump"]

    def test_urine_triggers_all(self):
        action = determine_action(State.URINE)
        assert action["suction_pump"]
        assert action["water_pump"]
        assert action["heater"]
        assert action["fan"]

    def test_feces_triggers_all(self):
        action = determine_action(State.FECES)
        assert action["suction_pump"]
        assert action["water_pump"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
