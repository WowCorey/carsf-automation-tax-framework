"""Automation Intensity Index formula."""

from __future__ import annotations

from math import isfinite

from .types import AIIWeights


def _bounded_unit(value: float, field_name: str) -> float:
    numeric = float(value)
    if not isfinite(numeric):
        raise ValueError(f"{field_name} must be finite")
    return max(0.0, min(1.0, numeric))


def _validate_weights(weights: AIIWeights) -> None:
    values = list(weights.as_mapping().values())
    if any(not isfinite(float(weight)) for weight in values):
        raise ValueError("AII weights must be finite")
    if any(weight < 0 for weight in values):
        raise ValueError("AII weights cannot be negative")
    if abs(sum(values) - 1.0) > 1e-9:
        raise ValueError("AII weights must sum to 1")


def automation_intensity_index(
    compute_ratio: float,
    auto_decision_ratio: float,
    robotics_capital_ratio: float,
    auto_process_share: float,
    weights: AIIWeights | None = None,
) -> float:
    """Calculate bounded AII.

    AII = w1*ComputeRatio + w2*AutoDecisionRatio
          + w3*RoboticsCapitalRatio + w4*AutoProcessShare
    """

    weights = weights or AIIWeights()
    _validate_weights(weights)
    result = (
        weights.compute_ratio * _bounded_unit(compute_ratio, "compute_ratio")
        + weights.auto_decision_ratio * _bounded_unit(auto_decision_ratio, "auto_decision_ratio")
        + weights.robotics_capital_ratio * _bounded_unit(robotics_capital_ratio, "robotics_capital_ratio")
        + weights.auto_process_share * _bounded_unit(auto_process_share, "auto_process_share")
    )
    return max(0.0, min(1.0, result))
