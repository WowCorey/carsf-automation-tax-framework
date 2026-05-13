"""Placeholder fiscal incidence of support payments."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any

from .transfer_baseline import TRANSFER_BASELINE_NON_CLAIMS


@dataclass(frozen=True)
class SupportIncidenceAssumption:
    household_spend_share: float
    gst_recovery_rate_placeholder: float
    hardship_offset_rate_placeholder: float
    savings_or_debt_repayment_share: float
    illustrative_placeholder_only: bool = True
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SupportIncidenceResult:
    gross_support_cost: float
    household_spending_flow: float
    placeholder_gst_recovery: float
    hardship_offset_preview: float
    net_fiscal_cost_after_placeholder_offsets: float
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(TRANSFER_BASELINE_NON_CLAIMS))

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


def _bounded_rate(value: Any, field_name: str) -> float:
    numeric = _finite_number(value, field_name)
    if not 0 <= numeric <= 1:
        raise ValueError(f"{field_name} must be in [0, 1]")
    return numeric


def _assumption_from_mapping(source: dict[str, Any]) -> SupportIncidenceAssumption:
    return SupportIncidenceAssumption(
        household_spend_share=source["household_spend_share"],
        gst_recovery_rate_placeholder=source.get("gst_recovery_rate_placeholder", 0.0),
        hardship_offset_rate_placeholder=source.get("hardship_offset_rate_placeholder", 0.0),
        savings_or_debt_repayment_share=source.get("savings_or_debt_repayment_share", 0.0),
        illustrative_placeholder_only=bool(source.get("illustrative_placeholder_only", True)),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def support_incidence_assumption_from_mapping(
    source: SupportIncidenceAssumption | dict[str, Any],
) -> SupportIncidenceAssumption:
    if isinstance(source, SupportIncidenceAssumption):
        return source
    return _assumption_from_mapping(source)


def evaluate_support_incidence(
    gross_support_cost: float,
    assumption: SupportIncidenceAssumption | dict[str, Any],
) -> SupportIncidenceResult:
    """Estimate placeholder household flow and fiscal offsets from support payments."""

    if isinstance(assumption, dict):
        assumption = _assumption_from_mapping(assumption)
    if assumption.illustrative_placeholder_only is not True:
        raise ValueError("support incidence assumption must be illustrative_placeholder_only")
    gross = _non_negative_number(gross_support_cost, "gross_support_cost")
    spend_share = _bounded_rate(assumption.household_spend_share, "household_spend_share")
    gst_rate = _bounded_rate(assumption.gst_recovery_rate_placeholder, "gst_recovery_rate_placeholder")
    hardship_rate = _bounded_rate(assumption.hardship_offset_rate_placeholder, "hardship_offset_rate_placeholder")
    savings_share = _bounded_rate(assumption.savings_or_debt_repayment_share, "savings_or_debt_repayment_share")
    if spend_share + savings_share > 1:
        raise ValueError("household_spend_share plus savings_or_debt_repayment_share cannot exceed 1")

    household_flow = gross * spend_share
    gst_recovery = household_flow * gst_rate
    hardship_offset = gross * hardship_rate
    net_cost = max(0.0, gross - gst_recovery - hardship_offset)
    return SupportIncidenceResult(
        gross_support_cost=gross,
        household_spending_flow=household_flow,
        placeholder_gst_recovery=gst_recovery,
        hardship_offset_preview=hardship_offset,
        net_fiscal_cost_after_placeholder_offsets=net_cost,
        warnings=[
            "Support incidence offsets are placeholder previews, not validated savings.",
            "This is not a macroeconomic multiplier, GST estimate, welfare costing, or budget offset.",
        ],
    )
