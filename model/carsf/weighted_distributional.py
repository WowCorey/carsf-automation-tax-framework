"""Weighted synthetic household distributional aggregation shell."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .household_weights import (
    HOUSEHOLD_WEIGHTING_NON_CLAIMS,
    HouseholdWeight,
    evaluate_household_weight,
    household_weight_from_mapping,
)
from .subgroups import SubgroupDefinition, assign_subgroups, subgroup_definition_from_mapping


@dataclass(frozen=True)
class WeightedDistributionalInput:
    aggregation_id: str
    scenario_results: list[dict[str, Any]]
    household_weights: list[HouseholdWeight]
    subgroup_definitions: list[SubgroupDefinition]
    calibration_status: str
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["household_weights"] = [weight.to_jsonable() for weight in self.household_weights]
        payload["subgroup_definitions"] = [definition.to_jsonable() for definition in self.subgroup_definitions]
        return payload


@dataclass(frozen=True)
class WeightedSubgroupResult:
    subgroup_id: str
    subgroup_name: str
    scenario_count: int
    total_synthetic_weight: float
    weighted_average_residual_gap: float | None
    weighted_high_or_critical_share: float | None
    highest_risk_scenarios: list[str] = field(default_factory=list)
    representativeness_warning: bool = True
    warnings: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class WeightedDistributionalResult:
    aggregation_id: str
    scenario_count: int
    total_synthetic_weight: float
    overall_weighted_average_residual_gap: float | None
    overall_weighted_high_or_critical_share: float | None
    subgroup_results: list[WeightedSubgroupResult]
    highest_risk_subgroups: list[str] = field(default_factory=list)
    calibration_status: str = "not_calibrated"
    representative_of_real_population: bool = False
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(HOUSEHOLD_WEIGHTING_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["subgroup_results"] = [item.to_jsonable() for item in self.subgroup_results]
        return payload


def _input_from_mapping(source: WeightedDistributionalInput | dict[str, Any]) -> WeightedDistributionalInput:
    if isinstance(source, WeightedDistributionalInput):
        return source
    return WeightedDistributionalInput(
        aggregation_id=str(source["aggregation_id"]),
        scenario_results=list(source.get("scenario_results", [])),
        household_weights=[household_weight_from_mapping(item) for item in source.get("household_weights", [])],
        subgroup_definitions=[subgroup_definition_from_mapping(item) for item in source.get("subgroup_definitions", [])],
        calibration_status=str(source.get("calibration_status", "not_calibrated")),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def _scenario_id(row: dict[str, Any]) -> str:
    return str(row.get("scenario_id") or row.get("household_id") or "")


def _severity(row: dict[str, Any]) -> tuple[int, float, str]:
    scores = {"critical": 3, "high": 2, "medium": 1, "low": 0, "not_assessable": -1}
    return (
        scores.get(str(row.get("household_shock_band")), 0),
        float(row.get("residual_household_gap_after_support", 0.0)),
        _scenario_id(row),
    )


def _weighted_average(rows: list[tuple[dict[str, Any], float]]) -> float | None:
    total_weight = sum(weight for _, weight in rows)
    if total_weight <= 0:
        return None
    return sum(float(row.get("residual_household_gap_after_support", 0.0)) * weight for row, weight in rows) / total_weight


def _weighted_high_critical_share(rows: list[tuple[dict[str, Any], float]]) -> float | None:
    total_weight = sum(weight for _, weight in rows)
    if total_weight <= 0:
        return None
    high_weight = sum(
        weight
        for row, weight in rows
        if str(row.get("household_shock_band")) in {"high", "critical"}
    )
    return high_weight / total_weight


def run_weighted_distributional_aggregation(
    inputs: WeightedDistributionalInput | dict[str, Any],
) -> WeightedDistributionalResult:
    """Aggregate synthetic household scenarios with placeholder weights."""

    input_obj = _input_from_mapping(inputs)
    if not input_obj.scenario_results:
        raise ValueError("weighted distributional aggregation requires at least one scenario")
    scenario_by_id = {_scenario_id(row): row for row in input_obj.scenario_results}
    if "" in scenario_by_id:
        raise ValueError("each scenario result must include scenario_id or household_id")
    definitions = sorted(input_obj.subgroup_definitions, key=lambda item: item.subgroup_id)
    definition_by_id = {definition.subgroup_id: definition for definition in definitions}
    if len(definition_by_id) != len(definitions):
        raise ValueError("subgroup definitions must have unique subgroup_id values")

    evaluated_weights = [evaluate_household_weight(weight) for weight in input_obj.household_weights]
    warnings = [
        "Weighted distributional aggregation uses synthetic placeholder weights only.",
        "Results are not representative of real Australian households.",
        "Firm-level CARSF liability is not modified by weighted distributional outputs.",
    ]
    for weight in evaluated_weights:
        if weight.scenario_id not in scenario_by_id:
            raise ValueError(f"household weight references unknown scenario_id: {weight.scenario_id}")
        if weight.subgroup_id not in definition_by_id:
            raise ValueError(f"household weight references unknown subgroup_id: {weight.subgroup_id}")

    assignments = {
        scenario_id: assign_subgroups(row, definitions)
        for scenario_id, row in sorted(scenario_by_id.items())
    }
    assignment_by_scenario = {scenario_id: set(assignment.subgroup_ids) for scenario_id, assignment in assignments.items()}

    weighted_rows = [(scenario_by_id[weight.scenario_id], weight.weight_value) for weight in evaluated_weights]
    total_weight = sum(weight.weight_value for weight in evaluated_weights)
    subgroup_results: list[WeightedSubgroupResult] = []
    for definition in definitions:
        subgroup_weights = [weight for weight in evaluated_weights if weight.subgroup_id == definition.subgroup_id]
        subgroup_rows = [(scenario_by_id[weight.scenario_id], weight.weight_value) for weight in subgroup_weights]
        subgroup_warnings = [
            "Subgroup result is synthetic placeholder-only and not representative.",
        ]
        for weight in subgroup_weights:
            if definition.subgroup_id not in assignment_by_scenario.get(weight.scenario_id, set()):
                subgroup_warnings.append(
                    f"weight for {weight.scenario_id} is assigned to {definition.subgroup_id} but does not match subgroup filters"
                )
        subgroup_total = sum(weight.weight_value for weight in subgroup_weights)
        ordered = sorted(
            [scenario_by_id[weight.scenario_id] for weight in subgroup_weights],
            key=lambda row: (-_severity(row)[0], -_severity(row)[1], _severity(row)[2]),
        )
        subgroup_results.append(
            WeightedSubgroupResult(
                subgroup_id=definition.subgroup_id,
                subgroup_name=definition.subgroup_name,
                scenario_count=len({weight.scenario_id for weight in subgroup_weights}),
                total_synthetic_weight=subgroup_total,
                weighted_average_residual_gap=_weighted_average(subgroup_rows),
                weighted_high_or_critical_share=_weighted_high_critical_share(subgroup_rows),
                highest_risk_scenarios=[_scenario_id(row) for row in ordered[:3]],
                representativeness_warning=True,
                warnings=subgroup_warnings,
            )
        )
    highest_subgroups = sorted(
        subgroup_results,
        key=lambda item: (
            -(item.weighted_high_or_critical_share if item.weighted_high_or_critical_share is not None else -1),
            -(item.weighted_average_residual_gap if item.weighted_average_residual_gap is not None else -1),
            item.subgroup_id,
        ),
    )
    if total_weight <= 0:
        warnings.append("Total synthetic weight is zero; weighted averages are not assessable.")
    if input_obj.calibration_status != "calibrated_external_reviewed":
        warnings.append("Calibration status does not support real-world representativeness claims.")
    return WeightedDistributionalResult(
        aggregation_id=input_obj.aggregation_id,
        scenario_count=len(input_obj.scenario_results),
        total_synthetic_weight=total_weight,
        overall_weighted_average_residual_gap=_weighted_average(weighted_rows),
        overall_weighted_high_or_critical_share=_weighted_high_critical_share(weighted_rows),
        subgroup_results=subgroup_results,
        highest_risk_subgroups=[item.subgroup_id for item in highest_subgroups[:3]],
        calibration_status=input_obj.calibration_status,
        representative_of_real_population=False,
        warnings=warnings,
    )
