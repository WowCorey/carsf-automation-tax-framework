from __future__ import annotations

import pytest

from carsf.support_incidence import evaluate_support_incidence


def _assumption(**overrides):
    data = {
        "household_spend_share": 0.7,
        "gst_recovery_rate_placeholder": 0.04,
        "hardship_offset_rate_placeholder": 0.1,
        "savings_or_debt_repayment_share": 0.2,
        "illustrative_placeholder_only": True,
    }
    data.update(overrides)
    return data


def test_support_incidence_rejects_invalid_rates() -> None:
    with pytest.raises(ValueError):
        evaluate_support_incidence(1000, _assumption(household_spend_share=1.2))
    with pytest.raises(ValueError):
        evaluate_support_incidence(1000, _assumption(savings_or_debt_repayment_share=0.4))
    with pytest.raises(ValueError):
        evaluate_support_incidence(-1, _assumption())


def test_support_incidence_does_not_treat_offsets_as_validated_savings() -> None:
    result = evaluate_support_incidence(1000, _assumption())

    assert result.household_spending_flow == 700
    assert result.placeholder_gst_recovery == 28
    assert result.hardship_offset_preview == 100
    assert result.net_fiscal_cost_after_placeholder_offsets == 872
    assert any("not validated savings" in warning for warning in result.warnings)
