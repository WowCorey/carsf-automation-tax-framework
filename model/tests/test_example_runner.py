from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from carsf.example_runner import EXAMPLE_IDS, run_all_examples


def results_by_id(repo_root: Path):
    return {result.id: result for result in run_all_examples(repo_root)}


def test_all_six_examples_load(repo_root: Path) -> None:
    results = run_all_examples(repo_root)

    assert [result.id for result in results] == EXAMPLE_IDS


def test_all_six_examples_run_without_error(repo_root: Path) -> None:
    results = run_all_examples(repo_root)

    assert len(results) == 6
    assert all(result.outputs.opfte_libc > 0 for result in results)


def test_traditional_mechanic_has_lower_or_equal_nltg_than_robotic(repo_root: Path) -> None:
    results = results_by_id(repo_root)

    assert results["mechanic_traditional"].outputs.nltg <= results["mechanic_robotic"].outputs.nltg


def test_ai_admin_mechanic_has_lower_nltg_than_robotic(repo_root: Path) -> None:
    results = results_by_id(repo_root)

    assert results["mechanic_ai_admin"].outputs.nltg < results["mechanic_robotic"].outputs.nltg


def test_human_heavy_logistics_has_lower_nltg_than_ai_platform(repo_root: Path) -> None:
    results = results_by_id(repo_root)

    assert results["logistics_human_heavy"].outputs.nltg < results["logistics_ai_platform"].outputs.nltg


def test_hybrid_logistics_sits_between_human_and_platform_where_supported(repo_root: Path) -> None:
    results = results_by_id(repo_root)
    human = results["logistics_human_heavy"].outputs
    hybrid = results["logistics_hybrid"].outputs
    platform = results["logistics_ai_platform"].outputs

    assert human.nltg <= hybrid.nltg <= platform.nltg
    assert human.aii < hybrid.aii < platform.aii


def test_hybrid_interpretation_matches_zero_nltg_and_liability(repo_root: Path) -> None:
    result = results_by_id(repo_root)["logistics_hybrid"]
    interpretation = result.interpretation.lower()

    assert result.outputs.nltg == 0
    assert result.outputs.liability == 0
    assert "aii is intermediate" in interpretation
    assert "nltg and liability remain zero" in interpretation
    assert "qlc remains strong" in interpretation
    assert "not automatically penalised" in interpretation
    assert "non-zero but intermediate nltg" in interpretation


def test_reports_are_generated(repo_root: Path) -> None:
    reports_dir = repo_root / "tmp" / "test-example-reports"
    completed = subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "example_results.json").exists()
    assert (reports_dir / "example_results.md").exists()


def test_json_output_contains_required_fields(repo_root: Path) -> None:
    reports_dir = repo_root / "tmp" / "test-example-json"
    subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    payload = json.loads((reports_dir / "example_results.json").read_text(encoding="utf-8"))

    assert set(payload["metadata"]) >= {"generated_at", "version", "status", "non_claims"}
    assert payload["metadata"]["status"] == "illustrative_placeholder_outputs_only"
    assert len(payload["examples"]) == 6
    required_example_fields = {
        "id",
        "name",
        "schedule",
        "inputs",
        "outputs",
        "interpretation",
        "warnings",
        "evidence_labels",
    }
    required_output_fields = {
        "qlc",
        "opfte_libc",
        "hle",
        "aii",
        "nltg",
        "aava",
        "ael_raw",
        "ael_payable",
        "shortfall",
        "arl",
        "credits",
        "liability",
        "coverage_ratio",
        "cars_i",
    }
    for example in payload["examples"]:
        assert set(example) >= required_example_fields
        assert set(example["outputs"]) >= required_output_fields
        assert any("placeholder" in label.lower() for label in example["evidence_labels"])


def test_markdown_output_contains_comparison_table(repo_root: Path) -> None:
    reports_dir = repo_root / "tmp" / "test-example-md"
    subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "example_results.md").read_text(encoding="utf-8")

    assert "## Summary Comparison" in markdown
    assert "| Example | Sector | QLC | HLE | AII | NLTG | AAVA | AEL Payable | ARL | Final Liability | Main Interpretation |" in markdown
    for example_id in EXAMPLE_IDS:
        assert example_id.replace("_", " ").title() in markdown


def test_reports_do_not_claim_real_tax_liability(repo_root: Path) -> None:
    reports_dir = repo_root / "tmp" / "test-example-claims"
    subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = (
        (reports_dir / "example_results.md").read_text(encoding="utf-8")
        + (reports_dir / "example_results.json").read_text(encoding="utf-8")
    ).lower()

    forbidden_claims = [
        "actual tax payable",
        "ato validated",
        "treasury validated",
        "legally validated",
        "real tax liability",
    ]
    for claim in forbidden_claims:
        assert claim not in combined
