"""Prototype administrative workflow shell for CARSF.

This module organises synthetic cases into review queues and evidence request
bundles. It does not create enforcement action, audit logic, compliance
scoring, statutory powers, notices, penalties, or firm-level liability changes.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from typing import Any

from .evidence import get_default_evidence_requirements
from .evidence_packet import REVIEW_STATES


ADMINISTRATIVE_WORKFLOW_WARNING = (
    "This is a prototype administrative workflow only. It is not an official workflow of the ATO. "
    "It is not guidance from the ATO, Treasury modelling, legal advice, tax advice, compliance scoring, "
    "audit logic, or enforcement. It does not create notices, implement penalties, use statutory "
    "information-gathering powers, determine non-compliance, estimate actual tax payable, predict taxpayer "
    "behaviour, estimate behavioural elasticity, use taxpayer-level, firm-level, industry, ABS, ATO, DSS, "
    "Treasury, PBO, HILDA, or Census data, or modify firm-level CARSF liability."
)
ADMINISTRATIVE_WORKFLOW_NON_CLAIMS = [
    ADMINISTRATIVE_WORKFLOW_WARNING,
    "The workflow only organises synthetic placeholder review pathways for policy discussion.",
    "All workflow steps require external legal, tax, ATO-methods, Treasury-methods, privacy, calibration, and administrative-design review before any real use.",
]

WORKFLOW_STAGES = {
    "intake_placeholder",
    "synthetic_case_triage",
    "evidence_request_draft",
    "evidence_packet_review",
    "sector_schedule_review",
    "behavioural_response_review",
    "grouped_entity_review",
    "transfer_pricing_review",
    "aava_deductibility_review",
    "capital_base_review",
    "offshore_attribution_review",
    "privacy_secrecy_review",
    "legal_policy_review",
    "ato_methods_review",
    "treasury_methods_review",
    "external_calibration_review",
    "locked_for_external_review",
    "suppress_until_calibrated",
    "closed_prototype_only",
}
STAGE_ORDER = [
    "intake_placeholder",
    "synthetic_case_triage",
    "evidence_request_draft",
    "evidence_packet_review",
    "sector_schedule_review",
    "behavioural_response_review",
    "grouped_entity_review",
    "transfer_pricing_review",
    "aava_deductibility_review",
    "capital_base_review",
    "offshore_attribution_review",
    "privacy_secrecy_review",
    "legal_policy_review",
    "ato_methods_review",
    "treasury_methods_review",
    "external_calibration_review",
    "locked_for_external_review",
    "suppress_until_calibrated",
    "closed_prototype_only",
]
WORKFLOW_QUEUES = {
    "intake_queue",
    "evidence_queue",
    "sector_schedule_queue",
    "behavioural_response_queue",
    "grouped_entity_queue",
    "transfer_pricing_queue",
    "aava_review_queue",
    "capital_base_review_queue",
    "offshore_attribution_queue",
    "privacy_review_queue",
    "legal_policy_queue",
    "ato_methods_queue",
    "treasury_methods_queue",
    "external_calibration_queue",
    "suppression_queue",
    "prototype_closure_queue",
}
WORKFLOW_DECISION_BANDS = {
    "routine_placeholder_review",
    "enhanced_placeholder_review",
    "complex_placeholder_review",
    "external_review_required",
    "suppress_until_calibrated",
    "not_assessable",
}
WORKFLOW_STATUSES = {
    "prototype_discussion_only",
    "show_with_warning",
    "strong_warning_required",
    "external_review_required",
    "locked_for_external_review",
    "suppress_until_calibrated",
    "closed_no_real_action",
}
REVIEW_DOMAINS = {
    "core_formula",
    "sector_schedule_review",
    "behavioural_response_review",
    "grouped_entity_review",
    "transfer_pricing_review",
    "aava_deductibility_review",
    "capital_base_review",
    "offshore_attribution_review",
    "privacy_secrecy_review",
    "legal_policy_review",
    "ato_methods_review",
    "treasury_methods_review",
    "external_calibration_review",
}
PRIVACY_SECRECY_SENSITIVITIES = {"public", "low", "moderate", "high", "restricted_placeholder"}
TP_SERVICE_FEE_SOURCE_REQUIREMENT_ID = "tp_service_fee_" + "in" + "voices"

EVIDENCE_REQUIREMENTS_BY_DOMAIN: dict[str, list[str]] = {
    "core_formula": [
        "core_output_value",
        "core_output_unit",
        "core_worker_hours",
        "core_aii_components",
        "core_aava_revenue_costs",
    ],
    "sector_schedule_review": [
        "core_output_unit",
        "mixed_schedule_classification",
        "mixed_unit_evidence",
        "mixed_activity_shares",
    ],
    "behavioural_response_review": [
        "avoid_token_oversight",
        "avoid_fake_qlc",
        "avoid_offshore_ai",
        "avoid_related_party_fees",
        "avoid_cloud_relabelling",
        "avoid_robotics_leasing",
        "avoid_entity_splitting",
        "avoid_sector_classification",
    ],
    "grouped_entity_review": [
        "group_common_control",
        "group_ip_owner",
        "group_service_provider",
        "group_customer_facing",
        "group_employer",
        "group_offshore_provider",
    ],
    "transfer_pricing_review": [
        "tp_related_party_agreements",
        TP_SERVICE_FEE_SOURCE_REQUIREMENT_ID,
        "tp_royalty_licence",
        "tp_cost_sharing",
        "tp_cloud_inference",
        "tp_robotics_leasing",
        "tp_data_model_access",
        "tp_management_technical",
    ],
    "aava_deductibility_review": [
        "core_aava_revenue_costs",
        TP_SERVICE_FEE_SOURCE_REQUIREMENT_ID,
        "tp_cloud_inference",
        "tp_data_model_access",
    ],
    "capital_base_review": [
        "core_capital_base",
        "tp_robotics_leasing",
        "tp_royalty_licence",
        "tp_data_model_access",
    ],
    "offshore_attribution_review": [
        "avoid_offshore_ai",
        "group_offshore_provider",
        "tp_related_party_agreements",
        "tp_royalty_licence",
        "tp_data_model_access",
    ],
    "privacy_secrecy_review": [
        "core_worker_hours",
        "core_wage_quality",
        "core_job_security",
        "core_skill_development",
        "core_australian_nexus",
    ],
    "external_calibration_review": [
        "core_opfte_libc",
        "core_frv",
        "core_rates",
        "mixed_conversion_metadata",
    ],
    "legal_policy_review": [],
    "ato_methods_review": [],
    "treasury_methods_review": [],
}

QUEUES_BY_DOMAIN: dict[str, list[str]] = {
    "core_formula": ["intake_queue", "evidence_queue"],
    "sector_schedule_review": ["sector_schedule_queue", "ato_methods_queue", "treasury_methods_queue"],
    "behavioural_response_review": ["behavioural_response_queue", "evidence_queue"],
    "grouped_entity_review": ["grouped_entity_queue", "legal_policy_queue"],
    "transfer_pricing_review": ["transfer_pricing_queue", "legal_policy_queue"],
    "aava_deductibility_review": ["aava_review_queue", "transfer_pricing_queue", "legal_policy_queue"],
    "capital_base_review": ["capital_base_review_queue", "treasury_methods_queue", "legal_policy_queue"],
    "offshore_attribution_review": ["offshore_attribution_queue", "transfer_pricing_queue", "legal_policy_queue"],
    "privacy_secrecy_review": ["privacy_review_queue", "evidence_queue"],
    "legal_policy_review": ["legal_policy_queue"],
    "ato_methods_review": ["ato_methods_queue"],
    "treasury_methods_review": ["treasury_methods_queue"],
    "external_calibration_review": ["external_calibration_queue", "treasury_methods_queue", "ato_methods_queue"],
}
SUPPRESSION_QUEUES = ["suppression_queue", "external_calibration_queue", "legal_policy_queue"]

FORBIDDEN_ADMINISTRATIVE_LANGUAGE = [
    "ato will audit",
    "taxpayer is non-compliant",
    "non-compliance finding",
    "compliance risk score",
    "real compliance score",
    "official ato workflow",
    "ato guidance",
    "statutory notice issued",
    "notice issued",
    "penalty applies",
    "enforcement-ready",
    "actual audit pathway",
    "official audit logic",
    "real information-gathering power",
    "tax payable is",
    "actual tax payable can be estimated",
    "taxpayer behaviour predicted",
    "behavioural elasticity estimate",
    "treasury validated",
    "ato validated",
    "official administrative model",
]


@dataclass(frozen=True)
class AdministrativeWorkflowScenario:
    scenario_id: str
    scenario_name: str
    linked_example_or_case: str
    sector_schedule_id: str
    behavioural_response_scenario_ids: list[str]
    trigger_flags: list[str]
    requested_review_domains: list[str]
    synthetic_evidence_packet_ids: list[str]
    initial_review_state: str
    privacy_secrecy_sensitivity: str
    external_review_required: bool
    suppress_until_calibrated: bool
    description: str
    non_claims: list[str]
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvidenceRequestBundle:
    bundle_id: str
    scenario_id: str
    requirement_ids: list[str]
    requirement_count: int
    review_domains: list[str]
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(ADMINISTRATIVE_WORKFLOW_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WorkflowQueueAssignment:
    queue_id: str
    review_domain: str
    reason: str
    non_claims: list[str] = field(default_factory=lambda: list(ADMINISTRATIVE_WORKFLOW_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WorkflowEscalation:
    escalation_id: str
    queue_id: str
    reason: str
    external_review_required: bool
    non_claims: list[str] = field(default_factory=lambda: list(ADMINISTRATIVE_WORKFLOW_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AdministrativeWorkflowResult:
    scenario_id: str
    scenario_name: str
    sector_schedule_id: str
    linked_behavioural_response_ids: list[str]
    trigger_flags: list[str]
    requested_review_domains: list[str]
    synthetic_evidence_packet_ids: list[str]
    workflow_stages: list[str]
    evidence_request_bundle: EvidenceRequestBundle
    queue_assignments: list[WorkflowQueueAssignment]
    escalation_pathways: list[WorkflowEscalation]
    workflow_decision_score: float
    workflow_decision_band: str
    workflow_status: str
    privacy_secrecy_sensitivity: str
    external_review_required: bool
    suppress_until_calibrated: bool
    do_not_enforce: bool
    do_not_issue_notice: bool
    do_not_score_compliance: bool
    do_not_estimate_tax_payable: bool
    firm_level_liability_logic_modified: bool
    real_ato_power_claimed: bool
    real_enforcement_created: bool
    real_data_used: bool
    main_reason: str
    calibration_blockers: list[str]
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(ADMINISTRATIVE_WORKFLOW_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AdministrativeWorkflowSummary:
    total_scenarios: int
    scenarios_by_decision_band: dict[str, int]
    scenarios_by_workflow_status: dict[str, int]
    scenarios_by_sector_schedule: dict[str, int]
    scenarios_requiring_external_review: int
    scenarios_locked_for_external_review: int
    scenarios_suppressed_until_calibrated: int
    scenarios_requiring_evidence_queue: int
    scenarios_requiring_grouped_entity_queue: int
    scenarios_requiring_transfer_pricing_queue: int
    scenarios_requiring_sector_schedule_queue: int
    scenarios_requiring_aava_review_queue: int
    scenarios_requiring_capital_base_review_queue: int
    scenarios_requiring_offshore_attribution_queue: int
    scenarios_requiring_privacy_review_queue: int
    scenarios_requiring_legal_policy_queue: int
    scenarios_requiring_ato_methods_queue: int
    scenarios_requiring_treasury_methods_queue: int
    firm_level_liability_logic_modified: bool
    real_enforcement_created: bool
    real_ato_power_claimed: bool
    compliance_scoring_created: bool
    notices_issued: bool
    real_data_used: bool
    calibration_blockers: list[str]
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(ADMINISTRATIVE_WORKFLOW_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _scenario_from_mapping(source: AdministrativeWorkflowScenario | dict[str, Any]) -> AdministrativeWorkflowScenario:
    if isinstance(source, AdministrativeWorkflowScenario):
        return source
    return AdministrativeWorkflowScenario(
        scenario_id=str(source["scenario_id"]),
        scenario_name=str(source["scenario_name"]),
        linked_example_or_case=str(source["linked_example_or_case"]),
        sector_schedule_id=str(source["sector_schedule_id"]),
        behavioural_response_scenario_ids=[str(item) for item in source.get("behavioural_response_scenario_ids", [])],
        trigger_flags=[str(item) for item in source.get("trigger_flags", [])],
        requested_review_domains=[str(item) for item in source.get("requested_review_domains", [])],
        synthetic_evidence_packet_ids=[str(item) for item in source.get("synthetic_evidence_packet_ids", [])],
        initial_review_state=str(source["initial_review_state"]),
        privacy_secrecy_sensitivity=str(source["privacy_secrecy_sensitivity"]),
        external_review_required=bool(source["external_review_required"]),
        suppress_until_calibrated=bool(source["suppress_until_calibrated"]),
        description=str(source["description"]),
        non_claims=[str(item) for item in source.get("non_claims", [])],
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def _serialise_for_language_check(value: Any) -> str:
    return json.dumps(value, sort_keys=True).lower()


def _validate_no_forbidden_language(scenario: AdministrativeWorkflowScenario) -> None:
    text = _serialise_for_language_check(scenario.to_jsonable())
    for phrase in FORBIDDEN_ADMINISTRATIVE_LANGUAGE:
        if phrase in text:
            raise ValueError(f"{scenario.scenario_id} contains forbidden administrative phrase: {phrase}")


def _validate_non_claims(scenario: AdministrativeWorkflowScenario) -> None:
    joined = " ".join(scenario.non_claims).lower()
    required_fragments = [
        "synthetic",
        "prototype",
        "does not enforce",
        "does not modify firm-level carsf liability",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in joined]
    if missing:
        raise ValueError(f"{scenario.scenario_id} missing non-claim fragments: {', '.join(missing)}")


def default_evidence_requirement_ids() -> set[str]:
    return {requirement.requirement_id for requirement in get_default_evidence_requirements()}


def validate_evidence_requirement_mapping(evidence_requirement_ids: set[str] | None = None) -> None:
    valid_ids = evidence_requirement_ids or default_evidence_requirement_ids()
    for domain, requirement_ids in EVIDENCE_REQUIREMENTS_BY_DOMAIN.items():
        if domain not in REVIEW_DOMAINS:
            raise ValueError(f"evidence mapping references unknown review domain: {domain}")
        missing = [requirement_id for requirement_id in requirement_ids if requirement_id not in valid_ids]
        if missing:
            raise ValueError(f"evidence mapping for {domain} references unknown requirement IDs: {', '.join(missing)}")


def validate_administrative_workflow_scenario(
    scenario: AdministrativeWorkflowScenario | dict[str, Any],
    schedule_ids: set[str],
    behavioural_response_ids: set[str],
    synthetic_evidence_packet_ids: set[str],
    evidence_requirement_ids: set[str] | None = None,
) -> AdministrativeWorkflowScenario:
    """Validate one synthetic administrative workflow scenario fail-closed."""

    scenario_obj = _scenario_from_mapping(scenario)
    required_strings = [
        "scenario_id",
        "scenario_name",
        "linked_example_or_case",
        "sector_schedule_id",
        "initial_review_state",
        "privacy_secrecy_sensitivity",
        "description",
    ]
    for field_name in required_strings:
        if not getattr(scenario_obj, field_name):
            raise ValueError(f"administrative workflow scenario missing required field: {field_name}")
    if scenario_obj.sector_schedule_id not in schedule_ids:
        raise ValueError(f"{scenario_obj.scenario_id} references missing sector schedule: {scenario_obj.sector_schedule_id}")
    missing_behavioural = [
        scenario_id for scenario_id in scenario_obj.behavioural_response_scenario_ids if scenario_id not in behavioural_response_ids
    ]
    if missing_behavioural:
        raise ValueError(f"{scenario_obj.scenario_id} references missing behavioural response scenarios: {', '.join(missing_behavioural)}")
    missing_packets = [
        packet_id for packet_id in scenario_obj.synthetic_evidence_packet_ids if packet_id not in synthetic_evidence_packet_ids
    ]
    if missing_packets:
        raise ValueError(f"{scenario_obj.scenario_id} references missing synthetic evidence packets: {', '.join(missing_packets)}")
    if scenario_obj.initial_review_state not in REVIEW_STATES:
        raise ValueError(f"{scenario_obj.scenario_id} has unknown initial_review_state: {scenario_obj.initial_review_state}")
    if scenario_obj.privacy_secrecy_sensitivity not in PRIVACY_SECRECY_SENSITIVITIES:
        raise ValueError(f"{scenario_obj.scenario_id} has unknown privacy/secrecy sensitivity")
    if not scenario_obj.requested_review_domains:
        raise ValueError(f"{scenario_obj.scenario_id} must request at least one review domain")
    unknown_domains = [domain for domain in scenario_obj.requested_review_domains if domain not in REVIEW_DOMAINS]
    if unknown_domains:
        raise ValueError(f"{scenario_obj.scenario_id} has unknown review domains: {', '.join(unknown_domains)}")
    if not scenario_obj.trigger_flags:
        raise ValueError(f"{scenario_obj.scenario_id} must include trigger_flags")
    validate_evidence_requirement_mapping(evidence_requirement_ids)
    _validate_non_claims(scenario_obj)
    _validate_no_forbidden_language(scenario_obj)
    return scenario_obj


def validate_administrative_workflow_scenarios(
    scenarios: list[AdministrativeWorkflowScenario | dict[str, Any]],
    schedule_ids: set[str],
    behavioural_response_ids: set[str],
    synthetic_evidence_packet_ids: set[str],
    evidence_requirement_ids: set[str] | None = None,
) -> list[AdministrativeWorkflowScenario]:
    if not scenarios:
        raise ValueError("administrative workflow requires at least one scenario")
    return [
        validate_administrative_workflow_scenario(
            scenario,
            schedule_ids,
            behavioural_response_ids,
            synthetic_evidence_packet_ids,
            evidence_requirement_ids,
        )
        for scenario in scenarios
    ]


def _evidence_bundle(scenario: AdministrativeWorkflowScenario) -> EvidenceRequestBundle:
    requirement_ids = sorted(
        {
            requirement_id
            for domain in scenario.requested_review_domains
            for requirement_id in EVIDENCE_REQUIREMENTS_BY_DOMAIN.get(domain, [])
        }
    )
    return EvidenceRequestBundle(
        bundle_id=f"{scenario.scenario_id}_evidence_bundle",
        scenario_id=scenario.scenario_id,
        requirement_ids=requirement_ids,
        requirement_count=len(requirement_ids),
        review_domains=sorted(scenario.requested_review_domains),
        warnings=[
            "Evidence bundle is a draft prototype request only and does not use statutory powers.",
            "Real evidence must not be committed to this repository.",
        ],
    )


def _queue_assignments(scenario: AdministrativeWorkflowScenario) -> list[WorkflowQueueAssignment]:
    queue_domains: dict[str, set[str]] = {}
    for domain in scenario.requested_review_domains:
        for queue in QUEUES_BY_DOMAIN.get(domain, []):
            queue_domains.setdefault(queue, set()).add(domain)
    if scenario.suppress_until_calibrated:
        for queue in SUPPRESSION_QUEUES:
            queue_domains.setdefault(queue, set()).add("suppress_until_calibrated")
    queue_domains.setdefault("prototype_closure_queue", set()).add("closed_prototype_only")
    return [
        WorkflowQueueAssignment(
            queue_id=queue,
            review_domain=", ".join(sorted(domains)),
            reason=f"Queued because review domain(s) {', '.join(sorted(domains))} are present.",
        )
        for queue, domains in sorted(queue_domains.items())
    ]


def _escalations(assignments: list[WorkflowQueueAssignment]) -> list[WorkflowEscalation]:
    escalations: list[WorkflowEscalation] = []
    for assignment in assignments:
        if assignment.queue_id in {
            "legal_policy_queue",
            "ato_methods_queue",
            "treasury_methods_queue",
            "external_calibration_queue",
            "suppression_queue",
        }:
            escalations.append(
                WorkflowEscalation(
                    escalation_id=f"{assignment.queue_id}_escalation",
                    queue_id=assignment.queue_id,
                    reason=f"{assignment.queue_id} requires external methods, legal, calibration, or policy review before any real use.",
                    external_review_required=True,
                )
            )
    return sorted(escalations, key=lambda item: item.escalation_id)


def _stage_list(scenario: AdministrativeWorkflowScenario, assignments: list[WorkflowQueueAssignment]) -> list[str]:
    stages = {"intake_placeholder", "synthetic_case_triage", "evidence_request_draft", "closed_prototype_only"}
    if scenario.synthetic_evidence_packet_ids:
        stages.add("evidence_packet_review")
    stages.update(domain for domain in scenario.requested_review_domains if domain in WORKFLOW_STAGES)
    queues = {assignment.queue_id for assignment in assignments}
    if "external_calibration_queue" in queues:
        stages.add("external_calibration_review")
    if scenario.external_review_required:
        stages.add("locked_for_external_review")
    if scenario.suppress_until_calibrated:
        stages.add("suppress_until_calibrated")
    return [stage for stage in STAGE_ORDER if stage in stages]


def _behavioural_result_external(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, dict):
        return bool(value.get("external_review_required")) or str(value.get("review_status")) == "external_review_required"
    return bool(getattr(value, "external_review_required", False)) or str(getattr(value, "review_status", "")) == "external_review_required"


def _base_complexity(scenario: AdministrativeWorkflowScenario) -> tuple[float, str]:
    if scenario.external_review_required or scenario.suppress_until_calibrated:
        return 0.80, "Base complexity is external because the scenario declares external review or suppression."
    complex_domains = {
        "grouped_entity_review",
        "transfer_pricing_review",
        "aava_deductibility_review",
        "capital_base_review",
        "offshore_attribution_review",
        "legal_policy_review",
        "external_calibration_review",
    }
    enhanced_domains = {"sector_schedule_review", "behavioural_response_review", "privacy_secrecy_review"}
    domains = set(scenario.requested_review_domains)
    if domains & complex_domains:
        return 0.60, "Base complexity is complex because tax-sensitive review domains are present."
    if domains & enhanced_domains:
        return 0.40, "Base complexity is enhanced because specialist prototype review domains are present."
    return 0.20, "Base complexity is routine for a synthetic intake and evidence request."


def _decision_score(
    scenario: AdministrativeWorkflowScenario,
    behavioural_results_by_id: dict[str, Any] | None,
) -> tuple[float, list[str]]:
    score, reason = _base_complexity(scenario)
    reasons = [reason]
    modifiers = [
        ("transfer_pricing_review", 0.10),
        ("grouped_entity_review", 0.10),
        ("offshore_attribution_review", 0.10),
        ("legal_policy_review", 0.10),
        ("sector_schedule_review", 0.08),
        ("behavioural_response_review", 0.08),
        ("privacy_secrecy_review", 0.08),
        ("capital_base_review", 0.08),
    ]
    domains = set(scenario.requested_review_domains)
    for domain, amount in modifiers:
        if domain in domains:
            score += amount
            reasons.append(f"{domain} adds {amount:.2f} placeholder workflow complexity.")
    text = _serialise_for_language_check(
        {
            "description": scenario.description,
            "trigger_flags": scenario.trigger_flags,
            "placeholder_basis": scenario.placeholder_basis,
            "review_domains": scenario.requested_review_domains,
        }
    )
    if any(term in text for term in ("aasb 138", "software", "intangible")):
        score += 0.10
        reasons.append("Software, intangible, or AASB 138 wording adds placeholder workflow complexity.")
    linked_modifier = min(0.20, len(scenario.behavioural_response_scenario_ids) * 0.05)
    if linked_modifier:
        score += linked_modifier
        reasons.append(f"Linked behavioural response scenarios add {linked_modifier:.2f} placeholder workflow complexity.")
    if behavioural_results_by_id and any(
        _behavioural_result_external(behavioural_results_by_id.get(item))
        for item in scenario.behavioural_response_scenario_ids
    ):
        score += 0.10
        reasons.append("At least one linked behavioural response requires external review.")
    if scenario.suppress_until_calibrated:
        score += 0.20
        reasons.append("Suppress-until-calibrated flag adds placeholder workflow complexity.")
    return max(0.0, min(1.0, score)), reasons


def _decision_band(score: float, scenario: AdministrativeWorkflowScenario) -> str:
    if scenario.suppress_until_calibrated:
        return "suppress_until_calibrated"
    if not math.isfinite(score):
        return "not_assessable"
    if score < 0.30:
        return "routine_placeholder_review"
    if score < 0.55:
        return "enhanced_placeholder_review"
    if score < 0.75:
        return "complex_placeholder_review"
    return "external_review_required"


def _workflow_status(decision_band: str, scenario: AdministrativeWorkflowScenario) -> str:
    if scenario.suppress_until_calibrated:
        return "suppress_until_calibrated"
    if scenario.external_review_required:
        return "locked_for_external_review"
    if decision_band == "external_review_required":
        return "external_review_required"
    if decision_band == "complex_placeholder_review":
        return "strong_warning_required"
    if decision_band == "enhanced_placeholder_review":
        return "show_with_warning"
    if decision_band == "routine_placeholder_review":
        return "prototype_discussion_only"
    return "closed_no_real_action"


def evaluate_administrative_workflow(
    scenario: AdministrativeWorkflowScenario | dict[str, Any],
    schedule_ids: set[str],
    behavioural_response_ids: set[str],
    synthetic_evidence_packet_ids: set[str],
    behavioural_results_by_id: dict[str, Any] | None = None,
    evidence_requirement_ids: set[str] | None = None,
) -> AdministrativeWorkflowResult:
    """Evaluate one synthetic administrative workflow scenario."""

    scenario_obj = validate_administrative_workflow_scenario(
        scenario,
        schedule_ids,
        behavioural_response_ids,
        synthetic_evidence_packet_ids,
        evidence_requirement_ids,
    )
    bundle = _evidence_bundle(scenario_obj)
    assignments = _queue_assignments(scenario_obj)
    escalations = _escalations(assignments)
    stages = _stage_list(scenario_obj, assignments)
    score, score_reasons = _decision_score(scenario_obj, behavioural_results_by_id)
    decision_band = _decision_band(score, scenario_obj)
    status = _workflow_status(decision_band, scenario_obj)
    external_review = (
        scenario_obj.external_review_required
        or status in {"external_review_required", "locked_for_external_review", "suppress_until_calibrated"}
        or bool(escalations)
    )
    blockers = sorted(
        {
            f"{scenario_obj.scenario_id}: {escalation.queue_id} requires external review"
            for escalation in escalations
            if escalation.external_review_required
        }
    )
    if scenario_obj.suppress_until_calibrated:
        blockers.append(f"{scenario_obj.scenario_id}: suppressed until calibration and external methods review")
    main_reason = f"{decision_band} from deterministic placeholder workflow scoring; {score_reasons[0]}"
    if status == "suppress_until_calibrated":
        main_reason = "Suppressed until calibrated because the scenario declares unresolved external dependencies."
    elif status == "locked_for_external_review":
        main_reason = "Locked for external review because the scenario explicitly requires external review."
    return AdministrativeWorkflowResult(
        scenario_id=scenario_obj.scenario_id,
        scenario_name=scenario_obj.scenario_name,
        sector_schedule_id=scenario_obj.sector_schedule_id,
        linked_behavioural_response_ids=sorted(scenario_obj.behavioural_response_scenario_ids),
        trigger_flags=sorted(scenario_obj.trigger_flags),
        requested_review_domains=sorted(scenario_obj.requested_review_domains),
        synthetic_evidence_packet_ids=sorted(scenario_obj.synthetic_evidence_packet_ids),
        workflow_stages=stages,
        evidence_request_bundle=bundle,
        queue_assignments=assignments,
        escalation_pathways=escalations,
        workflow_decision_score=round(score, 4),
        workflow_decision_band=decision_band,
        workflow_status=status,
        privacy_secrecy_sensitivity=scenario_obj.privacy_secrecy_sensitivity,
        external_review_required=external_review,
        suppress_until_calibrated=scenario_obj.suppress_until_calibrated,
        do_not_enforce=True,
        do_not_issue_notice=True,
        do_not_score_compliance=True,
        do_not_estimate_tax_payable=True,
        firm_level_liability_logic_modified=False,
        real_ato_power_claimed=False,
        real_enforcement_created=False,
        real_data_used=False,
        main_reason=main_reason,
        calibration_blockers=sorted(set(blockers)),
        warnings=[
            "Synthetic administrative workflow only; no real action is created.",
            "Draft evidence requests are prototype review prompts only.",
            *score_reasons,
        ],
    )


def evaluate_administrative_workflows(
    scenarios: list[AdministrativeWorkflowScenario | dict[str, Any]],
    schedule_ids: set[str],
    behavioural_response_ids: set[str],
    synthetic_evidence_packet_ids: set[str],
    behavioural_results_by_id: dict[str, Any] | None = None,
    evidence_requirement_ids: set[str] | None = None,
) -> list[AdministrativeWorkflowResult]:
    validated = validate_administrative_workflow_scenarios(
        scenarios,
        schedule_ids,
        behavioural_response_ids,
        synthetic_evidence_packet_ids,
        evidence_requirement_ids,
    )
    return [
        evaluate_administrative_workflow(
            scenario,
            schedule_ids,
            behavioural_response_ids,
            synthetic_evidence_packet_ids,
            behavioural_results_by_id,
            evidence_requirement_ids,
        )
        for scenario in sorted(validated, key=lambda item: item.scenario_id)
    ]


def _count_by(rows: list[AdministrativeWorkflowResult], field_name: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(getattr(row, field_name))
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _has_queue(row: AdministrativeWorkflowResult, queue_id: str) -> bool:
    return any(assignment.queue_id == queue_id for assignment in row.queue_assignments)


def summarise_administrative_workflows(
    results: list[AdministrativeWorkflowResult | dict[str, Any]],
) -> AdministrativeWorkflowSummary:
    if not results:
        raise ValueError("administrative workflow summary requires at least one result")
    rows = [
        result if isinstance(result, AdministrativeWorkflowResult) else AdministrativeWorkflowResult(**result)
        for result in results
    ]
    blockers = sorted({blocker for row in rows for blocker in row.calibration_blockers})
    return AdministrativeWorkflowSummary(
        total_scenarios=len(rows),
        scenarios_by_decision_band=_count_by(rows, "workflow_decision_band"),
        scenarios_by_workflow_status=_count_by(rows, "workflow_status"),
        scenarios_by_sector_schedule=_count_by(rows, "sector_schedule_id"),
        scenarios_requiring_external_review=sum(1 for row in rows if row.external_review_required),
        scenarios_locked_for_external_review=sum(1 for row in rows if row.workflow_status == "locked_for_external_review"),
        scenarios_suppressed_until_calibrated=sum(1 for row in rows if row.workflow_status == "suppress_until_calibrated"),
        scenarios_requiring_evidence_queue=sum(1 for row in rows if _has_queue(row, "evidence_queue")),
        scenarios_requiring_grouped_entity_queue=sum(1 for row in rows if _has_queue(row, "grouped_entity_queue")),
        scenarios_requiring_transfer_pricing_queue=sum(1 for row in rows if _has_queue(row, "transfer_pricing_queue")),
        scenarios_requiring_sector_schedule_queue=sum(1 for row in rows if _has_queue(row, "sector_schedule_queue")),
        scenarios_requiring_aava_review_queue=sum(1 for row in rows if _has_queue(row, "aava_review_queue")),
        scenarios_requiring_capital_base_review_queue=sum(1 for row in rows if _has_queue(row, "capital_base_review_queue")),
        scenarios_requiring_offshore_attribution_queue=sum(1 for row in rows if _has_queue(row, "offshore_attribution_queue")),
        scenarios_requiring_privacy_review_queue=sum(1 for row in rows if _has_queue(row, "privacy_review_queue")),
        scenarios_requiring_legal_policy_queue=sum(1 for row in rows if _has_queue(row, "legal_policy_queue")),
        scenarios_requiring_ato_methods_queue=sum(1 for row in rows if _has_queue(row, "ato_methods_queue")),
        scenarios_requiring_treasury_methods_queue=sum(1 for row in rows if _has_queue(row, "treasury_methods_queue")),
        firm_level_liability_logic_modified=False,
        real_enforcement_created=False,
        real_ato_power_claimed=False,
        compliance_scoring_created=False,
        notices_issued=False,
        real_data_used=False,
        calibration_blockers=blockers,
        warnings=[
            "Summary counts are deterministic prototype workflow counts only.",
            "Counts are not operational priorities, audit logic, or compliance scoring.",
        ],
    )
