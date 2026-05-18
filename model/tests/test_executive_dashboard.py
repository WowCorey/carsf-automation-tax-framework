from __future__ import annotations

import copy

import pytest
import yaml

from carsf.executive_dashboard import (
    REQUIRED_LAYER_IDS,
    REQUIRED_REPORT_PATHS,
    build_executive_dashboard_result,
    find_forbidden_affirmative_dashboard_claims,
)


def load_payload(repo_root):
    path = repo_root / "data" / "dashboard" / "executive_dashboard_manifest.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_executive_dashboard_manifest_parses_and_has_required_top_level_fields(repo_root) -> None:
    payload = load_payload(repo_root)

    for field in [
        "dashboard_id",
        "dashboard_name",
        "status",
        "non_claims",
        "layers",
        "report_entries",
        "forbidden_claims",
    ]:
        assert field in payload


def test_executive_dashboard_contains_required_layers(repo_root) -> None:
    result = build_executive_dashboard_result(load_payload(repo_root), repo_root)
    layer_ids = {layer.layer_id for layer in result.layers}

    assert REQUIRED_LAYER_IDS <= layer_ids


def test_every_layer_has_non_claims_use_limits_reviewer_and_read_order(repo_root) -> None:
    result = build_executive_dashboard_result(load_payload(repo_root), repo_root)

    for layer in result.layers:
        assert layer.non_claim_flags
        assert layer.must_not_be_used_for
        assert layer.recommended_reviewer
        assert isinstance(layer.read_order, int)


def test_every_required_report_entry_references_existing_generated_report(repo_root) -> None:
    result = build_executive_dashboard_result(load_payload(repo_root), repo_root)
    entries_by_path = {entry.report_path: entry for entry in result.report_entries}

    assert REQUIRED_REPORT_PATHS <= set(entries_by_path)
    for path in REQUIRED_REPORT_PATHS:
        assert entries_by_path[path].exists is True
        assert (repo_root / path).exists()


def test_every_listed_streamlit_page_exists(repo_root) -> None:
    result = build_executive_dashboard_result(load_payload(repo_root), repo_root)

    for layer in result.layers:
        for page in layer.streamlit_pages:
            assert (repo_root / page).exists()


def test_suggested_review_navigation_is_not_official_process(repo_root) -> None:
    result = build_executive_dashboard_result(load_payload(repo_root), repo_root)

    assert result.suggested_review_navigation
    assert all(item.official_process is False for item in result.suggested_review_navigation)


def test_executive_dashboard_summary_false_flags(repo_root) -> None:
    result = build_executive_dashboard_result(load_payload(repo_root), repo_root)
    summary = result.summary

    assert summary.real_data_used is False
    assert summary.readiness_score_created is False
    assert summary.operational_readiness_claimed is False
    assert summary.legal_sufficiency_claimed is False
    assert summary.economic_validation_claimed is False
    assert summary.firm_level_liability_logic_modified is False
    assert summary.reports_missing == 0


def test_executive_dashboard_does_not_create_readiness_or_maturity_score(repo_root) -> None:
    result = build_executive_dashboard_result(load_payload(repo_root), repo_root)
    payload = result.to_jsonable()

    assert payload["summary"]["readiness_score_created"] is False
    assert "maturity_score_created" not in payload["summary"]
    assert all("maturity_score" not in layer.status_labels for layer in result.layers)


def test_executive_dashboard_fails_if_required_layer_missing(repo_root) -> None:
    payload = load_payload(repo_root)
    broken = copy.deepcopy(payload)
    broken["layers"] = [layer for layer in broken["layers"] if layer["layer_id"] != "legislative_architecture"]

    with pytest.raises(ValueError, match="missing required layers"):
        build_executive_dashboard_result(broken, repo_root)


def test_executive_dashboard_fails_if_required_report_missing_from_index(repo_root) -> None:
    payload = load_payload(repo_root)
    broken = copy.deepcopy(payload)
    broken["report_entries"] = [
        entry for entry in broken["report_entries"] if entry["report_path"] != "reports/legislative_architecture.md"
    ]

    with pytest.raises(ValueError, match="missing required generated reports"):
        build_executive_dashboard_result(broken, repo_root)


def test_executive_dashboard_fails_if_layer_omits_non_claim_flags(repo_root) -> None:
    payload = load_payload(repo_root)
    broken = copy.deepcopy(payload)
    broken["layers"][0]["non_claim_flags"] = []

    with pytest.raises(ValueError, match="non-claim flags"):
        build_executive_dashboard_result(broken, repo_root)


def test_executive_dashboard_forbidden_claim_scanner_allows_negative_warnings() -> None:
    assert find_forbidden_affirmative_dashboard_claims("This is not a readiness score and not legally sufficient.") == []
    assert "readiness score" in find_forbidden_affirmative_dashboard_claims("This creates a readiness score.")
    assert "operationally ready" in find_forbidden_affirmative_dashboard_claims("The prototype is operationally ready.")
