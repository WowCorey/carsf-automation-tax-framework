from __future__ import annotations

import pytest

from carsf.uncertainty_summary import summarise_uncertainty_results


def _household(scenario_id: str, stability: str, fragile: bool = False):
    return {
        "uncertainty_id": scenario_id,
        "scenario_id": scenario_id,
        "risk_signal_stability": stability,
        "residual_gap_range": {"stability_band": "fragile" if fragile else "stable"},
        "transition_support_range": {"stability_band": "stable"},
        "reemployment_months_range": None,
        "regional_stress_range": None,
        "payment_cliff_loss_range": None,
    }


def test_uncertainty_summary_counts_stability_bands() -> None:
    summary = summarise_uncertainty_results(
        [
            _household("stable_high", "stable_high_risk"),
            _household("stable_low", "stable_low_risk"),
            _household("sensitive", "range_sensitive", fragile=True),
        ]
    )

    assert summary.household_uncertainty_count == 3
    assert summary.stable_high_risk_count == 1
    assert summary.stable_low_risk_count == 1
    assert summary.range_sensitive_count == 1
    assert summary.fragile_metric_count == 1
    assert "sensitive" in summary.highest_uncertainty_items


def test_uncertainty_summary_rejects_empty_household_results() -> None:
    with pytest.raises(ValueError, match="requires at least one household result"):
        summarise_uncertainty_results([])


def test_uncertainty_summary_includes_weighted_stable_high_signals() -> None:
    summary = summarise_uncertainty_results(
        [_household("stable_high", "stable_high_risk")],
        [{"stable_high_risk_subgroups": ["critical_budget_stress"], "subgroup_results": []}],
    )

    assert summary.strongest_stable_risk_signals == ["critical_budget_stress", "stable_high"]
    assert any("not real uncertainty quantification" in warning for warning in summary.warnings)
