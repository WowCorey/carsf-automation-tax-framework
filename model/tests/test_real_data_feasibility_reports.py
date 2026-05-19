from __future__ import annotations

import json
import runpy
import subprocess
import sys

from carsf.real_data_feasibility import (
    REAL_DATA_FEASIBILITY_WARNING,
    find_forbidden_affirmative_real_data_claims,
)


def test_real_data_feasibility_report_generates_json_and_markdown(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-real-data-feasibility" / "reports"
    completed = subprocess.run(
        [sys.executable, "scripts/run_real_data_feasibility.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "real_data_feasibility.md").exists()
    assert (reports_dir / "real_data_feasibility.json").exists()


def test_real_data_feasibility_report_includes_non_claims_and_flags(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-real-data-feasibility-nonclaims" / "reports"
    subprocess.run(
        [sys.executable, "scripts/run_real_data_feasibility.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "real_data_feasibility.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "real_data_feasibility.json").read_text(encoding="utf-8"))

    assert REAL_DATA_FEASIBILITY_WARNING in markdown
    assert REAL_DATA_FEASIBILITY_WARNING in payload["metadata"]["non_claims"]
    for key in [
        "real_data_loaded",
        "real_calibration_completed",
        "restricted_data_loaded",
        "taxpayer_data_loaded",
        "firm_level_confidential_data_loaded",
        "household_microdata_loaded",
        "validation_claimed",
        "approval_claimed",
        "operational_readiness_claimed",
        "legal_sufficiency_claimed",
        "official_status_claimed",
        "firm_level_liability_logic_modified",
    ]:
        assert payload["metadata"][key] is False
        assert payload["summary"][key] is False
    assert payload["summary"]["realistic_placeholders_created"] is True
    assert payload["summary"]["placeholders_labelled"] is True


def test_real_data_feasibility_report_contains_required_sections(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-real-data-feasibility-sections" / "reports"
    subprocess.run(
        [sys.executable, "scripts/run_real_data_feasibility.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "real_data_feasibility.md").read_text(encoding="utf-8")

    for heading in [
        "## A. Purpose",
        "## B. Non-Claims",
        "## C. Data Status Taxonomy",
        "## D. Access Class Taxonomy",
        "## E. Claim Level Taxonomy",
        "## F. Source Candidate Registry",
        "## G. Calibration Field Map",
        "## H. Module Data Needs",
        "## I. Realistic Placeholder Rules",
        "## J. Restricted Data Requirements",
        "## K. Forbidden Repo Data Rules",
        "## L. Public Data Pilot Candidates",
        "## M. What Can Be Sanity-Checked Now",
        "## N. What Cannot Be Calibrated Yet",
        "## O. What Must Remain Placeholder-Only",
        "## P. External Review Routes",
        "## Q. Build 27 Public Data Pilot Readiness",
        "## R. Limitations and Future Work",
    ]:
        assert heading in markdown


def test_real_data_feasibility_reports_have_no_forbidden_affirmative_claims(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-real-data-feasibility-forbidden" / "reports"
    subprocess.run(
        [sys.executable, "scripts/run_real_data_feasibility.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = (
        (reports_dir / "real_data_feasibility.md").read_text(encoding="utf-8")
        + "\n"
        + (reports_dir / "real_data_feasibility.json").read_text(encoding="utf-8")
    )

    assert find_forbidden_affirmative_real_data_claims(combined) == []


def test_real_data_feasibility_ci_runs_new_runner(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "python scripts/run_real_data_feasibility.py" in workflow
    assert workflow.index("python scripts/run_v1_5_final_rc_integrity_seal.py") < workflow.index(
        "python scripts/run_real_data_feasibility.py"
    )
    assert workflow.index("python scripts/run_real_data_feasibility.py") < workflow.index(
        "python scripts/run_evidence_workflow.py"
    )


def test_main_streamlit_app_imports_cleanly(repo_root) -> None:
    runpy.run_path(str(repo_root / "simulator" / "app.py"), run_name="__main__")
