"""Deterministic placeholder workforce displacement trajectories for CARSF."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any


WORKFORCE_NON_CLAIMS = [
    "Workforce displacement outputs are illustrative placeholders only and are not forecasts.",
    "No Treasury, ATO, ABS, DSS, PBO, legal, tax, or economic validation is implied.",
    "Workforce displacement results do not modify firm-level CARSF liability.",
]


@dataclass(frozen=True)
class WorkforceTrajectoryInput:
    start_year: int
    end_year: int
    baseline_employed_workers: float
    annual_displacement_rate: float
    annual_reabsorption_rate: float
    labour_force_growth_rate: float
    average_taxable_income: float
    average_payg_tax_per_worker: float
    average_super_contribution_per_worker: float
    average_help_repayment_per_worker: float
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WorkforceYearResult:
    year: int
    baseline_workers: float
    displaced_workers: float
    reabsorbed_workers: float
    net_displaced_workers: float
    remaining_employed_workers: float
    payg_revenue_loss: float
    super_contribution_loss: float
    help_repayment_loss: float
    warnings: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WorkforceTrajectoryResult:
    start_year: int
    end_year: int
    years: list[WorkforceYearResult]
    cumulative_net_displaced_workers: float
    cumulative_payg_loss: float
    cumulative_super_loss: float
    cumulative_help_loss: float
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(WORKFORCE_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["years"] = [year.to_jsonable() for year in self.years]
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


def _input_from_mapping(source: dict[str, Any]) -> WorkforceTrajectoryInput:
    return WorkforceTrajectoryInput(
        start_year=int(source["start_year"]),
        end_year=int(source["end_year"]),
        baseline_employed_workers=source["baseline_employed_workers"],
        annual_displacement_rate=source["annual_displacement_rate"],
        annual_reabsorption_rate=source["annual_reabsorption_rate"],
        labour_force_growth_rate=source["labour_force_growth_rate"],
        average_taxable_income=source["average_taxable_income"],
        average_payg_tax_per_worker=source["average_payg_tax_per_worker"],
        average_super_contribution_per_worker=source["average_super_contribution_per_worker"],
        average_help_repayment_per_worker=source["average_help_repayment_per_worker"],
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def run_workforce_trajectory(inputs: WorkforceTrajectoryInput | dict[str, Any]) -> WorkforceTrajectoryResult:
    """Run a deterministic placeholder worker-displacement path.

    The model carries unresolved displacement forward year to year. Reabsorption
    reduces that stock, and employment is never allowed to fall below zero.
    """

    if isinstance(inputs, dict):
        inputs = _input_from_mapping(inputs)

    if inputs.end_year < inputs.start_year:
        raise ValueError("end_year must be greater than or equal to start_year")

    baseline_workers = _non_negative_number(inputs.baseline_employed_workers, "baseline_employed_workers")
    displacement_rate = _bounded_rate(inputs.annual_displacement_rate, "annual_displacement_rate")
    reabsorption_rate = _bounded_rate(inputs.annual_reabsorption_rate, "annual_reabsorption_rate")
    growth_rate = _bounded_rate(inputs.labour_force_growth_rate, "labour_force_growth_rate")
    _non_negative_number(inputs.average_taxable_income, "average_taxable_income")
    payg_per_worker = _non_negative_number(inputs.average_payg_tax_per_worker, "average_payg_tax_per_worker")
    super_per_worker = _non_negative_number(
        inputs.average_super_contribution_per_worker,
        "average_super_contribution_per_worker",
    )
    help_per_worker = _non_negative_number(inputs.average_help_repayment_per_worker, "average_help_repayment_per_worker")

    years: list[WorkforceYearResult] = []
    unresolved_displacement = 0.0
    current_baseline = baseline_workers
    for year in range(inputs.start_year, inputs.end_year + 1):
        if year > inputs.start_year:
            current_baseline *= 1 + growth_rate

        displaced_workers = current_baseline * displacement_rate
        displacement_stock = unresolved_displacement + displaced_workers
        reabsorbed_workers = min(displacement_stock, displacement_stock * reabsorption_rate)
        net_displaced_workers = max(0.0, displacement_stock - reabsorbed_workers)
        net_displaced_workers = min(net_displaced_workers, current_baseline)
        remaining_employed_workers = max(0.0, current_baseline - net_displaced_workers)
        unresolved_displacement = net_displaced_workers

        years.append(
            WorkforceYearResult(
                year=year,
                baseline_workers=current_baseline,
                displaced_workers=displaced_workers,
                reabsorbed_workers=reabsorbed_workers,
                net_displaced_workers=net_displaced_workers,
                remaining_employed_workers=remaining_employed_workers,
                payg_revenue_loss=net_displaced_workers * payg_per_worker,
                super_contribution_loss=net_displaced_workers * super_per_worker,
                help_repayment_loss=net_displaced_workers * help_per_worker,
                warnings=["Illustrative placeholder workforce trajectory; no forecast claim is made."],
            )
        )

    return WorkforceTrajectoryResult(
        start_year=inputs.start_year,
        end_year=inputs.end_year,
        years=years,
        cumulative_net_displaced_workers=sum(year.net_displaced_workers for year in years),
        cumulative_payg_loss=sum(year.payg_revenue_loss for year in years),
        cumulative_super_loss=sum(year.super_contribution_loss for year in years),
        cumulative_help_loss=sum(year.help_repayment_loss for year in years),
        warnings=["Rates and per-worker amounts are placeholder-only and require calibration."],
    )
