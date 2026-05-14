from __future__ import annotations

from carsf.weighted_uncertainty import evaluate_weighted_uncertainty


def _range(range_id: str, metric: str, low: float, base: float, high: float):
    return {
        "range_id": range_id,
        "metric_name": metric,
        "low": low,
        "base": base,
        "high": high,
        "confidence_placeholder": "low_placeholder_confidence_not_statistical",
        "calibration_status": "not_calibrated",
        "uncertainty_drivers": [metric],
        "illustrative_placeholder_only": True,
        "placeholder_basis": ["synthetic placeholder range"],
    }


def _aggregation():
    return {
        "aggregation_id": "weighted_test",
        "representative_of_real_population": False,
        "subgroup_results": [
            {
                "subgroup_id": "stable_high",
                "subgroup_name": "Stable High",
                "weighted_average_residual_gap": 10_000,
                "weighted_high_or_critical_share": 1.0,
            },
            {
                "subgroup_id": "missing_ranges",
                "subgroup_name": "Missing Ranges",
                "weighted_average_residual_gap": 0,
                "weighted_high_or_critical_share": 0.0,
            },
        ],
    }


def test_weighted_uncertainty_warns_on_missing_subgroup_ranges() -> None:
    result = evaluate_weighted_uncertainty(
        {
            "uncertainty_id": "weighted_missing_test",
            "weighted_aggregation_result": _aggregation(),
            "subgroup_residual_gap_ranges": {
                "stable_high": _range("stable_residual", "weighted_average_residual_gap", 9_000, 10_000, 11_000)
            },
            "subgroup_high_critical_share_ranges": {
                "stable_high": _range("stable_share", "weighted_high_or_critical_share", 0.80, 0.90, 1.00)
            },
        }
    )

    assert any("missing residual gap range" in warning for warning in result.warnings)
    assert any("missing high/critical share range" in warning for warning in result.warnings)


def test_weighted_uncertainty_detects_fragile_high_uncertainty_subgroups() -> None:
    result = evaluate_weighted_uncertainty(
        {
            "uncertainty_id": "weighted_fragile_test",
            "weighted_aggregation_result": _aggregation(),
            "subgroup_residual_gap_ranges": {
                "stable_high": _range("fragile_residual", "weighted_average_residual_gap", 0, 10_000, 30_000)
            },
            "subgroup_high_critical_share_ranges": {
                "stable_high": _range("stable_share", "weighted_high_or_critical_share", 0.80, 0.90, 1.00)
            },
        }
    )

    assert result.overall_range_sensitivity == "fragile"
    assert "stable_high" in result.highest_uncertainty_subgroups


def test_weighted_uncertainty_does_not_claim_population_uncertainty() -> None:
    result = evaluate_weighted_uncertainty(
        {
            "uncertainty_id": "weighted_nonclaim_test",
            "weighted_aggregation_result": _aggregation(),
            "subgroup_residual_gap_ranges": {},
            "subgroup_high_critical_share_ranges": {},
        }
    )

    assert all(item["representative_of_real_population"] is False for item in result.subgroup_results)
    assert any("not population uncertainty" in warning for warning in result.warnings)
