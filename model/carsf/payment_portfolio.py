"""Placeholder transition-payment portfolio comparisons for CARSF."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any

from .transition_payments import (
    TRANSITION_PAYMENT_NON_CLAIMS,
    TransitionPaymentDesign,
    TransitionPaymentResult,
    evaluate_transition_payment,
    transition_design_from_mapping,
)


@dataclass(frozen=True)
class PaymentPortfolioInput:
    portfolio_id: str
    year: int
    population_base: float
    displaced_workers: float
    designs: list[TransitionPaymentDesign]
    automation_revenue_available: float
    commonwealth_gap_after_carsf: float
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["designs"] = [design.to_jsonable() for design in self.designs]
        return payload


@dataclass(frozen=True)
class PaymentPortfolioResult:
    portfolio_id: str
    year: int
    design_results: list[TransitionPaymentResult]
    total_program_cost: float
    automation_revenue_available: float
    funding_coverage_ratio: float | None
    residual_funding_gap: float
    residual_commonwealth_gap_plus_payment_gap: float
    affordability_band: str
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(TRANSITION_PAYMENT_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["design_results"] = [result.to_jsonable() for result in self.design_results]
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


def _input_from_mapping(source: dict[str, Any]) -> PaymentPortfolioInput:
    return PaymentPortfolioInput(
        portfolio_id=str(source["portfolio_id"]),
        year=int(source["year"]),
        population_base=source["population_base"],
        displaced_workers=source["displaced_workers"],
        designs=[transition_design_from_mapping(item) for item in source.get("designs", [])],
        automation_revenue_available=source.get("automation_revenue_available", 0.0),
        commonwealth_gap_after_carsf=source.get("commonwealth_gap_after_carsf", 0.0),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def _eligible_people_for_design(design: TransitionPaymentDesign, population_base: float, displaced_workers: float) -> float:
    population_key = design.eligible_population.lower()
    design_type = design.design_type.upper()
    if design_type in {"UBI_LITE", "AUTOMATION_DIVIDEND"}:
        return population_base
    if "population" in population_key or "universal" in population_key:
        return population_base
    return displaced_workers


def _affordability_band(coverage_ratio: float | None, residual_gap: float, commonwealth_plus_payment_gap: float) -> str:
    if coverage_ratio is None:
        return "not_assessable"
    if coverage_ratio >= 1 and residual_gap == 0:
        return "low_pressure"
    if coverage_ratio >= 0.75:
        return "moderate_pressure"
    if coverage_ratio >= 0.40:
        return "high_pressure"
    if commonwealth_plus_payment_gap > 0:
        return "critical_pressure"
    return "high_pressure"


def evaluate_payment_portfolio(inputs: PaymentPortfolioInput | dict[str, Any]) -> PaymentPortfolioResult:
    """Compare placeholder transition-payment designs for one year."""

    if isinstance(inputs, dict):
        inputs = _input_from_mapping(inputs)

    population_base = _non_negative_number(inputs.population_base, "population_base")
    displaced_workers = _non_negative_number(inputs.displaced_workers, "displaced_workers")
    automation_revenue = _non_negative_number(inputs.automation_revenue_available, "automation_revenue_available")
    commonwealth_gap = _finite_number(inputs.commonwealth_gap_after_carsf, "commonwealth_gap_after_carsf")
    if not inputs.designs:
        raise ValueError("portfolio must include at least one transition-payment design")

    design_results: list[TransitionPaymentResult] = []
    for design in inputs.designs:
        eligible_people = _eligible_people_for_design(design, population_base, displaced_workers)
        design_results.append(
            evaluate_transition_payment(
                {
                    "design": design,
                    "eligible_people": eligible_people,
                    "year": inputs.year,
                    "placeholder_basis": inputs.placeholder_basis,
                }
            )
        )

    total_cost = sum(result.total_program_cost for result in design_results)
    coverage_ratio = automation_revenue / total_cost if total_cost > 0 else None
    residual_gap = max(0.0, total_cost - automation_revenue)
    combined_gap = commonwealth_gap + residual_gap
    return PaymentPortfolioResult(
        portfolio_id=inputs.portfolio_id,
        year=int(inputs.year),
        design_results=design_results,
        total_program_cost=total_cost,
        automation_revenue_available=automation_revenue,
        funding_coverage_ratio=coverage_ratio,
        residual_funding_gap=residual_gap,
        residual_commonwealth_gap_plus_payment_gap=combined_gap,
        affordability_band=_affordability_band(coverage_ratio, residual_gap, combined_gap),
        warnings=[
            "Payment portfolio is a placeholder affordability preview, not a real policy costing.",
            "Firm-level CARSF liability is not modified by payment portfolio results.",
        ],
    )
