from __future__ import annotations

import copy
import json

import pytest
import yaml

from carsf.public_aggregate_scenario_constraint_layer import (
    CLAIM_LEVEL_VALUES,
    CONSTRAINT_STATUS_VALUES,
    DISPLAY_RULE_VALUES,
    FORBIDDEN_IMPLICATION_VALUES,
    SCENARIO_CONSTRAINT_NON_CLAIMS,
    SCENARIO_OUTPUT_STATUS_VALUES,
    build_public_aggregate_scenario_constraint_result,
)


def load_manifest(repo_root):
    path = repo_root / "data" / "public_real" / "manifests" / "public_aggregate_scenario_constraint_manifest.yaml"
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


def load_boundary_report(repo_root):
    path = repo_root / "reports" / "public_aggregate_calibration_boundary_map.json"
    return json.loads(path.read_text(encoding="utf-8"))


def build_result(repo_root):
    return build_public_aggregate_scenario_constraint_result(
        load_manifest(repo_root),
        load_public_values(repo_root),
        load_source_manifest(repo_root),
        load_replacement_report(repo_root),
        load_boundary_report(repo_root),
    )


def test_scenario_constraint_manifest_parses_and_has_required_fields(repo_root) -> None:
    payload = load_manifest(repo_root)

    for field in [
        "constraint_layer_id",
        "constraint_layer_name",
        "status",
        "non_claims",
        "input_artifacts",
        "scenario_output_status_taxonomy",
        "display_rule_taxonomy",
        "forbidden_implication_taxonomy",
        "constraint_status_taxonomy",
        "claim_level_taxonomy",
        "required_module_constraints",
        "required_field_constraints",
        "required_dashboard_rules",
        "forbidden_claims",
        "build_35_requirements",
    ]:
        assert field in payload

    assert SCENARIO_CONSTRAINT_NON_CLAIMS[0] in payload["non_claims"]


def test_scenario_constraint_taxonomies_contain_required_values(repo_root) -> None:
    payload = load_manifest(repo_root)

    assert set(payload["scenario_output_status_taxonomy"]) == SCENARIO_OUTPUT_STATUS_VALUES
    assert set(payload["display_rule_taxonomy"]) == DISPLAY_RULE_VALUES
    assert set(payload["forbidden_implication_taxonomy"]) == FORBIDDEN_IMPLICATION_VALUES
    assert set(payload["constraint_status_taxonomy"]) == CONSTRAINT_STATUS_VALUES
    assert set(payload["claim_level_taxonomy"]) == CLAIM_LEVEL_VALUES


def test_build_31_32_33_inputs_are_used_without_new_data(repo_root) -> None:
    result = build_result(repo_root)

    assert len(result.public_aggregate_values) == 10
    assert result.summary.loaded_public_values_used == 10
    assert result.summary.new_data_loaded is False
    assert result.summary.module_constraints_mapped == 20
    assert result.summary.field_constraints_mapped == 11
    assert any(item.linked_placeholder_decision_ids for item in result.module_scenario_constraints)
    assert all(item.linked_boundary_decision_id for item in result.module_scenario_constraints)
    assert all(item["data_status"] == "loaded_public_aggregate" for item in result.public_aggregate_values)
    assert all(item["restricted_data"] is False for item in result.public_aggregate_values)
    assert all(item["personal_data"] is False for item in result.public_aggregate_values)


def test_source_candidates_not_loaded_are_not_treated_as_loaded(repo_root) -> None:
    result = build_result(repo_root)

    assert {item["source_id"] for item in result.source_candidates_not_loaded} == {
        "study_assist_help_thresholds_2025_26",
        "qld_payroll_tax_threshold_2025_26",
        "abs_labour_wage_aggregate_source_reference",
    }
    assert result.summary.public_source_candidates_treated_as_loaded is False
    assert all(item["treated_as_loaded"] is False for item in result.source_candidates_not_loaded)


def test_module_and_field_scenario_constraints_have_required_fields(repo_root) -> None:
    result = build_result(repo_root)

    assert result.module_scenario_constraints
    assert result.field_scenario_constraints
    for constraint in result.module_scenario_constraints:
        assert constraint.scenario_output_status in SCENARIO_OUTPUT_STATUS_VALUES
        assert constraint.display_rule in DISPLAY_RULE_VALUES
        assert constraint.constraint_status in CONSTRAINT_STATUS_VALUES
        assert constraint.claim_level in CLAIM_LEVEL_VALUES
        assert constraint.allowed_display_outputs
        assert constraint.blocked_display_outputs
        assert constraint.forbidden_implications
        assert constraint.reviewer_warning
        assert constraint.evidence_needed_to_lift_constraint
        assert constraint.calibration_completed is False
        assert constraint.validation_claimed is False
        assert constraint.actual_tax_payable_determined is False
        assert constraint.official_status_claimed is False
        assert constraint.firm_level_liability_logic_modified is False

    for constraint in result.field_scenario_constraints:
        assert constraint.scenario_output_status in SCENARIO_OUTPUT_STATUS_VALUES
        assert constraint.display_rule in DISPLAY_RULE_VALUES
        assert constraint.constraint_status in CONSTRAINT_STATUS_VALUES
        assert constraint.claim_level in CLAIM_LEVEL_VALUES
        assert constraint.allowed_display_outputs
        assert constraint.blocked_display_outputs
        assert constraint.forbidden_implications
        assert constraint.reviewer_warning
        assert constraint.evidence_needed_to_lift_constraint
        assert constraint.calibration_completed is False
        assert constraint.validation_claimed is False
        assert constraint.actual_tax_payable_determined is False
        assert constraint.firm_level_liability_logic_modified is False


def test_specific_scenario_constraints_block_forbidden_implications(repo_root) -> None:
    constraints = {item.module_id: item for item in build_result(repo_root).module_scenario_constraints}

    opfte = constraints["opfte_benchmark_module"]
    assert opfte.scenario_output_status == "display_as_public_aggregate_anchor_only"
    assert "firm liability determination" in opfte.blocked_display_outputs
    assert "actual tax payable" in opfte.blocked_display_outputs
    assert "calibration_completed" in opfte.forbidden_implications

    hle = constraints["hle_assumptions_module"]
    assert hle.scenario_output_status == "display_as_public_aggregate_bound_only"
    assert "representative labour-cost estimate" in hle.blocked_display_outputs

    fiscal = constraints["fiscal_trajectory_assumptions"]
    assert fiscal.scenario_output_status == "display_as_public_aggregate_bound_only"
    assert "Treasury modelling" in fiscal.blocked_display_outputs
    assert "PBO costing" in fiscal.blocked_display_outputs
    assert "treasury_modelling" in fiscal.forbidden_implications
    assert "pbo_costing" in fiscal.forbidden_implications

    payg = constraints["payg_erosion_assumptions"]
    assert payg.scenario_output_status == "mark_non_interpretable"
    assert payg.constraint_status == "non_interpretable"
    assert "taxpayer behaviour estimate" in payg.blocked_display_outputs

    super_constraint = constraints["superannuation_contribution_pressure"]
    assert super_constraint.scenario_output_status == "display_as_public_aggregate_anchor_only"
    assert "employer behaviour estimate" in super_constraint.blocked_display_outputs
    assert "ato_guidance" in super_constraint.forbidden_implications


def test_household_administrative_legal_and_dashboard_constraints(repo_root) -> None:
    constraints = {item.module_id: item for item in build_result(repo_root).module_scenario_constraints}

    household = constraints["household_distributional_scenarios"]
    assert household.scenario_output_status == "hide_from_reviewer_dashboard"
    assert household.constraint_status == "hidden_for_reviewer_safety"
    assert "population estimate" in household.blocked_display_outputs

    behavioural = constraints["behavioural_response_gaming_simulation"]
    assert behavioural.scenario_output_status == "mark_non_interpretable"
    assert "causal response" in behavioural.blocked_display_outputs

    admin = constraints["administrative_compliance_workflow"]
    assert admin.scenario_output_status == "display_as_reviewer_traceability_only"
    assert "compliance scoring" in admin.blocked_display_outputs
    assert "compliance_scoring" in admin.forbidden_implications

    legal = constraints["legislative_architecture_skeleton"]
    assert legal.scenario_output_status == "display_as_reviewer_traceability_only"
    assert "legal sufficiency" in legal.blocked_display_outputs

    dashboard = constraints["executive_dashboard_consolidation"]
    assert dashboard.scenario_output_status == "display_as_reviewer_traceability_only"
    assert "readiness scoring" in dashboard.blocked_display_outputs
    assert "readiness_scoring" in dashboard.forbidden_implications


def test_scenario_constraint_summary_flags_are_false_for_forbidden_claims(repo_root) -> None:
    summary = build_result(repo_root).summary

    assert summary.public_aggregate_scenario_constraint_layer_created is True
    assert summary.new_data_loaded is False
    assert summary.loaded_public_values_used == 10
    assert summary.module_constraints_mapped == 20
    assert summary.field_constraints_mapped == 11
    assert summary.outputs_marked_non_interpretable >= 3
    assert summary.outputs_hidden_from_reviewer_dashboard >= 1
    assert summary.forbidden_implications_mapped == len(FORBIDDEN_IMPLICATION_VALUES)
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


def test_scenario_constraints_fail_closed_on_restricted_public_value(repo_root) -> None:
    values = copy.deepcopy(load_public_values(repo_root))
    values["values"][0]["restricted_data"] = True

    with pytest.raises(ValueError, match="privacy guardrails"):
        build_public_aggregate_scenario_constraint_result(
            load_manifest(repo_root),
            values,
            load_source_manifest(repo_root),
            load_replacement_report(repo_root),
            load_boundary_report(repo_root),
        )


def test_scenario_constraints_fail_closed_when_boundary_module_missing(repo_root) -> None:
    boundary = copy.deepcopy(load_boundary_report(repo_root))
    payload = boundary["public_aggregate_calibration_boundary_map"]
    payload["module_boundary_decisions"] = payload["module_boundary_decisions"][:-1]

    with pytest.raises(ValueError, match="module scenario constraint coverage mismatch"):
        build_public_aggregate_scenario_constraint_result(
            load_manifest(repo_root),
            load_public_values(repo_root),
            load_source_manifest(repo_root),
            load_replacement_report(repo_root),
            boundary,
        )
