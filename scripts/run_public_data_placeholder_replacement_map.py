"""Run the CARSF V1.5 public data placeholder replacement map."""

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
from carsf.public_data_placeholder_replacement_map import (  # noqa: E402
    BLOCKER_TYPE_VALUES,
    CLAIM_LEVEL_VALUES,
    PLACEHOLDER_REPLACEMENT_NON_CLAIMS,
    REPLACEMENT_CONFIDENCE_VALUES,
    REPLACEMENT_STATUS_VALUES,
    build_public_data_placeholder_replacement_result,
    find_forbidden_affirmative_placeholder_replacement_claims,
)


REPORT_STATUS = "public_data_placeholder_replacement_map_only"
DEFAULT_MANIFEST_PATH = (
    REPO_ROOT / "data" / "public_real" / "manifests" / "public_placeholder_replacement_manifest.yaml"
)
DEFAULT_PUBLIC_VALUES_PATH = REPO_ROOT / "data" / "public_real" / "parsed" / "public_real_aggregate_values.json"
DEFAULT_SOURCE_MANIFEST_PATH = REPO_ROOT / "data" / "public_real" / "manifests" / "public_real_data_sources.yaml"
DEFAULT_PLACEHOLDER_ANCHORS_PATH = (
    REPO_ROOT / "data" / "public_pilot" / "placeholders" / "realistic_placeholder_anchors.yaml"
)
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
        f"- placeholder_replacement_map_created: {summary.placeholder_replacement_map_created}",
        f"- new_data_loaded: {summary.new_data_loaded}",
        f"- loaded_public_values_used: {summary.loaded_public_values_used}",
        f"- placeholders_mapped: {summary.placeholders_mapped}",
        f"- placeholders_replaced_by_public_anchor: {summary.placeholders_replaced_by_public_anchor}",
        f"- placeholders_narrowed_by_public_anchor: {summary.placeholders_narrowed_by_public_anchor}",
        f"- placeholders_informed_by_public_anchor: {summary.placeholders_informed_by_public_anchor}",
        f"- placeholders_still_placeholder_only: {summary.placeholders_still_placeholder_only}",
        f"- placeholders_blocked_until_restricted_data: {summary.placeholders_blocked_until_restricted_data}",
        f"- placeholders_blocked_until_external_review: {summary.placeholders_blocked_until_external_review}",
        f"- placeholders_cannot_replace_with_public_aggregate_data: {summary.placeholders_cannot_replace_with_public_aggregate_data}",
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


def _decision_table(items: list[Any]) -> list[str]:
    lines = [
        "| Decision | Placeholder | Field | Status | Confidence | Claim Level | Linked Values | What Changed | Remaining Blockers |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.decision_id} | {item.placeholder_name} | {item.field_id} | {item.replacement_status} | "
            f"{item.replacement_confidence} | {item.claim_level} | {_join(item.linked_public_value_ids)} | "
            f"{item.what_changed} | {_join(item.remaining_blockers)} |"
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
            "non_claims": PLACEHOLDER_REPLACEMENT_NON_CLAIMS,
            "replacement_status_values": sorted(REPLACEMENT_STATUS_VALUES),
            "replacement_confidence_values": sorted(REPLACEMENT_CONFIDENCE_VALUES),
            "blocker_type_values": sorted(BLOCKER_TYPE_VALUES),
            "claim_level_values": sorted(CLAIM_LEVEL_VALUES),
        },
        "summary": _jsonable(result.summary),
        "public_data_placeholder_replacement_map": _jsonable(result),
    }


def _build_markdown(result: Any, metadata: dict[str, Any]) -> str:
    decisions = result.replacement_decisions
    by_status = {status: [item for item in decisions if item.replacement_status == status] for status in REPLACEMENT_STATUS_VALUES}
    lines: list[str] = [
        "# CARSF V1.5 Public Data Placeholder Replacement Map",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report maps Build 31 public aggregate values to existing realistic placeholders.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in PLACEHOLDER_REPLACEMENT_NON_CLAIMS)
    lines.extend(["", "## C. Input Public Aggregate Values", ""])
    lines.extend(_public_value_table(result.public_aggregate_anchors))
    lines.extend(["", "## D. Replacement Status Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(REPLACEMENT_STATUS_VALUES))
    lines.extend(["", "## E. Replacement Confidence Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(REPLACEMENT_CONFIDENCE_VALUES))
    lines.extend(["", "## F. Placeholder Replacement Decisions", ""])
    lines.extend(_decision_table(decisions))
    lines.extend(["", "## G. Replaced By Public Aggregate Anchor", ""])
    lines.extend(_decision_table(by_status["replaced_by_public_aggregate_anchor"]))
    lines.extend(["", "## H. Narrowed By Public Aggregate Anchor", ""])
    lines.extend(_decision_table(by_status["narrowed_by_public_aggregate_anchor"]))
    lines.extend(["", "## I. Informed By Public Aggregate Anchor", ""])
    lines.extend(_decision_table(by_status["informed_by_public_aggregate_anchor"]))
    lines.extend(["", "## J. Still Placeholder Only", ""])
    lines.extend(_decision_table(by_status["still_placeholder_only"]))
    lines.extend(["", "## K. Blocked Until Restricted Data", ""])
    lines.extend(_decision_table(by_status["blocked_until_restricted_data"]))
    lines.extend(["", "## L. Blocked Until External Review", ""])
    external_review_items = [item for item in decisions if item.requires_external_review]
    lines.extend(_decision_table(external_review_items))
    lines.extend(["", "## M. Source Candidates Not Loaded", ""])
    lines.extend(_candidate_table(result.source_candidates_not_loaded))
    lines.extend(["", "## N. What Changed", ""])
    lines.extend(f"- `{item.placeholder_id}`: {item.what_changed}" for item in decisions)
    lines.extend(["", "## O. What Did Not Change", ""])
    lines.extend(f"- `{item.placeholder_id}`: {item.what_did_not_change}" for item in decisions)
    lines.extend(["", "## P. Calibration Blockers Still Remaining", ""])
    lines.extend(
        f"- `{item.placeholder_id}` still needs: {_join(item.evidence_needed_before_calibration)}"
        for item in decisions
    )
    lines.extend(["", "## Q. Build 33 Readiness", ""])
    lines.extend(f"- {item}" for item in result.future_build_33_requirements)
    lines.extend(["", "## R. Limitations and Future Work", ""])
    lines.extend(
        [
            "- Build 32 does not load new data.",
            "- Public aggregate anchors can make placeholder treatment clearer but cannot create calibration or validation.",
            "- Restricted-data and external-review blockers remain visible.",
            "- Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-32 are included in a later sealed RC.",
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
    placeholder_anchors_path: Path,
    reports_dir: Path,
) -> dict[str, Any]:
    manifest = _load_yaml(manifest_path)
    if not isinstance(manifest, dict):
        raise ValueError("replacement manifest must be a mapping")
    public_values = _load_json(public_values_path)
    source_manifest = _load_yaml(source_manifest_path)
    if not isinstance(source_manifest, dict):
        raise ValueError("public real data source manifest must be a mapping")
    placeholder_anchors = _load_yaml(placeholder_anchors_path)
    if not isinstance(placeholder_anchors, list):
        raise ValueError("placeholder anchors must be a YAML list")

    for artifact in manifest["input_artifacts"]:
        artifact_path = REPO_ROOT / artifact
        if not artifact_path.exists():
            raise ValueError(f"required input artifact missing: {artifact}")

    result = build_public_data_placeholder_replacement_result(
        manifest=manifest,
        public_values_payload=public_values,
        placeholder_anchor_payload=placeholder_anchors,
        source_manifest=source_manifest,
    )
    metadata = report_metadata()
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_payload = _build_json_payload(result, metadata)
    markdown = _build_markdown(result, metadata)
    combined_for_scan = markdown + "\n" + json.dumps(json_payload, sort_keys=True)
    forbidden_claims = find_forbidden_affirmative_placeholder_replacement_claims(combined_for_scan)
    if forbidden_claims:
        raise ValueError(f"placeholder replacement output contains forbidden affirmative claims: {', '.join(forbidden_claims)}")
    json_path = reports_dir / "public_data_placeholder_replacement_map.json"
    md_path = reports_dir / "public_data_placeholder_replacement_map.md"
    json_path.write_text(json.dumps(json_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return json_payload


def main() -> None:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-path", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--public-values-path", type=Path, default=DEFAULT_PUBLIC_VALUES_PATH)
    parser.add_argument("--source-manifest-path", type=Path, default=DEFAULT_SOURCE_MANIFEST_PATH)
    parser.add_argument("--placeholder-anchors-path", type=Path, default=DEFAULT_PLACEHOLDER_ANCHORS_PATH)
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS_DIR)
    args = parser.parse_args()

    payload = run(
        manifest_path=args.manifest_path,
        public_values_path=args.public_values_path,
        source_manifest_path=args.source_manifest_path,
        placeholder_anchors_path=args.placeholder_anchors_path,
        reports_dir=args.reports_dir,
    )
    summary = payload["summary"]
    print(f"placeholder replacement map created: {summary['placeholder_replacement_map_created']}")
    print(f"new data loaded: {summary['new_data_loaded']}")
    print(f"loaded public values used: {summary['loaded_public_values_used']}")
    print(f"placeholders mapped: {summary['placeholders_mapped']}")
    print(f"placeholders replaced by public anchor: {summary['placeholders_replaced_by_public_anchor']}")
    print(f"placeholders narrowed by public anchor: {summary['placeholders_narrowed_by_public_anchor']}")
    print(f"placeholders informed by public anchor: {summary['placeholders_informed_by_public_anchor']}")
    print(f"source candidates treated as loaded: {summary['public_source_candidates_treated_as_loaded']}")
    print(f"calibration completed: {summary['calibration_completed']}")
    print(f"validation claimed: {summary['validation_claimed']}")
    print(f"actual tax payable determined: {summary['actual_tax_payable_determined']}")
    print(f"firm-level liability logic modified: {summary['firm_level_liability_logic_modified']}")


if __name__ == "__main__":
    main()
