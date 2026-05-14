from __future__ import annotations

import math
from pathlib import Path

import yaml

from scripts.run_sector_schedule_expansion import load_schedules, validate_schedules


NEW_SCHEDULE_IDS = {
    "call_centres_customer_support",
    "accounting_administration",
    "retail_self_checkout_fulfilment",
    "software_digital_platforms",
}
REQUIRED_FIELDS = {
    "schedule_id",
    "schedule_name",
    "status",
    "canonical_output_unit",
    "calibration_status",
    "confirmed_baseline_figures",
    "measurement_scope",
    "qlc",
    "aii",
    "opfte_libc_placeholder",
    "frv",
    "caps",
    "safe_harbours",
    "measurement_controls",
    "avoidance_controls",
    "placeholder_assumptions",
    "data_required_for_real_calibration",
}


def _schedule_paths(repo_root: Path) -> list[Path]:
    return [
        path
        for path in sorted((repo_root / "schedules").glob("*.yaml"))
        if path.name != "schedule_schema.yaml"
    ]


def _load(path: Path) -> dict:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    assert isinstance(loaded, dict)
    return loaded


def test_new_schedule_files_parse_as_yaml(repo_root) -> None:
    for schedule_id in NEW_SCHEDULE_IDS:
        path = repo_root / "schedules" / f"{schedule_id}.yaml"
        assert path.exists()
        loaded = _load(path)
        assert loaded["schedule_id"] == schedule_id


def test_all_sector_schedules_contain_required_top_level_fields(repo_root) -> None:
    for path in _schedule_paths(repo_root):
        schedule = _load(path)
        assert REQUIRED_FIELDS <= set(schedule), path


def test_all_aii_weights_sum_to_one(repo_root) -> None:
    for path in _schedule_paths(repo_root):
        weights = _load(path)["aii"]["weights"]
        assert math.isclose(sum(float(value) for value in weights.values()), 1.0, abs_tol=1e-9), path


def test_all_qlc_weights_are_non_negative(repo_root) -> None:
    for path in _schedule_paths(repo_root):
        weights = _load(path)["qlc"]["weights"]
        assert all(float(value) >= 0 for value in weights.values()), path


def test_opfte_placeholders_are_positive(repo_root) -> None:
    for path in _schedule_paths(repo_root):
        schedule = _load(path)
        assert float(schedule["opfte_libc_placeholder"]["value"]) > 0, path


def test_frv_placeholders_positive_and_ordered(repo_root) -> None:
    for path in _schedule_paths(repo_root):
        frv = _load(path)["frv"]
        floor = float(frv["floor_placeholder"])
        standard = float(frv["standard_placeholder"])
        full = float(frv["full_placeholder"])
        assert 0 < floor <= standard <= full, path


def test_caps_within_placeholder_bounds(repo_root) -> None:
    for path in _schedule_paths(repo_root):
        caps = _load(path)["caps"]
        for key in ["lambda_sector", "LAMBDA_sector", "theta", "rent_tax_rate"]:
            assert 0 <= float(caps[key]) <= 1, (path, key)
        assert 0 < float(caps["uplift_rate"]) <= 2, path


def test_each_schedule_contains_calibration_status_and_placeholder_warnings(repo_root) -> None:
    for path in _schedule_paths(repo_root):
        schedule = _load(path)
        text = path.read_text(encoding="utf-8").lower()
        assert schedule["calibration_status"] == "illustrative_placeholder_values_only"
        assert "not calibrated" in text
        assert "must not be used to estimate actual tax payable" in text


def test_each_schedule_contains_data_required_for_real_calibration(repo_root) -> None:
    for path in _schedule_paths(repo_root):
        requirements = _load(path)["data_required_for_real_calibration"]
        assert isinstance(requirements, list)
        assert requirements


def test_software_schedule_includes_aasb_138_capital_base_warning(repo_root) -> None:
    text = (repo_root / "schedules" / "software_digital_platforms.yaml").read_text(encoding="utf-8").lower()

    assert "aasb 138" in text
    assert "capital-base treatment" in text
    assert "unresolved" in text


def test_schedule_expansion_validation_loads_all_sector_schedules(repo_root) -> None:
    schedules = load_schedules(repo_root / "schedules")
    summaries = validate_schedules(schedules)

    assert {summary["schedule_id"] for summary in summaries} >= NEW_SCHEDULE_IDS
    assert len(summaries) == 6
    assert all(summary["calibration_status"] == "illustrative_placeholder_values_only" for summary in summaries)
