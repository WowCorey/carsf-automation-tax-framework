from __future__ import annotations

import json
import runpy


def test_full_repo_integrity_report_exists_in_repo(repo_root) -> None:
    assert (repo_root / "reports" / "full_repo_integrity_upgrade_audit.md").exists()
    assert (repo_root / "reports" / "full_repo_integrity_upgrade_audit.json").exists()


def test_full_repo_integrity_json_contains_coverage_matrices(repo_root) -> None:
    payload = json.loads((repo_root / "reports" / "full_repo_integrity_upgrade_audit.json").read_text(encoding="utf-8"))
    audit = payload["full_repo_integrity_upgrade_audit"]

    assert audit["runner_coverage_matrix"]
    assert audit["report_coverage_matrix"]
    assert audit["dashboard_coverage_matrix"]
    assert audit["release_manifest_coverage"]
    assert audit["docs_coverage"]
    assert audit["result_coverage_matrix"]
    assert audit["public_data_boundary_audit"]
    assert audit["placeholder_boundary_audit"]
    assert audit["calibration_boundary_audit"]
    assert audit["scenario_constraint_audit"]
    assert audit["guardrail_audit"]
    assert audit["non_claim_boundary_audit"]


def test_full_repo_integrity_json_contains_gap_registers(repo_root) -> None:
    payload = json.loads((repo_root / "reports" / "full_repo_integrity_upgrade_audit.json").read_text(encoding="utf-8"))
    audit = payload["full_repo_integrity_upgrade_audit"]

    assert audit["safe_fixes"]
    assert audit["findings"]
    assert audit["gaps"]
    assert audit["missing_factors"]
    assert audit["data_dependencies"]
    assert audit["external_review_dependencies"]
    assert audit["items_blocked_inside_repo"]
    assert any(item["requires_data"] for item in audit["missing_factors"])
    assert any(item["requires_external_review"] for item in audit["missing_factors"])
    assert any(item["restricted_data_required"] for item in audit["data_dependencies"])


def test_dashboard_and_release_manifests_reference_full_repo_audit(repo_root) -> None:
    dashboard = (repo_root / "data" / "dashboard" / "executive_dashboard_manifest.yaml").read_text(encoding="utf-8")
    release = (repo_root / "data" / "release" / "v1_5_release_manifest.yaml").read_text(encoding="utf-8")
    report_map = (repo_root / "release" / "v1_5_rc" / "REPORT_MAP.md").read_text(encoding="utf-8")

    for text in [dashboard, release, report_map]:
        assert "full_repo_integrity_upgrade_audit" in text
        assert "reports/full_repo_integrity_upgrade_audit.md" in text
        assert "reports/full_repo_integrity_upgrade_audit.json" in text or "JSON companions" in text


def test_existing_dashboard_pages_import_cleanly(repo_root) -> None:
    runpy.run_path(str(repo_root / "simulator" / "app.py"), run_name="__main__")
    runpy.run_path(str(repo_root / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py"), run_name="__main__")
