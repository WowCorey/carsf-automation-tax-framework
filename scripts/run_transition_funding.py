"""Run CARSF V1.5 transition-payment funding previews."""

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

from carsf.example_runner import report_metadata  # noqa: E402
from carsf.fiscal_trajectory import FiscalTrajectoryResult, run_fiscal_trajectory  # noqa: E402
from carsf.payment_portfolio import PaymentPortfolioResult, evaluate_payment_portfolio  # noqa: E402
from carsf.payment_sensitivity import PaymentSensitivityResult, run_payment_sensitivity  # noqa: E402
from carsf.transition_funding import TransitionFundingResult, run_transition_funding  # noqa: E402
from carsf.transition_payments import TRANSITION_PAYMENT_WARNING, transition_design_from_mapping  # noqa: E402


REPORT_STATUS = "prototype_transition_payment_funding_outputs_only"
REPORT_NON_CLAIMS = [
    TRANSITION_PAYMENT_WARNING,
    "All payment designs and population values are illustrative placeholders and are not calibrated welfare settings.",
    "Transition-payment funding outputs do not modify firm-level CARSF liability.",
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
        raise ValueError(f"transition funding example must be a mapping: {path}")
    return loaded


def example_paths(examples_dir: Path) -> list[Path]:
    if not examples_dir.exists():
        raise FileNotFoundError(f"missing transition payment example directory: {examples_dir}")
    paths = sorted(examples_dir.glob("*.yaml"))
    if not paths:
        raise FileNotFoundError(f"no transition payment examples found in {examples_dir}")
    return paths


def validate_placeholder_labels(example: dict[str, Any], path: Path) -> None:
    required_true = ["illustrative_placeholder_only", "not_calibrated", "no_policy_claim", "no_welfare_advice"]
    for key in required_true:
        if example.get(key) is not True:
            raise ValueError(f"{key} must be true in transition payment example: {path}")
    notice = str(example.get("placeholder_notice", "")).lower()
    if "placeholder" not in notice:
        raise ValueError(f"placeholder_notice must clearly label placeholders: {path}")


def _fiscal_example_path(example: dict[str, Any], fiscal_examples_dir: Path) -> Path:
    fiscal_name = str(example["fiscal_trajectory_example"])
    return fiscal_examples_dir / f"{fiscal_name}.yaml"


def _year_row(fiscal_result: FiscalTrajectoryResult, year: int) -> dict[str, Any]:
    for row in fiscal_result.years:
        if row.year == year:
            return row.to_jsonable()
    raise ValueError(f"fiscal trajectory does not include requested portfolio_year {year}")


def _population_by_year(fiscal_result: FiscalTrajectoryResult, population_base: float) -> dict[int, float]:
    return {year.year: float(population_base) for year in fiscal_result.years}


def run_one_example(path: Path, fiscal_examples_dir: Path) -> dict[str, Any]:
    example = load_yaml(path)
    validate_placeholder_labels(example, path)
    fiscal_example = load_yaml(_fiscal_example_path(example, fiscal_examples_dir))
    fiscal_result = run_fiscal_trajectory(fiscal_example)
    portfolio_year = int(example["portfolio_year"])
    selected_year = _year_row(fiscal_result, portfolio_year)
    designs = [transition_design_from_mapping(item) for item in example["payment_designs"]]
    portfolio_input = {
        "portfolio_id": example["example_id"],
        "year": portfolio_year,
        "population_base": example["population_base"],
        "displaced_workers": selected_year["net_displaced_workers"],
        "designs": [design.to_jsonable() for design in designs],
        "automation_revenue_available": selected_year["automation_revenue_captured"],
        "commonwealth_gap_after_carsf": selected_year["commonwealth_gap_after_carsf"],
        "placeholder_basis": [f"transition funding example: {example['example_id']}"],
    }
    portfolio_result = evaluate_payment_portfolio(portfolio_input)
    funding_result = run_transition_funding(
        {
            "funding_id": example["example_id"],
            "fiscal_trajectory": fiscal_result.to_jsonable(),
            "payment_designs_by_year": {0: [design.to_jsonable() for design in designs]},
            "population_base_by_year": _population_by_year(fiscal_result, float(example["population_base"])),
            "placeholder_basis": [f"transition funding example: {example['example_id']}"],
        }
    )
    sensitivity_grid = example.get("sensitivity", {})
    if sensitivity_grid and not isinstance(sensitivity_grid, dict):
        raise ValueError(f"sensitivity must be a mapping: {path}")
    sensitivity_result = run_payment_sensitivity(portfolio_input, sensitivity_grid) if sensitivity_grid else PaymentSensitivityResult(
        sensitivity_id=str(example["example_id"]),
        points=[],
        min_residual_gap=0.0,
        max_residual_gap=0.0,
        warnings=["No payment sensitivity grid configured."],
    )
    return {
        "fixture_path": str(path.relative_to(REPO_ROOT)),
        "example": example,
        "fiscal_trajectory_id": fiscal_result.trajectory_id,
        "portfolio_input": portfolio_input,
        "portfolio_result": portfolio_result,
        "funding_result": funding_result,
        "sensitivity_result": sensitivity_result,
        "firm_level_liability_modified": False,
    }


def run_transition_examples(examples_dir: Path, fiscal_examples_dir: Path) -> list[dict[str, Any]]:
    return [run_one_example(path, fiscal_examples_dir) for path in example_paths(examples_dir)]


def build_json_payload(rows: list[dict[str, Any]], metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": REPORT_NON_CLAIMS,
        },
        "examples": [
            {
                "fixture_path": row["fixture_path"],
                "example_id": row["example"]["example_id"],
                "name": row["example"]["name"],
                "purpose": row["example"]["purpose"],
                "status": row["example"]["status"],
                "fiscal_trajectory_id": row["fiscal_trajectory_id"],
                "portfolio_input": row["portfolio_input"],
                "portfolio_result": _jsonable(row["portfolio_result"]),
                "funding_result": _jsonable(row["funding_result"]),
                "sensitivity_result": _jsonable(row["sensitivity_result"]),
                "interpretation": row["example"].get("interpretation", ""),
                "firm_level_liability_modified": row["firm_level_liability_modified"],
            }
            for row in rows
        ],
    }


def _portfolio_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Example | Fiscal Trajectory | Year | Program Cost | Automation Revenue Available | Coverage | Residual Payment Gap | Combined Gap | Affordability Band | Final Liability Modified |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        result: PaymentPortfolioResult = row["portfolio_result"]
        lines.append(
            "| "
            f"{row['example']['name']} | {row['fiscal_trajectory_id']} | {result.year} | "
            f"{money(result.total_program_cost)} | {money(result.automation_revenue_available)} | "
            f"{rate(result.funding_coverage_ratio)} | {money(result.residual_funding_gap)} | "
            f"{money(result.residual_commonwealth_gap_plus_payment_gap)} | {result.affordability_band} | "
            f"{str(row['firm_level_liability_modified']).lower()} |"
        )
    return lines


def _design_table(result: PaymentPortfolioResult) -> list[str]:
    lines = [
        "| Design | Eligible People | Covered People | Base Payment | Retraining | Admin | Total Cost |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for design in result.design_results:
        lines.append(
            "| "
            f"{design.design_id} | {design.eligible_people:,.2f} | {design.covered_people:,.2f} | "
            f"{money(design.base_payment_cost)} | {money(design.retraining_component_cost)} | "
            f"{money(design.administrative_cost)} | {money(design.total_program_cost)} |"
        )
    return lines


def _funding_year_table(result: TransitionFundingResult) -> list[str]:
    lines = [
        "| Year | Net Displaced Workers | Automation Revenue | Payment Cost | Coverage | Residual Payment Gap | Combined Gap | Cliff Risk |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for year in result.years:
        lines.append(
            "| "
            f"{year.year} | {year.net_displaced_workers:,.2f} | {money(year.automation_revenue_captured)} | "
            f"{money(year.total_payment_cost)} | {rate(year.funding_coverage_ratio)} | "
            f"{money(year.residual_payment_gap)} | {money(year.combined_gap)} | {year.cliff_risk_band} |"
        )
    return lines


def _sensitivity_table(result: PaymentSensitivityResult) -> list[str]:
    lines = [
        "| Parameter | Value | Program Cost | Coverage | Residual Gap | Affordability Band |",
        "| --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for point in result.points:
        lines.append(
            "| "
            f"{point.parameter_name} | {point.parameter_value:,.4f} | {money(point.total_program_cost)} | "
            f"{rate(point.funding_coverage_ratio)} | {money(point.residual_funding_gap)} | "
            f"{point.affordability_band} |"
        )
    if not result.points:
        lines.append("| N/A | N/A | N/A | N/A | N/A | N/A |")
    return lines


def build_markdown(rows: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    lines = [
        "# CARSF V1.5 Transition-Payment Funding Preview",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report previews non-operative transition-payment and UBI-lite funding options against placeholder automation revenue captured and national fiscal trajectory outputs.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in REPORT_NON_CLAIMS)
    lines.extend(
        [
            "",
            "## C. Why Transition Funding Matters",
            "",
            "A national fiscal trajectory can identify displacement and residual gaps, but a human-support layer is needed to preview whether automation revenue could fund displaced-worker supplements, retraining support, UBI-lite, automation-dividend, or hybrid packages. These outputs are not policy recommendations and do not change firm-level liability.",
            "",
            "## D. Payment Design Comparison Table",
            "",
        ]
    )
    lines.extend(_portfolio_table(rows))
    lines.extend(["", "## E. Year-by-Year Funding Trajectory", ""])
    for row in rows:
        lines.extend([f"### {row['example']['name']}", ""])
        lines.extend(_funding_year_table(row["funding_result"]))
        lines.append("")
    lines.extend(
        [
            "## F. Automation Revenue Available",
            "",
            "Automation revenue available is taken from the selected fiscal trajectory as a placeholder transition-funding source. It is not real CARSF collections.",
            "",
            "## G. Payment Cost",
            "",
        ]
    )
    for row in rows:
        lines.extend([f"### {row['example']['name']}", ""])
        lines.extend(_design_table(row["portfolio_result"]))
        lines.append("")
    lines.extend(
        [
            "## H. Residual Payment Gap",
            "",
            "Residual payment gap is `max(0, total payment cost - automation revenue available)`.",
            "",
            "## I. Combined Commonwealth/Payment Gap",
            "",
            "Combined gap adds the residual payment gap to the placeholder Commonwealth gap after CARSF. It is not a government budget estimate.",
            "",
            "## J. Cliff-Risk Warning",
            "",
            "| Example | First High Cliff Risk | First Critical Cliff Risk | Cumulative Payment Cost | Cumulative Residual Gap | Cumulative Combined Gap |",
            "| --- | --- | --- | ---: | ---: | ---: |",
        ]
    )
    for row in rows:
        result: TransitionFundingResult = row["funding_result"]
        lines.append(
            "| "
            f"{row['example']['name']} | {result.first_high_cliff_risk_year or 'N/A'} | "
            f"{result.first_critical_cliff_risk_year or 'N/A'} | {money(result.cumulative_payment_cost)} | "
            f"{money(result.cumulative_residual_payment_gap)} | {money(result.cumulative_combined_gap)} |"
        )
    lines.extend(["", "## K. Sensitivity Sweep Summary", ""])
    for row in rows:
        lines.extend([f"### {row['example']['name']}", ""])
        lines.extend(_sensitivity_table(row["sensitivity_result"]))
        lines.append("")
    lines.extend(["## L. Plain-English Interpretation", ""])
    for row in rows:
        lines.extend(
            [
                f"### {row['example']['name']}",
                "",
                row["example"].get("interpretation", ""),
                "",
                "- Firm-level CARSF liability is not automatically modified by this transition-funding preview.",
                "",
            ]
        )
    lines.extend(
        [
            "## M. Limitations and Calibration Needs",
            "",
            "- All payment amounts, participation rates, population bases, and administrative costs are illustrative placeholders.",
            "- No UBI policy, welfare advice, DSS modelling, Services Australia modelling, Treasury costing, PBO costing, legal advice, tax advice, or economic validation is claimed.",
            "- Future calibration requires welfare, population, labour-market, fiscal, and legal review before any policy use.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_reports(reports_dir: Path, rows: list[dict[str, Any]]) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "transition_funding.json"
    md_path = reports_dir / "transition_funding.md"
    json_path.write_text(
        json.dumps(build_json_payload(rows, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(rows, metadata), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = ArgumentParser(description="Run CARSF transition-payment funding previews.")
    parser.add_argument("--examples-dir", type=Path, default=REPO_ROOT / "examples" / "transition_payments")
    parser.add_argument("--fiscal-examples-dir", type=Path, default=REPO_ROOT / "examples" / "fiscal_trajectory")
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args()

    rows = run_transition_examples(args.examples_dir, args.fiscal_examples_dir)
    json_path, md_path = write_reports(args.reports_dir, rows)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
