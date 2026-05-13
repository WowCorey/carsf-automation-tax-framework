from __future__ import annotations

from copy import deepcopy

from conftest import load_example, load_schedule

from carsf.avoidance import (
    CLOUD_COST_RELABELING,
    ENTITY_SPLITTING,
    FAKE_QLC_INFLATION,
    OFFSHORE_AUTOMATION_SERVICE,
    RELATED_PARTY_AI_SERVICE_FEES,
    SECTOR_CLASSIFICATION_ARBITRAGE,
    TOKEN_HUMAN_OVERSIGHT,
)
from carsf.example_runner import run_example


def result_for(example_id: str):
    example = load_example(example_id)
    schedule = load_schedule(example["schedule_used"])
    return run_example(example, schedule)


def test_human_heavy_logistics_is_lower_risk_than_ai_platform() -> None:
    human = result_for("logistics_human_heavy")
    platform = result_for("logistics_ai_platform")

    assert human.avoidance_result.risk_level == "low"
    assert platform.avoidance_result.risk_level == "high"
    assert len(platform.avoidance_result.flags) > len(human.avoidance_result.flags)


def test_ai_logistics_platform_triggers_high_risk_or_multiple_flags() -> None:
    result = result_for("logistics_ai_platform")

    assert result.avoidance_result.risk_level == "high"
    assert len(result.avoidance_result.flags) >= 4
    assert OFFSHORE_AUTOMATION_SERVICE in result.avoidance_result.flags
    assert RELATED_PARTY_AI_SERVICE_FEES in result.avoidance_result.flags
    assert ENTITY_SPLITTING in result.avoidance_result.flags
    assert SECTOR_CLASSIFICATION_ARBITRAGE in result.avoidance_result.flags


def test_robotic_mechanic_triggers_token_oversight_or_robotics_review() -> None:
    result = result_for("mechanic_robotic")

    assert TOKEN_HUMAN_OVERSIGHT in result.avoidance_result.flags
    assert result.avoidance_result.risk_level in {"medium", "high"}


def test_offshore_automation_service_metadata_triggers_flag() -> None:
    result = result_for("logistics_ai_platform")

    assert OFFSHORE_AUTOMATION_SERVICE in result.avoidance_result.flags


def test_related_party_ai_service_fee_metadata_triggers_flag() -> None:
    result = result_for("logistics_ai_platform")

    assert RELATED_PARTY_AI_SERVICE_FEES in result.avoidance_result.flags


def test_fake_qlc_inflation_metadata_triggers_flag() -> None:
    result = result_for("mechanic_robotic")

    assert FAKE_QLC_INFLATION in result.avoidance_result.flags


def test_cloud_cost_relabeling_metadata_triggers_flag() -> None:
    result = result_for("logistics_ai_platform")

    assert CLOUD_COST_RELABELING in result.avoidance_result.flags


def test_synthetic_offshore_metadata_triggers_flag_without_changing_outputs() -> None:
    example = load_example("mechanic_ai_admin")
    schedule = load_schedule(example["schedule_used"])
    base = run_example(example, schedule)
    modified = deepcopy(example)
    modified["risk_metadata"]["offshore_automation_service"] = True
    flagged = run_example(modified, schedule)

    assert OFFSHORE_AUTOMATION_SERVICE in flagged.avoidance_result.flags
    assert flagged.outputs == base.outputs
