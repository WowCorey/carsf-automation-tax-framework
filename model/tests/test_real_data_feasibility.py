from __future__ import annotations

import copy

import pytest
import yaml

from carsf.real_data_feasibility import (
    ACCESS_CLASS_VALUES,
    CLAIM_LEVEL_VALUES,
    DATA_STATUS_VALUES,
    build_calibration_intake_result,
    find_forbidden_affirmative_real_data_claims,
)


def load_payload(repo_root):
    path = repo_root / "data" / "calibration" / "real_data_feasibility_map.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_real_data_feasibility_manifest_parses_and_has_required_top_level_fields(repo_root) -> None:
    payload = load_payload(repo_root)

    for field in [
        "map_id",
        "map_name",
        "status",
        "non_claims",
        "data_status_taxonomy",
        "access_class_taxonomy",
        "claim_level_taxonomy",
        "source_candidates",
        "calibration_fields",
        "module_data_needs",
        "realistic_placeholders",
        "restricted_data_requirements",
        "forbidden_data_rules",
        "public_data_pilot_candidates",
        "external_review_routes",
        "forbidden_claims",
    ]:
        assert field in payload


def test_required_taxonomies_are_present(repo_root) -> None:
    result = build_calibration_intake_result(load_payload(repo_root), repo_root)

    assert set(result.data_status_taxonomy) == DATA_STATUS_VALUES
    assert set(result.access_class_taxonomy) == ACCESS_CLASS_VALUES
    assert set(result.claim_level_taxonomy) == CLAIM_LEVEL_VALUES


def test_source_candidates_use_valid_statuses_and_restricted_sources_cannot_be_committed(repo_root) -> None:
    result = build_calibration_intake_result(load_payload(repo_root), repo_root)

    for source in result.source_candidates:
        assert source.data_status in DATA_STATUS_VALUES
        assert source.access_class in ACCESS_CLASS_VALUES
        assert source.claim_level in CLAIM_LEVEL_VALUES
        if source.access_class in {
            "licence_required",
            "restricted_research_access",
            "government_internal_only",
            "confidential_or_prohibited",
        } or source.data_status in {"restricted_data_required", "forbidden_repo_data"}:
            assert source.can_be_committed_to_repo is False


def test_calibration_fields_have_source_mapping_and_must_not_claim(repo_root) -> None:
    result = build_calibration_intake_result(load_payload(repo_root), repo_root)
    source_ids = {source.source_id for source in result.source_candidates}

    for field in result.calibration_fields:
        assert field.candidate_sources
        assert set(field.candidate_sources) <= source_ids
        assert set(field.restricted_sources_needed) <= source_ids
        assert field.must_not_claim


def test_module_data_needs_have_blockers_and_must_not_claim(repo_root) -> None:
    result = build_calibration_intake_result(load_payload(repo_root), repo_root)

    for module in result.module_data_needs:
        assert module.main_blockers
        assert module.must_not_claim
        assert module.calibration_possible_now is False


def test_realistic_placeholders_are_labelled_and_not_real_or_calibrated(repo_root) -> None:
    result = build_calibration_intake_result(load_payload(repo_root), repo_root)

    assert result.realistic_placeholders
    for placeholder in result.realistic_placeholders:
        assert placeholder.data_status == "realistic_placeholder"
        assert placeholder.must_be_labelled_realistic_placeholder is True
        assert placeholder.must_not_be_labelled_real_data is True
        assert placeholder.must_not_be_labelled_calibrated is True


def test_forbidden_data_rules_block_repo_commits(repo_root) -> None:
    result = build_calibration_intake_result(load_payload(repo_root), repo_root)

    for rule in result.forbidden_data_rules:
        assert rule.must_not_commit_to_repo is True
        assert rule.must_not_use_in_tests is True


def test_public_data_pilot_candidates_do_not_claim_calibration(repo_root) -> None:
    result = build_calibration_intake_result(load_payload(repo_root), repo_root)

    for pilot in result.public_data_pilot_candidates:
        assert pilot.claim_level in {"sanity_check_only", "placeholder_anchor_only"}
        assert "calibration completed" in pilot.must_not_claim


def test_summary_false_flags_and_counts(repo_root) -> None:
    result = build_calibration_intake_result(load_payload(repo_root), repo_root)
    summary = result.summary

    assert summary.total_source_candidates >= 20
    assert summary.total_calibration_fields >= 30
    assert summary.total_forbidden_data_rules >= 17
    assert summary.total_public_data_pilot_candidates >= 8
    assert summary.real_data_loaded is False
    assert summary.real_calibration_completed is False
    assert summary.restricted_data_loaded is False
    assert summary.taxpayer_data_loaded is False
    assert summary.firm_level_confidential_data_loaded is False
    assert summary.household_microdata_loaded is False
    assert summary.realistic_placeholders_created is True
    assert summary.placeholders_labelled is True
    assert summary.validation_claimed is False
    assert summary.approval_claimed is False
    assert summary.operational_readiness_claimed is False
    assert summary.legal_sufficiency_claimed is False
    assert summary.official_status_claimed is False
    assert summary.firm_level_liability_logic_modified is False


def test_no_real_dataset_files_are_added(repo_root) -> None:
    dataset_suffixes = {".csv", ".parquet", ".feather", ".sqlite", ".db", ".xlsx", ".xls", ".jsonl"}
    dataset_files = [
        path
        for path in repo_root.rglob("*")
        if ".git" not in path.parts and path.is_file() and path.suffix.lower() in dataset_suffixes
    ]

    assert dataset_files == []


def test_invalid_source_status_fails_closed(repo_root) -> None:
    payload = load_payload(repo_root)
    broken = copy.deepcopy(payload)
    broken["source_candidates"][0]["data_status"] = "loaded_public_real_data_without_review"

    with pytest.raises(ValueError, match="invalid value"):
        build_calibration_intake_result(broken, repo_root)


def test_restricted_source_marked_committable_fails_closed(repo_root) -> None:
    payload = load_payload(repo_root)
    broken = copy.deepcopy(payload)
    for source in broken["source_candidates"]:
        if source["source_id"] == "ato_taxpayer_records":
            source["can_be_committed_to_repo"] = True
            break

    with pytest.raises(ValueError, match="cannot be committed"):
        build_calibration_intake_result(broken, repo_root)


def test_realistic_placeholder_without_labels_fails_closed(repo_root) -> None:
    payload = load_payload(repo_root)
    broken = copy.deepcopy(payload)
    broken["realistic_placeholders"][0]["must_not_be_labelled_calibrated"] = False

    with pytest.raises(ValueError, match="labelling safeguards"):
        build_calibration_intake_result(broken, repo_root)


def test_forbidden_claim_scanner_allows_negative_warnings() -> None:
    assert find_forbidden_affirmative_real_data_claims("This is not calibrated and no real data loaded.") == []
    assert find_forbidden_affirmative_real_data_claims("The forbidden_claims list includes calibrated.") == []
    assert "calibrated" in find_forbidden_affirmative_real_data_claims("The model is calibrated.")
    assert "real data loaded" in find_forbidden_affirmative_real_data_claims("Real data loaded for the model.")
