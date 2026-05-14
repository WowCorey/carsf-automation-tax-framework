"""Prototype payment cliff detection for synthetic distributional scenarios."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any

from .households import DISTRIBUTIONAL_NON_CLAIMS


@dataclass(frozen=True)
class PaymentCliffInput:
    cliff_id: str
    household_id: str
    support_before_change: float
    support_after_change: float
    income_before_change: float
    income_after_change: float
    trigger_type: str
    trigger_description: str
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PaymentCliffResult:
    cliff_id: str
    household_id: str
    support_loss: float
    income_gain: float
    net_position_change: float
    cliff_detected: bool
    cliff_severity_band: str
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(DISTRIBUTIONAL_NON_CLAIMS))

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


def _input_from_mapping(source: dict[str, Any]) -> PaymentCliffInput:
    return PaymentCliffInput(
        cliff_id=str(source["cliff_id"]),
        household_id=str(source["household_id"]),
        support_before_change=source["support_before_change"],
        support_after_change=source["support_after_change"],
        income_before_change=source["income_before_change"],
        income_after_change=source["income_after_change"],
        trigger_type=str(source.get("trigger_type", "placeholder_trigger")),
        trigger_description=str(source.get("trigger_description", "")),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def payment_cliff_input_from_mapping(source: PaymentCliffInput | dict[str, Any]) -> PaymentCliffInput:
    if isinstance(source, PaymentCliffInput):
        return source
    return _input_from_mapping(source)


def _severity_band(net_position_change: float, support_loss: float) -> str:
    if net_position_change >= 0:
        return "none"
    loss_gap = abs(net_position_change)
    if support_loss <= 0:
        return "none"
    ratio = loss_gap / support_loss
    if ratio >= 0.75:
        return "critical"
    if ratio >= 0.50:
        return "high"
    if ratio >= 0.20:
        return "medium"
    return "low"


def evaluate_payment_cliff(inputs: PaymentCliffInput | dict[str, Any]) -> PaymentCliffResult:
    """Detect placeholder support cliffs where support loss exceeds income gain."""

    if isinstance(inputs, dict):
        inputs = _input_from_mapping(inputs)
    support_before = _non_negative_number(inputs.support_before_change, "support_before_change")
    support_after = _non_negative_number(inputs.support_after_change, "support_after_change")
    income_before = _non_negative_number(inputs.income_before_change, "income_before_change")
    income_after = _non_negative_number(inputs.income_after_change, "income_after_change")
    support_loss = max(0.0, support_before - support_after)
    income_gain = max(0.0, income_after - income_before)
    net_position_change = income_gain - support_loss
    cliff_detected = support_loss > income_gain and support_loss - income_gain > max(100.0, support_loss * 0.10)
    return PaymentCliffResult(
        cliff_id=inputs.cliff_id,
        household_id=inputs.household_id,
        support_loss=support_loss,
        income_gain=income_gain,
        net_position_change=net_position_change,
        cliff_detected=cliff_detected,
        cliff_severity_band=_severity_band(net_position_change, support_loss) if cliff_detected else "none",
        warnings=[
            "Payment cliff result is a prototype warning only and not eligibility law.",
            "No real welfare, household, DSS, Services Australia, Treasury, PBO, ABS, or ATO data is used.",
        ],
    )
