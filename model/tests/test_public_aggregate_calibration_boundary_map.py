from __future__ import annotations

import copy
import json

import pytest
import yaml

from carsf.public_aggregate_calibration_boundary_map import (
    ALLOWED_USE_TYPE_VALUES,
    BLOCKER_TYPE_VALUES,
    BOUNDARY_STATUS_VALUES,
    CALIBRATION_BOUNDARY_NON_CLAIMS,
    CLAIM_LEVEL_VALUES,
    FORBIDDEN_USE_TYPE_VALUES,
    build_public_aggregate_calibration_boundary_result,
)


def load_manifest(repo_root):
    path = repo_root / "data" / "public_real" / "manifests" / "public_aggregate_calibration_boundary_manifest.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_public_values(repo_root):
    path = repo_root / "data" / "public_real" / "parsed" / "public_real_aggregate_values.json"
    return json.loads(path.read_text(encoding="utf-8"))


def load_source_manifest(repo_root):
    path = repo_root / "data" / "public_real" / "manifests" / "public_real_data_sources.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_replacement_report(repo_root):
    path = repo_root / "reports" / "public_data_placeholder_replacement_map.json"
    return json.loads(path.read_text(encoding="utf-8"))


def build_result(repo_root):
    return build_public_aggregate_calibration_boundary_result(
        load_manifest(repo_root),
        load_public_values(repo_root),
        load_source_manifest(repo_root),
        load_replacement_report(repo_root),
    )


def test_boundary_manifest_parses_and_has_required_fields(repo_root) -> None:
    payload = load_manifest(repo_root)

    for field in [
        "map_id",
        "map_name",
        "status",
        "non_claims",
        "input_artifacts",
        "allowed_use_type_taxonomy",
        "forbidden_use_type_taxonomy",
        "boundary_status_taxonomy",
        "claim_level_taxonomy",
        "blocker_type_taxonomy",
        "required_module_boundaries",
        "required_field_boundaries",
        "required_public_value_coverage",
        "forbidden_claims",
        "build_34_requirements",
    ]:
        assert field in payload

    assert CALIBRATION_BOUNDARY_NON_CLAIMS[0] in payload["non_claims"]


def test_boundary_taxonomies_contain_required_values(repo_root) -> None:
    payload = load_manifest(repo_root)

    assert set(payload["allowed_use_type_taxonomy"]) == ALLOWED_USE_TYPE_VALUES
    assert set(payload["forbidden_use_type_taxonomy"]) == FORBIDDEN_USE_TYPE_VALUES
    assert set(payload["boundary_status_taxonomy"]) == BOUNDARY_STATUS_VALUES
    assert set(payload["claim_level_taxonomy"]) == CLAIM_LEVEL_VALUES
    assert set(payload["blocker_type_taxonomy"]) == BLOCKER_TYPE_VALUES


def test_build_31_loaded_public_values_and_build_32_replacement_decisions_are_used(repo_root) -> None:
    result = build_result(repo_root)

    assert len(result.public_aggregate_values) == 10
    assert result.summary.loaded_public_values_used == 10
    assert result.summary.new_data_loaded is False
    assert result.field_boundary_decisions
    assert result.summary.field_boundaries_mapped == 11
    assert all(item.data_status == "loaded_public_aggregate" for item in result.public_aggregate_values)
    assert all(item.restricted_data is False for item in result.public_aggregate_values)
    assert all(item.personal_data is False for item in result.public_aggregate_values)


def test_source_candidates_not_loaded_are_not_treated_as_loaded(repo_root) -> None:
    result = build_result(repo_root)

    assert {item["source_id"] for item in result.source_candidates_not_loaded} == {
        "study_assist_help_thresholds_2025_26",
        "qld_payroll_tax_threshold_2025_26",
        "abs_labour_wage_aggregate_source_reference",
    }
    assert result.summary.public_source_candidates_treated_as_loaded is False
    assert all(item["treated_as_loaded"] is False for item in result.source_candidates_not_loaded)


def test_module_boundary_decisions_have_required_fields(repo_root) -> None:
    result = build_result(repo_root)

    assert result.summary.module_boundaries_mapped == len(result.module_boundary_decisions) == 19
    for decision in result.module_boundary_decisions:
        assert decision.allowed_use_types
        assert set(decision.allowed_use_types).issubset(ALLOWED_USE_TYPE_VALUES)
        assert decision.forbidden_use_types
        assert set(decision.forbidden_use_types).issubset(FORBIDDEN_USE_TYPE_VALUES)
        assert decision.boundary_status in BOUNDARY_STATUS_VALUES
        assert decision.claim_level in CLAIM_LEVEL_VALUES
        assert decision.what_public_data_can_support
        assert decision.what_public_data_cannot_support
        assert decision.calibration_blockers_remaining
        assert decision.evidence_needed_before_calibration
        assert decision.calibration_completed is False
        assert decision.validation_claimed is False
        assert decision.actual_tax_payable_determined is False
        assert decision.official_status_claimed is False
        assert decision.firm_level_liability_logic_modified is False


def test_specific_module_boundaries_are_non_claim_bounded(repo_root) -> None:
    decisions = {item.module_id: item for item in build_result(repo_root).module_boundary_decisions}

    opfte = decisions["opfte_benchmark_module"]
    assert "public_aggregate_anchor_only" in opfte.allowed_use_types
    assert "firm_liability_determination" in opfte.forbidden_use_types
    assert "actual_tax_payable" in opfte.forbidden_use_types
    assert "calibration_completed" in opfte.forbidden_use_types

    hle = decisions["hle_assumptions_module"]
    assert "public_aggregate_bound_only" in hle.allowed_use_types
    assert "representative labour costs" in hle.what_public_data_cannot_support

    fiscal = decisions["fiscal_trajectory_assumptions"]
    assert "contextual_reference_only" in fiscal.allowed_use_types
    assert "public_aggregate_bound_only" in fiscal.allowed_use_types
    assert "Treasury modelling" in fiscal.what_public_data_cannot_support
    assert "PBO costing" in fiscal.what_public_data_cannot_support

    payg = decisions["payg_erosion_assumptions"]
    assert payg.boundary_status == "requires_restricted_data"
    assert "taxpayer_behaviour_estimate" in payg.forbidden_use_types
    assert "CARSF revenue" in payg.what_public_data_cannot_support

    super_boundary = decisions["superannuation_contribution_pressure"]
    assert "public_aggregate_anchor_only" in super_boundary.allowed_use_types
    assert "employer behaviour" in super_boundary.what_public_data_cannot_support


def test_household_and_administrative_boundaries_remain_review_blocked(repo_root) -> None:
    decisions = {item.module_id: item for item in build_result(repo_root).module_boundary_decisions}

    household = decisions["household_distributional_scenarios"]
    assert household.boundary_status == "requires_restricted_data"
    assert household.requires_restricted_data is True
    assert household.requires_statistical_review is True

    weighting = decisions["household_weighting"]
    assert weighting.boundary_status == "requires_restricted_data"
    assert "household_population_estimate" in weighting.forbidden_use_types

    admin = decisions["administrative_compliance_workflow"]
    assert admin.requires_legal_review is True
    assert admin.requires_tax_review is True
    assert admin.requires_external_review is True


def test_boundary_summary_flags_are_false_for_forbidden_claims(repo_root) -> None:
    summary = build_result(repo_root).summary

    assert summary.public_aggregate_calibration_boundary_map_created is True
    assert summary.new_data_loaded is False
    assert summary.loaded_public_values_used == 10
    assert summary.module_boundaries_mapped == 19
    assert summary.field_boundaries_mapped == 11
    assert summary.public_source_candidates_treated_as_loaded is False
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


def test_boundary_guardrails_fail_closed_on_restricted_public_value(repo_root) -> None:
    values = copy.deepcopy(load_public_values(repo_root))
    values["values"][0]["restricted_data"] = True

    with pytest.raises(ValueError, match="public aggregate guardrails"):
        build_public_aggregate_calibration_boundary_result(
            load_manifest(repo_root),
            values,
            load_source_manifest(repo_root),
            load_replacement_report(repo_root),
        )


def test_boundary_guardrails_fail_closed_when_public_value_missing(repo_root) -> None:
    values = copy.deepcopy(load_public_values(repo_root))
    values["values"] = values["values"][:-1]

    with pytest.raises(ValueError, match="public value coverage mismatch"):
        build_public_aggregate_calibration_boundary_result(
            load_manifest(repo_root),
            values,
            load_source_manifest(repo_root),
            load_replacement_report(repo_root),
        )
