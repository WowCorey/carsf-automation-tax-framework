"""Calibration registry shell for CARSF V1.5.

No real calibration values are stored here. The registry identifies future data
requirements and unresolved dependencies only.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


CALIBRATION_NON_CLAIMS = [
    "This calibration registry is a prototype shell only.",
    "No real calibration values, official data, legal validation, tax validation, Treasury validation, ATO validation, ABS validation, Fair Work validation, or economic validation are included.",
    "All calibration statuses remain not_collected or placeholder until authorised data and review are supplied.",
]
SOURCE_PLACEHOLDERS = {
    "ABS labour force / industry data",
    "ATO aggregated tax data",
    "PBO fiscal projections",
    "DSS / Services Australia payment data",
    "Fair Work / wage award data",
    "HILDA longitudinal labour data",
    "superannuation guarantee data",
    "HELP/HECS repayment data",
    "state payroll tax datasets",
    "industry productivity datasets",
    "business survey data",
    "Treasury modelling",
    "independent legal/tax review",
}
REQUIRED_COMPONENTS = [
    "OPFTE_LIBC benchmarks",
    "FRV floor/standard/full",
    "QLC weights and QLCMaxMultiplier",
    "AII component weights",
    "AAVA deductibility categories",
    "cap rates lambda_sector / LAMBDA_sector",
    "theta credit cap",
    "uplift rate and rent tax rate",
    "safe-harbour thresholds",
    "avoidance risk thresholds",
    "transfer-pricing review shares",
    "mixed-unit exposure weighting",
    "labour-market absorption rates",
    "wage compression / underemployment modules",
    "GST consumption effects",
    "superannuation and HELP/HECS effects",
    "state payroll tax effects",
    "regional weighting",
    "public-sector automation",
    "investment deterrence / tax incidence parameters",
]


@dataclass(frozen=True)
class CalibrationRequirement:
    requirement_id: str
    model_component: str
    required_dataset: str
    preferred_source: str
    fallback_source: str
    update_frequency: str
    geographic_scope: str
    sector_scope: str
    privacy_sensitivity: str
    legal_sensitivity: str
    calibration_status: str
    notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CalibrationRegistry:
    version: str
    requirements: list[CalibrationRequirement]
    placeholder_fields: list[str]
    unresolved_dependencies: list[str]
    non_claims: list[str] = field(default_factory=lambda: list(CALIBRATION_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _slug(value: str) -> str:
    return (
        value.lower()
        .replace("/", "_")
        .replace("-", "_")
        .replace(" ", "_")
        .replace("__", "_")
    )


def _source_for(component: str) -> tuple[str, str]:
    if "OPFTE" in component:
        return "ABS labour force / industry data", "industry productivity datasets"
    if "FRV" in component or "tax" in component or "HELP" in component or "superannuation" in component:
        return "ATO aggregated tax data", "PBO fiscal projections"
    if "QLC" in component or "wage" in component or "underemployment" in component:
        return "Fair Work / wage award data", "HILDA longitudinal labour data"
    if "DSS" in component or "labour-market" in component:
        return "DSS / Services Australia payment data", "HILDA longitudinal labour data"
    if "transfer-pricing" in component or "deductibility" in component:
        return "independent legal/tax review", "Treasury modelling"
    if "mixed-unit" in component or "AII" in component:
        return "business survey data", "industry productivity datasets"
    return "Treasury modelling", "business survey data"


def get_calibration_registry() -> CalibrationRegistry:
    requirements: list[CalibrationRequirement] = []
    for component in REQUIRED_COMPONENTS:
        preferred, fallback = _source_for(component)
        requirements.append(
            CalibrationRequirement(
                requirement_id=f"cal_{_slug(component)}",
                model_component=component,
                required_dataset=f"{component} calibration dataset placeholder",
                preferred_source=preferred,
                fallback_source=fallback,
                update_frequency="to_be_determined_after_policy_review",
                geographic_scope="Australia; finer regional scope unresolved",
                sector_scope="Schedule-specific; prototype schedules only in V1.5",
                privacy_sensitivity="high" if component in {"labour-market absorption rates", "wage compression / underemployment modules"} else "medium",
                legal_sensitivity="high" if component in {"AAVA deductibility categories", "transfer-pricing review shares"} else "medium",
                calibration_status="not_collected",
                notes=[
                    "No real value is stored in this registry.",
                    "Requires authorised source data, privacy review, and independent policy/legal review before use.",
                ],
            )
        )
    return CalibrationRegistry(
        version="CARSF V1.5 calibration shell",
        requirements=requirements,
        placeholder_fields=[requirement.model_component for requirement in requirements],
        unresolved_dependencies=[
            "Treasury/ATO-style data access and modelling governance",
            "Privacy and secrecy review for restricted datasets",
            "Independent legal/tax review",
            "Sector-specific calibration methodology",
            "Economic incidence and behavioural response modelling",
        ],
    )


def list_requirements_by_component(component: str) -> list[CalibrationRequirement]:
    component_lower = component.lower()
    return [
        requirement
        for requirement in get_calibration_registry().requirements
        if component_lower in requirement.model_component.lower()
    ]


def validate_no_fake_calibration_values(registry: CalibrationRegistry) -> bool:
    allowed_statuses = {"not_collected", "placeholder", "placeholder_only"}
    for requirement in registry.requirements:
        if requirement.calibration_status not in allowed_statuses:
            return False
        if requirement.preferred_source not in SOURCE_PLACEHOLDERS:
            return False
        if requirement.fallback_source not in SOURCE_PLACEHOLDERS:
            return False
    return True
