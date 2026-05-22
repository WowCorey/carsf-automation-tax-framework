from __future__ import annotations

import json
import subprocess
import sys

from carsf.full_repo_integrity_upgrade_audit import find_forbidden_affirmative_repo_claims


def test_full_repo_integrity_runner_generates_reports(repo_root, tmp_path) -> None:
    reports_dir = tmp_path / "reports"
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_full_repo_integrity_upgrade_audit.py",
            "--reports-dir",
            str(reports_dir),
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "full_repo_integrity_upgrade_audit.md").exists()
    assert (reports_dir / "full_repo_integrity_upgrade_audit.json").exists()
    assert "full repo integrity audit created: True" in completed.stdout


def test_full_repo_integrity_report_sections_and_non_claims(repo_root, tmp_path) -> None:
    reports_dir = tmp_path / "reports"
    subprocess.run(
        [sys.executable, "scripts/run_full_repo_integrity_upgrade_audit.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "full_repo_integrity_upgrade_audit.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "full_repo_integrity_upgrade_audit.json").read_text(encoding="utf-8"))

    for heading in [
        "## A. Purpose",
        "## B. Non-Claims",
        "## C. Audit Scope",
        "## D. Repo-Wide Build Coverage Matrix",
        "## E. Runner Coverage Matrix",
        "## F. Report Coverage Matrix",
        "## G. JSON/Markdown Result Coverage",
        "## H. CI Coverage",
        "## I. Dashboard Coverage",
        "## J. Release Manifest Coverage",
        "## K. Documentation Coverage",
        "## L. Public Data Boundary Audit",
        "## M. Placeholder Boundary Audit",
        "## N. Calibration Boundary Audit",
        "## O. Scenario Constraint Audit",
        "## P. Guardrail Audit",
        "## Q. Non-Claim Boundary Audit",
        "## R. Safe Fixes Applied",
        "## S. Bugs Fixed",
        "## T. Missing Factors Identified",
        "## U. Missing Data Dependencies",
        "## V. External Review Dependencies",
        "## W. Items Blocked Inside Repo",
        "## X. What The Repo Can Currently Claim",
        "## Y. What The Repo Must Not Claim",
        "## Z. Recommended Next Builds",
    ]:
        assert heading in markdown

    assert "This is a full repo integrity audit only." in markdown
    assert "This does not determine actual tax payable." in markdown
    assert "This does not modify firm-level CARSF liability." in markdown
    assert "This is a full repo integrity audit only." in payload["metadata"]["non_claims"]


def test_full_repo_integrity_report_forbidden_claim_scan(repo_root, tmp_path) -> None:
    reports_dir = tmp_path / "reports"
    subprocess.run(
        [sys.executable, "scripts/run_full_repo_integrity_upgrade_audit.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "full_repo_integrity_upgrade_audit.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "full_repo_integrity_upgrade_audit.json").read_text(encoding="utf-8"))
    combined = markdown + "\n" + json.dumps(payload, sort_keys=True)
    summary = payload["summary"]

    assert find_forbidden_affirmative_repo_claims(combined) == []
    assert summary["full_repo_integrity_audit_created"] is True
    assert summary["new_data_loaded"] is False
    assert summary["calibration_completed"] is False
    assert summary["validation_claimed"] is False
    assert summary["actual_tax_payable_determined"] is False
    assert summary["official_status_claimed"] is False
    assert summary["firm_level_liability_logic_modified"] is False


def test_ci_runs_full_repo_integrity_audit_after_scenario_before_guardrails(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    scenario_index = workflow.index("python scripts/run_public_aggregate_scenario_constraint_layer.py")
    audit_index = workflow.index("python scripts/run_full_repo_integrity_upgrade_audit.py")
    guardrails_index = workflow.index("python scripts/run_repo_guardrails.py")

    assert '["schedules", "examples", "data", "release"]' in workflow
    assert scenario_index < audit_index < guardrails_index
