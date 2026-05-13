from __future__ import annotations

import math

import pytest

from carsf.workforce_displacement import run_workforce_trajectory


def _base_input() -> dict:
    return {
        "start_year": 2026,
        "end_year": 2028,
        "baseline_employed_workers": 1000,
        "annual_displacement_rate": 0.10,
        "annual_reabsorption_rate": 0.30,
        "labour_force_growth_rate": 0.01,
        "average_taxable_income": 80000,
        "average_payg_tax_per_worker": 18000,
        "average_super_contribution_per_worker": 9000,
        "average_help_repayment_per_worker": 900,
        "placeholder_basis": ["test placeholder"],
    }


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_workforce_trajectory_rejects_nan_and_infinity(value: float) -> None:
    inputs = _base_input()
    inputs["baseline_employed_workers"] = value

    with pytest.raises(ValueError, match="finite"):
        run_workforce_trajectory(inputs)


def test_workforce_trajectory_rejects_negative_workers() -> None:
    inputs = _base_input()
    inputs["baseline_employed_workers"] = -1

    with pytest.raises(ValueError, match="cannot be negative"):
        run_workforce_trajectory(inputs)


@pytest.mark.parametrize("field", ["annual_displacement_rate", "annual_reabsorption_rate", "labour_force_growth_rate"])
def test_workforce_trajectory_rejects_rates_outside_bounds(field: str) -> None:
    inputs = _base_input()
    inputs[field] = 1.2

    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        run_workforce_trajectory(inputs)


def test_workforce_trajectory_never_produces_negative_remaining_workers() -> None:
    inputs = _base_input()
    inputs["annual_displacement_rate"] = 1.0
    inputs["annual_reabsorption_rate"] = 0.0
    result = run_workforce_trajectory(inputs)

    assert all(year.remaining_employed_workers >= 0 for year in result.years)
    assert all(year.net_displaced_workers >= 0 for year in result.years)
    assert result.cumulative_payg_loss >= 0
