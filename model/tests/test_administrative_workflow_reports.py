from __future__ import annotations

import json
import subprocess
import sys


REQUIRED_WARNING = (
    "This is a prototype administrative workflow only. It is not an official workflow of the ATO. "
    "It is not guidance from the ATO, Treasury modelling, legal advice, tax advice, compliance scoring, "
    "audit logic, or enforcement. It does not create notices, implement penalties, use statutory "
    "information-gathering powers, determine non-compliance, estimate actual tax payable, predict taxpayer "
    "behaviour, estimate behavioural elasticity, use taxpayer-level, firm-level, industry, ABS, ATO, DSS, "
    "Treasury, PBO, HILDA, or Census data, or modify firm-level CARSF liability."
)
FORBIDDEN_PHRASES = [
    "ato will audit",
    "taxpayer is non-compliant",
    "non-compliance finding",
    "compliance risk score",
    "real compliance score",
    "official ato workflow",
    "ato guidance",
    "statutory notice issued",
    "notice issued",
    "penalty applies",
    "enforcement-ready",
    "actual audit pathway",
    "official audit logic",
    "real information-gathering power",
    "tax payable is",
    "actual tax payable can be estimated",
    "taxpayer behaviour predicted",
    "behavioural elasticity estimate",
    "treasury validated",
    "ato validated",
    "official administrative model",
]


def test_administrative_workflow_report_generates_json_and_markdown(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-administrative-workflow"
    completed = subprocess.run(
        [sys.executable, "scripts/run_administrative_compliance_workflow.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "administrative_compliance_workflow.md").exists()
    assert (reports_dir / "administrative_compliance_workflow.json").exists()


def test_administrative_workflow_report_includes_all_non_claim_language(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-administrative-workflow-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_administrative_compliance_workflow.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "administrative_compliance_workflow.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "administrative_compliance_workflow.json").read_text(encoding="utf-8"))

    assert REQUIRED_WARNING in markdown
    assert REQUIRED_WARNING in payload["metadata"]["non_claims"]
    assert payload["metadata"]["firm_level_liability_logic_modified"] is False
    assert payload["metadata"]["real_enforcement_created"] is False
    assert payload["metadata"]["real_ato_power_claimed"] is False
    assert payload["metadata"]["compliance_scoring_created"] is False
    assert payload["metadata"]["notices_issued"] is False
    assert payload["metadata"]["real_data_used"] is False


def test_administrative_workflow_report_has_required_summary_counts(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-administrative-workflow-summary"
    subprocess.run(
        [sys.executable, "scripts/run_administrative_compliance_workflow.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    payload = json.loads((reports_dir / "administrative_compliance_workflow.json").read_text(encoding="utf-8"))
    summary = payload["summary"]

    assert summary["total_scenarios"] == 10
    assert summary["scenarios_requiring_external_review"] >= 1
    assert summary["scenarios_locked_for_external_review"] >= 1
    assert summary["scenarios_suppressed_until_calibrated"] >= 1
    assert summary["scenarios_requiring_evidence_queue"] >= 1
    assert summary["scenarios_requiring_grouped_entity_queue"] >= 1
    assert summary["scenarios_requiring_transfer_pricing_queue"] >= 1
    assert summary["scenarios_requiring_sector_schedule_queue"] >= 1
    assert summary["scenarios_requiring_aava_review_queue"] >= 1
    assert summary["scenarios_requiring_capital_base_review_queue"] >= 1
    assert summary["scenarios_requiring_offshore_attribution_queue"] >= 1
    assert summary["scenarios_requiring_privacy_review_queue"] >= 1
    assert summary["scenarios_requiring_legal_policy_queue"] >= 1
    assert summary["scenarios_requiring_ato_methods_queue"] >= 1
    assert summary["scenarios_requiring_treasury_methods_queue"] >= 1
    assert summary["firm_level_liability_logic_modified"] is False
    assert summary["real_enforcement_created"] is False
    assert summary["real_ato_power_claimed"] is False
    assert summary["compliance_scoring_created"] is False
    assert summary["notices_issued"] is False
    assert summary["real_data_used"] is False


def test_administrative_workflow_report_contains_required_table(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-administrative-workflow-table"
    subprocess.run(
        [sys.executable, "scripts/run_administrative_compliance_workflow.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "administrative_compliance_workflow.md").read_text(encoding="utf-8")

    assert "Scenario ID | Scenario Name | Sector Schedule | Linked Behavioural Responses" in markdown
    assert "Evidence Bundle Size | Workflow Decision Band | Workflow Status" in markdown
    assert "External Review Required | Do Not Enforce | Main Reason" in markdown


def test_administrative_workflow_report_has_no_forbidden_operational_language(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-administrative-workflow-forbidden"
    subprocess.run(
        [sys.executable, "scripts/run_administrative_compliance_workflow.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in reports_dir.glob("administrative_compliance_workflow.*")
    )

    for phrase in FORBIDDEN_PHRASES:
        assert phrase not in combined


def test_streamlit_administrative_workflow_page_imports_without_error(repo_root) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('simulator/pages/23_Administrative_Workflow.py', run_name='__main__')",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_ci_runs_administrative_workflow_runner_after_behavioural_response(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    behavioural_index = workflow.index("python scripts/run_behavioural_response_simulation.py")
    administrative_index = workflow.index("python scripts/run_administrative_compliance_workflow.py")
    guardrail_index = workflow.index("python scripts/run_repo_guardrails.py")

    assert behavioural_index < administrative_index < guardrail_index
