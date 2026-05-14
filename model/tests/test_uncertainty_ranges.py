from __future__ import annotations

import math

import pytest

from carsf.uncertainty_ranges import evaluate_uncertainty_range


def _range(**overrides):
    payload = {
        "range_id": "test_range",
        "metric_name": "residual_gap",
        "low": 80.0,
        "base": 100.0,
        "high": 120.0,
        "confidence_placeholder": "low_placeholder_confidence_not_statistical",
        "calibration_status": "not_calibrated",
        "uncertainty_drivers": ["unit test"],
        "illustrative_placeholder_only": True,
        "placeholder_basis": ["synthetic placeholder"],
    }
    payload.update(overrides)
    return payload


@pytest.mark.parametrize("field", ["low", "base", "high"])
@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_uncertainty_range_rejects_non_finite_values(field, value) -> None:
    payload = _range()
    payload[field] = value
    with pytest.raises(ValueError, match="must be finite"):
        evaluate_uncertainty_range(payload)


def test_uncertainty_range_rejects_negative_values_unless_signed_allowed() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        evaluate_uncertainty_range(_range(low=-1.0, base=0.0, high=1.0))

    result = evaluate_uncertainty_range(
        _range(low=-1.0, base=0.0, high=1.0, placeholder_basis=["allow_signed synthetic metric"])
    )
    assert result.low == -1.0


@pytest.mark.parametrize("payload", [_range(low=101.0, base=100.0, high=120.0), _range(low=80.0, base=130.0, high=120.0)])
def test_uncertainty_range_rejects_unordered_values(payload) -> None:
    with pytest.raises(ValueError, match="low <= base <= high"):
        evaluate_uncertainty_range(payload)


def test_uncertainty_range_widths_calculate_correctly() -> None:
    result = evaluate_uncertainty_range(_range(low=80.0, base=100.0, high=120.0))

    assert result.absolute_range_width == pytest.approx(40.0)
    assert result.relative_range_width == pytest.approx(0.4)
    assert result.ordered_correctly is True


def test_uncertainty_range_stability_responds_to_width() -> None:
    stable = evaluate_uncertainty_range(_range(low=95.0, base=100.0, high=105.0))
    moderate = evaluate_uncertainty_range(_range(low=80.0, base=100.0, high=120.0))
    fragile = evaluate_uncertainty_range(_range(low=0.0, base=100.0, high=220.0))

    assert stable.stability_band == "stable"
    assert moderate.stability_band == "moderately_sensitive"
    assert fragile.stability_band == "fragile"
