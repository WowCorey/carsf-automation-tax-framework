"""Prototype tax-incidence and pass-through guardrails."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any


INCIDENCE_NON_CLAIMS = [
    "These incidence outputs are illustrative placeholders only.",
    "They do not claim actual consumer, worker, supplier, or capital pass-through behaviour.",
    "They are not economic validation, Treasury modelling, ATO guidance, legal advice, market forecasting, or tax advice.",
]


@dataclass(frozen=True)
class IncidenceAssumption:
    pass_through_rate: float
    worker_pressure_rate: float
    supplier_pressure_rate: float
    capital_absorption_rate: float
    assumption_basis: str
    illustrative_placeholder_only: bool = True

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IncidenceResult:
    consumer_pass_through_amount: float
    worker_pressure_amount: float
    supplier_pressure_amount: float
    capital_absorption_amount: float
    total_allocated_amount: float
    allocation_gap: float
    incidence_risk_band: str
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(INCIDENCE_NON_CLAIMS))

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


def _assumption_from_mapping(source: dict[str, Any]) -> IncidenceAssumption:
    return IncidenceAssumption(
        pass_through_rate=source.get("pass_through_rate", 0.0),
        worker_pressure_rate=source.get("worker_pressure_rate", 0.0),
        supplier_pressure_rate=source.get("supplier_pressure_rate", 0.0),
        capital_absorption_rate=source.get("capital_absorption_rate", 0.0),
        assumption_basis=str(source.get("assumption_basis", "")),
        illustrative_placeholder_only=bool(source.get("illustrative_placeholder_only", False)),
    )


def evaluate_tax_incidence(liability: float, assumption: IncidenceAssumption | dict[str, Any]) -> IncidenceResult:
    """Allocate placeholder incidence shares without claiming actual behaviour."""

    liability_value = _finite_number(liability, "liability")
    if liability_value < 0:
        raise ValueError("liability cannot be negative")
    if isinstance(assumption, dict):
        assumption = _assumption_from_mapping(assumption)

    pass_rate = _bounded_rate(assumption.pass_through_rate, "pass_through_rate")
    worker_rate = _bounded_rate(assumption.worker_pressure_rate, "worker_pressure_rate")
    supplier_rate = _bounded_rate(assumption.supplier_pressure_rate, "supplier_pressure_rate")
    capital_rate = _bounded_rate(assumption.capital_absorption_rate, "capital_absorption_rate")
    total_rate = pass_rate + worker_rate + supplier_rate + capital_rate
    if total_rate > 1:
        raise ValueError("incidence allocation rates cannot sum above 1")

    warnings = [
        "Pass-through and incidence rates are illustrative placeholders only.",
        "This incidence preview does not alter liability.",
    ]
    if not assumption.illustrative_placeholder_only:
        warnings.append("Assumption is not labelled illustrative_placeholder_only; results remain prototype-only.")
    if liability_value == 0:
        return IncidenceResult(
            consumer_pass_through_amount=0.0,
            worker_pressure_amount=0.0,
            supplier_pressure_amount=0.0,
            capital_absorption_amount=0.0,
            total_allocated_amount=0.0,
            allocation_gap=0.0,
            incidence_risk_band="low",
            warnings=warnings,
        )

    consumer = liability_value * pass_rate
    worker = liability_value * worker_rate
    supplier = liability_value * supplier_rate
    capital = liability_value * capital_rate
    total = consumer + worker + supplier + capital
    gap = liability_value - total

    if pass_rate + worker_rate >= 0.60:
        band = "high"
    elif pass_rate + worker_rate + supplier_rate >= 0.30:
        band = "medium"
    else:
        band = "low"

    return IncidenceResult(
        consumer_pass_through_amount=consumer,
        worker_pressure_amount=worker,
        supplier_pressure_amount=supplier,
        capital_absorption_amount=capital,
        total_allocated_amount=total,
        allocation_gap=gap,
        incidence_risk_band=band,
        warnings=warnings,
    )
