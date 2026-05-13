"""Prototype under-capture / over-capture burden-balance guardrails."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any


BURDEN_BALANCE_NON_CLAIMS = [
    "Burden-balance outputs are prototype-only and do not alter liability.",
    "National automation fiscal damage and captured revenue are not calibrated.",
    "No economic, Treasury, ATO, legal, tax, investment, or market validation is implied.",
]


@dataclass(frozen=True)
class BurdenBalanceInput:
    automation_fiscal_damage: float | None
    automation_revenue_captured: float | None
    final_liability: float
    aava: float
    nltg: float
    safe_harbour_category: str | None = None
    avoidance_risk: str | None = None
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class BurdenBalanceResult:
    coverage_ratio: float | None
    capture_gap: float | None
    burden_balance_band: str
    review_required: bool
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(BURDEN_BALANCE_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _finite_number(value: Any, field_name: str) -> float:
    numeric = float(value)
    if not isfinite(numeric):
        raise ValueError(f"{field_name} must be finite")
    return numeric


def _non_negative_number(value: Any, field_name: str) -> float:
    numeric = _finite_number(value, field_name)
    if numeric < 0:
        raise ValueError(f"{field_name} cannot be negative")
    return numeric


def _input_from_mapping(source: dict[str, Any]) -> BurdenBalanceInput:
    return BurdenBalanceInput(
        automation_fiscal_damage=source.get("automation_fiscal_damage"),
        automation_revenue_captured=source.get("automation_revenue_captured"),
        final_liability=source.get("final_liability", source.get("liability", 0.0)),
        aava=source.get("aava", 0.0),
        nltg=source.get("nltg", 0.0),
        safe_harbour_category=source.get("safe_harbour_category"),
        avoidance_risk=source.get("avoidance_risk"),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def evaluate_burden_balance(inputs: BurdenBalanceInput | dict[str, Any]) -> BurdenBalanceResult:
    """Assess public-revenue under-capture or over-capture using placeholders."""

    if isinstance(inputs, dict):
        inputs = _input_from_mapping(inputs)

    final_liability = _non_negative_number(inputs.final_liability, "final_liability")
    aava = _finite_number(inputs.aava, "aava")
    nltg = _non_negative_number(inputs.nltg, "nltg")
    warnings = [
        "National damage/capture inputs are illustrative placeholders and not calibrated.",
        "Burden-balance output does not alter final liability.",
    ]
    reasons: list[str] = []

    if inputs.automation_fiscal_damage is None or inputs.automation_revenue_captured is None:
        return BurdenBalanceResult(
            coverage_ratio=None,
            capture_gap=None,
            burden_balance_band="not_assessable",
            review_required=True,
            reasons=["National automation fiscal damage or captured revenue input is missing."],
            warnings=warnings,
        )

    damage = _non_negative_number(inputs.automation_fiscal_damage, "automation_fiscal_damage")
    captured = _non_negative_number(inputs.automation_revenue_captured, "automation_revenue_captured")
    if damage == 0:
        if captured > 0:
            return BurdenBalanceResult(
                coverage_ratio=None,
                capture_gap=-captured,
                burden_balance_band="over_capture",
                review_required=True,
                reasons=["Captured revenue is positive while measured fiscal damage is zero."],
                warnings=warnings,
            )
        return BurdenBalanceResult(
            coverage_ratio=None,
            capture_gap=0.0,
            burden_balance_band="balanced_placeholder",
            review_required=False,
            reasons=["Zero measured damage and zero captured revenue under placeholder inputs."],
            warnings=warnings,
        )

    coverage_ratio = captured / damage
    capture_gap = damage - captured
    if coverage_ratio < 0.75:
        band = "under_capture"
        review = True
        reasons.append("Captured automation revenue is materially below placeholder fiscal damage.")
    elif coverage_ratio > 1.10:
        band = "over_capture"
        review = True
        reasons.append("Captured automation revenue exceeds placeholder fiscal damage beyond tolerance.")
    else:
        band = "balanced_placeholder"
        review = False
        reasons.append("Placeholder captured revenue is within tolerance of placeholder fiscal damage.")

    if inputs.avoidance_risk and str(inputs.avoidance_risk).lower() == "high" and band == "under_capture":
        reasons.append("High avoidance risk reinforces under-capture review.")
    if final_liability == 0 and aava > 0 and nltg > 0:
        warnings.append("Positive AAVA/NLTG with zero liability may indicate firm-level under-capture.")

    return BurdenBalanceResult(
        coverage_ratio=coverage_ratio,
        capture_gap=capture_gap,
        burden_balance_band=band,
        review_required=review,
        reasons=reasons,
        warnings=warnings,
    )
