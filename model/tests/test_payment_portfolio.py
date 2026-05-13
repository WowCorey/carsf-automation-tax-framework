from __future__ import annotations

import math

import pytest

from carsf.payment_portfolio import evaluate_payment_portfolio


def _design(payment: float = 1000, participation: float = 0.5) -> dict:
    return {
        "design_id": "supplement",
        "design_type": "DISPLACED_WORKER_SUPPLEMENT",
        "design_name": "Supplement",
        "eligible_population": "displaced_workers",
        "annual_payment_per_person": payment,
        "participation_rate": participation,
        "admin_cost_per_person": 100,
        "retraining_component_per_person": 200,
        "duration_years": 1.0,
        "illustrative_placeholder_only": True,
    }


def _portfolio(revenue: float = 100000) -> dict:
    return {
        "portfolio_id": "test_portfolio",
        "year": 2026,
        "population_base": 1000,
        "displaced_workers": 100,
        "designs": [_design()],
        "automation_revenue_available": revenue,
        "commonwealth_gap_after_carsf": 5000,
    }


@pytest.mark.parametrize("field", ["population_base", "displaced_workers"])
def test_payment_portfolio_rejects_invalid_population_values(field: str) -> None:
    inputs = _portfolio()
    inputs[field] = -1

    with pytest.raises(ValueError, match="cannot be negative"):
        evaluate_payment_portfolio(inputs)


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_payment_portfolio_rejects_non_finite_population(value: float) -> None:
    inputs = _portfolio()
    inputs["population_base"] = value

    with pytest.raises(ValueError, match="finite"):
        evaluate_payment_portfolio(inputs)


def test_payment_portfolio_calculates_total_program_cost() -> None:
    result = evaluate_payment_portfolio(_portfolio())

    assert result.total_program_cost == 65000


def test_payment_portfolio_calculates_funding_coverage_ratio() -> None:
    result = evaluate_payment_portfolio(_portfolio(revenue=130000))

    assert result.funding_coverage_ratio == 2.0


def test_payment_portfolio_calculates_residual_funding_gap() -> None:
    result = evaluate_payment_portfolio(_portfolio(revenue=50000))

    assert result.residual_funding_gap == 15000
    assert result.residual_commonwealth_gap_plus_payment_gap == 20000


def test_automation_revenue_increase_improves_funding_coverage() -> None:
    low = evaluate_payment_portfolio(_portfolio(revenue=10000))
    high = evaluate_payment_portfolio(_portfolio(revenue=100000))

    assert high.funding_coverage_ratio > low.funding_coverage_ratio
    assert high.residual_funding_gap < low.residual_funding_gap
