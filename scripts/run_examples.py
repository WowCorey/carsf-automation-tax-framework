"""Run all illustrative CARSF examples and write JSON/Markdown reports."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = REPO_ROOT / "model"
if str(MODEL_ROOT) not in sys.path:
    sys.path.insert(0, str(MODEL_ROOT))

from carsf.example_runner import (  # noqa: E402
    EXAMPLE_IDS,
    ExampleResult,
    ExampleRunnerError,
    report_metadata,
    run_all_examples,
)


def money(value: float) -> str:
    return f"{value:,.2f}"


def number(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:,.4f}"


def output_table(result: ExampleResult) -> list[tuple[str, str]]:
    outputs = result.outputs
    return [
        ("QLC", number(outputs.qlc)),
        ("OPFTE_LIBC", number(outputs.opfte_libc)),
        ("HLE", number(outputs.hle)),
        ("AII", number(outputs.aii)),
        ("NLTG", number(outputs.nltg)),
        ("AAVA", money(outputs.aava)),
        ("AEL raw", money(outputs.ael_raw)),
        ("AEL payable", money(outputs.ael_payable)),
        ("AEL shortfall", money(outputs.shortfall)),
        ("ARL", money(outputs.arl)),
        ("Credits", money(outputs.credits)),
        ("Final liability (placeholder)", money(outputs.liability)),
        ("CARS-I", number(outputs.cars_i)),
        ("CoverageRatio", outputs.coverage_ratio_display),
    ]


def compact_inputs(result: ExampleResult) -> list[str]:
    inputs = result.inputs
    automation = inputs["automation_components"]
    aava = inputs["aava_inputs"]
    caps = inputs["schedule_placeholders"]["caps"]
    return [
        f"Output: {inputs['output']['value']:,.2f} {inputs['output']['unit']}",
        f"Workers: {len(inputs['workers'])}",
        (
            "Automation components: "
            f"compute={automation['compute_ratio']}, "
            f"auto_decision={automation['auto_decision_ratio']}, "
            f"robotics_capital={automation['robotics_capital_ratio']}, "
            f"auto_process={automation['auto_process_share']}"
        ),
        (
            "AAVA inputs: "
            f"revenue={aava['australian_attributable_revenue']:,.2f}, "
            f"non_automation_costs={aava['verified_non_automation_input_costs']:,.2f}, "
            f"qlc_wage_cost={aava['verified_qlc_wage_cost']:,.2f}"
        ),
        f"Capital base: {inputs['capital_base']:,.2f}",
        f"Verified credits: {inputs['credits']['verified_credits']:,.2f}",
        (
            "Caps: "
            f"lambda={caps['ael_capacity_cap_rate']}, "
            f"LAMBDA={caps['combined_liability_cap_rate']}, "
            f"theta={caps['credit_cap_rate']}"
        ),
    ]


def build_json_payload(results: list[ExampleResult], metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": metadata,
        "examples": [result.to_jsonable() for result in results],
    }


def build_markdown(results: list[ExampleResult], metadata: dict[str, Any]) -> str:
    lines = [
        "# CARSF V1.5 Worked Example Results",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        f"Version: {metadata['version']}",
        "",
        f"Status: `{metadata['status']}`",
        "",
        "These outputs are illustrative placeholders only. They are not legal, tax, Treasury, ATO, economic, or real liability calculations.",
        "",
        "## Summary Comparison",
        "",
        "| Example | Sector | QLC | HLE | AII | NLTG | AAVA | AEL Payable | ARL | Final Liability | Main Interpretation |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for result in results:
        outputs = result.outputs
        lines.append(
            "| "
            f"{result.name} | {result.schedule} | {outputs.qlc:.2f} | {outputs.hle:.2f} | "
            f"{outputs.aii:.2f} | {outputs.nltg:.2f} | {outputs.aava:,.2f} | "
            f"{outputs.ael_payable:,.2f} | {outputs.arl:,.2f} | {outputs.liability:,.2f} | "
            f"{result.interpretation} |"
        )
    lines.extend(
        [
            "",
            "The comparison should be read directionally only: AI-admin repair is not treated like robotic repair, robotic repair is higher-risk than traditional repair, and the AI logistics platform is higher-risk than hybrid logistics under these placeholders.",
            "",
        ]
    )

    for result in results:
        lines.extend(
            [
                f"## {result.name}",
                "",
                "### A. Business Description",
                "",
                result.business_description,
                "",
                "### B. Key Input Assumptions",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in compact_inputs(result))
        lines.extend(
            [
                "",
                "### C. Formula Trace",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in result.formula_trace)
        lines.extend(
            [
                "",
                "### D. Calculated Output Table",
                "",
                "| Output | Value |",
                "| --- | ---: |",
            ]
        )
        lines.extend(f"| {label} | {value} |" for label, value in output_table(result))
        lines.extend(
            [
                "",
                "### E. Plain-English Interpretation",
                "",
                result.interpretation,
                "",
                "### F. Red-Team / Limitation Notes",
                "",
                "**Warnings**",
                "",
            ]
        )
        lines.extend(f"- {warning}" for warning in result.warnings)
        lines.extend(["", "**Evidence labels**", ""])
        lines.extend(f"- `{label}`" for label in result.evidence_labels)
        lines.extend(["", "**Limitations**", ""])
        lines.extend(f"- {note}" for note in result.limitation_notes)
        lines.extend(["", "**Red-team notes**", ""])
        flags = result.red_team_notes.get("flags", [])
        notes = result.red_team_notes.get("notes", [])
        lines.append(f"- Flags: {', '.join(flags) if flags else 'none'}")
        lines.extend(f"- {note}" for note in notes)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_reports(reports_dir: Path, results: list[ExampleResult]) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = reports_dir / "example_results.json"
    md_path = reports_dir / "example_results.md"
    metadata = report_metadata()
    json_path.write_text(
        json.dumps(build_json_payload(results, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(results, metadata), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = ArgumentParser(description="Run illustrative CARSF worked examples.")
    parser.add_argument(
        "--reports-dir",
        type=Path,
        default=REPO_ROOT / "reports",
        help="Directory for generated JSON and Markdown reports.",
    )
    args = parser.parse_args()
    try:
        results = run_all_examples(REPO_ROOT)
        expected_ids = [result.id for result in results]
        if expected_ids != EXAMPLE_IDS:
            raise ExampleRunnerError(f"Unexpected example order or set: {expected_ids}")
        json_path, md_path = write_reports(args.reports_dir, results)
    except ExampleRunnerError as exc:
        print(f"example runner failed: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
