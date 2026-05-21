from __future__ import annotations

import json
import subprocess
import sys

from carsf.public_real_data_loader import (
    PUBLIC_REAL_DATA_WARNING,
    find_forbidden_affirmative_public_real_claims,
)


def test_public_real_data_loader_report_generates_json_markdown_parsed_and_digests(repo_root, tmp_path) -> None:
    reports_dir = tmp_path / "reports"
    parsed_path = tmp_path / "parsed" / "public_real_aggregate_values.json"
    digest_path = tmp_path / "digests" / "public_real_data_digests.json"
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_public_real_data_loader.py",
            "--reports-dir",
            str(reports_dir),
            "--parsed-path",
            str(parsed_path),
            "--digest-path",
            str(digest_path),
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "public_real_data_loader.md").exists()
    assert (reports_dir / "public_real_data_loader.json").exists()
    assert parsed_path.exists()
    assert digest_path.exists()


def test_public_real_data_loader_report_sections_and_non_claims(repo_root, tmp_path) -> None:
    reports_dir = tmp_path / "reports"
    parsed_path = tmp_path / "parsed" / "public_real_aggregate_values.json"
    digest_path = tmp_path / "digests" / "public_real_data_digests.json"
    subprocess.run(
        [
            sys.executable,
            "scripts/run_public_real_data_loader.py",
            "--reports-dir",
            str(reports_dir),
            "--parsed-path",
            str(parsed_path),
            "--digest-path",
            str(digest_path),
        ],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "public_real_data_loader.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "public_real_data_loader.json").read_text(encoding="utf-8"))

    for heading in [
        "## A. Purpose",
        "## B. Non-Claims",
        "## C. Source Inclusion Rules",
        "## D. Loaded Public Aggregate Sources",
        "## E. Source Candidates Not Loaded",
        "## F. Loaded Public Aggregate Values",
        "## G. Guardrail Checks",
        "## H. Digest Manifest",
        "## I. What This Data Can Support",
        "## J. What This Data Cannot Support",
        "## K. Placeholder Replacement Candidates",
        "## L. Calibration Blockers Still Remaining",
        "## M. Build 32 Readiness",
        "## N. Limitations and Future Work",
    ]:
        assert heading in markdown

    assert PUBLIC_REAL_DATA_WARNING in markdown
    assert PUBLIC_REAL_DATA_WARNING in payload["metadata"]["non_claims"]


def test_public_real_data_loader_report_summary_flags_and_forbidden_claims(repo_root, tmp_path) -> None:
    reports_dir = tmp_path / "reports"
    parsed_path = tmp_path / "parsed" / "public_real_aggregate_values.json"
    digest_path = tmp_path / "digests" / "public_real_data_digests.json"
    subprocess.run(
        [
            sys.executable,
            "scripts/run_public_real_data_loader.py",
            "--reports-dir",
            str(reports_dir),
            "--parsed-path",
            str(parsed_path),
            "--digest-path",
            str(digest_path),
        ],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "public_real_data_loader.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "public_real_data_loader.json").read_text(encoding="utf-8"))
    parsed = json.loads(parsed_path.read_text(encoding="utf-8"))
    combined = markdown + "\n" + json.dumps(payload, sort_keys=True)
    summary = payload["summary"]

    assert summary["public_real_data_loader_created"] is True
    assert summary["real_public_aggregate_data_loaded"] is True
    assert summary["new_public_aggregate_values_loaded"] == 10
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
    assert len(parsed["values"]) == 10
    assert find_forbidden_affirmative_public_real_claims(combined) == []


def test_ci_runs_public_real_data_loader_after_red_team_and_before_evidence_workflow(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    red_team_index = workflow.index("python scripts/run_red_team_reviewer_objections.py")
    loader_index = workflow.index("python scripts/run_public_real_data_loader.py")
    evidence_index = workflow.index("python scripts/run_evidence_workflow.py")

    assert red_team_index < loader_index < evidence_index
