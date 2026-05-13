from __future__ import annotations

import json
import subprocess
import sys

from carsf.aggregation import risk_rank
from carsf.example_runner import EXAMPLE_IDS, run_all_examples
from carsf.group_runner import run_grouped_previews, standalone_max_risk


def test_split_structure_group_risk_is_at_least_standalone_fragments(repo_root) -> None:
    preview = run_grouped_previews(repo_root)

    assert risk_rank(preview.aggregation_result.risk_level) >= risk_rank(standalone_max_risk(preview.split_entities))
    assert preview.aggregation_result.review_required is True


def test_hybrid_stress_variant_has_intermediate_nltg(repo_root) -> None:
    base_results = {result.id: result for result in run_all_examples(repo_root)}
    preview = run_grouped_previews(repo_root)
    stress_nltg = preview.hybrid_stress_result.outputs.nltg

    assert base_results["logistics_human_heavy"].outputs.nltg < stress_nltg
    assert stress_nltg < base_results["logistics_ai_platform"].outputs.nltg


def test_existing_six_examples_still_run(repo_root) -> None:
    results = run_all_examples(repo_root)

    assert [result.id for result in results] == EXAMPLE_IDS
    assert len(results) == 6


def test_existing_and_grouped_reports_generate(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-grouped-reports"
    completed = subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "example_results.md").exists()
    assert (reports_dir / "example_results.json").exists()
    assert (reports_dir / "grouped_entity_results.md").exists()
    assert (reports_dir / "grouped_entity_results.json").exists()


def test_grouped_json_report_contains_required_outputs(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-grouped-json"
    subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    payload = json.loads((reports_dir / "grouped_entity_results.json").read_text(encoding="utf-8"))

    assert payload["metadata"]["status"] == "illustrative_grouped_entity_and_apportionment_previews_only"
    assert payload["aggregation_result"]["risk_level"] == "high"
    assert payload["apportionment_result"]["valid"] is True
    assert payload["hybrid_stress_result"]["id"] == "logistics_hybrid_stress"


def test_grouped_markdown_report_contains_required_sections(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-grouped-md"
    subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "grouped_entity_results.md").read_text(encoding="utf-8")

    assert "## A. Grouped-Entity Aggregation Overview" in markdown
    assert "## G. Mixed-Activity / Prototype Apportionment Example" in markdown
    assert "## I. Hybrid Logistics Stress Variant" in markdown
    assert "| Example | Standalone Risk | Group Risk | Aggregation Needed | Apportionment Needed | Main Reason |" in markdown
    assert "not final cross-sector schedule blending" in markdown


def test_grouped_json_report_contains_apportionment_scope_note(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-grouped-json-note"
    subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    payload = json.loads((reports_dir / "grouped_entity_results.json").read_text(encoding="utf-8"))
    combined = json.dumps(payload).lower()

    assert "not final cross-sector schedule blending" in combined


def test_grouped_report_does_not_claim_legal_grouping_or_tax_validation(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-grouped-claims"
    subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = (
        (reports_dir / "grouped_entity_results.md").read_text(encoding="utf-8")
        + (reports_dir / "grouped_entity_results.json").read_text(encoding="utf-8")
    ).lower()

    forbidden_claims = [
        "legally validated",
        "tax validated",
        "treasury validated",
        "ato validated",
        "is a tax assessment",
        "actual tax payable is",
        "real tax payable is",
    ]
    for claim in forbidden_claims:
        assert claim not in combined
