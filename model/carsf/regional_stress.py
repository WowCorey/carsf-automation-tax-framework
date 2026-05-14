"""Placeholder regional stress scoring for synthetic households."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any

from .households import DISTRIBUTIONAL_NON_CLAIMS


@dataclass(frozen=True)
class RegionalStressInput:
    region_id: str
    region_type: str
    automation_exposure_placeholder: float
    labour_market_depth_placeholder: float
    retraining_access_placeholder: float
    housing_cost_pressure_placeholder: float
    transport_access_placeholder: float
    illustrative_placeholder_only: bool = True
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RegionalStressResult:
    region_id: str
    regional_stress_score: float
    regional_stress_band: str
    drivers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(DISTRIBUTIONAL_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _finite_number(value: Any, field_name: str) -> float:
    numeric = float(value)
    if not isfinite(numeric):
        raise ValueError(f"{field_name} must be finite")
    return numeric


def _bounded_score(value: Any, field_name: str) -> float:
    numeric = _finite_number(value, field_name)
    if not 0 <= numeric <= 1:
        raise ValueError(f"{field_name} must be in [0, 1]")
    return numeric


def _input_from_mapping(source: dict[str, Any]) -> RegionalStressInput:
    return RegionalStressInput(
        region_id=str(source["region_id"]),
        region_type=str(source.get("region_type", "placeholder_region")),
        automation_exposure_placeholder=source["automation_exposure_placeholder"],
        labour_market_depth_placeholder=source["labour_market_depth_placeholder"],
        retraining_access_placeholder=source["retraining_access_placeholder"],
        housing_cost_pressure_placeholder=source["housing_cost_pressure_placeholder"],
        transport_access_placeholder=source["transport_access_placeholder"],
        illustrative_placeholder_only=bool(source.get("illustrative_placeholder_only", True)),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def regional_stress_input_from_mapping(source: RegionalStressInput | dict[str, Any]) -> RegionalStressInput:
    if isinstance(source, RegionalStressInput):
        return source
    return _input_from_mapping(source)


def _band(score: float) -> str:
    if score < 0.25:
        return "low"
    if score < 0.50:
        return "medium"
    if score < 0.75:
        return "high"
    return "critical"


def evaluate_regional_stress(inputs: RegionalStressInput | dict[str, Any]) -> RegionalStressResult:
    """Score regional stress using placeholder vulnerability inputs."""

    if isinstance(inputs, dict):
        inputs = _input_from_mapping(inputs)
    if inputs.illustrative_placeholder_only is not True:
        raise ValueError("regional stress input must be illustrative_placeholder_only")
    automation = _bounded_score(inputs.automation_exposure_placeholder, "automation_exposure_placeholder")
    labour_depth = _bounded_score(inputs.labour_market_depth_placeholder, "labour_market_depth_placeholder")
    retraining = _bounded_score(inputs.retraining_access_placeholder, "retraining_access_placeholder")
    housing = _bounded_score(inputs.housing_cost_pressure_placeholder, "housing_cost_pressure_placeholder")
    transport = _bounded_score(inputs.transport_access_placeholder, "transport_access_placeholder")
    score = (
        automation * 0.25
        + (1 - labour_depth) * 0.20
        + (1 - retraining) * 0.20
        + housing * 0.20
        + (1 - transport) * 0.15
    )
    drivers: list[str] = []
    if automation >= 0.70:
        drivers.append("high automation exposure")
    if labour_depth <= 0.35:
        drivers.append("limited labour-market depth")
    if retraining <= 0.35:
        drivers.append("limited retraining access")
    if housing >= 0.70:
        drivers.append("high housing cost pressure")
    if transport <= 0.35:
        drivers.append("limited transport access")

    return RegionalStressResult(
        region_id=inputs.region_id,
        regional_stress_score=score,
        regional_stress_band=_band(score),
        drivers=drivers,
        warnings=[
            "Regional stress score is placeholder-only and not real regional modelling.",
            "No ABS, Census, DSS, Services Australia, Treasury, PBO, labour-market, or geographic data is used.",
        ],
    )
