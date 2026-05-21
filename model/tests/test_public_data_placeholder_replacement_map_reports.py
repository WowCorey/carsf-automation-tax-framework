from __future__ import annotations

import json
import subprocess
import sys

from carsf.public_data_placeholder_replacement_map import (
    PLACEHOLDER_REPLACEMENT_WARNING,
    find_forbidden_affirmative_placeholder_replacement_claims,
)


def test_placeholder_replacement_map_report_generates_json_and_markdown(repo_root, tmp_path) -> None:
    reports_dir = tmp_path / "reports"
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_public_data_placeholder_replacement_map.py",
            "--reports-dir",
            str(reports_dir),
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "public_data_placeholder_replacement_map.md").exists()
    assert (reports_dir / "public_data_placeholder_replacement_map.json").exists()


def test_placeholder_replacement_map_report_sections_and_non_claims(repo_root, tmp_path) -> None:
    reports_dir = tmp_path / "reports"
    subprocess.run(
        [sys.executable, "scripts/run_public_data_placeholder_replacement_map.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "public_data_placeholder_replacement_map.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "public_data_placeholder_replacement_map.json").read_text(encoding="utf-8"))

    for heading in [
        "## A. Purpose",
        "## B. Non-Claims",
        "## C. Input Public Aggregate Values",
        "## D. Replacement Status Taxonomy",
        "## E. Replacement Confidence Taxonomy",
        "## F. Placeholder Replacement Decisions",
        "## G. Replaced By Public Aggregate Anchor",
        "## H. Narrowed By Public Aggregate Anchor",
        "## I. Informed By Public Aggregate Anchor",
        "## J. Still Placeholder Only",
        "## K. Blocked Until Restricted Data",
        "## L. Blocked Until External Review",
        "## M. Source Candidates Not Loaded",
        "## N. What Changed",
        "## O. What Did Not Change",
        "## P. Calibration Blockers Still Remaining",
        "## Q. Build 33 Readiness",
        "## R. Limitations and Future Work",
    ]:
        assert heading in markdown

    assert PLACEHOLDER_REPLACEMENT_WARNING in markdown
    assert PLACEHOLDER_REPLACEMENT_WARNING in payload["metadata"]["non_claims"]


def test_placeholder_replacement_map_report_summary_flags_and_forbidden_claims(repo_root, tmp_path) -> None:
    reports_dir = tmp_path / "reports"
    subprocess.run(
        [sys.executable, "scripts/run_public_data_placeholder_replacement_map.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "public_data_placeholder_replacement_map.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "public_data_placeholder_replacement_map.json").read_text(encoding="utf-8"))
    combined = markdown + "\n" + json.dumps(payload, sort_keys=True)
    summary = payload["summary"]

    assert summary["placeholder_replacement_map_created"] is True
    assert summary["new_data_loaded"] is False
    assert summary["loaded_public_values_used"] == 10
    assert summary["placeholders_mapped"] == 11
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
    assert find_forbidden_affirmative_placeholder_replacement_claims(combined) == []


def test_ci_runs_placeholder_replacement_map_after_public_real_loader(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    public_real_index = workflow.index("python scripts/run_public_real_data_loader.py")
    replacement_index = workflow.index("python scripts/run_public_data_placeholder_replacement_map.py")
    evidence_index = workflow.index("python scripts/run_evidence_workflow.py")

    assert public_real_index < replacement_index < evidence_index
