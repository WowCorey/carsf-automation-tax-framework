from __future__ import annotations

from carsf.evidence import EvidenceItem
from carsf.evidence_packet import (
    MOCK_PACKET_NON_CLAIM,
    EvidencePacket,
    load_evidence_packet,
    summarise_evidence_packet,
    validate_evidence_packet,
)


def packet_fixture_path(repo_root, name: str):
    return repo_root / "data" / "mock_evidence" / name


def base_packet(**overrides) -> EvidencePacket:
    packet = EvidencePacket(
        packet_id="unit_test_packet",
        linked_example_id="unit_test_example",
        synthetic_mock_evidence_only=True,
        created_for=["core_formula"],
        evidence_items=[
            EvidenceItem(
                evidence_id="item_1",
                requirement_id="core_output_value",
                source_type="synthetic_record",
                source_description="Synthetic aggregate output record.",
                confidence="medium",
                provided=True,
            ),
            EvidenceItem(
                evidence_id="item_2",
                requirement_id="core_worker_hours",
                source_type="synthetic_worker_roster",
                source_description="Synthetic worker roster without personal records.",
                confidence="low",
                provided=True,
            ),
            EvidenceItem(
                evidence_id="item_3",
                requirement_id="core_aii_components",
                source_type="synthetic_gap_note",
                source_description="Synthetic missing item.",
                confidence="none",
                provided=False,
            ),
        ],
        privacy_classification="moderate",
        secrecy_classification="internal_research",
        review_state="submitted_mock",
        non_claims=[MOCK_PACKET_NON_CLAIM],
    )
    return EvidencePacket(**{**packet.__dict__, **overrides})


def test_evidence_packets_load(repo_root) -> None:
    paths = sorted((repo_root / "data" / "mock_evidence").glob("*.yaml"))

    assert paths
    packets = [load_evidence_packet(path) for path in paths]
    assert all(packet.synthetic_mock_evidence_only is True for packet in packets)


def test_evidence_packets_require_synthetic_mock_flag() -> None:
    packet = base_packet(synthetic_mock_evidence_only=False)

    assert "synthetic_mock_evidence_only must be true" in validate_evidence_packet(packet)


def test_forbidden_sensitive_markers_are_rejected() -> None:
    packet = base_packet(
        evidence_items=[
            EvidenceItem(
                evidence_id="bad_item",
                requirement_id="core_output_value",
                source_type="synthetic_record",
                source_description="Synthetic record containing TFN marker.",
                confidence="medium",
                provided=True,
            )
        ]
    )

    assert any("forbidden sensitive marker" in error for error in validate_evidence_packet(packet))


def test_unknown_review_state_is_rejected() -> None:
    packet = base_packet(review_state="officially_validated")

    assert any("unknown review_state" in error for error in validate_evidence_packet(packet))


def test_unknown_privacy_and_secrecy_classifications_are_rejected() -> None:
    packet = base_packet(privacy_classification="official_sensitive", secrecy_classification="official_secret")
    errors = validate_evidence_packet(packet)

    assert any("unknown privacy_classification" in error for error in errors)
    assert any("unknown secrecy_classification" in error for error in errors)


def test_packet_summaries_count_evidence_items() -> None:
    summary = summarise_evidence_packet(base_packet())

    assert summary.item_count == 3
    assert summary.sufficient_items == 1
    assert summary.partial_items == 1
    assert summary.missing_items == 1
    assert summary.low_confidence_items == 1
