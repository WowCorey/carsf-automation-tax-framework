"""Prototype grouped-entity review flags for CARSF examples.

This is not full tax-law grouping logic. It only identifies examples that
should be reviewed for aggregation, attribution, or related-entity structuring.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


ENTITY_SPLITTING_SAFE_HARBOUR = "ENTITY_SPLITTING_SAFE_HARBOUR"
RELATED_OPERATING_ENTITIES = "RELATED_OPERATING_ENTITIES"
SEPARATED_IP_PLATFORM_EMPLOYER = "SEPARATED_IP_PLATFORM_EMPLOYER"
THIN_AUSTRALIAN_EMPLOYING_ENTITY = "THIN_AUSTRALIAN_EMPLOYING_ENTITY"


@dataclass(frozen=True)
class GroupingRiskResult:
    """Prototype grouped-entity aggregation review result."""

    risk_level: str
    flags: list[str] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    recommended_review: list[str] = field(default_factory=list)
    placeholder_basis: list[str] = field(default_factory=list)


def _output_value(outputs: Any, field_name: str) -> float:
    if isinstance(outputs, dict):
        value = outputs[field_name]
    else:
        value = getattr(outputs, field_name)
    return float(value)


def _metadata(example: dict[str, Any]) -> dict[str, Any]:
    metadata = example.get("risk_metadata", {})
    return metadata if isinstance(metadata, dict) else {}


def _red_team_flags(example: dict[str, Any]) -> set[str]:
    notes = example.get("red_team_notes", {})
    if not isinstance(notes, dict):
        return set()
    flags = notes.get("flags", [])
    return {str(flag).lower() for flag in flags if flag}


def _qlc_hle_ratio(outputs: Any) -> float:
    hle = _output_value(outputs, "hle")
    if hle <= 0:
        return 0.0
    return _output_value(outputs, "qlc") / hle


def _add_flag(
    flags: list[str],
    reasons: list[str],
    recommended_review: list[str],
    flag: str,
    reason: str,
    review: str,
) -> None:
    if flag not in flags:
        flags.append(flag)
        reasons.append(reason)
        recommended_review.append(review)


def evaluate_grouping_risk(example: dict[str, Any], outputs: Any) -> GroupingRiskResult:
    """Flag examples requiring grouped-entity or attribution review."""

    metadata = _metadata(example)
    red_flags = _red_team_flags(example)
    related_entities = metadata.get("related_entities", [])
    if not isinstance(related_entities, list):
        related_entities = []

    flags: list[str] = []
    reasons: list[str] = []
    recommended_review: list[str] = [
        "Prototype grouping review only; this is not legal grouping analysis or tax-law validation."
    ]

    if metadata.get("entity_splitting_risk") or "entity_splitting_safe_harbour" in red_flags:
        _add_flag(
            flags,
            reasons,
            recommended_review,
            ENTITY_SPLITTING_SAFE_HARBOUR,
            "Metadata or red-team notes indicate possible entity splitting to access safe harbours or thresholds.",
            "Review grouped turnover, output, employment, IP, platform, and contractor entities together.",
        )

    if related_entities:
        _add_flag(
            flags,
            reasons,
            recommended_review,
            RELATED_OPERATING_ENTITIES,
            "Example metadata lists related operating entities relevant to the output or automation chain.",
            "Review whether related entities should be aggregated for schedule thresholds and output attribution.",
        )

    separated_roles = {
        "ip_owner_entity",
        "platform_owner_entity",
        "employer_entity",
        "contractor_entity",
    }
    if any(metadata.get(key) for key in separated_roles):
        _add_flag(
            flags,
            reasons,
            recommended_review,
            SEPARATED_IP_PLATFORM_EMPLOYER,
            "Metadata indicates separation of IP, platform, employer, or contractor entities.",
            "Review whether the split suppresses QLC, hides automation, or shifts AAVA outside the measured firm.",
        )

    aii = _output_value(outputs, "aii")
    output_value = float(example.get("output", {}).get("value", 0.0))
    if aii >= 0.65 and _qlc_hle_ratio(outputs) <= 0.20 and output_value >= 1_000_000:
        _add_flag(
            flags,
            reasons,
            recommended_review,
            THIN_AUSTRALIAN_EMPLOYING_ENTITY,
            "Thin Australian QLC is paired with high automated Australian-facing output.",
            "Review whether automated productive capacity sits in another related entity or offshore service provider.",
        )

    if len(flags) >= 3:
        risk_level = "high"
    elif flags:
        risk_level = "medium"
    else:
        risk_level = "low"
        reasons.append("No grouped-entity review flags were triggered.")

    return GroupingRiskResult(
        risk_level=risk_level,
        flags=flags,
        reasons=reasons,
        recommended_review=recommended_review,
        placeholder_basis=[
            "Grouping checks are prototype review flags only.",
            "No full legal grouping, transfer-pricing, or attribution rule is implemented.",
        ],
    )
