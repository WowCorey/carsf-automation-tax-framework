from __future__ import annotations

import json
import subprocess
import sys

from carsf.legislative_architecture import (
    LEGISLATIVE_ARCHITECTURE_WARNING,
    find_forbidden_affirmative_claims,
)


def test_legislative_architecture_report_generates_json_and_markdown(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-legislative-architecture"
    completed = subprocess.run(
        [sys.executable, "scripts/run_legislative_architecture.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "legislative_architecture.md").exists()
    assert (reports_dir / "legislative_architecture.json").exists()


def test_legislative_architecture_report_includes_non_claim_language_and_flags(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-legislative-architecture-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_legislative_architecture.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "legislative_architecture.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "legislative_architecture.json").read_text(encoding="utf-8"))

    assert LEGISLATIVE_ARCHITECTURE_WARNING in markdown
    assert LEGISLATIVE_ARCHITECTURE_WARNING in payload["metadata"]["non_claims"]
    for key in [
        "operative_law_created",
        "legal_sufficiency_claimed",
        "statutory_power_created",
        "notices_created",
        "penalties_created",
        "enforcement_created",
        "real_data_used",
        "firm_level_liability_logic_modified",
    ]:
        assert payload["metadata"][key] is False
        assert payload["summary"][key] is False


def test_legislative_architecture_report_contains_required_sections(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-legislative-architecture-sections"
    subprocess.run(
        [sys.executable, "scripts/run_legislative_architecture.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "legislative_architecture.md").read_text(encoding="utf-8")

    for heading in [
        "## E. Proposed Parts",
        "## F. Proposed Divisions",
        "## G. Definition Placeholders",
        "## H. Sector Schedule Placeholders",
        "## M. Evidence and Information Architecture Placeholders",
        "## N. Review Rights and Safeguards Placeholders",
        "## P. Regulation-Making Placeholders",
        "## R. External Review Blockers",
    ]:
        assert heading in markdown


def test_legislative_architecture_report_contains_required_tables(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-legislative-architecture-tables"
    subprocess.run(
        [sys.executable, "scripts/run_legislative_architecture.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "legislative_architecture.md").read_text(encoding="utf-8")

    assert "Part ID | Part Title | Purpose | Linked CARSF Modules" in markdown
    assert "Term | Plain-English Description | Linked Module or Doc" in markdown
    assert "Schedule ID | Schedule Name | Source YAML | Calibration Status" in markdown
    assert "Placeholder ID | Title | Type | Conceptual Scope" in markdown


def test_legislative_architecture_report_has_no_forbidden_affirmative_legal_claims(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-legislative-architecture-forbidden"
    subprocess.run(
        [sys.executable, "scripts/run_legislative_architecture.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in reports_dir.glob("legislative_architecture.*")
    )

    assert find_forbidden_affirmative_claims(combined) == []


def test_streamlit_legislative_architecture_page_imports_without_error(repo_root) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('simulator/pages/24_Legislative_Architecture.py', run_name='__main__')",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_ci_runs_legislative_architecture_runner_before_evidence_and_guardrails(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    administrative_index = workflow.index("python scripts/run_administrative_compliance_workflow.py")
    legislative_index = workflow.index("python scripts/run_legislative_architecture.py")
    evidence_index = workflow.index("python scripts/run_evidence_workflow.py")
    guardrail_index = workflow.index("python scripts/run_repo_guardrails.py")

    assert administrative_index < legislative_index < evidence_index < guardrail_index
