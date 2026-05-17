"""Validate and report CARSF V1.5 prototype sector schedules."""

from __future__ import annotations

import json
import math
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = REPO_ROOT / "model"
if str(MODEL_ROOT) not in sys.path:
    sys.path.insert(0, str(MODEL_ROOT))

from carsf.example_runner import report_metadata  # noqa: E402


REPORT_STATUS = "prototype_sector_schedule_expansion_placeholders_only"
REPORT_WARNING = (
    "Sector schedules are prototype placeholders only. They are not calibrated. They are not legal schedules. "
    "They are not Treasury schedules. They are not ATO guidance. They are not ABS/ATO/DSS/PBO analysis. "
    "They do not contain real industry data. They must not be used to estimate actual tax payable."
)
REPORT_NON_CLAIMS = [
    REPORT_WARNING,
    "Sector schedules do not modify firm-level CARSF liability logic.",
    "Sector schedules do not implement real multi-schedule attribution.",
    "Sector schedules do not validate OPFTE, FRV, caps, or safe-harbour thresholds.",
]
REQUIRED_FIELDS = [
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
]
NEW_SCHEDULE_IDS = {
    "call_centres_customer_support",
    "accounting_administration",
    "retail_self_checkout_fulfilment",
    "software_digital_platforms",
}


def load_schedules(schedules_dir: Path) -> list[dict[str, Any]]:
    paths = sorted(schedules_dir.glob("*.yaml"))
    if not paths:
        raise FileNotFoundError(f"no schedule YAML files found in {schedules_dir}")
    schedules = []
    for path in paths:
        if path.name == "schedule_schema.yaml":
            continue
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
        if not isinstance(loaded, dict):
            raise ValueError(f"schedule must be a mapping: {path}")
        loaded["_path"] = str(path.relative_to(REPO_ROOT))
        schedules.append(loaded)
    return schedules


def _finite(value: Any, label: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    return number


def _serialised_lower(schedule: dict[str, Any]) -> str:
    return json.dumps({key: value for key, value in schedule.items() if key != "_path"}, sort_keys=True).lower()


def _validate_required_fields(schedule: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in schedule]
    if missing:
        raise ValueError(f"{schedule.get('_path', 'schedule')} missing required fields: {', '.join(missing)}")


def _validate_placeholder_labels(schedule: dict[str, Any]) -> None:
    if schedule["status"] != "placeholder_prototype_for_v1_5":
        raise ValueError(f"{schedule['_path']} must have placeholder_prototype_for_v1_5 status")
    if schedule["calibration_status"] != "illustrative_placeholder_values_only":
        raise ValueError(f"{schedule['_path']} must have illustrative placeholder calibration_status")
    text = _serialised_lower(schedule)
    required_phrases = ["not calibrated", "must not be used to estimate actual tax payable", "placeholder"]
    for phrase in required_phrases:
        if phrase not in text:
            raise ValueError(f"{schedule['_path']} missing placeholder/non-claim phrase: {phrase}")
    if schedule["schedule_id"] == "software_digital_platforms":
        if "aasb 138" not in text or "capital-base treatment" not in text or "unresolved" not in text:
            raise ValueError("software_digital_platforms must include unresolved AASB 138 capital-base warning")


def _validate_confirmed_baselines(schedule: dict[str, Any]) -> None:
    baselines = schedule.get("confirmed_baseline_figures")
    if not isinstance(baselines, list):
        raise ValueError(f"{schedule['_path']} confirmed_baseline_figures must be a list")
    for item in baselines:
        if not isinstance(item, dict) or item.get("source_status") != "official_source_labelled":
            raise ValueError(f"{schedule['_path']} has unlabelled confirmed baseline figure")


def _validate_weights(schedule: dict[str, Any]) -> None:
    qlc_weights = schedule["qlc"]["weights"]
    for name, value in qlc_weights.items():
        if _finite(value, f"{schedule['_path']} qlc {name}") < 0:
            raise ValueError(f"{schedule['_path']} QLC weight cannot be negative: {name}")
    aii_weights = schedule["aii"]["weights"]
    total = sum(_finite(value, f"{schedule['_path']} aii {name}") for name, value in aii_weights.items())
    if abs(total - 1.0) > 1e-9:
        raise ValueError(f"{schedule['_path']} AII weights must sum to 1.0; got {total}")


def _validate_opfte_frv_caps(schedule: dict[str, Any]) -> None:
    opfte = _finite(schedule["opfte_libc_placeholder"]["value"], f"{schedule['_path']} OPFTE placeholder")
    if opfte <= 0:
        raise ValueError(f"{schedule['_path']} OPFTE placeholder must be positive")
    frv = schedule["frv"]
    floor = _finite(frv["floor_placeholder"], f"{schedule['_path']} FRV floor")
    standard = _finite(frv["standard_placeholder"], f"{schedule['_path']} FRV standard")
    full = _finite(frv["full_placeholder"], f"{schedule['_path']} FRV full")
    if floor <= 0 or standard <= 0 or full <= 0 or not (floor <= standard <= full):
        raise ValueError(f"{schedule['_path']} FRV placeholders must be positive and ordered floor <= standard <= full")
    caps = schedule["caps"]
    for name in ["lambda_sector", "LAMBDA_sector", "theta", "rent_tax_rate"]:
        value = _finite(caps[name], f"{schedule['_path']} cap {name}")
        if not (0 <= value <= 1):
            raise ValueError(f"{schedule['_path']} cap {name} must be in [0, 1]")
    uplift = _finite(caps["uplift_rate"], f"{schedule['_path']} uplift_rate")
    if not (0 < uplift <= 2):
        raise ValueError(f"{schedule['_path']} uplift_rate must be in a bounded placeholder range")


def _validate_calibration_requirements(schedule: dict[str, Any]) -> None:
    requirements = schedule["data_required_for_real_calibration"]
    if not isinstance(requirements, list) or not requirements:
        raise ValueError(f"{schedule['_path']} must list data_required_for_real_calibration")
    if not isinstance(schedule["placeholder_assumptions"], list) or not schedule["placeholder_assumptions"]:
        raise ValueError(f"{schedule['_path']} must list placeholder assumptions")


def validate_schedule(schedule: dict[str, Any]) -> dict[str, Any]:
    _validate_required_fields(schedule)
    _validate_placeholder_labels(schedule)
    _validate_confirmed_baselines(schedule)
    _validate_weights(schedule)
    _validate_opfte_frv_caps(schedule)
    _validate_calibration_requirements(schedule)
    aii_total = sum(float(value) for value in schedule["aii"]["weights"].values())
    qlc_total = sum(float(value) for value in schedule["qlc"]["weights"].values())
    return {
        "schedule_id": schedule["schedule_id"],
        "schedule_name": schedule["schedule_name"],
        "path": schedule["_path"],
        "canonical_output_unit": schedule["canonical_output_unit"],
        "calibration_status": schedule["calibration_status"],
        "status": schedule["status"],
        "is_new_v1_5_expansion_schedule": schedule["schedule_id"] in NEW_SCHEDULE_IDS,
        "aii_weight_total": aii_total,
        "qlc_weight_total": qlc_total,
        "opfte_placeholder": float(schedule["opfte_libc_placeholder"]["value"]),
        "frv": {
            "floor": float(schedule["frv"]["floor_placeholder"]),
            "standard": float(schedule["frv"]["standard_placeholder"]),
            "full": float(schedule["frv"]["full_placeholder"]),
        },
        "caps": dict(schedule["caps"]),
        "measurement_risks": list(schedule.get("measurement_controls", {}).get("classification_arbitrage_controls", [])),
        "avoidance_risks": sorted(schedule.get("avoidance_controls", {}).keys()),
        "data_required_for_real_calibration": list(schedule["data_required_for_real_calibration"]),
        "placeholder_assumptions": list(schedule["placeholder_assumptions"]),
    }


def validate_schedules(schedules: list[dict[str, Any]]) -> list[dict[str, Any]]:
    summaries = [validate_schedule(schedule) for schedule in schedules]
    ids = {summary["schedule_id"] for summary in summaries}
    missing_new = sorted(NEW_SCHEDULE_IDS - ids)
    if missing_new:
        raise ValueError(f"missing required new schedule ids: {', '.join(missing_new)}")
    return sorted(summaries, key=lambda item: item["schedule_id"])


def build_json_payload(schedules: list[dict[str, Any]], summaries: list[dict[str, Any]], metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": REPORT_NON_CLAIMS,
            "firm_level_liability_logic_modified": False,
            "real_industry_data_added": False,
        },
        "summary": {
            "schedule_count": len(summaries),
            "new_schedule_count": sum(1 for item in summaries if item["is_new_v1_5_expansion_schedule"]),
            "new_schedule_ids": sorted(NEW_SCHEDULE_IDS),
            "all_aii_weights_valid": all(abs(item["aii_weight_total"] - 1.0) <= 1e-9 for item in summaries),
            "all_schedules_placeholder_only": True,
        },
        "schedules": summaries,
        "raw_schedule_status": [
            {
                "schedule_id": schedule["schedule_id"],
                "status": schedule["status"],
                "calibration_status": schedule["calibration_status"],
                "confirmed_baseline_figures_count": len(schedule["confirmed_baseline_figures"]),
            }
            for schedule in sorted(schedules, key=lambda item: item["schedule_id"])
        ],
    }


def _table_schedule_summary(summaries: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Schedule | New In This Build | Canonical Output Unit | Calibration Status |",
        "| --- | --- | --- | --- |",
    ]
    for summary in summaries:
        lines.append(
            "| "
            f"{summary['schedule_name']} | {summary['is_new_v1_5_expansion_schedule']} | "
            f"{summary['canonical_output_unit']} | {summary['calibration_status']} |"
        )
    return lines


def _table_aii(summaries: list[dict[str, Any]], schedules_by_id: dict[str, dict[str, Any]]) -> list[str]:
    lines = [
        "| Schedule | Compute | Auto Decision | Robotics Capital | Auto Process | Total |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for summary in summaries:
        weights = schedules_by_id[summary["schedule_id"]]["aii"]["weights"]
        lines.append(
            "| "
            f"{summary['schedule_id']} | {weights['compute_ratio']:.2f} | {weights['auto_decision_ratio']:.2f} | "
            f"{weights['robotics_capital_ratio']:.2f} | {weights['auto_process_share']:.2f} | "
            f"{summary['aii_weight_total']:.2f} |"
        )
    return lines


def _table_qlc(summaries: list[dict[str, Any]], schedules_by_id: dict[str, dict[str, Any]]) -> list[str]:
    lines = [
        "| Schedule | Wage Quality | Job Security | Skill Development | Australian Nexus | QLC Max Multiplier |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for summary in summaries:
        schedule = schedules_by_id[summary["schedule_id"]]
        weights = schedule["qlc"]["weights"]
        lines.append(
            "| "
            f"{summary['schedule_id']} | {weights['alpha_wage_quality']:.2f} | {weights['beta_job_security']:.2f} | "
            f"{weights['gamma_skill_development']:.2f} | {weights['delta_australian_nexus']:.2f} | "
            f"{float(schedule['qlc']['qlc_max_multiplier']):.2f} |"
        )
    return lines


def build_markdown(schedules: list[dict[str, Any]], summaries: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    schedules_by_id = {schedule["schedule_id"]: schedule for schedule in schedules}
    new_summaries = [item for item in summaries if item["is_new_v1_5_expansion_schedule"]]
    lines = [
        "# CARSF V1.5 Sector Schedule Expansion",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report validates and summarises the expanded prototype sector schedule library for CARSF V1.5.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in REPORT_NON_CLAIMS)
    lines.extend(
        [
            "- Sector schedules are not legal schedules, Treasury schedules, ATO guidance, ABS/ATO/DSS/PBO analysis, or real industry data.",
            "- Sector schedules must not be used to estimate actual tax payable.",
            "",
            "## C. Schedule Coverage Summary",
            "",
        ]
    )
    lines.extend(_table_schedule_summary(summaries))
    lines.extend(["", "## D. New Prototype Schedules", ""])
    for summary in new_summaries:
        lines.extend(
            [
                f"### {summary['schedule_name']}",
                "",
                f"- Schedule ID: `{summary['schedule_id']}`",
                f"- Canonical output unit: `{summary['canonical_output_unit']}`",
                f"- OPFTE placeholder: `{summary['opfte_placeholder']}`",
                f"- Calibration status: `{summary['calibration_status']}`",
                "",
            ]
        )
    lines.extend(["## E. Canonical Output Units", ""])
    for summary in summaries:
        lines.append(f"- `{summary['schedule_id']}`: `{summary['canonical_output_unit']}`")
    lines.extend(["", "## F. AII Weight Comparison", ""])
    lines.extend(_table_aii(summaries, schedules_by_id))
    lines.extend(["", "## G. QLC Weight Comparison", ""])
    lines.extend(_table_qlc(summaries, schedules_by_id))
    lines.extend(["", "## H. Schedule Measurement Risks", ""])
    for summary in summaries:
        lines.append(f"### {summary['schedule_id']}")
        if summary["measurement_risks"]:
            lines.extend(f"- {item}" for item in summary["measurement_risks"])
        else:
            lines.append("- No specific measurement risk listed beyond schedule controls.")
        lines.append("")
    lines.extend(["## I. Avoidance / Gaming Risks", ""])
    for summary in summaries:
        lines.append(f"- `{summary['schedule_id']}`: {', '.join(summary['avoidance_risks']) or 'None listed'}")
    lines.extend(["", "## J. Calibration Data Requirements", ""])
    for summary in summaries:
        lines.append(f"### {summary['schedule_id']}")
        lines.extend(f"- {item}" for item in summary["data_required_for_real_calibration"])
        lines.append("")
    lines.extend(
        [
            "## K. Multi-Schedule Blending Status",
            "",
            "Additional prototype schedules improve demonstration coverage, but they do not implement real multi-schedule legal attribution. True multi-schedule blending still requires calibrated sector schedules, legal attribution rules, evidence standards, and Schedules Authority review.",
            "",
            "## L. Limitations and Future Review Needs",
            "",
            "- Values are prototype placeholders only.",
            "- No real sector, ABS, ATO, DSS, PBO, Treasury, or industry calibration data has been added.",
            "- OPFTE, FRV, caps, safe-harbour thresholds, and measurement controls are not validated.",
            "- Software / digital platform capital-base treatment remains unresolved and subject to AASB 138, tax counsel, and Treasury review.",
            "- Firm-level CARSF liability logic is not modified.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_reports(reports_dir: Path, schedules: list[dict[str, Any]], summaries: list[dict[str, Any]]) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "sector_schedule_expansion.json"
    md_path = reports_dir / "sector_schedule_expansion.md"
    json_path.write_text(
        json.dumps(build_json_payload(schedules, summaries, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(schedules, summaries, metadata), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = ArgumentParser(description="Validate and report prototype CARSF sector schedules.")
    parser.add_argument("--schedules-dir", type=Path, default=REPO_ROOT / "schedules")
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args()

    schedules = load_schedules(args.schedules_dir)
    summaries = validate_schedules(schedules)
    json_path, md_path = write_reports(args.reports_dir, schedules, summaries)
    print(f"validated {len(schedules)} schedules")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
