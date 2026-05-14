"""Deterministic uncertainty wrappers for synthetic household scenarios."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .uncertainty_ranges import (
    UNCERTAINTY_NON_CLAIMS,
    UncertaintyRange,
    evaluate_uncertainty_range,
    uncertainty_range_from_mapping,
)


@dataclass(frozen=True)
class HouseholdUncertaintyInput:
    uncertainty_id: str
    scenario_result: dict[str, Any]
    residual_gap_range: UncertaintyRange
    transition_support_range: UncertaintyRange
    reemployment_months_range: UncertaintyRange | None = None
    regional_stress_range: UncertaintyRange | None = None
    payment_cliff_loss_range: UncertaintyRange | None = None
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["residual_gap_range"] = self.residual_gap_range.to_jsonable()
        payload["transition_support_range"] = self.transition_support_range.to_jsonable()
        payload["reemployment_months_range"] = (
            None if self.reemployment_months_range is None else self.reemployment_months_range.to_jsonable()
        )
        payload["regional_stress_range"] = None if self.regional_stress_range is None else self.regional_stress_range.to_jsonable()
        payload["payment_cliff_loss_range"] = (
            None if self.payment_cliff_loss_range is None else self.payment_cliff_loss_range.to_jsonable()
        )
        return payload


@dataclass(frozen=True)
class HouseholdUncertaintyResult:
    uncertainty_id: str
    scenario_id: str
    household_id: str
    residual_gap_range: dict[str, Any]
    transition_support_range: dict[str, Any]
    reemployment_months_range: dict[str, Any] | None
    regional_stress_range: dict[str, Any] | None
    payment_cliff_loss_range: dict[str, Any] | None
    low_case_shock_band: str
    base_case_shock_band: str
    high_case_shock_band: str
    risk_signal_stability: str
    primary_uncertainty_drivers: list[str]
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(UNCERTAINTY_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _input_from_mapping(source: HouseholdUncertaintyInput | dict[str, Any]) -> HouseholdUncertaintyInput:
    if isinstance(source, HouseholdUncertaintyInput):
        return source
    return HouseholdUncertaintyInput(
        uncertainty_id=str(source["uncertainty_id"]),
        scenario_result=dict(source["scenario_result"]),
        residual_gap_range=uncertainty_range_from_mapping(source["residual_gap_range"]),
        transition_support_range=uncertainty_range_from_mapping(source["transition_support_range"]),
        reemployment_months_range=(
            None if source.get("reemployment_months_range") is None else uncertainty_range_from_mapping(source["reemployment_months_range"])
        ),
        regional_stress_range=(
            None if source.get("regional_stress_range") is None else uncertainty_range_from_mapping(source["regional_stress_range"])
        ),
        payment_cliff_loss_range=(
            None if source.get("payment_cliff_loss_range") is None else uncertainty_range_from_mapping(source["payment_cliff_loss_range"])
        ),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def _case_band(residual_gap: float, base_band: str, reemployment_months: float | None, regional_stress: float | None, cliff_loss: float | None) -> str:
    if residual_gap <= 0:
        score = 0
    elif residual_gap <= 5_000:
        score = 1
    elif residual_gap <= 15_000:
        score = 2
    else:
        score = 3
    if base_band in {"high", "critical"} and residual_gap > 0:
        score = max(score, 2)
    if base_band == "critical" and residual_gap > 15_000:
        score = 3
    if reemployment_months is not None and reemployment_months >= 18:
        score += 1
    if regional_stress is not None and regional_stress >= 0.75:
        score += 1
    if cliff_loss is not None and cliff_loss >= 5_000:
        score += 1
    if score <= 0:
        return "low"
    if score == 1:
        return "medium"
    if score <= 3:
        return "high"
    return "critical"


def _risk_signal_stability(low_band: str, base_band: str, high_band: str) -> str:
    bands = {low_band, base_band, high_band}
    high_set = {"high", "critical"}
    low_set = {"low", "medium"}
    if bands <= high_set:
        return "stable_high_risk"
    if bands <= low_set:
        return "stable_low_risk"
    if "not_assessable" in bands:
        return "not_assessable"
    return "range_sensitive"


def _value(result: dict[str, Any] | None, attr: str) -> float | None:
    if result is None:
        return None
    return None if result.get(attr) is None else float(result[attr])


def evaluate_household_uncertainty(inputs: HouseholdUncertaintyInput | dict[str, Any]) -> HouseholdUncertaintyResult:
    """Apply deterministic low/base/high ranges to one synthetic household scenario."""

    input_obj = _input_from_mapping(inputs)
    scenario = input_obj.scenario_result
    residual = evaluate_uncertainty_range(input_obj.residual_gap_range)
    support = evaluate_uncertainty_range(input_obj.transition_support_range)
    reemployment = None if input_obj.reemployment_months_range is None else evaluate_uncertainty_range(input_obj.reemployment_months_range)
    regional = None if input_obj.regional_stress_range is None else evaluate_uncertainty_range(input_obj.regional_stress_range)
    cliff = None if input_obj.payment_cliff_loss_range is None else evaluate_uncertainty_range(input_obj.payment_cliff_loss_range)

    existing_band = str(scenario.get("household_shock_band", "not_assessable"))
    low_band = _case_band(residual.low, existing_band, _value(reemployment.to_jsonable() if reemployment else None, "low"), _value(regional.to_jsonable() if regional else None, "low"), _value(cliff.to_jsonable() if cliff else None, "low"))
    base_band = _case_band(residual.base, existing_band, _value(reemployment.to_jsonable() if reemployment else None, "base"), _value(regional.to_jsonable() if regional else None, "base"), _value(cliff.to_jsonable() if cliff else None, "base"))
    high_band = _case_band(residual.high, existing_band, _value(reemployment.to_jsonable() if reemployment else None, "high"), _value(regional.to_jsonable() if regional else None, "high"), _value(cliff.to_jsonable() if cliff else None, "high"))
    risk_stability = _risk_signal_stability(low_band, base_band, high_band)

    drivers = sorted(
        {
            *residual.uncertainty_drivers,
            *support.uncertainty_drivers,
            *(reemployment.uncertainty_drivers if reemployment else []),
            *(regional.uncertainty_drivers if regional else []),
            *(cliff.uncertainty_drivers if cliff else []),
        }
    )
    range_results = [residual, support, *(item for item in [reemployment, regional, cliff] if item is not None)]
    warnings = [
        "Household uncertainty is deterministic placeholder-only and not a confidence interval.",
        "Firm-level CARSF liability is not modified by household uncertainty outputs.",
    ]
    if any(item.stability_band == "fragile" for item in range_results):
        warnings.append("One or more supplied household ranges is fragile and requires external calibration before interpretation.")
    if risk_stability == "range_sensitive":
        warnings.append("Household risk signal changes across low/base/high cases and is too fragile for point interpretation.")
    return HouseholdUncertaintyResult(
        uncertainty_id=input_obj.uncertainty_id,
        scenario_id=str(scenario.get("scenario_id", input_obj.uncertainty_id)),
        household_id=str(scenario.get("household_id", "")),
        residual_gap_range=residual.to_jsonable(),
        transition_support_range=support.to_jsonable(),
        reemployment_months_range=None if reemployment is None else reemployment.to_jsonable(),
        regional_stress_range=None if regional is None else regional.to_jsonable(),
        payment_cliff_loss_range=None if cliff is None else cliff.to_jsonable(),
        low_case_shock_band=low_band,
        base_case_shock_band=base_band,
        high_case_shock_band=high_band,
        risk_signal_stability=risk_stability,
        primary_uncertainty_drivers=drivers,
        warnings=warnings,
    )
