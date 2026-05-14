from __future__ import annotations

import pytest

from carsf.regional_stress import evaluate_regional_stress


SEVERITY = {"low": 0, "medium": 1, "high": 2, "critical": 3}


def _region(**overrides):
    data = {
        "region_id": "region_test",
        "region_type": "placeholder_region",
        "automation_exposure_placeholder": 0.5,
        "labour_market_depth_placeholder": 0.5,
        "retraining_access_placeholder": 0.5,
        "housing_cost_pressure_placeholder": 0.5,
        "transport_access_placeholder": 0.5,
        "illustrative_placeholder_only": True,
    }
    data.update(overrides)
    return data


@pytest.mark.parametrize("field,value", [("automation_exposure_placeholder", -0.1), ("labour_market_depth_placeholder", 1.1)])
def test_regional_stress_rejects_scores_outside_bounds(field, value) -> None:
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        evaluate_regional_stress(_region(**{field: value}))


def test_regional_stress_rises_with_high_exposure_and_low_labour_market_depth() -> None:
    low = evaluate_regional_stress(
        _region(
            automation_exposure_placeholder=0.1,
            labour_market_depth_placeholder=0.9,
            retraining_access_placeholder=0.9,
            housing_cost_pressure_placeholder=0.1,
            transport_access_placeholder=0.9,
        )
    )
    high = evaluate_regional_stress(
        _region(
            automation_exposure_placeholder=0.9,
            labour_market_depth_placeholder=0.1,
            retraining_access_placeholder=0.2,
            housing_cost_pressure_placeholder=0.9,
            transport_access_placeholder=0.2,
        )
    )

    assert high.regional_stress_score > low.regional_stress_score
    assert SEVERITY[high.regional_stress_band] > SEVERITY[low.regional_stress_band]
    assert "high automation exposure" in high.drivers
