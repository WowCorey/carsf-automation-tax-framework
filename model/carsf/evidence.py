"""Prototype evidence requirements and assessment helpers for CARSF.

This layer records what evidence would be required before CARSF inputs could be
treated as externally reviewable. It does not validate evidence or create legal,
tax, Treasury, ATO, forensic, or audit findings.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


EVIDENCE_NON_CLAIMS = [
    "This is a prototype evidence assessment only. It is not legal, tax, Treasury, ATO, evidentiary, forensic, or audit validation.",
    "Evidence requirements are draft scaffolding and are not final policy, law, guidance, or audit procedure.",
    "Placeholder examples remain insufficient for real liability, calibration, or policy claims.",
]
CONFIDENCE_RANK = {
    "none": 0,
    "placeholder": 1,
    "low": 2,
    "medium": 3,
    "high": 4,
    "verified": 5,
}


@dataclass(frozen=True)
class EvidenceRequirement:
    requirement_id: str
    field: str
    category: str
    description: str
    acceptable_sources: list[str]
    minimum_confidence: str
    required_for: list[str]
    legal_sensitivity: str
    privacy_sensitivity: str
    placeholder_only: bool
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class EvidenceItem:
    evidence_id: str
    requirement_id: str
    source_type: str
    source_description: str
    confidence: str
    provided: bool
    date_or_period: str | None = None
    limitations: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class EvidenceAssessment:
    status: str
    missing_requirements: list[str] = field(default_factory=list)
    low_confidence_items: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    review_required: bool = True
    non_claims: list[str] = field(default_factory=lambda: list(EVIDENCE_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _requirement(
    requirement_id: str,
    field: str,
    category: str,
    description: str,
    acceptable_sources: list[str],
    required_for: list[str],
    legal_sensitivity: str = "medium",
    privacy_sensitivity: str = "medium",
    minimum_confidence: str = "medium",
    placeholder_only: bool = True,
    notes: list[str] | None = None,
) -> EvidenceRequirement:
    return EvidenceRequirement(
        requirement_id=requirement_id,
        field=field,
        category=category,
        description=description,
        acceptable_sources=acceptable_sources,
        minimum_confidence=minimum_confidence,
        required_for=required_for,
        legal_sensitivity=legal_sensitivity,
        privacy_sensitivity=privacy_sensitivity,
        placeholder_only=placeholder_only,
        notes=notes or ["Prototype evidence requirement; final source rules require policy and legal review."],
    )


def get_default_evidence_requirements() -> list[EvidenceRequirement]:
    """Return draft evidence requirements for V1.5 review scaffolding."""

    payroll = ["payroll records", "timesheets", "employment contracts", "Fair Work / award mapping", "audited workforce records"]
    firm = ["audited accounts", "management accounts", "invoices", "contracts", "tax workpapers"]
    system = ["system logs", "workflow records", "platform records", "warehouse or transport-management records"]
    government = ["ATO aggregated tax data", "ABS industry data", "DSS / Services Australia data", "Treasury modelling", "state payroll tax datasets"]
    legal = ["legal review", "tax counsel review", "related-party agreements", "transfer-pricing workpapers"]

    return [
        _requirement("core_output_value", "output.value", "core_formula", "Canonical output quantity and measurement period.", system + firm, ["core_formula", "mixed_units"]),
        _requirement("core_output_unit", "output.unit", "core_formula", "Canonical output unit mapped to a prototype schedule.", system + ["schedule determination"], ["core_formula", "mixed_units"]),
        _requirement("core_opfte_libc", "schedule.opfte_libc_placeholder", "core_formula", "LIBC output-per-FTE benchmark.", government + ["industry productivity datasets"], ["core_formula", "calibration"], "high", "low"),
        _requirement("core_worker_hours", "workers.annual_hours", "core_formula", "Verified hours for QLC workers.", payroll, ["core_formula", "safe_harbour"], privacy_sensitivity="high"),
        _requirement("core_wage_quality", "workers.wage_quality", "core_formula", "Evidence supporting wage quality score.", payroll, ["core_formula", "safe_harbour"], privacy_sensitivity="high"),
        _requirement("core_job_security", "workers.job_security", "core_formula", "Evidence supporting job security score.", payroll, ["core_formula", "safe_harbour"], privacy_sensitivity="high"),
        _requirement("core_skill_development", "workers.skill_development", "core_formula", "Training, apprenticeship, or transition evidence.", payroll + ["training records"], ["core_formula", "safe_harbour"], privacy_sensitivity="high"),
        _requirement("core_australian_nexus", "workers.australian_nexus", "core_formula", "Australian nexus evidence for QLC.", payroll + ["work-location evidence"], ["core_formula", "grouping"], legal_sensitivity="high", privacy_sensitivity="high"),
        _requirement("core_aii_components", "automation_components", "core_formula", "Bounded AII component evidence.", system + firm, ["core_formula", "avoidance"]),
        _requirement("core_aava_revenue_costs", "aava_inputs", "core_formula", "Australian-attributable revenue and verified cost evidence.", firm + legal, ["core_formula", "transfer_pricing"], legal_sensitivity="high"),
        _requirement("core_frv", "schedule.frv", "core_formula", "Fiscal replacement value floor, standard, and full settings.", government, ["core_formula", "calibration"], "high", "medium"),
        _requirement("core_capital_base", "capital_base", "core_formula", "Capital base evidence for PRRT-inspired uplift logic.", firm + legal, ["core_formula", "transfer_pricing"]),
        _requirement("core_rates", "caps.uplift_rate/rent_tax_rate", "core_formula", "Uplift and rent-tax-rate settings.", government + ["Treasury modelling"], ["core_formula", "calibration"], "high", "low"),
        _requirement("core_credits", "credits", "core_formula", "Verified credit evidence.", firm + ["training records", "program records"], ["core_formula", "safe_harbour"]),
        _requirement("safe_harbour_revenue", "safe_harbours.revenue_threshold", "safe_harbour", "Revenue threshold evidence.", firm + ["ATO aggregated tax data"], ["safe_harbour"]),
        _requirement("safe_harbour_worker_assist", "risk_metadata.worker_assist_admin_ai", "safe_harbour", "Evidence that AI is worker-assist/admin rather than labour-substituting.", system + payroll, ["safe_harbour", "avoidance"]),
        _requirement("safe_harbour_low_nltg", "outputs.nltg", "safe_harbour", "Evidence supporting low-NLTG treatment.", firm + system, ["safe_harbour"]),
        _requirement("safe_harbour_startup", "risk_metadata.startup_placeholder", "safe_harbour", "Startup status and grouping review evidence.", firm + legal, ["safe_harbour", "grouping"]),
        _requirement("safe_harbour_essential_service", "risk_metadata.essential_service_review", "safe_harbour", "Essential-service review evidence.", ["regulatory classification", "policy review"], ["safe_harbour"]),
        _requirement("avoid_token_oversight", "risk_metadata.token_human_oversight_risk", "avoidance", "Token human oversight role evidence.", payroll + system, ["avoidance"]),
        _requirement("avoid_fake_qlc", "risk_metadata.fake_qlc_inflation_risk", "avoidance", "Fake QLC inflation evidence.", payroll + firm, ["avoidance"]),
        _requirement("avoid_offshore_ai", "risk_metadata.offshore_automation_service", "avoidance", "Offshore automation service evidence.", legal + system, ["avoidance", "transfer_pricing"], "high"),
        _requirement("avoid_related_party_fees", "risk_metadata.related_party_ai_service_fees", "avoidance", "Related-party service fee evidence.", legal + firm, ["avoidance", "transfer_pricing"], "high"),
        _requirement("avoid_cloud_relabelling", "risk_metadata.cloud_cost_relabeling_risk", "avoidance", "Cloud/inference relabelling evidence.", firm + ["cloud invoices"], ["avoidance", "transfer_pricing"]),
        _requirement("avoid_robotics_leasing", "risk_metadata.robotics_leasing_risk", "avoidance", "Robotics leasing evidence.", legal + firm, ["avoidance", "transfer_pricing"]),
        _requirement("avoid_entity_splitting", "risk_metadata.entity_splitting_risk", "avoidance", "Entity-splitting evidence.", legal + firm, ["avoidance", "grouping"], "high"),
        _requirement("avoid_sector_classification", "risk_metadata.sector_classification_risk", "avoidance", "Sector classification arbitrage evidence.", system + ["schedule determination"], ["avoidance", "mixed_units"]),
        _requirement("group_common_control", "group.common_ownership_control", "grouping", "Common ownership or control evidence.", legal + firm, ["grouping"], "high"),
        _requirement("group_ip_owner", "entities.role.platform_ip_owner", "grouping", "IP/platform ownership relationship evidence.", legal, ["grouping", "transfer_pricing"], "high"),
        _requirement("group_service_provider", "entities.role.service_provider", "grouping", "Platform/service-provider relationship evidence.", legal + system, ["grouping"]),
        _requirement("group_customer_facing", "entities.role.customer_facing", "grouping", "Australian customer-facing entity evidence.", firm + system, ["grouping"]),
        _requirement("group_employer", "entities.role.australian_employer", "grouping", "Australian employer entity evidence.", payroll + legal, ["grouping"], privacy_sensitivity="high"),
        _requirement("group_offshore_provider", "entities.role.offshore_service_provider", "grouping", "Offshore service provider evidence.", legal + system, ["grouping", "transfer_pricing"], "high"),
        _requirement("tp_related_party_agreements", "related_party_transactions.agreements", "transfer_pricing", "Related-party agreement evidence.", legal, ["transfer_pricing"], "high"),
        _requirement("tp_service_fee_invoices", "related_party_transactions.service_fees", "transfer_pricing", "Service fee invoice evidence.", firm + legal, ["transfer_pricing"]),
        _requirement("tp_royalty_licence", "related_party_transactions.royalties", "transfer_pricing", "Royalty or licence agreement evidence.", legal, ["transfer_pricing"], "high"),
        _requirement("tp_cost_sharing", "related_party_transactions.cost_sharing", "transfer_pricing", "Cost-sharing or group recharge evidence.", legal + firm, ["transfer_pricing"]),
        _requirement("tp_cloud_inference", "related_party_transactions.cloud_inference", "transfer_pricing", "Cloud/inference bill evidence.", firm + ["cloud invoices"], ["transfer_pricing"]),
        _requirement("tp_robotics_leasing", "related_party_transactions.robotics_leasing", "transfer_pricing", "Robotics leasing contract evidence.", legal + firm, ["transfer_pricing"]),
        _requirement("tp_data_model_access", "related_party_transactions.data_model_access", "transfer_pricing", "Data/model access fee evidence.", legal + system, ["transfer_pricing"]),
        _requirement("tp_management_technical", "related_party_transactions.management_service", "transfer_pricing", "Management or technical service fee evidence.", legal + firm, ["transfer_pricing"]),
        _requirement("mixed_unit_evidence", "canonical_output_unit", "mixed_units", "Canonical output unit evidence.", system + ["schedule determination"], ["mixed_units"]),
        _requirement("mixed_conversion_metadata", "conversion_metadata", "mixed_units", "Reviewed conversion metadata where units differ.", system + ["policy review"], ["mixed_units"], "high"),
        _requirement("mixed_activity_shares", "apportionment.activities.share", "mixed_units", "Activity-share evidence.", firm + system, ["mixed_units"]),
        _requirement("mixed_revenue_aava_basis", "revenue_or_aava_share_basis", "mixed_units", "Revenue/AAVA share basis evidence.", firm, ["mixed_units"]),
        _requirement("mixed_schedule_classification", "schedule_id", "mixed_units", "Schedule classification evidence.", ["schedule determination", "policy review"], ["mixed_units"], "high"),
    ]


def _targets(required_for: str | list[str]) -> set[str]:
    if isinstance(required_for, str):
        return {required_for}
    return {str(item) for item in required_for}


def _items(source: dict[str, Any]) -> list[EvidenceItem]:
    raw = source.get("evidence_items", [])
    if raw is None:
        return []
    if not isinstance(raw, list):
        return []
    items: list[EvidenceItem] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            continue
        items.append(
            EvidenceItem(
                evidence_id=str(item.get("evidence_id", f"evidence_{index + 1}")),
                requirement_id=str(item.get("requirement_id", "")),
                source_type=str(item.get("source_type", "")),
                source_description=str(item.get("source_description", "")),
                confidence=str(item.get("confidence", "none")).lower(),
                provided=bool(item.get("provided", False)),
                date_or_period=item.get("date_or_period"),
                limitations=[str(value) for value in item.get("limitations", [])],
            )
        )
    return items


def _is_placeholder_source(source: dict[str, Any]) -> bool:
    combined = " ".join(str(source.get(key, "")) for key in ("status", "placeholder_notice", "calibration_status"))
    return "placeholder" in combined.lower() or source.get("illustrative_placeholder_only") is True


def assess_evidence(
    example_or_group: dict[str, Any],
    required_for: str | list[str],
    evidence_packet: Any | None = None,
) -> EvidenceAssessment:
    """Assess whether supplied evidence items meet prototype requirements."""

    targets = _targets(required_for)
    requirements = [
        requirement
        for requirement in get_default_evidence_requirements()
        if targets.intersection(requirement.required_for)
    ]
    supplied_items = _items(example_or_group)
    if evidence_packet is not None:
        supplied_items.extend(list(getattr(evidence_packet, "evidence_items", [])))
    supplied = {item.requirement_id: item for item in supplied_items if item.provided}
    missing: list[str] = []
    low_confidence: list[str] = []
    warnings = [
        "Evidence assessment is prototype-only and does not validate any liability, legal position, tax position, or audit finding.",
    ]
    if evidence_packet is not None:
        warnings.append("Mock evidence can upgrade prototype status only; it does not create real-world sufficiency.")

    for requirement in requirements:
        item = supplied.get(requirement.requirement_id)
        if item is None:
            missing.append(requirement.requirement_id)
            continue
        if CONFIDENCE_RANK.get(item.confidence, 0) < CONFIDENCE_RANK.get(requirement.minimum_confidence, 3):
            low_confidence.append(item.evidence_id)

    if not supplied and _is_placeholder_source(example_or_group):
        status = "placeholder_only"
    elif not supplied:
        status = "insufficient"
    elif evidence_packet is not None and (missing or low_confidence):
        status = "partial"
    elif evidence_packet is not None:
        status = "sufficient_for_prototype"
    elif missing or low_confidence:
        status = "partial"
    else:
        status = "sufficient"

    if status != "sufficient":
        warnings.append("Evidence remains insufficient for real calibration, legal use, or actual tax-payable claims.")

    return EvidenceAssessment(
        status=status,
        missing_requirements=missing,
        low_confidence_items=low_confidence,
        warnings=warnings,
        review_required=status != "sufficient",
    )


def requirements_by_category() -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for requirement in get_default_evidence_requirements():
        grouped.setdefault(requirement.category, []).append(asdict(requirement))
    return grouped
