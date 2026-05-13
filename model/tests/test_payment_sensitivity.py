from __future__ import annotations

import math

import pytest

from carsf.payment_sensitivity import run_payment_sensitivity


def _base() -> dict:
    return {
        "portfolio_id": "sensitivity_base",
        "year": 2026,
        "population_base": 1000,
        "displaced_workers": 100,
        "automation_revenue_available": 100000,
        "commonwealth_gap_after_carsf": 0,
        "designs": [
            {
                "design_id": "supplement",
                "design_type": "DISPLACED_WORKER_SUPPLEMENT",
                "design_name": "Supplement",
                "eligible_population": "displaced_workers",
                "annual_payment_per_person": 1000,
                "participation_rate": 0.5,
                "admin_cost_per_person": 100,
                "retraining_component_per_person": 200,
                "duration_years": 1.0,
                "illustrative_placeholder_only": True,
            }
        ],
    }


def test_payment_sensitivity_output_ordering_is_deterministic() -> None:
    result = run_payment_sensitivity(
        _base(),
        {
            "participation_rate": [0.8, 0.2],
            "automation_revenue_available": [100000, 50000],
        },
    )

    assert [(point.parameter_name, point.parameter_value) for point in result.points] == [
        ("automation_revenue_available", 50000.0),
        ("automation_revenue_available", 100000.0),
        ("participation_rate", 0.2),
        ("participation_rate", 0.8),
    ]


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_payment_sensitivity_rejects_invalid_values(value: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        run_payment_sensitivity(_base(), {"participation_rate": [value]})


def test_payment_sensitivity_rejects_rates_outside_bounds() -> None:
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        run_payment_sensitivity(_base(), {"participation_rate": [1.2]})


def test_payment_sensitivity_gap_bounds() -> None:
    result = run_payment_sensitivity(_base(), {"automation_revenue_available": [0, 100000]})

    assert result.min_residual_gap <= result.max_residual_gap
    assert result.non_claims
