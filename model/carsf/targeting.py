"""Prototype targeting mechanics for automation-transition support."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any

from .transfer_baseline import TRANSFER_BASELINE_NON_CLAIMS


@dataclass(frozen=True)
class TargetingCriteria:
    criteria_id: str
    target_group: str
    displaced_worker_required: bool
    retraining_required: bool
    income_test_placeholder: bool
    household_test_placeholder: bool
    recent_employment_link_required: bool
    automation_displacement_link_required: bool
    exclusion_rules: list[str] = field(default_factory=list)
    illustrative_placeholder_only: bool = True
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TargetPopulationInput:
    total_population: float
    displaced_workers: float
    reabsorbed_workers: float
    retraining_participants: float
    existing_support_recipients: float
    criteria: TargetingCriteria
    placeholder_basis: list[str] = field(default_factory=list)
    counts_may_overlap: bool = False

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["criteria"] = self.criteria.to_jsonable()
        return payload


@dataclass(frozen=True)
class TargetPopulationResult:
    criteria_id: str
    estimated_eligible_people: float
    estimated_excluded_people: float
    estimated_leakage_risk_people: float
    estimated_exclusion_risk_people: float
    targeting_risk_band: str
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(TRANSFER_BASELINE_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _finite_number(value: Any, field_name: str) -> float:
    numeric = float(value)
    if not isfinite(numeric):
        raise ValueError(f"{field_name} must be finite")
    return numeric


def _non_negative_number(value: Any, field_name: str) -> float:
    numeric = _finite_number(value, field_name)
    if numeric < 0:
        raise ValueError(f"{field_name} cannot be negative")
    return numeric


def _criteria_from_mapping(source: dict[str, Any]) -> TargetingCriteria:
    return TargetingCriteria(
        criteria_id=str(source["criteria_id"]),
        target_group=str(source.get("target_group", "placeholder_target_group")),
        displaced_worker_required=bool(source.get("displaced_worker_required", False)),
        retraining_required=bool(source.get("retraining_required", False)),
        income_test_placeholder=bool(source.get("income_test_placeholder", False)),
        household_test_placeholder=bool(source.get("household_test_placeholder", False)),
        recent_employment_link_required=bool(source.get("recent_employment_link_required", False)),
        automation_displacement_link_required=bool(source.get("automation_displacement_link_required", False)),
        exclusion_rules=[str(item) for item in source.get("exclusion_rules", [])],
        illustrative_placeholder_only=bool(source.get("illustrative_placeholder_only", True)),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def targeting_criteria_from_mapping(source: TargetingCriteria | dict[str, Any]) -> TargetingCriteria:
    if isinstance(source, TargetingCriteria):
        return source
    return _criteria_from_mapping(source)


def _input_from_mapping(source: dict[str, Any]) -> TargetPopulationInput:
    return TargetPopulationInput(
        total_population=source["total_population"],
        displaced_workers=source["displaced_workers"],
        reabsorbed_workers=source.get("reabsorbed_workers", 0.0),
        retraining_participants=source.get("retraining_participants", 0.0),
        existing_support_recipients=source.get("existing_support_recipients", 0.0),
        criteria=targeting_criteria_from_mapping(source["criteria"]),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
        counts_may_overlap=bool(source.get("counts_may_overlap", False)),
    )


def _risk_band(score: int) -> str:
    if score <= 0:
        return "low"
    if score <= 2:
        return "medium"
    if score <= 4:
        return "high"
    return "critical"


def evaluate_target_population(inputs: TargetPopulationInput | dict[str, Any]) -> TargetPopulationResult:
    """Estimate placeholder eligible population and targeting risk."""

    if isinstance(inputs, dict):
        inputs = _input_from_mapping(inputs)

    total_population = _non_negative_number(inputs.total_population, "total_population")
    displaced_workers = _non_negative_number(inputs.displaced_workers, "displaced_workers")
    reabsorbed_workers = _non_negative_number(inputs.reabsorbed_workers, "reabsorbed_workers")
    retraining_participants = _non_negative_number(inputs.retraining_participants, "retraining_participants")
    existing_support_recipients = _non_negative_number(inputs.existing_support_recipients, "existing_support_recipients")
    criteria = inputs.criteria
    if criteria.illustrative_placeholder_only is not True:
        raise ValueError("targeting criteria must be illustrative_placeholder_only")
    if not inputs.counts_may_overlap:
        for field_name, value in {
            "displaced_workers": displaced_workers,
            "reabsorbed_workers": reabsorbed_workers,
            "retraining_participants": retraining_participants,
            "existing_support_recipients": existing_support_recipients,
        }.items():
            if value > total_population:
                raise ValueError(f"{field_name} cannot exceed total_population unless counts_may_overlap is true")

    unreabsorbed_displaced = max(0.0, displaced_workers - reabsorbed_workers)
    if criteria.displaced_worker_required:
        eligible = unreabsorbed_displaced
    else:
        eligible = total_population
    if criteria.retraining_required:
        eligible = min(eligible, retraining_participants)
    if "exclude_existing_support_recipients" in criteria.exclusion_rules:
        eligible = max(0.0, eligible - min(existing_support_recipients, eligible))
    eligible = min(eligible, total_population)
    excluded_people = max(0.0, total_population - eligible)
    leakage_risk = max(0.0, eligible - displaced_workers)
    exclusion_risk = max(0.0, unreabsorbed_displaced - eligible)

    score = 0
    if not criteria.automation_displacement_link_required:
        score += 2
    if not criteria.displaced_worker_required:
        score += 1
    if criteria.income_test_placeholder:
        score += 1
    if criteria.household_test_placeholder:
        score += 1
    if criteria.retraining_required and displaced_workers > 0 and retraining_participants < displaced_workers * 0.5:
        score += 1
    if displaced_workers > 0 and eligible > displaced_workers * 1.5:
        score += 1
    if displaced_workers > 0 and exclusion_risk > displaced_workers * 0.25:
        score += 1

    warnings = [
        "Targeting estimate is placeholder-only and uses no person-level data.",
        "Household and income test fields are unresolved policy placeholders.",
    ]
    if leakage_risk > 0:
        warnings.append("Targeting may include people not directly counted as displaced workers.")
    if exclusion_risk > 0:
        warnings.append("Targeting may exclude some unreabsorbed displaced workers.")

    return TargetPopulationResult(
        criteria_id=criteria.criteria_id,
        estimated_eligible_people=eligible,
        estimated_excluded_people=excluded_people,
        estimated_leakage_risk_people=leakage_risk,
        estimated_exclusion_risk_people=exclusion_risk,
        targeting_risk_band=_risk_band(score),
        warnings=warnings,
    )
