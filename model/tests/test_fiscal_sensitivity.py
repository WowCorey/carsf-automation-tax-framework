from __future__ import annotations

import math

import pytest
import yaml

from carsf.fiscal_sensitivity import run_fiscal_sensitivity


def _base(repo_root) -> dict:
    return yaml.safe_load(
        (repo_root / "examples" / "fiscal_trajectory" / "baseline_placeholder_2026_2034.yaml").read_text(
            encoding="utf-8"
        )
    )


def test_fiscal_sensitivity_output_ordering_is_deterministic(repo_root) -> None:
    result = run_fiscal_sensitivity(
        _base(repo_root),
        {
            "annual_reabsorption_rate": [0.4, 0.2],
            "annual_displacement_rate": [0.02, 0.01],
        },
    )

    names_and_values = [(point.parameter_name, point.parameter_value) for point in result.points]
    assert names_and_values == [
        ("annual_displacement_rate", 0.01),
        ("annual_displacement_rate", 0.02),
        ("annual_reabsorption_rate", 0.2),
        ("annual_reabsorption_rate", 0.4),
    ]


@pytest.mark.parametrize("value", [math.nan, math.inf, -math.inf])
def test_fiscal_sensitivity_rejects_invalid_parameter_values(repo_root, value: float) -> None:
    with pytest.raises(ValueError, match="finite"):
        run_fiscal_sensitivity(_base(repo_root), {"annual_displacement_rate": [value]})


def test_fiscal_sensitivity_rejects_rates_outside_bounds(repo_root) -> None:
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        run_fiscal_sensitivity(_base(repo_root), {"annual_displacement_rate": [1.5]})


def test_fiscal_sensitivity_produces_gap_bounds(repo_root) -> None:
    result = run_fiscal_sensitivity(_base(repo_root), {"automation_revenue_capture_multiplier": [0.5, 1.0]})

    assert len(result.points) == 2
    assert result.min_gap <= result.max_gap
    assert result.non_claims
