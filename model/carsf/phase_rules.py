"""Prototype phase-in and phase-out rules for transition support."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any


@dataclass(frozen=True)
class PhaseRule:
    rule_id: str
    phase_in_start_year: int
    phase_in_end_year: int
    phase_out_start_year: int | None = None
    phase_out_end_year: int | None = None
    minimum_payment_multiplier: float = 0.0
    maximum_payment_multiplier: float = 1.0
    taper_rate_placeholder: float = 0.0
    illustrative_placeholder_only: bool = True
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PhaseRuleYearResult:
    year: int
    payment_multiplier: float
    phase_status: str
    warnings: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _finite_number(value: Any, field_name: str) -> float:
    numeric = float(value)
    if not isfinite(numeric):
        raise ValueError(f"{field_name} must be finite")
    return numeric


def _bounded_rate(value: Any, field_name: str) -> float:
    numeric = _finite_number(value, field_name)
    if not 0 <= numeric <= 1:
        raise ValueError(f"{field_name} must be in [0, 1]")
    return numeric


def _year(value: Any, field_name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{field_name} must be an integer year")
    numeric = _finite_number(value, field_name)
    if numeric != int(numeric):
        raise ValueError(f"{field_name} must be an integer year")
    return int(numeric)


def _rule_from_mapping(source: dict[str, Any]) -> PhaseRule:
    return PhaseRule(
        rule_id=str(source["rule_id"]),
        phase_in_start_year=_year(source["phase_in_start_year"], "phase_in_start_year"),
        phase_in_end_year=_year(source["phase_in_end_year"], "phase_in_end_year"),
        phase_out_start_year=(
            None if source.get("phase_out_start_year") is None else _year(source["phase_out_start_year"], "phase_out_start_year")
        ),
        phase_out_end_year=(
            None if source.get("phase_out_end_year") is None else _year(source["phase_out_end_year"], "phase_out_end_year")
        ),
        minimum_payment_multiplier=source.get("minimum_payment_multiplier", 0.0),
        maximum_payment_multiplier=source.get("maximum_payment_multiplier", 1.0),
        taper_rate_placeholder=source.get("taper_rate_placeholder", 0.0),
        illustrative_placeholder_only=bool(source.get("illustrative_placeholder_only", True)),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def phase_rule_from_mapping(source: PhaseRule | dict[str, Any]) -> PhaseRule:
    if isinstance(source, PhaseRule):
        return source
    return _rule_from_mapping(source)


def _validate_rule(rule: PhaseRule) -> tuple[float, float]:
    if rule.illustrative_placeholder_only is not True:
        raise ValueError("phase rule must be illustrative_placeholder_only")
    if rule.phase_in_end_year < rule.phase_in_start_year:
        raise ValueError("phase_in_end_year must be >= phase_in_start_year")
    if (rule.phase_out_start_year is None) != (rule.phase_out_end_year is None):
        raise ValueError("phase_out_start_year and phase_out_end_year must both be supplied or both be absent")
    if rule.phase_out_start_year is not None and rule.phase_out_end_year is not None:
        if rule.phase_out_end_year < rule.phase_out_start_year:
            raise ValueError("phase_out_end_year must be >= phase_out_start_year")
    minimum = _bounded_rate(rule.minimum_payment_multiplier, "minimum_payment_multiplier")
    maximum = _bounded_rate(rule.maximum_payment_multiplier, "maximum_payment_multiplier")
    if minimum > maximum:
        raise ValueError("minimum_payment_multiplier cannot exceed maximum_payment_multiplier")
    _bounded_rate(rule.taper_rate_placeholder, "taper_rate_placeholder")
    return minimum, maximum


def _linear_multiplier(start: int, end: int, year: int, minimum: float, maximum: float, rising: bool) -> float:
    if start == end:
        return maximum if rising else minimum
    share = (year - start) / (end - start)
    if rising:
        return minimum + (maximum - minimum) * share
    return maximum - (maximum - minimum) * share


def evaluate_phase_rule(rule: PhaseRule | dict[str, Any], year: int) -> PhaseRuleYearResult:
    """Return placeholder payment multiplier for a year."""

    if isinstance(rule, dict):
        rule = _rule_from_mapping(rule)
    year_value = _year(year, "year")
    minimum, maximum = _validate_rule(rule)

    if year_value < rule.phase_in_start_year:
        status = "pre_phase_in"
        multiplier = 0.0
    elif year_value <= rule.phase_in_end_year:
        status = "phase_in"
        multiplier = _linear_multiplier(rule.phase_in_start_year, rule.phase_in_end_year, year_value, minimum, maximum, True)
    elif rule.phase_out_start_year is not None and year_value >= rule.phase_out_start_year:
        if year_value <= rule.phase_out_end_year:
            status = "phase_out"
            multiplier = _linear_multiplier(rule.phase_out_start_year, rule.phase_out_end_year, year_value, minimum, maximum, False)
        else:
            status = "ended"
            multiplier = 0.0
    else:
        status = "full"
        multiplier = maximum

    return PhaseRuleYearResult(
        year=year_value,
        payment_multiplier=multiplier,
        phase_status=status,
        warnings=["Phase-rule output is illustrative placeholder-only and not eligibility law."],
    )
