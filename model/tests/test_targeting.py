from __future__ import annotations

import pytest

from carsf.targeting import evaluate_target_population


def _target(**overrides):
    data = {
        "total_population": 1000,
        "displaced_workers": 200,
        "reabsorbed_workers": 50,
        "retraining_participants": 100,
        "existing_support_recipients": 80,
        "counts_may_overlap": False,
        "criteria": {
            "criteria_id": "direct",
            "target_group": "direct displaced workers",
            "displaced_worker_required": True,
            "retraining_required": False,
            "income_test_placeholder": False,
            "household_test_placeholder": False,
            "recent_employment_link_required": True,
            "automation_displacement_link_required": True,
            "exclusion_rules": [],
            "illustrative_placeholder_only": True,
        },
    }
    data.update(overrides)
    return data


def test_targeting_rejects_negative_populations() -> None:
    with pytest.raises(ValueError):
        evaluate_target_population(_target(displaced_workers=-1))


def test_targeting_prevents_component_counts_exceeding_total_without_overlap_label() -> None:
    with pytest.raises(ValueError):
        evaluate_target_population(_target(displaced_workers=1200))


def test_targeting_eligible_people_do_not_exceed_total_population() -> None:
    result = evaluate_target_population(
        _target(
            counts_may_overlap=True,
            displaced_workers=1200,
            reabsorbed_workers=0,
        )
    )

    assert result.estimated_eligible_people <= 1000


def test_targeting_risk_rises_when_link_is_weak_and_tests_unresolved() -> None:
    strong = evaluate_target_population(_target())
    weak = evaluate_target_population(
        _target(
            criteria={
                "criteria_id": "weak",
                "target_group": "broad placeholder",
                "displaced_worker_required": False,
                "retraining_required": True,
                "income_test_placeholder": True,
                "household_test_placeholder": True,
                "recent_employment_link_required": False,
                "automation_displacement_link_required": False,
                "exclusion_rules": [],
                "illustrative_placeholder_only": True,
            }
        )
    )

    ordering = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    assert ordering[weak.targeting_risk_band] > ordering[strong.targeting_risk_band]
