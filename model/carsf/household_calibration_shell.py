"""Calibration readiness shell for synthetic household weighting."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .household_weights import HOUSEHOLD_WEIGHTING_NON_CLAIMS


@dataclass(frozen=True)
class HouseholdCalibrationRequirement:
    requirement_id: str
    category: str
    description: str
    required_for: list[str]
    possible_source_type: str
    real_data_in_repo_allowed: bool = False
    status: str = "unmet"
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(HOUSEHOLD_WEIGHTING_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class HouseholdCalibrationShellResult:
    requirement_count: int
    unmet_requirement_count: int
    requirements: list[HouseholdCalibrationRequirement]
    ready_for_real_distributional_claims: bool = False
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(HOUSEHOLD_WEIGHTING_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["requirements"] = [requirement.to_jsonable() for requirement in self.requirements]
        return payload


def _requirement(requirement_id: str, category: str, description: str, required_for: list[str], source_type: str) -> HouseholdCalibrationRequirement:
    return HouseholdCalibrationRequirement(
        requirement_id=requirement_id,
        category=category,
        description=description,
        required_for=required_for,
        possible_source_type=source_type,
        real_data_in_repo_allowed=False,
        status="unmet",
        warnings=[
            "Requirement is unmet; no real household calibration data is stored in this repository.",
        ],
    )


def get_household_calibration_requirements() -> HouseholdCalibrationShellResult:
    """Return unmet external data requirements for future household weighting."""

    requirements = [
        _requirement("hh_comp", "household composition", "Household type and dependency composition distributions.", ["subgroup weighting"], "ABS/Census/HILDA category only"),
        _requirement("income_dist", "income distribution", "Income-band and post-displacement income distributions.", ["budget stress", "subgroup weighting"], "ATO/ABS/HILDA category only"),
        _requirement("employment_disp", "employment displacement", "Displacement incidence by sector, role, and household type.", ["shock weighting"], "Treasury/ABS/labour-market category only"),
        _requirement("regional_depth", "regional labour-market depth", "Regional employment depth and transition capacity.", ["regional stress"], "ABS/regional labour-market category only"),
        _requirement("housing_costs", "housing costs", "Housing cost pressure by household type and region.", ["budget stress"], "ABS/housing survey category only"),
        _requirement("essential_costs", "essential costs", "Essential living cost pressure by household type.", ["budget stress"], "household expenditure survey category only"),
        _requirement("buffers", "savings/debt buffers", "Savings and debt buffer distributions.", ["shock severity"], "HILDA/household survey category only"),
        _requirement("welfare_baseline", "welfare/transfer baseline", "Existing support baseline interaction by household type.", ["support adequacy"], "DSS/Services Australia category only"),
        _requirement("reemployment", "re-employment timing", "Re-employment timing and income recovery distributions.", ["reemployment risk"], "HILDA/labour-market transition category only"),
        _requirement("eligibility", "payment eligibility", "Eligibility, phase-out, exclusion, and leakage parameters.", ["payment cliff", "support targeting"], "DSS/legal policy category only"),
        _requirement("survey_weights", "survey weighting", "Survey weights or population weights for representativeness.", ["weighted aggregation"], "ABS/HILDA/Census category only"),
        _requirement("uncertainty", "uncertainty/confidence intervals", "Uncertainty ranges and confidence methods for weighted outputs.", ["reporting"], "Treasury/PBO/statistical review category only"),
    ]
    return HouseholdCalibrationShellResult(
        requirement_count=len(requirements),
        unmet_requirement_count=len(requirements),
        requirements=requirements,
        ready_for_real_distributional_claims=False,
        warnings=[
            "All household weighting calibration requirements are unmet.",
            "Real household data is not allowed in this repository.",
            "A controlled external data environment would be required before any real distributional claim.",
        ],
    )
