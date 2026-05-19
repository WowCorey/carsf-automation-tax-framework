"""Executive dashboard and report index mechanics for CARSF V1.5.

This module consolidates existing prototype layers and generated reports. It
does not create a readiness score, operational-readiness claim, legal
sufficiency claim, economic-validation claim, or firm-level liability change.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


EXECUTIVE_DASHBOARD_WARNING = (
    "This is a prototype dashboard and report index only. It is not legal advice, tax advice, "
    "ATO guidance, Treasury modelling, economic validation, welfare advice, compliance scoring, "
    "enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, "
    "and not an official review pathway. It does not determine actual tax payable, does not use taxpayer-level, "
    "firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, and does not modify "
    "firm-level CARSF liability."
)
EXECUTIVE_DASHBOARD_NON_CLAIMS = [
    EXECUTIVE_DASHBOARD_WARNING,
    "The dashboard only consolidates existing prototype reports, warnings, navigation, and review blockers.",
    "Suggested review navigation is a reviewer convenience only and is not an official process.",
]

REQUIRED_LAYER_IDS = {
    "core_formula_model",
    "worked_examples",
    "sector_schedules",
    "sector_schedule_expansion",
    "sector_stress_matrix",
    "behavioural_response",
    "administrative_workflow",
    "legislative_architecture",
    "evidence_workflow",
    "secure_ingestion",
    "repo_guardrails",
    "investment_incidence",
    "fiscal_trajectory",
    "transition_funding",
    "payment_interactions",
    "household_distributional",
    "household_weighting",
    "uncertainty_ranges",
    "reviewed_scenarios",
    "calibration_shell",
    "real_data_feasibility",
    "working_paper",
    "status_risks_docs",
}

REQUIRED_REPORT_PATHS = {
    "reports/example_results.md",
    "reports/example_results.json",
    "reports/evidence_requirements.md",
    "reports/evidence_requirements.json",
    "reports/mock_evidence_workflow.md",
    "reports/mock_evidence_workflow.json",
    "reports/secure_ingestion_controls.md",
    "reports/secure_ingestion_controls.json",
    "reports/repo_guardrails.md",
    "reports/repo_guardrails.json",
    "reports/investment_guardrails.md",
    "reports/investment_guardrails.json",
    "reports/fiscal_trajectory.md",
    "reports/fiscal_trajectory.json",
    "reports/transition_funding.md",
    "reports/transition_funding.json",
    "reports/payment_interactions.md",
    "reports/payment_interactions.json",
    "reports/distributional_scenarios.md",
    "reports/distributional_scenarios.json",
    "reports/household_weighting.md",
    "reports/household_weighting.json",
    "reports/uncertainty_ranges.md",
    "reports/uncertainty_ranges.json",
    "reports/reviewed_scenarios.md",
    "reports/reviewed_scenarios.json",
    "reports/sector_schedule_expansion.md",
    "reports/sector_schedule_expansion.json",
    "reports/sector_stress_matrix.md",
    "reports/sector_stress_matrix.json",
    "reports/behavioural_response_simulation.md",
    "reports/behavioural_response_simulation.json",
    "reports/administrative_compliance_workflow.md",
    "reports/administrative_compliance_workflow.json",
    "reports/legislative_architecture.md",
    "reports/legislative_architecture.json",
    "reports/calibration_requirements.md",
    "reports/calibration_requirements.json",
    "reports/real_data_feasibility.md",
    "reports/real_data_feasibility.json",
}

FORBIDDEN_AFFIRMATIVE_DASHBOARD_CLAIMS = [
    "ready for government",
    "ready for ato",
    "operationally ready",
    "legally sufficient",
    "legislative-ready",
    "bill-ready",
    "parliament-ready",
    "validated",
    "treasury validated",
    "ato validated",
    "official dashboard",
    "official review pathway",
    "compliance score",
    "readiness score",
    "maturity score",
    "approved",
    "enforceable",
    "actual tax payable",
    "real policy result",
    "real household estimate",
    "population estimate",
    "official sector ranking",
    "economic validation is complete",
    "welfare validation is complete",
]

NEGATIVE_CONTEXT_MARKERS = [
    "not ",
    "not a ",
    "not an ",
    "no ",
    "no real ",
    "does not ",
    "do not ",
    "must not ",
    "must_not",
    "not_",
    "without ",
    "is not ",
    "are not ",
    "created no ",
    "creates no ",
    "cannot ",
    "only ",
]


@dataclass(frozen=True)
class DashboardLayer:
    layer_id: str
    layer_name: str
    layer_group: str
    purpose: str
    primary_files: list[str]
    primary_reports: list[str]
    streamlit_pages: list[str]
    status_labels: list[str]
    non_claim_flags: list[str]
    calibration_blockers: list[str]
    external_review_blockers: list[str]
    blocker_explanation: str
    recommended_reviewer: list[str]
    read_order: int
    main_reason: str
    must_not_be_used_for: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DashboardReportEntry:
    report_path: str
    exists: bool
    layer_id: str
    report_type: str
    generated_by: str
    interpretation_warning: str
    must_not_be_used_for: list[str]
    linked_streamlit_page: str | None
    recommended_read_order: int
    optional: bool = False

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DashboardNonClaimProfile:
    layer_id: str
    non_claim_flags: list[str]
    must_not_be_used_for: list[str]
    not_for_real_world_use: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DashboardCalibrationBlocker:
    layer_id: str
    blocker_type: str
    blocker: str
    external_review_needed: bool
    main_reason: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DashboardGuardrailStatus:
    source_report: str
    exists: bool
    clean: bool | None
    denied_findings: int | None
    warning_findings: int | None
    interpretation_warning: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DashboardNavigationGroup:
    read_order: int
    layer_id: str
    layer_name: str
    purpose: str
    official_process: bool
    main_reason: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutiveDashboardSummary:
    total_layers: int
    total_reports_indexed: int
    reports_present: int
    reports_missing: int
    layers_with_generated_reports: int
    synthetic_only_layers: int
    placeholder_only_layers: int
    non_operative_layers: int
    external_review_required_layers: int
    calibration_required_layers: int
    legal_review_required_layers: int
    tax_review_required_layers: int
    ato_methods_review_required_layers: int
    treasury_methods_review_required_layers: int
    privacy_review_required_layers: int
    statistical_methods_review_required_layers: int
    real_data_used: bool
    readiness_score_created: bool
    operational_readiness_claimed: bool
    legal_sufficiency_claimed: bool
    economic_validation_claimed: bool
    firm_level_liability_logic_modified: bool
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(EXECUTIVE_DASHBOARD_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExecutiveDashboardResult:
    dashboard_id: str
    dashboard_name: str
    status: str
    layers: list[DashboardLayer]
    report_entries: list[DashboardReportEntry]
    streamlit_page_index: list[str]
    non_claim_profiles: list[DashboardNonClaimProfile]
    calibration_blockers: list[DashboardCalibrationBlocker]
    external_review_blockers: list[DashboardCalibrationBlocker]
    guardrail_statuses: list[DashboardGuardrailStatus]
    suggested_review_navigation: list[DashboardNavigationGroup]
    missing_reports_or_navigation_gaps: list[str]
    summary: ExecutiveDashboardSummary
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(EXECUTIVE_DASHBOARD_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _required_mapping(source: dict[str, Any], required: list[str], label: str) -> None:
    missing = [key for key in required if key not in source]
    if missing:
        raise ValueError(f"{label} missing required fields: {', '.join(missing)}")


def _list_of_strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{label} must be a list of strings")
    return list(value)


def _bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be boolean")
    return value


def _int(value: Any, label: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{label} must be an integer")
    return value


def _path_exists(repo_root: Path, relative_path: str, label: str) -> bool:
    path = repo_root / relative_path
    if not path.exists():
        raise ValueError(f"{label} references missing path: {relative_path}")
    return True


def _layer_from_mapping(source: dict[str, Any], repo_root: Path) -> DashboardLayer:
    _required_mapping(
        source,
        [
            "layer_id",
            "layer_name",
            "layer_group",
            "purpose",
            "primary_files",
            "primary_reports",
            "streamlit_pages",
            "status_labels",
            "non_claim_flags",
            "calibration_blockers",
            "external_review_blockers",
            "blocker_explanation",
            "recommended_reviewer",
            "read_order",
            "main_reason",
            "must_not_be_used_for",
        ],
        f"dashboard layer {source.get('layer_id', '?')}",
    )
    layer_id = str(source["layer_id"])
    primary_files = _list_of_strings(source["primary_files"], f"layer {layer_id}.primary_files")
    primary_reports = _list_of_strings(source["primary_reports"], f"layer {layer_id}.primary_reports")
    streamlit_pages = _list_of_strings(source["streamlit_pages"], f"layer {layer_id}.streamlit_pages")
    status_labels = _list_of_strings(source["status_labels"], f"layer {layer_id}.status_labels")
    non_claim_flags = _list_of_strings(source["non_claim_flags"], f"layer {layer_id}.non_claim_flags")
    calibration_blockers = _list_of_strings(source["calibration_blockers"], f"layer {layer_id}.calibration_blockers")
    external_review_blockers = _list_of_strings(source["external_review_blockers"], f"layer {layer_id}.external_review_blockers")
    recommended_reviewer = _list_of_strings(source["recommended_reviewer"], f"layer {layer_id}.recommended_reviewer")
    must_not_be_used_for = _list_of_strings(source["must_not_be_used_for"], f"layer {layer_id}.must_not_be_used_for")

    for relative_path in primary_files + primary_reports + streamlit_pages:
        _path_exists(repo_root, relative_path, f"layer {layer_id}")
    if not non_claim_flags:
        raise ValueError(f"layer {layer_id} must include non-claim flags")
    if not must_not_be_used_for:
        raise ValueError(f"layer {layer_id} must include must_not_be_used_for")
    if not recommended_reviewer:
        raise ValueError(f"layer {layer_id} must include recommended reviewer routing")
    if not calibration_blockers and not external_review_blockers and not str(source["blocker_explanation"]).strip():
        raise ValueError(f"layer {layer_id} must include blockers or blocker explanation")

    return DashboardLayer(
        layer_id=layer_id,
        layer_name=str(source["layer_name"]),
        layer_group=str(source["layer_group"]),
        purpose=str(source["purpose"]),
        primary_files=primary_files,
        primary_reports=primary_reports,
        streamlit_pages=streamlit_pages,
        status_labels=status_labels,
        non_claim_flags=non_claim_flags,
        calibration_blockers=calibration_blockers,
        external_review_blockers=external_review_blockers,
        blocker_explanation=str(source["blocker_explanation"]),
        recommended_reviewer=recommended_reviewer,
        read_order=_int(source["read_order"], f"layer {layer_id}.read_order"),
        main_reason=str(source["main_reason"]),
        must_not_be_used_for=must_not_be_used_for,
    )


def _report_entry_from_mapping(source: dict[str, Any], repo_root: Path) -> DashboardReportEntry:
    _required_mapping(
        source,
        [
            "report_path",
            "layer_id",
            "report_type",
            "generated_by",
            "interpretation_warning",
            "must_not_be_used_for",
            "linked_streamlit_page",
            "recommended_read_order",
        ],
        f"dashboard report entry {source.get('report_path', '?')}",
    )
    report_path = str(source["report_path"])
    optional = _bool(source.get("optional", False), f"report {report_path}.optional")
    exists = (repo_root / report_path).exists()
    if not exists and not optional:
        raise ValueError(f"required dashboard report is missing: {report_path}")
    linked_page = source["linked_streamlit_page"]
    if linked_page is not None:
        linked_page = str(linked_page)
        _path_exists(repo_root, linked_page, f"report {report_path}.linked_streamlit_page")
    must_not = _list_of_strings(source["must_not_be_used_for"], f"report {report_path}.must_not_be_used_for")
    if not must_not:
        raise ValueError(f"report {report_path} must include must_not_be_used_for")
    return DashboardReportEntry(
        report_path=report_path,
        exists=exists,
        layer_id=str(source["layer_id"]),
        report_type=str(source["report_type"]),
        generated_by=str(source["generated_by"]),
        interpretation_warning=str(source["interpretation_warning"]),
        must_not_be_used_for=must_not,
        linked_streamlit_page=linked_page,
        recommended_read_order=_int(source["recommended_read_order"], f"report {report_path}.recommended_read_order"),
        optional=optional,
    )


def _guardrail_status_from_report(repo_root: Path, report_path: str) -> DashboardGuardrailStatus:
    path = repo_root / report_path
    if not path.exists():
        return DashboardGuardrailStatus(
            source_report=report_path,
            exists=False,
            clean=None,
            denied_findings=None,
            warning_findings=None,
            interpretation_warning="Guardrail report is missing; dashboard must not infer safety status.",
        )
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return DashboardGuardrailStatus(
            source_report=report_path,
            exists=True,
            clean=None,
            denied_findings=None,
            warning_findings=None,
            interpretation_warning="Guardrail report is not valid JSON; dashboard must not infer safety status.",
        )
    result = payload.get("result", {}) if isinstance(payload, dict) else {}
    findings = result.get("findings", []) if isinstance(result, dict) else []
    denied = result.get("denied_findings", []) if isinstance(result, dict) else []
    return DashboardGuardrailStatus(
        source_report=report_path,
        exists=True,
        clean=result.get("clean") if isinstance(result.get("clean"), bool) else None,
        denied_findings=len(denied) if isinstance(denied, list) else None,
        warning_findings=len(findings) if isinstance(findings, list) else None,
        interpretation_warning="Guardrail status is a prototype repository-safety signal only, not operational readiness or validation.",
    )


def _non_claim_profile(layer: DashboardLayer) -> DashboardNonClaimProfile:
    return DashboardNonClaimProfile(
        layer_id=layer.layer_id,
        non_claim_flags=layer.non_claim_flags,
        must_not_be_used_for=layer.must_not_be_used_for,
        not_for_real_world_use="not_for_real_world_use" in layer.status_labels
        or "not_actual_tax_payable" in layer.non_claim_flags
        or bool(layer.must_not_be_used_for),
    )


def _blockers_for_layer(layer: DashboardLayer, blocker_type: str) -> list[DashboardCalibrationBlocker]:
    source = layer.calibration_blockers if blocker_type == "calibration" else layer.external_review_blockers
    return [
        DashboardCalibrationBlocker(
            layer_id=layer.layer_id,
            blocker_type=blocker_type,
            blocker=blocker,
            external_review_needed=blocker_type == "external_review",
            main_reason=layer.main_reason,
        )
        for blocker in source
    ]


def _navigation_from_layers(layers: list[DashboardLayer]) -> list[DashboardNavigationGroup]:
    return [
        DashboardNavigationGroup(
            read_order=layer.read_order,
            layer_id=layer.layer_id,
            layer_name=layer.layer_name,
            purpose=layer.purpose,
            official_process=False,
            main_reason="Suggested review navigation only; not an official process.",
        )
        for layer in sorted(layers, key=lambda item: (item.read_order, item.layer_id))
    ]


def find_forbidden_affirmative_dashboard_claims(text: str) -> list[str]:
    lowered = text.lower()
    findings: list[str] = []
    for phrase in FORBIDDEN_AFFIRMATIVE_DASHBOARD_CLAIMS:
        start = 0
        while True:
            index = lowered.find(phrase, start)
            if index == -1:
                break
            context = lowered[max(0, index - 160) : index]
            if not any(marker in context for marker in NEGATIVE_CONTEXT_MARKERS):
                findings.append(phrase)
                break
            start = index + len(phrase)
    return sorted(set(findings))


def build_executive_dashboard_result(payload: dict[str, Any], repo_root: Path) -> ExecutiveDashboardResult:
    _required_mapping(
        payload,
        ["dashboard_id", "dashboard_name", "status", "non_claims", "layers", "report_entries", "forbidden_claims"],
        "executive dashboard manifest",
    )
    if payload["status"] != "prototype_dashboard_report_index_only":
        raise ValueError("executive dashboard status must be prototype_dashboard_report_index_only")
    for claim in EXECUTIVE_DASHBOARD_NON_CLAIMS:
        if claim not in payload["non_claims"]:
            raise ValueError("executive dashboard manifest missing required non-claim language")

    layers = [_layer_from_mapping(item, repo_root) for item in payload["layers"]]
    report_entries = [_report_entry_from_mapping(item, repo_root) for item in payload["report_entries"]]
    layer_ids = {layer.layer_id for layer in layers}
    missing_layers = sorted(REQUIRED_LAYER_IDS - layer_ids)
    if missing_layers:
        raise ValueError(f"executive dashboard manifest missing required layers: {', '.join(missing_layers)}")
    unknown_report_layers = sorted({entry.layer_id for entry in report_entries} - layer_ids)
    if unknown_report_layers:
        raise ValueError(f"dashboard report entries reference unknown layers: {', '.join(unknown_report_layers)}")
    report_paths = {entry.report_path for entry in report_entries}
    missing_required_reports = sorted(REQUIRED_REPORT_PATHS - report_paths)
    if missing_required_reports:
        raise ValueError(f"dashboard report index missing required generated reports: {', '.join(missing_required_reports)}")

    payload_for_claim_scan = {key: value for key, value in payload.items() if key != "forbidden_claims"}
    forbidden = find_forbidden_affirmative_dashboard_claims(str(payload_for_claim_scan))
    if forbidden:
        raise ValueError(f"dashboard manifest contains forbidden affirmative claims: {', '.join(forbidden)}")

    non_claim_profiles = [_non_claim_profile(layer) for layer in layers]
    calibration_blockers = [
        blocker
        for layer in layers
        for blocker in _blockers_for_layer(layer, "calibration")
    ]
    external_review_blockers = [
        blocker
        for layer in layers
        for blocker in _blockers_for_layer(layer, "external_review")
    ]
    guardrail_statuses = [
        _guardrail_status_from_report(repo_root, "reports/repo_guardrails.json"),
        _guardrail_status_from_report(repo_root, "reports/secure_ingestion_controls.json"),
        _guardrail_status_from_report(repo_root, "reports/investment_guardrails.json"),
    ]
    missing_reports = [entry.report_path for entry in report_entries if not entry.exists]
    page_index = sorted({page for layer in layers for page in layer.streamlit_pages})

    def _count_label(label: str) -> int:
        return sum(label in layer.status_labels or label in layer.non_claim_flags for layer in layers)

    def _count_review_need(*needles: str) -> int:
        count = 0
        for layer in layers:
            haystack = " ".join(
                layer.status_labels
                + layer.non_claim_flags
                + layer.recommended_reviewer
                + layer.calibration_blockers
                + layer.external_review_blockers
            ).lower()
            if any(needle in haystack for needle in needles):
                count += 1
        return count

    summary = ExecutiveDashboardSummary(
        total_layers=len(layers),
        total_reports_indexed=len(report_entries),
        reports_present=sum(entry.exists for entry in report_entries),
        reports_missing=len(missing_reports),
        layers_with_generated_reports=sum(bool(layer.primary_reports) for layer in layers),
        synthetic_only_layers=_count_label("synthetic_only"),
        placeholder_only_layers=_count_label("placeholder_only"),
        non_operative_layers=_count_label("non_operative"),
        external_review_required_layers=_count_review_need("external_review_required", "external review", "review required"),
        calibration_required_layers=_count_review_need("calibration_required", "calibration"),
        legal_review_required_layers=_count_review_need("legal_review_required", "legal_reviewer", "legal review"),
        tax_review_required_layers=_count_review_need("tax_review_required", "tax_reviewer", "tax review"),
        ato_methods_review_required_layers=_count_review_need("ato_methods_review_required", "ato_methods_reviewer", "ato methods"),
        treasury_methods_review_required_layers=_count_review_need("treasury_methods_review_required", "treasury_methods_reviewer", "treasury"),
        privacy_review_required_layers=_count_review_need("privacy_review_required", "privacy_reviewer", "privacy"),
        statistical_methods_review_required_layers=_count_review_need("statistical_methods_review_required", "statistical_methods_reviewer", "statistical"),
        real_data_used=False,
        readiness_score_created=False,
        operational_readiness_claimed=False,
        legal_sufficiency_claimed=False,
        economic_validation_claimed=False,
        firm_level_liability_logic_modified=False,
        warnings=[
            "Dashboard is navigation and consolidation only.",
            "No readiness score, maturity score, official review status, validation claim, or liability change is created.",
        ],
    )

    return ExecutiveDashboardResult(
        dashboard_id=str(payload["dashboard_id"]),
        dashboard_name=str(payload["dashboard_name"]),
        status=str(payload["status"]),
        layers=sorted(layers, key=lambda item: (item.read_order, item.layer_id)),
        report_entries=sorted(report_entries, key=lambda item: (item.recommended_read_order, item.report_path)),
        streamlit_page_index=page_index,
        non_claim_profiles=non_claim_profiles,
        calibration_blockers=calibration_blockers,
        external_review_blockers=external_review_blockers,
        guardrail_statuses=guardrail_statuses,
        suggested_review_navigation=_navigation_from_layers(layers),
        missing_reports_or_navigation_gaps=missing_reports,
        summary=summary,
        warnings=list(summary.warnings),
    )
