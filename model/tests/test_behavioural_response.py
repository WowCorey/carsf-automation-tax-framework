from __future__ import annotations

import copy

import pytest

from carsf.behavioural_response import (
    KNOWN_AVOIDANCE_FLAGS,
    evaluate_behavioural_response,
    evaluate_behavioural_responses,
    validate_behavioural_response_scenario,
)
from scripts.run_behavioural_response_simulation import load_scenarios
from scripts.run_sector_schedule_expansion import load_schedules


def _schedule_ids(repo_root) -> set[str]:
    return {schedule["schedule_id"] for schedule in load_schedules(repo_root / "schedules")}


def _scenarios(repo_root) -> list[dict]:
    return load_scenarios(repo_root / "examples" / "behavioural_response_scenarios.yaml")


def test_all_synthetic_behavioural_scenarios_parse(repo_root) -> None:
    scenarios = _scenarios(repo_root)

    assert len(scenarios) >= 10
    assert {scenario["scenario_id"] for scenario in scenarios} >= {
        "token_oversight_workforce_wrapper",
        "related_party_ai_service_fee_routing",
        "offshore_automation_service_routing",
        "customer_self_checkout_labour_relabelling",
        "robotics_lease_substitution",
        "platform_ip_royalty_routing",
        "schedule_classification_arbitrage",
        "artificial_low_aava_cost_loading",
        "cloud_inference_operating_cost_relabelling",
        "mixed_unit_apportionment_gaming",
        "fake_qlc_concentrated_roles",
        "open_source_ai_treatment_gap",
    }


def test_all_scenarios_contain_required_fields(repo_root) -> None:
    required = {
        "scenario_id",
        "scenario_name",
        "sector_schedule_id",
        "response_type",
        "description",
        "synthetic_triggers",
        "linked_avoidance_flags",
        "linked_countermeasures",
        "placeholder_response_pressure",
        "requires_external_review",
        "non_claims",
    }

    for scenario in _scenarios(repo_root):
        assert required <= set(scenario)


def test_all_referenced_sector_schedules_exist(repo_root) -> None:
    schedule_ids = _schedule_ids(repo_root)

    for scenario in _scenarios(repo_root):
        assert scenario["sector_schedule_id"] in schedule_ids
        validate_behavioural_response_scenario(scenario, schedule_ids)


def test_known_linked_avoidance_flags_validate_against_existing_constants(repo_root) -> None:
    for scenario in _scenarios(repo_root):
        for flag in scenario["linked_avoidance_flags"]:
            if not scenario.get("unresolved_new_flag"):
                assert flag in KNOWN_AVOIDANCE_FLAGS


def test_unknown_linked_avoidance_flag_fails_closed_without_unresolved_marker(repo_root) -> None:
    scenario = copy.deepcopy(_scenarios(repo_root)[0])
    scenario["linked_avoidance_flags"] = ["UNKNOWN_FLAG"]
    scenario["unresolved_new_flag"] = False

    with pytest.raises(ValueError, match="unknown linked avoidance flags"):
        validate_behavioural_response_scenario(scenario, _schedule_ids(repo_root))


def test_unknown_linked_avoidance_flag_allowed_when_explicitly_unresolved(repo_root) -> None:
    scenario = copy.deepcopy(_scenarios(repo_root)[0])
    scenario["linked_avoidance_flags"] = ["UNRESOLVED_NEW_FLAG"]
    scenario["unresolved_new_flag"] = True

    validated = validate_behavioural_response_scenario(scenario, _schedule_ids(repo_root))

    assert validated.linked_avoidance_flags == ["UNRESOLVED_NEW_FLAG"]


def test_missing_sector_schedule_fails_closed(repo_root) -> None:
    scenario = copy.deepcopy(_scenarios(repo_root)[0])
    scenario["sector_schedule_id"] = "missing_schedule"

    with pytest.raises(ValueError, match="missing sector schedule"):
        validate_behavioural_response_scenario(scenario, _schedule_ids(repo_root))


def test_missing_non_claim_language_fails_closed(repo_root) -> None:
    scenario = copy.deepcopy(_scenarios(repo_root)[0])
    scenario["non_claims"] = []

    with pytest.raises(ValueError, match="missing non-claim"):
        validate_behavioural_response_scenario(scenario, _schedule_ids(repo_root))


def test_every_result_has_do_not_predict_and_no_liability_modification(repo_root) -> None:
    results = evaluate_behavioural_responses(_scenarios(repo_root), _schedule_ids(repo_root))

    assert all(result.do_not_predict is True for result in results)
    assert all(result.do_not_score_real_taxpayer is True for result in results)
    assert all(result.firm_level_liability_logic_modified is False for result in results)


def test_response_pressure_band_is_deterministic(repo_root) -> None:
    scenario = _scenarios(repo_root)[0]
    schedule_ids = _schedule_ids(repo_root)

    first = evaluate_behavioural_response(scenario, schedule_ids)
    second = evaluate_behavioural_response(scenario, schedule_ids)

    assert first.response_pressure_score == second.response_pressure_score
    assert first.response_pressure_band == second.response_pressure_band


def test_critical_pressure_produces_external_review_required(repo_root) -> None:
    scenario = next(item for item in _scenarios(repo_root) if item["scenario_id"] == "platform_ip_royalty_routing")
    result = evaluate_behavioural_response(scenario, _schedule_ids(repo_root))

    assert result.response_pressure_band == "critical_review_required"
    assert result.review_status == "external_review_required"


def test_high_pressure_produces_strong_warning(repo_root) -> None:
    scenario = copy.deepcopy(_scenarios(repo_root)[0])
    scenario["scenario_id"] = "high-pressure-unit"
    scenario["placeholder_response_pressure"] = "high"
    scenario["linked_avoidance_flags"] = []
    scenario["response_type"] = "fake_qlc_inflation"
    scenario["sector_schedule_id"] = "automotive_repair"
    scenario["description"] = "Synthetic QLC pathway for unit testing only."
    scenario["synthetic_triggers"] = ["QLC evidence review"]
    scenario["linked_countermeasures"] = ["evidence_requirement"]

    result = evaluate_behavioural_response(scenario, _schedule_ids(repo_root), sector_stress_by_schedule={})

    assert result.response_pressure_band == "high_placeholder_response_pressure"
    assert result.review_status == "strong_warning_required"


def test_suppressed_scenario_produces_suppress_until_calibrated(repo_root) -> None:
    scenario = next(item for item in _scenarios(repo_root) if item["scenario_id"] == "open_source_ai_treatment_gap")
    result = evaluate_behavioural_response(scenario, _schedule_ids(repo_root))

    assert result.review_status == "suppress_until_calibrated"
    assert result.external_review_required is True


def test_countermeasure_categories_map_for_response_types(repo_root) -> None:
    scenarios = {scenario["scenario_id"]: scenario for scenario in _scenarios(repo_root)}

    offshore = evaluate_behavioural_response(scenarios["offshore_automation_service_routing"], _schedule_ids(repo_root))
    customer = evaluate_behavioural_response(scenarios["customer_self_checkout_labour_relabelling"], _schedule_ids(repo_root))
    robotics = evaluate_behavioural_response(scenarios["robotics_lease_substitution"], _schedule_ids(repo_root))

    assert {"offshore_attribution_review", "transfer_pricing_review", "legal_policy_review"} <= set(offshore.countermeasure_categories)
    assert {"customer_self_service_review", "schedule_authority_review"} <= set(customer.countermeasure_categories)
    assert {"capital_base_review", "aava_deductibility_review"} <= set(robotics.countermeasure_categories)
