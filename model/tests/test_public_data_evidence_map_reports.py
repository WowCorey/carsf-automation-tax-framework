from __future__ import annotations

import json
import subprocess
import sys

from carsf.public_data_evidence_map import PUBLIC_DATA_EVIDENCE_MAP_WARNING
from carsf.public_data_pilot import find_forbidden_affirmative_public_data_claims


def run_report(repo_root, reports_dir):
    return subprocess.run(
        [
            sys.executable,
            "scripts/run_public_data_evidence_map.py",
            "--reports-dir",
            str(reports_dir),
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )


def test_public_data_evidence_map_report_generates_json_and_markdown(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-public-data-evidence-map"
    completed = run_report(repo_root, reports_dir)

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "public_data_evidence_map.md").exists()
    assert (reports_dir / "public_data_evidence_map.json").exists()


def test_public_data_evidence_map_report_includes_non_claims_and_sections(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-public-data-evidence-map-sections"
    completed = run_report(repo_root, reports_dir)
    assert completed.returncode == 0, completed.stderr

    markdown = (reports_dir / "public_data_evidence_map.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "public_data_evidence_map.json").read_text(encoding="utf-8"))

    assert PUBLIC_DATA_EVIDENCE_MAP_WARNING in markdown
    assert PUBLIC_DATA_EVIDENCE_MAP_WARNING in payload["metadata"]["non_claims"]
    for heading in [
        "## A. Purpose",
        "## B. Non-Claims",
        "## C. How Reviewers Should Use This Map",
        "## D. Evidence Status Taxonomy",
        "## E. Reviewer Interpretation Taxonomy",
        "## F. Confidence Labels",
        "## G. Source Evidence Map",
        "## H. Loaded Public Extract Evidence Map",
        "## I. Source-Reference-Only Evidence Map",
        "## J. Realistic Placeholder Evidence Map",
        "## K. Field Sanity Evidence Map",
        "## L. Module Sanity Evidence Map",
        "## M. Restricted Blocker Evidence Map",
        "## N. Forbidden Repo Data Evidence Map",
        "## O. Reviewer Questions",
        "## P. What Became More Reviewable",
        "## Q. What Still Cannot Be Claimed",
        "## R. Build 29 Readiness",
        "## S. Limitations and Future Work",
    ]:
        assert heading in markdown


def test_public_data_evidence_map_report_has_safe_summary_flags(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-public-data-evidence-map-flags"
    completed = run_report(repo_root, reports_dir)
    assert completed.returncode == 0, completed.stderr
    payload = json.loads((reports_dir / "public_data_evidence_map.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["evidence_map_created"] is True
    assert summary["new_data_loaded"] is False
    assert summary["real_public_data_loaded_from_build_27_only"] is True
    assert summary["source_references_mapped"] is True
    assert summary["loaded_public_extracts_mapped"] is True
    assert summary["source_reference_only_records_mapped"] is True
    assert summary["realistic_placeholders_mapped"] is True
    assert summary["restricted_blockers_mapped"] is True
    for key in [
        "real_calibration_completed",
        "actual_tax_payable_determined",
        "validation_claimed",
        "approval_claimed",
        "operational_readiness_claimed",
        "legal_sufficiency_claimed",
        "official_status_claimed",
        "firm_level_liability_logic_modified",
    ]:
        assert summary[key] is False


def test_public_data_evidence_map_reports_have_no_forbidden_affirmative_claims(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-public-data-evidence-map-forbidden"
    completed = run_report(repo_root, reports_dir)
    assert completed.returncode == 0, completed.stderr
    combined = (
        (reports_dir / "public_data_evidence_map.md").read_text(encoding="utf-8")
        + "\n"
        + (reports_dir / "public_data_evidence_map.json").read_text(encoding="utf-8")
    )

    assert find_forbidden_affirmative_public_data_claims(combined) == []


def test_public_data_evidence_map_ci_runs_new_runner(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "python scripts/run_public_data_evidence_map.py" in workflow
    assert workflow.index("python scripts/run_public_data_pilot.py") < workflow.index(
        "python scripts/run_public_data_evidence_map.py"
    )
    assert workflow.index("python scripts/run_public_data_evidence_map.py") < workflow.index(
        "python scripts/run_evidence_workflow.py"
    )
