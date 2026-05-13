"""Run CARSF V1.5 payment interaction and targeting previews."""

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
from carsf.payment_interactions import PAYMENT_INTERACTION_WARNING, evaluate_payment_interactions  # noqa: E402


REPORT_STATUS = "prototype_payment_interaction_outputs_only"
REPORT_NON_CLAIMS = [
    PAYMENT_INTERACTION_WARNING,
    "All targeting, phase, household, and support-incidence values are illustrative placeholders.",
    "Support incidence offsets are not validated savings.",
    "Payment interaction outputs do not modify firm-level CARSF liability.",
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
        raise ValueError(f"payment interaction example must be a mapping: {path}")
    return loaded


def example_paths(examples_dir: Path) -> list[Path]:
    if not examples_dir.exists():
        raise FileNotFoundError(f"missing payment interaction example directory: {examples_dir}")
    paths = sorted(examples_dir.glob("*.yaml"))
    if not paths:
        raise FileNotFoundError(f"no payment interaction examples found in {examples_dir}")
    return paths


def validate_placeholder_labels(example: dict[str, Any], path: Path) -> None:
    required_true = [
        "illustrative_placeholder_only",
        "not_calibrated",
        "no_policy_claim",
        "no_welfare_advice",
        "synthetic_placeholder_only",
    ]
    for key in required_true:
        if example.get(key) is not True:
            raise ValueError(f"{key} must be true in payment interaction example: {path}")
    notice = str(example.get("placeholder_notice", "")).lower()
    if "placeholder" not in notice:
        raise ValueError(f"placeholder_notice must clearly label placeholders: {path}")


def _interaction_input(example: dict[str, Any]) -> dict[str, Any]:
    return {
        "interaction_id": example["example_id"],
        "year": example["year"],
        "baseline": example["baseline"],
        "target_population": example["target_population"],
        "phase_rule": example["phase_rule"],
        "stack_components": example["stack_components"],
        "support_incidence_assumption": example["support_incidence_assumption"],
        "automation_revenue_available": example["automation_revenue_available"],
        "commonwealth_gap_after_carsf": example["commonwealth_gap_after_carsf"],
        "placeholder_basis": [f"payment interaction example: {example['example_id']}"],
    }


def run_one_example(path: Path) -> dict[str, Any]:
    example = load_yaml(path)
    validate_placeholder_labels(example, path)
    interaction_input = _interaction_input(example)
    result = evaluate_payment_interactions(interaction_input)
    return {
        "fixture_path": str(path.relative_to(REPO_ROOT)),
        "example": example,
        "interaction_input": interaction_input,
        "interaction_result": result,
        "firm_level_liability_modified": False,
    }


def run_payment_interaction_examples(examples_dir: Path) -> list[dict[str, Any]]:
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
                "purpose": row["example"]["purpose"],
                "status": row["example"]["status"],
                "interaction_input": row["interaction_input"],
                "interaction_result": _jsonable(row["interaction_result"]),
                "interpretation": row["example"].get("interpretation", ""),
                "firm_level_liability_modified": row["firm_level_liability_modified"],
            }
            for row in rows
        ],
    }


def _summary_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Example | Baseline Cost | Targeted Eligible People | Phase Multiplier | Gross Stack Cost | Double-Count Adjustment | Net Stack Cost | Residual Support Gap | Interaction Risk | Final Liability Modified |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        result = row["interaction_result"]
        lines.append(
            "| "
            f"{row['example']['name']} | {money(result.baseline_cost)} | {result.targeted_eligible_people:,.2f} | "
            f"{result.phase_multiplier:.2f} | {money(result.gross_stack_cost)} | {money(result.double_count_adjustment)} | "
            f"{money(result.net_stack_cost)} | {money(result.residual_support_gap)} | {result.interaction_risk_band} | "
            f"{str(row['firm_level_liability_modified']).lower()} |"
        )
    return lines


def _baseline_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Example | Existing Eligible Population | Support Per Person | Admin Per Person | Existing Baseline Cost | New Stack Cost |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        baseline = row["interaction_input"]["baseline"]
        result = row["interaction_result"]
        lines.append(
            "| "
            f"{row['example']['name']} | {float(baseline['eligible_population']):,.2f} | "
            f"{money(float(baseline['average_existing_support_per_person']))} | "
            f"{money(float(baseline.get('existing_admin_cost_per_person', 0.0)))} | "
            f"{money(result.baseline_cost)} | {money(result.net_stack_cost)} |"
        )
    return lines


def _targeting_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Example | Target Group | Displaced Required | Retraining Required | Household Test Placeholder | Income Test Placeholder | Eligible People | Targeting Risk |",
        "| --- | --- | --- | --- | --- | --- | ---: | --- |",
    ]
    for row in rows:
        criteria = row["interaction_input"]["target_population"]["criteria"]
        result = row["interaction_result"]
        lines.append(
            "| "
            f"{row['example']['name']} | {criteria.get('target_group', '')} | {criteria.get('displaced_worker_required')} | "
            f"{criteria.get('retraining_required')} | {criteria.get('household_test_placeholder')} | "
            f"{criteria.get('income_test_placeholder')} | {result.targeted_eligible_people:,.2f} | "
            f"{result.targeting_risk_band} |"
        )
    return lines


def _phase_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Example | Year | Phase-In Start | Phase-In End | Phase-Out Start | Phase-Out End | Phase Multiplier |",
        "| --- | ---: | ---: | ---: | --- | --- | ---: |",
    ]
    for row in rows:
        phase = row["interaction_input"]["phase_rule"]
        result = row["interaction_result"]
        lines.append(
            "| "
            f"{row['example']['name']} | {row['interaction_input']['year']} | {phase['phase_in_start_year']} | "
            f"{phase['phase_in_end_year']} | {phase.get('phase_out_start_year') or 'N/A'} | "
            f"{phase.get('phase_out_end_year') or 'N/A'} | {result.phase_multiplier:.2f} |"
        )
    return lines


def _stack_detail(row: dict[str, Any]) -> list[str]:
    lines = [
        "| Component | Type | Eligible People | Payment Per Person | Priority | Phase Multiplier | Mutually Exclusive With |",
        "| --- | --- | ---: | ---: | ---: | ---: | --- |",
    ]
    for component in row["interaction_input"]["stack_components"]:
        lines.append(
            "| "
            f"{component['component_id']} | {component.get('component_type', '')} | {float(component['eligible_people']):,.2f} | "
            f"{money(float(component['payment_per_person']))} | {int(component.get('stack_priority', 0))} | "
            f"{float(component.get('phase_multiplier', 1.0)):.2f} | {', '.join(component.get('mutually_exclusive_with', [])) or 'None'} |"
        )
    return lines


def _support_incidence_table(rows: list[dict[str, Any]]) -> list[str]:
    lines = [
        "| Example | Gross Support Cost | Household Spending Flow | Placeholder GST Recovery | Hardship Offset Preview | Net Fiscal Cost After Placeholder Offsets |",
        "| --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        incidence = row["interaction_result"].support_incidence
        lines.append(
            "| "
            f"{row['example']['name']} | {money(incidence['gross_support_cost'])} | "
            f"{money(incidence['household_spending_flow'])} | {money(incidence['placeholder_gst_recovery'])} | "
            f"{money(incidence['hardship_offset_preview'])} | "
            f"{money(incidence['net_fiscal_cost_after_placeholder_offsets'])} |"
        )
    return lines


def build_markdown(rows: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    lines = [
        "# CARSF V1.5 Payment Interactions and Targeting Preview",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report previews how existing transfer baselines, targeting criteria, phase rules, payment stacks, double-counting prevention, and support fiscal incidence may interact in the CARSF transition-payment prototype.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in REPORT_NON_CLAIMS)
    lines.extend(
        [
            "",
            "## C. Why Payment Interactions Matter",
            "",
            "Transition funding should not double-count existing transfer support, imply final eligibility law, or treat placeholder fiscal offsets as savings. This layer keeps new transition-payment stack costs separate from existing baselines and shows review flags where targeting or household eligibility is unresolved.",
            "",
            "## D. Existing Transfer Baseline Separation",
            "",
        ]
    )
    lines.extend(_baseline_table(rows))
    lines.extend(["", "## E. Targeting Summary", ""])
    lines.extend(_targeting_table(rows))
    lines.extend(["", "## F. Phase-In / Phase-Out Summary", ""])
    lines.extend(_phase_table(rows))
    lines.extend(["", "## G. Payment Stack and Double-Counting Review", ""])
    for row in rows:
        result = row["interaction_result"]
        lines.extend(
            [
                f"### {row['example']['name']}",
                "",
                f"Gross stack cost before interactions: `{money(result.gross_stack_cost)}`",
                "",
                f"Double-count adjustment: `{money(result.double_count_adjustment)}`",
                "",
                f"Net stack cost after interactions: `{money(result.net_stack_cost)}`",
                "",
            ]
        )
        lines.extend(_stack_detail(row))
        lines.append("")
    lines.extend(["## H. Support Fiscal Incidence Preview", ""])
    lines.append("Support incidence offsets are shown separately and are not validated savings.")
    lines.append("")
    lines.extend(_support_incidence_table(rows))
    lines.extend(
        [
            "",
            "## I. Residual Support Gap",
            "",
            "Residual support gap is `max(0, net stack cost - automation revenue available)`.",
            "",
            "## J. Combined Commonwealth/Support Gap",
            "",
            "Combined gap adds the residual support gap to the placeholder Commonwealth gap after CARSF. It is not a budget estimate.",
            "",
            "## K. Targeting and Interaction Risk Bands",
            "",
        ]
    )
    lines.extend(_summary_table(rows))
    lines.extend(["", "## L. Plain-English Interpretation", ""])
    for row in rows:
        lines.extend(
            [
                f"### {row['example']['name']}",
                "",
                row["example"].get("interpretation", ""),
                "",
                "- Firm-level CARSF liability is not automatically modified by this payment-interaction preview.",
                "",
            ]
        )
    lines.extend(
        [
            "## M. Limitations and Calibration Needs",
            "",
            "- All payment, eligibility, household, targeting, phase-rule, and support-incidence values are illustrative placeholders.",
            "- No UBI policy, welfare advice, eligibility law, Centrelink/DSS/Services Australia modelling, Treasury costing, PBO costing, legal advice, tax advice, or economic validation is claimed.",
            "- Future work requires welfare, household, population, labour-market, fiscal, legal, privacy, DSS / Services Australia, Treasury, PBO, and economic review before policy use.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_reports(reports_dir: Path, rows: list[dict[str, Any]]) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "payment_interactions.json"
    md_path = reports_dir / "payment_interactions.md"
    json_path.write_text(
        json.dumps(build_json_payload(rows, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(rows, metadata), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = ArgumentParser(description="Run CARSF payment interaction and targeting previews.")
    parser.add_argument("--examples-dir", type=Path, default=REPO_ROOT / "examples" / "payment_interactions")
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args()

    rows = run_payment_interaction_examples(args.examples_dir)
    json_path, md_path = write_reports(args.reports_dir, rows)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
