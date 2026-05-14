from __future__ import annotations

import json
import subprocess
import sys


REQUIRED_WARNING = (
    "These are synthetic household weighting outputs only. They are not population estimates, real "
    "distributional modelling, ABS/HILDA/Census analysis, DSS/Services Australia modelling, Treasury "
    "modelling, PBO costing, welfare advice, eligibility law, legal advice, tax advice, or economic validation."
)


def test_household_weighting_report_generates(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-household-weighting-reports"
    completed = subprocess.run(
        [sys.executable, "scripts/run_household_weighting.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "household_weighting.md").exists()
    assert (reports_dir / "household_weighting.json").exists()


def test_household_weighting_report_includes_required_non_claims(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-household-weighting-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_household_weighting.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "household_weighting.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "household_weighting.json").read_text(encoding="utf-8"))

    assert REQUIRED_WARNING in markdown
    assert REQUIRED_WARNING in payload["metadata"]["non_claims"]
    assert payload["metadata"]["status"] == "synthetic_household_weighting_outputs_only"
    assert len(payload["examples"]) == 5


def test_household_weighting_report_marks_outputs_not_representative(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-household-weighting-representativeness"
    subprocess.run(
        [sys.executable, "scripts/run_household_weighting.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    payload = json.loads((reports_dir / "household_weighting.json").read_text(encoding="utf-8"))

    assert payload["calibration_shell"]["ready_for_real_distributional_claims"] is False
    assert all(
        example["aggregation_result"]["representative_of_real_population"] is False
        for example in payload["examples"]
    )
    assert all(example["firm_level_liability_modified"] is False for example in payload["examples"])


def test_household_weighting_report_clarifies_weight_record_aggregation(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-household-weighting-aggregation-basis"
    subprocess.run(
        [sys.executable, "scripts/run_household_weighting.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "household_weighting.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "household_weighting.json").read_text(encoding="utf-8"))

    assert "Overall synthetic weight-record average residual gap" in markdown
    assert "Overall synthetic weight-record high/critical share" in markdown
    assert (
        "Overall metrics aggregate synthetic weight records. If the same scenario appears in multiple subgroup weights, "
        "it may contribute more than once. These outputs are stress-test summaries, not unique-household or "
        "population-weighted estimates."
    ) in markdown
    assert any(
        example["aggregation_result"]["aggregation_basis"]
        == "synthetic_weight_record_aggregate_not_unique_population_weight"
        for example in payload["examples"]
    )
    assert any(
        example["aggregation_result"]["duplicate_scenario_weight_records"]
        for example in payload["examples"]
    )


def test_existing_reports_repo_guardrails_and_household_weighting_still_generate(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-existing-plus-household-weighting"
    commands = [
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_evidence_workflow.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_ingestion_controls.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_investment_guardrails.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_fiscal_trajectory.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_transition_funding.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_payment_interactions.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_distributional_scenarios.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_household_weighting.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_repo_guardrails.py", "--reports-dir", str(reports_dir)],
    ]
    for command in commands:
        completed = subprocess.run(command, cwd=repo_root, check=False, capture_output=True, text=True)
        assert completed.returncode == 0, completed.stderr

    assert (reports_dir / "household_weighting.md").exists()
    assert (reports_dir / "repo_guardrails.md").exists()


def test_streamlit_household_weighting_page_imports_without_error(repo_root) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('simulator/pages/17_Household_Weighting.py', run_name='__main__')",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_household_weighting_report_does_not_claim_real_population_or_welfare_validation(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-household-weighting-validation-claims"
    subprocess.run(
        [sys.executable, "scripts/run_household_weighting.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in reports_dir.glob("household_weighting.*"))
    forbidden_claims = [
        "population estimates are validated",
        "real distributional modelling is complete",
        "abs/hilda/census analysis is validated",
        "dss/services australia modelling is validated",
        "treasury modelling is validated",
        "pbo costing is validated",
        "welfare advice is complete",
        "eligibility law is implemented",
        "legal validation is complete",
        "tax validation is complete",
        "economic validation is complete",
        "firm-level carsf liability is modified",
    ]

    for claim in forbidden_claims:
        assert claim not in combined
