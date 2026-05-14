from __future__ import annotations

from carsf.distributional_scenarios import evaluate_distributional_scenario


SEVERITY = {"low": 0, "medium": 1, "high": 2, "critical": 3}


def _scenario(**overrides):
    data = {
        "scenario_id": "scenario_test",
        "household": {
            "household_id": "hh_test",
            "household_type": "single_adult",
            "adults": 1,
            "children": 0,
            "region_type": "placeholder_region",
            "income_band": "middle_placeholder",
            "pre_displacement_income": 70000,
            "post_displacement_income": 20000,
            "existing_support_baseline": 5000,
            "housing_cost_placeholder": 20000,
            "essential_cost_placeholder": 18000,
            "debt_pressure_placeholder": 2000,
            "savings_buffer_placeholder": 1000,
            "illustrative_placeholder_only": True,
            "synthetic_household_only": True,
        },
        "reemployment_path": {
            "path_id": "reemployment_test",
            "household_id": "hh_test",
            "displacement_year": 2028,
            "expected_reemployment_months": 12,
            "retraining_months": 6,
            "partial_income_recovery_rate": 0.3,
            "full_income_recovery_rate": 0.7,
            "illustrative_placeholder_only": True,
        },
        "regional_stress": {
            "region_id": "region_test",
            "region_type": "placeholder_region",
            "automation_exposure_placeholder": 0.5,
            "labour_market_depth_placeholder": 0.5,
            "retraining_access_placeholder": 0.5,
            "housing_cost_pressure_placeholder": 0.5,
            "transport_access_placeholder": 0.5,
            "illustrative_placeholder_only": True,
        },
        "payment_cliff": None,
        "transition_support_amount": 10000,
    }
    data.update(overrides)
    return data


def test_distributional_scenario_calculates_residual_household_gap_after_support() -> None:
    result = evaluate_distributional_scenario(_scenario(transition_support_amount=7000))

    assert result.residual_household_gap_after_support == 8000
    assert result.transition_support_amount == 7000


def test_distributional_shock_band_rises_with_critical_budget_and_long_reemployment() -> None:
    low = evaluate_distributional_scenario(
        _scenario(
            household={
                "household_id": "hh_test",
                "household_type": "single_adult",
                "adults": 1,
                "children": 0,
                "region_type": "placeholder_region",
                "income_band": "middle_placeholder",
                "pre_displacement_income": 50000,
                "post_displacement_income": 45000,
                "existing_support_baseline": 0,
                "housing_cost_placeholder": 15000,
                "essential_cost_placeholder": 12000,
                "debt_pressure_placeholder": 0,
                "savings_buffer_placeholder": 20000,
                "illustrative_placeholder_only": True,
                "synthetic_household_only": True,
            },
            reemployment_path={
                "path_id": "quick",
                "household_id": "hh_test",
                "displacement_year": 2028,
                "expected_reemployment_months": 1,
                "retraining_months": 0,
                "partial_income_recovery_rate": 0.9,
                "full_income_recovery_rate": 1.0,
                "illustrative_placeholder_only": True,
            },
            transition_support_amount=0,
        )
    )
    high = evaluate_distributional_scenario(
        _scenario(
            reemployment_path={
                "path_id": "slow",
                "household_id": "hh_test",
                "displacement_year": 2028,
                "expected_reemployment_months": 24,
                "retraining_months": 12,
                "partial_income_recovery_rate": 0.1,
                "full_income_recovery_rate": 0.4,
                "illustrative_placeholder_only": True,
            },
            regional_stress={
                "region_id": "region_test",
                "region_type": "placeholder_region",
                "automation_exposure_placeholder": 0.9,
                "labour_market_depth_placeholder": 0.1,
                "retraining_access_placeholder": 0.2,
                "housing_cost_pressure_placeholder": 0.9,
                "transport_access_placeholder": 0.2,
                "illustrative_placeholder_only": True,
            },
            payment_cliff={
                "cliff_id": "cliff_test",
                "household_id": "hh_test",
                "support_before_change": 10000,
                "support_after_change": 1000,
                "income_before_change": 20000,
                "income_after_change": 22000,
                "trigger_type": "placeholder",
                "trigger_description": "placeholder",
            },
            transition_support_amount=0,
        )
    )

    assert SEVERITY[high.household_shock_band] > SEVERITY[low.household_shock_band]
    assert "residual household gap after support" in high.primary_risk_drivers
