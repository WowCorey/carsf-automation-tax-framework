from math import inf, nan

import pytest

from carsf import LevyParameters
from carsf.levy import (
    automation_equilibrium_levy,
    automation_rent_levy,
    calculate_liability,
)


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


@pytest.mark.parametrize("bad_value", [nan, inf, -inf])
@pytest.mark.parametrize("field", ["nltg", "frv_standard", "aava"])
def test_automation_equilibrium_levy_rejects_nan_and_infinity(
    field: str,
    bad_value: float,
) -> None:
    inputs = {
        "nltg": 10.0,
        "frv_standard": 50000.0,
        "lambda_sector": 0.2,
        "aava": 100000.0,
    }
    inputs[field] = bad_value

    with pytest.raises(ValueError):
        automation_equilibrium_levy(**inputs)


@pytest.mark.parametrize("bad_value", [nan, inf, -inf])
@pytest.mark.parametrize("field", ["aava", "uplift_rate", "capital_base", "rent_tax_rate"])
def test_automation_rent_levy_rejects_nan_and_infinity(
    field: str,
    bad_value: float,
) -> None:
    inputs = {
        "aava": 100000.0,
        "uplift_rate": 1.12,
        "capital_base": 50000.0,
        "rent_tax_rate": 0.2,
    }
    inputs[field] = bad_value

    with pytest.raises(ValueError):
        automation_rent_levy(**inputs)


@pytest.mark.parametrize("bad_value", [nan, inf, -inf])
@pytest.mark.parametrize("field", ["nltg", "aava", "capital_base", "verified_credits"])
def test_calculate_liability_rejects_nan_and_infinity_direct_inputs(
    field: str,
    bad_value: float,
) -> None:
    inputs = {
        "nltg": 1.0,
        "aava": 100000.0,
        "capital_base": 50000.0,
        "verified_credits": 0.0,
    }
    inputs[field] = bad_value

    with pytest.raises(ValueError):
        calculate_liability(
            **inputs,
            params=LevyParameters(
                frv_standard=50000.0,
                lambda_sector=0.2,
                lambda_combined=0.25,
                theta=0.6,
                uplift_rate=1.12,
                rent_tax_rate=0.2,
            ),
        )


@pytest.mark.parametrize("bad_value", [nan, inf, -inf])
@pytest.mark.parametrize(
    "field",
    [
        "frv_standard",
        "lambda_sector",
        "lambda_combined",
        "theta",
        "uplift_rate",
        "rent_tax_rate",
    ],
)
def test_calculate_liability_rejects_nan_and_infinity_parameter_inputs(
    field: str,
    bad_value: float,
) -> None:
    params = {
        "frv_standard": 50000.0,
        "lambda_sector": 0.2,
        "lambda_combined": 0.25,
        "theta": 0.6,
        "uplift_rate": 1.12,
        "rent_tax_rate": 0.2,
    }
    params[field] = bad_value

    with pytest.raises(ValueError):
        calculate_liability(
            nltg=1.0,
            aava=100000.0,
            capital_base=50000.0,
            verified_credits=0.0,
            params=LevyParameters(**params),
        )


def test_automation_equilibrium_levy_rejects_overflowed_ael_raw() -> None:
    with pytest.raises(ValueError):
        automation_equilibrium_levy(
            nltg=1e308,
            frv_standard=1e308,
            lambda_sector=0.2,
            aava=100000.0,
        )


def test_automation_rent_levy_rejects_overflowed_uplifted_capital_base() -> None:
    with pytest.raises(ValueError):
        automation_rent_levy(
            aava=100000.0,
            uplift_rate=1e308,
            capital_base=1e308,
            rent_tax_rate=0.2,
        )
