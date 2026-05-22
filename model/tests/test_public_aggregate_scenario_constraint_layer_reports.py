from __future__ import annotations

import json
import subprocess
import sys

from carsf.public_aggregate_scenario_constraint_layer import (
    SCENARIO_CONSTRAINT_WARNING,
    find_forbidden_affirmative_scenario_constraint_claims,
)


def test_scenario_constraint_layer_report_generates_json_and_markdown(repo_root, tmp_path) -> None:
    reports_dir = tmp_path / "reports"
    completed = subprocess.run(
        [
            sys.executable,
            "scripts/run_public_aggregate_scenario_constraint_layer.py",
            "--reports-dir",
            str(reports_dir),
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "public_aggregate_scenario_constraint_layer.md").exists()
    assert (reports_dir / "public_aggregate_scenario_constraint_layer.json").exists()


def test_scenario_constraint_layer_report_sections_and_non_claims(repo_root, tmp_path) -> None:
    reports_dir = tmp_path / "reports"
    subprocess.run(
        [sys.executable, "scripts/run_public_aggregate_scenario_constraint_layer.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "public_aggregate_scenario_constraint_layer.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "public_aggregate_scenario_constraint_layer.json").read_text(encoding="utf-8"))

    for heading in [
        "## A. Purpose",
        "## B. Non-Claims",
        "## C. Input Public Aggregate Values",
        "## D. Scenario Output Status Taxonomy",
        "## E. Display Rule Taxonomy",
        "## F. Forbidden Implication Taxonomy",
        "## G. Constraint Status Taxonomy",
        "## H. Claim Level Taxonomy",
        "## I. Module Scenario Constraints",
        "## J. Field Scenario Constraints",
        "## K. Outputs Displayed As Sanity Check Only",
        "## L. Outputs Displayed As Public Aggregate Anchor Only",
        "## M. Outputs Displayed As Public Aggregate Bound Only",
        "## N. Outputs Displayed As Context Only",
        "## O. Outputs Displayed As Placeholder Narrowing Only",
        "## P. Outputs Displayed As Reviewer Traceability Only",
        "## Q. Outputs Marked Non-Interpretable",
        "## R. Outputs Hidden From Reviewer Dashboard",
        "## S. Forbidden Implications Mapped",
        "## T. What Can Be Displayed",
        "## U. What Must Be Hidden Or Marked Non-Interpretable",
        "## V. Evidence Needed To Lift Constraints",
        "## W. Build 35 Readiness",
        "## X. Limitations and Future Work",
    ]:
        assert heading in markdown

    assert "Outputs Hidden From Reviewer Dashboard" in markdown
    assert SCENARIO_CONSTRAINT_WARNING in markdown
    assert SCENARIO_CONSTRAINT_WARNING in payload["metadata"]["non_claims"]


def test_scenario_constraint_layer_report_summary_flags_and_forbidden_claims(repo_root, tmp_path) -> None:
    reports_dir = tmp_path / "reports"
    subprocess.run(
        [sys.executable, "scripts/run_public_aggregate_scenario_constraint_layer.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "public_aggregate_scenario_constraint_layer.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "public_aggregate_scenario_constraint_layer.json").read_text(encoding="utf-8"))
    combined = markdown + "\n" + json.dumps(payload, sort_keys=True)
    summary = payload["summary"]

    assert summary["public_aggregate_scenario_constraint_layer_created"] is True
    assert summary["new_data_loaded"] is False
    assert summary["loaded_public_values_used"] == 10
    assert summary["module_constraints_mapped"] == 20
    assert summary["field_constraints_mapped"] == 11
    assert summary["outputs_marked_non_interpretable"] >= 3
    assert summary["outputs_hidden_from_reviewer_dashboard"] >= 1
    assert summary["public_source_candidates_treated_as_loaded"] is False
    assert summary["restricted_data_loaded"] is False
    assert summary["personal_data_loaded"] is False
    assert summary["taxpayer_level_data_loaded"] is False
    assert summary["firm_confidential_data_loaded"] is False
    assert summary["household_microdata_loaded"] is False
    assert summary["calibration_completed"] is False
    assert summary["validation_claimed"] is False
    assert summary["actual_tax_payable_determined"] is False
    assert summary["official_status_claimed"] is False
    assert summary["firm_level_liability_logic_modified"] is False
    assert find_forbidden_affirmative_scenario_constraint_claims(combined) == []


def test_ci_runs_scenario_constraint_layer_after_calibration_boundary_map(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    boundary_index = workflow.index("python scripts/run_public_aggregate_calibration_boundary_map.py")
    scenario_index = workflow.index("python scripts/run_public_aggregate_scenario_constraint_layer.py")
    evidence_index = workflow.index("python scripts/run_evidence_workflow.py")

    assert boundary_index < scenario_index < evidence_index
