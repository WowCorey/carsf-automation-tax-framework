from __future__ import annotations

import json
import subprocess
import sys


def test_evidence_and_calibration_reports_generate(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-evidence-reports"
    completed = subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "example_results.md").exists()
    assert (reports_dir / "grouped_entity_results.md").exists()
    assert (reports_dir / "transfer_pricing_results.md").exists()
    assert (reports_dir / "evidence_requirements.md").exists()
    assert (reports_dir / "evidence_requirements.json").exists()
    assert (reports_dir / "calibration_requirements.md").exists()
    assert (reports_dir / "calibration_requirements.json").exists()


def test_evidence_report_contains_placeholder_statuses(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-evidence-json"
    subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    payload = json.loads((reports_dir / "evidence_requirements.json").read_text(encoding="utf-8"))

    assert payload["metadata"]["status"] == "prototype_evidence_requirements_only"
    assert payload["example_evidence_summary"]
    assert all(item["status"] in {"placeholder_only", "insufficient", "partial"} for item in payload["example_evidence_summary"])


def test_calibration_report_contains_no_fake_values_flag(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-calibration-json"
    subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    payload = json.loads((reports_dir / "calibration_requirements.json").read_text(encoding="utf-8"))

    assert payload["metadata"]["status"] == "prototype_calibration_shell_only"
    assert payload["metadata"]["no_fake_calibration_values"] is True


def test_reports_do_not_claim_validation(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-evidence-claims"
    subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in reports_dir.glob("*.md")).lower()
    forbidden_claims = [
        "legally validated",
        "tax validated",
        "treasury validated",
        "ato validated",
        "economically validated",
        "actual tax payable is",
        "real tax payable is",
    ]

    for claim in forbidden_claims:
        assert claim not in combined


def test_streamlit_evidence_page_imports_without_error(repo_root) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('simulator/pages/8_Evidence_and_Calibration.py', run_name='__main__')",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
