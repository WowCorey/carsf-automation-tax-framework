from __future__ import annotations

import pytest

from carsf.distributional_summary import summarise_distributional_scenarios


def _result(household_id: str, band: str, gap: float, drivers: list[str] | None = None) -> dict:
    return {
        "scenario_id": household_id,
        "household_id": household_id,
        "household_type": "synthetic",
        "budget_stress_band": band,
        "reemployment_risk_band": band,
        "regional_stress_band": band,
        "cliff_severity_band": None,
        "transition_support_amount": 0,
        "residual_household_gap_after_support": gap,
        "household_shock_band": band,
        "primary_risk_drivers": drivers or [],
    }


def test_distributional_summary_counts_shock_bands() -> None:
    summary = summarise_distributional_scenarios(
        [
            _result("hh_low", "low", 0),
            _result("hh_medium", "medium", 100),
            _result("hh_high", "high", 200, ["regional stress: high"]),
            _result("hh_critical", "critical", 300, ["regional stress: high"]),
        ]
    )

    assert summary.scenario_count == 4
    assert summary.low_shock_count == 1
    assert summary.medium_shock_count == 1
    assert summary.high_shock_count == 1
    assert summary.critical_shock_count == 1
    assert summary.average_residual_gap_placeholder == 150
    assert summary.highest_risk_households[0] == "hh_critical"
    assert summary.primary_systemic_risks == ["regional stress: high"]


def test_distributional_summary_rejects_empty_list() -> None:
    with pytest.raises(ValueError, match="at least one"):
        summarise_distributional_scenarios([])
