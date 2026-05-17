"""Run CARSF V1.5 prototype sector stress matrix reports."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from dataclasses import asdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = REPO_ROOT / "model"
if str(MODEL_ROOT) not in sys.path:
    sys.path.insert(0, str(MODEL_ROOT))

SCRIPT_ROOT = REPO_ROOT / "scripts"
if str(SCRIPT_ROOT) not in sys.path:
    sys.path.insert(0, str(SCRIPT_ROOT))

from carsf.example_runner import report_metadata  # noqa: E402
from carsf.sector_stress_matrix import (  # noqa: E402
    SECTOR_STRESS_NON_CLAIMS,
    SECTOR_STRESS_WARNING,
    STRESS_DIMENSIONS,
    STRESS_BANDS,
    build_sector_stress_matrix,
    summarise_sector_stress,
)
from run_sector_schedule_expansion import load_schedules, validate_schedules  # noqa: E402


REPORT_STATUS = "prototype_sector_stress_matrix_metadata_only"


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def _label(value: str) -> str:
    return value.replace("_", " ")


def _dimension_value(row: Any, dimension: str) -> str:
    return str(getattr(row, dimension))


def build_json_payload(rows: list[Any], summary: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": SECTOR_STRESS_NON_CLAIMS,
            "firm_level_liability_logic_modified": False,
            "real_industry_data_added": False,
            "real_sector_rankings_created": False,
        },
        "summary": _jsonable(summary),
        "stress_matrix": [_jsonable(row) for row in rows],
    }


def _summary_lines(summary: Any) -> list[str]:
    lines = ["### Stress Band Counts", ""]
    for band in STRESS_BANDS:
        lines.append(f"- `{band}`: {summary.stress_band_counts.get(band, 0)}")
    lines.extend(["", "### Display-Control Counts", ""])
    for status, count in summary.display_status_counts.items():
        lines.append(f"- `{status}`: {count}")
    lines.extend(
        [
            "",
            f"- External-review-required rows: {summary.external_review_required_count}",
            f"- Strong-warning rows: {summary.strong_warning_required_count}",
            f"- All rows marked do-not-rank: {summary.do_not_rank_all}",
        ]
    )
    return lines


def _matrix_table(rows: list[Any]) -> list[str]:
    lines = [
        "| Schedule ID | Schedule Name | Canonical Output Unit | Automation Intensity | Digital Automation | Physical Automation | Decision Automation | Compute Dependency | QLC Vulnerability | AAVA Sensitivity | Incidence Risk | Investment Risk | Avoidance / Gaming Risk | Calibration Difficulty | Legal Attribution Difficulty | Display Status | Do Not Rank | Main Reason |",
        "| --- | --- | --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row.schedule_id} | {row.schedule_name} | {row.canonical_output_unit} | "
            f"{row.automation_intensity_placeholder} | {row.digital_automation_emphasis:.3f} | "
            f"{row.physical_automation_emphasis:.3f} | {row.decision_automation_emphasis:.3f} | "
            f"{row.compute_dependency_emphasis:.3f} | {row.qlc_vulnerability_placeholder} | "
            f"{row.aava_sensitivity_placeholder} | {row.incidence_risk_placeholder} | "
            f"{row.investment_deterrence_risk_placeholder} | {row.avoidance_gaming_risk_placeholder} | "
            f"{row.calibration_difficulty_placeholder} | {row.legal_attribution_difficulty_placeholder} | "
            f"{row.display_control_status} | {row.do_not_rank} | {row.main_reason} |"
        )
    return lines


def _band_group(rows: list[Any], dimension: str) -> list[str]:
    lines = []
    for band in STRESS_BANDS:
        grouped = [row.schedule_id for row in rows if _dimension_value(row, dimension) == band]
        if grouped:
            lines.append(f"- `{_label(band)}`: {', '.join(grouped)}")
    if not lines:
        lines.append("- No rows in this dimension.")
    return lines


def _automation_component_table(rows: list[Any]) -> list[str]:
    lines = [
        "| Schedule ID | Digital Automation Emphasis | Physical Automation Emphasis | Decision Automation Emphasis | Compute Dependency Emphasis | Robotics Dependency Note | Method Note |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row.schedule_id} | {row.digital_automation_emphasis:.3f} | "
            f"{row.physical_automation_emphasis:.3f} | {row.decision_automation_emphasis:.3f} | "
            f"{row.compute_dependency_emphasis:.3f} | {row.robotics_dependency_note} | "
            f"{row.automation_intensity_method_note} |"
        )
    return lines


def _display_status_group(rows: list[Any]) -> list[str]:
    statuses = sorted({row.display_control_status for row in rows})
    lines = []
    for status in statuses:
        grouped = [row.schedule_id for row in rows if row.display_control_status == status]
        lines.append(f"- `{status}`: {', '.join(grouped)}")
    return lines or ["- No display statuses generated."]


def _observations(rows: list[Any]) -> list[str]:
    lines = [
        "- This matrix groups schedules by placeholder metadata stress bands only.",
        "- A schedule with stronger warnings is not described as better or worse than another schedule.",
        "- Rows with external-review status require calibration, legal attribution review, and methods review before policy use.",
        "- Every row remains marked `do_not_rank: true`.",
    ]
    software = next((row for row in rows if row.schedule_id == "software_digital_platforms"), None)
    if software is not None:
        lines.append(
            "- `software_digital_platforms` carries software/intangible capital-base review warnings, including unresolved AASB 138 treatment."
        )
    return lines


def build_markdown(rows: list[Any], summary: Any, metadata: dict[str, Any]) -> str:
    lines = [
        "# CARSF V1.5 Sector Stress Matrix",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report compares prototype CARSF schedules across metadata-only review dimensions so reviewers can see where placeholder schedules are fragile, sensitive, or governance-heavy.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in SECTOR_STRESS_NON_CLAIMS)
    lines.extend(
        [
            "- Do not rank schedules using this matrix.",
            "",
            "## C. Method - Placeholder Metadata Only",
            "",
            "Scores are deterministic placeholders derived only from schedule metadata such as AII weights, QLC weights, cap placeholders, avoidance controls, calibration requirements, attribution wording, and unresolved review notes. No real sector data is used.",
            "",
            "Automation intensity separates digital automation emphasis, physical automation emphasis, decision automation emphasis, and compute dependency emphasis so low-robotics and high-robotics schedules are easier to read without creating a real sector score.",
            "",
            "## D. Sector Coverage",
            "",
        ]
    )
    for row in rows:
        lines.append(f"- `{row.schedule_id}`: {row.schedule_name}")
    lines.extend(["", "## E. Stress Band Definitions", ""])
    lines.extend(
        [
            "- `low_placeholder_stress`: low metadata review pressure.",
            "- `moderate_placeholder_stress`: moderate metadata review pressure.",
            "- `high_placeholder_stress`: high metadata review pressure.",
            "- `critical_review_required`: critical placeholder review pressure before policy discussion.",
            "- `not_assessable`: missing or non-interpretable metadata.",
            "",
            "## F. Sector Stress Matrix",
            "",
        ]
    )
    lines.extend(_matrix_table(rows))
    lines.extend(["", "## G. Automation Intensity Placeholder Bands", ""])
    lines.extend(_band_group(rows, "automation_intensity_placeholder"))
    lines.extend(["", "### Automation Intensity Component Explanation", ""])
    lines.extend(_automation_component_table(rows))
    lines.extend(["", "## H. QLC Vulnerability Placeholder Bands", ""])
    lines.extend(_band_group(rows, "qlc_vulnerability_placeholder"))
    lines.extend(["", "## I. AAVA Sensitivity Placeholder Bands", ""])
    lines.extend(_band_group(rows, "aava_sensitivity_placeholder"))
    lines.extend(["", "## J. Avoidance / Gaming Risk Placeholder Bands", ""])
    lines.extend(_band_group(rows, "avoidance_gaming_risk_placeholder"))
    lines.extend(["", "## K. Calibration Difficulty Placeholder Bands", ""])
    lines.extend(_band_group(rows, "calibration_difficulty_placeholder"))
    lines.extend(["", "## L. Legal Attribution Difficulty Placeholder Bands", ""])
    lines.extend(_band_group(rows, "legal_attribution_difficulty_placeholder"))
    lines.extend(["", "## M. Display-Control Status", ""])
    lines.extend(_display_status_group(rows))
    lines.extend(["", "## N. Cross-Sector Observations Without Rankings", ""])
    lines.extend(_observations(rows))
    lines.extend(["", "## O. Calibration and External Review Blockers", ""])
    for blocker in summary.calibration_blockers:
        lines.append(f"- {blocker}")
    lines.extend(["", "## P. Limitations and Future Review Needs", ""])
    lines.extend(_summary_lines(summary))
    lines.extend(
        [
            "",
            "- Prototype only.",
            "- Placeholder only.",
            "- Metadata-only.",
            "- Not calibrated.",
            "- Not a real-world ranking of sectors.",
            "- Not Treasury modelling, ATO guidance, ABS/ATO/DSS/PBO analysis, economic validation, investment advice, legal advice, or tax advice.",
            "- No real industry data is used.",
            "- Firm-level CARSF liability logic is not modified.",
            "- Legal sector attribution and real multi-schedule blending are not implemented.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def run_sector_stress_matrix(schedules_dir: Path) -> tuple[list[Any], Any]:
    schedules = load_schedules(schedules_dir)
    validate_schedules(schedules)
    rows = build_sector_stress_matrix(schedules)
    summary = summarise_sector_stress(rows)
    return rows, summary


def write_reports(reports_dir: Path, rows: list[Any], summary: Any) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "sector_stress_matrix.json"
    md_path = reports_dir / "sector_stress_matrix.md"
    json_path.write_text(
        json.dumps(build_json_payload(rows, summary, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(rows, summary, metadata), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = ArgumentParser(description="Run metadata-only prototype sector stress matrix.")
    parser.add_argument("--schedules-dir", type=Path, default=REPO_ROOT / "schedules")
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args()

    rows, summary = run_sector_stress_matrix(args.schedules_dir)
    json_path, md_path = write_reports(args.reports_dir, rows, summary)
    print(f"evaluated {len(rows)} sector schedules")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
