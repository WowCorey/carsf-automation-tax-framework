"""Immutable-style audit records for prototype ingestion decisions."""

from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any

from .secure_ingestion import IngestionDecision


AUDIT_NON_CLAIMS = [
    "This is immutable-style prototype logging only.",
    "It is not blockchain, legal audit logging, cybersecurity assurance, evidentiary validation, Treasury guidance, ATO guidance, tax validation, or forensic validation.",
]


@dataclass(frozen=True)
class IngestionAuditRecord:
    record_id: str
    request_id: str
    decision: str
    allowed: bool
    reasons_hash: str
    metadata_hash: str
    previous_record_hash: str | None
    record_hash: str
    generated_at: str
    non_claims: list[str] = field(default_factory=lambda: list(AUDIT_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _hash_payload(payload: Any) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def create_ingestion_audit_record(
    decision: IngestionDecision,
    previous_record_hash: str | None = None,
) -> IngestionAuditRecord:
    """Create a compact audit record without raw request or sensitive text."""

    reasons_hash = _hash_payload(decision.reasons)
    metadata_hash = _hash_payload(
        {
            "request_id": decision.request_id,
            "decision": decision.decision,
            "allowed": decision.allowed,
            "approvals": decision.required_approvals,
            "quarantine_required": decision.quarantine_required,
            "redaction_required": decision.redaction_required,
            "retention_policy": decision.retention_policy,
            "audit_required": decision.audit_required,
        }
    )
    stable_record = {
        "request_id": decision.request_id,
        "decision": decision.decision,
        "allowed": decision.allowed,
        "reasons_hash": reasons_hash,
        "metadata_hash": metadata_hash,
        "previous_record_hash": previous_record_hash,
    }
    record_hash = _hash_payload(stable_record)
    return IngestionAuditRecord(
        record_id=f"ingestion-audit-{record_hash[:16]}",
        request_id=decision.request_id,
        decision=decision.decision,
        allowed=decision.allowed,
        reasons_hash=reasons_hash,
        metadata_hash=metadata_hash,
        previous_record_hash=previous_record_hash,
        record_hash=record_hash,
        generated_at=datetime.now(UTC).replace(microsecond=0).isoformat(),
    )
