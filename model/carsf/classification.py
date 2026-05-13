"""Prototype privacy and secrecy classification helpers for evidence items."""

from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .evidence import EvidenceItem


PRIVACY_CLASSIFICATIONS = {"public", "low", "moderate", "high", "restricted_placeholder"}
SECRECY_CLASSIFICATIONS = {"open", "internal_research", "confidential_placeholder", "restricted_placeholder"}
SENSITIVE_MARKERS = (
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


def _item_dict(item: EvidenceItem | dict[str, Any]) -> dict[str, Any]:
    if isinstance(item, EvidenceItem):
        return asdict(item)
    return dict(item)


def _combined_text(payload: dict[str, Any]) -> str:
    return " ".join(str(value) for value in payload.values()).lower()


def _contains_sensitive_marker(text: str) -> bool:
    if any(marker in text for marker in SENSITIVE_MARKERS):
        return True
    return "abn" in text and "fake" not in text


def classify_evidence_item(item: EvidenceItem | dict[str, Any]) -> dict[str, Any]:
    """Classify one evidence item using prototype-only rules."""

    payload = _item_dict(item)
    text = _combined_text(payload)
    review_required = True
    reason = "Prototype classification only."

    if _contains_sensitive_marker(text):
        return {
            "privacy_classification": "restricted_placeholder",
            "secrecy_classification": "restricted_placeholder",
            "review_required": True,
            "reason": "Sensitive marker detected; restricted-placeholder review required.",
            "non_claims": ["Prototype classification only; no legal, tax, audit, or privacy validation."],
        }
    if any(term in text for term in ("worker", "wage", "hours", "payroll", "timesheet")):
        privacy = "high"
        secrecy = "confidential_placeholder"
        reason = "Worker-level wage/hour evidence is high sensitivity in this prototype."
    elif any(term in text for term in ("transfer-pricing", "transfer pricing", "related-party", "related party", "royalty", "licence", "contract")):
        privacy = "high"
        secrecy = "confidential_placeholder"
        reason = "Transfer-pricing contracts and related-party records are high sensitivity in this prototype."
    elif any(term in text for term in ("firm-level", "financial", "invoice", "management account", "aava", "revenue")):
        privacy = "moderate"
        secrecy = "internal_research"
        reason = "Firm-level financial evidence is at least moderate/internal research."
    elif any(term in text for term in ("public", "aggregate", "published")):
        privacy = "public"
        secrecy = "open"
        review_required = False
        reason = "Public aggregate data can be public/open in this prototype."
    else:
        privacy = "low"
        secrecy = "internal_research"

    return {
        "privacy_classification": privacy,
        "secrecy_classification": secrecy,
        "review_required": review_required,
        "reason": reason,
        "non_claims": ["Prototype classification only; no legal, tax, audit, or privacy validation."],
    }


def classify_packet(packet: Any) -> dict[str, Any]:
    """Classify a packet by taking the highest sensitivity across its items."""

    privacy_rank = {"public": 0, "low": 1, "moderate": 2, "high": 3, "restricted_placeholder": 4}
    secrecy_rank = {"open": 0, "internal_research": 1, "confidential_placeholder": 2, "restricted_placeholder": 3}
    item_classifications = [classify_evidence_item(item) for item in packet.evidence_items]
    packet_privacy = packet.privacy_classification
    packet_secrecy = packet.secrecy_classification
    for classification in item_classifications:
        if privacy_rank[classification["privacy_classification"]] > privacy_rank[packet_privacy]:
            packet_privacy = classification["privacy_classification"]
        if secrecy_rank[classification["secrecy_classification"]] > secrecy_rank[packet_secrecy]:
            packet_secrecy = classification["secrecy_classification"]
    return {
        "packet_id": packet.packet_id,
        "privacy_classification": packet_privacy,
        "secrecy_classification": packet_secrecy,
        "review_required": packet_privacy in {"high", "restricted_placeholder"} or packet_secrecy in {"confidential_placeholder", "restricted_placeholder"},
        "item_classifications": item_classifications,
        "non_claims": ["Prototype privacy/secrecy classification only; not legal, tax, ATO, Treasury, audit, forensic, or privacy validation."],
    }
