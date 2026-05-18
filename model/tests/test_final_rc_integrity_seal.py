from __future__ import annotations

import copy
import json

import yaml

from carsf.final_rc_integrity_seal import (
    SELF_GENERATED_DIGEST_EXCLUSIONS,
    build_digest_manifest,
    build_final_rc_integrity_seal_result,
    find_forbidden_affirmative_seal_claims,
)


def load_payload(repo_root):
    path = repo_root / "data" / "seal" / "v1_5_final_rc_integrity_seal.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_seal_manifest_parses_and_has_required_top_level_fields(repo_root) -> None:
    payload = load_payload(repo_root)

    for field in [
        "seal_id",
        "seal_name",
        "seal_status",
        "non_claims",
        "required_release_documents",
        "required_attack_pack_documents",
        "required_generated_reports",
        "required_manifests",
        "required_streamlit_pages",
        "required_docs",
        "required_scripts",
        "required_tests",
        "required_false_flags",
        "required_boundary_phrases",
        "forbidden_affirmative_claims",
        "guardrail_expectations",
        "ci_expectations",
        "digest_targets",
    ]:
        assert field in payload


def test_required_artefacts_exist_and_summary_flags_are_false(repo_root) -> None:
    result = build_final_rc_integrity_seal_result(load_payload(repo_root), repo_root)
    summary = result.summary

    assert summary.release_documents_missing == 0
    assert summary.attack_pack_documents_missing == 0
    assert summary.generated_reports_missing == 0
    assert summary.manifests_missing == 0
    assert summary.scripts_missing == 0
    assert summary.review_completed is False
    assert summary.approval_claimed is False
    assert summary.validation_claimed is False
    assert summary.readiness_score_created is False
    assert summary.maturity_score_created is False
    assert summary.operational_readiness_claimed is False
    assert summary.legal_sufficiency_claimed is False
    assert summary.legislative_readiness_claimed is False
    assert summary.economic_validation_claimed is False
    assert summary.welfare_validation_claimed is False
    assert summary.statistical_validation_claimed is False
    assert summary.official_status_claimed is False
    assert summary.official_review_pathway_claimed is False
    assert summary.real_data_used is False
    assert summary.actual_tax_payable_determined is False
    assert summary.compliance_scoring_created is False
    assert summary.enforcement_created is False
    assert summary.notices_created is False
    assert summary.penalties_created is False
    assert summary.operative_law_created is False
    assert summary.firm_level_liability_logic_modified is False


def test_seal_passed_only_when_required_checks_pass(repo_root) -> None:
    result = build_final_rc_integrity_seal_result(load_payload(repo_root), repo_root)

    assert result.summary.seal_passed is True
    assert result.summary.false_flag_failures == 0
    assert result.summary.boundary_phrase_failures == 0
    assert result.summary.forbidden_claim_findings == 0
    assert result.guardrail_status.denied_findings == 0


def test_missing_required_release_attack_or_report_fails_closed(repo_root) -> None:
    payload = load_payload(repo_root)

    missing_release = copy.deepcopy(payload)
    missing_release["required_release_documents"].append("release/v1_5_rc/MISSING_RELEASE_DOC.md")
    release_result = build_final_rc_integrity_seal_result(missing_release, repo_root)
    assert release_result.summary.seal_passed is False
    assert release_result.summary.release_documents_missing == 1

    missing_attack = copy.deepcopy(payload)
    missing_attack["required_attack_pack_documents"].append("release/v1_5_rc/attack_pack/MISSING_ATTACK_DOC.md")
    attack_result = build_final_rc_integrity_seal_result(missing_attack, repo_root)
    assert attack_result.summary.seal_passed is False
    assert attack_result.summary.attack_pack_documents_missing == 1

    missing_report = copy.deepcopy(payload)
    missing_report["required_generated_reports"].append("reports/missing_report.md")
    report_result = build_final_rc_integrity_seal_result(missing_report, repo_root)
    assert report_result.summary.seal_passed is False
    assert report_result.summary.generated_reports_missing == 1


def test_forbidden_affirmative_claim_scanner_allows_negative_warnings() -> None:
    assert find_forbidden_affirmative_seal_claims("This is not a readiness score.") == []
    assert find_forbidden_affirmative_seal_claims("It does not mean legal review complete.") == []
    assert "readiness score" in find_forbidden_affirmative_seal_claims("This creates a readiness score.")
    assert "review completed" in find_forbidden_affirmative_seal_claims("The review completed successfully.")


def test_digest_manifest_entries_include_sha256(repo_root) -> None:
    digests = build_digest_manifest(
        repo_root,
        [
            "release/v1_5_rc/*.json",
            "release/v1_5_rc/RELEASE_NOTES.md",
            "reports/executive_dashboard.json",
        ],
    )

    assert digests
    assert all(item.exists for item in digests)
    assert all(item.sha256 and len(item.sha256) == 64 for item in digests)
    assert all(item.byte_count and item.byte_count > 0 for item in digests)
    assert "release/v1_5_rc/FINAL_RC_DIGESTS.json" not in {item.artefact_path for item in digests}
    assert not (SELF_GENERATED_DIGEST_EXCLUSIONS & {item.artefact_path for item in digests})


def test_repo_guardrail_denied_findings_read_as_zero(repo_root) -> None:
    result = build_final_rc_integrity_seal_result(load_payload(repo_root), repo_root)

    assert result.guardrail_status.exists is True
    assert result.guardrail_status.readable is True
    assert result.guardrail_status.denied_findings == 0
    assert result.guardrail_status.status == "clean"


def test_release_manifest_includes_seal_documents_and_reports(repo_root) -> None:
    payload = json.loads((repo_root / "release" / "v1_5_rc" / "RELEASE_MANIFEST.json").read_text(encoding="utf-8"))

    for document in [
        "FINAL_RC_INTEGRITY_SEAL.md",
        "FINAL_RC_INTEGRITY_SEAL.json",
        "FINAL_RC_DIGESTS.json",
    ]:
        assert document in payload["release_documents"]
    for report in [
        "reports/v1_5_final_rc_integrity_seal.md",
        "reports/v1_5_final_rc_integrity_seal.json",
    ]:
        assert report in payload["generated_reports"]
