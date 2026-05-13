from __future__ import annotations

import math

import pytest

from carsf.transfer_pressure import evaluate_transfer_pressure


def _base_input() -> dict:
    return {
        "net_displaced_workers": 100,
        "average_support_payment_per_person": 20000,
        "transition_support_share": 0.5,
        "retraining_support_share": 0.2,
        "administrative_cost_per_person": 1000,
        "placeholder_basis": ["test placeholder"],
    }


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_transfer_pressure_rejects_nan_and_infinity(value: float) -> None:
    inputs = _base_input()
    inputs["net_displaced_workers"] = value

    with pytest.raises(ValueError, match="finite"):
        evaluate_transfer_pressure(inputs)


def test_transfer_pressure_rejects_negative_displaced_workers() -> None:
    inputs = _base_input()
    inputs["net_displaced_workers"] = -1

    with pytest.raises(ValueError, match="cannot be negative"):
        evaluate_transfer_pressure(inputs)


@pytest.mark.parametrize("field", ["transition_support_share", "retraining_support_share"])
def test_transfer_pressure_rejects_rates_outside_bounds(field: str) -> None:
    inputs = _base_input()
    inputs[field] = -0.1

    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        evaluate_transfer_pressure(inputs)


def test_transfer_pressure_calculates_placeholder_costs() -> None:
    result = evaluate_transfer_pressure(_base_input())

    assert result.support_payment_cost == 1000000
    assert result.retraining_support_cost == 400000
    assert result.administrative_cost == 100000
    assert result.total_transfer_pressure == 1500000
