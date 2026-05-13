from __future__ import annotations

import json
import subprocess
import sys

from carsf.transfer_runner import TRANSFER_PRICING_REPORT_WARNING, run_transfer_pricing_previews


def test_transfer_pricing_runner_loads_new_preview_examples(repo_root) -> None:
    preview = run_transfer_pricing_previews(repo_root)

    assert preview.related_party_ai_fee.scenario_id == "related_party_ai_fee_structure"
    assert preview.robotics_leasing.scenario_id == "robotics_leasing_structure"
    assert preview.unit_compatibility.compatible is False
    assert preview.mixed_unit_exposure.method == "mixed_units_no_direct_output_or_hle_aggregation"


def test_transfer_pricing_and_existing_reports_generate(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-transfer-pricing-reports"
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
    assert (reports_dir / "transfer_pricing_results.md").exists()
    assert (reports_dir / "transfer_pricing_results.json").exists()


def test_transfer_pricing_json_report_contains_required_outputs(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-transfer-pricing-json"
    subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    payload = json.loads((reports_dir / "transfer_pricing_results.json").read_text(encoding="utf-8"))

    assert payload["metadata"]["status"] == "illustrative_transfer_pricing_and_mixed_unit_previews_only"
    assert TRANSFER_PRICING_REPORT_WARNING in payload["metadata"]["warning"]
    assert payload["related_party_ai_fee"]["adjusted_aava_preview"]["adjusted_aava_preview"] > payload["related_party_ai_fee"]["reported_aava"]
    assert payload["unit_compatibility"]["compatible"] is False


def test_transfer_pricing_report_contains_non_claim_warnings(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-transfer-pricing-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = (
        (reports_dir / "transfer_pricing_results.md").read_text(encoding="utf-8")
        + (reports_dir / "transfer_pricing_results.json").read_text(encoding="utf-8")
    )

    assert "not transfer-pricing adjustments" in combined
    assert "not a tax base" in combined
    assert "Adjusted AAVA is preview-only" in combined


def test_transfer_pricing_report_does_not_claim_real_validation(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-transfer-pricing-claims"
    subprocess.run(
        [sys.executable, "scripts/run_examples.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = (
        (reports_dir / "transfer_pricing_results.md").read_text(encoding="utf-8")
        + (reports_dir / "transfer_pricing_results.json").read_text(encoding="utf-8")
    ).lower()

    forbidden_claims = [
        "legally validated",
        "tax validated",
        "treasury validated",
        "ato validated",
        "oecd validated",
        "beps validated",
        "is a transfer-pricing adjustment",
        "is an ato finding",
        "is treasury guidance",
        "actual tax payable is",
        "real tax payable is",
    ]
    for claim in forbidden_claims:
        assert claim not in combined
