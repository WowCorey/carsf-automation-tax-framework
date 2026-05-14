"""Synthetic household weighting validation for distributional previews."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any


HOUSEHOLD_WEIGHTING_WARNING = (
    "These are synthetic household weighting outputs only. They are not population estimates, real "
    "distributional modelling, ABS/HILDA/Census analysis, DSS/Services Australia modelling, Treasury "
    "modelling, PBO costing, welfare advice, eligibility law, legal advice, tax advice, or economic validation."
)
HOUSEHOLD_WEIGHTING_NON_CLAIMS = [
    HOUSEHOLD_WEIGHTING_WARNING,
    "Synthetic household weights are illustrative placeholders and are not representative of real households.",
    "Household weighting outputs do not modify firm-level CARSF liability.",
]


@dataclass(frozen=True)
class HouseholdWeight:
    scenario_id: str
    subgroup_id: str
    weight_value: float
    weight_basis: str
    calibrated: bool = False
    calibration_source: str | None = None
    illustrative_placeholder_only: bool = True
    synthetic_weight_only: bool = True
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HouseholdWeightResult:
    scenario_id: str
    subgroup_id: str
    weight_value: float
    calibrated: bool
    usable_for_real_world_claims: bool
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(HOUSEHOLD_WEIGHTING_NON_CLAIMS))

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


def household_weight_from_mapping(source: HouseholdWeight | dict[str, Any]) -> HouseholdWeight:
    if isinstance(source, HouseholdWeight):
        return source
    return HouseholdWeight(
        scenario_id=str(source["scenario_id"]),
        subgroup_id=str(source["subgroup_id"]),
        weight_value=source["weight_value"],
        weight_basis=str(source.get("weight_basis", "synthetic placeholder weight")),
        calibrated=bool(source.get("calibrated", False)),
        calibration_source=None if source.get("calibration_source") is None else str(source.get("calibration_source")),
        illustrative_placeholder_only=bool(source.get("illustrative_placeholder_only", True)),
        synthetic_weight_only=bool(source.get("synthetic_weight_only", True)),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def _validate_calibration_source(source: str | None) -> None:
    if source is None:
        return
    lowered = source.lower()
    allowed_markers = ("placeholder", "synthetic", "not_collected", "external_not_in_repo")
    if not any(marker in lowered for marker in allowed_markers):
        raise ValueError("calibration_source must not embed a real data source in this prototype")


def evaluate_household_weight(weight: HouseholdWeight | dict[str, Any]) -> HouseholdWeightResult:
    """Validate one synthetic household weight."""

    weight_obj = household_weight_from_mapping(weight)
    if weight_obj.illustrative_placeholder_only is not True or weight_obj.synthetic_weight_only is not True:
        raise ValueError("household weight must be illustrative_placeholder_only and synthetic_weight_only")
    _validate_calibration_source(weight_obj.calibration_source)
    weight_value = _non_negative_number(weight_obj.weight_value, "weight_value")
    warnings = [
        "Household weight is synthetic placeholder-only and not population representative.",
        "No real household, ABS, HILDA, Census, DSS, Services Australia, ATO, Treasury, PBO, welfare, income, or survey data is embedded.",
    ]
    if weight_obj.calibrated:
        warnings.append("calibrated=true is recorded as metadata only; it does not create validation inside this prototype.")
    return HouseholdWeightResult(
        scenario_id=weight_obj.scenario_id,
        subgroup_id=weight_obj.subgroup_id,
        weight_value=weight_value,
        calibrated=weight_obj.calibrated,
        usable_for_real_world_claims=False,
        warnings=warnings,
    )
