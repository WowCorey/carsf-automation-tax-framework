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
