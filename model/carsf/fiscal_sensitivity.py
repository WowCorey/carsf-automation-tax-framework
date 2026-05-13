"""Placeholder sensitivity sweeps for national fiscal trajectories."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any

from .fiscal_trajectory import FiscalTrajectoryInput, run_fiscal_trajectory


FISCAL_SENSITIVITY_NON_CLAIMS = [
    "Fiscal sensitivity sweeps are deterministic placeholders and are not forecasts.",
    "No real elasticity, Treasury, ATO, ABS, DSS, PBO, legal, tax, or economic validation is implied.",
]


@dataclass(frozen=True)
class FiscalSensitivityPoint:
    parameter_name: str
    parameter_value: float
    cumulative_gap: float
    first_high_warning_year: int | None
    first_critical_warning_year: int | None
    warnings: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FiscalSensitivityResult:
    trajectory_id: str
    points: list[FiscalSensitivityPoint]
    min_gap: float
    max_gap: float
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(FISCAL_SENSITIVITY_NON_CLAIMS))

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


def _to_mapping(base_input: FiscalTrajectoryInput | dict[str, Any]) -> dict[str, Any]:
    if isinstance(base_input, FiscalTrajectoryInput):
        return base_input.to_jsonable()
    return deepcopy(base_input)


def _apply_parameter(source: dict[str, Any], parameter_name: str, value: float) -> dict[str, Any]:
    adjusted = deepcopy(source)
    if parameter_name == "annual_displacement_rate":
        adjusted["workforce"]["annual_displacement_rate"] = _bounded_rate(value, parameter_name)
    elif parameter_name == "annual_reabsorption_rate":
        adjusted["workforce"]["annual_reabsorption_rate"] = _bounded_rate(value, parameter_name)
    elif parameter_name == "automation_revenue_capture_multiplier":
        multiplier = _non_negative_number(value, parameter_name)
        adjusted["automation_revenue_captured_by_year"] = {
            int(year): float(amount) * multiplier
            for year, amount in adjusted.get("automation_revenue_captured_by_year", {}).items()
        }
    elif parameter_name == "average_support_payment_per_person":
        adjusted["average_support_payment_per_person"] = _non_negative_number(value, parameter_name)
    elif parameter_name == "average_payg_tax_per_worker":
        adjusted["workforce"]["average_payg_tax_per_worker"] = _non_negative_number(value, parameter_name)
    else:
        raise ValueError(f"unsupported fiscal sensitivity parameter: {parameter_name}")
    return adjusted


def run_fiscal_sensitivity(base_input: FiscalTrajectoryInput | dict[str, Any], parameter_grid: dict[str, list[float]]) -> FiscalSensitivityResult:
    """Run deterministic one-at-a-time fiscal sensitivity sweeps."""

    base_mapping = _to_mapping(base_input)
    if not isinstance(parameter_grid, dict):
        raise ValueError("parameter_grid must be a mapping")

    points: list[FiscalSensitivityPoint] = []
    for parameter_name in sorted(parameter_grid):
        values = parameter_grid[parameter_name]
        if not isinstance(values, list):
            raise ValueError(f"parameter_grid[{parameter_name}] must be a list")
        for value in sorted(values, key=float):
            numeric = _finite_number(value, f"{parameter_name} value")
            adjusted = _apply_parameter(base_mapping, parameter_name, numeric)
            result = run_fiscal_trajectory(adjusted)
            points.append(
                FiscalSensitivityPoint(
                    parameter_name=parameter_name,
                    parameter_value=numeric,
                    cumulative_gap=result.cumulative_total_public_sector_gap,
                    first_high_warning_year=result.first_high_warning_year,
                    first_critical_warning_year=result.first_critical_warning_year,
                    warnings=["Fiscal sensitivity point is placeholder-only and not a forecast."],
                )
            )

    gaps = [point.cumulative_gap for point in points]
    return FiscalSensitivityResult(
        trajectory_id=str(base_mapping.get("trajectory_id", "")),
        points=points,
        min_gap=min(gaps) if gaps else 0.0,
        max_gap=max(gaps) if gaps else 0.0,
        warnings=["Sensitivity sweeps do not modify firm-level liability."],
    )
