"""Prototype safe-harbour classification for CARSF examples.

This module is a review-signalling layer only. It does not alter AEL, ARL,
credits, caps, or final liability.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


SMALL_BUSINESS_PLACEHOLDER = "SMALL_BUSINESS_PLACEHOLDER"
STARTUP_PLACEHOLDER = "STARTUP_PLACEHOLDER"
WORKER_ASSIST_OR_ADMIN_AI = "WORKER_ASSIST_OR_ADMIN_AI"
LOW_NLTG_EXCLUSION = "LOW_NLTG_EXCLUSION"
ESSENTIAL_SERVICES_REVIEW = "ESSENTIAL_SERVICES_REVIEW"
NO_SAFE_HARBOUR_REVIEW = "NO_SAFE_HARBOUR_REVIEW"


@dataclass(frozen=True)
class SafeHarbourResult:
    """Prototype safe-harbour or review-path classification."""

    eligible: bool
    category: str
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    review_required: bool = False
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


def _safe_harbour_config(schedule: dict[str, Any]) -> dict[str, Any]:
    config = schedule.get("safe_harbours", {})
    return config if isinstance(config, dict) else {}


def _placeholder_number(config: dict[str, Any], field_name: str, default: float) -> float:
    value = config.get(field_name, default)
    return float(value)


def _revenue(example: dict[str, Any]) -> float:
    return float(example["aava_inputs"]["australian_attributable_revenue"])


def _human_labour_ratio(outputs: Any) -> float:
    hle = _output_value(outputs, "hle")
    if hle <= 0:
        return 0.0
    return _output_value(outputs, "qlc") / hle


def _has_high_risk_metadata(example: dict[str, Any]) -> bool:
    metadata = _metadata(example)
    red_flags = _red_team_flags(example)
    high_risk_keys = {
        "offshore_automation_service",
        "related_party_ai_service_fees",
        "entity_splitting_risk",
        "sector_classification_risk",
        "token_human_oversight_risk",
        "fake_qlc_inflation_risk",
        "cloud_cost_relabeling_risk",
        "robotics_leasing_risk",
    }
    high_risk_red_flags = {
        "offshore_automation_service",
        "related_party_ai_service_fees",
        "entity_splitting_safe_harbour",
        "sector_classification_arbitrage",
        "token_human_oversight_jobs",
        "fake_qlc_inflation",
        "cloud_cost_relabeling",
        "robotics_leasing_avoidance",
    }
    return any(bool(metadata.get(key)) for key in high_risk_keys) or bool(red_flags & high_risk_red_flags)


def evaluate_safe_harbour(
    example: dict[str, Any],
    schedule: dict[str, Any],
    outputs: Any,
) -> SafeHarbourResult:
    """Classify prototype safe-harbour or review-path status.

    The result is deliberately non-operative: it does not reduce, cap, or erase
    any liability output from the formula chain.
    """

    metadata = _metadata(example)
    config = _safe_harbour_config(schedule)
    low_nltg_threshold = _placeholder_number(config, "low_nltg_threshold_placeholder", 0.25)
    human_ratio_threshold = _placeholder_number(
        config,
        "substantial_human_labour_qlc_hle_ratio_placeholder",
        0.35,
    )
    revenue_threshold = _placeholder_number(config, "small_business_revenue_threshold_placeholder", 10_000_000.0)
    qlc_low_ratio_threshold = _placeholder_number(config, "low_qlc_review_ratio_placeholder", 0.30)

    nltg = _output_value(outputs, "nltg")
    aii = _output_value(outputs, "aii")
    human_ratio = _human_labour_ratio(outputs)
    revenue = _revenue(example)
    low_nltg = nltg <= low_nltg_threshold
    human_labour_substantial = human_ratio >= human_ratio_threshold
    high_risk = _has_high_risk_metadata(example)

    placeholder_basis = [
        "Prototype safe-harbour checks use illustrative placeholder thresholds only.",
        f"low_nltg_threshold_placeholder={low_nltg_threshold}",
        f"substantial_human_labour_qlc_hle_ratio_placeholder={human_ratio_threshold}",
        f"small_business_revenue_threshold_placeholder={revenue_threshold}",
        "Safe-harbour classification does not alter liability in this build.",
    ]
    warnings = [
        "Prototype classification only; not legal advice, tax advice, Treasury guidance, or ATO guidance.",
        "This result does not constitute legal validation of any actual safe harbour.",
    ]

    if metadata.get("essential_service_review"):
        return SafeHarbourResult(
            eligible=False,
            category=ESSENTIAL_SERVICES_REVIEW,
            reasons=["Example metadata marks the activity for essential-services policy review."],
            warnings=warnings,
            review_required=True,
            placeholder_basis=placeholder_basis,
        )

    if high_risk:
        return SafeHarbourResult(
            eligible=False,
            category=NO_SAFE_HARBOUR_REVIEW,
            reasons=["High-risk avoidance metadata or red-team flags require review before any safe harbour."],
            warnings=warnings,
            review_required=True,
            placeholder_basis=placeholder_basis,
        )

    if metadata.get("startup_placeholder"):
        review_required = aii >= 0.65 and human_ratio <= qlc_low_ratio_threshold
        reasons = ["Example metadata explicitly marks a startup placeholder pathway."]
        if review_required:
            reasons.append("High automation intensity and low QLC/HLE ratio require review before startup treatment.")
        return SafeHarbourResult(
            eligible=not review_required,
            category=STARTUP_PLACEHOLDER,
            reasons=reasons,
            warnings=warnings,
            review_required=review_required,
            placeholder_basis=placeholder_basis,
        )

    if metadata.get("worker_assist_admin_ai") and human_labour_substantial and low_nltg:
        return SafeHarbourResult(
            eligible=True,
            category=WORKER_ASSIST_OR_ADMIN_AI,
            reasons=[
                "Metadata identifies worker-assist/admin AI rather than labour-substituting automation.",
                "QLC remains substantial relative to HLE under placeholder rules.",
                "NLTG is zero or near-zero under placeholder rules.",
            ],
            warnings=warnings,
            review_required=False,
            placeholder_basis=placeholder_basis,
        )

    if (
        metadata.get("small_business_placeholder")
        and revenue <= revenue_threshold
        and low_nltg
        and human_labour_substantial
    ):
        return SafeHarbourResult(
            eligible=True,
            category=SMALL_BUSINESS_PLACEHOLDER,
            reasons=[
                "Revenue is below the schedule placeholder small-business threshold.",
                "No high-risk avoidance metadata is present.",
                "NLTG is zero or near-zero and human labour remains substantial.",
            ],
            warnings=warnings,
            review_required=False,
            placeholder_basis=placeholder_basis,
        )

    if low_nltg and human_labour_substantial:
        return SafeHarbourResult(
            eligible=True,
            category=LOW_NLTG_EXCLUSION,
            reasons=[
                "NLTG is zero or near-zero under placeholder rules.",
                "Human labour remains substantial relative to measured output.",
            ],
            warnings=warnings,
            review_required=False,
            placeholder_basis=placeholder_basis,
        )

    return SafeHarbourResult(
        eligible=False,
        category=NO_SAFE_HARBOUR_REVIEW,
        reasons=["No prototype safe-harbour category was satisfied under the placeholder checks."],
        warnings=warnings,
        review_required=True,
        placeholder_basis=placeholder_basis,
    )
