"""CARSF concept modelling helpers.

This package implements the concept-level formulas from the CARSF paper. It is
not a tax calculator and does not contain calibrated Australian policy settings.
"""

from .aii import automation_intensity_index
from .aava import australian_automated_value_added
from .aggregation import AggregationResult, EntityInput, evaluate_group_aggregation
from .administrative_workflow import (
    AdministrativeWorkflowResult,
    AdministrativeWorkflowScenario,
    AdministrativeWorkflowSummary,
    EvidenceRequestBundle,
    WorkflowEscalation,
    WorkflowQueueAssignment,
    evaluate_administrative_workflow,
    evaluate_administrative_workflows,
    summarise_administrative_workflows,
    validate_administrative_workflow_scenario,
    validate_administrative_workflow_scenarios,
)
from .apportionment import ApportionmentActivity, ApportionmentResult, evaluate_apportionment
from .avoidance import AvoidanceResult, evaluate_avoidance_risk
from .behavioural_response import (
    BehaviouralCountermeasure,
    BehaviouralResponseResult,
    BehaviouralResponseScenario,
    BehaviouralResponseSummary,
    evaluate_behavioural_response,
    evaluate_behavioural_responses,
    summarise_behavioural_responses,
    validate_behavioural_response_scenario,
    validate_behavioural_response_scenarios,
)
from .burden_balance import BurdenBalanceInput, BurdenBalanceResult, evaluate_burden_balance
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
from .distributional_scenarios import (
    DistributionalScenarioInput,
    DistributionalScenarioResult,
    evaluate_distributional_scenario,
)
from .distributional_summary import DistributionalSummaryResult, summarise_distributional_scenarios
from .distributional_uncertainty import (
    HouseholdUncertaintyInput,
    HouseholdUncertaintyResult,
    evaluate_household_uncertainty,
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
from .fiscal_sensitivity import FiscalSensitivityPoint, FiscalSensitivityResult, run_fiscal_sensitivity
from .fiscal_trajectory import FiscalTrajectoryInput, FiscalTrajectoryResult, FiscalYearResult, run_fiscal_trajectory
from .frv import net_labour_tax_gap
from .group_runner import GroupedPreviewResult, run_grouped_previews
from .grouping import GroupingRiskResult, evaluate_grouping_risk
from .household_calibration_shell import (
    HouseholdCalibrationRequirement,
    HouseholdCalibrationShellResult,
    get_household_calibration_requirements,
)
from .household_weights import HouseholdWeight, HouseholdWeightResult, evaluate_household_weight
from .households import HouseholdBudgetResult, SyntheticHousehold, evaluate_household_budget
from .incidence import IncidenceAssumption, IncidenceResult, evaluate_tax_incidence
from .investment import InvestmentGuardrailInput, InvestmentGuardrailResult, evaluate_investment_guardrail
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
from .payment_interactions import PaymentInteractionInput, PaymentInteractionResult, evaluate_payment_interactions
from .payment_portfolio import PaymentPortfolioInput, PaymentPortfolioResult, evaluate_payment_portfolio
from .payment_sensitivity import PaymentSensitivityPoint, PaymentSensitivityResult, run_payment_sensitivity
from .payment_stack import PaymentStackComponent, PaymentStackResult, evaluate_payment_stack
from .payment_cliffs import PaymentCliffInput, PaymentCliffResult, evaluate_payment_cliff
from .phase_rules import PhaseRule, PhaseRuleYearResult, evaluate_phase_rule
from .public_revenue import PublicRevenueInput, PublicRevenueResult, evaluate_public_revenue
from .public_data_pilot import (
    FieldSanityCheck,
    ModuleSanityCheck,
    PlaceholderAnchorRecord,
    PublicAggregateExtract,
    PublicDataBoundaryCheck,
    PublicDataDigest,
    PublicDataPilotResult,
    PublicDataPilotSummary,
    PublicDataSourceReference,
    build_public_data_pilot_result,
    find_forbidden_affirmative_public_data_claims,
)
from .public_data_evidence_map import (
    ExtractEvidenceMap,
    FieldSanityEvidenceMap,
    ModuleSanityEvidenceMap,
    PlaceholderEvidenceMap,
    RestrictedBlockerEvidenceMap,
    ReviewerEvidenceMapResult,
    ReviewerEvidenceMapSummary,
    ReviewerQuestion,
    SourceEvidenceMap,
    build_public_data_evidence_map_result,
)
from .qlc import qualified_labour_contribution_firm, qualified_labour_contribution_worker
from .redaction import RedactionPlan, create_redaction_plan
from .real_data_feasibility import (
    CalibrationFieldRequirement,
    CalibrationIntakeResult,
    CalibrationIntakeSummary,
    DataSourceCandidate,
    ForbiddenDataRule,
    ModuleDataNeed,
    PublicDataPilotCandidate,
    RealisticPlaceholderSpec,
    RestrictedDataRequirement,
    build_calibration_intake_result,
    find_forbidden_affirmative_real_data_claims,
)
from .reemployment import ReemploymentPath, ReemploymentResult, evaluate_reemployment_path
from .regional_stress import RegionalStressInput, RegionalStressResult, evaluate_regional_stress
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
from .scenario_review import (
    ReviewedScenarioInput,
    ReviewedScenarioResult,
    ReviewedScenarioSummary,
    review_scenario,
    summarise_reviewed_scenarios,
)
from .safe_harbour import SafeHarbourResult, evaluate_safe_harbour
from .secure_ingestion import (
    IngestionDecision,
    IngestionPolicy,
    IngestionRequest,
    evaluate_ingestion_request,
    get_default_ingestion_policy,
)
from .sector_stress_matrix import (
    SectorStressInput,
    SectorStressResult,
    SectorStressSummary,
    build_sector_stress_matrix,
    evaluate_sector_stress,
    summarise_sector_stress,
)
from .sensitive_scan import SensitiveScanResult, scan_mapping_for_sensitive_markers, scan_text_for_sensitive_markers
from .sensitivity import (
    SensitivityPoint,
    SensitivitySweepResult,
    sweep_aava,
    sweep_liability_cap,
    sweep_pass_through,
)
from .support_incidence import SupportIncidenceAssumption, SupportIncidenceResult, evaluate_support_incidence
from .subgroups import SubgroupAssignment, SubgroupDefinition, assign_subgroups
from .targeting import TargetPopulationInput, TargetPopulationResult, TargetingCriteria, evaluate_target_population
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
from .transition_funding import TransitionFundingInput, TransitionFundingResult, TransitionFundingYearResult, run_transition_funding
from .transition_payments import (
    TransitionPaymentDesign,
    TransitionPaymentInput,
    TransitionPaymentResult,
    evaluate_transition_payment,
)
from .transfer_baseline import ExistingTransferBaseline, TransferBaselineResult, evaluate_existing_transfer_baseline
from .transfer_runner import (
    TransferPricingPreviewReport,
    TransferPricingScenarioResult,
    run_transfer_pricing_previews,
)
from .transfer_pressure import TransferPressureInput, TransferPressureResult, evaluate_transfer_pressure
from .types import AIIWeights, CoverageResult, LevyParameters, LevyResult, QLCWeights, Worker
from .uncertainty_ranges import UncertaintyRange, UncertaintyRangeResult, evaluate_uncertainty_range
from .uncertainty_summary import UncertaintySummaryResult, summarise_uncertainty_results
from .weighted_distributional import (
    WeightedDistributionalInput,
    WeightedDistributionalResult,
    WeightedSubgroupResult,
    run_weighted_distributional_aggregation,
)
from .weighted_uncertainty import (
    WeightedSubgroupUncertaintyInput,
    WeightedSubgroupUncertaintyResult,
    evaluate_weighted_uncertainty,
)
from .workforce_displacement import (
    WorkforceTrajectoryInput,
    WorkforceTrajectoryResult,
    WorkforceYearResult,
    run_workforce_trajectory,
)

__all__ = [
    "AIIWeights",
    "AdjustedAAVAPreview",
    "AggregationResult",
    "AccessControlPolicy",
    "AdjustmentCandidate",
    "AdministrativeWorkflowResult",
    "AdministrativeWorkflowScenario",
    "AdministrativeWorkflowSummary",
    "ApportionmentActivity",
    "ApportionmentResult",
    "AvoidanceResult",
    "BehaviouralCountermeasure",
    "BehaviouralResponseResult",
    "BehaviouralResponseScenario",
    "BehaviouralResponseSummary",
    "BurdenBalanceInput",
    "BurdenBalanceResult",
    "CalibrationFieldRequirement",
    "CalibrationIntakeResult",
    "CalibrationIntakeSummary",
    "CalibrationRegistry",
    "CalibrationRequirement",
    "CoverageResult",
    "DataSourceCandidate",
    "DecisionLog",
    "DecisionLogEntry",
    "DistributionalScenarioInput",
    "DistributionalScenarioResult",
    "DistributionalSummaryResult",
    "EntityInput",
    "EvidenceAssessment",
    "EvidenceItem",
    "EvidencePacket",
    "EvidencePacketSummary",
    "EvidenceRequirement",
    "EvidenceRequestBundle",
    "ExampleResult",
    "ExampleRunnerError",
    "ExtractEvidenceMap",
    "FieldSanityCheck",
    "FieldSanityEvidenceMap",
    "FiscalSensitivityPoint",
    "FiscalSensitivityResult",
    "FiscalTrajectoryInput",
    "FiscalTrajectoryResult",
    "FiscalYearResult",
    "ForbiddenDataRule",
    "GroupedPreviewResult",
    "GroupingRiskResult",
    "HouseholdBudgetResult",
    "HouseholdCalibrationRequirement",
    "HouseholdCalibrationShellResult",
    "HouseholdUncertaintyInput",
    "HouseholdUncertaintyResult",
    "HouseholdWeight",
    "HouseholdWeightResult",
    "IncidenceAssumption",
    "IncidenceResult",
    "IngestionAuditRecord",
    "IngestionDecision",
    "IngestionPolicy",
    "IngestionRequest",
    "InvestmentGuardrailInput",
    "InvestmentGuardrailResult",
    "LevyParameters",
    "LevyResult",
    "LiabilityAdjustmentPreview",
    "MixedUnitExposureResult",
    "ModuleDataNeed",
    "ModuleSanityCheck",
    "ModuleSanityEvidenceMap",
    "PaymentInteractionInput",
    "PaymentInteractionResult",
    "PaymentPortfolioInput",
    "PaymentPortfolioResult",
    "PaymentSensitivityPoint",
    "PaymentSensitivityResult",
    "PaymentCliffInput",
    "PaymentCliffResult",
    "PaymentStackComponent",
    "PaymentStackResult",
    "PhaseRule",
    "PhaseRuleYearResult",
    "PlaceholderAnchorRecord",
    "PlaceholderEvidenceMap",
    "PublicAggregateExtract",
    "PublicDataBoundaryCheck",
    "PublicDataDigest",
    "PublicRevenueInput",
    "PublicRevenueResult",
    "PublicDataPilotCandidate",
    "PublicDataPilotResult",
    "PublicDataPilotSummary",
    "PublicDataSourceReference",
    "QLCWeights",
    "RelatedPartyTransaction",
    "RealisticPlaceholderSpec",
    "RestrictedBlockerEvidenceMap",
    "RedactionPlan",
    "ReemploymentPath",
    "ReemploymentResult",
    "RegionalStressInput",
    "RegionalStressResult",
    "RepoGuardrailPolicy",
    "RepoScanFinding",
    "RepoScanResult",
    "ReviewTransition",
    "ReviewWorkflowResult",
    "ReviewedScenarioInput",
    "ReviewedScenarioResult",
    "ReviewedScenarioSummary",
    "ReviewerEvidenceMapResult",
    "ReviewerEvidenceMapSummary",
    "ReviewerQuestion",
    "RetentionPolicy",
    "RestrictedDataRequirement",
    "SafeHarbourResult",
    "SectorStressInput",
    "SectorStressResult",
    "SectorStressSummary",
    "SensitiveScanResult",
    "SensitivityPoint",
    "SensitivitySweepResult",
    "SourceEvidenceMap",
    "SupportIncidenceAssumption",
    "SupportIncidenceResult",
    "SyntheticHousehold",
    "SubgroupAssignment",
    "SubgroupDefinition",
    "TargetPopulationInput",
    "TargetPopulationResult",
    "TargetingCriteria",
    "TransferPricingPreviewResult",
    "TransferPricingPreviewReport",
    "TransferPricingScenarioResult",
    "TransitionFundingInput",
    "TransitionFundingResult",
    "TransitionFundingYearResult",
    "TransitionPaymentDesign",
    "TransitionPaymentInput",
    "TransitionPaymentResult",
    "ExistingTransferBaseline",
    "TransferBaselineResult",
    "TransferPressureInput",
    "TransferPressureResult",
    "UnitCompatibilityResult",
    "UncertaintyRange",
    "UncertaintyRangeResult",
    "UncertaintySummaryResult",
    "WeightedDistributionalInput",
    "WeightedDistributionalResult",
    "WeightedSubgroupUncertaintyInput",
    "WeightedSubgroupUncertaintyResult",
    "WeightedSubgroupResult",
    "Worker",
    "WorkforceTrajectoryInput",
    "WorkforceTrajectoryResult",
    "WorkforceYearResult",
    "WorkflowEscalation",
    "WorkflowQueueAssignment",
    "add_decision_entry",
    "assess_evidence",
    "automation_equilibrium_levy",
    "automation_intensity_index",
    "automation_rent_levy",
    "australian_automated_value_added",
    "build_calibration_intake_result",
    "build_public_data_evidence_map_result",
    "build_public_data_pilot_result",
    "build_sector_stress_matrix",
    "calculate_liability",
    "cars_i",
    "classify_evidence_item",
    "classify_packet",
    "coverage_measures",
    "coverage_ratio",
    "create_decision_log",
    "create_ingestion_audit_record",
    "create_redaction_plan",
    "assign_subgroups",
    "evaluate_administrative_workflow",
    "evaluate_administrative_workflows",
    "evaluate_apportionment",
    "evaluate_avoidance_risk",
    "evaluate_behavioural_response",
    "evaluate_behavioural_responses",
    "evaluate_burden_balance",
    "evaluate_distributional_scenario",
    "evaluate_group_aggregation",
    "evaluate_grouping_risk",
    "evaluate_household_budget",
    "evaluate_household_uncertainty",
    "evaluate_household_weight",
    "evaluate_ingestion_request",
    "evaluate_investment_guardrail",
    "evaluate_mixed_unit_exposure",
    "evaluate_payment_interactions",
    "evaluate_payment_cliff",
    "evaluate_payment_portfolio",
    "evaluate_payment_stack",
    "evaluate_phase_rule",
    "evaluate_public_revenue",
    "evaluate_reemployment_path",
    "evaluate_regional_stress",
    "evaluate_review_transition",
    "review_scenario",
    "evaluate_safe_harbour",
    "evaluate_sector_stress",
    "evaluate_tax_incidence",
    "evaluate_target_population",
    "evaluate_transition_payment",
    "evaluate_existing_transfer_baseline",
    "evaluate_support_incidence",
    "evaluate_transfer_pressure",
    "evaluate_transfer_pricing_preview",
    "evaluate_uncertainty_range",
    "evaluate_unit_compatibility",
    "evaluate_weighted_uncertainty",
    "find_forbidden_affirmative_real_data_claims",
    "find_forbidden_affirmative_public_data_claims",
    "format_coverage_ratio",
    "get_access_control_policy",
    "get_calibration_registry",
    "get_default_evidence_requirements",
    "get_household_calibration_requirements",
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
    "run_fiscal_sensitivity",
    "run_fiscal_trajectory",
    "run_grouped_previews",
    "run_weighted_distributional_aggregation",
    "run_payment_sensitivity",
    "run_example",
    "run_transition_funding",
    "run_transfer_pricing_previews",
    "run_workforce_trajectory",
    "scan_mapping_for_sensitive_markers",
    "scan_file",
    "scan_repo",
    "scan_text_for_sensitive_markers",
    "summarise_decision_log",
    "summarise_distributional_scenarios",
    "summarise_evidence_packet",
    "summarise_reviewed_scenarios",
    "summarise_behavioural_responses",
    "summarise_administrative_workflows",
    "summarise_sector_stress",
    "summarise_uncertainty_results",
    "sweep_aava",
    "sweep_liability_cap",
    "sweep_pass_through",
    "validate_no_fake_calibration_values",
    "validate_administrative_workflow_scenario",
    "validate_administrative_workflow_scenarios",
    "validate_behavioural_response_scenario",
    "validate_behavioural_response_scenarios",
    "validate_evidence_packet",
]
