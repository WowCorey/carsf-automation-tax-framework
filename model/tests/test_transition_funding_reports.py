from __future__ import annotations

import json
import subprocess
import sys


def test_transition_funding_report_generates(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-transition-reports"
    completed = subprocess.run(
        [sys.executable, "scripts/run_transition_funding.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "transition_funding.md").exists()
    assert (reports_dir / "transition_funding.json").exists()


def test_transition_funding_report_includes_required_non_claims(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-transition-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_transition_funding.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "transition_funding.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "transition_funding.json").read_text(encoding="utf-8"))
    required = (
        "These are prototype transition-payment funding outputs only. They are not UBI policy, welfare advice, "
        "DSS modelling, Services Australia modelling, Treasury costing, PBO costing, legal advice, tax advice, "
        "or economic validation."
    )

    assert required in markdown
    assert required in payload["metadata"]["non_claims"]
    assert payload["metadata"]["status"] == "prototype_transition_payment_funding_outputs_only"


def test_existing_reports_and_repo_guardrails_still_generate_with_transition_funding(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-existing-plus-transition"
    commands = [
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_evidence_workflow.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_ingestion_controls.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_investment_guardrails.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_fiscal_trajectory.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_transition_funding.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_repo_guardrails.py", "--reports-dir", str(reports_dir)],
    ]
    for command in commands:
        completed = subprocess.run(command, cwd=repo_root, check=False, capture_output=True, text=True)
        assert completed.returncode == 0, completed.stderr

    assert (reports_dir / "transition_funding.md").exists()
    assert (reports_dir / "repo_guardrails.md").exists()


def test_streamlit_transition_page_imports_without_error(repo_root) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('simulator/pages/14_Transition_Funding.py', run_name='__main__')",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_transition_report_does_not_claim_real_policy_or_validation(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-transition-validation-claims"
    subprocess.run(
        [sys.executable, "scripts/run_transition_funding.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in reports_dir.glob("transition_funding.*"))
    forbidden_claims = [
        "real ubi policy",
        "welfare validated",
        "dss validated",
        "services australia validated",
        "treasury validated",
        "pbo validated",
        "legal validation is complete",
        "tax validation is complete",
        "firm-level carsf liability is modified",
    ]

    for claim in forbidden_claims:
        assert claim not in combined
