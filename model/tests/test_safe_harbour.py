from __future__ import annotations

from copy import deepcopy

from conftest import load_example, load_schedule

from carsf.example_runner import run_example
from carsf.safe_harbour import (
    LOW_NLTG_EXCLUSION,
    NO_SAFE_HARBOUR_REVIEW,
    SMALL_BUSINESS_PLACEHOLDER,
    STARTUP_PLACEHOLDER,
    WORKER_ASSIST_OR_ADMIN_AI,
)


def result_for(example_id: str):
    example = load_example(example_id)
    schedule = load_schedule(example["schedule_used"])
    return run_example(example, schedule)


def test_traditional_mechanic_gets_low_risk_safe_harbour_treatment() -> None:
    result = result_for("mechanic_traditional")

    assert result.safe_harbour_result.eligible is True
    assert result.safe_harbour_result.category in {LOW_NLTG_EXCLUSION, SMALL_BUSINESS_PLACEHOLDER}
    assert result.safe_harbour_result.review_required is False
    assert result.avoidance_result.risk_level == "low"


def test_ai_admin_mechanic_is_worker_assist_or_low_nltg_safe_harbour() -> None:
    result = result_for("mechanic_ai_admin")

    assert result.safe_harbour_result.eligible is True
    assert result.safe_harbour_result.category in {WORKER_ASSIST_OR_ADMIN_AI, LOW_NLTG_EXCLUSION}
    assert result.avoidance_result.risk_level == "low"


def test_ai_admin_mechanic_is_not_classified_like_robotic_mechanic() -> None:
    ai_admin = result_for("mechanic_ai_admin")
    robotic = result_for("mechanic_robotic")

    assert ai_admin.safe_harbour_result.category != robotic.safe_harbour_result.category
    assert ai_admin.avoidance_result.risk_level == "low"
    assert robotic.avoidance_result.risk_level in {"medium", "high"}
    assert robotic.safe_harbour_result.category == NO_SAFE_HARBOUR_REVIEW


def test_safe_harbour_does_not_erase_liability() -> None:
    result = result_for("mechanic_robotic")

    assert result.outputs.liability > 0
    assert result.safe_harbour_result.eligible is False
    assert any("does not alter liability" in item.lower() for item in result.safe_harbour_result.placeholder_basis)


def test_startup_placeholder_requires_review_when_high_automation_and_low_qlc() -> None:
    example = load_example("mechanic_robotic")
    schedule = load_schedule(example["schedule_used"])
    modified = deepcopy(example)
    modified["red_team_notes"]["flags"] = []
    modified["risk_metadata"]["startup_placeholder"] = True
    modified["risk_metadata"]["token_human_oversight_risk"] = False
    modified["risk_metadata"]["fake_qlc_inflation_risk"] = False

    result = run_example(modified, schedule)

    assert result.safe_harbour_result.category == STARTUP_PLACEHOLDER
    assert result.safe_harbour_result.review_required is True
    assert result.safe_harbour_result.eligible is False
