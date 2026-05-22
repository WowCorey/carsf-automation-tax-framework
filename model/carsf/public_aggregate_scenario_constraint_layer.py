"""Public aggregate scenario constraint layer for Build 34.

This module constrains scenario outputs using the Build 33 public aggregate
calibration-boundary map. It does not load new data, perform calibration,
validate CARSF, determine tax payable, or modify firm-level CARSF liability
logic.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


SCENARIO_OUTPUT_STATUS_VALUES = {
    "display_as_sanity_check_only",
    "display_as_public_aggregate_anchor_only",
    "display_as_public_aggregate_bound_only",
    "display_as_context_only",
    "display_as_placeholder_narrowing_only",
    "display_as_reviewer_traceability_only",
    "mark_non_interpretable",
    "hide_from_reviewer_dashboard",
    "fail_closed_forbidden_claim",
}

DISPLAY_RULE_VALUES = {
    "show_with_non_claim_warning",
    "show_as_boundary_only",
    "show_as_context_only",
    "show_as_traceability_only",
    "show_placeholder_only",
    "show_blocked",
    "hide",
    "fail_closed",
}

FORBIDDEN_IMPLICATION_VALUES = {
    "calibration_completed",
    "statistical_validation",
    "model_validation",
    "causal_inference",
    "actual_tax_payable",
    "firm_liability_determination",
    "taxpayer_behaviour_estimate",
    "household_population_estimate",
    "official_policy_status",
    "legal_sufficiency",
    "implementation_readiness",
    "treasury_modelling",
    "ato_guidance",
    "pbo_costing",
    "compliance_scoring",
    "readiness_scoring",
    "maturity_scoring",
}

CONSTRAINT_STATUS_VALUES = {
    "compliant_boundary_output",
    "warning_boundary_limited",
    "non_interpretable",
    "hidden_for_reviewer_safety",
    "fail_closed",
}

CLAIM_LEVEL_VALUES = {
    "scenario_sanity_check_only",
    "scenario_public_anchor_only",
    "scenario_public_bound_only",
    "scenario_context_only",
    "scenario_placeholder_narrowing_only",
    "scenario_traceability_only",
    "scenario_non_interpretable",
    "no_scenario_claim_allowed",
}

SCENARIO_CONSTRAINT_WARNING = (
    "This is a public aggregate scenario constraint layer only. No new data is loaded by this build. Scenario "
    "constraints do not calibrate the model and do not validate the model. Public aggregate data can only appear "
    "as sanity checks, anchors, bounds, context, placeholder narrowing, or reviewer traceability. Public aggregate "
    "data does not prove the model works. Outputs marked non-interpretable are not usable as evidence. Hidden "
    "outputs are hidden to prevent overclaiming. Source candidates not loaded remain not loaded. Restricted-data "
    "blockers remain blockers. This is not validation, not legal advice, not tax advice, not ATO guidance, not "
    "Treasury modelling, not PBO costing, not economic validation, not welfare validation, not statistical "
    "validation, not operational readiness, not legal sufficiency, and not official status. It does not determine "
    "actual tax payable and does not modify firm-level CARSF liability."
)

SCENARIO_CONSTRAINT_NON_CLAIMS = [
    SCENARIO_CONSTRAINT_WARNING,
    "Build 34 uses existing Build 31 public aggregate values, Build 32 placeholder decisions, and Build 33 boundary decisions only.",
    "Scenario output labels are display constraints only; they are not calibration, validation, legal sufficiency, official status, readiness, or liability determinations.",
    "Outputs marked non-interpretable or hidden remain unavailable as reviewer-facing evidence until required data and reviews exist.",
]

FORBIDDEN_AFFIRMATIVE_SCENARIO_CONSTRAINT_CLAIMS = [
    "calibrated",
    "calibration completed",
    "model works",
    "public data proves",
    "actual tax payable",
    "validated",
    "externally validated",
    "source verified",
    "official policy",
    "official status",
    "ready for government",
    "ready for ato",
    "ready for treasury",
    "ready for parliament",
    "ready for implementation",
    "operationally ready",
    "legally sufficient",
    "treasury modelling",
    "pbo costing",
    "ato guidance",
    "economic validation complete",
    "welfare validation complete",
    "statistical validation complete",
    "readiness score",
    "maturity score",
    "approved",
    "representative estimate",
    "population estimate",
    "firm liability",
    "carsf liability determined",
    "calibrated scenario",
    "scenario validated",
    "scenario proves",
    "implementation ready",
    "compliance score",
    "enforcement score",
]

NEGATIVE_CONTEXT_MARKERS = [
    "not ",
    "not a ",
    "not an ",
    "not_",
    "no ",
    "does not ",
    "do not ",
    "must not ",
    "must_not",
    "without ",
    "is not ",
    "are not ",
    "has not ",
    "have not ",
    "cannot ",
    "non-claim",
    "forbidden",
    "blocked",
    "boundary",
    "constraint",
    "hidden",
    "non-interpretable",
    "fail_closed",
    "does_not_show",
    "must_not_infer",
    "not_used_for",
    "blocked_display_outputs",
    "forbidden_implications",
    "what_must_be_hidden_or_marked_non_interpretable",
    "what this layer does not mean",
    "does not mean",
]


@dataclass(frozen=True)
class ScenarioOutputConstraint:
    output_id: str
    source_id: str
    scenario_output_status: str
    display_rule: str
    constraint_status: str
    claim_level: str
    forbidden_implications: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ModuleScenarioConstraint:
    constraint_id: str
    module_id: str
    module_name: str
    linked_boundary_decision_id: str
    linked_placeholder_decision_ids: list[str]
    linked_public_value_ids: list[str]
    scenario_output_status: str
    display_rule: str
    constraint_status: str
    claim_level: str
    allowed_display_outputs: list[str]
    blocked_display_outputs: list[str]
    forbidden_implications: list[str]
    what_can_be_displayed: str
    what_must_be_hidden_or_marked_non_interpretable: str
    reviewer_warning: str
    evidence_needed_to_lift_constraint: list[str]
    requires_restricted_data: bool
    requires_legal_review: bool
    requires_tax_review: bool
    requires_economic_review: bool
    requires_statistical_review: bool
    requires_external_review: bool
    safe_for_repo_use: bool
    calibration_completed: bool
    validation_claimed: bool
    actual_tax_payable_determined: bool
    official_status_claimed: bool
    firm_level_liability_logic_modified: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FieldScenarioConstraint:
    constraint_id: str
    field_id: str
    placeholder_id: str
    linked_boundary_decision_id: str
    linked_placeholder_decision_ids: list[str]
    linked_public_value_ids: list[str]
    scenario_output_status: str
    display_rule: str
    constraint_status: str
    claim_level: str
    allowed_display_outputs: list[str]
    blocked_display_outputs: list[str]
    forbidden_implications: list[str]
    reviewer_warning: str
    evidence_needed_to_lift_constraint: list[str]
    calibration_completed: bool
    validation_claimed: bool
    actual_tax_payable_determined: bool
    firm_level_liability_logic_modified: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ForbiddenScenarioImplication:
    implication_id: str
    implication: str
    constraint_action: str
    reviewer_warning: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ScenarioDisplayRule:
    rule_id: str
    scenario_output_status: str
    display_rule: str
    explanation: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ScenarioConstraintSummary:
    public_aggregate_scenario_constraint_layer_created: bool
    new_data_loaded: bool
    loaded_public_values_used: int
    module_constraints_mapped: int
    field_constraints_mapped: int
    outputs_display_as_sanity_check_only: int
    outputs_display_as_public_anchor_only: int
    outputs_display_as_public_bound_only: int
    outputs_display_as_context_only: int
    outputs_display_as_placeholder_narrowing_only: int
    outputs_display_as_reviewer_traceability_only: int
    outputs_marked_non_interpretable: int
    outputs_hidden_from_reviewer_dashboard: int
    outputs_fail_closed_forbidden_claim: int
    forbidden_implications_mapped: int
    public_source_candidates_treated_as_loaded: bool
    restricted_data_loaded: bool
    personal_data_loaded: bool
    taxpayer_level_data_loaded: bool
    firm_confidential_data_loaded: bool
    household_microdata_loaded: bool
    calibration_completed: bool
    validation_claimed: bool
    actual_tax_payable_determined: bool
    official_status_claimed: bool
    firm_level_liability_logic_modified: bool
    forbidden_claim_findings: int

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicAggregateScenarioConstraintResult:
    constraint_layer_id: str
    constraint_layer_name: str
    status: str
    non_claims: list[str]
    public_aggregate_values: list[dict[str, Any]]
    module_scenario_constraints: list[ModuleScenarioConstraint]
    field_scenario_constraints: list[FieldScenarioConstraint]
    scenario_output_constraints: list[ScenarioOutputConstraint]
    forbidden_scenario_implications: list[ForbiddenScenarioImplication]
    dashboard_display_rules: list[ScenarioDisplayRule]
    source_candidates_not_loaded: list[dict[str, Any]]
    future_build_35_requirements: list[str]
    summary: ScenarioConstraintSummary

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _required_mapping(source: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [field for field in fields if field not in source]
    if missing:
        raise ValueError(f"{label} missing required fields: {', '.join(missing)}")


def _non_empty(value: Any, field: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field} must be non-empty")
    return text


def _bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field} must be boolean")
    return value


def _choice(value: str, allowed: set[str], field: str) -> str:
    if value not in allowed:
        raise ValueError(f"{field} has invalid value {value!r}; expected one of {sorted(allowed)}")
    return value


def _list_of_strings(value: Any, field: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{field} must be a list of strings")
    if not allow_empty and not value:
        raise ValueError(f"{field} must be non-empty")
    return [item.strip() for item in value]


def _is_negative_context(text: str, phrase_start: int) -> bool:
    window = text[max(0, phrase_start - 240) : phrase_start].lower()
    return any(marker in window for marker in NEGATIVE_CONTEXT_MARKERS)


def find_forbidden_affirmative_scenario_constraint_claims(text: str) -> list[str]:
    lowered = text.lower()
    findings: list[str] = []
    for phrase in FORBIDDEN_AFFIRMATIVE_SCENARIO_CONSTRAINT_CLAIMS:
        start = 0
        while True:
            index = lowered.find(phrase, start)
            if index == -1:
                break
            if not _is_negative_context(lowered, index):
                findings.append(phrase)
                break
            start = index + len(phrase)
    return sorted(set(findings))


def _public_values(public_values_payload: dict[str, Any]) -> list[dict[str, Any]]:
    values = public_values_payload.get("values", [])
    if not isinstance(values, list) or not values:
        raise ValueError("Build 31 public aggregate values must be present")
    output: list[dict[str, Any]] = []
    for item in values:
        if not isinstance(item, dict):
            raise ValueError("public aggregate values must be mappings")
        _required_mapping(
            item,
            [
                "value_id",
                "source_id",
                "metric_name",
                "value",
                "unit",
                "period",
                "geography",
                "data_status",
                "claim_level",
                "public_aggregate_only",
                "restricted_data",
                "personal_data",
                "safe_for_repo_use",
            ],
            "public aggregate value",
        )
        if item["data_status"] != "loaded_public_aggregate":
            raise ValueError(f"public value is not loaded_public_aggregate: {item['value_id']}")
        if item["claim_level"] != "real_public_aggregate_data":
            raise ValueError(f"public value has unexpected claim_level: {item['value_id']}")
        if not _bool(item["public_aggregate_only"], "public_aggregate_only"):
            raise ValueError(f"public value is not aggregate-only: {item['value_id']}")
        if _bool(item["restricted_data"], "restricted_data") or _bool(item["personal_data"], "personal_data"):
            raise ValueError(f"public value fails privacy guardrails: {item['value_id']}")
        if item.get("taxpayer_level_data", False) or item.get("firm_confidential_data", False) or item.get("household_microdata", False):
            raise ValueError(f"public value includes forbidden data flags: {item['value_id']}")
        if not _bool(item["safe_for_repo_use"], "safe_for_repo_use"):
            raise ValueError(f"public value is not safe for repo use: {item['value_id']}")
        output.append(dict(item))
    return output


def _source_candidates_not_loaded(source_manifest: dict[str, Any]) -> list[dict[str, Any]]:
    sources = source_manifest.get("sources", [])
    if not isinstance(sources, list):
        raise ValueError("public real data source manifest sources must be a list")
    candidates: list[dict[str, Any]] = []
    for source in sources:
        if source.get("loaded_status") == "source_candidate_not_loaded":
            candidates.append(
                {
                    "source_id": source["source_id"],
                    "publisher": source["publisher"],
                    "source_name": source["source_name"],
                    "loaded_status": source["loaded_status"],
                    "reason_if_not_loaded": source.get("reason_if_not_loaded", ""),
                    "treated_as_loaded": False,
                }
            )
    return candidates


def _replacement_decision_map(replacement_report: dict[str, Any]) -> dict[str, str]:
    payload = replacement_report.get("public_data_placeholder_replacement_map", {})
    decisions = payload.get("replacement_decisions", [])
    if not isinstance(decisions, list) or not decisions:
        raise ValueError("Build 32 placeholder replacement decisions must be present")
    return {item["placeholder_id"]: item["decision_id"] for item in decisions}


def _boundary_payload(boundary_report: dict[str, Any]) -> dict[str, Any]:
    payload = boundary_report.get("public_aggregate_calibration_boundary_map", {})
    if not isinstance(payload, dict) or not payload:
        raise ValueError("Build 33 calibration-boundary map payload must be present")
    return payload


def _module_boundaries(boundary_report: dict[str, Any]) -> list[dict[str, Any]]:
    boundaries = _boundary_payload(boundary_report).get("module_boundary_decisions", [])
    if not isinstance(boundaries, list) or not boundaries:
        raise ValueError("Build 33 module boundary decisions must be present")
    return boundaries


def _field_boundaries(boundary_report: dict[str, Any]) -> list[dict[str, Any]]:
    boundaries = _boundary_payload(boundary_report).get("field_boundary_decisions", [])
    if not isinstance(boundaries, list) or not boundaries:
        raise ValueError("Build 33 field boundary decisions must be present")
    return boundaries


def _status_profile(module_id: str) -> dict[str, Any]:
    profiles: dict[str, dict[str, Any]] = {
        "opfte_benchmark_module": {
            "status": "display_as_public_aggregate_anchor_only",
            "rule": "show_as_boundary_only",
            "constraint": "warning_boundary_limited",
            "claim": "scenario_public_anchor_only",
            "allowed": ["Fair Work public wage anchors", "visible sanity checks", "public aggregate wage bounds"],
            "blocked": ["OPFTE calibration", "representative labour-cost estimate", "firm liability determination", "actual tax payable"],
            "extra_forbidden": [],
        },
        "hle_assumptions_module": {
            "status": "display_as_public_aggregate_bound_only",
            "rule": "show_as_boundary_only",
            "constraint": "warning_boundary_limited",
            "claim": "scenario_public_bound_only",
            "allowed": ["wage boundary display", "placeholder narrowing display"],
            "blocked": ["representative labour-cost estimate", "occupation-specific wage model", "automation substitution calibration"],
            "extra_forbidden": [],
        },
        "qlc_weights_module": {
            "status": "display_as_placeholder_narrowing_only",
            "rule": "show_placeholder_only",
            "constraint": "warning_boundary_limited",
            "claim": "scenario_placeholder_narrowing_only",
            "allowed": ["placeholder narrowing display", "wage-threshold context"],
            "blocked": ["QLC calibration", "labour-quality validation", "legal attribution"],
            "extra_forbidden": [],
        },
        "fiscal_trajectory_assumptions": {
            "status": "display_as_public_aggregate_bound_only",
            "rule": "show_as_boundary_only",
            "constraint": "warning_boundary_limited",
            "claim": "scenario_public_bound_only",
            "allowed": ["fiscal context", "public aggregate fiscal bounds"],
            "blocked": ["Treasury modelling", "PBO costing", "fiscal sufficiency", "CARSF revenue estimate"],
            "extra_forbidden": ["treasury_modelling", "pbo_costing"],
        },
        "payg_erosion_assumptions": {
            "status": "mark_non_interpretable",
            "rule": "show_blocked",
            "constraint": "non_interpretable",
            "claim": "scenario_non_interpretable",
            "allowed": ["tax aggregate context only"],
            "blocked": ["PAYG erosion calibration", "taxpayer behaviour estimate", "CARSF revenue estimate"],
            "extra_forbidden": [],
        },
        "transition_funding_assumptions": {
            "status": "display_as_context_only",
            "rule": "show_as_context_only",
            "constraint": "warning_boundary_limited",
            "claim": "scenario_context_only",
            "allowed": ["transition funding scale context", "public aggregate fiscal bounds"],
            "blocked": ["fiscal sufficiency", "welfare impact estimate", "policy implementation readiness"],
            "extra_forbidden": [],
        },
        "superannuation_contribution_pressure": {
            "status": "display_as_public_aggregate_anchor_only",
            "rule": "show_as_boundary_only",
            "constraint": "warning_boundary_limited",
            "claim": "scenario_public_anchor_only",
            "allowed": ["public contribution-rate anchor", "payment interaction context"],
            "blocked": ["individual super estimate", "employer behaviour estimate", "payroll estimate", "ATO guidance claim"],
            "extra_forbidden": ["ato_guidance"],
        },
        "sector_schedule_values": {
            "status": "display_as_context_only",
            "rule": "show_as_context_only",
            "constraint": "warning_boundary_limited",
            "claim": "scenario_context_only",
            "allowed": ["sector schedule context", "reviewer traceability"],
            "blocked": ["official sector ranking", "schedule calibration", "legal attribution"],
            "extra_forbidden": [],
        },
        "sector_stress_matrix": {
            "status": "display_as_sanity_check_only",
            "rule": "show_with_non_claim_warning",
            "constraint": "warning_boundary_limited",
            "claim": "scenario_sanity_check_only",
            "allowed": ["stress assumption sanity checks", "public aggregate context"],
            "blocked": ["validated sector stress", "official sector ranking", "population estimate"],
            "extra_forbidden": [],
        },
        "behavioural_response_gaming_simulation": {
            "status": "mark_non_interpretable",
            "rule": "show_blocked",
            "constraint": "non_interpretable",
            "claim": "scenario_non_interpretable",
            "allowed": ["context only", "blocked warning"],
            "blocked": ["behavioural elasticity", "avoidance estimate", "gaming prediction", "causal response"],
            "extra_forbidden": [],
        },
        "administrative_compliance_workflow": {
            "status": "display_as_reviewer_traceability_only",
            "rule": "show_as_traceability_only",
            "constraint": "warning_boundary_limited",
            "claim": "scenario_traceability_only",
            "allowed": ["traceability and pathway concept only"],
            "blocked": ["ATO workflow", "compliance scoring", "enforcement", "notices", "operational readiness"],
            "extra_forbidden": ["ato_guidance", "compliance_scoring"],
        },
        "legislative_architecture_skeleton": {
            "status": "display_as_reviewer_traceability_only",
            "rule": "show_as_traceability_only",
            "constraint": "warning_boundary_limited",
            "claim": "scenario_traceability_only",
            "allowed": ["non-operative architecture traceability"],
            "blocked": ["operative law", "legal sufficiency", "drafting readiness", "official policy"],
            "extra_forbidden": [],
        },
        "household_distributional_scenarios": {
            "status": "hide_from_reviewer_dashboard",
            "rule": "hide",
            "constraint": "hidden_for_reviewer_safety",
            "claim": "no_scenario_claim_allowed",
            "allowed": ["synthetic placeholder context only"],
            "blocked": ["real household estimate", "population estimate", "welfare impact estimate", "distributional calibration"],
            "extra_forbidden": ["household_population_estimate"],
        },
        "household_weighting": {
            "status": "mark_non_interpretable",
            "rule": "show_blocked",
            "constraint": "non_interpretable",
            "claim": "scenario_non_interpretable",
            "allowed": ["synthetic placeholder context only"],
            "blocked": ["representative weighting", "population estimate", "household distributional estimate"],
            "extra_forbidden": ["household_population_estimate"],
        },
        "uncertainty_ranges": {
            "status": "display_as_context_only",
            "rule": "show_as_context_only",
            "constraint": "warning_boundary_limited",
            "claim": "scenario_context_only",
            "allowed": ["uncertainty label context", "blocked evidence traceability"],
            "blocked": ["real uncertainty quantification", "confidence interval", "statistical estimation"],
            "extra_forbidden": ["statistical_validation"],
        },
        "reviewed_scenario_comparison_layer": {
            "status": "display_as_reviewer_traceability_only",
            "rule": "show_as_traceability_only",
            "constraint": "warning_boundary_limited",
            "claim": "scenario_traceability_only",
            "allowed": ["reviewer-facing comparison labels", "non-claim warnings"],
            "blocked": ["policy ranking", "validation ranking", "implementation recommendation"],
            "extra_forbidden": [],
        },
        "executive_dashboard_consolidation": {
            "status": "display_as_reviewer_traceability_only",
            "rule": "show_as_traceability_only",
            "constraint": "warning_boundary_limited",
            "claim": "scenario_traceability_only",
            "allowed": ["boundary labels", "non-claim warnings", "source traceability"],
            "blocked": ["readiness scoring", "calibration scoring", "validation scoring", "tax payable estimate", "liability estimate"],
            "extra_forbidden": ["readiness_scoring", "maturity_scoring"],
        },
        "public_data_evidence_map": {
            "status": "display_as_reviewer_traceability_only",
            "rule": "show_as_traceability_only",
            "constraint": "compliant_boundary_output",
            "claim": "scenario_traceability_only",
            "allowed": ["evidence map traceability", "source-reference labels"],
            "blocked": ["validation evidence", "calibration evidence", "policy readiness evidence"],
            "extra_forbidden": [],
        },
        "public_data_placeholder_replacement_map": {
            "status": "display_as_placeholder_narrowing_only",
            "rule": "show_placeholder_only",
            "constraint": "warning_boundary_limited",
            "claim": "scenario_placeholder_narrowing_only",
            "allowed": ["placeholder replacement labels", "placeholder narrowing labels", "context labels"],
            "blocked": ["calibration replacement", "validation replacement", "liability replacement"],
            "extra_forbidden": [],
        },
    }
    return profiles[module_id]


def _fallback_forbidden(boundary: dict[str, Any], extra_forbidden: list[str]) -> list[str]:
    values = set(_list_of_strings(boundary.get("forbidden_use_types", []), "forbidden_use_types"))
    values.update(extra_forbidden)
    values.update(["treasury_modelling", "ato_guidance", "pbo_costing"])
    return sorted(_choice(item, FORBIDDEN_IMPLICATION_VALUES, "forbidden_implications") for item in values)


def _placeholder_decision_ids(placeholder_ids: list[str], replacement_ids: dict[str, str]) -> list[str]:
    output: list[str] = []
    for placeholder_id in placeholder_ids:
        if placeholder_id in replacement_ids:
            output.append(replacement_ids[placeholder_id])
    return output


def _module_constraint(boundary: dict[str, Any], replacement_ids: dict[str, str]) -> ModuleScenarioConstraint:
    module_id = _non_empty(boundary["module_id"], "module_id")
    profile = _status_profile(module_id)
    scenario_status = _choice(profile["status"], SCENARIO_OUTPUT_STATUS_VALUES, "scenario_output_status")
    display_rule = _choice(profile["rule"], DISPLAY_RULE_VALUES, "display_rule")
    constraint_status = _choice(profile["constraint"], CONSTRAINT_STATUS_VALUES, "constraint_status")
    claim_level = _choice(profile["claim"], CLAIM_LEVEL_VALUES, "claim_level")
    placeholder_ids = _list_of_strings(boundary.get("related_placeholder_ids", []), "related_placeholder_ids", allow_empty=True)
    forbidden = _fallback_forbidden(boundary, profile["extra_forbidden"])
    return ModuleScenarioConstraint(
        constraint_id=f"scenario_constraint_{module_id}",
        module_id=module_id,
        module_name=_non_empty(boundary["module_name"], "module_name"),
        linked_boundary_decision_id=_non_empty(boundary["decision_id"], "linked_boundary_decision_id"),
        linked_placeholder_decision_ids=_placeholder_decision_ids(placeholder_ids, replacement_ids),
        linked_public_value_ids=_list_of_strings(boundary.get("linked_public_value_ids", []), "linked_public_value_ids", allow_empty=True),
        scenario_output_status=scenario_status,
        display_rule=display_rule,
        constraint_status=constraint_status,
        claim_level=claim_level,
        allowed_display_outputs=_list_of_strings(profile["allowed"], "allowed_display_outputs"),
        blocked_display_outputs=_list_of_strings(profile["blocked"], "blocked_display_outputs"),
        forbidden_implications=forbidden,
        what_can_be_displayed=f"{boundary['module_name']} may display {', '.join(profile['allowed'])} only with non-claim warnings.",
        what_must_be_hidden_or_marked_non_interpretable=(
            f"{boundary['module_name']} must hide or mark non-interpretable any output implying "
            f"{', '.join(profile['blocked'])}."
        ),
        reviewer_warning=(
            "Scenario display is boundary-limited only; it is not calibration, validation, tax payable evidence, "
            "legal sufficiency, official status, implementation readiness, or firm-level CARSF liability."
        ),
        evidence_needed_to_lift_constraint=_list_of_strings(
            boundary.get("evidence_needed_before_calibration", []),
            "evidence_needed_to_lift_constraint",
        ),
        requires_restricted_data=_bool(boundary["requires_restricted_data"], "requires_restricted_data"),
        requires_legal_review=_bool(boundary["requires_legal_review"], "requires_legal_review"),
        requires_tax_review=_bool(boundary["requires_tax_review"], "requires_tax_review"),
        requires_economic_review=_bool(boundary["requires_economic_review"], "requires_economic_review"),
        requires_statistical_review=_bool(boundary["requires_statistical_review"], "requires_statistical_review"),
        requires_external_review=_bool(boundary["requires_external_review"], "requires_external_review"),
        safe_for_repo_use=_bool(boundary["safe_for_repo_use"], "safe_for_repo_use"),
        calibration_completed=False,
        validation_claimed=False,
        actual_tax_payable_determined=False,
        official_status_claimed=False,
        firm_level_liability_logic_modified=False,
    )


def _boundary_map_self_constraint(public_value_ids: list[str]) -> ModuleScenarioConstraint:
    return ModuleScenarioConstraint(
        constraint_id="scenario_constraint_public_aggregate_calibration_boundary_map",
        module_id="public_aggregate_calibration_boundary_map",
        module_name="Public aggregate calibration boundary map",
        linked_boundary_decision_id="public_aggregate_calibration_boundary_map_report",
        linked_placeholder_decision_ids=[],
        linked_public_value_ids=public_value_ids,
        scenario_output_status="display_as_reviewer_traceability_only",
        display_rule="show_as_traceability_only",
        constraint_status="compliant_boundary_output",
        claim_level="scenario_traceability_only",
        allowed_display_outputs=["boundary labels", "allowed-use labels", "forbidden-use labels", "reviewer traceability"],
        blocked_display_outputs=["calibration boundary satisfaction", "validation evidence", "implementation recommendation"],
        forbidden_implications=sorted(FORBIDDEN_IMPLICATION_VALUES),
        what_can_be_displayed="The boundary map may display allowed-use labels, forbidden-use labels, blockers, and reviewer traceability.",
        what_must_be_hidden_or_marked_non_interpretable=(
            "The boundary map must hide or mark non-interpretable any output implying calibration satisfaction, "
            "validation, legal sufficiency, official status, implementation readiness, tax payable, or firm liability."
        ),
        reviewer_warning=(
            "Boundary-map display is traceability only; it is not calibration, validation, legal sufficiency, "
            "official status, implementation readiness, or firm-level CARSF liability."
        ),
        evidence_needed_to_lift_constraint=["restricted data governance", "legal review", "economic review", "statistical review", "external domain review"],
        requires_restricted_data=True,
        requires_legal_review=True,
        requires_tax_review=True,
        requires_economic_review=True,
        requires_statistical_review=True,
        requires_external_review=True,
        safe_for_repo_use=True,
        calibration_completed=False,
        validation_claimed=False,
        actual_tax_payable_determined=False,
        official_status_claimed=False,
        firm_level_liability_logic_modified=False,
    )


def _field_status_from_boundary(boundary: dict[str, Any]) -> tuple[str, str, str, str]:
    allowed = set(boundary.get("allowed_use_types", []))
    boundary_status = boundary.get("boundary_status")
    if boundary_status == "requires_restricted_data":
        return "mark_non_interpretable", "show_blocked", "non_interpretable", "scenario_non_interpretable"
    if boundary_status == "requires_external_review":
        return "display_as_reviewer_traceability_only", "show_as_traceability_only", "warning_boundary_limited", "scenario_traceability_only"
    if "public_aggregate_anchor_only" in allowed:
        return "display_as_public_aggregate_anchor_only", "show_as_boundary_only", "warning_boundary_limited", "scenario_public_anchor_only"
    if "public_aggregate_bound_only" in allowed:
        return "display_as_public_aggregate_bound_only", "show_as_boundary_only", "warning_boundary_limited", "scenario_public_bound_only"
    if "placeholder_narrowing_only" in allowed:
        return "display_as_placeholder_narrowing_only", "show_placeholder_only", "warning_boundary_limited", "scenario_placeholder_narrowing_only"
    return "display_as_context_only", "show_as_context_only", "warning_boundary_limited", "scenario_context_only"


def _field_constraint(boundary: dict[str, Any], replacement_ids: dict[str, str]) -> FieldScenarioConstraint:
    scenario_status, display_rule, constraint_status, claim_level = _field_status_from_boundary(boundary)
    placeholder_id = _non_empty(boundary["placeholder_id"], "placeholder_id")
    forbidden = _fallback_forbidden(boundary, [])
    return FieldScenarioConstraint(
        constraint_id=f"field_scenario_constraint_{placeholder_id}",
        field_id=_non_empty(boundary["field_id"], "field_id"),
        placeholder_id=placeholder_id,
        linked_boundary_decision_id=_non_empty(boundary["decision_id"], "linked_boundary_decision_id"),
        linked_placeholder_decision_ids=_placeholder_decision_ids([placeholder_id], replacement_ids),
        linked_public_value_ids=_list_of_strings(boundary.get("linked_public_value_ids", []), "linked_public_value_ids", allow_empty=True),
        scenario_output_status=scenario_status,
        display_rule=display_rule,
        constraint_status=constraint_status,
        claim_level=claim_level,
        allowed_display_outputs=["field boundary label", "linked public value traceability", "placeholder status"],
        blocked_display_outputs=["calibration", "validation", "actual tax payable", "firm liability determination"],
        forbidden_implications=forbidden,
        reviewer_warning=(
            "Field scenario output is constrained to boundary display only; it is not calibration, validation, "
            "tax payable evidence, official status, or firm-level CARSF liability."
        ),
        evidence_needed_to_lift_constraint=_list_of_strings(
            boundary.get("evidence_needed_before_calibration", []),
            "evidence_needed_to_lift_constraint",
        ),
        calibration_completed=False,
        validation_claimed=False,
        actual_tax_payable_determined=False,
        firm_level_liability_logic_modified=False,
    )


def _display_rules() -> list[ScenarioDisplayRule]:
    explanations = {
        "display_as_sanity_check_only": ("show_with_non_claim_warning", "Show only as a sanity-check output with visible non-claim warning."),
        "display_as_public_aggregate_anchor_only": ("show_as_boundary_only", "Show only as a public aggregate anchor or boundary output."),
        "display_as_public_aggregate_bound_only": ("show_as_boundary_only", "Show only as a public aggregate bound or boundary output."),
        "display_as_context_only": ("show_as_context_only", "Show only as contextual public aggregate reference."),
        "display_as_placeholder_narrowing_only": ("show_placeholder_only", "Show only as placeholder narrowing or placeholder-status context."),
        "display_as_reviewer_traceability_only": ("show_as_traceability_only", "Show only as source, boundary, or reviewer traceability."),
        "mark_non_interpretable": ("show_blocked", "Show blocked or non-interpretable label instead of reviewer-facing scenario evidence."),
        "hide_from_reviewer_dashboard": ("hide", "Hide from reviewer dashboard to prevent overclaiming."),
        "fail_closed_forbidden_claim": ("fail_closed", "Fail closed if the scenario output contains a forbidden implication."),
    }
    return [
        ScenarioDisplayRule(
            rule_id=f"display_rule_{status}",
            scenario_output_status=status,
            display_rule=rule,
            explanation=explanation,
        )
        for status, (rule, explanation) in sorted(explanations.items())
    ]


def _scenario_output_constraints(module_constraints: list[ModuleScenarioConstraint]) -> list[ScenarioOutputConstraint]:
    return [
        ScenarioOutputConstraint(
            output_id=f"output_{item.module_id}",
            source_id=item.module_id,
            scenario_output_status=item.scenario_output_status,
            display_rule=item.display_rule,
            constraint_status=item.constraint_status,
            claim_level=item.claim_level,
            forbidden_implications=item.forbidden_implications,
        )
        for item in module_constraints
    ]


def _forbidden_implications() -> list[ForbiddenScenarioImplication]:
    return [
        ForbiddenScenarioImplication(
            implication_id=f"forbidden_{item}",
            implication=item,
            constraint_action="flag_hide_downgrade_or_mark_non_interpretable",
            reviewer_warning=f"Scenario output must not imply {item}; if it does, the layer must fail closed or hide the output.",
        )
        for item in sorted(FORBIDDEN_IMPLICATION_VALUES)
    ]


def _validate_constraint(item: ModuleScenarioConstraint | FieldScenarioConstraint) -> None:
    _choice(item.scenario_output_status, SCENARIO_OUTPUT_STATUS_VALUES, "scenario_output_status")
    _choice(item.display_rule, DISPLAY_RULE_VALUES, "display_rule")
    _choice(item.constraint_status, CONSTRAINT_STATUS_VALUES, "constraint_status")
    _choice(item.claim_level, CLAIM_LEVEL_VALUES, "claim_level")
    _list_of_strings(item.allowed_display_outputs, "allowed_display_outputs")
    _list_of_strings(item.blocked_display_outputs, "blocked_display_outputs")
    _list_of_strings(item.forbidden_implications, "forbidden_implications")
    _list_of_strings(item.evidence_needed_to_lift_constraint, "evidence_needed_to_lift_constraint")
    if item.calibration_completed or item.validation_claimed or item.actual_tax_payable_determined:
        raise ValueError(f"scenario constraint has forbidden true flag: {item.constraint_id}")
    if item.firm_level_liability_logic_modified:
        raise ValueError(f"scenario constraint modifies firm-level liability logic: {item.constraint_id}")
    if isinstance(item, ModuleScenarioConstraint) and item.official_status_claimed:
        raise ValueError(f"scenario constraint claims official status: {item.constraint_id}")


def build_public_aggregate_scenario_constraint_result(
    manifest: dict[str, Any],
    public_values_payload: dict[str, Any],
    source_manifest: dict[str, Any],
    replacement_report: dict[str, Any],
    boundary_report: dict[str, Any],
) -> PublicAggregateScenarioConstraintResult:
    _required_mapping(
        manifest,
        [
            "constraint_layer_id",
            "constraint_layer_name",
            "status",
            "non_claims",
            "input_artifacts",
            "scenario_output_status_taxonomy",
            "display_rule_taxonomy",
            "forbidden_implication_taxonomy",
            "constraint_status_taxonomy",
            "claim_level_taxonomy",
            "required_module_constraints",
            "required_field_constraints",
            "required_dashboard_rules",
            "forbidden_claims",
            "build_35_requirements",
        ],
        "scenario constraint manifest",
    )
    if set(_list_of_strings(manifest["scenario_output_status_taxonomy"], "scenario_output_status_taxonomy")) != SCENARIO_OUTPUT_STATUS_VALUES:
        raise ValueError("scenario output status taxonomy mismatch")
    if set(_list_of_strings(manifest["display_rule_taxonomy"], "display_rule_taxonomy")) != DISPLAY_RULE_VALUES:
        raise ValueError("display rule taxonomy mismatch")
    if set(_list_of_strings(manifest["forbidden_implication_taxonomy"], "forbidden_implication_taxonomy")) != FORBIDDEN_IMPLICATION_VALUES:
        raise ValueError("forbidden implication taxonomy mismatch")
    if set(_list_of_strings(manifest["constraint_status_taxonomy"], "constraint_status_taxonomy")) != CONSTRAINT_STATUS_VALUES:
        raise ValueError("constraint status taxonomy mismatch")
    if set(_list_of_strings(manifest["claim_level_taxonomy"], "claim_level_taxonomy")) != CLAIM_LEVEL_VALUES:
        raise ValueError("claim level taxonomy mismatch")

    public_values = _public_values(public_values_payload)
    public_value_ids = sorted(item["value_id"] for item in public_values)
    replacement_ids = _replacement_decision_map(replacement_report)
    boundary_modules = _module_boundaries(boundary_report)
    boundary_fields = _field_boundaries(boundary_report)

    boundary_module_ids = {item["module_id"] for item in boundary_modules}
    expected_from_boundary = set(boundary_module_ids) | {"public_aggregate_calibration_boundary_map"}
    required_modules = set(_list_of_strings(manifest["required_module_constraints"], "required_module_constraints"))
    if expected_from_boundary != required_modules:
        raise ValueError(
            "module scenario constraint coverage mismatch; "
            f"missing={sorted(required_modules - expected_from_boundary)}; extra={sorted(expected_from_boundary - required_modules)}"
        )

    required_fields = set(_list_of_strings(manifest["required_field_constraints"], "required_field_constraints"))
    field_ids = {item["placeholder_id"] for item in boundary_fields}
    if required_fields != field_ids:
        raise ValueError(f"field scenario constraint coverage mismatch; missing={sorted(required_fields - field_ids)}; extra={sorted(field_ids - required_fields)}")

    module_constraints = [_module_constraint(item, replacement_ids) for item in sorted(boundary_modules, key=lambda row: row["module_id"])]
    module_constraints.append(_boundary_map_self_constraint(public_value_ids))
    field_constraints = [_field_constraint(item, replacement_ids) for item in sorted(boundary_fields, key=lambda row: row["placeholder_id"])]
    for item in module_constraints:
        _validate_constraint(item)
    for item in field_constraints:
        _validate_constraint(item)

    source_candidates = _source_candidates_not_loaded(source_manifest)
    candidate_source_ids = {item["source_id"] for item in source_candidates}
    loaded_source_ids = {item["source_id"] for item in public_values}
    if candidate_source_ids & loaded_source_ids:
        raise ValueError(f"source candidates not loaded were treated as loaded: {sorted(candidate_source_ids & loaded_source_ids)}")

    status_counts = {status: sum(item.scenario_output_status == status for item in module_constraints) for status in SCENARIO_OUTPUT_STATUS_VALUES}
    forbidden_count = len({implication for item in module_constraints for implication in item.forbidden_implications})
    dashboard_rules = _display_rules()
    required_rules = set(_list_of_strings(manifest["required_dashboard_rules"], "required_dashboard_rules"))
    if required_rules != {item.display_rule for item in dashboard_rules}:
        raise ValueError("dashboard display rule coverage mismatch")

    scenario_outputs = _scenario_output_constraints(module_constraints)
    forbidden_implications = _forbidden_implications()
    summary = ScenarioConstraintSummary(
        public_aggregate_scenario_constraint_layer_created=True,
        new_data_loaded=False,
        loaded_public_values_used=len(public_values),
        module_constraints_mapped=len(module_constraints),
        field_constraints_mapped=len(field_constraints),
        outputs_display_as_sanity_check_only=status_counts["display_as_sanity_check_only"],
        outputs_display_as_public_anchor_only=status_counts["display_as_public_aggregate_anchor_only"],
        outputs_display_as_public_bound_only=status_counts["display_as_public_aggregate_bound_only"],
        outputs_display_as_context_only=status_counts["display_as_context_only"],
        outputs_display_as_placeholder_narrowing_only=status_counts["display_as_placeholder_narrowing_only"],
        outputs_display_as_reviewer_traceability_only=status_counts["display_as_reviewer_traceability_only"],
        outputs_marked_non_interpretable=status_counts["mark_non_interpretable"],
        outputs_hidden_from_reviewer_dashboard=status_counts["hide_from_reviewer_dashboard"],
        outputs_fail_closed_forbidden_claim=status_counts["fail_closed_forbidden_claim"],
        forbidden_implications_mapped=forbidden_count,
        public_source_candidates_treated_as_loaded=False,
        restricted_data_loaded=False,
        personal_data_loaded=False,
        taxpayer_level_data_loaded=False,
        firm_confidential_data_loaded=False,
        household_microdata_loaded=False,
        calibration_completed=False,
        validation_claimed=False,
        actual_tax_payable_determined=False,
        official_status_claimed=False,
        firm_level_liability_logic_modified=False,
        forbidden_claim_findings=0,
    )
    result = PublicAggregateScenarioConstraintResult(
        constraint_layer_id=_non_empty(manifest["constraint_layer_id"], "constraint_layer_id"),
        constraint_layer_name=_non_empty(manifest["constraint_layer_name"], "constraint_layer_name"),
        status=_non_empty(manifest["status"], "status"),
        non_claims=_list_of_strings(manifest["non_claims"], "non_claims"),
        public_aggregate_values=public_values,
        module_scenario_constraints=module_constraints,
        field_scenario_constraints=field_constraints,
        scenario_output_constraints=scenario_outputs,
        forbidden_scenario_implications=forbidden_implications,
        dashboard_display_rules=dashboard_rules,
        source_candidates_not_loaded=source_candidates,
        future_build_35_requirements=_list_of_strings(manifest["build_35_requirements"], "build_35_requirements"),
        summary=summary,
    )
    findings = find_forbidden_affirmative_scenario_constraint_claims(str(result.to_jsonable()))
    if findings:
        raise ValueError(f"forbidden affirmative scenario constraint claims found: {findings}")
    return result
