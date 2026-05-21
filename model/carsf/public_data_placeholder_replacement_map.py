"""Placeholder replacement mapping for Build 32 public aggregate anchors.

This module maps existing realistic placeholders to Build 31 public aggregate
values. It does not load new data, complete calibration, validate CARSF,
determine tax payable, or modify firm-level CARSF liability logic.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


REPLACEMENT_STATUS_VALUES = {
    "replaced_by_public_aggregate_anchor",
    "narrowed_by_public_aggregate_anchor",
    "informed_by_public_aggregate_anchor",
    "still_placeholder_only",
    "blocked_until_restricted_data",
    "blocked_until_external_review",
    "cannot_replace_with_public_aggregate_data",
}

REPLACEMENT_CONFIDENCE_VALUES = {
    "direct_public_aggregate_anchor",
    "public_aggregate_bound_only",
    "contextual_public_aggregate_only",
    "placeholder_only",
    "blocked_by_required_restricted_data",
    "external_review_required",
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
}

CLAIM_LEVEL_VALUES = {
    "public_aggregate_anchor_only",
    "placeholder_narrowing_only",
    "contextual_anchor_only",
    "blocked_placeholder",
    "cannot_support_replacement",
}

PLACEHOLDER_REPLACEMENT_WARNING = (
    "This is a public data placeholder replacement map only. No new data is loaded by this build. Public aggregate "
    "data can anchor or narrow some placeholders, but does not calibrate the model. Replaced by public aggregate "
    "anchor does not mean validated. Narrowed by public aggregate anchor does not mean statistically estimated. "
    "Informed by public aggregate anchor does not mean representative. Placeholder-only items remain placeholders. "
    "Restricted-data blockers remain blockers. Calibration has not been completed. Public data does not prove the "
    "model works. This is not validation, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, "
    "not PBO costing, not economic validation, not welfare validation, not statistical validation, not operational "
    "readiness, not legal sufficiency, and not official status. It does not determine actual tax payable and does "
    "not modify firm-level CARSF liability."
)

PLACEHOLDER_REPLACEMENT_NON_CLAIMS = [
    PLACEHOLDER_REPLACEMENT_WARNING,
    "Build 32 uses Build 31 loaded public aggregate values only and does not add new public source values.",
    "Replacement, narrowing, and context labels are mapping labels only; they are not calibration or validation.",
    "Source candidates not loaded in Build 31 remain not loaded and future-only.",
]

FORBIDDEN_AFFIRMATIVE_PLACEHOLDER_REPLACEMENT_CLAIMS = [
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
    "does_not_show",
    "must_not_infer",
    "not_used_for",
    "what_must_not_be_claimed",
    "what this map does not mean",
    "does not mean",
]


@dataclass(frozen=True)
class PublicAggregateAnchor:
    value_id: str
    source_id: str
    metric_name: str
    value: int | float | str
    unit: str
    period: str
    geography: str
    source_locator: str
    claim_level: str
    data_status: str
    public_aggregate_only: bool
    restricted_data: bool
    personal_data: bool
    safe_for_repo_use: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PlaceholderReplacementCandidate:
    placeholder_id: str
    placeholder_name: str
    field_id: str
    current_placeholder_status: str
    anchor_strength: str
    blocked_by_restricted_data: bool
    candidate_source_reference_ids: list[str]
    candidate_extract_ids: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PlaceholderReplacementBlocker:
    blocker_id: str
    placeholder_id: str
    blocker_type: str
    blocker: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PlaceholderReplacementDecision:
    decision_id: str
    placeholder_id: str
    placeholder_name: str
    field_id: str
    current_placeholder_status: str
    replacement_status: str
    replacement_confidence: str
    claim_level: str
    linked_public_value_ids: list[str]
    linked_source_ids: list[str]
    what_changed: str
    what_did_not_change: str
    what_can_now_be_said: str
    what_must_not_be_claimed: list[str]
    remaining_blockers: list[str]
    evidence_needed_before_calibration: list[str]
    requires_external_review: bool
    requires_restricted_data: bool
    safe_for_repo_use: bool
    calibration_completed: bool
    validation_claimed: bool
    actual_tax_payable_determined: bool
    firm_level_liability_logic_modified: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PlaceholderReplacementSummary:
    placeholder_replacement_map_created: bool
    new_data_loaded: bool
    loaded_public_values_used: int
    placeholders_mapped: int
    placeholders_replaced_by_public_anchor: int
    placeholders_narrowed_by_public_anchor: int
    placeholders_informed_by_public_anchor: int
    placeholders_still_placeholder_only: int
    placeholders_blocked_until_restricted_data: int
    placeholders_blocked_until_external_review: int
    placeholders_cannot_replace_with_public_aggregate_data: int
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
class PublicDataPlaceholderReplacementResult:
    map_id: str
    map_name: str
    status: str
    non_claims: list[str]
    public_aggregate_anchors: list[PublicAggregateAnchor]
    placeholder_candidates: list[PlaceholderReplacementCandidate]
    replacement_decisions: list[PlaceholderReplacementDecision]
    replacement_blockers: list[PlaceholderReplacementBlocker]
    source_candidates_not_loaded: list[dict[str, Any]]
    future_build_33_requirements: list[str]
    summary: PlaceholderReplacementSummary

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


COMMON_MUST_NOT_CLAIM = [
    "calibration completed",
    "validation",
    "model works",
    "actual tax payable",
    "official status",
    "firm-level CARSF liability modification",
]


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
    window = text[max(0, phrase_start - 180) : phrase_start].lower()
    return any(marker in window for marker in NEGATIVE_CONTEXT_MARKERS)


def find_forbidden_affirmative_placeholder_replacement_claims(text: str) -> list[str]:
    lowered = text.lower()
    findings: list[str] = []
    for phrase in FORBIDDEN_AFFIRMATIVE_PLACEHOLDER_REPLACEMENT_CLAIMS:
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


def _public_anchor_from_mapping(source: dict[str, Any]) -> PublicAggregateAnchor:
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
            "source_locator",
            "claim_level",
            "data_status",
            "public_aggregate_only",
            "restricted_data",
            "personal_data",
            "safe_for_repo_use",
        ],
        "public aggregate value",
    )
    item = PublicAggregateAnchor(
        value_id=_non_empty(source["value_id"], "value_id"),
        source_id=_non_empty(source["source_id"], "source_id"),
        metric_name=_non_empty(source["metric_name"], "metric_name"),
        value=source["value"],
        unit=_non_empty(source["unit"], "unit"),
        period=_non_empty(source["period"], "period"),
        geography=_non_empty(source["geography"], "geography"),
        source_locator=_non_empty(source["source_locator"], "source_locator"),
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


def _placeholder_from_mapping(source: dict[str, Any]) -> PlaceholderReplacementCandidate:
    _required_mapping(
        source,
        [
            "anchor_id",
            "field_id",
            "placeholder_name",
            "anchor_source_reference_ids",
            "anchor_extract_ids",
            "current_placeholder_status",
            "anchor_strength",
            "blocked_by_restricted_data",
        ],
        "placeholder anchor",
    )
    item = PlaceholderReplacementCandidate(
        placeholder_id=_non_empty(source["anchor_id"], "anchor_id"),
        placeholder_name=_non_empty(source["placeholder_name"], "placeholder_name"),
        field_id=_non_empty(source["field_id"], "field_id"),
        current_placeholder_status=_non_empty(source["current_placeholder_status"], "current_placeholder_status"),
        anchor_strength=_non_empty(source["anchor_strength"], "anchor_strength"),
        blocked_by_restricted_data=_bool(source["blocked_by_restricted_data"], "blocked_by_restricted_data"),
        candidate_source_reference_ids=_list_of_strings(source["anchor_source_reference_ids"], "anchor_source_reference_ids"),
        candidate_extract_ids=_list_of_strings(source["anchor_extract_ids"], "anchor_extract_ids"),
    )
    if item.current_placeholder_status != "realistic_placeholder":
        raise ValueError(f"placeholder must remain realistic_placeholder: {item.placeholder_id}")
    return item


def _decision_plan(placeholder: PlaceholderReplacementCandidate) -> dict[str, Any]:
    plans: dict[str, dict[str, Any]] = {
        "anchor_opfte_minimum_wage": {
            "status": "replaced_by_public_aggregate_anchor",
            "confidence": "direct_public_aggregate_anchor",
            "claim": "public_aggregate_anchor_only",
            "values": [
                "fair_work_national_minimum_wage_hourly_2025",
                "fair_work_national_minimum_wage_weekly_2025",
            ],
            "changed": "The OPFTE wage placeholder is now linked to loaded public hourly and weekly national minimum wage anchors.",
            "unchanged": "OPFTE remains a placeholder benchmark; occupation mix, sector labour requirements, and schedule authority methods remain unresolved.",
            "can_say": "A public wage threshold is available as a direct aggregate anchor for OPFTE placeholder review.",
            "blockers": ["statistical_review_required", "restricted_tax_data_required", "public_aggregate_data_insufficient"],
            "evidence": ["occupation-specific hours", "sector-specific labour requirements", "schedule authority method"],
            "external": True,
            "restricted": True,
        },
        "anchor_hle_minimum_wage": {
            "status": "narrowed_by_public_aggregate_anchor",
            "confidence": "public_aggregate_bound_only",
            "claim": "placeholder_narrowing_only",
            "values": [
                "fair_work_national_minimum_wage_hourly_2025",
                "fair_work_national_minimum_wage_weekly_2025",
                "fair_work_casual_loading_2025",
            ],
            "changed": "The HLE labour-cost placeholder can be bounded by loaded wage and casual-loading public anchors.",
            "unchanged": "The HLE method remains unresolved and does not model actual human labour equivalents.",
            "can_say": "Public wage and casual-loading anchors can narrow the visible labour-cost placeholder context.",
            "blockers": ["statistical_review_required", "behavioural_elasticity_required", "public_aggregate_data_insufficient"],
            "evidence": ["human labour equivalent method", "occupation mix", "worker-hour evidence"],
            "external": True,
            "restricted": True,
        },
        "anchor_qlc_minimum_wage": {
            "status": "narrowed_by_public_aggregate_anchor",
            "confidence": "public_aggregate_bound_only",
            "claim": "placeholder_narrowing_only",
            "values": [
                "fair_work_national_minimum_wage_hourly_2025",
                "fair_work_national_minimum_wage_weekly_2025",
            ],
            "changed": "The QLC wage component can be bounded by loaded public wage thresholds.",
            "unchanged": "QLC weighting remains a realistic placeholder and does not establish task allocation, sector labour mix, or tax treatment.",
            "can_say": "Public wage thresholds can narrow the QLC wage-anchor placeholder context.",
            "blockers": ["statistical_review_required", "tax_review_required", "public_aggregate_data_insufficient"],
            "evidence": ["qualified labour contribution method", "task allocation evidence", "sector labour mix"],
            "external": True,
            "restricted": True,
        },
        "anchor_sector_schedule_source_reference": {
            "status": "informed_by_public_aggregate_anchor",
            "confidence": "contextual_public_aggregate_only",
            "claim": "contextual_anchor_only",
            "values": [
                "fair_work_national_minimum_wage_hourly_2025",
                "fair_work_casual_loading_2025",
            ],
            "changed": "Loaded wage anchors give sector-schedule placeholders labour-cost context.",
            "unchanged": "ABS labour source remains not loaded and sector schedules are not official rankings, calibrated schedules, or legal attribution rules.",
            "can_say": "Public wage anchors provide limited context for sector schedule placeholder review.",
            "blockers": ["statistical_review_required", "legal_review_required", "public_aggregate_data_insufficient"],
            "evidence": ["ABS public aggregate table extraction", "sector schedule authority method", "mixed-unit attribution"],
            "external": True,
            "restricted": True,
        },
        "anchor_fiscal_public_aggregates": {
            "status": "narrowed_by_public_aggregate_anchor",
            "confidence": "public_aggregate_bound_only",
            "claim": "placeholder_narrowing_only",
            "values": [
                "ato_large_corporate_income_tax_received_2022_23",
                "ato_large_corporate_entities_no_income_tax_percent_2022_23",
                "ato_total_tax_revenue_collected_2022_23",
                "ato_company_tax_revenue_2022_23",
                "treasury_total_receipts_2025_26_estimate",
                "treasury_taxation_receipts_2025_26_estimate",
            ],
            "changed": "Fiscal placeholders now link to loaded ATO and Budget receipt scale anchors.",
            "unchanged": "The fiscal trajectory remains a placeholder; no CARSF revenue pathway, fiscal incidence, Treasury modelling, or PBO costing is created.",
            "can_say": "Public aggregate revenue values can bound fiscal-scale placeholder discussion.",
            "blockers": ["economic_review_required", "restricted_tax_data_required", "behavioural_elasticity_required"],
            "evidence": ["CARSF behavioural response method", "revenue capture method", "fiscal incidence method"],
            "external": True,
            "restricted": True,
        },
        "anchor_payg_public_tax_stats": {
            "status": "informed_by_public_aggregate_anchor",
            "confidence": "contextual_public_aggregate_only",
            "claim": "contextual_anchor_only",
            "values": [
                "ato_total_tax_revenue_collected_2022_23",
                "ato_company_tax_revenue_2022_23",
            ],
            "changed": "PAYG erosion placeholders now reference loaded public tax aggregate context.",
            "unchanged": "Public tax totals do not identify AI-related PAYG erosion, taxpayer behaviour, or CARSF revenue.",
            "can_say": "Public tax aggregates provide context for PAYG erosion placeholder review.",
            "blockers": ["restricted_tax_data_required", "statistical_review_required", "public_aggregate_data_insufficient"],
            "evidence": ["employment-tax pathway method", "sector attribution", "behavioural response method"],
            "external": True,
            "restricted": True,
        },
        "anchor_super_guarantee_rate": {
            "status": "replaced_by_public_aggregate_anchor",
            "confidence": "direct_public_aggregate_anchor",
            "claim": "public_aggregate_anchor_only",
            "values": ["ato_super_guarantee_rate_2025_26"],
            "changed": "The superannuation guarantee placeholder now links to a loaded public rate setting.",
            "unchanged": "The field does not estimate individual superannuation, payroll, employer behaviour, or ATO guidance.",
            "can_say": "A public superannuation guarantee rate is available as a direct aggregate anchor for payment-interaction placeholder review.",
            "blockers": ["firm_confidential_data_required", "welfare_payment_records_required", "tax_review_required"],
            "evidence": ["wage base", "employer contribution records", "payment interaction method"],
            "external": True,
            "restricted": True,
        },
        "anchor_help_source_reference": {
            "status": "blocked_until_restricted_data",
            "confidence": "blocked_by_required_restricted_data",
            "claim": "blocked_placeholder",
            "values": [],
            "changed": "No Build 31 public HELP value was loaded; the HELP threshold source remains future-only.",
            "unchanged": "HELP repayment pressure remains placeholder-only and cannot estimate individual repayment pressure.",
            "can_say": "The field remains blocked until safe public extraction and authorised welfare or repayment evidence are available.",
            "blockers": ["welfare_payment_records_required", "household_microdata_required", "legal_review_required"],
            "evidence": ["income distribution", "individual repayment records", "eligibility law review"],
            "external": True,
            "restricted": True,
        },
        "anchor_payroll_tax_source_reference": {
            "status": "blocked_until_external_review",
            "confidence": "external_review_required",
            "claim": "blocked_placeholder",
            "values": [],
            "changed": "No Build 31 public state payroll threshold value was loaded; the source remains future-only.",
            "unchanged": "State payroll tax pressure remains placeholder-only and does not provide state tax advice or employer incidence.",
            "can_say": "The field remains a visible future replacement candidate only.",
            "blockers": ["firm_confidential_data_required", "tax_review_required", "public_aggregate_data_insufficient"],
            "evidence": ["jurisdiction-specific payroll base", "employer records", "tax-law review"],
            "external": True,
            "restricted": True,
        },
        "anchor_transition_public_reference": {
            "status": "informed_by_public_aggregate_anchor",
            "confidence": "contextual_public_aggregate_only",
            "claim": "contextual_anchor_only",
            "values": [
                "treasury_total_receipts_2025_26_estimate",
                "treasury_taxation_receipts_2025_26_estimate",
                "ato_super_guarantee_rate_2025_26",
            ],
            "changed": "Transition funding placeholders now link to loaded fiscal receipt and superannuation context anchors.",
            "unchanged": "Transition eligibility, payment design, welfare effects, and fiscal sufficiency remain unresolved.",
            "can_say": "Public receipt and threshold values can inform transition-funding placeholder discussion.",
            "blockers": ["welfare_payment_records_required", "economic_review_required", "legal_review_required"],
            "evidence": ["transition eligibility method", "payment administrative data", "fiscal design review"],
            "external": True,
            "restricted": True,
        },
        "anchor_uncertainty_source_reference_only": {
            "status": "cannot_replace_with_public_aggregate_data",
            "confidence": "blocked_by_required_restricted_data",
            "claim": "cannot_support_replacement",
            "values": [
                "ato_total_tax_revenue_collected_2022_23",
                "ato_company_tax_revenue_2022_23",
            ],
            "changed": "Public aggregate tax values provide context but cannot replace uncertainty placeholders.",
            "unchanged": "Uncertainty ranges remain deterministic placeholders and are not confidence intervals or statistical estimates.",
            "can_say": "Public aggregates are structurally insufficient for uncertainty replacement without reviewed statistical methods.",
            "blockers": ["household_microdata_required", "statistical_review_required", "public_aggregate_data_insufficient"],
            "evidence": ["statistical sampling frame", "confidence method", "authorised microdata"],
            "external": True,
            "restricted": True,
        },
    }
    try:
        return plans[placeholder.placeholder_id]
    except KeyError as exc:
        raise ValueError(f"no replacement decision plan for placeholder: {placeholder.placeholder_id}") from exc


def _decision_from_plan(
    placeholder: PlaceholderReplacementCandidate,
    plan: dict[str, Any],
    values_by_id: dict[str, PublicAggregateAnchor],
) -> PlaceholderReplacementDecision:
    status = _choice(str(plan["status"]), REPLACEMENT_STATUS_VALUES, "replacement_status")
    confidence = _choice(str(plan["confidence"]), REPLACEMENT_CONFIDENCE_VALUES, "replacement_confidence")
    claim = _choice(str(plan["claim"]), CLAIM_LEVEL_VALUES, "claim_level")
    linked_value_ids = _list_of_strings(plan["values"], "linked_public_value_ids", allow_empty=True)
    for value_id in linked_value_ids:
        if value_id not in values_by_id:
            raise ValueError(f"replacement decision links missing public value: {value_id}")
    if status in {
        "replaced_by_public_aggregate_anchor",
        "narrowed_by_public_aggregate_anchor",
        "informed_by_public_aggregate_anchor",
        "cannot_replace_with_public_aggregate_data",
    } and not linked_value_ids:
        raise ValueError(f"replacement decision requires linked public value ids: {placeholder.placeholder_id}")
    linked_source_ids = sorted({values_by_id[value_id].source_id for value_id in linked_value_ids})
    blockers = _list_of_strings(plan["blockers"], "remaining_blockers")
    for blocker in blockers:
        _choice(blocker, BLOCKER_TYPE_VALUES, "remaining_blockers")
    return PlaceholderReplacementDecision(
        decision_id=f"decision_{placeholder.placeholder_id}",
        placeholder_id=placeholder.placeholder_id,
        placeholder_name=placeholder.placeholder_name,
        field_id=placeholder.field_id,
        current_placeholder_status=placeholder.current_placeholder_status,
        replacement_status=status,
        replacement_confidence=confidence,
        claim_level=claim,
        linked_public_value_ids=linked_value_ids,
        linked_source_ids=linked_source_ids,
        what_changed=_non_empty(plan["changed"], "what_changed"),
        what_did_not_change=_non_empty(plan["unchanged"], "what_did_not_change"),
        what_can_now_be_said=_non_empty(plan["can_say"], "what_can_now_be_said"),
        what_must_not_be_claimed=COMMON_MUST_NOT_CLAIM,
        remaining_blockers=blockers,
        evidence_needed_before_calibration=_list_of_strings(plan["evidence"], "evidence_needed_before_calibration"),
        requires_external_review=_bool(plan["external"], "requires_external_review"),
        requires_restricted_data=_bool(plan["restricted"], "requires_restricted_data"),
        safe_for_repo_use=True,
        calibration_completed=False,
        validation_claimed=False,
        actual_tax_payable_determined=False,
        firm_level_liability_logic_modified=False,
    )


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


def build_public_data_placeholder_replacement_result(
    manifest: dict[str, Any],
    public_values_payload: dict[str, Any],
    placeholder_anchor_payload: list[dict[str, Any]],
    source_manifest: dict[str, Any],
) -> PublicDataPlaceholderReplacementResult:
    _required_mapping(
        manifest,
        [
            "map_id",
            "map_name",
            "status",
            "non_claims",
            "input_artifacts",
            "replacement_status_taxonomy",
            "replacement_confidence_taxonomy",
            "blocker_type_taxonomy",
            "claim_level_taxonomy",
            "required_mapping_rules",
            "required_placeholder_coverage",
            "required_public_value_coverage",
            "forbidden_claims",
            "build_33_requirements",
        ],
        "public placeholder replacement manifest",
    )
    if manifest["status"] != "public_data_placeholder_replacement_map_only":
        raise ValueError("replacement manifest status must be public_data_placeholder_replacement_map_only")
    for non_claim in PLACEHOLDER_REPLACEMENT_NON_CLAIMS[:1]:
        if non_claim not in manifest["non_claims"]:
            raise ValueError("replacement manifest missing required non-claim language")
    if set(manifest["replacement_status_taxonomy"]) != REPLACEMENT_STATUS_VALUES:
        raise ValueError("replacement_status_taxonomy does not match required values")
    if set(manifest["replacement_confidence_taxonomy"]) != REPLACEMENT_CONFIDENCE_VALUES:
        raise ValueError("replacement_confidence_taxonomy does not match required values")
    if set(manifest["blocker_type_taxonomy"]) != BLOCKER_TYPE_VALUES:
        raise ValueError("blocker_type_taxonomy does not match required values")
    if set(manifest["claim_level_taxonomy"]) != CLAIM_LEVEL_VALUES:
        raise ValueError("claim_level_taxonomy does not match required values")

    values = [_public_anchor_from_mapping(item) for item in public_values_payload.get("values", [])]
    if not values:
        raise ValueError("Build 31 public real aggregate values must be present")
    values_by_id = {item.value_id: item for item in values}
    if len(values_by_id) != len(values):
        raise ValueError("public aggregate value ids must be unique")
    required_public_values = set(_list_of_strings(manifest["required_public_value_coverage"], "required_public_value_coverage"))
    if required_public_values != set(values_by_id):
        missing = sorted(required_public_values - set(values_by_id))
        extra = sorted(set(values_by_id) - required_public_values)
        raise ValueError(f"public value coverage mismatch; missing={missing}; extra={extra}")

    placeholders = [_placeholder_from_mapping(item) for item in placeholder_anchor_payload]
    placeholders_by_id = {item.placeholder_id: item for item in placeholders}
    required_placeholders = set(_list_of_strings(manifest["required_placeholder_coverage"], "required_placeholder_coverage"))
    if required_placeholders != set(placeholders_by_id):
        missing = sorted(required_placeholders - set(placeholders_by_id))
        extra = sorted(set(placeholders_by_id) - required_placeholders)
        raise ValueError(f"placeholder coverage mismatch; missing={missing}; extra={extra}")

    decisions = [
        _decision_from_plan(placeholder, _decision_plan(placeholder), values_by_id)
        for placeholder in sorted(placeholders, key=lambda item: item.placeholder_id)
    ]
    used_public_values = {value_id for decision in decisions for value_id in decision.linked_public_value_ids}
    if used_public_values != set(values_by_id):
        missing = sorted(set(values_by_id) - used_public_values)
        raise ValueError(f"not all loaded public values are used by replacement decisions: {missing}")
    source_candidates = _source_candidates_not_loaded(source_manifest)
    candidate_source_ids = {item["source_id"] for item in source_candidates}
    treated_as_loaded = any(source_id in candidate_source_ids for decision in decisions for source_id in decision.linked_source_ids)
    if treated_as_loaded:
        raise ValueError("source candidates not loaded were treated as loaded")

    blockers: list[PlaceholderReplacementBlocker] = []
    for decision in decisions:
        for blocker_type in decision.remaining_blockers:
            blockers.append(
                PlaceholderReplacementBlocker(
                    blocker_id=f"{decision.placeholder_id}_{blocker_type}",
                    placeholder_id=decision.placeholder_id,
                    blocker_type=blocker_type,
                    blocker=f"{blocker_type} remains unresolved for {decision.placeholder_id}",
                )
            )
        if decision.calibration_completed or decision.validation_claimed or decision.actual_tax_payable_determined:
            raise ValueError(f"replacement decision has forbidden true flag: {decision.decision_id}")
        if decision.firm_level_liability_logic_modified:
            raise ValueError(f"replacement decision modifies firm-level liability logic: {decision.decision_id}")

    scan_manifest = {key: value for key, value in manifest.items() if key != "forbidden_claims"}
    forbidden_claims = find_forbidden_affirmative_placeholder_replacement_claims(str(scan_manifest))
    if forbidden_claims:
        raise ValueError(f"replacement manifest contains forbidden affirmative claims: {', '.join(forbidden_claims)}")

    summary = PlaceholderReplacementSummary(
        placeholder_replacement_map_created=True,
        new_data_loaded=False,
        loaded_public_values_used=len(used_public_values),
        placeholders_mapped=len(decisions),
        placeholders_replaced_by_public_anchor=sum(
            item.replacement_status == "replaced_by_public_aggregate_anchor" for item in decisions
        ),
        placeholders_narrowed_by_public_anchor=sum(
            item.replacement_status == "narrowed_by_public_aggregate_anchor" for item in decisions
        ),
        placeholders_informed_by_public_anchor=sum(
            item.replacement_status == "informed_by_public_aggregate_anchor" for item in decisions
        ),
        placeholders_still_placeholder_only=sum(item.replacement_status == "still_placeholder_only" for item in decisions),
        placeholders_blocked_until_restricted_data=sum(
            item.replacement_status == "blocked_until_restricted_data" for item in decisions
        ),
        placeholders_blocked_until_external_review=sum(
            item.replacement_status == "blocked_until_external_review" for item in decisions
        ),
        placeholders_cannot_replace_with_public_aggregate_data=sum(
            item.replacement_status == "cannot_replace_with_public_aggregate_data" for item in decisions
        ),
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
    return PublicDataPlaceholderReplacementResult(
        map_id=str(manifest["map_id"]),
        map_name=str(manifest["map_name"]),
        status=str(manifest["status"]),
        non_claims=list(manifest["non_claims"]),
        public_aggregate_anchors=values,
        placeholder_candidates=placeholders,
        replacement_decisions=decisions,
        replacement_blockers=blockers,
        source_candidates_not_loaded=source_candidates,
        future_build_33_requirements=_list_of_strings(manifest["build_33_requirements"], "build_33_requirements"),
        summary=summary,
    )
