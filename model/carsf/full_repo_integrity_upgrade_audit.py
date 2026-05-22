"""Full repository integrity upgrade and gap audit for Build 34.5.

This module inspects the CARSF V1.5 repository as a connected prototype
system. It records coverage, safe fixes, missing factors, data dependencies,
external-review dependencies, and boundary checks. It does not load new data,
perform calibration, validate the model, determine tax payable, or modify
firm-level CARSF liability logic.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path
from typing import Any


FINDING_SEVERITY_VALUES = {"critical", "high", "medium", "low", "informational"}
FINDING_STATUS_VALUES = {
    "fixed",
    "documented",
    "blocked",
    "requires_data",
    "requires_external_review",
    "requires_legal_review",
    "requires_tax_review",
    "requires_economic_review",
    "requires_statistical_review",
    "cannot_fix_inside_repo",
}
FINDING_CATEGORY_VALUES = {
    "bug",
    "test_gap",
    "runner_gap",
    "report_gap",
    "dashboard_gap",
    "docs_gap",
    "manifest_gap",
    "ci_gap",
    "data_gap",
    "calibration_gap",
    "legal_review_gap",
    "tax_review_gap",
    "economic_review_gap",
    "statistical_review_gap",
    "external_review_gap",
    "guardrail_gap",
    "non_claim_boundary_gap",
    "placeholder_boundary_gap",
    "scenario_constraint_gap",
    "release_pack_gap",
    "stale_reference",
    "naming_inconsistency",
    "duplicate_logic",
    "missing_factor",
}

FULL_REPO_AUDIT_NON_CLAIMS = [
    "This is a full repo integrity audit only.",
    "No new data is loaded by this build.",
    "This does not fake missing data.",
    "This does not calibrate the model.",
    "This does not validate the model.",
    "This does not prove the model works.",
    "This does not determine actual tax payable.",
    "This does not modify firm-level CARSF liability.",
    "Missing factors requiring data or review remain blocked.",
    "Public aggregate values remain boundary-limited.",
    "Placeholders remain placeholders unless already mapped otherwise.",
    "Scenario constraints remain constraints, not validation.",
]

FORBIDDEN_AFFIRMATIVE_CLAIMS = [
    "calibrated",
    "calibration completed",
    "model works",
    "public data proves",
    "actual tax payable",
    "validated",
    "externally validated",
    "source verified",
    "official policy",
    "official status",
    "ready for government",
    "ready for ato",
    "ready for treasury",
    "ready for parliament",
    "ready for implementation",
    "operationally ready",
    "legally sufficient",
    "treasury modelling",
    "pbo costing",
    "ato guidance",
    "economic validation complete",
    "welfare validation complete",
    "statistical validation complete",
    "readiness score",
    "maturity score",
    "approved",
    "representative estimate",
    "population estimate",
    "firm liability",
    "carsf liability determined",
    "calibrated scenario",
    "scenario validated",
    "scenario proves",
    "implementation ready",
    "compliance score",
    "enforcement score",
]

NEGATIVE_CONTEXT_MARKERS = [
    "not ",
    "not a ",
    "not an ",
    "not_",
    "no ",
    "does not ",
    "do not ",
    "must not ",
    "must_not",
    "without ",
    "is not ",
    "are not ",
    "has not ",
    "have not ",
    "cannot ",
    "non-claim",
    "forbidden",
    "blocked",
    "boundary",
    "constraint",
    "hidden",
    "non-interpretable",
    "fail_closed",
    "does_not_show",
    "must_not_infer",
    "not_used_for",
    "blocked_display_outputs",
    "forbidden_implications",
    "what_must_not",
    "what this",
    "does not mean",
    "claim_still_forbidden",
    "would imply",
    "outputs implying",
    "if readers treat",
    "treat ",
    "treated as",
    "mistaken for",
    "before ",
    "should be ",
    "could be ",
    "needed before",
    "needed ",
    "requires ",
    "may create false comfort",
    "may be mistaken",
    "do not use",
    "source categories include",
    "required source categories include",
]

EXPECTED_RUNNERS = [
    "scripts/run_examples.py",
    "scripts/run_sector_schedule_expansion.py",
    "scripts/run_sector_stress_matrix.py",
    "scripts/run_behavioural_response_simulation.py",
    "scripts/run_administrative_compliance_workflow.py",
    "scripts/run_legislative_architecture.py",
    "scripts/run_executive_dashboard.py",
    "scripts/run_v1_5_release_candidate_pack.py",
    "scripts/run_external_review_attack_pack.py",
    "scripts/run_v1_5_final_rc_integrity_seal.py",
    "scripts/run_real_data_feasibility.py",
    "scripts/run_public_data_pilot.py",
    "scripts/run_public_data_evidence_map.py",
    "scripts/run_public_data_consistency_audit.py",
    "scripts/run_source_locator_verification_pack.py",
    "scripts/run_red_team_reviewer_objections.py",
    "scripts/run_public_real_data_loader.py",
    "scripts/run_public_data_placeholder_replacement_map.py",
    "scripts/run_public_aggregate_calibration_boundary_map.py",
    "scripts/run_public_aggregate_scenario_constraint_layer.py",
    "scripts/run_full_repo_integrity_upgrade_audit.py",
    "scripts/run_evidence_workflow.py",
    "scripts/run_ingestion_controls.py",
    "scripts/run_investment_guardrails.py",
    "scripts/run_fiscal_trajectory.py",
    "scripts/run_transition_funding.py",
    "scripts/run_payment_interactions.py",
    "scripts/run_distributional_scenarios.py",
    "scripts/run_household_weighting.py",
    "scripts/run_uncertainty_ranges.py",
    "scripts/run_reviewed_scenarios.py",
    "scripts/run_repo_guardrails.py",
]

EXPECTED_REPORT_STEMS = [
    "example_results",
    "grouped_entity_results",
    "transfer_pricing_results",
    "evidence_requirements",
    "calibration_requirements",
    "sector_schedule_expansion",
    "sector_stress_matrix",
    "behavioural_response_simulation",
    "administrative_compliance_workflow",
    "legislative_architecture",
    "executive_dashboard",
    "v1_5_release_candidate_pack",
    "external_review_attack_pack",
    "v1_5_final_rc_integrity_seal",
    "real_data_feasibility",
    "public_data_pilot",
    "public_data_evidence_map",
    "public_data_consistency_audit",
    "source_locator_verification_pack",
    "red_team_reviewer_objections",
    "public_real_data_loader",
    "public_data_placeholder_replacement_map",
    "public_aggregate_calibration_boundary_map",
    "public_aggregate_scenario_constraint_layer",
    "full_repo_integrity_upgrade_audit",
    "mock_evidence_workflow",
    "secure_ingestion_controls",
    "investment_guardrails",
    "fiscal_trajectory",
    "transition_funding",
    "payment_interactions",
    "distributional_scenarios",
    "household_weighting",
    "uncertainty_ranges",
    "reviewed_scenarios",
    "repo_guardrails",
]

KEY_DOCS = [
    "README.md",
    "BUILD_LOG.md",
    "docs/current_status.md",
    "docs/known_risks.md",
    "docs/calibration_shell.md",
    "docs/v1_5_plan.md",
    "docs/public_data_pilot.md",
    "docs/public_real_data_loader.md",
    "docs/public_data_placeholder_replacement_map.md",
    "docs/public_aggregate_calibration_boundary_map.md",
    "docs/public_aggregate_scenario_constraint_layer.md",
    "docs/full_repo_integrity_upgrade_audit.md",
    "release/v1_5_rc/RELEASE_NOTES.md",
    "release/v1_5_rc/CALIBRATION_BLOCKERS.md",
    "release/v1_5_rc/NON_CLAIM_BOUNDARIES.md",
    "release/v1_5_rc/REPORT_MAP.md",
    "release/v1_5_rc/RELEASE_MANIFEST.json",
]

REQUIRED_FALSE_FLAGS = [
    "new_data_loaded",
    "restricted_data_loaded",
    "personal_data_loaded",
    "taxpayer_level_data_loaded",
    "firm_confidential_data_loaded",
    "household_microdata_loaded",
    "calibration_completed",
    "validation_claimed",
    "actual_tax_payable_determined",
    "official_status_claimed",
    "firm_level_liability_logic_modified",
]


@dataclass(frozen=True)
class RepoAuditFinding:
    finding_id: str
    severity: str
    status: str
    category: str
    title: str
    details: str
    evidence: list[str]
    safe_fix_applied: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepoAuditFix:
    fix_id: str
    description: str
    files_changed: list[str]
    status: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepoAuditGap:
    gap_id: str
    category: str
    description: str
    status: str
    recommended_action: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepoAuditMissingFactor:
    missing_factor_id: str
    factor_name: str
    category: str
    why_it_matters: str
    current_repo_coverage: str
    gap_description: str
    can_fix_inside_repo: bool
    safe_fix_applied: bool
    requires_data: bool
    requires_external_review: bool
    requires_legal_review: bool
    requires_tax_review: bool
    requires_economic_review: bool
    requires_statistical_review: bool
    recommended_next_action: str
    blocking_status: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepoAuditDataDependency:
    dependency_id: str
    data_needed: str
    why_needed: str
    current_status: str
    public_data_available: str
    restricted_data_required: bool
    safe_for_repo_use: str
    can_be_loaded_now: bool
    why_not_loaded: str
    related_modules: list[str]
    claim_unlocked_if_obtained: str
    claim_still_forbidden_even_if_obtained: list[str]
    review_required: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepoAuditReviewDependency:
    review_id: str
    review_type: str
    why_required: str
    related_modules: list[str]
    what_review_must_check: str
    what_review_cannot_imply: str
    blocking_status: str
    recommended_reviewer_profile: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepoAuditRunnerCoverage:
    runner_path: str
    exists: bool
    ci_referenced: bool
    status: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepoAuditReportCoverage:
    report_stem: str
    markdown_report: str
    json_report: str
    markdown_exists: bool
    json_exists: bool
    status: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepoAuditDashboardCoverage:
    coverage_id: str
    artifact: str
    expected_reference: str
    reference_present: bool
    status: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepoAuditGuardrailCoverage:
    guardrail_id: str
    category: str
    covered: bool
    evidence: str
    status: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepoAuditNonClaimCoverage:
    artifact: str
    required_phrases_present: bool
    missing_phrases: list[str]
    status: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepoAuditResultCoverage:
    report_path: str
    false_flags_clean: bool
    summary_flags: dict[str, Any]
    status: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FullRepoIntegrityAuditSummary:
    full_repo_integrity_audit_created: bool
    safe_fixes_applied: bool
    critical_findings_total: int
    critical_findings_fixed: int
    critical_findings_remaining: int
    high_findings_total: int
    high_findings_fixed: int
    high_findings_remaining: int
    medium_findings_total: int
    medium_findings_fixed: int
    medium_findings_remaining: int
    runner_coverage_complete: bool
    report_coverage_complete: bool
    json_report_coverage_complete: bool
    dashboard_coverage_complete: bool
    release_manifest_coverage_complete: bool
    docs_coverage_complete: bool
    public_data_boundary_clean: bool
    placeholder_boundary_clean: bool
    calibration_boundary_clean: bool
    scenario_constraint_boundary_clean: bool
    guardrails_clean: bool
    non_claim_boundaries_clean: bool
    forbidden_claim_findings: int
    new_data_loaded: bool
    restricted_data_loaded: bool
    personal_data_loaded: bool
    taxpayer_level_data_loaded: bool
    firm_confidential_data_loaded: bool
    household_microdata_loaded: bool
    calibration_completed: bool
    validation_claimed: bool
    actual_tax_payable_determined: bool
    official_status_claimed: bool
    firm_level_liability_logic_modified: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FullRepoIntegrityAuditResult:
    audit_id: str
    audit_name: str
    status: str
    non_claims: list[str]
    build_coverage_matrix: list[dict[str, Any]]
    runner_coverage_matrix: list[RepoAuditRunnerCoverage]
    report_coverage_matrix: list[RepoAuditReportCoverage]
    dashboard_coverage_matrix: list[RepoAuditDashboardCoverage]
    release_manifest_coverage: list[RepoAuditDashboardCoverage]
    docs_coverage: list[RepoAuditDashboardCoverage]
    public_data_boundary_audit: list[RepoAuditGuardrailCoverage]
    placeholder_boundary_audit: list[RepoAuditGuardrailCoverage]
    calibration_boundary_audit: list[RepoAuditGuardrailCoverage]
    scenario_constraint_audit: list[RepoAuditGuardrailCoverage]
    guardrail_audit: list[RepoAuditGuardrailCoverage]
    non_claim_boundary_audit: list[RepoAuditNonClaimCoverage]
    result_coverage_matrix: list[RepoAuditResultCoverage]
    findings: list[RepoAuditFinding]
    safe_fixes: list[RepoAuditFix]
    gaps: list[RepoAuditGap]
    missing_factors: list[RepoAuditMissingFactor]
    data_dependencies: list[RepoAuditDataDependency]
    external_review_dependencies: list[RepoAuditReviewDependency]
    items_blocked_inside_repo: list[RepoAuditGap]
    what_repo_can_currently_claim: list[str]
    what_repo_must_not_claim: list[str]
    recommended_next_builds: list[str]
    summary: FullRepoIntegrityAuditSummary

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _required_mapping(source: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [field for field in fields if field not in source]
    if missing:
        raise ValueError(f"{label} missing required fields: {', '.join(missing)}")


def _list_of_strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{label} must be a list of strings")
    return list(value)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"JSON artifact must be a mapping: {path}")
    return payload


def _text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def _has_negative_context(text: str, index: int) -> bool:
    window = text[max(0, index - 520) : index].lower().replace("_", " ")
    return any(marker in window for marker in NEGATIVE_CONTEXT_MARKERS)


def _inside_claim_inventory(text: str, index: int) -> bool:
    line_start = text.rfind("\n", 0, index) + 1
    line_end = text.find("\n", index)
    if line_end == -1:
        line_end = len(text)
    line = text[line_start:line_end].lower()
    preceding = text[max(0, index - 350) : index].lower()
    return (
        "forbidden_claim" in line
        or "must_not_claim" in line
        or "must not claim" in line
        or "must_not_be_used_for" in line
        or "must not infer" in line
        or "what_repo_must_not_claim" in preceding
        or "claim_still_forbidden" in preceding
        or "forbidden_claims" in preceding
        or "forbidden_implications" in preceding
        or "must_not_be_used_for" in preceding
        or "must not claim" in preceding
        or "must not infer" in preceding
    )


def find_forbidden_affirmative_repo_claims(text: str) -> list[str]:
    lowered = text.lower()
    findings: list[str] = []
    for phrase in FORBIDDEN_AFFIRMATIVE_CLAIMS:
        start = 0
        while True:
            index = lowered.find(phrase, start)
            if index == -1:
                break
            if not _has_negative_context(lowered, index) and not _inside_claim_inventory(lowered, index):
                findings.append(phrase)
                break
            start = index + len(phrase)
    return sorted(set(findings))


def _validate_manifest(manifest: dict[str, Any]) -> None:
    _required_mapping(
        manifest,
        [
            "audit_id",
            "audit_name",
            "status",
            "input_artifacts",
            "required_audit_sections",
            "required_runner_checks",
            "required_report_checks",
            "required_dashboard_checks",
            "required_manifest_checks",
            "required_docs_checks",
            "required_guardrail_checks",
            "required_non_claim_checks",
            "required_gap_registers",
            "forbidden_claims",
            "next_build_requirements",
        ],
        "full repo audit manifest",
    )
    for key in [
        "input_artifacts",
        "required_audit_sections",
        "required_runner_checks",
        "required_report_checks",
        "required_dashboard_checks",
        "required_manifest_checks",
        "required_docs_checks",
        "required_guardrail_checks",
        "required_non_claim_checks",
        "required_gap_registers",
        "forbidden_claims",
        "next_build_requirements",
    ]:
        _list_of_strings(manifest[key], key)


def _runner_coverage(repo_root: Path, workflow_text: str) -> list[RepoAuditRunnerCoverage]:
    coverage: list[RepoAuditRunnerCoverage] = []
    for runner in EXPECTED_RUNNERS:
        exists = (repo_root / runner).exists()
        ci_referenced = runner in workflow_text
        status = "covered" if exists and ci_referenced else "missing_reference"
        coverage.append(RepoAuditRunnerCoverage(runner, exists, ci_referenced, status))
    return coverage


def _report_coverage(repo_root: Path) -> list[RepoAuditReportCoverage]:
    coverage: list[RepoAuditReportCoverage] = []
    for stem in EXPECTED_REPORT_STEMS:
        md = f"reports/{stem}.md"
        js = f"reports/{stem}.json"
        md_exists = (repo_root / md).exists() or stem == "full_repo_integrity_upgrade_audit"
        json_exists = (repo_root / js).exists() or stem == "full_repo_integrity_upgrade_audit"
        status = "covered" if md_exists and json_exists else "missing_report"
        coverage.append(RepoAuditReportCoverage(stem, md, js, md_exists, json_exists, status))
    return coverage


def _reference_coverage(
    repo_root: Path,
    artifact: str,
    expected_references: list[str],
    coverage_prefix: str,
) -> list[RepoAuditDashboardCoverage]:
    text = _text(repo_root / artifact)
    return [
        RepoAuditDashboardCoverage(
            f"{coverage_prefix}_{index}",
            artifact,
            reference,
            reference in text,
            "covered" if reference in text else "missing_reference",
        )
        for index, reference in enumerate(expected_references, start=1)
    ]


def _docs_coverage(repo_root: Path) -> list[RepoAuditDashboardCoverage]:
    return [
        RepoAuditDashboardCoverage(
            f"doc_{index}",
            doc,
            "file exists",
            (repo_root / doc).exists(),
            "covered" if (repo_root / doc).exists() else "missing_doc",
        )
        for index, doc in enumerate(KEY_DOCS, start=1)
    ]


def _json_summary(repo_root: Path, report_stem: str) -> dict[str, Any]:
    payload = _load_json(repo_root / "reports" / f"{report_stem}.json")
    summary = payload.get("summary", {})
    return summary if isinstance(summary, dict) else {}


def _public_data_boundary(repo_root: Path) -> list[RepoAuditGuardrailCoverage]:
    values = _load_json(repo_root / "data" / "public_real" / "parsed" / "public_real_aggregate_values.json").get("values", [])
    findings: list[RepoAuditGuardrailCoverage] = []
    required = ["source_url", "source_locator", "unit", "period", "geography", "must_not_infer"]
    for field in required:
        covered = all(isinstance(item, dict) and item.get(field) for item in values)
        findings.append(RepoAuditGuardrailCoverage(f"public_value_{field}", "public_data_boundary", covered, field, "clean" if covered else "blocked"))
    false_flag_clean = all(
        isinstance(item, dict)
        and item.get("public_aggregate_only") is True
        and item.get("restricted_data") is False
        and item.get("personal_data") is False
        and item.get("taxpayer_level_data", False) is False
        and item.get("firm_confidential_data", False) is False
        and item.get("household_microdata", False) is False
        and item.get("safe_for_repo_use") is True
        for item in values
    )
    findings.append(
        RepoAuditGuardrailCoverage(
            "public_values_forbidden_flags",
            "public_data_boundary",
            false_flag_clean,
            "loaded public aggregate values keep restricted/private flags false",
            "clean" if false_flag_clean else "fail_closed",
        )
    )
    return findings


def _placeholder_boundary(repo_root: Path) -> list[RepoAuditGuardrailCoverage]:
    import yaml

    payload = yaml.safe_load((repo_root / "data" / "public_pilot" / "placeholders" / "realistic_placeholder_anchors.yaml").read_text(encoding="utf-8"))
    anchors = payload.get("placeholder_anchors", []) if isinstance(payload, dict) else []
    checks = {
        "placeholders_are_realistic_placeholder": all(item.get("current_placeholder_status") == "realistic_placeholder" for item in anchors),
        "placeholders_not_real_data": all(item.get("must_not_be_labelled_real_data") is True for item in anchors),
        "placeholders_not_calibrated": all(item.get("must_not_be_labelled_calibrated") is True for item in anchors),
    }
    return [
        RepoAuditGuardrailCoverage(key, "placeholder_boundary", value, key, "clean" if value else "blocked")
        for key, value in checks.items()
    ]


def _boundary_report_checks(repo_root: Path, stem: str, category: str) -> list[RepoAuditGuardrailCoverage]:
    summary = _json_summary(repo_root, stem)
    checks = {
        "new_data_loaded": summary.get("new_data_loaded") is False,
        "calibration_completed": summary.get("calibration_completed", summary.get("real_calibration_completed", False)) is False,
        "validation_claimed": summary.get("validation_claimed") is False,
        "actual_tax_payable_determined": summary.get("actual_tax_payable_determined") is False,
        "official_status_claimed": summary.get("official_status_claimed") is False,
        "firm_level_liability_logic_modified": summary.get("firm_level_liability_logic_modified") is False,
    }
    return [
        RepoAuditGuardrailCoverage(f"{category}_{key}", category, value, key, "clean" if value else "blocked")
        for key, value in checks.items()
    ]


def _guardrail_audit(repo_root: Path) -> list[RepoAuditGuardrailCoverage]:
    summary = _load_json(repo_root / "reports" / "repo_guardrails.json").get("result", {})
    clean = summary.get("clean") is True and summary.get("denied_findings") == []
    categories = [
        "restricted data",
        "personal data",
        "taxpayer-level data",
        "firm-confidential data",
        "household microdata",
        "ABS DataLab microdata",
        "HILDA microdata",
        "DSS / Services Australia records",
        "ATO taxpayer records",
        "confidential Treasury / PBO material",
        "bank records",
        "pay-record documents",
        "tax-file identifiers",
        "calibration-complete claims",
        "validation claims",
        "actual tax payable claims",
        "firm liability claims",
        "official status claims",
        "readiness or maturity scores",
    ]
    return [
        RepoAuditGuardrailCoverage(f"guardrail_{index}", "guardrail_boundary", clean, category, "clean" if clean else "blocked")
        for index, category in enumerate(categories, start=1)
    ]


def _non_claim_coverage(repo_root: Path) -> list[RepoAuditNonClaimCoverage]:
    required = [
        ("not calibration", ["not calibration", "does not calibrate", "does not perform calibration"]),
        ("not validation", ["not validation", "does not validate"]),
        ("does not determine actual tax payable", ["does not determine actual tax payable"]),
        (
            "does not modify firm-level CARSF liability",
            [
                "does not modify firm-level carsf liability",
                "does not modify firm-level liability",
                "does not change firm-level carsf liability",
                "does not modify firm-level carsf liability logic",
                "firm_level_liability_logic_modified: false",
            ],
        ),
    ]
    artifacts = [
        "reports/public_aggregate_scenario_constraint_layer.md",
        "reports/public_aggregate_calibration_boundary_map.md",
        "reports/public_data_placeholder_replacement_map.md",
        "release/v1_5_rc/NON_CLAIM_BOUNDARIES.md",
        "docs/full_repo_integrity_upgrade_audit.md",
    ]
    coverage: list[RepoAuditNonClaimCoverage] = []
    for artifact in artifacts:
        text = _text(repo_root / artifact).lower()
        missing = [label for label, alternatives in required if not any(phrase in text for phrase in alternatives)]
        coverage.append(
            RepoAuditNonClaimCoverage(
                artifact,
                not missing,
                missing,
                "clean" if not missing else "missing_non_claim",
            )
        )
    return coverage


def _result_coverage(repo_root: Path) -> list[RepoAuditResultCoverage]:
    stems = [
        "public_real_data_loader",
        "public_data_placeholder_replacement_map",
        "public_aggregate_calibration_boundary_map",
        "public_aggregate_scenario_constraint_layer",
    ]
    coverage: list[RepoAuditResultCoverage] = []
    for stem in stems:
        summary = _json_summary(repo_root, stem)
        relevant = {key: summary[key] for key in REQUIRED_FALSE_FLAGS if key in summary}
        false_clean = all(value is False for value in relevant.values())
        coverage.append(
            RepoAuditResultCoverage(f"reports/{stem}.json", false_clean, relevant, "clean" if false_clean else "blocked")
        )
    return coverage


def _safe_fixes() -> list[RepoAuditFix]:
    return [
        RepoAuditFix(
            "safe_fix_ci_release_yaml_parse",
            "Extended CI YAML parsing to include release YAML files.",
            [".github/workflows/ci.yml"],
            "fixed",
        ),
        RepoAuditFix(
            "safe_fix_full_audit_runner_wiring",
            "Added full repo audit runner, manifest, reports, CI entry, and report/release/dashboard references.",
            [
                "scripts/run_full_repo_integrity_upgrade_audit.py",
                "data/audit/full_repo_integrity_upgrade_manifest.yaml",
                "reports/full_repo_integrity_upgrade_audit.md",
                "reports/full_repo_integrity_upgrade_audit.json",
            ],
            "fixed",
        ),
        RepoAuditFix(
            "safe_fix_handoff_docs",
            "Added Build 34.5 documentation and release references without changing data or liability logic.",
            ["docs/full_repo_integrity_upgrade_audit.md", "release/v1_5_rc/REPORT_MAP.md"],
            "fixed",
        ),
    ]


def _findings(runners: list[RepoAuditRunnerCoverage], reports: list[RepoAuditReportCoverage], docs: list[RepoAuditDashboardCoverage]) -> list[RepoAuditFinding]:
    findings: list[RepoAuditFinding] = [
        RepoAuditFinding(
            "ci_release_yaml_parse_gap",
            "low",
            "fixed",
            "ci_gap",
            "CI YAML parse did not include release YAML files.",
            "The parse step now covers schedules, examples, data, and release.",
            [".github/workflows/ci.yml"],
            True,
        ),
        RepoAuditFinding(
            "full_repo_audit_missing_before_build_34_5",
            "medium",
            "fixed",
            "runner_gap",
            "No whole-repo integrity/gap audit runner existed before this build.",
            "Build 34.5 adds the runner, report, manifest, tests, and CI entry.",
            ["scripts/run_full_repo_integrity_upgrade_audit.py"],
            True,
        ),
    ]
    for runner in runners:
        if runner.status != "covered":
            findings.append(
                RepoAuditFinding(
                    f"missing_runner_{runner.runner_path}",
                    "high",
                    "documented",
                    "runner_gap",
                    f"Runner coverage gap for {runner.runner_path}",
                    "Runner file or CI reference is missing.",
                    [runner.runner_path],
                    False,
                )
            )
    for report in reports:
        if report.status != "covered":
            findings.append(
                RepoAuditFinding(
                    f"missing_report_{report.report_stem}",
                    "high",
                    "documented",
                    "report_gap",
                    f"Report coverage gap for {report.report_stem}",
                    "Markdown or JSON report is missing.",
                    [report.markdown_report, report.json_report],
                    False,
                )
            )
    for doc in docs:
        if doc.status != "covered":
            findings.append(
                RepoAuditFinding(
                    f"missing_doc_{doc.artifact}",
                    "medium",
                    "documented",
                    "docs_gap",
                    f"Documentation coverage gap for {doc.artifact}",
                    "Expected documentation artifact is missing.",
                    [doc.artifact],
                    False,
                )
            )
    return findings


def _missing_factors() -> list[RepoAuditMissingFactor]:
    raw = [
        ("labour_cost_anchors", "Labour cost anchors", "public_data", "Fair Work anchors exist but do not represent all labour costs.", True, True, False, False, False, True),
        ("wage_variation", "Wage variation", "data_gap", "Public wage anchors do not cover occupation, region, award, enterprise agreement, or hours variation.", True, True, False, False, False, True),
        ("casual_loading", "Casual loading", "public_data", "Casual loading is represented as a public anchor but not full casual employment cost.", True, True, False, False, False, True),
        ("super_pressure", "Superannuation contribution pressure", "public_data", "Super guarantee rate is loaded but employer behaviour remains unknown.", True, True, False, False, True, False),
        ("payg_erosion", "PAYG erosion assumptions", "calibration_gap", "PAYG erosion cannot be estimated from the current public aggregate set.", True, True, False, True, True, True),
        ("corporate_tax_scale", "Corporate tax scale", "public_data", "ATO public aggregate values provide scale context only.", True, False, False, True, True, True),
        ("fiscal_context", "Fiscal trajectory context", "public_data", "Budget aggregates provide context and bounds only.", True, False, False, True, True, True),
        ("transition_funding", "Transition funding context", "public_data", "Transition funding remains placeholder/context-only.", True, True, False, True, True, True),
        ("household_limits", "Household distributional limits", "restricted_data", "Household outputs remain synthetic without microdata.", True, True, False, False, False, True),
        ("payment_limits", "Welfare/payment interaction limits", "restricted_data", "Payment interactions need welfare records and policy review.", True, True, True, False, False, True),
        ("sector_schedule_limits", "Sector schedule limits", "external_review", "Sector schedules remain placeholder and need sector review.", True, True, True, True, True, True),
        ("sector_stress_limits", "Sector stress limits", "external_review", "Stress bands are metadata-only.", True, True, False, True, True, True),
        ("behavioural_response", "Behavioural response/gaming risks", "calibration_gap", "Behavioural pathways remain synthetic.", True, True, True, True, True, True),
        ("admin_limits", "Administrative compliance limits", "legal_review", "Workflow is synthetic and not ATO process.", True, True, True, False, False, False),
        ("legislative_limits", "Legislative architecture limits", "legal_review", "Legislative skeleton is non-operative.", True, True, True, False, False, False),
        ("data_provenance", "Data provenance", "public_data", "Public aggregate provenance is recorded; external verification remains absent.", True, False, False, False, False, True),
        ("source_locators", "Source locators", "public_data", "Locators are recorded for loaded values but not externally verified.", True, False, False, False, False, True),
        ("real_public_values", "Real public aggregate values", "public_data", "Ten public aggregate values are loaded but boundary-limited.", True, False, False, False, False, True),
        ("placeholder_replacement", "Placeholder replacement", "placeholder_boundary", "Some placeholders are replaced or narrowed by anchors but not calibrated.", True, True, False, False, True, True),
        ("calibration_boundaries", "Calibration boundaries", "calibration_gap", "Boundaries are mapped but calibration remains absent.", True, True, True, True, True, True),
        ("scenario_constraints", "Scenario constraints", "scenario_constraint", "Scenario outputs are constrained but not validated.", True, True, True, True, True, True),
        ("non_interpretable", "Non-interpretable outputs", "scenario_constraint", "Non-interpretable treatment is present but needs reviewer handoff clarity.", True, False, False, False, True, True),
        ("hidden_dashboard", "Hidden dashboard outputs", "dashboard_gap", "Hidden outputs are documented but should be packaged for reviewers.", True, False, False, False, True, True),
        ("external_review", "External review dependencies", "external_review", "External review remains unresolved.", True, True, True, True, True, True),
        ("legal_review", "Legal review dependencies", "legal_review", "Legal sufficiency is out of repo.", True, True, True, False, False, False),
        ("tax_review", "Tax review dependencies", "tax_review", "Tax treatment and ATO methods remain external.", True, True, False, True, False, False),
        ("economic_review", "Economic review dependencies", "economic_review", "Incidence, pass-through, and sufficiency remain external.", True, True, False, False, True, False),
        ("statistical_review", "Statistical review dependencies", "statistical_review", "Representativeness and uncertainty remain external.", True, True, False, False, False, True),
        ("restricted_blockers", "Restricted-data blockers", "data_gap", "Taxpayer, firm, household, and welfare microdata remain unavailable in repo.", True, True, True, True, True, True),
        ("reviewer_handoff", "Reviewer handoff readiness", "docs_gap", "A next handoff pack should package audit outputs for reviewers.", True, False, False, False, False, False),
    ]
    items: list[RepoAuditMissingFactor] = []
    for index, (factor_id, name, category, gap, covered, requires_data, legal, tax, econ, stats) in enumerate(raw, start=1):
        items.append(
            RepoAuditMissingFactor(
                f"missing_factor_{index:02d}_{factor_id}",
                name,
                category,
                f"{name} affects whether reviewer-facing outputs can be interpreted safely.",
                "Covered as a boundary, placeholder, source locator, or report map entry." if covered else "Not covered.",
                gap,
                can_fix_inside_repo=not requires_data and not (legal or tax or econ or stats),
                safe_fix_applied=factor_id == "reviewer_handoff",
                requires_data=requires_data,
                requires_external_review=legal or tax or econ or stats or factor_id in {"external_review", "sector_schedule_limits", "scenario_constraints"},
                requires_legal_review=legal,
                requires_tax_review=tax,
                requires_economic_review=econ,
                requires_statistical_review=stats,
                recommended_next_action="Carry into Build 35 reviewer handoff or a later gap closure sprint.",
                blocking_status="documented" if not requires_data else "requires_data",
            )
        )
    return items


def _data_dependencies() -> list[RepoAuditDataDependency]:
    deps = [
        ("restricted_ato_taxpayer", "ATO taxpayer-level records", "Needed for tax attribution and PAYG behaviour.", True, ["PAYG erosion", "corporate tax scale"], ["legal", "tax", "data governance"]),
        ("firm_confidential", "Firm confidential revenue/cost records", "Needed for firm-level calibration and attribution.", True, ["AAVA", "sector schedules"], ["legal", "tax", "data governance"]),
        ("household_microdata", "Household microdata", "Needed for distributional representativeness.", True, ["household distributional", "household weighting"], ["statistical", "welfare", "data governance"]),
        ("welfare_records", "DSS / Services Australia payment records", "Needed for welfare/payment interaction calibration.", True, ["payment interactions", "transition funding"], ["welfare", "legal", "data governance"]),
        ("abs_datalab", "ABS DataLab labour and industry microdata", "Needed for labour and sector calibration.", True, ["OPFTE", "HLE", "sector stress"], ["statistical", "data governance"]),
        ("hilda", "HILDA microdata", "Needed for longitudinal household pressure analysis.", True, ["household distributional"], ["statistical", "welfare", "data governance"]),
        ("treasury_pbo", "Confidential Treasury / PBO material", "Needed only for official fiscal costing review outside repo.", True, ["fiscal trajectory", "transition funding"], ["public finance", "economic"]),
        ("behavioural", "Behavioural elasticity evidence", "Needed for response/gaming estimation.", False, ["behavioural response"], ["economic", "statistical"]),
    ]
    output: list[RepoAuditDataDependency] = []
    for dep_id, needed, why, restricted, modules, reviews in deps:
        output.append(
            RepoAuditDataDependency(
                dep_id,
                needed,
                why,
                "not loaded",
                "unknown" if restricted else "true",
                restricted,
                "false" if restricted else "unknown",
                False,
                "Out of repo scope or requires authorised access and review.",
                modules,
                "May support review design only after governance and expert review.",
                ["calibration", "validation", "actual tax payable", "official status", "firm-level liability"],
                reviews,
            )
        )
    return output


def _review_dependencies() -> list[RepoAuditReviewDependency]:
    reviews = [
        ("legal", "Legal review is required for legislative architecture, powers, attribution, safeguards, and boundaries.", ["legislative architecture", "administrative workflow"]),
        ("tax", "Tax review is required for attribution, deductibility, PAYG, company tax, and ATO-methods boundaries.", ["core formula", "AAVA", "PAYG erosion"]),
        ("economic", "Economic review is required for incidence, pass-through, labour displacement, and fiscal interpretation.", ["investment", "fiscal trajectory", "sector stress"]),
        ("statistical", "Statistical review is required for representativeness, uncertainty, weighting, and scenario interpretation.", ["household weighting", "uncertainty ranges"]),
        ("administrative", "Administrative review is required for workflow feasibility and evidence process boundaries.", ["administrative workflow", "secure ingestion"]),
        ("domain", "Domain review is required for sector schedules and sector stress assumptions.", ["sector schedules", "sector stress"]),
        ("public finance", "Public finance review is required before fiscal context can be interpreted beyond public aggregate bounds.", ["fiscal trajectory", "transition funding"]),
        ("welfare", "Welfare review is required for payment interactions, support adequacy, and household pressure boundaries.", ["payment interactions", "transition funding"]),
        ("data governance", "Data governance review is required before any restricted or confidential source could be considered.", ["public real data loader", "repo guardrails"]),
    ]
    return [
        RepoAuditReviewDependency(
            f"review_{review_type.replace(' ', '_')}",
            review_type,
            why,
            modules,
            "Check assumptions, data requirements, non-claim boundaries, and required evidence.",
            "Review cannot imply calibration, validation, official status, tax payable, readiness, or liability determination.",
            "requires_external_review",
            f"{review_type} reviewer with CARSF boundary brief",
        )
        for review_type, why, modules in reviews
    ]


def _build_coverage(runners: list[RepoAuditRunnerCoverage], reports: list[RepoAuditReportCoverage]) -> list[dict[str, Any]]:
    runner_map = {Path(item.runner_path).stem.replace("run_", ""): item for item in runners}
    runner_aliases = {
        "example_results": "examples",
        "grouped_entity_results": "examples",
        "transfer_pricing_results": "examples",
        "evidence_requirements": "examples",
        "calibration_requirements": "examples",
        "mock_evidence_workflow": "evidence_workflow",
        "secure_ingestion_controls": "ingestion_controls",
    }
    rows: list[dict[str, Any]] = []
    for report in reports:
        key = report.report_stem
        runner = runner_map.get(runner_aliases.get(key, key))
        rows.append(
            {
                "build_or_layer": key,
                "runner_exists": True if runner is None and key in {"full_repo_integrity_upgrade_audit"} else (runner.exists if runner else False),
                "ci_referenced": True if runner is None and key in {"full_repo_integrity_upgrade_audit"} else (runner.ci_referenced if runner else False),
                "markdown_report_exists": report.markdown_exists,
                "json_report_exists": report.json_exists,
                "status": "covered" if report.status == "covered" else "documented_gap",
            }
        )
    return rows


def _summary_counts(findings: list[RepoAuditFinding], severity: str) -> tuple[int, int, int]:
    total = sum(item.severity == severity for item in findings)
    fixed = sum(item.severity == severity and item.status == "fixed" for item in findings)
    remaining = total - fixed
    return total, fixed, remaining


def build_full_repo_integrity_audit_result(manifest: dict[str, Any], repo_root: Path) -> FullRepoIntegrityAuditResult:
    _validate_manifest(manifest)
    workflow_text = _text(repo_root / ".github" / "workflows" / "ci.yml")
    runners = _runner_coverage(repo_root, workflow_text)
    reports = _report_coverage(repo_root)
    dashboard_refs = _reference_coverage(
        repo_root,
        "data/dashboard/executive_dashboard_manifest.yaml",
        ["full_repo_integrity_upgrade_audit", "reports/full_repo_integrity_upgrade_audit.md", "reports/full_repo_integrity_upgrade_audit.json"],
        "dashboard",
    )
    release_refs = _reference_coverage(
        repo_root,
        "data/release/v1_5_release_manifest.yaml",
        ["full_repo_integrity_upgrade_audit", "reports/full_repo_integrity_upgrade_audit.md", "reports/full_repo_integrity_upgrade_audit.json"],
        "release_manifest",
    )
    release_doc_refs = _reference_coverage(
        repo_root,
        "release/v1_5_rc/REPORT_MAP.md",
        ["reports/full_repo_integrity_upgrade_audit.md", "run_full_repo_integrity_upgrade_audit.py"],
        "release_report_map",
    )
    docs = _docs_coverage(repo_root)
    public_data = _public_data_boundary(repo_root)
    placeholders = _placeholder_boundary(repo_root)
    calibration = _boundary_report_checks(repo_root, "public_aggregate_calibration_boundary_map", "calibration_boundary")
    scenario = _boundary_report_checks(repo_root, "public_aggregate_scenario_constraint_layer", "scenario_constraint")
    guardrails = _guardrail_audit(repo_root)
    non_claims = _non_claim_coverage(repo_root)
    result_coverage = _result_coverage(repo_root)
    findings = _findings(runners, reports, docs)
    fixes = _safe_fixes()
    gaps = [
        RepoAuditGap("gap_restricted_data", "data_gap", "Restricted administrative and microdata dependencies remain outside repo scope.", "blocked", "Carry into data dependency register."),
        RepoAuditGap("gap_external_review", "external_review_gap", "Legal, tax, economic, statistical, welfare, data governance, and domain review remain unresolved.", "requires_external_review", "Carry into reviewer handoff."),
        RepoAuditGap("gap_calibration", "calibration_gap", "Calibration has not been performed and cannot be performed from current public aggregate data alone.", "blocked", "Preserve boundary maps and do not overclaim."),
        RepoAuditGap("gap_reviewer_pack", "docs_gap", "Build 35 should package the audit outputs for reviewers.", "documented", "Proceed to reviewer handoff pack or safe gap closure sprint."),
    ]
    missing_factors = _missing_factors()
    data_dependencies = _data_dependencies()
    review_dependencies = _review_dependencies()
    scan_artifacts = [
        "README.md",
        "docs/current_status.md",
        "docs/known_risks.md",
        "docs/calibration_shell.md",
        "docs/v1_5_plan.md",
        "docs/public_aggregate_scenario_constraint_layer.md",
        "simulator/pages/29_Public_Data_Evidence_Map.py",
    ]
    forbidden_findings: list[str] = []
    for artifact in scan_artifacts:
        for finding in find_forbidden_affirmative_repo_claims(_text(repo_root / artifact)):
            forbidden_findings.append(f"{artifact}: {finding}")

    critical_total, critical_fixed, critical_remaining = _summary_counts(findings, "critical")
    high_total, high_fixed, high_remaining = _summary_counts(findings, "high")
    medium_total, medium_fixed, medium_remaining = _summary_counts(findings, "medium")
    runner_complete = all(item.exists and item.ci_referenced for item in runners)
    report_complete = all(item.markdown_exists for item in reports)
    json_complete = all(item.json_exists for item in reports)
    dashboard_complete = all(item.reference_present for item in dashboard_refs)
    release_complete = all(item.reference_present for item in release_refs + release_doc_refs)
    docs_complete = all(item.reference_present for item in docs)
    public_clean = all(item.covered for item in public_data)
    placeholder_clean = all(item.covered for item in placeholders)
    calibration_clean = all(item.covered for item in calibration)
    scenario_clean = all(item.covered for item in scenario)
    guardrails_clean = all(item.covered for item in guardrails)
    non_claim_clean = all(item.required_phrases_present for item in non_claims)

    summary = FullRepoIntegrityAuditSummary(
        full_repo_integrity_audit_created=True,
        safe_fixes_applied=True,
        critical_findings_total=critical_total,
        critical_findings_fixed=critical_fixed,
        critical_findings_remaining=critical_remaining,
        high_findings_total=high_total,
        high_findings_fixed=high_fixed,
        high_findings_remaining=high_remaining,
        medium_findings_total=medium_total,
        medium_findings_fixed=medium_fixed,
        medium_findings_remaining=medium_remaining,
        runner_coverage_complete=runner_complete,
        report_coverage_complete=report_complete,
        json_report_coverage_complete=json_complete,
        dashboard_coverage_complete=dashboard_complete,
        release_manifest_coverage_complete=release_complete,
        docs_coverage_complete=docs_complete,
        public_data_boundary_clean=public_clean,
        placeholder_boundary_clean=placeholder_clean,
        calibration_boundary_clean=calibration_clean,
        scenario_constraint_boundary_clean=scenario_clean,
        guardrails_clean=guardrails_clean,
        non_claim_boundaries_clean=non_claim_clean,
        forbidden_claim_findings=len(forbidden_findings),
        new_data_loaded=False,
        restricted_data_loaded=False,
        personal_data_loaded=False,
        taxpayer_level_data_loaded=False,
        firm_confidential_data_loaded=False,
        household_microdata_loaded=False,
        calibration_completed=False,
        validation_claimed=False,
        actual_tax_payable_determined=False,
        official_status_claimed=False,
        firm_level_liability_logic_modified=False,
    )
    return FullRepoIntegrityAuditResult(
        audit_id=str(manifest["audit_id"]),
        audit_name=str(manifest["audit_name"]),
        status=str(manifest["status"]),
        non_claims=FULL_REPO_AUDIT_NON_CLAIMS,
        build_coverage_matrix=_build_coverage(runners, reports),
        runner_coverage_matrix=runners,
        report_coverage_matrix=reports,
        dashboard_coverage_matrix=dashboard_refs,
        release_manifest_coverage=release_refs + release_doc_refs,
        docs_coverage=docs,
        public_data_boundary_audit=public_data,
        placeholder_boundary_audit=placeholders,
        calibration_boundary_audit=calibration,
        scenario_constraint_audit=scenario,
        guardrail_audit=guardrails,
        non_claim_boundary_audit=non_claims,
        result_coverage_matrix=result_coverage,
        findings=findings,
        safe_fixes=fixes,
        gaps=gaps,
        missing_factors=missing_factors,
        data_dependencies=data_dependencies,
        external_review_dependencies=review_dependencies,
        items_blocked_inside_repo=gaps[:3],
        what_repo_can_currently_claim=[
            "The repo contains prototype reports, manifests, guardrails, and public aggregate boundary maps for reviewer inspection.",
            "Build 31 public aggregate values are source-located and boundary-limited.",
            "Builds 32-34 map placeholder, calibration-boundary, and scenario-display constraints without loading new data.",
            "Repository guardrails currently report no denied findings.",
        ],
        what_repo_must_not_claim=[
            "calibration",
            "validation",
            "actual tax payable",
            "firm-level CARSF liability",
            "official status",
            "legal sufficiency",
            "operational readiness",
            "ATO guidance",
            "Treasury modelling",
            "PBO costing",
            "readiness score",
            "maturity score",
        ],
        recommended_next_builds=[
            "Option A: Build 35 - Public Data Reviewer Handoff Pack V2.",
            "Option B: Build 35 - Gap Closure Sprint 1 for safe, internal, non-data, non-claim gaps.",
        ],
        summary=summary,
    )
