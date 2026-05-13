"""Typed inputs and outputs for the CARSF concept model."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping


@dataclass(frozen=True)
class QLCWeights:
    """Schedule-defined weights for Qualified Labour Contribution."""

    alpha: float = 0.20
    beta: float = 0.20
    gamma: float = 0.15
    delta: float = 0.15
    qlc_max_multiplier: float = 1.25


@dataclass(frozen=True)
class Worker:
    """Worker inputs used to calculate QLC."""

    annual_hours: float
    wage_quality: float
    job_security: float
    skill_development: float
    australian_nexus: float
    full_time_hours: float = 1820.0


@dataclass(frozen=True)
class AIIWeights:
    """Schedule-defined weights for Automation Intensity Index."""

    compute_ratio: float = 0.25
    auto_decision_ratio: float = 0.25
    robotics_capital_ratio: float = 0.25
    auto_process_share: float = 0.25

    def as_mapping(self) -> Mapping[str, float]:
        return {
            "compute_ratio": self.compute_ratio,
            "auto_decision_ratio": self.auto_decision_ratio,
            "robotics_capital_ratio": self.robotics_capital_ratio,
            "auto_process_share": self.auto_process_share,
        }


@dataclass(frozen=True)
class LevyParameters:
    """Concept-level levy parameters.

    Values supplied by prototype schedules are placeholders until calibrated by
    Treasury/ATO/ABS/HILDA/DSS and sector data.
    """

    frv_standard: float
    lambda_sector: float
    lambda_combined: float
    theta: float
    uplift_rate: float
    rent_tax_rate: float


@dataclass(frozen=True)
class LevyResult:
    """Calculated liability components."""

    ael_raw: float
    ael_payable: float
    shortfall: float
    arl: float
    credits: float
    combined_liability: float
    liability: float


@dataclass(frozen=True)
class CoverageResult:
    """National-level fiscal coverage metrics."""

    cars_i: float
    coverage_ratio: float
    notes: tuple[str, ...] = field(default_factory=tuple)
