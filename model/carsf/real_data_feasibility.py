"""Real-data feasibility and calibration-intake mapping for CARSF V1.5.

This module inventories possible data sources, field needs, placeholder
provenance requirements, restricted-data blockers, and forbidden repo data.
It does not load real datasets, complete calibration, validate CARSF as a real
tax model, or modify firm-level CARSF liability.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


DATA_STATUS_VALUES = {
    "real_public_data_candidate",
    "real_public_data_loaded",
    "restricted_data_required",
    "realistic_placeholder",
    "synthetic_fixture",
    "forbidden_repo_data",
    "not_collected",
    "external_review_required",
}

ACCESS_CLASS_VALUES = {
    "public_open",
    "public_manual_download",
    "public_api_available",
    "licence_required",
    "restricted_research_access",
    "government_internal_only",
    "confidential_or_prohibited",
    "unknown",
}

CLAIM_LEVEL_VALUES = {
    "inventory_only",
    "feasibility_only",
    "sanity_check_only",
    "placeholder_anchor_only",
    "calibration_candidate_only",
    "external_review_only",
    "forbidden_for_model_use",
}

REAL_DATA_FEASIBILITY_WARNING = (
    "This is a feasibility and calibration-intake map only. No real data has been loaded by this build, "
    "no calibration has occurred, realistic placeholders are not real data and are not calibrated, "
    "public-data candidates are not loaded datasets, and restricted-data requirements are not data access. "
    "It is not legal advice, tax advice, ATO guidance, Treasury modelling, economic validation, welfare validation, "
    "statistical validation, operational readiness, legal sufficiency, official status, and does not determine actual tax payable. "
    "It does not use taxpayer-level, firm-level confidential, household microdata, ABS DataLab, HILDA microdata, "
    "DSS/Services Australia records, ATO records, Treasury/PBO confidential material, or restricted government data, "
    "and does not modify firm-level CARSF liability."
)

REAL_DATA_FEASIBILITY_NON_CLAIMS = [
    REAL_DATA_FEASIBILITY_WARNING,
    "The map only separates public-data candidates, restricted-data requirements, realistic placeholders, synthetic fixtures, forbidden repo data, and public-data pilot readiness.",
    "Build 26 performs feasibility mapping only; any future public-data pilot must keep loaded public aggregates separate from placeholders and restricted-data needs.",
]

FORBIDDEN_AFFIRMATIVE_REAL_DATA_CLAIMS = [
    "calibrated",
    "calibration completed",
    "real data loaded",
    "public data proves",
    "model works",
    "tax model works",
    "ready for government",
    "ready for ato",
    "operationally ready",
    "legally sufficient",
    "official status",
    "official policy",
    "validated",
    "externally validated",
    "treasury validated",
    "ato validated",
    "economic validation complete",
    "welfare validation complete",
    "statistical validation complete",
    "actual tax payable",
    "real household estimate",
    "population estimate",
    "official sector ranking",
    "compliance score",
    "readiness score",
    "approved",
]

NEGATIVE_CONTEXT_MARKERS = [
    "not ",
    "not a ",
    "not an ",
    "no ",
    "no real ",
    "does not ",
    "do not ",
    "must not ",
    "must_not",
    "must_not_be_used_for",
    "not_",
    "without ",
    "is not ",
    "are not ",
    "has not ",
    "have not ",
    "cannot ",
    "forbidden",
    "prohibited",
    "negative warning",
    "boundary",
    "non-claim",
    "prevent ",
    "overread ",
    "missing_real_source",
    "can_be_calibrated_from_public_data_only",
    "can_be_",
    "if ever ",
]

RESTRICTED_ACCESS_CLASSES = {
    "licence_required",
    "restricted_research_access",
    "government_internal_only",
    "confidential_or_prohibited",
}

PUBLIC_ACCESS_CLASSES = {"public_open", "public_manual_download", "public_api_available"}


@dataclass(frozen=True)
class DataSourceCandidate:
    source_id: str
    source_name: str
    publisher: str
    source_category: str
    access_class: str
    data_status: str
    public_url_required_later: bool
    licence_or_access_notes: str
    candidate_fields: list[str]
    candidate_modules: list[str]
    claim_level: str
    can_be_committed_to_repo: bool
    requires_external_access_process: bool
    privacy_or_confidentiality_risk: str
    main_use: str
    must_not_be_used_for: list[str]
    review_required: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CalibrationFieldRequirement:
    field_id: str
    field_name: str
    current_status: str
    required_data_status: str
    candidate_sources: list[str]
    restricted_sources_needed: list[str]
    placeholder_allowed: bool
    realistic_placeholder_allowed: bool
    placeholder_basis_required: str
    can_be_publicly_sanity_checked: bool
    can_be_calibrated_from_public_data_only: bool
    requires_external_review: bool
    required_review_tracks: list[str]
    must_not_claim: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ModuleDataNeed:
    module_id: str
    module_name: str
    current_data_status: str
    can_use_public_aggregate_data: bool
    can_only_use_synthetic_data: bool
    requires_restricted_data_for_calibration: bool
    forbidden_data_types: list[str]
    candidate_public_sources: list[str]
    required_restricted_sources: list[str]
    realistic_placeholder_fields: list[str]
    sanity_check_possible: bool
    calibration_possible_now: bool
    main_blockers: list[str]
    must_not_claim: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RealisticPlaceholderSpec:
    placeholder_id: str
    field_id: str
    placeholder_name: str
    basis_type: str
    allowed_anchor_sources: list[str]
    missing_real_source: str
    reason_placeholder_needed: str
    data_status: str
    must_be_labelled_realistic_placeholder: bool
    must_not_be_labelled_real_data: bool
    must_not_be_labelled_calibrated: bool
    must_not_claim: list[str]
    review_required_before_replacement: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RestrictedDataRequirement:
    requirement_id: str
    data_need: str
    restricted_sources: list[str]
    affected_fields: list[str]
    affected_modules: list[str]
    access_class: str
    can_be_committed_to_repo: bool
    reason: str
    review_required: list[str]
    must_not_claim: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ForbiddenDataRule:
    rule_id: str
    forbidden_data_type: str
    reason: str
    allowed_handling: str
    must_not_commit_to_repo: bool
    must_not_use_in_tests: bool
    external_system_required_if_ever_authorised: bool
    guardrail_expected: str
    non_claim: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicDataPilotCandidate:
    pilot_id: str
    source_candidate_id: str
    pilot_name: str
    why_useful: str
    candidate_modules: list[str]
    safe_to_commit_if_public_licence_allows: bool
    expected_file_type: str
    expected_update_frequency: str
    manual_download_or_api: str
    fields_to_extract: list[str]
    claim_level: str
    must_not_claim: list[str]
    build_27_ready: bool
    blockers_before_loading: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CalibrationIntakeSummary:
    total_source_candidates: int
    public_source_candidates: int
    restricted_source_candidates: int
    forbidden_repo_sources: int
    total_calibration_fields: int
    fields_public_sanity_check_possible: int
    fields_public_calibration_possible: int
    fields_requiring_restricted_data: int
    total_realistic_placeholders: int
    total_forbidden_data_rules: int
    total_public_data_pilot_candidates: int
    build_27_ready_candidates: int
    real_data_loaded: bool
    real_calibration_completed: bool
    restricted_data_loaded: bool
    taxpayer_data_loaded: bool
    firm_level_confidential_data_loaded: bool
    household_microdata_loaded: bool
    realistic_placeholders_created: bool
    placeholders_labelled: bool
    public_data_pilot_ready: bool
    validation_claimed: bool
    approval_claimed: bool
    operational_readiness_claimed: bool
    legal_sufficiency_claimed: bool
    official_status_claimed: bool
    firm_level_liability_logic_modified: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CalibrationIntakeResult:
    map_id: str
    map_name: str
    status: str
    non_claims: list[str]
    data_status_taxonomy: list[str]
    access_class_taxonomy: list[str]
    claim_level_taxonomy: list[str]
    source_candidates: list[DataSourceCandidate]
    calibration_fields: list[CalibrationFieldRequirement]
    module_data_needs: list[ModuleDataNeed]
    realistic_placeholders: list[RealisticPlaceholderSpec]
    restricted_data_requirements: list[RestrictedDataRequirement]
    forbidden_data_rules: list[ForbiddenDataRule]
    public_data_pilot_candidates: list[PublicDataPilotCandidate]
    external_review_routes: list[dict[str, Any]]
    forbidden_claims: list[str]
    summary: CalibrationIntakeSummary
    warnings: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        data = asdict(self)
        data["summary"] = self.summary.to_jsonable()
        return data


def _required_mapping(source: dict[str, Any], required: list[str], label: str) -> None:
    missing = [key for key in required if key not in source]
    if missing:
        raise ValueError(f"{label} missing required fields: {', '.join(missing)}")


def _list_of_strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{label} must be a list of strings")
    return value


def _bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be boolean")
    return value


def _validate_choice(value: str, allowed: set[str], label: str) -> str:
    if value not in allowed:
        raise ValueError(f"{label} has invalid value: {value}")
    return value


def _has_non_claim_language(text: str) -> bool:
    lowered = text.lower()
    required = ["no real data", "no calibration", "not legal advice", "does not modify firm-level carsf liability"]
    return all(term in lowered for term in required)


def _phrase_has_negative_context(text: str, start: int) -> bool:
    prefix = text[max(0, start - 180) : start].lower()
    return any(marker in prefix for marker in NEGATIVE_CONTEXT_MARKERS)


def _inside_forbidden_claim_inventory(text: str, start: int) -> bool:
    prefix = text[:start].lower()
    last_key = max(prefix.rfind("forbidden_claims"), prefix.rfind("forbidden claims"))
    if last_key == -1:
        return False
    last_list_close = prefix.rfind("]")
    last_section_break = prefix.rfind("\n")
    return last_key > last_list_close or last_key > last_section_break


def find_forbidden_affirmative_real_data_claims(text: str) -> list[str]:
    lowered = text.lower()
    findings: list[str] = []
    for phrase in FORBIDDEN_AFFIRMATIVE_REAL_DATA_CLAIMS:
        start = 0
        while True:
            idx = lowered.find(phrase, start)
            if idx == -1:
                break
            if not _phrase_has_negative_context(lowered, idx) and not _inside_forbidden_claim_inventory(lowered, idx):
                findings.append(phrase)
                break
            start = idx + len(phrase)
    return sorted(set(findings))


def _source_from_mapping(source: dict[str, Any]) -> DataSourceCandidate:
    _required_mapping(
        source,
        [
            "source_id",
            "source_name",
            "publisher",
            "source_category",
            "access_class",
            "data_status",
            "public_url_required_later",
            "licence_or_access_notes",
            "candidate_fields",
            "candidate_modules",
            "claim_level",
            "can_be_committed_to_repo",
            "requires_external_access_process",
            "privacy_or_confidentiality_risk",
            "main_use",
            "must_not_be_used_for",
            "review_required",
        ],
        "source candidate",
    )
    access_class = _validate_choice(str(source["access_class"]), ACCESS_CLASS_VALUES, f"source {source['source_id']}.access_class")
    data_status = _validate_choice(str(source["data_status"]), DATA_STATUS_VALUES, f"source {source['source_id']}.data_status")
    claim_level = _validate_choice(str(source["claim_level"]), CLAIM_LEVEL_VALUES, f"source {source['source_id']}.claim_level")
    can_commit = _bool(source["can_be_committed_to_repo"], f"source {source['source_id']}.can_be_committed_to_repo")
    if access_class in RESTRICTED_ACCESS_CLASSES and can_commit:
        raise ValueError(f"restricted or confidential source cannot be committed to repo: {source['source_id']}")
    if data_status in {"restricted_data_required", "forbidden_repo_data"} and can_commit:
        raise ValueError(f"restricted or forbidden source cannot be committed to repo: {source['source_id']}")
    return DataSourceCandidate(
        source_id=str(source["source_id"]),
        source_name=str(source["source_name"]),
        publisher=str(source["publisher"]),
        source_category=str(source["source_category"]),
        access_class=access_class,
        data_status=data_status,
        public_url_required_later=_bool(source["public_url_required_later"], f"source {source['source_id']}.public_url_required_later"),
        licence_or_access_notes=str(source["licence_or_access_notes"]),
        candidate_fields=_list_of_strings(source["candidate_fields"], f"source {source['source_id']}.candidate_fields"),
        candidate_modules=_list_of_strings(source["candidate_modules"], f"source {source['source_id']}.candidate_modules"),
        claim_level=claim_level,
        can_be_committed_to_repo=can_commit,
        requires_external_access_process=_bool(source["requires_external_access_process"], f"source {source['source_id']}.requires_external_access_process"),
        privacy_or_confidentiality_risk=str(source["privacy_or_confidentiality_risk"]),
        main_use=str(source["main_use"]),
        must_not_be_used_for=_list_of_strings(source["must_not_be_used_for"], f"source {source['source_id']}.must_not_be_used_for"),
        review_required=_list_of_strings(source["review_required"], f"source {source['source_id']}.review_required"),
    )


def _field_from_mapping(source: dict[str, Any], source_ids: set[str]) -> CalibrationFieldRequirement:
    _required_mapping(
        source,
        [
            "field_id",
            "field_name",
            "current_status",
            "required_data_status",
            "candidate_sources",
            "restricted_sources_needed",
            "placeholder_allowed",
            "realistic_placeholder_allowed",
            "placeholder_basis_required",
            "can_be_publicly_sanity_checked",
            "can_be_calibrated_from_public_data_only",
            "requires_external_review",
            "required_review_tracks",
            "must_not_claim",
        ],
        "calibration field",
    )
    candidate_sources = _list_of_strings(source["candidate_sources"], f"field {source['field_id']}.candidate_sources")
    restricted_sources = _list_of_strings(source["restricted_sources_needed"], f"field {source['field_id']}.restricted_sources_needed")
    unknown = sorted((set(candidate_sources) | set(restricted_sources)) - source_ids)
    if unknown:
        raise ValueError(f"calibration field references unknown source candidate: {source['field_id']}: {', '.join(unknown)}")
    if not candidate_sources:
        raise ValueError(f"calibration field must have candidate sources: {source['field_id']}")
    must_not_claim = _list_of_strings(source["must_not_claim"], f"field {source['field_id']}.must_not_claim")
    if not must_not_claim:
        raise ValueError(f"calibration field must include must_not_claim: {source['field_id']}")
    return CalibrationFieldRequirement(
        field_id=str(source["field_id"]),
        field_name=str(source["field_name"]),
        current_status=_validate_choice(str(source["current_status"]), DATA_STATUS_VALUES, f"field {source['field_id']}.current_status"),
        required_data_status=_validate_choice(str(source["required_data_status"]), DATA_STATUS_VALUES, f"field {source['field_id']}.required_data_status"),
        candidate_sources=candidate_sources,
        restricted_sources_needed=restricted_sources,
        placeholder_allowed=_bool(source["placeholder_allowed"], f"field {source['field_id']}.placeholder_allowed"),
        realistic_placeholder_allowed=_bool(source["realistic_placeholder_allowed"], f"field {source['field_id']}.realistic_placeholder_allowed"),
        placeholder_basis_required=str(source["placeholder_basis_required"]),
        can_be_publicly_sanity_checked=_bool(source["can_be_publicly_sanity_checked"], f"field {source['field_id']}.can_be_publicly_sanity_checked"),
        can_be_calibrated_from_public_data_only=_bool(source["can_be_calibrated_from_public_data_only"], f"field {source['field_id']}.can_be_calibrated_from_public_data_only"),
        requires_external_review=_bool(source["requires_external_review"], f"field {source['field_id']}.requires_external_review"),
        required_review_tracks=_list_of_strings(source["required_review_tracks"], f"field {source['field_id']}.required_review_tracks"),
        must_not_claim=must_not_claim,
    )


def _module_from_mapping(source: dict[str, Any], source_ids: set[str], field_ids: set[str]) -> ModuleDataNeed:
    _required_mapping(
        source,
        [
            "module_id",
            "module_name",
            "current_data_status",
            "can_use_public_aggregate_data",
            "can_only_use_synthetic_data",
            "requires_restricted_data_for_calibration",
            "forbidden_data_types",
            "candidate_public_sources",
            "required_restricted_sources",
            "realistic_placeholder_fields",
            "sanity_check_possible",
            "calibration_possible_now",
            "main_blockers",
            "must_not_claim",
        ],
        "module data need",
    )
    candidate_public_sources = _list_of_strings(source["candidate_public_sources"], f"module {source['module_id']}.candidate_public_sources")
    required_restricted_sources = _list_of_strings(source["required_restricted_sources"], f"module {source['module_id']}.required_restricted_sources")
    source_refs = set(candidate_public_sources) | set(required_restricted_sources)
    unknown_sources = sorted(source_refs - source_ids)
    if unknown_sources:
        raise ValueError(f"module data need references unknown source candidate: {source['module_id']}: {', '.join(unknown_sources)}")
    field_refs = set(_list_of_strings(source["realistic_placeholder_fields"], f"module {source['module_id']}.realistic_placeholder_fields"))
    unknown_fields = sorted(field_refs - field_ids)
    if unknown_fields:
        raise ValueError(f"module data need references unknown field: {source['module_id']}: {', '.join(unknown_fields)}")
    blockers = _list_of_strings(source["main_blockers"], f"module {source['module_id']}.main_blockers")
    must_not_claim = _list_of_strings(source["must_not_claim"], f"module {source['module_id']}.must_not_claim")
    if not blockers:
        raise ValueError(f"module data need must include blockers: {source['module_id']}")
    if not must_not_claim:
        raise ValueError(f"module data need must include must_not_claim: {source['module_id']}")
    return ModuleDataNeed(
        module_id=str(source["module_id"]),
        module_name=str(source["module_name"]),
        current_data_status=_validate_choice(str(source["current_data_status"]), DATA_STATUS_VALUES, f"module {source['module_id']}.current_data_status"),
        can_use_public_aggregate_data=_bool(source["can_use_public_aggregate_data"], f"module {source['module_id']}.can_use_public_aggregate_data"),
        can_only_use_synthetic_data=_bool(source["can_only_use_synthetic_data"], f"module {source['module_id']}.can_only_use_synthetic_data"),
        requires_restricted_data_for_calibration=_bool(source["requires_restricted_data_for_calibration"], f"module {source['module_id']}.requires_restricted_data_for_calibration"),
        forbidden_data_types=_list_of_strings(source["forbidden_data_types"], f"module {source['module_id']}.forbidden_data_types"),
        candidate_public_sources=candidate_public_sources,
        required_restricted_sources=required_restricted_sources,
        realistic_placeholder_fields=sorted(field_refs),
        sanity_check_possible=_bool(source["sanity_check_possible"], f"module {source['module_id']}.sanity_check_possible"),
        calibration_possible_now=_bool(source["calibration_possible_now"], f"module {source['module_id']}.calibration_possible_now"),
        main_blockers=blockers,
        must_not_claim=must_not_claim,
    )


def _placeholder_from_mapping(source: dict[str, Any], field_ids: set[str], source_ids: set[str]) -> RealisticPlaceholderSpec:
    _required_mapping(
        source,
        [
            "placeholder_id",
            "field_id",
            "placeholder_name",
            "basis_type",
            "allowed_anchor_sources",
            "missing_real_source",
            "reason_placeholder_needed",
            "data_status",
            "must_be_labelled_realistic_placeholder",
            "must_not_be_labelled_real_data",
            "must_not_be_labelled_calibrated",
            "must_not_claim",
            "review_required_before_replacement",
        ],
        "realistic placeholder",
    )
    field_id = str(source["field_id"])
    if field_id not in field_ids:
        raise ValueError(f"realistic placeholder references unknown field: {source['placeholder_id']}: {field_id}")
    anchors = _list_of_strings(source["allowed_anchor_sources"], f"placeholder {source['placeholder_id']}.allowed_anchor_sources")
    unknown_sources = sorted(set(anchors) - source_ids)
    if unknown_sources:
        raise ValueError(f"realistic placeholder references unknown anchor source: {source['placeholder_id']}: {', '.join(unknown_sources)}")
    data_status = _validate_choice(str(source["data_status"]), DATA_STATUS_VALUES, f"placeholder {source['placeholder_id']}.data_status")
    if data_status != "realistic_placeholder":
        raise ValueError(f"realistic placeholder must have data_status realistic_placeholder: {source['placeholder_id']}")
    labelled = _bool(source["must_be_labelled_realistic_placeholder"], f"placeholder {source['placeholder_id']}.must_be_labelled_realistic_placeholder")
    not_real = _bool(source["must_not_be_labelled_real_data"], f"placeholder {source['placeholder_id']}.must_not_be_labelled_real_data")
    not_calibrated = _bool(source["must_not_be_labelled_calibrated"], f"placeholder {source['placeholder_id']}.must_not_be_labelled_calibrated")
    if not (labelled and not_real and not_calibrated):
        raise ValueError(f"realistic placeholder labelling safeguards failed: {source['placeholder_id']}")
    return RealisticPlaceholderSpec(
        placeholder_id=str(source["placeholder_id"]),
        field_id=field_id,
        placeholder_name=str(source["placeholder_name"]),
        basis_type=str(source["basis_type"]),
        allowed_anchor_sources=anchors,
        missing_real_source=str(source["missing_real_source"]),
        reason_placeholder_needed=str(source["reason_placeholder_needed"]),
        data_status=data_status,
        must_be_labelled_realistic_placeholder=labelled,
        must_not_be_labelled_real_data=not_real,
        must_not_be_labelled_calibrated=not_calibrated,
        must_not_claim=_list_of_strings(source["must_not_claim"], f"placeholder {source['placeholder_id']}.must_not_claim"),
        review_required_before_replacement=_list_of_strings(source["review_required_before_replacement"], f"placeholder {source['placeholder_id']}.review_required_before_replacement"),
    )


def _restricted_requirement_from_mapping(source: dict[str, Any], source_ids: set[str], field_ids: set[str], module_ids: set[str]) -> RestrictedDataRequirement:
    _required_mapping(
        source,
        ["requirement_id", "data_need", "restricted_sources", "affected_fields", "affected_modules", "access_class", "can_be_committed_to_repo", "reason", "review_required", "must_not_claim"],
        "restricted data requirement",
    )
    restricted_sources = _list_of_strings(source["restricted_sources"], f"restricted {source['requirement_id']}.restricted_sources")
    unknown_sources = sorted(set(restricted_sources) - source_ids)
    if unknown_sources:
        raise ValueError(f"restricted requirement references unknown source: {source['requirement_id']}: {', '.join(unknown_sources)}")
    fields = _list_of_strings(source["affected_fields"], f"restricted {source['requirement_id']}.affected_fields")
    unknown_fields = sorted(set(fields) - field_ids)
    if unknown_fields:
        raise ValueError(f"restricted requirement references unknown field: {source['requirement_id']}: {', '.join(unknown_fields)}")
    modules = _list_of_strings(source["affected_modules"], f"restricted {source['requirement_id']}.affected_modules")
    unknown_modules = sorted(set(modules) - module_ids)
    if unknown_modules:
        raise ValueError(f"restricted requirement references unknown module: {source['requirement_id']}: {', '.join(unknown_modules)}")
    access_class = _validate_choice(str(source["access_class"]), ACCESS_CLASS_VALUES, f"restricted {source['requirement_id']}.access_class")
    can_commit = _bool(source["can_be_committed_to_repo"], f"restricted {source['requirement_id']}.can_be_committed_to_repo")
    if can_commit:
        raise ValueError(f"restricted requirement cannot be committed to repo: {source['requirement_id']}")
    return RestrictedDataRequirement(
        requirement_id=str(source["requirement_id"]),
        data_need=str(source["data_need"]),
        restricted_sources=restricted_sources,
        affected_fields=fields,
        affected_modules=modules,
        access_class=access_class,
        can_be_committed_to_repo=can_commit,
        reason=str(source["reason"]),
        review_required=_list_of_strings(source["review_required"], f"restricted {source['requirement_id']}.review_required"),
        must_not_claim=_list_of_strings(source["must_not_claim"], f"restricted {source['requirement_id']}.must_not_claim"),
    )


def _forbidden_rule_from_mapping(source: dict[str, Any]) -> ForbiddenDataRule:
    _required_mapping(
        source,
        [
            "rule_id",
            "forbidden_data_type",
            "reason",
            "allowed_handling",
            "must_not_commit_to_repo",
            "must_not_use_in_tests",
            "external_system_required_if_ever_authorised",
            "guardrail_expected",
            "non_claim",
        ],
        "forbidden data rule",
    )
    must_not_commit = _bool(source["must_not_commit_to_repo"], f"forbidden {source['rule_id']}.must_not_commit_to_repo")
    if not must_not_commit:
        raise ValueError(f"forbidden data rule must block repo commits: {source['rule_id']}")
    return ForbiddenDataRule(
        rule_id=str(source["rule_id"]),
        forbidden_data_type=str(source["forbidden_data_type"]),
        reason=str(source["reason"]),
        allowed_handling=str(source["allowed_handling"]),
        must_not_commit_to_repo=must_not_commit,
        must_not_use_in_tests=_bool(source["must_not_use_in_tests"], f"forbidden {source['rule_id']}.must_not_use_in_tests"),
        external_system_required_if_ever_authorised=_bool(source["external_system_required_if_ever_authorised"], f"forbidden {source['rule_id']}.external_system_required_if_ever_authorised"),
        guardrail_expected=str(source["guardrail_expected"]),
        non_claim=str(source["non_claim"]),
    )


def _pilot_from_mapping(source: dict[str, Any], source_ids: set[str]) -> PublicDataPilotCandidate:
    _required_mapping(
        source,
        [
            "pilot_id",
            "source_candidate_id",
            "pilot_name",
            "why_useful",
            "candidate_modules",
            "safe_to_commit_if_public_licence_allows",
            "expected_file_type",
            "expected_update_frequency",
            "manual_download_or_api",
            "fields_to_extract",
            "claim_level",
            "must_not_claim",
            "build_27_ready",
            "blockers_before_loading",
        ],
        "public data pilot candidate",
    )
    source_id = str(source["source_candidate_id"])
    if source_id not in source_ids:
        raise ValueError(f"public data pilot references unknown source candidate: {source['pilot_id']}: {source_id}")
    claim_level = _validate_choice(str(source["claim_level"]), CLAIM_LEVEL_VALUES, f"pilot {source['pilot_id']}.claim_level")
    if claim_level not in {"sanity_check_only", "placeholder_anchor_only"}:
        raise ValueError(f"public data pilot must not claim calibration: {source['pilot_id']}")
    must_not_claim = _list_of_strings(source["must_not_claim"], f"pilot {source['pilot_id']}.must_not_claim")
    if any("calibration completed" in item.lower() for item in must_not_claim):
        pass
    return PublicDataPilotCandidate(
        pilot_id=str(source["pilot_id"]),
        source_candidate_id=source_id,
        pilot_name=str(source["pilot_name"]),
        why_useful=str(source["why_useful"]),
        candidate_modules=_list_of_strings(source["candidate_modules"], f"pilot {source['pilot_id']}.candidate_modules"),
        safe_to_commit_if_public_licence_allows=_bool(source["safe_to_commit_if_public_licence_allows"], f"pilot {source['pilot_id']}.safe_to_commit_if_public_licence_allows"),
        expected_file_type=str(source["expected_file_type"]),
        expected_update_frequency=str(source["expected_update_frequency"]),
        manual_download_or_api=str(source["manual_download_or_api"]),
        fields_to_extract=_list_of_strings(source["fields_to_extract"], f"pilot {source['pilot_id']}.fields_to_extract"),
        claim_level=claim_level,
        must_not_claim=must_not_claim,
        build_27_ready=_bool(source["build_27_ready"], f"pilot {source['pilot_id']}.build_27_ready"),
        blockers_before_loading=_list_of_strings(source["blockers_before_loading"], f"pilot {source['pilot_id']}.blockers_before_loading"),
    )


def _no_real_dataset_files_added(repo_root: Path) -> bool:
    forbidden_suffixes = {".csv", ".parquet", ".feather", ".sqlite", ".db", ".xlsx", ".xls", ".jsonl"}
    ignored_dirs = {".git", "__pycache__"}
    for path in repo_root.rglob("*"):
        if any(part in ignored_dirs for part in path.parts):
            continue
        if path.is_file() and path.suffix.lower() in forbidden_suffixes:
            return False
    return True


def build_calibration_intake_result(payload: dict[str, Any], repo_root: Path) -> CalibrationIntakeResult:
    _required_mapping(
        payload,
        [
            "map_id",
            "map_name",
            "status",
            "non_claims",
            "data_status_taxonomy",
            "access_class_taxonomy",
            "claim_level_taxonomy",
            "source_candidates",
            "calibration_fields",
            "module_data_needs",
            "realistic_placeholders",
            "restricted_data_requirements",
            "forbidden_data_rules",
            "public_data_pilot_candidates",
            "external_review_routes",
            "forbidden_claims",
        ],
        "real data feasibility map",
    )
    if not _has_non_claim_language("\n".join(_list_of_strings(payload["non_claims"], "non_claims"))):
        raise ValueError("real data feasibility map missing required non-claim language")

    data_status_taxonomy = _list_of_strings(payload["data_status_taxonomy"], "data_status_taxonomy")
    access_class_taxonomy = _list_of_strings(payload["access_class_taxonomy"], "access_class_taxonomy")
    claim_level_taxonomy = _list_of_strings(payload["claim_level_taxonomy"], "claim_level_taxonomy")
    if set(data_status_taxonomy) != DATA_STATUS_VALUES:
        raise ValueError("data status taxonomy does not match required values")
    if set(access_class_taxonomy) != ACCESS_CLASS_VALUES:
        raise ValueError("access class taxonomy does not match required values")
    if set(claim_level_taxonomy) != CLAIM_LEVEL_VALUES:
        raise ValueError("claim level taxonomy does not match required values")

    source_candidates = [_source_from_mapping(item) for item in payload["source_candidates"]]
    source_ids = {source.source_id for source in source_candidates}
    if len(source_ids) != len(source_candidates):
        raise ValueError("source candidate IDs must be unique")

    calibration_fields = [_field_from_mapping(item, source_ids) for item in payload["calibration_fields"]]
    field_ids = {field.field_id for field in calibration_fields}
    if len(field_ids) != len(calibration_fields):
        raise ValueError("calibration field IDs must be unique")

    module_data_needs = [_module_from_mapping(item, source_ids, field_ids) for item in payload["module_data_needs"]]
    module_ids = {module.module_id for module in module_data_needs}
    if len(module_ids) != len(module_data_needs):
        raise ValueError("module IDs must be unique")

    realistic_placeholders = [_placeholder_from_mapping(item, field_ids, source_ids) for item in payload["realistic_placeholders"]]
    restricted_data_requirements = [
        _restricted_requirement_from_mapping(item, source_ids, field_ids, module_ids)
        for item in payload["restricted_data_requirements"]
    ]
    forbidden_data_rules = [_forbidden_rule_from_mapping(item) for item in payload["forbidden_data_rules"]]
    public_data_pilot_candidates = [_pilot_from_mapping(item, source_ids) for item in payload["public_data_pilot_candidates"]]

    serialized = str(payload)
    forbidden = find_forbidden_affirmative_real_data_claims(serialized)
    if forbidden:
        raise ValueError(f"real data feasibility map contains forbidden affirmative claims: {', '.join(forbidden)}")
    if not _no_real_dataset_files_added(repo_root):
        raise ValueError("real dataset-like files are present in the repository")

    public_source_candidates = sum(1 for source in source_candidates if source.access_class in PUBLIC_ACCESS_CLASSES)
    restricted_source_candidates = sum(
        1
        for source in source_candidates
        if source.access_class in RESTRICTED_ACCESS_CLASSES or source.data_status == "restricted_data_required"
    )
    forbidden_repo_sources = sum(
        1
        for source in source_candidates
        if source.data_status == "forbidden_repo_data" or not source.can_be_committed_to_repo
    )
    fields_public_sanity = sum(1 for field in calibration_fields if field.can_be_publicly_sanity_checked)
    fields_public_calibration = sum(1 for field in calibration_fields if field.can_be_calibrated_from_public_data_only)
    fields_restricted = sum(1 for field in calibration_fields if field.restricted_sources_needed or field.required_data_status == "restricted_data_required")
    build_27_ready = sum(1 for pilot in public_data_pilot_candidates if pilot.build_27_ready)

    summary = CalibrationIntakeSummary(
        total_source_candidates=len(source_candidates),
        public_source_candidates=public_source_candidates,
        restricted_source_candidates=restricted_source_candidates,
        forbidden_repo_sources=forbidden_repo_sources,
        total_calibration_fields=len(calibration_fields),
        fields_public_sanity_check_possible=fields_public_sanity,
        fields_public_calibration_possible=fields_public_calibration,
        fields_requiring_restricted_data=fields_restricted,
        total_realistic_placeholders=len(realistic_placeholders),
        total_forbidden_data_rules=len(forbidden_data_rules),
        total_public_data_pilot_candidates=len(public_data_pilot_candidates),
        build_27_ready_candidates=build_27_ready,
        real_data_loaded=False,
        real_calibration_completed=False,
        restricted_data_loaded=False,
        taxpayer_data_loaded=False,
        firm_level_confidential_data_loaded=False,
        household_microdata_loaded=False,
        realistic_placeholders_created=bool(realistic_placeholders),
        placeholders_labelled=all(
            item.data_status == "realistic_placeholder"
            and item.must_be_labelled_realistic_placeholder
            and item.must_not_be_labelled_real_data
            and item.must_not_be_labelled_calibrated
            for item in realistic_placeholders
        ),
        public_data_pilot_ready=build_27_ready > 0,
        validation_claimed=False,
        approval_claimed=False,
        operational_readiness_claimed=False,
        legal_sufficiency_claimed=False,
        official_status_claimed=False,
        firm_level_liability_logic_modified=False,
    )

    return CalibrationIntakeResult(
        map_id=str(payload["map_id"]),
        map_name=str(payload["map_name"]),
        status=str(payload["status"]),
        non_claims=_list_of_strings(payload["non_claims"], "non_claims"),
        data_status_taxonomy=data_status_taxonomy,
        access_class_taxonomy=access_class_taxonomy,
        claim_level_taxonomy=claim_level_taxonomy,
        source_candidates=sorted(source_candidates, key=lambda item: item.source_id),
        calibration_fields=sorted(calibration_fields, key=lambda item: item.field_id),
        module_data_needs=sorted(module_data_needs, key=lambda item: item.module_id),
        realistic_placeholders=sorted(realistic_placeholders, key=lambda item: item.placeholder_id),
        restricted_data_requirements=sorted(restricted_data_requirements, key=lambda item: item.requirement_id),
        forbidden_data_rules=sorted(forbidden_data_rules, key=lambda item: item.rule_id),
        public_data_pilot_candidates=sorted(public_data_pilot_candidates, key=lambda item: item.pilot_id),
        external_review_routes=list(payload["external_review_routes"]),
        forbidden_claims=_list_of_strings(payload["forbidden_claims"], "forbidden_claims"),
        summary=summary,
        warnings=[
            "No real data has been loaded by Build 26.",
            "Realistic placeholders remain labelled placeholders and are not calibrated data.",
            "Build 25 sealed the prior RC state; a later sealed RC must rerun the integrity seal if Build 26 is included.",
        ],
    )
