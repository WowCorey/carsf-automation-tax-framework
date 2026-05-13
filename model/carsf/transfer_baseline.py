"""Prototype separation of existing transfer baselines from new transition payments."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any


TRANSFER_BASELINE_WARNING = (
    "These are prototype payment-interaction outputs only. They are not UBI policy, welfare advice, "
    "eligibility law, Centrelink/DSS/Services Australia modelling, Treasury costing, PBO costing, "
    "legal advice, tax advice, or economic validation."
)
TRANSFER_BASELINE_NON_CLAIMS = [
    TRANSFER_BASELINE_WARNING,
    "Existing transfer baseline outputs are illustrative placeholders only.",
    "Existing transfer baseline outputs do not modify firm-level CARSF liability.",
]


@dataclass(frozen=True)
class ExistingTransferBaseline:
    baseline_id: str
    eligible_population: float
    average_existing_support_per_person: float
    existing_admin_cost_per_person: float
    baseline_program_type: str
    illustrative_placeholder_only: bool = True
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TransferBaselineResult:
    baseline_id: str
    eligible_population: float
    existing_support_cost: float
    existing_admin_cost: float
    total_existing_baseline_cost: float
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


def _baseline_from_mapping(source: dict[str, Any]) -> ExistingTransferBaseline:
    return ExistingTransferBaseline(
        baseline_id=str(source["baseline_id"]),
        eligible_population=source["eligible_population"],
        average_existing_support_per_person=source["average_existing_support_per_person"],
        existing_admin_cost_per_person=source.get("existing_admin_cost_per_person", 0.0),
        baseline_program_type=str(source.get("baseline_program_type", "placeholder_existing_transfer")),
        illustrative_placeholder_only=bool(source.get("illustrative_placeholder_only", True)),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def existing_transfer_baseline_from_mapping(source: ExistingTransferBaseline | dict[str, Any]) -> ExistingTransferBaseline:
    if isinstance(source, ExistingTransferBaseline):
        return source
    return _baseline_from_mapping(source)


def evaluate_existing_transfer_baseline(baseline: ExistingTransferBaseline | dict[str, Any]) -> TransferBaselineResult:
    """Calculate placeholder existing-transfer baseline costs separately from new support."""

    if isinstance(baseline, dict):
        baseline = _baseline_from_mapping(baseline)

    if baseline.illustrative_placeholder_only is not True:
        raise ValueError("existing transfer baseline must be illustrative_placeholder_only")
    eligible_population = _non_negative_number(baseline.eligible_population, "eligible_population")
    support = _non_negative_number(
        baseline.average_existing_support_per_person,
        "average_existing_support_per_person",
    )
    admin = _non_negative_number(baseline.existing_admin_cost_per_person, "existing_admin_cost_per_person")
    support_cost = eligible_population * support
    admin_cost = eligible_population * admin
    return TransferBaselineResult(
        baseline_id=baseline.baseline_id,
        eligible_population=eligible_population,
        existing_support_cost=support_cost,
        existing_admin_cost=admin_cost,
        total_existing_baseline_cost=support_cost + admin_cost,
        warnings=[
            "Existing transfer baseline is separated from new automation-transition payment cost.",
            "This is not a real DSS, Centrelink, Services Australia, Treasury, or PBO estimate.",
        ],
    )
