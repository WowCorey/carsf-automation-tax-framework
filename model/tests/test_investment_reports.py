from __future__ import annotations

import json
import subprocess
import sys


def test_investment_report_generates(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-investment-reports"
    completed = subprocess.run(
        [sys.executable, "scripts/run_investment_guardrails.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "investment_guardrails.md").exists()
    assert (reports_dir / "investment_guardrails.json").exists()


def test_investment_report_includes_non_claim_warning(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-investment-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_investment_guardrails.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "investment_guardrails.md").read_text(encoding="utf-8").lower()
    payload = json.loads((reports_dir / "investment_guardrails.json").read_text(encoding="utf-8"))

    assert "prototype investment and tax-incidence guardrails only" in markdown
    assert "not economic validation" in markdown
    assert payload["metadata"]["status"] == "prototype_investment_incidence_guardrails_only"
    assert all(example["final_liability_modified"] is False for example in payload["examples"])


def test_existing_reports_and_repo_guardrails_still_generate(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-existing-plus-investment"
    commands = [
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_evidence_workflow.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_ingestion_controls.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_investment_guardrails.py", "--reports-dir", str(reports_dir)],
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
    assert (reports_dir / "mock_evidence_workflow.md").exists()
    assert (reports_dir / "secure_ingestion_controls.md").exists()
    assert (reports_dir / "investment_guardrails.md").exists()
    assert (reports_dir / "repo_guardrails.md").exists()


def test_streamlit_investment_page_imports_without_error(repo_root) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('simulator/pages/12_Investment_and_Incidence_Guardrails.py', run_name='__main__')",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_investment_report_does_not_claim_economic_validation(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-investment-validation-claims"
    subprocess.run(
        [sys.executable, "scripts/run_investment_guardrails.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in reports_dir.glob("investment_guardrails.*"))
    forbidden_claims = [
        "economically validated",
        "investment validated",
        "treasury validated",
        "ato validated",
        "market validated",
        "liability has been changed",
    ]

    for claim in forbidden_claims:
        assert claim not in combined
