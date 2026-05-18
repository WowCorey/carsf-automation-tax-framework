"""Non-operative legislative architecture skeleton for CARSF V1.5.

This module validates and reports conceptual architecture metadata only. It
does not draft operative law, create powers, create obligations, issue notices,
create penalties, implement enforcement, or modify firm-level CARSF liability.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


LEGISLATIVE_ARCHITECTURE_WARNING = (
    "This is a non-operative legislative architecture skeleton only. It is not operative law. "
    "It is not a Bill. It is not legal drafting. It is not legal advice. It is not tax advice. "
    "It is not ATO guidance. It is not Treasury modelling. It is not Parliamentary Counsel drafting. "
    "It is not legally sufficient and it has not been constitutionally reviewed. It creates no rights, "
    "obligations, statutory powers, information-gathering powers, notices, penalties, enforcement process, "
    "or compliance scoring. It does not determine tax payable, does not use taxpayer-level, firm-level, industry, "
    "ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, and does not modify firm-level CARSF liability."
)
LEGISLATIVE_ARCHITECTURE_NON_CLAIMS = [
    LEGISLATIVE_ARCHITECTURE_WARNING,
    "The skeleton maps conceptual architecture only for external legal, tax, Treasury, ATO, Parliamentary Counsel, privacy, calibration, administrative-design, and policy review.",
    "All Parts, Divisions, definitions, schedules, evidence placeholders, safeguards, regulation-making placeholders, and anti-avoidance placeholders are reserved for external drafting review before any real use.",
]

REQUIRED_CORE_DEFINITIONS = {
    "CARSF",
    "Qualified Labour Contribution",
    "QLC",
    "Output-Linked Full-Time Equivalent",
    "OPFTE",
    "Human Labour Equivalent",
    "HLE",
    "Automation Intensity Index",
    "AII",
    "National Labour Tax Gap",
    "NLTG",
    "Australian Automated Value Added",
    "AAVA",
    "Automation Exposure Levy",
    "AEL",
    "Automation Rent Levy",
    "ARL",
    "CARS-I",
    "CoverageRatio",
    "sector schedule",
    "canonical output unit",
    "safe harbour",
    "grouped entity",
    "related-party automation service",
    "offshore automation service",
    "mixed-unit activity",
    "evidence bundle",
    "review queue",
    "external calibration",
    "schedule authority",
    "transition payment",
    "automation dividend",
}

REQUIRED_SCHEDULE_IDS = {
    "automotive_repair",
    "logistics_warehousing",
    "call_centres_customer_support",
    "accounting_administration",
    "retail_self_checkout_fulfilment",
    "software_digital_platforms",
}

LEGAL_REVIEW_FLAG_FIELDS = [
    "requires_legal_review",
    "requires_tax_review",
    "requires_ato_methods_review",
    "requires_treasury_review",
    "requires_privacy_review",
    "requires_external_calibration",
]

FORBIDDEN_AFFIRMATIVE_LEGAL_CLAIMS = [
    "legally sufficient",
    "legislative-ready",
    "bill-ready",
    "parliament-ready",
    "official legal architecture",
    "official bill",
    "operative law",
    "enforceable provision",
    "valid law",
    "lawful power",
    "statutory power is created",
    "information-gathering power is created",
    "notice is issued",
    "penalty applies",
    "offence",
    "taxpayer must pay",
    "firm is liable",
    "commissioner may require",
    "ato may require",
    "ato will audit",
    "official ato process",
    "ato guidance",
    "treasury validated",
    "ato validated",
    "actual tax payable",
    "binding obligation",
    "real review right",
    "appeal right created",
    "objection right created",
    "regulation-making power is created",
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
    "creates no ",
    "create no ",
    "created no ",
    "is not ",
    "are not ",
    "has not ",
    "have not ",
    "without ",
]


@dataclass(frozen=True)
class LegislativeArchitectureDivision:
    division_id: str
    division_title: str
    conceptual_scope: str
    linked_existing_layer: str
    placeholder_provision_types: list[str]
    requires_legal_review: bool
    requires_tax_review: bool
    requires_ato_methods_review: bool
    requires_treasury_review: bool
    requires_privacy_review: bool
    requires_external_calibration: bool
    forbidden_operational_claims: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LegislativeArchitecturePart:
    part_id: str
    part_title: str
    purpose: str
    non_operative_status: bool
    linked_carsf_modules: list[str]
    linked_reports: list[str]
    divisions: list[LegislativeArchitectureDivision]
    external_review_required: bool
    drafting_risk: str
    main_reason: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LegislativeDefinitionPlaceholder:
    term: str
    plain_english_description: str
    linked_module_or_doc: str
    drafting_status: str
    requires_legal_review: bool
    requires_tax_review: bool
    requires_policy_review: bool
    must_not_be_used_as_operative_definition: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LegislativeSchedulePlaceholder:
    schedule_id: str
    schedule_name: str
    source_yaml: str
    status: str
    calibration_status: str
    legal_attribution_status: str
    capital_base_issue: str
    multi_schedule_attribution_issue: str
    requires_external_calibration: bool
    requires_legal_review: bool
    must_not_be_treated_as_official_schedule: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LegislativeProvisionPlaceholder:
    placeholder_id: str
    placeholder_title: str
    conceptual_scope: str
    placeholder_type: str
    flags: dict[str, bool]
    review_requirements: list[str]
    non_claims: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LegislativeReviewBlocker:
    blocker_id: str
    blocker_title: str
    blocker_type: str
    affected_parts: list[str]
    required_review: list[str]
    locked_or_reserved_for_counsel: bool
    main_reason: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LegislativeArchitectureSummary:
    total_parts: int
    total_divisions: int
    total_definition_placeholders: int
    total_schedule_placeholders: int
    total_regulation_making_placeholders: int
    total_safeguard_placeholders: int
    total_evidence_power_placeholders: int
    total_anti_avoidance_placeholders: int
    total_commencement_transition_placeholders: int
    parts_requiring_legal_review: int
    parts_requiring_tax_review: int
    parts_requiring_ato_methods_review: int
    parts_requiring_treasury_review: int
    parts_requiring_privacy_review: int
    parts_requiring_external_calibration: int
    locked_or_reserved_for_counsel_count: int
    operative_law_created: bool
    legal_sufficiency_claimed: bool
    statutory_power_created: bool
    notices_created: bool
    penalties_created: bool
    enforcement_created: bool
    real_data_used: bool
    firm_level_liability_logic_modified: bool
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(LEGISLATIVE_ARCHITECTURE_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LegislativeArchitectureResult:
    architecture_id: str
    architecture_name: str
    status: str
    parts: list[LegislativeArchitecturePart]
    definitions: list[LegislativeDefinitionPlaceholder]
    schedules: list[LegislativeSchedulePlaceholder]
    regulation_making_placeholders: list[LegislativeProvisionPlaceholder]
    safeguards: list[LegislativeProvisionPlaceholder]
    evidence_power_placeholders: list[LegislativeProvisionPlaceholder]
    anti_avoidance_placeholders: list[LegislativeProvisionPlaceholder]
    commencement_transition_placeholders: list[LegislativeProvisionPlaceholder]
    external_review_blockers: list[LegislativeReviewBlocker]
    locked_or_reserved_for_counsel_areas: list[str]
    summary: LegislativeArchitectureSummary
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(LEGISLATIVE_ARCHITECTURE_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _required_mapping(source: dict[str, Any], fields: list[str], label: str) -> None:
    missing = [field for field in fields if field not in source]
    if missing:
        raise ValueError(f"{label} missing required fields: {', '.join(missing)}")


def _bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be boolean")
    return value


def _list_of_strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{label} must be a list of strings")
    return list(value)


def _path_exists(repo_root: Path, relative_path: str, label: str) -> None:
    if relative_path in {"not_applicable", "reserved_for_counsel"}:
        return
    if not (repo_root / relative_path).exists():
        raise ValueError(f"{label} references missing path: {relative_path}")


def _normalise_text(value: Any) -> str:
    return str(value).lower().replace("`", "")


def _has_negative_context(text: str, phrase_start: int) -> bool:
    window = text[max(0, phrase_start - 36) : phrase_start]
    return any(marker in window for marker in NEGATIVE_CONTEXT_MARKERS)


def find_forbidden_affirmative_claims(text: str) -> list[str]:
    lowered = _normalise_text(text)
    findings: list[str] = []
    for phrase in FORBIDDEN_AFFIRMATIVE_LEGAL_CLAIMS:
        start = 0
        while True:
            index = lowered.find(phrase, start)
            if index == -1:
                break
            if not _has_negative_context(lowered, index):
                findings.append(phrase)
                break
            start = index + len(phrase)
    return sorted(set(findings))


def _division_from_mapping(source: dict[str, Any], label: str) -> LegislativeArchitectureDivision:
    _required_mapping(
        source,
        [
            "division_id",
            "division_title",
            "conceptual_scope",
            "linked_existing_layer",
            "placeholder_provision_types",
            *LEGAL_REVIEW_FLAG_FIELDS,
            "forbidden_operational_claims",
        ],
        label,
    )
    return LegislativeArchitectureDivision(
        division_id=str(source["division_id"]),
        division_title=str(source["division_title"]),
        conceptual_scope=str(source["conceptual_scope"]),
        linked_existing_layer=str(source["linked_existing_layer"]),
        placeholder_provision_types=_list_of_strings(source["placeholder_provision_types"], f"{label}.placeholder_provision_types"),
        requires_legal_review=_bool(source["requires_legal_review"], f"{label}.requires_legal_review"),
        requires_tax_review=_bool(source["requires_tax_review"], f"{label}.requires_tax_review"),
        requires_ato_methods_review=_bool(source["requires_ato_methods_review"], f"{label}.requires_ato_methods_review"),
        requires_treasury_review=_bool(source["requires_treasury_review"], f"{label}.requires_treasury_review"),
        requires_privacy_review=_bool(source["requires_privacy_review"], f"{label}.requires_privacy_review"),
        requires_external_calibration=_bool(source["requires_external_calibration"], f"{label}.requires_external_calibration"),
        forbidden_operational_claims=_list_of_strings(source["forbidden_operational_claims"], f"{label}.forbidden_operational_claims"),
    )


def _part_from_mapping(source: dict[str, Any], repo_root: Path) -> LegislativeArchitecturePart:
    _required_mapping(
        source,
        [
            "part_id",
            "part_title",
            "purpose",
            "non_operative_status",
            "linked_carsf_modules",
            "linked_reports",
            "divisions",
            "external_review_required",
            "drafting_risk",
            "main_reason",
        ],
        f"part {source.get('part_id', '?')}",
    )
    if source["non_operative_status"] is not True:
        raise ValueError(f"{source['part_id']} must be marked non-operative")
    modules = _list_of_strings(source["linked_carsf_modules"], f"{source['part_id']}.linked_carsf_modules")
    reports = _list_of_strings(source["linked_reports"], f"{source['part_id']}.linked_reports")
    for module in modules:
        _path_exists(repo_root, module, f"{source['part_id']} linked module")
    for report in reports:
        _path_exists(repo_root, report, f"{source['part_id']} linked report")
    divisions_source = source["divisions"]
    if not isinstance(divisions_source, list) or not divisions_source:
        raise ValueError(f"{source['part_id']} must include at least one Division")
    divisions = [
        _division_from_mapping(item, f"{source['part_id']}.division[{index}]")
        for index, item in enumerate(divisions_source)
    ]
    return LegislativeArchitecturePart(
        part_id=str(source["part_id"]),
        part_title=str(source["part_title"]),
        purpose=str(source["purpose"]),
        non_operative_status=True,
        linked_carsf_modules=modules,
        linked_reports=reports,
        divisions=divisions,
        external_review_required=_bool(source["external_review_required"], f"{source['part_id']}.external_review_required"),
        drafting_risk=str(source["drafting_risk"]),
        main_reason=str(source["main_reason"]),
    )


def _definition_from_mapping(source: dict[str, Any], repo_root: Path) -> LegislativeDefinitionPlaceholder:
    _required_mapping(
        source,
        [
            "term",
            "plain_english_description",
            "linked_module_or_doc",
            "drafting_status",
            "requires_legal_review",
            "requires_tax_review",
            "requires_policy_review",
            "must_not_be_used_as_operative_definition",
        ],
        f"definition {source.get('term', '?')}",
    )
    _path_exists(repo_root, str(source["linked_module_or_doc"]), f"definition {source['term']}")
    if source["must_not_be_used_as_operative_definition"] is not True:
        raise ValueError(f"definition {source['term']} must not be usable as an operative definition")
    return LegislativeDefinitionPlaceholder(
        term=str(source["term"]),
        plain_english_description=str(source["plain_english_description"]),
        linked_module_or_doc=str(source["linked_module_or_doc"]),
        drafting_status=str(source["drafting_status"]),
        requires_legal_review=_bool(source["requires_legal_review"], f"definition {source['term']}.requires_legal_review"),
        requires_tax_review=_bool(source["requires_tax_review"], f"definition {source['term']}.requires_tax_review"),
        requires_policy_review=_bool(source["requires_policy_review"], f"definition {source['term']}.requires_policy_review"),
        must_not_be_used_as_operative_definition=True,
    )


def _schedule_from_mapping(source: dict[str, Any], repo_root: Path) -> LegislativeSchedulePlaceholder:
    _required_mapping(
        source,
        [
            "schedule_id",
            "schedule_name",
            "source_yaml",
            "status",
            "calibration_status",
            "legal_attribution_status",
            "capital_base_issue",
            "multi_schedule_attribution_issue",
            "requires_external_calibration",
            "requires_legal_review",
            "must_not_be_treated_as_official_schedule",
        ],
        f"schedule {source.get('schedule_id', '?')}",
    )
    _path_exists(repo_root, str(source["source_yaml"]), f"schedule {source['schedule_id']}")
    if source["must_not_be_treated_as_official_schedule"] is not True:
        raise ValueError(f"schedule {source['schedule_id']} must be marked not official")
    return LegislativeSchedulePlaceholder(
        schedule_id=str(source["schedule_id"]),
        schedule_name=str(source["schedule_name"]),
        source_yaml=str(source["source_yaml"]),
        status=str(source["status"]),
        calibration_status=str(source["calibration_status"]),
        legal_attribution_status=str(source["legal_attribution_status"]),
        capital_base_issue=str(source["capital_base_issue"]),
        multi_schedule_attribution_issue=str(source["multi_schedule_attribution_issue"]),
        requires_external_calibration=_bool(source["requires_external_calibration"], f"schedule {source['schedule_id']}.requires_external_calibration"),
        requires_legal_review=_bool(source["requires_legal_review"], f"schedule {source['schedule_id']}.requires_legal_review"),
        must_not_be_treated_as_official_schedule=True,
    )


def _provision_from_mapping(source: dict[str, Any], label: str) -> LegislativeProvisionPlaceholder:
    _required_mapping(
        source,
        ["placeholder_id", "placeholder_title", "conceptual_scope", "placeholder_type", "flags", "review_requirements", "non_claims"],
        label,
    )
    flags = source["flags"]
    if not isinstance(flags, dict) or not flags:
        raise ValueError(f"{label}.flags must be a non-empty mapping")
    normalised_flags = {str(key): _bool(value, f"{label}.flags.{key}") for key, value in flags.items()}
    return LegislativeProvisionPlaceholder(
        placeholder_id=str(source["placeholder_id"]),
        placeholder_title=str(source["placeholder_title"]),
        conceptual_scope=str(source["conceptual_scope"]),
        placeholder_type=str(source["placeholder_type"]),
        flags=normalised_flags,
        review_requirements=_list_of_strings(source["review_requirements"], f"{label}.review_requirements"),
        non_claims=_list_of_strings(source["non_claims"], f"{label}.non_claims"),
    )


def _blocker_from_mapping(source: dict[str, Any]) -> LegislativeReviewBlocker:
    _required_mapping(
        source,
        ["blocker_id", "blocker_title", "blocker_type", "affected_parts", "required_review", "locked_or_reserved_for_counsel", "main_reason"],
        f"external review blocker {source.get('blocker_id', '?')}",
    )
    if source["locked_or_reserved_for_counsel"] is not True:
        raise ValueError(f"external review blocker {source['blocker_id']} must be locked or reserved for counsel")
    return LegislativeReviewBlocker(
        blocker_id=str(source["blocker_id"]),
        blocker_title=str(source["blocker_title"]),
        blocker_type=str(source["blocker_type"]),
        affected_parts=_list_of_strings(source["affected_parts"], f"blocker {source['blocker_id']}.affected_parts"),
        required_review=_list_of_strings(source["required_review"], f"blocker {source['blocker_id']}.required_review"),
        locked_or_reserved_for_counsel=True,
        main_reason=str(source["main_reason"]),
    )


def _validate_provision_flags(payload: list[LegislativeProvisionPlaceholder], required_true: list[str], label: str) -> None:
    for item in payload:
        missing = [flag for flag in required_true if item.flags.get(flag) is not True]
        if missing:
            raise ValueError(f"{label} {item.placeholder_id} missing required true flags: {', '.join(missing)}")


def build_legislative_architecture_result(payload: dict[str, Any], repo_root: Path) -> LegislativeArchitectureResult:
    _required_mapping(
        payload,
        [
            "architecture_id",
            "architecture_name",
            "status",
            "non_claims",
            "parts",
            "definitions",
            "schedules",
            "regulation_making_placeholders",
            "external_review_blockers",
            "safeguards",
            "evidence_power_placeholders",
            "anti_avoidance_placeholders",
            "commencement_transition_placeholders",
            "forbidden_claims",
        ],
        "legislative architecture payload",
    )
    if payload["status"] != "non_operative_architecture_skeleton_only":
        raise ValueError("legislative architecture status must be non_operative_architecture_skeleton_only")
    for claim in LEGISLATIVE_ARCHITECTURE_NON_CLAIMS:
        if claim not in payload["non_claims"]:
            raise ValueError("legislative architecture payload missing required non-claim language")

    parts = [_part_from_mapping(item, repo_root) for item in payload["parts"]]
    definitions = [_definition_from_mapping(item, repo_root) for item in payload["definitions"]]
    schedules = [_schedule_from_mapping(item, repo_root) for item in payload["schedules"]]
    regulation_placeholders = [
        _provision_from_mapping(item, f"regulation_making_placeholders[{index}]")
        for index, item in enumerate(payload["regulation_making_placeholders"])
    ]
    safeguards = [
        _provision_from_mapping(item, f"safeguards[{index}]")
        for index, item in enumerate(payload["safeguards"])
    ]
    evidence_power_placeholders = [
        _provision_from_mapping(item, f"evidence_power_placeholders[{index}]")
        for index, item in enumerate(payload["evidence_power_placeholders"])
    ]
    anti_avoidance_placeholders = [
        _provision_from_mapping(item, f"anti_avoidance_placeholders[{index}]")
        for index, item in enumerate(payload["anti_avoidance_placeholders"])
    ]
    commencement_transition_placeholders = [
        _provision_from_mapping(item, f"commencement_transition_placeholders[{index}]")
        for index, item in enumerate(payload["commencement_transition_placeholders"])
    ]
    blockers = [_blocker_from_mapping(item) for item in payload["external_review_blockers"]]

    terms = {item.term for item in definitions}
    missing_terms = sorted(REQUIRED_CORE_DEFINITIONS - terms)
    if missing_terms:
        raise ValueError(f"missing required definition placeholders: {', '.join(missing_terms)}")

    schedule_ids = {item.schedule_id for item in schedules}
    missing_schedules = sorted(REQUIRED_SCHEDULE_IDS - schedule_ids)
    if missing_schedules:
        raise ValueError(f"missing schedule placeholders: {', '.join(missing_schedules)}")

    _validate_provision_flags(
        regulation_placeholders,
        [
            "no_real_regulation_making_power_created",
            "requires_constitutional_legal_drafting_review",
            "requires_treasury_ato_methods_review",
            "may_require_parliamentary_scrutiny_design",
        ],
        "regulation-making placeholder",
    )
    _validate_provision_flags(
        safeguards,
        [
            "not_real_review_right",
            "not_real_appeal_right",
            "not_real_objection_process",
            "requires_legal_and_administrative_law_review",
        ],
        "safeguard placeholder",
    )
    _validate_provision_flags(
        evidence_power_placeholders,
        [
            "no_statutory_information_gathering_power_created",
            "no_notice_issued",
            "no_real_evidence_collected",
            "no_taxpayer_data_ingested",
            "no_firm_data_ingested",
            "no_restricted_data_ingested",
            "requires_legal_privacy_secrecy_ato_and_administrative_design_review",
        ],
        "evidence-power placeholder",
    )
    _validate_provision_flags(
        anti_avoidance_placeholders,
        [
            "not_operative_anti_avoidance_rule",
            "not_legal_test",
            "not_ato_position",
            "requires_legal_tax_treasury_ato_international_tax_and_behavioural_review",
        ],
        "anti-avoidance placeholder",
    )

    payload_for_claim_scan = {key: value for key, value in payload.items() if key != "forbidden_claims"}
    serialised_text = str(payload_for_claim_scan)
    forbidden = find_forbidden_affirmative_claims(serialised_text)
    if forbidden:
        raise ValueError(f"legislative architecture payload contains forbidden affirmative claims: {', '.join(forbidden)}")

    all_divisions = [division for part in parts for division in part.divisions]
    locked_areas = sorted({blocker.blocker_title for blocker in blockers if blocker.locked_or_reserved_for_counsel})
    summary = LegislativeArchitectureSummary(
        total_parts=len(parts),
        total_divisions=len(all_divisions),
        total_definition_placeholders=len(definitions),
        total_schedule_placeholders=len(schedules),
        total_regulation_making_placeholders=len(regulation_placeholders),
        total_safeguard_placeholders=len(safeguards),
        total_evidence_power_placeholders=len(evidence_power_placeholders),
        total_anti_avoidance_placeholders=len(anti_avoidance_placeholders),
        total_commencement_transition_placeholders=len(commencement_transition_placeholders),
        parts_requiring_legal_review=sum(any(division.requires_legal_review for division in part.divisions) for part in parts),
        parts_requiring_tax_review=sum(any(division.requires_tax_review for division in part.divisions) for part in parts),
        parts_requiring_ato_methods_review=sum(any(division.requires_ato_methods_review for division in part.divisions) for part in parts),
        parts_requiring_treasury_review=sum(any(division.requires_treasury_review for division in part.divisions) for part in parts),
        parts_requiring_privacy_review=sum(any(division.requires_privacy_review for division in part.divisions) for part in parts),
        parts_requiring_external_calibration=sum(any(division.requires_external_calibration for division in part.divisions) for part in parts),
        locked_or_reserved_for_counsel_count=len(locked_areas),
        operative_law_created=False,
        legal_sufficiency_claimed=False,
        statutory_power_created=False,
        notices_created=False,
        penalties_created=False,
        enforcement_created=False,
        real_data_used=False,
        firm_level_liability_logic_modified=False,
        warnings=[
            "Architecture skeleton is non-operative and reserved for external drafting review.",
            "Required negative non-claim language is present; no affirmative legal sufficiency claim is allowed.",
        ],
    )
    return LegislativeArchitectureResult(
        architecture_id=str(payload["architecture_id"]),
        architecture_name=str(payload["architecture_name"]),
        status=str(payload["status"]),
        parts=parts,
        definitions=definitions,
        schedules=schedules,
        regulation_making_placeholders=regulation_placeholders,
        safeguards=safeguards,
        evidence_power_placeholders=evidence_power_placeholders,
        anti_avoidance_placeholders=anti_avoidance_placeholders,
        commencement_transition_placeholders=commencement_transition_placeholders,
        external_review_blockers=blockers,
        locked_or_reserved_for_counsel_areas=locked_areas,
        summary=summary,
        warnings=list(summary.warnings),
    )
