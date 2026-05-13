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
from carsf.group_runner import (  # noqa: E402
    APPORTIONMENT_SCOPE_NOTE,
    GROUPED_NON_CLAIMS,
    GROUPED_REPORT_STATUS,
    GroupedPreviewResult,
    run_grouped_previews,
    standalone_max_risk,
)
from carsf.transfer_runner import (  # noqa: E402
    TRANSFER_PRICING_NON_CLAIMS,
    TRANSFER_PRICING_REPORT_STATUS,
    TRANSFER_PRICING_REPORT_WARNING,
    TransferPricingPreviewReport,
    TransferPricingScenarioResult,
    run_transfer_pricing_previews,
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


def risk_review_required(result: ExampleResult) -> bool:
    return (
        result.safe_harbour_result.review_required
        or result.avoidance_result.risk_level != "low"
        or result.grouping_risk_result.risk_level != "low"
    )


def main_risk_reason(result: ExampleResult) -> str:
    if result.safe_harbour_result.reasons:
        return result.safe_harbour_result.reasons[0]
    if result.avoidance_result.reasons:
        return result.avoidance_result.reasons[0]
    if result.grouping_risk_result.reasons:
        return result.grouping_risk_result.reasons[0]
    return "No prototype review reason recorded."


def risk_flags(flags: list[str]) -> str:
    return ", ".join(flags) if flags else "none"


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
            "## Safe Harbour and Review Flags",
            "",
            "These are prototype review flags, not legal findings. Safe harbour classification does not reduce or erase liability in this build.",
            "",
            "| Example | Safe Harbour Category | Avoidance Risk | Grouping Risk | Review Required | Main Reason |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for result in results:
        lines.append(
            "| "
            f"{result.name} | {result.safe_harbour_result.category} | "
            f"{result.avoidance_result.risk_level} | {result.grouping_risk_result.risk_level} | "
            f"{'yes' if risk_review_required(result) else 'no'} | {main_risk_reason(result)} |"
        )
    lines.extend(
        [
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
        lines.extend(
            [
                "",
                "### G. Safe Harbour Assessment",
                "",
                f"- Eligible: {str(result.safe_harbour_result.eligible).lower()}",
                f"- Category: {result.safe_harbour_result.category}",
                f"- Review required: {str(result.safe_harbour_result.review_required).lower()}",
                "- Reasons:",
            ]
        )
        lines.extend(f"  - {reason}" for reason in result.safe_harbour_result.reasons)
        lines.extend(["- Warnings:"])
        lines.extend(f"  - {warning}" for warning in result.safe_harbour_result.warnings)
        lines.extend(["- Placeholder basis:"])
        lines.extend(f"  - {basis}" for basis in result.safe_harbour_result.placeholder_basis)
        lines.extend(
            [
                "",
                "### H. Avoidance / Gaming Risk Assessment",
                "",
                f"- Risk level: {result.avoidance_result.risk_level}",
                f"- Flags: {risk_flags(result.avoidance_result.flags)}",
                "- Reasons:",
            ]
        )
        lines.extend(f"  - {reason}" for reason in result.avoidance_result.reasons)
        lines.extend(["- Recommended review:"])
        lines.extend(f"  - {review}" for review in result.avoidance_result.recommended_review)
        lines.extend(["- Placeholder basis:"])
        lines.extend(f"  - {basis}" for basis in result.avoidance_result.placeholder_basis)
        lines.extend(
            [
                "",
                "### I. Grouped-Entity Review Flag",
                "",
                f"- Risk level: {result.grouping_risk_result.risk_level}",
                f"- Flags: {risk_flags(result.grouping_risk_result.flags)}",
                "- Reasons:",
            ]
        )
        lines.extend(f"  - {reason}" for reason in result.grouping_risk_result.reasons)
        lines.extend(["- Recommended review:"])
        lines.extend(f"  - {review}" for review in result.grouping_risk_result.recommended_review)
        lines.extend(["- Placeholder basis:"])
        lines.extend(f"  - {basis}" for basis in result.grouping_risk_result.placeholder_basis)
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


def grouped_json_payload(grouped: GroupedPreviewResult, metadata: dict[str, Any]) -> dict[str, Any]:
    payload = grouped.to_jsonable()
    payload["apportionment_scope_note"] = APPORTIONMENT_SCOPE_NOTE
    payload["transfer_pricing_preview_note"] = "Related-party and mixed-unit previews are generated in transfer_pricing_results.*."
    payload["metadata"] = {
        **metadata,
        "status": GROUPED_REPORT_STATUS,
        "non_claims": GROUPED_NON_CLAIMS,
        "apportionment_scope_note": APPORTIONMENT_SCOPE_NOTE,
        "transfer_pricing_preview_note": "Related-party and mixed-unit previews are generated in transfer_pricing_results.*.",
    }
    return payload


def _grouped_number(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:,.2f}"


def build_grouped_markdown(grouped: GroupedPreviewResult, metadata: dict[str, Any]) -> str:
    aggregation = grouped.aggregation_result
    apportionment = grouped.apportionment_result
    stress = grouped.hybrid_stress_result
    split = grouped.split_structure
    mixed = grouped.mixed_apportionment
    standalone_liability = aggregation.standalone_entity_liability_sum
    group_liability = aggregation.group_recomputed_liability_preview
    liability_difference = None if group_liability is None else group_liability - standalone_liability

    lines = [
        "# CARSF V1.5 Grouped-Entity and Apportionment Results",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        f"Version: {metadata['version']}",
        "",
        f"Status: `{GROUPED_REPORT_STATUS}`",
        "",
        "These outputs are prototype review previews only. They are not legal grouping findings, tax assessments, Treasury guidance, ATO guidance, or economic validation.",
        "",
        "## A. Grouped-Entity Aggregation Overview",
        "",
        "This report shows non-operative modelling previews for related-entity aggregation, mixed-activity apportionment, and a hybrid logistics stress case. It does not alter any final liability calculation in the single-entity examples.",
        "",
        "Related-party and mixed-unit previews are generated in `reports/transfer_pricing_results.md` and `reports/transfer_pricing_results.json`.",
        "",
        "## B. Why Grouping Matters",
        "",
        "A split structure can make each standalone entity look lower-risk while the economic group still contains high automated output, thin Australian QLC, offshore automation services, and related-party fee paths. The preview aggregates only where output units are comparable and flags review where they are not.",
        "",
        "| Example | Standalone Risk | Group Risk | Aggregation Needed | Apportionment Needed | Main Reason |",
        "| --- | --- | --- | --- | --- | --- |",
        (
            f"| {split['title']} | {standalone_max_risk(grouped.split_entities)} | "
            f"{aggregation.risk_level} | yes | no | Split entities share Australian-facing automated logistics output. |"
        ),
        (
            f"| {mixed['title']} | N/A | {'medium' if apportionment.review_required else 'low'} | no | yes | "
            "Mixed activities require schedule-share review rather than unreviewed single classification. |"
        ),
        (
            f"| {stress.name} | {stress.avoidance_result.risk_level} | N/A | no | no | "
            "Stress variant tests non-zero but intermediate NLTG for hybrid automation. |"
        ),
        "",
        "## C. Split Logistics Structure Example",
        "",
        split["purpose"],
        "",
        "## D. Standalone Entity View",
        "",
        "| Entity | Role | Standalone Risk | Revenue | Output | QLC | HLE | AII | NLTG | AAVA | Liability | Flags |",
        "| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for entity in grouped.split_entities:
        lines.append(
            "| "
            f"{entity.entity_id} | {entity.role} | {entity.standalone_risk} | "
            f"{entity.revenue:,.2f} | {entity.output_value:,.2f} | {entity.qlc:.2f} | "
            f"{entity.hle:.2f} | {entity.aii:.2f} | {entity.nltg:.2f} | "
            f"{entity.aava:,.2f} | {entity.liability:,.2f} | {risk_flags(entity.flags)} |"
        )
    lines.extend(
        [
            "",
            "## E. Aggregated Group Preview",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| Entity count | {aggregation.entity_count} |",
            f"| Aggregate revenue | {aggregation.aggregate_revenue:,.2f} |",
            f"| Aggregate output | {_grouped_number(aggregation.aggregate_output)} |",
            f"| Aggregate QLC | {aggregation.aggregate_qlc:.2f} |",
            f"| Aggregate HLE | {_grouped_number(aggregation.aggregate_hle)} |",
            f"| Weighted AII | {_grouped_number(aggregation.weighted_aii)} |",
            f"| Aggregate NLTG preview | {_grouped_number(aggregation.aggregate_nltg_preview)} |",
            f"| Aggregate AAVA | {aggregation.aggregate_aava:,.2f} |",
            f"| Standalone entity liability sum | {standalone_liability:,.2f} |",
            f"| Group recomputed liability preview | {_grouped_number(group_liability)} |",
            f"| Group risk | {aggregation.risk_level} |",
            "",
            "## F. Difference Between Standalone and Group-Level Preview",
            "",
            f"- Standalone entity liability sum: {standalone_liability:,.2f}",
            f"- Group recomputed liability preview: {_grouped_number(group_liability)}",
            f"- Difference: {_grouped_number(liability_difference)}",
            f"- Aggregation flags: {risk_flags(aggregation.flags)}",
            "",
            "## G. Mixed-Activity / Prototype Apportionment Example",
            "",
            mixed["purpose"],
            "",
            APPORTIONMENT_SCOPE_NOTE,
            "",
            f"- Valid: {str(apportionment.valid).lower()}",
            f"- Review required: {str(apportionment.review_required).lower()}",
            "",
            "Weighted placeholder parameters:",
            "",
        ]
    )
    for key, value in apportionment.weighted_parameters.items():
        if isinstance(value, dict):
            lines.append(f"- {key}: {json.dumps(value, sort_keys=True)}")
        else:
            lines.append(f"- {key}: {value:.6f}")
    lines.extend(
        [
            "",
            "## H. Apportionment Basis Table",
            "",
            "| Activity | Schedule | Share | Basis | Placeholder Basis |",
            "| --- | --- | ---: | --- | --- |",
        ]
    )
    for activity in apportionment.activities:
        placeholder_basis = activity.placeholder_basis
        if isinstance(placeholder_basis, list):
            basis_text = "; ".join(str(item) for item in placeholder_basis)
        else:
            basis_text = str(placeholder_basis)
        lines.append(
            f"| {activity.activity_id or activity.description} | {activity.schedule_id} | "
            f"{activity.share:.2f} | {activity.basis} | {basis_text} |"
        )
    lines.extend(
        [
            "",
            "## I. Hybrid Logistics Stress Variant",
            "",
            stress.business_description,
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| QLC | {stress.outputs.qlc:.2f} |",
            f"| HLE | {stress.outputs.hle:.2f} |",
            f"| AII | {stress.outputs.aii:.2f} |",
            f"| NLTG | {stress.outputs.nltg:.2f} |",
            f"| AAVA | {stress.outputs.aava:,.2f} |",
            f"| Final liability preview | {stress.outputs.liability:,.2f} |",
            "",
            stress.interpretation,
            "",
            "## J. Limitations and Non-Claims",
            "",
        ]
    )
    for warning in aggregation.warnings + apportionment.warnings + stress.warnings:
        lines.append(f"- {warning}")
    for basis in aggregation.placeholder_basis + apportionment.placeholder_basis + stress.limitation_notes:
        lines.append(f"- {basis}")
    lines.append("- These outputs are prototype review previews only. They are not legal grouping findings, tax assessments, Treasury guidance, ATO guidance, or economic validation.")
    return "\n".join(lines).rstrip() + "\n"


def write_grouped_reports(reports_dir: Path, grouped: GroupedPreviewResult) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "grouped_entity_results.json"
    md_path = reports_dir / "grouped_entity_results.md"
    json_path.write_text(
        json.dumps(grouped_json_payload(grouped, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_grouped_markdown(grouped, metadata), encoding="utf-8")
    return json_path, md_path


def transfer_pricing_json_payload(
    transfer_report: TransferPricingPreviewReport,
    metadata: dict[str, Any],
) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": TRANSFER_PRICING_REPORT_STATUS,
            "non_claims": TRANSFER_PRICING_NON_CLAIMS,
            "warning": TRANSFER_PRICING_REPORT_WARNING,
        },
        **transfer_report.to_jsonable(),
    }


def _scenario_summary_rows(scenario: TransferPricingScenarioResult) -> list[tuple[str, str]]:
    return [
        ("Reported AAVA", money(scenario.reported_aava)),
        ("Preview adjustments total", money(scenario.adjusted_aava_preview.preview_adjustments_total)),
        ("Adjusted AAVA preview", money(scenario.adjusted_aava_preview.adjusted_aava_preview)),
        ("Original final liability", money(scenario.liability_preview.original_final_liability)),
        (
            "Adjusted-AAVA liability preview",
            "N/A"
            if scenario.liability_preview.adjusted_aava_liability_preview is None
            else money(scenario.liability_preview.adjusted_aava_liability_preview),
        ),
        (
            "Liability preview difference",
            "N/A" if scenario.liability_preview.difference is None else money(scenario.liability_preview.difference),
        ),
        ("Risk level", scenario.transfer_pricing_result.risk_level),
        ("Review required", str(scenario.transfer_pricing_result.review_required).lower()),
    ]


def _append_scenario_markdown(lines: list[str], scenario: TransferPricingScenarioResult) -> None:
    lines.extend(
        [
            f"### {scenario.title}",
            "",
            scenario.source["purpose"],
            "",
            "| Metric | Value |",
            "| --- | ---: |",
        ]
    )
    lines.extend(f"| {label} | {value} |" for label, value in _scenario_summary_rows(scenario))
    lines.extend(
        [
            "",
            "Adjustment candidates:",
            "",
            "| Transaction | Type | Amount | Review Share | Preview Addback | Confidence | Reason |",
            "| --- | --- | ---: | ---: | ---: | --- | --- |",
        ]
    )
    candidates = scenario.transfer_pricing_result.candidates
    if not candidates:
        lines.append("| none | none | 0.00 | 0.00 | 0.00 | low | No candidate supplied. |")
    for candidate in candidates:
        lines.append(
            "| "
            f"{candidate.transaction_id} | {candidate.transaction_type} | "
            f"{candidate.amount:,.2f} | {candidate.review_share:.2f} | "
            f"{candidate.preview_addback_amount:,.2f} | {candidate.confidence} | {candidate.reason} |"
        )
    lines.extend(
        [
            "",
            "Warnings and non-claims:",
            "",
        ]
    )
    for warning in scenario.transfer_pricing_result.warnings + scenario.adjusted_aava_preview.warnings + scenario.liability_preview.warnings:
        lines.append(f"- {warning}")
    for non_claim in scenario.transfer_pricing_result.non_claims:
        lines.append(f"- {non_claim}")
    lines.extend(["", "Limitations:", ""])
    for limitation in scenario.source.get("limitations", []):
        lines.append(f"- {limitation}")
    lines.append("")


def build_transfer_pricing_markdown(
    transfer_report: TransferPricingPreviewReport,
    metadata: dict[str, Any],
) -> str:
    mixed = transfer_report.mixed_unit_group
    compatibility = transfer_report.unit_compatibility
    exposure = transfer_report.mixed_unit_exposure
    lines = [
        "# CARSF V1.5 Transfer-Pricing and Mixed-Unit Preview Results",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        f"Version: {metadata['version']}",
        "",
        f"Status: `{TRANSFER_PRICING_REPORT_STATUS}`",
        "",
        TRANSFER_PRICING_REPORT_WARNING,
        "",
        "## A. Purpose and Non-Claims",
        "",
        "This report adds non-operative review previews for related-party automation charges, adjusted AAVA review candidates, and mixed-unit output handling. It does not change the reported-AAVA pathway or any existing final liability calculation.",
        "",
    ]
    lines.extend(f"- {non_claim}" for non_claim in TRANSFER_PRICING_NON_CLAIMS)
    lines.extend(
        [
            "",
            "## B. Why Related-Party / Offshore Fees Matter",
            "",
            "AAVA can be suppressed in a prototype scenario where automated Australian-facing output is paired with offshore AI service fees, IP royalties, platform licences, cloud/inference relabelling, or robotics leasing charges. The preview only identifies review candidates and illustrative addback amounts.",
            "",
            "## C. Related-Party AI Fee Example",
            "",
        ]
    )
    _append_scenario_markdown(lines, transfer_report.related_party_ai_fee)
    lines.extend(
        [
            "## D. Reported AAVA vs Adjusted AAVA Preview",
            "",
            "| Scenario | Reported AAVA | Preview Adjustments | Adjusted AAVA Preview | Original Liability | Adjusted-AAVA Liability Preview |",
            "| --- | ---: | ---: | ---: | ---: | ---: |",
        ]
    )
    for scenario in (transfer_report.related_party_ai_fee, transfer_report.robotics_leasing):
        adjusted_liability = scenario.liability_preview.adjusted_aava_liability_preview
        lines.append(
            "| "
            f"{scenario.title} | {scenario.reported_aava:,.2f} | "
            f"{scenario.adjusted_aava_preview.preview_adjustments_total:,.2f} | "
            f"{scenario.adjusted_aava_preview.adjusted_aava_preview:,.2f} | "
            f"{scenario.liability_preview.original_final_liability:,.2f} | "
            f"{'N/A' if adjusted_liability is None else f'{adjusted_liability:,.2f}'} |"
        )
    lines.extend(
        [
            "",
            "## E. Adjustment Candidate Table",
            "",
            "| Scenario | Transaction | Type | Amount | Preview Addback | Confidence |",
            "| --- | --- | --- | ---: | ---: | --- |",
        ]
    )
    for scenario in (transfer_report.related_party_ai_fee, transfer_report.robotics_leasing):
        for candidate in scenario.transfer_pricing_result.candidates:
            lines.append(
                "| "
                f"{scenario.title} | {candidate.transaction_id} | {candidate.transaction_type} | "
                f"{candidate.amount:,.2f} | {candidate.preview_addback_amount:,.2f} | {candidate.confidence} |"
            )
    lines.extend(
        [
            "",
            "## F. Robotics Leasing Example",
            "",
        ]
    )
    _append_scenario_markdown(lines, transfer_report.robotics_leasing)
    lines.extend(
        [
            "## G. Mixed-Unit Platform Group",
            "",
            mixed["purpose"],
            "",
            "| Entity | Schedule | Canonical Output Unit | Revenue | AAVA | Standalone Liability | Risk |",
            "| --- | --- | --- | ---: | ---: | ---: | --- |",
        ]
    )
    for entity in mixed["entities"]:
        lines.append(
            "| "
            f"{entity['entity_id']} | {entity['schedule_id']} | {entity['canonical_output_unit']} | "
            f"{entity['revenue']:,.2f} | {entity['aava']:,.2f} | {entity['liability']:,.2f} | "
            f"{entity.get('risk_level', 'unknown')} |"
        )
    lines.extend(
        [
            "",
            "## H. Mixed-Unit Compatibility Result",
            "",
            f"- Compatible: {str(compatibility.compatible).lower()}",
            f"- Units: {', '.join(compatibility.unit_set)}",
            f"- Comparable unit: {compatibility.comparable_unit or 'N/A'}",
            f"- Reason: {compatibility.reason}",
            f"- Review required: {str(compatibility.review_required).lower()}",
            "",
        ]
    )
    lines.extend(f"- {warning}" for warning in compatibility.warnings)
    lines.extend(
        [
            "",
            "## I. Value-Weighted Exposure Index Explanation",
            "",
            "Where units differ, the prototype prohibits direct output and HLE aggregation. It can still show standalone liability sum, schedule-level comparison, and a value-weighted exposure index. That index is not a tax base and is not a replacement for calibrated sector schedules.",
            "",
            "| Metric | Value |",
            "| --- | ---: |",
            f"| Method | {exposure.method} |",
            f"| Standalone liability sum | {exposure.standalone_liability_sum:,.2f} |",
            f"| Value-weighted exposure index | {number(exposure.value_weighted_exposure_index)} |",
            f"| Review required | {str(exposure.review_required).lower()} |",
            "",
        ]
    )
    lines.extend(f"- {warning}" for warning in exposure.warnings)
    lines.extend(f"- {non_claim}" for non_claim in exposure.non_claims)
    lines.extend(
        [
            "",
            "## J. Limitations and Required Legal/Tax Review",
            "",
        ]
    )
    for limitation in mixed.get("limitations", []):
        lines.append(f"- {limitation}")
    lines.append(f"- {TRANSFER_PRICING_REPORT_WARNING}")
    return "\n".join(lines).rstrip() + "\n"


def write_transfer_pricing_reports(
    reports_dir: Path,
    transfer_report: TransferPricingPreviewReport,
) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "transfer_pricing_results.json"
    md_path = reports_dir / "transfer_pricing_results.md"
    json_path.write_text(
        json.dumps(transfer_pricing_json_payload(transfer_report, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_transfer_pricing_markdown(transfer_report, metadata), encoding="utf-8")
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
        grouped = run_grouped_previews(REPO_ROOT)
        grouped_json_path, grouped_md_path = write_grouped_reports(args.reports_dir, grouped)
        transfer_report = run_transfer_pricing_previews(REPO_ROOT)
        transfer_json_path, transfer_md_path = write_transfer_pricing_reports(args.reports_dir, transfer_report)
    except ExampleRunnerError as exc:
        print(f"example runner failed: {exc}", file=sys.stderr)
        return 1
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    print(f"wrote {grouped_json_path}")
    print(f"wrote {grouped_md_path}")
    print(f"wrote {transfer_json_path}")
    print(f"wrote {transfer_md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
