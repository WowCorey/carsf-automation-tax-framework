"""Synthetic household distributional scenario orchestration."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any

from .households import (
    DISTRIBUTIONAL_NON_CLAIMS,
    SyntheticHousehold,
    evaluate_household_budget,
    synthetic_household_from_mapping,
)
from .payment_cliffs import PaymentCliffInput, evaluate_payment_cliff, payment_cliff_input_from_mapping
from .reemployment import ReemploymentPath, evaluate_reemployment_path, reemployment_path_from_mapping
from .regional_stress import RegionalStressInput, evaluate_regional_stress, regional_stress_input_from_mapping


@dataclass(frozen=True)
class DistributionalScenarioInput:
    scenario_id: str
    household: SyntheticHousehold
    reemployment_path: ReemploymentPath
    regional_stress: RegionalStressInput
    payment_cliff: PaymentCliffInput | None = None
    payment_interaction_result: dict[str, Any] | None = None
    transition_support_amount: float = 0.0
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["household"] = self.household.to_jsonable()
        payload["reemployment_path"] = self.reemployment_path.to_jsonable()
        payload["regional_stress"] = self.regional_stress.to_jsonable()
        payload["payment_cliff"] = None if self.payment_cliff is None else self.payment_cliff.to_jsonable()
        return payload


@dataclass(frozen=True)
class DistributionalScenarioResult:
    scenario_id: str
    household_id: str
    household_type: str
    budget_stress_band: str
    reemployment_risk_band: str
    regional_stress_band: str
    cliff_severity_band: str | None
    transition_support_amount: float
    residual_household_gap_after_support: float
    household_shock_band: str
    primary_risk_drivers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(DISTRIBUTIONAL_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


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


def _input_from_mapping(source: dict[str, Any]) -> DistributionalScenarioInput:
    return DistributionalScenarioInput(
        scenario_id=str(source["scenario_id"]),
        household=synthetic_household_from_mapping(source["household"]),
        reemployment_path=reemployment_path_from_mapping(source["reemployment_path"]),
        regional_stress=regional_stress_input_from_mapping(source["regional_stress"]),
        payment_cliff=(
            None if source.get("payment_cliff") is None else payment_cliff_input_from_mapping(source["payment_cliff"])
        ),
        payment_interaction_result=source.get("payment_interaction_result"),
        transition_support_amount=source.get("transition_support_amount", 0.0),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def _band_score(band: str | None) -> int:
    return {
        None: 0,
        "none": 0,
        "low": 0,
        "medium": 1,
        "high": 2,
        "critical": 3,
        "not_assessable": 1,
    }.get(band, 1)


def _shock_band(score: int) -> str:
    if score <= 1:
        return "low"
    if score <= 3:
        return "medium"
    if score <= 5:
        return "high"
    return "critical"


def evaluate_distributional_scenario(inputs: DistributionalScenarioInput | dict[str, Any]) -> DistributionalScenarioResult:
    """Combine synthetic household, re-employment, cliff, and regional stress outputs."""

    if isinstance(inputs, dict):
        inputs = _input_from_mapping(inputs)
    support = _non_negative_number(inputs.transition_support_amount, "transition_support_amount")
    budget = evaluate_household_budget(inputs.household)
    reemployment = evaluate_reemployment_path(inputs.reemployment_path, inputs.household)
    regional = evaluate_regional_stress(inputs.regional_stress)
    cliff = evaluate_payment_cliff(inputs.payment_cliff) if inputs.payment_cliff is not None else None
    residual_gap = max(0.0, budget.immediate_budget_gap - support)

    score = _band_score(budget.budget_stress_band) + _band_score(reemployment.reemployment_risk_band) + _band_score(regional.regional_stress_band)
    if cliff is not None:
        score += _band_score(cliff.cliff_severity_band)
    if budget.immediate_budget_gap > 0:
        support_coverage = support / budget.immediate_budget_gap
        if support_coverage < 0.25:
            score += 2
        elif support_coverage < 0.75:
            score += 1
    if residual_gap > 0 and budget.budget_stress_band in {"high", "critical"}:
        score += 1

    drivers: list[str] = []
    if budget.budget_stress_band in {"high", "critical"}:
        drivers.append(f"budget stress: {budget.budget_stress_band}")
    if reemployment.reemployment_risk_band in {"high", "critical"}:
        drivers.append(f"re-employment risk: {reemployment.reemployment_risk_band}")
    if regional.regional_stress_band in {"high", "critical"}:
        drivers.append(f"regional stress: {regional.regional_stress_band}")
    if cliff is not None and cliff.cliff_severity_band in {"high", "critical"}:
        drivers.append(f"payment cliff: {cliff.cliff_severity_band}")
    if residual_gap > 0:
        drivers.append("residual household gap after support")

    return DistributionalScenarioResult(
        scenario_id=inputs.scenario_id,
        household_id=budget.household_id,
        household_type=budget.household_type,
        budget_stress_band=budget.budget_stress_band,
        reemployment_risk_band=reemployment.reemployment_risk_band,
        regional_stress_band=regional.regional_stress_band,
        cliff_severity_band=None if cliff is None else cliff.cliff_severity_band,
        transition_support_amount=support,
        residual_household_gap_after_support=residual_gap,
        household_shock_band=_shock_band(score),
        primary_risk_drivers=drivers,
        warnings=[
            *budget.warnings,
            *reemployment.warnings,
            *regional.warnings,
            *(cliff.warnings if cliff is not None else []),
            "Distributional scenario is synthetic-only and does not use or represent real households.",
            "Firm-level CARSF liability is not modified by distributional scenario outputs.",
        ],
    )
