"""Prototype multi-schedule apportionment previews.

This module blends placeholder schedule parameters for modelling review only.
It is not legal attribution, tax-law apportionment, Treasury guidance, ATO
guidance, or a calibrated policy setting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from typing import Any


SHARE_TOLERANCE = 1e-6
VAGUE_BASIS_TERMS = {
    "",
    "estimate",
    "rough estimate",
    "management estimate",
    "management judgement",
    "unsupported",
    "unknown",
    "tbd",
    "to be determined",
}


@dataclass(frozen=True)
class ApportionmentActivity:
    """One activity slice used for prototype schedule apportionment."""

    schedule_id: str
    share: float
    basis: str
    placeholder_basis: str | list[str]
    activity_id: str = ""
    description: str = ""


@dataclass(frozen=True)
class ApportionmentResult:
    """Prototype schedule-blending result."""

    valid: bool
    activities: list[ApportionmentActivity] = field(default_factory=list)
    weighted_parameters: dict[str, Any] = field(default_factory=dict)
    warnings: list[str] = field(default_factory=list)
    review_required: bool = False
    placeholder_basis: list[str] = field(default_factory=list)


def _activity_rows(example: dict[str, Any]) -> list[dict[str, Any]]:
    apportionment = example.get("apportionment", {})
    if isinstance(apportionment, dict) and isinstance(apportionment.get("activities"), list):
        return apportionment["activities"]
    activities = example.get("activities", [])
    return activities if isinstance(activities, list) else []


def _normalisation_permitted(example: dict[str, Any]) -> bool:
    apportionment = example.get("apportionment", {})
    if isinstance(apportionment, dict):
        return bool(apportionment.get("normalisation_permitted", False))
    metadata = example.get("metadata", {})
    return bool(isinstance(metadata, dict) and metadata.get("normalisation_permitted"))


def _placeholder_basis_for(example: dict[str, Any]) -> list[str]:
    return [
        "Apportionment is a prototype schedule-blending model only.",
        "It is not legal attribution, tax-law apportionment, Treasury guidance, or ATO guidance.",
        "All shares and weighted parameters are illustrative placeholders unless separately calibrated.",
        str(example.get("placeholder_notice", "No example placeholder notice supplied.")),
    ]


def _fail(
    activities: list[ApportionmentActivity],
    warning: str,
    placeholder_basis: list[str],
) -> ApportionmentResult:
    return ApportionmentResult(
        valid=False,
        activities=activities,
        weighted_parameters={},
        warnings=[warning],
        review_required=True,
        placeholder_basis=placeholder_basis,
    )


def _as_activity(row: dict[str, Any]) -> ApportionmentActivity:
    return ApportionmentActivity(
        schedule_id=str(row.get("schedule_id", "")),
        share=float(row.get("share", 0.0)),
        basis=str(row.get("basis", "")),
        placeholder_basis=row.get("placeholder_basis", ""),
        activity_id=str(row.get("activity_id", "")),
        description=str(row.get("description", "")),
    )


def _basis_needs_review(activity: ApportionmentActivity) -> bool:
    basis = activity.basis.strip().lower()
    if basis in VAGUE_BASIS_TERMS:
        return True
    placeholder_text = activity.placeholder_basis
    if isinstance(placeholder_text, list):
        joined = " ".join(str(item) for item in placeholder_text)
    else:
        joined = str(placeholder_text)
    return "placeholder" not in joined.lower() and "prototype" not in joined.lower()


def _weighted_sum(activities: list[ApportionmentActivity], schedules_by_id: dict[str, dict[str, Any]], path: str) -> float:
    total = 0.0
    for activity in activities:
        current: Any = schedules_by_id[activity.schedule_id]
        for part in path.split("."):
            current = current[part]
        total += activity.share * float(current)
    return total


def _weighted_aii_weights(
    activities: list[ApportionmentActivity],
    schedules_by_id: dict[str, dict[str, Any]],
) -> dict[str, float]:
    keys = [
        "compute_ratio",
        "auto_decision_ratio",
        "robotics_capital_ratio",
        "auto_process_share",
    ]
    return {
        key: sum(activity.share * float(schedules_by_id[activity.schedule_id]["aii"]["weights"][key]) for activity in activities)
        for key in keys
    }


def evaluate_apportionment(
    example: dict[str, Any],
    schedules_by_id: dict[str, dict[str, Any]],
) -> ApportionmentResult:
    """Evaluate prototype schedule apportionment for a mixed-activity example."""

    placeholder_basis = _placeholder_basis_for(example)
    raw_activities = _activity_rows(example)
    if not raw_activities:
        return _fail([], "No apportionment activities were supplied.", placeholder_basis)

    activities: list[ApportionmentActivity] = []
    warnings = [
        "Prototype apportionment preview only; no legal, tax, Treasury, or ATO validation is provided."
    ]

    for index, row in enumerate(raw_activities):
        if not isinstance(row, dict):
            return _fail(activities, f"Apportionment activity {index} must be a mapping.", placeholder_basis)
        try:
            activity = _as_activity(row)
        except (TypeError, ValueError) as exc:
            return _fail(activities, f"Apportionment activity {index} share must be numeric: {exc}", placeholder_basis)
        activities.append(activity)
        if not isfinite(activity.share):
            return _fail(activities, f"Apportionment share for {activity.activity_id or index} must be finite.", placeholder_basis)
        if activity.share < 0:
            return _fail(activities, f"Apportionment share for {activity.activity_id or index} cannot be negative.", placeholder_basis)
        if activity.schedule_id not in schedules_by_id:
            return _fail(activities, f"Unknown schedule_id for apportionment: {activity.schedule_id}", placeholder_basis)

    share_sum = sum(activity.share for activity in activities)
    if abs(share_sum - 1.0) > SHARE_TOLERANCE:
        if not _normalisation_permitted(example):
            return _fail(
                activities,
                f"Apportionment shares must sum to 1.0; received {share_sum:.8f}.",
                placeholder_basis,
            )
        if share_sum <= 0:
            return _fail(activities, "Apportionment shares cannot be normalised when their sum is zero.", placeholder_basis)
        activities = [
            ApportionmentActivity(
                schedule_id=activity.schedule_id,
                share=activity.share / share_sum,
                basis=activity.basis,
                placeholder_basis=activity.placeholder_basis,
                activity_id=activity.activity_id,
                description=activity.description,
            )
            for activity in activities
        ]
        warnings.append(f"Shares were normalised from total {share_sum:.8f}; review is required.")

    review_required = False
    for activity in activities:
        if _basis_needs_review(activity):
            review_required = True
            warnings.append(
                f"Activity {activity.activity_id or activity.schedule_id} has unsupported or vague apportionment basis."
            )

    weighted_parameters = {
        "opfte_libc": _weighted_sum(activities, schedules_by_id, "opfte_libc_placeholder.value"),
        "frv_floor": _weighted_sum(activities, schedules_by_id, "frv.floor_placeholder"),
        "frv_standard": _weighted_sum(activities, schedules_by_id, "frv.standard_placeholder"),
        "frv_full": _weighted_sum(activities, schedules_by_id, "frv.full_placeholder"),
        "lambda_sector": _weighted_sum(activities, schedules_by_id, "caps.lambda_sector"),
        "LAMBDA_sector": _weighted_sum(activities, schedules_by_id, "caps.LAMBDA_sector"),
        "theta": _weighted_sum(activities, schedules_by_id, "caps.theta"),
        "qlc_max_multiplier": _weighted_sum(activities, schedules_by_id, "qlc.qlc_max_multiplier"),
        "aii_weights": _weighted_aii_weights(activities, schedules_by_id),
    }

    return ApportionmentResult(
        valid=True,
        activities=activities,
        weighted_parameters=weighted_parameters,
        warnings=warnings,
        review_required=review_required,
        placeholder_basis=placeholder_basis,
    )
