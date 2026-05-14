from __future__ import annotations

import pytest

from carsf.weighted_distributional import run_weighted_distributional_aggregation


def _scenario(scenario_id: str, shock: str, residual_gap: float, **overrides):
    payload = {
        "scenario_id": scenario_id,
        "household_type": "single_adult",
        "income_band": "low_placeholder",
        "region_type": "metro",
        "reemployment_risk_band": "medium",
        "budget_stress_band": "high" if shock in {"high", "critical"} else "medium",
        "regional_stress_band": "medium",
        "household_shock_band": shock,
        "residual_household_gap_after_support": residual_gap,
    }
    payload.update(overrides)
    return payload


def _definition(subgroup_id: str = "all_synthetic", **overrides):
    payload = {
        "subgroup_id": subgroup_id,
        "subgroup_name": subgroup_id.replace("_", " ").title(),
        "illustrative_placeholder_only": True,
    }
    payload.update(overrides)
    return payload


def _weight(scenario_id: str, weight_value: float, subgroup_id: str = "all_synthetic"):
    return {
        "scenario_id": scenario_id,
        "subgroup_id": subgroup_id,
        "weight_value": weight_value,
        "weight_basis": "synthetic placeholder test weight",
        "calibrated": False,
        "illustrative_placeholder_only": True,
        "synthetic_weight_only": True,
    }


def _run(scenarios, weights, definitions=None):
    return run_weighted_distributional_aggregation(
        {
            "aggregation_id": "unit_test_weighted_distribution",
            "scenario_results": scenarios,
            "household_weights": weights,
            "subgroup_definitions": definitions or [_definition()],
            "calibration_status": "not_calibrated",
            "placeholder_basis": ["unit test"],
        }
    )


def test_weighted_aggregation_rejects_empty_scenario_list() -> None:
    with pytest.raises(ValueError, match="requires at least one scenario"):
        _run([], [])


def test_weighted_aggregation_handles_zero_total_weight_as_not_representative() -> None:
    result = _run(
        [_scenario("scenario_a", "high", 100.0)],
        [_weight("scenario_a", 0.0)],
    )

    assert result.total_synthetic_weight == 0.0
    assert result.overall_weighted_average_residual_gap is None
    assert result.overall_weighted_high_or_critical_share is None
    assert result.representative_of_real_population is False
    assert any("zero" in warning for warning in result.warnings)


def test_weighted_average_residual_gap_is_calculated_correctly() -> None:
    result = _run(
        [
            _scenario("scenario_a", "medium", 100.0),
            _scenario("scenario_b", "critical", 300.0),
        ],
        [_weight("scenario_a", 1.0), _weight("scenario_b", 3.0)],
    )

    assert result.overall_weighted_average_residual_gap == pytest.approx(250.0)


def test_weighted_high_critical_share_is_calculated_correctly() -> None:
    result = _run(
        [
            _scenario("scenario_a", "medium", 100.0),
            _scenario("scenario_b", "high", 200.0),
            _scenario("scenario_c", "critical", 400.0),
        ],
        [_weight("scenario_a", 2.0), _weight("scenario_b", 1.0), _weight("scenario_c", 1.0)],
    )

    assert result.overall_weighted_high_or_critical_share == pytest.approx(0.5)


def test_highest_risk_subgroups_are_deterministic() -> None:
    result = _run(
        [
            _scenario("scenario_a", "critical", 400.0, region_type="regional"),
            _scenario("scenario_b", "high", 200.0, region_type="metro"),
        ],
        [
            _weight("scenario_a", 2.0, "regional_stress"),
            _weight("scenario_b", 2.0, "metro_stress"),
        ],
        [
            _definition("metro_stress", region_type_filter="metro"),
            _definition("regional_stress", region_type_filter="regional"),
        ],
    )

    assert result.highest_risk_subgroups == ["regional_stress", "metro_stress"]
    assert result.representative_of_real_population is False


def test_weighted_aggregation_rejects_unknown_scenario_ids() -> None:
    with pytest.raises(ValueError, match="unknown scenario_id"):
        _run([_scenario("known", "low", 0.0)], [_weight("unknown", 1.0)])
