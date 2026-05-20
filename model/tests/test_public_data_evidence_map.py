from __future__ import annotations

import json

import yaml

from carsf.public_data_evidence_map import (
    CONFIDENCE_LABEL_VALUES,
    EVIDENCE_STATUS_VALUES,
    PUBLIC_DATA_EVIDENCE_MAP_WARNING,
    REVIEWER_INTERPRETATION_VALUES,
    build_public_data_evidence_map_result,
)


def load_manifest(repo_root):
    return yaml.safe_load((repo_root / "data" / "public_pilot" / "reviewer_evidence_map_manifest.yaml").read_text(encoding="utf-8"))


def load_pilot_report(repo_root):
    return json.loads((repo_root / "reports" / "public_data_pilot.json").read_text(encoding="utf-8"))


def build_result(repo_root):
    return build_public_data_evidence_map_result(load_manifest(repo_root), load_pilot_report(repo_root))


def test_evidence_map_manifest_parses_and_has_required_top_level_fields(repo_root) -> None:
    payload = load_manifest(repo_root)

    for field in [
        "evidence_map_id",
        "evidence_map_name",
        "status",
        "non_claims",
        "input_artifacts",
        "evidence_status_taxonomy",
        "reviewer_interpretation_taxonomy",
        "confidence_label_taxonomy",
        "reviewer_questions",
        "forbidden_claims",
        "build_29_requirements",
    ]:
        assert field in payload
    assert PUBLIC_DATA_EVIDENCE_MAP_WARNING in payload["non_claims"]


def test_evidence_map_taxonomies_contain_required_values(repo_root) -> None:
    payload = load_manifest(repo_root)

    assert set(payload["evidence_status_taxonomy"]) == EVIDENCE_STATUS_VALUES
    assert set(payload["reviewer_interpretation_taxonomy"]) == REVIEWER_INTERPRETATION_VALUES
    assert set(payload["confidence_label_taxonomy"]) == CONFIDENCE_LABEL_VALUES


def test_evidence_map_uses_build_27_artefacts_only(repo_root) -> None:
    payload = load_manifest(repo_root)

    assert "reports/public_data_pilot.json" in payload["input_artifacts"]
    assert all("public_data_evidence_map" not in item for item in payload["input_artifacts"])


def test_no_new_public_extracts_are_added_by_evidence_map(repo_root) -> None:
    result = build_result(repo_root)
    pilot = load_pilot_report(repo_root)["public_data_pilot"]

    mapped_extract_ids = {item.extract_id for item in result.loaded_extract_evidence + result.source_reference_only_evidence}
    pilot_extract_ids = {item["extract_id"] for item in pilot["public_aggregate_extracts"]}

    assert mapped_extract_ids == pilot_extract_ids
    assert result.summary.new_data_loaded is False


def test_source_reference_only_records_are_not_counted_as_loaded(repo_root) -> None:
    result = build_result(repo_root)

    assert result.source_reference_only_evidence
    assert all(item.evidence_status == "source_reference_only" for item in result.source_reference_only_evidence)
    assert result.summary.total_loaded_public_extract_evidence_items == 5
    assert result.summary.total_source_reference_only_evidence_items == 3


def test_loaded_public_extract_evidence_has_locator_and_review_status(repo_root) -> None:
    result = build_result(repo_root)

    assert result.loaded_extract_evidence
    for item in result.loaded_extract_evidence:
        assert item.source_locator
        assert item.source_value_note
        assert item.value_review_status


def test_required_extract_confidence_labels(repo_root) -> None:
    result = build_result(repo_root)
    by_id = {item.extract_id: item for item in result.loaded_extract_evidence}

    assert by_id["fair_work_minimum_wage_2025_extract"].confidence_label == "arithmetic_checked"
    treasury = by_id["treasury_budget_2026_27_receipts_extract"]
    assert treasury.confidence_label == "source_locator_recorded"
    treasury_text = f"{treasury.value_review_status} {treasury.source_value_note}".lower()
    assert "treasury validated" not in treasury_text
    assert "not treasury modelling" in treasury_text
    assert by_id["ato_corporate_transparency_2022_23_extract"].confidence_label == "source_locator_recorded"
    assert by_id["ato_taxation_statistics_2022_23_extract"].confidence_label == "source_locator_recorded"
    assert by_id["super_guarantee_2025_26_extract"].confidence_label == "source_locator_recorded"
    assert "guidance" not in by_id["super_guarantee_2025_26_extract"].source_value_note.lower()


def test_placeholders_modules_and_blockers_keep_boundaries(repo_root) -> None:
    result = build_result(repo_root)

    assert result.placeholder_evidence
    assert all(item.evidence_status == "realistic_placeholder_anchor" for item in result.placeholder_evidence)
    assert result.module_sanity_evidence
    assert all(item.calibration_possible is False for item in result.module_sanity_evidence)
    assert result.restricted_blocker_evidence
    assert all(item.evidence_status == "blocked_by_restricted_data" for item in result.restricted_blocker_evidence)
    assert result.forbidden_repo_data_evidence
    assert all(item.evidence_status == "forbidden_for_repo_use" for item in result.forbidden_repo_data_evidence)


def test_summary_flags_are_safe(repo_root) -> None:
    summary = build_result(repo_root).summary

    assert summary.evidence_map_created is True
    assert summary.new_data_loaded is False
    assert summary.real_public_data_loaded_from_build_27_only is True
    assert summary.source_references_mapped is True
    assert summary.loaded_public_extracts_mapped is True
    assert summary.source_reference_only_records_mapped is True
    assert summary.realistic_placeholders_mapped is True
    assert summary.restricted_blockers_mapped is True
    assert summary.real_calibration_completed is False
    assert summary.actual_tax_payable_determined is False
    assert summary.validation_claimed is False
    assert summary.approval_claimed is False
    assert summary.operational_readiness_claimed is False
    assert summary.legal_sufficiency_claimed is False
    assert summary.official_status_claimed is False
    assert summary.firm_level_liability_logic_modified is False
