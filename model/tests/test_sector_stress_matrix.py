from __future__ import annotations

import pytest

from carsf.sector_stress_matrix import (
    STRESS_DIMENSIONS,
    build_sector_stress_matrix,
    evaluate_sector_stress,
    summarise_sector_stress,
)
from scripts.run_sector_schedule_expansion import load_schedules, validate_schedules


def test_all_schedules_produce_stress_row(repo_root) -> None:
    schedules = load_schedules(repo_root / "schedules")
    rows = build_sector_stress_matrix(schedules)

    assert len(rows) == 6
    assert {row.schedule_id for row in rows} == {schedule["schedule_id"] for schedule in schedules}


def test_schedule_schema_yaml_is_ignored(repo_root) -> None:
    schedules = load_schedules(repo_root / "schedules")

    assert "schedule_schema" not in {schedule.get("schedule_id") for schedule in schedules}


def test_every_stress_row_has_required_dimensions(repo_root) -> None:
    rows = build_sector_stress_matrix(load_schedules(repo_root / "schedules"))

    for row in rows:
        for dimension in STRESS_DIMENSIONS:
            assert getattr(row, dimension)
        assert row.display_control_status
        assert row.main_reason


def test_every_stress_row_is_do_not_rank(repo_root) -> None:
    rows = build_sector_stress_matrix(load_schedules(repo_root / "schedules"))
    summary = summarise_sector_stress(rows)

    assert all(row.do_not_rank is True for row in rows)
    assert summary.do_not_rank_all is True


def test_software_schedule_requires_strong_warning_or_external_review(repo_root) -> None:
    rows = build_sector_stress_matrix(load_schedules(repo_root / "schedules"))
    software = next(row for row in rows if row.schedule_id == "software_digital_platforms")

    assert software.display_control_status in {"strong_warning_required", "external_review_required"}
    assert any("AASB 138" in warning for warning in software.warnings)


def test_schedule_missing_calibration_status_fails_closed(repo_root) -> None:
    schedule = next(
        item for item in load_schedules(repo_root / "schedules") if item["schedule_id"] == "automotive_repair"
    )
    schedule = dict(schedule)
    schedule.pop("calibration_status")

    with pytest.raises(ValueError, match="calibration_status"):
        evaluate_sector_stress({"schedule": schedule})


def test_invalid_aii_weights_fail_through_schedule_validation(repo_root) -> None:
    schedules = load_schedules(repo_root / "schedules")
    mutated = []
    for schedule in schedules:
        copied = dict(schedule)
        if schedule["schedule_id"] == "automotive_repair":
            copied["aii"] = {"weights": dict(schedule["aii"]["weights"])}
            copied["aii"]["weights"]["compute_ratio"] = copied["aii"]["weights"]["compute_ratio"] + 0.10
        mutated.append(copied)

    with pytest.raises(ValueError, match="AII weights must sum to 1.0"):
        validate_schedules(mutated)


def test_sector_stress_output_order_is_deterministic(repo_root) -> None:
    schedules = load_schedules(repo_root / "schedules")
    first = build_sector_stress_matrix(schedules)
    second = build_sector_stress_matrix(schedules)

    assert [row.schedule_id for row in first] == [row.schedule_id for row in second]
    assert summarise_sector_stress(first).to_jsonable() == summarise_sector_stress(second).to_jsonable()
