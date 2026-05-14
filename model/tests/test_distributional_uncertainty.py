from __future__ import annotations

from carsf.distributional_uncertainty import evaluate_household_uncertainty


def _range(range_id: str, metric: str, low: float, base: float, high: float):
    return {
        "range_id": range_id,
        "metric_name": metric,
        "low": low,
        "base": base,
        "high": high,
        "confidence_placeholder": "low_placeholder_confidence_not_statistical",
        "calibration_status": "not_calibrated",
        "uncertainty_drivers": [metric],
        "illustrative_placeholder_only": True,
        "placeholder_basis": ["synthetic placeholder range"],
    }


def _input(residual_range, shock_band="high", **overrides):
    payload = {
        "uncertainty_id": "household_uncertainty_test",
        "scenario_result": {
            "scenario_id": "scenario_a",
            "household_id": "household_a",
            "household_shock_band": shock_band,
        },
        "residual_gap_range": residual_range,
        "transition_support_range": _range("support", "transition_support_amount", 10_000, 12_000, 14_000),
        "placeholder_basis": ["unit test"],
    }
    payload.update(overrides)
    return payload


def test_household_uncertainty_returns_stable_high_risk_when_all_cases_high_or_critical() -> None:
    result = evaluate_household_uncertainty(
        _input(_range("residual", "residual_household_gap_after_support", 8_000, 14_000, 22_000), shock_band="high")
    )

    assert result.low_case_shock_band in {"high", "critical"}
    assert result.base_case_shock_band in {"high", "critical"}
    assert result.high_case_shock_band in {"high", "critical"}
    assert result.risk_signal_stability == "stable_high_risk"


def test_household_uncertainty_returns_range_sensitive_when_cases_cross_bands() -> None:
    result = evaluate_household_uncertainty(
        _input(_range("residual", "residual_household_gap_after_support", 0, 4_500, 22_000), shock_band="medium")
    )

    assert result.low_case_shock_band == "low"
    assert result.high_case_shock_band in {"high", "critical"}
    assert result.risk_signal_stability == "range_sensitive"
    assert any("too fragile" in warning for warning in result.warnings)


def test_household_uncertainty_preserves_non_claims_and_liability_warning() -> None:
    result = evaluate_household_uncertainty(
        _input(_range("residual", "residual_household_gap_after_support", 0, 0, 3_000), shock_band="low")
    )

    assert any("not statistical confidence" in claim for claim in result.non_claims)
    assert any("Firm-level CARSF liability is not modified" in warning for warning in result.warnings)
