"""Synthetic household budget scenarios for CARSF distributional previews."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any


DISTRIBUTIONAL_WARNING = (
    "These are synthetic household distributional scenarios only. They are not real household modelling, "
    "welfare advice, eligibility law, DSS/Services Australia modelling, ABS analysis, Treasury modelling, "
    "PBO costing, legal advice, tax advice, or economic validation."
)
DISTRIBUTIONAL_NON_CLAIMS = [
    DISTRIBUTIONAL_WARNING,
    "Synthetic household outputs use illustrative placeholders only and no real household or personal data.",
    "Distributional scenario outputs do not modify firm-level CARSF liability.",
]


@dataclass(frozen=True)
class SyntheticHousehold:
    household_id: str
    household_type: str
    adults: int
    children: int
    region_type: str
    income_band: str
    pre_displacement_income: float
    post_displacement_income: float
    existing_support_baseline: float
    housing_cost_placeholder: float
    essential_cost_placeholder: float
    debt_pressure_placeholder: float
    savings_buffer_placeholder: float
    illustrative_placeholder_only: bool = True
    synthetic_household_only: bool = True
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HouseholdBudgetResult:
    household_id: str
    household_type: str
    pre_displacement_income: float
    post_displacement_income: float
    income_loss: float
    existing_support_baseline: float
    total_basic_costs: float
    disposable_after_basic_costs: float
    savings_buffer_placeholder: float
    immediate_budget_gap: float
    budget_stress_band: str
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(DISTRIBUTIONAL_NON_CLAIMS))

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


def _non_negative_int(value: Any, field_name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be a non-negative integer")
    numeric = _finite_number(value, field_name)
    if numeric != int(numeric) or numeric < 0:
        raise ValueError(f"{field_name} must be a non-negative integer")
    return int(numeric)


def _household_from_mapping(source: dict[str, Any]) -> SyntheticHousehold:
    return SyntheticHousehold(
        household_id=str(source["household_id"]),
        household_type=str(source.get("household_type", "synthetic_household")),
        adults=source.get("adults", 0),
        children=source.get("children", 0),
        region_type=str(source.get("region_type", "placeholder_region")),
        income_band=str(source.get("income_band", "placeholder_income_band")),
        pre_displacement_income=source["pre_displacement_income"],
        post_displacement_income=source["post_displacement_income"],
        existing_support_baseline=source.get("existing_support_baseline", 0.0),
        housing_cost_placeholder=source.get("housing_cost_placeholder", 0.0),
        essential_cost_placeholder=source.get("essential_cost_placeholder", 0.0),
        debt_pressure_placeholder=source.get("debt_pressure_placeholder", 0.0),
        savings_buffer_placeholder=source.get("savings_buffer_placeholder", 0.0),
        illustrative_placeholder_only=bool(source.get("illustrative_placeholder_only", True)),
        synthetic_household_only=bool(source.get("synthetic_household_only", True)),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def synthetic_household_from_mapping(source: SyntheticHousehold | dict[str, Any]) -> SyntheticHousehold:
    if isinstance(source, SyntheticHousehold):
        return source
    return _household_from_mapping(source)


def _stress_band(score: int) -> str:
    if score <= 0:
        return "low"
    if score <= 2:
        return "medium"
    if score <= 4:
        return "high"
    return "critical"


def evaluate_household_budget(household: SyntheticHousehold | dict[str, Any]) -> HouseholdBudgetResult:
    """Evaluate one synthetic household budget stress preview."""

    if isinstance(household, dict):
        household = _household_from_mapping(household)

    if household.illustrative_placeholder_only is not True or household.synthetic_household_only is not True:
        raise ValueError("household must be marked illustrative_placeholder_only and synthetic_household_only")
    adults = _non_negative_int(household.adults, "adults")
    children = _non_negative_int(household.children, "children")
    if adults + children <= 0:
        raise ValueError("household must include at least one adult or child")
    pre_income = _non_negative_number(household.pre_displacement_income, "pre_displacement_income")
    post_income = _non_negative_number(household.post_displacement_income, "post_displacement_income")
    existing_support = _non_negative_number(household.existing_support_baseline, "existing_support_baseline")
    housing = _non_negative_number(household.housing_cost_placeholder, "housing_cost_placeholder")
    essentials = _non_negative_number(household.essential_cost_placeholder, "essential_cost_placeholder")
    debt = _non_negative_number(household.debt_pressure_placeholder, "debt_pressure_placeholder")
    savings = _non_negative_number(household.savings_buffer_placeholder, "savings_buffer_placeholder")
    if post_income > pre_income and "re_employed_gain" not in household.placeholder_basis:
        raise ValueError("post_displacement_income cannot exceed pre_displacement_income without re_employed_gain placeholder_basis")

    income_loss = max(0.0, pre_income - post_income)
    total_basic_costs = housing + essentials + debt
    disposable = post_income + existing_support - total_basic_costs
    immediate_gap = max(0.0, total_basic_costs - post_income - existing_support)
    income_loss_ratio = income_loss / pre_income if pre_income > 0 else 0.0
    gap_ratio = immediate_gap / total_basic_costs if total_basic_costs > 0 else 0.0
    savings_months_proxy = savings / (total_basic_costs / 12) if total_basic_costs > 0 else 12.0

    score = 0
    if income_loss_ratio >= 0.50:
        score += 2
    elif income_loss_ratio >= 0.20:
        score += 1
    if gap_ratio >= 0.40:
        score += 2
    elif immediate_gap > 0:
        score += 1
    if savings_months_proxy < 1:
        score += 2
    elif savings_months_proxy < 3:
        score += 1
    if children > 0 and immediate_gap > 0:
        score += 1

    return HouseholdBudgetResult(
        household_id=household.household_id,
        household_type=household.household_type,
        pre_displacement_income=pre_income,
        post_displacement_income=post_income,
        income_loss=income_loss,
        existing_support_baseline=existing_support,
        total_basic_costs=total_basic_costs,
        disposable_after_basic_costs=disposable,
        savings_buffer_placeholder=savings,
        immediate_budget_gap=immediate_gap,
        budget_stress_band=_stress_band(score),
        warnings=[
            "Household budget result is synthetic and placeholder-only.",
            "No real household, income, welfare, ABS, DSS, Services Australia, ATO, Treasury, PBO, or survey data is used.",
        ],
    )
