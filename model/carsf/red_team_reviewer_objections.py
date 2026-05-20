"""Red-team reviewer objections pack for the CARSF V1.5 public-data pilot.

This layer packages likely reviewer objections and honest project responses. It
does not load data, externally verify source values, complete calibration,
validate CARSF, determine tax payable, or modify firm-level CARSF liability.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

OBJECTION_STATUS_VALUES = {
    "acknowledged",
    "partially_mitigated",
    "unresolved",
    "blocked_by_restricted_data",
    "requires_external_review",
    "requires_legal_review",
    "requires_economic_review",
    "requires_statistical_review",
    "cannot_be_resolved_inside_repo",
}

SEVERITY_VALUES = {"critical", "high", "medium", "low", "informational"}

OBJECTION_CATEGORY_VALUES = {
    "public_data_limitations",
    "placeholder_limitations",
    "source_reference_limitations",
    "restricted_data_blockers",
    "calibration_limitations",
    "statistical_limitations",
    "legal_and_tax_limitations",
    "economic_incidence_limitations",
    "administrative_feasibility_limitations",
    "dashboard_interpretation_risk",
    "non_claim_boundary_risk",
    "external_review_required",
    "reviewer_misinterpretation_risk",
}

RED_TEAM_REVIEWER_OBJECTIONS_WARNING = (
    "This is a red-team reviewer objections pack only. No new data is loaded by this build. "
    "This does not externally verify source values, does not scrape public sources, and does not call external APIs. "
    "Objections being acknowledged does not mean they are resolved. Partially mitigated does not mean solved. "
    "This is not calibration; calibration has not been completed. Public data does not prove the model works. "
    "Realistic placeholders remain placeholders, realistic placeholders are not real data, realistic placeholders are "
    "not calibrated, source references are not loaded datasets, and restricted-data requirements are not data access. "
    "This is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic "
    "validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, "
    "and not official status. It does not determine actual tax payable, does not use taxpayer-level data, firm-level "
    "confidential data, household microdata, ABS DataLab, HILDA microdata, DSS/Services Australia records, ATO taxpayer "
    "records, Treasury/PBO confidential material, or restricted government data, and does not modify firm-level CARSF "
    "liability. It only packages likely reviewer objections and honest responses."
)

RED_TEAM_REVIEWER_OBJECTIONS_NON_CLAIMS = [
    RED_TEAM_REVIEWER_OBJECTIONS_WARNING,
    "This pack acknowledges weaknesses and does not claim objections are resolved.",
    "Every response is an objection-handling note only, not a defence brief, validation result, approval, or calibration.",
    "The pack adds no public values and uses only existing Build 26-29.5 artefacts.",
]

FORBIDDEN_AFFIRMATIVE_RED_TEAM_CLAIMS = [
    "calibrated",
    "calibration completed",
    "real calibration",
    "public data proves",
    "model works",
    "tax model works",
    "carsf works",
    "ready for government",
    "ready for ato",
    "ready for treasury",
    "ready for parliament",
    "ready for implementation",
    "ready for public release",
    "operationally ready",
    "legally sufficient",
    "official status",
    "official policy",
    "validated",
    "externally validated",
    "source verified",
    "externally verified",
    "treasury validated",
    "ato validated",
    "pbo validated",
    "economic validation complete",
    "welfare validation complete",
    "statistical validation complete",
    "actual tax payable",
    "real household estimate",
    "population estimate",
    "official sector ranking",
    "compliance score",
    "readiness score",
    "maturity score",
    "approved",
    "objections resolved",
    "all objections resolved",
    "no material limitations",
]

REQUIRED_FALSE_FLAGS = [
    "new_data_loaded",
    "external_source_verification_claimed",
    "real_calibration_completed",
    "actual_tax_payable_determined",
    "validation_claimed",
    "approval_claimed",
    "operational_readiness_claimed",
    "legal_sufficiency_claimed",
    "official_status_claimed",
    "firm_level_liability_logic_modified",
]

BASE_MUST_NOT_CLAIM = [
    "not_calibration_completed",
    "not_external_source_verification",
    "not_validation",
    "not_approval",
    "not_actual_tax_payable",
    "not_legal_sufficiency",
    "not_operational_readiness",
    "not_official_status",
    "not_firm_level_liability_change",
]


@dataclass(frozen=True)
class ReviewerObjection:
    objection_id: str
    objection_title: str
    objection_category: str
    severity: str
    affected_artifacts: list[str]
    reviewer_concern: str
    why_the_concern_is_valid: str
    current_project_response: str
    what_the_project_can_say: list[str]
    what_the_project_must_not_claim: list[str]
    unresolved_blockers: list[str]
    evidence_needed_to_resolve: list[str]
    future_build_route: list[str]
    status: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReviewerObjectionResponse:
    objection_id: str
    current_project_response: str
    can_say: list[str]
    must_not_claim: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ObjectionCategorySummary:
    objection_category: str
    count: int

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ObjectionSeveritySummary:
    severity: str
    count: int

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class UnresolvedBlockerSummary:
    blocker: str
    affected_objection_ids: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FutureEvidenceNeed:
    evidence_need: str
    affected_objection_ids: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RedTeamReviewerObjectionsSummary:
    total_objections: int
    critical_objections: int
    high_objections: int
    medium_objections: int
    low_objections: int
    informational_objections: int
    acknowledged_objections: int
    partially_mitigated_objections: int
    unresolved_objections: int
    blocked_by_restricted_data_objections: int
    external_review_required_objections: int
    legal_review_required_objections: int
    economic_review_required_objections: int
    statistical_review_required_objections: int
    cannot_be_resolved_inside_repo_objections: int
    total_categories: int
    categories_covered: int
    unresolved_blockers_total: int
    future_evidence_needs_total: int
    forbidden_claim_findings: int
    red_team_pack_created: bool
    new_data_loaded: bool
    external_source_verification_claimed: bool
    objections_acknowledged: bool
    unresolved_blockers_visible: bool
    calibration_limitations_visible: bool
    legal_limitations_visible: bool
    statistical_limitations_visible: bool
    dashboard_misinterpretation_risks_visible: bool
    real_calibration_completed: bool
    actual_tax_payable_determined: bool
    validation_claimed: bool
    approval_claimed: bool
    operational_readiness_claimed: bool
    legal_sufficiency_claimed: bool
    official_status_claimed: bool
    firm_level_liability_logic_modified: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RedTeamReviewerObjectionsResult:
    pack_id: str
    pack_name: str
    status: str
    non_claims: list[str]
    input_artifacts: list[str]
    objections: list[ReviewerObjection]
    responses: list[ReviewerObjectionResponse]
    category_summaries: list[ObjectionCategorySummary]
    severity_summaries: list[ObjectionSeveritySummary]
    unresolved_blockers: list[UnresolvedBlockerSummary]
    future_evidence_needs: list[FutureEvidenceNeed]
    forbidden_claims: list[str]
    build_30_requirements: list[str]
    summary: RedTeamReviewerObjectionsSummary

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _obj(
    objection_id: str,
    title: str,
    category: str,
    severity: str,
    status: str,
    artifacts: list[str],
    concern: str,
    valid_reason: str,
    response: str,
    can_say: list[str],
    blockers: list[str],
    evidence: list[str],
    route: list[str],
    extra_must_not_claim: list[str] | None = None,
) -> ReviewerObjection:
    return ReviewerObjection(
        objection_id=objection_id,
        objection_title=title,
        objection_category=category,
        severity=severity,
        affected_artifacts=artifacts,
        reviewer_concern=concern,
        why_the_concern_is_valid=valid_reason,
        current_project_response=response,
        what_the_project_can_say=can_say,
        what_the_project_must_not_claim=sorted(set(BASE_MUST_NOT_CLAIM + (extra_must_not_claim or []))),
        unresolved_blockers=blockers,
        evidence_needed_to_resolve=evidence,
        future_build_route=route,
        status=status,
    )


PUBLIC_DATA_ARTIFACTS = [
    "reports/public_data_pilot.json",
    "reports/public_data_evidence_map.json",
    "reports/public_data_consistency_audit.json",
    "reports/source_locator_verification_pack.json",
]

PLACEHOLDER_ARTIFACTS = [
    "data/public_pilot/placeholders/realistic_placeholder_anchors.yaml",
    "reports/public_data_pilot.json",
    "reports/public_data_evidence_map.json",
]

LEGAL_TAX_ARTIFACTS = [
    "reports/legislative_architecture.json",
    "reports/administrative_compliance_workflow.json",
    "reports/public_data_pilot.json",
]


DEFAULT_OBJECTIONS = [
    _obj(
        "obj_001_small_public_extract_set",
        "Only a small number of public aggregate extracts are loaded",
        "public_data_limitations",
        "high",
        "partially_mitigated",
        PUBLIC_DATA_ARTIFACTS,
        "A reviewer may argue that five loaded public extracts are too small to support broad CARSF interpretation.",
        "The concern is valid because the pilot is intentionally narrow and cannot represent the full labour, tax, fiscal, household, or sector data environment.",
        "The project labels the pilot as a small public aggregate-data pilot and keeps counts visible.",
        ["The repo can say a small set of public aggregate records is present for reviewer inspection only."],
        ["small_public_extract_set", "no_full_public_dataset_load", "restricted_data_required_for_calibration"],
        ["larger public aggregate catalogue", "external review of source coverage", "future source selection protocol"],
        ["Build 30 reviewer handoff", "future public-data expansion build"],
    ),
    _obj(
        "obj_002_public_extracts_not_calibration",
        "Public aggregate extracts are not enough to calibrate CARSF",
        "calibration_limitations",
        "critical",
        "unresolved",
        PUBLIC_DATA_ARTIFACTS,
        "A reviewer may object that aggregate public records cannot calibrate firm-level, behavioural, fiscal, or household interactions.",
        "The concern is valid because public aggregates do not contain the restricted, entity-level, or household-level detail needed for calibration using real data.",
        "The project keeps real_calibration_completed false and describes the pilot as sanity-check-only or placeholder-anchor-only.",
        ["The repo can say public aggregates may support limited sanity checks and placeholder transparency."],
        ["restricted_data_required", "no_calibration_method_review", "no_microdata"],
        ["authorised restricted data access", "statistical methods review", "calibration protocol"],
        ["Build 30 handoff", "external statistical review", "future authorised data process"],
    ),
    _obj(
        "obj_003_minimum_wage_not_labour_costs",
        "Fair Work minimum wage is not representative of all labour costs",
        "public_data_limitations",
        "high",
        "partially_mitigated",
        ["reports/public_data_pilot.json", "reports/source_locator_verification_pack.json"],
        "A reviewer may object that the national minimum wage cannot stand in for sector labour costs, overheads, or total employment cost.",
        "The concern is valid because minimum wage is only one public wage anchor and does not represent all occupations, sectors, loadings, hours, or on-costs.",
        "The project uses the value only as a placeholder anchor and arithmetic-check card, not as a labour-cost calibration.",
        ["The repo can say the Fair Work value is a public wage anchor with an internal arithmetic check."],
        ["minimum_wage_not_representative", "sector_wage_data_missing", "on_costs_not_modelled"],
        ["sector wage aggregates", "award and occupation review", "labour-cost methods review"],
        ["Build 30 handoff", "future labour anchor expansion"],
    ),
    _obj(
        "obj_004_ato_transparency_not_liability",
        "ATO corporate tax transparency data cannot infer CARSF firm liability",
        "public_data_limitations",
        "critical",
        "requires_legal_review",
        PUBLIC_DATA_ARTIFACTS,
        "A reviewer may argue that public ATO transparency records cannot infer CARSF liability for any firm.",
        "The concern is valid because public transparency data is aggregate/contextual and CARSF liability would require legal, tax, and entity-specific analysis that is absent.",
        "The project states the extract is context only and must not be used for firm-level CARSF liability.",
        ["The repo can say public ATO records are source-locator context only."],
        ["no_firm_level_confidential_data", "no_tax_base_review", "no_liability_logic_change"],
        ["tax law review", "legal drafting review", "authorised data governance"],
        ["external tax review", "external legal review"],
        ["not_firm_liability_estimate"],
    ),
    _obj(
        "obj_005_ato_statistics_not_ai_displacement",
        "ATO taxation statistics cannot prove AI-related revenue displacement",
        "public_data_limitations",
        "high",
        "requires_statistical_review",
        PUBLIC_DATA_ARTIFACTS,
        "A reviewer may object that aggregate tax statistics cannot isolate AI-related revenue or labour displacement.",
        "The concern is valid because the public statistics do not identify AI adoption, counterfactual employment, or causal displacement channels.",
        "The project treats these records as source-locator context and not as displacement evidence.",
        ["The repo can say aggregate tax statistics are not AI displacement evidence."],
        ["no_ai_adoption_dataset", "no_counterfactual_model", "no_causal_design"],
        ["AI adoption measures", "causal identification design", "statistical methods review"],
        ["external statistical review", "future methods build"],
    ),
    _obj(
        "obj_006_budget_aggregates_not_fiscal_impact",
        "Budget Paper aggregates cannot prove CARSF fiscal impact",
        "public_data_limitations",
        "critical",
        "requires_economic_review",
        ["reports/public_data_pilot.json", "reports/public_data_consistency_audit.json", "reports/source_locator_verification_pack.json"],
        "A reviewer may object that Budget Paper aggregates are not evidence of CARSF revenue, cost, or fiscal sufficiency.",
        "The concern is valid because public fiscal aggregates do not model CARSF tax bases, behavioural change, implementation costs, or transfer interactions.",
        "The project labels Budget data as fiscal context only and not Treasury modelling.",
        ["The repo can say a public fiscal source locator is recorded for context."],
        ["no_revenue_model_validation", "no_treasury_costing", "no_behavioural_fiscal_integration"],
        ["Treasury methods review", "fiscal modelling review", "implementation-cost evidence"],
        ["external Treasury methods review", "Build 30 handoff"],
        ["not_treasury_modelling"],
    ),
    _obj(
        "obj_007_super_settings_not_employer_behaviour",
        "Super guarantee settings do not model real employer contribution behaviour",
        "public_data_limitations",
        "medium",
        "partially_mitigated",
        PUBLIC_DATA_ARTIFACTS,
        "A reviewer may object that a statutory rate does not model actual contribution behaviour, compliance, wage offsets, or labour market responses.",
        "The concern is valid because a public setting is not an empirical behavioural model.",
        "The project uses the setting as a public threshold anchor only.",
        ["The repo can say the public setting is an anchor for reviewer inspection only."],
        ["no_employer_behaviour_data", "no_wage_offset_estimate", "no_compliance_data"],
        ["labour economics review", "payroll and super contribution evidence", "external methods review"],
        ["future incidence review", "Build 30 handoff"],
        ["not_ato_guidance"],
    ),
    _obj(
        "obj_008_help_thresholds_not_household_pressure",
        "HELP / HECS thresholds do not model real household repayment pressure",
        "public_data_limitations",
        "medium",
        "unresolved",
        PUBLIC_DATA_ARTIFACTS,
        "A reviewer may object that public thresholds cannot model household repayment pressure or eligibility interactions.",
        "The concern is valid because individual incomes, debts, repayment histories, and household circumstances are not loaded.",
        "The project marks the HELP/HECS row as source-reference-only unless exact public values are loaded by a later build.",
        ["The repo can say HELP/HECS is a source reference or placeholder anchor only."],
        ["no_household_microdata", "no_individual_debt_data", "source_reference_only"],
        ["public threshold extract review", "household microdata governance", "welfare policy review"],
        ["future public-data pilot expansion", "external welfare review"],
    ),
    _obj(
        "obj_009_payroll_tax_state_variation",
        "Payroll tax thresholds vary by state and do not establish national incidence",
        "public_data_limitations",
        "medium",
        "unresolved",
        PUBLIC_DATA_ARTIFACTS,
        "A reviewer may object that a payroll-tax source reference cannot support national incidence claims.",
        "The concern is valid because state payroll-tax thresholds, exemptions, and bases differ and no employer-level payroll data is loaded.",
        "The project keeps payroll tax as source-reference-only or placeholder-anchor-only.",
        ["The repo can say state payroll-tax references identify future review needs only."],
        ["state_variation", "no_employer_payroll_data", "no_incidence_estimate"],
        ["state-by-state public threshold map", "employer payroll evidence governance", "economic incidence review"],
        ["future public threshold build", "external economic review"],
    ),
    _obj(
        "obj_010_source_reference_only_not_loaded",
        "Source-reference-only records are not loaded public data",
        "source_reference_limitations",
        "high",
        "partially_mitigated",
        ["reports/public_data_evidence_map.json", "reports/source_locator_verification_pack.json"],
        "A reviewer may object that source-reference-only rows could be mistaken for loaded data.",
        "The concern is valid because source references still have URLs and can look evidentiary in dashboards.",
        "The project separates source-reference-only rows and excludes them from loaded public data counts.",
        ["The repo can say source-reference-only rows are not loaded public data."],
        ["no_value_loaded", "future_extract_required", "dashboard_interpretation_risk"],
        ["manual review of dashboard labels", "source-reference-only count audit", "future exact extract protocol"],
        ["Build 30 handoff", "external reviewer checklist"],
    ),
    _obj(
        "obj_011_placeholders_remain_placeholders",
        "Realistic placeholders remain placeholders",
        "placeholder_limitations",
        "critical",
        "partially_mitigated",
        PLACEHOLDER_ARTIFACTS,
        "A reviewer may object that realistic placeholders could be overread as real data.",
        "The concern is valid because public anchors can make placeholders appear more empirical than they are.",
        "The project labels placeholders as realistic_placeholder and not real data.",
        ["The repo can say placeholders are transparently labelled and remain non-calibrated."],
        ["placeholder_not_replaced", "restricted_data_missing", "external_review_required"],
        ["replacement criteria", "authorised data access", "methods review"],
        ["Build 30 handoff", "future calibration governance"],
    ),
    _obj(
        "obj_012_placeholder_anchors_not_calibration",
        "Placeholder anchors do not equal calibration",
        "placeholder_limitations",
        "critical",
        "unresolved",
        PLACEHOLDER_ARTIFACTS,
        "A reviewer may object that anchoring a placeholder to a public category is still not calibration.",
        "The concern is valid because calibration requires a method, target variable, data quality review, and external scrutiny that are absent.",
        "The project keeps real_calibration_completed false and states anchor-only status.",
        ["The repo can say anchors clarify provenance but do not complete calibration."],
        ["no_calibration_target", "no_estimation_method", "no_external_review"],
        ["calibration method design", "reviewed target data", "external statistical review"],
        ["future calibration design build", "external methods review"],
    ),
    _obj(
        "obj_013_public_anchors_not_validated",
        "Public anchors can make placeholders more transparent but not validated",
        "placeholder_limitations",
        "high",
        "requires_external_review",
        PLACEHOLDER_ARTIFACTS,
        "A reviewer may object that transparency is useful but does not establish validity.",
        "The concern is valid because a clear anchor can still be the wrong anchor for CARSF purposes.",
        "The project describes anchors as provenance aids and keeps validation_claimed false.",
        ["The repo can say public anchors improve inspectability."],
        ["anchor_relevance_unreviewed", "validation_absent", "restricted_data_missing"],
        ["anchor relevance review", "domain expert review", "statistical methods review"],
        ["Build 30 reviewer handoff", "external review"],
    ),
    _obj(
        "obj_014_household_scenarios_synthetic",
        "Household distributional scenarios remain synthetic",
        "placeholder_limitations",
        "high",
        "blocked_by_restricted_data",
        ["reports/distributional_scenarios.json", "reports/public_data_evidence_map.json"],
        "A reviewer may object that household scenarios cannot be interpreted as real household estimates.",
        "The concern is valid because no household microdata, Census microdata, HILDA, or DSS records are used.",
        "The project keeps household scenarios synthetic and warns against population-level estimate overread.",
        ["The repo can say household examples are synthetic-only."],
        ["no_household_microdata", "no_population_weights", "no_welfare_records"],
        ["authorised household microdata process", "welfare policy review", "statistical representativeness review"],
        ["external welfare review", "future authorised data process"],
        ["not_population_estimate"],
    ),
    _obj(
        "obj_015_weighted_subgroups_nonrepresentative",
        "Weighted subgroup outputs remain non-representative",
        "statistical_limitations",
        "high",
        "requires_statistical_review",
        ["reports/household_weighting.json", "reports/public_data_evidence_map.json"],
        "A reviewer may object that subgroup weights are not population-representative.",
        "The concern is valid because representative survey design, weights, and validation are absent.",
        "The project labels weighting as prototype-only and not population inference.",
        ["The repo can say weighting controls are display controls only."],
        ["no_survey_weight_design", "no_population_frame", "no_statistical_validation"],
        ["statistical weighting review", "survey design evidence", "representativeness assessment"],
        ["external statistical review"],
        ["not_population_estimate"],
    ),
    _obj(
        "obj_016_no_taxpayer_ato_data",
        "No taxpayer-level ATO data is used",
        "restricted_data_blockers",
        "critical",
        "blocked_by_restricted_data",
        PUBLIC_DATA_ARTIFACTS,
        "A reviewer may object that no taxpayer-level ATO data means CARSF cannot be calibrated or operationalised.",
        "The concern is valid because taxpayer-level data is necessary for many real tax-base and compliance questions and cannot be stored in this repo.",
        "The project explicitly forbids taxpayer-level ATO data in the repository.",
        ["The repo can say taxpayer data is not loaded and remains forbidden for repo use."],
        ["taxpayer_data_forbidden", "authorised_access_required", "privacy_and_secrecy_review_required"],
        ["ATO and legal access process", "privacy/secrecy review", "secure external environment"],
        ["external legal and ATO-methods review"],
    ),
    _obj(
        "obj_017_no_firm_confidential_data",
        "No firm-level confidential data is used",
        "restricted_data_blockers",
        "critical",
        "blocked_by_restricted_data",
        PUBLIC_DATA_ARTIFACTS,
        "A reviewer may object that no firm-confidential data means firm-level liability and attribution cannot be tested.",
        "The concern is valid because entity attribution, transfer pricing, and firm-level CARSF exposure require confidential or authorised data not present here.",
        "The project forbids firm-confidential records and does not modify firm-level liability logic.",
        ["The repo can say no firm-confidential data is present."],
        ["firm_confidential_data_forbidden", "no_entity_attribution_evidence", "no_liability_estimate"],
        ["authorised secure environment", "tax and legal review", "confidential data governance"],
        ["external tax review", "future authorised data process"],
    ),
    _obj(
        "obj_018_no_dss_services_records",
        "No DSS / Services Australia records are used",
        "restricted_data_blockers",
        "high",
        "blocked_by_restricted_data",
        ["reports/payment_interactions.json", "reports/public_data_evidence_map.json"],
        "A reviewer may object that payment interaction analysis cannot be grounded without administrative welfare records.",
        "The concern is valid because real eligibility, payment histories, and cliffs require restricted records and legal authority.",
        "The project treats welfare interactions as placeholder-only and blocked by restricted data.",
        ["The repo can say DSS and Services Australia records are not loaded."],
        ["no_welfare_records", "eligibility_law_review_required", "restricted_access_required"],
        ["welfare policy review", "privacy/secrecy review", "authorised secure data process"],
        ["external welfare review"],
    ),
    _obj(
        "obj_019_no_licensed_longitudinal_microdata",
        "No HILDA microdata is used",
        "restricted_data_blockers",
        "medium",
        "blocked_by_restricted_data",
        ["reports/household_weighting.json", "reports/distributional_scenarios.json"],
        "A reviewer may object that HILDA-style longitudinal household patterns are absent.",
        "The concern is valid because HILDA microdata is licensed and cannot be treated as repo data.",
        "The project forbids HILDA microdata in the repo and keeps household outputs synthetic.",
        ["The repo can say no HILDA microdata is loaded."],
        ["hilda_not_loaded", "licensed_microdata_forbidden", "no_longitudinal_household_evidence"],
        ["licensed access process", "statistical methods review", "privacy review"],
        ["future authorised microdata review"],
    ),
    _obj(
        "obj_020_no_abs_restricted_lab_microdata",
        "No ABS DataLab microdata is used",
        "restricted_data_blockers",
        "high",
        "blocked_by_restricted_data",
        PUBLIC_DATA_ARTIFACTS,
        "A reviewer may object that ABS public aggregates cannot substitute for DataLab microdata.",
        "The concern is valid because DataLab microdata has access, confidentiality, and output-checking constraints absent from this repo.",
        "The project forbids DataLab microdata and uses only safe public aggregate/source-reference records.",
        ["The repo can say ABS DataLab microdata is not present."],
        ["abs_restricted_lab_microdata_forbidden", "no_microdata_output_clearance", "no_population_estimate"],
        ["ABS access process", "output checking", "statistical methods review"],
        ["future authorised ABS process"],
    ),
    _obj(
        "obj_021_restricted_blockers_prevent_calibration",
        "Restricted-data blockers prevent calibration using real data",
        "restricted_data_blockers",
        "critical",
        "blocked_by_restricted_data",
        ["reports/real_data_feasibility.json", "reports/public_data_consistency_audit.json"],
        "A reviewer may object that blockers mean the prototype cannot progress to calibration using real data inside the repo.",
        "The concern is valid because required restricted data categories are explicitly outside repo scope.",
        "The project preserves blockers and does not hide them behind public-data pilot outputs.",
        ["The repo can say calibration remains blocked without authorised external access."],
        ["restricted_data_missing", "secure_environment_required", "external_review_required"],
        ["data access governance", "secure environment design", "external legal/privacy/statistical review"],
        ["Build 30 handoff", "external access planning"],
    ),
    _obj(
        "obj_022_sanity_check_only",
        "Public-data pilot is sanity-check-only",
        "calibration_limitations",
        "critical",
        "partially_mitigated",
        PUBLIC_DATA_ARTIFACTS,
        "A reviewer may object that sanity checks can be overstated as calibration.",
        "The concern is valid because sanity-check language can still be overread if output tables look formal.",
        "The project uses explicit claim-level labels and false flags.",
        ["The repo can say the pilot supports sanity-check-only and placeholder-anchor-only inspection."],
        ["claim_level_overread", "no_calibration_protocol", "dashboard_interpretation_risk"],
        ["reviewer-facing handoff notes", "external review of labels", "calibration protocol"],
        ["Build 30 handoff"],
    ),
    _obj(
        "obj_023_no_statistical_inference",
        "No statistical inference is performed",
        "statistical_limitations",
        "high",
        "requires_statistical_review",
        ["reports/public_data_pilot.json", "reports/uncertainty_ranges.json"],
        "A reviewer may object that no inference, estimation, or hypothesis testing occurs.",
        "The concern is valid because the current public pilot carries source records and checks, not statistical analysis.",
        "The project keeps statistical_validation_claimed false and avoids population-level inference.",
        ["The repo can say no statistical inference is performed."],
        ["no_estimator", "no_sampling_frame", "no_uncertainty_model"],
        ["statistical methods design", "sampling and weighting review", "external statistical review"],
        ["external statistical review"],
    ),
    _obj(
        "obj_024_no_confidence_intervals",
        "No confidence intervals or real uncertainty quantification are produced",
        "statistical_limitations",
        "high",
        "requires_statistical_review",
        ["reports/uncertainty_ranges.json", "reports/public_data_evidence_map.json"],
        "A reviewer may object that uncertainty ranges are deterministic placeholders and not confidence intervals.",
        "The concern is valid because uncertainty labels can be confused with statistical intervals.",
        "The project states no confidence intervals or population-level estimates are created.",
        ["The repo can say uncertainty outputs are placeholder ranges only."],
        ["no_sampling_distribution", "no_estimation_error", "no_confidence_interval_method"],
        ["uncertainty methodology", "statistical peer review", "calibration data"],
        ["future statistical methods build"],
        ["not_confidence_interval"],
    ),
    _obj(
        "obj_025_no_behavioural_elasticity",
        "No behavioural elasticity is estimated",
        "economic_incidence_limitations",
        "high",
        "requires_economic_review",
        ["reports/behavioural_response_simulation.json", "reports/public_data_pilot.json"],
        "A reviewer may object that behavioural responses are not empirically estimated.",
        "The concern is valid because no observed behavioural data or econometric design is present.",
        "The project labels behavioural outputs as simulation/prototype only.",
        ["The repo can say behavioural response material is not an elasticity estimate."],
        ["no_observed_behavioural_data", "no_elasticity_estimation", "no_econometric_review"],
        ["behavioural economics review", "observed response data", "econometric methods design"],
        ["external economic review"],
    ),
    _obj(
        "obj_026_no_causal_relationship",
        "No causal relationship is established",
        "statistical_limitations",
        "critical",
        "requires_statistical_review",
        PUBLIC_DATA_ARTIFACTS,
        "A reviewer may object that the public pilot cannot establish causality.",
        "The concern is valid because no causal design, counterfactual, or identification strategy is included.",
        "The project avoids causal claims and keeps outputs as inspection aids.",
        ["The repo can say no causal relationship is established."],
        ["no_identification_strategy", "no_counterfactual", "no_causal_evidence"],
        ["causal design", "reviewed data access", "statistical/economic methods review"],
        ["external statistical and economic review"],
    ),
    _obj(
        "obj_027_no_external_validation",
        "No external validation has occurred",
        "external_review_required",
        "critical",
        "requires_external_review",
        PUBLIC_DATA_ARTIFACTS,
        "A reviewer may object that internal checks are not external validation.",
        "The concern is valid because internal reconciliation, arithmetic checks, and source-locator cards do not substitute for independent review.",
        "The project keeps validation_claimed false and frames outputs as reviewer materials.",
        ["The repo can say external validation has not occurred."],
        ["external_review_not_completed", "independent_validation_absent", "source_values_not_externally_checked"],
        ["independent reviewer process", "documented review findings", "issue resolution log"],
        ["Build 30 handoff", "external review process"],
    ),
    _obj(
        "obj_028_legislative_architecture_non_operative",
        "Legislative architecture is non-operative",
        "legal_and_tax_limitations",
        "critical",
        "requires_legal_review",
        LEGAL_TAX_ARTIFACTS,
        "A reviewer may object that legislative architecture headings are not law.",
        "The concern is valid because no Parliamentary Counsel drafting, enactment, definitions, rights, obligations, or operative provisions exist.",
        "The project labels legislative architecture as a skeleton and non-operative.",
        ["The repo can say legislative material is a non-operative architecture sketch."],
        ["no_operative_law", "no_parliamentary_counsel_review", "legal_sufficiency_absent"],
        ["Parliamentary Counsel review", "legal policy instructions", "statutory drafting process"],
        ["external legal review", "Parliamentary Counsel review"],
        ["not_operative_law"],
    ),
    _obj(
        "obj_029_admin_workflow_not_ato_guidance",
        "Administrative workflow is not ATO guidance",
        "administrative_feasibility_limitations",
        "critical",
        "requires_external_review",
        ["reports/administrative_compliance_workflow.json", "reports/public_data_evidence_map.json"],
        "A reviewer may object that workflow diagrams could be mistaken for ATO process or guidance.",
        "The concern is valid because administrative labels can imply operational authority if not bounded.",
        "The project states administrative workflow is non-operative and not ATO guidance.",
        ["The repo can say workflow material is a prototype shell only."],
        ["no_ato_review", "no_operational_authority", "no_notice_or_enforcement_power"],
        ["ATO methods review", "administrative law review", "operational feasibility review"],
        ["external ATO methods review"],
        ["not_ato_guidance"],
    ),
    _obj(
        "obj_030_no_legal_sufficiency_review",
        "No legal sufficiency review has occurred",
        "legal_and_tax_limitations",
        "critical",
        "requires_legal_review",
        LEGAL_TAX_ARTIFACTS,
        "A reviewer may object that legal sufficiency has not been assessed.",
        "The concern is valid because no legal advice, tax advice, constitutional review, administrative-law review, or Parliamentary Counsel review has occurred.",
        "The project keeps legal_sufficiency_claimed false.",
        ["The repo can say legal review remains required."],
        ["legal_review_absent", "tax_review_absent", "parliamentary_counsel_review_absent"],
        ["legal review", "tax review", "Parliamentary Counsel review"],
        ["external legal and tax review"],
    ),
    _obj(
        "obj_031_no_tax_payable_determination",
        "No tax-payable determination can be made",
        "legal_and_tax_limitations",
        "critical",
        "requires_legal_review",
        LEGAL_TAX_ARTIFACTS,
        "A reviewer may object that outputs might be mistaken for tax payable.",
        "The concern is valid because examples and reports can look numerical, but no operative law or real data exists.",
        "The project keeps actual_tax_payable_determined false and preserves non-claim warnings.",
        ["The repo can say no actual tax payable is determined."],
        ["no_operative_law", "no_taxpayer_data", "no_firm_liability_logic_change"],
        ["tax law review", "legal authority", "authorised data process"],
        ["external legal and tax review"],
    ),
    _obj(
        "obj_032_anti_avoidance_drafting_review",
        "Anti-avoidance and attribution rules require legal drafting review",
        "legal_and_tax_limitations",
        "high",
        "requires_legal_review",
        ["reports/legislative_architecture.json", "reports/transfer_pricing_results.json"],
        "A reviewer may object that anti-avoidance and attribution concepts are placeholder-only until legally drafted.",
        "The concern is valid because attribution, transfer pricing, and avoidance provisions are legal constructs requiring precise drafting and safeguards.",
        "The project treats these as prototype concepts and not operative law.",
        ["The repo can say legal drafting review is required before any operative interpretation."],
        ["no_legal_drafting", "no_tax_base_definition", "review_rights_placeholder"],
        ["legal drafting instructions", "tax review", "Parliamentary Counsel review"],
        ["external legal and tax review"],
        ["not_operative_law"],
    ),
    _obj(
        "obj_033_economic_incidence_not_proven",
        "Economic incidence is not proven",
        "economic_incidence_limitations",
        "critical",
        "requires_economic_review",
        ["reports/investment_guardrails.json", "reports/public_data_pilot.json"],
        "A reviewer may object that incidence is asserted structurally but not proven empirically.",
        "The concern is valid because no observed incidence data, pass-through model, or external economic review is included.",
        "The project labels incidence material as guardrails and limitations, not validation.",
        ["The repo can say economic incidence remains an unresolved review issue."],
        ["no_incidence_estimate", "no_pass_through_data", "no_economic_review"],
        ["economic incidence study", "public and restricted data review", "external economic methods review"],
        ["external economic review"],
    ),
    _obj(
        "obj_034_pass_through_not_estimated",
        "Employer pass-through behaviour is not estimated",
        "economic_incidence_limitations",
        "high",
        "requires_economic_review",
        ["reports/behavioural_response_simulation.json", "reports/investment_guardrails.json"],
        "A reviewer may object that employer pass-through behaviour is not empirically estimated.",
        "The concern is valid because prices, wages, investment, and employment channels require data and modelling not present here.",
        "The project keeps pass-through assumptions as placeholders or guardrails.",
        ["The repo can say pass-through is not estimated."],
        ["no_pass_through_estimate", "no_firm_behaviour_data", "no_market_model"],
        ["economic methods review", "firm behaviour data", "incidence modelling"],
        ["external economic review"],
    ),
    _obj(
        "obj_035_labour_displacement_not_calibrated",
        "Labour displacement assumptions are not calibrated",
        "economic_incidence_limitations",
        "critical",
        "unresolved",
        ["reports/behavioural_response_simulation.json", "reports/public_data_pilot.json"],
        "A reviewer may object that labour displacement assumptions are central but not calibrated.",
        "The concern is valid because the public pilot does not observe displacement or substitution pathways.",
        "The project labels displacement assumptions as calibration blockers.",
        ["The repo can say displacement assumptions remain unresolved."],
        ["no_displacement_dataset", "no_sector_substitution_measure", "no_behavioural_calibration"],
        ["labour displacement data", "sector review", "economic/statistical review"],
        ["future calibration planning", "external review"],
    ),
    _obj(
        "obj_036_fiscal_sufficiency_not_proven",
        "Revenue neutrality or fiscal sufficiency is not proven",
        "economic_incidence_limitations",
        "critical",
        "requires_economic_review",
        ["reports/fiscal_trajectory.json", "reports/transition_funding.json", "reports/public_data_pilot.json"],
        "A reviewer may object that fiscal trajectory outputs could be overread as sufficiency analysis.",
        "The concern is valid because no real revenue model, costing, or Treasury/PBO review exists.",
        "The project labels fiscal material as prototype-only and not Treasury modelling or PBO costing.",
        ["The repo can say fiscal sufficiency is not proven."],
        ["no_real_revenue_model", "no_costing_review", "no_transition_cost_evidence"],
        ["Treasury methods review", "PBO-style costing process", "implementation-cost evidence"],
        ["external Treasury methods review"],
        ["not_treasury_modelling", "not_pbo_costing"],
    ),
    _obj(
        "obj_037_dashboard_cards_mistaken_validation",
        "Dashboard cards may be mistaken for validation",
        "dashboard_interpretation_risk",
        "high",
        "partially_mitigated",
        ["simulator/pages/29_Public_Data_Evidence_Map.py", "reports/public_data_evidence_map.json"],
        "A reviewer may object that dashboard cards and tables make outputs look more settled than they are.",
        "The concern is valid because UI summaries can be overread even when warnings are present.",
        "The project uses explicit warning text and avoids readiness, calibration, and validation scores.",
        ["The repo can say dashboard content is reviewer navigation only."],
        ["ui_overread_risk", "summary_card_risk", "non_claim_prominence_review_needed"],
        ["hostile UI review", "reviewer wording review", "non-claim prominence checks"],
        ["Build 30 handoff", "hostile/red-team review"],
    ),
    _obj(
        "obj_038_reconciled_mistaken_verified",
        "Reconciled may be mistaken for an external source check",
        "reviewer_misinterpretation_risk",
        "high",
        "partially_mitigated",
        ["reports/public_data_consistency_audit.json", "simulator/pages/29_Public_Data_Evidence_Map.py"],
        "A reviewer may object that reconciled sounds like verified.",
        "The concern is valid because reconciliation language can imply more assurance than internal consistency.",
        "The project states reconciled means internally consistent only.",
        ["The repo can say reconciled means internal consistency only."],
        ["wording_overread_risk", "external_review_not_completed", "source_values_not_externally_checked"],
        ["wording review", "external source check process", "reviewer handoff note"],
        ["Build 30 handoff"],
    ),
    _obj(
        "obj_039_ready_manual_review_mistaken_reviewed",
        "Ready for manual review may be mistaken for reviewed",
        "reviewer_misinterpretation_risk",
        "high",
        "partially_mitigated",
        ["reports/source_locator_verification_pack.json", "simulator/pages/29_Public_Data_Evidence_Map.py"],
        "A reviewer may object that ready_for_manual_review could be mistaken for completed review.",
        "The concern is valid because readiness language can be overread as a completed status.",
        "The project states ready for manual review does not mean reviewed.",
        ["The repo can say locator metadata is sufficient for a reviewer to inspect manually."],
        ["manual_review_not_completed", "external_check_absent", "wording_overread_risk"],
        ["reviewer checklist execution", "signed review notes outside repo", "terminology review"],
        ["Build 30 handoff"],
    ),
    _obj(
        "obj_040_locator_metadata_not_source_verification",
        "Source locator metadata may be mistaken for source verification",
        "non_claim_boundary_risk",
        "high",
        "partially_mitigated",
        ["reports/source_locator_verification_pack.json", "docs/source_locator_verification_pack.md"],
        "A reviewer may object that locators can be confused with source verification.",
        "The concern is valid because a precise locator improves traceability but does not prove the extracted value was checked by an independent reviewer.",
        "The project keeps external_source_verification_claimed false.",
        ["The repo can say source locator metadata is recorded for manual review."],
        ["external_source_check_not_completed", "manual_review_needed", "locator_not_attestation"],
        ["manual source review", "documented source check", "independent reviewer note"],
        ["external review process", "Build 30 handoff"],
    ),
    _obj(
        "obj_041_evidence_maps_not_policy_readiness",
        "Reviewer evidence maps may be mistaken for policy readiness",
        "dashboard_interpretation_risk",
        "critical",
        "requires_external_review",
        ["reports/public_data_evidence_map.json", "reports/source_locator_verification_pack.json", "reports/red_team_reviewer_objections.json"],
        "A reviewer may object that organised reviewer material could make the project look ready for policy use.",
        "The concern is valid because coherent documentation can be mistaken for readiness even where evidence gaps remain.",
        "The project repeats non-claim boundaries and keeps readiness score creation false.",
        ["The repo can say reviewer materials organise weaknesses and inspection routes only."],
        ["policy_readiness_absent", "external_review_not_completed", "legal_economic_statistical_review_required"],
        ["external review findings", "policy design review", "legal/economic/statistical assessment"],
        ["Build 30 handoff", "external review"],
    ),
]


def find_forbidden_affirmative_red_team_claims(text: str) -> list[str]:
    findings: set[str] = set()
    lowered = text.lower()
    negative_markers = [
        "not ",
        "no ",
        "does not ",
        "do not ",
        "must not ",
        "must_not",
        "not_",
        "without ",
        "is not ",
        "are not ",
        "has not ",
        "have not ",
        "cannot ",
        "non-claim",
        "forbidden_claim",
        "objections being acknowledged does not mean",
        "partially mitigated does not mean",
    ]
    for phrase in FORBIDDEN_AFFIRMATIVE_RED_TEAM_CLAIMS:
        start = 0
        phrase_lower = phrase.lower()
        while True:
            index = lowered.find(phrase_lower, start)
            if index == -1:
                break
            context = lowered[max(0, index - 260) : min(len(lowered), index + len(phrase_lower) + 100)]
            if not any(marker in context for marker in negative_markers):
                findings.add(phrase)
                break
            start = index + len(phrase_lower)
    return sorted(findings)


def _required_mapping(source: dict[str, Any], keys: list[str], label: str) -> None:
    missing = [key for key in keys if key not in source]
    if missing:
        raise ValueError(f"{label} missing required fields: {', '.join(missing)}")


def _validate_manifest(manifest: dict[str, Any]) -> None:
    _required_mapping(
        manifest,
        [
            "pack_id",
            "pack_name",
            "status",
            "non_claims",
            "input_artifacts",
            "objection_status_taxonomy",
            "severity_taxonomy",
            "objection_category_taxonomy",
            "required_objection_categories",
            "minimum_objections_per_category",
            "required_objections",
            "forbidden_claims",
            "build_30_requirements",
        ],
        "red-team objections manifest",
    )
    if manifest["status"] != "red_team_reviewer_objections_pack_only":
        raise ValueError("red-team objections manifest status must be red_team_reviewer_objections_pack_only")
    if set(manifest["objection_status_taxonomy"]) != OBJECTION_STATUS_VALUES:
        raise ValueError("objection_status_taxonomy must match required values")
    if set(manifest["severity_taxonomy"]) != SEVERITY_VALUES:
        raise ValueError("severity_taxonomy must match required values")
    if set(manifest["objection_category_taxonomy"]) != OBJECTION_CATEGORY_VALUES:
        raise ValueError("objection_category_taxonomy must match required values")
    if set(manifest["required_objection_categories"]) - OBJECTION_CATEGORY_VALUES:
        raise ValueError("required objection categories contain unknown values")
    for non_claim in RED_TEAM_REVIEWER_OBJECTIONS_NON_CLAIMS:
        if non_claim not in manifest["non_claims"]:
            raise ValueError("red-team objections manifest missing required non-claim language")


def _validate_inputs(inputs: dict[str, dict[str, Any]]) -> None:
    required_keys = {
        "real_data_feasibility": "summary",
        "public_data_pilot": "summary",
        "public_data_evidence_map": "summary",
        "public_data_consistency_audit": "summary",
        "source_locator_verification_pack": "summary",
    }
    for name, key in required_keys.items():
        if key not in inputs.get(name, {}):
            raise ValueError(f"input report missing {key}: {name}")
    for name, payload in inputs.items():
        summary = payload.get("summary", {})
        for flag in REQUIRED_FALSE_FLAGS:
            if flag in summary and summary[flag] is not False:
                raise ValueError(f"input report has true false-flag {flag}: {name}")


def _validate_objections(objections: list[ReviewerObjection], manifest: dict[str, Any]) -> None:
    if len(objections) < 30:
        raise ValueError("at least 30 red-team objections are required")
    required_ids = set(manifest["required_objections"])
    actual_ids = {item.objection_id for item in objections}
    if required_ids - actual_ids:
        raise ValueError(f"required objections missing: {', '.join(sorted(required_ids - actual_ids))}")
    categories = {item.objection_category for item in objections}
    missing_categories = set(manifest["required_objection_categories"]) - categories
    if missing_categories:
        raise ValueError(f"required objection categories missing: {', '.join(sorted(missing_categories))}")
    minimum = int(manifest["minimum_objections_per_category"])
    for category in manifest["required_objection_categories"]:
        if sum(item.objection_category == category for item in objections) < minimum:
            raise ValueError(f"category has fewer than required objections: {category}")
    for item in objections:
        if item.status not in OBJECTION_STATUS_VALUES:
            raise ValueError(f"invalid objection status: {item.objection_id}")
        if item.severity not in SEVERITY_VALUES:
            raise ValueError(f"invalid severity: {item.objection_id}")
        if item.objection_category not in OBJECTION_CATEGORY_VALUES:
            raise ValueError(f"invalid objection category: {item.objection_id}")
        if not item.why_the_concern_is_valid:
            raise ValueError(f"missing valid concern explanation: {item.objection_id}")
        if not item.what_the_project_must_not_claim:
            raise ValueError(f"missing must-not-claim boundary: {item.objection_id}")
        if not item.unresolved_blockers:
            raise ValueError(f"missing unresolved blockers: {item.objection_id}")
        if not item.evidence_needed_to_resolve:
            raise ValueError(f"missing evidence needed to resolve: {item.objection_id}")


def _summaries_by_category(objections: list[ReviewerObjection]) -> list[ObjectionCategorySummary]:
    return [
        ObjectionCategorySummary(category, sum(item.objection_category == category for item in objections))
        for category in sorted({item.objection_category for item in objections})
    ]


def _summaries_by_severity(objections: list[ReviewerObjection]) -> list[ObjectionSeveritySummary]:
    return [
        ObjectionSeveritySummary(severity, sum(item.severity == severity for item in objections))
        for severity in sorted(SEVERITY_VALUES)
    ]


def _blocker_summaries(objections: list[ReviewerObjection]) -> list[UnresolvedBlockerSummary]:
    blockers = sorted({blocker for item in objections for blocker in item.unresolved_blockers})
    return [
        UnresolvedBlockerSummary(
            blocker,
            [item.objection_id for item in objections if blocker in item.unresolved_blockers],
        )
        for blocker in blockers
    ]


def _future_evidence_needs(objections: list[ReviewerObjection]) -> list[FutureEvidenceNeed]:
    needs = sorted({need for item in objections for need in item.evidence_needed_to_resolve})
    return [
        FutureEvidenceNeed(
            need,
            [item.objection_id for item in objections if need in item.evidence_needed_to_resolve],
        )
        for need in needs
    ]


def build_red_team_reviewer_objections_result(
    manifest: dict[str, Any],
    input_reports: dict[str, dict[str, Any]],
) -> RedTeamReviewerObjectionsResult:
    _validate_manifest(manifest)
    _validate_inputs(input_reports)
    objections = list(DEFAULT_OBJECTIONS)
    _validate_objections(objections, manifest)

    responses = [
        ReviewerObjectionResponse(
            objection_id=item.objection_id,
            current_project_response=item.current_project_response,
            can_say=item.what_the_project_can_say,
            must_not_claim=item.what_the_project_must_not_claim,
        )
        for item in objections
    ]
    category_summaries = _summaries_by_category(objections)
    severity_summaries = _summaries_by_severity(objections)
    blocker_summaries = _blocker_summaries(objections)
    evidence_needs = _future_evidence_needs(objections)

    partial_result = {
        "objections": [item.to_jsonable() for item in objections],
        "responses": [item.to_jsonable() for item in responses],
        "category_summaries": [item.to_jsonable() for item in category_summaries],
        "severity_summaries": [item.to_jsonable() for item in severity_summaries],
        "unresolved_blockers": [item.to_jsonable() for item in blocker_summaries],
        "future_evidence_needs": [item.to_jsonable() for item in evidence_needs],
    }
    forbidden_claims = find_forbidden_affirmative_red_team_claims(str(partial_result))
    summary = RedTeamReviewerObjectionsSummary(
        total_objections=len(objections),
        critical_objections=sum(item.severity == "critical" for item in objections),
        high_objections=sum(item.severity == "high" for item in objections),
        medium_objections=sum(item.severity == "medium" for item in objections),
        low_objections=sum(item.severity == "low" for item in objections),
        informational_objections=sum(item.severity == "informational" for item in objections),
        acknowledged_objections=sum(item.status == "acknowledged" for item in objections),
        partially_mitigated_objections=sum(item.status == "partially_mitigated" for item in objections),
        unresolved_objections=sum(item.status == "unresolved" for item in objections),
        blocked_by_restricted_data_objections=sum(item.status == "blocked_by_restricted_data" for item in objections),
        external_review_required_objections=sum(item.status == "requires_external_review" for item in objections),
        legal_review_required_objections=sum(item.status == "requires_legal_review" for item in objections),
        economic_review_required_objections=sum(item.status == "requires_economic_review" for item in objections),
        statistical_review_required_objections=sum(item.status == "requires_statistical_review" for item in objections),
        cannot_be_resolved_inside_repo_objections=sum(item.status == "cannot_be_resolved_inside_repo" for item in objections),
        total_categories=len(OBJECTION_CATEGORY_VALUES),
        categories_covered=len({item.objection_category for item in objections}),
        unresolved_blockers_total=len(blocker_summaries),
        future_evidence_needs_total=len(evidence_needs),
        forbidden_claim_findings=len(forbidden_claims),
        red_team_pack_created=True,
        new_data_loaded=False,
        external_source_verification_claimed=False,
        objections_acknowledged=True,
        unresolved_blockers_visible=bool(blocker_summaries),
        calibration_limitations_visible=any(item.objection_category == "calibration_limitations" for item in objections),
        legal_limitations_visible=any(item.objection_category == "legal_and_tax_limitations" for item in objections),
        statistical_limitations_visible=any(item.objection_category == "statistical_limitations" for item in objections),
        dashboard_misinterpretation_risks_visible=any(
            item.objection_category in {"dashboard_interpretation_risk", "reviewer_misinterpretation_risk"}
            for item in objections
        ),
        real_calibration_completed=False,
        actual_tax_payable_determined=False,
        validation_claimed=False,
        approval_claimed=False,
        operational_readiness_claimed=False,
        legal_sufficiency_claimed=False,
        official_status_claimed=False,
        firm_level_liability_logic_modified=False,
    )
    if forbidden_claims:
        raise ValueError(f"forbidden affirmative red-team claims found: {', '.join(forbidden_claims)}")

    return RedTeamReviewerObjectionsResult(
        pack_id=manifest["pack_id"],
        pack_name=manifest["pack_name"],
        status=manifest["status"],
        non_claims=manifest["non_claims"],
        input_artifacts=manifest["input_artifacts"],
        objections=objections,
        responses=responses,
        category_summaries=category_summaries,
        severity_summaries=severity_summaries,
        unresolved_blockers=blocker_summaries,
        future_evidence_needs=evidence_needs,
        forbidden_claims=forbidden_claims,
        build_30_requirements=manifest["build_30_requirements"],
        summary=summary,
    )
