"""Synthetic mock evidence packet model for CARSF V1.5."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

import yaml

from .classification import PRIVACY_CLASSIFICATIONS, SECRECY_CLASSIFICATIONS, classify_packet
from .evidence import CONFIDENCE_RANK, EvidenceItem


MOCK_PACKET_NON_CLAIM = (
    "This packet is synthetic mock evidence only and does not validate any real liability, "
    "tax position, audit finding, legal conclusion, Treasury assessment, ATO assessment, or economic claim."
)
REVIEW_STATES = {
    "placeholder_only",
    "submitted_mock",
    "incomplete",
    "partial",
    "sufficient_for_prototype",
    "rejected",
    "needs_legal_review",
    "needs_tax_review",
    "needs_privacy_review",
    "needs_calibration",
    "locked_for_external_review",
}
FORBIDDEN_MARKERS = (
    "tfn",
    "tax file number",
    "password",
    "api key",
    "api_key",
    "secret",
    "private key",
    "bank account",
    "medicare number",
    "real taxpayer",
)


@dataclass(frozen=True)
class EvidencePacket:
    packet_id: str
    linked_example_id: str
    synthetic_mock_evidence_only: bool
    created_for: list[str]
    evidence_items: list[EvidenceItem]
    privacy_classification: str
    secrecy_classification: str
    review_state: str
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: [MOCK_PACKET_NON_CLAIM])
    ready_for_external_review: bool = False
    tests_pass_marker: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvidencePacketSummary:
    packet_id: str
    linked_example_id: str
    item_count: int
    sufficient_items: int
    partial_items: int
    missing_items: int
    low_confidence_items: int
    review_state: str
    privacy_classification: str
    secrecy_classification: str
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: [MOCK_PACKET_NON_CLAIM])
    review_flags: list[str] = field(default_factory=list)
    ready_for_external_review: bool = False
    tests_pass_marker: bool = False

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _evidence_items(raw_items: Any) -> list[EvidenceItem]:
    if not isinstance(raw_items, list):
        raise ValueError("evidence_items must be a list")
    items: list[EvidenceItem] = []
    for index, raw in enumerate(raw_items):
        if not isinstance(raw, dict):
            raise ValueError(f"evidence_items[{index}] must be a mapping")
        items.append(
            EvidenceItem(
                evidence_id=str(raw.get("evidence_id", f"evidence_{index + 1}")),
                requirement_id=str(raw.get("requirement_id", "")),
                source_type=str(raw.get("source_type", "")),
                source_description=str(raw.get("source_description", "")),
                confidence=str(raw.get("confidence", "none")).lower(),
                provided=bool(raw.get("provided", False)),
                date_or_period=raw.get("date_or_period"),
                limitations=[str(value) for value in raw.get("limitations", [])],
            )
        )
    return items


def _packet_from_mapping(data: dict[str, Any]) -> EvidencePacket:
    non_claims = [str(value) for value in data.get("non_claims", [MOCK_PACKET_NON_CLAIM])]
    if MOCK_PACKET_NON_CLAIM not in non_claims:
        non_claims.append(MOCK_PACKET_NON_CLAIM)
    return EvidencePacket(
        packet_id=str(data.get("packet_id", "")),
        linked_example_id=str(data.get("linked_example_id", "")),
        synthetic_mock_evidence_only=bool(data.get("synthetic_mock_evidence_only", False)),
        created_for=[str(value) for value in data.get("created_for", [])],
        evidence_items=_evidence_items(data.get("evidence_items", [])),
        privacy_classification=str(data.get("privacy_classification", "")),
        secrecy_classification=str(data.get("secrecy_classification", "")),
        review_state=str(data.get("review_state", "")),
        warnings=[str(value) for value in data.get("warnings", [])],
        non_claims=non_claims,
        ready_for_external_review=bool(data.get("ready_for_external_review", False)),
        tests_pass_marker=bool(data.get("tests_pass_marker", False)),
        metadata=dict(data.get("metadata", {}) or {}),
    )


def _forbidden_marker_errors(packet: EvidencePacket) -> list[str]:
    text = str(packet.to_jsonable()).lower()
    errors = [f"forbidden sensitive marker detected: {marker}" for marker in FORBIDDEN_MARKERS if marker in text]
    if "abn" in text and "fake" not in text:
        errors.append("real business ABN marker detected without explicit fake label")
    return errors


def validate_evidence_packet(packet: EvidencePacket) -> list[str]:
    errors: list[str] = []
    if packet.synthetic_mock_evidence_only is not True:
        errors.append("synthetic_mock_evidence_only must be true")
    if packet.review_state not in REVIEW_STATES:
        errors.append(f"unknown review_state: {packet.review_state}")
    if packet.privacy_classification not in PRIVACY_CLASSIFICATIONS:
        errors.append(f"unknown privacy_classification: {packet.privacy_classification}")
    if packet.secrecy_classification not in SECRECY_CLASSIFICATIONS:
        errors.append(f"unknown secrecy_classification: {packet.secrecy_classification}")
    if MOCK_PACKET_NON_CLAIM not in packet.non_claims:
        errors.append("required synthetic mock evidence non-claim is missing")
    errors.extend(_forbidden_marker_errors(packet))
    return errors


def load_evidence_packet(path: str | Path) -> EvidencePacket:
    packet_path = Path(path)
    loaded = yaml.safe_load(packet_path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"evidence packet must be a mapping: {packet_path}")
    packet = _packet_from_mapping(loaded)
    errors = validate_evidence_packet(packet)
    if errors:
        raise ValueError("; ".join(errors))
    return packet


def _review_flags(packet: EvidencePacket, packet_classification: dict[str, Any]) -> list[str]:
    flags: set[str] = set()
    if packet_classification["privacy_classification"] in {"high", "restricted_placeholder"} or packet_classification["secrecy_classification"] in {"confidential_placeholder", "restricted_placeholder"}:
        flags.add("needs_privacy_review")
    for item in packet.evidence_items:
        text = f"{item.requirement_id} {item.source_type} {item.source_description}".lower()
        if item.requirement_id.startswith("tp_") or "transfer" in text or "related-party" in text or "related party" in text:
            flags.add("needs_tax_review")
        if item.requirement_id.startswith(("tp_", "group_", "avoid_offshore", "avoid_entity")) or "contract" in text or "agreement" in text:
            flags.add("needs_legal_review")
        if item.requirement_id.startswith("mixed_") or "conversion" in text:
            flags.add("needs_calibration")
    return sorted(flags)


def summarise_evidence_packet(packet: EvidencePacket) -> EvidencePacketSummary:
    sufficient = 0
    partial = 0
    missing = 0
    low_confidence = 0
    for item in packet.evidence_items:
        confidence_rank = CONFIDENCE_RANK.get(item.confidence, 0)
        if not item.provided:
            missing += 1
        elif confidence_rank >= CONFIDENCE_RANK["medium"]:
            sufficient += 1
        else:
            partial += 1
            low_confidence += 1
    packet_classification = classify_packet(packet)
    flags = _review_flags(packet, packet_classification)
    warnings = list(dict.fromkeys([*packet.warnings, packet_classification.get("reason", "Prototype classification only.")]))
    return EvidencePacketSummary(
        packet_id=packet.packet_id,
        linked_example_id=packet.linked_example_id,
        item_count=len(packet.evidence_items),
        sufficient_items=sufficient,
        partial_items=partial,
        missing_items=missing,
        low_confidence_items=low_confidence,
        review_state=packet.review_state,
        privacy_classification=packet_classification["privacy_classification"],
        secrecy_classification=packet_classification["secrecy_classification"],
        warnings=warnings,
        non_claims=packet.non_claims,
        review_flags=flags,
        ready_for_external_review=packet.ready_for_external_review,
        tests_pass_marker=packet.tests_pass_marker,
    )
