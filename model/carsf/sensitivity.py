"""Placeholder sensitivity sweeps for CARSF burden and incidence guardrails."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any

from .incidence import IncidenceAssumption, evaluate_tax_incidence


SENSITIVITY_NON_CLAIMS = [
    "Sensitivity sweeps are placeholder-only and do not claim real elasticity or market behaviour.",
    "No economic, investment, Treasury, ATO, legal, or tax validation is implied.",
    "Sensitivity sweeps do not automatically modify final liability.",
]


@dataclass(frozen=True)
class SensitivityPoint:
    parameter_name: str
    parameter_value: float
    liability_preview: float
    effective_burden_rate: float | None
    incidence_result: dict[str, Any]
    warnings: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SensitivitySweepResult:
    example_id: str
    sweep_name: str
    points: list[SensitivityPoint]
    min_liability: float
    max_liability: float
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(SENSITIVITY_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["points"] = [point.to_jsonable() for point in self.points]
        return payload


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


def _bounded_rate(value: Any, field_name: str) -> float:
    numeric = _finite_number(value, field_name)
    if not 0 <= numeric <= 1:
        raise ValueError(f"{field_name} must be in [0, 1]")
    return numeric


def _build_result(example_id: str, sweep_name: str, points: list[SensitivityPoint]) -> SensitivitySweepResult:
    liabilities = [point.liability_preview for point in points]
    return SensitivitySweepResult(
        example_id=example_id,
        sweep_name=sweep_name,
        points=points,
        min_liability=min(liabilities) if liabilities else 0.0,
        max_liability=max(liabilities) if liabilities else 0.0,
        warnings=["Sensitivity values are illustrative placeholders only."],
    )


def sweep_pass_through(liability: float, rates: list[float], example_id: str = "") -> SensitivitySweepResult:
    liability_value = _non_negative_number(liability, "liability")
    points: list[SensitivityPoint] = []
    for index, rate in enumerate(rates):
        bounded = _bounded_rate(rate, f"rates[{index}]")
        incidence = evaluate_tax_incidence(
            liability_value,
            IncidenceAssumption(
                pass_through_rate=bounded,
                worker_pressure_rate=0.0,
                supplier_pressure_rate=0.0,
                capital_absorption_rate=0.0,
                assumption_basis="placeholder pass-through sensitivity",
                illustrative_placeholder_only=True,
            ),
        )
        points.append(
            SensitivityPoint(
                parameter_name="pass_through_rate",
                parameter_value=bounded,
                liability_preview=liability_value,
                effective_burden_rate=None,
                incidence_result=incidence.to_jsonable(),
                warnings=["No real pass-through elasticity is claimed."],
            )
        )
    return _build_result(example_id, "pass_through_rate_sweep", points)


def sweep_liability_cap(aava: float, raw_liability: float, cap_rates: list[float], example_id: str = "") -> SensitivitySweepResult:
    aava_value = _non_negative_number(aava, "aava")
    raw = _non_negative_number(raw_liability, "raw_liability")
    points: list[SensitivityPoint] = []
    for index, rate in enumerate(cap_rates):
        bounded = _bounded_rate(rate, f"cap_rates[{index}]")
        liability_preview = min(raw, bounded * aava_value)
        incidence = evaluate_tax_incidence(
            liability_preview,
            {
                "pass_through_rate": 0.25,
                "worker_pressure_rate": 0.10,
                "supplier_pressure_rate": 0.05,
                "capital_absorption_rate": 0.20,
                "assumption_basis": "placeholder cap sensitivity incidence allocation",
                "illustrative_placeholder_only": True,
            },
        )
        points.append(
            SensitivityPoint(
                parameter_name="liability_cap_rate",
                parameter_value=bounded,
                liability_preview=liability_preview,
                effective_burden_rate=liability_preview / aava_value if aava_value > 0 else None,
                incidence_result=incidence.to_jsonable(),
                warnings=["Cap-rate sweep is non-operative and does not modify final liability."],
            )
        )
    return _build_result(example_id, "liability_cap_rate_sweep", points)


def sweep_aava(liability: float, aava_values: list[float], example_id: str = "") -> SensitivitySweepResult:
    liability_value = _non_negative_number(liability, "liability")
    points: list[SensitivityPoint] = []
    for index, value in enumerate(aava_values):
        aava = _non_negative_number(value, f"aava_values[{index}]")
        incidence = evaluate_tax_incidence(
            liability_value,
            {
                "pass_through_rate": 0.25,
                "worker_pressure_rate": 0.10,
                "supplier_pressure_rate": 0.05,
                "capital_absorption_rate": 0.20,
                "assumption_basis": "placeholder AAVA sensitivity incidence allocation",
                "illustrative_placeholder_only": True,
            },
        )
        points.append(
            SensitivityPoint(
                parameter_name="aava",
                parameter_value=aava,
                liability_preview=liability_value,
                effective_burden_rate=liability_value / aava if aava > 0 else None,
                incidence_result=incidence.to_jsonable(),
                warnings=["AAVA sweep is non-operative and does not modify final liability."],
            )
        )
    return _build_result(example_id, "aava_sweep", points)
