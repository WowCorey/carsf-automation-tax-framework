"""Qualified Labour Contribution formula."""

from __future__ import annotations

from collections.abc import Iterable
from math import isfinite

from .types import QLCWeights, Worker


def _bounded_unit(value: float, field_name: str) -> float:
    """Clamp placeholder scores into [0, 1] while preserving a validation hook."""

    numeric = float(value)
    if not isfinite(numeric):
        raise ValueError(f"{field_name} must be finite")
    return max(0.0, min(1.0, numeric))


def _validate_weights(weights: QLCWeights) -> None:
    values = [float(weights.alpha), float(weights.beta), float(weights.gamma), float(weights.delta)]
    if any(not isfinite(weight) for weight in values):
        raise ValueError("QLC weights must be finite")
    if any(weight < 0 for weight in values):
        raise ValueError("QLC weights cannot be negative")
    if not isfinite(float(weights.qlc_max_multiplier)):
        raise ValueError("qlc_max_multiplier must be finite")


def qualified_labour_contribution_worker(
    worker: Worker,
    weights: QLCWeights | None = None,
) -> float:
    """Calculate capped QLC for one worker.

    QLC_worker = min(
        FTE_worker * (1 + alpha*WQ + beta*JS + gamma*SD + delta*AN),
        FTE_worker * QLCMaxMultiplier
    )
    """

    weights = weights or QLCWeights()
    if worker.full_time_hours <= 0:
        raise ValueError("full_time_hours must be positive")
    if worker.annual_hours < 0:
        raise ValueError("annual_hours cannot be negative")
    if not isfinite(float(worker.annual_hours)) or not isfinite(float(worker.full_time_hours)):
        raise ValueError("worker hours must be finite")
    if weights.qlc_max_multiplier < 1:
        raise ValueError("qlc_max_multiplier must be at least 1")
    _validate_weights(weights)

    fte = worker.annual_hours / worker.full_time_hours
    multiplier = 1.0 + (
        weights.alpha * _bounded_unit(worker.wage_quality, "wage_quality")
        + weights.beta * _bounded_unit(worker.job_security, "job_security")
        + weights.gamma * _bounded_unit(worker.skill_development, "skill_development")
        + weights.delta * _bounded_unit(worker.australian_nexus, "australian_nexus")
    )
    return min(fte * multiplier, fte * weights.qlc_max_multiplier)


def qualified_labour_contribution_firm(
    workers: Iterable[Worker],
    weights: QLCWeights | None = None,
) -> float:
    """Sum capped worker-level QLC across a firm."""

    return sum(qualified_labour_contribution_worker(worker, weights) for worker in workers)
