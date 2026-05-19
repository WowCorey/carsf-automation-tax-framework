from __future__ import annotations

import copy
import json

import pytest
import yaml

from carsf.public_data_pilot import (
    CLAIM_LEVEL_VALUES,
    DATA_STATUS_VALUES,
    PUBLIC_PILOT_DATASET_EXTENSIONS,
    build_public_data_pilot_result,
    find_forbidden_affirmative_public_data_claims,
)


def load_manifest(repo_root):
    path = repo_root / "data" / "public_pilot" / "public_data_pilot_manifest.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_extracts(repo_root):
    path = repo_root / "data" / "public_pilot" / "extracts" / "public_aggregate_extracts.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def load_anchors(repo_root):
    path = repo_root / "data" / "public_pilot" / "placeholders" / "realistic_placeholder_anchors.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def build_result(repo_root):
    return build_public_data_pilot_result(
        load_manifest(repo_root),
        load_extracts(repo_root),
        load_anchors(repo_root),
        repo_root,
        digest_targets_total=5,
        digests_written=5,
    )


def test_public_data_pilot_manifest_parses_and_has_required_top_level_fields(repo_root) -> None:
    payload = load_manifest(repo_root)

    for field in [
        "pilot_id",
        "pilot_name",
        "status",
        "non_claims",
        "source_references",
        "public_aggregate_extracts",
        "placeholder_anchors",
        "field_sanity_checks",
        "module_sanity_checks",
        "restricted_data_blockers",
        "forbidden_data_rules",
        "build_27_flags",
        "future_build_28_requirements",
        "forbidden_claims",
    ]:
        assert field in payload


def test_source_references_have_required_public_source_metadata(repo_root) -> None:
    result = build_result(repo_root)

    assert result.source_references
    for source in result.source_references:
        assert source.publisher
        assert source.source_url.startswith("https://")
        assert source.source_kind
        assert source.access_class
        assert source.claim_level in CLAIM_LEVEL_VALUES
        assert source.must_not_claim
        assert source.raw_dataset_committed is False


def test_public_aggregate_extracts_have_status_source_and_commit_safety(repo_root) -> None:
    result = build_result(repo_root)

    assert result.public_aggregate_extracts
    for extract in result.public_aggregate_extracts:
        assert extract.source_reference_id
        assert extract.data_status in DATA_STATUS_VALUES
        assert extract.claim_level in CLAIM_LEVEL_VALUES
        assert extract.source_url.startswith("https://")
        assert extract.must_not_claim
        assert extract.safe_to_commit is True
        if extract.data_status == "real_public_data_loaded":
            assert extract.source_note
            assert extract.licence_notes
            assert extract.safe_to_commit is True


def test_source_reference_only_extracts_do_not_count_as_loaded_public_data(repo_root) -> None:
    result = build_result(repo_root)
    source_reference_only = [
        item for item in result.public_aggregate_extracts if item.data_status == "source_reference_only"
    ]

    assert source_reference_only
    assert result.summary.source_reference_only_extracts == len(source_reference_only)
    assert result.summary.real_public_data_loaded_extracts == sum(
        item.data_status == "real_public_data_loaded" for item in result.public_aggregate_extracts
    )
    assert result.summary.real_public_data_loaded_extracts < result.summary.total_public_aggregate_extracts


def test_realistic_placeholder_anchors_remain_placeholders(repo_root) -> None:
    result = build_result(repo_root)

    assert result.placeholder_anchors
    for anchor in result.placeholder_anchors:
        assert anchor.current_placeholder_status == "realistic_placeholder"
        assert anchor.must_be_labelled_realistic_placeholder is True
        assert anchor.must_not_be_labelled_real_data is True
        assert anchor.must_not_be_labelled_calibrated is True
        assert anchor.review_required_before_calibration
        assert anchor.must_not_claim


def test_module_sanity_checks_keep_calibration_false(repo_root) -> None:
    result = build_result(repo_root)

    assert result.module_sanity_checks
    for module in result.module_sanity_checks:
        assert module.calibration_possible is False
        assert module.claim_level in CLAIM_LEVEL_VALUES
        assert module.main_blockers
        assert module.must_not_claim


def test_restricted_and_forbidden_data_are_not_loaded(repo_root) -> None:
    result = build_result(repo_root)

    assert result.summary.restricted_data_loaded is False
    assert result.summary.taxpayer_data_loaded is False
    assert result.summary.firm_level_confidential_data_loaded is False
    assert result.summary.household_microdata_loaded is False
    assert result.summary.restricted_data_findings == 0
    for rule in result.forbidden_data_rules:
        assert rule["must_not_commit_to_repo"] is True
        assert rule["must_not_use_in_tests"] is True


def test_no_forbidden_dataset_files_exist_outside_public_pilot_whitelist(repo_root) -> None:
    dataset_suffixes = {".csv", ".parquet", ".feather", ".sqlite", ".db", ".xlsx", ".xls", ".jsonl"}
    dataset_files = [
        path
        for path in repo_root.rglob("*")
        if ".git" not in path.parts and path.is_file() and path.suffix.lower() in dataset_suffixes
    ]
    public_pilot_dataset_files = [
        path
        for path in dataset_files
        if "data" in path.parts and "public_pilot" in path.parts and path.suffix.lower() in PUBLIC_PILOT_DATASET_EXTENSIONS
    ]

    assert dataset_files == public_pilot_dataset_files
    assert public_pilot_dataset_files == []


def test_no_forbidden_data_markers_in_public_pilot_directories(repo_root) -> None:
    public_root = repo_root / "data" / "public_pilot"
    combined = "\n".join(path.read_text(encoding="utf-8") for path in public_root.rglob("*") if path.is_file())
    forbidden_markers = [
        "tax_file_number",
        "taxpayer_id",
        "person_name",
        "home_address",
        "bank_account_number",
        "raw_bank_record",
        "payslip_number",
        "employee_record_id",
        "household_microdata_row",
        "datalab_microdata",
        "hilda_microdata",
        "services_australia_customer_id",
        "ato_taxpayer_record_id",
        "confidential_treasury_document",
        "confidential_pbo_document",
        "restricted_government_record",
        "raw bank record",
        "TFN",
    ]

    for marker in forbidden_markers:
        assert marker not in combined


def test_summary_flags_are_build_27_safe(repo_root) -> None:
    result = build_result(repo_root)
    summary = result.summary

    assert summary.public_data_pilot_created is True
    assert summary.source_references_created is True
    assert summary.realistic_placeholders_anchored is True
    assert summary.real_public_data_loaded is True
    assert summary.real_calibration_completed is False
    assert summary.restricted_data_loaded is False
    assert summary.taxpayer_data_loaded is False
    assert summary.firm_level_confidential_data_loaded is False
    assert summary.household_microdata_loaded is False
    assert summary.actual_tax_payable_determined is False
    assert summary.validation_claimed is False
    assert summary.approval_claimed is False
    assert summary.operational_readiness_claimed is False
    assert summary.legal_sufficiency_claimed is False
    assert summary.official_status_claimed is False
    assert summary.firm_level_liability_logic_modified is False


def test_digest_manifest_does_not_hash_itself(repo_root) -> None:
    digest_path = repo_root / "data" / "public_pilot" / "digests" / "public_data_pilot_digests.json"
    payload = json.loads(digest_path.read_text(encoding="utf-8"))
    paths = {item["path"] for item in payload["digests"]}

    assert "data/public_pilot/digests/public_data_pilot_digests.json" not in paths
    assert payload["metadata"]["digest_file_hashes_itself"] is False
    assert all(item["sha256"] for item in payload["digests"])


def test_invalid_loaded_public_extract_without_source_url_fails_closed(repo_root) -> None:
    manifest = load_manifest(repo_root)
    extracts = copy.deepcopy(load_extracts(repo_root))
    anchors = load_anchors(repo_root)
    extracts[0]["source_url"] = ""

    with pytest.raises(ValueError, match="source_url"):
        build_public_data_pilot_result(manifest, extracts, anchors, repo_root, 5, 5)


def test_loaded_public_extract_without_commit_safety_fails_closed(repo_root) -> None:
    manifest = load_manifest(repo_root)
    extracts = copy.deepcopy(load_extracts(repo_root))
    anchors = load_anchors(repo_root)
    extracts[0]["safe_to_commit"] = False

    with pytest.raises(ValueError, match="safe_to_commit"):
        build_public_data_pilot_result(manifest, extracts, anchors, repo_root, 5, 5)


def test_placeholder_labelled_as_calibrated_fails_closed(repo_root) -> None:
    manifest = load_manifest(repo_root)
    extracts = load_extracts(repo_root)
    anchors = copy.deepcopy(load_anchors(repo_root))
    anchors[0]["must_not_be_labelled_calibrated"] = False

    with pytest.raises(ValueError, match="calibrated"):
        build_public_data_pilot_result(manifest, extracts, anchors, repo_root, 5, 5)


def test_module_calibration_possible_fails_closed(repo_root) -> None:
    manifest = copy.deepcopy(load_manifest(repo_root))
    extracts = load_extracts(repo_root)
    anchors = load_anchors(repo_root)
    manifest["module_sanity_checks"][0]["calibration_possible"] = True

    with pytest.raises(ValueError, match="calibration_possible"):
        build_public_data_pilot_result(manifest, extracts, anchors, repo_root, 5, 5)


def test_forbidden_claim_scanner_allows_negative_warnings() -> None:
    assert find_forbidden_affirmative_public_data_claims("This is not calibrated.") == []
    assert find_forbidden_affirmative_public_data_claims("Calibration has not been completed.") == []
    assert find_forbidden_affirmative_public_data_claims("Public data does not prove the model works.") == []
    assert find_forbidden_affirmative_public_data_claims("forbidden_claims: [calibrated]") == []
    assert "calibrated" in find_forbidden_affirmative_public_data_claims("The model is calibrated.")
