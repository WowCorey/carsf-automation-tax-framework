"""Run the CARSF V1.5 public aggregate calibration-boundary map."""

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
from carsf.public_aggregate_calibration_boundary_map import (  # noqa: E402
    ALLOWED_USE_TYPE_VALUES,
    BLOCKER_TYPE_VALUES,
    BOUNDARY_STATUS_VALUES,
    CALIBRATION_BOUNDARY_NON_CLAIMS,
    CLAIM_LEVEL_VALUES,
    FORBIDDEN_USE_TYPE_VALUES,
    build_public_aggregate_calibration_boundary_result,
    find_forbidden_affirmative_calibration_boundary_claims,
)


REPORT_STATUS = "public_aggregate_calibration_boundary_map_only"
DEFAULT_MANIFEST_PATH = (
    REPO_ROOT / "data" / "public_real" / "manifests" / "public_aggregate_calibration_boundary_manifest.yaml"
)
DEFAULT_PUBLIC_VALUES_PATH = REPO_ROOT / "data" / "public_real" / "parsed" / "public_real_aggregate_values.json"
DEFAULT_SOURCE_MANIFEST_PATH = REPO_ROOT / "data" / "public_real" / "manifests" / "public_real_data_sources.yaml"
DEFAULT_REPLACEMENT_REPORT_PATH = REPO_ROOT / "reports" / "public_data_placeholder_replacement_map.json"
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
        f"- public_aggregate_calibration_boundary_map_created: {summary.public_aggregate_calibration_boundary_map_created}",
        f"- new_data_loaded: {summary.new_data_loaded}",
        f"- loaded_public_values_used: {summary.loaded_public_values_used}",
        f"- module_boundaries_mapped: {summary.module_boundaries_mapped}",
        f"- field_boundaries_mapped: {summary.field_boundaries_mapped}",
        f"- modules_allowed_sanity_check_only: {summary.modules_allowed_sanity_check_only}",
        f"- modules_allowed_anchor_only: {summary.modules_allowed_anchor_only}",
        f"- modules_allowed_bound_only: {summary.modules_allowed_bound_only}",
        f"- modules_allowed_context_only: {summary.modules_allowed_context_only}",
        f"- modules_blocked_for_calibration: {summary.modules_blocked_for_calibration}",
        f"- modules_requiring_restricted_data: {summary.modules_requiring_restricted_data}",
        f"- modules_requiring_external_review: {summary.modules_requiring_external_review}",
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


def _public_value_table(items: list[Any]) -> list[str]:
    lines = [
        "| Value ID | Source | Metric | Value | Unit | Period | Geography |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.value_id} | {item.source_id} | {item.metric_name} | {item.value} | {item.unit} | "
            f"{item.period} | {item.geography} |"
        )
    return lines


def _module_table(items: list[Any]) -> list[str]:
    lines = [
        "| Module | Status | Claim Level | Allowed Uses | Linked Values | Can Support | Cannot Support | Blockers |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.module_name} | {item.boundary_status} | {item.claim_level} | "
            f"{_join(item.allowed_use_types)} | {_join(item.linked_public_value_ids)} | "
            f"{item.what_public_data_can_support} | {item.what_public_data_cannot_support} | "
            f"{_join(item.calibration_blockers_remaining)} |"
        )
    return lines


def _field_table(items: list[Any]) -> list[str]:
    lines = [
        "| Field | Placeholder | Status | Claim Level | Allowed Uses | Linked Values | Evidence Needed |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.field_id} | {item.placeholder_id} | {item.boundary_status} | {item.claim_level} | "
            f"{_join(item.allowed_use_types)} | {_join(item.linked_public_value_ids)} | "
            f"{_join(item.evidence_needed_before_calibration)} |"
        )
    return lines


def _candidate_table(items: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Source ID | Publisher | Source | Status | Reason | Treated As Loaded |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item['source_id']} | {item['publisher']} | {item['source_name']} | {item['loaded_status']} | "
            f"{item['reason_if_not_loaded']} | {item['treated_as_loaded']} |"
        )
    return lines


def _build_json_payload(result: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": CALIBRATION_BOUNDARY_NON_CLAIMS,
            "allowed_use_type_values": sorted(ALLOWED_USE_TYPE_VALUES),
            "forbidden_use_type_values": sorted(FORBIDDEN_USE_TYPE_VALUES),
            "boundary_status_values": sorted(BOUNDARY_STATUS_VALUES),
            "claim_level_values": sorted(CLAIM_LEVEL_VALUES),
            "blocker_type_values": sorted(BLOCKER_TYPE_VALUES),
        },
        "summary": _jsonable(result.summary),
        "public_aggregate_calibration_boundary_map": _jsonable(result),
    }


def _build_markdown(result: Any, metadata: dict[str, Any]) -> str:
    modules = result.module_boundary_decisions
    fields = result.field_boundary_decisions
    by_status = {status: [item for item in modules if item.boundary_status == status] for status in BOUNDARY_STATUS_VALUES}
    anchor_modules = [item for item in modules if "public_aggregate_anchor_only" in item.allowed_use_types]
    bound_modules = [item for item in modules if "public_aggregate_bound_only" in item.allowed_use_types]
    context_modules = [item for item in modules if "contextual_reference_only" in item.allowed_use_types]
    restricted_modules = [item for item in modules if item.requires_restricted_data]
    external_modules = [item for item in modules if item.requires_external_review]
    lines: list[str] = [
        "# CARSF V1.5 Public Aggregate Calibration Boundary Map",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report defines how loaded public aggregate values may be used as boundary inputs across CARSF.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in CALIBRATION_BOUNDARY_NON_CLAIMS)
    lines.extend(["", "## C. Input Public Aggregate Values", ""])
    lines.extend(_public_value_table(result.public_aggregate_values))
    lines.extend(["", "## D. Allowed Use Type Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(ALLOWED_USE_TYPE_VALUES))
    lines.extend(["", "## E. Forbidden Use Type Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(FORBIDDEN_USE_TYPE_VALUES))
    lines.extend(["", "## F. Boundary Status Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(BOUNDARY_STATUS_VALUES))
    lines.extend(["", "## G. Claim Level Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(CLAIM_LEVEL_VALUES))
    lines.extend(["", "## H. Module Calibration Boundary Decisions", ""])
    lines.extend(_module_table(modules))
    lines.extend(["", "## I. Field Calibration Boundary Decisions", ""])
    lines.extend(_field_table(fields))
    lines.extend(["", "## J. What Public Aggregate Data Can Support", ""])
    lines.extend(f"- `{item.module_id}`: {item.what_public_data_can_support}" for item in modules)
    lines.extend(["", "## K. What Public Aggregate Data Cannot Support", ""])
    lines.extend(f"- `{item.module_id}`: {item.what_public_data_cannot_support}" for item in modules)
    lines.extend(["", "## L. Modules Allowed Sanity Checks Only", ""])
    lines.extend(_module_table([item for item in modules if "sanity_check_only" in item.allowed_use_types]))
    lines.extend(["", "## M. Modules Allowed Public Aggregate Anchors", ""])
    lines.extend(_module_table(anchor_modules))
    lines.extend(["", "## N. Modules Allowed Public Aggregate Bounds", ""])
    lines.extend(_module_table(bound_modules))
    lines.extend(["", "## O. Modules Allowed Context Only", ""])
    lines.extend(_module_table(context_modules))
    lines.extend(["", "## P. Modules Blocked For Calibration", ""])
    lines.extend(
        _module_table(
            by_status["blocked_for_calibration"]
            + by_status["requires_restricted_data"]
            + by_status["requires_external_review"]
            + by_status["forbidden_for_claim"]
        )
    )
    lines.extend(["", "## Q. Modules Requiring Restricted Data", ""])
    lines.extend(_module_table(restricted_modules))
    lines.extend(["", "## R. Modules Requiring External Review", ""])
    lines.extend(_module_table(external_modules))
    lines.extend(["", "## S. Source Candidates Not Loaded", ""])
    lines.extend(_candidate_table(result.source_candidates_not_loaded))
    lines.extend(["", "## T. Calibration Blockers Still Remaining", ""])
    lines.extend(
        f"- `{item.module_id}` still needs: {_join(item.evidence_needed_before_calibration)}"
        for item in modules
    )
    lines.extend(["", "## U. Build 34 Readiness", ""])
    lines.extend(f"- {item}" for item in result.future_build_34_requirements)
    lines.extend(["", "## V. Limitations and Future Work", ""])
    lines.extend(
        [
            "- Build 33 does not load new data.",
            "- Public aggregate boundary labels do not create calibration or validation.",
            "- Modules requiring external review are boundary-limited; the label does not mean every use is fully blocked.",
            "- Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-33 are included in a later sealed RC.",
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
    reports_dir: Path,
) -> dict[str, Any]:
    manifest = _load_yaml(manifest_path)
    if not isinstance(manifest, dict):
        raise ValueError("boundary manifest must be a mapping")
    public_values = _load_json(public_values_path)
    source_manifest = _load_yaml(source_manifest_path)
    if not isinstance(source_manifest, dict):
        raise ValueError("public real data source manifest must be a mapping")
    replacement_report = _load_json(replacement_report_path)

    for artifact in manifest["input_artifacts"]:
        artifact_path = REPO_ROOT / artifact
        if not artifact_path.exists():
            raise ValueError(f"required input artifact missing: {artifact}")

    result = build_public_aggregate_calibration_boundary_result(
        manifest=manifest,
        public_values_payload=public_values,
        source_manifest=source_manifest,
        replacement_report=replacement_report,
    )
    metadata = report_metadata()
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_payload = _build_json_payload(result, metadata)
    markdown = _build_markdown(result, metadata)
    combined_for_scan = markdown + "\n" + json.dumps(json_payload, sort_keys=True)
    forbidden_claims = find_forbidden_affirmative_calibration_boundary_claims(combined_for_scan)
    if forbidden_claims:
        raise ValueError(f"calibration boundary output contains forbidden affirmative claims: {', '.join(forbidden_claims)}")
    json_path = reports_dir / "public_aggregate_calibration_boundary_map.json"
    md_path = reports_dir / "public_aggregate_calibration_boundary_map.md"
    json_path.write_text(json.dumps(json_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return json_payload


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-path", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--public-values-path", type=Path, default=DEFAULT_PUBLIC_VALUES_PATH)
    parser.add_argument("--source-manifest-path", type=Path, default=DEFAULT_SOURCE_MANIFEST_PATH)
    parser.add_argument("--replacement-report-path", type=Path, default=DEFAULT_REPLACEMENT_REPORT_PATH)
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS_DIR)
    args = parser.parse_args()

    payload = run(
        manifest_path=args.manifest_path,
        public_values_path=args.public_values_path,
        source_manifest_path=args.source_manifest_path,
        replacement_report_path=args.replacement_report_path,
        reports_dir=args.reports_dir,
    )
    summary = payload["summary"]
    print(f"public aggregate calibration boundary map created: {summary['public_aggregate_calibration_boundary_map_created']}")
    print(f"new data loaded: {summary['new_data_loaded']}")
    print(f"loaded public values used: {summary['loaded_public_values_used']}")
    print(f"module boundaries mapped: {summary['module_boundaries_mapped']}")
    print(f"field boundaries mapped: {summary['field_boundaries_mapped']}")
    print(f"modules blocked for calibration: {summary['modules_blocked_for_calibration']}")
    print(f"modules requiring restricted data: {summary['modules_requiring_restricted_data']}")
    print(f"modules requiring external review: {summary['modules_requiring_external_review']}")
    print(f"source candidates treated as loaded: {summary['public_source_candidates_treated_as_loaded']}")
    print(f"calibration completed: {summary['calibration_completed']}")
    print(f"validation claimed: {summary['validation_claimed']}")
    print(f"actual tax payable determined: {summary['actual_tax_payable_determined']}")
    print(f"firm-level liability logic modified: {summary['firm_level_liability_logic_modified']}")


if __name__ == "__main__":
    main()
