from __future__ import annotations

import json
import runpy
import subprocess
import sys

from carsf.public_data_pilot import (
    PUBLIC_DATA_PILOT_WARNING,
    find_forbidden_affirmative_public_data_claims,
)


def run_report(repo_root, reports_dir, digest_path):
    return subprocess.run(
        [
            sys.executable,
            "scripts/run_public_data_pilot.py",
            "--reports-dir",
            str(reports_dir),
            "--digest-path",
            str(digest_path),
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )


def test_public_data_pilot_report_generates_json_markdown_and_digest(repo_root) -> None:
    root = repo_root / "tmp" / "test-public-data-pilot"
    reports_dir = root / "reports"
    digest_path = root / "public_data_pilot_digests.json"
    completed = run_report(repo_root, reports_dir, digest_path)

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "public_data_pilot.md").exists()
    assert (reports_dir / "public_data_pilot.json").exists()
    assert digest_path.exists()


def test_public_data_pilot_report_includes_non_claims_and_flags(repo_root) -> None:
    root = repo_root / "tmp" / "test-public-data-pilot-nonclaims"
    reports_dir = root / "reports"
    digest_path = root / "public_data_pilot_digests.json"
    completed = run_report(repo_root, reports_dir, digest_path)
    assert completed.returncode == 0, completed.stderr

    markdown = (reports_dir / "public_data_pilot.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "public_data_pilot.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert PUBLIC_DATA_PILOT_WARNING in markdown
    assert PUBLIC_DATA_PILOT_WARNING in payload["metadata"]["non_claims"]
    assert summary["public_data_pilot_created"] is True
    assert summary["source_references_created"] is True
    assert summary["real_public_data_loaded"] is True
    assert summary["realistic_placeholders_anchored"] is True
    for key in [
        "real_calibration_completed",
        "restricted_data_loaded",
        "taxpayer_data_loaded",
        "firm_level_confidential_data_loaded",
        "household_microdata_loaded",
        "actual_tax_payable_determined",
        "validation_claimed",
        "approval_claimed",
        "operational_readiness_claimed",
        "legal_sufficiency_claimed",
        "official_status_claimed",
        "firm_level_liability_logic_modified",
    ]:
        assert summary[key] is False


def test_public_data_pilot_report_contains_required_sections(repo_root) -> None:
    root = repo_root / "tmp" / "test-public-data-pilot-sections"
    reports_dir = root / "reports"
    digest_path = root / "public_data_pilot_digests.json"
    completed = run_report(repo_root, reports_dir, digest_path)
    assert completed.returncode == 0, completed.stderr

    markdown = (reports_dir / "public_data_pilot.md").read_text(encoding="utf-8")
    for heading in [
        "## A. Purpose",
        "## B. Non-Claims",
        "## C. Public Data Loading Rules",
        "## D. Source Reference Registry",
        "## E. Public Aggregate Extracts",
        "## F. Realistic Placeholder Anchors",
        "## G. Field Sanity Checks",
        "## H. Module Sanity Checks",
        "## I. Restricted Data Still Required",
        "## J. Forbidden Repo Data Rules",
        "## K. What Became More Realistic",
        "## L. What Remains Placeholder-Only",
        "## M. What Remains Blocked",
        "## N. Digest Summary",
        "## O. Build 28 Readiness",
        "## P. Limitations and Future Work",
    ]:
        assert heading in markdown


def test_public_data_pilot_reports_have_no_forbidden_affirmative_claims(repo_root) -> None:
    root = repo_root / "tmp" / "test-public-data-pilot-forbidden"
    reports_dir = root / "reports"
    digest_path = root / "public_data_pilot_digests.json"
    completed = run_report(repo_root, reports_dir, digest_path)
    assert completed.returncode == 0, completed.stderr
    combined = (
        (reports_dir / "public_data_pilot.md").read_text(encoding="utf-8")
        + "\n"
        + (reports_dir / "public_data_pilot.json").read_text(encoding="utf-8")
    )

    assert find_forbidden_affirmative_public_data_claims(combined) == []


def test_public_data_pilot_digest_manifest_excludes_itself(repo_root) -> None:
    root = repo_root / "tmp" / "test-public-data-pilot-digests"
    reports_dir = root / "reports"
    digest_path = root / "public_data_pilot_digests.json"

    first = run_report(repo_root, reports_dir, digest_path)
    assert first.returncode == 0, first.stderr
    second = run_report(repo_root, reports_dir, digest_path)
    assert second.returncode == 0, second.stderr
    second_digest = digest_path.read_text(encoding="utf-8")
    payload = json.loads(second_digest)
    paths = {item["path"] for item in payload["digests"]}

    assert str(digest_path).replace("\\", "/") not in paths
    assert "data/public_pilot/digests/public_data_pilot_digests.json" not in paths
    assert payload["metadata"]["digest_file_hashes_itself"] is False
    assert all(len(item["sha256"]) == 64 for item in payload["digests"])


def test_public_data_pilot_ci_runs_new_runner(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "python scripts/run_public_data_pilot.py" in workflow
    assert workflow.index("python scripts/run_real_data_feasibility.py") < workflow.index(
        "python scripts/run_public_data_pilot.py"
    )
    assert workflow.index("python scripts/run_public_data_pilot.py") < workflow.index(
        "python scripts/run_evidence_workflow.py"
    )


def test_main_streamlit_app_imports_cleanly(repo_root) -> None:
    runpy.run_path(str(repo_root / "simulator" / "app.py"), run_name="__main__")
