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
from .classification import classify_evidence_item, classify_packet
from .evidence import (
    EvidenceAssessment,
    EvidenceItem,
    EvidenceRequirement,
    assess_evidence,
    get_default_evidence_requirements,
)
from .evidence_packet import (
    EvidencePacket,
    EvidencePacketSummary,
    load_evidence_packet,
    summarise_evidence_packet,
    validate_evidence_packet,
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
from .redaction import RedactionPlan, create_redaction_plan
from .repo_guardrails import (
    RepoGuardrailPolicy,
    RepoScanFinding,
    RepoScanResult,
    get_default_repo_guardrail_policy,
    scan_file,
    scan_repo,
)
from .retention import AccessControlPolicy, RetentionPolicy, get_access_control_policy, get_retention_policy
from .review_workflow import ReviewTransition, ReviewWorkflowResult, evaluate_review_transition
from .safe_harbour import SafeHarbourResult, evaluate_safe_harbour
from .secure_ingestion import (
    IngestionDecision,
    IngestionPolicy,
    IngestionRequest,
    evaluate_ingestion_request,
    get_default_ingestion_policy,
)
from .sensitive_scan import SensitiveScanResult, scan_mapping_for_sensitive_markers, scan_text_for_sensitive_markers
from .ingestion_audit import IngestionAuditRecord, create_ingestion_audit_record
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
    "AccessControlPolicy",
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
    "EvidencePacket",
    "EvidencePacketSummary",
    "EvidenceRequirement",
    "ExampleResult",
    "ExampleRunnerError",
    "GroupedPreviewResult",
    "GroupingRiskResult",
    "IngestionAuditRecord",
    "IngestionDecision",
    "IngestionPolicy",
    "IngestionRequest",
    "LevyParameters",
    "LevyResult",
    "LiabilityAdjustmentPreview",
    "MixedUnitExposureResult",
    "QLCWeights",
    "RelatedPartyTransaction",
    "RedactionPlan",
    "RepoGuardrailPolicy",
    "RepoScanFinding",
    "RepoScanResult",
    "ReviewTransition",
    "ReviewWorkflowResult",
    "RetentionPolicy",
    "SafeHarbourResult",
    "SensitiveScanResult",
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
    "classify_evidence_item",
    "classify_packet",
    "coverage_measures",
    "coverage_ratio",
    "create_decision_log",
    "create_ingestion_audit_record",
    "create_redaction_plan",
    "evaluate_apportionment",
    "evaluate_avoidance_risk",
    "evaluate_group_aggregation",
    "evaluate_grouping_risk",
    "evaluate_ingestion_request",
    "evaluate_mixed_unit_exposure",
    "evaluate_review_transition",
    "evaluate_safe_harbour",
    "evaluate_transfer_pricing_preview",
    "evaluate_unit_compatibility",
    "format_coverage_ratio",
    "get_access_control_policy",
    "get_calibration_registry",
    "get_default_evidence_requirements",
    "get_default_ingestion_policy",
    "get_default_repo_guardrail_policy",
    "get_retention_policy",
    "human_labour_equivalent",
    "list_requirements_by_component",
    "load_evidence_packet",
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
    "scan_mapping_for_sensitive_markers",
    "scan_file",
    "scan_repo",
    "scan_text_for_sensitive_markers",
    "summarise_decision_log",
    "summarise_evidence_packet",
    "validate_no_fake_calibration_values",
    "validate_evidence_packet",
]
