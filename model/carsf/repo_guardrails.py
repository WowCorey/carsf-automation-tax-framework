"""Repository-level guardrails for evidence and secret leak prevention."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from .sensitive_scan import scan_text_for_sensitive_markers


REPO_GUARDRAIL_NON_CLAIMS = [
    "These are prototype repository guardrails only.",
    "They are not a complete DLP system, secret scanner, cybersecurity control, legal/privacy audit, Treasury control, ATO control, or forensic validation.",
]

REQUIRED_WARNING = (
    "These are prototype repository guardrails only. They are not a complete DLP system, secret scanner, "
    "cybersecurity control, legal/privacy audit, Treasury control, ATO control, or forensic validation."
)


@dataclass(frozen=True)
class RepoGuardrailPolicy:
    policy_id: str
    version: str
    default_action: str
    prohibited_paths: list[str]
    prohibited_extensions: list[str]
    allowed_mock_paths: list[str]
    generated_report_paths: list[str]
    required_non_claims: list[str]
    allowed_synthetic_markers: list[str]
    non_claims: list[str] = field(default_factory=lambda: list(REPO_GUARDRAIL_NON_CLAIMS))
    skipped_paths: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepoScanFinding:
    finding_id: str
    path: str
    severity: str
    finding_type: str
    message: str
    line_number: int | None
    deny: bool
    allowlisted: bool
    reason: str

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class RepoScanResult:
    clean: bool
    findings: list[RepoScanFinding]
    denied_findings: list[RepoScanFinding]
    warning_findings: list[RepoScanFinding]
    files_scanned: int
    files_skipped: int
    non_claims: list[str] = field(default_factory=lambda: list(REPO_GUARDRAIL_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def get_default_repo_guardrail_policy() -> RepoGuardrailPolicy:
    return RepoGuardrailPolicy(
        policy_id="carsf-v1.5-repo-guardrails",
        version="CARSF V1.5 prototype repository enforcement gates",
        default_action="FAIL_CLOSED",
        prohibited_paths=[
            "data/incoming/",
            "data/private/",
            "data/restricted/",
            "data/real_evidence/",
            "evidence_inbox/",
            "secure_drop/",
            ".env",
            ".env.",
            "secrets/",
            "private/",
        ],
        prohibited_extensions=[
            ".pem",
            ".key",
            ".p12",
            ".pfx",
            ".secret",
            ".crt",
            ".cer",
            ".der",
            ".sqlite",
            ".db",
            ".mdb",
            ".accdb",
        ],
        allowed_mock_paths=[
            "data/mock_evidence/",
            "data/mock_ingestion_requests/",
        ],
        generated_report_paths=[
            "reports/",
        ],
        required_non_claims=[
            "not legal",
            "not a legal",
            "not legal, tax",
            "prototype",
            "not a complete dlp",
            "not a tax",
            "not a tax calculator",
            "not a secure evidence platform",
            "not transfer-pricing adjustments",
        ],
        allowed_synthetic_markers=[
            "FAKE_",
        ],
        skipped_paths=[
            ".git/",
            ".pytest_cache/",
            ".mypy_cache/",
            ".ruff_cache/",
            "__pycache__/",
            "tmp/",
            ".venv/",
            "venv/",
            "env/",
            "dist/",
            "build/",
            "model/tests/fixtures/repo_guardrails/",
        ],
    )


def _normalise(path: str | Path) -> str:
    return str(path).replace("\\", "/").lstrip("./")


def _matches_prefix(path: str, prefixes: list[str]) -> bool:
    normalised = _normalise(path)
    for prefix in prefixes:
        prefix_norm = _normalise(prefix)
        if prefix_norm.endswith("/"):
            if normalised.startswith(prefix_norm):
                return True
        elif normalised == prefix_norm or normalised.startswith(prefix_norm):
            return True
    return False


def _line_number_for(text: str, needle: str) -> int | None:
    needle_lower = needle.lower().replace("_", " ")
    for index, line in enumerate(text.splitlines(), start=1):
        lowered = line.lower().replace("_", " ")
        if needle_lower in lowered:
            return index
    return None


def _finding(
    path: str,
    finding_type: str,
    message: str,
    severity: str = "high",
    line_number: int | None = None,
    deny: bool = True,
    allowlisted: bool = False,
    reason: str = "Default fail-closed repository guardrail.",
) -> RepoScanFinding:
    safe_type = finding_type.lower().replace(" ", "_")
    return RepoScanFinding(
        finding_id=f"{safe_type}:{path}:{line_number or 0}",
        path=path,
        severity=severity,
        finding_type=finding_type,
        message=message,
        line_number=line_number,
        deny=deny,
        allowlisted=allowlisted,
        reason=reason,
    )


def _is_generated_report(path: str, policy: RepoGuardrailPolicy) -> bool:
    return _matches_prefix(path, policy.generated_report_paths) and Path(path).suffix.lower() in {".md", ".json"}


def _is_allowed_mock(path: str, text: str, policy: RepoGuardrailPolicy) -> bool:
    lowered = text.lower()
    return _matches_prefix(path, policy.allowed_mock_paths) and (
        "synthetic_mock_evidence_only: true" in lowered or "synthetic_fixture_only: true" in lowered
    )


def _mock_marker_terms_allowed(path: str, text: str, markers: list[str], policy: RepoGuardrailPolicy) -> bool:
    if any(marker.lower() in text.lower() for marker in policy.allowed_synthetic_markers):
        return True
    normalised = _normalise(path).lower()
    return normalised.startswith("data/mock_ingestion_requests/") and set(markers) <= {"SECRET"}


def _is_documented_marker_example(path: str, text: str) -> bool:
    normalised = _normalise(path).lower()
    documentation_paths = (
        normalised.startswith("docs/")
        or normalised.startswith("release/")
        or normalised.startswith("paper/")
        or normalised.startswith("model/tests/")
        or normalised in {
            "readme.md",
            "build_log.md",
            "contributing.md",
            ".pre-commit-config.yaml",
            "gitignore",
            ".gitignore",
            "data/readme.md",
        }
    )
    if documentation_paths:
        return True
    lowered = text.lower()
    if normalised.startswith("schedules/") and (
        "status: placeholder_prototype" in lowered or "calibration_status: illustrative_placeholder" in lowered
    ):
        return True
    return normalised.startswith("examples/") and "illustrative_placeholder_only: true" in lowered


def _is_guardrail_policy_definition(path: str, text: str) -> bool:
    normalised = _normalise(path).lower()
    allowed_code_paths = {
        "model/carsf/sensitive_scan.py",
        "model/carsf/secure_ingestion.py",
        "model/carsf/evidence_packet.py",
        "model/carsf/classification.py",
        "model/carsf/redaction.py",
        "model/carsf/retention.py",
        "model/carsf/ingestion_audit.py",
        "model/carsf/repo_guardrails.py",
        "scripts/run_evidence_workflow.py",
        "scripts/run_ingestion_controls.py",
        "scripts/run_repo_guardrails.py",
        "simulator/pages/10_secure_ingestion_controls.py",
        "simulator/pages/11_repository_guardrails.py",
    }
    return normalised in allowed_code_paths


def _documented_model_marker_reason(path: str, markers: list[str]) -> str | None:
    normalised = _normalise(path).lower()
    marker_set = set(markers)
    documented_references = {
        "model/carsf/avoidance.py": (
            {"INVOICE"},
            "Allowed only because the avoidance review text names cloud invoices as evidence vocabulary.",
        ),
        "model/carsf/evidence.py": (
            {"EMPLOYMENT_CONTRACT", "INVOICE"},
            "Allowed only because the evidence registry enumerates prototype acceptable-source categories.",
        ),
        "model/carsf/decision_log.py": (
            {"API_KEY", "PASSWORD", "TFN"},
            "Allowed only because the decision-log sanitizer defines marker names that must not appear in log content.",
        ),
    }
    if normalised not in documented_references:
        return None
    allowed_markers, reason = documented_references[normalised]
    if marker_set <= allowed_markers:
        return reason
    return None


def _has_required_non_claim(text: str, policy: RepoGuardrailPolicy) -> bool:
    lowered = text.lower()
    return any(required.lower() in lowered for required in policy.required_non_claims)


def _raw_evidence_payload_markers(text: str) -> list[str]:
    lowered = text.lower()
    markers = []
    for marker in ('"evidence_items"', "evidence_items:"):
        if marker in lowered:
            markers.append(marker)
    return markers


def _scan_file_with_relative(
    full_path: str | Path,
    relative_path_value: str | Path,
    policy: RepoGuardrailPolicy,
) -> list[RepoScanFinding]:
    file_path = Path(full_path)
    relative_path = _normalise(relative_path_value)
    findings: list[RepoScanFinding] = []

    if _matches_prefix(relative_path, policy.prohibited_paths):
        findings.append(
            _finding(
                relative_path,
                "prohibited_path",
                "File is inside a prohibited evidence/secrets storage path.",
                severity="critical",
            )
        )
    if file_path.suffix.lower() in policy.prohibited_extensions:
        findings.append(
            _finding(
                relative_path,
                "prohibited_extension",
                f"File has prohibited extension `{file_path.suffix.lower()}`.",
                severity="critical",
            )
        )

    try:
        text = file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return findings
    except OSError:
        return findings

    if _is_generated_report(relative_path, policy):
        if not _has_required_non_claim(text, policy):
            findings.append(
                _finding(
                    relative_path,
                    "missing_report_non_claim",
                    "Generated report is missing required prototype/non-claim language.",
                    severity="high",
                )
            )
        if relative_path not in {"reports/repo_guardrails.md", "reports/repo_guardrails.json"}:
            for marker in _raw_evidence_payload_markers(text):
                findings.append(
                    _finding(
                        relative_path,
                        "raw_evidence_payload",
                        f"Generated report appears to contain raw evidence payload marker `{marker}`.",
                        severity="critical",
                        line_number=_line_number_for(text, marker),
                    )
                )
        return findings

    scan = scan_text_for_sensitive_markers(text)
    if scan.markers_found:
        if _is_allowed_mock(relative_path, text, policy):
            if _mock_marker_terms_allowed(relative_path, text, scan.markers_found, policy):
                findings.append(
                    _finding(
                        relative_path,
                        "allowlisted_synthetic_marker",
                        f"Synthetic mock fixture contains controlled marker terms: {', '.join(scan.markers_found)}.",
                        severity="low",
                        deny=False,
                        allowlisted=True,
                        reason=(
                            "Allowed only in controlled synthetic mock fixture paths with "
                            "synthetic_mock_evidence_only: true and FAKE_ marker text or fixture control fields."
                        ),
                    )
                )
            else:
                findings.append(
                    _finding(
                        relative_path,
                        "mock_marker_without_fake_prefix",
                        f"Synthetic mock fixture contains marker terms without FAKE_ prefix: {', '.join(scan.markers_found)}.",
                        severity="high",
                        deny=True,
                        allowlisted=False,
                        reason="Synthetic marker examples must use explicit FAKE_ markers unless they are fixture control fields.",
                    )
                )
        elif _is_documented_marker_example(relative_path, text):
            findings.append(
                _finding(
                    relative_path,
                    "documented_marker_example",
                    f"Documentation/test file contains marker examples: {', '.join(scan.markers_found)}.",
                    severity="low",
                    deny=False,
                    allowlisted=True,
                    reason="Allowed as documented scanner examples in docs/tests only.",
                )
            )
        elif _is_guardrail_policy_definition(relative_path, text):
            findings.append(
                _finding(
                    relative_path,
                    "policy_marker_definition",
                    f"Guardrail implementation contains policy marker definitions: {', '.join(scan.markers_found)}.",
                    severity="low",
                    deny=False,
                    allowlisted=True,
                    reason="Allowed in guardrail policy implementation files only.",
                )
            )
        elif model_reason := _documented_model_marker_reason(relative_path, scan.markers_found):
            findings.append(
                _finding(
                    relative_path,
                    "documented_model_marker_reference",
                    f"Model file contains narrowly documented marker vocabulary: {', '.join(scan.markers_found)}.",
                    severity="low",
                    deny=False,
                    allowlisted=True,
                    reason=model_reason,
                )
            )
        else:
            first_marker = scan.markers_found[0]
            findings.append(
                _finding(
                    relative_path,
                    "sensitive_marker",
                    f"Sensitive scanner found markers: {', '.join(scan.markers_found)}.",
                    severity=scan.severity if scan.severity != "none" else "high",
                    line_number=_line_number_for(text, first_marker),
                    deny=True,
                    allowlisted=False,
                    reason="Apparent sensitive marker outside controlled synthetic/mock documentation allowlist.",
                )
            )

    if _matches_prefix(relative_path, policy.allowed_mock_paths) and "synthetic_mock_evidence_only: true" not in text.lower():
        findings.append(
            _finding(
                relative_path,
                "mock_missing_synthetic_flag",
                "Mock fixture path is missing synthetic_mock_evidence_only: true.",
                severity="critical",
            )
        )

    return findings


def scan_file(path: str | Path, policy: RepoGuardrailPolicy) -> list[RepoScanFinding]:
    """Scan one file path."""

    return _scan_file_with_relative(path, path, policy)


def _should_skip(path: Path, root: Path, policy: RepoGuardrailPolicy) -> bool:
    try:
        relative = _normalise(path.relative_to(root))
    except ValueError:
        relative = _normalise(path)
    return _matches_prefix(relative, policy.skipped_paths) or any(part in {"__pycache__"} for part in path.parts)


def scan_repo(root: str | Path, policy: RepoGuardrailPolicy | None = None) -> RepoScanResult:
    policy = policy or get_default_repo_guardrail_policy()
    root_path = Path(root).resolve()
    findings: list[RepoScanFinding] = []
    files_scanned = 0
    files_skipped = 0

    for path in sorted(root_path.rglob("*"), key=lambda item: _normalise(item.relative_to(root_path))):
        if path.is_dir():
            continue
        if _should_skip(path, root_path, policy):
            files_skipped += 1
            continue
        try:
            relative = path.relative_to(root_path)
        except ValueError:
            relative = path
        files_scanned += 1
        findings.extend(_scan_file_with_relative(path, relative, policy))

    denied = [finding for finding in findings if finding.deny]
    warnings = [finding for finding in findings if not finding.deny]
    return RepoScanResult(
        clean=not denied,
        findings=findings,
        denied_findings=denied,
        warning_findings=warnings,
        files_scanned=files_scanned,
        files_skipped=files_skipped,
    )
