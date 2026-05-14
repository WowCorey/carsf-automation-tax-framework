from __future__ import annotations

import json
import subprocess
import sys


def test_distributional_report_generates(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-distributional-reports"
    completed = subprocess.run(
        [sys.executable, "scripts/run_distributional_scenarios.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "distributional_scenarios.md").exists()
    assert (reports_dir / "distributional_scenarios.json").exists()


def test_distributional_report_includes_required_non_claims(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-distributional-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_distributional_scenarios.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "distributional_scenarios.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "distributional_scenarios.json").read_text(encoding="utf-8"))
    required = (
        "These are synthetic household distributional scenarios only. They are not real household modelling, "
        "welfare advice, eligibility law, DSS/Services Australia modelling, ABS analysis, Treasury modelling, "
        "PBO costing, legal advice, tax advice, or economic validation."
    )

    assert required in markdown
    assert required in payload["metadata"]["non_claims"]
    assert payload["metadata"]["status"] == "synthetic_household_distributional_outputs_only"
    assert payload["summary"]["scenario_count"] == 7


def test_existing_reports_and_repo_guardrails_still_generate_with_distributional_scenarios(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-existing-plus-distributional"
    commands = [
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_evidence_workflow.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_ingestion_controls.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_investment_guardrails.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_fiscal_trajectory.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_transition_funding.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_payment_interactions.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_distributional_scenarios.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_repo_guardrails.py", "--reports-dir", str(reports_dir)],
    ]
    for command in commands:
        completed = subprocess.run(command, cwd=repo_root, check=False, capture_output=True, text=True)
        assert completed.returncode == 0, completed.stderr

    assert (reports_dir / "distributional_scenarios.md").exists()
    assert (reports_dir / "repo_guardrails.md").exists()


def test_streamlit_distributional_page_imports_without_error(repo_root) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('simulator/pages/16_Distributional_Scenarios.py', run_name='__main__')",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_distributional_report_does_not_claim_real_household_or_welfare_validation(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-distributional-validation-claims"
    subprocess.run(
        [sys.executable, "scripts/run_distributional_scenarios.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in reports_dir.glob("distributional_scenarios.*"))
    forbidden_claims = [
        "real household modelling is complete",
        "welfare validated",
        "eligibility law is implemented",
        "dss validated",
        "services australia validated",
        "abs validated",
        "treasury validated",
        "pbo validated",
        "legal validation is complete",
        "tax validation is complete",
        "firm-level carsf liability is modified",
    ]

    for claim in forbidden_claims:
        assert claim not in combined

    payload = json.loads((reports_dir / "distributional_scenarios.json").read_text(encoding="utf-8"))
    assert all(item["firm_level_liability_modified"] is False for item in payload["examples"])
