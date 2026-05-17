"""Run CARSF V1.5 behavioural response / gaming simulation reports."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from dataclasses import asdict
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = REPO_ROOT / "model"
if str(MODEL_ROOT) not in sys.path:
    sys.path.insert(0, str(MODEL_ROOT))

SCRIPT_ROOT = REPO_ROOT / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from carsf.behavioural_response import (  # noqa: E402
    BEHAVIOURAL_RESPONSE_NON_CLAIMS,
    BEHAVIOURAL_RESPONSE_WARNING,
    COUNTERMEASURE_CATEGORIES,
    evaluate_behavioural_responses,
    summarise_behavioural_responses,
    validate_behavioural_response_scenarios,
)
from carsf.example_runner import report_metadata  # noqa: E402
from carsf.sector_stress_matrix import build_sector_stress_matrix  # noqa: E402
from run_sector_schedule_expansion import load_schedules, validate_schedules  # noqa: E402


REPORT_STATUS = "prototype_behavioural_response_simulation_synthetic_only"
DEFAULT_SCENARIOS_PATH = REPO_ROOT / "examples" / "behavioural_response_scenarios.yaml"


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def load_scenarios(path: Path) -> list[dict[str, Any]]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"behavioural response scenario file must be a mapping: {path}")
    required_labels = [
        "illustrative_placeholder_only",
        "synthetic_scenarios_only",
        "not_calibrated",
        "no_behavioural_prediction",
        "no_real_firm_data",
        "no_real_taxpayer_level_data",
        "no_compliance_scoring",
    ]
    missing = [label for label in required_labels if loaded.get(label) is not True]
    if missing:
        raise ValueError(f"behavioural response scenario file missing synthetic-only labels: {', '.join(missing)}")
    scenarios = loaded.get("scenarios", [])
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("behavioural response scenario file must contain non-empty scenarios list")
    if not all(isinstance(item, dict) for item in scenarios):
        raise ValueError("each behavioural response scenario must be a mapping")
    return scenarios


def _stress_by_schedule(schedules: list[dict[str, Any]]) -> dict[str, Any]:
    rows = build_sector_stress_matrix(schedules)
    return {row.schedule_id: row for row in rows}


def run_behavioural_response_simulation(schedules_dir: Path, scenarios_path: Path) -> tuple[list[Any], Any]:
    schedules = load_schedules(schedules_dir)
    validate_schedules(schedules)
    schedule_ids = {schedule["schedule_id"] for schedule in schedules}
    scenarios = load_scenarios(scenarios_path)
    validate_behavioural_response_scenarios(scenarios, schedule_ids)
    results = evaluate_behavioural_responses(scenarios, schedule_ids, _stress_by_schedule(schedules))
    summary = summarise_behavioural_responses(results)
    return results, summary


def build_json_payload(results: list[Any], summary: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": BEHAVIOURAL_RESPONSE_NON_CLAIMS,
            "firm_level_liability_logic_modified": False,
            "real_data_added": False,
            "behavioural_prediction_created": False,
            "compliance_scoring_created": False,
        },
        "summary": _jsonable(summary),
        "behavioural_response_results": [_jsonable(result) for result in results],
    }


def _table(results: list[Any]) -> list[str]:
    lines = [
        "| Scenario ID | Scenario Name | Sector Schedule | Response Type | Linked Avoidance Flags | Response Pressure Band | Review Status | Countermeasure Categories | External Review Required | Do Not Predict | Main Reason |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in results:
        lines.append(
            "| "
            f"{result.scenario_id} | {result.scenario_name} | {result.sector_schedule_id} | "
            f"{result.response_type} | {', '.join(result.linked_avoidance_flags) or 'None'} | "
            f"{result.response_pressure_band} | {result.review_status} | "
            f"{', '.join(result.countermeasure_categories)} | {result.external_review_required} | "
            f"{result.do_not_predict} | {result.main_reason} |"
        )
    return lines


def _counts_section(title: str, counts: dict[str, int]) -> list[str]:
    lines = [f"### {title}", ""]
    if not counts:
        lines.append("- None.")
    else:
        for key, value in counts.items():
            lines.append(f"- `{key}`: {value}")
    return lines


def _group_by_review_status(results: list[Any]) -> list[str]:
    lines: list[str] = []
    for status in sorted({result.review_status for result in results}):
        grouped = [result.scenario_id for result in results if result.review_status == status]
        lines.append(f"- `{status}`: {', '.join(grouped)}")
    return lines or ["- No review statuses generated."]


def _countermeasure_summary(results: list[Any]) -> list[str]:
    lines: list[str] = []
    for category in sorted(COUNTERMEASURE_CATEGORIES):
        grouped = [result.scenario_id for result in results if category in result.countermeasure_categories]
        if grouped:
            lines.append(f"- `{category}`: {', '.join(grouped)}")
    return lines or ["- No countermeasure categories generated."]


def _avoidance_flag_summary(results: list[Any]) -> list[str]:
    flags = sorted({flag for result in results for flag in result.linked_avoidance_flags})
    lines = []
    for flag in flags:
        grouped = [result.scenario_id for result in results if flag in result.linked_avoidance_flags]
        lines.append(f"- `{flag}`: {', '.join(grouped)}")
    return lines or ["- No linked avoidance flags listed."]


def build_markdown(results: list[Any], summary: Any, metadata: dict[str, Any]) -> str:
    lines = [
        "# CARSF V1.5 Behavioural Response / Gaming Simulation",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report maps synthetic CARSF response pathways to placeholder pressure bands, linked avoidance flags, and review pathways for policy discussion.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in BEHAVIOURAL_RESPONSE_NON_CLAIMS)
    lines.extend(
        [
            "- Every result has `do_not_predict: true`.",
            "- Every result has `do_not_score_real_taxpayer: true`.",
            "- Firm-level CARSF liability logic is not modified.",
            "",
            "## C. Method - Synthetic Placeholder Pathways Only",
            "",
            "The simulation uses declared synthetic scenario metadata, linked prototype avoidance flags, countermeasure categories, and sector stress display status. It simulates response pathways, not behavioural outcomes.",
            "",
            "## D. Scenario Coverage",
            "",
        ]
    )
    for result in results:
        lines.append(f"- `{result.scenario_id}`: {result.scenario_name} (`{result.response_type}`)")
    lines.extend(["", "## E. Behavioural Response Matrix", ""])
    lines.extend(_table(results))
    lines.extend(["", "## F. Response Pressure Bands", ""])
    lines.extend(_counts_section("Scenarios By Pressure Band", summary.scenarios_by_pressure_band))
    lines.extend(["", "## G. Linked Avoidance Flags", ""])
    lines.extend(_avoidance_flag_summary(results))
    lines.extend(["", "## H. Countermeasure / Review Pathways", ""])
    lines.extend(_countermeasure_summary(results))
    lines.extend(["", "## I. Sector Schedule Exposure Notes", ""])
    for result in results:
        lines.append(f"- `{result.scenario_id}` uses `{result.sector_schedule_id}` as a synthetic schedule context only.")
    lines.extend(["", "## J. Suppressed / External-Review Scenarios", ""])
    lines.extend(_group_by_review_status(results))
    lines.extend(["", "## K. Calibration and Behavioural Research Blockers", ""])
    if summary.calibration_blockers:
        lines.extend(f"- {blocker}" for blocker in summary.calibration_blockers)
    else:
        lines.append("- No blockers listed beyond global external calibration and methods review.")
    lines.extend(["", "## L. Plain-English Interpretation", ""])
    lines.extend(
        [
            "- Higher pressure bands indicate stronger prototype review pressure, not observed conduct.",
            "- Linked avoidance flags identify which existing prototype review checks a pathway touches.",
            "- Countermeasure categories show where evidence, grouping, transfer-pricing, schedule, AAVA, capital-base, offshore-attribution, or legal-policy review would be needed.",
            "- Suppressed scenarios are not ready for point-estimate presentation until calibration dependencies are resolved.",
        ]
    )
    lines.extend(["", "## M. Limitations and Future Review Needs", ""])
    lines.extend(_counts_section("Scenarios By Response Type", summary.scenarios_by_response_type))
    lines.extend([""])
    lines.extend(_counts_section("Scenarios By Review Status", summary.scenarios_by_review_status))
    lines.extend(
        [
            "",
            f"- Total scenarios: {summary.total_scenarios}",
            f"- Scenarios requiring external review: {summary.scenarios_requiring_external_review}",
            f"- Scenarios requiring transfer-pricing review: {summary.scenarios_requiring_transfer_pricing_review}",
            f"- Scenarios requiring grouped-entity review: {summary.scenarios_requiring_grouped_entity_review}",
            f"- Scenarios requiring schedule-authority review: {summary.scenarios_requiring_schedule_authority_review}",
            f"- Scenarios requiring AAVA deductibility review: {summary.scenarios_requiring_aava_deductibility_review}",
            f"- Scenarios requiring capital-base review: {summary.scenarios_requiring_capital_base_review}",
            f"- Scenarios requiring offshore-attribution review: {summary.scenarios_requiring_offshore_attribution_review}",
            f"- Scenarios requiring customer-self-service review: {summary.scenarios_requiring_customer_self_service_review}",
            f"- Scenarios suppress_until_calibrated: {summary.scenarios_suppress_until_calibrated}",
            f"- Firm-level liability logic modified: {summary.firm_level_liability_logic_modified}",
            "- Prototype only.",
            "- Placeholder only.",
            "- Synthetic scenarios only.",
            "- Deterministic scenario review only.",
            "- Not behavioural prediction or behavioural elasticity.",
            "- Not ATO audit logic, Treasury modelling, ABS/ATO/DSS/PBO analysis, compliance-risk scoring, legal advice, tax advice, investment advice, enforcement, or penalty modelling.",
            "- No firm-level, taxpayer-level, or industry data is used.",
            "- Not usable to estimate actual tax payable.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_reports(reports_dir: Path, results: list[Any], summary: Any) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "behavioural_response_simulation.json"
    md_path = reports_dir / "behavioural_response_simulation.md"
    json_path.write_text(
        json.dumps(build_json_payload(results, summary, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(results, summary, metadata), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = ArgumentParser(description="Run synthetic behavioural response / gaming simulation reports.")
    parser.add_argument("--schedules-dir", type=Path, default=REPO_ROOT / "schedules")
    parser.add_argument("--scenarios-path", type=Path, default=DEFAULT_SCENARIOS_PATH)
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args()

    results, summary = run_behavioural_response_simulation(args.schedules_dir, args.scenarios_path)
    json_path, md_path = write_reports(args.reports_dir, results, summary)
    print(f"evaluated {len(results)} behavioural response scenarios")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
