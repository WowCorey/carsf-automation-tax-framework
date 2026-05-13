from __future__ import annotations

import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = PROJECT_ROOT / "model" / "tests" / "fixtures" / "repo_guardrails"
SCRIPT = PROJECT_ROOT / "scripts" / "run_repo_guardrails.py"


def run_script(root: Path, reports_dir: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--root", str(root), "--reports-dir", str(reports_dir)],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def test_run_repo_guardrails_exits_nonzero_on_denied_findings(tmp_path):
    completed = run_script(FIXTURES / "bad_secret_marker_fixture", tmp_path / "reports")

    assert completed.returncode == 1
    assert "denied findings:" in completed.stdout
    assert "DENY" in completed.stderr


def test_run_repo_guardrails_exits_zero_on_clean_fixture(tmp_path):
    reports_dir = tmp_path / "reports"
    completed = run_script(FIXTURES / "clean_repo_fixture", reports_dir)

    assert completed.returncode == 0
    assert "repo guardrails clean: true" in completed.stdout
    assert (reports_dir / "repo_guardrails.md").exists()
    assert (reports_dir / "repo_guardrails.json").exists()


def test_ci_workflow_runs_repo_guardrails():
    workflow = (PROJECT_ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "python scripts/run_repo_guardrails.py" in workflow


def test_repo_guardrail_report_contains_non_claims():
    report_path = PROJECT_ROOT / "reports" / "repo_guardrails.md"
    if not report_path.exists():
        completed = run_script(PROJECT_ROOT, PROJECT_ROOT / "reports")
        assert completed.returncode == 0
    report = report_path.read_text(encoding="utf-8").lower()

    assert "not a complete dlp" in report
    assert "legal/privacy audit" in report
    assert "treasury control" in report
    assert "ato control" in report


def test_streamlit_repository_guardrails_page_imports_without_error():
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('simulator/pages/11_Repository_Guardrails.py', run_name='__main__')",
        ],
        cwd=PROJECT_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr
