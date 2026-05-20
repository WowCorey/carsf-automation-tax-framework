"""Public aggregate-data pilot and placeholder-anchor validation for CARSF V1.5.

This layer allows small, source-referenced public aggregate extracts to enter
the repo while keeping them separate from realistic placeholders, synthetic
fixtures, restricted-data blockers, and forbidden repo data. It does not
complete calibration, validate CARSF as a real tax model, determine tax
payable, or modify firm-level CARSF liability.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


DATA_STATUS_VALUES = {
    "real_public_data_loaded",
    "source_reference_only",
    "realistic_placeholder",
    "synthetic_fixture",
    "restricted_data_required",
    "forbidden_repo_data",
}

CLAIM_LEVEL_VALUES = {
    "sanity_check_only",
    "placeholder_anchor_only",
    "source_reference_only",
    "blocked_by_restricted_data",
    "forbidden_for_model_use",
}

SOURCE_KIND_VALUES = {
    "ABS_public_aggregate",
    "ATO_public_aggregate",
    "Treasury_public_fiscal",
    "PBO_public_reference",
    "Fair_Work_public_wage_anchor",
    "HELP_HECS_public_threshold",
    "Super_Guarantee_public_setting",
    "State_payroll_tax_public_threshold",
    "source_reference_only",
    "realistic_placeholder_anchor",
}

PUBLIC_DATA_PILOT_WARNING = (
    "This is a public aggregate-data pilot and realistic-placeholder anchor layer only. "
    "It may include small public aggregate extracts or source-reference records, but it is not calibration, "
    "calibration has not been completed, public data extracts do not prove the model works, public data does not prove "
    "the model works, realistic placeholders remain placeholders, realistic placeholders "
    "remain realistic placeholders, source references are not loaded datasets, and restricted-data requirements are "
    "not data access. It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic "
    "validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, and not official "
    "status. It does not determine actual tax payable, does not use taxpayer-level data, firm-level confidential "
    "data, household microdata, ABS DataLab, HILDA microdata, DSS/Services Australia records, ATO taxpayer records, "
    "Treasury/PBO confidential material, or restricted government data, and does not modify firm-level CARSF liability."
)

PUBLIC_DATA_PILOT_NON_CLAIMS = [
    PUBLIC_DATA_PILOT_WARNING,
    "Loaded public aggregate extracts are sanity-check-only or placeholder-anchor-only records, not completed calibration.",
    "Realistic placeholders anchored to public sources remain placeholders and must not be labelled as real data or calibrated.",
    "The pilot only tests whether small public aggregates can support sanity checks and placeholder anchors.",
]

FORBIDDEN_AFFIRMATIVE_PUBLIC_DATA_CLAIMS = [
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
]

NEGATIVE_CONTEXT_MARKERS = [
    "not ",
    "not a ",
    "not an ",
    "no ",
    "does not ",
    "do not ",
    "must not ",
    "must_not",
    "must_not_claim",
    "must_not_be_labelled",
    "not_",
    "without ",
    "is not ",
    "are not ",
    "has not ",
    "have not ",
    "cannot ",
    "forbidden",
    "prohibited",
    "blocked",
    "non-claim",
    "boundary",
    "prevent ",
    "overread ",
    "does_not_show",
    "claim_level",
    "what it does not",
    "must not infer",
]

FORBIDDEN_PUBLIC_PILOT_PATH_PARTS = {
    "private",
    "restricted",
    "incoming",
    "real_evidence",
    "secure_drop",
}

PUBLIC_PILOT_ALLOWED_EXTENSIONS = {".yaml", ".yml", ".json", ".md"}
PUBLIC_PILOT_DATASET_EXTENSIONS = {".csv", ".xlsx", ".parquet", ".db", ".sqlite", ".jsonl"}


@dataclass(frozen=True)
class PublicDataSourceReference:
    source_reference_id: str
    source_name: str
    publisher: str
    source_kind: str
    source_url: str
    publication_or_release_name: str
    publication_date_or_year: str
    accessed_date: str
    access_class: str
    licence_notes: str
    raw_dataset_committed: bool
    extract_committed: bool
    candidate_modules: list[str]
    candidate_fields: list[str]
    claim_level: str
    must_not_claim: list[str]
    source_review_required: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicAggregateExtract:
    extract_id: str
    source_reference_id: str
    publisher: str
    source_kind: str
    data_status: str
    claim_level: str
    extract_type: str
    units: str
    period: str
    geography: str
    values: list[dict[str, Any]]
    source_url: str
    source_note: str
    source_locator: str
    source_value_note: str
    value_review_status: str
    licence_notes: str
    raw_dataset_committed: bool
    safe_to_commit: bool
    must_not_claim: list[str]
    load_status: str = "loaded_public_extract"
    blocker: str = ""

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PlaceholderAnchorRecord:
    anchor_id: str
    field_id: str
    placeholder_name: str
    anchor_source_reference_ids: list[str]
    anchor_extract_ids: list[str]
    basis_type: str
    current_placeholder_status: str
    anchored_to_public_data: bool
    anchor_strength: str
    blocked_by_restricted_data: bool
    missing_data_for_calibration: list[str]
    must_be_labelled_realistic_placeholder: bool
    must_not_be_labelled_real_data: bool
    must_not_be_labelled_calibrated: bool
    must_not_claim: list[str]
    review_required_before_calibration: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class FieldSanityCheck:
    check_id: str
    field_id: str
    field_name: str
    public_extract_ids: list[str]
    placeholder_anchor_ids: list[str]
    check_type: str
    check_status: str
    claim_level: str
    finding: str
    must_not_claim: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ModuleSanityCheck:
    module_id: str
    module_name: str
    public_extract_ids: list[str]
    placeholder_anchor_ids: list[str]
    sanity_check_possible: bool
    calibration_possible: bool
    blocked_by_restricted_data: bool
    result_status: str
    claim_level: str
    main_blockers: list[str]
    must_not_claim: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicDataDigest:
    path: str
    sha256: str
    bytes: int
    digest_scope: str = "public_data_pilot_integrity_metadata_only"

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicDataBoundaryCheck:
    boundary_id: str
    boundary_description: str
    passed: bool
    finding: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicDataPilotSummary:
    total_source_references: int
    source_references_created: bool
    total_public_aggregate_extracts: int
    real_public_data_loaded_extracts: int
    source_reference_only_extracts: int
    total_placeholder_anchors: int
    placeholders_anchored_to_public_data: int
    placeholders_source_reference_only: int
    total_field_sanity_checks: int
    field_sanity_checks_passed: int
    field_sanity_checks_warning: int
    field_sanity_checks_blocked: int
    total_module_sanity_checks: int
    modules_sanity_check_possible: int
    modules_placeholder_anchor_possible: int
    modules_blocked_by_restricted_data: int
    digest_targets_total: int
    digests_written: int
    forbidden_claim_findings: int
    restricted_data_findings: int
    public_data_pilot_created: bool
    real_public_data_loaded: bool
    realistic_placeholders_anchored: bool
    real_calibration_completed: bool
    restricted_data_loaded: bool
    taxpayer_data_loaded: bool
    firm_level_confidential_data_loaded: bool
    household_microdata_loaded: bool
    actual_tax_payable_determined: bool
    validation_claimed: bool
    approval_claimed: bool
    operational_readiness_claimed: bool
    legal_sufficiency_claimed: bool
    official_status_claimed: bool
    firm_level_liability_logic_modified: bool
    warnings: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicDataPilotResult:
    pilot_id: str
    pilot_name: str
    status: str
    non_claims: list[str]
    source_references: list[PublicDataSourceReference]
    public_aggregate_extracts: list[PublicAggregateExtract]
    placeholder_anchors: list[PlaceholderAnchorRecord]
    field_sanity_checks: list[FieldSanityCheck]
    module_sanity_checks: list[ModuleSanityCheck]
    restricted_data_blockers: list[dict[str, Any]]
    forbidden_data_rules: list[dict[str, Any]]
    boundary_checks: list[PublicDataBoundaryCheck]
    future_build_28_requirements: list[str]
    summary: PublicDataPilotSummary

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


def _bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be true or false")
    return value


def _choice(value: str, allowed: set[str], label: str) -> str:
    if value not in allowed:
        raise ValueError(f"{label} has invalid value: {value}")
    return value


def _non_empty(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value


def _has_negative_context(text: str, index: int) -> bool:
    window = text[max(0, index - 220) : index].lower().replace("_", " ")
    return any(marker in window for marker in NEGATIVE_CONTEXT_MARKERS)


def _inside_claim_inventory(text: str, index: int) -> bool:
    line_start = text.rfind("\n", 0, index) + 1
    line = text[line_start : text.find("\n", index) if "\n" in text[index:] else len(text)].lower()
    preceding = text[max(0, index - 300) : index].lower()
    return (
        "forbidden_claim" in line
        or "must_not_claim" in line
        or "must not claim" in line
        or "must_not_be_used_for" in line
        or "must not infer" in line
        or '"must_not_claim"' in preceding
        or "forbidden_claims" in preceding
        or "must not claim" in preceding
        or "must not infer" in preceding
    )


def find_forbidden_affirmative_public_data_claims(text: str) -> list[str]:
    lowered = text.lower()
    findings: list[str] = []
    for phrase in FORBIDDEN_AFFIRMATIVE_PUBLIC_DATA_CLAIMS:
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


def _source_reference_from_mapping(source: dict[str, Any]) -> PublicDataSourceReference:
    _required_mapping(
        source,
        [
            "source_reference_id",
            "source_name",
            "publisher",
            "source_kind",
            "source_url",
            "publication_or_release_name",
            "publication_date_or_year",
            "accessed_date",
            "access_class",
            "licence_notes",
            "raw_dataset_committed",
            "extract_committed",
            "candidate_modules",
            "candidate_fields",
            "claim_level",
            "must_not_claim",
            "source_review_required",
        ],
        "source reference",
    )
    return PublicDataSourceReference(
        source_reference_id=_non_empty(source["source_reference_id"], "source_reference_id"),
        source_name=_non_empty(source["source_name"], "source_name"),
        publisher=_non_empty(source["publisher"], "publisher"),
        source_kind=_choice(str(source["source_kind"]), SOURCE_KIND_VALUES, "source_kind"),
        source_url=_non_empty(source["source_url"], "source_url"),
        publication_or_release_name=_non_empty(source["publication_or_release_name"], "publication_or_release_name"),
        publication_date_or_year=str(source["publication_date_or_year"]),
        accessed_date=_non_empty(source["accessed_date"], "accessed_date"),
        access_class=_non_empty(source["access_class"], "access_class"),
        licence_notes=_non_empty(source["licence_notes"], "licence_notes"),
        raw_dataset_committed=_bool(source["raw_dataset_committed"], "raw_dataset_committed"),
        extract_committed=_bool(source["extract_committed"], "extract_committed"),
        candidate_modules=_list_of_strings(source["candidate_modules"], "candidate_modules"),
        candidate_fields=_list_of_strings(source["candidate_fields"], "candidate_fields"),
        claim_level=_choice(str(source["claim_level"]), CLAIM_LEVEL_VALUES, "claim_level"),
        must_not_claim=_list_of_strings(source["must_not_claim"], "must_not_claim"),
        source_review_required=_list_of_strings(source["source_review_required"], "source_review_required"),
    )


def _extract_from_mapping(source: dict[str, Any], source_ids: set[str]) -> PublicAggregateExtract:
    _required_mapping(
        source,
        [
            "extract_id",
            "source_reference_id",
            "publisher",
            "source_kind",
            "data_status",
            "claim_level",
            "extract_type",
            "units",
            "period",
            "geography",
            "values",
            "source_url",
            "source_note",
            "licence_notes",
            "raw_dataset_committed",
            "safe_to_commit",
            "must_not_claim",
        ],
        "public aggregate extract",
    )
    source_reference_id = _non_empty(source["source_reference_id"], "source_reference_id")
    if source_reference_id not in source_ids:
        raise ValueError(f"extract references unknown source_reference_id: {source_reference_id}")
    data_status = _choice(str(source["data_status"]), DATA_STATUS_VALUES, "extract.data_status")
    claim_level = _choice(str(source["claim_level"]), CLAIM_LEVEL_VALUES, "extract.claim_level")
    if data_status == "real_public_data_loaded":
        if not _non_empty(source["source_url"], "extract.source_url").startswith("https://"):
            raise ValueError(f"real_public_data_loaded extract lacks https source URL: {source['extract_id']}")
        if not _non_empty(source["source_note"], "extract.source_note"):
            raise ValueError(f"real_public_data_loaded extract lacks source note: {source['extract_id']}")
        if not _non_empty(source.get("source_locator"), "extract.source_locator"):
            raise ValueError(f"real_public_data_loaded extract lacks source locator: {source['extract_id']}")
        if not _non_empty(source.get("source_value_note"), "extract.source_value_note"):
            raise ValueError(f"real_public_data_loaded extract lacks source value note: {source['extract_id']}")
        if not _non_empty(source.get("value_review_status"), "extract.value_review_status"):
            raise ValueError(f"real_public_data_loaded extract lacks value review status: {source['extract_id']}")
        if not _non_empty(source["licence_notes"], "extract.licence_notes"):
            raise ValueError(f"real_public_data_loaded extract lacks licence notes: {source['extract_id']}")
        if _bool(source["safe_to_commit"], "extract.safe_to_commit") is not True:
            raise ValueError(f"real_public_data_loaded extract must be safe_to_commit: {source['extract_id']}")
    values = source["values"]
    if not isinstance(values, list):
        raise ValueError(f"extract values must be a list: {source['extract_id']}")
    _validate_wage_extract_consistency(str(source["extract_id"]), values)
    return PublicAggregateExtract(
        extract_id=_non_empty(source["extract_id"], "extract_id"),
        source_reference_id=source_reference_id,
        publisher=_non_empty(source["publisher"], "publisher"),
        source_kind=_choice(str(source["source_kind"]), SOURCE_KIND_VALUES, "extract.source_kind"),
        data_status=data_status,
        claim_level=claim_level,
        extract_type=_non_empty(source["extract_type"], "extract_type"),
        units=_non_empty(source["units"], "units"),
        period=str(source["period"]),
        geography=_non_empty(source["geography"], "geography"),
        values=[dict(item) for item in values],
        source_url=_non_empty(source["source_url"], "source_url"),
        source_note=_non_empty(source["source_note"], "source_note"),
        source_locator=str(source.get("source_locator", "")),
        source_value_note=str(source.get("source_value_note", "")),
        value_review_status=str(source.get("value_review_status", "")),
        licence_notes=_non_empty(source["licence_notes"], "licence_notes"),
        raw_dataset_committed=_bool(source["raw_dataset_committed"], "raw_dataset_committed"),
        safe_to_commit=_bool(source["safe_to_commit"], "safe_to_commit"),
        must_not_claim=_list_of_strings(source["must_not_claim"], "must_not_claim"),
        load_status=str(source.get("load_status", "loaded_public_extract")),
        blocker=str(source.get("blocker", "")),
    )


def _extract_numeric_value(values: list[dict[str, Any]], value_id: str) -> float | None:
    for item in values:
        if item.get("value_id") == value_id:
            value = item.get("value")
            if isinstance(value, bool) or not isinstance(value, int | float):
                raise ValueError(f"{value_id} must be numeric when present")
            return float(value)
    return None


def _validate_wage_extract_consistency(extract_id: str, values: list[dict[str, Any]]) -> None:
    hourly = _extract_numeric_value(values, "national_minimum_wage_hourly")
    weekly = _extract_numeric_value(values, "national_minimum_wage_weekly")
    if hourly is None or weekly is None:
        return
    expected_weekly = round(hourly * 38, 2)
    if abs(weekly - expected_weekly) > 0.001:
        raise ValueError(
            f"minimum wage weekly value inconsistent in {extract_id}: "
            f"expected {expected_weekly:.2f} from hourly * 38, got {weekly:.2f}"
        )


def _anchor_from_mapping(source: dict[str, Any], source_ids: set[str], extract_ids: set[str]) -> PlaceholderAnchorRecord:
    _required_mapping(
        source,
        [
            "anchor_id",
            "field_id",
            "placeholder_name",
            "anchor_source_reference_ids",
            "anchor_extract_ids",
            "basis_type",
            "current_placeholder_status",
            "anchored_to_public_data",
            "anchor_strength",
            "blocked_by_restricted_data",
            "missing_data_for_calibration",
            "must_be_labelled_realistic_placeholder",
            "must_not_be_labelled_real_data",
            "must_not_be_labelled_calibrated",
            "must_not_claim",
            "review_required_before_calibration",
        ],
        "placeholder anchor",
    )
    anchor_sources = _list_of_strings(source["anchor_source_reference_ids"], "anchor_source_reference_ids")
    unknown_sources = sorted(set(anchor_sources) - source_ids)
    if unknown_sources:
        raise ValueError(f"placeholder anchor references unknown sources: {', '.join(unknown_sources)}")
    anchor_extracts = [str(item) for item in source.get("anchor_extract_ids", [])]
    unknown_extracts = sorted(set(anchor_extracts) - extract_ids)
    if unknown_extracts:
        raise ValueError(f"placeholder anchor references unknown extracts: {', '.join(unknown_extracts)}")
    if source["current_placeholder_status"] != "realistic_placeholder":
        raise ValueError("placeholder anchor must remain realistic_placeholder")
    if not _bool(source["must_be_labelled_realistic_placeholder"], "must_be_labelled_realistic_placeholder"):
        raise ValueError("placeholder anchor must be labelled realistic placeholder")
    if not _bool(source["must_not_be_labelled_real_data"], "must_not_be_labelled_real_data"):
        raise ValueError("placeholder anchor must not be labelled real data")
    if not _bool(source["must_not_be_labelled_calibrated"], "must_not_be_labelled_calibrated"):
        raise ValueError("placeholder anchor must not be labelled calibrated")
    return PlaceholderAnchorRecord(
        anchor_id=_non_empty(source["anchor_id"], "anchor_id"),
        field_id=_non_empty(source["field_id"], "field_id"),
        placeholder_name=_non_empty(source["placeholder_name"], "placeholder_name"),
        anchor_source_reference_ids=anchor_sources,
        anchor_extract_ids=anchor_extracts,
        basis_type=_non_empty(source["basis_type"], "basis_type"),
        current_placeholder_status="realistic_placeholder",
        anchored_to_public_data=_bool(source["anchored_to_public_data"], "anchored_to_public_data"),
        anchor_strength=_choice(str(source["anchor_strength"]), {"weak", "moderate", "source_reference_only"}, "anchor_strength"),
        blocked_by_restricted_data=_bool(source["blocked_by_restricted_data"], "blocked_by_restricted_data"),
        missing_data_for_calibration=_list_of_strings(source["missing_data_for_calibration"], "missing_data_for_calibration"),
        must_be_labelled_realistic_placeholder=True,
        must_not_be_labelled_real_data=True,
        must_not_be_labelled_calibrated=True,
        must_not_claim=_list_of_strings(source["must_not_claim"], "must_not_claim"),
        review_required_before_calibration=_list_of_strings(
            source["review_required_before_calibration"], "review_required_before_calibration"
        ),
    )


def _field_check_from_mapping(source: dict[str, Any], extract_ids: set[str], anchor_ids: set[str]) -> FieldSanityCheck:
    _required_mapping(
        source,
        [
            "check_id",
            "field_id",
            "field_name",
            "public_extract_ids",
            "placeholder_anchor_ids",
            "check_type",
            "check_status",
            "claim_level",
            "finding",
            "must_not_claim",
        ],
        "field sanity check",
    )
    public_extract_ids = [str(item) for item in source.get("public_extract_ids", [])]
    placeholder_anchor_ids = [str(item) for item in source.get("placeholder_anchor_ids", [])]
    unknown_extracts = sorted(set(public_extract_ids) - extract_ids)
    unknown_anchors = sorted(set(placeholder_anchor_ids) - anchor_ids)
    if unknown_extracts or unknown_anchors:
        raise ValueError(f"field sanity check references unknown ids: {unknown_extracts + unknown_anchors}")
    return FieldSanityCheck(
        check_id=_non_empty(source["check_id"], "check_id"),
        field_id=_non_empty(source["field_id"], "field_id"),
        field_name=_non_empty(source["field_name"], "field_name"),
        public_extract_ids=public_extract_ids,
        placeholder_anchor_ids=placeholder_anchor_ids,
        check_type=_choice(
            str(source["check_type"]),
            {"value_presence_check", "range_plausibility_check", "source_reference_check", "blocked_by_restricted_data_check"},
            "check_type",
        ),
        check_status=_choice(str(source["check_status"]), {"passed", "warning", "blocked", "not_applicable"}, "check_status"),
        claim_level=_choice(str(source["claim_level"]), CLAIM_LEVEL_VALUES, "field check claim_level"),
        finding=_non_empty(source["finding"], "finding"),
        must_not_claim=_list_of_strings(source["must_not_claim"], "must_not_claim"),
    )


def _module_check_from_mapping(source: dict[str, Any], extract_ids: set[str], anchor_ids: set[str]) -> ModuleSanityCheck:
    _required_mapping(
        source,
        [
            "module_id",
            "module_name",
            "public_extract_ids",
            "placeholder_anchor_ids",
            "sanity_check_possible",
            "calibration_possible",
            "blocked_by_restricted_data",
            "result_status",
            "claim_level",
            "main_blockers",
            "must_not_claim",
        ],
        "module sanity check",
    )
    if _bool(source["calibration_possible"], "module calibration_possible") is not False:
        raise ValueError(f"module sanity check must keep calibration_possible false: {source['module_id']}")
    public_extract_ids = [str(item) for item in source.get("public_extract_ids", [])]
    placeholder_anchor_ids = [str(item) for item in source.get("placeholder_anchor_ids", [])]
    unknown_extracts = sorted(set(public_extract_ids) - extract_ids)
    unknown_anchors = sorted(set(placeholder_anchor_ids) - anchor_ids)
    if unknown_extracts or unknown_anchors:
        raise ValueError(f"module sanity check references unknown ids: {unknown_extracts + unknown_anchors}")
    return ModuleSanityCheck(
        module_id=_non_empty(source["module_id"], "module_id"),
        module_name=_non_empty(source["module_name"], "module_name"),
        public_extract_ids=public_extract_ids,
        placeholder_anchor_ids=placeholder_anchor_ids,
        sanity_check_possible=_bool(source["sanity_check_possible"], "sanity_check_possible"),
        calibration_possible=False,
        blocked_by_restricted_data=_bool(source["blocked_by_restricted_data"], "blocked_by_restricted_data"),
        result_status=_choice(
            str(source["result_status"]),
            {"sanity_check_possible", "placeholder_anchor_possible", "blocked_by_restricted_data", "source_reference_only"},
            "result_status",
        ),
        claim_level=_choice(str(source["claim_level"]), CLAIM_LEVEL_VALUES, "module check claim_level"),
        main_blockers=_list_of_strings(source["main_blockers"], "main_blockers"),
        must_not_claim=_list_of_strings(source["must_not_claim"], "must_not_claim"),
    )


def _validate_forbidden_rules(items: list[dict[str, Any]]) -> None:
    for item in items:
        _required_mapping(item, ["rule_id", "forbidden_data_type", "must_not_commit_to_repo", "must_not_use_in_tests"], "forbidden data rule")
        if item["must_not_commit_to_repo"] is not True:
            raise ValueError(f"forbidden data rule weakens repo ban: {item['rule_id']}")
        if item["must_not_use_in_tests"] is not True:
            raise ValueError(f"forbidden data rule weakens test ban: {item['rule_id']}")


def _validate_public_pilot_files(repo_root: Path) -> list[PublicDataBoundaryCheck]:
    checks: list[PublicDataBoundaryCheck] = []
    public_root = repo_root / "data" / "public_pilot"
    restricted_findings: list[str] = []
    dataset_findings: list[str] = []
    for path in public_root.rglob("*"):
        if path.is_dir():
            continue
        relative = str(path.relative_to(repo_root)).replace("\\", "/").lower()
        if any(part in relative for part in FORBIDDEN_PUBLIC_PILOT_PATH_PARTS):
            restricted_findings.append(relative)
        suffix = path.suffix.lower()
        if suffix in PUBLIC_PILOT_DATASET_EXTENSIONS:
            text = path.read_text(encoding="utf-8", errors="ignore")
            required = [
                "public_aggregate_only: true",
                "source_url:",
                "licence_notes:",
                "no_person_level_data: true",
                "no_taxpayer_level_data: true",
                "no_firm_confidential_data: true",
                "no_household_microdata: true",
            ]
            if not all(marker in text for marker in required):
                dataset_findings.append(relative)
        elif suffix not in PUBLIC_PILOT_ALLOWED_EXTENSIONS:
            dataset_findings.append(relative)
    checks.append(
        PublicDataBoundaryCheck(
            boundary_id="restricted_path_boundary",
            boundary_description="No restricted/private/incoming public-pilot paths are present.",
            passed=not restricted_findings,
            finding=", ".join(restricted_findings) if restricted_findings else "no restricted public-pilot paths found",
        )
    )
    checks.append(
        PublicDataBoundaryCheck(
            boundary_id="dataset_extension_boundary",
            boundary_description="Dataset-like files are absent or explicitly whitelisted as public aggregate fixtures.",
            passed=not dataset_findings,
            finding=", ".join(dataset_findings) if dataset_findings else "no unapproved dataset-like public-pilot files found",
        )
    )
    return checks


def build_public_data_pilot_result(
    manifest: dict[str, Any],
    extracts_payload: list[dict[str, Any]],
    anchors_payload: list[dict[str, Any]],
    repo_root: Path,
    digest_targets_total: int,
    digests_written: int,
) -> PublicDataPilotResult:
    _required_mapping(
        manifest,
        [
            "pilot_id",
            "pilot_name",
            "status",
            "non_claims",
            "source_references",
            "field_sanity_checks",
            "module_sanity_checks",
            "restricted_data_blockers",
            "forbidden_data_rules",
            "build_27_flags",
            "future_build_28_requirements",
            "forbidden_claims",
        ],
        "public data pilot manifest",
    )
    if manifest["status"] != "public_data_pilot_placeholder_anchor_layer_only":
        raise ValueError("public data pilot status must be public_data_pilot_placeholder_anchor_layer_only")
    for non_claim in PUBLIC_DATA_PILOT_NON_CLAIMS:
        if non_claim not in manifest["non_claims"]:
            raise ValueError("public data pilot manifest missing required non-claim language")

    source_references = [_source_reference_from_mapping(item) for item in manifest["source_references"]]
    source_ids = {item.source_reference_id for item in source_references}
    extracts = [_extract_from_mapping(item, source_ids) for item in extracts_payload]
    extract_ids = {item.extract_id for item in extracts}
    anchors = [_anchor_from_mapping(item, source_ids, extract_ids) for item in anchors_payload]
    anchor_ids = {item.anchor_id for item in anchors}
    field_checks = [_field_check_from_mapping(item, extract_ids, anchor_ids) for item in manifest["field_sanity_checks"]]
    module_checks = [_module_check_from_mapping(item, extract_ids, anchor_ids) for item in manifest["module_sanity_checks"]]
    _validate_forbidden_rules(manifest["forbidden_data_rules"])
    boundary_checks = _validate_public_pilot_files(repo_root)
    restricted_data_findings = sum(1 for check in boundary_checks if not check.passed)

    combined_for_claim_scan = str(manifest) + str(extracts_payload) + str(anchors_payload)
    forbidden_claims = find_forbidden_affirmative_public_data_claims(combined_for_claim_scan)
    if forbidden_claims:
        raise ValueError(f"public data pilot contains forbidden affirmative claims: {', '.join(forbidden_claims)}")

    flags = manifest["build_27_flags"]
    expected_false_flags = [
        "real_calibration_completed",
        "restricted_data_loaded",
        "taxpayer_data_loaded",
        "firm_level_confidential_data_loaded",
        "household_microdata_loaded",
        "actual_tax_payable_determined",
        "validation_claimed",
        "approval_claimed",
        "operational_readiness_claimed",
        "legal_sufficiency_claimed",
        "official_status_claimed",
        "firm_level_liability_logic_modified",
    ]
    for flag in expected_false_flags:
        if flags.get(flag) is not False:
            raise ValueError(f"build_27_flags.{flag} must be false")
    if flags.get("public_data_pilot_created") is not True:
        raise ValueError("build_27_flags.public_data_pilot_created must be true")
    loaded_extracts = [item for item in extracts if item.data_status == "real_public_data_loaded"]
    source_ref_extracts = [item for item in extracts if item.data_status == "source_reference_only"]
    if flags.get("real_public_data_loaded") is not bool(loaded_extracts):
        raise ValueError("build_27_flags.real_public_data_loaded does not match loaded public extract count")

    summary = PublicDataPilotSummary(
        total_source_references=len(source_references),
        source_references_created=bool(source_references),
        total_public_aggregate_extracts=len(extracts),
        real_public_data_loaded_extracts=len(loaded_extracts),
        source_reference_only_extracts=len(source_ref_extracts),
        total_placeholder_anchors=len(anchors),
        placeholders_anchored_to_public_data=sum(item.anchored_to_public_data for item in anchors),
        placeholders_source_reference_only=sum(item.anchor_strength == "source_reference_only" for item in anchors),
        total_field_sanity_checks=len(field_checks),
        field_sanity_checks_passed=sum(item.check_status == "passed" for item in field_checks),
        field_sanity_checks_warning=sum(item.check_status == "warning" for item in field_checks),
        field_sanity_checks_blocked=sum(item.check_status == "blocked" for item in field_checks),
        total_module_sanity_checks=len(module_checks),
        modules_sanity_check_possible=sum(item.result_status == "sanity_check_possible" for item in module_checks),
        modules_placeholder_anchor_possible=sum(item.result_status == "placeholder_anchor_possible" for item in module_checks),
        modules_blocked_by_restricted_data=sum(item.blocked_by_restricted_data for item in module_checks),
        digest_targets_total=digest_targets_total,
        digests_written=digests_written,
        forbidden_claim_findings=0,
        restricted_data_findings=restricted_data_findings,
        public_data_pilot_created=True,
        real_public_data_loaded=bool(loaded_extracts),
        realistic_placeholders_anchored=bool(anchors),
        real_calibration_completed=False,
        restricted_data_loaded=False,
        taxpayer_data_loaded=False,
        firm_level_confidential_data_loaded=False,
        household_microdata_loaded=False,
        actual_tax_payable_determined=False,
        validation_claimed=False,
        approval_claimed=False,
        operational_readiness_claimed=False,
        legal_sufficiency_claimed=False,
        official_status_claimed=False,
        firm_level_liability_logic_modified=False,
        warnings=[
            "Public extracts are small source-referenced records only.",
            "Realistic placeholders remain placeholders and are not calibrated.",
            "Restricted-data blockers remain unresolved.",
        ],
    )
    return PublicDataPilotResult(
        pilot_id=str(manifest["pilot_id"]),
        pilot_name=str(manifest["pilot_name"]),
        status=str(manifest["status"]),
        non_claims=list(manifest["non_claims"]),
        source_references=source_references,
        public_aggregate_extracts=extracts,
        placeholder_anchors=anchors,
        field_sanity_checks=field_checks,
        module_sanity_checks=module_checks,
        restricted_data_blockers=[dict(item) for item in manifest["restricted_data_blockers"]],
        forbidden_data_rules=[dict(item) for item in manifest["forbidden_data_rules"]],
        boundary_checks=boundary_checks,
        future_build_28_requirements=_list_of_strings(manifest["future_build_28_requirements"], "future_build_28_requirements"),
        summary=summary,
    )
