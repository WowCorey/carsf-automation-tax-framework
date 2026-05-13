"""Prototype mixed-unit handling for grouped CARSF previews."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


MIXED_UNIT_NON_CLAIMS = [
    "Mixed-unit exposure outputs are prototype-only and are not a tax base.",
    "Value-weighted exposure index is not a replacement for sector schedules.",
    "No legal, tax, ATO, Treasury, OECD, BEPS, or economic validation is implied.",
]
RISK_SCORE = {"low": 0.25, "medium": 0.55, "high": 0.85}


@dataclass(frozen=True)
class UnitCompatibilityResult:
    """Canonical output-unit compatibility result."""

    compatible: bool
    unit_set: list[str]
    comparable_unit: str | None
    reason: str
    warnings: list[str] = field(default_factory=list)
    review_required: bool = False


@dataclass(frozen=True)
class MixedUnitExposureResult:
    """Preview handling where direct output aggregation may be unsafe."""

    method: str
    standalone_liability_sum: float
    schedule_level_results: list[dict[str, Any]] = field(default_factory=list)
    value_weighted_exposure_index: float | None = None
    warnings: list[str] = field(default_factory=list)
    review_required: bool = False
    non_claims: list[str] = field(default_factory=lambda: list(MIXED_UNIT_NON_CLAIMS))


def _unit(row: dict[str, Any]) -> str:
    if "canonical_output_unit" in row:
        return str(row["canonical_output_unit"])
    output = row.get("output", {})
    if isinstance(output, dict) and "unit" in output:
        return str(output["unit"])
    return ""


def _conversion_metadata(row: dict[str, Any]) -> Any:
    return row.get("conversion_metadata") or row.get("unit_conversion_metadata")


def _liability(row: dict[str, Any]) -> float:
    if "liability" in row:
        return float(row["liability"])
    outputs = row.get("outputs", {})
    if isinstance(outputs, dict):
        return float(outputs.get("liability", 0.0))
    return 0.0


def _revenue(row: dict[str, Any]) -> float:
    for key in ("revenue", "reported_revenue"):
        if key in row:
            return float(row[key])
    aava_inputs = row.get("aava_inputs", {})
    if isinstance(aava_inputs, dict):
        return float(aava_inputs.get("australian_attributable_revenue", 0.0))
    return 0.0


def _aava(row: dict[str, Any]) -> float:
    if "aava" in row:
        return float(row["aava"])
    outputs = row.get("outputs", {})
    if isinstance(outputs, dict):
        return float(outputs.get("aava", 0.0))
    return 0.0


def _risk_value(row: dict[str, Any]) -> float:
    if "risk_score" in row:
        return float(row["risk_score"])
    risk_level = str(row.get("risk_level", row.get("standalone_risk", "low"))).lower()
    if risk_level in RISK_SCORE:
        return RISK_SCORE[risk_level]
    if "aii" in row:
        return min(1.0, max(0.0, float(row["aii"])))
    outputs = row.get("outputs", {})
    if isinstance(outputs, dict) and "aii" in outputs:
        return min(1.0, max(0.0, float(outputs["aii"])))
    return RISK_SCORE["low"]


def evaluate_unit_compatibility(entities_or_activities: list[dict[str, Any]]) -> UnitCompatibilityResult:
    """Check whether output units can be aggregated without conversion."""

    units = sorted({_unit(row) for row in entities_or_activities if _unit(row)})
    conversion_present = any(_conversion_metadata(row) for row in entities_or_activities)
    warnings = [
        "Mixed-unit compatibility is a prototype review check only.",
    ]
    if not units:
        return UnitCompatibilityResult(
            compatible=False,
            unit_set=[],
            comparable_unit=None,
            reason="No canonical output units were supplied.",
            warnings=warnings,
            review_required=True,
        )
    if len(units) == 1:
        if conversion_present:
            warnings.append("Conversion metadata was supplied even though units match; review is still required.")
        return UnitCompatibilityResult(
            compatible=True,
            unit_set=units,
            comparable_unit=units[0],
            reason="All canonical output units match.",
            warnings=warnings,
            review_required=conversion_present,
        )
    if conversion_present:
        warnings.append("Conversion metadata exists, but conversion remains review-required in this prototype.")
    warnings.append("Output and HLE aggregation are prohibited while canonical output units differ.")
    return UnitCompatibilityResult(
        compatible=False,
        unit_set=units,
        comparable_unit=None,
        reason="Canonical output units differ; direct output/HLE aggregation is prohibited.",
        warnings=warnings,
        review_required=True,
    )


def _schedule_level_results(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for row in rows:
        results.append(
            {
                "entity_id": row.get("entity_id", row.get("activity_id", "")),
                "schedule_id": row.get("schedule_id", ""),
                "canonical_output_unit": _unit(row),
                "revenue": _revenue(row),
                "aava": _aava(row),
                "liability": _liability(row),
                "risk_score": _risk_value(row),
            }
        )
    return results


def _value_weighted_exposure(rows: list[dict[str, Any]]) -> float | None:
    weights = [_revenue(row) if _revenue(row) > 0 else max(0.0, _aava(row)) for row in rows]
    total = sum(weights)
    if total <= 0:
        return None
    return sum((weight / total) * _risk_value(row) for row, weight in zip(rows, weights, strict=True))


def evaluate_mixed_unit_exposure(entities_or_activities: list[dict[str, Any]]) -> MixedUnitExposureResult:
    """Evaluate non-operative exposure handling for mixed output units."""

    compatibility = evaluate_unit_compatibility(entities_or_activities)
    liability_sum = sum(_liability(row) for row in entities_or_activities)
    schedule_results = _schedule_level_results(entities_or_activities)
    warnings = [
        *compatibility.warnings,
        "Value-weighted exposure index is prototype-only, not a tax base, and not a replacement for sector schedules.",
    ]
    if compatibility.compatible:
        method = "compatible_units_normal_aggregation_available"
        exposure_index = _value_weighted_exposure(entities_or_activities)
    else:
        method = "mixed_units_no_direct_output_or_hle_aggregation"
        exposure_index = _value_weighted_exposure(entities_or_activities)
        warnings.append("Standalone liability summation and schedule-level comparison are allowed; direct output/HLE aggregation is not.")
    return MixedUnitExposureResult(
        method=method,
        standalone_liability_sum=liability_sum,
        schedule_level_results=schedule_results,
        value_weighted_exposure_index=exposure_index,
        warnings=warnings,
        review_required=compatibility.review_required or not compatibility.compatible,
    )
