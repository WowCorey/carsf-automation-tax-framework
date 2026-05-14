"""Run CARSF V1.5 synthetic household distributional scenarios."""

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

from carsf.distributional_scenarios import evaluate_distributional_scenario  # noqa: E402
from carsf.distributional_summary import DistributionalSummaryResult, summarise_distributional_scenarios  # noqa: E402
from carsf.example_runner import report_metadata  # noqa: E402
from carsf.households import DISTRIBUTIONAL_WARNING, evaluate_household_budget  # noqa: E402
from carsf.payment_cliffs import evaluate_payment_cliff  # noqa: E402
from carsf.reemployment import evaluate_reemployment_path  # noqa: E402
from carsf.regional_stress import evaluate_regional_stress  # noqa: E402


REPORT_STATUS = "synthetic_household_distributional_outputs_only"
REPORT_NON_CLAIMS = [
    DISTRIBUTIONAL_WARNING,
    "All household, regional, re-employment, payment cliff, and support values are illustrative placeholders.",
    "Synthetic distributional scenario outputs do not modify firm-level CARSF liability.",
]
REQUIRED_TRUE_LABELS = [
    "illustrative_placeholder_only",
    "synthetic_household_only",
    "not_calibrated",
    "no_policy_claim",
    "no_welfare_advice",
    "no_real_household_data",
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


def load_yaml(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"distributional scenario must be a mapping: {path}")
    return loaded


def example_paths(examples_dir: Path) -> list[Path]:
    if not examples_dir.exists():
        raise FileNotFoundError(f"missing distributional scenario directory: {examples_dir}")
    paths = sorted(examples_dir.glob("*.yaml"))
    if not paths:
        raise FileNotFoundError(f"no distributional scenarios found in {examples_dir}")
    return paths


def validate_placeholder_labels(example: dict[str, Any], path: Path) -> None:
    for key in REQUIRED_TRUE_LABELS:
        if example.get(key) is not True:
            raise ValueError(f"{key} must be true in distributional scenario: {path}")
    notice = str(example.get("placeholder_notice", "")).lower()
    if "synthetic" not in notice or "placeholder" not in notice:
        raise ValueError(f"placeholder_notice must clearly label synthetic placeholders: {path}")


def run_one_scenario(path: Path) -> dict[str, Any]:
    example = load_yaml(path)
    validate_placeholder_labels(example, path)
    household = example["household"]
    reemployment_path = example["reemployment_path"]
    regional_stress = example["regional_stress"]
    payment_cliff = example.get("payment_cliff")
    budget_result = evaluate_household_budget(household)
    reemployment_result = evaluate_reemployment_path(reemployment_path, household)
    regional_result = evaluate_regional_stress(regional_stress)
    cliff_result = evaluate_payment_cliff(payment_cliff) if payment_cliff is not None else None
    scenario_result = evaluate_distributional_scenario(example)
    return {
        "fixture_path": str(path.relative_to(REPO_ROOT)),
        "example": example,
        "household_budget_result": budget_result,
        "reemployment_result": reemployment_result,
        "regional_stress_result": regional_result,
        "payment_cliff_result": cliff_result,
        "scenario_result": scenario_result,
        "firm_level_liability_modified": False,
    }


def run_distributional_examples(examples_dir: Path) -> list[dict[str, Any]]:
    return [run_one_scenario(path) for path in example_paths(examples_dir)]


def build_json_payload(rows: list[dict[str, Any]], summary: DistributionalSummaryResult, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": REPORT_NON_CLAIMS,
        },
        "summary": summary.to_jsonable(),
        "examples": [
            {
                "fixture_path": row["fixture_path"],
                "scenario_id": row["example"]["scenario_id"],
                "name": row["example"]["name"],
                "purpose": row["example"]["purpose"],
                "status": row["example"]["status"],
                "household": row["example"]["household"],
                "household_budget_result": _jsonable(row["household_budget_result"]),
                "reemployment_result": _jsonable(row["reemployment_result"]),
                "regional_stress_result": _jsonable(row["regional_stress_result"]),
                "payment_cliff_result": _jsonable(row["payment_cliff_result"]) if row["payment_cliff_result"] is not None else None,
                "scenario_result": _jsonable(row["scenario_result"]),
                "interpretation": row["example"].get("interpretation", ""),
                "firm_level_liability_modified": row["firm_level_liability_modified"],
            }
            for row in rows
        ],
    }


def _household_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Scenario | Household Type | Adults | Children | Region | Income Band | Pre-Income | Post-Income |",
        "| --- | --- | ---: | ---: | --- | --- | ---: | ---: |",
    ]
    for row in rows:
        household = row["example"]["household"]
        lines.append(
            "| "
            f"{row['example']['name']} | {household['household_type']} | {household['adults']} | "
            f"{household['children']} | {household['region_type']} | {household['income_band']} | "
            f"{money(float(household['pre_displacement_income']))} | {money(float(household['post_displacement_income']))} |"
        )
    return lines


def _budget_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Scenario | Income Loss | Existing Support | Basic Costs | Disposable After Costs | Savings Buffer | Immediate Gap | Stress Band |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        budget = row["household_budget_result"]
        lines.append(
            "| "
            f"{row['example']['name']} | {money(budget.income_loss)} | {money(budget.existing_support_baseline)} | "
            f"{money(budget.total_basic_costs)} | {money(budget.disposable_after_basic_costs)} | "
            f"{money(budget.savings_buffer_placeholder)} | {money(budget.immediate_budget_gap)} | "
            f"{budget.budget_stress_band} |"
        )
    return lines


def _reemployment_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Scenario | Months Without Full Income | Interim Recovery | Full Recovery | Re-Employment Risk |",
        "| --- | ---: | ---: | ---: | --- |",
    ]
    for row in rows:
        result = row["reemployment_result"]
        months = "N/A" if result.months_without_full_income is None else str(result.months_without_full_income)
        lines.append(
            "| "
            f"{row['example']['name']} | {months} | {money(result.interim_income_recovery_amount)} | "
            f"{money(result.full_income_recovery_amount)} | {result.reemployment_risk_band} |"
        )
    return lines


def _regional_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Scenario | Regional Score | Regional Band | Drivers |",
        "| --- | ---: | --- | --- |",
    ]
    for row in rows:
        result = row["regional_stress_result"]
        lines.append(
            "| "
            f"{row['example']['name']} | {result.regional_stress_score:.3f} | {result.regional_stress_band} | "
            f"{', '.join(result.drivers) or 'None'} |"
        )
    return lines


def _cliff_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Scenario | Support Loss | Income Gain | Net Position Change | Cliff Detected | Cliff Severity |",
        "| --- | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        result = row["payment_cliff_result"]
        if result is None:
            lines.append(f"| {row['example']['name']} | N/A | N/A | N/A | false | none |")
            continue
        lines.append(
            "| "
            f"{row['example']['name']} | {money(result.support_loss)} | {money(result.income_gain)} | "
            f"{money(result.net_position_change)} | {str(result.cliff_detected).lower()} | {result.cliff_severity_band} |"
        )
    return lines


def _support_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Scenario | Transition Support | Residual Household Gap After Support | Household Shock Band | Primary Risk Drivers |",
        "| --- | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        result = row["scenario_result"]
        lines.append(
            "| "
            f"{row['example']['name']} | {money(result.transition_support_amount)} | "
            f"{money(result.residual_household_gap_after_support)} | {result.household_shock_band} | "
            f"{', '.join(result.primary_risk_drivers) or 'None'} |"
        )
    return lines


def _summary_table(summary: DistributionalSummaryResult) -> list[str]:
    return [
        "| Scenario Count | Low | Medium | High | Critical | Average Residual Gap | Highest-Risk Synthetic Households |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | --- |",
        (
            f"| {summary.scenario_count} | {summary.low_shock_count} | {summary.medium_shock_count} | "
            f"{summary.high_shock_count} | {summary.critical_shock_count} | "
            f"{money(summary.average_residual_gap_placeholder)} | {', '.join(summary.highest_risk_households)} |"
        ),
    ]


def build_markdown(rows: list[dict[str, Any]], summary: DistributionalSummaryResult, metadata: dict[str, Any]) -> str:
    lines = [
        "# CARSF V1.5 Synthetic Household Distributional Scenarios",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report previews synthetic household-level distributional stress for placeholder automation displacement scenarios.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in REPORT_NON_CLAIMS)
    lines.extend(
        [
            "",
            "## C. Why Distributional Scenarios Matter",
            "",
            "National fiscal and transition-payment outputs can hide differences between household types. These synthetic scenarios show how composition, savings buffers, re-employment timing, payment cliffs, and regional stress may change household shock severity. They are not representative household modelling.",
            "",
            "## D. Synthetic Household Table",
            "",
        ]
    )
    lines.extend(_household_table(rows))
    lines.extend(["", "## E. Household Budget Stress", ""])
    lines.extend(_budget_table(rows))
    lines.extend(["", "## F. Re-Employment Timing Risk", ""])
    lines.extend(_reemployment_table(rows))
    lines.extend(["", "## G. Regional Stress", ""])
    lines.extend(_regional_table(rows))
    lines.extend(["", "## H. Payment Cliff Analysis", ""])
    lines.extend(_cliff_table(rows))
    lines.extend(["", "## I. Transition Support and Residual Household Gap", ""])
    lines.extend(_support_table(rows))
    lines.extend(["", "## J. Household Shock Band", ""])
    lines.append("Household shock bands are prototype-only labels that combine budget stress, re-employment timing, regional stress, payment cliff severity, and residual gap after support.")
    lines.append("")
    lines.extend(_support_table(rows))
    lines.extend(["", "## K. Distributional Summary", ""])
    lines.extend(_summary_table(summary))
    lines.extend(["", "## L. Highest-Risk Synthetic Households", ""])
    lines.append(", ".join(summary.highest_risk_households) if summary.highest_risk_households else "None")
    lines.extend(["", "Primary systemic risks: " + (", ".join(summary.primary_systemic_risks) if summary.primary_systemic_risks else "None"), ""])
    lines.extend(["## M. Plain-English Interpretation", ""])
    for row in rows:
        lines.extend(
            [
                f"### {row['example']['name']}",
                "",
                row["example"].get("interpretation", ""),
                "",
                "- Firm-level CARSF liability is not automatically modified by this synthetic distributional scenario.",
                "",
            ]
        )
    lines.extend(
        [
            "## N. Limitations and Calibration Needs",
            "",
            "- All household, income, cost, support, regional, and re-employment values are synthetic illustrative placeholders.",
            "- No real household data, welfare records, income records, ABS, DSS, Services Australia, ATO, Treasury, PBO, HILDA, Census, or household survey data is used.",
            "- Household shock bands, regional stress, and payment cliff warnings are prototype-only labels and not welfare advice, eligibility law, forecasts, or validated distributional modelling.",
            "- Future calibration would require ABS, HILDA, DSS, Services Australia, labour-market, regional, household survey, legal, privacy, Treasury, PBO, and economic review before policy use.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_reports(reports_dir: Path, rows: list[dict[str, Any]]) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    summary = summarise_distributional_scenarios([row["scenario_result"] for row in rows])
    json_path = reports_dir / "distributional_scenarios.json"
    md_path = reports_dir / "distributional_scenarios.md"
    json_path.write_text(
        json.dumps(build_json_payload(rows, summary, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(rows, summary, metadata), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = ArgumentParser(description="Run CARSF synthetic household distributional scenarios.")
    parser.add_argument("--examples-dir", type=Path, default=REPO_ROOT / "examples" / "distributional_scenarios")
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args()

    rows = run_distributional_examples(args.examples_dir)
    json_path, md_path = write_reports(args.reports_dir, rows)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
