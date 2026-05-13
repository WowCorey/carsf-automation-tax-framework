from __future__ import annotations

import math

import pytest

from carsf.transition_payments import evaluate_transition_payment


def _design() -> dict:
    return {
        "design_id": "test_supplement",
        "design_type": "DISPLACED_WORKER_SUPPLEMENT",
        "design_name": "Test Supplement",
        "eligible_population": "displaced_workers",
        "annual_payment_per_person": 1000,
        "participation_rate": 0.5,
        "admin_cost_per_person": 100,
        "retraining_component_per_person": 200,
        "duration_years": 1.0,
        "illustrative_placeholder_only": True,
    }


def _input() -> dict:
    return {"design": _design(), "eligible_people": 100, "year": 2026}


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_transition_payment_rejects_nan_and_infinity(value: float) -> None:
    inputs = _input()
    inputs["eligible_people"] = value

    with pytest.raises(ValueError, match="finite"):
        evaluate_transition_payment(inputs)


def test_transition_payment_rejects_negative_eligible_people() -> None:
    inputs = _input()
    inputs["eligible_people"] = -1

    with pytest.raises(ValueError, match="cannot be negative"):
        evaluate_transition_payment(inputs)


@pytest.mark.parametrize("field", ["annual_payment_per_person", "admin_cost_per_person", "retraining_component_per_person"])
def test_transition_payment_rejects_negative_payment_values(field: str) -> None:
    inputs = _input()
    inputs["design"][field] = -1

    with pytest.raises(ValueError, match="cannot be negative"):
        evaluate_transition_payment(inputs)


def test_transition_payment_rejects_participation_rates_outside_bounds() -> None:
    inputs = _input()
    inputs["design"]["participation_rate"] = 1.1

    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        evaluate_transition_payment(inputs)


def test_transition_payment_calculates_cost_components() -> None:
    result = evaluate_transition_payment(_input())

    assert result.covered_people == 50
    assert result.base_payment_cost == 50000
    assert result.retraining_component_cost == 10000
    assert result.administrative_cost == 5000
    assert result.total_program_cost == 65000
    assert result.non_claims
