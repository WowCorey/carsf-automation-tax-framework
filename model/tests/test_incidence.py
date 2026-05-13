from __future__ import annotations

import math

import pytest

from carsf.incidence import evaluate_tax_incidence


def assumption() -> dict:
    return {
        "pass_through_rate": 0.2,
        "worker_pressure_rate": 0.1,
        "supplier_pressure_rate": 0.1,
        "capital_absorption_rate": 0.2,
        "assumption_basis": "illustrative placeholder",
        "illustrative_placeholder_only": True,
    }


def test_incidence_rejects_nan_and_infinity() -> None:
    for value in [math.nan, math.inf, -math.inf]:
        with pytest.raises(ValueError, match="liability must be finite"):
            evaluate_tax_incidence(value, assumption())


def test_incidence_rejects_negative_liability() -> None:
    with pytest.raises(ValueError, match="liability cannot be negative"):
        evaluate_tax_incidence(-1, assumption())


def test_incidence_rejects_rates_outside_bounds() -> None:
    bad = assumption()
    bad["pass_through_rate"] = 1.1

    with pytest.raises(ValueError, match="pass_through_rate must be in"):
        evaluate_tax_incidence(100, bad)


def test_incidence_rejects_allocation_rate_sums_above_one() -> None:
    bad = assumption()
    bad.update(
        {
            "pass_through_rate": 0.4,
            "worker_pressure_rate": 0.3,
            "supplier_pressure_rate": 0.2,
            "capital_absorption_rate": 0.2,
        }
    )

    with pytest.raises(ValueError, match="cannot sum above 1"):
        evaluate_tax_incidence(100, bad)


def test_zero_liability_produces_zero_incidence_amounts() -> None:
    result = evaluate_tax_incidence(0.0, assumption())

    assert result.consumer_pass_through_amount == 0.0
    assert result.worker_pressure_amount == 0.0
    assert result.supplier_pressure_amount == 0.0
    assert result.capital_absorption_amount == 0.0
    assert result.incidence_risk_band == "low"
