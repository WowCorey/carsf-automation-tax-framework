from __future__ import annotations

import math

import pytest

from carsf.sensitivity import sweep_aava, sweep_liability_cap, sweep_pass_through


def test_sensitivity_sweeps_reject_invalid_values() -> None:
    with pytest.raises(ValueError):
        sweep_pass_through(-1, [0.1])
    with pytest.raises(ValueError):
        sweep_pass_through(100, [math.inf])
    with pytest.raises(ValueError):
        sweep_liability_cap(100, 100, [1.2])
    with pytest.raises(ValueError):
        sweep_aava(100, [-1])


def test_sensitivity_sweeps_produce_deterministic_points() -> None:
    first = sweep_liability_cap(1000, 500, [0.1, 0.2], example_id="case").to_jsonable()
    second = sweep_liability_cap(1000, 500, [0.1, 0.2], example_id="case").to_jsonable()

    assert first == second
    assert first["points"][0]["liability_preview"] == 100
    assert first["points"][1]["liability_preview"] == 200
