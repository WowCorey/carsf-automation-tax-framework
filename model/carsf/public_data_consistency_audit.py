"""Internal consistency audit for the CARSF V1.5 public-data pilot.

This layer reconciles existing Build 27 and Build 28 artefacts only. It does
not load new data, externally verify source values, complete calibration,
validate CARSF, determine tax payable, or modify firm-level CARSF liability.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .public_data_pilot import find_forbidden_affirmative_public_data_claims


AUDIT_STATUS_VALUES = {
    "reconciled",
    "warning",
    "blocked",
    "not_applicable",
    "fail_closed",
}

AUDIT_TYPE_VALUES = {
    "source_reference_to_extract",
    "extract_to_evidence_map",
    "source_reference_only_counting",
    "arithmetic_consistency",
    "placeholder_boundary",
    "module_calibration_boundary",
    "restricted_blocker_preservation",
    "forbidden_repo_data_preservation",
    "digest_consistency",
    "report_json_consistency",
    "dashboard_source_consistency",
    "non_claim_boundary",
    "forbidden_claim_scan",
}

RECONCILIATION_SCOPE_VALUES = {
    "internal_repo_only",
    "source_locator_metadata_only",
    "arithmetic_only",
    "count_consistency_only",
    "boundary_consistency_only",
    "external_review_required",
}

PUBLIC_DATA_CONSISTENCY_AUDIT_WARNING = (
    "This is an internal consistency audit and source-reconciliation map only. No new data is loaded by this build. "
    "This does not externally verify source values, does not scrape public sources, and does not call external APIs. "
    "This is not calibration; calibration has not been completed. Public data does not prove the model works. "
    "Reconciled means internally consistent only; reconciled does not mean validated, official, or ready. "
    "Realistic placeholders remain placeholders, realistic placeholders are not real data, realistic placeholders are not calibrated, "
    "source references are not loaded datasets, and restricted-data requirements are not data access. This is not legal advice, "
    "not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, "
    "not statistical validation, not operational readiness, not legal sufficiency, and not official status. It does not determine "
    "actual tax payable, does not use taxpayer-level data, firm-level confidential data, household microdata, ABS DataLab, "
    "HILDA microdata, DSS/Services Australia records, ATO taxpayer records, Treasury/PBO confidential material, or restricted "
    "government data, and does not modify firm-level CARSF liability. It only checks internal consistency across source records, "
    "extracts, reports, digests, dashboard source, and non-claim boundaries."
)

PUBLIC_DATA_CONSISTENCY_AUDIT_NON_CLAIMS = [
    PUBLIC_DATA_CONSISTENCY_AUDIT_WARNING,
    "Audit statuses are internal consistency statuses only; they are not validation, approval, calibration, readiness, or official status.",
    "Source locators and value notes are metadata for reviewer inspection only and do not mean external source verification has occurred.",
    "Digest checks are repository integrity metadata only and are not signatures, external attestation, approval, validation, or calibration.",
]

REQUIRED_FALSE_FLAGS = [
    "real_calibration_completed",
    "actual_tax_payable_determined",
    "validation_claimed",
    "approval_claimed",
    "operational_readiness_claimed",
    "legal_sufficiency_claimed",
    "official_status_claimed",
    "firm_level_liability_logic_modified",
]

REQUIRED_NON_CLAIM_PHRASES = [
    "not calibration",
    "calibration has not been completed",
    "public data does not prove the model works",
    "realistic placeholders remain placeholders",
    "source references are not loaded datasets",
    "restricted-data requirements are not data access",
    "not legal advice",
    "not tax advice",
    "not ATO guidance",
    "not Treasury modelling",
    "not PBO costing",
    "not economic validation",
    "not welfare validation",
    "not statistical validation",
    "not operational readiness",
    "not legal sufficiency",
    "not official status",
    "does not determine actual tax payable",
    "does not modify firm-level CARSF liability",
]

PROHIBITED_REVIEW_STATUS_CLAIMS = [
    "externally_validated",
    "validated_by",
    "approved",
    "official_status",
    "official guidance",
    "ato_guidance",
    "treasury_modelling",
    "pbo_costing",
]


@dataclass(frozen=True)
class ConsistencyAuditFinding:
    finding_id: str
    audit_type: str
    audit_status: str
    reconciliation_scope: str
    what_was_checked: str
    what_passed: str
    what_failed: str
    what_reviewer_should_inspect_next: str
    what_must_not_be_inferred: list[str]
    related_ids: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SourceReferenceReconciliation:
    finding: ConsistencyAuditFinding
    checked_extract_ids: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExtractEvidenceReconciliation:
    finding: ConsistencyAuditFinding
    checked_extract_ids: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SourceReferenceOnlyCountAudit:
    finding: ConsistencyAuditFinding
    expected_counts: dict[str, int]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ArithmeticAudit:
    finding: ConsistencyAuditFinding
    hourly_value: float
    expected_weekly_value: float
    actual_weekly_value: float

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PlaceholderBoundaryAudit:
    finding: ConsistencyAuditFinding
    checked_anchor_ids: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ModuleCalibrationBoundaryAudit:
    finding: ConsistencyAuditFinding
    checked_module_ids: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RestrictedBlockerAudit:
    finding: ConsistencyAuditFinding
    checked_blocker_ids: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ForbiddenRepoDataAudit:
    finding: ConsistencyAuditFinding
    checked_rule_ids: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DigestConsistencyAudit:
    finding: ConsistencyAuditFinding
    digest_paths: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReportJsonConsistencyAudit:
    finding: ConsistencyAuditFinding
    checked_reports: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DashboardSourceConsistencyAudit:
    finding: ConsistencyAuditFinding
    checked_dashboard_path: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class NonClaimBoundaryAudit:
    finding: ConsistencyAuditFinding
    checked_phrases: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicDataConsistencyAuditSummary:
    total_audit_findings: int
    findings_reconciled: int
    findings_warning: int
    findings_blocked: int
    findings_not_applicable: int
    findings_fail_closed: int
    source_references_total: int
    loaded_public_extracts_total: int
    source_reference_only_extracts_total: int
    placeholder_anchors_total: int
    field_sanity_checks_total: int
    module_sanity_checks_total: int
    restricted_blockers_total: int
    forbidden_repo_data_items_total: int
    digest_targets_total: int
    digest_self_hash_findings: int
    forbidden_claim_findings: int
    non_claim_boundary_failures: int
    consistency_audit_created: bool
    new_data_loaded: bool
    external_source_verification_claimed: bool
    source_references_reconciled: bool
    extract_evidence_reconciled: bool
    source_reference_only_counts_reconciled: bool
    arithmetic_checks_reconciled: bool
    placeholder_boundaries_preserved: bool
    module_calibration_boundaries_preserved: bool
    restricted_blockers_preserved: bool
    forbidden_repo_data_preserved: bool
    digest_consistency_checked: bool
    report_json_consistency_checked: bool
    dashboard_source_consistency_checked: bool
    real_calibration_completed: bool
    actual_tax_payable_determined: bool
    validation_claimed: bool
    approval_claimed: bool
    operational_readiness_claimed: bool
    legal_sufficiency_claimed: bool
    official_status_claimed: bool
    firm_level_liability_logic_modified: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicDataConsistencyAuditResult:
    audit_id: str
    audit_name: str
    status: str
    non_claims: list[str]
    input_artifacts: list[str]
    source_reference_reconciliation: SourceReferenceReconciliation
    extract_evidence_reconciliation: ExtractEvidenceReconciliation
    source_reference_only_count_audit: SourceReferenceOnlyCountAudit
    arithmetic_audit: ArithmeticAudit
    placeholder_boundary_audit: PlaceholderBoundaryAudit
    module_calibration_boundary_audit: ModuleCalibrationBoundaryAudit
    restricted_blocker_audit: RestrictedBlockerAudit
    forbidden_repo_data_audit: ForbiddenRepoDataAudit
    digest_consistency_audit: DigestConsistencyAudit
    report_json_consistency_audit: ReportJsonConsistencyAudit
    dashboard_source_consistency_audit: DashboardSourceConsistencyAudit
    non_claim_boundary_audit: NonClaimBoundaryAudit
    forbidden_claim_scan: ConsistencyAuditFinding
    findings: list[ConsistencyAuditFinding]
    build_30_requirements: list[str]
    summary: PublicDataConsistencyAuditSummary

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _required_mapping(source: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [field for field in fields if field not in source]
    if missing:
        raise ValueError(f"{label} missing required fields: {', '.join(missing)}")


def _list_of_strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{label} must be a list of strings")
    return list(value)


def _finding(
    finding_id: str,
    audit_type: str,
    audit_status: str,
    reconciliation_scope: str,
    what_was_checked: str,
    what_passed: str,
    what_failed: str,
    what_reviewer_should_inspect_next: str,
    related_ids: list[str] | None = None,
) -> ConsistencyAuditFinding:
    if audit_type not in AUDIT_TYPE_VALUES:
        raise ValueError(f"invalid audit type: {audit_type}")
    if audit_status not in AUDIT_STATUS_VALUES:
        raise ValueError(f"invalid audit status: {audit_status}")
    if reconciliation_scope not in RECONCILIATION_SCOPE_VALUES:
        raise ValueError(f"invalid reconciliation scope: {reconciliation_scope}")
    return ConsistencyAuditFinding(
        finding_id=finding_id,
        audit_type=audit_type,
        audit_status=audit_status,
        reconciliation_scope=reconciliation_scope,
        what_was_checked=what_was_checked,
        what_passed=what_passed,
        what_failed=what_failed,
        what_reviewer_should_inspect_next=what_reviewer_should_inspect_next,
        what_must_not_be_inferred=[
            "external source verification",
            "calibration",
            "validation",
            "actual tax payable",
            "legal sufficiency",
            "operational readiness",
            "official status",
        ],
        related_ids=related_ids or [],
    )


def _status_from_failures(failures: list[str], warning_only: bool = False) -> str:
    if failures and warning_only:
        return "warning"
    if failures:
        return "fail_closed"
    return "reconciled"


def _raise_if_fail_closed(findings: list[ConsistencyAuditFinding]) -> None:
    failed = [finding for finding in findings if finding.audit_status == "fail_closed"]
    if failed:
        details = "; ".join(f"{finding.finding_id}: {finding.what_failed}" for finding in failed)
        raise ValueError(f"public data consistency audit failed closed: {details}")


def _validate_manifest(manifest: dict[str, Any]) -> None:
    _required_mapping(
        manifest,
        [
            "audit_id",
            "audit_name",
            "status",
            "non_claims",
            "input_artifacts",
            "audit_status_taxonomy",
            "audit_type_taxonomy",
            "reconciliation_scope_taxonomy",
            "required_count_reconciliations",
            "required_source_reference_reconciliations",
            "required_extract_reconciliations",
            "required_placeholder_reconciliations",
            "required_module_boundary_checks",
            "required_digest_checks",
            "required_report_json_checks",
            "required_dashboard_checks",
            "required_non_claim_checks",
            "forbidden_claims",
            "build_30_requirements",
        ],
        "public data consistency audit manifest",
    )
    if manifest["status"] != "internal_consistency_audit_only":
        raise ValueError("consistency audit status must be internal_consistency_audit_only")
    for non_claim in PUBLIC_DATA_CONSISTENCY_AUDIT_NON_CLAIMS:
        if non_claim not in manifest["non_claims"]:
            raise ValueError("consistency audit manifest missing required non-claim language")
    if set(manifest["audit_status_taxonomy"]) != AUDIT_STATUS_VALUES:
        raise ValueError("audit status taxonomy does not match required values")
    if set(manifest["audit_type_taxonomy"]) != AUDIT_TYPE_VALUES:
        raise ValueError("audit type taxonomy does not match required values")
    if set(manifest["reconciliation_scope_taxonomy"]) != RECONCILIATION_SCOPE_VALUES:
        raise ValueError("reconciliation scope taxonomy does not match required values")
    for field in [
        "required_count_reconciliations",
        "required_source_reference_reconciliations",
        "required_extract_reconciliations",
        "required_placeholder_reconciliations",
        "required_module_boundary_checks",
        "required_digest_checks",
        "required_report_json_checks",
        "required_dashboard_checks",
        "required_non_claim_checks",
        "forbidden_claims",
        "build_30_requirements",
    ]:
        _list_of_strings(manifest[field], field)


def _public_pilot_payload(report: dict[str, Any]) -> dict[str, Any]:
    payload = report.get("public_data_pilot")
    if not isinstance(payload, dict):
        raise ValueError("public_data_pilot report payload missing")
    return payload


def _evidence_map_payload(report: dict[str, Any]) -> dict[str, Any]:
    payload = report.get("public_data_evidence_map")
    if not isinstance(payload, dict):
        raise ValueError("public_data_evidence_map report payload missing")
    return payload


def _source_reference_reconciliation(pilot: dict[str, Any]) -> SourceReferenceReconciliation:
    sources = pilot.get("source_references", [])
    extracts = pilot.get("public_aggregate_extracts", [])
    source_ids = {item.get("source_reference_id") for item in sources}
    failures: list[str] = []
    checked_ids: list[str] = []
    for extract in extracts:
        extract_id = str(extract.get("extract_id", ""))
        checked_ids.append(extract_id)
        if extract.get("source_reference_id") not in source_ids:
            failures.append(f"{extract_id} references unknown source_reference_id")
        if extract.get("data_status") == "real_public_data_loaded":
            for field in ["source_url", "source_locator", "source_value_note", "value_review_status"]:
                if not str(extract.get(field, "")).strip():
                    failures.append(f"{extract_id} missing {field}")
            review_status = str(extract.get("value_review_status", "")).lower()
            for phrase in PROHIBITED_REVIEW_STATUS_CLAIMS:
                if phrase in review_status:
                    failures.append(f"{extract_id} value_review_status overclaims {phrase}")
        if extract.get("data_status") == "source_reference_only" and extract.get("values"):
            failures.append(f"{extract_id} is source-reference-only but has loaded values")
    finding = _finding(
        "source_reference_to_extract",
        "source_reference_to_extract",
        _status_from_failures(failures),
        "source_locator_metadata_only",
        "Every extract source reference and loaded-extract source metadata field.",
        "All extract source_reference_id values are present and loaded extracts carry source locator metadata."
        if not failures
        else "Some source-reference metadata checks did not reconcile.",
        "; ".join(failures) if failures else "None",
        "Inspect source locators and value review status text before relying on any row as a review input.",
        checked_ids,
    )
    return SourceReferenceReconciliation(finding=finding, checked_extract_ids=checked_ids)


def _extract_evidence_reconciliation(pilot: dict[str, Any], evidence: dict[str, Any]) -> ExtractEvidenceReconciliation:
    extracts = pilot.get("public_aggregate_extracts", [])
    loaded_ids = {item["extract_id"] for item in extracts if item.get("data_status") == "real_public_data_loaded"}
    source_only_ids = {item["extract_id"] for item in extracts if item.get("data_status") == "source_reference_only"}
    evidence_loaded = {item["extract_id"]: item for item in evidence.get("loaded_extract_evidence", [])}
    evidence_source_only = {item["extract_id"]: item for item in evidence.get("source_reference_only_evidence", [])}
    failures: list[str] = []
    for extract_id in sorted(loaded_ids):
        row = evidence_loaded.get(extract_id)
        if not row:
            failures.append(f"{extract_id} missing from loaded_extract_evidence")
            continue
        if row.get("evidence_status") != "loaded_public_aggregate":
            failures.append(f"{extract_id} evidence_status is not loaded_public_aggregate")
        expected = "arithmetic_checked" if extract_id == "fair_work_minimum_wage_2025_extract" else "source_locator_recorded"
        if row.get("confidence_label") != expected:
            failures.append(f"{extract_id} confidence_label expected {expected}, got {row.get('confidence_label')}")
        text = f"{row.get('confidence_label', '')} {row.get('source_value_note', '')} {row.get('value_review_status', '')}".lower()
        if "ato validated" in text or "treasury validated" in text or "pbo validated" in text:
            failures.append(f"{extract_id} evidence text claims validation")
        if "ato guidance" in text:
            failures.append(f"{extract_id} evidence text claims ATO guidance")
        if "treasury modelling" in text and "not treasury modelling" not in text:
            failures.append(f"{extract_id} evidence text claims Treasury modelling")
    for extract_id in sorted(source_only_ids):
        if extract_id in evidence_loaded:
            failures.append(f"{extract_id} source-reference-only row appears as loaded evidence")
        if extract_id not in evidence_source_only:
            failures.append(f"{extract_id} missing from source_reference_only_evidence")
    checked_ids = sorted(loaded_ids | source_only_ids)
    finding = _finding(
        "extract_to_evidence_map",
        "extract_to_evidence_map",
        _status_from_failures(failures),
        "internal_repo_only",
        "Loaded and source-reference-only extract rows against evidence-map rows.",
        "Loaded extracts map to loaded public aggregate evidence and source-reference-only rows remain separate."
        if not failures
        else "Some extract evidence rows did not reconcile.",
        "; ".join(failures) if failures else "None",
        "Inspect the evidence-map JSON before presenting loaded-public-extract counts.",
        checked_ids,
    )
    return ExtractEvidenceReconciliation(finding=finding, checked_extract_ids=checked_ids)


def _summary_value(report: dict[str, Any], key: str) -> int:
    value = report.get("summary", {}).get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"summary value is missing or not an integer: {key}")
    return value


def _count_audit(
    pilot: dict[str, Any],
    pilot_report: dict[str, Any],
    evidence_report: dict[str, Any],
) -> SourceReferenceOnlyCountAudit:
    source_counts = {
        "total_source_references": len(pilot.get("source_references", [])),
        "total_public_aggregate_extracts": len(pilot.get("public_aggregate_extracts", [])),
        "real_public_data_loaded_extracts": sum(
            item.get("data_status") == "real_public_data_loaded" for item in pilot.get("public_aggregate_extracts", [])
        ),
        "source_reference_only_extracts": sum(
            item.get("data_status") == "source_reference_only" for item in pilot.get("public_aggregate_extracts", [])
        ),
        "total_placeholder_anchors": len(pilot.get("placeholder_anchors", [])),
        "total_field_sanity_checks": len(pilot.get("field_sanity_checks", [])),
        "total_module_sanity_checks": len(pilot.get("module_sanity_checks", [])),
    }
    equivalent_evidence_counts = {
        "total_source_references": _summary_value(evidence_report, "total_source_evidence_items"),
        "real_public_data_loaded_extracts": _summary_value(evidence_report, "total_loaded_public_extract_evidence_items"),
        "source_reference_only_extracts": _summary_value(evidence_report, "total_source_reference_only_evidence_items"),
        "total_placeholder_anchors": _summary_value(evidence_report, "total_placeholder_evidence_items"),
        "total_field_sanity_checks": _summary_value(evidence_report, "total_field_sanity_evidence_items"),
        "total_module_sanity_checks": _summary_value(evidence_report, "total_module_sanity_evidence_items"),
    }
    failures: list[str] = []
    for key, source_value in source_counts.items():
        if _summary_value(pilot_report, key) != source_value:
            failures.append(f"pilot summary {key} does not match source count {source_value}")
        if key in equivalent_evidence_counts and equivalent_evidence_counts[key] != source_value:
            failures.append(f"evidence summary {key} does not match source count {source_value}")
    expected_current = {
        "total_source_references": 8,
        "total_public_aggregate_extracts": 8,
        "real_public_data_loaded_extracts": 5,
        "source_reference_only_extracts": 3,
        "total_placeholder_anchors": 11,
        "total_field_sanity_checks": 10,
        "total_module_sanity_checks": 11,
    }
    warnings = [f"{key} current count is {source_counts[key]}, expected Build 29 baseline {value}" for key, value in expected_current.items() if source_counts.get(key) != value]
    status = _status_from_failures(failures) if failures else _status_from_failures(warnings, warning_only=True)
    finding = _finding(
        "source_reference_only_counting",
        "source_reference_only_counting",
        status,
        "count_consistency_only",
        "Source counts against pilot JSON and evidence-map JSON summary counts.",
        "Source-reference-only rows are excluded from loaded public data counts and JSON counts agree."
        if not failures
        else "Some JSON count summaries disagree with source artefacts.",
        "; ".join(failures or warnings) if (failures or warnings) else "None",
        "Inspect generated summaries whenever source files or report JSONs change.",
        sorted(source_counts),
    )
    return SourceReferenceOnlyCountAudit(finding=finding, expected_counts=source_counts)


def _extract_numeric(values: list[dict[str, Any]], value_id: str) -> float | None:
    for item in values:
        if item.get("value_id") == value_id:
            value = item.get("value")
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise ValueError(f"{value_id} must be numeric")
            return float(value)
    return None


def _arithmetic_audit(pilot: dict[str, Any]) -> ArithmeticAudit:
    fair_work = next(
        (item for item in pilot.get("public_aggregate_extracts", []) if item.get("extract_id") == "fair_work_minimum_wage_2025_extract"),
        None,
    )
    if not fair_work:
        raise ValueError("fair_work_minimum_wage_2025_extract missing")
    hourly = _extract_numeric(fair_work.get("values", []), "national_minimum_wage_hourly")
    weekly = _extract_numeric(fair_work.get("values", []), "national_minimum_wage_weekly")
    failures: list[str] = []
    if hourly is None:
        failures.append("national_minimum_wage_hourly missing")
        hourly = 0.0
    if weekly is None:
        failures.append("national_minimum_wage_weekly missing")
        weekly = 0.0
    expected_weekly = round(hourly * 38, 2)
    if abs(weekly - expected_weekly) > 0.001:
        failures.append(f"expected {expected_weekly:.2f} from hourly * 38, got {weekly:.2f}")
    finding = _finding(
        "fair_work_wage_arithmetic",
        "arithmetic_consistency",
        _status_from_failures(failures),
        "arithmetic_only",
        "Fair Work hourly and weekly national minimum wage values in the loaded public extract.",
        f"{hourly:.2f} * 38 = {expected_weekly:.2f}, matching the weekly value."
        if not failures
        else "Fair Work wage arithmetic did not reconcile.",
        "; ".join(failures) if failures else "None",
        "Inspect the source locator and arithmetic if either wage value changes.",
        ["fair_work_minimum_wage_2025_extract"],
    )
    return ArithmeticAudit(
        finding=finding,
        hourly_value=hourly,
        expected_weekly_value=expected_weekly,
        actual_weekly_value=weekly,
    )


def _placeholder_audit(pilot: dict[str, Any], evidence: dict[str, Any]) -> PlaceholderBoundaryAudit:
    anchors = pilot.get("placeholder_anchors", [])
    evidence_by_anchor = {item.get("anchor_id"): item for item in evidence.get("placeholder_evidence", [])}
    failures: list[str] = []
    checked: list[str] = []
    for anchor in anchors:
        anchor_id = str(anchor.get("anchor_id", ""))
        checked.append(anchor_id)
        if anchor.get("current_placeholder_status") != "realistic_placeholder":
            failures.append(f"{anchor_id} status is not realistic_placeholder")
        for field in [
            "must_be_labelled_realistic_placeholder",
            "must_not_be_labelled_real_data",
            "must_not_be_labelled_calibrated",
        ]:
            if anchor.get(field) is not True:
                failures.append(f"{anchor_id} {field} is not true")
        row = evidence_by_anchor.get(anchor_id)
        if row and row.get("evidence_status") == "loaded_public_aggregate":
            failures.append(f"{anchor_id} evidence row is incorrectly loaded_public_aggregate")
    finding = _finding(
        "placeholder_boundary",
        "placeholder_boundary",
        _status_from_failures(failures),
        "boundary_consistency_only",
        "Placeholder source rows and evidence rows for real-data or calibration overread.",
        "All placeholder anchors remain realistic placeholders and are not labelled loaded public data."
        if not failures
        else "Some placeholder boundary checks did not reconcile.",
        "; ".join(failures) if failures else "None",
        "Inspect placeholder evidence rows before using any anchor in a later calibration design.",
        checked,
    )
    return PlaceholderBoundaryAudit(finding=finding, checked_anchor_ids=checked)


def _module_boundary_audit(pilot: dict[str, Any], evidence: dict[str, Any]) -> ModuleCalibrationBoundaryAudit:
    modules = pilot.get("module_sanity_checks", [])
    evidence_modules = evidence.get("module_sanity_evidence", [])
    failures: list[str] = []
    checked: list[str] = []
    for module in modules:
        module_id = str(module.get("module_id", ""))
        checked.append(module_id)
        if module.get("calibration_possible") is not False:
            failures.append(f"{module_id} source module has calibration_possible true")
    for row in evidence_modules:
        module_id = str(row.get("module_id", ""))
        if row.get("calibration_possible") is not False:
            failures.append(f"{module_id} evidence row has calibration_possible true")
        if not row.get("main_blockers"):
            failures.append(f"{module_id} evidence row hides main blockers")
    finding = _finding(
        "module_calibration_boundary",
        "module_calibration_boundary",
        _status_from_failures(failures),
        "boundary_consistency_only",
        "Module sanity-check rows and evidence rows for calibration_possible false and blocker visibility.",
        "Every module sanity-check row keeps calibration_possible false and preserves blockers."
        if not failures
        else "Some module boundary checks did not reconcile.",
        "; ".join(failures) if failures else "None",
        "Inspect module rows before using public-pilot evidence as calibration input.",
        checked,
    )
    return ModuleCalibrationBoundaryAudit(finding=finding, checked_module_ids=checked)


def _restricted_blocker_audit(pilot: dict[str, Any], evidence: dict[str, Any]) -> RestrictedBlockerAudit:
    blockers = pilot.get("restricted_data_blockers", [])
    evidence_blockers = {item.get("blocker_id"): item for item in evidence.get("restricted_blocker_evidence", [])}
    required = {"restricted_tax_records", "restricted_household_microdata", "restricted_welfare_records"}
    blocker_ids = {item.get("blocker_id") for item in blockers}
    failures = [f"missing blocker {blocker}" for blocker in sorted(required - blocker_ids)]
    for blocker_id in sorted(blocker_ids):
        row = evidence_blockers.get(blocker_id)
        if not row:
            failures.append(f"{blocker_id} missing from evidence blocker rows")
        elif row.get("evidence_status") != "blocked_by_restricted_data":
            failures.append(f"{blocker_id} is not blocked_by_restricted_data")
    finding = _finding(
        "restricted_blocker_preservation",
        "restricted_blocker_preservation",
        _status_from_failures(failures),
        "boundary_consistency_only",
        "Restricted-data blocker IDs and evidence-map blocker rows.",
        "Restricted tax, household microdata, and welfare/payment blockers remain visible and blocked."
        if not failures
        else "Some restricted blocker checks did not reconcile.",
        "; ".join(failures) if failures else "None",
        "Inspect blocker rows before planning any future data access process.",
        sorted(blocker_ids),
    )
    return RestrictedBlockerAudit(finding=finding, checked_blocker_ids=sorted(blocker_ids))


def _forbidden_repo_data_audit(pilot: dict[str, Any], evidence: dict[str, Any]) -> ForbiddenRepoDataAudit:
    rules = pilot.get("forbidden_data_rules", [])
    evidence_rules = {item.get("blocker_id"): item for item in evidence.get("forbidden_repo_data_evidence", [])}
    required_terms = [
        "confidential tax records",
        "firm confidential records",
        "person-level records",
        "household microdata",
        "restricted government data",
    ]
    rule_types = {str(item.get("forbidden_data_type", "")).lower() for item in rules}
    failures: list[str] = []
    for term in required_terms:
        if term not in rule_types:
            failures.append(f"missing forbidden category {term}")
    checked: list[str] = []
    for rule in rules:
        rule_id = str(rule.get("rule_id", ""))
        checked.append(rule_id)
        if rule.get("must_not_commit_to_repo") is not True:
            failures.append(f"{rule_id} weakens commit ban")
        row = evidence_rules.get(rule_id)
        if not row:
            failures.append(f"{rule_id} missing from forbidden evidence rows")
        elif row.get("evidence_status") != "forbidden_for_repo_use":
            failures.append(f"{rule_id} is not forbidden_for_repo_use")
    finding = _finding(
        "forbidden_repo_data_preservation",
        "forbidden_repo_data_preservation",
        _status_from_failures(failures),
        "boundary_consistency_only",
        "Forbidden repo data rules and evidence-map forbidden rows.",
        "Forbidden categories remain excluded and marked forbidden for repo use."
        if not failures
        else "Some forbidden-data checks did not reconcile.",
        "; ".join(failures) if failures else "None",
        "Inspect forbidden data rules before adding any public-pilot file type.",
        checked,
    )
    return ForbiddenRepoDataAudit(finding=finding, checked_rule_ids=checked)


def _digest_audit(digest_payload: dict[str, Any], repo_root: Path) -> DigestConsistencyAudit:
    entries = digest_payload.get("digests", [])
    if not isinstance(entries, list):
        raise ValueError("digest payload missing digests list")
    failures: list[str] = []
    paths: list[str] = []
    digest_file = "data/public_pilot/digests/public_data_pilot_digests.json"
    for entry in entries:
        path = str(entry.get("path", ""))
        paths.append(path)
        if path == digest_file:
            failures.append("digest manifest hashes itself")
        if not entry.get("sha256"):
            failures.append(f"{path} missing sha256")
        if path and not (repo_root / path).exists():
            failures.append(f"{path} digest target missing")
    if digest_payload.get("metadata", {}).get("digest_file_hashes_itself") is not False:
        failures.append("digest metadata does not explicitly exclude self-hash")
    finding = _finding(
        "digest_consistency",
        "digest_consistency",
        _status_from_failures(failures),
        "internal_repo_only",
        "Public-pilot digest entries, target paths, sha256 fields, and self-hash exclusion.",
        "Digest entries include sha256, target files exist, and the digest file does not hash itself."
        if not failures
        else "Some digest consistency checks did not reconcile.",
        "; ".join(failures) if failures else "None",
        "Inspect digest entries after regenerating public-pilot reports.",
        paths,
    )
    return DigestConsistencyAudit(finding=finding, digest_paths=paths)


def _report_json_audit(
    pilot_report: dict[str, Any],
    evidence_report: dict[str, Any],
    pilot_markdown: str,
    evidence_markdown: str,
) -> ReportJsonConsistencyAudit:
    failures: list[str] = []
    for report_name, report in [("public_data_pilot", pilot_report), ("public_data_evidence_map", evidence_report)]:
        for flag in REQUIRED_FALSE_FLAGS:
            if report.get("summary", {}).get(flag) is not False:
                failures.append(f"{report_name} summary flag {flag} is not false")
    for report_name, markdown in [("public_data_pilot.md", pilot_markdown), ("public_data_evidence_map.md", evidence_markdown)]:
        lowered = markdown.lower()
        missing = [phrase for phrase in REQUIRED_NON_CLAIM_PHRASES if phrase.lower() not in lowered]
        if missing:
            failures.append(f"{report_name} missing non-claim phrases: {', '.join(missing)}")
    finding = _finding(
        "report_json_consistency",
        "report_json_consistency",
        _status_from_failures(failures),
        "internal_repo_only",
        "Public-pilot and evidence-map JSON flags plus Markdown non-claim language.",
        "JSON false flags remain false and Markdown reports retain non-claim warnings."
        if not failures
        else "Some report/JSON consistency checks did not reconcile.",
        "; ".join(failures) if failures else "None",
        "Inspect generated report JSON and Markdown together after any runner change.",
        ["reports/public_data_pilot.json", "reports/public_data_evidence_map.json"],
    )
    return ReportJsonConsistencyAudit(
        finding=finding,
        checked_reports=["reports/public_data_pilot.json", "reports/public_data_evidence_map.json"],
    )


def _dashboard_audit(dashboard_path: Path, dashboard_text: str) -> DashboardSourceConsistencyAudit:
    failures: list[str] = []
    if "reports\" / \"public_data_evidence_map.json" not in dashboard_text and "public_data_evidence_map.json" not in dashboard_text:
        failures.append("dashboard does not read reports/public_data_evidence_map.json")
    if "requests" in dashboard_text or "urllib" in dashboard_text:
        failures.append("dashboard appears to import external request tooling")
    score_patterns = [
        "readiness_score",
        "calibration_score",
        "validation_score",
        "st.metric(\"readiness",
        "st.metric(\"calibration",
        "st.metric(\"validation",
    ]
    lowered = dashboard_text.lower()
    for pattern in score_patterns:
        if pattern in lowered:
            failures.append(f"dashboard contains score pattern {pattern}")
    finding = _finding(
        "dashboard_source_consistency",
        "dashboard_source_consistency",
        _status_from_failures(failures),
        "internal_repo_only",
        "Streamlit evidence-map page source for report source, external-source reads, and score-like widgets.",
        "Dashboard reads generated evidence-map JSON, does not read external sources, and does not create score-style metrics."
        if not failures
        else "Some dashboard source checks did not reconcile.",
        "; ".join(failures) if failures else "None",
        "Inspect the Streamlit page whenever evidence-map or audit sections are changed.",
        [str(dashboard_path).replace("\\", "/")],
    )
    return DashboardSourceConsistencyAudit(
        finding=finding,
        checked_dashboard_path=str(dashboard_path).replace("\\", "/"),
    )


def _non_claim_audit(texts: dict[str, str]) -> NonClaimBoundaryAudit:
    failures: list[str] = []
    for label, text in texts.items():
        lowered = text.lower()
        missing = [phrase for phrase in REQUIRED_NON_CLAIM_PHRASES if phrase.lower() not in lowered]
        if missing:
            failures.append(f"{label} missing: {', '.join(missing)}")
    finding = _finding(
        "non_claim_boundary",
        "non_claim_boundary",
        _status_from_failures(failures),
        "boundary_consistency_only",
        "Required non-claim phrases across generated public-data reports and dashboard text.",
        "Required non-claim boundaries remain visible."
        if not failures
        else "Some non-claim boundary phrases are missing.",
        "; ".join(failures) if failures else "None",
        "Inspect non-claim language before reviewer handoff.",
        REQUIRED_NON_CLAIM_PHRASES,
    )
    return NonClaimBoundaryAudit(finding=finding, checked_phrases=REQUIRED_NON_CLAIM_PHRASES)


def _forbidden_claim_scan(texts: dict[str, str]) -> ConsistencyAuditFinding:
    findings: list[str] = []
    for label, text in texts.items():
        for finding in find_forbidden_affirmative_public_data_claims(text):
            findings.append(f"{label}: {finding}")
    return _finding(
        "forbidden_claim_scan",
        "forbidden_claim_scan",
        _status_from_failures(findings),
        "boundary_consistency_only",
        "Generated reports, manifest text, and dashboard source for forbidden affirmative public-data claims.",
        "No forbidden affirmative claims were found."
        if not findings
        else "Forbidden affirmative claim findings were found.",
        "; ".join(sorted(set(findings))) if findings else "None",
        "Inspect any finding manually for negative-warning context before changing the scanner.",
        sorted(set(findings)),
    )


def build_public_data_consistency_audit_result(
    manifest: dict[str, Any],
    public_pilot_report: dict[str, Any],
    public_data_evidence_map_report: dict[str, Any],
    public_pilot_markdown: str,
    public_data_evidence_map_markdown: str,
    digest_payload: dict[str, Any],
    dashboard_path: Path,
    dashboard_text: str,
    repo_root: Path,
) -> PublicDataConsistencyAuditResult:
    _validate_manifest(manifest)
    pilot = _public_pilot_payload(public_pilot_report)
    evidence = _evidence_map_payload(public_data_evidence_map_report)

    source_reconciliation = _source_reference_reconciliation(pilot)
    extract_reconciliation = _extract_evidence_reconciliation(pilot, evidence)
    count_audit = _count_audit(pilot, public_pilot_report, public_data_evidence_map_report)
    arithmetic_audit = _arithmetic_audit(pilot)
    placeholder_audit = _placeholder_audit(pilot, evidence)
    module_audit = _module_boundary_audit(pilot, evidence)
    restricted_audit = _restricted_blocker_audit(pilot, evidence)
    forbidden_audit = _forbidden_repo_data_audit(pilot, evidence)
    digest_audit = _digest_audit(digest_payload, repo_root)
    report_audit = _report_json_audit(
        public_pilot_report,
        public_data_evidence_map_report,
        public_pilot_markdown,
        public_data_evidence_map_markdown,
    )
    dashboard_audit = _dashboard_audit(dashboard_path, dashboard_text)
    non_claim_audit = _non_claim_audit(
        {
            "public_data_pilot.md": public_pilot_markdown,
            "public_data_evidence_map.md": public_data_evidence_map_markdown,
            "simulator/pages/29_Public_Data_Evidence_Map.py": dashboard_text,
            "consistency_audit_non_claims": "\n".join(PUBLIC_DATA_CONSISTENCY_AUDIT_NON_CLAIMS),
        }
    )
    forbidden_scan = _forbidden_claim_scan(
        {
            "public_data_pilot.md": public_pilot_markdown,
            "public_data_pilot.json": str(public_pilot_report),
            "public_data_evidence_map.md": public_data_evidence_map_markdown,
            "public_data_evidence_map.json": str(public_data_evidence_map_report),
            "simulator/pages/29_Public_Data_Evidence_Map.py": dashboard_text,
            "consistency_audit_manifest": str(manifest),
            "consistency_audit_non_claims": "\n".join(PUBLIC_DATA_CONSISTENCY_AUDIT_NON_CLAIMS),
        }
    )
    findings = [
        source_reconciliation.finding,
        extract_reconciliation.finding,
        count_audit.finding,
        arithmetic_audit.finding,
        placeholder_audit.finding,
        module_audit.finding,
        restricted_audit.finding,
        forbidden_audit.finding,
        digest_audit.finding,
        report_audit.finding,
        dashboard_audit.finding,
        non_claim_audit.finding,
        forbidden_scan,
    ]
    _raise_if_fail_closed(findings)

    status_counts = {status: sum(finding.audit_status == status for finding in findings) for status in AUDIT_STATUS_VALUES}
    pilot_summary = public_pilot_report["summary"]
    summary = PublicDataConsistencyAuditSummary(
        total_audit_findings=len(findings),
        findings_reconciled=status_counts["reconciled"],
        findings_warning=status_counts["warning"],
        findings_blocked=status_counts["blocked"],
        findings_not_applicable=status_counts["not_applicable"],
        findings_fail_closed=status_counts["fail_closed"],
        source_references_total=len(pilot.get("source_references", [])),
        loaded_public_extracts_total=count_audit.expected_counts["real_public_data_loaded_extracts"],
        source_reference_only_extracts_total=count_audit.expected_counts["source_reference_only_extracts"],
        placeholder_anchors_total=count_audit.expected_counts["total_placeholder_anchors"],
        field_sanity_checks_total=count_audit.expected_counts["total_field_sanity_checks"],
        module_sanity_checks_total=count_audit.expected_counts["total_module_sanity_checks"],
        restricted_blockers_total=len(pilot.get("restricted_data_blockers", [])),
        forbidden_repo_data_items_total=len(pilot.get("forbidden_data_rules", [])),
        digest_targets_total=len(digest_audit.digest_paths),
        digest_self_hash_findings=1 if "digest manifest hashes itself" in digest_audit.finding.what_failed else 0,
        forbidden_claim_findings=len(forbidden_scan.related_ids),
        non_claim_boundary_failures=0 if non_claim_audit.finding.audit_status == "reconciled" else 1,
        consistency_audit_created=True,
        new_data_loaded=False,
        external_source_verification_claimed=False,
        source_references_reconciled=source_reconciliation.finding.audit_status == "reconciled",
        extract_evidence_reconciled=extract_reconciliation.finding.audit_status == "reconciled",
        source_reference_only_counts_reconciled=count_audit.finding.audit_status in {"reconciled", "warning"},
        arithmetic_checks_reconciled=arithmetic_audit.finding.audit_status == "reconciled",
        placeholder_boundaries_preserved=placeholder_audit.finding.audit_status == "reconciled",
        module_calibration_boundaries_preserved=module_audit.finding.audit_status == "reconciled",
        restricted_blockers_preserved=restricted_audit.finding.audit_status == "reconciled",
        forbidden_repo_data_preserved=forbidden_audit.finding.audit_status == "reconciled",
        digest_consistency_checked=digest_audit.finding.audit_status == "reconciled",
        report_json_consistency_checked=report_audit.finding.audit_status == "reconciled",
        dashboard_source_consistency_checked=dashboard_audit.finding.audit_status == "reconciled",
        real_calibration_completed=bool(pilot_summary.get("real_calibration_completed")),
        actual_tax_payable_determined=bool(pilot_summary.get("actual_tax_payable_determined")),
        validation_claimed=bool(pilot_summary.get("validation_claimed")),
        approval_claimed=bool(pilot_summary.get("approval_claimed")),
        operational_readiness_claimed=bool(pilot_summary.get("operational_readiness_claimed")),
        legal_sufficiency_claimed=bool(pilot_summary.get("legal_sufficiency_claimed")),
        official_status_claimed=bool(pilot_summary.get("official_status_claimed")),
        firm_level_liability_logic_modified=bool(pilot_summary.get("firm_level_liability_logic_modified")),
    )
    false_flag_failures = [
        flag
        for flag in REQUIRED_FALSE_FLAGS
        if getattr(summary, flag) is not False
    ]
    if false_flag_failures:
        raise ValueError(f"public data consistency audit false flags are not false: {', '.join(false_flag_failures)}")

    result = PublicDataConsistencyAuditResult(
        audit_id=str(manifest["audit_id"]),
        audit_name=str(manifest["audit_name"]),
        status=str(manifest["status"]),
        non_claims=list(manifest["non_claims"]),
        input_artifacts=list(manifest["input_artifacts"]),
        source_reference_reconciliation=source_reconciliation,
        extract_evidence_reconciliation=extract_reconciliation,
        source_reference_only_count_audit=count_audit,
        arithmetic_audit=arithmetic_audit,
        placeholder_boundary_audit=placeholder_audit,
        module_calibration_boundary_audit=module_audit,
        restricted_blocker_audit=restricted_audit,
        forbidden_repo_data_audit=forbidden_audit,
        digest_consistency_audit=digest_audit,
        report_json_consistency_audit=report_audit,
        dashboard_source_consistency_audit=dashboard_audit,
        non_claim_boundary_audit=non_claim_audit,
        forbidden_claim_scan=forbidden_scan,
        findings=findings,
        build_30_requirements=list(manifest["build_30_requirements"]),
        summary=summary,
    )
    final_findings = find_forbidden_affirmative_public_data_claims(str(result.to_jsonable()))
    if final_findings:
        raise ValueError(f"public data consistency audit contains forbidden affirmative claims: {', '.join(final_findings)}")
    return result
