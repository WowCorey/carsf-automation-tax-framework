from carsf import LevyParameters
from carsf.levy import automation_equilibrium_levy, calculate_liability


def test_ael_is_capped_by_lambda_sector_times_aava() -> None:
    raw, payable, shortfall = automation_equilibrium_levy(
        nltg=10,
        frv_standard=50000,
        lambda_sector=0.2,
        aava=100000,
    )

    assert raw == 500000
    assert payable == 20000
    assert shortfall == 480000


def test_credits_cannot_erase_beyond_theta_cap() -> None:
    result = calculate_liability(
        nltg=1,
        aava=1000000,
        capital_base=1000000,
        verified_credits=999999,
        params=LevyParameters(
            frv_standard=100000,
            lambda_sector=1,
            lambda_combined=1,
            theta=0.6,
            uplift_rate=10,
            rent_tax_rate=0.2,
        ),
    )

    assert result.credits == 60000
    assert result.liability == 40000
