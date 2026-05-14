from __future__ import annotations

from carsf.subgroups import assign_subgroups


def _scenario(**overrides):
    payload = {
        "scenario_id": "dual_income_one_displaced_regional",
        "household_type": "dual_income_one_displaced",
        "income_band": "middle_placeholder",
        "region_type": "regional",
        "reemployment_risk_band": "high",
        "budget_stress_band": "medium",
        "regional_stress_band": "high",
    }
    payload.update(overrides)
    return payload


def _definitions():
    return [
        {
            "subgroup_id": "regional_high_stress",
            "subgroup_name": "Regional High Stress",
            "region_type_filter": "regional",
            "regional_stress_filter": "high",
            "illustrative_placeholder_only": True,
        },
        {
            "subgroup_id": "delayed_reemployment",
            "subgroup_name": "Delayed Re-Employment",
            "reemployment_risk_filter": "high",
            "illustrative_placeholder_only": True,
        },
        {
            "subgroup_id": "low_income",
            "subgroup_name": "Low Income",
            "income_band_filter": "low_placeholder",
            "illustrative_placeholder_only": True,
        },
    ]


def test_subgroup_assignment_is_deterministic() -> None:
    assignment = assign_subgroups(_scenario(), list(reversed(_definitions())))

    assert assignment.subgroup_ids == ["delayed_reemployment", "regional_high_stress"]


def test_scenario_can_belong_to_multiple_subgroups() -> None:
    assignment = assign_subgroups(_scenario(income_band="low_placeholder"), _definitions())

    assert assignment.subgroup_ids == ["delayed_reemployment", "low_income", "regional_high_stress"]


def test_missing_subgroup_fields_warn_without_crashing() -> None:
    scenario = {"scenario_id": "incomplete_synthetic_scenario", "region_type": "regional"}
    assignment = assign_subgroups(scenario, _definitions())

    assert assignment.subgroup_ids == []
    assert any("missing field for subgroup filter" in warning for warning in assignment.warnings)
