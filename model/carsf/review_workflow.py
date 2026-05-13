"""Prototype review-state workflow for synthetic evidence packets."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

from .evidence_packet import EvidencePacketSummary, MOCK_PACKET_NON_CLAIM, REVIEW_STATES


WORKFLOW_NON_CLAIMS = [
    MOCK_PACKET_NON_CLAIM,
    "Review states are prototype workflow states only and do not imply real-world validation.",
]


@dataclass(frozen=True)
class ReviewTransition:
    from_state: str
    to_state: str
    allowed: bool
    reason: str
    required_conditions: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ReviewWorkflowResult:
    original_state: str
    requested_state: str
    approved_state: str
    allowed: bool
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(WORKFLOW_NON_CLAIMS))

    def to_jsonable(self) -> dict:
        return asdict(self)


def _prototype_progress_state(summary: EvidencePacketSummary) -> str:
    if summary.item_count == 0:
        return "incomplete"
    if summary.missing_items == 0 and summary.low_confidence_items == 0 and summary.sufficient_items == summary.item_count:
        return "sufficient_for_prototype"
    if summary.sufficient_items + summary.partial_items > 0:
        return "partial"
    return "incomplete"


def _review_gate(summary: EvidencePacketSummary, requested_state: str) -> str | None:
    if summary.review_state == "placeholder_only" and requested_state == "submitted_mock":
        return None
    if "needs_privacy_review" in summary.review_flags and requested_state != "needs_privacy_review":
        return "needs_privacy_review"
    if "needs_tax_review" in summary.review_flags and requested_state not in {"needs_tax_review", "needs_privacy_review"}:
        return "needs_tax_review"
    if "needs_legal_review" in summary.review_flags and requested_state not in {"needs_legal_review", "needs_tax_review", "needs_privacy_review"}:
        return "needs_legal_review"
    if "needs_calibration" in summary.review_flags and requested_state not in {"needs_calibration", "needs_legal_review", "needs_tax_review", "needs_privacy_review"}:
        return "needs_calibration"
    return None


def evaluate_review_transition(packet_summary: EvidencePacketSummary, requested_state: str) -> ReviewWorkflowResult:
    """Evaluate one prototype evidence review transition."""

    original = packet_summary.review_state
    reasons = ["Review workflow is prototype-only and does not validate real-world evidence."]
    warnings = ["No review state may imply legal, tax, Treasury, ATO, audit, forensic, or economic validation."]
    if requested_state not in REVIEW_STATES:
        return ReviewWorkflowResult(
            original_state=original,
            requested_state=requested_state,
            approved_state=original,
            allowed=False,
            reasons=[*reasons, f"Unknown requested review state: {requested_state}"],
            warnings=warnings,
        )

    gate = _review_gate(packet_summary, requested_state)
    if gate is not None:
        return ReviewWorkflowResult(
            original_state=original,
            requested_state=requested_state,
            approved_state=gate,
            allowed=False,
            reasons=[*reasons, f"Review gate triggered: {gate}"],
            warnings=warnings,
        )

    progress = _prototype_progress_state(packet_summary)
    allowed = False
    approved = original
    if original == "placeholder_only" and requested_state == "submitted_mock" and packet_summary.item_count > 0:
        allowed = True
        approved = "submitted_mock"
        reasons.append("Valid mock packet can move placeholder-only evidence into submitted_mock.")
    elif original == "submitted_mock" and requested_state == "partial" and progress == "partial":
        allowed = True
        approved = "partial"
        reasons.append("Some required prototype evidence is supplied, but gaps or low confidence remain.")
    elif original == "submitted_mock" and requested_state == "sufficient_for_prototype" and progress == "sufficient_for_prototype":
        allowed = True
        approved = "sufficient_for_prototype"
        reasons.append("All provided prototype requirements in the packet are medium confidence or better.")
    elif requested_state == "locked_for_external_review":
        state_ready = original in {"partial", "sufficient_for_prototype"}
        marker_ready = packet_summary.tests_pass_marker or packet_summary.ready_for_external_review
        allowed = state_ready and marker_ready
        approved = "locked_for_external_review" if allowed else original
        reasons.append("External review lock requires partial/sufficient prototype state and explicit readiness marker.")
    elif requested_state in {"needs_legal_review", "needs_tax_review", "needs_privacy_review", "needs_calibration", "rejected", "incomplete"}:
        allowed = True
        approved = requested_state
        reasons.append("Manual review state is allowed as a prototype workflow flag.")
    else:
        reasons.append(f"Transition {original} -> {requested_state} is not allowed by the prototype workflow.")

    return ReviewWorkflowResult(
        original_state=original,
        requested_state=requested_state,
        approved_state=approved,
        allowed=allowed,
        reasons=reasons,
        warnings=warnings,
    )
