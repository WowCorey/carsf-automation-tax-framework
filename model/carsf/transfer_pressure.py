"""Placeholder transfer-payment pressure calculations for CARSF trajectories."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any


TRANSFER_PRESSURE_NON_CLAIMS = [
    "Transfer-pressure outputs are illustrative placeholders only and are not DSS estimates.",
    "This is not a UBI, welfare, or transition-payment design module.",
    "No Treasury, ATO, ABS, DSS, PBO, legal, tax, or economic validation is implied.",
]


@dataclass(frozen=True)
class TransferPressureInput:
    net_displaced_workers: float
    average_support_payment_per_person: float
    transition_support_share: float
    retraining_support_share: float
    administrative_cost_per_person: float
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TransferPressureResult:
    support_payment_cost: float
    retraining_support_cost: float
    administrative_cost: float
    total_transfer_pressure: float
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(TRANSFER_PRESSURE_NON_CLAIMS))

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


def _input_from_mapping(source: dict[str, Any]) -> TransferPressureInput:
    return TransferPressureInput(
        net_displaced_workers=source["net_displaced_workers"],
        average_support_payment_per_person=source["average_support_payment_per_person"],
        transition_support_share=source["transition_support_share"],
        retraining_support_share=source["retraining_support_share"],
        administrative_cost_per_person=source["administrative_cost_per_person"],
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def evaluate_transfer_pressure(inputs: TransferPressureInput | dict[str, Any]) -> TransferPressureResult:
    """Estimate placeholder transfer and retraining pressure for displaced workers."""

    if isinstance(inputs, dict):
        inputs = _input_from_mapping(inputs)

    workers = _non_negative_number(inputs.net_displaced_workers, "net_displaced_workers")
    support_payment = _non_negative_number(inputs.average_support_payment_per_person, "average_support_payment_per_person")
    transition_share = _bounded_rate(inputs.transition_support_share, "transition_support_share")
    retraining_share = _bounded_rate(inputs.retraining_support_share, "retraining_support_share")
    admin_cost = _non_negative_number(inputs.administrative_cost_per_person, "administrative_cost_per_person")

    support_payment_cost = workers * support_payment * transition_share
    retraining_support_cost = workers * support_payment * retraining_share
    administrative_cost = workers * admin_cost

    return TransferPressureResult(
        support_payment_cost=support_payment_cost,
        retraining_support_cost=retraining_support_cost,
        administrative_cost=administrative_cost,
        total_transfer_pressure=support_payment_cost + retraining_support_cost + administrative_cost,
        warnings=["Transfer-pressure values are placeholder-only and are not welfare-system costings."],
    )
