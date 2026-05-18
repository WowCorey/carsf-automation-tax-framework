"""Prototype behavioural response / gaming pathway simulation for CARSF.

This module models synthetic response pathways only. It does not predict
taxpayer behaviour, estimate behavioural elasticity, implement enforcement, or
modify firm-level CARSF liability.
"""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from typing import Any

from .avoidance import (
    ARTIFICIAL_LOW_PROFIT_OR_AAVA,
    CLOUD_COST_RELABELING,
    ENTITY_SPLITTING,
    FAKE_QLC_INFLATION,
    OFFSHORE_AUTOMATION_SERVICE,
    RELATED_PARTY_AI_SERVICE_FEES,
    ROBOTICS_LEASING_AVOIDANCE,
    SECTOR_CLASSIFICATION_ARBITRAGE,
    TOKEN_HUMAN_OVERSIGHT,
)


BEHAVIOURAL_RESPONSE_WARNING = (
    "Behavioural response simulation is prototype-only deterministic placeholder scenario review. "
    "It does not predict taxpayer behaviour. It does not estimate behavioural elasticity. "
    "It is not ATO audit logic, Treasury modelling, ABS/ATO/DSS/PBO analysis, economic validation, "
    "compliance-risk scoring, legal advice, tax advice, or investment advice. It does not estimate "
    "actual tax payable, modify firm-level CARSF liability, implement penalties, or implement enforcement."
)
BEHAVIOURAL_RESPONSE_NON_CLAIMS = [
    BEHAVIOURAL_RESPONSE_WARNING,
    "The simulation does not use firm-level, taxpayer-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.",
    "All response scenarios are synthetic placeholders requiring external calibration, legal review, ATO/Treasury methods review, and behavioural research.",
    "Scenario pressure bands are review prompts only, not compliance findings or real-world outcome estimates.",
]

KNOWN_AVOIDANCE_FLAGS = {
    TOKEN_HUMAN_OVERSIGHT,
    FAKE_QLC_INFLATION,
    OFFSHORE_AUTOMATION_SERVICE,
    RELATED_PARTY_AI_SERVICE_FEES,
    ENTITY_SPLITTING,
    SECTOR_CLASSIFICATION_ARBITRAGE,
    CLOUD_COST_RELABELING,
    ROBOTICS_LEASING_AVOIDANCE,
    ARTIFICIAL_LOW_PROFIT_OR_AAVA,
}

COUNTERMEASURE_CATEGORIES = {
    "evidence_requirement",
    "grouped_entity_review",
    "transfer_pricing_review",
    "schedule_authority_review",
    "aava_deductibility_review",
    "capital_base_review",
    "customer_self_service_review",
    "offshore_attribution_review",
    "legal_policy_review",
    "external_calibration_required",
}

RESPONSE_TYPES = {
    "labour_relabelling",
    "token_human_oversight",
    "fake_qlc_inflation",
    "entity_splitting",
    "offshore_automation_service_routing",
    "related_party_ai_service_fees",
    "cloud_inference_relabelling",
    "robotics_leasing_shift",
    "customer_self_service_shift",
    "schedule_classification_arbitrage",
    "artificial_low_profit_or_aava",
    "platform_ip_royalty_routing",
    "open_source_ai_treatment_gap",
    "mixed_unit_apportionment_gaming",
}

PRESSURE_BASE = {
    "low": 0.20,
    "moderate": 0.45,
    "high": 0.65,
    "critical": 0.85,
    "low_placeholder_response_pressure": 0.20,
    "moderate_placeholder_response_pressure": 0.45,
    "high_placeholder_response_pressure": 0.65,
    "critical_review_required": 0.85,
}

COUNTERMEASURE_BY_RESPONSE_TYPE = {
    "labour_relabelling": ["evidence_requirement", "grouped_entity_review", "legal_policy_review"],
    "token_human_oversight": ["evidence_requirement", "grouped_entity_review", "legal_policy_review"],
    "fake_qlc_inflation": ["evidence_requirement", "grouped_entity_review"],
    "entity_splitting": ["grouped_entity_review", "legal_policy_review"],
    "offshore_automation_service_routing": [
        "offshore_attribution_review",
        "transfer_pricing_review",
        "legal_policy_review",
    ],
    "related_party_ai_service_fees": [
        "transfer_pricing_review",
        "aava_deductibility_review",
        "evidence_requirement",
    ],
    "cloud_inference_relabelling": [
        "aava_deductibility_review",
        "evidence_requirement",
        "transfer_pricing_review",
    ],
    "robotics_leasing_shift": [
        "capital_base_review",
        "aava_deductibility_review",
        "evidence_requirement",
    ],
    "customer_self_service_shift": [
        "customer_self_service_review",
        "schedule_authority_review",
        "legal_policy_review",
    ],
    "schedule_classification_arbitrage": ["schedule_authority_review", "legal_policy_review"],
    "artificial_low_profit_or_aava": [
        "aava_deductibility_review",
        "transfer_pricing_review",
        "grouped_entity_review",
    ],
    "platform_ip_royalty_routing": [
        "transfer_pricing_review",
        "offshore_attribution_review",
        "capital_base_review",
        "legal_policy_review",
    ],
    "open_source_ai_treatment_gap": [
        "legal_policy_review",
        "capital_base_review",
        "external_calibration_required",
    ],
    "mixed_unit_apportionment_gaming": [
        "schedule_authority_review",
        "evidence_requirement",
        "legal_policy_review",
    ],
}

FORBIDDEN_PREDICTION_LANGUAGE = [
    "firms will avoid",
    "taxpayers will avoid",
    "predicted taxpayer behaviour",
    "behavioural elasticity estimate",
    "validated compliance risk",
    "ato audit score",
    "real compliance score",
    "actual taxpayer response",
    "expected avoidance rate",
    "enforcement-ready",
    "penalty applies",
    "actual tax payable can be estimated",
    "economic validation is complete",
    "treasury validated",
    "ato validated",
    "official behavioural model",
]


@dataclass(frozen=True)
class BehaviouralResponseScenario:
    scenario_id: str
    scenario_name: str
    sector_schedule_id: str
    response_type: str
    description: str
    synthetic_triggers: list[str]
    linked_avoidance_flags: list[str]
    linked_countermeasures: list[str]
    placeholder_response_pressure: str
    requires_external_review: bool
    non_claims: list[str]
    pressure_basis: str = "multi_pathway"
    unresolved_new_flag: bool = False
    suppress_until_calibrated: bool = False
    suppression_calibration_dependencies: list[str] = field(default_factory=list)
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BehaviouralCountermeasure:
    category: str
    description: str
    review_owner_placeholder: str
    ready_for_operational_use: bool
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(BEHAVIOURAL_RESPONSE_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BehaviouralResponseResult:
    scenario_id: str
    scenario_name: str
    sector_schedule_id: str
    response_type: str
    linked_avoidance_flags: list[str]
    response_pressure_score: float
    response_pressure_band: str
    pressure_basis: str
    pressure_band_explanation: str
    review_status: str
    countermeasure_categories: list[str]
    countermeasures: list[BehaviouralCountermeasure]
    external_review_required: bool
    do_not_predict: bool
    do_not_score_real_taxpayer: bool
    firm_level_liability_logic_modified: bool
    main_reason: str
    calibration_blockers: list[str]
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(BEHAVIOURAL_RESPONSE_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BehaviouralResponseSummary:
    total_scenarios: int
    scenarios_by_response_type: dict[str, int]
    scenarios_by_pressure_band: dict[str, int]
    scenarios_by_review_status: dict[str, int]
    scenarios_requiring_external_review: int
    scenarios_requiring_transfer_pricing_review: int
    scenarios_requiring_grouped_entity_review: int
    scenarios_requiring_schedule_authority_review: int
    scenarios_requiring_aava_deductibility_review: int
    scenarios_requiring_capital_base_review: int
    scenarios_requiring_offshore_attribution_review: int
    scenarios_requiring_customer_self_service_review: int
    scenarios_suppress_until_calibrated: int
    firm_level_liability_logic_modified: bool
    calibration_blockers: list[str]
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(BEHAVIOURAL_RESPONSE_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _scenario_from_mapping(source: BehaviouralResponseScenario | dict[str, Any]) -> BehaviouralResponseScenario:
    if isinstance(source, BehaviouralResponseScenario):
        return source
    return BehaviouralResponseScenario(
        scenario_id=str(source["scenario_id"]),
        scenario_name=str(source["scenario_name"]),
        sector_schedule_id=str(source["sector_schedule_id"]),
        response_type=str(source["response_type"]),
        description=str(source["description"]),
        synthetic_triggers=[str(item) for item in source.get("synthetic_triggers", [])],
        linked_avoidance_flags=[str(item) for item in source.get("linked_avoidance_flags", [])],
        linked_countermeasures=[str(item) for item in source.get("linked_countermeasures", [])],
        placeholder_response_pressure=str(source["placeholder_response_pressure"]),
        requires_external_review=bool(source["requires_external_review"]),
        non_claims=[str(item) for item in source.get("non_claims", [])],
        pressure_basis=str(source.get("pressure_basis", "multi_pathway")),
        unresolved_new_flag=bool(source.get("unresolved_new_flag", False)),
        suppress_until_calibrated=bool(source.get("suppress_until_calibrated", False)),
        suppression_calibration_dependencies=[
            str(item) for item in source.get("suppression_calibration_dependencies", [])
        ],
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def _serialise_for_language_check(value: Any) -> str:
    return json.dumps(value, sort_keys=True).lower()


def _validate_no_prediction_language(scenario: BehaviouralResponseScenario) -> None:
    text = _serialise_for_language_check(scenario.to_jsonable())
    for phrase in FORBIDDEN_PREDICTION_LANGUAGE:
        if phrase in text:
            raise ValueError(f"{scenario.scenario_id} contains forbidden prediction or enforcement phrase: {phrase}")


def _validate_non_claims(scenario: BehaviouralResponseScenario) -> None:
    joined = " ".join(scenario.non_claims).lower()
    required_fragments = [
        "synthetic",
        "does not predict taxpayer behaviour",
        "does not modify firm-level carsf liability",
    ]
    missing = [fragment for fragment in required_fragments if fragment not in joined]
    if missing:
        raise ValueError(f"{scenario.scenario_id} missing non-claim fragments: {', '.join(missing)}")


def validate_behavioural_response_scenario(
    scenario: BehaviouralResponseScenario | dict[str, Any],
    schedule_ids: set[str],
) -> BehaviouralResponseScenario:
    """Validate one synthetic behavioural response scenario fail-closed."""

    scenario_obj = _scenario_from_mapping(scenario)
    required_strings = [
        "scenario_id",
        "scenario_name",
        "sector_schedule_id",
        "response_type",
        "description",
        "placeholder_response_pressure",
    ]
    for field_name in required_strings:
        if not getattr(scenario_obj, field_name):
            raise ValueError(f"behavioural response scenario missing required field: {field_name}")
    if scenario_obj.sector_schedule_id not in schedule_ids:
        raise ValueError(f"{scenario_obj.scenario_id} references missing sector schedule: {scenario_obj.sector_schedule_id}")
    if scenario_obj.response_type not in RESPONSE_TYPES:
        raise ValueError(f"{scenario_obj.scenario_id} has unknown response_type: {scenario_obj.response_type}")
    if scenario_obj.placeholder_response_pressure not in PRESSURE_BASE:
        raise ValueError(f"{scenario_obj.scenario_id} has unknown placeholder_response_pressure")
    if scenario_obj.pressure_basis not in {
        "single_pathway",
        "multi_pathway",
        "cross_border",
        "unresolved_legal_treatment",
        "calibration_suppressed",
    }:
        raise ValueError(f"{scenario_obj.scenario_id} has unknown pressure_basis")
    if not scenario_obj.synthetic_triggers:
        raise ValueError(f"{scenario_obj.scenario_id} must include synthetic_triggers")
    if not scenario_obj.linked_countermeasures:
        raise ValueError(f"{scenario_obj.scenario_id} must include linked_countermeasures")
    unknown_flags = [flag for flag in scenario_obj.linked_avoidance_flags if flag not in KNOWN_AVOIDANCE_FLAGS]
    if unknown_flags and not scenario_obj.unresolved_new_flag:
        raise ValueError(f"{scenario_obj.scenario_id} has unknown linked avoidance flags: {', '.join(unknown_flags)}")
    unknown_countermeasures = [
        item for item in scenario_obj.linked_countermeasures if item not in COUNTERMEASURE_CATEGORIES
    ]
    if unknown_countermeasures:
        raise ValueError(f"{scenario_obj.scenario_id} has unknown countermeasure categories: {', '.join(unknown_countermeasures)}")
    _validate_non_claims(scenario_obj)
    _validate_no_prediction_language(scenario_obj)
    return scenario_obj


def validate_behavioural_response_scenarios(
    scenarios: list[BehaviouralResponseScenario | dict[str, Any]],
    schedule_ids: set[str],
) -> list[BehaviouralResponseScenario]:
    if not scenarios:
        raise ValueError("behavioural response simulation requires at least one scenario")
    return [validate_behavioural_response_scenario(scenario, schedule_ids) for scenario in scenarios]


def _score_cap(value: float) -> float:
    return max(0.0, min(1.0, value))


def _band(score: float) -> str:
    if not math.isfinite(score):
        raise ValueError("response pressure score must be finite")
    if score < 0.25:
        return "low_placeholder_response_pressure"
    if score < 0.45:
        return "moderate_placeholder_response_pressure"
    if score < 0.70:
        return "high_placeholder_response_pressure"
    return "critical_review_required"


def _review_status(band: str, scenario: BehaviouralResponseScenario) -> str:
    if scenario.suppress_until_calibrated or scenario.suppression_calibration_dependencies:
        return "suppress_until_calibrated"
    if band == "critical_review_required":
        return "external_review_required"
    if band == "high_placeholder_response_pressure":
        return "strong_warning_required"
    if band == "moderate_placeholder_response_pressure":
        return "show_with_warning"
    return "prototype_discussion_only"


def _scenario_text(scenario: BehaviouralResponseScenario) -> str:
    return _serialise_for_language_check(
        {
            "response_type": scenario.response_type,
            "description": scenario.description,
            "synthetic_triggers": scenario.synthetic_triggers,
            "linked_countermeasures": scenario.linked_countermeasures,
        }
    )


def _stress_status(sector_stress_by_schedule: dict[str, Any] | None, schedule_id: str) -> str | None:
    if not sector_stress_by_schedule:
        return None
    value = sector_stress_by_schedule.get(schedule_id)
    if value is None:
        return None
    if isinstance(value, dict):
        return str(value.get("display_control_status")) if value.get("display_control_status") else None
    return str(getattr(value, "display_control_status", "")) or None


def _pressure_score(
    scenario: BehaviouralResponseScenario,
    sector_stress_by_schedule: dict[str, Any] | None,
) -> tuple[float, list[str]]:
    score = PRESSURE_BASE[scenario.placeholder_response_pressure]
    reasons = [f"Base pressure comes from declared placeholder pressure `{scenario.placeholder_response_pressure}`."]
    basis_adjustments = {
        "single_pathway": -0.10,
        "multi_pathway": 0.0,
        "cross_border": 0.05,
        "unresolved_legal_treatment": 0.08,
        "calibration_suppressed": 0.0,
    }
    basis_adjustment = basis_adjustments[scenario.pressure_basis]
    if basis_adjustment:
        score += basis_adjustment
        reasons.append(f"Pressure basis `{scenario.pressure_basis}` adjusts placeholder pressure by {basis_adjustment:+.2f}.")
    else:
        reasons.append(f"Pressure basis `{scenario.pressure_basis}` adds no standalone modifier.")
    text = _scenario_text(scenario)
    modifiers = [
        ("offshore", 0.10, "offshore routing wording adds review pressure"),
        ("related-party", 0.10, "related-party fee wording adds review pressure"),
        ("entity splitting", 0.10, "entity splitting wording adds review pressure"),
        ("schedule classification", 0.08, "schedule classification wording adds review pressure"),
        ("cloud", 0.08, "cloud or inference relabelling wording adds review pressure"),
        ("inference", 0.08, "cloud or inference relabelling wording adds review pressure"),
        ("customer self-service", 0.08, "customer self-service wording adds review pressure"),
        ("self-checkout", 0.08, "customer self-service wording adds review pressure"),
        ("robotics leasing", 0.08, "robotics leasing wording adds review pressure"),
        ("royalty", 0.10, "IP or royalty routing wording adds review pressure"),
        (" ip ", 0.10, "IP or royalty routing wording adds review pressure"),
        ("aasb 138", 0.10, "unresolved software, intangible, or AASB 138 wording adds review pressure"),
        ("intangible", 0.10, "unresolved software, intangible, or AASB 138 wording adds review pressure"),
        ("unresolved", 0.10, "unresolved software, intangible, or AASB 138 wording adds review pressure"),
    ]
    applied: set[str] = set()
    text_modifier = 0.0
    for term, amount, reason in modifiers:
        if term in text and reason not in applied:
            text_modifier += amount
            reasons.append(reason)
            applied.add(reason)
    text_modifier = min(0.20, text_modifier)
    if text_modifier:
        score += text_modifier
        reasons.append(f"Text modifiers are capped at {text_modifier:.2f} to avoid double-counting related pathway wording.")
    flag_modifier = min(0.10, len(scenario.linked_avoidance_flags) * 0.03)
    if flag_modifier:
        score += flag_modifier
        reasons.append(f"Linked avoidance flags add {flag_modifier:.2f} placeholder review pressure.")
    status = _stress_status(sector_stress_by_schedule, scenario.sector_schedule_id)
    if status == "external_review_required":
        score += 0.05
        reasons.append("Sector stress matrix external-review status adds placeholder review pressure.")
    elif status == "strong_warning_required":
        score += 0.03
        reasons.append("Sector stress matrix strong-warning status adds placeholder review pressure.")
    return _score_cap(score), reasons


def _countermeasures(scenario: BehaviouralResponseScenario) -> list[str]:
    mapped = COUNTERMEASURE_BY_RESPONSE_TYPE.get(scenario.response_type, [])
    return sorted(set(mapped) | set(scenario.linked_countermeasures))


def _countermeasure_detail(category: str) -> BehaviouralCountermeasure:
    return BehaviouralCountermeasure(
        category=category,
        description=f"{category} is a prototype review pathway only.",
        review_owner_placeholder="external policy, legal, ATO/Treasury methods, or calibration review",
        ready_for_operational_use=False,
        warnings=[
            "Countermeasure category is non-operative and does not implement enforcement.",
            "External calibration and legal/policy review are required before any operational design.",
        ],
    )


def evaluate_behavioural_response(
    scenario: BehaviouralResponseScenario | dict[str, Any],
    schedule_ids: set[str],
    sector_stress_by_schedule: dict[str, Any] | None = None,
) -> BehaviouralResponseResult:
    """Evaluate a synthetic behavioural response pathway."""

    scenario_obj = validate_behavioural_response_scenario(scenario, schedule_ids)
    score, reasons = _pressure_score(scenario_obj, sector_stress_by_schedule)
    band = _band(score)
    review_status = _review_status(band, scenario_obj)
    countermeasure_categories = _countermeasures(scenario_obj)
    external_review_required = (
        scenario_obj.requires_external_review
        or review_status in {"external_review_required", "suppress_until_calibrated"}
        or "external_calibration_required" in countermeasure_categories
    )
    blockers = list(scenario_obj.suppression_calibration_dependencies)
    blockers.extend(
        [
            f"{category}: external review required before operational use"
            for category in countermeasure_categories
            if category in {
                "external_calibration_required",
                "legal_policy_review",
                "transfer_pricing_review",
                "capital_base_review",
                "offshore_attribution_review",
            }
        ]
    )
    main_reason = f"{band} from deterministic placeholder scoring; {reasons[0]}"
    if review_status == "suppress_until_calibrated":
        main_reason = "Suppressed until calibration because required dependencies are unresolved."
    return BehaviouralResponseResult(
        scenario_id=scenario_obj.scenario_id,
        scenario_name=scenario_obj.scenario_name,
        sector_schedule_id=scenario_obj.sector_schedule_id,
        response_type=scenario_obj.response_type,
        linked_avoidance_flags=sorted(scenario_obj.linked_avoidance_flags),
        response_pressure_score=round(score, 4),
        response_pressure_band=band,
        pressure_basis=scenario_obj.pressure_basis,
        pressure_band_explanation=(
            f"{band} is based on declared placeholder pressure, pressure_basis={scenario_obj.pressure_basis}, "
            "capped text modifiers, linked avoidance flags, and sector stress display status. It is not a behavioural probability."
        ),
        review_status=review_status,
        countermeasure_categories=countermeasure_categories,
        countermeasures=[_countermeasure_detail(category) for category in countermeasure_categories],
        external_review_required=external_review_required,
        do_not_predict=True,
        do_not_score_real_taxpayer=True,
        firm_level_liability_logic_modified=False,
        main_reason=main_reason,
        calibration_blockers=sorted(set(blockers)),
        warnings=[
            "Synthetic pathway only; do not treat as a conduct forecast.",
            "Do not use this result for taxpayer-level scoring or compliance action.",
            *reasons,
        ],
    )


def evaluate_behavioural_responses(
    scenarios: list[BehaviouralResponseScenario | dict[str, Any]],
    schedule_ids: set[str],
    sector_stress_by_schedule: dict[str, Any] | None = None,
) -> list[BehaviouralResponseResult]:
    validated = validate_behavioural_response_scenarios(scenarios, schedule_ids)
    return [
        evaluate_behavioural_response(scenario, schedule_ids, sector_stress_by_schedule)
        for scenario in sorted(validated, key=lambda item: item.scenario_id)
    ]


def _count_by(rows: list[BehaviouralResponseResult], field_name: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        value = str(getattr(row, field_name))
        counts[value] = counts.get(value, 0) + 1
    return dict(sorted(counts.items()))


def _count_category(rows: list[BehaviouralResponseResult], category: str) -> int:
    return sum(1 for row in rows if category in row.countermeasure_categories)


def summarise_behavioural_responses(
    results: list[BehaviouralResponseResult | dict[str, Any]],
) -> BehaviouralResponseSummary:
    if not results:
        raise ValueError("behavioural response summary requires at least one result")
    rows = [
        result if isinstance(result, BehaviouralResponseResult) else BehaviouralResponseResult(**result)
        for result in results
    ]
    blockers = sorted(
        {
            f"{row.scenario_id}: {blocker}"
            for row in rows
            for blocker in row.calibration_blockers
        }
    )
    return BehaviouralResponseSummary(
        total_scenarios=len(rows),
        scenarios_by_response_type=_count_by(rows, "response_type"),
        scenarios_by_pressure_band=_count_by(rows, "response_pressure_band"),
        scenarios_by_review_status=_count_by(rows, "review_status"),
        scenarios_requiring_external_review=sum(1 for row in rows if row.external_review_required),
        scenarios_requiring_transfer_pricing_review=_count_category(rows, "transfer_pricing_review"),
        scenarios_requiring_grouped_entity_review=_count_category(rows, "grouped_entity_review"),
        scenarios_requiring_schedule_authority_review=_count_category(rows, "schedule_authority_review"),
        scenarios_requiring_aava_deductibility_review=_count_category(rows, "aava_deductibility_review"),
        scenarios_requiring_capital_base_review=_count_category(rows, "capital_base_review"),
        scenarios_requiring_offshore_attribution_review=_count_category(rows, "offshore_attribution_review"),
        scenarios_requiring_customer_self_service_review=_count_category(rows, "customer_self_service_review"),
        scenarios_suppress_until_calibrated=sum(1 for row in rows if row.review_status == "suppress_until_calibrated"),
        firm_level_liability_logic_modified=False,
        calibration_blockers=blockers,
        warnings=[
            "Summary counts are deterministic placeholder review counts only.",
            "Counts are not conduct forecasts, compliance scores, or enforcement priorities.",
        ],
    )
