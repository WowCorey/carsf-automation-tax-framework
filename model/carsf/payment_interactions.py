"""Prototype orchestration for payment interactions and targeting mechanics."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any

from .payment_stack import PaymentStackComponent, evaluate_payment_stack, payment_stack_component_from_mapping
from .phase_rules import PhaseRule, evaluate_phase_rule, phase_rule_from_mapping
from .support_incidence import (
    SupportIncidenceAssumption,
    evaluate_support_incidence,
    support_incidence_assumption_from_mapping,
)
from .targeting import TargetPopulationInput, evaluate_target_population, targeting_criteria_from_mapping
from .transfer_baseline import (
    TRANSFER_BASELINE_NON_CLAIMS,
    ExistingTransferBaseline,
    evaluate_existing_transfer_baseline,
    existing_transfer_baseline_from_mapping,
)


PAYMENT_INTERACTION_WARNING = (
    "These are prototype payment-interaction outputs only. They are not UBI policy, welfare advice, "
    "eligibility law, Centrelink/DSS/Services Australia modelling, Treasury costing, PBO costing, "
    "legal advice, tax advice, or economic validation."
)
PAYMENT_INTERACTION_NON_CLAIMS = [
    PAYMENT_INTERACTION_WARNING,
    "Payment interaction outputs do not modify firm-level CARSF liability.",
    "Support incidence offsets are not validated savings.",
]


@dataclass(frozen=True)
class PaymentInteractionInput:
    interaction_id: str
    year: int
    baseline: ExistingTransferBaseline
    target_population: TargetPopulationInput
    phase_rule: PhaseRule
    stack_components: list[PaymentStackComponent]
    support_incidence_assumption: SupportIncidenceAssumption
    automation_revenue_available: float
    commonwealth_gap_after_carsf: float
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["baseline"] = self.baseline.to_jsonable()
        payload["target_population"] = self.target_population.to_jsonable()
        payload["phase_rule"] = self.phase_rule.to_jsonable()
        payload["stack_components"] = [component.to_jsonable() for component in self.stack_components]
        payload["support_incidence_assumption"] = self.support_incidence_assumption.to_jsonable()
        return payload


@dataclass(frozen=True)
class PaymentInteractionResult:
    interaction_id: str
    year: int
    baseline_cost: float
    targeted_eligible_people: float
    phase_multiplier: float
    gross_stack_cost: float
    net_stack_cost: float
    double_count_adjustment: float
    support_incidence: dict[str, Any]
    automation_revenue_available: float
    residual_support_gap: float
    combined_commonwealth_gap: float
    targeting_risk_band: str
    interaction_risk_band: str
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(PAYMENT_INTERACTION_NON_CLAIMS))

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


def _input_from_mapping(source: dict[str, Any]) -> PaymentInteractionInput:
    return PaymentInteractionInput(
        interaction_id=str(source["interaction_id"]),
        year=int(source["year"]),
        baseline=existing_transfer_baseline_from_mapping(source["baseline"]),
        target_population=TargetPopulationInput(
            total_population=source["target_population"]["total_population"],
            displaced_workers=source["target_population"]["displaced_workers"],
            reabsorbed_workers=source["target_population"].get("reabsorbed_workers", 0.0),
            retraining_participants=source["target_population"].get("retraining_participants", 0.0),
            existing_support_recipients=source["target_population"].get("existing_support_recipients", 0.0),
            criteria=targeting_criteria_from_mapping(source["target_population"]["criteria"]),
            placeholder_basis=[str(item) for item in source["target_population"].get("placeholder_basis", [])],
            counts_may_overlap=bool(source["target_population"].get("counts_may_overlap", False)),
        ),
        phase_rule=phase_rule_from_mapping(source["phase_rule"]),
        stack_components=[payment_stack_component_from_mapping(item) for item in source.get("stack_components", [])],
        support_incidence_assumption=support_incidence_assumption_from_mapping(source["support_incidence_assumption"]),
        automation_revenue_available=source.get("automation_revenue_available", 0.0),
        commonwealth_gap_after_carsf=source.get("commonwealth_gap_after_carsf", 0.0),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def _risk_score(band: str) -> int:
    return {"low": 0, "medium": 1, "high": 3, "critical": 5}.get(band, 2)


def _interaction_band(score: int) -> str:
    if score <= 1:
        return "low"
    if score <= 3:
        return "medium"
    if score <= 5:
        return "high"
    return "critical"


def evaluate_payment_interactions(inputs: PaymentInteractionInput | dict[str, Any]) -> PaymentInteractionResult:
    """Combine baseline separation, targeting, phase rules, stack interactions, and support incidence."""

    if isinstance(inputs, dict):
        inputs = _input_from_mapping(inputs)

    automation_revenue = _non_negative_number(inputs.automation_revenue_available, "automation_revenue_available")
    commonwealth_gap = _finite_number(inputs.commonwealth_gap_after_carsf, "commonwealth_gap_after_carsf")
    baseline_result = evaluate_existing_transfer_baseline(inputs.baseline)
    target_result = evaluate_target_population(inputs.target_population)
    phase_result = evaluate_phase_rule(inputs.phase_rule, inputs.year)
    phase_adjusted_components = [
        PaymentStackComponent(
            component_id=component.component_id,
            component_type=component.component_type,
            eligible_people=component.eligible_people,
            payment_per_person=component.payment_per_person,
            stack_priority=component.stack_priority,
            mutually_exclusive_with=list(component.mutually_exclusive_with),
            can_stack_with=list(component.can_stack_with),
            phase_multiplier=component.phase_multiplier * phase_result.payment_multiplier,
            placeholder_basis=list(component.placeholder_basis),
        )
        for component in inputs.stack_components
    ]
    stack_result = evaluate_payment_stack(inputs.interaction_id, phase_adjusted_components)
    support_incidence = evaluate_support_incidence(stack_result.net_cost_after_interactions, inputs.support_incidence_assumption)
    residual_support_gap = max(0.0, stack_result.net_cost_after_interactions - automation_revenue)
    combined_gap = commonwealth_gap + residual_support_gap

    coverage_ratio = automation_revenue / stack_result.net_cost_after_interactions if stack_result.net_cost_after_interactions > 0 else None
    score = _risk_score(target_result.targeting_risk_band)
    if residual_support_gap > 0:
        score += 1
    if coverage_ratio is None:
        score += 1
    elif coverage_ratio < 0.40:
        score += 2
    elif coverage_ratio < 0.75:
        score += 1
    if combined_gap > 0 and residual_support_gap > 0:
        score += 1
    if target_result.estimated_exclusion_risk_people > 0:
        score += 1

    warnings = [
        *baseline_result.warnings,
        *target_result.warnings,
        *phase_result.warnings,
        *stack_result.warnings,
        *support_incidence.warnings,
        "Existing baseline cost is reported separately from new transition-payment stack cost.",
        "Firm-level CARSF liability is not modified by payment interaction outputs.",
    ]

    return PaymentInteractionResult(
        interaction_id=inputs.interaction_id,
        year=int(inputs.year),
        baseline_cost=baseline_result.total_existing_baseline_cost,
        targeted_eligible_people=target_result.estimated_eligible_people,
        phase_multiplier=phase_result.payment_multiplier,
        gross_stack_cost=stack_result.gross_cost_before_interactions,
        net_stack_cost=stack_result.net_cost_after_interactions,
        double_count_adjustment=stack_result.double_count_adjustment,
        support_incidence=support_incidence.to_jsonable(),
        automation_revenue_available=automation_revenue,
        residual_support_gap=residual_support_gap,
        combined_commonwealth_gap=combined_gap,
        targeting_risk_band=target_result.targeting_risk_band,
        interaction_risk_band=_interaction_band(score),
        warnings=warnings,
    )
