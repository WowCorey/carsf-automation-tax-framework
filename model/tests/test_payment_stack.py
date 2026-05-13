from __future__ import annotations

import pytest

from carsf.payment_stack import evaluate_payment_stack


def test_payment_stack_rejects_invalid_values() -> None:
    with pytest.raises(ValueError):
        evaluate_payment_stack(
            "bad",
            [
                {
                    "component_id": "bad_component",
                    "component_type": "SUPPLEMENT",
                    "eligible_people": -1,
                    "payment_per_person": 1000,
                    "stack_priority": 1,
                    "phase_multiplier": 1.0,
                }
            ],
        )
    with pytest.raises(ValueError):
        evaluate_payment_stack(
            "bad",
            [
                {
                    "component_id": "bad_component",
                    "component_type": "SUPPLEMENT",
                    "eligible_people": 10,
                    "payment_per_person": 1000,
                    "stack_priority": 1,
                    "phase_multiplier": 1.5,
                }
            ],
        )


def test_payment_stack_applies_phase_multiplier() -> None:
    result = evaluate_payment_stack(
        "phase",
        [
            {
                "component_id": "supplement",
                "component_type": "SUPPLEMENT",
                "eligible_people": 100,
                "payment_per_person": 1000,
                "stack_priority": 1,
                "phase_multiplier": 0.5,
            }
        ],
    )

    assert result.gross_cost_before_interactions == 50000
    assert result.net_cost_after_interactions == 50000


def test_payment_stack_calculates_double_count_adjustment_for_mutual_exclusion() -> None:
    result = evaluate_payment_stack(
        "double",
        [
            {
                "component_id": "supplement",
                "component_type": "SUPPLEMENT",
                "eligible_people": 100,
                "payment_per_person": 1000,
                "stack_priority": 1,
                "mutually_exclusive_with": ["grant"],
                "phase_multiplier": 1.0,
            },
            {
                "component_id": "grant",
                "component_type": "GRANT",
                "eligible_people": 80,
                "payment_per_person": 500,
                "stack_priority": 2,
                "mutually_exclusive_with": ["supplement"],
                "phase_multiplier": 1.0,
            },
        ],
    )

    assert result.gross_cost_before_interactions == 140000
    assert result.people_double_counted_preview == 80
    assert result.double_count_adjustment == 40000
    assert result.net_cost_after_interactions == 100000
