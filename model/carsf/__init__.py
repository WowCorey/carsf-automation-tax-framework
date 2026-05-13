"""CARSF concept modelling helpers.

This package implements the concept-level formulas from the CARSF paper. It is
not a tax calculator and does not contain calibrated Australian policy settings.
"""

from .aii import automation_intensity_index
from .aava import australian_automated_value_added
from .aggregation import AggregationResult, EntityInput, evaluate_group_aggregation
from .apportionment import ApportionmentActivity, ApportionmentResult, evaluate_apportionment
from .avoidance import AvoidanceResult, evaluate_avoidance_risk
from .calibration import (
    CalibrationRegistry,
    CalibrationRequirement,
    get_calibration_registry,
    list_requirements_by_component,
    validate_no_fake_calibration_values,
)
from .coverage import coverage_measures, cars_i, coverage_ratio, format_coverage_ratio
from .decision_log import (
    DecisionLog,
    DecisionLogEntry,
    add_decision_entry,
    create_decision_log,
    summarise_decision_log,
)
from .evidence import (
    EvidenceAssessment,
    EvidenceItem,
    EvidenceRequirement,
    assess_evidence,
    get_default_evidence_requirements,
)
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
from .mixed_units import (
    MixedUnitExposureResult,
    UnitCompatibilityResult,
    evaluate_mixed_unit_exposure,
    evaluate_unit_compatibility,
)
from .qlc import qualified_labour_contribution_firm, qualified_labour_contribution_worker
from .safe_harbour import SafeHarbourResult, evaluate_safe_harbour
from .transfer_pricing import (
    AdjustedAAVAPreview,
    AdjustmentCandidate,
    LiabilityAdjustmentPreview,
    RelatedPartyTransaction,
    TransferPricingPreviewResult,
    evaluate_transfer_pricing_preview,
    preview_adjusted_aava,
    preview_liability_with_adjusted_aava,
)
from .transfer_runner import (
    TransferPricingPreviewReport,
    TransferPricingScenarioResult,
    run_transfer_pricing_previews,
)
from .types import AIIWeights, CoverageResult, LevyParameters, LevyResult, QLCWeights, Worker

__all__ = [
    "AIIWeights",
    "AdjustedAAVAPreview",
    "AggregationResult",
    "AdjustmentCandidate",
    "ApportionmentActivity",
    "ApportionmentResult",
    "AvoidanceResult",
    "CalibrationRegistry",
    "CalibrationRequirement",
    "CoverageResult",
    "DecisionLog",
    "DecisionLogEntry",
    "EntityInput",
    "EvidenceAssessment",
    "EvidenceItem",
    "EvidenceRequirement",
    "ExampleResult",
    "ExampleRunnerError",
    "GroupedPreviewResult",
    "GroupingRiskResult",
    "LevyParameters",
    "LevyResult",
    "LiabilityAdjustmentPreview",
    "MixedUnitExposureResult",
    "QLCWeights",
    "RelatedPartyTransaction",
    "SafeHarbourResult",
    "TransferPricingPreviewResult",
    "TransferPricingPreviewReport",
    "TransferPricingScenarioResult",
    "UnitCompatibilityResult",
    "Worker",
    "add_decision_entry",
    "assess_evidence",
    "automation_equilibrium_levy",
    "automation_intensity_index",
    "automation_rent_levy",
    "australian_automated_value_added",
    "calculate_liability",
    "cars_i",
    "coverage_measures",
    "coverage_ratio",
    "create_decision_log",
    "evaluate_apportionment",
    "evaluate_avoidance_risk",
    "evaluate_group_aggregation",
    "evaluate_grouping_risk",
    "evaluate_mixed_unit_exposure",
    "evaluate_safe_harbour",
    "evaluate_transfer_pricing_preview",
    "evaluate_unit_compatibility",
    "format_coverage_ratio",
    "get_calibration_registry",
    "get_default_evidence_requirements",
    "human_labour_equivalent",
    "list_requirements_by_component",
    "net_labour_tax_gap",
    "output_per_fte_benchmark",
    "preview_adjusted_aava",
    "preview_liability_with_adjusted_aava",
    "qualified_labour_contribution_firm",
    "qualified_labour_contribution_worker",
    "run_all_examples",
    "run_grouped_previews",
    "run_example",
    "run_transfer_pricing_previews",
    "summarise_decision_log",
    "validate_no_fake_calibration_values",
]
