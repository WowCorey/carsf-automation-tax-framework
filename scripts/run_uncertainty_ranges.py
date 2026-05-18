"""Run CARSF V1.5 deterministic placeholder uncertainty ranges."""

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

from carsf.distributional_uncertainty import evaluate_household_uncertainty  # noqa: E402
from carsf.example_runner import report_metadata  # noqa: E402
from carsf.uncertainty_ranges import UNCERTAINTY_WARNING, evaluate_uncertainty_range  # noqa: E402
from carsf.uncertainty_summary import summarise_uncertainty_results  # noqa: E402
from carsf.weighted_uncertainty import evaluate_weighted_uncertainty  # noqa: E402
from run_distributional_scenarios import run_distributional_examples  # noqa: E402
from run_household_weighting import run_household_weighting_examples  # noqa: E402


REPORT_STATUS = "deterministic_placeholder_uncertainty_outputs_only"
REPORT_NON_CLAIMS = [
    UNCERTAINTY_WARNING,
    "This is a prototype deterministic range wrapper only; it is not Monte Carlo, calibration, forecasting, or statistical inference.",
    "Uncertainty range outputs do not modify firm-level CARSF liability.",
]
REQUIRED_TRUE_LABELS = [
    "illustrative_placeholder_only",
    "synthetic_uncertainty_only",
    "not_calibrated",
    "not_representative",
    "no_real_household_data",
    "no_statistical_confidence_claim",
    "no_distributional_claim",
]


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def money(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:,.2f}"


def number(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:,.3f}"


def load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"uncertainty range example must be a mapping: {path}")
    return loaded


def example_paths(examples_dir: Path) -> list[Path]:
    if not examples_dir.exists():
        raise FileNotFoundError(f"missing uncertainty range examples directory: {examples_dir}")
    paths = sorted(examples_dir.glob("*.yaml"))
    if not paths:
        raise FileNotFoundError(f"no uncertainty range examples found in {examples_dir}")
    return paths


def validate_placeholder_labels(example: dict[str, Any], path: Path) -> None:
    for key in REQUIRED_TRUE_LABELS:
        if example.get(key) is not True:
            raise ValueError(f"{key} must be true in uncertainty range example: {path}")
    notice = str(example.get("placeholder_notice", "")).lower()
    if "deterministic" not in notice or "synthetic" not in notice or "placeholder" not in notice:
        raise ValueError(f"placeholder_notice must clearly label deterministic synthetic placeholders: {path}")


def _scenario_rows(distributional_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for row in distributional_rows:
        scenario = row["scenario_result"].to_jsonable()
        scenario["name"] = row["example"]["name"]
        rows[scenario["scenario_id"]] = scenario
    return rows


def _weighting_rows(weighting_rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {
        row["example"]["example_id"]: row["aggregation_result"].to_jsonable()
        for row in weighting_rows
    }


def _range_result_rows(example: dict[str, Any]) -> list[dict[str, Any]]:
    ranges: list[dict[str, Any]] = []
    if example.get("uncertainty_type") == "household":
        for value in example.get("ranges", {}).values():
            ranges.append(evaluate_uncertainty_range(value).to_jsonable())
    if example.get("uncertainty_type") == "weighted":
        for value in example.get("subgroup_residual_gap_ranges", {}).values():
            ranges.append(evaluate_uncertainty_range(value).to_jsonable())
        for value in example.get("subgroup_high_critical_share_ranges", {}).values():
            ranges.append(evaluate_uncertainty_range(value).to_jsonable())
    return ranges


def run_one_uncertainty_example(
    path: Path,
    scenarios_by_id: dict[str, dict[str, Any]],
    weighting_by_id: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    example = load_yaml(path)
    validate_placeholder_labels(example, path)
    uncertainty_type = str(example.get("uncertainty_type"))
    result = None
    if uncertainty_type == "household":
        scenario_id = str(example["scenario_id"])
        if scenario_id not in scenarios_by_id:
            raise ValueError(f"uncertainty example references unknown scenario_id: {scenario_id}")
        ranges = example["ranges"]
        result = evaluate_household_uncertainty(
            {
                "uncertainty_id": example["example_id"],
                "scenario_result": scenarios_by_id[scenario_id],
                "residual_gap_range": ranges["residual_gap"],
                "transition_support_range": ranges["transition_support"],
                "reemployment_months_range": ranges.get("reemployment_months"),
                "regional_stress_range": ranges.get("regional_stress"),
                "payment_cliff_loss_range": ranges.get("payment_cliff_loss"),
                "placeholder_basis": [f"uncertainty example: {example['example_id']}"],
            }
        )
    elif uncertainty_type == "weighted":
        weighting_id = str(example["weighting_example_id"])
        if weighting_id not in weighting_by_id:
            raise ValueError(f"uncertainty example references unknown weighting_example_id: {weighting_id}")
        result = evaluate_weighted_uncertainty(
            {
                "uncertainty_id": example["example_id"],
                "weighted_aggregation_result": weighting_by_id[weighting_id],
                "subgroup_residual_gap_ranges": example.get("subgroup_residual_gap_ranges", {}),
                "subgroup_high_critical_share_ranges": example.get("subgroup_high_critical_share_ranges", {}),
                "placeholder_basis": [f"uncertainty example: {example['example_id']}"],
            }
        )
    else:
        raise ValueError(f"unknown uncertainty_type in {path}: {uncertainty_type}")
    return {
        "fixture_path": str(path.relative_to(REPO_ROOT)),
        "example": example,
        "range_results": _range_result_rows(example),
        "uncertainty_result": result,
        "firm_level_liability_modified": False,
    }


def run_uncertainty_examples(
    examples_dir: Path,
    distributional_examples_dir: Path,
    household_weighting_examples_dir: Path,
) -> tuple[list[dict[str, Any]], Any]:
    distributional_rows = run_distributional_examples(distributional_examples_dir)
    scenarios_by_id = _scenario_rows(distributional_rows)
    weighting_rows, _, _ = run_household_weighting_examples(household_weighting_examples_dir, distributional_examples_dir)
    weighting_by_id = _weighting_rows(weighting_rows)
    rows = [
        run_one_uncertainty_example(path, scenarios_by_id, weighting_by_id)
        for path in example_paths(examples_dir)
    ]
    household_results = [
        row["uncertainty_result"]
        for row in rows
        if row["example"].get("uncertainty_type") == "household"
    ]
    weighted_results = [
        row["uncertainty_result"]
        for row in rows
        if row["example"].get("uncertainty_type") == "weighted"
    ]
    summary = summarise_uncertainty_results(household_results, weighted_results)
    return rows, summary


def build_json_payload(rows: list[dict[str, Any]], summary: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": REPORT_NON_CLAIMS,
        },
        "summary": _jsonable(summary),
        "examples": [
            {
                "fixture_path": row["fixture_path"],
                "example_id": row["example"]["example_id"],
                "name": row["example"]["name"],
                "purpose": row["example"]["purpose"],
                "status": row["example"]["status"],
                "uncertainty_type": row["example"]["uncertainty_type"],
                "range_results": row["range_results"],
                "uncertainty_result": _jsonable(row["uncertainty_result"]),
                "interpretation": row["example"].get("interpretation", ""),
                "firm_level_liability_modified": row["firm_level_liability_modified"],
            }
            for row in rows
        ],
    }


def _range_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Example | Metric | Low | Base | High | Abs Width | Rel Width | Stability |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        for result in row["range_results"]:
            rel = None if result["relative_range_width"] is None else f"{result['relative_range_width']:.2%}"
            lines.append(
                "| "
                f"{row['example']['name']} | {result['metric_name']} | {number(result['low'])} | "
                f"{number(result['base'])} | {number(result['high'])} | {number(result['absolute_range_width'])} | "
                f"{rel or 'N/A'} | {result['stability_band']} |"
            )
    return lines


def _household_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Example | Scenario | Low Case | Base Case | High Case | Risk Signal Stability | Drivers |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        if row["example"].get("uncertainty_type") != "household":
            continue
        result = row["uncertainty_result"]
        lines.append(
            "| "
            f"{row['example']['name']} | {result.scenario_id} | {result.low_case_shock_band} | "
            f"{result.base_case_shock_band} | {result.high_case_shock_band} | {result.risk_signal_stability} | "
            f"{', '.join(result.primary_uncertainty_drivers) or 'None'} |"
        )
    return lines


def _weighted_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Example | Subgroup | Scenario Count | Synthetic Weight | Matched Scenarios | Unmatched Scenarios | Not Population Estimate | Residual Gap Stability | High/Critical Share Stability | Subgroup Sensitivity |",
        "| --- | --- | ---: | ---: | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        if row["example"].get("uncertainty_type") != "weighted":
            continue
        result = row["uncertainty_result"]
        for subgroup in result.subgroup_results:
            residual = subgroup.get("residual_gap_range") or {}
            share = subgroup.get("high_critical_share_range") or {}
            lines.append(
                "| "
                f"{row['example']['name']} | {subgroup['subgroup_id']} | "
                f"{subgroup.get('scenario_count', 'N/A')} | {number(subgroup.get('total_synthetic_weight'))} | "
                f"{', '.join(subgroup.get('matched_scenarios', [])) or 'None'} | "
                f"{', '.join(subgroup.get('unmatched_scenarios', [])) or 'None'} | "
                f"{subgroup.get('not_population_estimate', True)} | "
                f"{residual.get('stability_band', 'missing')} | {share.get('stability_band', 'missing')} | "
                f"{subgroup['subgroup_range_sensitivity']} |"
            )
    return lines


def build_markdown(rows: list[dict[str, Any]], summary: Any, metadata: dict[str, Any]) -> str:
    lines = [
        "# CARSF V1.5 Uncertainty Range Mechanics",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report applies deterministic low/base/high placeholder ranges to synthetic household and weighted subgroup outputs.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in REPORT_NON_CLAIMS)
    lines.extend(
        [
            "",
            "## C. Why Uncertainty Ranges Matter",
            "",
            "Point estimates can imply false precision. These deterministic ranges show where synthetic household and subgroup signals are stable, sensitive, or too fragile to interpret without external calibration.",
            "",
            "## D. Low/Base/High Range Summary",
            "",
        ]
    )
    lines.extend(_range_table(rows))
    lines.extend(["", "## E. Household Uncertainty Results", ""])
    lines.extend(_household_table(rows))
    lines.extend(["", "## F. Weighted Subgroup Uncertainty Results", ""])
    lines.extend(_weighted_table(rows))
    lines.extend(
        [
            "",
            "## G. Stable High-Risk Signals",
            "",
            ", ".join(summary.strongest_stable_risk_signals) or "None",
            "",
            "## H. Range-Sensitive / Fragile Outputs",
            "",
            f"- Range-sensitive household count: {summary.range_sensitive_count}",
            f"- Fragile metric count: {summary.fragile_metric_count}",
            f"- Highest uncertainty items: {', '.join(summary.highest_uncertainty_items) or 'None'}",
            "",
            "## I. Calibration Blockers",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in summary.calibration_blockers)
    lines.extend(["", "## J. Plain-English Interpretation", ""])
    for row in rows:
        lines.extend([f"### {row['example']['name']}", "", row["example"].get("interpretation", ""), ""])
    lines.extend(
        [
            "## K. Limitations and Future Calibration Needs",
            "",
            "- Low/base/high values are deterministic placeholders, not Monte Carlo outputs or confidence intervals.",
            "- Stable high-risk signals still require external validation before policy use.",
            "- Fragile outputs require calibration before they should be interpreted.",
            "- No real household, ABS, HILDA, Census, DSS, Services Australia, ATO, Treasury, PBO, welfare, income, or survey data is used.",
            "- Firm-level CARSF liability is not automatically modified by uncertainty range outputs.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_reports(reports_dir: Path, rows: list[dict[str, Any]], summary: Any) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "uncertainty_ranges.json"
    md_path = reports_dir / "uncertainty_ranges.md"
    json_path.write_text(
        json.dumps(build_json_payload(rows, summary, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(rows, summary, metadata), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = ArgumentParser(description="Run deterministic placeholder uncertainty range examples.")
    parser.add_argument("--examples-dir", type=Path, default=REPO_ROOT / "examples" / "uncertainty_ranges")
    parser.add_argument("--distributional-examples-dir", type=Path, default=REPO_ROOT / "examples" / "distributional_scenarios")
    parser.add_argument("--household-weighting-examples-dir", type=Path, default=REPO_ROOT / "examples" / "household_weighting")
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args()

    rows, summary = run_uncertainty_examples(
        args.examples_dir,
        args.distributional_examples_dir,
        args.household_weighting_examples_dir,
    )
    json_path, md_path = write_reports(args.reports_dir, rows, summary)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
