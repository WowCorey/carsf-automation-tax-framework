from __future__ import annotations

import json

import yaml

from carsf.full_repo_integrity_upgrade_audit import (
    FINDING_CATEGORY_VALUES,
    FINDING_SEVERITY_VALUES,
    FINDING_STATUS_VALUES,
    build_full_repo_integrity_audit_result,
)


def load_manifest(repo_root):
    return yaml.safe_load((repo_root / "data" / "audit" / "full_repo_integrity_upgrade_manifest.yaml").read_text(encoding="utf-8"))


def build_result(repo_root):
    return build_full_repo_integrity_audit_result(load_manifest(repo_root), repo_root)


def test_full_repo_integrity_manifest_parses_and_has_required_fields(repo_root) -> None:
    payload = load_manifest(repo_root)

    for field in [
        "audit_id",
        "audit_name",
        "status",
        "input_artifacts",
        "required_audit_sections",
        "required_runner_checks",
        "required_report_checks",
        "required_dashboard_checks",
        "required_manifest_checks",
        "required_docs_checks",
        "required_guardrail_checks",
        "required_non_claim_checks",
        "required_gap_registers",
        "forbidden_claims",
        "next_build_requirements",
    ]:
        assert field in payload

    assert "runner_coverage_matrix" in payload["required_audit_sections"]
    assert "missing_factor_register" in payload["required_gap_registers"]


def test_full_repo_integrity_taxonomies_are_available() -> None:
    assert {"critical", "high", "medium", "low", "informational"} == FINDING_SEVERITY_VALUES
    assert "fixed" in FINDING_STATUS_VALUES
    assert "cannot_fix_inside_repo" in FINDING_STATUS_VALUES
    assert "runner_gap" in FINDING_CATEGORY_VALUES
    assert "missing_factor" in FINDING_CATEGORY_VALUES


def test_full_repo_integrity_result_contains_required_registers(repo_root) -> None:
    result = build_result(repo_root)

    assert result.runner_coverage_matrix
    assert result.report_coverage_matrix
    assert result.dashboard_coverage_matrix
    assert result.release_manifest_coverage
    assert result.docs_coverage
    assert result.public_data_boundary_audit
    assert result.placeholder_boundary_audit
    assert result.calibration_boundary_audit
    assert result.scenario_constraint_audit
    assert result.guardrail_audit
    assert result.non_claim_boundary_audit
    assert result.result_coverage_matrix
    assert len(result.missing_factors) >= 30
    assert result.data_dependencies
    assert result.external_review_dependencies
    assert result.items_blocked_inside_repo


def test_full_repo_integrity_summary_flags_preserve_boundaries(repo_root) -> None:
    summary = build_result(repo_root).summary

    assert summary.full_repo_integrity_audit_created is True
    assert summary.safe_fixes_applied is True
    assert summary.runner_coverage_complete is True
    assert summary.report_coverage_complete is True
    assert summary.json_report_coverage_complete is True
    assert summary.dashboard_coverage_complete is True
    assert summary.release_manifest_coverage_complete is True
    assert summary.docs_coverage_complete is True
    assert summary.public_data_boundary_clean is True
    assert summary.placeholder_boundary_clean is True
    assert summary.calibration_boundary_clean is True
    assert summary.scenario_constraint_boundary_clean is True
    assert summary.guardrails_clean is True
    assert summary.non_claim_boundaries_clean is True
    assert summary.forbidden_claim_findings == 0
    assert summary.new_data_loaded is False
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


def test_full_repo_integrity_represents_existing_runners_and_reports(repo_root) -> None:
    result = build_result(repo_root)
    runners = {item.runner_path: item for item in result.runner_coverage_matrix}
    reports = {item.report_stem: item for item in result.report_coverage_matrix}
    build_rows = {item["build_or_layer"]: item for item in result.build_coverage_matrix}

    assert runners["scripts/run_public_aggregate_scenario_constraint_layer.py"].exists is True
    assert runners["scripts/run_full_repo_integrity_upgrade_audit.py"].ci_referenced is True
    assert runners["scripts/run_repo_guardrails.py"].ci_referenced is True
    assert reports["public_aggregate_scenario_constraint_layer"].markdown_exists is True
    assert reports["full_repo_integrity_upgrade_audit"].json_exists is True
    assert build_rows["example_results"]["runner_exists"] is True
    assert build_rows["mock_evidence_workflow"]["runner_exists"] is True


def test_generated_repo_report_contains_required_summary_flags(repo_root) -> None:
    payload = json.loads((repo_root / "reports" / "full_repo_integrity_upgrade_audit.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    for key in [
        "full_repo_integrity_audit_created",
        "safe_fixes_applied",
        "critical_findings_total",
        "runner_coverage_complete",
        "report_coverage_complete",
        "dashboard_coverage_complete",
        "public_data_boundary_clean",
        "placeholder_boundary_clean",
        "calibration_boundary_clean",
        "scenario_constraint_boundary_clean",
        "guardrails_clean",
        "non_claim_boundaries_clean",
        "forbidden_claim_findings",
        "new_data_loaded",
        "restricted_data_loaded",
        "personal_data_loaded",
        "taxpayer_level_data_loaded",
        "firm_confidential_data_loaded",
        "household_microdata_loaded",
        "calibration_completed",
        "validation_claimed",
        "actual_tax_payable_determined",
        "official_status_claimed",
        "firm_level_liability_logic_modified",
    ]:
        assert key in summary
