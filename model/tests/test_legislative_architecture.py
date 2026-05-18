from __future__ import annotations

import copy

import pytest
import yaml

from carsf.legislative_architecture import (
    REQUIRED_CORE_DEFINITIONS,
    REQUIRED_SCHEDULE_IDS,
    build_legislative_architecture_result,
    find_forbidden_affirmative_claims,
)


def load_payload(repo_root):
    path = repo_root / "data" / "legislative_architecture" / "legislative_architecture_skeleton.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_legislative_architecture_yaml_parses_and_has_required_top_level_fields(repo_root) -> None:
    payload = load_payload(repo_root)

    for field in [
        "architecture_id",
        "architecture_name",
        "status",
        "non_claims",
        "parts",
        "definitions",
        "schedules",
        "regulation_making_placeholders",
        "external_review_blockers",
        "safeguards",
        "evidence_power_placeholders",
        "anti_avoidance_placeholders",
        "commencement_transition_placeholders",
        "forbidden_claims",
    ]:
        assert field in payload


def test_legislative_architecture_builds_expected_summary_and_false_flags(repo_root) -> None:
    result = build_legislative_architecture_result(load_payload(repo_root), repo_root)
    summary = result.summary

    assert summary.total_parts == 21
    assert summary.total_divisions == 21
    assert summary.total_definition_placeholders >= len(REQUIRED_CORE_DEFINITIONS)
    assert summary.total_schedule_placeholders == len(REQUIRED_SCHEDULE_IDS)
    assert summary.total_regulation_making_placeholders >= 11
    assert summary.total_safeguard_placeholders >= 10
    assert summary.total_evidence_power_placeholders >= 9
    assert summary.total_anti_avoidance_placeholders >= 13
    assert summary.locked_or_reserved_for_counsel_count >= 1
    assert summary.operative_law_created is False
    assert summary.legal_sufficiency_claimed is False
    assert summary.statutory_power_created is False
    assert summary.notices_created is False
    assert summary.penalties_created is False
    assert summary.enforcement_created is False
    assert summary.real_data_used is False
    assert summary.firm_level_liability_logic_modified is False


def test_all_parts_are_non_operative_and_divisions_have_review_flags(repo_root) -> None:
    result = build_legislative_architecture_result(load_payload(repo_root), repo_root)

    for part in result.parts:
        assert part.non_operative_status is True
        assert part.external_review_required is True
        assert part.divisions
        for division in part.divisions:
            assert isinstance(division.requires_legal_review, bool)
            assert isinstance(division.requires_tax_review, bool)
            assert isinstance(division.requires_ato_methods_review, bool)
            assert isinstance(division.requires_treasury_review, bool)
            assert isinstance(division.requires_privacy_review, bool)
            assert isinstance(division.requires_external_calibration, bool)


def test_core_definition_placeholders_exist_and_are_not_operative(repo_root) -> None:
    result = build_legislative_architecture_result(load_payload(repo_root), repo_root)
    definitions_by_term = {item.term: item for item in result.definitions}

    assert REQUIRED_CORE_DEFINITIONS <= set(definitions_by_term)
    for definition in definitions_by_term.values():
        assert definition.must_not_be_used_as_operative_definition is True
        assert definition.requires_legal_review is True
        assert definition.requires_policy_review is True


def test_schedule_placeholders_reference_existing_yaml_and_are_not_official(repo_root) -> None:
    result = build_legislative_architecture_result(load_payload(repo_root), repo_root)
    schedules_by_id = {item.schedule_id: item for item in result.schedules}

    assert REQUIRED_SCHEDULE_IDS <= set(schedules_by_id)
    for schedule in schedules_by_id.values():
        assert (repo_root / schedule.source_yaml).exists()
        assert schedule.must_not_be_treated_as_official_schedule is True
        assert schedule.requires_external_calibration is True
        assert schedule.requires_legal_review is True


def test_evidence_power_placeholders_create_no_power_notice_or_real_data(repo_root) -> None:
    result = build_legislative_architecture_result(load_payload(repo_root), repo_root)

    for placeholder in result.evidence_power_placeholders:
        assert placeholder.flags["no_statutory_information_gathering_power_created"] is True
        assert placeholder.flags["no_notice_issued"] is True
        assert placeholder.flags["no_real_evidence_collected"] is True
        assert placeholder.flags["no_taxpayer_data_ingested"] is True
        assert placeholder.flags["no_firm_data_ingested"] is True
        assert placeholder.flags["no_restricted_data_ingested"] is True


def test_anti_avoidance_and_regulation_placeholders_are_non_operative(repo_root) -> None:
    result = build_legislative_architecture_result(load_payload(repo_root), repo_root)

    for placeholder in result.anti_avoidance_placeholders:
        assert placeholder.flags["not_operative_anti_avoidance_rule"] is True
        assert placeholder.flags["not_legal_test"] is True
        assert placeholder.flags["not_ato_position"] is True
    for placeholder in result.regulation_making_placeholders:
        assert placeholder.flags["no_real_regulation_making_power_created"] is True
        assert placeholder.flags["requires_constitutional_legal_drafting_review"] is True


def test_architecture_fails_if_part_is_not_non_operative(repo_root) -> None:
    payload = load_payload(repo_root)
    broken = copy.deepcopy(payload)
    broken["parts"][0]["non_operative_status"] = False

    with pytest.raises(ValueError, match="non-operative"):
        build_legislative_architecture_result(broken, repo_root)


def test_architecture_fails_if_definition_can_be_used_operatively(repo_root) -> None:
    payload = load_payload(repo_root)
    broken = copy.deepcopy(payload)
    broken["definitions"][0]["must_not_be_used_as_operative_definition"] = False

    with pytest.raises(ValueError, match="operative definition"):
        build_legislative_architecture_result(broken, repo_root)


def test_architecture_fails_on_missing_schedule_reference(repo_root) -> None:
    payload = load_payload(repo_root)
    broken = copy.deepcopy(payload)
    broken["schedules"][0]["source_yaml"] = "schedules/missing.yaml"

    with pytest.raises(ValueError, match="missing path"):
        build_legislative_architecture_result(broken, repo_root)


def test_forbidden_claim_scanner_allows_negative_non_claims_but_blocks_affirmative_claims() -> None:
    assert find_forbidden_affirmative_claims("This is not operative law and no statutory power is created.") == []
    assert "operative law" in find_forbidden_affirmative_claims("This architecture is operative law.")
    assert "statutory power is created" in find_forbidden_affirmative_claims("A statutory power is created.")
