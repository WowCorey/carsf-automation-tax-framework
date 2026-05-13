from __future__ import annotations

from carsf.burden_balance import evaluate_burden_balance


def test_burden_balance_not_assessable_when_national_inputs_missing() -> None:
    result = evaluate_burden_balance(
        {
            "automation_fiscal_damage": None,
            "automation_revenue_captured": None,
            "final_liability": 100,
            "aava": 1000,
            "nltg": 3,
        }
    )

    assert result.burden_balance_band == "not_assessable"
    assert result.review_required is True


def test_burden_balance_flags_under_capture() -> None:
    result = evaluate_burden_balance(
        {
            "automation_fiscal_damage": 1000,
            "automation_revenue_captured": 200,
            "final_liability": 200,
            "aava": 2000,
            "nltg": 4,
        }
    )

    assert result.coverage_ratio == 0.2
    assert result.capture_gap == 800
    assert result.burden_balance_band == "under_capture"


def test_burden_balance_flags_over_capture() -> None:
    result = evaluate_burden_balance(
        {
            "automation_fiscal_damage": 1000,
            "automation_revenue_captured": 1300,
            "final_liability": 1300,
            "aava": 2000,
            "nltg": 4,
        }
    )

    assert result.coverage_ratio == 1.3
    assert result.capture_gap == -300
    assert result.burden_balance_band == "over_capture"
