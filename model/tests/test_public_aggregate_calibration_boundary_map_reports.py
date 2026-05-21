from __future__ import annotations

import json
import subprocess
import sys

from carsf.public_aggregate_calibration_boundary_map import (
    CALIBRATION_BOUNDARY_WARNING,
    find_forbidden_affirmative_calibration_boundary_claims,
)


def test_calibration_boundary_map_report_generates_json_and_markdown(repo_root, tmp_path) -> None:
    reports_dir = tmp_path / "reports"
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_public_aggregate_calibration_boundary_map.py",
            "--reports-dir",
            str(reports_dir),
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "public_aggregate_calibration_boundary_map.md").exists()
    assert (reports_dir / "public_aggregate_calibration_boundary_map.json").exists()


def test_calibration_boundary_map_report_sections_and_non_claims(repo_root, tmp_path) -> None:
    reports_dir = tmp_path / "reports"
    subprocess.run(
        [sys.executable, "scripts/run_public_aggregate_calibration_boundary_map.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "public_aggregate_calibration_boundary_map.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "public_aggregate_calibration_boundary_map.json").read_text(encoding="utf-8"))

    for heading in [
        "## A. Purpose",
        "## B. Non-Claims",
        "## C. Input Public Aggregate Values",
        "## D. Allowed Use Type Taxonomy",
        "## E. Forbidden Use Type Taxonomy",
        "## F. Boundary Status Taxonomy",
        "## G. Claim Level Taxonomy",
        "## H. Module Calibration Boundary Decisions",
        "## I. Field Calibration Boundary Decisions",
        "## J. What Public Aggregate Data Can Support",
        "## K. What Public Aggregate Data Cannot Support",
        "## L. Modules Allowed Sanity Checks Only",
        "## M. Modules Allowed Public Aggregate Anchors",
        "## N. Modules Allowed Public Aggregate Bounds",
        "## O. Modules Allowed Context Only",
        "## P. Modules Blocked For Calibration",
        "## Q. Modules Requiring Restricted Data",
        "## R. Modules Requiring External Review",
        "## S. Source Candidates Not Loaded",
        "## T. Calibration Blockers Still Remaining",
        "## U. Build 34 Readiness",
        "## V. Limitations and Future Work",
    ]:
        assert heading in markdown

    assert "Modules Requiring External Review" in markdown
    assert CALIBRATION_BOUNDARY_WARNING in markdown
    assert CALIBRATION_BOUNDARY_WARNING in payload["metadata"]["non_claims"]


def test_calibration_boundary_map_report_summary_flags_and_forbidden_claims(repo_root, tmp_path) -> None:
    reports_dir = tmp_path / "reports"
    subprocess.run(
        [sys.executable, "scripts/run_public_aggregate_calibration_boundary_map.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "public_aggregate_calibration_boundary_map.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "public_aggregate_calibration_boundary_map.json").read_text(encoding="utf-8"))
    combined = markdown + "\n" + json.dumps(payload, sort_keys=True)
    summary = payload["summary"]

    assert summary["public_aggregate_calibration_boundary_map_created"] is True
    assert summary["new_data_loaded"] is False
    assert summary["loaded_public_values_used"] == 10
    assert summary["module_boundaries_mapped"] == 19
    assert summary["field_boundaries_mapped"] == 11
    assert summary["public_source_candidates_treated_as_loaded"] is False
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
    assert find_forbidden_affirmative_calibration_boundary_claims(combined) == []


def test_ci_runs_calibration_boundary_map_after_placeholder_replacement(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    replacement_index = workflow.index("python scripts/run_public_data_placeholder_replacement_map.py")
    boundary_index = workflow.index("python scripts/run_public_aggregate_calibration_boundary_map.py")
    evidence_index = workflow.index("python scripts/run_evidence_workflow.py")

    assert replacement_index < boundary_index < evidence_index
