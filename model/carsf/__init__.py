"""CARSF concept modelling helpers.

This package implements the concept-level formulas from the CARSF paper. It is
not a tax calculator and does not contain calibrated Australian policy settings.
"""

from .aii import automation_intensity_index
from .aava import australian_automated_value_added
from .aggregation import AggregationResult, EntityInput, evaluate_group_aggregation
from .apportionment import ApportionmentActivity, ApportionmentResult, evaluate_apportionment
from .avoidance import AvoidanceResult, evaluate_avoidance_risk
from .coverage import coverage_measures, cars_i, coverage_ratio, format_coverage_ratio
from .example_runner import ExampleResult, ExampleRunnerError, run_all_examples, run_example
from .frv import net_labour_tax_gap
from .group_runner import GroupedPreviewResult, run_grouped_previews
from .grouping import GroupingRiskResult, evaluate_grouping_risk
from .libc import human_labour_equivalent, output_per_fte_benchmark
from .levy import (
    automation_equilibrium_levy,
    automation_rent_levy,
    calculate_liability,
)
from .qlc import qualified_labour_contribution_firm, qualified_labour_contribution_worker
from .safe_harbour import SafeHarbourResult, evaluate_safe_harbour
from .types import AIIWeights, CoverageResult, LevyParameters, LevyResult, QLCWeights, Worker

__all__ = [
    "AIIWeights",
    "AggregationResult",
    "ApportionmentActivity",
    "ApportionmentResult",
    "AvoidanceResult",
    "CoverageResult",
    "EntityInput",
    "ExampleResult",
    "ExampleRunnerError",
    "GroupedPreviewResult",
    "GroupingRiskResult",
    "LevyParameters",
    "LevyResult",
    "QLCWeights",
    "SafeHarbourResult",
    "Worker",
    "automation_equilibrium_levy",
    "automation_intensity_index",
    "automation_rent_levy",
    "australian_automated_value_added",
    "calculate_liability",
    "cars_i",
    "coverage_measures",
    "coverage_ratio",
    "evaluate_apportionment",
    "evaluate_avoidance_risk",
    "evaluate_group_aggregation",
    "evaluate_grouping_risk",
    "evaluate_safe_harbour",
    "format_coverage_ratio",
    "human_labour_equivalent",
    "net_labour_tax_gap",
    "output_per_fte_benchmark",
    "qualified_labour_contribution_firm",
    "qualified_labour_contribution_worker",
    "run_all_examples",
    "run_grouped_previews",
    "run_example",
]
