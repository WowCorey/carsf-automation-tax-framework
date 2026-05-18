from __future__ import annotations

import copy

import pytest
import yaml

from carsf.external_review_attack_pack import (
    REQUIRED_ATTACK_DOCUMENTS,
    REQUIRED_REVIEW_TRACKS,
    build_external_review_attack_pack_result,
    find_forbidden_affirmative_attack_pack_claims,
)
from carsf.release_candidate_pack import REQUIRED_LAYER_IDS, REQUIRED_REPORT_PATHS


def load_payload(repo_root):
    path = repo_root / "data" / "review" / "v1_5_external_review_attack_pack.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_attack_pack_manifest_parses_and_has_required_top_level_fields(repo_root) -> None:
    payload = load_payload(repo_root)

    for field in [
        "attack_pack_id",
        "attack_pack_name",
        "status",
        "non_claims",
        "review_tracks",
        "prototype_layers",
        "generated_reports",
        "attack_categories",
        "cross_cutting_attack_questions",
        "boundary_checks",
        "forbidden_claims",
    ]:
        assert field in payload


def test_attack_pack_contains_required_review_tracks(repo_root) -> None:
    result = build_external_review_attack_pack_result(load_payload(repo_root), repo_root)
    track_ids = {track.track_id for track in result.review_tracks}

    assert REQUIRED_REVIEW_TRACKS <= track_ids


def test_each_review_track_has_required_question_failure_input_and_warning_counts(repo_root) -> None:
    result = build_external_review_attack_pack_result(load_payload(repo_root), repo_root)

    for track in result.review_tracks:
        assert len(track.core_attack_questions) >= 10
        assert len(track.failure_modes) >= 5
        assert len(track.required_external_inputs) >= 5
        assert len(track.must_not_infer) >= 5


def test_every_attack_question_has_required_fields_and_not_validation_flag(repo_root) -> None:
    result = build_external_review_attack_pack_result(load_payload(repo_root), repo_root)

    for track in result.review_tracks:
        for question in track.core_attack_questions:
            assert question.question_id
            assert question.attack_category
            assert question.target_layers
            assert question.target_reports
            assert question.why_it_matters
            assert question.what_would_fail
            assert question.required_evidence_or_review
            assert question.severity_label
            assert question.must_not_be_treated_as_validation is True


def test_every_failure_mode_is_not_actual_error_finding(repo_root) -> None:
    result = build_external_review_attack_pack_result(load_payload(repo_root), repo_root)

    for track in result.review_tracks:
        for failure in track.failure_modes:
            assert failure.not_a_finding_of_actual_error is True


def test_referenced_layers_reports_and_documents_exist(repo_root) -> None:
    result = build_external_review_attack_pack_result(load_payload(repo_root), repo_root)

    assert REQUIRED_LAYER_IDS <= set(result.prototype_layers)
    assert REQUIRED_REPORT_PATHS <= set(result.generated_reports)
    assert REQUIRED_ATTACK_DOCUMENTS <= {document.document_path for document in result.release_documents}
    for report in result.generated_reports:
        assert (repo_root / report).exists()
    for document in result.release_documents:
        assert document.exists is True
        assert document.contains_non_claims is True
        assert (repo_root / document.document_path).exists()


def test_boundary_checks_fail_closed(repo_root) -> None:
    result = build_external_review_attack_pack_result(load_payload(repo_root), repo_root)

    assert len(result.boundary_checks) >= 18
    assert all(check.fail_closed_if_found is True for check in result.boundary_checks)


def test_report_and_layer_attack_matrices_cover_required_release_items(repo_root) -> None:
    result = build_external_review_attack_pack_result(load_payload(repo_root), repo_root)

    assert REQUIRED_REPORT_PATHS <= {row.report_path for row in result.report_attack_matrix}
    assert REQUIRED_LAYER_IDS <= {row.layer_id for row in result.layer_attack_matrix}


def test_attack_pack_summary_false_flags(repo_root) -> None:
    result = build_external_review_attack_pack_result(load_payload(repo_root), repo_root)
    summary = result.summary

    assert summary.review_completed is False
    assert summary.approval_claimed is False
    assert summary.validation_claimed is False
    assert summary.readiness_score_created is False
    assert summary.legal_sufficiency_claimed is False
    assert summary.operational_readiness_claimed is False
    assert summary.legislative_readiness_claimed is False
    assert summary.official_status_claimed is False
    assert summary.real_data_used is False
    assert summary.firm_level_liability_logic_modified is False


def test_attack_pack_fails_if_required_track_missing(repo_root) -> None:
    payload = load_payload(repo_root)
    broken = copy.deepcopy(payload)
    broken["review_tracks"] = [track for track in broken["review_tracks"] if track["track_id"] != "legal_review"]

    with pytest.raises(ValueError, match="missing required review tracks"):
        build_external_review_attack_pack_result(broken, repo_root)


def test_attack_pack_fails_if_track_has_too_few_questions(repo_root) -> None:
    payload = load_payload(repo_root)
    broken = copy.deepcopy(payload)
    broken["review_tracks"][0]["core_attack_questions"] = broken["review_tracks"][0]["core_attack_questions"][:9]

    with pytest.raises(ValueError, match="fewer than 10 attack questions"):
        build_external_review_attack_pack_result(broken, repo_root)


def test_attack_pack_fails_if_unknown_layer_or_report_referenced(repo_root) -> None:
    payload = load_payload(repo_root)
    broken_layer = copy.deepcopy(payload)
    broken_layer["review_tracks"][0]["relevant_layers"].append("missing_layer")

    with pytest.raises(ValueError, match="unknown layers"):
        build_external_review_attack_pack_result(broken_layer, repo_root)

    broken_report = copy.deepcopy(payload)
    broken_report["review_tracks"][0]["relevant_reports"].append("reports/missing.md")

    with pytest.raises(ValueError, match="unknown reports"):
        build_external_review_attack_pack_result(broken_report, repo_root)


def test_attack_pack_fails_if_question_or_failure_can_be_treated_as_validation(repo_root) -> None:
    payload = load_payload(repo_root)
    broken_question = copy.deepcopy(payload)
    broken_question["review_tracks"][0]["core_attack_questions"][0]["must_not_be_treated_as_validation"] = False

    with pytest.raises(ValueError, match="can be treated as validation"):
        build_external_review_attack_pack_result(broken_question, repo_root)

    broken_failure = copy.deepcopy(payload)
    broken_failure["review_tracks"][0]["failure_modes"][0]["not_a_finding_of_actual_error"] = False

    with pytest.raises(ValueError, match="actual finding"):
        build_external_review_attack_pack_result(broken_failure, repo_root)


def test_attack_pack_forbidden_claim_scanner_allows_negative_and_boundary_context() -> None:
    assert find_forbidden_affirmative_attack_pack_claims("This is not a readiness score.") == []
    assert find_forbidden_affirmative_attack_pack_claims("Boundary check: does any output imply official status?") == []
    assert "readiness score" in find_forbidden_affirmative_attack_pack_claims("This creates a readiness score.")
    assert "externally validated" in find_forbidden_affirmative_attack_pack_claims("The package is externally validated.")
