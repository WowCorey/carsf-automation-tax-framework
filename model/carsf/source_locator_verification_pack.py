"""Source-locator verification pack for the CARSF V1.5 public-data pilot.

This layer converts existing Build 27-29 artefacts into reviewer-facing source
locator cards. It does not load new data, externally verify source values,
complete calibration, validate CARSF, determine tax payable, or modify
firm-level CARSF liability.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .public_data_pilot import (
    FORBIDDEN_AFFIRMATIVE_PUBLIC_DATA_CLAIMS,
    find_forbidden_affirmative_public_data_claims,
)


LOCATOR_STATUS_VALUES = {
    "complete_locator",
    "partial_locator",
    "source_reference_only",
    "placeholder_anchor_only",
    "blocked_by_restricted_data",
    "forbidden_for_repo_use",
}

VERIFICATION_STATUS_VALUES = {
    "ready_for_manual_review",
    "arithmetic_checked_only",
    "source_locator_recorded_only",
    "source_reference_only_not_loaded",
    "placeholder_not_real_data",
    "blocked_until_authorised_access",
    "external_review_required",
}

REVIEWER_WARNING_VALUES = {
    "not_external_verification",
    "not_calibration",
    "not_model_proof",
    "not_tax_payable",
    "not_legal_or_tax_advice",
    "not_official_status",
}

SOURCE_LOCATOR_VERIFICATION_PACK_WARNING = (
    "This is a source-locator verification pack only. No new data is loaded by this build. "
    "This does not externally verify source values, does not scrape public sources, and does not call external APIs. "
    "Ready for manual review does not mean reviewed and does not mean externally verified. This is not calibration; "
    "calibration has not been completed. Public data does not prove the model works. Realistic placeholders remain "
    "placeholders, realistic placeholders are not real data, realistic placeholders are not calibrated, source references "
    "are not loaded datasets, and restricted-data requirements are not data access. This is not legal advice, not tax "
    "advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, "
    "not statistical validation, not operational readiness, not legal sufficiency, and not official status. It does not "
    "determine actual tax payable, does not use taxpayer-level data, firm-level confidential data, household microdata, "
    "ABS DataLab, HILDA microdata, DSS/Services Australia records, ATO taxpayer records, Treasury/PBO confidential "
    "material, or restricted government data, and does not modify firm-level CARSF liability. It only packages locator "
    "metadata and manual-review checklists."
)

SOURCE_LOCATOR_VERIFICATION_PACK_NON_CLAIMS = [
    SOURCE_LOCATOR_VERIFICATION_PACK_WARNING,
    "Locator cards are manual-review aids only; they are not source verified, not externally verified, not validation, not approval, and not calibration.",
    "Loaded public value cards are copied from existing Build 27 extracts only and do not introduce new public values.",
    "Source-reference-only cards are not counted as loaded public data.",
    "Placeholder-anchor cards remain realistic placeholders and are not real data or calibrated values.",
]

FORBIDDEN_AFFIRMATIVE_SOURCE_LOCATOR_CLAIMS = sorted(
    set(FORBIDDEN_AFFIRMATIVE_PUBLIC_DATA_CLAIMS + ["source verified", "externally verified"])
)

NEGATIVE_CONTEXT_MARKERS = [
    "not ",
    "not a ",
    "not an ",
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
    "forbidden",
    "blocked",
    "non-claim",
    "boundary",
    "does_not_show",
    "must_not_infer",
    "must not infer",
    "must_not_claim",
    "reviewer_must_not_infer",
    "forbidden_claim",
    "ready for manual review does not mean",
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


@dataclass(frozen=True)
class ReviewerChecklistItem:
    checklist_id: str
    prompt: str
    reviewer_warning: list[str]
    must_not_infer: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SourceLocatorCard:
    card_id: str
    card_type: str
    locator_status: str
    verification_status: str
    reviewer_warning: list[str]
    reviewer_should_verify: list[str]
    reviewer_must_not_infer: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class LoadedValueLocatorCard:
    card_id: str
    extract_id: str
    source_reference_id: str
    publisher: str
    source_kind: str
    source_url: str
    source_locator: str
    source_value_note: str
    value_review_status: str
    data_status: str
    claim_level: str
    locator_status: str
    verification_status: str
    reviewer_warning: list[str]
    values_summary: str
    units: str
    period: str
    geography: str
    arithmetic_check_summary: str
    linked_evidence_item_id: str
    linked_consistency_audit_finding_id: str
    reviewer_checklist: list[ReviewerChecklistItem]
    reviewer_should_verify: list[str]
    reviewer_must_not_infer: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SourceReferenceOnlyLocatorCard:
    card_id: str
    extract_id: str
    source_reference_id: str
    publisher: str
    source_kind: str
    source_url: str
    publication_or_release_name: str
    data_status: str
    claim_level: str
    locator_status: str
    verification_status: str
    reviewer_warning: list[str]
    why_not_loaded: str
    reviewer_checklist: list[ReviewerChecklistItem]
    reviewer_should_verify: list[str]
    reviewer_must_not_infer: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class PlaceholderAnchorLocatorCard:
    card_id: str
    anchor_id: str
    field_id: str
    placeholder_name: str
    anchor_source_reference_ids: list[str]
    anchor_extract_ids: list[str]
    anchored_to_public_data: bool
    anchor_strength: str
    locator_status: str
    verification_status: str
    reviewer_warning: list[str]
    blocked_by_restricted_data: bool
    missing_data_for_calibration: list[str]
    review_required_before_calibration: list[str]
    reviewer_checklist: list[ReviewerChecklistItem]
    reviewer_should_verify: list[str]
    reviewer_must_not_infer: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RestrictedBlockerLocatorCard:
    card_id: str
    blocker_id: str
    blocker_type: str
    description: str
    affected_fields: list[str]
    affected_modules: list[str]
    locator_status: str
    verification_status: str
    reviewer_warning: list[str]
    required_access_or_review: list[str]
    reviewer_should_verify: list[str]
    reviewer_must_not_infer: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SourceLocatorVerificationSummary:
    total_loaded_value_cards: int
    complete_locator_cards: int
    partial_locator_cards: int
    source_reference_only_cards: int
    placeholder_anchor_cards: int
    restricted_blocker_cards: int
    reviewer_checklist_items_total: int
    fair_work_arithmetic_cards: int
    cards_ready_for_manual_review: int
    cards_source_locator_recorded_only: int
    cards_source_reference_only_not_loaded: int
    cards_placeholder_not_real_data: int
    cards_blocked_until_authorised_access: int
    forbidden_claim_findings: int
    source_locator_pack_created: bool
    new_data_loaded: bool
    external_source_verification_claimed: bool
    manual_review_pack_only: bool
    loaded_value_cards_created: bool
    source_reference_only_cards_created: bool
    placeholder_anchor_cards_created: bool
    restricted_blocker_cards_created: bool
    reviewer_checklists_created: bool
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
class SourceLocatorVerificationResult:
    pack_id: str
    pack_name: str
    status: str
    non_claims: list[str]
    input_artifacts: list[str]
    loaded_value_cards: list[LoadedValueLocatorCard]
    source_reference_only_cards: list[SourceReferenceOnlyLocatorCard]
    placeholder_anchor_cards: list[PlaceholderAnchorLocatorCard]
    restricted_blocker_cards: list[RestrictedBlockerLocatorCard]
    reviewer_checklists: list[ReviewerChecklistItem]
    forbidden_claims: list[str]
    build_29_6_requirements: list[str]
    build_30_requirements: list[str]
    summary: SourceLocatorVerificationSummary

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def find_forbidden_affirmative_source_locator_claims(text: str) -> list[str]:
    lowered = text.lower()
    findings = set(find_forbidden_affirmative_public_data_claims(text))
    for phrase in ["source verified", "externally verified"]:
        start = 0
        while True:
            index = lowered.find(phrase, start)
            if index == -1:
                break
            context = lowered[max(0, index - 260) : min(len(lowered), index + len(phrase) + 100)]
            if not any(marker in context for marker in NEGATIVE_CONTEXT_MARKERS):
                findings.add(phrase)
                break
            start = index + len(phrase)
    return sorted(findings)


def _required_mapping(source: dict[str, Any], keys: list[str], label: str) -> None:
    missing = [key for key in keys if key not in source]
    if missing:
        raise ValueError(f"{label} missing required fields: {', '.join(missing)}")


def _list_of_strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) and item for item in value):
        raise ValueError(f"{label} must be a list of strings")
    return value


def _validate_manifest(payload: dict[str, Any]) -> None:
    _required_mapping(
        payload,
        [
            "pack_id",
            "pack_name",
            "status",
            "non_claims",
            "input_artifacts",
            "locator_status_taxonomy",
            "verification_status_taxonomy",
            "reviewer_warning_taxonomy",
            "required_loaded_value_cards",
            "required_source_reference_only_cards",
            "required_placeholder_anchor_cards",
            "required_restricted_blocker_cards",
            "required_reviewer_checklists",
            "forbidden_claims",
            "build_29_6_requirements",
            "build_30_requirements",
        ],
        "source-locator verification manifest",
    )
    if payload["status"] != "source_locator_verification_pack_only":
        raise ValueError("source-locator verification manifest status must be source_locator_verification_pack_only")
    if set(payload["locator_status_taxonomy"]) != LOCATOR_STATUS_VALUES:
        raise ValueError("locator_status_taxonomy must match required values")
    if set(payload["verification_status_taxonomy"]) != VERIFICATION_STATUS_VALUES:
        raise ValueError("verification_status_taxonomy must match required values")
    if set(payload["reviewer_warning_taxonomy"]) != REVIEWER_WARNING_VALUES:
        raise ValueError("reviewer_warning_taxonomy must match required values")
    for non_claim in SOURCE_LOCATOR_VERIFICATION_PACK_NON_CLAIMS:
        if non_claim not in payload["non_claims"]:
            raise ValueError("source-locator manifest missing required non-claim language")


def _public_pilot_payload(report: dict[str, Any]) -> dict[str, Any]:
    payload = report.get("public_data_pilot")
    if not isinstance(payload, dict):
        raise ValueError("public_data_pilot report payload missing")
    return payload


def _evidence_map_payload(report: dict[str, Any]) -> dict[str, Any]:
    payload = report.get("public_data_evidence_map")
    if not isinstance(payload, dict):
        raise ValueError("public_data_evidence_map report payload missing")
    return payload


def _consistency_audit_payload(report: dict[str, Any]) -> dict[str, Any]:
    payload = report.get("public_data_consistency_audit")
    if not isinstance(payload, dict):
        raise ValueError("public_data_consistency_audit report payload missing")
    return payload


def _values_summary(values: list[dict[str, Any]]) -> str:
    if not values:
        return "source reference only"
    return "; ".join(f"{item.get('value_id')}={item.get('value')} {item.get('unit')}" for item in values)


def _loaded_checklist(card_id: str) -> list[ReviewerChecklistItem]:
    prompts = [
        "Can the public source URL be opened manually?",
        "Can the exact source locator be found manually?",
        "Does the public value match the extracted value?",
        "Does the unit match?",
        "Does the period or year match?",
        "Does the geography match?",
        "Is the value aggregate-only?",
        "Is the value being used only for sanity-check or placeholder-anchor purposes?",
        "Is the value not being overread as calibration?",
        "Is the value not being used to determine actual tax payable?",
    ]
    return [
        ReviewerChecklistItem(
            checklist_id=f"{card_id}_loaded_{index}",
            prompt=prompt,
            reviewer_warning=sorted(REVIEWER_WARNING_VALUES),
            must_not_infer=[
                "not_external_source_verification",
                "not_calibration",
                "not_validation",
                "not_actual_tax_payable",
                "not_official_status",
            ],
        )
        for index, prompt in enumerate(prompts, start=1)
    ]


def _source_reference_only_checklist(card_id: str) -> list[ReviewerChecklistItem]:
    prompts = [
        "Is this only a source reference?",
        "Is no value being counted as loaded?",
        "What future extract would be needed?",
        "Is the missing value clearly marked?",
        "Is there any overclaim?",
    ]
    return [
        ReviewerChecklistItem(
            checklist_id=f"{card_id}_source_reference_{index}",
            prompt=prompt,
            reviewer_warning=sorted(REVIEWER_WARNING_VALUES),
            must_not_infer=["not_loaded_public_data", "not_calibration", "not_validation", "not_actual_tax_payable"],
        )
        for index, prompt in enumerate(prompts, start=1)
    ]


def _placeholder_checklist(card_id: str) -> list[ReviewerChecklistItem]:
    prompts = [
        "Is this still labelled a realistic placeholder?",
        "Is it clearly not real data?",
        "Is it clearly not calibrated?",
        "What restricted data or external review would be needed to replace it?",
        "Is the placeholder basis transparent?",
    ]
    return [
        ReviewerChecklistItem(
            checklist_id=f"{card_id}_placeholder_{index}",
            prompt=prompt,
            reviewer_warning=sorted(REVIEWER_WARNING_VALUES),
            must_not_infer=["not_real_data_replacement", "not_calibration", "not_validation", "not_actual_tax_payable"],
        )
        for index, prompt in enumerate(prompts, start=1)
    ]


def _blocker_checklist(card_id: str) -> list[ReviewerChecklistItem]:
    prompts = [
        "Is the blocker still visible?",
        "Is the blocker not marked as loaded or accessed?",
        "Is any restricted or forbidden data still outside the repository?",
        "What authorised access or review would be needed outside this repository?",
        "Is there any overclaim that the blocker has been resolved?",
    ]
    return [
        ReviewerChecklistItem(
            checklist_id=f"{card_id}_blocker_{index}",
            prompt=prompt,
            reviewer_warning=sorted(REVIEWER_WARNING_VALUES),
            must_not_infer=["not_data_access", "not_external_source_verification", "not_calibration", "not_validation"],
        )
        for index, prompt in enumerate(prompts, start=1)
    ]


def _arithmetic_summary(extract: dict[str, Any]) -> str:
    if extract.get("extract_id") != "fair_work_minimum_wage_2025_extract":
        return "No arithmetic check required; source locator metadata recorded only."
    values = {item["value_id"]: float(item["value"]) for item in extract.get("values", [])}
    hourly = values.get("national_minimum_wage_hourly")
    weekly = values.get("national_minimum_wage_weekly")
    if hourly is None or weekly is None:
        raise ValueError("Fair Work minimum wage extract must include hourly and weekly values")
    expected = round(hourly * 38, 2)
    if abs(expected - weekly) > 0.001:
        raise ValueError(f"Fair Work arithmetic mismatch: {hourly:.2f} * 38 = {expected:.2f}, got {weekly:.2f}")
    return f"{hourly:.2f} * 38 = {weekly:.2f}; arithmetic checked internally only and not externally verified."


def _loaded_verification_status(extract_id: str) -> str:
    if extract_id == "fair_work_minimum_wage_2025_extract":
        return "ready_for_manual_review"
    return "source_locator_recorded_only"


def _loaded_locator_status(extract: dict[str, Any]) -> str:
    if extract.get("source_url") and extract.get("source_locator") and extract.get("source_value_note"):
        return "complete_locator"
    return "partial_locator"


def _finding_id_for_extract(extract_id: str) -> str:
    if extract_id == "fair_work_minimum_wage_2025_extract":
        return "fair_work_wage_arithmetic"
    return "extract_to_evidence_map"


def _build_loaded_cards(
    pilot: dict[str, Any],
    evidence: dict[str, Any],
) -> list[LoadedValueLocatorCard]:
    sources = {item["source_reference_id"]: item for item in pilot.get("source_references", [])}
    evidence_by_extract = {item["extract_id"]: item for item in evidence.get("loaded_extract_evidence", [])}
    cards: list[LoadedValueLocatorCard] = []
    for extract in pilot.get("public_aggregate_extracts", []):
        if extract.get("data_status") != "real_public_data_loaded":
            continue
        extract_id = extract["extract_id"]
        source = sources.get(extract["source_reference_id"])
        if source is None:
            raise ValueError(f"loaded extract references unknown source: {extract_id}")
        evidence_item = evidence_by_extract.get(extract_id)
        if evidence_item is None:
            raise ValueError(f"loaded extract missing from evidence map: {extract_id}")
        for key in ["source_url", "source_locator", "source_value_note", "value_review_status"]:
            if not extract.get(key):
                raise ValueError(f"loaded value card would be missing {key}: {extract_id}")
        if "validation" in str(extract.get("value_review_status", "")).lower() and "not_external_validation" not in str(
            extract.get("value_review_status", "")
        ).lower():
            raise ValueError(f"value_review_status overclaims validation: {extract_id}")
        card_id = f"loaded_value_{extract_id}"
        cards.append(
            LoadedValueLocatorCard(
                card_id=card_id,
                extract_id=extract_id,
                source_reference_id=extract["source_reference_id"],
                publisher=extract["publisher"],
                source_kind=extract["source_kind"],
                source_url=extract["source_url"],
                source_locator=extract["source_locator"],
                source_value_note=extract["source_value_note"],
                value_review_status=extract["value_review_status"],
                data_status=extract["data_status"],
                claim_level=extract["claim_level"],
                locator_status=_loaded_locator_status(extract),
                verification_status=_loaded_verification_status(extract_id),
                reviewer_warning=sorted(REVIEWER_WARNING_VALUES),
                values_summary=evidence_item.get("values_summary") or _values_summary(extract.get("values", [])),
                units=extract.get("units", ""),
                period=str(extract.get("period", "")),
                geography=extract.get("geography", ""),
                arithmetic_check_summary=_arithmetic_summary(extract),
                linked_evidence_item_id=evidence_item["evidence_id"],
                linked_consistency_audit_finding_id=_finding_id_for_extract(extract_id),
                reviewer_checklist=_loaded_checklist(card_id),
                reviewer_should_verify=[
                    "Open the public source URL manually.",
                    "Find the exact source locator manually.",
                    "Compare values, units, period, geography, and aggregate-only status.",
                ],
                reviewer_must_not_infer=[
                    "not_external_source_verification",
                    "not_calibration",
                    "not_validation",
                    "not_ato_validation",
                    "not_treasury_modelling",
                    "not_pbo_costing",
                    "not_actual_tax_payable",
                    "not_official_status",
                ],
            )
        )
    return cards


def _build_source_reference_only_cards(
    pilot: dict[str, Any],
) -> list[SourceReferenceOnlyLocatorCard]:
    sources = {item["source_reference_id"]: item for item in pilot.get("source_references", [])}
    cards: list[SourceReferenceOnlyLocatorCard] = []
    for extract in pilot.get("public_aggregate_extracts", []):
        if extract.get("data_status") != "source_reference_only":
            continue
        if extract.get("values"):
            raise ValueError(f"source-reference-only card has loaded values: {extract['extract_id']}")
        source = sources.get(extract["source_reference_id"])
        if source is None:
            raise ValueError(f"source-reference-only extract references unknown source: {extract['extract_id']}")
        card_id = f"source_reference_only_{extract['extract_id']}"
        cards.append(
            SourceReferenceOnlyLocatorCard(
                card_id=card_id,
                extract_id=extract["extract_id"],
                source_reference_id=extract["source_reference_id"],
                publisher=extract["publisher"],
                source_kind=extract["source_kind"],
                source_url=extract["source_url"],
                publication_or_release_name=source.get("publication_or_release_name", ""),
                data_status=extract["data_status"],
                claim_level=extract["claim_level"],
                locator_status="source_reference_only",
                verification_status="source_reference_only_not_loaded",
                reviewer_warning=sorted(REVIEWER_WARNING_VALUES),
                why_not_loaded=extract.get("blocker", "source reference only; no public value loaded"),
                reviewer_checklist=_source_reference_only_checklist(card_id),
                reviewer_should_verify=[
                    "Confirm the row is source-reference-only.",
                    "Confirm no value is counted as loaded public data.",
                    "Identify what future public extract or review would be needed.",
                ],
                reviewer_must_not_infer=["not_loaded_public_data", "not_calibration", "not_validation", "not_actual_tax_payable"],
            )
        )
    return cards


def _build_placeholder_cards(pilot: dict[str, Any]) -> list[PlaceholderAnchorLocatorCard]:
    cards: list[PlaceholderAnchorLocatorCard] = []
    for anchor in pilot.get("placeholder_anchors", []):
        if anchor.get("current_placeholder_status") != "realistic_placeholder":
            raise ValueError(f"placeholder anchor is not labelled realistic_placeholder: {anchor.get('anchor_id')}")
        if not anchor.get("must_be_labelled_realistic_placeholder") or not anchor.get("must_not_be_labelled_real_data"):
            raise ValueError(f"placeholder anchor boundary labels missing: {anchor.get('anchor_id')}")
        if not anchor.get("must_not_be_labelled_calibrated"):
            raise ValueError(f"placeholder anchor could be mistaken for calibrated data: {anchor.get('anchor_id')}")
        card_id = f"placeholder_anchor_{anchor['anchor_id']}"
        cards.append(
            PlaceholderAnchorLocatorCard(
                card_id=card_id,
                anchor_id=anchor["anchor_id"],
                field_id=anchor["field_id"],
                placeholder_name=anchor["placeholder_name"],
                anchor_source_reference_ids=anchor.get("anchor_source_reference_ids", []),
                anchor_extract_ids=anchor.get("anchor_extract_ids", []),
                anchored_to_public_data=bool(anchor.get("anchored_to_public_data")),
                anchor_strength=anchor.get("anchor_strength", ""),
                locator_status="placeholder_anchor_only",
                verification_status="placeholder_not_real_data",
                reviewer_warning=sorted(REVIEWER_WARNING_VALUES),
                blocked_by_restricted_data=bool(anchor.get("blocked_by_restricted_data")),
                missing_data_for_calibration=anchor.get("missing_data_for_calibration", []),
                review_required_before_calibration=anchor.get("review_required_before_calibration", []),
                reviewer_checklist=_placeholder_checklist(card_id),
                reviewer_should_verify=[
                    "Check that this remains labelled as a realistic placeholder.",
                    "Check that replacement would require restricted data or external review.",
                    "Check that no calibration conclusion is attached.",
                ],
                reviewer_must_not_infer=["not_real_data", "not_calibration", "not_validation", "not_actual_tax_payable"],
            )
        )
    return cards


def _build_blocker_cards(evidence: dict[str, Any]) -> list[RestrictedBlockerLocatorCard]:
    cards: list[RestrictedBlockerLocatorCard] = []
    for row in evidence.get("restricted_blocker_evidence", []):
        if row.get("evidence_status") != "blocked_by_restricted_data":
            raise ValueError(f"restricted blocker is not blocked: {row.get('blocker_id')}")
        card_id = f"restricted_blocker_{row['blocker_id']}"
        cards.append(
            RestrictedBlockerLocatorCard(
                card_id=card_id,
                blocker_id=row["blocker_id"],
                blocker_type=row["blocker_type"],
                description=row["description"],
                affected_fields=row.get("affected_fields", []),
                affected_modules=row.get("affected_modules", []),
                locator_status="blocked_by_restricted_data",
                verification_status="blocked_until_authorised_access",
                reviewer_warning=sorted(REVIEWER_WARNING_VALUES),
                required_access_or_review=row.get("required_access_or_review", []),
                reviewer_should_verify=row.get("what_reviewer_should_check", []) + ["Confirm no restricted data is loaded."],
                reviewer_must_not_infer=row.get("what_reviewer_must_not_infer", [])
                + ["not_external_source_verification", "not_calibration", "not_validation"],
            )
        )
    for row in evidence.get("forbidden_repo_data_evidence", []):
        if row.get("evidence_status") != "forbidden_for_repo_use":
            raise ValueError(f"forbidden repo data item is not forbidden: {row.get('blocker_id')}")
        card_id = f"forbidden_repo_data_{row['blocker_id']}"
        cards.append(
            RestrictedBlockerLocatorCard(
                card_id=card_id,
                blocker_id=row["blocker_id"],
                blocker_type=row["blocker_type"],
                description=row["description"],
                affected_fields=row.get("affected_fields", []),
                affected_modules=row.get("affected_modules", []),
                locator_status="forbidden_for_repo_use",
                verification_status="external_review_required",
                reviewer_warning=sorted(REVIEWER_WARNING_VALUES),
                required_access_or_review=row.get("required_access_or_review", []),
                reviewer_should_verify=row.get("what_reviewer_should_check", []) + ["Confirm forbidden data remains outside the repository."],
                reviewer_must_not_infer=row.get("what_reviewer_must_not_infer", [])
                + ["not_safe_repository_use", "not_calibration", "not_validation"],
            )
        )
    return cards


def build_source_locator_verification_result(
    manifest: dict[str, Any],
    public_pilot_report: dict[str, Any],
    evidence_map_report: dict[str, Any],
    consistency_audit_report: dict[str, Any],
) -> SourceLocatorVerificationResult:
    _validate_manifest(manifest)
    pilot = _public_pilot_payload(public_pilot_report)
    evidence = _evidence_map_payload(evidence_map_report)
    audit = _consistency_audit_payload(consistency_audit_report)
    if not audit.get("summary", {}).get("consistency_audit_created", True):
        raise ValueError("consistency audit report is not created")

    loaded_cards = _build_loaded_cards(pilot, evidence)
    source_only_cards = _build_source_reference_only_cards(pilot)
    placeholder_cards = _build_placeholder_cards(pilot)
    blocker_cards = _build_blocker_cards(evidence)

    loaded_extract_ids = {item["extract_id"] for item in pilot.get("public_aggregate_extracts", []) if item["data_status"] == "real_public_data_loaded"}
    card_extract_ids = {item.extract_id for item in loaded_cards}
    if loaded_extract_ids != card_extract_ids:
        raise ValueError("loaded value cards do not match existing Build 27 loaded extracts")
    source_only_extract_ids = {
        item["extract_id"] for item in pilot.get("public_aggregate_extracts", []) if item["data_status"] == "source_reference_only"
    }
    if any(card.extract_id in loaded_extract_ids for card in source_only_cards):
        raise ValueError("source-reference-only card counted as loaded data")
    if {card.extract_id for card in source_only_cards} != source_only_extract_ids:
        raise ValueError("source-reference-only cards do not match source-reference-only extracts")

    reviewer_checklists = [
        checklist
        for card in [*loaded_cards, *source_only_cards, *placeholder_cards]
        for checklist in card.reviewer_checklist
    ]
    for card in blocker_cards:
        reviewer_checklists.extend(_blocker_checklist(card.card_id))

    result_without_summary = {
        "loaded_value_cards": [item.to_jsonable() for item in loaded_cards],
        "source_reference_only_cards": [item.to_jsonable() for item in source_only_cards],
        "placeholder_anchor_cards": [item.to_jsonable() for item in placeholder_cards],
        "restricted_blocker_cards": [item.to_jsonable() for item in blocker_cards],
    }
    forbidden_claims = find_forbidden_affirmative_source_locator_claims(str(result_without_summary))

    summary = SourceLocatorVerificationSummary(
        total_loaded_value_cards=len(loaded_cards),
        complete_locator_cards=sum(card.locator_status == "complete_locator" for card in loaded_cards),
        partial_locator_cards=sum(card.locator_status == "partial_locator" for card in loaded_cards),
        source_reference_only_cards=len(source_only_cards),
        placeholder_anchor_cards=len(placeholder_cards),
        restricted_blocker_cards=len(blocker_cards),
        reviewer_checklist_items_total=len(reviewer_checklists),
        fair_work_arithmetic_cards=sum(
            "24.95 * 38 = 948.10" in card.arithmetic_check_summary for card in loaded_cards
        ),
        cards_ready_for_manual_review=sum(card.verification_status == "ready_for_manual_review" for card in loaded_cards),
        cards_source_locator_recorded_only=sum(card.verification_status == "source_locator_recorded_only" for card in loaded_cards),
        cards_source_reference_only_not_loaded=len(source_only_cards),
        cards_placeholder_not_real_data=len(placeholder_cards),
        cards_blocked_until_authorised_access=sum(
            card.verification_status == "blocked_until_authorised_access" for card in blocker_cards
        ),
        forbidden_claim_findings=len(forbidden_claims),
        source_locator_pack_created=True,
        new_data_loaded=False,
        external_source_verification_claimed=False,
        manual_review_pack_only=True,
        loaded_value_cards_created=bool(loaded_cards),
        source_reference_only_cards_created=bool(source_only_cards),
        placeholder_anchor_cards_created=bool(placeholder_cards),
        restricted_blocker_cards_created=bool(blocker_cards),
        reviewer_checklists_created=bool(reviewer_checklists),
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
        raise ValueError(f"forbidden affirmative source-locator claims found: {', '.join(forbidden_claims)}")
    if summary.fair_work_arithmetic_cards != 1:
        raise ValueError("Fair Work arithmetic summary is missing")
    for key in REQUIRED_FALSE_FLAGS:
        if getattr(summary, key):
            raise ValueError(f"summary false flag is true: {key}")

    return SourceLocatorVerificationResult(
        pack_id=manifest["pack_id"],
        pack_name=manifest["pack_name"],
        status=manifest["status"],
        non_claims=_list_of_strings(manifest["non_claims"], "manifest.non_claims"),
        input_artifacts=_list_of_strings(manifest["input_artifacts"], "manifest.input_artifacts"),
        loaded_value_cards=loaded_cards,
        source_reference_only_cards=source_only_cards,
        placeholder_anchor_cards=placeholder_cards,
        restricted_blocker_cards=blocker_cards,
        reviewer_checklists=reviewer_checklists,
        forbidden_claims=forbidden_claims,
        build_29_6_requirements=_list_of_strings(manifest["build_29_6_requirements"], "manifest.build_29_6_requirements"),
        build_30_requirements=_list_of_strings(manifest["build_30_requirements"], "manifest.build_30_requirements"),
        summary=summary,
    )
