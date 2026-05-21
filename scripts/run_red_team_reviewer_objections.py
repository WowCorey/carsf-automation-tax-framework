"""Run the CARSF V1.5 red-team reviewer objections pack."""

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
from carsf.red_team_reviewer_objections import (  # noqa: E402
    OBJECTION_CATEGORY_VALUES,
    OBJECTION_STATUS_VALUES,
    RED_TEAM_REVIEWER_OBJECTIONS_NON_CLAIMS,
    SEVERITY_VALUES,
    build_red_team_reviewer_objections_result,
    find_forbidden_affirmative_red_team_claims,
)


REPORT_STATUS = "red_team_reviewer_objections_pack_only"
DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "public_pilot" / "red_team_reviewer_objections_manifest.yaml"
DEFAULT_REPORTS_DIR = REPO_ROOT / "reports"
DEFAULT_INPUT_REPORTS = {
    "real_data_feasibility": REPO_ROOT / "reports" / "real_data_feasibility.json",
    "public_data_pilot": REPO_ROOT / "reports" / "public_data_pilot.json",
    "public_data_evidence_map": REPO_ROOT / "reports" / "public_data_evidence_map.json",
    "public_data_consistency_audit": REPO_ROOT / "reports" / "public_data_consistency_audit.json",
    "source_locator_verification_pack": REPO_ROOT / "reports" / "source_locator_verification_pack.json",
}


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"YAML file must be a mapping: {path}")
    return payload


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON file must be a mapping: {path}")
    return payload


def _join(values: list[str] | None) -> str:
    if not values:
        return "None"
    return ", ".join(str(item) for item in values)


def _summary_lines(summary: Any) -> list[str]:
    return [
        f"- total_objections: {summary.total_objections}",
        f"- critical_objections: {summary.critical_objections}",
        f"- high_objections: {summary.high_objections}",
        f"- medium_objections: {summary.medium_objections}",
        f"- low_objections: {summary.low_objections}",
        f"- informational_objections: {summary.informational_objections}",
        f"- acknowledged_objections: {summary.acknowledged_objections}",
        f"- partially_mitigated_objections: {summary.partially_mitigated_objections}",
        f"- unresolved_objections: {summary.unresolved_objections}",
        f"- blocked_by_restricted_data_objections: {summary.blocked_by_restricted_data_objections}",
        f"- external_review_required_objections: {summary.external_review_required_objections}",
        f"- legal_review_required_objections: {summary.legal_review_required_objections}",
        f"- economic_review_required_objections: {summary.economic_review_required_objections}",
        f"- statistical_review_required_objections: {summary.statistical_review_required_objections}",
        f"- cannot_be_resolved_inside_repo_objections: {summary.cannot_be_resolved_inside_repo_objections}",
        f"- total_categories: {summary.total_categories}",
        f"- categories_covered: {summary.categories_covered}",
        f"- unresolved_blockers_total: {summary.unresolved_blockers_total}",
        f"- future_evidence_needs_total: {summary.future_evidence_needs_total}",
        f"- forbidden_claim_findings: {summary.forbidden_claim_findings}",
        f"- red_team_pack_created: {summary.red_team_pack_created}",
        f"- new_data_loaded: {summary.new_data_loaded}",
        f"- external_source_verification_claimed: {summary.external_source_verification_claimed}",
        f"- objections_acknowledged: {summary.objections_acknowledged}",
        f"- unresolved_blockers_visible: {summary.unresolved_blockers_visible}",
        f"- calibration_limitations_visible: {summary.calibration_limitations_visible}",
        f"- legal_limitations_visible: {summary.legal_limitations_visible}",
        f"- statistical_limitations_visible: {summary.statistical_limitations_visible}",
        f"- dashboard_misinterpretation_risks_visible: {summary.dashboard_misinterpretation_risks_visible}",
        f"- real_calibration_completed: {summary.real_calibration_completed}",
        f"- actual_tax_payable_determined: {summary.actual_tax_payable_determined}",
        f"- validation_claimed: {summary.validation_claimed}",
        f"- approval_claimed: {summary.approval_claimed}",
        f"- operational_readiness_claimed: {summary.operational_readiness_claimed}",
        f"- legal_sufficiency_claimed: {summary.legal_sufficiency_claimed}",
        f"- official_status_claimed: {summary.official_status_claimed}",
        f"- firm_level_liability_logic_modified: {summary.firm_level_liability_logic_modified}",
    ]


def _objection_table(items: list[Any]) -> list[str]:
    lines = [
        "| Objection ID | Severity | Status | Category | Title | Valid Concern | Current Response | Must Not Claim |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.objection_id} | {item.severity} | {item.status} | {item.objection_category} | "
            f"{item.objection_title} | {item.why_the_concern_is_valid} | {item.current_project_response} | "
            f"{_join(item.what_the_project_must_not_claim)} |"
        )
    return lines


def _blocker_table(items: list[Any]) -> list[str]:
    lines = [
        "| Blocker | Affected Objections |",
        "| --- | --- |",
    ]
    for item in items:
        lines.append(f"| {item.blocker} | {_join(item.affected_objection_ids)} |")
    return lines


def _evidence_table(items: list[Any]) -> list[str]:
    lines = [
        "| Evidence Need | Affected Objections |",
        "| --- | --- |",
    ]
    for item in items:
        lines.append(f"| {item.evidence_need} | {_join(item.affected_objection_ids)} |")
    return lines


def _build_json_payload(result: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": RED_TEAM_REVIEWER_OBJECTIONS_NON_CLAIMS,
            "objection_status_values": sorted(OBJECTION_STATUS_VALUES),
            "severity_values": sorted(SEVERITY_VALUES),
            "objection_category_values": sorted(OBJECTION_CATEGORY_VALUES),
        },
        "summary": _jsonable(result.summary),
        "red_team_reviewer_objections": _jsonable(result),
    }


def _build_markdown(result: Any, metadata: dict[str, Any]) -> str:
    critical = [item for item in result.objections if item.severity == "critical"]
    high = [item for item in result.objections if item.severity == "high"]
    medium = [item for item in result.objections if item.severity == "medium"]
    by_category = {
        category: [item for item in result.objections if item.objection_category == category]
        for category in sorted(OBJECTION_CATEGORY_VALUES)
    }
    lines: list[str] = [
        "# CARSF V1.5 Red-Team Reviewer Objections Pack",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report packages likely reviewer objections and honest responses for the Build 26-29.5 public-data pilot materials without loading new data.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in RED_TEAM_REVIEWER_OBJECTIONS_NON_CLAIMS)
    lines.extend(["", "## C. How Reviewers Should Use This Pack", ""])
    lines.extend(
        [
            "- Treat each objection as a weakness to inspect, not as a resolved issue.",
            "- Use the can-say and must-not-claim fields to test whether wording remains bounded.",
            "- Do not treat this pack as calibration, validation, approval, legal sufficiency, operational readiness, official status, or tax-payable evidence.",
        ]
    )
    lines.extend(["", "## D. Objection Status Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(OBJECTION_STATUS_VALUES))
    lines.extend(["", "## E. Severity Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(SEVERITY_VALUES))
    lines.extend(["", "## F. Objection Category Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(OBJECTION_CATEGORY_VALUES))
    lines.extend(["", "## G. Critical Objections", ""])
    lines.extend(_objection_table(critical))
    lines.extend(["", "## H. High-Severity Objections", ""])
    lines.extend(_objection_table(high))
    lines.extend(["", "## I. Medium-Severity Objections", ""])
    lines.extend(_objection_table(medium))
    category_sections = [
        ("## J. Public Data Limitation Objections", "public_data_limitations"),
        ("## K. Placeholder Limitation Objections", "placeholder_limitations"),
        ("## L. Restricted Data Blocker Objections", "restricted_data_blockers"),
        ("## M. Calibration and Statistical Objections", "calibration_limitations"),
        ("## N. Legal / Tax / Administrative Objections", "legal_and_tax_limitations"),
        ("## O. Economic Incidence Objections", "economic_incidence_limitations"),
        ("## P. Dashboard / Misinterpretation Risk Objections", "dashboard_interpretation_risk"),
    ]
    for heading, category in category_sections:
        items = by_category[category]
        if category == "calibration_limitations":
            items = items + by_category["statistical_limitations"]
        if category == "legal_and_tax_limitations":
            items = items + by_category["administrative_feasibility_limitations"]
        if category == "dashboard_interpretation_risk":
            items = items + by_category["reviewer_misinterpretation_risk"] + by_category["non_claim_boundary_risk"]
        lines.extend(["", heading, ""])
        lines.extend(_objection_table(items))
    lines.extend(["", "## Q. Unresolved Blockers", ""])
    lines.extend(_blocker_table(result.unresolved_blockers))
    lines.extend(["", "## R. Evidence Needed To Resolve", ""])
    lines.extend(_evidence_table(result.future_evidence_needs))
    lines.extend(["", "## S. What The Project Can Say", ""])
    for item in result.objections:
        lines.append(f"- {item.objection_id}: {_join(item.what_the_project_can_say)}")
    lines.extend(["", "## T. What The Project Must Not Claim", ""])
    for item in result.objections:
        lines.append(f"- {item.objection_id}: {_join(item.what_the_project_must_not_claim)}")
    lines.extend(["", "## U. Build 30 Readiness", ""])
    lines.extend(f"- {item}" for item in result.build_30_requirements)
    lines.extend(["", "## V. Limitations and Future Work", ""])
    lines.extend(
        [
            "- This objections pack is a reviewer aid only and does not resolve objections.",
            "- Future work should package reviewer handoff material without loading new data or claiming calibration.",
            "- Summary counts:",
        ]
    )
    lines.extend(_summary_lines(result.summary))
    return "\n".join(lines) + "\n"


def run(
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
    reports_dir: Path = DEFAULT_REPORTS_DIR,
) -> tuple[Path, Path, dict[str, Any]]:
    manifest = _load_yaml(manifest_path)
    input_reports = {name: _load_json(path) for name, path in DEFAULT_INPUT_REPORTS.items()}
    result = build_red_team_reviewer_objections_result(manifest, input_reports)
    metadata = report_metadata()
    json_payload = _build_json_payload(result, metadata)
    markdown = _build_markdown(result, metadata)
    combined = markdown + "\n" + json.dumps(json_payload, sort_keys=True)
    findings = find_forbidden_affirmative_red_team_claims(combined)
    if findings:
        raise ValueError(f"forbidden affirmative red-team claims found in outputs: {', '.join(findings)}")

    reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = reports_dir / "red_team_reviewer_objections.json"
    md_path = reports_dir / "red_team_reviewer_objections.md"
    json_path.write_text(json.dumps(json_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return json_path, md_path, json_payload


def main() -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS_DIR)
    args = parser.parse_args()
    json_path, md_path, payload = run(args.manifest, args.reports_dir)
    summary = payload["summary"]
    print(f"red-team objections: {summary['total_objections']}")
    print(f"critical objections: {summary['critical_objections']}")
    print(f"high objections: {summary['high_objections']}")
    print(f"categories covered: {summary['categories_covered']}")
    print(f"unresolved blockers: {summary['unresolved_blockers_total']}")
    print(f"future evidence needs: {summary['future_evidence_needs_total']}")
    print(f"forbidden claim findings: {summary['forbidden_claim_findings']}")
    print(f"new_data_loaded: {summary['new_data_loaded']}")
    print(f"external_source_verification_claimed: {summary['external_source_verification_claimed']}")
    print(f"real_calibration_completed: {summary['real_calibration_completed']}")
    print(f"validation_claimed: {summary['validation_claimed']}")
    print(f"firm_level_liability_logic_modified: {summary['firm_level_liability_logic_modified']}")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
