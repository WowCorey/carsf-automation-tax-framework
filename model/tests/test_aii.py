import pytest
from math import inf

from carsf import AIIWeights, automation_intensity_index


def test_aii_is_bounded_between_zero_and_one() -> None:
    value = automation_intensity_index(
        compute_ratio=-10,
        auto_decision_ratio=2,
        robotics_capital_ratio=0.5,
        auto_process_share=3,
    )

    assert 0 <= value <= 1


def test_aii_weights_must_sum_to_one() -> None:
    with pytest.raises(ValueError):
        automation_intensity_index(
            compute_ratio=0.1,
            auto_decision_ratio=0.1,
            robotics_capital_ratio=0.1,
            auto_process_share=0.1,
            weights=AIIWeights(0.5, 0.5, 0.5, 0.5),
        )


def test_aii_rejects_non_finite_components() -> None:
    with pytest.raises(ValueError):
        automation_intensity_index(
            compute_ratio=inf,
            auto_decision_ratio=0.1,
            robotics_capital_ratio=0.1,
            auto_process_share=0.1,
        )
