from __future__ import annotations

import json
import subprocess
import sys


def test_ingestion_reports_generate(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-ingestion-reports"
    completed = subprocess.run(
        [sys.executable, "scripts/run_ingestion_controls.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "secure_ingestion_controls.md").exists()
    assert (reports_dir / "secure_ingestion_controls.json").exists()


def test_ingestion_report_contains_required_non_claims(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-ingestion-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_ingestion_controls.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "secure_ingestion_controls.md").read_text(encoding="utf-8").lower()
    payload = json.loads((reports_dir / "secure_ingestion_controls.json").read_text(encoding="utf-8"))

    assert "prototype governance controls only" in markdown
    assert "do not create legal, privacy, cybersecurity" in markdown
    assert payload["metadata"]["status"] == "prototype_secure_ingestion_controls_only"


def test_existing_example_and_evidence_workflow_reports_still_generate(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-existing-plus-ingestion"
    examples = subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )
    evidence = subprocess.run(
        [sys.executable, "scripts/run_evidence_workflow.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert examples.returncode == 0, examples.stderr
    assert evidence.returncode == 0, evidence.stderr
    assert (reports_dir / "example_results.md").exists()
    assert (reports_dir / "mock_evidence_workflow.md").exists()
    assert "Secure Ingestion Controls" in (reports_dir / "mock_evidence_workflow.md").read_text(encoding="utf-8")


def test_streamlit_secure_ingestion_page_imports_without_error(repo_root) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('simulator/pages/10_Secure_Ingestion_Controls.py', run_name='__main__')",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_no_ingestion_report_claims_validation(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-ingestion-claims"
    subprocess.run(
        [sys.executable, "scripts/run_ingestion_controls.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in reports_dir.glob("*.md")).lower()
    forbidden_claims = [
        "legally validated",
        "privacy validated",
        "cybersecurity validated",
        "ato validated",
        "treasury validated",
        "tax validated",
        "audit validated",
        "real evidence is allowed",
    ]

    for claim in forbidden_claims:
        assert claim not in combined
