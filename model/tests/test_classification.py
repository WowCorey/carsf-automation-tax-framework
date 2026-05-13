from __future__ import annotations

from carsf.classification import classify_evidence_item
from carsf.evidence import EvidenceItem


def test_worker_level_wage_hour_evidence_is_high_sensitivity() -> None:
    result = classify_evidence_item(
        EvidenceItem(
            evidence_id="worker_hours",
            requirement_id="core_worker_hours",
            source_type="synthetic_worker_roster",
            source_description="Synthetic worker wage and hours summary.",
            confidence="medium",
            provided=True,
        )
    )

    assert result["privacy_classification"] == "high"
    assert result["secrecy_classification"] == "confidential_placeholder"


def test_transfer_pricing_contracts_are_high_sensitivity() -> None:
    result = classify_evidence_item(
        EvidenceItem(
            evidence_id="tp_contract",
            requirement_id="tp_related_party_agreements",
            source_type="synthetic_related_party_agreement",
            source_description="Synthetic transfer-pricing contract placeholder.",
            confidence="medium",
            provided=True,
        )
    )

    assert result["privacy_classification"] == "high"
    assert result["secrecy_classification"] == "confidential_placeholder"


def test_sensitive_marker_forces_restricted_placeholder() -> None:
    result = classify_evidence_item(
        {
            "evidence_id": "bad",
            "requirement_id": "core_output_value",
            "source_description": "Synthetic text with private key marker.",
        }
    )

    assert result["privacy_classification"] == "restricted_placeholder"
    assert result["secrecy_classification"] == "restricted_placeholder"
