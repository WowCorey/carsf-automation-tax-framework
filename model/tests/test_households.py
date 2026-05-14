from __future__ import annotations

import math

import pytest

from carsf.households import evaluate_household_budget


def _household(**overrides):
    data = {
        "household_id": "hh_test",
        "household_type": "single_adult",
        "adults": 1,
        "children": 0,
        "region_type": "placeholder_region",
        "income_band": "middle_placeholder",
        "pre_displacement_income": 60000,
        "post_displacement_income": 20000,
        "existing_support_baseline": 5000,
        "housing_cost_placeholder": 20000,
        "essential_cost_placeholder": 18000,
        "debt_pressure_placeholder": 2000,
        "savings_buffer_placeholder": 3000,
        "illustrative_placeholder_only": True,
        "synthetic_household_only": True,
        "placeholder_basis": [],
    }
    data.update(overrides)
    return data


@pytest.mark.parametrize("field", ["pre_displacement_income", "post_displacement_income", "housing_cost_placeholder"])
def test_household_budget_rejects_nan_and_infinity(field) -> None:
    with pytest.raises(ValueError, match="finite"):
        evaluate_household_budget(_household(**{field: math.inf}))
    with pytest.raises(ValueError, match="finite"):
        evaluate_household_budget(_household(**{field: math.nan}))


@pytest.mark.parametrize("field", ["pre_displacement_income", "post_displacement_income", "existing_support_baseline", "housing_cost_placeholder"])
def test_household_budget_rejects_negative_values(field) -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        evaluate_household_budget(_household(**{field: -1}))


def test_household_budget_rejects_zero_person_household() -> None:
    with pytest.raises(ValueError, match="at least one"):
        evaluate_household_budget(_household(adults=0, children=0))


def test_household_budget_calculates_immediate_budget_gap() -> None:
    result = evaluate_household_budget(
        _household(
            post_displacement_income=10000,
            existing_support_baseline=5000,
            housing_cost_placeholder=20000,
            essential_cost_placeholder=15000,
            debt_pressure_placeholder=5000,
        )
    )

    assert result.total_basic_costs == 40000
    assert result.immediate_budget_gap == 25000


def test_household_budget_rejects_unlabelled_post_displacement_gain() -> None:
    with pytest.raises(ValueError, match="re_employed_gain"):
        evaluate_household_budget(_household(pre_displacement_income=50000, post_displacement_income=55000))

    result = evaluate_household_budget(
        _household(
            pre_displacement_income=50000,
            post_displacement_income=55000,
            placeholder_basis=["re_employed_gain"],
        )
    )
    assert result.income_loss == 0
