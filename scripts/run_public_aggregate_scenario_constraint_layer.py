"""Run the CARSF V1.5 public aggregate scenario constraint layer."""

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
from carsf.public_aggregate_scenario_constraint_layer import (  # noqa: E402
    CLAIM_LEVEL_VALUES,
    CONSTRAINT_STATUS_VALUES,
    DISPLAY_RULE_VALUES,
    FORBIDDEN_IMPLICATION_VALUES,
    SCENARIO_CONSTRAINT_NON_CLAIMS,
    SCENARIO_OUTPUT_STATUS_VALUES,
    build_public_aggregate_scenario_constraint_result,
    find_forbidden_affirmative_scenario_constraint_claims,
)


REPORT_STATUS = "public_aggregate_scenario_constraint_layer_only"
DEFAULT_MANIFEST_PATH = (
    REPO_ROOT / "data" / "public_real" / "manifests" / "public_aggregate_scenario_constraint_manifest.yaml"
)
DEFAULT_PUBLIC_VALUES_PATH = REPO_ROOT / "data" / "public_real" / "parsed" / "public_real_aggregate_values.json"
DEFAULT_SOURCE_MANIFEST_PATH = REPO_ROOT / "data" / "public_real" / "manifests" / "public_real_data_sources.yaml"
DEFAULT_REPLACEMENT_REPORT_PATH = REPO_ROOT / "reports" / "public_data_placeholder_replacement_map.json"
DEFAULT_BOUNDARY_REPORT_PATH = REPO_ROOT / "reports" / "public_aggregate_calibration_boundary_map.json"
DEFAULT_REPORTS_DIR = REPO_ROOT / "reports"


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def _load_yaml(path: Path) -> Any:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if payload is None:
        raise ValueError(f"YAML file is empty: {path}")
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
        f"- public_aggregate_scenario_constraint_layer_created: {summary.public_aggregate_scenario_constraint_layer_created}",
        f"- new_data_loaded: {summary.new_data_loaded}",
        f"- loaded_public_values_used: {summary.loaded_public_values_used}",
        f"- module_constraints_mapped: {summary.module_constraints_mapped}",
        f"- field_constraints_mapped: {summary.field_constraints_mapped}",
        f"- outputs_display_as_sanity_check_only: {summary.outputs_display_as_sanity_check_only}",
        f"- outputs_display_as_public_anchor_only: {summary.outputs_display_as_public_anchor_only}",
        f"- outputs_display_as_public_bound_only: {summary.outputs_display_as_public_bound_only}",
        f"- outputs_display_as_context_only: {summary.outputs_display_as_context_only}",
        f"- outputs_display_as_placeholder_narrowing_only: {summary.outputs_display_as_placeholder_narrowing_only}",
        f"- outputs_display_as_reviewer_traceability_only: {summary.outputs_display_as_reviewer_traceability_only}",
        f"- outputs_marked_non_interpretable: {summary.outputs_marked_non_interpretable}",
        f"- outputs_hidden_from_reviewer_dashboard: {summary.outputs_hidden_from_reviewer_dashboard}",
        f"- outputs_fail_closed_forbidden_claim: {summary.outputs_fail_closed_forbidden_claim}",
        f"- forbidden_implications_mapped: {summary.forbidden_implications_mapped}",
        f"- public_source_candidates_treated_as_loaded: {summary.public_source_candidates_treated_as_loaded}",
        f"- restricted_data_loaded: {summary.restricted_data_loaded}",
        f"- personal_data_loaded: {summary.personal_data_loaded}",
        f"- taxpayer_level_data_loaded: {summary.taxpayer_level_data_loaded}",
        f"- firm_confidential_data_loaded: {summary.firm_confidential_data_loaded}",
        f"- household_microdata_loaded: {summary.household_microdata_loaded}",
        f"- calibration_completed: {summary.calibration_completed}",
        f"- validation_claimed: {summary.validation_claimed}",
        f"- actual_tax_payable_determined: {summary.actual_tax_payable_determined}",
        f"- official_status_claimed: {summary.official_status_claimed}",
        f"- firm_level_liability_logic_modified: {summary.firm_level_liability_logic_modified}",
        f"- forbidden_claim_findings: {summary.forbidden_claim_findings}",
    ]


def _public_value_table(items: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Value ID | Source | Metric | Value | Unit | Period | Geography |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item['value_id']} | {item['source_id']} | {item['metric_name']} | {item['value']} | "
            f"{item['unit']} | {item['period']} | {item['geography']} |"
        )
    return lines


def _module_table(items: list[Any]) -> list[str]:
    lines = [
        "| Module | Output Status | Display Rule | Constraint Status | Claim Level | Allowed Display | Hidden Or Non-Interpretable | Evidence Needed |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.module_name} | {item.scenario_output_status} | {item.display_rule} | {item.constraint_status} | "
            f"{item.claim_level} | {_join(item.allowed_display_outputs)} | "
            f"{item.what_must_be_hidden_or_marked_non_interpretable} | {_join(item.evidence_needed_to_lift_constraint)} |"
        )
    return lines


def _field_table(items: list[Any]) -> list[str]:
    lines = [
        "| Field | Placeholder | Output Status | Display Rule | Constraint Status | Claim Level | Linked Values | Evidence Needed |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.field_id} | {item.placeholder_id} | {item.scenario_output_status} | {item.display_rule} | "
            f"{item.constraint_status} | {item.claim_level} | {_join(item.linked_public_value_ids)} | "
            f"{_join(item.evidence_needed_to_lift_constraint)} |"
        )
    return lines


def _implication_table(items: list[Any]) -> list[str]:
    lines = [
        "| Implication | Constraint Action | Reviewer Warning |",
        "| --- | --- | --- |",
    ]
    for item in items:
        lines.append(f"| {item.implication} | {item.constraint_action} | {item.reviewer_warning} |")
    return lines


def _build_json_payload(result: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": SCENARIO_CONSTRAINT_NON_CLAIMS,
            "scenario_output_status_values": sorted(SCENARIO_OUTPUT_STATUS_VALUES),
            "display_rule_values": sorted(DISPLAY_RULE_VALUES),
            "forbidden_implication_values": sorted(FORBIDDEN_IMPLICATION_VALUES),
            "constraint_status_values": sorted(CONSTRAINT_STATUS_VALUES),
            "claim_level_values": sorted(CLAIM_LEVEL_VALUES),
        },
        "summary": _jsonable(result.summary),
        "public_aggregate_scenario_constraint_layer": _jsonable(result),
    }


def _build_markdown(result: Any, metadata: dict[str, Any]) -> str:
    modules = result.module_scenario_constraints
    fields = result.field_scenario_constraints
    by_status = {status: [item for item in modules if item.scenario_output_status == status] for status in SCENARIO_OUTPUT_STATUS_VALUES}
    lines: list[str] = [
        "# CARSF V1.5 Public Aggregate Scenario Constraint Layer",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report constrains scenario outputs using the Build 33 public aggregate calibration-boundary map.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in SCENARIO_CONSTRAINT_NON_CLAIMS)
    lines.extend(["", "## C. Input Public Aggregate Values", ""])
    lines.extend(_public_value_table(result.public_aggregate_values))
    lines.extend(["", "## D. Scenario Output Status Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(SCENARIO_OUTPUT_STATUS_VALUES))
    lines.extend(["", "## E. Display Rule Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(DISPLAY_RULE_VALUES))
    lines.extend(["", "## F. Forbidden Implication Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(FORBIDDEN_IMPLICATION_VALUES))
    lines.extend(["", "## G. Constraint Status Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(CONSTRAINT_STATUS_VALUES))
    lines.extend(["", "## H. Claim Level Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(CLAIM_LEVEL_VALUES))
    lines.extend(["", "## I. Module Scenario Constraints", ""])
    lines.extend(_module_table(modules))
    lines.extend(["", "## J. Field Scenario Constraints", ""])
    lines.extend(_field_table(fields))
    lines.extend(["", "## K. Outputs Displayed As Sanity Check Only", ""])
    lines.extend(_module_table(by_status["display_as_sanity_check_only"]))
    lines.extend(["", "## L. Outputs Displayed As Public Aggregate Anchor Only", ""])
    lines.extend(_module_table(by_status["display_as_public_aggregate_anchor_only"]))
    lines.extend(["", "## M. Outputs Displayed As Public Aggregate Bound Only", ""])
    lines.extend(_module_table(by_status["display_as_public_aggregate_bound_only"]))
    lines.extend(["", "## N. Outputs Displayed As Context Only", ""])
    lines.extend(_module_table(by_status["display_as_context_only"]))
    lines.extend(["", "## O. Outputs Displayed As Placeholder Narrowing Only", ""])
    lines.extend(_module_table(by_status["display_as_placeholder_narrowing_only"]))
    lines.extend(["", "## P. Outputs Displayed As Reviewer Traceability Only", ""])
    lines.extend(_module_table(by_status["display_as_reviewer_traceability_only"]))
    lines.extend(["", "## Q. Outputs Marked Non-Interpretable", ""])
    lines.extend(_module_table(by_status["mark_non_interpretable"]))
    lines.extend(["", "## R. Outputs Hidden From Reviewer Dashboard", ""])
    lines.extend(_module_table(by_status["hide_from_reviewer_dashboard"]))
    lines.extend(["", "## S. Forbidden Implications Mapped", ""])
    lines.extend(_implication_table(result.forbidden_scenario_implications))
    lines.extend(["", "## T. What Can Be Displayed", ""])
    lines.extend(f"- `{item.module_id}`: {item.what_can_be_displayed}" for item in modules)
    lines.extend(["", "## U. What Must Be Hidden Or Marked Non-Interpretable", ""])
    lines.extend(f"- `{item.module_id}`: {item.what_must_be_hidden_or_marked_non_interpretable}" for item in modules)
    lines.extend(["", "## V. Evidence Needed To Lift Constraints", ""])
    lines.extend(f"- `{item.module_id}`: {_join(item.evidence_needed_to_lift_constraint)}" for item in modules)
    lines.extend(["", "## W. Build 35 Readiness", ""])
    lines.extend(f"- {item}" for item in result.future_build_35_requirements)
    lines.extend(["", "## X. Limitations and Future Work", ""])
    lines.extend(
        [
            "- Build 34 does not load new data.",
            "- Scenario constraints do not create calibration or validation.",
            "- Hidden and non-interpretable outputs remain unavailable as reviewer-facing evidence.",
            "- Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-34 are included in a later sealed RC.",
        ]
    )
    lines.extend(["", "## Summary Counts", ""])
    lines.extend(_summary_lines(result.summary))
    lines.append("")
    return "\n".join(lines)


def run(
    manifest_path: Path,
    public_values_path: Path,
    source_manifest_path: Path,
    replacement_report_path: Path,
    boundary_report_path: Path,
    reports_dir: Path,
) -> dict[str, Any]:
    result = build_public_aggregate_scenario_constraint_result(
        _load_yaml(manifest_path),
        _load_json(public_values_path),
        _load_yaml(source_manifest_path),
        _load_json(replacement_report_path),
        _load_json(boundary_report_path),
    )
    metadata = report_metadata()
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_payload = _build_json_payload(result, metadata)
    markdown = _build_markdown(result, metadata)
    combined = markdown + "\n" + json.dumps(json_payload, sort_keys=True)
    findings = find_forbidden_affirmative_scenario_constraint_claims(combined)
    if findings:
        raise ValueError(f"forbidden affirmative scenario constraint claims found: {findings}")
    json_payload["summary"]["forbidden_claim_findings"] = len(findings)
    json_path = reports_dir / "public_aggregate_scenario_constraint_layer.json"
    md_path = reports_dir / "public_aggregate_scenario_constraint_layer.md"
    json_path.write_text(json.dumps(json_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return json_payload


def parse_args() -> ArgumentParser:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--public-values", type=Path, default=DEFAULT_PUBLIC_VALUES_PATH)
    parser.add_argument("--source-manifest", type=Path, default=DEFAULT_SOURCE_MANIFEST_PATH)
    parser.add_argument("--replacement-report", type=Path, default=DEFAULT_REPLACEMENT_REPORT_PATH)
    parser.add_argument("--boundary-report", type=Path, default=DEFAULT_BOUNDARY_REPORT_PATH)
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS_DIR)
    return parser


def main() -> int:
    args = parse_args().parse_args()
    payload = run(
        args.manifest,
        args.public_values,
        args.source_manifest,
        args.replacement_report,
        args.boundary_report,
        args.reports_dir,
    )
    summary = payload["summary"]
    print(f"public aggregate scenario constraint layer created: {summary['public_aggregate_scenario_constraint_layer_created']}")
    print(f"new data loaded: {summary['new_data_loaded']}")
    print(f"loaded public values used: {summary['loaded_public_values_used']}")
    print(f"module constraints mapped: {summary['module_constraints_mapped']}")
    print(f"field constraints mapped: {summary['field_constraints_mapped']}")
    print(f"outputs marked non-interpretable: {summary['outputs_marked_non_interpretable']}")
    print(f"outputs hidden from reviewer dashboard: {summary['outputs_hidden_from_reviewer_dashboard']}")
    print(f"forbidden implications mapped: {summary['forbidden_implications_mapped']}")
    print(f"source candidates treated as loaded: {summary['public_source_candidates_treated_as_loaded']}")
    print(f"calibration completed: {summary['calibration_completed']}")
    print(f"validation claimed: {summary['validation_claimed']}")
    print(f"actual tax payable determined: {summary['actual_tax_payable_determined']}")
    print(f"firm-level liability logic modified: {summary['firm_level_liability_logic_modified']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
