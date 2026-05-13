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

    assert result.commonwealth_revenue_loss_before_carsf == 121
    assert result.retirement_contribution_pressure == 20
    assert result.net_commonwealth_gap_after_carsf == 71
    assert result.total_public_sector_gap == 74
    assert result.broader_labour_linked_pressure == 94


def test_superannuation_loss_does_not_increase_commonwealth_gap() -> None:
    base = _base_input()
    without_super = dict(base, super_contribution_loss=0)
    with_super = dict(base, super_contribution_loss=999)

    low = evaluate_public_revenue(without_super)
    high = evaluate_public_revenue(with_super)

    assert high.net_commonwealth_gap_after_carsf == low.net_commonwealth_gap_after_carsf
    assert high.total_public_sector_gap == low.total_public_sector_gap
    assert high.retirement_contribution_pressure == 999
    assert high.broader_labour_linked_pressure == low.broader_labour_linked_pressure + 999


def test_offsetting_revenue_gain_reduces_commonwealth_gap_when_allowed() -> None:
    without_gain = evaluate_public_revenue(_base_input())
    with_gain = evaluate_public_revenue(dict(_base_input(), company_tax_change=-25, allow_revenue_gains=True))

    assert with_gain.net_commonwealth_gap_after_carsf == without_gain.net_commonwealth_gap_after_carsf - 35
