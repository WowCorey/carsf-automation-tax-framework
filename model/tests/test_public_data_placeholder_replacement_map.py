from __future__ import annotations

import copy
import json

import pytest
import yaml

from carsf.public_data_placeholder_replacement_map import (
    BLOCKER_TYPE_VALUES,
    CLAIM_LEVEL_VALUES,
    PLACEHOLDER_REPLACEMENT_NON_CLAIMS,
    REPLACEMENT_CONFIDENCE_VALUES,
    REPLACEMENT_STATUS_VALUES,
    build_public_data_placeholder_replacement_result,
)


def load_manifest(repo_root):
    path = repo_root / "data" / "public_real" / "manifests" / "public_placeholder_replacement_manifest.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_public_values(repo_root):
    path = repo_root / "data" / "public_real" / "parsed" / "public_real_aggregate_values.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_placeholder_anchors(repo_root):
    path = repo_root / "data" / "public_pilot" / "placeholders" / "realistic_placeholder_anchors.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_source_manifest(repo_root):
    path = repo_root / "data" / "public_real" / "manifests" / "public_real_data_sources.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def build_result(repo_root):
    return build_public_data_placeholder_replacement_result(
        load_manifest(repo_root),
        load_public_values(repo_root),
        load_placeholder_anchors(repo_root),
        load_source_manifest(repo_root),
    )


def test_replacement_manifest_parses_and_has_required_fields(repo_root) -> None:
    payload = load_manifest(repo_root)

    for field in [
        "map_id",
        "map_name",
        "status",
        "non_claims",
        "input_artifacts",
        "replacement_status_taxonomy",
        "replacement_confidence_taxonomy",
        "blocker_type_taxonomy",
        "claim_level_taxonomy",
        "required_mapping_rules",
        "required_placeholder_coverage",
        "required_public_value_coverage",
        "forbidden_claims",
        "build_33_requirements",
    ]:
        assert field in payload

    assert PLACEHOLDER_REPLACEMENT_NON_CLAIMS[0] in payload["non_claims"]


def test_replacement_taxonomies_contain_required_values(repo_root) -> None:
    payload = load_manifest(repo_root)

    assert set(payload["replacement_status_taxonomy"]) == REPLACEMENT_STATUS_VALUES
    assert set(payload["replacement_confidence_taxonomy"]) == REPLACEMENT_CONFIDENCE_VALUES
    assert set(payload["blocker_type_taxonomy"]) == BLOCKER_TYPE_VALUES
    assert set(payload["claim_level_taxonomy"]) == CLAIM_LEVEL_VALUES


def test_build_31_loaded_public_values_are_loaded_and_used(repo_root) -> None:
    result = build_result(repo_root)

    assert len(result.public_aggregate_anchors) == 10
    assert result.summary.loaded_public_values_used == 10
    assert all(item.data_status == "loaded_public_aggregate" for item in result.public_aggregate_anchors)
    assert all(item.restricted_data is False for item in result.public_aggregate_anchors)
    assert all(item.personal_data is False for item in result.public_aggregate_anchors)


def test_source_candidates_not_loaded_are_not_treated_as_loaded(repo_root) -> None:
    result = build_result(repo_root)

    assert {item["source_id"] for item in result.source_candidates_not_loaded} == {
        "study_assist_help_thresholds_2025_26",
        "qld_payroll_tax_threshold_2025_26",
        "abs_labour_wage_aggregate_source_reference",
    }
    assert result.summary.public_source_candidates_treated_as_loaded is False
    assert all(item["treated_as_loaded"] is False for item in result.source_candidates_not_loaded)


def test_replacement_decisions_have_required_fields(repo_root) -> None:
    result = build_result(repo_root)

    assert result.replacement_decisions
    assert result.summary.placeholders_mapped == len(result.replacement_decisions) == 11
    for decision in result.replacement_decisions:
        assert decision.placeholder_id
        assert decision.replacement_status in REPLACEMENT_STATUS_VALUES
        assert decision.replacement_confidence in REPLACEMENT_CONFIDENCE_VALUES
        assert decision.claim_level in CLAIM_LEVEL_VALUES
        assert decision.what_changed
        assert decision.what_did_not_change
        assert decision.what_must_not_be_claimed
        assert decision.remaining_blockers
        assert decision.evidence_needed_before_calibration
        assert decision.current_placeholder_status == "realistic_placeholder"
        assert decision.calibration_completed is False
        assert decision.validation_claimed is False
        assert decision.actual_tax_payable_determined is False
        assert decision.firm_level_liability_logic_modified is False


def test_specific_public_value_mappings_are_bounded(repo_root) -> None:
    result = build_result(repo_root)
    decisions = {item.placeholder_id: item for item in result.replacement_decisions}

    opfte = decisions["anchor_opfte_minimum_wage"]
    assert opfte.replacement_status == "replaced_by_public_aggregate_anchor"
    assert {
        "fair_work_national_minimum_wage_hourly_2025",
        "fair_work_national_minimum_wage_weekly_2025",
    }.issubset(set(opfte.linked_public_value_ids))

    fiscal = decisions["anchor_fiscal_public_aggregates"]
    assert fiscal.replacement_status == "narrowed_by_public_aggregate_anchor"
    assert "ato_large_corporate_income_tax_received_2022_23" in fiscal.linked_public_value_ids
    assert "treasury_total_receipts_2025_26_estimate" in fiscal.linked_public_value_ids
    assert "firm-level CARSF liability modification" in fiscal.what_must_not_be_claimed

    super_anchor = decisions["anchor_super_guarantee_rate"]
    assert super_anchor.replacement_status == "replaced_by_public_aggregate_anchor"
    assert super_anchor.linked_public_value_ids == ["ato_super_guarantee_rate_2025_26"]


def test_placeholder_only_and_blocker_boundaries_remain(repo_root) -> None:
    result = build_result(repo_root)
    decisions = {item.placeholder_id: item for item in result.replacement_decisions}

    assert decisions["anchor_help_source_reference"].replacement_status == "blocked_until_restricted_data"
    assert decisions["anchor_payroll_tax_source_reference"].replacement_status == "blocked_until_external_review"
    assert decisions["anchor_uncertainty_source_reference_only"].replacement_status == "cannot_replace_with_public_aggregate_data"
    assert all(item.requires_external_review for item in result.replacement_decisions)
    assert any(item.requires_restricted_data for item in result.replacement_decisions)


def test_replacement_summary_flags_are_bounded(repo_root) -> None:
    summary = build_result(repo_root).summary

    assert summary.placeholder_replacement_map_created is True
    assert summary.new_data_loaded is False
    assert summary.loaded_public_values_used == 10
    assert summary.placeholders_replaced_by_public_anchor == 2
    assert summary.placeholders_narrowed_by_public_anchor == 3
    assert summary.placeholders_informed_by_public_anchor == 3
    assert summary.placeholders_blocked_until_restricted_data == 1
    assert summary.placeholders_blocked_until_external_review == 1
    assert summary.placeholders_cannot_replace_with_public_aggregate_data == 1
    assert summary.restricted_data_loaded is False
    assert summary.personal_data_loaded is False
    assert summary.taxpayer_level_data_loaded is False
    assert summary.firm_confidential_data_loaded is False
    assert summary.household_microdata_loaded is False
    assert summary.calibration_completed is False
    assert summary.validation_claimed is False
    assert summary.actual_tax_payable_determined is False
    assert summary.official_status_claimed is False
    assert summary.firm_level_liability_logic_modified is False


def test_replacement_guardrails_fail_closed_on_restricted_public_value(repo_root) -> None:
    values = copy.deepcopy(load_public_values(repo_root))
    values["values"][0]["restricted_data"] = True

    with pytest.raises(ValueError, match="public aggregate guardrails"):
        build_public_data_placeholder_replacement_result(
            load_manifest(repo_root),
            values,
            load_placeholder_anchors(repo_root),
            load_source_manifest(repo_root),
        )


def test_replacement_guardrails_fail_closed_when_public_value_missing(repo_root) -> None:
    values = copy.deepcopy(load_public_values(repo_root))
    values["values"] = values["values"][:-1]

    with pytest.raises(ValueError, match="public value coverage mismatch"):
        build_public_data_placeholder_replacement_result(
            load_manifest(repo_root),
            values,
            load_placeholder_anchors(repo_root),
            load_source_manifest(repo_root),
        )
