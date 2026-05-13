"""Heuristic sensitive-content scanner for CARSF evidence ingestion controls."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


SCAN_NON_CLAIMS = [
    "This scanner is a prototype over-blocking guardrail only.",
    "It is not a complete DLP, privacy, cybersecurity, evidentiary, forensic, tax, ATO, Treasury, or audit tool.",
]

MARKERS: dict[str, str] = {
    "tfn": "critical",
    "tax file number": "critical",
    "medicare number": "critical",
    "bank account": "critical",
    "bsb": "critical",
    "password": "critical",
    "passphrase": "critical",
    "api key": "critical",
    "api_key": "critical",
    "access token": "critical",
    "private key": "critical",
    "secret": "critical",
    "real taxpayer": "critical",
    "real business record": "critical",
    "payslip": "high",
    "employment contract": "high",
    "invoice": "high",
    "abn": "high",
    "acn": "high",
    "credit card": "critical",
    "date of birth": "critical",
    "residential address": "critical",
}

SEVERITY_RANK = {"none": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}


@dataclass(frozen=True)
class SensitiveScanResult:
    clean: bool
    markers_found: list[str] = field(default_factory=list)
    severity: str = "none"
    deny_ingestion: bool = False
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(SCAN_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _canonical_marker(marker: str) -> str:
    return marker.upper().replace(" ", "_")


def _severity(markers: list[str]) -> str:
    severity = "none"
    found = {marker.lower().replace("_", " ") for marker in markers}
    for marker, marker_severity in MARKERS.items():
        if marker in found and SEVERITY_RANK[marker_severity] > SEVERITY_RANK[severity]:
            severity = marker_severity
    if severity == "none" and markers:
        severity = "high"
    return severity


def scan_text_for_sensitive_markers(text: str) -> SensitiveScanResult:
    """Scan text for prohibited markers.

    The scanner intentionally over-blocks. It checks marker presence only and
    does not attempt to prove that a detected value is genuine.
    """

    lowered = str(text).lower()
    markers = sorted({_canonical_marker(marker) for marker in MARKERS if marker in lowered})
    severity = _severity(markers)
    return SensitiveScanResult(
        clean=not markers,
        markers_found=markers,
        severity=severity,
        deny_ingestion=bool(markers),
        warnings=(
            ["Sensitive marker detected; ingestion must fail closed or route to an external secure system."]
            if markers
            else ["No configured sensitive markers detected by this heuristic scan."]
        ),
    )


def _scalar_values(data: Any) -> list[str]:
    if isinstance(data, dict):
        values: list[str] = []
        for value in data.values():
            values.extend(_scalar_values(value))
        return values
    if isinstance(data, list):
        values = []
        for value in data:
            values.extend(_scalar_values(value))
        return values
    if data is None or isinstance(data, bool):
        return []
    return [str(data)]


def scan_mapping_for_sensitive_markers(data: dict[str, Any]) -> SensitiveScanResult:
    """Scan mapping values for prohibited markers without treating field names as content."""

    return scan_text_for_sensitive_markers(" ".join(_scalar_values(data)))
