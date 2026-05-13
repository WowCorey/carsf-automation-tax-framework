from __future__ import annotations

import json
import subprocess
import sys


def test_fiscal_report_generates(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-fiscal-reports"
    completed = subprocess.run(
        [sys.executable, "scripts/run_fiscal_trajectory.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "fiscal_trajectory.md").exists()
    assert (reports_dir / "fiscal_trajectory.json").exists()


def test_fiscal_report_includes_required_non_claim_warning(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-fiscal-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_fiscal_trajectory.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "fiscal_trajectory.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "fiscal_trajectory.json").read_text(encoding="utf-8"))

    required = (
        "These are prototype fiscal trajectory outputs only. They are not forecasts, Treasury modelling, "
        "ATO estimates, ABS analysis, DSS estimates, PBO costing, legal advice, tax advice, or economic validation."
    )
    assert required in markdown
    assert required in payload["metadata"]["non_claims"]
    assert payload["metadata"]["status"] == "prototype_fiscal_trajectory_outputs_only"


def test_fiscal_report_clarifies_super_is_retirement_pressure(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-fiscal-super-clarity"
    subprocess.run(
        [sys.executable, "scripts/run_fiscal_trajectory.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "fiscal_trajectory.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "fiscal_trajectory.json").read_text(encoding="utf-8"))

    assert (
        "Superannuation contribution loss is tracked as retirement-system contribution pressure, "
        "not ordinary Commonwealth revenue loss."
    ) in markdown
    first_year = payload["examples"][0]["trajectory_result"]["years"][0]
    assert "retirement_contribution_pressure" in first_year
    assert "broader_labour_linked_pressure" in first_year


def test_existing_reports_and_repo_guardrails_still_generate_with_fiscal(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-existing-plus-fiscal"
    commands = [
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_evidence_workflow.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_ingestion_controls.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_investment_guardrails.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_fiscal_trajectory.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_repo_guardrails.py", "--reports-dir", str(reports_dir)],
    ]
    for command in commands:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0, completed.stderr

    assert (reports_dir / "example_results.md").exists()
    assert (reports_dir / "investment_guardrails.md").exists()
    assert (reports_dir / "fiscal_trajectory.md").exists()
    assert (reports_dir / "repo_guardrails.md").exists()


def test_streamlit_fiscal_page_imports_without_error(repo_root) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('simulator/pages/13_Fiscal_Trajectory.py', run_name='__main__')",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_fiscal_report_does_not_claim_real_forecast_or_validation(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-fiscal-validation-claims"
    subprocess.run(
        [sys.executable, "scripts/run_fiscal_trajectory.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in reports_dir.glob("fiscal_trajectory.*"))
    forbidden_claims = [
        "treasury validated",
        "ato validated",
        "abs validated",
        "dss validated",
        "pbo validated",
        "forecast validated",
        "economic validation is complete",
        "real forecast",
        "firm-level carsf liability is modified",
    ]

    for claim in forbidden_claims:
        assert claim not in combined
