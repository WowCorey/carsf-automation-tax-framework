from __future__ import annotations

import json

import yaml

from carsf.red_team_reviewer_objections import (
    OBJECTION_CATEGORY_VALUES,
    OBJECTION_STATUS_VALUES,
    SEVERITY_VALUES,
    build_red_team_reviewer_objections_result,
)


def _load_yaml(path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def _load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def _input_reports(repo_root):
    return {
        "real_data_feasibility": _load_json(repo_root / "reports" / "real_data_feasibility.json"),
        "public_data_pilot": _load_json(repo_root / "reports" / "public_data_pilot.json"),
        "public_data_evidence_map": _load_json(repo_root / "reports" / "public_data_evidence_map.json"),
        "public_data_consistency_audit": _load_json(repo_root / "reports" / "public_data_consistency_audit.json"),
        "source_locator_verification_pack": _load_json(repo_root / "reports" / "source_locator_verification_pack.json"),
    }


def test_red_team_objections_manifest_parses_and_contains_required_taxonomies(repo_root) -> None:
    manifest = _load_yaml(repo_root / "data" / "public_pilot" / "red_team_reviewer_objections_manifest.yaml")

    for key in [
        "pack_id",
        "pack_name",
        "status",
        "non_claims",
        "input_artifacts",
        "objection_status_taxonomy",
        "severity_taxonomy",
        "objection_category_taxonomy",
        "required_objection_categories",
        "minimum_objections_per_category",
        "required_objections",
        "forbidden_claims",
        "build_30_requirements",
    ]:
        assert key in manifest

    assert set(manifest["objection_status_taxonomy"]) == OBJECTION_STATUS_VALUES
    assert set(manifest["severity_taxonomy"]) == SEVERITY_VALUES
    assert set(manifest["objection_category_taxonomy"]) == OBJECTION_CATEGORY_VALUES


def test_red_team_objection_catalogue_covers_required_categories(repo_root) -> None:
    manifest = _load_yaml(repo_root / "data" / "public_pilot" / "red_team_reviewer_objections_manifest.yaml")
    result = build_red_team_reviewer_objections_result(manifest, _input_reports(repo_root))
    categories = {item.objection_category for item in result.objections}

    assert len(result.objections) >= 30
    assert set(manifest["required_objection_categories"]) <= categories
    assert result.summary.categories_covered == len(OBJECTION_CATEGORY_VALUES)
    assert "public_data_limitations" in categories
    assert "placeholder_limitations" in categories
    assert "restricted_data_blockers" in categories
    assert "calibration_limitations" in categories
    assert "statistical_limitations" in categories
    assert "legal_and_tax_limitations" in categories
    assert "administrative_feasibility_limitations" in categories
    assert "economic_incidence_limitations" in categories
    assert "dashboard_interpretation_risk" in categories
    assert "reviewer_misinterpretation_risk" in categories


def test_every_red_team_objection_has_required_fields_and_no_resolved_status(repo_root) -> None:
    manifest = _load_yaml(repo_root / "data" / "public_pilot" / "red_team_reviewer_objections_manifest.yaml")
    result = build_red_team_reviewer_objections_result(manifest, _input_reports(repo_root))

    for objection in result.objections:
        assert objection.objection_id
        assert objection.objection_title
        assert objection.objection_category in OBJECTION_CATEGORY_VALUES
        assert objection.severity in SEVERITY_VALUES
        assert objection.affected_artifacts
        assert objection.reviewer_concern
        assert objection.why_the_concern_is_valid
        assert objection.current_project_response
        assert objection.what_the_project_can_say
        assert objection.what_the_project_must_not_claim
        assert objection.unresolved_blockers
        assert objection.evidence_needed_to_resolve
        assert objection.future_build_route
        assert objection.status in OBJECTION_STATUS_VALUES
        assert objection.status != "resolved"
        combined = " ".join(
            [
                objection.objection_title,
                objection.reviewer_concern,
                objection.current_project_response,
                " ".join(objection.what_the_project_can_say),
            ]
        ).lower()
        assert "all issues are resolved" not in combined


def test_red_team_summary_flags_preserve_non_claim_boundaries(repo_root) -> None:
    manifest = _load_yaml(repo_root / "data" / "public_pilot" / "red_team_reviewer_objections_manifest.yaml")
    result = build_red_team_reviewer_objections_result(manifest, _input_reports(repo_root))
    summary = result.summary

    assert summary.red_team_pack_created is True
    assert summary.new_data_loaded is False
    assert summary.external_source_verification_claimed is False
    assert summary.objections_acknowledged is True
    assert summary.unresolved_blockers_visible is True
    assert summary.calibration_limitations_visible is True
    assert summary.legal_limitations_visible is True
    assert summary.statistical_limitations_visible is True
    assert summary.dashboard_misinterpretation_risks_visible is True
    assert summary.real_calibration_completed is False
    assert summary.actual_tax_payable_determined is False
    assert summary.validation_claimed is False
    assert summary.approval_claimed is False
    assert summary.operational_readiness_claimed is False
    assert summary.legal_sufficiency_claimed is False
    assert summary.official_status_claimed is False
    assert summary.firm_level_liability_logic_modified is False
