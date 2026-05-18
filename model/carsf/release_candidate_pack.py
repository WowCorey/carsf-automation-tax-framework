"""Release-candidate pack indexing for the CARSF V1.5 prototype.

This module packages existing prototype materials for review navigation. It
does not add modelling logic, create a readiness score, claim official status,
or modify firm-level CARSF liability.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


RELEASE_CANDIDATE_WARNING = (
    "This is a private research prototype and release-candidate pack only. It is not legal advice, "
    "not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare advice, not statistical "
    "validation, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, not legislative "
    "readiness, not a readiness score, and not an official review pathway. It does not determine actual tax payable, "
    "does not use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, "
    "and does not modify firm-level CARSF liability."
)

RELEASE_CANDIDATE_NON_CLAIMS = [
    RELEASE_CANDIDATE_WARNING,
    "The release-candidate pack only packages existing prototype reports, warnings, navigation, review blockers, and working-paper material for external review.",
    "Suggested reviewer routing is review navigation only and is not an official process.",
]

REQUIRED_LAYER_IDS = {
    "release_candidate_pack",
    "core_formula_model",
    "worked_examples",
    "sector_schedules",
    "sector_schedule_expansion",
    "sector_stress_matrix",
    "behavioural_response",
    "administrative_workflow",
    "legislative_architecture",
    "executive_dashboard",
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
    "working_paper",
    "status_risks_docs",
}

REQUIRED_LAYER_GROUPS = {
    "overview",
    "paper",
    "formula_core",
    "worked_examples",
    "sector_schedules",
    "sector_stress",
    "behavioural_response",
    "administrative_workflow",
    "legislative_architecture",
    "executive_dashboard",
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
    "calibration",
    "documentation",
}

REQUIRED_REPORT_PATHS = {
    "reports/example_results.md",
    "reports/example_results.json",
    "reports/grouped_entity_results.md",
    "reports/grouped_entity_results.json",
    "reports/transfer_pricing_results.md",
    "reports/transfer_pricing_results.json",
    "reports/evidence_requirements.md",
    "reports/evidence_requirements.json",
    "reports/calibration_requirements.md",
    "reports/calibration_requirements.json",
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
    "reports/executive_dashboard.md",
    "reports/executive_dashboard.json",
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
}

REQUIRED_RELEASE_DOCUMENTS = {
    "release/v1_5_rc/RELEASE_NOTES.md",
    "release/v1_5_rc/REVIEWER_BRIEFING.md",
    "release/v1_5_rc/REPORT_MAP.md",
    "release/v1_5_rc/CALIBRATION_BLOCKERS.md",
    "release/v1_5_rc/NON_CLAIM_BOUNDARIES.md",
    "release/v1_5_rc/EXTERNAL_REVIEW_ROUTING.md",
    "release/v1_5_rc/RELEASE_MANIFEST.json",
}

REQUIRED_WORKING_PAPER_REFERENCES = [
    "sector stress matrix",
    "behavioural response",
    "administrative workflow",
    "legislative architecture",
    "executive dashboard",
    "secure ingestion controls",
    "investment / incidence guardrails",
    "fiscal trajectory",
    "transition funding",
    "payment interactions",
    "household distributional scenarios",
    "household weighting",
    "uncertainty ranges",
    "reviewed scenario controls",
    "calibration blockers",
    "external review requirements",
]

FORBIDDEN_AFFIRMATIVE_RELEASE_CLAIMS = [
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
    "official release",
    "official review pathway",
    "official policy",
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
    "statistical validation is complete",
    "operational validation is complete",
    "legal review complete",
    "tax review complete",
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
    "what it does not show",
    "what_it_does_not_show",
    "primary_non_claim",
    "non-claim",
]


@dataclass(frozen=True)
class ReleaseCandidateLayer:
    layer_id: str
    layer_name: str
    layer_group: str
    summary: str
    primary_files: list[str]
    primary_reports: list[str]
    streamlit_pages: list[str]
    status_labels: list[str]
    non_claim_flags: list[str]
    calibration_blockers: list[str]
    external_review_blockers: list[str]
    must_not_be_used_for: list[str]
    recommended_reviewer: list[str]
    main_reason: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReleaseCandidateReport:
    report_path: str
    exists: bool
    layer_id: str
    generated_by: str
    what_it_shows: str
    what_it_does_not_show: str
    primary_non_claim: str
    recommended_reviewer: list[str]
    suggested_read_order: int
    optional: bool = False

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReleaseCandidateDocument:
    document_path: str
    exists: bool
    document_type: str
    purpose: str
    contains_non_claims: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReleaseCandidateBlocker:
    layer_id: str
    blocker_type: str
    blocker: str
    review_needed: str
    main_reason: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReleaseCandidateReviewRoute:
    reviewer: str
    layers: list[str]
    reports: list[str]
    release_documents: list[str]
    main_reason: str
    official_process: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReleaseCandidateNonClaim:
    layer_id: str
    non_claim_flags: list[str]
    must_not_be_used_for: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReleaseCandidatePackSummary:
    total_layers: int
    total_reports_indexed: int
    reports_present: int
    reports_missing: int
    total_release_documents: int
    release_documents_present: int
    release_documents_missing: int
    paper_files_checked: int
    working_paper_updated: bool
    layers_requiring_calibration: int
    layers_requiring_legal_review: int
    layers_requiring_tax_review: int
    layers_requiring_ato_methods_review: int
    layers_requiring_treasury_methods_review: int
    layers_requiring_privacy_review: int
    layers_requiring_statistical_review: int
    layers_requiring_economic_review: int
    layers_requiring_welfare_review: int
    layers_requiring_parliamentary_counsel_review: int
    real_data_used: bool
    readiness_score_created: bool
    operational_readiness_claimed: bool
    legal_sufficiency_claimed: bool
    legislative_readiness_claimed: bool
    economic_validation_claimed: bool
    welfare_validation_claimed: bool
    statistical_validation_claimed: bool
    official_status_claimed: bool
    firm_level_liability_logic_modified: bool
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(RELEASE_CANDIDATE_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReleaseCandidatePackResult:
    release_id: str
    release_name: str
    release_status: str
    release_date_placeholder: str
    source_documents: list[str]
    prototype_layers: list[ReleaseCandidateLayer]
    generated_reports: list[ReleaseCandidateReport]
    release_documents: list[ReleaseCandidateDocument]
    reviewer_routes: list[ReleaseCandidateReviewRoute]
    calibration_blockers: list[ReleaseCandidateBlocker]
    external_review_blockers: list[ReleaseCandidateBlocker]
    non_claim_profiles: list[ReleaseCandidateNonClaim]
    missing_items_or_release_gaps: list[str]
    guardrail_status: dict[str, Any]
    summary: ReleaseCandidatePackSummary
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(RELEASE_CANDIDATE_NON_CLAIMS))

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


def _int(value: Any, label: str) -> int:
    if not isinstance(value, int):
        raise ValueError(f"{label} must be an integer")
    return value


def _bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be boolean")
    return value


def _path_exists(repo_root: Path, relative_path: str, label: str) -> bool:
    path = repo_root / relative_path
    if not path.exists():
        raise ValueError(f"{label} references missing path: {relative_path}")
    return True


def _has_non_claim_language(text: str) -> bool:
    lowered = text.lower()
    return all(
        phrase in lowered
        for phrase in [
            "not legal advice",
            "not tax advice",
            "not ato guidance",
            "not treasury modelling",
            "does not modify firm-level carsf liability",
        ]
    )


def find_forbidden_affirmative_release_claims(text: str) -> list[str]:
    lowered = text.lower()
    findings: list[str] = []
    for phrase in FORBIDDEN_AFFIRMATIVE_RELEASE_CLAIMS:
        start = 0
        while True:
            index = lowered.find(phrase, start)
            if index == -1:
                break
            context = lowered[max(0, index - 180) : index]
            if not any(marker in context for marker in NEGATIVE_CONTEXT_MARKERS):
                findings.append(phrase)
                break
            start = index + len(phrase)
    return sorted(set(findings))


def _layer_from_mapping(source: dict[str, Any], repo_root: Path) -> ReleaseCandidateLayer:
    _required_mapping(
        source,
        [
            "layer_id",
            "layer_name",
            "layer_group",
            "summary",
            "primary_files",
            "primary_reports",
            "streamlit_pages",
            "status_labels",
            "non_claim_flags",
            "calibration_blockers",
            "external_review_blockers",
            "must_not_be_used_for",
            "recommended_reviewer",
            "main_reason",
        ],
        f"release layer {source.get('layer_id', '?')}",
    )
    layer_id = str(source["layer_id"])
    primary_files = _list_of_strings(source["primary_files"], f"layer {layer_id}.primary_files")
    primary_reports = _list_of_strings(source["primary_reports"], f"layer {layer_id}.primary_reports")
    streamlit_pages = _list_of_strings(source["streamlit_pages"], f"layer {layer_id}.streamlit_pages")
    status_labels = _list_of_strings(source["status_labels"], f"layer {layer_id}.status_labels")
    non_claim_flags = _list_of_strings(source["non_claim_flags"], f"layer {layer_id}.non_claim_flags")
    calibration_blockers = _list_of_strings(source["calibration_blockers"], f"layer {layer_id}.calibration_blockers")
    external_review_blockers = _list_of_strings(source["external_review_blockers"], f"layer {layer_id}.external_review_blockers")
    must_not = _list_of_strings(source["must_not_be_used_for"], f"layer {layer_id}.must_not_be_used_for")
    reviewers = _list_of_strings(source["recommended_reviewer"], f"layer {layer_id}.recommended_reviewer")
    for relative_path in primary_files + primary_reports + streamlit_pages:
        _path_exists(repo_root, relative_path, f"layer {layer_id}")
    if not non_claim_flags:
        raise ValueError(f"layer {layer_id} must include non-claim flags")
    if not must_not:
        raise ValueError(f"layer {layer_id} must include must_not_be_used_for")
    if not reviewers:
        raise ValueError(f"layer {layer_id} must include reviewer routing")
    return ReleaseCandidateLayer(
        layer_id=layer_id,
        layer_name=str(source["layer_name"]),
        layer_group=str(source["layer_group"]),
        summary=str(source["summary"]),
        primary_files=primary_files,
        primary_reports=primary_reports,
        streamlit_pages=streamlit_pages,
        status_labels=status_labels,
        non_claim_flags=non_claim_flags,
        calibration_blockers=calibration_blockers,
        external_review_blockers=external_review_blockers,
        must_not_be_used_for=must_not,
        recommended_reviewer=reviewers,
        main_reason=str(source["main_reason"]),
    )


def _report_from_mapping(source: dict[str, Any], repo_root: Path) -> ReleaseCandidateReport:
    _required_mapping(
        source,
        [
            "report_path",
            "layer_id",
            "generated_by",
            "what_it_shows",
            "what_it_does_not_show",
            "primary_non_claim",
            "recommended_reviewer",
            "suggested_read_order",
        ],
        f"release report {source.get('report_path', '?')}",
    )
    report_path = str(source["report_path"])
    optional = _bool(source.get("optional", False), f"report {report_path}.optional")
    exists = (repo_root / report_path).exists()
    if not exists and not optional:
        raise ValueError(f"required release report is missing: {report_path}")
    reviewers = _list_of_strings(source["recommended_reviewer"], f"report {report_path}.recommended_reviewer")
    return ReleaseCandidateReport(
        report_path=report_path,
        exists=exists,
        layer_id=str(source["layer_id"]),
        generated_by=str(source["generated_by"]),
        what_it_shows=str(source["what_it_shows"]),
        what_it_does_not_show=str(source["what_it_does_not_show"]),
        primary_non_claim=str(source["primary_non_claim"]),
        recommended_reviewer=reviewers,
        suggested_read_order=_int(source["suggested_read_order"], f"report {report_path}.suggested_read_order"),
        optional=optional,
    )


def _document_from_mapping(source: dict[str, Any], repo_root: Path) -> ReleaseCandidateDocument:
    _required_mapping(source, ["document_path", "document_type", "purpose"], "release document")
    document_path = str(source["document_path"])
    exists = (repo_root / document_path).exists()
    if not exists:
        raise ValueError(f"required release document is missing: {document_path}")
    text = (repo_root / document_path).read_text(encoding="utf-8")
    if not _has_non_claim_language(text):
        raise ValueError(f"release document missing required non-claim language: {document_path}")
    forbidden = find_forbidden_affirmative_release_claims(text)
    if forbidden:
        raise ValueError(f"release document contains forbidden affirmative claims: {document_path}: {', '.join(forbidden)}")
    return ReleaseCandidateDocument(
        document_path=document_path,
        exists=exists,
        document_type=str(source["document_type"]),
        purpose=str(source["purpose"]),
        contains_non_claims=True,
    )


def _review_route_from_mapping(source: dict[str, Any]) -> ReleaseCandidateReviewRoute:
    _required_mapping(source, ["reviewer", "layers", "reports", "release_documents", "main_reason"], "review route")
    return ReleaseCandidateReviewRoute(
        reviewer=str(source["reviewer"]),
        layers=_list_of_strings(source["layers"], f"route {source.get('reviewer', '?')}.layers"),
        reports=_list_of_strings(source["reports"], f"route {source.get('reviewer', '?')}.reports"),
        release_documents=_list_of_strings(source["release_documents"], f"route {source.get('reviewer', '?')}.release_documents"),
        main_reason=str(source["main_reason"]),
        official_process=False,
    )


def _blockers_from_layer(layer: ReleaseCandidateLayer, blocker_type: str) -> list[ReleaseCandidateBlocker]:
    blockers = layer.calibration_blockers if blocker_type == "calibration" else layer.external_review_blockers
    return [
        ReleaseCandidateBlocker(
            layer_id=layer.layer_id,
            blocker_type=blocker_type,
            blocker=blocker,
            review_needed=blocker_type,
            main_reason=layer.main_reason,
        )
        for blocker in blockers
    ]


def _non_claim_profile(layer: ReleaseCandidateLayer) -> ReleaseCandidateNonClaim:
    return ReleaseCandidateNonClaim(
        layer_id=layer.layer_id,
        non_claim_flags=layer.non_claim_flags,
        must_not_be_used_for=layer.must_not_be_used_for,
    )


def _guardrail_status(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "reports" / "repo_guardrails.json"
    if not path.exists():
        return {
            "source_report": "reports/repo_guardrails.json",
            "exists": False,
            "clean": None,
            "denied_findings": None,
            "warning_findings": None,
            "interpretation_warning": "Missing guardrail report; release pack cannot infer repository safety.",
        }
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {
            "source_report": "reports/repo_guardrails.json",
            "exists": True,
            "clean": None,
            "denied_findings": None,
            "warning_findings": None,
            "interpretation_warning": "Guardrail report is not valid JSON.",
        }
    result = payload.get("result", {}) if isinstance(payload, dict) else {}
    findings = result.get("findings", []) if isinstance(result, dict) else []
    denied = result.get("denied_findings", []) if isinstance(result, dict) else []
    return {
        "source_report": "reports/repo_guardrails.json",
        "exists": True,
        "clean": result.get("clean") if isinstance(result.get("clean"), bool) else None,
        "denied_findings": len(denied) if isinstance(denied, list) else None,
        "warning_findings": len(findings) if isinstance(findings, list) else None,
        "interpretation_warning": "Guardrail status is a prototype repository-safety signal only, not validation or operational readiness.",
    }


def _count_review_need(layers: list[ReleaseCandidateLayer], *needles: str) -> int:
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


def _working_paper_has_required_references(repo_root: Path, source_documents: list[str]) -> bool:
    paper_paths = [path for path in source_documents if path.endswith("CARSF_V1_5_WORKING.md")]
    if not paper_paths:
        raise ValueError("release manifest must reference paper/CARSF_V1_5_WORKING.md")
    paper_text = "\n".join((repo_root / path).read_text(encoding="utf-8").lower() for path in paper_paths)
    missing = [term for term in REQUIRED_WORKING_PAPER_REFERENCES if term not in paper_text]
    if missing:
        raise ValueError(f"working paper missing V1.5 release-candidate references: {', '.join(missing)}")
    return True


def build_release_candidate_pack_result(payload: dict[str, Any], repo_root: Path) -> ReleaseCandidatePackResult:
    _required_mapping(
        payload,
        [
            "release_id",
            "release_name",
            "release_status",
            "release_date_placeholder",
            "non_claims",
            "source_documents",
            "prototype_layers",
            "generated_reports",
            "streamlit_pages",
            "reviewer_routes",
            "release_documents",
            "forbidden_claims",
        ],
        "release manifest",
    )
    if payload["release_status"] != "private_research_prototype_release_candidate_pack":
        raise ValueError("release_status must be private_research_prototype_release_candidate_pack")
    for non_claim in RELEASE_CANDIDATE_NON_CLAIMS:
        if non_claim not in payload["non_claims"]:
            raise ValueError("release manifest missing required non-claim language")

    source_documents = _list_of_strings(payload["source_documents"], "source_documents")
    for source_path in source_documents:
        _path_exists(repo_root, source_path, "source document")
    working_paper_updated = _working_paper_has_required_references(repo_root, source_documents)

    layers = [_layer_from_mapping(item, repo_root) for item in payload["prototype_layers"]]
    layer_ids = {layer.layer_id for layer in layers}
    missing_layers = sorted(REQUIRED_LAYER_IDS - layer_ids)
    if missing_layers:
        raise ValueError(f"release manifest missing required layers: {', '.join(missing_layers)}")
    missing_groups = sorted(REQUIRED_LAYER_GROUPS - {layer.layer_group for layer in layers})
    if missing_groups:
        raise ValueError(f"release manifest missing required layer groups: {', '.join(missing_groups)}")

    reports = [_report_from_mapping(item, repo_root) for item in payload["generated_reports"]]
    report_paths = {report.report_path for report in reports}
    missing_reports_from_index = sorted(REQUIRED_REPORT_PATHS - report_paths)
    if missing_reports_from_index:
        raise ValueError(f"release report index missing required reports: {', '.join(missing_reports_from_index)}")
    unknown_report_layers = sorted({report.layer_id for report in reports} - layer_ids)
    if unknown_report_layers:
        raise ValueError(f"release reports reference unknown layers: {', '.join(unknown_report_layers)}")

    documents = [_document_from_mapping(item, repo_root) for item in payload["release_documents"]]
    document_paths = {document.document_path for document in documents}
    missing_release_documents = sorted(REQUIRED_RELEASE_DOCUMENTS - document_paths)
    if missing_release_documents:
        raise ValueError(f"release document index missing required documents: {', '.join(missing_release_documents)}")

    for page in _list_of_strings(payload["streamlit_pages"], "streamlit_pages"):
        _path_exists(repo_root, page, "release streamlit page")
    routes = [_review_route_from_mapping(item) for item in payload["reviewer_routes"]]
    if not routes:
        raise ValueError("release manifest must include reviewer routes")
    route_layers = sorted({layer_id for route in routes for layer_id in route.layers} - layer_ids)
    if route_layers:
        raise ValueError(f"release reviewer routes reference unknown layers: {', '.join(route_layers)}")
    route_reports = sorted({report for route in routes for report in route.reports} - report_paths)
    if route_reports:
        raise ValueError(f"release reviewer routes reference unknown reports: {', '.join(route_reports)}")
    route_documents = sorted({document for route in routes for document in route.release_documents} - document_paths)
    if route_documents:
        raise ValueError(f"release reviewer routes reference unknown release documents: {', '.join(route_documents)}")

    calibration_blockers = [blocker for layer in layers for blocker in _blockers_from_layer(layer, "calibration")]
    external_review_blockers = [blocker for layer in layers for blocker in _blockers_from_layer(layer, "external_review")]
    missing_reports = [report.report_path for report in reports if not report.exists]
    missing_documents = [document.document_path for document in documents if not document.exists]

    payload_for_claim_scan = {key: value for key, value in payload.items() if key != "forbidden_claims"}
    forbidden = find_forbidden_affirmative_release_claims(str(payload_for_claim_scan))
    if forbidden:
        raise ValueError(f"release manifest contains forbidden affirmative claims: {', '.join(forbidden)}")

    summary = ReleaseCandidatePackSummary(
        total_layers=len(layers),
        total_reports_indexed=len(reports),
        reports_present=sum(report.exists for report in reports),
        reports_missing=len(missing_reports),
        total_release_documents=len(documents),
        release_documents_present=sum(document.exists for document in documents),
        release_documents_missing=len(missing_documents),
        paper_files_checked=len(source_documents),
        working_paper_updated=working_paper_updated,
        layers_requiring_calibration=_count_review_need(layers, "calibration"),
        layers_requiring_legal_review=_count_review_need(layers, "legal_review_required", "legal_reviewer", "legal review"),
        layers_requiring_tax_review=_count_review_need(layers, "tax_review_required", "tax_reviewer", "tax review"),
        layers_requiring_ato_methods_review=_count_review_need(layers, "ato_methods_review_required", "ato_methods_reviewer", "ato methods"),
        layers_requiring_treasury_methods_review=_count_review_need(layers, "treasury_methods_review_required", "treasury_methods_reviewer", "treasury"),
        layers_requiring_privacy_review=_count_review_need(layers, "privacy_review_required", "privacy_reviewer", "privacy"),
        layers_requiring_statistical_review=_count_review_need(layers, "statistical_methods_review_required", "statistical_methods_reviewer", "statistical"),
        layers_requiring_economic_review=_count_review_need(layers, "economic_methods_review_required", "economic_methods_reviewer", "economic"),
        layers_requiring_welfare_review=_count_review_need(layers, "welfare_policy_review_required", "welfare_policy_reviewer", "welfare"),
        layers_requiring_parliamentary_counsel_review=_count_review_need(layers, "parliamentary_counsel_review_required", "parliamentary_counsel_reviewer", "parliamentary"),
        real_data_used=False,
        readiness_score_created=False,
        operational_readiness_claimed=False,
        legal_sufficiency_claimed=False,
        legislative_readiness_claimed=False,
        economic_validation_claimed=False,
        welfare_validation_claimed=False,
        statistical_validation_claimed=False,
        official_status_claimed=False,
        firm_level_liability_logic_modified=False,
        warnings=[
            "Release-candidate pack is packaging and review navigation only.",
            "No readiness score, official status, validation, legal sufficiency, operational readiness, or liability change is created.",
        ],
    )

    return ReleaseCandidatePackResult(
        release_id=str(payload["release_id"]),
        release_name=str(payload["release_name"]),
        release_status=str(payload["release_status"]),
        release_date_placeholder=str(payload["release_date_placeholder"]),
        source_documents=source_documents,
        prototype_layers=sorted(layers, key=lambda item: item.layer_id),
        generated_reports=sorted(reports, key=lambda item: (item.suggested_read_order, item.report_path)),
        release_documents=sorted(documents, key=lambda item: item.document_path),
        reviewer_routes=sorted(routes, key=lambda item: item.reviewer),
        calibration_blockers=calibration_blockers,
        external_review_blockers=external_review_blockers,
        non_claim_profiles=[_non_claim_profile(layer) for layer in layers],
        missing_items_or_release_gaps=missing_reports + missing_documents,
        guardrail_status=_guardrail_status(repo_root),
        summary=summary,
        warnings=list(summary.warnings),
    )
