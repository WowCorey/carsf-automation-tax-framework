from __future__ import annotations

import json
import subprocess
import sys

from carsf.red_team_reviewer_objections import (
    RED_TEAM_REVIEWER_OBJECTIONS_WARNING,
    find_forbidden_affirmative_red_team_claims,
)


def test_red_team_reviewer_objections_report_generates_json_and_markdown(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-red-team-reviewer-objections"
    completed = subprocess.run(
        [sys.executable, "scripts/run_red_team_reviewer_objections.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "red_team_reviewer_objections.md").exists()
    assert (reports_dir / "red_team_reviewer_objections.json").exists()


def test_red_team_reviewer_objections_report_sections_and_non_claims(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-red-team-reviewer-objections-sections"
    subprocess.run(
        [sys.executable, "scripts/run_red_team_reviewer_objections.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "red_team_reviewer_objections.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "red_team_reviewer_objections.json").read_text(encoding="utf-8"))

    for heading in [
        "## A. Purpose",
        "## B. Non-Claims",
        "## G. Critical Objections",
        "## H. High-Severity Objections",
        "## J. Public Data Limitation Objections",
        "## K. Placeholder Limitation Objections",
        "## L. Restricted Data Blocker Objections",
        "## M. Calibration and Statistical Objections",
        "## N. Legal / Tax / Administrative Objections",
        "## O. Economic Incidence Objections",
        "## P. Dashboard / Misinterpretation Risk Objections",
        "## Q. Unresolved Blockers",
        "## R. Evidence Needed To Resolve",
        "## S. What The Project Can Say",
        "## T. What The Project Must Not Claim",
    ]:
        assert heading in markdown

    assert RED_TEAM_REVIEWER_OBJECTIONS_WARNING in markdown
    assert RED_TEAM_REVIEWER_OBJECTIONS_WARNING in payload["metadata"]["non_claims"]


def test_red_team_reviewer_objections_report_summary_flags_and_forbidden_claims(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-red-team-reviewer-objections-flags"
    subprocess.run(
        [sys.executable, "scripts/run_red_team_reviewer_objections.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "red_team_reviewer_objections.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "red_team_reviewer_objections.json").read_text(encoding="utf-8"))
    combined = markdown + "\n" + json.dumps(payload, sort_keys=True)
    summary = payload["summary"]

    assert summary["red_team_pack_created"] is True
    assert summary["new_data_loaded"] is False
    assert summary["external_source_verification_claimed"] is False
    assert summary["objections_acknowledged"] is True
    assert summary["unresolved_blockers_visible"] is True
    assert summary["calibration_limitations_visible"] is True
    assert summary["legal_limitations_visible"] is True
    assert summary["statistical_limitations_visible"] is True
    assert summary["dashboard_misinterpretation_risks_visible"] is True
    assert summary["real_calibration_completed"] is False
    assert summary["actual_tax_payable_determined"] is False
    assert summary["validation_claimed"] is False
    assert summary["approval_claimed"] is False
    assert summary["operational_readiness_claimed"] is False
    assert summary["legal_sufficiency_claimed"] is False
    assert summary["official_status_claimed"] is False
    assert summary["firm_level_liability_logic_modified"] is False
    assert find_forbidden_affirmative_red_team_claims(combined) == []


def test_ci_runs_red_team_objections_runner_after_source_locator_pack(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    locator_index = workflow.index("python scripts/run_source_locator_verification_pack.py")
    red_team_index = workflow.index("python scripts/run_red_team_reviewer_objections.py")
    evidence_index = workflow.index("python scripts/run_evidence_workflow.py")

    assert locator_index < red_team_index < evidence_index
