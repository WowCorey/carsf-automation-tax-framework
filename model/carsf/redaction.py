"""Redaction-plan metadata for prototype secure evidence ingestion."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .sensitive_scan import SensitiveScanResult


REDACTION_NON_CLAIMS = [
    "This is a prototype redaction plan only.",
    "It is not legal, privacy, cybersecurity, evidentiary, forensic, Treasury, ATO, tax, or audit validation.",
    "Real sensitive evidence must not be redacted into this repository.",
]


@dataclass(frozen=True)
class RedactionPlan:
    plan_id: str
    required: bool
    fields_to_remove: list[str]
    fields_to_hash: list[str]
    fields_to_generalise: list[str]
    denied_fields: list[str]
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(REDACTION_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def create_redaction_plan(scan_result: SensitiveScanResult, evidence_mode: str) -> RedactionPlan:
    """Create redaction metadata without emitting any sensitive source values."""

    synthetic = evidence_mode == "synthetic_mock"
    required = scan_result.deny_ingestion or not synthetic
    if scan_result.markers_found:
        warnings = [
            "Sensitive markers were found; repo ingestion must be denied rather than creating a redacted repo copy.",
            "Use an external secure system for any real redaction workflow.",
        ]
    elif not synthetic:
        warnings = ["Non-synthetic evidence requires external secure-system design before any redaction workflow."]
    else:
        warnings = ["No redaction required for clean synthetic mock metadata."]

    return RedactionPlan(
        plan_id=f"redaction-{evidence_mode}",
        required=required,
        fields_to_remove=["direct identifiers", "raw source documents"] if required else [],
        fields_to_hash=["stable external reference IDs"] if required else [],
        fields_to_generalise=["synthetic scenario descriptions"] if synthetic else [],
        denied_fields=scan_result.markers_found,
        warnings=warnings,
    )
