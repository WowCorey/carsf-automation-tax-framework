from __future__ import annotations

from carsf.evidence_packet import MOCK_PACKET_NON_CLAIM, EvidencePacketSummary
from carsf.review_workflow import evaluate_review_transition


def summary(**overrides) -> EvidencePacketSummary:
    base = EvidencePacketSummary(
        packet_id="unit_test_packet",
        linked_example_id="unit_test_example",
        item_count=2,
        sufficient_items=1,
        partial_items=1,
        missing_items=0,
        low_confidence_items=1,
        review_state="placeholder_only",
        privacy_classification="moderate",
        secrecy_classification="internal_research",
        non_claims=[MOCK_PACKET_NON_CLAIM],
    )
    return EvidencePacketSummary(**{**base.__dict__, **overrides})


def test_review_workflow_allows_placeholder_to_submitted_with_valid_packet() -> None:
    result = evaluate_review_transition(summary(), "submitted_mock")

    assert result.allowed is True
    assert result.approved_state == "submitted_mock"


def test_review_workflow_rejects_invalid_transition() -> None:
    result = evaluate_review_transition(summary(), "sufficient_for_prototype")

    assert result.allowed is False
    assert result.approved_state == "placeholder_only"


def test_high_privacy_classification_triggers_privacy_review() -> None:
    result = evaluate_review_transition(
        summary(review_state="submitted_mock", review_flags=["needs_privacy_review"]),
        "partial",
    )

    assert result.allowed is False
    assert result.approved_state == "needs_privacy_review"


def test_tax_sensitive_transfer_pricing_triggers_tax_review() -> None:
    result = evaluate_review_transition(
        summary(review_state="submitted_mock", review_flags=["needs_tax_review"]),
        "partial",
    )

    assert result.allowed is False
    assert result.approved_state == "needs_tax_review"


def test_legal_sensitive_evidence_triggers_legal_review() -> None:
    result = evaluate_review_transition(
        summary(review_state="submitted_mock", review_flags=["needs_legal_review"]),
        "partial",
    )

    assert result.allowed is False
    assert result.approved_state == "needs_legal_review"


def test_no_review_state_implies_real_world_validation() -> None:
    result = evaluate_review_transition(summary(review_state="submitted_mock"), "partial")
    combined = " ".join(result.reasons + result.warnings + result.non_claims).lower()

    assert "do not imply real-world validation" in combined
    assert result.approved_state != "sufficient"
