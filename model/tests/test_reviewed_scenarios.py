from __future__ import annotations

from carsf.scenario_review import review_scenario, summarise_reviewed_scenarios


def _range(metric: str, stability: str = "stable") -> dict:
    return {
        "range_id": f"{metric}-range",
        "metric_name": metric,
        "low": 10.0,
        "base": 12.0,
        "high": 14.0,
        "absolute_range_width": 4.0,
        "relative_range_width": 0.33,
        "ordered_correctly": True,
        "confidence_placeholder": "low",
        "calibration_status": "not_calibrated",
        "uncertainty_drivers": ["synthetic placeholder"],
        "stability_band": stability,
        "warnings": [],
        "non_claims": [],
    }


def _household_source(stability: str = "stable_high_risk", residual_stability: str = "stable") -> dict:
    return {
        "scenario_id": "synthetic_household_case",
        "household_id": "household_1",
        "residual_gap_range": _range("residual gap", residual_stability),
        "transition_support_range": _range("transition support", "stable"),
        "low_case_shock_band": "high",
        "base_case_shock_band": "high",
        "high_case_shock_band": "critical",
        "risk_signal_stability": stability,
        "primary_uncertainty_drivers": ["residual gap"],
        "warnings": [],
        "non_claims": [],
    }


def test_stable_high_risk_household_can_be_discussion_signal() -> None:
    result = review_scenario(
        {
            "review_id": "review-1",
            "source_type": "household",
            "source_result": _household_source(),
            "scenario_name": "Stable high household",
        }
    )

    assert result.review_category == "prototype_discussion_signal"
    assert result.display_level == "show_with_warning"
    assert result.firm_level_liability_modified is False


def test_stable_high_risk_household_with_fragile_metric_gets_strong_warning() -> None:
    result = review_scenario(
        {
            "review_id": "review-2",
            "source_type": "household",
            "source_result": _household_source(residual_stability="fragile"),
            "scenario_name": "Fragile high household",
        }
    )

    assert result.review_category == "discussion_with_strong_warning"
    assert result.display_level == "show_with_warning"
    assert "residual gap" in result.fragile_metrics


def test_range_sensitive_household_hides_point_estimate() -> None:
    result = review_scenario(
        {
            "review_id": "review-3",
            "source_type": "household",
            "source_result": _household_source(stability="range_sensitive"),
        }
    )

    assert result.review_category == "range_sensitive_do_not_use_as_point_estimate"
    assert result.display_level == "hide_point_estimate"
    assert result.suppress_point_estimate is True


def test_not_assessable_household_becomes_non_interpretable() -> None:
    result = review_scenario(
        {
            "review_id": "review-4",
            "source_type": "household",
            "source_result": _household_source(residual_stability="not_assessable"),
        }
    )

    assert result.review_category == "non_interpretable_until_calibrated"
    assert result.display_level == "hide_until_calibrated"


def test_missing_uncertainty_range_becomes_external_review_only() -> None:
    source = _household_source()
    source.pop("transition_support_range")

    result = review_scenario(
        {
            "review_id": "review-5",
            "source_type": "household",
            "source_result": source,
        }
    )

    assert result.review_category == "missing_uncertainty_range"
    assert result.display_level == "external_review_only"
    assert result.missing_ranges == ["transition_support_range"]


def test_fragile_subgroup_suppresses_point_estimate() -> None:
    source = {
        "subgroup_id": "regional_high_stress",
        "subgroup_name": "Regional high stress",
        "residual_gap_range": _range("residual gap", "stable"),
        "high_critical_share_range": _range("high critical share", "moderately_sensitive"),
        "subgroup_range_sensitivity": "fragile",
        "representative_of_real_population": False,
        "warnings": [],
    }

    result = review_scenario(
        {
            "review_id": "review-6",
            "source_type": "weighted_subgroup",
            "source_result": source,
            "subgroup_id": "regional_high_stress",
        }
    )

    assert result.review_category == "fragile_suppress_point_estimate"
    assert result.display_level == "hide_point_estimate"
    assert result.suppress_point_estimate is True


def test_non_representative_subgroup_always_warns() -> None:
    source = {
        "subgroup_id": "low_income",
        "subgroup_name": "Low income",
        "residual_gap_range": _range("residual gap", "stable"),
        "high_critical_share_range": _range("high critical share", "stable"),
        "subgroup_range_sensitivity": "stable",
        "representative_of_real_population": False,
        "warnings": [],
    }

    result = review_scenario(
        {
            "review_id": "review-7",
            "source_type": "weighted_subgroup",
            "source_result": source,
            "subgroup_id": "low_income",
        }
    )

    assert result.representative_of_real_population is False
    assert "Synthetic subgroup output is not population representative." in result.warnings


def test_zero_weight_subgroup_is_non_interpretable_until_calibrated() -> None:
    source = {
        "subgroup_id": "zero_weight",
        "subgroup_name": "Zero weight",
        "residual_gap_range": _range("residual gap", "stable"),
        "high_critical_share_range": _range("high critical share", "stable"),
        "subgroup_range_sensitivity": "stable",
        "representative_of_real_population": False,
        "warnings": [],
    }

    result = review_scenario(
        {
            "review_id": "review-8",
            "source_type": "weighted_subgroup",
            "source_result": source,
            "subgroup_id": "zero_weight",
            "total_synthetic_weight": 0,
        }
    )

    assert result.review_category == "non_interpretable_until_calibrated"
    assert result.display_level == "hide_until_calibrated"


def test_summary_counts_are_deterministic() -> None:
    rows = [
        review_scenario(
            {
                "review_id": "summary-1",
                "source_type": "household",
                "source_result": _household_source(),
                "scenario_name": "A",
            }
        ),
        review_scenario(
            {
                "review_id": "summary-2",
                "source_type": "household",
                "source_result": _household_source(stability="range_sensitive"),
                "scenario_name": "B",
            }
        ),
    ]

    first = summarise_reviewed_scenarios(rows).to_jsonable()
    second = summarise_reviewed_scenarios(rows).to_jsonable()

    assert first == second
    assert first["prototype_discussion_signal_count"] == 1
    assert first["range_sensitive_hidden_count"] == 1
