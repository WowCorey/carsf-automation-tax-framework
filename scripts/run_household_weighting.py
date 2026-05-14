"""Run CARSF V1.5 synthetic household weighting and subgroup aggregation."""

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

from carsf.example_runner import report_metadata  # noqa: E402
from carsf.household_calibration_shell import get_household_calibration_requirements  # noqa: E402
from carsf.household_weights import HOUSEHOLD_WEIGHTING_WARNING, evaluate_household_weight  # noqa: E402
from carsf.subgroups import assign_subgroups, subgroup_definition_from_mapping  # noqa: E402
from carsf.weighted_distributional import WeightedDistributionalResult, run_weighted_distributional_aggregation  # noqa: E402
from run_distributional_scenarios import run_distributional_examples  # noqa: E402


REPORT_STATUS = "synthetic_household_weighting_outputs_only"
REPORT_NON_CLAIMS = [
    HOUSEHOLD_WEIGHTING_WARNING,
    "This is a prototype weighting and subgroup aggregation shell only; it is not a validated distributional model.",
    "All household weights and subgroup aggregations are illustrative placeholders and are not representative.",
    "Household weighting outputs do not modify firm-level CARSF liability.",
]
REQUIRED_TRUE_LABELS = [
    "illustrative_placeholder_only",
    "synthetic_weight_only",
    "not_calibrated",
    "not_representative",
    "no_real_household_data",
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


def rate(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:.2%}"


def load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"household weighting example must be a mapping: {path}")
    return loaded


def example_paths(examples_dir: Path) -> list[Path]:
    if not examples_dir.exists():
        raise FileNotFoundError(f"missing household weighting examples directory: {examples_dir}")
    paths = sorted(examples_dir.glob("*.yaml"))
    if not paths:
        raise FileNotFoundError(f"no household weighting examples found in {examples_dir}")
    return paths


def validate_placeholder_labels(example: dict[str, Any], path: Path) -> None:
    for key in REQUIRED_TRUE_LABELS:
        if example.get(key) is not True:
            raise ValueError(f"{key} must be true in household weighting example: {path}")
    notice = str(example.get("placeholder_notice", "")).lower()
    if "synthetic" not in notice or "placeholder" not in notice:
        raise ValueError(f"placeholder_notice must clearly label synthetic placeholders: {path}")


def scenario_rows(distributional_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in distributional_rows:
        scenario = row["scenario_result"].to_jsonable()
        household = row["example"]["household"]
        scenario.update(
            {
                "name": row["example"]["name"],
                "household_type": household["household_type"],
                "income_band": household["income_band"],
                "region_type": household["region_type"],
            }
        )
        rows.append(scenario)
    return rows


def run_one_weighting_example(path: Path, scenarios: list[dict[str, Any]]) -> dict[str, Any]:
    example = load_yaml(path)
    validate_placeholder_labels(example, path)
    subgroup_definitions = [subgroup_definition_from_mapping(item) for item in example["subgroup_definitions"]]
    weight_results = [evaluate_household_weight(item) for item in example["household_weights"]]
    assignments = [assign_subgroups(row, subgroup_definitions) for row in scenarios]
    aggregation_result = run_weighted_distributional_aggregation(
        {
            "aggregation_id": example["example_id"],
            "scenario_results": scenarios,
            "household_weights": example["household_weights"],
            "subgroup_definitions": example["subgroup_definitions"],
            "calibration_status": example.get("calibration_status", "not_calibrated"),
            "placeholder_basis": [f"household weighting example: {example['example_id']}"],
        }
    )
    return {
        "fixture_path": str(path.relative_to(REPO_ROOT)),
        "example": example,
        "weight_results": weight_results,
        "subgroup_assignments": assignments,
        "aggregation_result": aggregation_result,
        "firm_level_liability_modified": False,
    }


def run_household_weighting_examples(examples_dir: Path, distributional_examples_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]], Any]:
    distributional_rows = run_distributional_examples(distributional_examples_dir)
    scenarios = scenario_rows(distributional_rows)
    calibration_shell = get_household_calibration_requirements()
    rows = [run_one_weighting_example(path, scenarios) for path in example_paths(examples_dir)]
    return rows, scenarios, calibration_shell


def build_json_payload(rows: list[dict[str, Any]], scenarios: list[dict[str, Any]], calibration_shell: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": REPORT_NON_CLAIMS,
        },
        "source_scenarios": scenarios,
        "calibration_shell": _jsonable(calibration_shell),
        "examples": [
            {
                "fixture_path": row["fixture_path"],
                "example_id": row["example"]["example_id"],
                "name": row["example"]["name"],
                "purpose": row["example"]["purpose"],
                "status": row["example"]["status"],
                "weight_results": [_jsonable(item) for item in row["weight_results"]],
                "subgroup_assignments": [_jsonable(item) for item in row["subgroup_assignments"]],
                "aggregation_result": _jsonable(row["aggregation_result"]),
                "interpretation": row["example"].get("interpretation", ""),
                "firm_level_liability_modified": row["firm_level_liability_modified"],
            }
            for row in rows
        ],
    }


def _weight_table(row: dict[str, Any]) -> list[str]:
    lines = [
        "| Scenario | Subgroup | Weight | Calibrated | Usable for Real-World Claims | Basis |",
        "| --- | --- | ---: | --- | --- | --- |",
    ]
    weight_by_key = {(item.scenario_id, item.subgroup_id): item for item in row["weight_results"]}
    for weight in row["example"]["household_weights"]:
        result = weight_by_key[(str(weight["scenario_id"]), str(weight["subgroup_id"]))]
        lines.append(
            "| "
            f"{result.scenario_id} | {result.subgroup_id} | {result.weight_value:,.4f} | "
            f"{str(result.calibrated).lower()} | {str(result.usable_for_real_world_claims).lower()} | "
            f"{weight.get('weight_basis', '')} |"
        )
    return lines


def _subgroup_definition_table(row: dict[str, Any]) -> list[str]:
    lines = [
        "| Subgroup | Name | Household Type | Income Band | Region | Re-Employment Risk | Budget Stress | Regional Stress |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for definition in row["example"]["subgroup_definitions"]:
        lines.append(
            "| "
            f"{definition['subgroup_id']} | {definition.get('subgroup_name', definition['subgroup_id'])} | "
            f"{definition.get('household_type_filter') or 'Any'} | {definition.get('income_band_filter') or 'Any'} | "
            f"{definition.get('region_type_filter') or 'Any'} | {definition.get('reemployment_risk_filter') or 'Any'} | "
            f"{definition.get('budget_stress_filter') or 'Any'} | {definition.get('regional_stress_filter') or 'Any'} |"
        )
    return lines


def _aggregation_table(row: dict[str, Any]) -> list[str]:
    result: WeightedDistributionalResult = row["aggregation_result"]
    lines = [
        "| Metric | Value |",
        "| --- | ---: |",
        f"| Total synthetic weight | {result.total_synthetic_weight:,.4f} |",
        f"| Overall weighted average residual gap | {money(result.overall_weighted_average_residual_gap)} |",
        f"| Overall weighted high/critical share | {rate(result.overall_weighted_high_or_critical_share)} |",
        f"| Representative of real population | {str(result.representative_of_real_population).lower()} |",
    ]
    return lines


def _subgroup_result_table(row: dict[str, Any]) -> list[str]:
    result: WeightedDistributionalResult = row["aggregation_result"]
    lines = [
        "| Subgroup | Scenarios | Weight | Weighted Avg Residual Gap | High/Critical Share | Highest-Risk Scenarios | Representativeness Warning |",
        "| --- | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for subgroup in result.subgroup_results:
        lines.append(
            "| "
            f"{subgroup.subgroup_name} | {subgroup.scenario_count} | {subgroup.total_synthetic_weight:,.4f} | "
            f"{money(subgroup.weighted_average_residual_gap)} | {rate(subgroup.weighted_high_or_critical_share)} | "
            f"{', '.join(subgroup.highest_risk_scenarios) or 'None'} | {str(subgroup.representativeness_warning).lower()} |"
        )
    return lines


def _calibration_table(calibration_shell: Any) -> list[str]:
    lines = [
        "| Requirement | Category | Required For | Source Type | Status | Real Data In Repo Allowed |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for requirement in calibration_shell.requirements:
        lines.append(
            "| "
            f"{requirement.requirement_id} | {requirement.category} | {', '.join(requirement.required_for)} | "
            f"{requirement.possible_source_type} | {requirement.status} | {str(requirement.real_data_in_repo_allowed).lower()} |"
        )
    return lines


def build_markdown(rows: list[dict[str, Any]], calibration_shell: Any, metadata: dict[str, Any]) -> str:
    lines = [
        "# CARSF V1.5 Household Weighting and Subgroup Aggregation Shell",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report previews synthetic household weighting and subgroup aggregation over existing synthetic distributional scenarios.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in REPORT_NON_CLAIMS)
    lines.extend(
        [
            "",
            "## C. Why Weighting and Subgroup Aggregation Matter",
            "",
            "Individual synthetic scenarios can show household mechanics, but policy review also needs a controlled shell for subgroup aggregation. This shell validates placeholder weights, groups scenarios, and makes representativeness warnings explicit. It is not population weighting.",
            "",
            "## D. Synthetic Weight Summary",
            "",
        ]
    )
    for row in rows:
        lines.extend([f"### {row['example']['name']}", ""])
        lines.extend(_weight_table(row))
        lines.append("")
    lines.extend(["## E. Subgroup Definitions", ""])
    for row in rows:
        lines.extend([f"### {row['example']['name']}", ""])
        lines.extend(_subgroup_definition_table(row))
        lines.append("")
    lines.extend(["## F. Weighted Aggregation Results", ""])
    for row in rows:
        lines.extend([f"### {row['example']['name']}", ""])
        lines.extend(_aggregation_table(row))
        lines.append("")
        lines.extend(_subgroup_result_table(row))
        lines.append("")
    lines.extend(["## G. Highest-Risk Synthetic Subgroups", ""])
    lines.extend(["| Example | Highest-Risk Subgroups |", "| --- | --- |"])
    for row in rows:
        result: WeightedDistributionalResult = row["aggregation_result"]
        lines.append(f"| {row['example']['name']} | {', '.join(result.highest_risk_subgroups) or 'None'} |")
    lines.extend(["", "## H. Representativeness Warnings", ""])
    for row in rows:
        result: WeightedDistributionalResult = row["aggregation_result"]
        lines.extend([f"### {row['example']['name']}", ""])
        lines.extend(f"- {warning}" for warning in result.warnings)
        lines.append("- representative_of_real_population: false")
        lines.append("")
    lines.extend(["## I. Calibration Readiness Requirements", ""])
    lines.append(f"Ready for real distributional claims: `{str(calibration_shell.ready_for_real_distributional_claims).lower()}`")
    lines.append("")
    lines.extend(_calibration_table(calibration_shell))
    lines.extend(["", "## J. Plain-English Interpretation", ""])
    for row in rows:
        lines.extend(
            [
                f"### {row['example']['name']}",
                "",
                row["example"].get("interpretation", ""),
                "",
                "- Firm-level CARSF liability is not automatically modified by this household weighting shell.",
                "",
            ]
        )
    lines.extend(
        [
            "## K. Limitations and Future Data Needs",
            "",
            "- All weights, subgroup definitions, and aggregation outputs are synthetic illustrative placeholders.",
            "- These outputs are not population estimates and are not representative of real Australian households.",
            "- No real household data, ABS, HILDA, Census, DSS, Services Australia, ATO, Treasury, PBO, welfare, income, or survey data is used.",
            "- Future calibration requires a controlled external data environment and legal, privacy, DSS / Services Australia, ABS, HILDA, Treasury, PBO, and economic review.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_reports(reports_dir: Path, rows: list[dict[str, Any]], scenarios: list[dict[str, Any]], calibration_shell: Any) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "household_weighting.json"
    md_path = reports_dir / "household_weighting.md"
    json_path.write_text(
        json.dumps(build_json_payload(rows, scenarios, calibration_shell, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(rows, calibration_shell, metadata), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = ArgumentParser(description="Run CARSF synthetic household weighting and subgroup aggregation.")
    parser.add_argument("--examples-dir", type=Path, default=REPO_ROOT / "examples" / "household_weighting")
    parser.add_argument("--distributional-examples-dir", type=Path, default=REPO_ROOT / "examples" / "distributional_scenarios")
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args()

    rows, scenarios, calibration_shell = run_household_weighting_examples(args.examples_dir, args.distributional_examples_dir)
    json_path, md_path = write_reports(args.reports_dir, rows, scenarios, calibration_shell)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
