from __future__ import annotations

from copy import deepcopy
from math import inf, nan

import pytest

from conftest import load_schedule, load_yaml

from carsf.transfer_pricing import evaluate_transfer_pricing_preview, preview_liability_with_adjusted_aava


def source_with_transactions(transactions: list[dict]) -> dict:
    return {
        "group_id": "test_structure",
        "placeholder_notice": "illustrative placeholder only",
        "reported_revenue": 1000000.0,
        "related_party_transactions": transactions,
    }


def transaction(**overrides) -> dict:
    base = {
        "transaction_id": "tx_1",
        "transaction_type": "OFFSHORE_AI_SERVICE_FEE",
        "counterparty_role": "related offshore AI provider",
        "amount": 100000.0,
        "australian_nexus": "Australian-facing automated output",
        "automation_nexus_score": 0.80,
        "review_share": 0.50,
        "evidence_basis": "illustrative placeholder ledger",
        "placeholder_basis": ["illustrative_placeholder_only"],
        "flags": ["related_party", "offshore", "automation"],
    }
    base.update(overrides)
    return base


@pytest.mark.parametrize("reported_aava", [nan, inf, -inf])
def test_transfer_pricing_preview_rejects_non_finite_reported_aava(reported_aava: float) -> None:
    with pytest.raises(ValueError, match="reported_aava must be finite"):
        evaluate_transfer_pricing_preview(source_with_transactions([]), reported_aava)


def test_transfer_pricing_preview_rejects_negative_transaction_amount() -> None:
    with pytest.raises(ValueError, match="cannot be negative"):
        evaluate_transfer_pricing_preview(source_with_transactions([transaction(amount=-1.0)]), 1000.0)


@pytest.mark.parametrize("amount", [nan, inf, -inf])
def test_transfer_pricing_preview_rejects_non_finite_transaction_amount(amount: float) -> None:
    with pytest.raises(ValueError, match="amount must be finite"):
        evaluate_transfer_pricing_preview(source_with_transactions([transaction(amount=amount)]), 1000.0)


@pytest.mark.parametrize("review_share", [-0.01, 1.01, nan, inf])
def test_review_share_must_be_between_zero_and_one(review_share: float) -> None:
    with pytest.raises(ValueError):
        evaluate_transfer_pricing_preview(source_with_transactions([transaction(review_share=review_share)]), 1000.0)


def test_adjusted_aava_preview_equals_reported_aava_plus_preview_adjustments() -> None:
    result = evaluate_transfer_pricing_preview(source_with_transactions([transaction(amount=200000.0, review_share=0.25)]), 1000.0)

    assert result.preview_adjustments_total == 50000.0
    assert result.adjusted_aava_preview == 51000.0


def test_adjustment_preview_does_not_mutate_reported_aava_or_source() -> None:
    source = source_with_transactions([transaction(amount=200000.0, review_share=0.25)])
    original = deepcopy(source)
    reported_aava = 1000.0

    result = evaluate_transfer_pricing_preview(source, reported_aava)

    assert source == original
    assert reported_aava == 1000.0
    assert result.reported_aava == 1000.0
    assert result.adjusted_aava_preview > result.reported_aava


@pytest.mark.parametrize(
    ("transaction_type", "expected"),
    [
        ("OFFSHORE_AI_SERVICE_FEE", "OFFSHORE_AI_SERVICE_FEE"),
        ("IP_ROYALTY_OR_PLATFORM_LICENSE", "IP_ROYALTY_OR_PLATFORM_LICENSE"),
        ("ROBOTICS_LEASE_OR_SERVICE_CONTRACT", "ROBOTICS_LEASE_OR_SERVICE_CONTRACT"),
    ],
)
def test_high_risk_transaction_types_produce_adjustment_candidates(transaction_type: str, expected: str) -> None:
    result = evaluate_transfer_pricing_preview(source_with_transactions([transaction(transaction_type=transaction_type)]), 1000.0)

    assert [candidate.transaction_type for candidate in result.candidates] == [expected]
    assert result.review_required is True


def test_related_party_fee_structure_adjusted_aava_exceeds_reported_aava(repo_root) -> None:
    source = load_yaml(repo_root / "examples" / "groups" / "related_party_ai_fee_structure.yaml")

    result = evaluate_transfer_pricing_preview(source, source["reported_aava"])

    assert result.adjusted_aava_preview > result.reported_aava
    assert len(result.candidates) >= 2
    assert result.risk_level == "high"


def test_adjusted_aava_liability_preview_fails_closed_without_required_outputs() -> None:
    result = preview_liability_with_adjusted_aava(
        {"liability": 0.0},
        100000.0,
        load_schedule("logistics_warehousing"),
    )

    assert result.computable is False
    assert result.adjusted_aava_liability_preview is None
    assert any("missing required output" in warning for warning in result.warnings)
