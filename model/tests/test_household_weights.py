from __future__ import annotations

import math

import pytest

from carsf.household_weights import evaluate_household_weight


def _weight(**overrides):
    payload = {
        "scenario_id": "single_parent_retraining_gap",
        "subgroup_id": "low_income",
        "weight_value": 1.0,
        "weight_basis": "synthetic placeholder stress weight",
        "calibrated": False,
        "calibration_source": None,
        "illustrative_placeholder_only": True,
        "synthetic_weight_only": True,
        "placeholder_basis": ["unit test synthetic placeholder"],
    }
    payload.update(overrides)
    return payload


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_household_weight_rejects_non_finite_values(value) -> None:
    with pytest.raises(ValueError, match="weight_value must be finite"):
        evaluate_household_weight(_weight(weight_value=value))


def test_household_weight_rejects_negative_values() -> None:
    with pytest.raises(ValueError, match="weight_value cannot be negative"):
        evaluate_household_weight(_weight(weight_value=-0.01))


def test_uncalibrated_weight_cannot_be_used_for_real_world_claims() -> None:
    result = evaluate_household_weight(_weight(calibrated=False))

    assert result.usable_for_real_world_claims is False
    assert result.calibrated is False
    assert "not population representative" in " ".join(result.warnings)


def test_calibrated_metadata_still_does_not_validate_prototype_weight() -> None:
    result = evaluate_household_weight(
        _weight(calibrated=True, calibration_source="external_not_in_repo placeholder category")
    )

    assert result.calibrated is True
    assert result.usable_for_real_world_claims is False
    assert any("does not create validation" in warning for warning in result.warnings)


def test_household_weight_rejects_real_source_like_calibration_source() -> None:
    with pytest.raises(ValueError, match="must not embed a real data source"):
        evaluate_household_weight(_weight(calibration_source="ABS household microdata extract"))
