from __future__ import annotations

import json
import subprocess
import sys

from carsf.public_data_consistency_audit import PUBLIC_DATA_CONSISTENCY_AUDIT_WARNING
from carsf.public_data_pilot import find_forbidden_affirmative_public_data_claims


def test_public_data_consistency_audit_report_generates_json_and_markdown(repo_root) -> None:
    completed = subprocess.run(
        [sys.executable, "scripts/run_public_data_consistency_audit.py"],
        cwd=repo_root,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "audit findings: 13" in completed.stdout
    assert "findings fail closed: 0" in completed.stdout
    assert (repo_root / "reports" / "public_data_consistency_audit.md").exists()
    assert (repo_root / "reports" / "public_data_consistency_audit.json").exists()


def test_public_data_consistency_audit_report_includes_sections_and_non_claims(repo_root) -> None:
    markdown = (repo_root / "reports" / "public_data_consistency_audit.md").read_text(encoding="utf-8")
    payload = json.loads((repo_root / "reports" / "public_data_consistency_audit.json").read_text(encoding="utf-8"))
    for section in [
        "## A. Purpose",
        "## B. Non-Claims",
        "## C. Audit Method",
        "## E. Source Reference To Extract Audit",
        "## F. Loaded Extract To Evidence Map Audit",
        "## G. Source-Reference-Only Count Audit",
        "## H. Fair Work Wage Arithmetic Audit",
        "## I. Placeholder Boundary Audit",
        "## J. Module Calibration Boundary Audit",
        "## K. Restricted Blocker Preservation Audit",
        "## L. Forbidden Repo Data Preservation Audit",
        "## M. Digest Consistency Audit",
        "## N. Report / JSON Consistency Audit",
        "## O. Dashboard Source Consistency Audit",
        "## P. Non-Claim Boundary Audit",
        "## Q. Forbidden Claim Scan",
        "## R. Audit Findings",
        "## S. Reconciliation Summary",
        "## T. What This Audit Does Not Mean",
        "## U. Build 30 Readiness",
        "## V. Limitations and Future Work",
    ]:
        assert section in markdown
    assert PUBLIC_DATA_CONSISTENCY_AUDIT_WARNING in markdown
    assert payload["summary"]["consistency_audit_created"] is True
    assert payload["summary"]["forbidden_claim_findings"] == 0
    assert payload["summary"]["non_claim_boundary_failures"] == 0


def test_public_data_consistency_audit_reports_have_no_forbidden_affirmative_claims(repo_root) -> None:
    text = (
        (repo_root / "reports" / "public_data_consistency_audit.md").read_text(encoding="utf-8")
        + "\n"
        + (repo_root / "reports" / "public_data_consistency_audit.json").read_text(encoding="utf-8")
    )
    assert find_forbidden_affirmative_public_data_claims(text) == []


def test_public_data_consistency_audit_ci_runs_new_runner_after_evidence_map(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
    assert "python scripts/run_public_data_consistency_audit.py" in workflow
    assert workflow.index("python scripts/run_public_data_evidence_map.py") < workflow.index(
        "python scripts/run_public_data_consistency_audit.py"
    )
    assert workflow.index("python scripts/run_public_data_consistency_audit.py") < workflow.index(
        "python scripts/run_evidence_workflow.py"
    )
