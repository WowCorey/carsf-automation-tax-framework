from __future__ import annotations

import json
import subprocess
import sys

from carsf.external_review_attack_pack import (
    EXTERNAL_REVIEW_ATTACK_PACK_WARNING,
    find_forbidden_affirmative_attack_pack_claims,
)


def test_external_review_attack_pack_report_generates_json_and_markdown(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-external-review-attack-pack"
    completed = subprocess.run(
        [sys.executable, "scripts/run_external_review_attack_pack.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "external_review_attack_pack.md").exists()
    assert (reports_dir / "external_review_attack_pack.json").exists()


def test_external_review_attack_pack_report_includes_non_claims_and_false_flags(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-external-review-attack-pack-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_external_review_attack_pack.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "external_review_attack_pack.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "external_review_attack_pack.json").read_text(encoding="utf-8"))

    assert EXTERNAL_REVIEW_ATTACK_PACK_WARNING in markdown
    assert EXTERNAL_REVIEW_ATTACK_PACK_WARNING in payload["metadata"]["non_claims"]
    for key in [
        "review_completed",
        "approval_claimed",
        "validation_claimed",
        "readiness_score_created",
        "legal_sufficiency_claimed",
        "operational_readiness_claimed",
        "legislative_readiness_claimed",
        "official_status_claimed",
        "real_data_used",
        "firm_level_liability_logic_modified",
    ]:
        assert payload["metadata"][key] is False
        assert payload["summary"][key] is False


def test_external_review_attack_pack_report_contains_major_sections(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-external-review-attack-pack-sections"
    subprocess.run(
        [sys.executable, "scripts/run_external_review_attack_pack.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "external_review_attack_pack.md").read_text(encoding="utf-8")

    for heading in [
        "## D. Review Track Index",
        "## E. Cross-Cutting Boundary Checks",
        "## F. Policy Review Attacks",
        "## G. Technical Review Attacks",
        "## H. Legal Review Attacks",
        "## I. Tax Review Attacks",
        "## J. ATO Methods Review Attacks",
        "## K. Treasury Methods Review Attacks",
        "## L. Privacy / Secrecy Review Attacks",
        "## M. Statistical Methods Review Attacks",
        "## N. Economic Methods Review Attacks",
        "## O. Welfare Policy Review Attacks",
        "## P. Parliamentary Counsel Review Attacks",
        "## Q. Hostile / Red-Team Attacks",
        "## R. Report-by-Report Attack Matrix",
        "## S. Layer-by-Layer Attack Matrix",
        "## T. Locked-Until-Review Items",
        "## U. Required External Inputs",
        "## V. Suggested Reviewer Output Format",
        "## W. Limitations and Future Work",
    ]:
        assert heading in markdown


def test_external_review_attack_pack_report_has_no_forbidden_affirmative_claims(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-external-review-attack-pack-forbidden"
    subprocess.run(
        [sys.executable, "scripts/run_external_review_attack_pack.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in reports_dir.glob("external_review_attack_pack.*"))

    assert find_forbidden_affirmative_attack_pack_claims(combined) == []


def test_attack_pack_release_documents_have_non_claims_and_no_forbidden_affirmative_claims(repo_root) -> None:
    docs_dir = repo_root / "release" / "v1_5_rc" / "attack_pack"
    for path in sorted(docs_dir.iterdir()):
        if path.suffix not in {".md", ".json"}:
            continue
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()

        assert "does not mean external review has been completed" in lowered
        assert "does not mean approval has been granted" in lowered
        assert "does not mean validation has occurred" in lowered
        assert "not legal advice" in lowered
        assert "not tax advice" in lowered
        assert "not ato guidance" in lowered
        assert "does not modify firm-level carsf liability" in lowered
        assert find_forbidden_affirmative_attack_pack_claims(text) == []


def test_ci_runs_attack_pack_runner_after_release_pack(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    release_index = workflow.index("python scripts/run_v1_5_release_candidate_pack.py")
    attack_index = workflow.index("python scripts/run_external_review_attack_pack.py")
    evidence_index = workflow.index("python scripts/run_evidence_workflow.py")
    guardrail_index = workflow.index("python scripts/run_repo_guardrails.py")

    assert release_index < attack_index < evidence_index < guardrail_index


def test_main_streamlit_app_imports_cleanly_after_attack_pack(repo_root) -> None:
    completed = subprocess.run(
        [sys.executable, "-c", "import runpy; runpy.run_path('simulator/app.py', run_name='__main__')"],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
