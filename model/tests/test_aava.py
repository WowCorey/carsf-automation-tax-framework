from carsf import australian_automated_value_added


def test_aava_subtracts_verified_costs() -> None:
    assert australian_automated_value_added(1000, 300, 200) == 500
