from __future__ import annotations

import json
import subprocess
import sys


def test_risk_outputs_appear_in_json_reports(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-risk-json"
    completed = subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    payload = json.loads((reports_dir / "example_results.json").read_text(encoding="utf-8"))
    for example in payload["examples"]:
        assert "safe_harbour_result" in example
        assert "avoidance_result" in example
        assert "grouping_risk_result" in example
        assert "category" in example["safe_harbour_result"]
        assert "risk_level" in example["avoidance_result"]
        assert "risk_level" in example["grouping_risk_result"]


def test_risk_outputs_appear_in_markdown_reports(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-risk-md"
    completed = subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    markdown = (reports_dir / "example_results.md").read_text(encoding="utf-8")

    assert "## Safe Harbour and Review Flags" in markdown
    assert "### G. Safe Harbour Assessment" in markdown
    assert "### H. Avoidance / Gaming Risk Assessment" in markdown
    assert "### I. Grouped-Entity Review Flag" in markdown
    assert "WORKER_ASSIST_OR_ADMIN_AI" in markdown
    assert "OFFSHORE_AUTOMATION_SERVICE" in markdown


def test_reports_do_not_claim_legal_tax_treasury_or_ato_validation(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-risk-claims"
    completed = subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    combined = (
        (reports_dir / "example_results.md").read_text(encoding="utf-8")
        + (reports_dir / "example_results.json").read_text(encoding="utf-8")
    ).lower()

    forbidden_claims = [
        "is a legal finding",
        "is a tax finding",
        "treasury validated",
        "ato validated",
        "legal conclusion",
        "actual tax payable is",
        "real tax payable is",
    ]
    for claim in forbidden_claims:
        assert claim not in combined
