from __future__ import annotations

import json

from carsf.ingestion_audit import create_ingestion_audit_record
from carsf.secure_ingestion import IngestionDecision


def decision(**overrides) -> IngestionDecision:
    base = {
        "request_id": "audit_request",
        "allowed": True,
        "decision": "ALLOW_SYNTHETIC_MOCK_ONLY",
        "reasons": ["Default-deny checks passed for synthetic mock evidence."],
        "required_approvals": [],
        "quarantine_required": False,
        "redaction_required": False,
        "retention_policy": "retain synthetic mock evidence in repo",
        "audit_required": True,
        "warnings": ["Synthetic only."],
    }
    return IngestionDecision(**{**base, **overrides})


def test_audit_record_hashes_are_stable_for_same_decision_content() -> None:
    first = create_ingestion_audit_record(decision())
    second = create_ingestion_audit_record(decision())

    assert first.record_hash == second.record_hash
    assert first.reasons_hash == second.reasons_hash


def test_audit_record_hash_changes_when_decision_content_changes() -> None:
    first = create_ingestion_audit_record(decision())
    second = create_ingestion_audit_record(decision(allowed=False, decision="DENY"))

    assert first.record_hash != second.record_hash


def test_audit_record_does_not_include_raw_sensitive_text() -> None:
    record = create_ingestion_audit_record(
        decision(reasons=["Synthetic denied reason with FAKE_API_KEY_MARKER raw marker."])
    )
    payload = json.dumps(record.to_jsonable())

    assert "FAKE_API_KEY_MARKER" not in payload
    assert record.record_hash
