from __future__ import annotations

import json

import yaml

from carsf.source_locator_verification_pack import (
    LOCATOR_STATUS_VALUES,
    REVIEWER_WARNING_VALUES,
    VERIFICATION_STATUS_VALUES,
    build_source_locator_verification_result,
)


def _load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_source_locator_verification_manifest_parses_and_contains_required_taxonomies(repo_root) -> None:
    manifest = _load_yaml(repo_root / "data" / "public_pilot" / "source_locator_verification_manifest.yaml")

    for key in [
        "pack_id",
        "pack_name",
        "status",
        "non_claims",
        "input_artifacts",
        "locator_status_taxonomy",
        "verification_status_taxonomy",
        "reviewer_warning_taxonomy",
        "required_loaded_value_cards",
        "required_source_reference_only_cards",
        "required_placeholder_anchor_cards",
        "required_restricted_blocker_cards",
        "required_reviewer_checklists",
        "forbidden_claims",
    ]:
        assert key in manifest

    assert set(manifest["locator_status_taxonomy"]) == LOCATOR_STATUS_VALUES
    assert set(manifest["verification_status_taxonomy"]) == VERIFICATION_STATUS_VALUES
    assert set(manifest["reviewer_warning_taxonomy"]) == REVIEWER_WARNING_VALUES


def test_source_locator_cards_are_built_from_existing_public_pilot_extracts_only(repo_root) -> None:
    manifest = _load_yaml(repo_root / "data" / "public_pilot" / "source_locator_verification_manifest.yaml")
    pilot_report = _load_json(repo_root / "reports" / "public_data_pilot.json")
    evidence_report = _load_json(repo_root / "reports" / "public_data_evidence_map.json")
    audit_report = _load_json(repo_root / "reports" / "public_data_consistency_audit.json")

    result = build_source_locator_verification_result(manifest, pilot_report, evidence_report, audit_report)
    extracts = pilot_report["public_data_pilot"]["public_aggregate_extracts"]
    loaded_extract_ids = {item["extract_id"] for item in extracts if item["data_status"] == "real_public_data_loaded"}
    source_only_extract_ids = {item["extract_id"] for item in extracts if item["data_status"] == "source_reference_only"}

    assert {card.extract_id for card in result.loaded_value_cards} == loaded_extract_ids
    assert {card.extract_id for card in result.source_reference_only_cards} == source_only_extract_ids
    assert result.summary.new_data_loaded is False
    assert result.summary.external_source_verification_claimed is False
    assert result.summary.manual_review_pack_only is True


def test_loaded_value_cards_have_locator_metadata_and_checklists(repo_root) -> None:
    manifest = _load_yaml(repo_root / "data" / "public_pilot" / "source_locator_verification_manifest.yaml")
    result = build_source_locator_verification_result(
        manifest,
        _load_json(repo_root / "reports" / "public_data_pilot.json"),
        _load_json(repo_root / "reports" / "public_data_evidence_map.json"),
        _load_json(repo_root / "reports" / "public_data_consistency_audit.json"),
    )

    for card in result.loaded_value_cards:
        assert card.source_url
        assert card.source_locator
        assert card.source_value_note
        assert card.value_review_status
        assert card.reviewer_checklist
        assert card.reviewer_must_not_infer
        assert card.locator_status in {"complete_locator", "partial_locator"}

    fair_work = next(card for card in result.loaded_value_cards if card.extract_id == "fair_work_minimum_wage_2025_extract")
    assert "24.95 * 38 = 948.10" in fair_work.arithmetic_check_summary


def test_source_reference_placeholder_and_blocker_cards_preserve_boundaries(repo_root) -> None:
    manifest = _load_yaml(repo_root / "data" / "public_pilot" / "source_locator_verification_manifest.yaml")
    result = build_source_locator_verification_result(
        manifest,
        _load_json(repo_root / "reports" / "public_data_pilot.json"),
        _load_json(repo_root / "reports" / "public_data_evidence_map.json"),
        _load_json(repo_root / "reports" / "public_data_consistency_audit.json"),
    )

    assert all(card.verification_status == "source_reference_only_not_loaded" for card in result.source_reference_only_cards)
    assert all(card.locator_status == "source_reference_only" for card in result.source_reference_only_cards)
    assert all(card.verification_status == "placeholder_not_real_data" for card in result.placeholder_anchor_cards)
    assert all(card.locator_status == "placeholder_anchor_only" for card in result.placeholder_anchor_cards)
    assert all(card.locator_status in {"blocked_by_restricted_data", "forbidden_for_repo_use"} for card in result.restricted_blocker_cards)
    assert result.summary.real_calibration_completed is False
    assert result.summary.actual_tax_payable_determined is False
    assert result.summary.validation_claimed is False
    assert result.summary.approval_claimed is False
    assert result.summary.operational_readiness_claimed is False
    assert result.summary.legal_sufficiency_claimed is False
    assert result.summary.official_status_claimed is False
    assert result.summary.firm_level_liability_logic_modified is False
