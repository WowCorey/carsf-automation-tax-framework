from __future__ import annotations

import json
import subprocess
import sys

from carsf.evidence import assess_evidence
from carsf.evidence_packet import load_evidence_packet


def test_mock_evidence_upgrades_only_to_prototype_status(repo_root) -> None:
    packet = load_evidence_packet(repo_root / "data" / "mock_evidence" / "mechanic_ai_admin_mock_packet.yaml")
    assessment = assess_evidence(
        {"status": "illustrative_placeholder", "placeholder_notice": "synthetic mock evidence workflow only"},
        packet.created_for,
        evidence_packet=packet,
    )

    assert assessment.status in {"partial", "sufficient_for_prototype"}
    assert assessment.status != "sufficient"
    assert "real-world sufficiency" in " ".join(assessment.warnings)


def test_mock_evidence_workflow_report_generates(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-mock-evidence-workflow"
    completed = subprocess.run(
        [sys.executable, "scripts/run_evidence_workflow.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "mock_evidence_workflow.md").exists()
    assert (reports_dir / "mock_evidence_workflow.json").exists()


def test_mock_evidence_report_contains_required_non_claims(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-mock-evidence-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_evidence_workflow.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "mock_evidence_workflow.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "mock_evidence_workflow.json").read_text(encoding="utf-8"))

    markdown_lower = markdown.lower()
    assert "synthetic mock evidence only" in markdown_lower
    assert "do not validate any real liability" in markdown_lower
    assert payload["metadata"]["status"] == "synthetic_mock_evidence_workflow_only"


def test_existing_reports_still_generate_with_mock_workflow_link(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-existing-reports-with-mock-link"
    completed = subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    evidence_report = (reports_dir / "evidence_requirements.md").read_text(encoding="utf-8")
    assert "Controlled Mock Evidence Workflow" in evidence_report
    assert "mock_evidence_workflow.md" in evidence_report


def test_streamlit_mock_evidence_page_imports_without_error(repo_root) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('simulator/pages/9_Mock_Evidence_Workflow.py', run_name='__main__')",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
