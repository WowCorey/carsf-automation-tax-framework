"""Run CARSF V1.5 reviewed scenario comparison layer."""

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
from carsf.scenario_review import (  # noqa: E402
    SCENARIO_REVIEW_NON_CLAIMS,
    SCENARIO_REVIEW_WARNING,
    review_scenario,
    summarise_reviewed_scenarios,
)
from run_uncertainty_ranges import run_uncertainty_examples  # noqa: E402


REPORT_STATUS = "prototype_reviewed_scenario_display_control_only"


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def _fmt(value: Any) -> str:
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:,.3f}"
    return str(value)


def _join(values: list[str] | None) -> str:
    if not values:
        return "None"
    return ", ".join(values)


def build_reviewed_rows(uncertainty_rows: list[dict[str, Any]]) -> tuple[list[Any], list[Any]]:
    household_reviews = []
    weighted_reviews = []
    for row in uncertainty_rows:
        example = row["example"]
        result = _jsonable(row["uncertainty_result"])
        example_id = str(example["example_id"])
        if example.get("uncertainty_type") == "household":
            household_reviews.append(
                review_scenario(
                    {
                        "review_id": f"household:{example_id}",
                        "source_type": "household",
                        "source_result": result,
                        "scenario_name": str(example["name"]),
                        "representative_of_real_population": False,
                        "placeholder_basis": [f"reviewed uncertainty example: {example_id}"],
                    }
                )
            )
        elif example.get("uncertainty_type") == "weighted":
            for subgroup in result.get("subgroup_results", []):
                subgroup_id = str(subgroup.get("subgroup_id"))
                weighted_reviews.append(
                    review_scenario(
                        {
                            "review_id": f"weighted:{example_id}:{subgroup_id}",
                            "source_type": "weighted_subgroup",
                            "source_result": subgroup,
                            "subgroup_id": subgroup_id,
                            "subgroup_name": str(subgroup.get("subgroup_name", subgroup_id)),
                            "representative_of_real_population": False,
                            "total_synthetic_weight": subgroup.get("total_synthetic_weight"),
                            "placeholder_basis": [f"reviewed uncertainty example: {example_id}"],
                        }
                    )
                )
    return household_reviews, weighted_reviews


def build_json_payload(
    uncertainty_rows: list[dict[str, Any]],
    household_reviews: list[Any],
    weighted_reviews: list[Any],
    summary: Any,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": SCENARIO_REVIEW_NON_CLAIMS,
            "firm_level_liability_modified": False,
        },
        "summary": _jsonable(summary),
        "household_reviews": [_jsonable(item) for item in household_reviews],
        "weighted_subgroup_reviews": [_jsonable(item) for item in weighted_reviews],
        "source_uncertainty_examples": [
            {
                "example_id": row["example"]["example_id"],
                "name": row["example"]["name"],
                "uncertainty_type": row["example"]["uncertainty_type"],
                "firm_level_liability_modified": row["firm_level_liability_modified"],
            }
            for row in uncertainty_rows
        ],
    }


def _summary_counts(summary: Any) -> list[str]:
    return [
        f"- Prototype discussion signals: {summary.prototype_discussion_signal_count}",
        f"- Discussion with strong warning: {summary.discussion_with_strong_warning_count}",
        f"- Range-sensitive hidden point estimates: {summary.range_sensitive_hidden_count}",
        f"- Fragile suppressed point estimates: {summary.fragile_suppressed_count}",
        f"- Non-interpretable outputs: {summary.non_interpretable_count}",
        f"- Missing uncertainty range outputs: {summary.missing_uncertainty_range_count}",
        f"- External review required outputs: {summary.external_review_required_count}",
    ]


def _household_table(household_reviews: list[Any]) -> list[str]:
    lines = [
        "| Scenario | Risk Signal Stability | Low Case | Base Case | High Case | Fragile Metrics | Review Category | Display Level | Main Reason |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for review in household_reviews:
        lines.append(
            "| "
            f"{review.subject_name} | {review.risk_signal_stability or 'N/A'} | "
            f"{review.low_case_shock_band or 'N/A'} | {review.base_case_shock_band or 'N/A'} | "
            f"{review.high_case_shock_band or 'N/A'} | {_join(review.fragile_metrics)} | "
            f"{review.review_category} | {review.display_level} | {review.main_reason} |"
        )
    return lines


def _weighted_table(weighted_reviews: list[Any]) -> list[str]:
    lines = [
        "| Subgroup | Scenario Count | Synthetic Weight | Not Population Estimate | Residual Gap Stability | High/Critical Share Stability | Subgroup Sensitivity | Representative of Real Population | Review Category | Display Level | Main Reason |",
        "| --- | ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for review in weighted_reviews:
        lines.append(
            "| "
            f"{review.subject_name} | {_fmt(review.scenario_count)} | {_fmt(review.total_synthetic_weight)} | "
            f"{review.not_population_estimate} | {_fmt(review.residual_gap_stability)} | "
            f"{_fmt(review.high_critical_share_stability)} | {_fmt(review.subgroup_range_sensitivity)} | "
            f"{review.representative_of_real_population} | {review.review_category} | "
            f"{review.display_level} | {review.main_reason} |"
        )
    return lines


def _review_list(title: str, reviews: list[Any]) -> list[str]:
    lines = [f"### {title}", ""]
    if not reviews:
        lines.append("None")
        return lines
    for review in reviews:
        lines.append(f"- {review.subject_name}: `{review.review_category}` / `{review.display_level}` - {review.main_reason}")
    return lines


def build_markdown(
    household_reviews: list[Any],
    weighted_reviews: list[Any],
    summary: Any,
    metadata: dict[str, Any],
) -> str:
    all_reviews = household_reviews + weighted_reviews
    prototype = [item for item in all_reviews if item.review_category == "prototype_discussion_signal"]
    strong_warning = [item for item in all_reviews if item.review_category == "discussion_with_strong_warning"]
    suppressed = [
        item
        for item in all_reviews
        if item.display_level in {"hide_point_estimate", "external_review_only"}
    ]
    non_interpretable = [
        item
        for item in all_reviews
        if item.review_category in {"non_interpretable_until_calibrated", "missing_uncertainty_range"}
    ]
    blockers = sorted(
        set(summary.non_interpretable_outputs + summary.suppressed_or_hidden_outputs)
    )
    lines = [
        "# CARSF V1.5 Reviewed Scenario Comparison Layer",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report classifies deterministic synthetic uncertainty outputs into prototype display-control categories. It separates discussion-ready signals from fragile, range-sensitive, missing-range, or non-interpretable outputs.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in SCENARIO_REVIEW_NON_CLAIMS)
    lines.extend(
        [
            "- Reviewed scenario outputs are not population representative.",
            "- Fragile or missing-range outputs must not be presented as clean point estimates.",
            "",
            "## C. Review Category Rules",
            "",
            "- Stable high-risk or stable low-risk household signals can be shown with warnings when primary metrics are not fragile.",
            "- Stable household signals with fragile primary metrics are discussion signals only with strong warnings.",
            "- Range-sensitive household outputs hide point estimates.",
            "- Missing or non-assessable required ranges are hidden until calibrated or routed to external review.",
            "- Weighted subgroup outputs are always marked non-representative of a real population.",
            "- Fragile weighted subgroup ranges suppress point estimates.",
            "",
            "### Summary Counts",
            "",
        ]
    )
    lines.extend(_summary_counts(summary))
    lines.extend(["", "## D. Household Scenario Review Table", ""])
    lines.extend(_household_table(household_reviews))
    lines.extend(["", "## E. Weighted Subgroup Review Table", ""])
    lines.extend(_weighted_table(weighted_reviews))
    lines.extend(["", "## F. Prototype Discussion Signals", ""])
    lines.extend(_review_list("Show With Warning", prototype))
    lines.extend([""])
    lines.extend(_review_list("Strong Warning", strong_warning))
    lines.extend(["", "## G. Suppressed / Hidden Point Estimates", ""])
    lines.extend(_review_list("Hidden or Suppressed", suppressed))
    lines.extend(["", "## H. Non-Interpretable Outputs", ""])
    lines.extend(_review_list("Non-Interpretable", non_interpretable))
    lines.extend(
        [
            "",
            "## I. Missing Calibration / External Review Blockers",
            "",
        ]
    )
    if blockers:
        lines.extend(f"- {item}" for item in blockers)
    else:
        lines.append("- None in this generated synthetic fixture set.")
    lines.extend(
        [
            "",
            "## J. Plain-English Interpretation",
            "",
            "This layer is a review screen for presentation discipline. It keeps stable synthetic signals visible with warnings, hides point estimates where low/base/high cases are unstable, and routes missing or non-assessable uncertainty outputs away from policy interpretation until external calibration and methods review exists.",
            "",
            "## K. Limitations and Future Review Needs",
            "",
            "- This is synthetic only and placeholder only.",
            "- It is not statistical validation, confidence intervals, forecasting, real distributional modelling, or population estimation.",
            "- It is not ABS/HILDA/Census analysis, DSS/Services Australia modelling, ATO analysis, Treasury modelling, or PBO costing.",
            "- It is not welfare advice, eligibility law, legal advice, tax advice, or economic validation.",
            "- Stable prototype discussion signals still require external calibration and methods review.",
            "- Firm-level CARSF liability is not modified.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def run_reviewed_scenarios(
    examples_dir: Path,
    distributional_examples_dir: Path,
    household_weighting_examples_dir: Path,
) -> tuple[list[Any], list[Any], Any, list[dict[str, Any]]]:
    uncertainty_rows, _ = run_uncertainty_examples(
        examples_dir,
        distributional_examples_dir,
        household_weighting_examples_dir,
    )
    household_reviews, weighted_reviews = build_reviewed_rows(uncertainty_rows)
    summary = summarise_reviewed_scenarios(household_reviews + weighted_reviews)
    return household_reviews, weighted_reviews, summary, uncertainty_rows


def write_reports(
    reports_dir: Path,
    household_reviews: list[Any],
    weighted_reviews: list[Any],
    summary: Any,
    uncertainty_rows: list[dict[str, Any]],
) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "reviewed_scenarios.json"
    md_path = reports_dir / "reviewed_scenarios.md"
    json_path.write_text(
        json.dumps(
            build_json_payload(uncertainty_rows, household_reviews, weighted_reviews, summary, metadata),
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(household_reviews, weighted_reviews, summary, metadata), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = ArgumentParser(description="Run reviewed scenario comparison classifications.")
    parser.add_argument("--examples-dir", type=Path, default=REPO_ROOT / "examples" / "uncertainty_ranges")
    parser.add_argument("--distributional-examples-dir", type=Path, default=REPO_ROOT / "examples" / "distributional_scenarios")
    parser.add_argument("--household-weighting-examples-dir", type=Path, default=REPO_ROOT / "examples" / "household_weighting")
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args()

    household_reviews, weighted_reviews, summary, uncertainty_rows = run_reviewed_scenarios(
        args.examples_dir,
        args.distributional_examples_dir,
        args.household_weighting_examples_dir,
    )
    json_path, md_path = write_reports(args.reports_dir, household_reviews, weighted_reviews, summary, uncertainty_rows)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
