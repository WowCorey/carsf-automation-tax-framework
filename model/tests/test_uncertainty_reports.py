from __future__ import annotations

import json
import subprocess
import sys


REQUIRED_WARNING = (
    "These are deterministic placeholder uncertainty ranges only. They are not statistical confidence intervals, "
    "forecasts, real uncertainty quantification, population estimates, ABS/HILDA/Census analysis, "
    "DSS/Services Australia modelling, Treasury modelling, PBO costing, welfare advice, eligibility law, legal "
    "advice, tax advice, or economic validation."
)


def test_uncertainty_report_generates(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-uncertainty-reports"
    completed = subprocess.run(
        [sys.executable, "scripts/run_uncertainty_ranges.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "uncertainty_ranges.md").exists()
    assert (reports_dir / "uncertainty_ranges.json").exists()


def test_uncertainty_report_includes_required_non_claims(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-uncertainty-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_uncertainty_ranges.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "uncertainty_ranges.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "uncertainty_ranges.json").read_text(encoding="utf-8"))

    assert REQUIRED_WARNING in markdown
    assert REQUIRED_WARNING in payload["metadata"]["non_claims"]
    assert payload["metadata"]["status"] == "deterministic_placeholder_uncertainty_outputs_only"
    assert all(example["firm_level_liability_modified"] is False for example in payload["examples"])


def test_existing_reports_repo_guardrails_and_uncertainty_reports_still_generate(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-existing-plus-uncertainty"
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
        [sys.executable, "scripts/run_uncertainty_ranges.py", "--reports-dir", str(reports_dir)],
        [sys.executable, "scripts/run_repo_guardrails.py", "--reports-dir", str(reports_dir)],
    ]
    for command in commands:
        completed = subprocess.run(command, cwd=repo_root, check=False, capture_output=True, text=True)
        assert completed.returncode == 0, completed.stderr

    assert (reports_dir / "uncertainty_ranges.md").exists()
    assert (reports_dir / "repo_guardrails.md").exists()


def test_streamlit_uncertainty_page_imports_without_error(repo_root) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('simulator/pages/18_Uncertainty_Ranges.py', run_name='__main__')",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_uncertainty_report_does_not_claim_validation_or_forecasts(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-uncertainty-validation-claims"
    subprocess.run(
        [sys.executable, "scripts/run_uncertainty_ranges.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in reports_dir.glob("uncertainty_ranges.*"))
    forbidden_claims = [
        "confidence intervals are validated",
        "forecast is validated",
        "population estimates are validated",
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


def test_uncertainty_report_preserves_weighted_subgroup_metadata(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-uncertainty-subgroup-metadata"
    subprocess.run(
        [sys.executable, "scripts/run_uncertainty_ranges.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "uncertainty_ranges.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "uncertainty_ranges.json").read_text(encoding="utf-8"))
    weighted_examples = [
        example for example in payload["examples"] if example["uncertainty_type"] == "weighted"
    ]

    assert "Matched Scenarios | Unmatched Scenarios | Not Population Estimate" in markdown
    assert weighted_examples
    subgroup = weighted_examples[0]["uncertainty_result"]["subgroup_results"][0]
    assert "scenario_count" in subgroup
    assert "total_synthetic_weight" in subgroup
    assert "matched_scenarios" in subgroup
    assert subgroup["representative_of_real_population"] is False
    assert subgroup["not_population_estimate"] is True
