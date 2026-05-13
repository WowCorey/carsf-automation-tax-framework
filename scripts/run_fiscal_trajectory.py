"""Run CARSF V1.5 national fiscal trajectory examples."""

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
from carsf.fiscal_sensitivity import FiscalSensitivityResult, run_fiscal_sensitivity  # noqa: E402
from carsf.fiscal_trajectory import (  # noqa: E402
    FISCAL_TRAJECTORY_WARNING,
    FiscalTrajectoryResult,
    run_fiscal_trajectory,
)


REPORT_STATUS = "prototype_fiscal_trajectory_outputs_only"
REPORT_NON_CLAIMS = [
    FISCAL_TRAJECTORY_WARNING,
    "All fiscal values are illustrative placeholders and are not calibrated Australian fiscal data.",
    "National fiscal trajectory outputs do not modify firm-level CARSF liability.",
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
        raise ValueError(f"fiscal trajectory example must be a mapping: {path}")
    return loaded


def example_paths(examples_dir: Path) -> list[Path]:
    if not examples_dir.exists():
        raise FileNotFoundError(f"missing fiscal trajectory example directory: {examples_dir}")
    paths = sorted(examples_dir.glob("*.yaml"))
    if not paths:
        raise FileNotFoundError(f"no fiscal trajectory examples found in {examples_dir}")
    return paths


def validate_placeholder_labels(example: dict[str, Any], path: Path) -> None:
    required_true = ["illustrative_placeholder_only", "not_calibrated", "no_forecast_claim"]
    for key in required_true:
        if example.get(key) is not True:
            raise ValueError(f"{key} must be true in fiscal example: {path}")
    notice = str(example.get("placeholder_notice", "")).lower()
    if "placeholder" not in notice:
        raise ValueError(f"placeholder_notice must clearly label placeholders: {path}")


def run_one_example(path: Path) -> dict[str, Any]:
    example = load_yaml(path)
    validate_placeholder_labels(example, path)
    result = run_fiscal_trajectory(example)
    sensitivity_grid = example.get("sensitivity", {})
    if sensitivity_grid and not isinstance(sensitivity_grid, dict):
        raise ValueError(f"sensitivity must be a mapping: {path}")
    sensitivity = run_fiscal_sensitivity(example, sensitivity_grid) if sensitivity_grid else FiscalSensitivityResult(
        trajectory_id=str(example["trajectory_id"]),
        points=[],
        min_gap=0.0,
        max_gap=0.0,
        warnings=["No sensitivity grid configured."],
    )
    return {
        "fixture_path": str(path.relative_to(REPO_ROOT)),
        "example": example,
        "trajectory_result": result,
        "sensitivity_result": sensitivity,
        "firm_level_liability_modified": False,
    }


def run_fiscal_examples(examples_dir: Path) -> list[dict[str, Any]]:
    return [run_one_example(path) for path in example_paths(examples_dir)]


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
                "trajectory_id": row["example"]["trajectory_id"],
                "name": row["example"]["name"],
                "purpose": row["example"]["purpose"],
                "status": row["example"]["status"],
                "illustrative_placeholder_only": row["example"]["illustrative_placeholder_only"],
                "not_calibrated": row["example"]["not_calibrated"],
                "no_forecast_claim": row["example"]["no_forecast_claim"],
                "trajectory_result": _jsonable(row["trajectory_result"]),
                "sensitivity_result": _jsonable(row["sensitivity_result"]),
                "interpretation": row["example"].get("interpretation", ""),
                "firm_level_liability_modified": row["firm_level_liability_modified"],
            }
            for row in rows
        ],
    }


def _summary_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Example | Years | PAYG Loss | HELP/HECS Loss | Retirement Contribution Pressure | Transfer Pressure | Automation Revenue Captured | Commonwealth Gap | State Pressure | Public-Sector Gap | Broader Pressure | First High | First Critical |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        result: FiscalTrajectoryResult = row["trajectory_result"]
        lines.append(
            "| "
            f"{row['example']['name']} | {result.start_year}-{result.end_year} | "
            f"{money(result.cumulative_payg_loss)} | {money(result.cumulative_help_repayment_loss)} | "
            f"{money(result.cumulative_retirement_contribution_pressure)} | {money(result.cumulative_transfer_pressure)} | "
            f"{money(result.cumulative_automation_revenue_captured)} | "
            f"{money(result.cumulative_commonwealth_gap_after_carsf)} | "
            f"{money(result.cumulative_state_revenue_pressure)} | {money(result.cumulative_total_public_sector_gap)} | "
            f"{money(result.cumulative_broader_labour_linked_pressure)} | "
            f"{result.first_high_warning_year or 'N/A'} | {result.first_critical_warning_year or 'N/A'} |"
        )
    return lines


def _year_table(result: FiscalTrajectoryResult) -> list[str]:
    lines = [
        "| Year | Net Displaced Workers | PAYG Loss | HELP/HECS Loss | Retirement Contribution Pressure | Transfer Pressure | Automation Revenue Captured | Coverage Ratio | Commonwealth Gap | State Pressure | Public-Sector Gap | Broader Pressure | Warning Band |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for year in result.years:
        lines.append(
            "| "
            f"{year.year} | {year.net_displaced_workers:,.2f} | {money(year.payg_revenue_loss)} | "
            f"{money(year.help_repayment_loss)} | {money(year.retirement_contribution_pressure)} | "
            f"{money(year.transfer_pressure)} | {money(year.automation_revenue_captured)} | "
            f"{rate(year.coverage_ratio)} | {money(year.commonwealth_gap_after_carsf)} | "
            f"{money(year.state_payroll_tax_loss)} | {money(year.total_public_sector_gap)} | "
            f"{money(year.broader_labour_linked_pressure)} | {year.warning_band} |"
        )
    return lines


def _sensitivity_table(result: FiscalSensitivityResult) -> list[str]:
    lines = [
        "| Parameter | Value | Cumulative Public-Sector Gap | First High | First Critical |",
        "| --- | ---: | ---: | --- | --- |",
    ]
    for point in result.points:
        lines.append(
            "| "
            f"{point.parameter_name} | {point.parameter_value:,.4f} | {money(point.cumulative_gap)} | "
            f"{point.first_high_warning_year or 'N/A'} | {point.first_critical_warning_year or 'N/A'} |"
        )
    if not result.points:
        lines.append("| N/A | N/A | N/A | N/A | N/A |")
    return lines


def build_markdown(rows: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    lines = [
        "# CARSF V1.5 National Fiscal Trajectory Engine",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report runs deterministic placeholder national fiscal trajectories for PAYG erosion, HELP/HECS repayment loss, retirement-system contribution pressure, transfer-payment pressure, automation revenue captured, and residual fiscal gaps.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in REPORT_NON_CLAIMS)
    lines.extend(
        [
            "",
            "## C. Why Fiscal Trajectory Matters",
            "",
            "CARSF exists because productive capacity may migrate from labour to automation-heavy capital. This national layer tests whether placeholder automation revenue capture tracks PAYG erosion, HELP/HECS repayment loss, support pressure, retirement-system contribution pressure from lost superannuation, GST effects, and state payroll-tax pressure. It does not change firm-level liability.",
            "",
            "Superannuation contribution loss is tracked as retirement-system contribution pressure, not ordinary Commonwealth revenue loss.",
            "",
            "## D. Input Assumptions Summary",
            "",
            "| Example | Displacement Rate | Reabsorption Rate | Support Payment | Placeholder Label |",
            "| --- | ---: | ---: | ---: | --- |",
        ]
    )
    for row in rows:
        workforce = row["example"]["workforce"]
        lines.append(
            "| "
            f"{row['example']['name']} | {rate(workforce['annual_displacement_rate'])} | "
            f"{rate(workforce['annual_reabsorption_rate'])} | "
            f"{money(row['example']['average_support_payment_per_person'])} | "
            f"{row['example']['status']} |"
        )
    lines.extend(["", "## E. Year-by-Year Trajectory Tables", ""])
    for row in rows:
        result: FiscalTrajectoryResult = row["trajectory_result"]
        lines.extend([f"### {row['example']['name']}", ""])
        lines.extend(_year_table(result))
        lines.append("")
    lines.extend(
        [
            "## F. PAYG Erosion, HELP/HECS Loss, and Retirement-System Contribution Pressure",
            "",
            "PAYG loss and HELP/HECS repayment loss are included in Commonwealth fiscal pressure. Superannuation contribution loss is tracked separately as retirement-system contribution pressure, not ordinary Commonwealth revenue loss.",
            "",
        ]
    )
    lines.extend(_summary_table(rows))
    lines.extend(
        [
            "",
            "## G. Transfer-Pressure Estimate",
            "",
            "Transfer pressure is calculated from net displaced workers, placeholder support-payment amounts, retraining shares, and administrative costs. This is not a UBI, welfare, or transition-payment design module.",
            "",
            "## H. Automation Revenue Captured",
            "",
            "Automation revenue captured is supplied as a placeholder national input for each year. It is not derived from real tax collections or calibrated firm-level CARSF liabilities.",
            "",
            "## I. Residual Commonwealth Gap",
            "",
            "Residual Commonwealth gap equals placeholder Commonwealth revenue/cashflow pressure before CARSF minus automation revenue captured, plus transfer pressure. It excludes superannuation contribution loss.",
            "",
            "## J. State Revenue Pressure and Broader Labour-Linked Pressure",
            "",
            "Total public-sector gap adds placeholder state payroll-tax pressure to the Commonwealth gap. Broader labour-linked pressure adds retirement-system contribution pressure as a separate broader pressure measure. It is not an intergovernmental fiscal model and not ordinary Commonwealth revenue loss.",
            "",
            "## K. Coverage Ratio",
            "",
            "Coverage ratio is calculated as automation revenue captured divided by PAYG loss plus transfer pressure where that denominator is positive. It is `N/A` when the denominator is zero.",
            "",
            "## L. First High/Critical Warning Year",
            "",
            "| Example | First High Warning Year | First Critical Warning Year |",
            "| --- | --- | --- |",
        ]
    )
    for row in rows:
        result = row["trajectory_result"]
        lines.append(
            "| "
            f"{row['example']['name']} | {result.first_high_warning_year or 'N/A'} | "
            f"{result.first_critical_warning_year or 'N/A'} |"
        )
    lines.extend(["", "## M. Sensitivity Sweep Summary", ""])
    for row in rows:
        lines.extend([f"### {row['example']['name']}", ""])
        lines.extend(_sensitivity_table(row["sensitivity_result"]))
        lines.append("")
    lines.extend(["## N. Limitations and Calibration Needs", ""])
    for row in rows:
        lines.extend(
            [
                f"### {row['example']['name']}",
                "",
                row["example"].get("interpretation", ""),
                "",
                "- Values are illustrative placeholders only.",
                "- No fiscal forecast, government revenue estimate, or public-costing claim is made.",
                "- Firm-level CARSF liability is not automatically changed by this trajectory result.",
                "",
            ]
        )
    lines.extend(
        [
            "Required future calibration includes Treasury, ATO, ABS, DSS, PBO, state payroll tax, superannuation, HELP/HECS, labour-market, and transfer-payment datasets plus legal and economic review.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_reports(reports_dir: Path, rows: list[dict[str, Any]]) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "fiscal_trajectory.json"
    md_path = reports_dir / "fiscal_trajectory.md"
    json_path.write_text(
        json.dumps(build_json_payload(rows, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(rows, metadata), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = ArgumentParser(description="Run CARSF national fiscal trajectory examples.")
    parser.add_argument("--examples-dir", type=Path, default=REPO_ROOT / "examples" / "fiscal_trajectory")
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args()

    rows = run_fiscal_examples(args.examples_dir)
    json_path, md_path = write_reports(args.reports_dir, rows)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
