from __future__ import annotations

import math

import pytest

from carsf.investment import evaluate_investment_guardrail


def base_inputs() -> dict:
    return {
        "example_id": "test",
        "aava": 1000.0,
        "final_liability": 100.0,
        "capital_base": 2000.0,
        "uplift_rate": 0.10,
        "revenue": 5000.0,
        "normal_return_proxy": 100.0,
        "sector": "placeholder",
        "placeholder_basis": ["illustrative placeholder"],
    }


def test_investment_guardrail_rejects_nan_and_infinity() -> None:
    for value in [math.nan, math.inf, -math.inf]:
        inputs = base_inputs()
        inputs["aava"] = value
        with pytest.raises(ValueError, match="aava must be finite"):
            evaluate_investment_guardrail(inputs)


def test_investment_guardrail_rejects_negative_liability() -> None:
    inputs = base_inputs()
    inputs["final_liability"] = -1

    with pytest.raises(ValueError, match="final_liability cannot be negative"):
        evaluate_investment_guardrail(inputs)


def test_investment_guardrail_rejects_negative_revenue() -> None:
    inputs = base_inputs()
    inputs["revenue"] = -1

    with pytest.raises(ValueError, match="revenue cannot be negative"):
        evaluate_investment_guardrail(inputs)


def test_aava_zero_with_positive_liability_triggers_critical_review() -> None:
    inputs = base_inputs()
    inputs["aava"] = 0.0
    inputs["final_liability"] = 50.0

    result = evaluate_investment_guardrail(inputs)

    assert result.investment_risk_band == "critical"
    assert result.over_capture_warning is True
    assert result.effective_burden_rate is None


def test_effective_burden_is_liability_divided_by_aava() -> None:
    result = evaluate_investment_guardrail(base_inputs())

    assert result.effective_burden_rate == pytest.approx(0.10)
    assert result.liability_to_aava_rate == pytest.approx(0.10)
    assert result.liability_to_revenue_rate == pytest.approx(0.02)
