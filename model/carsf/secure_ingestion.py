"""Default-deny secure ingestion controls for CARSF evidence prototypes."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .sensitive_scan import scan_mapping_for_sensitive_markers


INGESTION_NON_CLAIMS = [
    "This is a prototype ingestion-control decision only. It is not a legal, privacy, cybersecurity, tax, ATO, Treasury, evidentiary, forensic, or audit determination.",
    "These controls are governance scaffolding only and do not implement secure storage or real access control.",
]

ALLOWED_STORAGE_ZONE = "data/mock_evidence/"


@dataclass(frozen=True)
class IngestionPolicy:
    policy_id: str
    version: str
    default_action: str
    allowed_modes: list[str]
    prohibited_content: list[str]
    allowed_storage_zones: list[str]
    prohibited_storage_zones: list[str]
    approval_required_for: list[str]
    non_claims: list[str] = field(default_factory=lambda: list(INGESTION_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IngestionRequest:
    request_id: str
    evidence_mode: str
    source_description: str
    intended_use: str
    storage_zone: str
    synthetic_mock_evidence_only: bool
    contains_personal_data: bool
    contains_real_business_data: bool
    contains_restricted_data: bool
    contains_secrets: bool
    declared_sensitivity: str
    requested_by: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IngestionDecision:
    request_id: str
    allowed: bool
    decision: str
    reasons: list[str]
    required_approvals: list[str]
    quarantine_required: bool
    redaction_required: bool
    retention_policy: str
    audit_required: bool
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(INGESTION_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def get_default_ingestion_policy() -> IngestionPolicy:
    return IngestionPolicy(
        policy_id="carsf-v1.5-default-deny-ingestion",
        version="CARSF V1.5 prototype secure ingestion controls",
        default_action="DENY",
        allowed_modes=["synthetic_mock"],
        prohibited_content=[
            "personal data",
            "real taxpayer data",
            "real business records",
            "restricted government data",
            "secrets, API keys, tokens, private keys, credentials",
            "TFNs, ABNs, ACNs, Medicare numbers, bank details, payslips, invoices, contracts",
        ],
        allowed_storage_zones=[ALLOWED_STORAGE_ZONE],
        prohibited_storage_zones=[
            "reports/",
            "docs/",
            "paper/",
            "model/",
            "simulator/",
            "scripts/",
            "./",
            "data/incoming/",
            "data/private/",
            "data/restricted/",
            "data/real_evidence/",
            "evidence_inbox/",
            "secure_drop/",
        ],
        approval_required_for=[
            "high synthetic sensitivity",
            "restricted-placeholder synthetic sensitivity",
            "external secure system design",
            "any future non-synthetic evidence path",
        ],
    )


def _request_from_any(request: IngestionRequest | dict[str, Any]) -> IngestionRequest:
    if isinstance(request, IngestionRequest):
        return request
    return IngestionRequest(
        request_id=str(request.get("request_id", "")),
        evidence_mode=str(request.get("evidence_mode", "")),
        source_description=str(request.get("source_description", "")),
        intended_use=str(request.get("intended_use", "")),
        storage_zone=str(request.get("storage_zone", "")),
        synthetic_mock_evidence_only=bool(request.get("synthetic_mock_evidence_only", False)),
        contains_personal_data=bool(request.get("contains_personal_data", False)),
        contains_real_business_data=bool(request.get("contains_real_business_data", False)),
        contains_restricted_data=bool(request.get("contains_restricted_data", False)),
        contains_secrets=bool(request.get("contains_secrets", False)),
        declared_sensitivity=str(request.get("declared_sensitivity", "unknown")),
        requested_by=request.get("requested_by"),
        metadata=dict(request.get("metadata", {}) or {}),
    )


def _normalised_zone(zone: str) -> str:
    cleaned = str(zone).replace("\\", "/").strip()
    return cleaned if cleaned.endswith("/") else f"{cleaned}/"


def evaluate_ingestion_request(
    request: IngestionRequest | dict[str, Any],
    policy: IngestionPolicy | None = None,
) -> IngestionDecision:
    """Evaluate one ingestion request under a default-deny prototype policy."""

    policy = policy or get_default_ingestion_policy()
    req = _request_from_any(request)
    reasons = [f"Default action is {policy.default_action}; request must satisfy every allow condition."]
    approvals: list[str] = []
    warnings = ["Real evidence must not be committed to this repository."]
    allowed = True
    zone = _normalised_zone(req.storage_zone)
    scan_result = scan_mapping_for_sensitive_markers(req.to_jsonable())

    if req.evidence_mode not in policy.allowed_modes:
        allowed = False
        reasons.append(f"evidence_mode `{req.evidence_mode}` is not allowed in this repo.")
    if req.synthetic_mock_evidence_only is not True:
        allowed = False
        approvals.append("external_secure_system_design")
        reasons.append("non-synthetic evidence is denied and must be handled outside this repo.")
    if zone not in policy.allowed_storage_zones:
        allowed = False
        reasons.append(f"storage_zone `{zone}` is not an allowed evidence storage zone.")
    if any(zone == _normalised_zone(prohibited) for prohibited in policy.prohibited_storage_zones):
        allowed = False
        reasons.append(f"storage_zone `{zone}` is explicitly prohibited for evidence storage.")
    if req.contains_personal_data:
        allowed = False
        approvals.append("privacy_review")
        reasons.append("declared personal data is denied.")
    if req.contains_real_business_data:
        allowed = False
        approvals.append("legal_tax_review")
        reasons.append("declared real taxpayer/business data is denied.")
    if req.contains_restricted_data:
        allowed = False
        approvals.append("restricted_data_governance_review")
        reasons.append("declared restricted government data is denied.")
    if req.contains_secrets:
        allowed = False
        approvals.append("security_review")
        reasons.append("declared secrets or credentials are denied.")
    if scan_result.deny_ingestion:
        allowed = False
        reasons.append(f"sensitive scanner found prohibited markers: {', '.join(scan_result.markers_found)}.")
    if req.declared_sensitivity in {"high", "restricted_placeholder"}:
        approvals.append("privacy_review")
        warnings.append("High-sensitivity mock evidence requires review before any external workflow use.")

    approvals = sorted(set(approvals))
    decision = "ALLOW_SYNTHETIC_MOCK_ONLY" if allowed else "DENY"
    if allowed and approvals:
        decision = "ALLOW_SYNTHETIC_MOCK_WITH_REVIEW"

    return IngestionDecision(
        request_id=req.request_id,
        allowed=allowed,
        decision=decision,
        reasons=reasons,
        required_approvals=approvals,
        quarantine_required=not allowed,
        redaction_required=scan_result.deny_ingestion or not allowed,
        retention_policy=("retain synthetic mock evidence in repo" if allowed else "do not retain evidence in repo"),
        audit_required=True,
        warnings=warnings + scan_result.warnings,
    )
