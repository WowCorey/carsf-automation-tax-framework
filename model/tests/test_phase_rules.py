from __future__ import annotations

import pytest

from carsf.phase_rules import evaluate_phase_rule


def _rule(**overrides):
    data = {
        "rule_id": "phase_test",
        "phase_in_start_year": 2026,
        "phase_in_end_year": 2028,
        "phase_out_start_year": 2030,
        "phase_out_end_year": 2032,
        "minimum_payment_multiplier": 0.25,
        "maximum_payment_multiplier": 1.0,
        "taper_rate_placeholder": 0.1,
        "illustrative_placeholder_only": True,
    }
    data.update(overrides)
    return data


def test_phase_rules_reject_invalid_years() -> None:
    with pytest.raises(ValueError):
        evaluate_phase_rule(_rule(phase_in_end_year=2025), 2026)
    with pytest.raises(ValueError):
        evaluate_phase_rule(_rule(phase_out_start_year=2032, phase_out_end_year=2031), 2026)
    with pytest.raises(ValueError):
        evaluate_phase_rule(_rule(), 2026.5)


def test_phase_rules_calculate_all_states() -> None:
    assert evaluate_phase_rule(_rule(), 2025).phase_status == "pre_phase_in"
    assert evaluate_phase_rule(_rule(), 2027).phase_status == "phase_in"
    assert evaluate_phase_rule(_rule(), 2029).phase_status == "full"
    assert evaluate_phase_rule(_rule(), 2031).phase_status == "phase_out"
    assert evaluate_phase_rule(_rule(), 2033).phase_status == "ended"


def test_phase_rules_apply_multiplier_bounds() -> None:
    phase_in = evaluate_phase_rule(_rule(), 2027)
    ended = evaluate_phase_rule(_rule(), 2033)

    assert 0 <= phase_in.payment_multiplier <= 1
    assert ended.payment_multiplier == 0
