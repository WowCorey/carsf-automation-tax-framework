from __future__ import annotations

import json
import subprocess
import sys

from carsf.source_locator_verification_pack import (
    SOURCE_LOCATOR_VERIFICATION_PACK_WARNING,
    find_forbidden_affirmative_source_locator_claims,
)


def test_source_locator_verification_pack_report_generates_json_and_markdown(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-source-locator-verification-pack"
    completed = subprocess.run(
        [sys.executable, "scripts/run_source_locator_verification_pack.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "source_locator_verification_pack.md").exists()
    assert (reports_dir / "source_locator_verification_pack.json").exists()


def test_source_locator_verification_pack_report_sections_and_non_claims(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-source-locator-verification-pack-sections"
    subprocess.run(
        [sys.executable, "scripts/run_source_locator_verification_pack.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "source_locator_verification_pack.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "source_locator_verification_pack.json").read_text(encoding="utf-8"))

    for heading in [
        "## A. Purpose",
        "## B. Non-Claims",
        "## G. Loaded Public Value Cards",
        "## H. Source-Reference-Only Cards",
        "## I. Placeholder Anchor Cards",
        "## J. Restricted Blocker Cards",
        "## K. Reviewer Checklists",
        "## L. Source Locator Completeness Summary",
        "## M. Manual Review Readiness Summary",
    ]:
        assert heading in markdown

    assert SOURCE_LOCATOR_VERIFICATION_PACK_WARNING in markdown
    assert SOURCE_LOCATOR_VERIFICATION_PACK_WARNING in payload["metadata"]["non_claims"]


def test_source_locator_verification_pack_report_summary_flags_and_forbidden_claims(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-source-locator-verification-pack-flags"
    subprocess.run(
        [sys.executable, "scripts/run_source_locator_verification_pack.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "source_locator_verification_pack.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "source_locator_verification_pack.json").read_text(encoding="utf-8"))
    combined = markdown + "\n" + json.dumps(payload, sort_keys=True)
    summary = payload["summary"]

    assert summary["source_locator_pack_created"] is True
    assert summary["new_data_loaded"] is False
    assert summary["external_source_verification_claimed"] is False
    assert summary["manual_review_pack_only"] is True
    assert summary["real_calibration_completed"] is False
    assert summary["actual_tax_payable_determined"] is False
    assert summary["validation_claimed"] is False
    assert summary["approval_claimed"] is False
    assert summary["operational_readiness_claimed"] is False
    assert summary["legal_sufficiency_claimed"] is False
    assert summary["official_status_claimed"] is False
    assert summary["firm_level_liability_logic_modified"] is False
    assert find_forbidden_affirmative_source_locator_claims(combined) == []


def test_ci_runs_source_locator_verification_runner_after_consistency_audit(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    consistency_index = workflow.index("python scripts/run_public_data_consistency_audit.py")
    locator_index = workflow.index("python scripts/run_source_locator_verification_pack.py")
    evidence_index = workflow.index("python scripts/run_evidence_workflow.py")

    assert consistency_index < locator_index < evidence_index
