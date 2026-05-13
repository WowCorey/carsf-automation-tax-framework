"""Placeholder transition-payment design calculations for CARSF."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any


TRANSITION_PAYMENT_WARNING = (
    "These are prototype transition-payment funding outputs only. They are not UBI policy, welfare advice, "
    "DSS modelling, Services Australia modelling, Treasury costing, PBO costing, legal advice, tax advice, "
    "or economic validation."
)
TRANSITION_PAYMENT_NON_CLAIMS = [
    TRANSITION_PAYMENT_WARNING,
    "Transition-payment outputs are illustrative placeholders only.",
    "Transition-payment outputs do not modify firm-level CARSF liability.",
]


@dataclass(frozen=True)
class TransitionPaymentDesign:
    design_id: str
    design_name: str
    eligible_population: str
    annual_payment_per_person: float
    participation_rate: float
    admin_cost_per_person: float
    retraining_component_per_person: float
    duration_years: float | None = None
    illustrative_placeholder_only: bool = True
    placeholder_basis: list[str] = field(default_factory=list)
    design_type: str = "DISPLACED_WORKER_SUPPLEMENT"

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TransitionPaymentInput:
    design: TransitionPaymentDesign
    eligible_people: float
    year: int
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["design"] = self.design.to_jsonable()
        return payload


@dataclass(frozen=True)
class TransitionPaymentResult:
    year: int
    design_id: str
    eligible_people: float
    covered_people: float
    base_payment_cost: float
    retraining_component_cost: float
    administrative_cost: float
    total_program_cost: float
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(TRANSITION_PAYMENT_NON_CLAIMS))

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


def _design_from_mapping(source: dict[str, Any]) -> TransitionPaymentDesign:
    return TransitionPaymentDesign(
        design_id=str(source["design_id"]),
        design_name=str(source.get("design_name", source["design_id"])),
        eligible_population=str(source.get("eligible_population", "displaced_workers")),
        annual_payment_per_person=source.get("annual_payment_per_person", 0.0),
        participation_rate=source.get("participation_rate", 0.0),
        admin_cost_per_person=source.get("admin_cost_per_person", 0.0),
        retraining_component_per_person=source.get("retraining_component_per_person", 0.0),
        duration_years=source.get("duration_years"),
        illustrative_placeholder_only=bool(source.get("illustrative_placeholder_only", True)),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
        design_type=str(source.get("design_type", source.get("design_id", "DISPLACED_WORKER_SUPPLEMENT"))),
    )


def transition_design_from_mapping(source: dict[str, Any] | TransitionPaymentDesign) -> TransitionPaymentDesign:
    if isinstance(source, TransitionPaymentDesign):
        return source
    return _design_from_mapping(source)


def _input_from_mapping(source: dict[str, Any]) -> TransitionPaymentInput:
    return TransitionPaymentInput(
        design=transition_design_from_mapping(source["design"]),
        eligible_people=source["eligible_people"],
        year=int(source["year"]),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def evaluate_transition_payment(inputs: TransitionPaymentInput | dict[str, Any]) -> TransitionPaymentResult:
    """Calculate placeholder transition-payment cost for one design/year."""

    if isinstance(inputs, dict):
        inputs = _input_from_mapping(inputs)

    design = inputs.design
    eligible_people = _non_negative_number(inputs.eligible_people, "eligible_people")
    annual_payment = _non_negative_number(design.annual_payment_per_person, "annual_payment_per_person")
    participation_rate = _bounded_rate(design.participation_rate, "participation_rate")
    admin_cost = _non_negative_number(design.admin_cost_per_person, "admin_cost_per_person")
    retraining = _non_negative_number(design.retraining_component_per_person, "retraining_component_per_person")
    if design.duration_years is not None and _finite_number(design.duration_years, "duration_years") <= 0:
        raise ValueError("duration_years must be positive when supplied")
    if design.illustrative_placeholder_only is not True:
        raise ValueError("transition payment design must be illustrative_placeholder_only")

    covered_people = eligible_people * participation_rate
    return TransitionPaymentResult(
        year=int(inputs.year),
        design_id=design.design_id,
        eligible_people=eligible_people,
        covered_people=covered_people,
        base_payment_cost=covered_people * annual_payment,
        retraining_component_cost=covered_people * retraining,
        administrative_cost=covered_people * admin_cost,
        total_program_cost=covered_people * (annual_payment + retraining + admin_cost),
        warnings=[
            "Transition-payment design is illustrative placeholder only.",
            "This result is not a real UBI, welfare, DSS, Services Australia, Treasury, or PBO costing.",
        ],
    )
