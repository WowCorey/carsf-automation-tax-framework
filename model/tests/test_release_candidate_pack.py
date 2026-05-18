from __future__ import annotations

import copy

import pytest
import yaml

from carsf.release_candidate_pack import (
    REQUIRED_LAYER_IDS,
    REQUIRED_REPORT_PATHS,
    REQUIRED_RELEASE_DOCUMENTS,
    build_release_candidate_pack_result,
    find_forbidden_affirmative_release_claims,
)


def load_payload(repo_root):
    path = repo_root / "data" / "release" / "v1_5_release_manifest.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_release_manifest_parses_and_has_required_top_level_fields(repo_root) -> None:
    payload = load_payload(repo_root)

    for field in [
        "release_id",
        "release_name",
        "release_status",
        "release_date_placeholder",
        "non_claims",
        "source_documents",
        "prototype_layers",
        "generated_reports",
        "streamlit_pages",
        "reviewer_routes",
        "release_documents",
        "forbidden_claims",
    ]:
        assert field in payload


def test_release_candidate_pack_contains_required_layers(repo_root) -> None:
    result = build_release_candidate_pack_result(load_payload(repo_root), repo_root)
    layer_ids = {layer.layer_id for layer in result.prototype_layers}

    assert REQUIRED_LAYER_IDS <= layer_ids


def test_release_candidate_pack_required_reports_and_documents_exist(repo_root) -> None:
    result = build_release_candidate_pack_result(load_payload(repo_root), repo_root)
    reports_by_path = {report.report_path: report for report in result.generated_reports}
    docs_by_path = {document.document_path: document for document in result.release_documents}

    assert REQUIRED_REPORT_PATHS <= set(reports_by_path)
    assert REQUIRED_RELEASE_DOCUMENTS <= set(docs_by_path)
    for path in REQUIRED_REPORT_PATHS:
        assert reports_by_path[path].exists is True
        assert (repo_root / path).exists()
    for path in REQUIRED_RELEASE_DOCUMENTS:
        assert docs_by_path[path].exists is True
        assert (repo_root / path).exists()


def test_release_candidate_pack_references_paper_files_and_working_paper_layers(repo_root) -> None:
    result = build_release_candidate_pack_result(load_payload(repo_root), repo_root)

    for path in result.source_documents:
        assert (repo_root / path).exists()
    assert result.summary.working_paper_updated is True


def test_every_release_layer_has_non_claims_use_limits_and_reviewer_routing(repo_root) -> None:
    result = build_release_candidate_pack_result(load_payload(repo_root), repo_root)

    for layer in result.prototype_layers:
        assert layer.non_claim_flags
        assert layer.must_not_be_used_for
        assert layer.recommended_reviewer


def test_release_candidate_pack_summary_false_flags(repo_root) -> None:
    result = build_release_candidate_pack_result(load_payload(repo_root), repo_root)
    summary = result.summary

    assert summary.real_data_used is False
    assert summary.readiness_score_created is False
    assert summary.operational_readiness_claimed is False
    assert summary.legal_sufficiency_claimed is False
    assert summary.legislative_readiness_claimed is False
    assert summary.economic_validation_claimed is False
    assert summary.welfare_validation_claimed is False
    assert summary.statistical_validation_claimed is False
    assert summary.official_status_claimed is False
    assert summary.firm_level_liability_logic_modified is False
    assert summary.reports_missing == 0
    assert summary.release_documents_missing == 0


def test_release_candidate_pack_fails_if_required_layer_missing(repo_root) -> None:
    payload = load_payload(repo_root)
    broken = copy.deepcopy(payload)
    broken["prototype_layers"] = [
        layer for layer in broken["prototype_layers"] if layer["layer_id"] != "legislative_architecture"
    ]

    with pytest.raises(ValueError, match="missing required layers"):
        build_release_candidate_pack_result(broken, repo_root)


def test_release_candidate_pack_fails_if_required_report_missing_from_manifest(repo_root) -> None:
    payload = load_payload(repo_root)
    broken = copy.deepcopy(payload)
    broken["generated_reports"] = [
        report for report in broken["generated_reports"] if report["report_path"] != "reports/executive_dashboard.md"
    ]

    with pytest.raises(ValueError, match="missing required reports"):
        build_release_candidate_pack_result(broken, repo_root)


def test_release_candidate_pack_fails_if_layer_omits_non_claim_flags(repo_root) -> None:
    payload = load_payload(repo_root)
    broken = copy.deepcopy(payload)
    broken["prototype_layers"][0]["non_claim_flags"] = []

    with pytest.raises(ValueError, match="non-claim flags"):
        build_release_candidate_pack_result(broken, repo_root)


def test_release_candidate_forbidden_claim_scanner_allows_negative_warnings() -> None:
    assert find_forbidden_affirmative_release_claims(
        "This is not a readiness score and is not legally sufficient."
    ) == []
    assert "readiness score" in find_forbidden_affirmative_release_claims("This creates a readiness score.")
    assert "operationally ready" in find_forbidden_affirmative_release_claims("The pack is operationally ready.")
