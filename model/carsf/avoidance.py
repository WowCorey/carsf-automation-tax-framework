"""Prototype anti-avoidance risk checks for CARSF examples.

These checks are heuristic review flags only. They are not legal findings,
tax findings, Treasury validation, ATO validation, or calibrated audit rules.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


TOKEN_HUMAN_OVERSIGHT = "TOKEN_HUMAN_OVERSIGHT"
FAKE_QLC_INFLATION = "FAKE_QLC_INFLATION"
OFFSHORE_AUTOMATION_SERVICE = "OFFSHORE_AUTOMATION_SERVICE"
RELATED_PARTY_AI_SERVICE_FEES = "RELATED_PARTY_AI_SERVICE_FEES"
ENTITY_SPLITTING = "ENTITY_SPLITTING"
SECTOR_CLASSIFICATION_ARBITRAGE = "SECTOR_CLASSIFICATION_ARBITRAGE"
CLOUD_COST_RELABELING = "CLOUD_COST_RELABELING"
ROBOTICS_LEASING_AVOIDANCE = "ROBOTICS_LEASING_AVOIDANCE"
ARTIFICIAL_LOW_PROFIT_OR_AAVA = "ARTIFICIAL_LOW_PROFIT_OR_AAVA"


@dataclass(frozen=True)
class AvoidanceResult:
    """Prototype anti-avoidance risk assessment."""

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


def _workers(example: dict[str, Any]) -> list[dict[str, Any]]:
    workers = example.get("workers", [])
    return workers if isinstance(workers, list) else []


def _automation(example: dict[str, Any]) -> dict[str, float]:
    components = example.get("automation_components", {})
    if not isinstance(components, dict):
        return {}
    return {key: float(value) for key, value in components.items()}


def _aava_inputs(example: dict[str, Any]) -> dict[str, float]:
    inputs = example.get("aava_inputs", {})
    if not isinstance(inputs, dict):
        return {}
    return {key: float(value) for key, value in inputs.items()}


def _qlc_hle_ratio(outputs: Any) -> float:
    hle = _output_value(outputs, "hle")
    if hle <= 0:
        return 0.0
    return _output_value(outputs, "qlc") / hle


def _cost_ratio(example: dict[str, Any]) -> float:
    inputs = _aava_inputs(example)
    revenue = inputs.get("australian_attributable_revenue", 0.0)
    if revenue <= 0:
        return 0.0
    return inputs.get("verified_non_automation_input_costs", 0.0) / revenue


def _aava_ratio(example: dict[str, Any], outputs: Any) -> float:
    revenue = _aava_inputs(example).get("australian_attributable_revenue", 0.0)
    if revenue <= 0:
        return 0.0
    return _output_value(outputs, "aava") / revenue


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


def _workers_approaching_cap(example: dict[str, Any], schedule: dict[str, Any]) -> int:
    weights = schedule.get("qlc", {}).get("weights", {})
    cap = float(schedule.get("qlc", {}).get("qlc_max_multiplier", 1.25))
    alpha = float(weights.get("alpha_wage_quality", 0.0))
    beta = float(weights.get("beta_job_security", 0.0))
    gamma = float(weights.get("gamma_skill_development", 0.0))
    delta = float(weights.get("delta_australian_nexus", 0.0))
    count = 0
    for worker in _workers(example):
        multiplier = 1.0 + (
            alpha * float(worker.get("wage_quality", 0.0))
            + beta * float(worker.get("job_security", 0.0))
            + gamma * float(worker.get("skill_development", 0.0))
            + delta * float(worker.get("australian_nexus", 0.0))
        )
        if multiplier >= cap * 0.95:
            count += 1
    return count


def evaluate_avoidance_risk(
    example: dict[str, Any],
    schedule: dict[str, Any],
    outputs: Any,
) -> AvoidanceResult:
    """Evaluate prototype gaming and avoidance risk flags."""

    metadata = _metadata(example)
    red_flags = _red_team_flags(example)
    automation = _automation(example)
    aii = _output_value(outputs, "aii")
    qlc_ratio = _qlc_hle_ratio(outputs)
    worker_count = len(_workers(example))
    cost_ratio = _cost_ratio(example)
    aava_ratio = _aava_ratio(example, outputs)
    revenue = _aava_inputs(example).get("australian_attributable_revenue", 0.0)
    capital_base = float(example.get("capital_base", 0.0))
    robotics_ratio = automation.get("robotics_capital_ratio", 0.0)

    flags: list[str] = []
    reasons: list[str] = []
    recommended_review: list[str] = [
        "Prototype review flags only; no legal, tax, Treasury, or ATO validation is provided."
    ]

    if (
        metadata.get("token_human_oversight_risk")
        or "token_human_oversight_jobs" in red_flags
        or (aii >= 0.65 and qlc_ratio <= 0.30 and worker_count <= 3)
    ):
        _add_flag(
            flags,
            reasons,
            recommended_review,
            TOKEN_HUMAN_OVERSIGHT,
            "High automation with low QLC/HLE and a small workforce may indicate nominal human oversight.",
            "Review whether human roles are substantive, verified, and appropriately scored for QLC.",
        )

    if (
        metadata.get("fake_qlc_inflation_risk")
        or "fake_qlc_inflation" in red_flags
        or (_workers_approaching_cap(example, schedule) >= 3 and aii >= 0.50 and qlc_ratio <= 0.45)
    ):
        _add_flag(
            flags,
            reasons,
            recommended_review,
            FAKE_QLC_INFLATION,
            "QLC scoring may be inflated or concentrated in too few roles relative to automated output.",
            "Review payroll, hours, wage quality, security, training, and Australian nexus evidence.",
        )

    if metadata.get("offshore_automation_service") or "offshore_automation_service" in red_flags:
        _add_flag(
            flags,
            reasons,
            recommended_review,
            OFFSHORE_AUTOMATION_SERVICE,
            "Metadata or red-team notes identify offshore automation services serving Australian output.",
            "Review destination/activity attribution and offshore automation-as-a-service contracts.",
        )

    if (
        metadata.get("related_party_ai_service_fees")
        or "related_party_ai_service_fees" in red_flags
        or (aii >= 0.60 and cost_ratio >= 0.45 and metadata.get("related_party_fee_review"))
    ):
        _add_flag(
            flags,
            reasons,
            recommended_review,
            RELATED_PARTY_AI_SERVICE_FEES,
            "Related-party AI service fees may reduce AAVA without arm's-length support.",
            "Review transfer-pricing support, service descriptions, and AAVA deductibility treatment.",
        )

    if metadata.get("entity_splitting_risk") or "entity_splitting_safe_harbour" in red_flags:
        _add_flag(
            flags,
            reasons,
            recommended_review,
            ENTITY_SPLITTING,
            "Metadata or red-team notes indicate potential grouped-entity threshold avoidance.",
            "Review related entities, output ownership, employment entity, IP owner, and platform owner.",
        )

    if metadata.get("sector_classification_risk") or "sector_classification_arbitrage" in red_flags:
        _add_flag(
            flags,
            reasons,
            recommended_review,
            SECTOR_CLASSIFICATION_ARBITRAGE,
            "Schedule choice may be material to liability or may not match Australian-facing activity.",
            "Review dominant activity, schedule apportionment, and Schedules Authority classification.",
        )

    if metadata.get("cloud_cost_relabeling_risk") or "cloud_cost_relabeling" in red_flags:
        _add_flag(
            flags,
            reasons,
            recommended_review,
            CLOUD_COST_RELABELING,
            "AI cloud or inference costs may be relabelled as ordinary non-automation input costs.",
            "Review cloud invoices, inference allocation, and AAVA deductibility taxonomy treatment.",
        )

    if (
        metadata.get("robotics_leasing_risk")
        or "robotics_leasing_avoidance" in red_flags
        or (robotics_ratio >= 0.75 and revenue > 0 and capital_base / revenue <= 0.20)
    ):
        _add_flag(
            flags,
            reasons,
            recommended_review,
            ROBOTICS_LEASING_AVOIDANCE,
            "Robotics capital intensity appears high relative to the declared capital base.",
            "Review leases, outsourced robotics contracts, asset ownership, and capital-base treatment.",
        )

    if (
        metadata.get("artificial_low_profit_or_aava_risk")
        or (aii >= 0.65 and aava_ratio <= 0.15 and cost_ratio >= 0.75)
        or (aava_ratio <= 0.10 and (metadata.get("related_party_ai_service_fees") or metadata.get("offshore_automation_service")))
    ):
        _add_flag(
            flags,
            reasons,
            recommended_review,
            ARTIFICIAL_LOW_PROFIT_OR_AAVA,
            "AAVA appears low relative to revenue/output/automation intensity.",
            "Review whether ordinary-cost deductions, related-party charges, or offshore services suppress AAVA.",
        )

    high_severity = {
        OFFSHORE_AUTOMATION_SERVICE,
        RELATED_PARTY_AI_SERVICE_FEES,
        ENTITY_SPLITTING,
        SECTOR_CLASSIFICATION_ARBITRAGE,
        ARTIFICIAL_LOW_PROFIT_OR_AAVA,
    }
    if len(set(flags) & high_severity) >= 2 or len(flags) >= 4:
        risk_level = "high"
    elif flags:
        risk_level = "medium"
    else:
        risk_level = "low"
        reasons.append("No executable prototype avoidance flags were triggered.")

    return AvoidanceResult(
        risk_level=risk_level,
        flags=flags,
        reasons=reasons,
        recommended_review=recommended_review,
        placeholder_basis=[
            "Avoidance checks are prototype heuristics only.",
            "Thresholds are illustrative placeholders and not calibrated enforcement rules.",
            "No result constitutes legal, tax, Treasury, or ATO validation.",
        ],
    )
