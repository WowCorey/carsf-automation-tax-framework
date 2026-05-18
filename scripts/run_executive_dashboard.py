"""Run the CARSF V1.5 executive dashboard consolidation report."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from dataclasses import asdict
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = REPO_ROOT / "model"
if str(MODEL_ROOT) not in sys.path:
    sys.path.insert(0, str(MODEL_ROOT))

from carsf.example_runner import report_metadata  # noqa: E402
from carsf.executive_dashboard import (  # noqa: E402
    EXECUTIVE_DASHBOARD_NON_CLAIMS,
    EXECUTIVE_DASHBOARD_WARNING,
    build_executive_dashboard_result,
    find_forbidden_affirmative_dashboard_claims,
)


REPORT_STATUS = "prototype_executive_dashboard_report_index_only"
DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "dashboard" / "executive_dashboard_manifest.yaml"


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def load_dashboard_manifest(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"dashboard manifest must be a mapping: {path}")
    return loaded


def run_executive_dashboard(manifest_path: Path, repo_root: Path = REPO_ROOT) -> Any:
    payload = load_dashboard_manifest(manifest_path)
    return build_executive_dashboard_result(payload, repo_root)


def build_json_payload(result: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": EXECUTIVE_DASHBOARD_NON_CLAIMS,
            "real_data_used": False,
            "readiness_score_created": False,
            "maturity_score_created": False,
            "operational_readiness_claimed": False,
            "legal_sufficiency_claimed": False,
            "economic_validation_claimed": False,
            "firm_level_liability_logic_modified": False,
        },
        "summary": _jsonable(result.summary),
        "executive_dashboard": _jsonable(result),
    }


def _join(values: list[str] | None) -> str:
    if not values:
        return "None"
    return ", ".join(values)


def _summary_lines(summary: Any) -> list[str]:
    return [
        f"- Total layers: {summary.total_layers}",
        f"- Total reports indexed: {summary.total_reports_indexed}",
        f"- Reports present: {summary.reports_present}",
        f"- Reports missing: {summary.reports_missing}",
        f"- Layers with generated reports: {summary.layers_with_generated_reports}",
        f"- Synthetic-only layers: {summary.synthetic_only_layers}",
        f"- Placeholder-only layers: {summary.placeholder_only_layers}",
        f"- Non-operative layers: {summary.non_operative_layers}",
        f"- External-review-required layers: {summary.external_review_required_layers}",
        f"- Calibration-required layers: {summary.calibration_required_layers}",
        f"- Legal-review-required layers: {summary.legal_review_required_layers}",
        f"- Tax-review-required layers: {summary.tax_review_required_layers}",
        f"- ATO-methods-review-required layers: {summary.ato_methods_review_required_layers}",
        f"- Treasury-methods-review-required layers: {summary.treasury_methods_review_required_layers}",
        f"- Privacy-review-required layers: {summary.privacy_review_required_layers}",
        f"- Statistical-methods-review-required layers: {summary.statistical_methods_review_required_layers}",
        f"- real_data_used: {summary.real_data_used}",
        f"- readiness_score_created: {summary.readiness_score_created}",
        f"- operational_readiness_claimed: {summary.operational_readiness_claimed}",
        f"- legal_sufficiency_claimed: {summary.legal_sufficiency_claimed}",
        f"- economic_validation_claimed: {summary.economic_validation_claimed}",
        f"- firm_level_liability_logic_modified: {summary.firm_level_liability_logic_modified}",
    ]


def _navigation_table(items: list[Any]) -> list[str]:
    lines = [
        "| Read Order | Layer ID | Layer Name | Purpose | Official Process | Main Reason |",
        "| ---: | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            "| "
            f"{item.read_order} | {item.layer_id} | {item.layer_name} | {item.purpose} | "
            f"{item.official_process} | {item.main_reason} |"
        )
    return lines


def _layer_table(layers: list[Any]) -> list[str]:
    lines = [
        "| Layer ID | Layer Name | Group | Purpose | Status Labels | Primary Reports | Streamlit Pages | Recommended Reviewer | Read Order | Main Reason |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- |",
    ]
    for layer in layers:
        lines.append(
            "| "
            f"{layer.layer_id} | {layer.layer_name} | {layer.layer_group} | {layer.purpose} | "
            f"{_join(layer.status_labels)} | {_join(layer.primary_reports)} | {_join(layer.streamlit_pages)} | "
            f"{_join(layer.recommended_reviewer)} | {layer.read_order} | {layer.main_reason} |"
        )
    return lines


def _report_table(entries: list[Any]) -> list[str]:
    lines = [
        "| Report | Layer ID | Exists | Generated By | Interpretation Warning | Must Not Be Used For | Suggested Read Order |",
        "| --- | --- | --- | --- | --- | --- | ---: |",
    ]
    for entry in entries:
        lines.append(
            "| "
            f"{entry.report_path} | {entry.layer_id} | {entry.exists} | {entry.generated_by} | "
            f"{entry.interpretation_warning} | must not use for: {_join(entry.must_not_be_used_for)} | "
            f"{entry.recommended_read_order} |"
        )
    return lines


def _page_table(pages: list[str]) -> list[str]:
    lines = ["| Streamlit Page |", "| --- |"]
    for page in pages:
        lines.append(f"| {page} |")
    return lines


def _profile_table(profiles: list[Any]) -> list[str]:
    lines = [
        "| Layer ID | Non-Claim Flags | Must Not Be Used For | Not For Real-World Use |",
        "| --- | --- | --- | --- |",
    ]
    for profile in profiles:
        lines.append(
            "| "
            f"{profile.layer_id} | {_join(profile.non_claim_flags)} | "
            f"must not use for: {_join(profile.must_not_be_used_for)} | {profile.not_for_real_world_use} |"
        )
    return lines


def _blocker_table(blockers: list[Any]) -> list[str]:
    lines = [
        "| Layer ID | Blocker Type | Blocker | External Review Needed | Main Reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    for blocker in blockers:
        lines.append(
            "| "
            f"{blocker.layer_id} | {blocker.blocker_type} | {blocker.blocker} | "
            f"{blocker.external_review_needed} | {blocker.main_reason} |"
        )
    return lines


def _guardrail_table(statuses: list[Any]) -> list[str]:
    lines = [
        "| Source Report | Exists | Clean | Denied Findings | Warning Findings | Interpretation Warning |",
        "| --- | --- | --- | ---: | ---: | --- |",
    ]
    for status in statuses:
        lines.append(
            "| "
            f"{status.source_report} | {status.exists} | {status.clean} | "
            f"{status.denied_findings} | {status.warning_findings} | {status.interpretation_warning} |"
        )
    return lines


def _reviewer_table(layers: list[Any]) -> list[str]:
    lines = ["| Reviewer | Layers |", "| --- | --- |"]
    reviewers = sorted({reviewer for layer in layers for reviewer in layer.recommended_reviewer})
    for reviewer in reviewers:
        layer_ids = [layer.layer_id for layer in layers if reviewer in layer.recommended_reviewer]
        lines.append(f"| {reviewer} | {', '.join(layer_ids)} |")
    return lines


def build_markdown(result: Any, metadata: dict[str, Any]) -> str:
    lines = [
        "# CARSF V1.5 Executive Dashboard Consolidation",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This dashboard consolidates existing CARSF V1.5 prototype layers, generated reports, Streamlit pages, non-claim profiles, calibration blockers, external-review blockers, suggested review navigation, and reviewer routing.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in EXECUTIVE_DASHBOARD_NON_CLAIMS)
    lines.extend(
        [
            "- It creates no readiness score, maturity score, official review status, validation claim, enforcement pathway, or firm-level liability change.",
            "",
            "## C. How to Read This Dashboard",
            "",
            "Use this as a review navigation index. Read order is suggested review navigation only and is not an official process. Each linked report keeps its own non-claim boundaries.",
            "",
            "## D. Prototype Stack Overview",
            "",
        ]
    )
    lines.extend(_summary_lines(result.summary))
    lines.extend(["", "## E. Suggested Review Navigation", ""])
    lines.extend(_navigation_table(result.suggested_review_navigation))
    lines.extend(["", "## F. Layer Index", ""])
    lines.extend(_layer_table(result.layers))
    lines.extend(["", "## G. Report Index", ""])
    lines.extend(_report_table(result.report_entries))
    lines.extend(["", "## H. Streamlit Page Index", ""])
    lines.extend(_page_table(result.streamlit_page_index))
    lines.extend(["", "## I. Non-Claim Profile by Layer", ""])
    lines.extend(_profile_table(result.non_claim_profiles))
    lines.extend(["", "## J. Calibration Blockers", ""])
    lines.extend(_blocker_table(result.calibration_blockers))
    lines.extend(["", "## K. External Review Blockers", ""])
    lines.extend(_blocker_table(result.external_review_blockers))
    lines.extend(["", "## L. Guardrail / Safety Status", ""])
    lines.extend(_guardrail_table(result.guardrail_statuses))
    lines.extend(
        [
            "",
            "## M. Legislative / Administrative Boundary Warnings",
            "",
            "- Legislative architecture outputs are non-operative and are not a Bill, legal drafting, legal advice, tax advice, ATO guidance, Treasury modelling, legal sufficiency, or legislative readiness.",
            "- Administrative workflow outputs organise synthetic review pathways only and are not enforcement, notices, penalties, compliance scoring, audit logic, or operational readiness.",
            "",
            "## N. Household / Distributional Boundary Warnings",
            "",
            "- Household, weighting, uncertainty, and reviewed-scenario layers are synthetic or placeholder outputs only.",
            "- They are not real household modelling, population estimates, statistical validation, confidence intervals, forecasts, welfare advice, or eligibility law.",
            "",
            "## O. Fiscal / Economic Boundary Warnings",
            "",
            "- Fiscal, transition-funding, payment, investment, incidence, and sector-stress layers are placeholders only.",
            "- They are not Treasury modelling, ATO guidance, economic validation, investment advice, welfare validation, official sector ranking, or actual-tax-payable analysis.",
            "",
            "## P. Missing Reports or Navigation Gaps",
            "",
        ]
    )
    if result.missing_reports_or_navigation_gaps:
        lines.extend(f"- {item}" for item in result.missing_reports_or_navigation_gaps)
    else:
        lines.append("- No required dashboard report paths are missing.")
    lines.extend(["", "## Q. Recommended Reviewer Routing", ""])
    lines.extend(_reviewer_table(result.layers))
    lines.extend(
        [
            "",
            "## R. Plain-English Interpretation",
            "",
            "The dashboard is a map of what exists, where to find it, how to read it, and what not to infer from it. It makes the prototype easier to review without converting any layer into validation, approval, readiness, legal sufficiency, or tax-payable output.",
            "",
            "## S. Limitations and Future Review Needs",
            "",
            "- Prototype dashboard only.",
            "- Report index only.",
            "- Not legal advice.",
            "- Not tax advice.",
            "- Not ATO guidance.",
            "- Not Treasury modelling.",
            "- Not economic validation.",
            "- Not welfare advice.",
            "- Not compliance scoring.",
            "- Not enforcement.",
            "- Not operational readiness.",
            "- Not legal sufficiency.",
            "- Not legislative readiness.",
            "- Not a readiness score.",
            "- Not an official review pathway.",
            "- Does not determine actual tax payable.",
            "- Uses no taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.",
            "- Does not modify firm-level CARSF liability.",
            "- Only consolidates existing prototype reports, warnings, navigation, and review blockers.",
        ]
    )
    markdown = "\n".join(lines).rstrip() + "\n"
    forbidden = find_forbidden_affirmative_dashboard_claims(markdown)
    if forbidden:
        raise ValueError(f"generated executive dashboard report contains forbidden affirmative claims: {', '.join(forbidden)}")
    return markdown


def write_reports(reports_dir: Path, result: Any) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    payload = build_json_payload(result, metadata)
    markdown = build_markdown(result, metadata)
    forbidden = find_forbidden_affirmative_dashboard_claims(json.dumps(payload, sort_keys=True))
    if forbidden:
        raise ValueError(f"generated executive dashboard JSON contains forbidden affirmative claims: {', '.join(forbidden)}")
    json_path = reports_dir / "executive_dashboard.json"
    md_path = reports_dir / "executive_dashboard.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return json_path, md_path


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-path", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args(argv)

    result = run_executive_dashboard(args.manifest_path)
    json_path, md_path = write_reports(args.reports_dir, result)
    print(f"indexed {result.summary.total_layers} dashboard layers")
    print(f"indexed {result.summary.total_reports_indexed} generated report paths")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
