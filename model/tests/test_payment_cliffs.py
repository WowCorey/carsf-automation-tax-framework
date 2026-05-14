from __future__ import annotations

import math

import pytest

from carsf.payment_cliffs import evaluate_payment_cliff


def _cliff(**overrides):
    data = {
        "cliff_id": "cliff_test",
        "household_id": "hh_test",
        "support_before_change": 10000,
        "support_after_change": 2000,
        "income_before_change": 30000,
        "income_after_change": 34000,
        "trigger_type": "placeholder_phase_out",
        "trigger_description": "Synthetic support phase-out placeholder.",
    }
    data.update(overrides)
    return data


@pytest.mark.parametrize("field,value", [("support_before_change", math.inf), ("support_after_change", math.nan), ("income_before_change", -1)])
def test_payment_cliff_rejects_invalid_values(field, value) -> None:
    with pytest.raises(ValueError):
        evaluate_payment_cliff(_cliff(**{field: value}))


def test_payment_cliff_detects_support_loss_greater_than_income_gain() -> None:
    result = evaluate_payment_cliff(_cliff())

    assert result.support_loss == 8000
    assert result.income_gain == 4000
    assert result.net_position_change == -4000
    assert result.cliff_detected is True
    assert result.cliff_severity_band in {"medium", "high", "critical"}


def test_payment_cliff_does_not_trigger_when_income_gain_offsets_support_loss() -> None:
    result = evaluate_payment_cliff(_cliff(support_before_change=6000, support_after_change=3000, income_after_change=36000))

    assert result.support_loss == 3000
    assert result.income_gain == 6000
    assert result.cliff_detected is False
    assert result.cliff_severity_band == "none"
