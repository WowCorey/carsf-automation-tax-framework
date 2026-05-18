from __future__ import annotations

import json
import subprocess
import sys

from carsf.release_candidate_pack import (
    RELEASE_CANDIDATE_WARNING,
    find_forbidden_affirmative_release_claims,
)


def test_release_candidate_pack_report_generates_json_and_markdown(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-release-candidate-pack"
    completed = subprocess.run(
        [sys.executable, "scripts/run_v1_5_release_candidate_pack.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "v1_5_release_candidate_pack.md").exists()
    assert (reports_dir / "v1_5_release_candidate_pack.json").exists()


def test_release_candidate_pack_report_includes_non_claim_language_and_false_flags(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-release-candidate-pack-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_v1_5_release_candidate_pack.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "v1_5_release_candidate_pack.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "v1_5_release_candidate_pack.json").read_text(encoding="utf-8"))

    assert RELEASE_CANDIDATE_WARNING in markdown
    assert RELEASE_CANDIDATE_WARNING in payload["metadata"]["non_claims"]
    for key in [
        "real_data_used",
        "readiness_score_created",
        "operational_readiness_claimed",
        "legal_sufficiency_claimed",
        "legislative_readiness_claimed",
        "economic_validation_claimed",
        "welfare_validation_claimed",
        "statistical_validation_claimed",
        "official_status_claimed",
        "firm_level_liability_logic_modified",
    ]:
        assert payload["metadata"][key] is False
        assert payload["summary"][key] is False


def test_release_candidate_pack_report_contains_required_sections(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-release-candidate-pack-sections"
    subprocess.run(
        [sys.executable, "scripts/run_v1_5_release_candidate_pack.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "v1_5_release_candidate_pack.md").read_text(encoding="utf-8")

    for heading in [
        "## C. Release Pack Contents",
        "## D. Working Paper Update Summary",
        "## E. Prototype Stack Summary",
        "## F. Generated Report Map",
        "## G. Release Documents",
        "## H. Suggested Reviewer Routing",
        "## I. Calibration Blockers",
        "## J. External Review Blockers",
        "## Q. Missing Items / Release Gaps",
    ]:
        assert heading in markdown


def test_release_candidate_pack_report_has_no_forbidden_affirmative_claims(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-release-candidate-pack-forbidden"
    subprocess.run(
        [sys.executable, "scripts/run_v1_5_release_candidate_pack.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in reports_dir.glob("v1_5_release_candidate_pack.*"))

    assert find_forbidden_affirmative_release_claims(combined) == []


def test_release_documents_have_non_claims_and_no_forbidden_affirmative_claims(repo_root) -> None:
    for path in sorted((repo_root / "release" / "v1_5_rc").iterdir()):
        if path.suffix not in {".md", ".json"}:
            continue
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()

        assert "not legal advice" in lowered
        assert "not tax advice" in lowered
        assert "not ato guidance" in lowered
        assert "does not modify firm-level carsf liability" in lowered
        assert find_forbidden_affirmative_release_claims(text) == []


def test_main_streamlit_app_imports_cleanly(repo_root) -> None:
    completed = subprocess.run(
        [sys.executable, "-c", "import runpy; runpy.run_path('simulator/app.py', run_name='__main__')"],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_ci_runs_release_candidate_pack_runner_after_executive_dashboard(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    dashboard_index = workflow.index("python scripts/run_executive_dashboard.py")
    release_index = workflow.index("python scripts/run_v1_5_release_candidate_pack.py")
    evidence_index = workflow.index("python scripts/run_evidence_workflow.py")
    guardrail_index = workflow.index("python scripts/run_repo_guardrails.py")

    assert dashboard_index < release_index < evidence_index < guardrail_index
