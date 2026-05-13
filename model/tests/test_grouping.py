from __future__ import annotations

from conftest import load_example, load_schedule

from carsf.example_runner import run_example
from carsf.grouping import (
    ENTITY_SPLITTING_SAFE_HARBOUR,
    RELATED_OPERATING_ENTITIES,
    SEPARATED_IP_PLATFORM_EMPLOYER,
    THIN_AUSTRALIAN_EMPLOYING_ENTITY,
)


def result_for(example_id: str):
    example = load_example(example_id)
    schedule = load_schedule(example["schedule_used"])
    return run_example(example, schedule)


def test_entity_splitting_metadata_triggers_grouping_review() -> None:
    result = result_for("logistics_ai_platform")

    assert result.grouping_risk_result.risk_level == "high"
    assert ENTITY_SPLITTING_SAFE_HARBOUR in result.grouping_risk_result.flags


def test_related_entity_structure_triggers_grouping_review() -> None:
    result = result_for("logistics_ai_platform")

    assert RELATED_OPERATING_ENTITIES in result.grouping_risk_result.flags
    assert SEPARATED_IP_PLATFORM_EMPLOYER in result.grouping_risk_result.flags


def test_thin_australian_entity_is_flagged_for_ai_platform() -> None:
    result = result_for("logistics_ai_platform")

    assert THIN_AUSTRALIAN_EMPLOYING_ENTITY in result.grouping_risk_result.flags


def test_human_heavy_logistics_has_lower_grouping_risk_than_ai_platform() -> None:
    human = result_for("logistics_human_heavy")
    platform = result_for("logistics_ai_platform")

    assert human.grouping_risk_result.risk_level == "low"
    assert platform.grouping_risk_result.risk_level == "high"
