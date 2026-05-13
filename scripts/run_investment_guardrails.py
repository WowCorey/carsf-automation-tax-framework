"""Run CARSF V1.5 investment, incidence, and burden guardrails."""

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

from carsf.burden_balance import BurdenBalanceResult, evaluate_burden_balance  # noqa: E402
from carsf.example_runner import report_metadata  # noqa: E402
from carsf.incidence import IncidenceResult, evaluate_tax_incidence  # noqa: E402
from carsf.investment import InvestmentGuardrailResult, evaluate_investment_guardrail  # noqa: E402
from carsf.sensitivity import (  # noqa: E402
    SensitivitySweepResult,
    sweep_aava,
    sweep_liability_cap,
    sweep_pass_through,
)


REPORT_WARNING = (
    "These are prototype investment and tax-incidence guardrails only. They are not economic validation, "
    "investment advice, Treasury modelling, ATO guidance, legal advice, market forecasting, or tax advice."
)
REPORT_STATUS = "prototype_investment_incidence_guardrails_only"
REPORT_NON_CLAIMS = [
    REPORT_WARNING,
    "Guardrail outputs do not automatically modify final liability.",
    "Pass-through, burden, normal-return, and sensitivity values are illustrative placeholders requiring calibration.",
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
        raise ValueError(f"investment guardrail example must be a mapping: {path}")
    return loaded


def example_paths(examples_dir: Path) -> list[Path]:
    if not examples_dir.exists():
        raise FileNotFoundError(f"missing investment guardrail example directory: {examples_dir}")
    paths = sorted(examples_dir.glob("*.yaml"))
    if not paths:
        raise FileNotFoundError(f"no investment guardrail examples found in {examples_dir}")
    return paths


def validate_placeholder_labels(example: dict[str, Any], path: Path) -> None:
    status = str(example.get("status", "")).lower()
    notice = str(example.get("placeholder_notice", "")).lower()
    if "placeholder" not in status:
        raise ValueError(f"example status must be placeholder-labelled: {path}")
    if "placeholder" not in notice:
        raise ValueError(f"example placeholder_notice must be placeholder-labelled: {path}")
    assumption = example.get("incidence_assumption", {})
    if not isinstance(assumption, dict) or assumption.get("illustrative_placeholder_only") is not True:
        raise ValueError(f"incidence assumption must be illustrative_placeholder_only: true: {path}")


def run_one_example(path: Path) -> dict[str, Any]:
    example = load_yaml(path)
    validate_placeholder_labels(example, path)
    example_id = str(example["example_id"])
    investment_inputs = dict(example["investment_inputs"])
    investment_inputs.setdefault("example_id", example_id)
    investment_result = evaluate_investment_guardrail(investment_inputs)
    incidence_result = evaluate_tax_incidence(
        investment_inputs.get("final_liability", investment_inputs.get("liability", 0.0)),
        example["incidence_assumption"],
    )
    burden_inputs = dict(example.get("burden_balance", {}))
    burden_inputs.setdefault("final_liability", investment_inputs.get("final_liability", 0.0))
    burden_inputs.setdefault("aava", investment_inputs.get("aava", 0.0))
    burden_result = evaluate_burden_balance(burden_inputs)
    sensitivity = example.get("sensitivity", {})
    if not isinstance(sensitivity, dict):
        raise ValueError(f"sensitivity must be a mapping: {path}")
    final_liability = float(investment_inputs.get("final_liability", 0.0))
    aava = float(investment_inputs.get("aava", 0.0))
    raw_liability = float(sensitivity.get("raw_liability", final_liability))
    sweeps = [
        sweep_pass_through(final_liability, list(sensitivity.get("pass_through_rates", [])), example_id=example_id),
        sweep_liability_cap(max(0.0, aava), raw_liability, list(sensitivity.get("cap_rates", [])), example_id=example_id),
        sweep_aava(final_liability, list(sensitivity.get("aava_values", [])), example_id=example_id),
    ]
    return {
        "fixture_path": str(path.relative_to(REPO_ROOT)),
        "example": example,
        "investment_result": investment_result,
        "incidence_result": incidence_result,
        "burden_balance_result": burden_result,
        "sensitivity_sweeps": sweeps,
        "final_liability_modified": False,
    }


def run_investment_guardrails(examples_dir: Path) -> list[dict[str, Any]]:
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
                "example_id": row["example"]["example_id"],
                "name": row["example"]["name"],
                "sector": row["example"]["sector"],
                "status": row["example"]["status"],
                "investment_inputs": row["example"]["investment_inputs"],
                "incidence_assumption": row["example"]["incidence_assumption"],
                "investment_result": _jsonable(row["investment_result"]),
                "incidence_result": _jsonable(row["incidence_result"]),
                "burden_balance_result": _jsonable(row["burden_balance_result"]),
                "sensitivity_sweeps": [_jsonable(sweep) for sweep in row["sensitivity_sweeps"]],
                "interpretation": row["example"].get("interpretation", ""),
                "final_liability_modified": row["final_liability_modified"],
                "non_claims": row["example"].get("non_claims", []),
            }
            for row in rows
        ],
    }


def _summary_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Example | Sector | Liability | AAVA | Effective Burden | Liability/Revenue | Investment Risk | Incidence Risk | Burden Balance | Final Liability Modified |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |",
    ]
    for row in rows:
        example = row["example"]
        investment: InvestmentGuardrailResult = row["investment_result"]
        incidence: IncidenceResult = row["incidence_result"]
        burden: BurdenBalanceResult = row["burden_balance_result"]
        lines.append(
            "| "
            f"{example['name']} | {example['sector']} | "
            f"{money(example['investment_inputs']['final_liability'])} | {money(example['investment_inputs']['aava'])} | "
            f"{rate(investment.effective_burden_rate)} | {rate(investment.liability_to_revenue_rate)} | "
            f"{investment.investment_risk_band} | {incidence.incidence_risk_band} | "
            f"{burden.burden_balance_band} | {str(row['final_liability_modified']).lower()} |"
        )
    return lines


def _sweep_summary(row: dict[str, Any]) -> list[str]:
    lines = [
        "| Sweep | Points | Min Liability | Max Liability |",
        "| --- | ---: | ---: | ---: |",
    ]
    for sweep in row["sensitivity_sweeps"]:
        lines.append(
            "| "
            f"{sweep.sweep_name} | {len(sweep.points)} | {money(sweep.min_liability)} | {money(sweep.max_liability)} |"
        )
    return lines


def build_markdown(rows: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    lines = [
        "# CARSF V1.5 Investment and Tax-Incidence Guardrails",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report previews non-operative guardrails for effective automation burden, normal-return preservation, tax-incidence pressure, investment-deterrence review, and under-capture / over-capture risk.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in REPORT_NON_CLAIMS)
    lines.extend(
        [
            "",
            "## C. Why Investment/Tax-Incidence Guardrails Matter",
            "",
            "A prototype automation fiscal framework can be too weak, too punitive, or shifted onto consumers, workers, suppliers, or ordinary capital. These checks are designed to surface that review problem without changing final liability.",
            "",
            "## D. Effective Burden Table",
            "",
        ]
    )
    lines.extend(_summary_table(rows))
    lines.extend(
        [
            "",
            "## E. Normal Return Preservation Preview",
            "",
            "| Example | Preserved Return Amount | Normal Return Preserved | Main Reason |",
            "| --- | ---: | --- | --- |",
        ]
    )
    for row in rows:
        investment: InvestmentGuardrailResult = row["investment_result"]
        lines.append(
            "| "
            f"{row['example']['name']} | {money(investment.preserved_return_amount)} | "
            f"{investment.normal_return_preserved} | {investment.reasons[0] if investment.reasons else 'No reason recorded.'} |"
        )
    lines.extend(
        [
            "",
            "## F. Consumer/Worker/Supplier/Capital Incidence Preview",
            "",
            "| Example | Consumer | Worker | Supplier | Capital | Allocation Gap | Risk Band |",
            "| --- | ---: | ---: | ---: | ---: | ---: | --- |",
        ]
    )
    for row in rows:
        incidence: IncidenceResult = row["incidence_result"]
        lines.append(
            "| "
            f"{row['example']['name']} | {money(incidence.consumer_pass_through_amount)} | "
            f"{money(incidence.worker_pressure_amount)} | {money(incidence.supplier_pressure_amount)} | "
            f"{money(incidence.capital_absorption_amount)} | {money(incidence.allocation_gap)} | "
            f"{incidence.incidence_risk_band} |"
        )
    lines.extend(
        [
            "",
            "## G. Under-Capture / Over-Capture Review",
            "",
            "Firm-level zero-liability under-capture warning and public-revenue burden-balance are separate prototype checks. A case can have no firm-level zero-liability warning while still showing public-revenue under-capture.",
            "",
            "| Example | Coverage Ratio | Capture Gap | Band | Review Required |",
            "| --- | ---: | ---: | --- | --- |",
        ]
    )
    for row in rows:
        burden: BurdenBalanceResult = row["burden_balance_result"]
        lines.append(
            "| "
            f"{row['example']['name']} | {rate(burden.coverage_ratio)} | {money(burden.capture_gap)} | "
            f"{burden.burden_balance_band} | {str(burden.review_required).lower()} |"
        )
    lines.extend(
        [
            "",
            "## H. Sensitivity Sweep Summary",
            "",
        ]
    )
    for row in rows:
        lines.extend([f"### {row['example']['name']}", ""])
        lines.extend(_sweep_summary(row))
        lines.append("")
    lines.extend(
        [
            "## I. Example-by-Example Plain-English Interpretation",
            "",
            "Firm-level zero-liability under-capture warning and public-revenue burden-balance are separate prototype checks. A case can have no firm-level zero-liability warning while still showing public-revenue under-capture.",
            "",
        ]
    )
    for row in rows:
        investment: InvestmentGuardrailResult = row["investment_result"]
        burden: BurdenBalanceResult = row["burden_balance_result"]
        lines.extend(
            [
                f"### {row['example']['name']}",
                "",
                row["example"].get("interpretation", ""),
                "",
                f"- Investment risk band: `{investment.investment_risk_band}`",
                f"- Over-capture warning: `{str(investment.over_capture_warning).lower()}`",
                f"- Firm-level zero-liability under-capture warning: `{str(investment.under_capture_warning).lower()}`",
                f"- Public-revenue burden-balance band: `{burden.burden_balance_band}`",
                "- Final liability modified by this report: `false`",
                "",
            ]
        )
    lines.extend(
        [
            "## J. Limitations and Future Calibration Needs",
            "",
            "- Pass-through, worker pressure, supplier pressure, and capital absorption rates are illustrative placeholders.",
            "- Normal-return proxies are placeholders and are not calibrated sector returns.",
            "- Public-revenue coverage inputs are not official national damage estimates.",
            "- The guardrails do not prove investment deterrence, over-capture, under-capture, or pass-through.",
            "- Future calibration requires Treasury/economic/tax-incidence modelling and legal/tax review.",
            "- Final liability is not automatically modified by these guardrails.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_reports(reports_dir: Path, rows: list[dict[str, Any]]) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "investment_guardrails.json"
    md_path = reports_dir / "investment_guardrails.md"
    json_path.write_text(
        json.dumps(build_json_payload(rows, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(rows, metadata), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = ArgumentParser(description="Run CARSF investment and tax-incidence guardrails.")
    parser.add_argument("--examples-dir", type=Path, default=REPO_ROOT / "examples" / "investment_guardrails")
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args()

    rows = run_investment_guardrails(args.examples_dir)
    json_path, md_path = write_reports(args.reports_dir, rows)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
