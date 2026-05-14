"""Summaries for synthetic household distributional scenario results."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .distributional_scenarios import DistributionalScenarioResult
from .households import DISTRIBUTIONAL_NON_CLAIMS


@dataclass(frozen=True)
class DistributionalSummaryResult:
    scenario_count: int
    low_shock_count: int
    medium_shock_count: int
    high_shock_count: int
    critical_shock_count: int
    average_residual_gap_placeholder: float
    highest_risk_households: list[str] = field(default_factory=list)
    primary_systemic_risks: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(DISTRIBUTIONAL_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _result_to_mapping(result: DistributionalScenarioResult | dict[str, Any]) -> dict[str, Any]:
    if isinstance(result, DistributionalScenarioResult):
        return result.to_jsonable()
    return result


def summarise_distributional_scenarios(results: list[DistributionalScenarioResult | dict[str, Any]]) -> DistributionalSummaryResult:
    """Summarise synthetic household shock bands without population weighting."""

    if not results:
        raise ValueError("distributional summary requires at least one result")
    rows = [_result_to_mapping(result) for result in results]
    counts = {"low": 0, "medium": 0, "high": 0, "critical": 0}
    for row in rows:
        band = str(row["household_shock_band"])
        if band in counts:
            counts[band] += 1
    average_gap = sum(float(row["residual_household_gap_after_support"]) for row in rows) / len(rows)
    severity = {"critical": 3, "high": 2, "medium": 1, "low": 0, "not_assessable": -1}
    ordered = sorted(
        rows,
        key=lambda row: (
            -severity.get(str(row["household_shock_band"]), 0),
            -float(row["residual_household_gap_after_support"]),
            str(row["household_id"]),
        ),
    )
    risk_counts: dict[str, int] = {}
    for row in rows:
        for driver in row.get("primary_risk_drivers", []):
            risk_counts[str(driver)] = risk_counts.get(str(driver), 0) + 1
    systemic = [
        key
        for key, _ in sorted(risk_counts.items(), key=lambda item: (-item[1], item[0]))
        if key
    ][:5]
    return DistributionalSummaryResult(
        scenario_count=len(rows),
        low_shock_count=counts["low"],
        medium_shock_count=counts["medium"],
        high_shock_count=counts["high"],
        critical_shock_count=counts["critical"],
        average_residual_gap_placeholder=average_gap,
        highest_risk_households=[str(row["household_id"]) for row in ordered[:3]],
        primary_systemic_risks=systemic,
        warnings=[
            "Distributional summary is deterministic but not population-representative.",
            "Synthetic household scenarios are not calibrated household modelling.",
        ],
    )
