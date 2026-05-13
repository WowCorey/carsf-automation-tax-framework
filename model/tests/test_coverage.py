from math import isfinite

from carsf import cars_i, coverage_measures, coverage_ratio, format_coverage_ratio


def test_coverage_ratio_handles_zero_damage_safely() -> None:
    assert coverage_ratio(automation_revenue_captured=0, national_automation_fiscal_damage=0) is None
    result = coverage_measures(0, 0)
    assert result.coverage_ratio is None
    assert format_coverage_ratio(result.coverage_ratio) == "N/A - no measured damage"


def test_cars_i_handles_zero_revenue_safely() -> None:
    value = cars_i(national_automation_fiscal_damage=1000, automation_revenue_captured=0)
    assert isfinite(value)
    assert value > 0
