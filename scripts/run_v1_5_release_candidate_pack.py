"""Run the CARSF V1.5 release-candidate pack report."""

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
from carsf.release_candidate_pack import (  # noqa: E402
    RELEASE_CANDIDATE_NON_CLAIMS,
    build_release_candidate_pack_result,
    find_forbidden_affirmative_release_claims,
)


REPORT_STATUS = "private_research_prototype_release_candidate_pack_only"
DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "release" / "v1_5_release_manifest.yaml"


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def load_release_manifest(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"release manifest must be a mapping: {path}")
    return loaded


def run_release_candidate_pack(manifest_path: Path, repo_root: Path = REPO_ROOT) -> Any:
    payload = load_release_manifest(manifest_path)
    return build_release_candidate_pack_result(payload, repo_root)


def build_json_payload(result: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": RELEASE_CANDIDATE_NON_CLAIMS,
            "real_data_used": False,
            "readiness_score_created": False,
            "operational_readiness_claimed": False,
            "legal_sufficiency_claimed": False,
            "legislative_readiness_claimed": False,
            "economic_validation_claimed": False,
            "welfare_validation_claimed": False,
            "statistical_validation_claimed": False,
            "official_status_claimed": False,
            "firm_level_liability_logic_modified": False,
        },
        "summary": _jsonable(result.summary),
        "release_candidate_pack": _jsonable(result),
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
        f"- Total release documents: {summary.total_release_documents}",
        f"- Release documents present: {summary.release_documents_present}",
        f"- Release documents missing: {summary.release_documents_missing}",
        f"- Paper files checked: {summary.paper_files_checked}",
        f"- Working paper updated: {summary.working_paper_updated}",
        f"- Layers requiring calibration: {summary.layers_requiring_calibration}",
        f"- Layers requiring legal review: {summary.layers_requiring_legal_review}",
        f"- Layers requiring tax review: {summary.layers_requiring_tax_review}",
        f"- Layers requiring ATO methods review: {summary.layers_requiring_ato_methods_review}",
        f"- Layers requiring Treasury methods review: {summary.layers_requiring_treasury_methods_review}",
        f"- Layers requiring privacy review: {summary.layers_requiring_privacy_review}",
        f"- Layers requiring statistical review: {summary.layers_requiring_statistical_review}",
        f"- Layers requiring economic review: {summary.layers_requiring_economic_review}",
        f"- Layers requiring welfare review: {summary.layers_requiring_welfare_review}",
        f"- Layers requiring Parliamentary Counsel review: {summary.layers_requiring_parliamentary_counsel_review}",
        f"- real_data_used: {summary.real_data_used}",
        f"- readiness_score_created: {summary.readiness_score_created}",
        f"- operational_readiness_claimed: {summary.operational_readiness_claimed}",
        f"- legal_sufficiency_claimed: {summary.legal_sufficiency_claimed}",
        f"- legislative_readiness_claimed: {summary.legislative_readiness_claimed}",
        f"- economic_validation_claimed: {summary.economic_validation_claimed}",
        f"- welfare_validation_claimed: {summary.welfare_validation_claimed}",
        f"- statistical_validation_claimed: {summary.statistical_validation_claimed}",
        f"- official_status_claimed: {summary.official_status_claimed}",
        f"- firm_level_liability_logic_modified: {summary.firm_level_liability_logic_modified}",
    ]


def _layer_table(layers: list[Any]) -> list[str]:
    lines = [
        "| Layer ID | Layer Name | Group | Summary | Status Labels | Primary Reports | Streamlit Pages | Reviewer Routing | Main Reason |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for layer in layers:
        lines.append(
            "| "
            f"{layer.layer_id} | {layer.layer_name} | {layer.layer_group} | {layer.summary} | "
            f"{_join(layer.status_labels)} | {_join(layer.primary_reports)} | {_join(layer.streamlit_pages)} | "
            f"{_join(layer.recommended_reviewer)} | {layer.main_reason} |"
        )
    return lines


def _report_table(reports: list[Any]) -> list[str]:
    lines = [
        "| Report | Layer | Exists | Generated By | What It Shows | What It Does Not Show | Primary Non-Claim | Reviewer | Read Order |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | ---: |",
    ]
    for report in reports:
        lines.append(
            "| "
            f"{report.report_path} | {report.layer_id} | {report.exists} | {report.generated_by} | "
            f"{report.what_it_shows} | does not show: {report.what_it_does_not_show} | {report.primary_non_claim} | "
            f"{_join(report.recommended_reviewer)} | {report.suggested_read_order} |"
        )
    return lines


def _document_table(documents: list[Any]) -> list[str]:
    lines = [
        "| Document | Type | Exists | Purpose | Contains Non-Claims |",
        "| --- | --- | --- | --- | --- |",
    ]
    for document in documents:
        lines.append(
            "| "
            f"{document.document_path} | {document.document_type} | {document.exists} | "
            f"{document.purpose} | {document.contains_non_claims} |"
        )
    return lines


def _route_table(routes: list[Any]) -> list[str]:
    lines = [
        "| Reviewer | Layers | Reports | Release Documents | Official Process | Main Reason |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for route in routes:
        lines.append(
            "| "
            f"{route.reviewer} | {_join(route.layers)} | {_join(route.reports)} | "
            f"{_join(route.release_documents)} | {route.official_process} | {route.main_reason} |"
        )
    return lines


def _blocker_table(blockers: list[Any]) -> list[str]:
    lines = [
        "| Layer ID | Blocker Type | Blocker | Review Needed | Main Reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    for blocker in blockers:
        lines.append(
            "| "
            f"{blocker.layer_id} | {blocker.blocker_type} | {blocker.blocker} | "
            f"{blocker.review_needed} | {blocker.main_reason} |"
        )
    return lines


def build_markdown(result: Any, metadata: dict[str, Any]) -> str:
    lines = [
        "# CARSF V1.5 Release Candidate Pack",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This release-candidate pack consolidates the CARSF V1.5 private research prototype into a working-paper, report, reviewer-routing, calibration-blocker, and non-claim package for external review.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in RELEASE_CANDIDATE_NON_CLAIMS)
    lines.extend(
        [
            "- It creates no readiness score, official status, validation claim, legal sufficiency, operational readiness, legislative readiness, enforcement pathway, or firm-level liability change.",
            "",
            "## C. Release Pack Contents",
            "",
        ]
    )
    lines.extend(_summary_lines(result.summary))
    lines.extend(["", "## D. Working Paper Update Summary", ""])
    lines.extend(
        [
            "- Checked source working paper and paper support files: " + _join(result.source_documents),
            f"- Working paper updated with current V1.5 layer references: {result.summary.working_paper_updated}",
            "- Working-paper updates are additive and do not convert the paper into law, legal drafting, official policy, or validation.",
            "",
            "## E. Prototype Stack Summary",
            "",
        ]
    )
    lines.extend(_layer_table(result.prototype_layers))
    lines.extend(["", "## F. Generated Report Map", ""])
    lines.extend(_report_table(result.generated_reports))
    lines.extend(["", "## G. Release Documents", ""])
    lines.extend(_document_table(result.release_documents))
    lines.extend(["", "## H. Suggested Reviewer Routing", ""])
    lines.extend(_route_table(result.reviewer_routes))
    lines.extend(["", "## I. Calibration Blockers", ""])
    lines.extend(_blocker_table(result.calibration_blockers))
    lines.extend(["", "## J. External Review Blockers", ""])
    lines.extend(_blocker_table(result.external_review_blockers))
    lines.extend(["", "## K. Guardrail / Safety Status", ""])
    lines.extend(
        [
            f"- Source report: {result.guardrail_status.get('source_report')}",
            f"- Exists: {result.guardrail_status.get('exists')}",
            f"- Clean: {result.guardrail_status.get('clean')}",
            f"- Denied findings: {result.guardrail_status.get('denied_findings')}",
            f"- Warning findings: {result.guardrail_status.get('warning_findings')}",
            f"- Interpretation warning: {result.guardrail_status.get('interpretation_warning')}",
        ]
    )
    lines.extend(
        [
            "",
            "## L. Legislative / Legal Boundary",
            "",
            "- Legislative architecture material is non-operative and does not create rights, obligations, statutory powers, notices, penalties, enforcement, legal sufficiency, or legislative readiness.",
            "- Legal and Parliamentary Counsel review remain external blockers before any operative drafting.",
            "",
            "## M. Tax / ATO / Treasury Boundary",
            "",
            "- Formula, schedule, administrative, behavioural, and evidence layers are not ATO guidance, Treasury modelling, tax advice, compliance scoring, or actual-tax-payable analysis.",
            "- Tax, Treasury, ATO methods, transfer-pricing, offshore-attribution, and schedule-authority review remain unresolved.",
            "",
            "## N. Household / Welfare Boundary",
            "",
            "- Household, payment, weighting, and reviewed-scenario layers are synthetic or placeholder-only.",
            "- They are not real household modelling, welfare advice, eligibility law, Services Australia modelling, population estimates, or validated support-policy outputs.",
            "",
            "## O. Fiscal / Economic Boundary",
            "",
            "- Fiscal trajectory, transition funding, investment/incidence, and sector stress outputs are not forecasts, economic validation, investment advice, Treasury modelling, or calibrated public-finance estimates.",
            "",
            "## P. Statistical / Uncertainty Boundary",
            "",
            "- Uncertainty ranges are deterministic low/base/high placeholders only.",
            "- They are not Monte Carlo, confidence intervals, forecasts, statistical validation, or calibrated uncertainty quantification.",
            "",
            "## Q. Missing Items / Release Gaps",
            "",
        ]
    )
    if result.missing_items_or_release_gaps:
        lines.extend(f"- {item}" for item in result.missing_items_or_release_gaps)
    else:
        lines.append("- No required release-pack documents or indexed reports are missing.")
    lines.extend(
        [
            "",
            "## R. Suggested Next Review Steps",
            "",
            "- Use the executive dashboard first for navigation.",
            "- Read the working paper status note and release documents before interpreting generated reports.",
            "- Route findings to legal, tax, Treasury methods, ATO methods, privacy, statistical, economic, welfare, Parliamentary Counsel, technical, and hostile-review paths as appropriate.",
            "- Treat all recommendations as external-review prompts only, not an official process.",
            "",
            "## S. Limitations and Future Work",
            "",
            "- Private research prototype only.",
            "- Release-candidate pack only.",
            "- Not legal advice.",
            "- Not tax advice.",
            "- Not ATO guidance.",
            "- Not Treasury modelling.",
            "- Not economic validation.",
            "- Not welfare advice.",
            "- Not statistical validation.",
            "- Not compliance scoring.",
            "- Not enforcement.",
            "- Not operational readiness.",
            "- Not legal sufficiency.",
            "- Not legislative readiness.",
            "- Not a readiness score.",
            "- Not official status.",
            "- Not an official review pathway.",
            "- Does not determine actual tax payable.",
            "- Uses no taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.",
            "- Does not modify firm-level CARSF liability.",
            "- Only packages existing prototype reports, warnings, navigation, review blockers, and working-paper material for external review.",
        ]
    )
    markdown = "\n".join(lines).rstrip() + "\n"
    forbidden = find_forbidden_affirmative_release_claims(markdown)
    if forbidden:
        raise ValueError(f"generated release-candidate report contains forbidden affirmative claims: {', '.join(forbidden)}")
    return markdown


def write_reports(reports_dir: Path, result: Any) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    payload = build_json_payload(result, metadata)
    markdown = build_markdown(result, metadata)
    forbidden = find_forbidden_affirmative_release_claims(json.dumps(payload, sort_keys=True))
    if forbidden:
        raise ValueError(f"generated release-candidate JSON contains forbidden affirmative claims: {', '.join(forbidden)}")
    json_path = reports_dir / "v1_5_release_candidate_pack.json"
    md_path = reports_dir / "v1_5_release_candidate_pack.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return json_path, md_path


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-path", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args(argv)

    result = run_release_candidate_pack(args.manifest_path)
    json_path, md_path = write_reports(args.reports_dir, result)
    print(f"indexed {result.summary.total_layers} release-candidate layers")
    print(f"indexed {result.summary.total_reports_indexed} generated reports")
    print(f"checked {result.summary.total_release_documents} release documents")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
