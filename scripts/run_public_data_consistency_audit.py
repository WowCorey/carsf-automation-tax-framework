"""Run the CARSF V1.5 public-data pilot consistency audit report."""

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
from carsf.public_data_consistency_audit import (  # noqa: E402
    AUDIT_STATUS_VALUES,
    AUDIT_TYPE_VALUES,
    PUBLIC_DATA_CONSISTENCY_AUDIT_NON_CLAIMS,
    RECONCILIATION_SCOPE_VALUES,
    build_public_data_consistency_audit_result,
)
from carsf.public_data_pilot import find_forbidden_affirmative_public_data_claims  # noqa: E402


REPORT_STATUS = "internal_consistency_audit_only"
DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "public_pilot" / "consistency_audit_manifest.yaml"
DEFAULT_PUBLIC_PILOT_REPORT_PATH = REPO_ROOT / "reports" / "public_data_pilot.json"
DEFAULT_PUBLIC_PILOT_MARKDOWN_PATH = REPO_ROOT / "reports" / "public_data_pilot.md"
DEFAULT_EVIDENCE_MAP_REPORT_PATH = REPO_ROOT / "reports" / "public_data_evidence_map.json"
DEFAULT_EVIDENCE_MAP_MARKDOWN_PATH = REPO_ROOT / "reports" / "public_data_evidence_map.md"
DEFAULT_DIGEST_PATH = REPO_ROOT / "data" / "public_pilot" / "digests" / "public_data_pilot_digests.json"
DEFAULT_DASHBOARD_PATH = REPO_ROOT / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py"
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
        f"- Total audit findings: {summary.total_audit_findings}",
        f"- Findings reconciled: {summary.findings_reconciled}",
        f"- Findings warning: {summary.findings_warning}",
        f"- Findings blocked: {summary.findings_blocked}",
        f"- Findings not applicable: {summary.findings_not_applicable}",
        f"- Findings fail closed: {summary.findings_fail_closed}",
        f"- Source references total: {summary.source_references_total}",
        f"- Loaded public extracts total: {summary.loaded_public_extracts_total}",
        f"- Source-reference-only extracts total: {summary.source_reference_only_extracts_total}",
        f"- Placeholder anchors total: {summary.placeholder_anchors_total}",
        f"- Field sanity checks total: {summary.field_sanity_checks_total}",
        f"- Module sanity checks total: {summary.module_sanity_checks_total}",
        f"- Restricted blockers total: {summary.restricted_blockers_total}",
        f"- Forbidden repo data items total: {summary.forbidden_repo_data_items_total}",
        f"- Digest targets total: {summary.digest_targets_total}",
        f"- Digest self-hash findings: {summary.digest_self_hash_findings}",
        f"- Forbidden claim findings: {summary.forbidden_claim_findings}",
        f"- Non-claim boundary failures: {summary.non_claim_boundary_failures}",
        f"- consistency_audit_created: {summary.consistency_audit_created}",
        f"- new_data_loaded: {summary.new_data_loaded}",
        f"- external_source_verification_claimed: {summary.external_source_verification_claimed}",
        f"- source_references_reconciled: {summary.source_references_reconciled}",
        f"- extract_evidence_reconciled: {summary.extract_evidence_reconciled}",
        f"- source_reference_only_counts_reconciled: {summary.source_reference_only_counts_reconciled}",
        f"- arithmetic_checks_reconciled: {summary.arithmetic_checks_reconciled}",
        f"- placeholder_boundaries_preserved: {summary.placeholder_boundaries_preserved}",
        f"- module_calibration_boundaries_preserved: {summary.module_calibration_boundaries_preserved}",
        f"- restricted_blockers_preserved: {summary.restricted_blockers_preserved}",
        f"- forbidden_repo_data_preserved: {summary.forbidden_repo_data_preserved}",
        f"- digest_consistency_checked: {summary.digest_consistency_checked}",
        f"- report_json_consistency_checked: {summary.report_json_consistency_checked}",
        f"- dashboard_source_consistency_checked: {summary.dashboard_source_consistency_checked}",
        f"- real_calibration_completed: {summary.real_calibration_completed}",
        f"- actual_tax_payable_determined: {summary.actual_tax_payable_determined}",
        f"- validation_claimed: {summary.validation_claimed}",
        f"- approval_claimed: {summary.approval_claimed}",
        f"- operational_readiness_claimed: {summary.operational_readiness_claimed}",
        f"- legal_sufficiency_claimed: {summary.legal_sufficiency_claimed}",
        f"- official_status_claimed: {summary.official_status_claimed}",
        f"- firm_level_liability_logic_modified: {summary.firm_level_liability_logic_modified}",
    ]


def _finding_table(items: list[Any]) -> list[str]:
    lines = [
        "| Finding ID | Audit Type | Status | Scope | Checked | Passed | Failed | Reviewer Next Step | Must Not Infer |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.finding_id} | {item.audit_type} | {item.audit_status} | {item.reconciliation_scope} | "
            f"{item.what_was_checked} | {item.what_passed} | {item.what_failed} | "
            f"{item.what_reviewer_should_inspect_next} | must_not_infer: {_join_boundary_tokens(item.what_must_not_be_inferred)} |"
        )
    return lines


def _single_audit_table(item: Any) -> list[str]:
    return _finding_table([item.finding])


def _build_json_payload(result: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": PUBLIC_DATA_CONSISTENCY_AUDIT_NON_CLAIMS,
            "audit_status_values": sorted(AUDIT_STATUS_VALUES),
            "audit_type_values": sorted(AUDIT_TYPE_VALUES),
            "reconciliation_scope_values": sorted(RECONCILIATION_SCOPE_VALUES),
        },
        "summary": _jsonable(result.summary),
        "public_data_consistency_audit": _jsonable(result),
    }


def _build_markdown(result: Any, metadata: dict[str, Any]) -> str:
    lines: list[str] = [
        "# CARSF V1.5 Public Data Pilot Consistency Audit & Source Reconciliation",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report audits internal consistency across existing Build 27 and Build 28 public-data pilot artefacts without loading new data.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in PUBLIC_DATA_CONSISTENCY_AUDIT_NON_CLAIMS)
    lines.extend(["", "## C. Audit Method", ""])
    lines.extend(
        [
            "- Reconcile source references, loaded extracts, source-reference-only rows, placeholder anchors, field checks, module checks, digests, generated reports, and dashboard source.",
            "- Treat `reconciled` as internal consistency only, not external source verification.",
            "- Raise fail-closed if required boundaries or count agreements break.",
        ]
    )
    lines.extend(["", "## D. Audit Status Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in sorted(AUDIT_STATUS_VALUES))
    lines.extend(["", "## E. Source Reference To Extract Audit", ""])
    lines.extend(_single_audit_table(result.source_reference_reconciliation))
    lines.extend(["", "## F. Loaded Extract To Evidence Map Audit", ""])
    lines.extend(_single_audit_table(result.extract_evidence_reconciliation))
    lines.extend(["", "## G. Source-Reference-Only Count Audit", ""])
    lines.extend(_single_audit_table(result.source_reference_only_count_audit))
    lines.extend(["", "## H. Fair Work Wage Arithmetic Audit", ""])
    lines.extend(_single_audit_table(result.arithmetic_audit))
    lines.append(
        f"- Fair Work arithmetic: {result.arithmetic_audit.hourly_value:.2f} * 38 = "
        f"{result.arithmetic_audit.expected_weekly_value:.2f}; stored weekly value "
        f"{result.arithmetic_audit.actual_weekly_value:.2f}."
    )
    lines.extend(["", "## I. Placeholder Boundary Audit", ""])
    lines.extend(_single_audit_table(result.placeholder_boundary_audit))
    lines.extend(["", "## J. Module Calibration Boundary Audit", ""])
    lines.extend(_single_audit_table(result.module_calibration_boundary_audit))
    lines.extend(["", "## K. Restricted Blocker Preservation Audit", ""])
    lines.extend(_single_audit_table(result.restricted_blocker_audit))
    lines.extend(["", "## L. Forbidden Repo Data Preservation Audit", ""])
    lines.extend(_single_audit_table(result.forbidden_repo_data_audit))
    lines.extend(["", "## M. Digest Consistency Audit", ""])
    lines.extend(_single_audit_table(result.digest_consistency_audit))
    lines.extend(["", "## N. Report / JSON Consistency Audit", ""])
    lines.extend(_single_audit_table(result.report_json_consistency_audit))
    lines.extend(["", "## O. Dashboard Source Consistency Audit", ""])
    lines.extend(_single_audit_table(result.dashboard_source_consistency_audit))
    lines.extend(["", "## P. Non-Claim Boundary Audit", ""])
    lines.extend(_single_audit_table(result.non_claim_boundary_audit))
    lines.extend(["", "## Q. Forbidden Claim Scan", ""])
    lines.extend(_finding_table([result.forbidden_claim_scan]))
    lines.extend(["", "## R. Audit Findings", ""])
    lines.extend(_finding_table(result.findings))
    lines.extend(["", "## S. Reconciliation Summary", ""])
    lines.extend(_summary_lines(result.summary))
    lines.extend(["", "## T. What This Audit Does Not Mean", ""])
    lines.extend(
        [
            "- It does not mean external source verification has occurred.",
            "- It is not calibration, validation, legal advice, tax advice, ATO guidance, Treasury modelling, PBO costing, legal sufficiency, operational readiness, or official status.",
            "- It does not determine actual tax payable and does not modify firm-level CARSF liability.",
        ]
    )
    lines.extend(["", "## U. Build 30 Readiness", ""])
    lines.extend(f"- {item}" for item in result.build_30_requirements)
    lines.extend(["", "## V. Limitations and Future Work", ""])
    lines.append("Build 30 can package the feasibility map, public-data pilot, evidence map, and consistency audit into a reviewer handoff bundle without adding data or claiming calibration.")
    text = "\n".join(lines) + "\n"
    findings = find_forbidden_affirmative_public_data_claims(text)
    if findings:
        raise ValueError(f"generated public data consistency audit Markdown contains forbidden affirmative claims: {', '.join(findings)}")
    return text


def run_public_data_consistency_audit(
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
    public_pilot_report_path: Path = DEFAULT_PUBLIC_PILOT_REPORT_PATH,
    public_pilot_markdown_path: Path = DEFAULT_PUBLIC_PILOT_MARKDOWN_PATH,
    evidence_map_report_path: Path = DEFAULT_EVIDENCE_MAP_REPORT_PATH,
    evidence_map_markdown_path: Path = DEFAULT_EVIDENCE_MAP_MARKDOWN_PATH,
    digest_path: Path = DEFAULT_DIGEST_PATH,
    dashboard_path: Path = DEFAULT_DASHBOARD_PATH,
) -> Any:
    manifest = _load_yaml(manifest_path)
    public_pilot_report = _load_json(public_pilot_report_path)
    evidence_map_report = _load_json(evidence_map_report_path)
    digest_payload = _load_json(digest_path)
    return build_public_data_consistency_audit_result(
        manifest=manifest,
        public_pilot_report=public_pilot_report,
        public_data_evidence_map_report=evidence_map_report,
        public_pilot_markdown=public_pilot_markdown_path.read_text(encoding="utf-8"),
        public_data_evidence_map_markdown=evidence_map_markdown_path.read_text(encoding="utf-8"),
        digest_payload=digest_payload,
        dashboard_path=dashboard_path,
        dashboard_text=dashboard_path.read_text(encoding="utf-8"),
        repo_root=REPO_ROOT,
    )


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--public-pilot-report", type=Path, default=DEFAULT_PUBLIC_PILOT_REPORT_PATH)
    parser.add_argument("--public-pilot-markdown", type=Path, default=DEFAULT_PUBLIC_PILOT_MARKDOWN_PATH)
    parser.add_argument("--evidence-map-report", type=Path, default=DEFAULT_EVIDENCE_MAP_REPORT_PATH)
    parser.add_argument("--evidence-map-markdown", type=Path, default=DEFAULT_EVIDENCE_MAP_MARKDOWN_PATH)
    parser.add_argument("--digest-path", type=Path, default=DEFAULT_DIGEST_PATH)
    parser.add_argument("--dashboard-path", type=Path, default=DEFAULT_DASHBOARD_PATH)
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS_DIR)
    args = parser.parse_args(argv)

    args.reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    result = run_public_data_consistency_audit(
        manifest_path=args.manifest,
        public_pilot_report_path=args.public_pilot_report,
        public_pilot_markdown_path=args.public_pilot_markdown,
        evidence_map_report_path=args.evidence_map_report,
        evidence_map_markdown_path=args.evidence_map_markdown,
        digest_path=args.digest_path,
        dashboard_path=args.dashboard_path,
    )
    json_payload = _build_json_payload(result, metadata)
    json_text = json.dumps(json_payload, indent=2, sort_keys=True) + "\n"
    findings = find_forbidden_affirmative_public_data_claims(json_text)
    if findings:
        raise ValueError(f"generated public data consistency audit JSON contains forbidden affirmative claims: {', '.join(findings)}")
    json_path = args.reports_dir / "public_data_consistency_audit.json"
    md_path = args.reports_dir / "public_data_consistency_audit.md"
    json_path.write_text(json_text, encoding="utf-8")
    md_path.write_text(_build_markdown(result, metadata), encoding="utf-8")

    print(f"audit findings: {result.summary.total_audit_findings}")
    print(f"findings reconciled: {result.summary.findings_reconciled}")
    print(f"findings warning: {result.summary.findings_warning}")
    print(f"findings fail closed: {result.summary.findings_fail_closed}")
    print(f"forbidden claim findings: {result.summary.forbidden_claim_findings}")
    print(f"non-claim boundary failures: {result.summary.non_claim_boundary_failures}")
    print(f"new_data_loaded: {result.summary.new_data_loaded}")
    print(f"external_source_verification_claimed: {result.summary.external_source_verification_claimed}")
    print(f"real_calibration_completed: {result.summary.real_calibration_completed}")
    print(f"validation_claimed: {result.summary.validation_claimed}")
    print(f"firm_level_liability_logic_modified: {result.summary.firm_level_liability_logic_modified}")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
