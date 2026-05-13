"""Prototype transfer-pricing and related-party review previews.

This module is a non-operative review layer only. It does not implement
transfer-pricing law, OECD guidance, BEPS analysis, ATO findings, Treasury
policy, or economic validation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from typing import Any

from .levy import calculate_liability
from .types import LevyParameters


NON_OPERATIVE_STATUS = (
    "This is a non-operative transfer-pricing / related-party review preview only. "
    "It is not a legal, tax, ATO, Treasury, OECD, BEPS, or economic finding."
)
TRANSFER_PRICING_NON_CLAIMS = [
    NON_OPERATIVE_STATUS,
    "Adjusted AAVA is preview-only and does not replace reported AAVA.",
    "No arm's-length price, transfer-pricing adjustment, tax assessment, or legal conclusion is calculated.",
]
SUPPORTED_TRANSACTION_TYPES = {
    "OFFSHORE_AI_SERVICE_FEE",
    "IP_ROYALTY_OR_PLATFORM_LICENSE",
    "CLOUD_INFERENCE_RELABELLED_AS_ORDINARY_COST",
    "ROBOTICS_LEASE_OR_SERVICE_CONTRACT",
    "MANAGEMENT_OR_TECHNICAL_SERVICE_FEE",
    "DATA_ACCESS_OR_MODEL_LICENSE_FEE",
    "COST_SHARING_OR_GROUP_RECHARGE",
    "OTHER_RELATED_PARTY_AUTOMATION_COST",
}
HIGH_RISK_TRANSACTION_TYPES = {
    "OFFSHORE_AI_SERVICE_FEE",
    "IP_ROYALTY_OR_PLATFORM_LICENSE",
    "CLOUD_INFERENCE_RELABELLED_AS_ORDINARY_COST",
    "ROBOTICS_LEASE_OR_SERVICE_CONTRACT",
    "DATA_ACCESS_OR_MODEL_LICENSE_FEE",
}


@dataclass(frozen=True)
class RelatedPartyTransaction:
    """Related-party or offshore automation transaction used for preview review."""

    transaction_id: str
    transaction_type: str
    counterparty_role: str
    amount: float
    australian_nexus: str
    automation_nexus_score: float
    evidence_basis: str
    placeholder_basis: list[str] = field(default_factory=list)
    flags: list[str] = field(default_factory=list)
    review_share: float | None = None


@dataclass(frozen=True)
class AdjustmentCandidate:
    """Non-operative addback candidate for review."""

    transaction_id: str
    transaction_type: str
    amount: float
    review_share: float
    preview_addback_amount: float
    reason: str
    confidence: str
    non_legal_status: str = NON_OPERATIVE_STATUS


@dataclass(frozen=True)
class TransferPricingPreviewResult:
    """Transfer-pricing / related-party preview output."""

    reported_aava: float
    preview_adjustments_total: float
    adjusted_aava_preview: float
    candidates: list[AdjustmentCandidate] = field(default_factory=list)
    risk_level: str = "low"
    flags: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    review_required: bool = False
    placeholder_basis: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(TRANSFER_PRICING_NON_CLAIMS))


@dataclass(frozen=True)
class AdjustedAAVAPreview:
    """Preview-only adjusted AAVA summary."""

    reported_aava: float
    preview_adjustments_total: float
    adjusted_aava_preview: float
    difference: float
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(TRANSFER_PRICING_NON_CLAIMS))


@dataclass(frozen=True)
class LiabilityAdjustmentPreview:
    """Preview-only liability recomputation using adjusted AAVA."""

    original_final_liability: float
    adjusted_aava_liability_preview: float | None
    difference: float | None
    computable: bool
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(TRANSFER_PRICING_NON_CLAIMS))


def _finite_number(value: float, field_name: str) -> float:
    numeric = float(value)
    if not isfinite(numeric):
        raise ValueError(f"{field_name} must be finite")
    return numeric


def _bounded_share(value: float, field_name: str) -> float:
    numeric = _finite_number(value, field_name)
    if not 0 <= numeric <= 1:
        raise ValueError(f"{field_name} must be between 0 and 1")
    return numeric


def _transactions(source: dict[str, Any]) -> list[RelatedPartyTransaction]:
    raw = source.get("related_party_transactions", source.get("transactions", []))
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError("related_party_transactions must be a list")

    transactions: list[RelatedPartyTransaction] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"related_party_transactions[{index}] must be a mapping")
        amount = _finite_number(item.get("amount", 0.0), f"transaction {index} amount")
        if amount < 0:
            raise ValueError(f"transaction {index} amount cannot be negative")
        nexus_score = _bounded_share(item.get("automation_nexus_score", 0.0), f"transaction {index} automation_nexus_score")
        review_share = item.get("review_share")
        transactions.append(
            RelatedPartyTransaction(
                transaction_id=str(item.get("transaction_id", f"transaction_{index + 1}")),
                transaction_type=str(item.get("transaction_type", "OTHER_RELATED_PARTY_AUTOMATION_COST")),
                counterparty_role=str(item.get("counterparty_role", "")),
                amount=amount,
                australian_nexus=str(item.get("australian_nexus", "")),
                automation_nexus_score=nexus_score,
                evidence_basis=str(item.get("evidence_basis", "")),
                placeholder_basis=[str(value) for value in item.get("placeholder_basis", [])],
                flags=[str(value) for value in item.get("flags", [])],
                review_share=None if review_share is None else _bounded_share(review_share, f"transaction {index} review_share"),
            )
        )
    return transactions


def _revenue(source: dict[str, Any]) -> float:
    if "revenue" in source:
        return _finite_number(source["revenue"], "revenue")
    if "reported_revenue" in source:
        return _finite_number(source["reported_revenue"], "reported_revenue")
    if "aava_inputs" in source and isinstance(source["aava_inputs"], dict):
        return _finite_number(source["aava_inputs"].get("australian_attributable_revenue", 0.0), "australian_attributable_revenue")
    entities = source.get("entities")
    if isinstance(entities, list):
        return sum(_finite_number(entity.get("revenue", 0.0), "entity revenue") for entity in entities if isinstance(entity, dict))
    return 0.0


def _metadata_flags(source: dict[str, Any]) -> list[str]:
    flags: list[str] = []
    metadata = source.get("risk_metadata", {})
    if isinstance(metadata, dict):
        if metadata.get("related_party_ai_service_fees"):
            flags.append("RELATED_PARTY_AI_SERVICE_FEES")
        if metadata.get("offshore_automation_service"):
            flags.append("OFFSHORE_AUTOMATION_SERVICE")
        if metadata.get("cloud_cost_relabeling_risk"):
            flags.append("CLOUD_COST_RELABELING")
        if metadata.get("robotics_leasing_risk"):
            flags.append("ROBOTICS_LEASING_AVOIDANCE")
    return flags


def _candidate_reason(transaction: RelatedPartyTransaction) -> str:
    if transaction.transaction_type == "OFFSHORE_AI_SERVICE_FEE":
        return "Offshore AI service fee may suppress reported AAVA where automated capacity serves Australian output."
    if transaction.transaction_type == "IP_ROYALTY_OR_PLATFORM_LICENSE":
        return "IP or platform licence fee may extract automated value through a related counterparty."
    if transaction.transaction_type == "CLOUD_INFERENCE_RELABELLED_AS_ORDINARY_COST":
        return "Cloud or inference costs may be relabelled as ordinary non-automation inputs."
    if transaction.transaction_type == "ROBOTICS_LEASE_OR_SERVICE_CONTRACT":
        return "Robotics lease or service contract may keep capital base low while shifting automation costs."
    return "Related-party automation-linked charge requires AAVA deductibility and transfer-pricing review."


def _confidence(transaction: RelatedPartyTransaction, amount_ratio: float) -> str:
    if transaction.automation_nexus_score >= 0.75 and amount_ratio >= 0.20:
        return "high"
    if transaction.automation_nexus_score >= 0.40 or amount_ratio >= 0.10:
        return "medium"
    return "low"


def _should_candidate(transaction: RelatedPartyTransaction) -> bool:
    if transaction.review_share is not None and transaction.review_share > 0:
        return True
    if transaction.transaction_type in HIGH_RISK_TRANSACTION_TYPES:
        return True
    if transaction.automation_nexus_score >= 0.35:
        return True
    return bool({"related_party", "offshore", "automation"} & {flag.lower() for flag in transaction.flags})


def evaluate_transfer_pricing_preview(
    example_or_group: dict[str, Any],
    reported_aava: float,
) -> TransferPricingPreviewResult:
    """Evaluate non-operative related-party adjustment preview candidates."""

    reported = _finite_number(reported_aava, "reported_aava")
    transactions = _transactions(example_or_group)
    revenue = _revenue(example_or_group)
    warnings = [NON_OPERATIVE_STATUS]
    placeholder_basis = [
        "Transfer-pricing preview values are illustrative placeholders only.",
        "No OECD, BEPS, ATO, Treasury, legal, tax, or economic validation is implied.",
        str(example_or_group.get("placeholder_notice", "No placeholder notice supplied.")),
    ]
    flags = _metadata_flags(example_or_group)
    candidates: list[AdjustmentCandidate] = []

    if not transactions and flags:
        warnings.append("Risk metadata flags related-party/offshore risk, but no transaction data was supplied.")

    for transaction in transactions:
        if transaction.transaction_type not in SUPPORTED_TRANSACTION_TYPES:
            warnings.append(f"Unsupported prototype transaction type was treated as review-only: {transaction.transaction_type}")
        if transaction.flags:
            for flag in transaction.flags:
                if flag not in flags:
                    flags.append(flag)
        if transaction.transaction_type in HIGH_RISK_TRANSACTION_TYPES and transaction.transaction_type not in flags:
            flags.append(transaction.transaction_type)
        if not _should_candidate(transaction):
            continue
        review_share = transaction.review_share
        if review_share is None:
            review_share = min(1.0, max(0.0, transaction.automation_nexus_score))
        amount_ratio = transaction.amount / revenue if revenue > 0 else 0.0
        addback = _finite_number(transaction.amount * review_share, f"{transaction.transaction_id} preview_addback_amount")
        candidates.append(
            AdjustmentCandidate(
                transaction_id=transaction.transaction_id,
                transaction_type=transaction.transaction_type,
                amount=transaction.amount,
                review_share=review_share,
                preview_addback_amount=addback,
                reason=_candidate_reason(transaction),
                confidence=_confidence(transaction, amount_ratio),
            )
        )

    adjustments_total = _finite_number(sum(candidate.preview_addback_amount for candidate in candidates), "preview_adjustments_total")
    adjusted_aava = _finite_number(reported + adjustments_total, "adjusted_aava_preview")
    if len(candidates) >= 3 or any(candidate.confidence == "high" for candidate in candidates):
        risk_level = "high"
    elif candidates or flags:
        risk_level = "medium"
    else:
        risk_level = "low"

    return TransferPricingPreviewResult(
        reported_aava=reported,
        preview_adjustments_total=adjustments_total,
        adjusted_aava_preview=adjusted_aava,
        candidates=candidates,
        risk_level=risk_level,
        flags=flags,
        warnings=warnings,
        review_required=bool(candidates or flags),
        placeholder_basis=placeholder_basis,
    )


def preview_adjusted_aava(
    reported_aava: float,
    transfer_pricing_result: TransferPricingPreviewResult,
) -> AdjustedAAVAPreview:
    """Return a preview-only adjusted AAVA summary."""

    reported = _finite_number(reported_aava, "reported_aava")
    return AdjustedAAVAPreview(
        reported_aava=reported,
        preview_adjustments_total=transfer_pricing_result.preview_adjustments_total,
        adjusted_aava_preview=transfer_pricing_result.adjusted_aava_preview,
        difference=transfer_pricing_result.adjusted_aava_preview - reported,
        warnings=[
            NON_OPERATIVE_STATUS,
            "Adjusted AAVA is preview-only and does not mutate reported AAVA.",
        ],
    )


def _required_value_from_outputs(outputs: Any, name: str) -> float:
    if isinstance(outputs, dict):
        if name not in outputs:
            raise ValueError(f"missing required output for adjusted-AAVA liability preview: {name}")
        return _finite_number(outputs[name], name)
    if not hasattr(outputs, name):
        raise ValueError(f"missing required output for adjusted-AAVA liability preview: {name}")
    return _finite_number(getattr(outputs, name), name)


def _params_from_schedule(schedule: dict[str, Any]) -> LevyParameters | None:
    if "caps" not in schedule or "frv" not in schedule:
        return None
    caps = schedule["caps"]
    frv = schedule["frv"]
    return LevyParameters(
        frv_standard=float(frv["standard_placeholder"]),
        lambda_sector=float(caps["lambda_sector"]),
        lambda_combined=float(caps["LAMBDA_sector"]),
        theta=float(caps["theta"]),
        uplift_rate=float(caps["uplift_rate"]),
        rent_tax_rate=float(caps["rent_tax_rate"]),
    )


def preview_liability_with_adjusted_aava(
    existing_outputs: dict[str, Any] | Any,
    adjusted_aava_preview: float,
    schedule: dict[str, Any],
    capital_base: float | None = None,
    verified_credits: float | None = None,
) -> LiabilityAdjustmentPreview:
    """Preview liability using adjusted AAVA without changing original outputs."""

    adjusted_aava = _finite_number(adjusted_aava_preview, "adjusted_aava_preview")
    warnings = [NON_OPERATIVE_STATUS, "Adjusted-AAVA liability is non-operative preview only."]
    try:
        original_liability = _required_value_from_outputs(existing_outputs, "liability")
    except ValueError as exc:
        warnings.append(str(exc))
        return LiabilityAdjustmentPreview(
            original_final_liability=0.0,
            adjusted_aava_liability_preview=None,
            difference=None,
            computable=False,
            warnings=warnings,
        )
    params = _params_from_schedule(schedule)
    if params is None:
        warnings.append("Could not recompute liability preview because schedule caps/FRV were missing.")
        return LiabilityAdjustmentPreview(
            original_final_liability=original_liability,
            adjusted_aava_liability_preview=None,
            difference=None,
            computable=False,
            warnings=warnings,
        )
    try:
        nltg = _required_value_from_outputs(existing_outputs, "nltg")
        if capital_base is None:
            capital_base = _required_value_from_outputs(existing_outputs, "capital_base")
        if verified_credits is None:
            verified_credits = _required_value_from_outputs(existing_outputs, "verified_credits")
    except ValueError as exc:
        warnings.append(str(exc))
        return LiabilityAdjustmentPreview(
            original_final_liability=original_liability,
            adjusted_aava_liability_preview=None,
            difference=None,
            computable=False,
            warnings=warnings,
        )
    liability = calculate_liability(
        nltg=nltg,
        aava=adjusted_aava,
        capital_base=_finite_number(capital_base, "capital_base"),
        verified_credits=_finite_number(verified_credits, "verified_credits"),
        params=params,
    ).liability
    return LiabilityAdjustmentPreview(
        original_final_liability=original_liability,
        adjusted_aava_liability_preview=liability,
        difference=liability - original_liability,
        computable=True,
        warnings=warnings,
    )
