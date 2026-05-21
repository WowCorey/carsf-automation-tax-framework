"""Final RC integrity seal checks for the CARSF V1.5 prototype.

This module verifies internal artefact presence, manifest alignment, report
availability, boundary language, digest metadata, guardrail expectations, and
false readiness/legal/validation flags. It does not approve, validate, complete
external review, create readiness scoring, or modify firm-level CARSF liability.
"""

from __future__ import annotations

import glob
import hashlib
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


FINAL_RC_INTEGRITY_SEAL_WARNING = (
    "This is an internal integrity seal only. It is not approval, not validation, not external review completion, "
    "not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, "
    "not welfare validation, not statistical validation, not compliance scoring, not enforcement, not operational readiness, "
    "not legal sufficiency, not legislative readiness, not a readiness score, not a maturity score, not official status, "
    "and not an official review pathway. It does not determine actual tax payable, does not use taxpayer-level data, "
    "firm-level confidential data, household microdata, restricted government data, confidential Treasury/PBO material, "
    "or unauthorised data, and does not modify firm-level CARSF liability."
)

FINAL_RC_INTEGRITY_SEAL_NON_CLAIMS = [
    FINAL_RC_INTEGRITY_SEAL_WARNING,
    "The seal only verifies internal artefact presence, manifest alignment, report availability, non-claim boundaries, guardrail status expectations, digest metadata, and false readiness/legal/validation flags.",
    "Seal status is an internal integrity status only and is not approval, validation, legal sufficiency, operational readiness, legislative readiness, official status, or external review completion.",
]

FORBIDDEN_AFFIRMATIVE_SEAL_CLAIMS = [
    "review completed",
    "approved by reviewer",
    "validated by reviewer",
    "externally validated",
    "ready for government",
    "ready for ato",
    "ready for treasury",
    "ready for parliament",
    "ready for implementation",
    "ready for public release",
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
    "final approval",
    "final validation",
]

NEGATIVE_CONTEXT_MARKERS = [
    "not ",
    "not a ",
    "not an ",
    "no ",
    "no real ",
    "does not ",
    "does not show:",
    "do not ",
    "must not ",
    "must not be used for:",
    "must_not",
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
    "boundary",
    "forbidden",
    "prohibited",
    "imply ",
    "implies ",
    "claiming ",
    "claimed",
    "could ",
    "mistaken for ",
    "what this seal does not mean",
]

FALSE_FLAG_SOURCE_PATHS = [
    "reports/v1_5_release_candidate_pack.json",
    "reports/external_review_attack_pack.json",
    "reports/executive_dashboard.json",
    "reports/legislative_architecture.json",
    "reports/administrative_compliance_workflow.json",
    "release/v1_5_rc/RELEASE_MANIFEST.json",
    "release/v1_5_rc/attack_pack/ATTACK_PACK_MANIFEST.json",
]

SELF_GENERATED_DIGEST_EXCLUSIONS = {
    "release/v1_5_rc/FINAL_RC_DIGESTS.json",
    "release/v1_5_rc/FINAL_RC_INTEGRITY_SEAL.json",
    "release/v1_5_rc/FINAL_RC_INTEGRITY_SEAL.md",
    "reports/v1_5_final_rc_integrity_seal.json",
    "reports/v1_5_final_rc_integrity_seal.md",
}


@dataclass(frozen=True)
class IntegritySealArtefact:
    artefact_path: str
    artefact_group: str
    exists: bool
    status: str
    main_reason: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IntegritySealManifestCheck:
    manifest_path: str
    exists: bool
    aligned: bool
    checked_items: int
    missing_items: list[str]
    main_reason: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IntegritySealReportCheck:
    report_path: str
    exists: bool
    forbidden_claim_findings: list[str]
    status: str
    main_reason: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IntegritySealDocumentCheck:
    document_path: str
    document_group: str
    exists: bool
    contains_boundary_phrases: bool
    missing_boundary_phrases: list[str]
    forbidden_claim_findings: list[str]
    status: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IntegritySealFalseFlagCheck:
    flag_name: str
    expected_value: bool
    actual_value: bool | None
    source_path: str
    passed: bool
    main_reason: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IntegritySealBoundaryCheck:
    boundary_phrase: str
    checked_locations: list[str]
    missing_locations: list[str]
    passed: bool

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IntegritySealDigest:
    artefact_path: str
    exists: bool
    sha256: str | None
    byte_count: int | None
    status: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IntegritySealGuardrailStatus:
    source_report: str
    exists: bool
    readable: bool
    clean: bool | None
    denied_findings: int | None
    warning_findings: int | None
    status: str
    main_reason: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IntegritySealSummary:
    total_release_documents_required: int
    release_documents_present: int
    release_documents_missing: int
    total_attack_pack_documents_required: int
    attack_pack_documents_present: int
    attack_pack_documents_missing: int
    total_generated_reports_required: int
    generated_reports_present: int
    generated_reports_missing: int
    total_required_manifests: int
    manifests_present: int
    manifests_missing: int
    total_required_scripts: int
    scripts_present: int
    scripts_missing: int
    digest_targets_total: int
    digests_written: int
    forbidden_claim_findings: int
    boundary_phrase_failures: int
    false_flag_failures: int
    guardrail_denied_findings: int | None
    seal_passed: bool
    review_completed: bool
    approval_claimed: bool
    validation_claimed: bool
    readiness_score_created: bool
    maturity_score_created: bool
    operational_readiness_claimed: bool
    legal_sufficiency_claimed: bool
    legislative_readiness_claimed: bool
    economic_validation_claimed: bool
    welfare_validation_claimed: bool
    statistical_validation_claimed: bool
    official_status_claimed: bool
    official_review_pathway_claimed: bool
    real_data_used: bool
    actual_tax_payable_determined: bool
    compliance_scoring_created: bool
    enforcement_created: bool
    notices_created: bool
    penalties_created: bool
    operative_law_created: bool
    firm_level_liability_logic_modified: bool
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(FINAL_RC_INTEGRITY_SEAL_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class IntegritySealResult:
    seal_id: str
    seal_name: str
    seal_status: str
    artefact_inventory: list[IntegritySealArtefact]
    release_document_checks: list[IntegritySealDocumentCheck]
    attack_pack_document_checks: list[IntegritySealDocumentCheck]
    generated_report_checks: list[IntegritySealReportCheck]
    manifest_alignment_checks: list[IntegritySealManifestCheck]
    false_flag_checks: list[IntegritySealFalseFlagCheck]
    boundary_phrase_checks: list[IntegritySealBoundaryCheck]
    digest_manifest: list[IntegritySealDigest]
    guardrail_status: IntegritySealGuardrailStatus
    ci_expectations: dict[str, Any]
    known_blockers_preserved: list[str]
    missing_artefacts_or_seal_gaps: list[str]
    summary: IntegritySealSummary
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(FINAL_RC_INTEGRITY_SEAL_NON_CLAIMS))

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


def _mapping_of_false_flags(value: Any, label: str) -> dict[str, bool]:
    if not isinstance(value, dict) or not all(isinstance(key, str) and isinstance(item, bool) for key, item in value.items()):
        raise ValueError(f"{label} must be a mapping of string keys to boolean values")
    return dict(value)


def _normalise_text(value: str) -> str:
    return value.lower().replace("_", " ")


def find_forbidden_affirmative_seal_claims(text: str) -> list[str]:
    lowered = _normalise_text(text)
    findings: list[str] = []
    for phrase in FORBIDDEN_AFFIRMATIVE_SEAL_CLAIMS:
        needle = phrase.lower()
        start = 0
        while True:
            index = lowered.find(needle, start)
            if index == -1:
                break
            context = lowered[max(0, index - 260) : index]
            following = lowered[index : index + len(needle) + 60]
            if (
                ": false" in following
                or " false" in following
                or "boundary" in following[:80]
                or "approved state" in following[:80]
            ):
                start = index + len(needle)
                continue
            if not any(marker in context for marker in NEGATIVE_CONTEXT_MARKERS):
                findings.append(needle)
                break
            start = index + len(needle)
    return sorted(set(findings))


def _strip_claim_list_fields(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _strip_claim_list_fields(item)
            for key, item in value.items()
            if key
            not in {
                "forbidden_claims",
                "forbidden_affirmative_claims",
                "prohibited_affirmative_claims",
                "allowed_negative_warnings",
                "required_false_flags",
            }
        }
    if isinstance(value, list):
        return [_strip_claim_list_fields(item) for item in value]
    return value


def _read_text_if_exists(repo_root: Path, relative_path: str) -> str:
    path = repo_root / relative_path
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def _artefact_check(repo_root: Path, relative_path: str, group: str) -> IntegritySealArtefact:
    exists = (repo_root / relative_path).exists()
    return IntegritySealArtefact(
        artefact_path=relative_path,
        artefact_group=group,
        exists=exists,
        status="present" if exists else "missing",
        main_reason="Required final RC integrity artefact is present." if exists else "Required final RC integrity artefact is missing.",
    )


def _document_check(
    repo_root: Path,
    relative_path: str,
    group: str,
    boundary_phrases: list[str],
) -> IntegritySealDocumentCheck:
    exists = (repo_root / relative_path).exists()
    if not exists:
        return IntegritySealDocumentCheck(
            document_path=relative_path,
            document_group=group,
            exists=False,
            contains_boundary_phrases=False,
            missing_boundary_phrases=boundary_phrases,
            forbidden_claim_findings=[],
            status="missing",
        )
    text = _read_text_if_exists(repo_root, relative_path)
    lowered = text.lower()
    missing_phrases = [phrase for phrase in boundary_phrases if phrase.lower() not in lowered]
    forbidden = find_forbidden_affirmative_seal_claims(text)
    status = "clean" if not missing_phrases and not forbidden else "fail_closed"
    return IntegritySealDocumentCheck(
        document_path=relative_path,
        document_group=group,
        exists=True,
        contains_boundary_phrases=not missing_phrases,
        missing_boundary_phrases=missing_phrases,
        forbidden_claim_findings=forbidden,
        status=status,
    )


def _report_check(repo_root: Path, relative_path: str) -> IntegritySealReportCheck:
    exists = (repo_root / relative_path).exists()
    if not exists:
        return IntegritySealReportCheck(
            report_path=relative_path,
            exists=False,
            forbidden_claim_findings=[],
            status="missing",
            main_reason="Required generated report is missing.",
        )
    text = _read_text_if_exists(repo_root, relative_path)
    if relative_path.endswith(".json"):
        try:
            parsed = json.loads(text)
            text = json.dumps(_strip_claim_list_fields(parsed), sort_keys=True)
        except json.JSONDecodeError:
            pass
    forbidden = find_forbidden_affirmative_seal_claims(text)
    return IntegritySealReportCheck(
        report_path=relative_path,
        exists=True,
        forbidden_claim_findings=forbidden,
        status="clean" if not forbidden else "fail_closed",
        main_reason="Generated report exists and has no forbidden affirmative seal claims." if not forbidden else "Generated report contains forbidden affirmative seal claims.",
    )


def _load_json(repo_root: Path, relative_path: str) -> Any:
    path = repo_root / relative_path
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def _find_key_values(value: Any, key: str) -> list[Any]:
    matches: list[Any] = []
    if isinstance(value, dict):
        for current_key, current_value in value.items():
            if current_key == key:
                matches.append(current_value)
            matches.extend(_find_key_values(current_value, key))
    elif isinstance(value, list):
        for item in value:
            matches.extend(_find_key_values(item, key))
    return matches


def _false_flag_checks(repo_root: Path, false_flags: dict[str, bool]) -> list[IntegritySealFalseFlagCheck]:
    checks: list[IntegritySealFalseFlagCheck] = [
        IntegritySealFalseFlagCheck(
            flag_name=flag_name,
            expected_value=expected,
            actual_value=False,
            source_path="final_rc_integrity_seal_summary",
            passed=(expected is False),
            main_reason="Final seal summary sets this required false flag to false.",
        )
        for flag_name, expected in false_flags.items()
    ]
    for source_path in FALSE_FLAG_SOURCE_PATHS:
        payload = _load_json(repo_root, source_path)
        if payload is None:
            continue
        for flag_name, expected in false_flags.items():
            values = _find_key_values(payload, flag_name)
            for actual in values:
                passed = actual is expected
                checks.append(
                    IntegritySealFalseFlagCheck(
                        flag_name=flag_name,
                        expected_value=expected,
                        actual_value=actual if isinstance(actual, bool) else None,
                        source_path=source_path,
                        passed=passed,
                        main_reason="Referenced JSON source preserves the false flag." if passed else "Referenced JSON source has a true or non-boolean value for a required false flag.",
                    )
                )
    return checks


def _boundary_checks(document_checks: list[IntegritySealDocumentCheck], boundary_phrases: list[str]) -> list[IntegritySealBoundaryCheck]:
    checks: list[IntegritySealBoundaryCheck] = []
    locations = [check.document_path for check in document_checks]
    for phrase in boundary_phrases:
        missing = [check.document_path for check in document_checks if phrase in check.missing_boundary_phrases]
        checks.append(
            IntegritySealBoundaryCheck(
                boundary_phrase=phrase,
                checked_locations=locations,
                missing_locations=missing,
                passed=not missing,
            )
        )
    return checks


def _manifest_alignment_checks(repo_root: Path, payload: dict[str, Any]) -> list[IntegritySealManifestCheck]:
    checks: list[IntegritySealManifestCheck] = []
    required_reports = set(_list_of_strings(payload["required_generated_reports"], "required_generated_reports"))
    required_release_docs = set(_list_of_strings(payload["required_release_documents"], "required_release_documents"))
    required_attack_docs = set(_list_of_strings(payload["required_attack_pack_documents"], "required_attack_pack_documents"))

    release_yaml = repo_root / "data" / "release" / "v1_5_release_manifest.yaml"
    release_json = _load_json(repo_root, "release/v1_5_rc/RELEASE_MANIFEST.json")
    attack_json = _load_json(repo_root, "release/v1_5_rc/attack_pack/ATTACK_PACK_MANIFEST.json")

    checks.append(
        IntegritySealManifestCheck(
            manifest_path="data/release/v1_5_release_manifest.yaml",
            exists=release_yaml.exists(),
            aligned=release_yaml.exists(),
            checked_items=0,
            missing_items=[] if release_yaml.exists() else ["data/release/v1_5_release_manifest.yaml"],
            main_reason="YAML release manifest is present for release-pack validation." if release_yaml.exists() else "YAML release manifest is missing.",
        )
    )
    if isinstance(release_json, dict):
        indexed_docs = {
            "release/v1_5_rc/" + str(item)
            for item in release_json.get("release_documents", [])
            if isinstance(item, str)
        }
        indexed_reports = {str(item) for item in release_json.get("generated_reports", []) if isinstance(item, str)}
        expected_docs = {
            "release/v1_5_rc/FINAL_RC_INTEGRITY_SEAL.md",
            "release/v1_5_rc/FINAL_RC_INTEGRITY_SEAL.json",
            "release/v1_5_rc/FINAL_RC_DIGESTS.json",
        }
        expected_reports = {
            "reports/v1_5_final_rc_integrity_seal.md",
            "reports/v1_5_final_rc_integrity_seal.json",
        }
        missing = sorted((expected_docs - indexed_docs) | (expected_reports - indexed_reports))
        checks.append(
            IntegritySealManifestCheck(
                manifest_path="release/v1_5_rc/RELEASE_MANIFEST.json",
                exists=True,
                aligned=not missing,
                checked_items=len(expected_docs) + len(expected_reports),
                missing_items=missing,
                main_reason="Release manifest snapshot indexes final seal documents and reports." if not missing else "Release manifest snapshot omits final seal documents or reports.",
            )
        )
    else:
        checks.append(
            IntegritySealManifestCheck(
                manifest_path="release/v1_5_rc/RELEASE_MANIFEST.json",
                exists=False,
                aligned=False,
                checked_items=0,
                missing_items=["release/v1_5_rc/RELEASE_MANIFEST.json"],
                main_reason="Release manifest snapshot is missing or unreadable.",
            )
        )

    if isinstance(attack_json, dict):
        attack_docs = {
            "release/v1_5_rc/attack_pack/" + str(item)
            for item in attack_json.get("release_documents", [])
            if isinstance(item, str)
        }
        missing_attack_docs = sorted(required_attack_docs - attack_docs)
        checks.append(
            IntegritySealManifestCheck(
                manifest_path="release/v1_5_rc/attack_pack/ATTACK_PACK_MANIFEST.json",
                exists=True,
                aligned=not missing_attack_docs,
                checked_items=len(required_attack_docs),
                missing_items=missing_attack_docs,
                main_reason="Attack-pack manifest snapshot indexes required attack-pack documents." if not missing_attack_docs else "Attack-pack manifest snapshot omits required attack-pack documents.",
            )
        )
    else:
        checks.append(
            IntegritySealManifestCheck(
                manifest_path="release/v1_5_rc/attack_pack/ATTACK_PACK_MANIFEST.json",
                exists=False,
                aligned=False,
                checked_items=0,
                missing_items=["release/v1_5_rc/attack_pack/ATTACK_PACK_MANIFEST.json"],
                main_reason="Attack-pack manifest snapshot is missing or unreadable.",
            )
        )

    dashboard_manifest = repo_root / "data" / "dashboard" / "executive_dashboard_manifest.yaml"
    checks.append(
        IntegritySealManifestCheck(
            manifest_path="data/dashboard/executive_dashboard_manifest.yaml",
            exists=dashboard_manifest.exists(),
            aligned=dashboard_manifest.exists(),
            checked_items=0,
            missing_items=[] if dashboard_manifest.exists() else ["data/dashboard/executive_dashboard_manifest.yaml"],
            main_reason="Executive dashboard manifest is present for navigation alignment." if dashboard_manifest.exists() else "Executive dashboard manifest is missing.",
        )
    )

    all_required_docs = required_release_docs | required_attack_docs
    all_required = all_required_docs | required_reports
    missing_paths = sorted(path for path in all_required if not (repo_root / path).exists())
    checks.append(
        IntegritySealManifestCheck(
            manifest_path="data/seal/v1_5_final_rc_integrity_seal.yaml",
            exists=True,
            aligned=not missing_paths,
            checked_items=len(all_required),
            missing_items=missing_paths,
            main_reason="Seal manifest required artefacts exist on disk." if not missing_paths else "Seal manifest references missing required artefacts.",
        )
    )
    return checks


def _guardrail_status(repo_root: Path, expectations: dict[str, Any]) -> IntegritySealGuardrailStatus:
    source_report = str(expectations.get("source_report", "reports/repo_guardrails.json"))
    path = repo_root / source_report
    if not path.exists():
        return IntegritySealGuardrailStatus(
            source_report=source_report,
            exists=False,
            readable=False,
            clean=None,
            denied_findings=None,
            warning_findings=None,
            status="missing",
            main_reason="Repo guardrail report is missing.",
        )
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return IntegritySealGuardrailStatus(
            source_report=source_report,
            exists=True,
            readable=False,
            clean=None,
            denied_findings=None,
            warning_findings=None,
            status="fail_closed",
            main_reason="Repo guardrail report is not readable JSON.",
        )
    result = payload.get("result", {}) if isinstance(payload, dict) else {}
    denied = result.get("denied_findings", []) if isinstance(result, dict) else []
    findings = result.get("findings", []) if isinstance(result, dict) else []
    denied_count = len(denied) if isinstance(denied, list) else None
    warning_count = len(findings) if isinstance(findings, list) else None
    clean = result.get("clean") if isinstance(result.get("clean"), bool) else None
    expected_denied = expectations.get("denied_findings", 0)
    clean_expected = expectations.get("clean_expected", True)
    passed = denied_count == expected_denied and (clean is clean_expected or clean is None)
    return IntegritySealGuardrailStatus(
        source_report=source_report,
        exists=True,
        readable=True,
        clean=clean,
        denied_findings=denied_count,
        warning_findings=warning_count,
        status="clean" if passed else "fail_closed",
        main_reason="Repo guardrail report has the expected denied finding count." if passed else "Repo guardrail report did not meet the seal guardrail expectation.",
    )


def _expand_digest_targets(repo_root: Path, patterns: list[str]) -> list[str]:
    paths: set[str] = set()
    for pattern in patterns:
        matches = glob.glob(str(repo_root / pattern))
        if matches:
            for match in matches:
                path = Path(match)
                relative = path.relative_to(repo_root).as_posix()
                if path.is_file() and relative not in SELF_GENERATED_DIGEST_EXCLUSIONS:
                    paths.add(relative)
        elif (repo_root / pattern).is_file() and pattern not in SELF_GENERATED_DIGEST_EXCLUSIONS:
            paths.add(pattern)
    return sorted(paths)


def build_digest_manifest(repo_root: Path, digest_targets: list[str]) -> list[IntegritySealDigest]:
    expanded = _expand_digest_targets(repo_root, digest_targets)
    digests: list[IntegritySealDigest] = []
    for relative_path in expanded:
        path = repo_root / relative_path
        if not path.exists():
            digests.append(
                IntegritySealDigest(
                    artefact_path=relative_path,
                    exists=False,
                    sha256=None,
                    byte_count=None,
                    status="missing",
                )
            )
            continue
        data = path.read_bytes()
        digests.append(
            IntegritySealDigest(
                artefact_path=relative_path,
                exists=True,
                sha256=hashlib.sha256(data).hexdigest(),
                byte_count=len(data),
                status="present",
            )
        )
    return digests


def _ci_expectations(repo_root: Path, ci_payload: dict[str, Any]) -> dict[str, Any]:
    workflow_path = str(ci_payload.get("workflow_path", ".github/workflows/ci.yml"))
    required_commands = _list_of_strings(ci_payload.get("required_commands", []), "ci_expectations.required_commands")
    text = _read_text_if_exists(repo_root, workflow_path)
    missing = [command for command in required_commands if command not in text]
    return {
        "workflow_path": workflow_path,
        "exists": bool(text),
        "required_commands": required_commands,
        "commands_present": len(required_commands) - len(missing),
        "commands_missing": missing,
        "aligned": bool(text) and not missing,
        "interpretation_warning": "CI expectations are documented command expectations only and are not approval, validation, or readiness.",
    }


def _known_blockers(repo_root: Path) -> list[str]:
    blockers: list[str] = []
    for relative_path in [
        "release/v1_5_rc/CALIBRATION_BLOCKERS.md",
        "release/v1_5_rc/NON_CLAIM_BOUNDARIES.md",
        "release/v1_5_rc/EXTERNAL_REVIEW_ROUTING.md",
    ]:
        if (repo_root / relative_path).exists():
            blockers.append(f"{relative_path} remains part of the RC package and preserves unresolved blocker/non-claim material.")
    return blockers


def build_final_rc_integrity_seal_result(payload: dict[str, Any], repo_root: Path) -> IntegritySealResult:
    _required_mapping(
        payload,
        [
            "seal_id",
            "seal_name",
            "seal_status",
            "non_claims",
            "required_release_documents",
            "required_attack_pack_documents",
            "required_generated_reports",
            "required_manifests",
            "required_streamlit_pages",
            "required_docs",
            "required_scripts",
            "required_tests",
            "required_false_flags",
            "required_boundary_phrases",
            "forbidden_affirmative_claims",
            "guardrail_expectations",
            "ci_expectations",
            "digest_targets",
        ],
        "seal manifest",
    )
    if payload["seal_status"] != "internal_integrity_seal_only":
        raise ValueError("seal_status must be internal_integrity_seal_only")
    for non_claim in FINAL_RC_INTEGRITY_SEAL_NON_CLAIMS:
        if non_claim not in payload["non_claims"]:
            raise ValueError("seal manifest missing required non-claim language")

    release_docs = _list_of_strings(payload["required_release_documents"], "required_release_documents")
    attack_docs = _list_of_strings(payload["required_attack_pack_documents"], "required_attack_pack_documents")
    reports = _list_of_strings(payload["required_generated_reports"], "required_generated_reports")
    manifests = _list_of_strings(payload["required_manifests"], "required_manifests")
    streamlit_pages = _list_of_strings(payload["required_streamlit_pages"], "required_streamlit_pages")
    docs = _list_of_strings(payload["required_docs"], "required_docs")
    scripts = _list_of_strings(payload["required_scripts"], "required_scripts")
    tests = _list_of_strings(payload["required_tests"], "required_tests")
    false_flags = _mapping_of_false_flags(payload["required_false_flags"], "required_false_flags")
    boundary_phrases = _list_of_strings(payload["required_boundary_phrases"], "required_boundary_phrases")
    digest_targets = _list_of_strings(payload["digest_targets"], "digest_targets")

    release_document_checks = [_document_check(repo_root, path, "release_documents", boundary_phrases) for path in release_docs]
    attack_pack_document_checks = [_document_check(repo_root, path, "attack_pack_documents", boundary_phrases) for path in attack_docs]
    generated_report_checks = [_report_check(repo_root, path) for path in reports]
    all_artefacts = (
        [_artefact_check(repo_root, path, "working_paper") for path in ["paper/CARSF_V1_5_WORKING.md"]]
        + [_artefact_check(repo_root, path, "release_documents") for path in release_docs]
        + [_artefact_check(repo_root, path, "attack_pack_documents") for path in attack_docs]
        + [_artefact_check(repo_root, path, "generated_reports") for path in reports]
        + [_artefact_check(repo_root, path, "dashboard_manifests") for path in manifests if "dashboard" in path]
        + [_artefact_check(repo_root, path, "release_manifests") for path in manifests if "release" in path]
        + [_artefact_check(repo_root, path, "attack_pack_manifests") for path in manifests if "review" in path or "attack_pack" in path]
        + [_artefact_check(repo_root, path, "streamlit_pages") for path in streamlit_pages]
        + [_artefact_check(repo_root, path, "docs") for path in docs]
        + [_artefact_check(repo_root, path, "ci_workflow") for path in [str(payload["ci_expectations"].get("workflow_path", ".github/workflows/ci.yml"))]]
        + [_artefact_check(repo_root, path, "tests") for path in tests]
        + [_artefact_check(repo_root, path, "scripts") for path in scripts]
    )

    manifest_alignment = _manifest_alignment_checks(repo_root, payload)
    false_flag_checks = _false_flag_checks(repo_root, false_flags)
    boundary_phrase_checks = _boundary_checks(release_document_checks + attack_pack_document_checks, boundary_phrases)
    guardrail_status = _guardrail_status(repo_root, payload["guardrail_expectations"])
    ci_expectations = _ci_expectations(repo_root, payload["ci_expectations"])
    digest_manifest = build_digest_manifest(repo_root, digest_targets)
    known_blockers = _known_blockers(repo_root)

    payload_for_claim_scan = _strip_claim_list_fields(payload)
    manifest_forbidden = find_forbidden_affirmative_seal_claims(str(payload_for_claim_scan))
    forbidden_count = (
        len(manifest_forbidden)
        + sum(len(check.forbidden_claim_findings) for check in release_document_checks)
        + sum(len(check.forbidden_claim_findings) for check in attack_pack_document_checks)
        + sum(len(check.forbidden_claim_findings) for check in generated_report_checks)
    )
    missing_release_docs = sum(not check.exists for check in release_document_checks)
    missing_attack_docs = sum(not check.exists for check in attack_pack_document_checks)
    missing_reports = sum(not check.exists for check in generated_report_checks)
    missing_manifests = sum(not (repo_root / path).exists() for path in manifests)
    missing_scripts = sum(not (repo_root / path).exists() for path in scripts)
    boundary_failures = sum(not check.passed for check in boundary_phrase_checks)
    false_flag_failures = sum(not check.passed for check in false_flag_checks)
    digest_failures = sum(not digest.exists or not digest.sha256 for digest in digest_manifest)
    manifest_failures = sum(not check.aligned for check in manifest_alignment)
    ci_failures = 0 if ci_expectations["aligned"] else 1
    guardrail_failures = 0 if guardrail_status.status == "clean" else 1

    missing_gaps = [
        artefact.artefact_path
        for artefact in all_artefacts
        if not artefact.exists
    ]
    missing_gaps.extend(
        f"{check.manifest_path}: {', '.join(check.missing_items)}"
        for check in manifest_alignment
        if check.missing_items
    )
    if manifest_forbidden:
        missing_gaps.append("seal manifest contains forbidden affirmative claims: " + ", ".join(manifest_forbidden))
    if ci_expectations["commands_missing"]:
        missing_gaps.append("CI workflow missing expected commands: " + ", ".join(ci_expectations["commands_missing"]))

    seal_passed = all(
        failure == 0
        for failure in [
            missing_release_docs,
            missing_attack_docs,
            missing_reports,
            missing_manifests,
            missing_scripts,
            false_flag_failures,
            forbidden_count,
            boundary_failures,
            guardrail_failures,
            digest_failures,
            manifest_failures,
            ci_failures,
        ]
    )

    false_flag_values = {flag: False for flag in false_flags}
    summary = IntegritySealSummary(
        total_release_documents_required=len(release_docs),
        release_documents_present=len(release_docs) - missing_release_docs,
        release_documents_missing=missing_release_docs,
        total_attack_pack_documents_required=len(attack_docs),
        attack_pack_documents_present=len(attack_docs) - missing_attack_docs,
        attack_pack_documents_missing=missing_attack_docs,
        total_generated_reports_required=len(reports),
        generated_reports_present=len(reports) - missing_reports,
        generated_reports_missing=missing_reports,
        total_required_manifests=len(manifests),
        manifests_present=len(manifests) - missing_manifests,
        manifests_missing=missing_manifests,
        total_required_scripts=len(scripts),
        scripts_present=len(scripts) - missing_scripts,
        scripts_missing=missing_scripts,
        digest_targets_total=len(digest_manifest),
        digests_written=sum(digest.exists and bool(digest.sha256) for digest in digest_manifest),
        forbidden_claim_findings=forbidden_count,
        boundary_phrase_failures=boundary_failures,
        false_flag_failures=false_flag_failures,
        guardrail_denied_findings=guardrail_status.denied_findings,
        seal_passed=seal_passed,
        review_completed=false_flag_values["review_completed"],
        approval_claimed=false_flag_values["approval_claimed"],
        validation_claimed=false_flag_values["validation_claimed"],
        readiness_score_created=false_flag_values["readiness_score_created"],
        maturity_score_created=false_flag_values["maturity_score_created"],
        operational_readiness_claimed=false_flag_values["operational_readiness_claimed"],
        legal_sufficiency_claimed=false_flag_values["legal_sufficiency_claimed"],
        legislative_readiness_claimed=false_flag_values["legislative_readiness_claimed"],
        economic_validation_claimed=false_flag_values["economic_validation_claimed"],
        welfare_validation_claimed=false_flag_values["welfare_validation_claimed"],
        statistical_validation_claimed=false_flag_values["statistical_validation_claimed"],
        official_status_claimed=false_flag_values["official_status_claimed"],
        official_review_pathway_claimed=false_flag_values["official_review_pathway_claimed"],
        real_data_used=false_flag_values["real_data_used"],
        actual_tax_payable_determined=false_flag_values["actual_tax_payable_determined"],
        compliance_scoring_created=false_flag_values["compliance_scoring_created"],
        enforcement_created=false_flag_values["enforcement_created"],
        notices_created=false_flag_values["notices_created"],
        penalties_created=false_flag_values["penalties_created"],
        operative_law_created=false_flag_values["operative_law_created"],
        firm_level_liability_logic_modified=false_flag_values["firm_level_liability_logic_modified"],
        warnings=[
            "seal_passed is an internal artefact integrity status only.",
            "The seal does not mean approval, validation, external review completion, readiness, legal sufficiency, official status, or implementation readiness.",
        ],
    )

    return IntegritySealResult(
        seal_id=str(payload["seal_id"]),
        seal_name=str(payload["seal_name"]),
        seal_status=str(payload["seal_status"]),
        artefact_inventory=sorted(all_artefacts, key=lambda item: (item.artefact_group, item.artefact_path)),
        release_document_checks=release_document_checks,
        attack_pack_document_checks=attack_pack_document_checks,
        generated_report_checks=generated_report_checks,
        manifest_alignment_checks=manifest_alignment,
        false_flag_checks=false_flag_checks,
        boundary_phrase_checks=boundary_phrase_checks,
        digest_manifest=digest_manifest,
        guardrail_status=guardrail_status,
        ci_expectations=ci_expectations,
        known_blockers_preserved=known_blockers,
        missing_artefacts_or_seal_gaps=missing_gaps,
        summary=summary,
        warnings=list(summary.warnings),
    )
