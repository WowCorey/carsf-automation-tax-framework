"""Prototype grouped-entity aggregation previews.

This module is a non-operative modelling aid. It does not implement tax-law
grouping, transfer-pricing adjustment, legal attribution, Treasury guidance, or
ATO guidance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .levy import calculate_liability
from .types import LevyParameters


RISK_RANK = {"low": 0, "medium": 1, "high": 2}


@dataclass(frozen=True)
class EntityInput:
    """Standalone entity snapshot used for a group preview."""

    entity_id: str
    description: str
    revenue: float
    output_value: float
    qlc: float
    hle: float
    aii: float
    nltg: float
    aava: float
    liability: float
    role: str
    flags: list[str] = field(default_factory=list)
    canonical_output_unit: str = ""
    capital_base: float = 0.0
    verified_credits: float = 0.0
    standalone_risk: str = "low"


@dataclass(frozen=True)
class AggregationResult:
    """Prototype grouped-entity aggregation preview."""

    group_id: str
    entity_count: int
    aggregate_revenue: float
    aggregate_output: float | None
    aggregate_qlc: float
    aggregate_hle: float | None
    weighted_aii: float | None
    aggregate_nltg_preview: float | None
    aggregate_aava: float
    aggregate_liability_preview: float
    standalone_entity_liability_sum: float
    group_recomputed_liability_preview: float | None
    flags: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    review_required: bool = False
    placeholder_basis: list[str] = field(default_factory=list)
    risk_level: str = "low"
    output_units_match: bool = True


def risk_rank(level: str) -> int:
    return RISK_RANK.get(str(level).lower(), 0)


def _entity_from_mapping(row: dict[str, Any]) -> EntityInput:
    outputs = row.get("outputs", {})
    if not isinstance(outputs, dict):
        outputs = {}
    return EntityInput(
        entity_id=str(row.get("entity_id", row.get("id", ""))),
        description=str(row.get("description", "")),
        revenue=float(row.get("revenue", row.get("australian_attributable_revenue", 0.0))),
        output_value=float(row.get("output_value", row.get("output", {}).get("value", 0.0) if isinstance(row.get("output"), dict) else 0.0)),
        qlc=float(row.get("qlc", outputs.get("qlc", 0.0))),
        hle=float(row.get("hle", outputs.get("hle", 0.0))),
        aii=float(row.get("aii", outputs.get("aii", 0.0))),
        nltg=float(row.get("nltg", outputs.get("nltg", 0.0))),
        aava=float(row.get("aava", outputs.get("aava", 0.0))),
        liability=float(row.get("liability", outputs.get("liability", 0.0))),
        role=str(row.get("role", "")),
        flags=[str(flag) for flag in row.get("flags", [])],
        canonical_output_unit=str(row.get("canonical_output_unit", row.get("output", {}).get("unit", "") if isinstance(row.get("output"), dict) else "")),
        capital_base=float(row.get("capital_base", 0.0)),
        verified_credits=float(row.get("verified_credits", 0.0)),
        standalone_risk=str(row.get("standalone_risk", "low")),
    )


def _entity_from_object(value: Any) -> EntityInput:
    if isinstance(value, EntityInput):
        return value
    if isinstance(value, dict):
        return _entity_from_mapping(value)
    outputs = getattr(value, "outputs")
    inputs = getattr(value, "inputs", {})
    output = inputs.get("output", {}) if isinstance(inputs, dict) else {}
    return EntityInput(
        entity_id=str(getattr(value, "id", "")),
        description=str(getattr(value, "business_description", "")),
        revenue=float(inputs.get("aava_inputs", {}).get("australian_attributable_revenue", 0.0)),
        output_value=float(output.get("value", 0.0)),
        qlc=float(outputs.qlc),
        hle=float(outputs.hle),
        aii=float(outputs.aii),
        nltg=float(outputs.nltg),
        aava=float(outputs.aava),
        liability=float(outputs.liability),
        role=str(getattr(value, "schedule", "")),
        flags=list(getattr(value, "avoidance_result", None).flags if getattr(value, "avoidance_result", None) else []),
        canonical_output_unit=str(output.get("unit", "")),
        capital_base=float(inputs.get("capital_base", 0.0)),
        verified_credits=float(inputs.get("credits", {}).get("verified_credits", 0.0)),
        standalone_risk=str(getattr(getattr(value, "avoidance_result", None), "risk_level", "low")),
    )


def _entities(entity_results: list[Any] | dict[str, Any]) -> list[EntityInput]:
    if isinstance(entity_results, dict):
        rows = entity_results.get("entities", [])
        if not isinstance(rows, list):
            rows = list(entity_results.values())
    else:
        rows = entity_results
    return [_entity_from_object(row) for row in rows]


def _unique_flags(entities: list[EntityInput], group_example: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    for entity in entities:
        for flag in entity.flags:
            if flag and flag not in flags:
                flags.append(flag)
    metadata = group_example.get("risk_metadata", {})
    if isinstance(metadata, dict):
        if metadata.get("entity_splitting_risk") and "ENTITY_SPLITTING_PREVIEW" not in flags:
            flags.append("ENTITY_SPLITTING_PREVIEW")
        if metadata.get("offshore_automation_service") and "OFFSHORE_AUTOMATION_SERVICE" not in flags:
            flags.append("OFFSHORE_AUTOMATION_SERVICE")
        if metadata.get("related_party_ai_service_fees") and "RELATED_PARTY_AI_SERVICE_FEES" not in flags:
            flags.append("RELATED_PARTY_AI_SERVICE_FEES")
    return flags


def _levy_parameters(group_example: dict[str, Any]) -> LevyParameters | None:
    raw = group_example.get("recompute_parameters", {})
    if not isinstance(raw, dict):
        return None
    required = {
        "frv_standard",
        "lambda_sector",
        "lambda_combined",
        "theta",
        "uplift_rate",
        "rent_tax_rate",
    }
    if not required.issubset(raw):
        return None
    return LevyParameters(
        frv_standard=float(raw["frv_standard"]),
        lambda_sector=float(raw["lambda_sector"]),
        lambda_combined=float(raw["lambda_combined"]),
        theta=float(raw["theta"]),
        uplift_rate=float(raw["uplift_rate"]),
        rent_tax_rate=float(raw["rent_tax_rate"]),
    )


def _risk_level(flags: list[str], standalone_max: str, output_units_match: bool) -> str:
    if not output_units_match:
        return "high"
    if len(flags) >= 3 or risk_rank(standalone_max) >= risk_rank("high"):
        return "high"
    if flags or risk_rank(standalone_max) >= risk_rank("medium"):
        return "medium"
    return "low"


def evaluate_group_aggregation(
    group_example: dict[str, Any],
    entity_results: list[Any] | dict[str, Any],
) -> AggregationResult:
    """Evaluate a prototype grouped-entity aggregation preview."""

    entities = _entities(entity_results)
    group_id = str(group_example.get("group_id", group_example.get("example_id", "group_preview")))
    aggregate_revenue = sum(entity.revenue for entity in entities)
    aggregate_qlc = sum(entity.qlc for entity in entities)
    aggregate_aava = sum(entity.aava for entity in entities)
    standalone_liability_sum = sum(entity.liability for entity in entities)
    aggregate_liability_preview = standalone_liability_sum
    output_units = {entity.canonical_output_unit for entity in entities if entity.canonical_output_unit}
    output_units_match = len(output_units) <= 1
    flags = _unique_flags(entities, group_example)
    warnings = [
        "Prototype grouped-entity preview only; no legal, tax, Treasury, or ATO validation is provided.",
        "This is not full tax-law grouping, transfer-pricing, or attribution logic.",
    ]

    if not output_units_match:
        warnings.append("Canonical output units differ; output, HLE, weighted AII, and group NLTG were not blindly aggregated.")
        aggregate_output = None
        aggregate_hle = None
        weighted_aii = None
        aggregate_nltg_preview = None
        group_recomputed_liability_preview = None
    else:
        aggregate_output = sum(entity.output_value for entity in entities)
        aggregate_hle = sum(entity.hle for entity in entities)
        if aggregate_output > 0:
            weighted_aii = sum(entity.aii * entity.output_value for entity in entities) / aggregate_output
        elif aggregate_revenue > 0:
            weighted_aii = sum(entity.aii * entity.revenue for entity in entities) / aggregate_revenue
        else:
            weighted_aii = 0.0
        aggregate_nltg_preview = max(0.0, aggregate_hle * weighted_aii - aggregate_qlc)
        params = _levy_parameters(group_example)
        if params is None:
            group_recomputed_liability_preview = None
            warnings.append("Group-level liability was not recomputed because recompute parameters were not supplied.")
        else:
            capital_base = float(
                group_example.get("capital_base", sum(entity.capital_base for entity in entities))
            )
            verified_credits = float(
                group_example.get("verified_credits", sum(entity.verified_credits for entity in entities))
            )
            group_recomputed_liability_preview = calculate_liability(
                nltg=aggregate_nltg_preview,
                aava=aggregate_aava,
                capital_base=capital_base,
                verified_credits=verified_credits,
                params=params,
            ).liability
            aggregate_liability_preview = group_recomputed_liability_preview

    standalone_max_risk = max((entity.standalone_risk for entity in entities), key=risk_rank, default="low")
    risk_level = _risk_level(flags, standalone_max_risk, output_units_match)
    review_required = bool(flags) or not output_units_match or risk_level != "low"

    return AggregationResult(
        group_id=group_id,
        entity_count=len(entities),
        aggregate_revenue=aggregate_revenue,
        aggregate_output=aggregate_output,
        aggregate_qlc=aggregate_qlc,
        aggregate_hle=aggregate_hle,
        weighted_aii=weighted_aii,
        aggregate_nltg_preview=aggregate_nltg_preview,
        aggregate_aava=aggregate_aava,
        aggregate_liability_preview=aggregate_liability_preview,
        standalone_entity_liability_sum=standalone_liability_sum,
        group_recomputed_liability_preview=group_recomputed_liability_preview,
        flags=flags,
        warnings=warnings,
        review_required=review_required,
        placeholder_basis=[
            "Grouped aggregation is a prototype modelling preview only.",
            str(group_example.get("placeholder_notice", "No group placeholder notice supplied.")),
            "Do not use this result as legal grouping, tax assessment, Treasury guidance, or ATO guidance.",
        ],
        risk_level=risk_level,
        output_units_match=output_units_match,
    )
