"""Reviewer evidence map for the CARSF V1.5 public-data pilot.

This module maps existing Build 27 public-pilot artefacts into reviewer-facing
evidence rows. It does not load new data, complete calibration, validate the
model, determine tax payable, or modify firm-level CARSF liability.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .public_data_pilot import find_forbidden_affirmative_public_data_claims


EVIDENCE_STATUS_VALUES = {
    "loaded_public_aggregate",
    "source_reference_only",
    "realistic_placeholder_anchor",
    "synthetic_fixture",
    "blocked_by_restricted_data",
    "forbidden_for_repo_use",
}

REVIEWER_INTERPRETATION_VALUES = {
    "inspect_source",
    "inspect_arithmetic",
    "inspect_placeholder_basis",
    "inspect_blocker",
    "inspect_non_claim_boundary",
    "not_evidence_for_calibration",
    "not_evidence_for_tax_payable",
    "not_evidence_for_validation",
}

CONFIDENCE_LABEL_VALUES = {
    "source_locator_recorded",
    "arithmetic_checked",
    "source_reference_only",
    "placeholder_anchor_only",
    "blocked_until_restricted_data_access",
    "external_review_required",
}

PUBLIC_DATA_EVIDENCE_MAP_WARNING = (
    "This is a reviewer evidence map and dashboard for the public data pilot only. No new data is loaded by this build. "
    "Build 27 public aggregate extracts remain sanity-check-only or placeholder-anchor-only. This is not calibration, "
    "calibration has not been completed, public data does not prove the model works, realistic placeholders remain "
    "placeholders, realistic placeholders are not real data, realistic placeholders are not calibrated, source references "
    "are not loaded datasets, and restricted-data requirements are not data access. It is not legal advice, not tax advice, "
    "not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, not statistical "
    "validation, not operational readiness, not legal sufficiency, and not official status. It does not determine actual tax payable, "
    "does not use taxpayer-level data, firm-level confidential data, household microdata, ABS DataLab, HILDA microdata, "
    "DSS/Services Australia records, ATO taxpayer records, Treasury/PBO confidential material, or restricted government data, "
    "and does not modify firm-level CARSF liability. It only maps evidence for reviewer inspection."
)

PUBLIC_DATA_EVIDENCE_MAP_NON_CLAIMS = [
    PUBLIC_DATA_EVIDENCE_MAP_WARNING,
    "Confidence labels are evidence classification labels only; they are not validation scores, not readiness scores, not maturity scores, and not approval.",
    "Source-reference-only records are mapped for review but are not counted as loaded public data.",
    "Reviewer questions are prompts for inspection and do not mean external review has occurred.",
]


@dataclass(frozen=True)
class SourceEvidenceMap:
    evidence_id: str
    source_reference_id: str
    publisher: str
    source_kind: str
    source_url: str
    publication_or_release_name: str
    data_status: str
    claim_level: str
    evidence_status: str
    confidence_label: str
    reviewer_interpretation: list[str]
    what_reviewer_should_check: list[str]
    what_reviewer_must_not_infer: list[str]
    linked_extract_ids: list[str]
    linked_placeholder_anchor_ids: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExtractEvidenceMap:
    evidence_id: str
    extract_id: str
    source_reference_id: str
    data_status: str
    claim_level: str
    evidence_status: str
    confidence_label: str
    values_summary: str
    source_locator: str
    source_value_note: str
    value_review_status: str
    arithmetic_check_status: str
    safe_to_commit: bool
    reviewer_interpretation: list[str]
    what_reviewer_should_check: list[str]
    what_reviewer_must_not_infer: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PlaceholderEvidenceMap:
    evidence_id: str
    anchor_id: str
    field_id: str
    placeholder_name: str
    anchored_to_public_data: bool
    anchor_strength: str
    evidence_status: str
    confidence_label: str
    blocked_by_restricted_data: bool
    missing_data_for_calibration: list[str]
    review_required_before_calibration: list[str]
    what_reviewer_should_check: list[str]
    what_reviewer_must_not_infer: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FieldSanityEvidenceMap:
    evidence_id: str
    check_id: str
    field_id: str
    field_name: str
    check_type: str
    check_status: str
    claim_level: str
    linked_extract_ids: list[str]
    linked_anchor_ids: list[str]
    evidence_status: str
    confidence_label: str
    reviewer_interpretation: list[str]
    finding: str
    reviewer_questions: list[str]
    what_reviewer_must_not_infer: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ModuleSanityEvidenceMap:
    evidence_id: str
    module_id: str
    module_name: str
    result_status: str
    sanity_check_possible: bool
    calibration_possible: bool
    blocked_by_restricted_data: bool
    claim_level: str
    linked_extract_ids: list[str]
    linked_anchor_ids: list[str]
    evidence_status: str
    confidence_label: str
    main_blockers: list[str]
    reviewer_questions: list[str]
    what_reviewer_must_not_infer: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RestrictedBlockerEvidenceMap:
    evidence_id: str
    blocker_id: str
    blocker_type: str
    description: str
    evidence_status: str
    confidence_label: str
    affected_fields: list[str]
    affected_modules: list[str]
    what_reviewer_should_check: list[str]
    what_reviewer_must_not_infer: list[str]
    required_access_or_review: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReviewerQuestion:
    question_id: str
    category: str
    question: str
    reviewer_interpretation: str
    target_evidence_status: str
    must_not_infer: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ReviewerEvidenceMapSummary:
    total_source_evidence_items: int
    total_loaded_public_extract_evidence_items: int
    total_source_reference_only_evidence_items: int
    total_placeholder_evidence_items: int
    total_field_sanity_evidence_items: int
    field_sanity_passed: int
    field_sanity_warning: int
    field_sanity_blocked: int
    total_module_sanity_evidence_items: int
    modules_sanity_check_possible: int
    modules_placeholder_anchor_possible: int
    modules_blocked_by_restricted_data: int
    total_restricted_blocker_items: int
    total_forbidden_repo_data_items: int
    total_reviewer_questions: int
    forbidden_claim_findings: int
    evidence_map_created: bool
    new_data_loaded: bool
    real_public_data_loaded_from_build_27_only: bool
    source_references_mapped: bool
    loaded_public_extracts_mapped: bool
    source_reference_only_records_mapped: bool
    realistic_placeholders_mapped: bool
    restricted_blockers_mapped: bool
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
class ReviewerEvidenceMapResult:
    evidence_map_id: str
    evidence_map_name: str
    status: str
    non_claims: list[str]
    input_artifacts: list[str]
    source_evidence: list[SourceEvidenceMap]
    loaded_extract_evidence: list[ExtractEvidenceMap]
    source_reference_only_evidence: list[ExtractEvidenceMap]
    placeholder_evidence: list[PlaceholderEvidenceMap]
    field_sanity_evidence: list[FieldSanityEvidenceMap]
    module_sanity_evidence: list[ModuleSanityEvidenceMap]
    restricted_blocker_evidence: list[RestrictedBlockerEvidenceMap]
    forbidden_repo_data_evidence: list[RestrictedBlockerEvidenceMap]
    reviewer_questions: list[ReviewerQuestion]
    build_29_requirements: list[str]
    summary: ReviewerEvidenceMapSummary

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _required_mapping(source: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [field for field in fields if field not in source]
    if missing:
        raise ValueError(f"{label} missing required fields: {', '.join(missing)}")


def _list_of_strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{label} must be a non-empty list of strings")
    return list(value)


def _choice(value: str, allowed: set[str], label: str) -> str:
    if value not in allowed:
        raise ValueError(f"{label} has invalid value: {value}")
    return value


def _values_summary(values: list[dict[str, Any]]) -> str:
    if not values:
        return "source reference only"
    return "; ".join(f"{item.get('value_id')}={item.get('value')} {item.get('unit')}" for item in values)


def _linked_extracts(source_reference_id: str, extracts: list[dict[str, Any]]) -> list[str]:
    return [item["extract_id"] for item in extracts if item.get("source_reference_id") == source_reference_id]


def _linked_anchors(source_reference_id: str, anchors: list[dict[str, Any]]) -> list[str]:
    return [item["anchor_id"] for item in anchors if source_reference_id in item.get("anchor_source_reference_ids", [])]


def _extract_has_loaded_status(extract_id: str, extracts_by_id: dict[str, dict[str, Any]]) -> bool:
    extract = extracts_by_id.get(extract_id, {})
    return extract.get("data_status") == "real_public_data_loaded"


def _extract_confidence(extract: dict[str, Any]) -> tuple[str, str]:
    if extract.get("data_status") == "source_reference_only":
        return "source_reference_only", "not_recalculated"
    if extract.get("extract_id") == "fair_work_minimum_wage_2025_extract":
        values = {item.get("value_id"): item.get("value") for item in extract.get("values", [])}
        hourly = values.get("national_minimum_wage_hourly")
        weekly = values.get("national_minimum_wage_weekly")
        if isinstance(hourly, (int, float)) and isinstance(weekly, (int, float)) and abs(round(hourly * 38, 2) - weekly) <= 0.001:
            return "arithmetic_checked", "hourly_times_38_matches_weekly"
        raise ValueError("Fair Work wage arithmetic check is missing or inconsistent")
    return "source_locator_recorded", "source_locator_recorded_not_recalculated"


def _field_evidence_status(check: dict[str, Any], extracts_by_id: dict[str, dict[str, Any]]) -> tuple[str, str, list[str]]:
    if check.get("check_status") == "blocked":
        return "blocked_by_restricted_data", "blocked_until_restricted_data_access", ["inspect_blocker", "not_evidence_for_calibration"]
    extract_ids = check.get("public_extract_ids", [])
    if extract_ids and all(_extract_has_loaded_status(extract_id, extracts_by_id) for extract_id in extract_ids):
        if "fair_work_minimum_wage_2025_extract" in extract_ids:
            return "loaded_public_aggregate", "arithmetic_checked", ["inspect_arithmetic", "not_evidence_for_calibration"]
        return "loaded_public_aggregate", "source_locator_recorded", ["inspect_source", "not_evidence_for_calibration"]
    if extract_ids:
        return "source_reference_only", "source_reference_only", ["inspect_source", "not_evidence_for_calibration"]
    return "realistic_placeholder_anchor", "placeholder_anchor_only", ["inspect_placeholder_basis", "not_evidence_for_calibration"]


def _module_evidence_status(module: dict[str, Any], extracts_by_id: dict[str, dict[str, Any]]) -> tuple[str, str]:
    if module.get("blocked_by_restricted_data"):
        return "blocked_by_restricted_data", "blocked_until_restricted_data_access"
    extract_ids = module.get("public_extract_ids", [])
    if extract_ids and all(_extract_has_loaded_status(extract_id, extracts_by_id) for extract_id in extract_ids):
        return "loaded_public_aggregate", "source_locator_recorded"
    if module.get("placeholder_anchor_ids"):
        return "realistic_placeholder_anchor", "placeholder_anchor_only"
    return "source_reference_only", "source_reference_only"


def _validate_manifest(manifest: dict[str, Any]) -> None:
    _required_mapping(
        manifest,
        [
            "evidence_map_id",
            "evidence_map_name",
            "status",
            "non_claims",
            "input_artifacts",
            "evidence_status_taxonomy",
            "reviewer_interpretation_taxonomy",
            "confidence_label_taxonomy",
            "reviewer_questions",
            "forbidden_claims",
            "build_29_requirements",
        ],
        "public data evidence map manifest",
    )
    if manifest["status"] != "reviewer_evidence_map_only":
        raise ValueError("evidence map status must be reviewer_evidence_map_only")
    for non_claim in PUBLIC_DATA_EVIDENCE_MAP_NON_CLAIMS:
        if non_claim not in manifest["non_claims"]:
            raise ValueError("evidence map manifest missing required non-claim language")
    if set(manifest["evidence_status_taxonomy"]) != EVIDENCE_STATUS_VALUES:
        raise ValueError("evidence status taxonomy does not match required values")
    if set(manifest["reviewer_interpretation_taxonomy"]) != REVIEWER_INTERPRETATION_VALUES:
        raise ValueError("reviewer interpretation taxonomy does not match required values")
    if set(manifest["confidence_label_taxonomy"]) != CONFIDENCE_LABEL_VALUES:
        raise ValueError("confidence label taxonomy does not match required values")
    categories: dict[str, int] = {}
    for item in manifest["reviewer_questions"]:
        _required_mapping(
            item,
            ["question_id", "category", "question", "reviewer_interpretation", "target_evidence_status", "must_not_infer"],
            "reviewer question",
        )
        _choice(str(item["reviewer_interpretation"]), REVIEWER_INTERPRETATION_VALUES, "reviewer question interpretation")
        _choice(str(item["target_evidence_status"]), EVIDENCE_STATUS_VALUES, "reviewer question target evidence status")
        _list_of_strings(item["must_not_infer"], "reviewer question must_not_infer")
        categories[item["category"]] = categories.get(item["category"], 0) + 1
    missing_counts = [category for category, count in categories.items() if count < 5]
    if missing_counts:
        raise ValueError(f"reviewer question categories need at least five questions: {', '.join(missing_counts)}")


def build_public_data_evidence_map_result(
    manifest: dict[str, Any],
    pilot_report: dict[str, Any],
) -> ReviewerEvidenceMapResult:
    _validate_manifest(manifest)
    public_pilot = pilot_report.get("public_data_pilot", {})
    if not public_pilot:
        raise ValueError("public data pilot report is missing public_data_pilot payload")

    sources = public_pilot.get("source_references", [])
    extracts = public_pilot.get("public_aggregate_extracts", [])
    anchors = public_pilot.get("placeholder_anchors", [])
    field_checks = public_pilot.get("field_sanity_checks", [])
    module_checks = public_pilot.get("module_sanity_checks", [])
    restricted_blockers = public_pilot.get("restricted_data_blockers", [])
    forbidden_rules = public_pilot.get("forbidden_data_rules", [])
    extracts_by_id = {item["extract_id"]: item for item in extracts}

    source_evidence = [
        SourceEvidenceMap(
            evidence_id=f"source_{source['source_reference_id']}",
            source_reference_id=source["source_reference_id"],
            publisher=source["publisher"],
            source_kind=source["source_kind"],
            source_url=source["source_url"],
            publication_or_release_name=source["publication_or_release_name"],
            data_status="source_reference",
            claim_level=source["claim_level"],
            evidence_status="source_reference_only",
            confidence_label="source_reference_only" if not source.get("extract_committed") else "source_locator_recorded",
            reviewer_interpretation=["inspect_source", "not_evidence_for_calibration"],
            what_reviewer_should_check=[
                "Check that the source URL and release name can be independently found.",
                "Check whether linked extract rows remain aggregate-only or source-reference-only.",
            ],
            what_reviewer_must_not_infer=["calibration", "validation", "official status", "actual tax payable"],
            linked_extract_ids=_linked_extracts(source["source_reference_id"], extracts),
            linked_placeholder_anchor_ids=_linked_anchors(source["source_reference_id"], anchors),
        )
        for source in sources
    ]

    extract_evidence: list[ExtractEvidenceMap] = []
    for extract in extracts:
        confidence, arithmetic_status = _extract_confidence(extract)
        evidence_status = "loaded_public_aggregate" if extract["data_status"] == "real_public_data_loaded" else "source_reference_only"
        interpretation = ["inspect_source", "not_evidence_for_calibration", "not_evidence_for_tax_payable"]
        if confidence == "arithmetic_checked":
            interpretation = ["inspect_arithmetic", "inspect_source", "not_evidence_for_calibration"]
        item = ExtractEvidenceMap(
            evidence_id=f"extract_{extract['extract_id']}",
            extract_id=extract["extract_id"],
            source_reference_id=extract["source_reference_id"],
            data_status=extract["data_status"],
            claim_level=extract["claim_level"],
            evidence_status=evidence_status,
            confidence_label=confidence,
            values_summary=_values_summary(extract.get("values", [])),
            source_locator=extract.get("source_locator", ""),
            source_value_note=extract.get("source_value_note", ""),
            value_review_status=extract.get("value_review_status", ""),
            arithmetic_check_status=arithmetic_status,
            safe_to_commit=bool(extract.get("safe_to_commit")),
            reviewer_interpretation=interpretation,
            what_reviewer_should_check=[
                "Check the source locator and value note before interpreting the row.",
                "Check that the row is still labelled sanity-check-only or placeholder-anchor-only.",
            ],
            what_reviewer_must_not_infer=["calibration", "validation", "ATO guidance", "Treasury modelling", "actual tax payable"],
        )
        if item.evidence_status == "loaded_public_aggregate" and (not item.source_locator or not item.value_review_status):
            raise ValueError(f"loaded public extract evidence lacks source locator or review status: {item.extract_id}")
        extract_evidence.append(item)

    placeholder_evidence = [
        PlaceholderEvidenceMap(
            evidence_id=f"placeholder_{anchor['anchor_id']}",
            anchor_id=anchor["anchor_id"],
            field_id=anchor["field_id"],
            placeholder_name=anchor["placeholder_name"],
            anchored_to_public_data=bool(anchor["anchored_to_public_data"]),
            anchor_strength=anchor["anchor_strength"],
            evidence_status="realistic_placeholder_anchor",
            confidence_label="source_reference_only" if anchor["anchor_strength"] == "source_reference_only" else "placeholder_anchor_only",
            blocked_by_restricted_data=bool(anchor["blocked_by_restricted_data"]),
            missing_data_for_calibration=list(anchor["missing_data_for_calibration"]),
            review_required_before_calibration=list(anchor["review_required_before_calibration"]),
            what_reviewer_should_check=[
                "Check whether the anchor source supports only placeholder review.",
                "Check whether missing data for calibration is still explicit.",
            ],
            what_reviewer_must_not_infer=["real data replacement", "calibration", "validation", "actual tax payable"],
        )
        for anchor in anchors
    ]

    field_evidence: list[FieldSanityEvidenceMap] = []
    for check in field_checks:
        evidence_status, confidence, interpretation = _field_evidence_status(check, extracts_by_id)
        field_evidence.append(
            FieldSanityEvidenceMap(
                evidence_id=f"field_{check['check_id']}",
                check_id=check["check_id"],
                field_id=check["field_id"],
                field_name=check["field_name"],
                check_type=check["check_type"],
                check_status=check["check_status"],
                claim_level=check["claim_level"],
                linked_extract_ids=list(check["public_extract_ids"]),
                linked_anchor_ids=list(check["placeholder_anchor_ids"]),
                evidence_status=evidence_status,
                confidence_label=confidence,
                reviewer_interpretation=interpretation,
                finding=check["finding"],
                reviewer_questions=[
                    "Does the linked extract remain source-located or source-reference-only?",
                    "Is the finding being read only as a sanity-check map?",
                ],
                what_reviewer_must_not_infer=["calibration", "validation", "actual tax payable"],
            )
        )

    module_evidence: list[ModuleSanityEvidenceMap] = []
    for module in module_checks:
        if module.get("calibration_possible") is not False:
            raise ValueError(f"module sanity check has calibration_possible true: {module['module_id']}")
        evidence_status, confidence = _module_evidence_status(module, extracts_by_id)
        module_evidence.append(
            ModuleSanityEvidenceMap(
                evidence_id=f"module_{module['module_id']}",
                module_id=module["module_id"],
                module_name=module["module_name"],
                result_status=module["result_status"],
                sanity_check_possible=bool(module["sanity_check_possible"]),
                calibration_possible=False,
                blocked_by_restricted_data=bool(module["blocked_by_restricted_data"]),
                claim_level=module["claim_level"],
                linked_extract_ids=list(module["public_extract_ids"]),
                linked_anchor_ids=list(module["placeholder_anchor_ids"]),
                evidence_status=evidence_status,
                confidence_label=confidence,
                main_blockers=list(module["main_blockers"]),
                reviewer_questions=[
                    "Does this module remain sanity-check-only or placeholder-anchor-only?",
                    "Are restricted-data blockers still preserved?",
                ],
                what_reviewer_must_not_infer=["calibration", "validation", "model proof", "operational readiness"],
            )
        )

    restricted_evidence = [
        RestrictedBlockerEvidenceMap(
            evidence_id=f"restricted_{item['blocker_id']}",
            blocker_id=item["blocker_id"],
            blocker_type="restricted_data_blocker",
            description=item["blocker"],
            evidence_status="blocked_by_restricted_data",
            confidence_label="blocked_until_restricted_data_access",
            affected_fields=[],
            affected_modules=list(item.get("affected_modules", [])),
            what_reviewer_should_check=["Check that the blocker remains visible and unresolved."],
            what_reviewer_must_not_infer=["data access", "calibration", "validation"],
            required_access_or_review=["authorised external data access process", "privacy and legal review"],
        )
        for item in restricted_blockers
    ]
    forbidden_evidence = [
        RestrictedBlockerEvidenceMap(
            evidence_id=f"forbidden_{item['rule_id']}",
            blocker_id=item["rule_id"],
            blocker_type="forbidden_repo_data",
            description=item["forbidden_data_type"],
            evidence_status="forbidden_for_repo_use",
            confidence_label="external_review_required",
            affected_fields=[],
            affected_modules=[],
            what_reviewer_should_check=["Check that forbidden data remains excluded from the repository."],
            what_reviewer_must_not_infer=["data access", "safe repository use", "calibration"],
            required_access_or_review=["external system design if ever authorised", "legal and privacy review"],
        )
        for item in forbidden_rules
    ]

    reviewer_questions = [
        ReviewerQuestion(
            question_id=item["question_id"],
            category=item["category"],
            question=item["question"],
            reviewer_interpretation=item["reviewer_interpretation"],
            target_evidence_status=item["target_evidence_status"],
            must_not_infer=list(item["must_not_infer"]),
        )
        for item in manifest["reviewer_questions"]
    ]

    loaded_extracts = [item for item in extract_evidence if item.evidence_status == "loaded_public_aggregate"]
    source_reference_only = [item for item in extract_evidence if item.evidence_status == "source_reference_only"]
    if any(item.extract_id == "fair_work_minimum_wage_2025_extract" and item.confidence_label != "arithmetic_checked" for item in extract_evidence):
        raise ValueError("Fair Work wage extract must be represented as arithmetic_checked")
    for item in extract_evidence:
        text = (item.confidence_label + " " + item.value_review_status + " " + item.source_value_note).lower()
        if "treasury validated" in text or "ato validated" in text or "ato guidance" in text:
            raise ValueError(f"extract evidence overclaims source status: {item.extract_id}")

    summary = ReviewerEvidenceMapSummary(
        total_source_evidence_items=len(source_evidence),
        total_loaded_public_extract_evidence_items=len(loaded_extracts),
        total_source_reference_only_evidence_items=len(source_reference_only),
        total_placeholder_evidence_items=len(placeholder_evidence),
        total_field_sanity_evidence_items=len(field_evidence),
        field_sanity_passed=sum(item.check_status == "passed" for item in field_evidence),
        field_sanity_warning=sum(item.check_status == "warning" for item in field_evidence),
        field_sanity_blocked=sum(item.check_status == "blocked" for item in field_evidence),
        total_module_sanity_evidence_items=len(module_evidence),
        modules_sanity_check_possible=sum(item.result_status == "sanity_check_possible" for item in module_evidence),
        modules_placeholder_anchor_possible=sum(item.result_status == "placeholder_anchor_possible" for item in module_evidence),
        modules_blocked_by_restricted_data=sum(item.blocked_by_restricted_data for item in module_evidence),
        total_restricted_blocker_items=len(restricted_evidence),
        total_forbidden_repo_data_items=len(forbidden_evidence),
        total_reviewer_questions=len(reviewer_questions),
        forbidden_claim_findings=0,
        evidence_map_created=True,
        new_data_loaded=False,
        real_public_data_loaded_from_build_27_only=bool(loaded_extracts),
        source_references_mapped=bool(source_evidence),
        loaded_public_extracts_mapped=bool(loaded_extracts),
        source_reference_only_records_mapped=bool(source_reference_only),
        realistic_placeholders_mapped=bool(placeholder_evidence),
        restricted_blockers_mapped=bool(restricted_evidence),
        real_calibration_completed=False,
        actual_tax_payable_determined=False,
        validation_claimed=False,
        approval_claimed=False,
        operational_readiness_claimed=False,
        legal_sufficiency_claimed=False,
        official_status_claimed=False,
        firm_level_liability_logic_modified=False,
    )

    result = ReviewerEvidenceMapResult(
        evidence_map_id=str(manifest["evidence_map_id"]),
        evidence_map_name=str(manifest["evidence_map_name"]),
        status=str(manifest["status"]),
        non_claims=list(manifest["non_claims"]),
        input_artifacts=list(manifest["input_artifacts"]),
        source_evidence=source_evidence,
        loaded_extract_evidence=loaded_extracts,
        source_reference_only_evidence=source_reference_only,
        placeholder_evidence=placeholder_evidence,
        field_sanity_evidence=field_evidence,
        module_sanity_evidence=module_evidence,
        restricted_blocker_evidence=restricted_evidence,
        forbidden_repo_data_evidence=forbidden_evidence,
        reviewer_questions=reviewer_questions,
        build_29_requirements=list(manifest["build_29_requirements"]),
        summary=summary,
    )
    findings = find_forbidden_affirmative_public_data_claims(str(result.to_jsonable()))
    if findings:
        raise ValueError(f"public data evidence map contains forbidden affirmative claims: {', '.join(findings)}")
    return result
