from __future__ import annotations

import math

import pytest

from carsf.public_revenue import evaluate_public_revenue


def _base_input() -> dict:
    return {
        "payg_loss": 100,
        "company_tax_change": 10,
        "gst_consumption_change": 5,
        "super_contribution_loss": 20,
        "help_repayment_loss": 2,
        "state_payroll_tax_loss": 3,
        "automation_revenue_captured": 50,
        "other_revenue_change": 4,
        "placeholder_basis": ["test placeholder"],
    }


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_public_revenue_rejects_nan_and_infinity(value: float) -> None:
    inputs = _base_input()
    inputs["payg_loss"] = value

    with pytest.raises(ValueError, match="finite"):
        evaluate_public_revenue(inputs)


def test_public_revenue_rejects_negative_automation_revenue_captured() -> None:
    inputs = _base_input()
    inputs["automation_revenue_captured"] = -1

    with pytest.raises(ValueError, match="cannot be negative"):
        evaluate_public_revenue(inputs)


def test_public_revenue_calculates_residual_gap() -> None:
    result = evaluate_public_revenue(_base_input())

    assert result.labour_linked_revenue_loss == 122
    assert result.total_revenue_loss_before_carsf == 141
    assert result.net_commonwealth_gap_after_carsf == 91
    assert result.total_public_sector_gap == 94
