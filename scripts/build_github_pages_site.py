from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]

SITE_FILES = [
    "site/index.html",
    "site/styles.css",
    "site/app.js",
    "site/assets/carsf-logo.svg",
    "site/site_manifest.json",
    "site/README.md",
]

SOURCE_REPORTS = {
    "public_real_data_loader": "reports/public_real_data_loader.json",
    "public_data_placeholder_replacement_map": "reports/public_data_placeholder_replacement_map.json",
    "public_aggregate_calibration_boundary_map": "reports/public_aggregate_calibration_boundary_map.json",
    "public_aggregate_scenario_constraint_layer": "reports/public_aggregate_scenario_constraint_layer.json",
    "full_repo_integrity_upgrade_audit": "reports/full_repo_integrity_upgrade_audit.json",
    "repo_guardrails": "reports/repo_guardrails.json",
}

REQUIRED_HTML_MARKERS = {
    "hero": "CARSF Automation Tax Framework",
    "what_carsf_is": "Commonwealth Automation Revenue Stabilisation Framework",
    "what_problem_it_tests": "What Problem It Tests",
    "what_the_model_currently_does": "What The Model Currently Does",
    "what_is_calculated": "What Is Calculated",
    "what_is_not_calculated": "What Is Not Calculated",
    "public_aggregate_data_loaded": "Public Aggregate Data Loaded",
    "placeholder_replacement_map": "Placeholder Replacement Map",
    "calibration_boundary_map": "Calibration Boundary Map",
    "scenario_constraint_layer": "Scenario Constraint Layer",
    "full_repo_integrity_gap_audit": "Full Repo Integrity / Gap Audit",
    "missing_data": "What Data Is Still Missing?",
    "how_to_test_the_model": "How To Test The Model",
    "how_to_read_reports": "How To Read The Reports",
    "reviewer_pathway": "What Review Is Still Required?",
    "github_pages_setup": "GitHub Pages setup",
}

REQUIRED_NON_CLAIM_TEXT = [
    "private research/prototype",
    "not law",
    "not legal advice",
    "not tax advice",
    "not ATO guidance",
    "not Treasury modelling",
    "not PBO costing",
    "not official policy",
    "not calibrated",
    "not validated",
    "No tax payable estimate",
    "No firm liability calculation",
    "does not determine actual tax payable",
    "does not determine firm-level liability",
]

FORBIDDEN_AFFIRMATIVE_CLAIMS = [
    "calibrated",
    "calibration completed",
    "model works",
    "public data proves",
    "actual tax payable",
    "validated",
    "externally validated",
    "source verified",
    "official policy",
    "official status",
    "ready for government",
    "ready for ATO",
    "ready for Treasury",
    "ready for Parliament",
    "ready for implementation",
    "operationally ready",
    "legally sufficient",
    "Treasury modelling",
    "PBO costing",
    "ATO guidance",
    "economic validation complete",
    "welfare validation complete",
    "statistical validation complete",
    "readiness score",
    "maturity score",
    "approved",
    "representative estimate",
    "population estimate",
    "firm liability",
    "CARSF liability determined",
    "calibrated scenario",
    "scenario validated",
    "scenario proves",
    "implementation ready",
    "compliance score",
    "enforcement score",
]

NEGATION_MARKERS = [
    "not ",
    "not as ",
    "no ",
    "does not ",
    "do not ",
    "must not ",
    "cannot ",
    "is not ",
    "are not ",
    "has not ",
    "without ",
    "doesn't ",
    "isn't ",
    "never ",
    "must_not_claim",
    "must not claim",
    "does not show",
    "not used for",
    "what is not calculated",
    "forbidden use",
    "forbidden uses",
    "forbidden implications",
    "must never imply",
    "must not show",
    "must_not_be_used_for",
    "forbidden_claims",
    "non_claims",
    "not_",
    "misread as",
    "not calculated",
]


@dataclass(frozen=True)
class GithubPagesSiteSummary:
    github_pages_site_created: bool
    static_site_only: bool
    backend_required: bool
    external_api_calls: bool
    scraping: bool
    analytics_or_tracking: bool
    external_cdn_dependencies: bool
    required_site_files_present: bool
    required_sections_present: bool
    source_reports_available: bool
    source_report_counts_reconciled: bool
    non_claim_boundaries_visible: bool
    forbidden_claim_findings: int
    loaded_public_aggregate_values_displayed: int
    source_candidates_not_loaded_displayed: int
    placeholders_mapped_displayed: int
    module_boundaries_mapped_displayed: int
    scenario_constraints_mapped_displayed: int
    full_repo_audit_referenced: bool
    github_pages_workflow_added: bool
    new_data_loaded: bool
    restricted_data_loaded: bool
    personal_data_loaded: bool
    taxpayer_level_data_loaded: bool
    firm_confidential_data_loaded: bool
    household_microdata_loaded: bool
    calibration_completed: bool
    validation_claimed: bool
    actual_tax_payable_determined: bool
    official_status_claimed: bool
    firm_level_liability_logic_modified: bool


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalise_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def is_negated(text: str, start: int) -> bool:
    prefix = text[max(0, start - 800) : start].lower()
    suffix = text[start : start + 80].lower()
    if any(marker in prefix for marker in NEGATION_MARKERS):
        return True
    return any(marker in suffix for marker in [": false", "is false", " false", " no", " only"])


def find_forbidden_affirmative_site_claims(text: str) -> list[str]:
    haystack = normalise_text(text)
    findings: list[str] = []
    for phrase in FORBIDDEN_AFFIRMATIVE_CLAIMS:
        pattern = re.compile(re.escape(phrase.lower()))
        for match in pattern.finditer(haystack):
            if is_negated(haystack, match.start()):
                continue
            findings.append(phrase)
            break
    return sorted(set(findings))


def has_external_dependency(html: str, css: str, js: str) -> bool:
    external_asset_patterns = [
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
    combined = "\n".join([html, css, js])
    return any(re.search(pattern, combined, flags=re.IGNORECASE) for pattern in external_asset_patterns)


def collect_source_counts(repo_root: Path) -> dict[str, int]:
    public_real = load_json(repo_root / SOURCE_REPORTS["public_real_data_loader"])["summary"]
    replacement = load_json(repo_root / SOURCE_REPORTS["public_data_placeholder_replacement_map"])["summary"]
    boundary = load_json(repo_root / SOURCE_REPORTS["public_aggregate_calibration_boundary_map"])["summary"]
    scenario = load_json(repo_root / SOURCE_REPORTS["public_aggregate_scenario_constraint_layer"])["summary"]
    full_audit = load_json(repo_root / SOURCE_REPORTS["full_repo_integrity_upgrade_audit"])["summary"]

    return {
        "loaded_public_aggregate_sources": int(public_real["loaded_sources"]),
        "loaded_public_aggregate_values": int(public_real["loaded_values_total"]),
        "source_candidates_not_loaded": int(public_real["source_candidates_not_loaded"]),
        "placeholders_mapped": int(replacement["placeholders_mapped"]),
        "placeholders_replaced_by_public_anchor": int(replacement["placeholders_replaced_by_public_anchor"]),
        "placeholders_narrowed_by_public_anchor": int(replacement["placeholders_narrowed_by_public_anchor"]),
        "placeholders_informed_by_public_anchor": int(replacement["placeholders_informed_by_public_anchor"]),
        "placeholders_blocked_until_restricted_data": int(replacement["placeholders_blocked_until_restricted_data"]),
        "placeholders_blocked_until_external_review": int(replacement["placeholders_blocked_until_external_review"]),
        "module_boundaries_mapped": int(boundary["module_boundaries_mapped"]),
        "field_boundaries_mapped": int(boundary["field_boundaries_mapped"]),
        "module_scenario_constraints": int(scenario["module_constraints_mapped"]),
        "field_scenario_constraints": int(scenario["field_constraints_mapped"]),
        "full_repo_critical_findings_remaining": int(full_audit["critical_findings_remaining"]),
    }


def build_site_report(repo_root: Path) -> dict[str, Any]:
    site_paths = [repo_root / file_path for file_path in SITE_FILES]
    html_path = repo_root / "site" / "index.html"
    css_path = repo_root / "site" / "styles.css"
    js_path = repo_root / "site" / "app.js"
    manifest_path = repo_root / "site" / "site_manifest.json"

    html = read_text(html_path)
    css = read_text(css_path)
    js = read_text(js_path)
    manifest = load_json(manifest_path)
    source_counts = collect_source_counts(repo_root)
    manifest_counts = manifest["source_summary"]
    combined_text = "\n".join(
        [
            html,
            css,
            js,
            json.dumps(manifest, indent=2, sort_keys=True),
            read_text(repo_root / "site" / "README.md"),
        ]
    )

    file_checks = [
        {"path": str(path.relative_to(repo_root)).replace("\\", "/"), "exists": path.exists()}
        for path in site_paths
    ]
    section_checks = [
        {"section": section, "marker": marker, "present": marker in html}
        for section, marker in REQUIRED_HTML_MARKERS.items()
    ]
    report_checks = [
        {"report": label, "path": path, "exists": (repo_root / path).exists()}
        for label, path in SOURCE_REPORTS.items()
    ]
    count_reconciliations = [
        {
            "count_name": key,
            "site_manifest_value": manifest_counts.get(key),
            "source_report_value": value,
            "reconciled": manifest_counts.get(key) == value,
        }
        for key, value in source_counts.items()
    ]
    non_claim_checks = [
        {"text": text, "present": text.lower() in combined_text.lower()}
        for text in REQUIRED_NON_CLAIM_TEXT
    ]
    forbidden_claims = find_forbidden_affirmative_site_claims(combined_text)
    no_external_dependencies = not has_external_dependency(html, css, js)

    summary = GithubPagesSiteSummary(
        github_pages_site_created=True,
        static_site_only=True,
        backend_required=False,
        external_api_calls=False,
        scraping=False,
        analytics_or_tracking=False,
        external_cdn_dependencies=not no_external_dependencies,
        required_site_files_present=all(item["exists"] for item in file_checks),
        required_sections_present=all(item["present"] for item in section_checks),
        source_reports_available=all(item["exists"] for item in report_checks),
        source_report_counts_reconciled=all(item["reconciled"] for item in count_reconciliations),
        non_claim_boundaries_visible=all(item["present"] for item in non_claim_checks),
        forbidden_claim_findings=len(forbidden_claims),
        loaded_public_aggregate_values_displayed=source_counts["loaded_public_aggregate_values"],
        source_candidates_not_loaded_displayed=source_counts["source_candidates_not_loaded"],
        placeholders_mapped_displayed=source_counts["placeholders_mapped"],
        module_boundaries_mapped_displayed=source_counts["module_boundaries_mapped"],
        scenario_constraints_mapped_displayed=source_counts["module_scenario_constraints"],
        full_repo_audit_referenced="full_repo_integrity_upgrade_audit" in html,
        github_pages_workflow_added=(repo_root / ".github" / "workflows" / "pages.yml").exists(),
        new_data_loaded=False,
        restricted_data_loaded=False,
        personal_data_loaded=False,
        taxpayer_level_data_loaded=False,
        firm_confidential_data_loaded=False,
        household_microdata_loaded=False,
        calibration_completed=False,
        validation_claimed=False,
        actual_tax_payable_determined=False,
        official_status_claimed=False,
        firm_level_liability_logic_modified=False,
    )

    return {
        "metadata": {
            "report_id": "github_pages_site",
            "report_name": "CARSF V1.5 GitHub Pages Project Website",
            "status": "static_site_validated",
            "non_claims": manifest["non_claims"],
        },
        "github_pages_site": {
            "site_files": file_checks,
            "required_sections": section_checks,
            "source_reports": report_checks,
            "source_summary": source_counts,
            "count_reconciliations": count_reconciliations,
            "non_claim_checks": non_claim_checks,
            "forbidden_claim_findings": forbidden_claims,
            "external_dependency_check": {
                "no_external_dependencies": no_external_dependencies,
                "scope": "external scripts, stylesheets, images, fonts, analytics, tracking, fetch calls, and XMLHttpRequest",
            },
            "manual_pages_setup_steps": manifest["manual_pages_setup_steps"],
            "what_the_site_can_claim": [
                "The repo contains a structured private research prototype.",
                "The repo contains public aggregate-data anchors and source-locator metadata.",
                "The repo contains placeholder replacement mapping, calibration-boundary mapping, scenario-output constraints, and a full repo integrity/gap audit.",
                "The repo can be reviewed and tested locally.",
            ],
            "what_the_site_must_not_claim": [
                "law",
                "legal advice",
                "tax advice",
                "ATO guidance",
                "Treasury modelling",
                "PBO costing",
                "official policy",
                "calibrated modelling",
                "validated modelling",
                "actual tax payable calculation",
                "firm-level liability determination",
                "economic validation",
                "welfare validation",
                "statistical validation",
                "implementation readiness",
            ],
            "summary": asdict(summary),
        },
        "summary": asdict(summary),
    }


def render_markdown(report: dict[str, Any]) -> str:
    site = report["github_pages_site"]
    summary = report["summary"]

    lines = [
        "# CARSF V1.5 GitHub Pages Project Website",
        "",
        "## A. Purpose",
        "",
        "This report validates the static GitHub Pages-ready project website for the CARSF Automation Tax Framework.",
        "The website is reviewer-facing only and packages existing generated report outputs without loading new data.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in report["metadata"]["non_claims"])
    lines.extend(
        [
            "",
            "## C. Static Site Files",
            "",
            "| File | Exists |",
            "| --- | --- |",
        ]
    )
    lines.extend(f"| `{item['path']}` | {item['exists']} |" for item in site["site_files"])
    lines.extend(
        [
            "",
            "## D. Required Content Sections",
            "",
            "| Section | Present |",
            "| --- | --- |",
        ]
    )
    lines.extend(f"| {item['section']} | {item['present']} |" for item in site["required_sections"])
    lines.extend(
        [
            "",
            "## E. Source Report Inputs",
            "",
            "| Report | Path | Exists |",
            "| --- | --- | --- |",
        ]
    )
    lines.extend(f"| {item['report']} | `{item['path']}` | {item['exists']} |" for item in site["source_reports"])
    lines.extend(
        [
            "",
            "## F. Source Summary Counts",
            "",
            "| Count | Value |",
            "| --- | ---: |",
        ]
    )
    lines.extend(f"| {key} | {value} |" for key, value in site["source_summary"].items())
    lines.extend(
        [
            "",
            "## G. Report Count Reconciliation",
            "",
            "| Count | Site Manifest | Source Report | Reconciled |",
            "| --- | ---: | ---: | --- |",
        ]
    )
    lines.extend(
        f"| {item['count_name']} | {item['site_manifest_value']} | {item['source_report_value']} | {item['reconciled']} |"
        for item in site["count_reconciliations"]
    )
    lines.extend(
        [
            "",
            "## H. External Dependency Check",
            "",
            f"- No external dependencies: {site['external_dependency_check']['no_external_dependencies']}",
            f"- Scope: {site['external_dependency_check']['scope']}",
            "",
            "## I. Non-Claim Boundary Check",
            "",
            "| Required text | Present |",
            "| --- | --- |",
        ]
    )
    lines.extend(f"| {item['text']} | {item['present']} |" for item in site["non_claim_checks"])
    lines.extend(
        [
            "",
            "## J. Forbidden Claim Scan",
            "",
            f"- Forbidden affirmative claim findings: {summary['forbidden_claim_findings']}",
        ]
    )
    if site["forbidden_claim_findings"]:
        lines.extend(f"- {item}" for item in site["forbidden_claim_findings"])
    lines.extend(
        [
            "",
            "## K. GitHub Pages Setup",
            "",
        ]
    )
    lines.extend(f"{index}. {step}" for index, step in enumerate(site["manual_pages_setup_steps"], start=1))
    lines.extend(
        [
            "",
            "## L. What The Site Can Claim",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in site["what_the_site_can_claim"])
    lines.extend(
        [
            "",
            "## M. What The Site Must Not Claim",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in site["what_the_site_must_not_claim"])
    lines.extend(
        [
            "",
            "## N. Summary Flags",
            "",
            "| Flag | Value |",
            "| --- | --- |",
        ]
    )
    lines.extend(f"| {key} | {value} |" for key, value in summary.items())
    lines.extend(
        [
            "",
            "## O. Limitations and Future Work",
            "",
            "This is a static project website only. It does not enable GitHub Pages from code, does not load new data, and does not change model calculations.",
            "Repository settings must still be configured before the site is published through GitHub Pages.",
            "",
        ]
    )
    return "\n".join(lines)


def write_report(report: dict[str, Any], reports_dir: Path) -> None:
    reports_dir.mkdir(parents=True, exist_ok=True)
    (reports_dir / "github_pages_site.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (reports_dir / "github_pages_site.md").write_text(render_markdown(report), encoding="utf-8")


def validate_report(report: dict[str, Any]) -> None:
    summary = report["summary"]
    required_true = [
        "github_pages_site_created",
        "static_site_only",
        "required_site_files_present",
        "required_sections_present",
        "source_reports_available",
        "source_report_counts_reconciled",
        "non_claim_boundaries_visible",
        "full_repo_audit_referenced",
    ]
    for field in required_true:
        if summary[field] is not True:
            raise SystemExit(f"GitHub Pages site validation failed: {field} is not true")

    required_false = [
        "backend_required",
        "external_api_calls",
        "scraping",
        "analytics_or_tracking",
        "external_cdn_dependencies",
        "new_data_loaded",
        "restricted_data_loaded",
        "personal_data_loaded",
        "taxpayer_level_data_loaded",
        "firm_confidential_data_loaded",
        "household_microdata_loaded",
        "calibration_completed",
        "validation_claimed",
        "actual_tax_payable_determined",
        "official_status_claimed",
        "firm_level_liability_logic_modified",
    ]
    for field in required_false:
        if summary[field] is not False:
            raise SystemExit(f"GitHub Pages site validation failed: {field} is not false")

    if summary["forbidden_claim_findings"] != 0:
        findings = ", ".join(report["github_pages_site"]["forbidden_claim_findings"])
        raise SystemExit(f"GitHub Pages site validation failed: forbidden claims found: {findings}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate and report the CARSF GitHub Pages static site.")
    parser.add_argument("--reports-dir", default="reports", help="Directory for generated site validation reports.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    reports_dir = Path(args.reports_dir)
    if not reports_dir.is_absolute():
        reports_dir = REPO_ROOT / reports_dir

    report = build_site_report(REPO_ROOT)
    validate_report(report)
    write_report(report, reports_dir)
    print(f"Wrote {reports_dir / 'github_pages_site.md'}")
    print(f"Wrote {reports_dir / 'github_pages_site.json'}")


if __name__ == "__main__":
    main()
