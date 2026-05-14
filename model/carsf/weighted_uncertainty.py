"""Deterministic uncertainty wrappers for weighted subgroup outputs."""

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
class WeightedSubgroupUncertaintyInput:
    uncertainty_id: str
    weighted_aggregation_result: dict[str, Any]
    subgroup_residual_gap_ranges: dict[str, UncertaintyRange]
    subgroup_high_critical_share_ranges: dict[str, UncertaintyRange]
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["subgroup_residual_gap_ranges"] = {
            key: value.to_jsonable() for key, value in self.subgroup_residual_gap_ranges.items()
        }
        payload["subgroup_high_critical_share_ranges"] = {
            key: value.to_jsonable() for key, value in self.subgroup_high_critical_share_ranges.items()
        }
        return payload


@dataclass(frozen=True)
class WeightedSubgroupUncertaintyResult:
    uncertainty_id: str
    subgroup_results: list[dict[str, Any]]
    overall_range_sensitivity: str
    highest_uncertainty_subgroups: list[str]
    stable_high_risk_subgroups: list[str]
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(UNCERTAINTY_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _range_map(source: dict[str, Any] | None) -> dict[str, UncertaintyRange]:
    return {
        str(key): uncertainty_range_from_mapping(value)
        for key, value in (source or {}).items()
    }


def _input_from_mapping(source: WeightedSubgroupUncertaintyInput | dict[str, Any]) -> WeightedSubgroupUncertaintyInput:
    if isinstance(source, WeightedSubgroupUncertaintyInput):
        return source
    return WeightedSubgroupUncertaintyInput(
        uncertainty_id=str(source["uncertainty_id"]),
        weighted_aggregation_result=dict(source["weighted_aggregation_result"]),
        subgroup_residual_gap_ranges=_range_map(source.get("subgroup_residual_gap_ranges")),
        subgroup_high_critical_share_ranges=_range_map(source.get("subgroup_high_critical_share_ranges")),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def _sensitivity_rank(stability: str) -> int:
    return {
        "not_assessable": 3,
        "fragile": 3,
        "moderately_sensitive": 2,
        "stable": 1,
    }.get(stability, 0)


def _sensitivity_from_rank(rank: int) -> str:
    if rank >= 3:
        return "fragile"
    if rank == 2:
        return "moderately_sensitive"
    if rank == 1:
        return "stable"
    return "not_assessable"


def evaluate_weighted_uncertainty(
    inputs: WeightedSubgroupUncertaintyInput | dict[str, Any],
) -> WeightedSubgroupUncertaintyResult:
    """Apply deterministic ranges to synthetic weighted subgroup outputs."""

    input_obj = _input_from_mapping(inputs)
    aggregation = input_obj.weighted_aggregation_result
    warnings = [
        "Weighted subgroup uncertainty is deterministic placeholder-only and not population uncertainty.",
        "Firm-level CARSF liability is not modified by weighted uncertainty outputs.",
    ]
    if aggregation.get("representative_of_real_population") is not False:
        warnings.append("Weighted aggregation input is not explicitly marked as non-representative; review required.")

    subgroup_rows = aggregation.get("subgroup_results", [])
    subgroup_ids = [str(row.get("subgroup_id")) for row in subgroup_rows]
    results: list[dict[str, Any]] = []
    highest_uncertainty: list[str] = []
    stable_high_risk: list[str] = []
    max_rank = 0
    for row in subgroup_rows:
        subgroup_id = str(row.get("subgroup_id"))
        residual_result = None
        share_result = None
        subgroup_warnings = []
        if subgroup_id in input_obj.subgroup_residual_gap_ranges:
            residual_result = evaluate_uncertainty_range(input_obj.subgroup_residual_gap_ranges[subgroup_id])
            max_rank = max(max_rank, _sensitivity_rank(residual_result.stability_band))
        else:
            subgroup_warnings.append(f"missing residual gap range for subgroup: {subgroup_id}")
        if subgroup_id in input_obj.subgroup_high_critical_share_ranges:
            share_result = evaluate_uncertainty_range(input_obj.subgroup_high_critical_share_ranges[subgroup_id])
            max_rank = max(max_rank, _sensitivity_rank(share_result.stability_band))
        else:
            subgroup_warnings.append(f"missing high/critical share range for subgroup: {subgroup_id}")
        if subgroup_warnings:
            warnings.extend(subgroup_warnings)
        stability_values = [
            item.stability_band
            for item in [residual_result, share_result]
            if item is not None
        ]
        subgroup_sensitivity = _sensitivity_from_rank(max((_sensitivity_rank(item) for item in stability_values), default=0))
        if subgroup_sensitivity in {"fragile", "not_assessable"}:
            highest_uncertainty.append(subgroup_id)
        if share_result is not None and share_result.low >= 0.75 and share_result.base >= 0.75 and share_result.high >= 0.75:
            stable_high_risk.append(subgroup_id)
        results.append(
            {
                "subgroup_id": subgroup_id,
                "subgroup_name": row.get("subgroup_name", subgroup_id),
                "residual_gap_range": None if residual_result is None else residual_result.to_jsonable(),
                "high_critical_share_range": None if share_result is None else share_result.to_jsonable(),
                "subgroup_range_sensitivity": subgroup_sensitivity,
                "representative_of_real_population": False,
                "warnings": subgroup_warnings,
            }
        )
    unused_residual = sorted(set(input_obj.subgroup_residual_gap_ranges) - set(subgroup_ids))
    unused_share = sorted(set(input_obj.subgroup_high_critical_share_ranges) - set(subgroup_ids))
    for subgroup_id in unused_residual:
        warnings.append(f"residual gap range supplied for unknown subgroup: {subgroup_id}")
    for subgroup_id in unused_share:
        warnings.append(f"high/critical share range supplied for unknown subgroup: {subgroup_id}")

    return WeightedSubgroupUncertaintyResult(
        uncertainty_id=input_obj.uncertainty_id,
        subgroup_results=results,
        overall_range_sensitivity=_sensitivity_from_rank(max_rank),
        highest_uncertainty_subgroups=sorted(set(highest_uncertainty)),
        stable_high_risk_subgroups=sorted(set(stable_high_risk)),
        warnings=warnings,
    )
