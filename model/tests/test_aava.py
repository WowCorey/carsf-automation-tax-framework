from carsf import australian_automated_value_added
from carsf import LevyParameters
from carsf.levy import calculate_liability


def test_aava_subtracts_verified_costs() -> None:
    assert australian_automated_value_added(1000, 300, 200) == 500


def test_aava_can_be_zero_without_creating_liability_capacity() -> None:
    assert australian_automated_value_added(1000, 500, 500) == 0


def test_negative_aava_result_is_safe_for_caps() -> None:
    aava = australian_automated_value_added(1000, 800, 400)
    result = calculate_liability(
        nltg=10,
        aava=aava,
        capital_base=1000,
        verified_credits=100,
        params=LevyParameters(
            frv_standard=50000,
            lambda_sector=0.2,
            lambda_combined=0.25,
            theta=0.6,
            uplift_rate=1.12,
            rent_tax_rate=0.2,
        ),
    )

    assert aava == -200
    assert result.ael_payable == 0
    assert result.arl == 0
    assert result.credits == 0
    assert result.liability == 0
