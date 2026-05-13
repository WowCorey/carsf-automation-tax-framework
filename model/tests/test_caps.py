from carsf import LevyParameters
from carsf.levy import calculate_liability


def test_combined_liability_is_capped_by_lambda_sector_aava() -> None:
    result = calculate_liability(
        nltg=50,
        aava=100000,
        capital_base=0,
        verified_credits=0,
        params=LevyParameters(
            frv_standard=100000,
            lambda_sector=1,
            lambda_combined=0.25,
            theta=0.6,
            uplift_rate=1.0,
            rent_tax_rate=1.0,
        ),
    )

    assert result.combined_liability > 25000
    assert result.liability == 25000


def test_ael_and_combined_caps_zero_out_when_aava_is_zero() -> None:
    result = calculate_liability(
        nltg=25,
        aava=0,
        capital_base=0,
        verified_credits=0,
        params=LevyParameters(
            frv_standard=100000,
            lambda_sector=0.5,
            lambda_combined=0.5,
            theta=0.6,
            uplift_rate=1.0,
            rent_tax_rate=0.5,
        ),
    )

    assert result.ael_raw == 2500000
    assert result.ael_payable == 0
    assert result.arl == 0
    assert result.liability == 0


def test_ael_and_combined_caps_zero_out_when_aava_is_negative() -> None:
    result = calculate_liability(
        nltg=25,
        aava=-100000,
        capital_base=0,
        verified_credits=0,
        params=LevyParameters(
            frv_standard=100000,
            lambda_sector=0.5,
            lambda_combined=0.5,
            theta=0.6,
            uplift_rate=1.0,
            rent_tax_rate=0.5,
        ),
    )

    assert result.ael_raw == 2500000
    assert result.ael_payable == 0
    assert result.arl == 0
    assert result.liability == 0
