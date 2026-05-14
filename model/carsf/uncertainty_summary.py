"""Summary helpers for deterministic uncertainty range outputs."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .uncertainty_ranges import UNCERTAINTY_NON_CLAIMS


@dataclass(frozen=True)
class UncertaintySummaryResult:
    household_uncertainty_count: int
    stable_high_risk_count: int
    stable_low_risk_count: int
    range_sensitive_count: int
    fragile_metric_count: int
    highest_uncertainty_items: list[str]
    strongest_stable_risk_signals: list[str]
    calibration_blockers: list[str]
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(UNCERTAINTY_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _jsonable(source: Any) -> dict[str, Any]:
    if hasattr(source, "to_jsonable"):
        return source.to_jsonable()
    return dict(source)


def _fragile_ranges(row: dict[str, Any]) -> list[str]:
    names = []
    for key in [
        "residual_gap_range",
        "transition_support_range",
        "reemployment_months_range",
        "regional_stress_range",
        "payment_cliff_loss_range",
    ]:
        value = row.get(key)
        if isinstance(value, dict) and value.get("stability_band") == "fragile":
            names.append(f"{row.get('scenario_id', row.get('uncertainty_id', 'unknown'))}:{key}")
    return names


def summarise_uncertainty_results(
    household_results: list[dict[str, Any] | Any],
    weighted_results: list[dict[str, Any] | Any] | None = None,
) -> UncertaintySummaryResult:
    """Summarise deterministic uncertainty results without claiming real quantification."""

    if not household_results:
        raise ValueError("uncertainty summary requires at least one household result")
    household_rows = [_jsonable(row) for row in household_results]
    weighted_rows = [_jsonable(row) for row in (weighted_results or [])]
    stable_high = [row for row in household_rows if row.get("risk_signal_stability") == "stable_high_risk"]
    stable_low = [row for row in household_rows if row.get("risk_signal_stability") == "stable_low_risk"]
    sensitive = [row for row in household_rows if row.get("risk_signal_stability") == "range_sensitive"]
    fragile_items: list[str] = []
    for row in household_rows:
        fragile_items.extend(_fragile_ranges(row))
    for weighted in weighted_rows:
        for subgroup in weighted.get("subgroup_results", []):
            for key in ["residual_gap_range", "high_critical_share_range"]:
                value = subgroup.get(key)
                if isinstance(value, dict) and value.get("stability_band") == "fragile":
                    fragile_items.append(f"{subgroup.get('subgroup_id')}:{key}")
    highest_uncertainty = sorted(set(fragile_items + [row["scenario_id"] for row in sensitive]))
    strongest_signals = sorted(
        {
            *(row["scenario_id"] for row in stable_high),
            *(subgroup for weighted in weighted_rows for subgroup in weighted.get("stable_high_risk_subgroups", [])),
        }
    )
    blockers = [
        "household ranges are not calibrated",
        "weighted subgroup ranges are not representative",
        "no real ABS/HILDA/Census/DSS/Services Australia/Treasury/PBO data is used",
        "no statistical confidence intervals or forecasts are produced",
    ]
    return UncertaintySummaryResult(
        household_uncertainty_count=len(household_rows),
        stable_high_risk_count=len(stable_high),
        stable_low_risk_count=len(stable_low),
        range_sensitive_count=len(sensitive),
        fragile_metric_count=len(fragile_items),
        highest_uncertainty_items=highest_uncertainty,
        strongest_stable_risk_signals=strongest_signals,
        calibration_blockers=blockers,
        warnings=[
            "Uncertainty summary is deterministic placeholder-only and not real uncertainty quantification.",
            "Firm-level CARSF liability is not modified by uncertainty summary outputs.",
        ],
    )
