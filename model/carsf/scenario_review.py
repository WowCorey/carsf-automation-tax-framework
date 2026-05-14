"""Reviewed scenario display-control layer for synthetic uncertainty outputs."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


SCENARIO_REVIEW_WARNING = (
    "Reviewed scenario outputs are prototype display-control signals only. They are not statistical validation, "
    "population estimates, real household modelling, ABS/HILDA/Census analysis, DSS/Services Australia modelling, "
    "ATO analysis, Treasury modelling, PBO costing, welfare advice, eligibility law, legal advice, tax advice, "
    "or economic validation."
)

SCENARIO_REVIEW_NON_CLAIMS = [
    SCENARIO_REVIEW_WARNING,
    "Stable prototype discussion signals still require external calibration and methods review.",
    "Reviewed scenario outputs do not modify firm-level CARSF liability.",
]

HOUSEHOLD_REQUIRED_RANGES = ("residual_gap_range", "transition_support_range")
HOUSEHOLD_RANGE_FIELDS = (
    "residual_gap_range",
    "transition_support_range",
    "reemployment_months_range",
    "regional_stress_range",
    "payment_cliff_loss_range",
)
WEIGHTED_REQUIRED_RANGES = ("residual_gap_range", "high_critical_share_range")


@dataclass(frozen=True)
class ReviewedScenarioInput:
    review_id: str
    source_type: str
    source_result: dict[str, Any]
    scenario_name: str | None = None
    subgroup_id: str | None = None
    subgroup_name: str | None = None
    representative_of_real_population: bool = False
    total_synthetic_weight: float | None = None
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReviewedScenarioResult:
    review_id: str
    source_type: str
    subject_id: str
    subject_name: str
    risk_signal_stability: str | None
    low_case_shock_band: str | None
    base_case_shock_band: str | None
    high_case_shock_band: str | None
    residual_gap_stability: str | None
    high_critical_share_stability: str | None
    subgroup_range_sensitivity: str | None
    representative_of_real_population: bool
    total_synthetic_weight: float | None
    fragile_metrics: list[str]
    missing_ranges: list[str]
    review_signals: list[str]
    review_category: str
    display_level: str
    main_reason: str
    suppress_point_estimate: bool
    external_review_required: bool
    firm_level_liability_modified: bool = False
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(SCENARIO_REVIEW_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReviewedScenarioSummary:
    total_reviewed_outputs: int
    prototype_discussion_signal_count: int
    discussion_with_strong_warning_count: int
    range_sensitive_hidden_count: int
    fragile_suppressed_count: int
    non_interpretable_count: int
    missing_uncertainty_range_count: int
    external_review_required_count: int
    display_counts: dict[str, int]
    prototype_discussion_signals: list[str]
    suppressed_or_hidden_outputs: list[str]
    non_interpretable_outputs: list[str]
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(SCENARIO_REVIEW_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _input_from_mapping(source: ReviewedScenarioInput | dict[str, Any]) -> ReviewedScenarioInput:
    if isinstance(source, ReviewedScenarioInput):
        return source
    return ReviewedScenarioInput(
        review_id=str(source["review_id"]),
        source_type=str(source["source_type"]),
        source_result=dict(source["source_result"]),
        scenario_name=None if source.get("scenario_name") is None else str(source.get("scenario_name")),
        subgroup_id=None if source.get("subgroup_id") is None else str(source.get("subgroup_id")),
        subgroup_name=None if source.get("subgroup_name") is None else str(source.get("subgroup_name")),
        representative_of_real_population=bool(source.get("representative_of_real_population", False)),
        total_synthetic_weight=(
            None if source.get("total_synthetic_weight") is None else float(source.get("total_synthetic_weight"))
        ),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def _range_stability(range_result: Any) -> str | None:
    if not isinstance(range_result, dict):
        return None
    value = range_result.get("stability_band")
    return None if value is None else str(value)


def _range_metric_name(field_name: str, range_result: Any) -> str:
    if isinstance(range_result, dict) and range_result.get("metric_name"):
        return str(range_result["metric_name"])
    return field_name.replace("_range", "").replace("_", " ")


def _missing_ranges(source: dict[str, Any], required_ranges: tuple[str, ...]) -> list[str]:
    return [field_name for field_name in required_ranges if not isinstance(source.get(field_name), dict)]


def _fragile_metrics(source: dict[str, Any], range_fields: tuple[str, ...]) -> list[str]:
    fragile = []
    for field_name in range_fields:
        range_result = source.get(field_name)
        if _range_stability(range_result) == "fragile":
            fragile.append(_range_metric_name(field_name, range_result))
    return sorted(set(fragile))


def _not_assessable_required_ranges(source: dict[str, Any], required_ranges: tuple[str, ...]) -> list[str]:
    return [
        _range_metric_name(field_name, source.get(field_name))
        for field_name in required_ranges
        if _range_stability(source.get(field_name)) == "not_assessable"
    ]


def _suppresses(display_level: str) -> bool:
    return display_level in {"hide_point_estimate", "hide_until_calibrated", "external_review_only"}


def _household_review(input_obj: ReviewedScenarioInput) -> ReviewedScenarioResult:
    source = input_obj.source_result
    subject_id = str(source.get("scenario_id") or input_obj.review_id)
    subject_name = input_obj.scenario_name or subject_id
    missing = _missing_ranges(source, HOUSEHOLD_REQUIRED_RANGES)
    fragile = _fragile_metrics(source, HOUSEHOLD_RANGE_FIELDS)
    not_assessable_ranges = _not_assessable_required_ranges(source, HOUSEHOLD_REQUIRED_RANGES)
    stability = str(source.get("risk_signal_stability") or "not_assessable")
    warnings = [
        "Reviewed household scenario output is synthetic and controls display only.",
        "Firm-level CARSF liability is not modified by reviewed scenario classification.",
    ]
    signals = [stability]

    if missing:
        category = "missing_uncertainty_range"
        display_level = "external_review_only"
        reason = "Required household uncertainty range is missing."
        signals.append("missing_range")
    elif not_assessable_ranges or stability == "not_assessable":
        category = "non_interpretable_until_calibrated"
        display_level = "hide_until_calibrated"
        reason = "One or more required household uncertainty ranges is not assessable without calibration."
        signals.append("not_assessable")
    elif stability == "range_sensitive":
        category = "range_sensitive_do_not_use_as_point_estimate"
        display_level = "hide_point_estimate"
        reason = "Low/base/high cases cross risk bands, so the point estimate should not be used."
        signals.append("range_sensitive")
    elif stability == "stable_high_risk" and fragile:
        category = "discussion_with_strong_warning"
        display_level = "show_with_warning"
        reason = "Stable high-risk signal exists, but primary uncertainty metrics include fragile ranges."
        signals.extend(["stable_high_risk", "fragile"])
    elif stability == "stable_high_risk":
        category = "prototype_discussion_signal"
        display_level = "show_with_warning"
        reason = "Risk remains high across the deterministic low/base/high placeholder range."
        signals.append("stable_high_risk")
    elif stability == "stable_low_risk" and fragile:
        category = "discussion_with_strong_warning"
        display_level = "show_with_warning"
        reason = "Low-risk signal is stable, but fragile primary metrics require strong warnings."
        signals.extend(["stable_low_risk", "fragile"])
    elif stability == "stable_low_risk":
        category = "prototype_discussion_signal"
        display_level = "show_with_warning"
        reason = "Risk remains low or medium across the deterministic low/base/high placeholder range."
        signals.append("stable_low_risk")
    elif fragile:
        category = "fragile_suppress_point_estimate"
        display_level = "hide_point_estimate"
        reason = "Fragile uncertainty metrics make the point estimate unsuitable for headline display."
        signals.append("fragile")
    else:
        category = "non_interpretable_until_calibrated"
        display_level = "hide_until_calibrated"
        reason = "Household scenario review state is not interpretable until external calibration and methods review."
        signals.append("not_calibrated")

    if fragile:
        warnings.append("One or more household uncertainty metrics is fragile; point estimates require de-emphasis.")
    if missing:
        warnings.append("Missing household uncertainty ranges require external review before interpretation.")
    if category == "prototype_discussion_signal":
        warnings.append("Prototype discussion signals still require external calibration and methods review.")

    return ReviewedScenarioResult(
        review_id=input_obj.review_id,
        source_type="household",
        subject_id=subject_id,
        subject_name=subject_name,
        risk_signal_stability=stability,
        low_case_shock_band=None if source.get("low_case_shock_band") is None else str(source.get("low_case_shock_band")),
        base_case_shock_band=None if source.get("base_case_shock_band") is None else str(source.get("base_case_shock_band")),
        high_case_shock_band=None if source.get("high_case_shock_band") is None else str(source.get("high_case_shock_band")),
        residual_gap_stability=_range_stability(source.get("residual_gap_range")),
        high_critical_share_stability=None,
        subgroup_range_sensitivity=None,
        representative_of_real_population=False,
        total_synthetic_weight=None,
        fragile_metrics=fragile,
        missing_ranges=missing,
        review_signals=sorted(set(signals)),
        review_category=category,
        display_level=display_level,
        main_reason=reason,
        suppress_point_estimate=_suppresses(display_level),
        external_review_required=True,
        warnings=warnings,
    )


def _weighted_review(input_obj: ReviewedScenarioInput) -> ReviewedScenarioResult:
    source = input_obj.source_result
    subject_id = input_obj.subgroup_id or str(source.get("subgroup_id") or input_obj.review_id)
    subject_name = input_obj.subgroup_name or str(source.get("subgroup_name") or subject_id)
    missing = _missing_ranges(source, WEIGHTED_REQUIRED_RANGES)
    residual_stability = _range_stability(source.get("residual_gap_range"))
    share_stability = _range_stability(source.get("high_critical_share_range"))
    subgroup_sensitivity = str(source.get("subgroup_range_sensitivity") or "not_assessable")
    total_weight = input_obj.total_synthetic_weight
    scenario_count = source.get("scenario_count")
    representative = bool(source.get("representative_of_real_population", input_obj.representative_of_real_population))
    warnings = [
        "Reviewed weighted subgroup output is synthetic and controls display only.",
        "Synthetic subgroup output is not population representative.",
        "Firm-level CARSF liability is not modified by weighted subgroup review.",
    ]
    signals = [subgroup_sensitivity, "not_representative"]

    zero_or_unmatched = (total_weight is not None and total_weight == 0) or scenario_count == 0
    if missing:
        category = "missing_uncertainty_range"
        display_level = "external_review_only"
        reason = "Required weighted subgroup uncertainty range is missing."
        signals.append("missing_range")
    elif zero_or_unmatched:
        category = "non_interpretable_until_calibrated"
        display_level = "hide_until_calibrated"
        reason = "Subgroup has zero synthetic weight or no matched scenarios."
        signals.append("not_assessable")
    elif subgroup_sensitivity == "fragile":
        category = "fragile_suppress_point_estimate"
        display_level = "hide_point_estimate"
        reason = "Weighted subgroup range sensitivity is fragile; suppress the point estimate."
        signals.append("fragile")
    elif subgroup_sensitivity == "not_assessable" or residual_stability == "not_assessable" or share_stability == "not_assessable":
        category = "non_interpretable_until_calibrated"
        display_level = "hide_until_calibrated"
        reason = "Weighted subgroup output is not assessable without calibration."
        signals.append("not_assessable")
    elif residual_stability in {"stable", "moderately_sensitive"} and share_stability in {"stable", "moderately_sensitive"}:
        category = "prototype_discussion_signal"
        display_level = "show_with_warning"
        reason = "Required subgroup ranges are stable or moderately sensitive and no required range is missing."
        signals.append("stable_high_risk")
    else:
        category = "range_sensitive_do_not_use_as_point_estimate"
        display_level = "hide_point_estimate"
        reason = "Weighted subgroup range output is sensitive enough that a point estimate should be hidden."
        signals.append("range_sensitive")

    if missing:
        warnings.append("Missing weighted subgroup uncertainty ranges require external review before interpretation.")
    if subgroup_sensitivity == "fragile":
        warnings.append("Fragile weighted subgroup output should not be presented as a clean point estimate.")
    if zero_or_unmatched:
        warnings.append("Zero-weight or unmatched subgroup output is non-interpretable until calibrated.")
    if representative is not False:
        warnings.append("Representative status was not explicitly false; review required.")

    return ReviewedScenarioResult(
        review_id=input_obj.review_id,
        source_type="weighted_subgroup",
        subject_id=subject_id,
        subject_name=subject_name,
        risk_signal_stability=None,
        low_case_shock_band=None,
        base_case_shock_band=None,
        high_case_shock_band=None,
        residual_gap_stability=residual_stability,
        high_critical_share_stability=share_stability,
        subgroup_range_sensitivity=subgroup_sensitivity,
        representative_of_real_population=False,
        total_synthetic_weight=total_weight,
        fragile_metrics=["weighted subgroup range"] if subgroup_sensitivity == "fragile" else [],
        missing_ranges=missing,
        review_signals=sorted(set(signals)),
        review_category=category,
        display_level=display_level,
        main_reason=reason,
        suppress_point_estimate=_suppresses(display_level),
        external_review_required=True,
        warnings=warnings,
    )


def review_scenario(inputs: ReviewedScenarioInput | dict[str, Any]) -> ReviewedScenarioResult:
    """Classify a household or weighted subgroup output for prototype display control."""

    input_obj = _input_from_mapping(inputs)
    if input_obj.source_type == "household":
        return _household_review(input_obj)
    if input_obj.source_type == "weighted_subgroup":
        return _weighted_review(input_obj)
    raise ValueError(f"unknown scenario review source_type: {input_obj.source_type}")


def summarise_reviewed_scenarios(
    results: list[ReviewedScenarioResult | dict[str, Any]],
) -> ReviewedScenarioSummary:
    """Summarise reviewed scenario display-control classifications."""

    if not results:
        raise ValueError("reviewed scenario summary requires at least one result")

    rows = [
        result if isinstance(result, ReviewedScenarioResult) else ReviewedScenarioResult(**result)
        for result in results
    ]
    category_counts = {
        "prototype_discussion_signal": 0,
        "discussion_with_strong_warning": 0,
        "range_sensitive_do_not_use_as_point_estimate": 0,
        "fragile_suppress_point_estimate": 0,
        "non_interpretable_until_calibrated": 0,
        "missing_uncertainty_range": 0,
    }
    display_counts: dict[str, int] = {}
    for row in rows:
        if row.review_category in category_counts:
            category_counts[row.review_category] += 1
        display_counts[row.display_level] = display_counts.get(row.display_level, 0) + 1

    prototype_signals = sorted(
        row.subject_name
        for row in rows
        if row.review_category in {"prototype_discussion_signal", "discussion_with_strong_warning"}
    )
    suppressed = sorted(
        row.subject_name
        for row in rows
        if row.display_level in {"hide_point_estimate", "external_review_only"}
    )
    non_interpretable = sorted(
        row.subject_name
        for row in rows
        if row.review_category in {"non_interpretable_until_calibrated", "missing_uncertainty_range"}
    )
    warnings = [
        "Reviewed scenario summary is a prototype display-control summary only.",
        "No reviewed scenario output is representative of a real population.",
        "Reviewed scenario classifications do not modify firm-level CARSF liability.",
    ]
    return ReviewedScenarioSummary(
        total_reviewed_outputs=len(rows),
        prototype_discussion_signal_count=category_counts["prototype_discussion_signal"],
        discussion_with_strong_warning_count=category_counts["discussion_with_strong_warning"],
        range_sensitive_hidden_count=category_counts["range_sensitive_do_not_use_as_point_estimate"],
        fragile_suppressed_count=category_counts["fragile_suppress_point_estimate"],
        non_interpretable_count=category_counts["non_interpretable_until_calibrated"],
        missing_uncertainty_range_count=category_counts["missing_uncertainty_range"],
        external_review_required_count=sum(1 for row in rows if row.external_review_required),
        display_counts=dict(sorted(display_counts.items())),
        prototype_discussion_signals=prototype_signals,
        suppressed_or_hidden_outputs=suppressed,
        non_interpretable_outputs=non_interpretable,
        warnings=warnings,
    )
