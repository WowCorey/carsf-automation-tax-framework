from __future__ import annotations

import json
import subprocess
import sys

from carsf.final_rc_integrity_seal import (
    FINAL_RC_INTEGRITY_SEAL_WARNING,
    find_forbidden_affirmative_seal_claims,
)


def test_final_rc_integrity_seal_report_generates_json_markdown_and_release_docs(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-final-rc-integrity-seal" / "reports"
    release_dir = repo_root / "tmp" / "test-final-rc-integrity-seal" / "release"
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_v1_5_final_rc_integrity_seal.py",
            "--reports-dir",
            str(reports_dir),
            "--release-dir",
            str(release_dir),
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "v1_5_final_rc_integrity_seal.md").exists()
    assert (reports_dir / "v1_5_final_rc_integrity_seal.json").exists()
    assert (release_dir / "FINAL_RC_INTEGRITY_SEAL.md").exists()
    assert (release_dir / "FINAL_RC_INTEGRITY_SEAL.json").exists()
    assert (release_dir / "FINAL_RC_DIGESTS.json").exists()


def test_final_rc_integrity_seal_report_includes_non_claims_and_false_flags(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-final-rc-integrity-seal-nonclaims" / "reports"
    release_dir = repo_root / "tmp" / "test-final-rc-integrity-seal-nonclaims" / "release"
    subprocess.run(
        [
            sys.executable,
            "scripts/run_v1_5_final_rc_integrity_seal.py",
            "--reports-dir",
            str(reports_dir),
            "--release-dir",
            str(release_dir),
        ],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "v1_5_final_rc_integrity_seal.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "v1_5_final_rc_integrity_seal.json").read_text(encoding="utf-8"))

    assert FINAL_RC_INTEGRITY_SEAL_WARNING in markdown
    assert FINAL_RC_INTEGRITY_SEAL_WARNING in payload["metadata"]["non_claims"]
    for key in [
        "review_completed",
        "approval_claimed",
        "validation_claimed",
        "readiness_score_created",
        "maturity_score_created",
        "operational_readiness_claimed",
        "legal_sufficiency_claimed",
        "legislative_readiness_claimed",
        "economic_validation_claimed",
        "welfare_validation_claimed",
        "statistical_validation_claimed",
        "official_status_claimed",
        "official_review_pathway_claimed",
        "real_data_used",
        "actual_tax_payable_determined",
        "compliance_scoring_created",
        "enforcement_created",
        "notices_created",
        "penalties_created",
        "operative_law_created",
        "firm_level_liability_logic_modified",
    ]:
        assert payload["metadata"][key] is False
        assert payload["summary"][key] is False


def test_final_rc_integrity_seal_report_contains_required_sections(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-final-rc-integrity-seal-sections" / "reports"
    release_dir = repo_root / "tmp" / "test-final-rc-integrity-seal-sections" / "release"
    subprocess.run(
        [
            sys.executable,
            "scripts/run_v1_5_final_rc_integrity_seal.py",
            "--reports-dir",
            str(reports_dir),
            "--release-dir",
            str(release_dir),
        ],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "v1_5_final_rc_integrity_seal.md").read_text(encoding="utf-8")

    for heading in [
        "## D. Release Document Inventory",
        "## E. Attack-Pack Document Inventory",
        "## F. Generated Report Inventory",
        "## G. Manifest Alignment",
        "## H. Digest Summary",
        "## I. False Flag Verification",
        "## J. Boundary Phrase Verification",
        "## K. Forbidden Claim Scan",
        "## L. Guardrail Status",
        "## M. CI Expectations",
        "## P. What This Seal Does Not Mean",
    ]:
        assert heading in markdown


def test_final_rc_integrity_seal_reports_have_no_forbidden_affirmative_claims(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-final-rc-integrity-seal-forbidden" / "reports"
    release_dir = repo_root / "tmp" / "test-final-rc-integrity-seal-forbidden" / "release"
    subprocess.run(
        [
            sys.executable,
            "scripts/run_v1_5_final_rc_integrity_seal.py",
            "--reports-dir",
            str(reports_dir),
            "--release-dir",
            str(release_dir),
        ],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in reports_dir.glob("v1_5_final_rc_integrity_seal.*"))
    combined += "\n".join(path.read_text(encoding="utf-8") for path in release_dir.glob("FINAL_RC_*.*"))

    assert find_forbidden_affirmative_seal_claims(combined) == []


def test_final_rc_integrity_seal_ci_order(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    attack_index = workflow.index("python scripts/run_external_review_attack_pack.py")
    seal_index = workflow.index("python scripts/run_v1_5_final_rc_integrity_seal.py")
    evidence_index = workflow.index("python scripts/run_evidence_workflow.py")
    guardrail_index = workflow.index("python scripts/run_repo_guardrails.py")

    assert attack_index < seal_index < evidence_index < guardrail_index


def test_main_streamlit_app_imports_cleanly(repo_root) -> None:
    completed = subprocess.run(
        [sys.executable, "-c", "import runpy; runpy.run_path('simulator/app.py', run_name='__main__')"],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
