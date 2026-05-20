"""Run the CARSF V1.5 public-data pilot reviewer evidence map report."""

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
from carsf.public_data_evidence_map import (  # noqa: E402
    CONFIDENCE_LABEL_VALUES,
    EVIDENCE_STATUS_VALUES,
    PUBLIC_DATA_EVIDENCE_MAP_NON_CLAIMS,
    REVIEWER_INTERPRETATION_VALUES,
    build_public_data_evidence_map_result,
)
from carsf.public_data_pilot import find_forbidden_affirmative_public_data_claims  # noqa: E402


REPORT_STATUS = "reviewer_evidence_map_only"
DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "public_pilot" / "reviewer_evidence_map_manifest.yaml"
DEFAULT_PUBLIC_PILOT_REPORT_PATH = REPO_ROOT / "reports" / "public_data_pilot.json"
DEFAULT_REPORTS_DIR = REPO_ROOT / "reports"


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


def _join_boundary_tokens(values: list[str] | None) -> str:
    if not values:
        return "None"
    return ", ".join(str(item).replace(" ", "_") for item in values)


def _summary_lines(summary: Any) -> list[str]:
    return [
        f"- Total source evidence items: {summary.total_source_evidence_items}",
        f"- Total loaded public extract evidence items: {summary.total_loaded_public_extract_evidence_items}",
        f"- Total source-reference-only evidence items: {summary.total_source_reference_only_evidence_items}",
        f"- Total placeholder evidence items: {summary.total_placeholder_evidence_items}",
        f"- Total field sanity evidence items: {summary.total_field_sanity_evidence_items}",
        f"- Field sanity passed: {summary.field_sanity_passed}",
        f"- Field sanity warning: {summary.field_sanity_warning}",
        f"- Field sanity blocked: {summary.field_sanity_blocked}",
        f"- Total module sanity evidence items: {summary.total_module_sanity_evidence_items}",
        f"- Modules sanity check possible: {summary.modules_sanity_check_possible}",
        f"- Modules placeholder anchor possible: {summary.modules_placeholder_anchor_possible}",
        f"- Modules blocked by restricted data: {summary.modules_blocked_by_restricted_data}",
        f"- Total restricted blocker items: {summary.total_restricted_blocker_items}",
        f"- Total forbidden repo data items: {summary.total_forbidden_repo_data_items}",
        f"- Total reviewer questions: {summary.total_reviewer_questions}",
        f"- Forbidden claim findings: {summary.forbidden_claim_findings}",
        f"- evidence_map_created: {summary.evidence_map_created}",
        f"- new_data_loaded: {summary.new_data_loaded}",
        f"- real_public_data_loaded_from_build_27_only: {summary.real_public_data_loaded_from_build_27_only}",
        f"- source_references_mapped: {summary.source_references_mapped}",
        f"- loaded_public_extracts_mapped: {summary.loaded_public_extracts_mapped}",
        f"- source_reference_only_records_mapped: {summary.source_reference_only_records_mapped}",
        f"- realistic_placeholders_mapped: {summary.realistic_placeholders_mapped}",
        f"- restricted_blockers_mapped: {summary.restricted_blockers_mapped}",
        f"- real_calibration_completed: {summary.real_calibration_completed}",
        f"- actual_tax_payable_determined: {summary.actual_tax_payable_determined}",
        f"- validation_claimed: {summary.validation_claimed}",
        f"- approval_claimed: {summary.approval_claimed}",
        f"- operational_readiness_claimed: {summary.operational_readiness_claimed}",
        f"- legal_sufficiency_claimed: {summary.legal_sufficiency_claimed}",
        f"- official_status_claimed: {summary.official_status_claimed}",
        f"- firm_level_liability_logic_modified: {summary.firm_level_liability_logic_modified}",
    ]


def _source_table(items: list[Any]) -> list[str]:
    lines = [
        "| Evidence ID | Source Reference | Publisher | Kind | URL | Evidence Status | Confidence Label | Linked Extracts | Must Not Infer |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.evidence_id} | {item.source_reference_id} | {item.publisher} | {item.source_kind} | {item.source_url} | "
            f"{item.evidence_status} | {item.confidence_label} | {_join(item.linked_extract_ids)} | {_join_boundary_tokens(item.what_reviewer_must_not_infer)} |"
        )
    return lines


def _extract_table(items: list[Any]) -> list[str]:
    lines = [
        "| Evidence ID | Extract | Evidence Status | Confidence Label | Claim Level | Values | Source Locator | Value Review Status | Reviewer Interpretation | Must Not Infer |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.evidence_id} | {item.extract_id} | {item.evidence_status} | {item.confidence_label} | {item.claim_level} | "
            f"{item.values_summary} | {item.source_locator or 'source reference only'} | {item.value_review_status or 'source reference only'} | "
            f"{_join(item.reviewer_interpretation)} | {_join_boundary_tokens(item.what_reviewer_must_not_infer)} |"
        )
    return lines


def _placeholder_table(items: list[Any]) -> list[str]:
    lines = [
        "| Evidence ID | Anchor | Field | Public Data Anchored | Strength | Confidence Label | Blocked By Restricted Data | Missing Data For Calibration | Must Not Infer |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.evidence_id} | {item.anchor_id} | {item.field_id} | {item.anchored_to_public_data} | {item.anchor_strength} | "
            f"{item.confidence_label} | {item.blocked_by_restricted_data} | {_join(item.missing_data_for_calibration)} | "
            f"{_join_boundary_tokens(item.what_reviewer_must_not_infer)} |"
        )
    return lines


def _field_table(items: list[Any]) -> list[str]:
    lines = [
        "| Evidence ID | Field | Check Type | Check Status | Evidence Status | Confidence Label | Extracts | Anchors | Finding |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.evidence_id} | {item.field_id} | {item.check_type} | {item.check_status} | {item.evidence_status} | "
            f"{item.confidence_label} | {_join(item.linked_extract_ids)} | {_join(item.linked_anchor_ids)} | {item.finding} |"
        )
    return lines


def _module_table(items: list[Any]) -> list[str]:
    lines = [
        "| Evidence ID | Module | Result Status | Sanity Check Possible | Calibration Possible | Evidence Status | Confidence Label | Main Blockers |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.evidence_id} | {item.module_id} | {item.result_status} | {item.sanity_check_possible} | {item.calibration_possible} | "
            f"{item.evidence_status} | {item.confidence_label} | {_join(item.main_blockers)} |"
        )
    return lines


def _blocker_table(items: list[Any]) -> list[str]:
    lines = [
        "| Evidence ID | Blocker ID | Type | Evidence Status | Confidence Label | Description | Required Access Or Review |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.evidence_id} | {item.blocker_id} | {item.blocker_type} | {item.evidence_status} | {item.confidence_label} | "
            f"{item.description} | {_join(item.required_access_or_review)} |"
        )
    return lines


def _questions_table(items: list[Any]) -> list[str]:
    lines = [
        "| Question ID | Category | Question | Interpretation | Target Evidence Status | Must Not Infer |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.question_id} | {item.category} | {item.question} | {item.reviewer_interpretation} | "
            f"{item.target_evidence_status} | {_join_boundary_tokens(item.must_not_infer)} |"
        )
    return lines


def _build_json_payload(result: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": PUBLIC_DATA_EVIDENCE_MAP_NON_CLAIMS,
            "evidence_status_values": sorted(EVIDENCE_STATUS_VALUES),
            "reviewer_interpretation_values": sorted(REVIEWER_INTERPRETATION_VALUES),
            "confidence_label_values": sorted(CONFIDENCE_LABEL_VALUES),
        },
        "summary": _jsonable(result.summary),
        "public_data_evidence_map": _jsonable(result),
    }


def _build_markdown(result: Any, metadata: dict[str, Any]) -> str:
    lines: list[str] = [
        "# CARSF V1.5 Public Data Pilot Reviewer Evidence Map",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report maps Build 27 public-data pilot evidence into reviewer-facing rows without loading new data.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in PUBLIC_DATA_EVIDENCE_MAP_NON_CLAIMS)
    lines.extend(["", "## C. How Reviewers Should Use This Map", ""])
    lines.extend(
        [
            "- Treat each row as a prompt for source, arithmetic, placeholder, blocker, or boundary inspection.",
            "- Treat confidence labels as evidence classifications only.",
            "- Do not treat this map as calibration, validation, readiness, or approval.",
        ]
    )
    lines.extend(["", "## D. Evidence Status Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(EVIDENCE_STATUS_VALUES))
    lines.extend(["", "## E. Reviewer Interpretation Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(REVIEWER_INTERPRETATION_VALUES))
    lines.extend(["", "## F. Confidence Labels", ""])
    lines.extend(f"- `{item}`" for item in sorted(CONFIDENCE_LABEL_VALUES))
    lines.extend(["", "## G. Source Evidence Map", ""])
    lines.extend(_source_table(result.source_evidence))
    lines.extend(["", "## H. Loaded Public Extract Evidence Map", ""])
    lines.extend(_extract_table(result.loaded_extract_evidence))
    lines.extend(["", "## I. Source-Reference-Only Evidence Map", ""])
    lines.extend(_extract_table(result.source_reference_only_evidence))
    lines.extend(["", "## J. Realistic Placeholder Evidence Map", ""])
    lines.extend(_placeholder_table(result.placeholder_evidence))
    lines.extend(["", "## K. Field Sanity Evidence Map", ""])
    lines.extend(_field_table(result.field_sanity_evidence))
    lines.extend(["", "## L. Module Sanity Evidence Map", ""])
    lines.extend(_module_table(result.module_sanity_evidence))
    lines.extend(["", "## M. Restricted Blocker Evidence Map", ""])
    lines.extend(_blocker_table(result.restricted_blocker_evidence))
    lines.extend(["", "## N. Forbidden Repo Data Evidence Map", ""])
    lines.extend(_blocker_table(result.forbidden_repo_data_evidence))
    lines.extend(["", "## O. Reviewer Questions", ""])
    lines.extend(_questions_table(result.reviewer_questions))
    lines.extend(["", "## P. What Became More Reviewable", ""])
    lines.append("Reviewers can now inspect source locators, arithmetic classification, placeholder anchors, field rows, module rows, and blocker rows in one report.")
    lines.extend(["", "## Q. What Still Cannot Be Claimed", ""])
    lines.append("This evidence map is not calibration, not validation, not tax-payable use, not legal sufficiency, not operational readiness, not official status, and not a firm-level liability change.")
    lines.extend(["", "## R. Build 29 Readiness", ""])
    lines.extend(f"- {item}" for item in result.build_29_requirements)
    lines.extend(["", "## S. Limitations and Future Work", ""])
    lines.extend(_summary_lines(result.summary))
    text = "\n".join(lines) + "\n"
    findings = find_forbidden_affirmative_public_data_claims(text)
    if findings:
        raise ValueError(f"generated public data evidence map Markdown contains forbidden affirmative claims: {', '.join(findings)}")
    return text


def run_public_data_evidence_map(
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
    public_pilot_report_path: Path = DEFAULT_PUBLIC_PILOT_REPORT_PATH,
) -> Any:
    manifest = _load_yaml(manifest_path)
    pilot_report = _load_json(public_pilot_report_path)
    return build_public_data_evidence_map_result(manifest, pilot_report)


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--public-pilot-report", type=Path, default=DEFAULT_PUBLIC_PILOT_REPORT_PATH)
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS_DIR)
    args = parser.parse_args(argv)

    args.reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    result = run_public_data_evidence_map(args.manifest, args.public_pilot_report)
    json_payload = _build_json_payload(result, metadata)
    json_text = json.dumps(json_payload, indent=2, sort_keys=True) + "\n"
    findings = find_forbidden_affirmative_public_data_claims(json_text)
    if findings:
        raise ValueError(f"generated public data evidence map JSON contains forbidden affirmative claims: {', '.join(findings)}")
    json_path = args.reports_dir / "public_data_evidence_map.json"
    md_path = args.reports_dir / "public_data_evidence_map.md"
    json_path.write_text(json_text, encoding="utf-8")
    md_path.write_text(_build_markdown(result, metadata), encoding="utf-8")

    print(f"source evidence items: {result.summary.total_source_evidence_items}")
    print(f"loaded public extract evidence items: {result.summary.total_loaded_public_extract_evidence_items}")
    print(f"source-reference-only evidence items: {result.summary.total_source_reference_only_evidence_items}")
    print(f"placeholder evidence items: {result.summary.total_placeholder_evidence_items}")
    print(f"reviewer questions: {result.summary.total_reviewer_questions}")
    print(f"new_data_loaded: {result.summary.new_data_loaded}")
    print(f"real_calibration_completed: {result.summary.real_calibration_completed}")
    print(f"validation_claimed: {result.summary.validation_claimed}")
    print(f"firm_level_liability_logic_modified: {result.summary.firm_level_liability_logic_modified}")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
