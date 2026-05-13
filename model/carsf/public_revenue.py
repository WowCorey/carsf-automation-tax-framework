"""Placeholder public-revenue impact calculations for CARSF trajectories."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any


PUBLIC_REVENUE_NON_CLAIMS = [
    "Public-revenue outputs are illustrative placeholders only and are not government revenue estimates.",
    "No Treasury, ATO, ABS, DSS, PBO, legal, tax, or economic validation is implied.",
    "Public-revenue outputs do not modify firm-level CARSF liability.",
]


@dataclass(frozen=True)
class PublicRevenueInput:
    payg_loss: float
    company_tax_change: float
    gst_consumption_change: float
    super_contribution_loss: float
    help_repayment_loss: float
    state_payroll_tax_loss: float
    automation_revenue_captured: float
    other_revenue_change: float
    placeholder_basis: list[str] = field(default_factory=list)
    allow_revenue_gains: bool = False

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicRevenueResult:
    commonwealth_revenue_loss_before_carsf: float
    retirement_contribution_pressure: float
    automation_revenue_captured: float
    net_commonwealth_gap_after_carsf: float
    state_revenue_pressure: float
    total_public_sector_gap: float
    broader_labour_linked_pressure: float
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(PUBLIC_REVENUE_NON_CLAIMS))

    @property
    def labour_linked_revenue_loss(self) -> float:
        """Backward-compatible alias for Commonwealth revenue pressure only."""

        return self.commonwealth_revenue_loss_before_carsf

    @property
    def total_revenue_loss_before_carsf(self) -> float:
        """Backward-compatible alias for Commonwealth revenue loss before CARSF."""

        return self.commonwealth_revenue_loss_before_carsf

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


def _revenue_loss_or_gain(value: Any, field_name: str, allow_gain: bool) -> float:
    numeric = _finite_number(value, field_name)
    if numeric < 0 and not allow_gain:
        raise ValueError(f"{field_name} cannot be negative unless allow_revenue_gains is true")
    return numeric


def _input_from_mapping(source: dict[str, Any]) -> PublicRevenueInput:
    return PublicRevenueInput(
        payg_loss=source.get("payg_loss", 0.0),
        company_tax_change=source.get("company_tax_change", 0.0),
        gst_consumption_change=source.get("gst_consumption_change", 0.0),
        super_contribution_loss=source.get("super_contribution_loss", 0.0),
        help_repayment_loss=source.get("help_repayment_loss", 0.0),
        state_payroll_tax_loss=source.get("state_payroll_tax_loss", 0.0),
        automation_revenue_captured=source.get("automation_revenue_captured", 0.0),
        other_revenue_change=source.get("other_revenue_change", 0.0),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
        allow_revenue_gains=bool(source.get("allow_revenue_gains", False)),
    )


def evaluate_public_revenue(inputs: PublicRevenueInput | dict[str, Any]) -> PublicRevenueResult:
    """Calculate placeholder revenue loss and residual public-sector pressure."""

    if isinstance(inputs, dict):
        inputs = _input_from_mapping(inputs)

    allow_gain = inputs.allow_revenue_gains
    payg_loss = _non_negative_number(inputs.payg_loss, "payg_loss")
    company_tax_change = _revenue_loss_or_gain(inputs.company_tax_change, "company_tax_change", allow_gain)
    gst_consumption_change = _revenue_loss_or_gain(inputs.gst_consumption_change, "gst_consumption_change", allow_gain)
    super_loss = _non_negative_number(inputs.super_contribution_loss, "super_contribution_loss")
    help_loss = _non_negative_number(inputs.help_repayment_loss, "help_repayment_loss")
    state_loss = _non_negative_number(inputs.state_payroll_tax_loss, "state_payroll_tax_loss")
    automation_captured = _non_negative_number(inputs.automation_revenue_captured, "automation_revenue_captured")
    other_change = _revenue_loss_or_gain(inputs.other_revenue_change, "other_revenue_change", allow_gain)

    commonwealth_before_carsf = payg_loss + help_loss + company_tax_change + gst_consumption_change + other_change
    commonwealth_gap = commonwealth_before_carsf - automation_captured
    total_public_gap = commonwealth_gap + state_loss
    broader_pressure = total_public_gap + super_loss

    return PublicRevenueResult(
        commonwealth_revenue_loss_before_carsf=commonwealth_before_carsf,
        retirement_contribution_pressure=super_loss,
        automation_revenue_captured=automation_captured,
        net_commonwealth_gap_after_carsf=commonwealth_gap,
        state_revenue_pressure=state_loss,
        total_public_sector_gap=total_public_gap,
        broader_labour_linked_pressure=broader_pressure,
        warnings=[
            "Revenue changes are placeholder inputs and are not government revenue estimates.",
            "Superannuation contribution loss is tracked as retirement-system contribution pressure, not ordinary Commonwealth revenue loss.",
        ],
    )
