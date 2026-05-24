from __future__ import annotations

import json
import re


def test_github_pages_site_contains_required_reviewer_sections(repo_root) -> None:
    html = (repo_root / "site" / "index.html").read_text(encoding="utf-8")

    for text in [
        "CARSF Automation Tax Framework",
        "A prototype Australian policy and modelling framework for examining automation-driven labour-tax-base risk.",
        "Commonwealth Automation Revenue Stabilisation Framework",
        "What Problem It Tests",
        "What The Model Currently Does",
        "What Is Calculated",
        "What Is Not Calculated",
        "Public Aggregate Data Loaded",
        "Placeholder Replacement Map",
        "Calibration Boundary Map",
        "Scenario Constraint Layer",
        "Full Repo Integrity / Gap Audit",
        "What Data Is Still Missing?",
        "How To Test The Model",
        "How To Read The Reports",
        "What Review Is Still Required?",
    ]:
        assert text in html


def test_github_pages_site_contains_required_non_claims(repo_root) -> None:
    html = (repo_root / "site" / "index.html").read_text(encoding="utf-8")

    for text in [
        "Private research/prototype",
        "Public aggregate anchors only",
        "Placeholder-boundary protected",
        "Not calibrated",
        "Not validated",
        "No tax payable estimate",
        "No firm liability calculation",
        "not law",
        "not legal advice",
        "not tax advice",
        "not ATO guidance",
        "not Treasury modelling",
        "not PBO costing",
        "not official policy",
        "does not determine actual tax payable",
        "does not determine firm-level liability",
    ]:
        assert text.lower() in html.lower()


def test_github_pages_site_uses_local_static_dependencies_only(repo_root) -> None:
    html = (repo_root / "site" / "index.html").read_text(encoding="utf-8")
    css = (repo_root / "site" / "styles.css").read_text(encoding="utf-8")
    js = (repo_root / "site" / "app.js").read_text(encoding="utf-8")
    combined = "\n".join([html, css, js])

    forbidden_patterns = [
        r"<script[^>]+src=[\"']https?://",
        r"<link[^>]+href=[\"']https?://",
        r"<img[^>]+src=[\"']https?://",
        r"@import\s+url\([\"']?https?://",
        r"fonts\.googleapis\.com",
        r"googletagmanager",
        r"google-analytics",
        r"plausible\.io",
        r"\bfetch\s*\(",
        r"XMLHttpRequest",
    ]

    for pattern in forbidden_patterns:
        assert re.search(pattern, combined, flags=re.IGNORECASE) is None

    assert 'href="./styles.css"' in html
    assert 'src="./app.js"' in html
    assert 'src="./assets/carsf-logo.svg"' in html


def test_github_pages_site_reconciles_displayed_counts_with_manifest(repo_root) -> None:
    html = (repo_root / "site" / "index.html").read_text(encoding="utf-8")
    manifest = json.loads((repo_root / "site" / "site_manifest.json").read_text(encoding="utf-8"))
    summary = manifest["source_summary"]

    for expected in [
        summary["loaded_public_aggregate_values"],
        summary["source_candidates_not_loaded"],
        summary["module_scenario_constraints"],
        summary["module_boundaries_mapped"],
        summary["full_repo_critical_findings_remaining"],
    ]:
        assert f">{expected}<" in html or f"{expected} output" in html or f"{expected} forbidden" in html


def test_github_pages_site_links_to_core_reports_and_commands(repo_root) -> None:
    html = (repo_root / "site" / "index.html").read_text(encoding="utf-8")

    for path in [
        "../reports/public_real_data_loader.md",
        "../reports/public_data_placeholder_replacement_map.md",
        "../reports/public_aggregate_calibration_boundary_map.md",
        "../reports/public_aggregate_scenario_constraint_layer.md",
        "../reports/full_repo_integrity_upgrade_audit.md",
        "../reports/repo_guardrails.md",
    ]:
        assert path in html

    for command in [
        "python -m pytest",
        "python -m compileall -q model simulator scripts",
        "python scripts/run_public_real_data_loader.py",
        "python scripts/run_public_data_placeholder_replacement_map.py",
        "python scripts/run_public_aggregate_calibration_boundary_map.py",
        "python scripts/run_public_aggregate_scenario_constraint_layer.py",
        "python scripts/run_full_repo_integrity_upgrade_audit.py",
        "python scripts/build_github_pages_site.py",
        "python scripts/run_repo_guardrails.py",
    ]:
        assert command in html
