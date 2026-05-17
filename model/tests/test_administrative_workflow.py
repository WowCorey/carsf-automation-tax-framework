from __future__ import annotations

import copy

import pytest

import carsf.administrative_workflow as admin
from carsf.administrative_workflow import (
    default_evidence_requirement_ids,
    evaluate_administrative_workflow,
    evaluate_administrative_workflows,
    validate_administrative_workflow_scenario,
)
from scripts.run_administrative_compliance_workflow import (
    load_administrative_workflow_scenarios,
    load_synthetic_evidence_packet_ids,
)
from scripts.run_behavioural_response_simulation import load_scenarios as load_behavioural_scenarios
from scripts.run_sector_schedule_expansion import load_schedules


def _schedule_ids(repo_root) -> set[str]:
    return {schedule["schedule_id"] for schedule in load_schedules(repo_root / "schedules")}


def _behavioural_ids(repo_root) -> set[str]:
    return {
        scenario["scenario_id"]
        for scenario in load_behavioural_scenarios(repo_root / "examples" / "behavioural_response_scenarios.yaml")
    }


def _packet_ids(repo_root) -> set[str]:
    return load_synthetic_evidence_packet_ids(repo_root / "data" / "mock_evidence")


def _scenarios(repo_root) -> list[dict]:
    return load_administrative_workflow_scenarios(repo_root / "examples" / "administrative_workflow_scenarios.yaml")


def test_all_administrative_workflow_scenarios_parse(repo_root) -> None:
    scenarios = _scenarios(repo_root)

    assert len(scenarios) >= 8
    assert {scenario["scenario_id"] for scenario in scenarios} >= {
        "call_centre_token_oversight_triage",
        "related_party_ai_service_fee_review",
        "offshore_automation_service_attribution_review",
        "retail_self_checkout_labour_relabelling_review",
        "robotics_leasing_capital_base_review",
        "software_platform_ip_royalty_aasb_review",
        "mixed_unit_schedule_classification_review",
        "open_source_ai_treatment_locked_calibration_review",
        "artificial_low_aava_cost_loading_review",
        "grouped_entity_thin_australian_employer_review",
    }


def test_all_scenarios_contain_required_fields(repo_root) -> None:
    required = {
        "scenario_id",
        "scenario_name",
        "linked_example_or_case",
        "sector_schedule_id",
        "behavioural_response_scenario_ids",
        "trigger_flags",
        "requested_review_domains",
        "synthetic_evidence_packet_ids",
        "initial_review_state",
        "privacy_secrecy_sensitivity",
        "external_review_required",
        "suppress_until_calibrated",
        "description",
        "non_claims",
    }

    for scenario in _scenarios(repo_root):
        assert required <= set(scenario)


def test_all_referenced_sector_schedules_and_behavioural_responses_exist(repo_root) -> None:
    schedule_ids = _schedule_ids(repo_root)
    behavioural_ids = _behavioural_ids(repo_root)
    packet_ids = _packet_ids(repo_root)

    for scenario in _scenarios(repo_root):
        assert scenario["sector_schedule_id"] in schedule_ids
        assert set(scenario["behavioural_response_scenario_ids"]) <= behavioural_ids
        validate_administrative_workflow_scenario(
            scenario,
            schedule_ids,
            behavioural_ids,
            packet_ids,
        )


def test_unknown_behavioural_response_fails_closed(repo_root) -> None:
    scenario = copy.deepcopy(_scenarios(repo_root)[0])
    scenario["behavioural_response_scenario_ids"] = ["missing_behavioural_response"]

    with pytest.raises(ValueError, match="missing behavioural response"):
        validate_administrative_workflow_scenario(
            scenario,
            _schedule_ids(repo_root),
            _behavioural_ids(repo_root),
            _packet_ids(repo_root),
        )


def test_missing_sector_schedule_fails_closed(repo_root) -> None:
    scenario = copy.deepcopy(_scenarios(repo_root)[0])
    scenario["sector_schedule_id"] = "missing_schedule"

    with pytest.raises(ValueError, match="missing sector schedule"):
        validate_administrative_workflow_scenario(
            scenario,
            _schedule_ids(repo_root),
            _behavioural_ids(repo_root),
            _packet_ids(repo_root),
        )


def test_missing_non_claim_language_fails_closed(repo_root) -> None:
    scenario = copy.deepcopy(_scenarios(repo_root)[0])
    scenario["non_claims"] = []

    with pytest.raises(ValueError, match="missing non-claim"):
        validate_administrative_workflow_scenario(
            scenario,
            _schedule_ids(repo_root),
            _behavioural_ids(repo_root),
            _packet_ids(repo_root),
        )


def test_unknown_review_domain_fails_closed(repo_root) -> None:
    scenario = copy.deepcopy(_scenarios(repo_root)[0])
    scenario["requested_review_domains"] = ["unknown_review_domain"]

    with pytest.raises(ValueError, match="unknown review domains"):
        validate_administrative_workflow_scenario(
            scenario,
            _schedule_ids(repo_root),
            _behavioural_ids(repo_root),
            _packet_ids(repo_root),
        )


def test_unknown_evidence_requirement_mapping_fails_closed(repo_root, monkeypatch) -> None:
    scenario = copy.deepcopy(_scenarios(repo_root)[0])
    monkeypatch.setitem(admin.EVIDENCE_REQUIREMENTS_BY_DOMAIN, "core_formula", ["missing_requirement_id"])

    with pytest.raises(ValueError, match="unknown requirement IDs"):
        validate_administrative_workflow_scenario(
            scenario,
            _schedule_ids(repo_root),
            _behavioural_ids(repo_root),
            _packet_ids(repo_root),
            default_evidence_requirement_ids(),
        )


def test_evidence_request_bundles_only_use_existing_requirement_ids(repo_root) -> None:
    results = evaluate_administrative_workflows(
        _scenarios(repo_root),
        _schedule_ids(repo_root),
        _behavioural_ids(repo_root),
        _packet_ids(repo_root),
    )
    valid_ids = default_evidence_requirement_ids()

    for result in results:
        assert set(result.evidence_request_bundle.requirement_ids) <= valid_ids


def test_suppress_until_calibrated_scenario_is_suppressed(repo_root) -> None:
    scenario = next(
        item for item in _scenarios(repo_root) if item["scenario_id"] == "open_source_ai_treatment_locked_calibration_review"
    )
    result = evaluate_administrative_workflow(
        scenario,
        _schedule_ids(repo_root),
        _behavioural_ids(repo_root),
        _packet_ids(repo_root),
    )

    assert result.workflow_decision_band == "suppress_until_calibrated"
    assert result.workflow_status == "suppress_until_calibrated"
    assert result.external_review_required is True


def test_external_review_scenario_produces_locked_or_external_status(repo_root) -> None:
    scenario = next(item for item in _scenarios(repo_root) if item["scenario_id"] == "software_platform_ip_royalty_aasb_review")
    result = evaluate_administrative_workflow(
        scenario,
        _schedule_ids(repo_root),
        _behavioural_ids(repo_root),
        _packet_ids(repo_root),
    )

    assert result.external_review_required is True
    assert result.workflow_status in {"locked_for_external_review", "external_review_required"}


def test_every_result_has_no_enforcement_and_no_real_data_flags(repo_root) -> None:
    results = evaluate_administrative_workflows(
        _scenarios(repo_root),
        _schedule_ids(repo_root),
        _behavioural_ids(repo_root),
        _packet_ids(repo_root),
    )

    assert all(result.do_not_enforce is True for result in results)
    assert all(result.do_not_issue_notice is True for result in results)
    assert all(result.do_not_score_compliance is True for result in results)
    assert all(result.do_not_estimate_tax_payable is True for result in results)
    assert all(result.firm_level_liability_logic_modified is False for result in results)
    assert all(result.real_ato_power_claimed is False for result in results)
    assert all(result.real_enforcement_created is False for result in results)
    assert all(result.real_data_used is False for result in results)
