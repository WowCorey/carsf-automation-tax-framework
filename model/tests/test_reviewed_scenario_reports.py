from __future__ import annotations

import json
import subprocess
import sys


REQUIRED_WARNING = (
    "Reviewed scenario outputs are prototype display-control signals only. They are not statistical validation, "
    "population estimates, real household modelling, ABS/HILDA/Census analysis, DSS/Services Australia modelling, "
    "ATO analysis, Treasury modelling, PBO costing, welfare advice, eligibility law, legal advice, tax advice, "
    "or economic validation."
)


def test_reviewed_scenario_runner_writes_json_and_markdown(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-reviewed-scenarios"
    completed = subprocess.run(
        [sys.executable, "scripts/run_reviewed_scenarios.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "reviewed_scenarios.md").exists()
    assert (reports_dir / "reviewed_scenarios.json").exists()


def test_reviewed_scenario_report_includes_non_claim_language(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-reviewed-scenarios-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_reviewed_scenarios.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "reviewed_scenarios.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "reviewed_scenarios.json").read_text(encoding="utf-8"))

    assert REQUIRED_WARNING in markdown
    assert REQUIRED_WARNING in payload["metadata"]["non_claims"]
    assert payload["metadata"]["firm_level_liability_modified"] is False
    assert "Fragile or missing-range outputs must not be presented as clean point estimates." in markdown


def test_reviewed_scenario_report_has_required_tables_and_counts(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-reviewed-scenarios-tables"
    subprocess.run(
        [sys.executable, "scripts/run_reviewed_scenarios.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "reviewed_scenarios.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "reviewed_scenarios.json").read_text(encoding="utf-8"))

    assert "## D. Household Scenario Review Table" in markdown
    assert "## E. Weighted Subgroup Review Table" in markdown
    assert "Scenario | Risk Signal Stability | Low Case | Base Case | High Case" in markdown
    assert "Subgroup | Residual Gap Stability | High/Critical Share Stability" in markdown
    assert payload["summary"]["total_reviewed_outputs"] == (
        len(payload["household_reviews"]) + len(payload["weighted_subgroup_reviews"])
    )
    assert payload["summary"]["external_review_required_count"] == payload["summary"]["total_reviewed_outputs"]


def test_reviewed_scenario_report_deterministic_counts(repo_root) -> None:
    first_dir = repo_root / "tmp" / "test-reviewed-scenarios-deterministic-1"
    second_dir = repo_root / "tmp" / "test-reviewed-scenarios-deterministic-2"
    subprocess.run(
        [sys.executable, "scripts/run_reviewed_scenarios.py", "--reports-dir", str(first_dir)],
        cwd=repo_root,
        check=True,
    )
    subprocess.run(
        [sys.executable, "scripts/run_reviewed_scenarios.py", "--reports-dir", str(second_dir)],
        cwd=repo_root,
        check=True,
    )

    first = json.loads((first_dir / "reviewed_scenarios.json").read_text(encoding="utf-8"))
    second = json.loads((second_dir / "reviewed_scenarios.json").read_text(encoding="utf-8"))

    assert first["summary"] == second["summary"]
    assert [
        item["review_category"] for item in first["household_reviews"]
    ] == [
        item["review_category"] for item in second["household_reviews"]
    ]


def test_streamlit_reviewed_scenarios_page_imports_without_error(repo_root) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('simulator/pages/19_Reviewed_Scenarios.py', run_name='__main__')",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_ci_runs_reviewed_scenario_runner_after_uncertainty(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    uncertainty_index = workflow.index("python scripts/run_uncertainty_ranges.py")
    reviewed_index = workflow.index("python scripts/run_reviewed_scenarios.py")
    guardrail_index = workflow.index("python scripts/run_repo_guardrails.py")

    assert uncertainty_index < reviewed_index < guardrail_index


def test_reviewed_scenario_report_does_not_claim_real_validation(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-reviewed-scenarios-validation-claims"
    subprocess.run(
        [sys.executable, "scripts/run_reviewed_scenarios.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in reports_dir.glob("reviewed_scenarios.*"))
    forbidden_claims = [
        "results are statistically validated",
        "results are population estimates",
        "real household modelling is validated",
        "welfare advice is provided",
        "eligibility law is implemented",
        "legal advice is provided",
        "tax advice is provided",
        "economic validation is complete",
        "firm-level carsf liability is modified",
    ]

    for claim in forbidden_claims:
        assert claim not in combined
