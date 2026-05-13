"""Prototype payment-stack and double-counting mechanics."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any

from .transfer_baseline import TRANSFER_BASELINE_NON_CLAIMS


@dataclass(frozen=True)
class PaymentStackComponent:
    component_id: str
    component_type: str
    eligible_people: float
    payment_per_person: float
    stack_priority: int
    mutually_exclusive_with: list[str] = field(default_factory=list)
    can_stack_with: list[str] = field(default_factory=list)
    phase_multiplier: float = 1.0
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PaymentStackResult:
    stack_id: str
    components: list[dict[str, Any]]
    gross_cost_before_interactions: float
    double_count_adjustment: float
    net_cost_after_interactions: float
    people_double_counted_preview: float
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


def _component_from_mapping(source: dict[str, Any]) -> PaymentStackComponent:
    return PaymentStackComponent(
        component_id=str(source["component_id"]),
        component_type=str(source.get("component_type", source["component_id"])),
        eligible_people=source["eligible_people"],
        payment_per_person=source["payment_per_person"],
        stack_priority=int(source.get("stack_priority", 0)),
        mutually_exclusive_with=[str(item) for item in source.get("mutually_exclusive_with", [])],
        can_stack_with=[str(item) for item in source.get("can_stack_with", [])],
        phase_multiplier=source.get("phase_multiplier", 1.0),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def payment_stack_component_from_mapping(source: PaymentStackComponent | dict[str, Any]) -> PaymentStackComponent:
    if isinstance(source, PaymentStackComponent):
        return source
    return _component_from_mapping(source)


def _validated_component(component: PaymentStackComponent) -> PaymentStackComponent:
    return PaymentStackComponent(
        component_id=component.component_id,
        component_type=component.component_type,
        eligible_people=_non_negative_number(component.eligible_people, f"{component.component_id}.eligible_people"),
        payment_per_person=_non_negative_number(component.payment_per_person, f"{component.component_id}.payment_per_person"),
        stack_priority=int(component.stack_priority),
        mutually_exclusive_with=list(component.mutually_exclusive_with),
        can_stack_with=list(component.can_stack_with),
        phase_multiplier=_bounded_rate(component.phase_multiplier, f"{component.component_id}.phase_multiplier"),
        placeholder_basis=list(component.placeholder_basis),
    )


def _component_cost(component: PaymentStackComponent) -> float:
    return component.eligible_people * component.payment_per_person * component.phase_multiplier


def evaluate_payment_stack(stack_id: str, components: list[PaymentStackComponent | dict[str, Any]]) -> PaymentStackResult:
    """Calculate placeholder stack cost and mutual-exclusion double-count adjustment."""

    if not components:
        raise ValueError("payment stack must include at least one component")
    validated = [_validated_component(payment_stack_component_from_mapping(component)) for component in components]
    validated.sort(key=lambda item: (item.stack_priority, item.component_id))

    component_rows: list[dict[str, Any]] = []
    for component in validated:
        row = component.to_jsonable()
        row["phase_adjusted_cost"] = _component_cost(component)
        component_rows.append(row)

    gross_cost = sum(row["phase_adjusted_cost"] for row in component_rows)
    by_id = {component.component_id: component for component in validated}
    adjustment = 0.0
    double_counted_people = 0.0
    seen_pairs: set[tuple[str, str]] = set()
    warnings = [
        "Payment-stack interaction is placeholder-only and does not use person-level eligibility data.",
        "Double-count adjustments are review previews, not real welfare-system offsets.",
    ]

    for component in validated:
        for target_id in component.mutually_exclusive_with:
            if target_id not in by_id:
                warnings.append(f"Mutual exclusion target {target_id} is not present in stack.")
                continue
            pair = tuple(sorted([component.component_id, target_id]))
            if pair in seen_pairs:
                continue
            seen_pairs.add(pair)
            other = by_id[target_id]
            lower_priority = component if component.stack_priority >= other.stack_priority else other
            overlap_people = min(component.eligible_people, other.eligible_people)
            adjustment += overlap_people * lower_priority.payment_per_person * lower_priority.phase_multiplier
            double_counted_people += overlap_people

    if not seen_pairs and len(validated) > 1:
        warnings.append("No explicit overlap metadata supplied; stack assumes no double-count adjustment pending review.")

    net_cost = max(0.0, gross_cost - adjustment)
    return PaymentStackResult(
        stack_id=stack_id,
        components=component_rows,
        gross_cost_before_interactions=gross_cost,
        double_count_adjustment=adjustment,
        net_cost_after_interactions=net_cost,
        people_double_counted_preview=double_counted_people,
        warnings=warnings,
    )
