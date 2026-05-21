"""Controlled public aggregate-data loader for CARSF V1.5.

This layer loads only repo-local, source-located public aggregate records.
It does not complete calibration, validate CARSF, determine tax payable,
provide legal or tax advice, or modify firm-level CARSF liability.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


SOURCE_LOAD_STATUS_VALUES = {
    "loaded",
    "source_candidate_not_loaded",
    "blocked",
    "rejected",
}

VALUE_REVIEW_STATUS_VALUES = {
    "loaded_from_public_aggregate_file",
    "manually_recorded_public_source_value",
    "source_locator_recorded_only",
    "arithmetic_checked_only",
    "not_loaded",
}

CLAIM_LEVEL_VALUES = {
    "real_public_aggregate_data",
    "source_reference_only",
    "placeholder_anchor_only",
    "blocked_restricted_data",
}

GUARDRAIL_STATUS_VALUES = {
    "clean",
    "warning",
    "blocked",
    "fail_closed",
}

PUBLIC_REAL_DATA_WARNING = (
    "This loads real public aggregate data only. This does not load restricted data, personal data, "
    "taxpayer-level data, firm-confidential data, or household microdata. Public aggregate data does not equal "
    "calibration; calibration has not been completed. Public data does not prove the model works. This is not "
    "validation, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, "
    "not economic validation, not welfare validation, not statistical validation, not operational readiness, "
    "not legal sufficiency, and not official status. It does not determine actual tax payable and does not modify "
    "firm-level CARSF liability."
)

PUBLIC_REAL_DATA_NON_CLAIMS = [
    PUBLIC_REAL_DATA_WARNING,
    "Loaded records are public aggregate/source-located values only and do not create a calibrated model.",
    "Source candidates without safe local values remain source_candidate_not_loaded and are not counted as loaded data.",
    "The loader only supports sanity-check context and placeholder replacement review; it does not replace legal, tax, Treasury, ATO, statistical, welfare, or economic review.",
]

FORBIDDEN_AFFIRMATIVE_PUBLIC_REAL_CLAIMS = [
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
    "does_not_show",
    "must_not_infer",
    "not_used_for",
    "what this data cannot support",
    "does not mean",
]


@dataclass(frozen=True)
class PublicRealDataSource:
    source_id: str
    publisher: str
    source_name: str
    source_url: str
    source_locator: str
    source_file_name: str
    source_file_type: str
    access_method: str
    access_date: str
    licence_or_access_note: str
    public_aggregate_only: bool
    restricted_data: bool
    personal_data: bool
    taxpayer_level_data: bool
    firm_confidential_data: bool
    household_microdata: bool
    safe_for_repo_use: bool
    loaded_status: str
    reason_if_not_loaded: str
    allowed_use: list[str]
    must_not_infer: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicRealAggregateValue:
    value_id: str
    source_id: str
    publisher: str
    source_name: str
    source_url: str
    source_locator: str
    metric_name: str
    value: int | float | str
    unit: str
    period: str
    geography: str
    industry_or_sector: str
    extraction_method: str
    value_review_status: str
    claim_level: str
    data_status: str
    public_aggregate_only: bool
    restricted_data: bool
    personal_data: bool
    safe_for_repo_use: bool
    used_for: list[str]
    not_used_for: list[str]
    must_not_infer: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicRealDataGuardrailFinding:
    finding_id: str
    guardrail: str
    status: str
    finding: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicRealDataDigestEntry:
    path: str
    sha256: str
    bytes: int
    digest_scope: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicRealDataLoadSummary:
    total_sources: int
    loaded_sources: int
    source_candidates_not_loaded: int
    blocked_sources: int
    rejected_sources: int
    loaded_values_total: int
    loaded_value_units_present: int
    loaded_value_periods_present: int
    loaded_value_geographies_present: int
    guardrail_findings_total: int
    guardrail_fail_closed_findings: int
    digest_targets_total: int
    digests_written: int
    forbidden_claim_findings: int
    public_real_data_loader_created: bool
    real_public_aggregate_data_loaded: bool
    new_public_aggregate_values_loaded: int
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
    warnings: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PublicRealDataLoadResult:
    manifest_id: str
    manifest_name: str
    status: str
    non_claims: list[str]
    sources: list[PublicRealDataSource]
    loaded_public_aggregate_values: list[PublicRealAggregateValue]
    source_candidates_not_loaded: list[PublicRealDataSource]
    guardrail_findings: list[PublicRealDataGuardrailFinding]
    future_build_32_requirements: list[str]
    summary: PublicRealDataLoadSummary

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _required_mapping(source: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [field for field in fields if field not in source]
    if missing:
        raise ValueError(f"{label} missing required fields: {', '.join(missing)}")


def _non_empty(value: Any, field: str) -> str:
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field} must be non-empty")
    return text


def _choice(value: str, allowed: set[str], field: str) -> str:
    if value not in allowed:
        raise ValueError(f"{field} has invalid value {value!r}; expected one of {sorted(allowed)}")
    return value


def _bool(value: Any, field: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{field} must be boolean")
    return value


def _list_of_strings(value: Any, field: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item.strip() for item in value):
        raise ValueError(f"{field} must be a non-empty list of strings")
    return [item.strip() for item in value]


def _is_negative_context(text: str, phrase_start: int) -> bool:
    window = text[max(0, phrase_start - 160) : phrase_start].lower()
    return any(marker in window for marker in NEGATIVE_CONTEXT_MARKERS)


def find_forbidden_affirmative_public_real_claims(text: str) -> list[str]:
    lowered = text.lower()
    findings: list[str] = []
    for phrase in FORBIDDEN_AFFIRMATIVE_PUBLIC_REAL_CLAIMS:
        start = 0
        while True:
            index = lowered.find(phrase, start)
            if index == -1:
                break
            if not _is_negative_context(lowered, index):
                findings.append(phrase)
                break
            start = index + len(phrase)
    return sorted(set(findings))


def _source_from_mapping(source: dict[str, Any]) -> PublicRealDataSource:
    _required_mapping(
        source,
        [
            "source_id",
            "publisher",
            "source_name",
            "source_url",
            "source_locator",
            "source_file_name",
            "source_file_type",
            "access_method",
            "access_date",
            "licence_or_access_note",
            "public_aggregate_only",
            "restricted_data",
            "personal_data",
            "taxpayer_level_data",
            "firm_confidential_data",
            "household_microdata",
            "safe_for_repo_use",
            "loaded_status",
            "reason_if_not_loaded",
            "allowed_use",
            "must_not_infer",
        ],
        "public real data source",
    )
    loaded_status = _choice(str(source["loaded_status"]), SOURCE_LOAD_STATUS_VALUES, "loaded_status")
    item = PublicRealDataSource(
        source_id=_non_empty(source["source_id"], "source_id"),
        publisher=_non_empty(source["publisher"], "publisher"),
        source_name=_non_empty(source["source_name"], "source_name"),
        source_url=_non_empty(source["source_url"], "source_url"),
        source_locator=_non_empty(source["source_locator"], "source_locator"),
        source_file_name=_non_empty(source["source_file_name"], "source_file_name"),
        source_file_type=_non_empty(source["source_file_type"], "source_file_type"),
        access_method=_non_empty(source["access_method"], "access_method"),
        access_date=_non_empty(source["access_date"], "access_date"),
        licence_or_access_note=_non_empty(source["licence_or_access_note"], "licence_or_access_note"),
        public_aggregate_only=_bool(source["public_aggregate_only"], "public_aggregate_only"),
        restricted_data=_bool(source["restricted_data"], "restricted_data"),
        personal_data=_bool(source["personal_data"], "personal_data"),
        taxpayer_level_data=_bool(source["taxpayer_level_data"], "taxpayer_level_data"),
        firm_confidential_data=_bool(source["firm_confidential_data"], "firm_confidential_data"),
        household_microdata=_bool(source["household_microdata"], "household_microdata"),
        safe_for_repo_use=_bool(source["safe_for_repo_use"], "safe_for_repo_use"),
        loaded_status=loaded_status,
        reason_if_not_loaded=str(source["reason_if_not_loaded"]).strip(),
        allowed_use=_list_of_strings(source["allowed_use"], "allowed_use"),
        must_not_infer=_list_of_strings(source["must_not_infer"], "must_not_infer"),
    )
    if item.loaded_status == "loaded":
        if not item.source_url.startswith("https://"):
            raise ValueError(f"loaded source lacks https source_url: {item.source_id}")
        if item.restricted_data:
            raise ValueError(f"loaded source has restricted_data true: {item.source_id}")
        if item.personal_data:
            raise ValueError(f"loaded source has personal_data true: {item.source_id}")
        if item.taxpayer_level_data:
            raise ValueError(f"loaded source has taxpayer_level_data true: {item.source_id}")
        if item.firm_confidential_data:
            raise ValueError(f"loaded source has firm_confidential_data true: {item.source_id}")
        if item.household_microdata:
            raise ValueError(f"loaded source has household_microdata true: {item.source_id}")
        if not item.public_aggregate_only:
            raise ValueError(f"loaded source is not public aggregate only: {item.source_id}")
        if not item.safe_for_repo_use:
            raise ValueError(f"loaded source is not safe_for_repo_use: {item.source_id}")
    else:
        if not item.reason_if_not_loaded:
            raise ValueError(f"not-loaded source must explain reason_if_not_loaded: {item.source_id}")
    return item


def _value_from_mapping(source: dict[str, Any], source_item: PublicRealDataSource) -> PublicRealAggregateValue:
    _required_mapping(
        source,
        [
            "value_id",
            "metric_name",
            "value",
            "unit",
            "period",
            "geography",
            "industry_or_sector",
            "extraction_method",
            "value_review_status",
            "claim_level",
            "used_for",
            "not_used_for",
            "must_not_infer",
        ],
        "public real aggregate value",
    )
    if source.get("value") is None or str(source.get("value")).strip() == "":
        raise ValueError("public real aggregate value must include value")
    value = PublicRealAggregateValue(
        value_id=_non_empty(source["value_id"], "value_id"),
        source_id=source_item.source_id,
        publisher=source_item.publisher,
        source_name=source_item.source_name,
        source_url=source_item.source_url,
        source_locator=source_item.source_locator,
        metric_name=_non_empty(source["metric_name"], "metric_name"),
        value=source["value"],
        unit=_non_empty(source["unit"], "unit"),
        period=_non_empty(source["period"], "period"),
        geography=_non_empty(source["geography"], "geography"),
        industry_or_sector=_non_empty(source["industry_or_sector"], "industry_or_sector"),
        extraction_method=_non_empty(source["extraction_method"], "extraction_method"),
        value_review_status=_choice(str(source["value_review_status"]), VALUE_REVIEW_STATUS_VALUES, "value_review_status"),
        claim_level=_choice(str(source["claim_level"]), CLAIM_LEVEL_VALUES, "value claim_level"),
        data_status="loaded_public_aggregate",
        public_aggregate_only=True,
        restricted_data=False,
        personal_data=False,
        safe_for_repo_use=True,
        used_for=_list_of_strings(source["used_for"], "used_for"),
        not_used_for=_list_of_strings(source["not_used_for"], "not_used_for"),
        must_not_infer=_list_of_strings(source["must_not_infer"], "must_not_infer"),
    )
    if value.claim_level != "real_public_aggregate_data":
        raise ValueError(f"loaded value must use claim_level real_public_aggregate_data: {value.value_id}")
    return value


def _validate_public_real_files(repo_root: Path) -> list[PublicRealDataGuardrailFinding]:
    public_real_root = repo_root / "data" / "public_real"
    findings: list[PublicRealDataGuardrailFinding] = []
    blocked_paths: list[str] = []
    blocked_suffixes: list[str] = []
    for path in public_real_root.rglob("*"):
        if path.is_dir():
            continue
        relative = str(path.relative_to(repo_root)).replace("\\", "/")
        lower = relative.lower()
        if any(part in lower for part in ["private", "restricted", "secure_drop", "incoming"]):
            blocked_paths.append(relative)
        if path.suffix.lower() in {".csv", ".xlsx", ".xls", ".parquet", ".db", ".sqlite", ".jsonl"}:
            blocked_suffixes.append(relative)
    findings.append(
        PublicRealDataGuardrailFinding(
            finding_id="public_real_restricted_path_scan",
            guardrail="No restricted/private public-real paths are present.",
            status="clean" if not blocked_paths else "fail_closed",
            finding=", ".join(blocked_paths) if blocked_paths else "no restricted public-real paths found",
        )
    )
    findings.append(
        PublicRealDataGuardrailFinding(
            finding_id="public_real_dataset_extension_scan",
            guardrail="No raw dataset file types are committed in Build 31.",
            status="clean" if not blocked_suffixes else "fail_closed",
            finding=", ".join(blocked_suffixes) if blocked_suffixes else "no unapproved raw dataset-like files found",
        )
    )
    return findings


def build_public_real_data_load_result(
    manifest: dict[str, Any],
    repo_root: Path,
    digest_targets_total: int,
    digests_written: int,
) -> PublicRealDataLoadResult:
    _required_mapping(
        manifest,
        [
            "manifest_id",
            "manifest_name",
            "status",
            "non_claims",
            "source_load_status_taxonomy",
            "value_review_status_taxonomy",
            "claim_level_taxonomy",
            "guardrail_status_taxonomy",
            "sources",
            "build_31_flags",
            "forbidden_claims",
            "future_build_32_requirements",
        ],
        "public real data source manifest",
    )
    if manifest["status"] != "public_real_aggregate_data_loader_only":
        raise ValueError("public real data manifest status must be public_real_aggregate_data_loader_only")
    for non_claim in PUBLIC_REAL_DATA_NON_CLAIMS:
        if non_claim not in manifest["non_claims"]:
            raise ValueError("public real data manifest missing required non-claim language")
    if set(manifest["source_load_status_taxonomy"]) != SOURCE_LOAD_STATUS_VALUES:
        raise ValueError("source_load_status_taxonomy does not match required values")
    if set(manifest["value_review_status_taxonomy"]) != VALUE_REVIEW_STATUS_VALUES:
        raise ValueError("value_review_status_taxonomy does not match required values")
    if set(manifest["claim_level_taxonomy"]) != CLAIM_LEVEL_VALUES:
        raise ValueError("claim_level_taxonomy does not match required values")
    if set(manifest["guardrail_status_taxonomy"]) != GUARDRAIL_STATUS_VALUES:
        raise ValueError("guardrail_status_taxonomy does not match required values")

    sources: list[PublicRealDataSource] = []
    values: list[PublicRealAggregateValue] = []
    for source_mapping in manifest["sources"]:
        source_item = _source_from_mapping(source_mapping)
        sources.append(source_item)
        source_values = source_mapping.get("values", [])
        if source_item.loaded_status == "loaded" and not source_values:
            raise ValueError(f"loaded source must contain at least one value: {source_item.source_id}")
        if source_item.loaded_status != "loaded" and source_values:
            raise ValueError(f"not-loaded source cannot carry values: {source_item.source_id}")
        for value_mapping in source_values:
            values.append(_value_from_mapping(value_mapping, source_item))

    if len({value.value_id for value in values}) != len(values):
        raise ValueError("public real aggregate value ids must be unique")
    candidates_not_loaded = [item for item in sources if item.loaded_status == "source_candidate_not_loaded"]
    blocked_sources = [item for item in sources if item.loaded_status == "blocked"]
    rejected_sources = [item for item in sources if item.loaded_status == "rejected"]
    loaded_sources = [item for item in sources if item.loaded_status == "loaded"]
    guardrail_findings = _validate_public_real_files(repo_root)
    fail_closed_count = sum(item.status == "fail_closed" for item in guardrail_findings)
    if fail_closed_count:
        raise ValueError("public real data guardrail scan failed closed")

    flags = manifest["build_31_flags"]
    expected_false_flags = [
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
    for flag in expected_false_flags:
        if flags.get(flag) is not False:
            raise ValueError(f"build_31_flags.{flag} must be false")
    if flags.get("public_real_data_loader_created") is not True:
        raise ValueError("build_31_flags.public_real_data_loader_created must be true")
    if flags.get("real_public_aggregate_data_loaded") is not bool(values):
        raise ValueError("build_31_flags.real_public_aggregate_data_loaded does not match loaded values")

    scan_manifest = {key: value for key, value in manifest.items() if key != "forbidden_claims"}
    combined_for_claim_scan = str(scan_manifest)
    forbidden_claims = find_forbidden_affirmative_public_real_claims(combined_for_claim_scan)
    if forbidden_claims:
        raise ValueError(f"public real data manifest contains forbidden affirmative claims: {', '.join(forbidden_claims)}")

    summary = PublicRealDataLoadSummary(
        total_sources=len(sources),
        loaded_sources=len(loaded_sources),
        source_candidates_not_loaded=len(candidates_not_loaded),
        blocked_sources=len(blocked_sources),
        rejected_sources=len(rejected_sources),
        loaded_values_total=len(values),
        loaded_value_units_present=sum(bool(item.unit) for item in values),
        loaded_value_periods_present=sum(bool(item.period) for item in values),
        loaded_value_geographies_present=sum(bool(item.geography) for item in values),
        guardrail_findings_total=len(guardrail_findings),
        guardrail_fail_closed_findings=fail_closed_count,
        digest_targets_total=digest_targets_total,
        digests_written=digests_written,
        forbidden_claim_findings=0,
        public_real_data_loader_created=True,
        real_public_aggregate_data_loaded=bool(values),
        new_public_aggregate_values_loaded=len(values),
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
        warnings=[
            "Loaded values are public aggregate/source-located records only.",
            "Source candidates without exact safe values remain not loaded.",
            "Calibration, validation, model-proof, official-status, and tax-payable claims remain false.",
        ],
    )
    return PublicRealDataLoadResult(
        manifest_id=str(manifest["manifest_id"]),
        manifest_name=str(manifest["manifest_name"]),
        status=str(manifest["status"]),
        non_claims=list(manifest["non_claims"]),
        sources=sources,
        loaded_public_aggregate_values=values,
        source_candidates_not_loaded=candidates_not_loaded,
        guardrail_findings=guardrail_findings,
        future_build_32_requirements=_list_of_strings(manifest["future_build_32_requirements"], "future_build_32_requirements"),
        summary=summary,
    )
