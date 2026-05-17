from __future__ import annotations

import json
import subprocess
import sys


REQUIRED_WARNING = (
    "Behavioural response simulation is prototype-only deterministic placeholder scenario review. "
    "It does not predict taxpayer behaviour. It does not estimate behavioural elasticity. "
    "It is not ATO audit logic, Treasury modelling, ABS/ATO/DSS/PBO analysis, economic validation, "
    "compliance-risk scoring, legal advice, tax advice, or investment advice. It does not estimate "
    "actual tax payable, modify firm-level CARSF liability, implement penalties, or implement enforcement."
)
FORBIDDEN_PHRASES = [
    "firms will avoid",
    "taxpayers will avoid",
    "predicted taxpayer behaviour",
    "behavioural elasticity estimate",
    "validated compliance risk",
    "ato audit score",
    "real compliance score",
    "actual taxpayer response",
    "expected avoidance rate",
    "enforcement-ready",
    "penalty applies",
    "actual tax payable can be estimated",
    "economic validation is complete",
    "treasury validated",
    "ato validated",
    "official behavioural model",
]


def test_behavioural_response_report_generates_json_and_markdown(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-behavioural-response"
    completed = subprocess.run(
        [sys.executable, "scripts/run_behavioural_response_simulation.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "behavioural_response_simulation.md").exists()
    assert (reports_dir / "behavioural_response_simulation.json").exists()


def test_behavioural_response_report_includes_all_non_claim_language(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-behavioural-response-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_behavioural_response_simulation.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "behavioural_response_simulation.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "behavioural_response_simulation.json").read_text(encoding="utf-8"))

    assert REQUIRED_WARNING in markdown
    assert REQUIRED_WARNING in payload["metadata"]["non_claims"]
    assert payload["metadata"]["firm_level_liability_logic_modified"] is False
    assert payload["metadata"]["behavioural_prediction_created"] is False
    assert payload["metadata"]["compliance_scoring_created"] is False


def test_behavioural_response_report_has_required_summary_counts(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-behavioural-response-summary"
    subprocess.run(
        [sys.executable, "scripts/run_behavioural_response_simulation.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    payload = json.loads((reports_dir / "behavioural_response_simulation.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["total_scenarios"] == 12
    assert summary["scenarios_requiring_external_review"] >= 1
    assert summary["scenarios_requiring_transfer_pricing_review"] >= 1
    assert summary["scenarios_requiring_grouped_entity_review"] >= 1
    assert summary["scenarios_requiring_schedule_authority_review"] >= 1
    assert summary["scenarios_requiring_aava_deductibility_review"] >= 1
    assert summary["scenarios_requiring_capital_base_review"] >= 1
    assert summary["scenarios_requiring_offshore_attribution_review"] >= 1
    assert summary["scenarios_requiring_customer_self_service_review"] >= 1
    assert summary["scenarios_suppress_until_calibrated"] >= 1
    assert summary["firm_level_liability_logic_modified"] is False
    assert summary["scenarios_by_pressure_band"]["moderate_placeholder_response_pressure"] >= 1
    assert summary["scenarios_by_pressure_band"]["high_placeholder_response_pressure"] >= 1
    assert summary["scenarios_by_pressure_band"]["critical_review_required"] >= 1


def test_behavioural_response_report_contains_required_table(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-behavioural-response-table"
    subprocess.run(
        [sys.executable, "scripts/run_behavioural_response_simulation.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "behavioural_response_simulation.md").read_text(encoding="utf-8")

    assert "Scenario ID | Scenario Name | Sector Schedule | Response Type" in markdown
    assert "Pressure Basis | Linked Avoidance Flags | Response Pressure Band | Review Status" in markdown
    assert "Do Not Predict | Main Reason" in markdown


def test_behavioural_response_report_has_no_forbidden_prediction_language(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-behavioural-response-forbidden"
    subprocess.run(
        [sys.executable, "scripts/run_behavioural_response_simulation.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in reports_dir.glob("behavioural_response_simulation.*")
    )

    for phrase in FORBIDDEN_PHRASES:
        assert phrase not in combined


def test_streamlit_behavioural_response_page_imports_without_error(repo_root) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('simulator/pages/22_Behavioural_Response.py', run_name='__main__')",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_ci_runs_behavioural_response_runner_after_sector_stress(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    sector_stress_index = workflow.index("python scripts/run_sector_stress_matrix.py")
    behavioural_index = workflow.index("python scripts/run_behavioural_response_simulation.py")
    guardrail_index = workflow.index("python scripts/run_repo_guardrails.py")

    assert sector_stress_index < behavioural_index < guardrail_index


def test_behavioural_response_report_deterministic_counts(repo_root) -> None:
    first_dir = repo_root / "tmp" / "test-behavioural-response-deterministic-1"
    second_dir = repo_root / "tmp" / "test-behavioural-response-deterministic-2"
    subprocess.run(
        [sys.executable, "scripts/run_behavioural_response_simulation.py", "--reports-dir", str(first_dir)],
        cwd=repo_root,
        check=True,
    )
    subprocess.run(
        [sys.executable, "scripts/run_behavioural_response_simulation.py", "--reports-dir", str(second_dir)],
        cwd=repo_root,
        check=True,
    )

    first = json.loads((first_dir / "behavioural_response_simulation.json").read_text(encoding="utf-8"))
    second = json.loads((second_dir / "behavioural_response_simulation.json").read_text(encoding="utf-8"))

    assert first["summary"] == second["summary"]
    assert [item["scenario_id"] for item in first["behavioural_response_results"]] == [
        item["scenario_id"] for item in second["behavioural_response_results"]
    ]
