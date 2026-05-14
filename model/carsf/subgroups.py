"""Synthetic household subgroup assignment helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .household_weights import HOUSEHOLD_WEIGHTING_NON_CLAIMS


@dataclass(frozen=True)
class SubgroupDefinition:
    subgroup_id: str
    subgroup_name: str
    household_type_filter: str | None = None
    income_band_filter: str | None = None
    region_type_filter: str | None = None
    reemployment_risk_filter: str | None = None
    budget_stress_filter: str | None = None
    regional_stress_filter: str | None = None
    illustrative_placeholder_only: bool = True
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SubgroupAssignment:
    scenario_id: str
    subgroup_ids: list[str]
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(HOUSEHOLD_WEIGHTING_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def subgroup_definition_from_mapping(source: SubgroupDefinition | dict[str, Any]) -> SubgroupDefinition:
    if isinstance(source, SubgroupDefinition):
        return source
    return SubgroupDefinition(
        subgroup_id=str(source["subgroup_id"]),
        subgroup_name=str(source.get("subgroup_name", source["subgroup_id"])),
        household_type_filter=None if source.get("household_type_filter") is None else str(source.get("household_type_filter")),
        income_band_filter=None if source.get("income_band_filter") is None else str(source.get("income_band_filter")),
        region_type_filter=None if source.get("region_type_filter") is None else str(source.get("region_type_filter")),
        reemployment_risk_filter=None if source.get("reemployment_risk_filter") is None else str(source.get("reemployment_risk_filter")),
        budget_stress_filter=None if source.get("budget_stress_filter") is None else str(source.get("budget_stress_filter")),
        regional_stress_filter=None if source.get("regional_stress_filter") is None else str(source.get("regional_stress_filter")),
        illustrative_placeholder_only=bool(source.get("illustrative_placeholder_only", True)),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def _field_matches(scenario: dict[str, Any], field_name: str, expected: str | None, warnings: list[str]) -> bool:
    if expected is None:
        return True
    if field_name not in scenario or scenario.get(field_name) is None:
        warnings.append(f"missing field for subgroup filter: {field_name}")
        return False
    return str(scenario.get(field_name)) == expected


def assign_subgroups(
    scenario_result: dict[str, Any],
    subgroup_definitions: list[SubgroupDefinition | dict[str, Any]],
) -> SubgroupAssignment:
    """Assign a synthetic household scenario to deterministic placeholder subgroups."""

    scenario_id = str(scenario_result.get("scenario_id") or scenario_result.get("household_id") or "")
    if not scenario_id:
        raise ValueError("scenario_result must include scenario_id or household_id")
    subgroup_ids: list[str] = []
    warnings: list[str] = [
        "Subgroup assignment is synthetic placeholder-only and not real demographic classification.",
    ]
    for definition_source in sorted(
        [subgroup_definition_from_mapping(item) for item in subgroup_definitions],
        key=lambda item: item.subgroup_id,
    ):
        if definition_source.illustrative_placeholder_only is not True:
            raise ValueError("subgroup definition must be illustrative_placeholder_only")
        matched = (
            _field_matches(scenario_result, "household_type", definition_source.household_type_filter, warnings)
            and _field_matches(scenario_result, "income_band", definition_source.income_band_filter, warnings)
            and _field_matches(scenario_result, "region_type", definition_source.region_type_filter, warnings)
            and _field_matches(scenario_result, "reemployment_risk_band", definition_source.reemployment_risk_filter, warnings)
            and _field_matches(scenario_result, "budget_stress_band", definition_source.budget_stress_filter, warnings)
            and _field_matches(scenario_result, "regional_stress_band", definition_source.regional_stress_filter, warnings)
        )
        if matched:
            subgroup_ids.append(definition_source.subgroup_id)
    return SubgroupAssignment(
        scenario_id=scenario_id,
        subgroup_ids=sorted(subgroup_ids),
        warnings=warnings,
    )
