"""National-level placeholder fiscal trajectory engine for CARSF."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any

from .public_revenue import evaluate_public_revenue
from .transfer_pressure import evaluate_transfer_pressure
from .workforce_displacement import (
    WorkforceTrajectoryInput,
    WorkforceTrajectoryResult,
    run_workforce_trajectory,
)


FISCAL_TRAJECTORY_WARNING = (
    "These are prototype fiscal trajectory outputs only. They are not forecasts, Treasury modelling, "
    "ATO estimates, ABS analysis, DSS estimates, PBO costing, legal advice, tax advice, or economic validation."
)
FISCAL_TRAJECTORY_NON_CLAIMS = [
    FISCAL_TRAJECTORY_WARNING,
    "Fiscal trajectory outputs do not modify firm-level CARSF liability.",
    "All thresholds and values are illustrative placeholders requiring calibration.",
]


@dataclass(frozen=True)
class FiscalTrajectoryInput:
    trajectory_id: str
    workforce: WorkforceTrajectoryInput
    average_support_payment_per_person: float
    transition_support_share: float
    retraining_support_share: float
    administrative_cost_per_person: float
    company_tax_change_by_year: dict[int, float] = field(default_factory=dict)
    gst_consumption_change_by_year: dict[int, float] = field(default_factory=dict)
    state_payroll_tax_loss_by_year: dict[int, float] = field(default_factory=dict)
    automation_revenue_captured_by_year: dict[int, float] = field(default_factory=dict)
    other_revenue_change_by_year: dict[int, float] = field(default_factory=dict)
    placeholder_basis: list[str] = field(default_factory=list)
    allow_revenue_gains: bool = False

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["workforce"] = self.workforce.to_jsonable()
        return payload


@dataclass(frozen=True)
class FiscalYearResult:
    year: int
    net_displaced_workers: float
    payg_revenue_loss: float
    super_contribution_loss: float
    retirement_contribution_pressure: float
    help_repayment_loss: float
    company_tax_change: float
    gst_consumption_change: float
    state_payroll_tax_loss: float
    automation_revenue_captured: float
    transfer_pressure: float
    commonwealth_gap_after_carsf: float
    total_public_sector_gap: float
    broader_labour_linked_pressure: float
    coverage_ratio: float | None
    warning_band: str
    warnings: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FiscalTrajectoryResult:
    trajectory_id: str
    start_year: int
    end_year: int
    years: list[FiscalYearResult]
    cumulative_payg_loss: float
    cumulative_help_repayment_loss: float
    cumulative_retirement_contribution_pressure: float
    cumulative_transfer_pressure: float
    cumulative_automation_revenue_captured: float
    cumulative_commonwealth_gap_after_carsf: float
    cumulative_state_revenue_pressure: float
    cumulative_total_public_sector_gap: float
    cumulative_broader_labour_linked_pressure: float
    first_high_warning_year: int | None
    first_critical_warning_year: int | None
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(FISCAL_TRAJECTORY_NON_CLAIMS))

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


def _year_map(source: dict[Any, Any] | None, field_name: str, allow_negative: bool = False) -> dict[int, float]:
    if source is None:
        return {}
    if not isinstance(source, dict):
        raise ValueError(f"{field_name} must be a mapping")
    mapped: dict[int, float] = {}
    for key, value in source.items():
        year = int(key)
        numeric = _finite_number(value, f"{field_name}[{year}]")
        if numeric < 0 and not allow_negative:
            raise ValueError(f"{field_name}[{year}] cannot be negative")
        mapped[year] = numeric
    return mapped


def _input_from_mapping(source: dict[str, Any]) -> FiscalTrajectoryInput:
    workforce_source = source["workforce"]
    allow_revenue_gains = bool(source.get("allow_revenue_gains", False))
    workforce = workforce_source if isinstance(workforce_source, WorkforceTrajectoryInput) else WorkforceTrajectoryInput(
        start_year=int(workforce_source["start_year"]),
        end_year=int(workforce_source["end_year"]),
        baseline_employed_workers=workforce_source["baseline_employed_workers"],
        annual_displacement_rate=workforce_source["annual_displacement_rate"],
        annual_reabsorption_rate=workforce_source["annual_reabsorption_rate"],
        labour_force_growth_rate=workforce_source["labour_force_growth_rate"],
        average_taxable_income=workforce_source["average_taxable_income"],
        average_payg_tax_per_worker=workforce_source["average_payg_tax_per_worker"],
        average_super_contribution_per_worker=workforce_source["average_super_contribution_per_worker"],
        average_help_repayment_per_worker=workforce_source["average_help_repayment_per_worker"],
        placeholder_basis=[str(item) for item in workforce_source.get("placeholder_basis", [])],
    )
    return FiscalTrajectoryInput(
        trajectory_id=str(source["trajectory_id"]),
        workforce=workforce,
        average_support_payment_per_person=source["average_support_payment_per_person"],
        transition_support_share=source["transition_support_share"],
        retraining_support_share=source["retraining_support_share"],
        administrative_cost_per_person=source["administrative_cost_per_person"],
        company_tax_change_by_year=_year_map(
            source.get("company_tax_change_by_year"),
            "company_tax_change_by_year",
            allow_negative=allow_revenue_gains,
        ),
        gst_consumption_change_by_year=_year_map(
            source.get("gst_consumption_change_by_year"),
            "gst_consumption_change_by_year",
            allow_negative=allow_revenue_gains,
        ),
        state_payroll_tax_loss_by_year=_year_map(source.get("state_payroll_tax_loss_by_year"), "state_payroll_tax_loss_by_year"),
        automation_revenue_captured_by_year=_year_map(
            source.get("automation_revenue_captured_by_year"),
            "automation_revenue_captured_by_year",
        ),
        other_revenue_change_by_year=_year_map(
            source.get("other_revenue_change_by_year"),
            "other_revenue_change_by_year",
            allow_negative=allow_revenue_gains,
        ),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
        allow_revenue_gains=allow_revenue_gains,
    )


def _year_value(mapping: dict[int, float], year: int) -> float:
    return mapping.get(year, 0.0)


def _warning_band(coverage_ratio: float | None, displacement_ratio: float, commonwealth_gap: float, previous_gap: float | None) -> str:
    if coverage_ratio is None:
        return "not_assessable"
    if coverage_ratio >= 0.75:
        return "low"
    if coverage_ratio >= 0.40:
        return "medium"
    if coverage_ratio >= 0.15:
        return "high"
    if displacement_ratio >= 0.05 or (previous_gap is not None and commonwealth_gap > previous_gap):
        return "critical"
    return "high"


def run_fiscal_trajectory(inputs: FiscalTrajectoryInput | dict[str, Any]) -> FiscalTrajectoryResult:
    """Combine workforce, revenue, transfer-pressure, and CARSF capture placeholders."""

    if isinstance(inputs, dict):
        inputs = _input_from_mapping(inputs)

    _non_negative_number(inputs.average_support_payment_per_person, "average_support_payment_per_person")
    _non_negative_number(inputs.administrative_cost_per_person, "administrative_cost_per_person")
    workforce_result: WorkforceTrajectoryResult = run_workforce_trajectory(inputs.workforce)
    years: list[FiscalYearResult] = []
    previous_gap: float | None = None
    first_high: int | None = None
    first_critical: int | None = None

    for workforce_year in workforce_result.years:
        year = workforce_year.year
        transfer = evaluate_transfer_pressure(
            {
                "net_displaced_workers": workforce_year.net_displaced_workers,
                "average_support_payment_per_person": inputs.average_support_payment_per_person,
                "transition_support_share": inputs.transition_support_share,
                "retraining_support_share": inputs.retraining_support_share,
                "administrative_cost_per_person": inputs.administrative_cost_per_person,
                "placeholder_basis": inputs.placeholder_basis,
            }
        )
        company_tax_change = _year_value(inputs.company_tax_change_by_year, year)
        gst_consumption_change = _year_value(inputs.gst_consumption_change_by_year, year)
        state_payroll_loss = _year_value(inputs.state_payroll_tax_loss_by_year, year)
        automation_captured = _year_value(inputs.automation_revenue_captured_by_year, year)
        other_revenue_change = _year_value(inputs.other_revenue_change_by_year, year)
        revenue = evaluate_public_revenue(
            {
                "payg_loss": workforce_year.payg_revenue_loss,
                "company_tax_change": company_tax_change,
                "gst_consumption_change": gst_consumption_change,
                "super_contribution_loss": workforce_year.super_contribution_loss,
                "help_repayment_loss": workforce_year.help_repayment_loss,
                "state_payroll_tax_loss": state_payroll_loss,
                "automation_revenue_captured": automation_captured,
                "other_revenue_change": other_revenue_change,
                "placeholder_basis": inputs.placeholder_basis,
                "allow_revenue_gains": inputs.allow_revenue_gains,
            }
        )
        commonwealth_gap = revenue.net_commonwealth_gap_after_carsf + transfer.total_transfer_pressure
        total_public_gap = commonwealth_gap + revenue.state_revenue_pressure
        broader_pressure = total_public_gap + revenue.retirement_contribution_pressure
        coverage_denominator = workforce_year.payg_revenue_loss + transfer.total_transfer_pressure
        coverage_ratio = automation_captured / coverage_denominator if coverage_denominator > 0 else None
        displacement_ratio = (
            workforce_year.net_displaced_workers / workforce_year.baseline_workers
            if workforce_year.baseline_workers > 0
            else 0.0
        )
        band = _warning_band(coverage_ratio, displacement_ratio, commonwealth_gap, previous_gap)
        previous_gap = commonwealth_gap
        if band in {"high", "critical"} and first_high is None:
            first_high = year
        if band == "critical" and first_critical is None:
            first_critical = year

        years.append(
            FiscalYearResult(
                year=year,
                net_displaced_workers=workforce_year.net_displaced_workers,
                payg_revenue_loss=workforce_year.payg_revenue_loss,
                super_contribution_loss=workforce_year.super_contribution_loss,
                retirement_contribution_pressure=revenue.retirement_contribution_pressure,
                help_repayment_loss=workforce_year.help_repayment_loss,
                company_tax_change=company_tax_change,
                gst_consumption_change=gst_consumption_change,
                state_payroll_tax_loss=state_payroll_loss,
                automation_revenue_captured=automation_captured,
                transfer_pressure=transfer.total_transfer_pressure,
                commonwealth_gap_after_carsf=commonwealth_gap,
                total_public_sector_gap=total_public_gap,
                broader_labour_linked_pressure=broader_pressure,
                coverage_ratio=coverage_ratio,
                warning_band=band,
                warnings=[
                    "Warning-band thresholds are illustrative placeholders.",
                    "Coverage ratio uses PAYG loss plus transfer pressure as a prototype denominator.",
                    "Superannuation contribution loss is tracked as retirement-system contribution pressure, not ordinary Commonwealth revenue loss.",
                ],
            )
        )

    return FiscalTrajectoryResult(
        trajectory_id=inputs.trajectory_id,
        start_year=workforce_result.start_year,
        end_year=workforce_result.end_year,
        years=years,
        cumulative_payg_loss=sum(year.payg_revenue_loss for year in years),
        cumulative_help_repayment_loss=sum(year.help_repayment_loss for year in years),
        cumulative_retirement_contribution_pressure=sum(year.retirement_contribution_pressure for year in years),
        cumulative_transfer_pressure=sum(year.transfer_pressure for year in years),
        cumulative_automation_revenue_captured=sum(year.automation_revenue_captured for year in years),
        cumulative_commonwealth_gap_after_carsf=sum(year.commonwealth_gap_after_carsf for year in years),
        cumulative_state_revenue_pressure=sum(year.state_payroll_tax_loss for year in years),
        cumulative_total_public_sector_gap=sum(year.total_public_sector_gap for year in years),
        cumulative_broader_labour_linked_pressure=sum(year.broader_labour_linked_pressure for year in years),
        first_high_warning_year=first_high,
        first_critical_warning_year=first_critical,
        warnings=[
            "National trajectory inputs are placeholders and are not fiscal forecasts.",
            "Firm-level CARSF liability is not modified by this national trajectory layer.",
        ],
    )
