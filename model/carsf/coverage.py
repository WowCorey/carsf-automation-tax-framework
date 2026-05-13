"""National-level coverage metrics."""

from __future__ import annotations

from math import isfinite

from .types import CoverageResult


def cars_i(
    national_automation_fiscal_damage: float,
    automation_revenue_captured: float,
    epsilon: float = 1e-9,
) -> float:
    """CARS-I = NationalAutomationFiscalDamage / (AutomationRevenueCaptured + epsilon)."""

    if national_automation_fiscal_damage < 0:
        raise ValueError("national_automation_fiscal_damage cannot be negative")
    if automation_revenue_captured < 0:
        raise ValueError("automation_revenue_captured cannot be negative")
    if epsilon <= 0:
        raise ValueError("epsilon must be positive")
    result = national_automation_fiscal_damage / (automation_revenue_captured + epsilon)
    if not isfinite(result):
        return float("inf")
    return result


def coverage_ratio(
    automation_revenue_captured: float,
    national_automation_fiscal_damage: float,
) -> float:
    """CoverageRatio = AutomationRevenueCaptured / NationalAutomationFiscalDamage.

    Zero-damage periods are treated as fully covered because there is no measured
    damage to cover. This is a modelling convention, not a policy conclusion.
    """

    if national_automation_fiscal_damage < 0:
        raise ValueError("national_automation_fiscal_damage cannot be negative")
    if automation_revenue_captured < 0:
        raise ValueError("automation_revenue_captured cannot be negative")
    if national_automation_fiscal_damage == 0:
        return 1.0
    return automation_revenue_captured / national_automation_fiscal_damage


def coverage_measures(
    national_automation_fiscal_damage: float,
    automation_revenue_captured: float,
    epsilon: float = 1e-9,
) -> CoverageResult:
    """Return CARS-I and CoverageRatio with safe zero handling."""

    notes: list[str] = []
    if national_automation_fiscal_damage == 0:
        notes.append("CoverageRatio set to 1.0 because measured fiscal damage is zero.")
    if automation_revenue_captured == 0:
        notes.append("CARS-I used epsilon because captured automation revenue is zero.")
    return CoverageResult(
        cars_i=cars_i(national_automation_fiscal_damage, automation_revenue_captured, epsilon),
        coverage_ratio=coverage_ratio(automation_revenue_captured, national_automation_fiscal_damage),
        notes=tuple(notes),
    )
