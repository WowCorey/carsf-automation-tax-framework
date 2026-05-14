"""Synthetic re-employment timing previews for displaced households."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any

from .households import DISTRIBUTIONAL_NON_CLAIMS, SyntheticHousehold, synthetic_household_from_mapping


@dataclass(frozen=True)
class ReemploymentPath:
    path_id: str
    household_id: str
    displacement_year: int
    expected_reemployment_months: int | None = None
    retraining_months: int | None = None
    partial_income_recovery_rate: float = 0.0
    full_income_recovery_rate: float = 0.0
    probability_band_placeholder: str = "not_assessable"
    illustrative_placeholder_only: bool = True
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReemploymentResult:
    path_id: str
    household_id: str
    months_without_full_income: int | None
    interim_income_recovery_amount: float
    full_income_recovery_amount: float
    reemployment_risk_band: str
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(DISTRIBUTIONAL_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _finite_number(value: Any, field_name: str) -> float:
    numeric = float(value)
    if not isfinite(numeric):
        raise ValueError(f"{field_name} must be finite")
    return numeric


def _non_negative_int_or_none(value: Any, field_name: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be a non-negative integer or None")
    numeric = _finite_number(value, field_name)
    if numeric != int(numeric) or numeric < 0:
        raise ValueError(f"{field_name} must be a non-negative integer or None")
    return int(numeric)


def _bounded_rate(value: Any, field_name: str) -> float:
    numeric = _finite_number(value, field_name)
    if not 0 <= numeric <= 1:
        raise ValueError(f"{field_name} must be in [0, 1]")
    return numeric


def _year(value: Any, field_name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be an integer")
    numeric = _finite_number(value, field_name)
    if numeric != int(numeric):
        raise ValueError(f"{field_name} must be an integer")
    return int(numeric)


def _path_from_mapping(source: dict[str, Any]) -> ReemploymentPath:
    return ReemploymentPath(
        path_id=str(source["path_id"]),
        household_id=str(source["household_id"]),
        displacement_year=_year(source["displacement_year"], "displacement_year"),
        expected_reemployment_months=source.get("expected_reemployment_months"),
        retraining_months=source.get("retraining_months"),
        partial_income_recovery_rate=source.get("partial_income_recovery_rate", 0.0),
        full_income_recovery_rate=source.get("full_income_recovery_rate", 0.0),
        probability_band_placeholder=str(source.get("probability_band_placeholder", "not_assessable")),
        illustrative_placeholder_only=bool(source.get("illustrative_placeholder_only", True)),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def reemployment_path_from_mapping(source: ReemploymentPath | dict[str, Any]) -> ReemploymentPath:
    if isinstance(source, ReemploymentPath):
        return source
    return _path_from_mapping(source)


def _risk_band(months: int | None, income_loss: float, full_recovery_rate: float) -> str:
    if months is None:
        return "critical" if income_loss > 0 else "not_assessable"
    score = 0
    if months > 18:
        score += 3
    elif months > 9:
        score += 2
    elif months > 3:
        score += 1
    if full_recovery_rate < 0.50 and income_loss > 0:
        score += 2
    elif full_recovery_rate < 0.80 and income_loss > 0:
        score += 1
    if score <= 0:
        return "low"
    if score == 1:
        return "medium"
    if score <= 3:
        return "high"
    return "critical"


def evaluate_reemployment_path(path: ReemploymentPath | dict[str, Any], household: SyntheticHousehold | dict[str, Any]) -> ReemploymentResult:
    """Evaluate placeholder re-employment timing risk for a synthetic household."""

    if isinstance(path, dict):
        path = _path_from_mapping(path)
    household_obj = synthetic_household_from_mapping(household)
    if path.illustrative_placeholder_only is not True:
        raise ValueError("reemployment path must be illustrative_placeholder_only")
    months = _non_negative_int_or_none(path.expected_reemployment_months, "expected_reemployment_months")
    retraining_months = _non_negative_int_or_none(path.retraining_months, "retraining_months")
    partial_rate = _bounded_rate(path.partial_income_recovery_rate, "partial_income_recovery_rate")
    full_rate = _bounded_rate(path.full_income_recovery_rate, "full_income_recovery_rate")
    if path.household_id != household_obj.household_id:
        raise ValueError("reemployment path household_id must match household")
    income_loss = max(0.0, float(household_obj.pre_displacement_income) - float(household_obj.post_displacement_income))
    months_without_full_income = months
    if months_without_full_income is not None and retraining_months is not None:
        months_without_full_income = max(months_without_full_income, retraining_months)

    return ReemploymentResult(
        path_id=path.path_id,
        household_id=path.household_id,
        months_without_full_income=months_without_full_income,
        interim_income_recovery_amount=income_loss * partial_rate,
        full_income_recovery_amount=income_loss * full_rate,
        reemployment_risk_band=_risk_band(months_without_full_income, income_loss, full_rate),
        warnings=[
            "Re-employment timing is a synthetic placeholder and not a labour-market forecast.",
            "No ABS, HILDA, DSS, Services Australia, Treasury, PBO, or employer records are used.",
        ],
    )
