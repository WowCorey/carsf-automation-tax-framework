"""Run the CARSF V1.5 public-data source-locator verification pack."""

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
from carsf.source_locator_verification_pack import (  # noqa: E402
    LOCATOR_STATUS_VALUES,
    REVIEWER_WARNING_VALUES,
    SOURCE_LOCATOR_VERIFICATION_PACK_NON_CLAIMS,
    VERIFICATION_STATUS_VALUES,
    build_source_locator_verification_result,
    find_forbidden_affirmative_source_locator_claims,
)


REPORT_STATUS = "source_locator_verification_pack_only"
DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "public_pilot" / "source_locator_verification_manifest.yaml"
DEFAULT_PUBLIC_PILOT_REPORT_PATH = REPO_ROOT / "reports" / "public_data_pilot.json"
DEFAULT_EVIDENCE_MAP_REPORT_PATH = REPO_ROOT / "reports" / "public_data_evidence_map.json"
DEFAULT_CONSISTENCY_AUDIT_REPORT_PATH = REPO_ROOT / "reports" / "public_data_consistency_audit.json"
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
        f"- total_loaded_value_cards: {summary.total_loaded_value_cards}",
        f"- complete_locator_cards: {summary.complete_locator_cards}",
        f"- partial_locator_cards: {summary.partial_locator_cards}",
        f"- source_reference_only_cards: {summary.source_reference_only_cards}",
        f"- placeholder_anchor_cards: {summary.placeholder_anchor_cards}",
        f"- restricted_blocker_cards: {summary.restricted_blocker_cards}",
        f"- reviewer_checklist_items_total: {summary.reviewer_checklist_items_total}",
        f"- fair_work_arithmetic_cards: {summary.fair_work_arithmetic_cards}",
        f"- cards_ready_for_manual_review: {summary.cards_ready_for_manual_review}",
        f"- cards_source_locator_recorded_only: {summary.cards_source_locator_recorded_only}",
        f"- cards_source_reference_only_not_loaded: {summary.cards_source_reference_only_not_loaded}",
        f"- cards_placeholder_not_real_data: {summary.cards_placeholder_not_real_data}",
        f"- cards_blocked_until_authorised_access: {summary.cards_blocked_until_authorised_access}",
        f"- forbidden_claim_findings: {summary.forbidden_claim_findings}",
        f"- source_locator_pack_created: {summary.source_locator_pack_created}",
        f"- new_data_loaded: {summary.new_data_loaded}",
        f"- external_source_verification_claimed: {summary.external_source_verification_claimed}",
        f"- manual_review_pack_only: {summary.manual_review_pack_only}",
        f"- loaded_value_cards_created: {summary.loaded_value_cards_created}",
        f"- source_reference_only_cards_created: {summary.source_reference_only_cards_created}",
        f"- placeholder_anchor_cards_created: {summary.placeholder_anchor_cards_created}",
        f"- restricted_blocker_cards_created: {summary.restricted_blocker_cards_created}",
        f"- reviewer_checklists_created: {summary.reviewer_checklists_created}",
        f"- real_calibration_completed: {summary.real_calibration_completed}",
        f"- actual_tax_payable_determined: {summary.actual_tax_payable_determined}",
        f"- validation_claimed: {summary.validation_claimed}",
        f"- approval_claimed: {summary.approval_claimed}",
        f"- operational_readiness_claimed: {summary.operational_readiness_claimed}",
        f"- legal_sufficiency_claimed: {summary.legal_sufficiency_claimed}",
        f"- official_status_claimed: {summary.official_status_claimed}",
        f"- firm_level_liability_logic_modified: {summary.firm_level_liability_logic_modified}",
    ]


def _loaded_cards_table(items: list[Any]) -> list[str]:
    lines = [
        "| Card ID | Extract | Publisher | Locator Status | Verification Status | Values | Source Locator | Arithmetic | Must Not Infer |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.card_id} | {item.extract_id} | {item.publisher} | {item.locator_status} | "
            f"{item.verification_status} | {item.values_summary} | {item.source_locator} | "
            f"{item.arithmetic_check_summary} | must_not_infer: {_join_boundary_tokens(item.reviewer_must_not_infer)} |"
        )
    return lines


def _source_only_table(items: list[Any]) -> list[str]:
    lines = [
        "| Card ID | Extract | Publisher | Source URL | Locator Status | Verification Status | Why Not Loaded | Must Not Infer |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.card_id} | {item.extract_id} | {item.publisher} | {item.source_url} | {item.locator_status} | "
            f"{item.verification_status} | {item.why_not_loaded} | must_not_infer: {_join_boundary_tokens(item.reviewer_must_not_infer)} |"
        )
    return lines


def _placeholder_table(items: list[Any]) -> list[str]:
    lines = [
        "| Card ID | Anchor | Field | Anchor Strength | Anchored To Public Data | Verification Status | Missing Data | Must Not Infer |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.card_id} | {item.anchor_id} | {item.field_id} | {item.anchor_strength} | "
            f"{item.anchored_to_public_data} | {item.verification_status} | {_join(item.missing_data_for_calibration)} | "
            f"must_not_infer: {_join_boundary_tokens(item.reviewer_must_not_infer)} |"
        )
    return lines


def _blocker_table(items: list[Any]) -> list[str]:
    lines = [
        "| Card ID | Blocker | Type | Locator Status | Verification Status | Description | Required Access Or Review | Must Not Infer |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.card_id} | {item.blocker_id} | {item.blocker_type} | {item.locator_status} | {item.verification_status} | "
            f"{item.description} | {_join(item.required_access_or_review)} | must_not_infer: {_join_boundary_tokens(item.reviewer_must_not_infer)} |"
        )
    return lines


def _checklist_table(items: list[Any]) -> list[str]:
    lines = [
        "| Checklist ID | Prompt | Reviewer Warning | Must Not Infer |",
        "| --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.checklist_id} | {item.prompt} | {_join(item.reviewer_warning)} | must_not_infer: {_join_boundary_tokens(item.must_not_infer)} |"
        )
    return lines


def _build_json_payload(result: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": SOURCE_LOCATOR_VERIFICATION_PACK_NON_CLAIMS,
            "locator_status_values": sorted(LOCATOR_STATUS_VALUES),
            "verification_status_values": sorted(VERIFICATION_STATUS_VALUES),
            "reviewer_warning_values": sorted(REVIEWER_WARNING_VALUES),
        },
        "summary": _jsonable(result.summary),
        "source_locator_verification_pack": _jsonable(result),
    }


def _build_markdown(result: Any, metadata: dict[str, Any]) -> str:
    lines: list[str] = [
        "# CARSF V1.5 Public Data Source-Locator Verification Pack",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report packages existing Build 27-29 source-locator metadata into reviewer-facing cards without loading new data.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in SOURCE_LOCATOR_VERIFICATION_PACK_NON_CLAIMS)
    lines.extend(["", "## C. How Reviewers Should Use This Pack", ""])
    lines.extend(
        [
            "- Use each card to manually inspect source URL, source locator, value notes, unit, period, geography, and boundary warnings.",
            "- Treat ready_for_manual_review as locator metadata completeness only.",
            "- Do not treat this pack as external source verification, calibration, validation, legal sufficiency, official status, or tax-payable evidence.",
        ]
    )
    lines.extend(["", "## D. Locator Status Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(LOCATOR_STATUS_VALUES))
    lines.extend(["", "## E. Verification Status Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(VERIFICATION_STATUS_VALUES))
    lines.extend(["", "## F. Reviewer Warning Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(REVIEWER_WARNING_VALUES))
    lines.extend(["", "## G. Loaded Public Value Cards", ""])
    lines.extend(_loaded_cards_table(result.loaded_value_cards))
    lines.extend(["", "## H. Source-Reference-Only Cards", ""])
    lines.extend(_source_only_table(result.source_reference_only_cards))
    lines.extend(["", "## I. Placeholder Anchor Cards", ""])
    lines.extend(_placeholder_table(result.placeholder_anchor_cards))
    lines.extend(["", "## J. Restricted Blocker Cards", ""])
    lines.extend(_blocker_table(result.restricted_blocker_cards))
    lines.extend(["", "## K. Reviewer Checklists", ""])
    lines.extend(_checklist_table(result.reviewer_checklists))
    lines.extend(["", "## L. Source Locator Completeness Summary", ""])
    lines.extend(
        [
            f"- Complete locator cards: {result.summary.complete_locator_cards}",
            f"- Partial locator cards: {result.summary.partial_locator_cards}",
            f"- Source-reference-only cards: {result.summary.source_reference_only_cards}",
        ]
    )
    lines.extend(["", "## M. Manual Review Readiness Summary", ""])
    lines.extend(_summary_lines(result.summary))
    lines.extend(["", "## N. What This Pack Does Not Mean", ""])
    lines.extend(
        [
            "- It does not mean manual review has been completed.",
            "- It does not mean source values are externally verified.",
            "- It is not calibration, validation, legal advice, tax advice, ATO guidance, Treasury modelling, PBO costing, legal sufficiency, operational readiness, or official status.",
            "- It does not determine actual tax payable and does not modify firm-level CARSF liability.",
        ]
    )
    lines.extend(["", "## O. Build 29.6 Readiness", ""])
    lines.extend(f"- {item}" for item in result.build_29_6_requirements)
    lines.extend(["", "## P. Build 30 Readiness", ""])
    lines.extend(f"- {item}" for item in result.build_30_requirements)
    lines.extend(["", "## Q. Limitations and Future Work", ""])
    lines.extend(
        [
            "- Build 29.5 creates source-locator cards only from existing artefacts.",
            "- Future work may add reviewer objections or handoff material without loading new data or claiming calibration.",
        ]
    )
    return "\n".join(lines) + "\n"


def run(args: list[str] | None = None) -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--public-pilot-report", type=Path, default=DEFAULT_PUBLIC_PILOT_REPORT_PATH)
    parser.add_argument("--evidence-map-report", type=Path, default=DEFAULT_EVIDENCE_MAP_REPORT_PATH)
    parser.add_argument("--consistency-audit-report", type=Path, default=DEFAULT_CONSISTENCY_AUDIT_REPORT_PATH)
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS_DIR)
    namespace = parser.parse_args(args)

    manifest = _load_yaml(namespace.manifest)
    public_pilot_report = _load_json(namespace.public_pilot_report)
    evidence_map_report = _load_json(namespace.evidence_map_report)
    consistency_audit_report = _load_json(namespace.consistency_audit_report)

    result = build_source_locator_verification_result(
        manifest=manifest,
        public_pilot_report=public_pilot_report,
        evidence_map_report=evidence_map_report,
        consistency_audit_report=consistency_audit_report,
    )
    metadata = report_metadata()
    payload = _build_json_payload(result, metadata)
    markdown = _build_markdown(result, metadata)
    combined_for_claim_scan = json.dumps(payload, sort_keys=True) + "\n" + markdown
    forbidden = find_forbidden_affirmative_source_locator_claims(combined_for_claim_scan)
    if forbidden:
        raise ValueError(f"forbidden affirmative source-locator claims found in generated report: {', '.join(forbidden)}")

    namespace.reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = namespace.reports_dir / "source_locator_verification_pack.json"
    markdown_path = namespace.reports_dir / "source_locator_verification_pack.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    markdown_path.write_text(markdown, encoding="utf-8")

    summary = result.summary
    print(f"loaded value cards: {summary.total_loaded_value_cards}")
    print(f"source-reference-only cards: {summary.source_reference_only_cards}")
    print(f"placeholder anchor cards: {summary.placeholder_anchor_cards}")
    print(f"restricted blocker cards: {summary.restricted_blocker_cards}")
    print(f"reviewer checklist items: {summary.reviewer_checklist_items_total}")
    print(f"fair work arithmetic cards: {summary.fair_work_arithmetic_cards}")
    print(f"forbidden claim findings: {summary.forbidden_claim_findings}")
    print(f"new_data_loaded: {summary.new_data_loaded}")
    print(f"external_source_verification_claimed: {summary.external_source_verification_claimed}")
    print(f"real_calibration_completed: {summary.real_calibration_completed}")
    print(f"validation_claimed: {summary.validation_claimed}")
    print(f"firm_level_liability_logic_modified: {summary.firm_level_liability_logic_modified}")
    print(f"wrote {json_path}")
    print(f"wrote {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
