from __future__ import annotations

import json
import subprocess
import sys


def test_github_pages_site_manifest_and_files_exist(repo_root) -> None:
    manifest_path = repo_root / "site" / "site_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert manifest["site_id"] == "carsf_github_pages_project_website"
    assert manifest["static_site_only"] is True
    assert manifest["backend_required"] is False
    assert manifest["external_api_calls"] is False
    assert manifest["scraping"] is False
    assert manifest["analytics_or_tracking"] is False
    assert manifest["external_cdn_dependencies"] is False

    for path in manifest["site_files"]:
        assert (repo_root / path).exists(), path

    assert "reports/public_real_data_loader.json" in manifest["source_reports"]
    assert "reports/full_repo_integrity_upgrade_audit.json" in manifest["source_reports"]
    assert manifest["source_summary"]["loaded_public_aggregate_values"] == 10
    assert manifest["source_summary"]["module_scenario_constraints"] == 20


def test_github_pages_site_runner_generates_reports(repo_root, tmp_path) -> None:
    reports_dir = tmp_path / "reports"
    completed = subprocess.run(
        [sys.executable, "scripts/build_github_pages_site.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "github_pages_site.md").exists()
    assert (reports_dir / "github_pages_site.json").exists()

    payload = json.loads((reports_dir / "github_pages_site.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["github_pages_site_created"] is True
    assert summary["static_site_only"] is True
    assert summary["required_site_files_present"] is True
    assert summary["required_sections_present"] is True
    assert summary["source_reports_available"] is True
    assert summary["source_report_counts_reconciled"] is True
    assert summary["non_claim_boundaries_visible"] is True
    assert summary["forbidden_claim_findings"] == 0
    assert summary["new_data_loaded"] is False
    assert summary["restricted_data_loaded"] is False
    assert summary["personal_data_loaded"] is False
    assert summary["taxpayer_level_data_loaded"] is False
    assert summary["firm_confidential_data_loaded"] is False
    assert summary["household_microdata_loaded"] is False
    assert summary["calibration_completed"] is False
    assert summary["validation_claimed"] is False
    assert summary["actual_tax_payable_determined"] is False
    assert summary["official_status_claimed"] is False
    assert summary["firm_level_liability_logic_modified"] is False


def test_github_pages_site_documentation_and_report_map_entries(repo_root) -> None:
    docs = (repo_root / "docs" / "github_pages_site.md").read_text(encoding="utf-8")
    report_map = (repo_root / "release" / "v1_5_rc" / "REPORT_MAP.md").read_text(encoding="utf-8")
    release_manifest = json.loads((repo_root / "release" / "v1_5_rc" / "RELEASE_MANIFEST.json").read_text(encoding="utf-8"))

    assert "GitHub Pages Project Website" in docs
    assert "python scripts/build_github_pages_site.py" in docs
    assert "reports/github_pages_site.md" in report_map
    assert "reports/github_pages_site.md" in release_manifest["generated_reports"]
    assert "reports/github_pages_site.json" in release_manifest["generated_reports"]
    assert release_manifest["summary_flags"]["github_pages_site_created_by_build_35"] is True
    assert release_manifest["summary_flags"]["new_data_loaded_by_github_pages_site"] is False


def test_ci_runs_github_pages_site_builder_before_repo_guardrails(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    audit_index = workflow.index("python scripts/run_full_repo_integrity_upgrade_audit.py")
    site_index = workflow.index("python scripts/build_github_pages_site.py")
    guardrail_index = workflow.index("python scripts/run_repo_guardrails.py")

    assert audit_index < site_index < guardrail_index
