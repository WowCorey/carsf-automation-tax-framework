"""Deterministic placeholder sensitivity sweeps for transition-payment funding."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any

from .payment_portfolio import PaymentPortfolioInput, evaluate_payment_portfolio
from .transition_payments import TRANSITION_PAYMENT_NON_CLAIMS


@dataclass(frozen=True)
class PaymentSensitivityPoint:
    parameter_name: str
    parameter_value: float
    total_program_cost: float
    funding_coverage_ratio: float | None
    residual_funding_gap: float
    affordability_band: str
    warnings: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PaymentSensitivityResult:
    sensitivity_id: str
    points: list[PaymentSensitivityPoint]
    min_residual_gap: float
    max_residual_gap: float
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(TRANSITION_PAYMENT_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["points"] = [point.to_jsonable() for point in self.points]
        return payload


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


def _non_negative_number(value: Any, field_name: str) -> float:
    numeric = _finite_number(value, field_name)
    if numeric < 0:
        raise ValueError(f"{field_name} cannot be negative")
    return numeric


def _to_mapping(base_input: PaymentPortfolioInput | dict[str, Any]) -> dict[str, Any]:
    if isinstance(base_input, PaymentPortfolioInput):
        return base_input.to_jsonable()
    return deepcopy(base_input)


def _apply_parameter(source: dict[str, Any], parameter_name: str, value: float) -> dict[str, Any]:
    adjusted = deepcopy(source)
    if parameter_name == "annual_payment_multiplier":
        multiplier = _non_negative_number(value, parameter_name)
        for design in adjusted["designs"]:
            design["annual_payment_per_person"] = float(design.get("annual_payment_per_person", 0.0)) * multiplier
    elif parameter_name == "annual_payment_per_person":
        payment = _non_negative_number(value, parameter_name)
        for design in adjusted["designs"]:
            design["annual_payment_per_person"] = payment
    elif parameter_name == "participation_rate":
        rate = _bounded_rate(value, parameter_name)
        for design in adjusted["designs"]:
            design["participation_rate"] = rate
    elif parameter_name == "population_base":
        adjusted["population_base"] = _non_negative_number(value, parameter_name)
    elif parameter_name == "displaced_workers":
        adjusted["displaced_workers"] = _non_negative_number(value, parameter_name)
    elif parameter_name == "automation_revenue_available":
        adjusted["automation_revenue_available"] = _non_negative_number(value, parameter_name)
    else:
        raise ValueError(f"unsupported payment sensitivity parameter: {parameter_name}")
    return adjusted


def run_payment_sensitivity(base_portfolio_input: PaymentPortfolioInput | dict[str, Any], parameter_grid: dict[str, list[float]]) -> PaymentSensitivityResult:
    """Run deterministic one-at-a-time transition-payment sensitivity sweeps."""

    base_mapping = _to_mapping(base_portfolio_input)
    if not isinstance(parameter_grid, dict):
        raise ValueError("parameter_grid must be a mapping")

    points: list[PaymentSensitivityPoint] = []
    for parameter_name in sorted(parameter_grid):
        values = parameter_grid[parameter_name]
        if not isinstance(values, list):
            raise ValueError(f"parameter_grid[{parameter_name}] must be a list")
        for value in sorted(values, key=float):
            numeric = _finite_number(value, f"{parameter_name} value")
            adjusted = _apply_parameter(base_mapping, parameter_name, numeric)
            result = evaluate_payment_portfolio(adjusted)
            points.append(
                PaymentSensitivityPoint(
                    parameter_name=parameter_name,
                    parameter_value=numeric,
                    total_program_cost=result.total_program_cost,
                    funding_coverage_ratio=result.funding_coverage_ratio,
                    residual_funding_gap=result.residual_funding_gap,
                    affordability_band=result.affordability_band,
                    warnings=["Payment sensitivity point is placeholder-only and not a welfare-policy claim."],
                )
            )

    residuals = [point.residual_funding_gap for point in points]
    return PaymentSensitivityResult(
        sensitivity_id=str(base_mapping.get("portfolio_id", "")),
        points=points,
        min_residual_gap=min(residuals) if residuals else 0.0,
        max_residual_gap=max(residuals) if residuals else 0.0,
        warnings=["Payment sensitivity does not modify firm-level CARSF liability."],
    )
