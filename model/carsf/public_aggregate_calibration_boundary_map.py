"""Public aggregate calibration-boundary mapping for Build 33.

This module defines how Build 31 public aggregate values may be used across
the prototype. It does not load new data, perform calibration, validate CARSF,
determine tax payable, or modify firm-level CARSF liability logic.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


ALLOWED_USE_TYPE_VALUES = {
    "sanity_check_only",
    "public_aggregate_anchor_only",
    "public_aggregate_bound_only",
    "contextual_reference_only",
    "placeholder_narrowing_only",
    "reviewer_traceability_only",
}

FORBIDDEN_USE_TYPE_VALUES = {
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
}

BOUNDARY_STATUS_VALUES = {
    "allowed_as_boundary_only",
    "allowed_as_anchor_only",
    "allowed_as_context_only",
    "blocked_for_calibration",
    "requires_restricted_data",
    "requires_external_review",
    "forbidden_for_claim",
}

CLAIM_LEVEL_VALUES = {
    "public_aggregate_sanity_check",
    "public_aggregate_anchor",
    "public_aggregate_bound",
    "contextual_public_reference",
    "placeholder_boundary_only",
    "no_calibration_claim_allowed",
    "no_validation_claim_allowed",
}

BLOCKER_TYPE_VALUES = {
    "restricted_tax_data_required",
    "firm_confidential_data_required",
    "household_microdata_required",
    "welfare_payment_records_required",
    "behavioural_elasticity_required",
    "legal_review_required",
    "tax_review_required",
    "economic_review_required",
    "statistical_review_required",
    "public_aggregate_data_insufficient",
    "external_domain_review_required",
}

CALIBRATION_BOUNDARY_WARNING = (
    "This is a public aggregate calibration-boundary map only. No new data is loaded by this build. Public aggregate "
    "data can support sanity checks, anchors, bounds, context, placeholder narrowing, or reviewer traceability only. "
    "Public aggregate data does not calibrate the model. Calibration has not been completed. Public data does not "
    "prove the model works. Boundary mapping does not mean validation, statistical estimation, legal sufficiency, "
    "or implementation readiness. Source candidates not loaded remain not loaded. Restricted-data blockers remain "
    "blockers. This is not validation, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, "
    "not PBO costing, not economic validation, not welfare validation, not statistical validation, not operational "
    "readiness, not legal sufficiency, and not official status. It does not determine actual tax payable and does "
    "not modify firm-level CARSF liability."
)

CALIBRATION_BOUNDARY_NON_CLAIMS = [
    CALIBRATION_BOUNDARY_WARNING,
    "Build 33 uses existing Build 31 public aggregate values and Build 32 placeholder replacement decisions only.",
    "Allowed-use labels are boundary labels only; they are not calibration, validation, legal sufficiency, readiness, or liability determinations.",
    "Source candidates not loaded in Build 31 remain not loaded and future-only.",
]

FORBIDDEN_AFFIRMATIVE_CALIBRATION_BOUNDARY_CLAIMS = [
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
    "calibrated boundary",
    "calibration boundary satisfied",
    "public aggregate calibration complete",
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
    "forbidden",
    "blocked",
    "boundary",
    "does_not_show",
    "must_not_infer",
    "not_used_for",
    "what_public_data_cannot_support",
    "forbidden_use_types",
    "what this map does not mean",
    "does not mean",
]


@dataclass(frozen=True)
class PublicAggregateCalibrationBoundary:
    value_id: str
    source_id: str
    metric_name: str
    value: int | float | str
    unit: str
    period: str
    geography: str
    data_status: str
    claim_level: str
    public_aggregate_only: bool
    restricted_data: bool
    personal_data: bool
    safe_for_repo_use: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AllowedUseDecision:
    decision_id: str
    use_type: str
    explanation: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ForbiddenUseDecision:
    decision_id: str
    use_type: str
    explanation: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CalibrationBoundaryBlocker:
    blocker_id: str
    target_id: str
    blocker_type: str
    blocker: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ModuleCalibrationBoundaryDecision:
    decision_id: str
    module_id: str
    module_name: str
    related_placeholder_ids: list[str]
    linked_public_value_ids: list[str]
    allowed_use_types: list[str]
    forbidden_use_types: list[str]
    boundary_status: str
    claim_level: str
    what_public_data_can_support: str
    what_public_data_cannot_support: str
    calibration_blockers_remaining: list[str]
    evidence_needed_before_calibration: list[str]
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
class FieldCalibrationBoundaryDecision:
    decision_id: str
    field_id: str
    placeholder_id: str
    linked_public_value_ids: list[str]
    allowed_use_types: list[str]
    forbidden_use_types: list[str]
    boundary_status: str
    claim_level: str
    what_public_data_can_support: str
    what_public_data_cannot_support: str
    calibration_blockers_remaining: list[str]
    evidence_needed_before_calibration: list[str]
    calibration_completed: bool
    validation_claimed: bool
    actual_tax_payable_determined: bool
    firm_level_liability_logic_modified: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CalibrationBoundarySummary:
    public_aggregate_calibration_boundary_map_created: bool
    new_data_loaded: bool
    loaded_public_values_used: int
    module_boundaries_mapped: int
    field_boundaries_mapped: int
    modules_allowed_sanity_check_only: int
    modules_allowed_anchor_only: int
    modules_allowed_bound_only: int
    modules_allowed_context_only: int
    modules_blocked_for_calibration: int
    modules_requiring_restricted_data: int
    modules_requiring_external_review: int
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
class PublicAggregateCalibrationBoundaryResult:
    map_id: str
    map_name: str
    status: str
    non_claims: list[str]
    public_aggregate_values: list[PublicAggregateCalibrationBoundary]
    module_boundary_decisions: list[ModuleCalibrationBoundaryDecision]
    field_boundary_decisions: list[FieldCalibrationBoundaryDecision]
    allowed_use_decisions: list[AllowedUseDecision]
    forbidden_use_decisions: list[ForbiddenUseDecision]
    calibration_boundary_blockers: list[CalibrationBoundaryBlocker]
    source_candidates_not_loaded: list[dict[str, Any]]
    future_build_34_requirements: list[str]
    summary: CalibrationBoundarySummary

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


def _choice(value: str, allowed: set[str], field: str) -> str:
    if value not in allowed:
        raise ValueError(f"{field} has invalid value {value!r}; expected one of {sorted(allowed)}")
    return value


def _bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field} must be boolean")
    return value


def _list_of_strings(value: Any, field: str, *, allow_empty: bool = False) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{field} must be a list of strings")
    if not allow_empty and not value:
        raise ValueError(f"{field} must be non-empty")
    return [item.strip() for item in value]


def _is_negative_context(text: str, phrase_start: int) -> bool:
    window = text[max(0, phrase_start - 220) : phrase_start].lower()
    return any(marker in window for marker in NEGATIVE_CONTEXT_MARKERS)


def find_forbidden_affirmative_calibration_boundary_claims(text: str) -> list[str]:
    lowered = text.lower()
    findings: list[str] = []
    for phrase in FORBIDDEN_AFFIRMATIVE_CALIBRATION_BOUNDARY_CLAIMS:
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


def _public_value_from_mapping(source: dict[str, Any]) -> PublicAggregateCalibrationBoundary:
    _required_mapping(
        source,
        [
            "value_id",
            "source_id",
            "metric_name",
            "value",
            "unit",
            "period",
            "geography",
            "claim_level",
            "data_status",
            "public_aggregate_only",
            "restricted_data",
            "personal_data",
            "safe_for_repo_use",
        ],
        "public aggregate value",
    )
    item = PublicAggregateCalibrationBoundary(
        value_id=_non_empty(source["value_id"], "value_id"),
        source_id=_non_empty(source["source_id"], "source_id"),
        metric_name=_non_empty(source["metric_name"], "metric_name"),
        value=source["value"],
        unit=_non_empty(source["unit"], "unit"),
        period=_non_empty(source["period"], "period"),
        geography=_non_empty(source["geography"], "geography"),
        claim_level=_non_empty(source["claim_level"], "claim_level"),
        data_status=_non_empty(source["data_status"], "data_status"),
        public_aggregate_only=_bool(source["public_aggregate_only"], "public_aggregate_only"),
        restricted_data=_bool(source["restricted_data"], "restricted_data"),
        personal_data=_bool(source["personal_data"], "personal_data"),
        safe_for_repo_use=_bool(source["safe_for_repo_use"], "safe_for_repo_use"),
    )
    if item.data_status != "loaded_public_aggregate":
        raise ValueError(f"public value is not loaded_public_aggregate: {item.value_id}")
    if item.claim_level != "real_public_aggregate_data":
        raise ValueError(f"public value has unexpected claim_level: {item.value_id}")
    if not item.public_aggregate_only or item.restricted_data or item.personal_data or not item.safe_for_repo_use:
        raise ValueError(f"public value fails public aggregate guardrails: {item.value_id}")
    return item


def _replacement_decisions(replacement_report: dict[str, Any]) -> list[dict[str, Any]]:
    payload = replacement_report.get("public_data_placeholder_replacement_map", {})
    decisions = payload.get("replacement_decisions", [])
    if not isinstance(decisions, list) or not decisions:
        raise ValueError("Build 32 placeholder replacement decisions must be present")
    return decisions


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


def _module_plan() -> dict[str, dict[str, Any]]:
    common_forbidden = [
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
    ]
    return {
        "opfte_benchmark_module": {
            "name": "OPFTE benchmark module",
            "placeholders": ["anchor_opfte_minimum_wage"],
            "values": ["fair_work_national_minimum_wage_hourly_2025", "fair_work_national_minimum_wage_weekly_2025"],
            "allowed": ["sanity_check_only", "public_aggregate_anchor_only", "public_aggregate_bound_only", "reviewer_traceability_only"],
            "forbidden": common_forbidden,
            "status": "allowed_as_anchor_only",
            "claim": "public_aggregate_anchor",
            "can": "Use Fair Work wage thresholds as public aggregate anchors and visible bounds for OPFTE placeholder inspection.",
            "cannot": "Cannot calibrate OPFTE, estimate representative labour costs, determine firm liability, or determine tax payable.",
            "blockers": ["statistical_review_required", "restricted_tax_data_required", "public_aggregate_data_insufficient"],
            "evidence": ["occupation-specific labour evidence", "sector schedule authority method", "statistical review"],
            "reviews": {"restricted": True, "legal": False, "tax": True, "economic": False, "statistical": True, "external": True},
        },
        "hle_assumptions_module": {
            "name": "HLE assumptions module",
            "placeholders": ["anchor_hle_minimum_wage"],
            "values": ["fair_work_national_minimum_wage_hourly_2025", "fair_work_national_minimum_wage_weekly_2025", "fair_work_casual_loading_2025"],
            "allowed": ["sanity_check_only", "public_aggregate_bound_only", "placeholder_narrowing_only", "reviewer_traceability_only"],
            "forbidden": common_forbidden,
            "status": "allowed_as_boundary_only",
            "claim": "public_aggregate_bound",
            "can": "Use wage and casual-loading values as boundary checks and narrowing context for HLE placeholders.",
            "cannot": "Cannot estimate representative labour costs, occupation-specific wage models, or automation substitution calibration.",
            "blockers": ["behavioural_elasticity_required", "statistical_review_required", "public_aggregate_data_insufficient"],
            "evidence": ["human labour equivalent method", "occupation mix evidence", "behavioural elasticity review"],
            "reviews": {"restricted": True, "legal": False, "tax": False, "economic": True, "statistical": True, "external": True},
        },
        "qlc_weights_module": {
            "name": "QLC weights module",
            "placeholders": ["anchor_qlc_minimum_wage"],
            "values": ["fair_work_national_minimum_wage_hourly_2025", "fair_work_national_minimum_wage_weekly_2025"],
            "allowed": ["sanity_check_only", "public_aggregate_bound_only", "placeholder_narrowing_only"],
            "forbidden": common_forbidden,
            "status": "allowed_as_boundary_only",
            "claim": "placeholder_boundary_only",
            "can": "Use wage thresholds as bounded context for QLC wage components.",
            "cannot": "Cannot set QLC weights, validate labour quality, or establish legal attribution.",
            "blockers": ["statistical_review_required", "tax_review_required", "public_aggregate_data_insufficient"],
            "evidence": ["QLC weighting method", "sector labour evidence", "tax-method review"],
            "reviews": {"restricted": True, "legal": True, "tax": True, "economic": False, "statistical": True, "external": True},
        },
        "fiscal_trajectory_assumptions": {
            "name": "Fiscal trajectory assumptions",
            "placeholders": ["anchor_fiscal_public_aggregates"],
            "values": [
                "ato_large_corporate_income_tax_received_2022_23",
                "ato_large_corporate_entities_no_income_tax_percent_2022_23",
                "ato_total_tax_revenue_collected_2022_23",
                "ato_company_tax_revenue_2022_23",
                "treasury_total_receipts_2025_26_estimate",
                "treasury_taxation_receipts_2025_26_estimate",
            ],
            "allowed": ["sanity_check_only", "public_aggregate_bound_only", "contextual_reference_only", "reviewer_traceability_only"],
            "forbidden": common_forbidden,
            "status": "allowed_as_context_only",
            "claim": "contextual_public_reference",
            "can": "Use ATO and Budget receipt values as fiscal scale context and public aggregate bounds.",
            "cannot": "Cannot create Treasury modelling, PBO costing, fiscal sufficiency, CARSF revenue estimates, or implementation readiness.",
            "blockers": ["economic_review_required", "restricted_tax_data_required", "behavioural_elasticity_required"],
            "evidence": ["revenue incidence method", "behavioural response method", "economic review"],
            "reviews": {"restricted": True, "legal": False, "tax": True, "economic": True, "statistical": True, "external": True},
        },
        "payg_erosion_assumptions": {
            "name": "PAYG erosion assumptions",
            "placeholders": ["anchor_payg_public_tax_stats"],
            "values": ["ato_total_tax_revenue_collected_2022_23", "ato_company_tax_revenue_2022_23"],
            "allowed": ["sanity_check_only", "contextual_reference_only", "reviewer_traceability_only"],
            "forbidden": common_forbidden,
            "status": "requires_restricted_data",
            "claim": "no_calibration_claim_allowed",
            "can": "Use public tax aggregates as scale context only.",
            "cannot": "Cannot calibrate PAYG erosion, infer taxpayer behaviour, or estimate CARSF revenue.",
            "blockers": ["restricted_tax_data_required", "statistical_review_required", "public_aggregate_data_insufficient"],
            "evidence": ["taxpayer behaviour evidence", "employment tax pathway method", "authorised tax data governance"],
            "reviews": {"restricted": True, "legal": False, "tax": True, "economic": True, "statistical": True, "external": True},
        },
        "transition_funding_assumptions": {
            "name": "Transition funding assumptions",
            "placeholders": ["anchor_transition_public_reference"],
            "values": ["treasury_total_receipts_2025_26_estimate", "treasury_taxation_receipts_2025_26_estimate", "ato_super_guarantee_rate_2025_26"],
            "allowed": ["sanity_check_only", "public_aggregate_bound_only", "contextual_reference_only"],
            "forbidden": common_forbidden,
            "status": "requires_external_review",
            "claim": "contextual_public_reference",
            "can": "Use public receipt and rate values as scale context for transition-funding placeholder review.",
            "cannot": "Cannot prove fiscal sufficiency, payment eligibility, welfare effects, or policy readiness.",
            "blockers": ["welfare_payment_records_required", "economic_review_required", "legal_review_required"],
            "evidence": ["transition design review", "welfare payment evidence", "economic review"],
            "reviews": {"restricted": True, "legal": True, "tax": False, "economic": True, "statistical": True, "external": True},
        },
        "superannuation_contribution_pressure": {
            "name": "Superannuation contribution pressure",
            "placeholders": ["anchor_super_guarantee_rate"],
            "values": ["ato_super_guarantee_rate_2025_26"],
            "allowed": ["sanity_check_only", "public_aggregate_anchor_only", "contextual_reference_only"],
            "forbidden": common_forbidden,
            "status": "allowed_as_anchor_only",
            "claim": "public_aggregate_anchor",
            "can": "Use the public superannuation guarantee rate as an anchor for payment-interaction review.",
            "cannot": "Cannot estimate individual super, employer behaviour, payroll amounts, or ATO guidance.",
            "blockers": ["firm_confidential_data_required", "tax_review_required", "public_aggregate_data_insufficient"],
            "evidence": ["wage base evidence", "employer contribution behaviour evidence", "tax review"],
            "reviews": {"restricted": True, "legal": False, "tax": True, "economic": True, "statistical": False, "external": True},
        },
        "sector_schedule_values": {
            "name": "Sector schedule values",
            "placeholders": ["anchor_sector_schedule_source_reference"],
            "values": ["fair_work_national_minimum_wage_hourly_2025", "fair_work_casual_loading_2025"],
            "allowed": ["sanity_check_only", "contextual_reference_only", "reviewer_traceability_only"],
            "forbidden": common_forbidden,
            "status": "requires_external_review",
            "claim": "contextual_public_reference",
            "can": "Use wage anchors as limited labour-cost context for sector schedule review.",
            "cannot": "Cannot produce official sector rankings, schedule calibration, or legal attribution rules.",
            "blockers": ["statistical_review_required", "legal_review_required", "public_aggregate_data_insufficient"],
            "evidence": ["sector-specific public aggregates", "schedule authority method", "legal review"],
            "reviews": {"restricted": True, "legal": True, "tax": True, "economic": True, "statistical": True, "external": True},
        },
        "sector_stress_matrix": {
            "name": "Sector stress matrix",
            "placeholders": ["anchor_sector_schedule_source_reference", "anchor_uncertainty_source_reference_only"],
            "values": ["fair_work_national_minimum_wage_hourly_2025", "ato_total_tax_revenue_collected_2022_23"],
            "allowed": ["sanity_check_only", "contextual_reference_only"],
            "forbidden": common_forbidden,
            "status": "requires_external_review",
            "claim": "placeholder_boundary_only",
            "can": "Use public aggregates as review context for visible stress assumptions.",
            "cannot": "Cannot establish sector stress calibration, ranking, incidence, or population estimates.",
            "blockers": ["economic_review_required", "statistical_review_required", "public_aggregate_data_insufficient"],
            "evidence": ["sector exposure evidence", "economic incidence review", "statistical review"],
            "reviews": {"restricted": True, "legal": False, "tax": False, "economic": True, "statistical": True, "external": True},
        },
        "behavioural_response_gaming_simulation": {
            "name": "Behavioural response / gaming simulation",
            "placeholders": ["anchor_uncertainty_source_reference_only"],
            "values": ["ato_total_tax_revenue_collected_2022_23", "ato_company_tax_revenue_2022_23"],
            "allowed": ["contextual_reference_only", "reviewer_traceability_only"],
            "forbidden": common_forbidden,
            "status": "blocked_for_calibration",
            "claim": "no_calibration_claim_allowed",
            "can": "Use public aggregates only as traceable context for why behavioural calibration remains blocked.",
            "cannot": "Cannot estimate behavioural elasticity, avoidance, gaming, causal response, or taxpayer behaviour.",
            "blockers": ["behavioural_elasticity_required", "restricted_tax_data_required", "economic_review_required"],
            "evidence": ["behavioural elasticity evidence", "authorised administrative data", "economic review"],
            "reviews": {"restricted": True, "legal": True, "tax": True, "economic": True, "statistical": True, "external": True},
        },
        "administrative_compliance_workflow": {
            "name": "Administrative compliance workflow",
            "placeholders": ["anchor_payg_public_tax_stats"],
            "values": ["ato_total_tax_revenue_collected_2022_23"],
            "allowed": ["reviewer_traceability_only", "contextual_reference_only"],
            "forbidden": common_forbidden,
            "status": "requires_external_review",
            "claim": "no_validation_claim_allowed",
            "can": "Use public aggregates only to show source traceability around administrative scale context.",
            "cannot": "Cannot create compliance scoring, ATO guidance, notices, enforcement, or operational workflow readiness.",
            "blockers": ["legal_review_required", "tax_review_required", "external_domain_review_required"],
            "evidence": ["ATO methods review", "legal review", "secure operational design"],
            "reviews": {"restricted": False, "legal": True, "tax": True, "economic": False, "statistical": False, "external": True},
        },
        "legislative_architecture_skeleton": {
            "name": "Legislative architecture skeleton",
            "placeholders": [],
            "values": [],
            "allowed": ["reviewer_traceability_only"],
            "forbidden": common_forbidden,
            "status": "forbidden_for_claim",
            "claim": "no_validation_claim_allowed",
            "can": "Use public data references only to identify where legal review would be required.",
            "cannot": "Cannot support legal sufficiency, operative law, drafting readiness, or official policy status.",
            "blockers": ["legal_review_required", "tax_review_required", "external_domain_review_required"],
            "evidence": ["legal drafting review", "tax review", "Parliamentary Counsel review"],
            "reviews": {"restricted": False, "legal": True, "tax": True, "economic": False, "statistical": False, "external": True},
        },
        "household_distributional_scenarios": {
            "name": "Household distributional scenarios",
            "placeholders": ["anchor_help_source_reference", "anchor_transition_public_reference"],
            "values": ["treasury_total_receipts_2025_26_estimate"],
            "allowed": ["contextual_reference_only", "reviewer_traceability_only"],
            "forbidden": common_forbidden,
            "status": "requires_restricted_data",
            "claim": "no_calibration_claim_allowed",
            "can": "Use public fiscal context only to show that household placeholders remain boundary-limited.",
            "cannot": "Cannot produce real household estimates, population estimates, welfare impacts, or distributional calibration.",
            "blockers": ["household_microdata_required", "welfare_payment_records_required", "statistical_review_required"],
            "evidence": ["authorised household microdata", "welfare payment evidence", "statistical review"],
            "reviews": {"restricted": True, "legal": False, "tax": False, "economic": True, "statistical": True, "external": True},
        },
        "household_weighting": {
            "name": "Household weighting",
            "placeholders": ["anchor_help_source_reference"],
            "values": [],
            "allowed": ["reviewer_traceability_only"],
            "forbidden": common_forbidden,
            "status": "requires_restricted_data",
            "claim": "no_calibration_claim_allowed",
            "can": "Use the boundary map to show that public aggregate values do not support representative household weighting.",
            "cannot": "Cannot create household population estimates, real subgroup weights, or statistical validation.",
            "blockers": ["household_microdata_required", "statistical_review_required", "public_aggregate_data_insufficient"],
            "evidence": ["authorised household sample frame", "weighting method", "statistical review"],
            "reviews": {"restricted": True, "legal": False, "tax": False, "economic": True, "statistical": True, "external": True},
        },
        "uncertainty_ranges": {
            "name": "Uncertainty ranges",
            "placeholders": ["anchor_uncertainty_source_reference_only"],
            "values": ["ato_total_tax_revenue_collected_2022_23", "ato_company_tax_revenue_2022_23"],
            "allowed": ["contextual_reference_only", "reviewer_traceability_only"],
            "forbidden": common_forbidden,
            "status": "requires_external_review",
            "claim": "placeholder_boundary_only",
            "can": "Use public aggregates as context for non-statistical placeholder ranges only.",
            "cannot": "Cannot produce confidence intervals, statistical estimation, or real uncertainty quantification.",
            "blockers": ["statistical_review_required", "public_aggregate_data_insufficient"],
            "evidence": ["uncertainty method", "sample design", "statistical review"],
            "reviews": {"restricted": True, "legal": False, "tax": False, "economic": False, "statistical": True, "external": True},
        },
        "reviewed_scenario_comparison_layer": {
            "name": "Reviewed scenario comparison layer",
            "placeholders": ["anchor_uncertainty_source_reference_only"],
            "values": ["ato_total_tax_revenue_collected_2022_23"],
            "allowed": ["sanity_check_only", "contextual_reference_only", "reviewer_traceability_only"],
            "forbidden": common_forbidden,
            "status": "requires_external_review",
            "claim": "placeholder_boundary_only",
            "can": "Use public aggregates to help label scenario comparisons as bounded or contextual.",
            "cannot": "Cannot validate scenarios, produce official rankings, or imply policy readiness.",
            "blockers": ["statistical_review_required", "economic_review_required", "external_domain_review_required"],
            "evidence": ["scenario review protocol", "statistical review", "economic review"],
            "reviews": {"restricted": False, "legal": False, "tax": False, "economic": True, "statistical": True, "external": True},
        },
        "executive_dashboard_consolidation": {
            "name": "Executive dashboard consolidation",
            "placeholders": [],
            "values": [],
            "allowed": ["reviewer_traceability_only", "contextual_reference_only"],
            "forbidden": common_forbidden,
            "status": "allowed_as_context_only",
            "claim": "contextual_public_reference",
            "can": "Surface boundary labels, source traceability, and non-claim warnings for reviewers.",
            "cannot": "Cannot create a readiness score, calibration score, validation score, tax payable estimate, or liability estimate.",
            "blockers": ["external_domain_review_required", "public_aggregate_data_insufficient"],
            "evidence": ["reviewer feedback", "dashboard interpretation testing", "guardrail review"],
            "reviews": {"restricted": False, "legal": True, "tax": True, "economic": False, "statistical": False, "external": True},
        },
        "public_data_evidence_map": {
            "name": "Public data evidence map",
            "placeholders": [],
            "values": [],
            "allowed": ["reviewer_traceability_only", "contextual_reference_only"],
            "forbidden": common_forbidden,
            "status": "allowed_as_context_only",
            "claim": "contextual_public_reference",
            "can": "Show reviewers which values, anchors, and blockers are traceable.",
            "cannot": "Cannot turn source traceability into calibration, validation, source verification, or official status.",
            "blockers": ["external_domain_review_required", "statistical_review_required"],
            "evidence": ["manual reviewer inspection", "statistical review where relevant"],
            "reviews": {"restricted": False, "legal": False, "tax": False, "economic": False, "statistical": True, "external": True},
        },
        "public_data_placeholder_replacement_map": {
            "name": "Public data placeholder replacement map",
            "placeholders": [
                "anchor_opfte_minimum_wage",
                "anchor_hle_minimum_wage",
                "anchor_qlc_minimum_wage",
                "anchor_fiscal_public_aggregates",
                "anchor_super_guarantee_rate",
            ],
            "values": [
                "fair_work_national_minimum_wage_hourly_2025",
                "fair_work_national_minimum_wage_weekly_2025",
                "fair_work_casual_loading_2025",
                "ato_company_tax_revenue_2022_23",
                "ato_super_guarantee_rate_2025_26",
            ],
            "allowed": ["public_aggregate_anchor_only", "public_aggregate_bound_only", "placeholder_narrowing_only", "reviewer_traceability_only"],
            "forbidden": common_forbidden,
            "status": "allowed_as_boundary_only",
            "claim": "placeholder_boundary_only",
            "can": "Define which placeholder decisions are anchors, bounds, context, or blocked.",
            "cannot": "Cannot represent replacement mapping as calibration, validation, statistical estimation, or liability determination.",
            "blockers": ["restricted_tax_data_required", "statistical_review_required", "external_domain_review_required"],
            "evidence": ["reviewer inspection", "restricted-data governance", "statistical review"],
            "reviews": {"restricted": True, "legal": False, "tax": True, "economic": False, "statistical": True, "external": True},
        },
    }


def _validate_plan_values(plan: dict[str, dict[str, Any]], values_by_id: dict[str, PublicAggregateCalibrationBoundary]) -> None:
    for module_id, item in plan.items():
        for value_id in item["values"]:
            if value_id not in values_by_id:
                raise ValueError(f"module boundary {module_id} links missing public value: {value_id}")


def _module_decision(module_id: str, plan: dict[str, Any]) -> ModuleCalibrationBoundaryDecision:
    allowed = _list_of_strings(plan["allowed"], f"{module_id}.allowed_use_types")
    forbidden = _list_of_strings(plan["forbidden"], f"{module_id}.forbidden_use_types")
    blockers = _list_of_strings(plan["blockers"], f"{module_id}.calibration_blockers_remaining")
    for item in allowed:
        _choice(item, ALLOWED_USE_TYPE_VALUES, "allowed_use_types")
    for item in forbidden:
        _choice(item, FORBIDDEN_USE_TYPE_VALUES, "forbidden_use_types")
    for item in blockers:
        _choice(item, BLOCKER_TYPE_VALUES, "calibration_blockers_remaining")
    reviews = plan["reviews"]
    decision = ModuleCalibrationBoundaryDecision(
        decision_id=f"boundary_{module_id}",
        module_id=module_id,
        module_name=_non_empty(plan["name"], "module_name"),
        related_placeholder_ids=_list_of_strings(plan["placeholders"], "related_placeholder_ids", allow_empty=True),
        linked_public_value_ids=_list_of_strings(plan["values"], "linked_public_value_ids", allow_empty=True),
        allowed_use_types=allowed,
        forbidden_use_types=forbidden,
        boundary_status=_choice(plan["status"], BOUNDARY_STATUS_VALUES, "boundary_status"),
        claim_level=_choice(plan["claim"], CLAIM_LEVEL_VALUES, "claim_level"),
        what_public_data_can_support=_non_empty(plan["can"], "what_public_data_can_support"),
        what_public_data_cannot_support=_non_empty(plan["cannot"], "what_public_data_cannot_support"),
        calibration_blockers_remaining=blockers,
        evidence_needed_before_calibration=_list_of_strings(plan["evidence"], "evidence_needed_before_calibration"),
        requires_restricted_data=_bool(reviews["restricted"], "requires_restricted_data"),
        requires_legal_review=_bool(reviews["legal"], "requires_legal_review"),
        requires_tax_review=_bool(reviews["tax"], "requires_tax_review"),
        requires_economic_review=_bool(reviews["economic"], "requires_economic_review"),
        requires_statistical_review=_bool(reviews["statistical"], "requires_statistical_review"),
        requires_external_review=_bool(reviews["external"], "requires_external_review"),
        safe_for_repo_use=True,
        calibration_completed=False,
        validation_claimed=False,
        actual_tax_payable_determined=False,
        official_status_claimed=False,
        firm_level_liability_logic_modified=False,
    )
    if not decision.allowed_use_types or not decision.forbidden_use_types:
        raise ValueError(f"module boundary missing allowed/forbidden uses: {module_id}")
    return decision


def _field_boundary_from_replacement(decision: dict[str, Any]) -> FieldCalibrationBoundaryDecision:
    replacement_status = decision["replacement_status"]
    if replacement_status == "replaced_by_public_aggregate_anchor":
        allowed = ["public_aggregate_anchor_only", "sanity_check_only", "reviewer_traceability_only"]
        status = "allowed_as_anchor_only"
        claim = "public_aggregate_anchor"
        can = "Use the linked public aggregate value as an anchor for placeholder review only."
    elif replacement_status == "narrowed_by_public_aggregate_anchor":
        allowed = ["public_aggregate_bound_only", "placeholder_narrowing_only", "sanity_check_only"]
        status = "allowed_as_boundary_only"
        claim = "public_aggregate_bound"
        can = "Use the linked public aggregate value as a boundary or narrowing reference only."
    elif replacement_status == "informed_by_public_aggregate_anchor":
        allowed = ["contextual_reference_only", "reviewer_traceability_only"]
        status = "allowed_as_context_only"
        claim = "contextual_public_reference"
        can = "Use the linked public aggregate value as contextual reference only."
    elif replacement_status == "blocked_until_restricted_data":
        allowed = ["reviewer_traceability_only"]
        status = "requires_restricted_data"
        claim = "no_calibration_claim_allowed"
        can = "Use the field boundary only to show that restricted data remains required."
    elif replacement_status == "blocked_until_external_review":
        allowed = ["reviewer_traceability_only"]
        status = "requires_external_review"
        claim = "no_validation_claim_allowed"
        can = "Use the field boundary only to show that external review remains required."
    else:
        allowed = ["contextual_reference_only", "reviewer_traceability_only"]
        status = "blocked_for_calibration"
        claim = "placeholder_boundary_only"
        can = "Use the field boundary only to show that public aggregate data is structurally insufficient."
    forbidden = [
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
    ]
    return FieldCalibrationBoundaryDecision(
        decision_id=f"field_boundary_{decision['placeholder_id']}",
        field_id=_non_empty(decision["field_id"], "field_id"),
        placeholder_id=_non_empty(decision["placeholder_id"], "placeholder_id"),
        linked_public_value_ids=_list_of_strings(decision["linked_public_value_ids"], "linked_public_value_ids", allow_empty=True),
        allowed_use_types=allowed,
        forbidden_use_types=forbidden,
        boundary_status=status,
        claim_level=claim,
        what_public_data_can_support=can,
        what_public_data_cannot_support="Public aggregate data cannot turn this field into calibration, validation, actual tax payable, official status, legal sufficiency, or firm-level CARSF liability.",
        calibration_blockers_remaining=_list_of_strings(decision["remaining_blockers"], "calibration_blockers_remaining"),
        evidence_needed_before_calibration=_list_of_strings(
            decision["evidence_needed_before_calibration"], "evidence_needed_before_calibration"
        ),
        calibration_completed=False,
        validation_claimed=False,
        actual_tax_payable_determined=False,
        firm_level_liability_logic_modified=False,
    )


def build_public_aggregate_calibration_boundary_result(
    manifest: dict[str, Any],
    public_values_payload: dict[str, Any],
    source_manifest: dict[str, Any],
    replacement_report: dict[str, Any],
) -> PublicAggregateCalibrationBoundaryResult:
    _required_mapping(
        manifest,
        [
            "map_id",
            "map_name",
            "status",
            "non_claims",
            "input_artifacts",
            "allowed_use_type_taxonomy",
            "forbidden_use_type_taxonomy",
            "boundary_status_taxonomy",
            "claim_level_taxonomy",
            "blocker_type_taxonomy",
            "required_module_boundaries",
            "required_field_boundaries",
            "required_public_value_coverage",
            "forbidden_claims",
            "build_34_requirements",
        ],
        "public aggregate calibration boundary manifest",
    )
    if manifest["status"] != "public_aggregate_calibration_boundary_map_only":
        raise ValueError("boundary manifest status must be public_aggregate_calibration_boundary_map_only")
    if CALIBRATION_BOUNDARY_WARNING not in manifest["non_claims"]:
        raise ValueError("boundary manifest missing required non-claim warning")
    if set(manifest["allowed_use_type_taxonomy"]) != ALLOWED_USE_TYPE_VALUES:
        raise ValueError("allowed_use_type_taxonomy does not match required values")
    if set(manifest["forbidden_use_type_taxonomy"]) != FORBIDDEN_USE_TYPE_VALUES:
        raise ValueError("forbidden_use_type_taxonomy does not match required values")
    if set(manifest["boundary_status_taxonomy"]) != BOUNDARY_STATUS_VALUES:
        raise ValueError("boundary_status_taxonomy does not match required values")
    if set(manifest["claim_level_taxonomy"]) != CLAIM_LEVEL_VALUES:
        raise ValueError("claim_level_taxonomy does not match required values")
    if set(manifest["blocker_type_taxonomy"]) != BLOCKER_TYPE_VALUES:
        raise ValueError("blocker_type_taxonomy does not match required values")

    values = [_public_value_from_mapping(item) for item in public_values_payload.get("values", [])]
    values_by_id = {item.value_id: item for item in values}
    if len(values_by_id) != len(values):
        raise ValueError("public aggregate value ids must be unique")
    required_values = set(_list_of_strings(manifest["required_public_value_coverage"], "required_public_value_coverage"))
    if required_values != set(values_by_id):
        missing = sorted(required_values - set(values_by_id))
        extra = sorted(set(values_by_id) - required_values)
        raise ValueError(f"public value coverage mismatch; missing={missing}; extra={extra}")

    replacement_decisions = _replacement_decisions(replacement_report)
    replacement_ids = {item["placeholder_id"] for item in replacement_decisions}
    required_fields = set(_list_of_strings(manifest["required_field_boundaries"], "required_field_boundaries"))
    if required_fields != replacement_ids:
        missing = sorted(required_fields - replacement_ids)
        extra = sorted(replacement_ids - required_fields)
        raise ValueError(f"field boundary coverage mismatch; missing={missing}; extra={extra}")

    plan = _module_plan()
    _validate_plan_values(plan, values_by_id)
    required_modules = set(_list_of_strings(manifest["required_module_boundaries"], "required_module_boundaries"))
    if required_modules != set(plan):
        missing = sorted(required_modules - set(plan))
        extra = sorted(set(plan) - required_modules)
        raise ValueError(f"module boundary coverage mismatch; missing={missing}; extra={extra}")
    module_decisions = [_module_decision(module_id, plan[module_id]) for module_id in sorted(plan)]
    field_decisions = [_field_boundary_from_replacement(item) for item in sorted(replacement_decisions, key=lambda row: row["placeholder_id"])]

    source_candidates = _source_candidates_not_loaded(source_manifest)
    candidate_source_ids = {item["source_id"] for item in source_candidates}
    candidate_value_use = any(
        source_id in candidate_source_ids
        for source_id in {values_by_id[value_id].source_id for decision in module_decisions for value_id in decision.linked_public_value_ids}
    )
    if candidate_value_use:
        raise ValueError("source candidates not loaded were treated as loaded")

    used_public_values = {value_id for decision in module_decisions for value_id in decision.linked_public_value_ids}
    used_public_values.update(value_id for decision in field_decisions for value_id in decision.linked_public_value_ids)
    if used_public_values != set(values_by_id):
        missing = sorted(set(values_by_id) - used_public_values)
        raise ValueError(f"not all loaded public values are used by boundary decisions: {missing}")

    for decision in module_decisions:
        if (
            decision.calibration_completed
            or decision.validation_claimed
            or decision.actual_tax_payable_determined
            or decision.official_status_claimed
            or decision.firm_level_liability_logic_modified
        ):
            raise ValueError(f"module boundary has forbidden true flag: {decision.decision_id}")
    for decision in field_decisions:
        if decision.calibration_completed or decision.validation_claimed or decision.actual_tax_payable_determined:
            raise ValueError(f"field boundary has forbidden true flag: {decision.decision_id}")
        if decision.firm_level_liability_logic_modified:
            raise ValueError(f"field boundary modifies firm-level liability logic: {decision.decision_id}")

    blockers = [
        CalibrationBoundaryBlocker(
            blocker_id=f"{decision.module_id}_{blocker}",
            target_id=decision.module_id,
            blocker_type=blocker,
            blocker=f"{blocker} remains unresolved for {decision.module_name}",
        )
        for decision in module_decisions
        for blocker in decision.calibration_blockers_remaining
    ]
    allowed_use_decisions = [
        AllowedUseDecision(
            decision_id=f"allowed_{value}",
            use_type=value,
            explanation=f"Public aggregate data may be used for {value} only when non-claim boundaries remain visible.",
        )
        for value in sorted(ALLOWED_USE_TYPE_VALUES)
    ]
    forbidden_use_decisions = [
        ForbiddenUseDecision(
            decision_id=f"forbidden_{value}",
            use_type=value,
            explanation=f"Public aggregate data must not be used for {value}.",
        )
        for value in sorted(FORBIDDEN_USE_TYPE_VALUES)
    ]

    scan_manifest = {key: value for key, value in manifest.items() if key != "forbidden_claims"}
    forbidden_claims = find_forbidden_affirmative_calibration_boundary_claims(str(scan_manifest))
    if forbidden_claims:
        raise ValueError(f"boundary manifest contains forbidden affirmative claims: {', '.join(forbidden_claims)}")

    summary = CalibrationBoundarySummary(
        public_aggregate_calibration_boundary_map_created=True,
        new_data_loaded=False,
        loaded_public_values_used=len(used_public_values),
        module_boundaries_mapped=len(module_decisions),
        field_boundaries_mapped=len(field_decisions),
        modules_allowed_sanity_check_only=sum("sanity_check_only" in item.allowed_use_types for item in module_decisions),
        modules_allowed_anchor_only=sum("public_aggregate_anchor_only" in item.allowed_use_types for item in module_decisions),
        modules_allowed_bound_only=sum("public_aggregate_bound_only" in item.allowed_use_types for item in module_decisions),
        modules_allowed_context_only=sum("contextual_reference_only" in item.allowed_use_types for item in module_decisions),
        modules_blocked_for_calibration=sum(
            item.boundary_status
            in {"blocked_for_calibration", "requires_restricted_data", "requires_external_review", "forbidden_for_claim"}
            for item in module_decisions
        ),
        modules_requiring_restricted_data=sum(item.requires_restricted_data for item in module_decisions),
        modules_requiring_external_review=sum(item.requires_external_review for item in module_decisions),
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
    return PublicAggregateCalibrationBoundaryResult(
        map_id=str(manifest["map_id"]),
        map_name=str(manifest["map_name"]),
        status=str(manifest["status"]),
        non_claims=list(manifest["non_claims"]),
        public_aggregate_values=values,
        module_boundary_decisions=module_decisions,
        field_boundary_decisions=field_decisions,
        allowed_use_decisions=allowed_use_decisions,
        forbidden_use_decisions=forbidden_use_decisions,
        calibration_boundary_blockers=blockers,
        source_candidates_not_loaded=source_candidates,
        future_build_34_requirements=_list_of_strings(manifest["build_34_requirements"], "build_34_requirements"),
        summary=summary,
    )
