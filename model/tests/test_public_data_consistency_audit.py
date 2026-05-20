from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest
import yaml

from carsf.public_data_consistency_audit import (
    AUDIT_STATUS_VALUES,
    AUDIT_TYPE_VALUES,
    RECONCILIATION_SCOPE_VALUES,
    build_public_data_consistency_audit_result,
)


def _load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _result(repo_root: Path):
    return build_public_data_consistency_audit_result(
        manifest=_load_yaml(repo_root / "data" / "public_pilot" / "consistency_audit_manifest.yaml"),
        public_pilot_report=_load_json(repo_root / "reports" / "public_data_pilot.json"),
        public_data_evidence_map_report=_load_json(repo_root / "reports" / "public_data_evidence_map.json"),
        public_pilot_markdown=(repo_root / "reports" / "public_data_pilot.md").read_text(encoding="utf-8"),
        public_data_evidence_map_markdown=(repo_root / "reports" / "public_data_evidence_map.md").read_text(encoding="utf-8"),
        digest_payload=_load_json(repo_root / "data" / "public_pilot" / "digests" / "public_data_pilot_digests.json"),
        dashboard_path=repo_root / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py",
        dashboard_text=(repo_root / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py").read_text(encoding="utf-8"),
        repo_root=repo_root,
    )


def test_consistency_audit_manifest_parses_and_has_required_top_level_fields(repo_root) -> None:
    manifest = _load_yaml(repo_root / "data" / "public_pilot" / "consistency_audit_manifest.yaml")
    required = {
        "audit_id",
        "audit_name",
        "status",
        "non_claims",
        "input_artifacts",
        "audit_status_taxonomy",
        "audit_type_taxonomy",
        "reconciliation_scope_taxonomy",
        "required_count_reconciliations",
        "required_source_reference_reconciliations",
        "required_extract_reconciliations",
        "required_placeholder_reconciliations",
        "required_module_boundary_checks",
        "required_digest_checks",
        "required_report_json_checks",
        "required_dashboard_checks",
        "required_non_claim_checks",
        "forbidden_claims",
        "build_30_requirements",
    }
    assert required <= set(manifest)
    assert set(manifest["audit_status_taxonomy"]) == AUDIT_STATUS_VALUES
    assert set(manifest["audit_type_taxonomy"]) == AUDIT_TYPE_VALUES
    assert set(manifest["reconciliation_scope_taxonomy"]) == RECONCILIATION_SCOPE_VALUES


def test_consistency_audit_reconciles_current_public_data_pilot_counts(repo_root) -> None:
    result = _result(repo_root)
    summary = result.summary
    assert summary.total_audit_findings == 13
    assert summary.findings_reconciled == 13
    assert summary.findings_fail_closed == 0
    assert summary.source_references_total == 8
    assert summary.loaded_public_extracts_total == 5
    assert summary.source_reference_only_extracts_total == 3
    assert summary.placeholder_anchors_total == 11
    assert summary.field_sanity_checks_total == 10
    assert summary.module_sanity_checks_total == 11


def test_loaded_extracts_have_metadata_and_evidence_rows(repo_root) -> None:
    result = _result(repo_root)
    assert result.source_reference_reconciliation.finding.audit_status == "reconciled"
    assert result.extract_evidence_reconciliation.finding.audit_status == "reconciled"
    pilot = _load_json(repo_root / "reports" / "public_data_pilot.json")["public_data_pilot"]
    evidence = _load_json(repo_root / "reports" / "public_data_evidence_map.json")["public_data_evidence_map"]
    evidence_ids = {item["extract_id"] for item in evidence["loaded_extract_evidence"]}
    for extract in pilot["public_aggregate_extracts"]:
        if extract["data_status"] == "real_public_data_loaded":
            assert extract["source_url"]
            assert extract["source_locator"]
            assert extract["source_value_note"]
            assert extract["value_review_status"]
            status = extract["value_review_status"].lower()
            assert "externally_validated" not in status
            assert "approved" not in status
            assert "ato_guidance" not in status
            assert "treasury_modelling" not in status
            assert extract["extract_id"] in evidence_ids


def test_source_reference_only_records_are_not_counted_as_loaded(repo_root) -> None:
    result = _result(repo_root)
    assert result.source_reference_only_count_audit.finding.audit_status == "reconciled"
    evidence = _load_json(repo_root / "reports" / "public_data_evidence_map.json")["public_data_evidence_map"]
    loaded = {item["extract_id"] for item in evidence["loaded_extract_evidence"]}
    source_only = {item["extract_id"] for item in evidence["source_reference_only_evidence"]}
    assert loaded.isdisjoint(source_only)
    assert len(loaded) == 5
    assert len(source_only) == 3


def test_fair_work_wage_arithmetic_reconciles(repo_root) -> None:
    result = _result(repo_root)
    audit = result.arithmetic_audit
    assert audit.finding.audit_status == "reconciled"
    assert audit.hourly_value == 24.95
    assert audit.actual_weekly_value == 948.10
    assert audit.expected_weekly_value == round(24.95 * 38, 2)


def test_fair_work_wage_arithmetic_mismatch_fails_closed(repo_root) -> None:
    manifest = _load_yaml(repo_root / "data" / "public_pilot" / "consistency_audit_manifest.yaml")
    pilot_report = _load_json(repo_root / "reports" / "public_data_pilot.json")
    mutated = copy.deepcopy(pilot_report)
    extracts = mutated["public_data_pilot"]["public_aggregate_extracts"]
    fair_work = next(item for item in extracts if item["extract_id"] == "fair_work_minimum_wage_2025_extract")
    weekly = next(value for value in fair_work["values"] if value["value_id"] == "national_minimum_wage_weekly")
    weekly["value"] = 948.00
    with pytest.raises(ValueError, match="fair_work_wage_arithmetic"):
        build_public_data_consistency_audit_result(
            manifest=manifest,
            public_pilot_report=mutated,
            public_data_evidence_map_report=_load_json(repo_root / "reports" / "public_data_evidence_map.json"),
            public_pilot_markdown=(repo_root / "reports" / "public_data_pilot.md").read_text(encoding="utf-8"),
            public_data_evidence_map_markdown=(repo_root / "reports" / "public_data_evidence_map.md").read_text(encoding="utf-8"),
            digest_payload=_load_json(repo_root / "data" / "public_pilot" / "digests" / "public_data_pilot_digests.json"),
            dashboard_path=repo_root / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py",
            dashboard_text=(repo_root / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py").read_text(encoding="utf-8"),
            repo_root=repo_root,
        )


def test_placeholders_modules_blockers_and_digests_preserve_boundaries(repo_root) -> None:
    result = _result(repo_root)
    assert result.placeholder_boundary_audit.finding.audit_status == "reconciled"
    assert result.module_calibration_boundary_audit.finding.audit_status == "reconciled"
    assert result.restricted_blocker_audit.finding.audit_status == "reconciled"
    assert result.forbidden_repo_data_audit.finding.audit_status == "reconciled"
    assert result.digest_consistency_audit.finding.audit_status == "reconciled"
    digest_paths = result.digest_consistency_audit.digest_paths
    assert "data/public_pilot/digests/public_data_pilot_digests.json" not in digest_paths


def test_consistency_audit_summary_false_flags(repo_root) -> None:
    summary = _result(repo_root).summary
    for flag in [
        "new_data_loaded",
        "external_source_verification_claimed",
        "real_calibration_completed",
        "actual_tax_payable_determined",
        "validation_claimed",
        "approval_claimed",
        "operational_readiness_claimed",
        "legal_sufficiency_claimed",
        "official_status_claimed",
        "firm_level_liability_logic_modified",
    ]:
        assert getattr(summary, flag) is False
