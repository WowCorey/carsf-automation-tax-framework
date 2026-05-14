from __future__ import annotations

import math

import pytest

from carsf.reemployment import evaluate_reemployment_path


SEVERITY = {"low": 0, "medium": 1, "high": 2, "critical": 3, "not_assessable": -1}


def _household(**overrides):
    data = {
        "household_id": "hh_test",
        "household_type": "single_adult",
        "adults": 1,
        "children": 0,
        "region_type": "placeholder_region",
        "income_band": "middle_placeholder",
        "pre_displacement_income": 70000,
        "post_displacement_income": 20000,
        "existing_support_baseline": 5000,
        "housing_cost_placeholder": 20000,
        "essential_cost_placeholder": 18000,
        "debt_pressure_placeholder": 2000,
        "savings_buffer_placeholder": 3000,
        "illustrative_placeholder_only": True,
        "synthetic_household_only": True,
    }
    data.update(overrides)
    return data


def _path(**overrides):
    data = {
        "path_id": "reemployment_test",
        "household_id": "hh_test",
        "displacement_year": 2028,
        "expected_reemployment_months": 3,
        "retraining_months": 3,
        "partial_income_recovery_rate": 0.5,
        "full_income_recovery_rate": 1.0,
        "probability_band_placeholder": "medium",
        "illustrative_placeholder_only": True,
    }
    data.update(overrides)
    return data


@pytest.mark.parametrize("field,value", [("expected_reemployment_months", -1), ("retraining_months", 1.5), ("displacement_year", math.inf)])
def test_reemployment_rejects_invalid_months_and_years(field, value) -> None:
    with pytest.raises(ValueError):
        evaluate_reemployment_path(_path(**{field: value}), _household())


@pytest.mark.parametrize("field,value", [("partial_income_recovery_rate", -0.1), ("full_income_recovery_rate", 1.1)])
def test_reemployment_rejects_invalid_rates(field, value) -> None:
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        evaluate_reemployment_path(_path(**{field: value}), _household())


def test_long_or_unknown_reemployment_is_riskier_than_quick_recovery() -> None:
    quick = evaluate_reemployment_path(_path(expected_reemployment_months=2, retraining_months=2, full_income_recovery_rate=1.0), _household())
    long = evaluate_reemployment_path(_path(expected_reemployment_months=24, retraining_months=12, full_income_recovery_rate=0.4), _household())
    unknown = evaluate_reemployment_path(_path(expected_reemployment_months=None, retraining_months=None, full_income_recovery_rate=0.3), _household())

    assert SEVERITY[long.reemployment_risk_band] > SEVERITY[quick.reemployment_risk_band]
    assert unknown.reemployment_risk_band == "critical"
