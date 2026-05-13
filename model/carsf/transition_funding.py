"""Link fiscal trajectories to placeholder transition-payment funding."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .fiscal_trajectory import FiscalTrajectoryResult
from .payment_portfolio import PaymentPortfolioResult, evaluate_payment_portfolio
from .transition_payments import TRANSITION_PAYMENT_NON_CLAIMS, TransitionPaymentDesign, transition_design_from_mapping


@dataclass(frozen=True)
class TransitionFundingInput:
    funding_id: str
    fiscal_trajectory: dict[str, Any] | FiscalTrajectoryResult
    payment_designs_by_year: dict[int, list[TransitionPaymentDesign]]
    population_base_by_year: dict[int, float]
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TransitionFundingYearResult:
    year: int
    net_displaced_workers: float
    automation_revenue_captured: float
    commonwealth_gap_after_carsf: float
    total_payment_cost: float
    funding_coverage_ratio: float | None
    residual_payment_gap: float
    combined_gap: float
    cliff_risk_band: str
    warnings: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TransitionFundingResult:
    funding_id: str
    years: list[TransitionFundingYearResult]
    cumulative_payment_cost: float
    cumulative_automation_revenue_available: float
    cumulative_residual_payment_gap: float
    cumulative_combined_gap: float
    first_high_cliff_risk_year: int | None
    first_critical_cliff_risk_year: int | None
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(TRANSITION_PAYMENT_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["years"] = [year.to_jsonable() for year in self.years]
        return payload


def _trajectory_to_dict(source: dict[str, Any] | FiscalTrajectoryResult) -> dict[str, Any]:
    if isinstance(source, FiscalTrajectoryResult):
        return source.to_jsonable()
    return source


def _input_from_mapping(source: dict[str, Any]) -> TransitionFundingInput:
    designs_by_year: dict[int, list[TransitionPaymentDesign]] = {}
    for year, designs in source.get("payment_designs_by_year", {}).items():
        designs_by_year[int(year)] = [transition_design_from_mapping(item) for item in designs]
    return TransitionFundingInput(
        funding_id=str(source["funding_id"]),
        fiscal_trajectory=source["fiscal_trajectory"],
        payment_designs_by_year=designs_by_year,
        population_base_by_year={int(year): float(value) for year, value in source.get("population_base_by_year", {}).items()},
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def _cliff_risk_band(portfolio: PaymentPortfolioResult, displacement_growth: float, commonwealth_gap: float) -> str:
    coverage = portfolio.funding_coverage_ratio
    if coverage is None:
        return "not_assessable"
    if coverage >= 1 and portfolio.residual_funding_gap == 0:
        band = "low"
    elif coverage >= 0.75:
        band = "medium"
    elif coverage >= 0.40:
        band = "high"
    else:
        band = "critical"
    if displacement_growth > 0.20 and portfolio.residual_funding_gap > 0 and band == "medium":
        band = "high"
    if displacement_growth > 0.20 and portfolio.residual_funding_gap > 0 and commonwealth_gap > 0 and band == "high":
        band = "critical"
    return band


def run_transition_funding(inputs: TransitionFundingInput | dict[str, Any]) -> TransitionFundingResult:
    """Run a year-by-year transition-payment funding preview from fiscal trajectory output."""

    if isinstance(inputs, dict):
        inputs = _input_from_mapping(inputs)

    trajectory = _trajectory_to_dict(inputs.fiscal_trajectory)
    years = trajectory.get("years", [])
    if not isinstance(years, list) or not years:
        raise ValueError("fiscal_trajectory must include year results")

    results: list[TransitionFundingYearResult] = []
    first_high: int | None = None
    first_critical: int | None = None
    previous_displaced: float | None = None
    for year_row in years:
        year = int(year_row["year"])
        designs = inputs.payment_designs_by_year.get(year)
        if designs is None:
            designs = inputs.payment_designs_by_year.get(0)
        if not designs:
            raise ValueError(f"missing transition payment designs for year {year}")
        net_displaced = float(year_row["net_displaced_workers"])
        population_base = float(inputs.population_base_by_year.get(year, inputs.population_base_by_year.get(0, 0.0)))
        portfolio = evaluate_payment_portfolio(
            {
                "portfolio_id": f"{inputs.funding_id}_{year}",
                "year": year,
                "population_base": population_base,
                "displaced_workers": net_displaced,
                "designs": designs,
                "automation_revenue_available": year_row["automation_revenue_captured"],
                "commonwealth_gap_after_carsf": year_row["commonwealth_gap_after_carsf"],
                "placeholder_basis": inputs.placeholder_basis,
            }
        )
        displacement_growth = 0.0
        if previous_displaced is not None and previous_displaced > 0:
            displacement_growth = max(0.0, (net_displaced - previous_displaced) / previous_displaced)
        previous_displaced = net_displaced
        cliff_band = _cliff_risk_band(portfolio, displacement_growth, float(year_row["commonwealth_gap_after_carsf"]))
        if cliff_band in {"high", "critical"} and first_high is None:
            first_high = year
        if cliff_band == "critical" and first_critical is None:
            first_critical = year
        results.append(
            TransitionFundingYearResult(
                year=year,
                net_displaced_workers=net_displaced,
                automation_revenue_captured=float(year_row["automation_revenue_captured"]),
                commonwealth_gap_after_carsf=float(year_row["commonwealth_gap_after_carsf"]),
                total_payment_cost=portfolio.total_program_cost,
                funding_coverage_ratio=portfolio.funding_coverage_ratio,
                residual_payment_gap=portfolio.residual_funding_gap,
                combined_gap=portfolio.residual_commonwealth_gap_plus_payment_gap,
                cliff_risk_band=cliff_band,
                warnings=[
                    "Cliff-risk band is placeholder-only and not a welfare-system stress test.",
                    "Transition funding output does not modify firm-level CARSF liability.",
                ],
            )
        )

    return TransitionFundingResult(
        funding_id=inputs.funding_id,
        years=results,
        cumulative_payment_cost=sum(year.total_payment_cost for year in results),
        cumulative_automation_revenue_available=sum(year.automation_revenue_captured for year in results),
        cumulative_residual_payment_gap=sum(year.residual_payment_gap for year in results),
        cumulative_combined_gap=sum(year.combined_gap for year in results),
        first_high_cliff_risk_year=first_high,
        first_critical_cliff_risk_year=first_critical,
        warnings=[
            "Transition funding consumes fiscal trajectory outputs as placeholders only.",
            "This is not a real UBI, welfare, DSS, Services Australia, Treasury, or PBO model.",
        ],
    )
