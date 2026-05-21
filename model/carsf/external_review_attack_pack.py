"""External review attack-pack validation for the CARSF V1.5 prototype.

This module structures reviewer challenge questions, failure modes, report
attack matrices, and boundary checks. It does not record completed review,
approval, validation, readiness, official status, or any change to firm-level
CARSF liability.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

from carsf.release_candidate_pack import REQUIRED_LAYER_IDS, REQUIRED_REPORT_PATHS


EXTERNAL_REVIEW_ATTACK_PACK_WARNING = (
    "This is an attack pack for external review. It does not mean external review has been completed, "
    "does not mean approval has been granted, does not mean validation has occurred, is not legal advice, "
    "not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare validation, "
    "not statistical validation, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, "
    "not legislative readiness, not a readiness score, not official status, and not an official review pathway. "
    "It does not determine actual tax payable, does not use taxpayer-level, firm-level, industry, ABS, ATO, DSS, "
    "Treasury, PBO, HILDA, or Census data, and does not modify firm-level CARSF liability."
)

EXTERNAL_REVIEW_ATTACK_PACK_NON_CLAIMS = [
    EXTERNAL_REVIEW_ATTACK_PACK_WARNING,
    "The attack pack only structures questions, challenges, failure modes, boundary checks, and review routes for external reviewers.",
    "Challenge severity labels are not risk scores, not validation outcomes, not approval statuses, and not readiness ratings.",
]

REQUIRED_REVIEW_TRACKS = {
    "policy_review",
    "technical_review",
    "legal_review",
    "tax_review",
    "ato_methods_review",
    "treasury_methods_review",
    "privacy_review",
    "statistical_methods_review",
    "economic_methods_review",
    "welfare_policy_review",
    "parliamentary_counsel_review",
    "hostile_red_team_review",
}

REQUIRED_ATTACK_DOCUMENTS = {
    "release/v1_5_rc/attack_pack/ATTACK_PACK_OVERVIEW.md",
    "release/v1_5_rc/attack_pack/POLICY_REVIEW_ATTACKS.md",
    "release/v1_5_rc/attack_pack/TECHNICAL_REVIEW_ATTACKS.md",
    "release/v1_5_rc/attack_pack/LEGAL_REVIEW_ATTACKS.md",
    "release/v1_5_rc/attack_pack/TAX_REVIEW_ATTACKS.md",
    "release/v1_5_rc/attack_pack/ATO_METHODS_REVIEW_ATTACKS.md",
    "release/v1_5_rc/attack_pack/TREASURY_METHODS_REVIEW_ATTACKS.md",
    "release/v1_5_rc/attack_pack/PRIVACY_SECRECY_REVIEW_ATTACKS.md",
    "release/v1_5_rc/attack_pack/STATISTICAL_METHODS_REVIEW_ATTACKS.md",
    "release/v1_5_rc/attack_pack/ECONOMIC_METHODS_REVIEW_ATTACKS.md",
    "release/v1_5_rc/attack_pack/WELFARE_POLICY_REVIEW_ATTACKS.md",
    "release/v1_5_rc/attack_pack/PARLIAMENTARY_COUNSEL_REVIEW_ATTACKS.md",
    "release/v1_5_rc/attack_pack/HOSTILE_RED_TEAM_ATTACKS.md",
    "release/v1_5_rc/attack_pack/REPORT_ATTACK_MATRIX.md",
    "release/v1_5_rc/attack_pack/LAYER_ATTACK_MATRIX.md",
    "release/v1_5_rc/attack_pack/BOUNDARY_CHECKS.md",
    "release/v1_5_rc/attack_pack/ATTACK_PACK_MANIFEST.json",
}

ATTACK_SEVERITY_LABELS = {
    "review_note",
    "material_issue",
    "critical_blocker",
    "locked_until_external_review",
}

FORBIDDEN_AFFIRMATIVE_ATTACK_PACK_CLAIMS = [
    "review completed",
    "approved by reviewer",
    "validated by reviewer",
    "externally validated",
    "ready for government",
    "ready for ato",
    "operationally ready",
    "legally sufficient",
    "legislative-ready",
    "bill-ready",
    "parliament-ready",
    "treasury validated",
    "ato validated",
    "official review completed",
    "official review pathway",
    "official status",
    "official policy",
    "compliance score",
    "readiness score",
    "maturity score",
    "approved",
    "enforceable",
    "actual tax payable",
    "real policy result",
    "real household estimate",
    "population estimate",
    "official sector ranking",
    "economic validation is complete",
    "welfare validation is complete",
    "statistical validation is complete",
    "operational validation is complete",
    "legal review complete",
    "tax review complete",
]

NEGATIVE_CONTEXT_MARKERS = [
    "not ",
    "not a ",
    "not an ",
    "no ",
    "no real ",
    "does not ",
    "do not ",
    "does not show:",
    "must not ",
    "must not be used for:",
    "must_not",
    "_used_for",
    "not_",
    "without ",
    "is not ",
    "are not ",
    "created no ",
    "creates no ",
    "cannot ",
    "only ",
    "false",
    "non-claim",
    "boundary check",
    "prohibited",
    "forbidden",
    "imply ",
    "implies ",
    "mistaken for ",
    "be read as ",
    "could ",
    "question: ",
]


@dataclass(frozen=True)
class AttackQuestion:
    question_id: str
    question: str
    attack_category: str
    target_layers: list[str]
    target_reports: list[str]
    why_it_matters: str
    what_would_fail: str
    required_evidence_or_review: str
    severity_label: str
    must_not_be_treated_as_validation: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AttackFailureMode:
    failure_id: str
    failure_mode: str
    affected_layers: list[str]
    affected_reports: list[str]
    boundary_at_risk: str
    required_follow_up: str
    severity_label: str
    not_a_finding_of_actual_error: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExternalReviewTrack:
    track_id: str
    track_name: str
    reviewer_type: str
    purpose: str
    inspect_first: list[str]
    relevant_layers: list[str]
    relevant_reports: list[str]
    core_attack_questions: list[AttackQuestion]
    layer_attack_questions: list[str]
    report_attack_questions: list[str]
    required_external_inputs: list[str]
    failure_modes: list[AttackFailureMode]
    must_not_infer: list[str]
    locked_until_review_items: list[str]
    recommended_output_format: str
    non_claims: list[str]

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AttackBoundaryCheck:
    boundary_id: str
    boundary_question: str
    prohibited_affirmative_claims: list[str]
    allowed_negative_warnings: list[str]
    affected_layers: list[str]
    affected_reports: list[str]
    fail_closed_if_found: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AttackPackReport:
    report_path: str
    layer_id: str
    primary_reviewer_tracks: list[str]
    attack_question_ids: list[str]
    likely_overread_risk: str
    calibration_or_review_blockers: list[str]
    must_not_be_used_for: list[str]
    required_follow_up: str
    not_validation_statement: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AttackPackLayer:
    layer_id: str
    layer_name: str
    attack_tracks: list[str]
    attack_categories: list[str]
    known_blockers: list[str]
    missing_external_inputs: list[str]
    failure_mode_ids: list[str]
    must_not_infer: list[str]
    locked_until_review: list[str]
    not_validation_statement: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AttackPackDocument:
    document_path: str
    exists: bool
    contains_non_claims: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExternalReviewAttackPackSummary:
    total_review_tracks: int
    total_attack_questions: int
    total_failure_modes: int
    total_boundary_checks: int
    total_report_attack_rows: int
    total_layer_attack_rows: int
    total_release_documents: int
    release_documents_present: int
    release_documents_missing: int
    reports_referenced: int
    reports_missing: int
    layers_referenced: int
    unknown_layers: int
    tracks_with_required_question_count: int
    tracks_missing_required_question_count: int
    review_completed: bool
    approval_claimed: bool
    validation_claimed: bool
    readiness_score_created: bool
    legal_sufficiency_claimed: bool
    operational_readiness_claimed: bool
    legislative_readiness_claimed: bool
    official_status_claimed: bool
    real_data_used: bool
    firm_level_liability_logic_modified: bool
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(EXTERNAL_REVIEW_ATTACK_PACK_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class ExternalReviewAttackPackResult:
    attack_pack_id: str
    attack_pack_name: str
    status: str
    review_tracks: list[ExternalReviewTrack]
    prototype_layers: list[str]
    generated_reports: list[str]
    attack_categories: list[str]
    cross_cutting_attack_questions: list[AttackQuestion]
    boundary_checks: list[AttackBoundaryCheck]
    report_attack_matrix: list[AttackPackReport]
    layer_attack_matrix: list[AttackPackLayer]
    release_documents: list[AttackPackDocument]
    locked_until_review_items: list[str]
    required_external_inputs: list[str]
    suggested_reviewer_output_format: str
    summary: ExternalReviewAttackPackSummary
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(EXTERNAL_REVIEW_ATTACK_PACK_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _required_mapping(source: dict[str, Any], required: list[str], label: str) -> None:
    missing = [key for key in required if key not in source]
    if missing:
        raise ValueError(f"{label} missing required fields: {', '.join(missing)}")


def _list_of_strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ValueError(f"{label} must be a list of strings")
    return list(value)


def _bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be boolean")
    return value


def _load_release_manifest(repo_root: Path) -> dict[str, Any]:
    path = repo_root / "data" / "release" / "v1_5_release_manifest.yaml"
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError("release manifest must be a mapping")
    return loaded


def _release_layer_maps(repo_root: Path) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    release = _load_release_manifest(repo_root)
    layers = {str(layer["layer_id"]): layer for layer in release.get("prototype_layers", [])}
    reports = {str(report["report_path"]): report for report in release.get("generated_reports", [])}
    return layers, reports


def _has_attack_pack_non_claim_language(text: str) -> bool:
    lowered = text.lower()
    return all(
        phrase in lowered
        for phrase in [
            "does not mean external review has been completed",
            "does not mean approval has been granted",
            "does not mean validation has occurred",
            "not legal advice",
            "not tax advice",
            "not ato guidance",
            "does not modify firm-level carsf liability",
        ]
    )


def find_forbidden_affirmative_attack_pack_claims(text: str) -> list[str]:
    lowered = text.lower()
    findings: list[str] = []
    for phrase in FORBIDDEN_AFFIRMATIVE_ATTACK_PACK_CLAIMS:
        start = 0
        while True:
            index = lowered.find(phrase, start)
            if index == -1:
                break
            context = lowered[max(0, index - 220) : index]
            if not any(marker in context for marker in NEGATIVE_CONTEXT_MARKERS):
                findings.append(phrase)
                break
            start = index + len(phrase)
    return sorted(set(findings))


def _question_from_mapping(source: dict[str, Any], label: str, layer_ids: set[str], report_paths: set[str]) -> AttackQuestion:
    _required_mapping(
        source,
        [
            "question_id",
            "question",
            "attack_category",
            "target_layers",
            "target_reports",
            "why_it_matters",
            "what_would_fail",
            "required_evidence_or_review",
            "severity_label",
            "must_not_be_treated_as_validation",
        ],
        label,
    )
    question_id = str(source["question_id"])
    target_layers = _list_of_strings(source["target_layers"], f"{question_id}.target_layers")
    target_reports = _list_of_strings(source["target_reports"], f"{question_id}.target_reports")
    unknown_layers = sorted(set(target_layers) - layer_ids)
    unknown_reports = sorted(set(target_reports) - report_paths)
    if unknown_layers:
        raise ValueError(f"attack question {question_id} references unknown layers: {', '.join(unknown_layers)}")
    if unknown_reports:
        raise ValueError(f"attack question {question_id} references unknown reports: {', '.join(unknown_reports)}")
    severity_label = str(source["severity_label"])
    if severity_label not in ATTACK_SEVERITY_LABELS:
        raise ValueError(f"attack question {question_id} has unknown severity label: {severity_label}")
    if _bool(source["must_not_be_treated_as_validation"], f"{question_id}.must_not_be_treated_as_validation") is not True:
        raise ValueError(f"attack question {question_id} can be treated as validation")
    return AttackQuestion(
        question_id=question_id,
        question=str(source["question"]),
        attack_category=str(source["attack_category"]),
        target_layers=target_layers,
        target_reports=target_reports,
        why_it_matters=str(source["why_it_matters"]),
        what_would_fail=str(source["what_would_fail"]),
        required_evidence_or_review=str(source["required_evidence_or_review"]),
        severity_label=severity_label,
        must_not_be_treated_as_validation=True,
    )


def _failure_from_mapping(source: dict[str, Any], label: str, layer_ids: set[str], report_paths: set[str]) -> AttackFailureMode:
    _required_mapping(
        source,
        [
            "failure_id",
            "failure_mode",
            "affected_layers",
            "affected_reports",
            "boundary_at_risk",
            "required_follow_up",
            "severity_label",
            "not_a_finding_of_actual_error",
        ],
        label,
    )
    failure_id = str(source["failure_id"])
    affected_layers = _list_of_strings(source["affected_layers"], f"{failure_id}.affected_layers")
    affected_reports = _list_of_strings(source["affected_reports"], f"{failure_id}.affected_reports")
    unknown_layers = sorted(set(affected_layers) - layer_ids)
    unknown_reports = sorted(set(affected_reports) - report_paths)
    if unknown_layers:
        raise ValueError(f"failure mode {failure_id} references unknown layers: {', '.join(unknown_layers)}")
    if unknown_reports:
        raise ValueError(f"failure mode {failure_id} references unknown reports: {', '.join(unknown_reports)}")
    severity_label = str(source["severity_label"])
    if severity_label not in ATTACK_SEVERITY_LABELS:
        raise ValueError(f"failure mode {failure_id} has unknown severity label: {severity_label}")
    if _bool(source["not_a_finding_of_actual_error"], f"{failure_id}.not_a_finding_of_actual_error") is not True:
        raise ValueError(f"failure mode {failure_id} appears as an actual finding")
    return AttackFailureMode(
        failure_id=failure_id,
        failure_mode=str(source["failure_mode"]),
        affected_layers=affected_layers,
        affected_reports=affected_reports,
        boundary_at_risk=str(source["boundary_at_risk"]),
        required_follow_up=str(source["required_follow_up"]),
        severity_label=severity_label,
        not_a_finding_of_actual_error=True,
    )


def _track_from_mapping(source: dict[str, Any], layer_ids: set[str], report_paths: set[str]) -> ExternalReviewTrack:
    _required_mapping(
        source,
        [
            "track_id",
            "track_name",
            "reviewer_type",
            "purpose",
            "inspect_first",
            "relevant_layers",
            "relevant_reports",
            "core_attack_questions",
            "layer_attack_questions",
            "report_attack_questions",
            "required_external_inputs",
            "failure_modes",
            "must_not_infer",
            "locked_until_review_items",
            "recommended_output_format",
            "non_claims",
        ],
        f"review track {source.get('track_id', '?')}",
    )
    track_id = str(source["track_id"])
    relevant_layers = _list_of_strings(source["relevant_layers"], f"{track_id}.relevant_layers")
    relevant_reports = _list_of_strings(source["relevant_reports"], f"{track_id}.relevant_reports")
    unknown_layers = sorted(set(relevant_layers) - layer_ids)
    unknown_reports = sorted(set(relevant_reports) - report_paths)
    if unknown_layers:
        raise ValueError(f"review track {track_id} references unknown layers: {', '.join(unknown_layers)}")
    if unknown_reports:
        raise ValueError(f"review track {track_id} references unknown reports: {', '.join(unknown_reports)}")
    questions = [
        _question_from_mapping(item, f"track {track_id} question", layer_ids, report_paths)
        for item in source["core_attack_questions"]
    ]
    failures = [
        _failure_from_mapping(item, f"track {track_id} failure", layer_ids, report_paths)
        for item in source["failure_modes"]
    ]
    if len(questions) < 10:
        raise ValueError(f"review track {track_id} has fewer than 10 attack questions")
    if len(failures) < 5:
        raise ValueError(f"review track {track_id} has fewer than 5 failure modes")
    required_inputs = _list_of_strings(source["required_external_inputs"], f"{track_id}.required_external_inputs")
    must_not_infer = _list_of_strings(source["must_not_infer"], f"{track_id}.must_not_infer")
    if len(required_inputs) < 5:
        raise ValueError(f"review track {track_id} has fewer than 5 required external inputs")
    if len(must_not_infer) < 5:
        raise ValueError(f"review track {track_id} has fewer than 5 must-not-infer warnings")
    non_claims = _list_of_strings(source["non_claims"], f"{track_id}.non_claims")
    if not any("does not mean external review has been completed" in item.lower() for item in non_claims):
        raise ValueError(f"review track {track_id} missing external-review non-claim")
    return ExternalReviewTrack(
        track_id=track_id,
        track_name=str(source["track_name"]),
        reviewer_type=str(source["reviewer_type"]),
        purpose=str(source["purpose"]),
        inspect_first=_list_of_strings(source["inspect_first"], f"{track_id}.inspect_first"),
        relevant_layers=relevant_layers,
        relevant_reports=relevant_reports,
        core_attack_questions=questions,
        layer_attack_questions=_list_of_strings(source["layer_attack_questions"], f"{track_id}.layer_attack_questions"),
        report_attack_questions=_list_of_strings(source["report_attack_questions"], f"{track_id}.report_attack_questions"),
        required_external_inputs=required_inputs,
        failure_modes=failures,
        must_not_infer=must_not_infer,
        locked_until_review_items=_list_of_strings(source["locked_until_review_items"], f"{track_id}.locked_until_review_items"),
        recommended_output_format=str(source["recommended_output_format"]),
        non_claims=non_claims,
    )


def _boundary_from_mapping(source: dict[str, Any], layer_ids: set[str], report_paths: set[str]) -> AttackBoundaryCheck:
    _required_mapping(
        source,
        [
            "boundary_id",
            "boundary_question",
            "prohibited_affirmative_claims",
            "allowed_negative_warnings",
            "affected_layers",
            "affected_reports",
            "fail_closed_if_found",
        ],
        "boundary check",
    )
    boundary_id = str(source["boundary_id"])
    affected_layers = _list_of_strings(source["affected_layers"], f"{boundary_id}.affected_layers")
    affected_reports = _list_of_strings(source["affected_reports"], f"{boundary_id}.affected_reports")
    unknown_layers = sorted(set(affected_layers) - layer_ids)
    unknown_reports = sorted(set(affected_reports) - report_paths)
    if unknown_layers:
        raise ValueError(f"boundary check {boundary_id} references unknown layers: {', '.join(unknown_layers)}")
    if unknown_reports:
        raise ValueError(f"boundary check {boundary_id} references unknown reports: {', '.join(unknown_reports)}")
    if _bool(source["fail_closed_if_found"], f"{boundary_id}.fail_closed_if_found") is not True:
        raise ValueError(f"boundary check {boundary_id} omits fail_closed_if_found")
    return AttackBoundaryCheck(
        boundary_id=boundary_id,
        boundary_question=str(source["boundary_question"]),
        prohibited_affirmative_claims=_list_of_strings(source["prohibited_affirmative_claims"], f"{boundary_id}.prohibited_affirmative_claims"),
        allowed_negative_warnings=_list_of_strings(source["allowed_negative_warnings"], f"{boundary_id}.allowed_negative_warnings"),
        affected_layers=affected_layers,
        affected_reports=affected_reports,
        fail_closed_if_found=True,
    )


def _document_from_path(relative_path: str, repo_root: Path) -> AttackPackDocument:
    path = repo_root / relative_path
    if not path.exists():
        raise ValueError(f"required attack-pack release document is missing: {relative_path}")
    text = path.read_text(encoding="utf-8")
    if not _has_attack_pack_non_claim_language(text):
        raise ValueError(f"attack-pack release document missing required non-claim language: {relative_path}")
    forbidden = find_forbidden_affirmative_attack_pack_claims(text)
    if forbidden:
        raise ValueError(f"attack-pack release document contains forbidden affirmative claims: {relative_path}: {', '.join(forbidden)}")
    return AttackPackDocument(document_path=relative_path, exists=True, contains_non_claims=True)


def _strip_claim_list_fields(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _strip_claim_list_fields(item)
            for key, item in value.items()
            if key not in {"forbidden_claims", "prohibited_affirmative_claims"}
        }
    if isinstance(value, list):
        return [_strip_claim_list_fields(item) for item in value]
    return value


def _tracks_for_layer(tracks: list[ExternalReviewTrack], layer_id: str) -> list[str]:
    matches = [track.track_id for track in tracks if layer_id in track.relevant_layers]
    return sorted(matches or ["hostile_red_team_review"])


def _tracks_for_report(tracks: list[ExternalReviewTrack], report_path: str, layer_id: str) -> list[str]:
    matches = [
        track.track_id
        for track in tracks
        if report_path in track.relevant_reports or layer_id in track.relevant_layers
    ]
    return sorted(matches or ["hostile_red_team_review"])


def _question_ids_for_report(tracks: list[ExternalReviewTrack], report_path: str, layer_id: str) -> list[str]:
    ids = [
        question.question_id
        for track in tracks
        for question in track.core_attack_questions
        if report_path in question.target_reports or layer_id in question.target_layers
    ]
    return sorted(set(ids))[:12]


def _release_layer_blockers(layer: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    for field in ["calibration_blockers", "external_review_blockers"]:
        value = layer.get(field, [])
        if isinstance(value, list):
            blockers.extend(str(item) for item in value)
    return blockers or ["External review required before any real-world interpretation."]


def _build_report_attack_matrix(
    reports: dict[str, dict[str, Any]],
    layers: dict[str, dict[str, Any]],
    tracks: list[ExternalReviewTrack],
    required_paths: list[str],
) -> list[AttackPackReport]:
    rows: list[AttackPackReport] = []
    for report_path in sorted(required_paths):
        source = reports[report_path]
        layer_id = str(source["layer_id"])
        layer = layers[layer_id]
        rows.append(
            AttackPackReport(
                report_path=report_path,
                layer_id=layer_id,
                primary_reviewer_tracks=_tracks_for_report(tracks, report_path, layer_id),
                attack_question_ids=_question_ids_for_report(tracks, report_path, layer_id),
                likely_overread_risk="does not show: "
                + str(source.get("what_it_does_not_show", "reviewed, validated, approved, or ready output")),
                calibration_or_review_blockers=_release_layer_blockers(layer),
                must_not_be_used_for=[str(item) for item in layer.get("must_not_be_used_for", [])],
                required_follow_up="External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload.",
                not_validation_statement="This report attack row is a challenge prompt only and is not validation, approval, readiness, or a finding of actual error.",
            )
        )
    return rows


def _build_layer_attack_matrix(
    layers: dict[str, dict[str, Any]],
    tracks: list[ExternalReviewTrack],
    required_layers: list[str],
) -> list[AttackPackLayer]:
    rows: list[AttackPackLayer] = []
    for layer_id in sorted(required_layers):
        layer = layers[layer_id]
        layer_tracks = _tracks_for_layer(tracks, layer_id)
        questions = [
            question
            for track in tracks
            for question in track.core_attack_questions
            if layer_id in question.target_layers
        ]
        failures = [
            failure
            for track in tracks
            for failure in track.failure_modes
            if layer_id in failure.affected_layers
        ]
        external_inputs = [
            item
            for track in tracks
            if track.track_id in layer_tracks
            for item in track.required_external_inputs
        ]
        must_not = [
            item
            for track in tracks
            if track.track_id in layer_tracks
            for item in track.must_not_infer
        ]
        locked = [
            item
            for track in tracks
            if track.track_id in layer_tracks
            for item in track.locked_until_review_items
        ]
        rows.append(
            AttackPackLayer(
                layer_id=layer_id,
                layer_name=str(layer.get("layer_name", layer_id)),
                attack_tracks=layer_tracks,
                attack_categories=sorted({question.attack_category for question in questions}) or ["overclaiming_risk"],
                known_blockers=_release_layer_blockers(layer),
                missing_external_inputs=sorted(set(external_inputs))[:12],
                failure_mode_ids=sorted({failure.failure_id for failure in failures})[:12],
                must_not_infer=sorted(set(must_not))[:12],
                locked_until_review=sorted(set(locked))[:12],
                not_validation_statement="This layer attack row is a challenge prompt only and is not validation, approval, readiness, or an official review outcome.",
            )
        )
    return rows


def build_external_review_attack_pack_result(payload: dict[str, Any], repo_root: Path) -> ExternalReviewAttackPackResult:
    _required_mapping(
        payload,
        [
            "attack_pack_id",
            "attack_pack_name",
            "status",
            "non_claims",
            "review_tracks",
            "prototype_layers",
            "generated_reports",
            "attack_categories",
            "cross_cutting_attack_questions",
            "boundary_checks",
            "release_documents",
            "forbidden_claims",
        ],
        "attack pack manifest",
    )
    if payload["status"] != "prototype_external_review_attack_pack_only":
        raise ValueError("status must be prototype_external_review_attack_pack_only")
    for non_claim in EXTERNAL_REVIEW_ATTACK_PACK_NON_CLAIMS:
        if non_claim not in payload["non_claims"]:
            raise ValueError("attack pack manifest missing required non-claim language")

    release_layers, release_reports = _release_layer_maps(repo_root)
    release_layer_ids = set(release_layers)
    release_report_paths = set(release_reports)
    layer_ids = set(_list_of_strings(payload["prototype_layers"], "prototype_layers"))
    report_paths = set(_list_of_strings(payload["generated_reports"], "generated_reports"))
    missing_layers = sorted(REQUIRED_LAYER_IDS - layer_ids)
    missing_reports = sorted(REQUIRED_REPORT_PATHS - report_paths)
    unknown_layers = sorted(layer_ids - release_layer_ids)
    unknown_reports = sorted(report_paths - release_report_paths)
    if missing_layers:
        raise ValueError(f"attack pack manifest missing required layers: {', '.join(missing_layers)}")
    if missing_reports:
        raise ValueError(f"attack pack manifest missing required generated reports: {', '.join(missing_reports)}")
    if unknown_layers:
        raise ValueError(f"attack pack manifest references unknown layers: {', '.join(unknown_layers)}")
    if unknown_reports:
        raise ValueError(f"attack pack manifest references unknown reports: {', '.join(unknown_reports)}")
    for report_path in report_paths:
        if not (repo_root / report_path).exists():
            raise ValueError(f"referenced report path is missing: {report_path}")

    tracks = [_track_from_mapping(item, layer_ids, report_paths) for item in payload["review_tracks"]]
    track_ids = {track.track_id for track in tracks}
    missing_tracks = sorted(REQUIRED_REVIEW_TRACKS - track_ids)
    if missing_tracks:
        raise ValueError(f"attack pack manifest missing required review tracks: {', '.join(missing_tracks)}")

    cross_cutting_questions = [
        _question_from_mapping(item, "cross-cutting attack question", layer_ids, report_paths)
        for item in payload["cross_cutting_attack_questions"]
    ]
    boundary_checks = [_boundary_from_mapping(item, layer_ids, report_paths) for item in payload["boundary_checks"]]
    if len(boundary_checks) < 18:
        raise ValueError("attack pack manifest must include at least 18 boundary checks")

    document_paths = set(_list_of_strings(payload["release_documents"], "release_documents"))
    missing_documents = sorted(REQUIRED_ATTACK_DOCUMENTS - document_paths)
    if missing_documents:
        raise ValueError(f"attack pack document index missing required documents: {', '.join(missing_documents)}")
    documents = [_document_from_path(path, repo_root) for path in sorted(document_paths)]

    payload_for_claim_scan = _strip_claim_list_fields(payload)
    forbidden = find_forbidden_affirmative_attack_pack_claims(str(payload_for_claim_scan))
    if forbidden:
        raise ValueError(f"attack pack manifest contains forbidden affirmative claims: {', '.join(forbidden)}")

    report_attack_matrix = _build_report_attack_matrix(release_reports, release_layers, tracks, sorted(report_paths))
    layer_attack_matrix = _build_layer_attack_matrix(release_layers, tracks, sorted(layer_ids))
    all_questions = [question for track in tracks for question in track.core_attack_questions] + cross_cutting_questions
    all_failures = [failure for track in tracks for failure in track.failure_modes]
    locked_items = sorted({item for track in tracks for item in track.locked_until_review_items})
    required_inputs = sorted({item for track in tracks for item in track.required_external_inputs})
    tracks_with_question_count = sum(1 for track in tracks if len(track.core_attack_questions) >= 10)

    summary = ExternalReviewAttackPackSummary(
        total_review_tracks=len(tracks),
        total_attack_questions=len(all_questions),
        total_failure_modes=len(all_failures),
        total_boundary_checks=len(boundary_checks),
        total_report_attack_rows=len(report_attack_matrix),
        total_layer_attack_rows=len(layer_attack_matrix),
        total_release_documents=len(documents),
        release_documents_present=sum(document.exists for document in documents),
        release_documents_missing=sum(not document.exists for document in documents),
        reports_referenced=len(report_paths),
        reports_missing=0,
        layers_referenced=len(layer_ids),
        unknown_layers=0,
        tracks_with_required_question_count=tracks_with_question_count,
        tracks_missing_required_question_count=len(tracks) - tracks_with_question_count,
        review_completed=False,
        approval_claimed=False,
        validation_claimed=False,
        readiness_score_created=False,
        legal_sufficiency_claimed=False,
        operational_readiness_claimed=False,
        legislative_readiness_claimed=False,
        official_status_claimed=False,
        real_data_used=False,
        firm_level_liability_logic_modified=False,
        warnings=[
            "Attack-pack severity labels are challenge severities only.",
            "No reviewer approval, validation, readiness, official status, legal sufficiency, or liability change is created.",
        ],
    )

    return ExternalReviewAttackPackResult(
        attack_pack_id=str(payload["attack_pack_id"]),
        attack_pack_name=str(payload["attack_pack_name"]),
        status=str(payload["status"]),
        review_tracks=sorted(tracks, key=lambda item: item.track_id),
        prototype_layers=sorted(layer_ids),
        generated_reports=sorted(report_paths),
        attack_categories=_list_of_strings(payload["attack_categories"], "attack_categories"),
        cross_cutting_attack_questions=sorted(cross_cutting_questions, key=lambda item: item.question_id),
        boundary_checks=sorted(boundary_checks, key=lambda item: item.boundary_id),
        report_attack_matrix=report_attack_matrix,
        layer_attack_matrix=layer_attack_matrix,
        release_documents=documents,
        locked_until_review_items=locked_items,
        required_external_inputs=required_inputs,
        suggested_reviewer_output_format=str(payload.get("suggested_reviewer_output_format", "Reviewer findings should separate blocker, evidence request, overclaim risk, and non-claim boundary notes.")),
        summary=summary,
        warnings=list(summary.warnings),
    )
