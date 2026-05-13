from __future__ import annotations

import math

import pytest

from carsf.transfer_baseline import evaluate_existing_transfer_baseline


def _baseline(**overrides):
    data = {
        "baseline_id": "baseline_test",
        "eligible_population": 100,
        "average_existing_support_per_person": 1000,
        "existing_admin_cost_per_person": 100,
        "baseline_program_type": "placeholder",
        "illustrative_placeholder_only": True,
    }
    data.update(overrides)
    return data


def test_existing_transfer_baseline_rejects_invalid_values() -> None:
    for field in ["eligible_population", "average_existing_support_per_person", "existing_admin_cost_per_person"]:
        with pytest.raises(ValueError):
            evaluate_existing_transfer_baseline(_baseline(**{field: -1}))
        with pytest.raises(ValueError):
            evaluate_existing_transfer_baseline(_baseline(**{field: math.inf}))


def test_existing_transfer_baseline_calculates_separate_cost() -> None:
    result = evaluate_existing_transfer_baseline(_baseline())

    assert result.existing_support_cost == 100000
    assert result.existing_admin_cost == 10000
    assert result.total_existing_baseline_cost == 110000
    assert "not UBI policy" in result.non_claims[0]
