"""Run CARSF V1.5 prototype administrative compliance workflow reports."""

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

from carsf.administrative_workflow import (  # noqa: E402
    ADMINISTRATIVE_WORKFLOW_NON_CLAIMS,
    ADMINISTRATIVE_WORKFLOW_WARNING,
    default_evidence_requirement_ids,
    evaluate_administrative_workflows,
    summarise_administrative_workflows,
    validate_administrative_workflow_scenarios,
)
from carsf.evidence_packet import load_evidence_packet  # noqa: E402
from carsf.example_runner import report_metadata  # noqa: E402
from run_behavioural_response_simulation import (  # noqa: E402
    DEFAULT_SCENARIOS_PATH as DEFAULT_BEHAVIOURAL_SCENARIOS_PATH,
)
from run_behavioural_response_simulation import run_behavioural_response_simulation  # noqa: E402
from run_sector_schedule_expansion import load_schedules, validate_schedules  # noqa: E402


REPORT_STATUS = "prototype_administrative_compliance_workflow_synthetic_only"
DEFAULT_SCENARIOS_PATH = REPO_ROOT / "examples" / "administrative_workflow_scenarios.yaml"


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def load_administrative_workflow_scenarios(path: Path) -> list[dict[str, Any]]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"administrative workflow scenario file must be a mapping: {path}")
    required_labels = [
        "illustrative_placeholder_only",
        "synthetic_workflow_only",
        "not_calibrated",
        "no_real_data",
        "no_enforcement",
        "no_compliance_scoring",
        "no_tax_payable_estimate",
    ]
    missing = [label for label in required_labels if loaded.get(label) is not True]
    if missing:
        raise ValueError(f"administrative workflow scenario file missing synthetic-only labels: {', '.join(missing)}")
    scenarios = loaded.get("scenarios", [])
    if not isinstance(scenarios, list) or not scenarios:
        raise ValueError("administrative workflow scenario file must contain a non-empty scenarios list")
    if not all(isinstance(item, dict) for item in scenarios):
        raise ValueError("each administrative workflow scenario must be a mapping")
    return scenarios


def load_synthetic_evidence_packet_ids(mock_evidence_dir: Path) -> set[str]:
    packet_ids: set[str] = set()
    for path in sorted(mock_evidence_dir.glob("*.yaml")):
        packet = load_evidence_packet(path)
        if packet.synthetic_mock_evidence_only is not True:
            raise ValueError(f"mock evidence packet is not synthetic-only: {path}")
        packet_ids.add(packet.packet_id)
    return packet_ids


def run_administrative_compliance_workflow(
    schedules_dir: Path,
    scenarios_path: Path,
    behavioural_scenarios_path: Path,
    mock_evidence_dir: Path,
) -> tuple[list[Any], Any]:
    schedules = load_schedules(schedules_dir)
    validate_schedules(schedules)
    schedule_ids = {schedule["schedule_id"] for schedule in schedules}

    behavioural_results, _behavioural_summary = run_behavioural_response_simulation(
        schedules_dir,
        behavioural_scenarios_path,
    )
    behavioural_response_ids = {result.scenario_id for result in behavioural_results}
    behavioural_results_by_id = {result.scenario_id: result for result in behavioural_results}

    synthetic_packet_ids = load_synthetic_evidence_packet_ids(mock_evidence_dir)
    scenarios = load_administrative_workflow_scenarios(scenarios_path)
    evidence_requirement_ids = default_evidence_requirement_ids()
    validate_administrative_workflow_scenarios(
        scenarios,
        schedule_ids,
        behavioural_response_ids,
        synthetic_packet_ids,
        evidence_requirement_ids,
    )
    results = evaluate_administrative_workflows(
        scenarios,
        schedule_ids,
        behavioural_response_ids,
        synthetic_packet_ids,
        behavioural_results_by_id,
        evidence_requirement_ids,
    )
    summary = summarise_administrative_workflows(results)
    return results, summary


def build_json_payload(results: list[Any], summary: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": ADMINISTRATIVE_WORKFLOW_NON_CLAIMS,
            "firm_level_liability_logic_modified": False,
            "real_enforcement_created": False,
            "real_ato_power_claimed": False,
            "compliance_scoring_created": False,
            "notices_issued": False,
            "real_data_used": False,
        },
        "summary": _jsonable(summary),
        "administrative_workflow_results": [_jsonable(result) for result in results],
    }


def _workflow_table(results: list[Any]) -> list[str]:
    lines = [
        "| Scenario ID | Scenario Name | Sector Schedule | Linked Behavioural Responses | Trigger Flags | Review Domains | Evidence Bundle Size | Workflow Decision Band | Workflow Status | Escalation Queues | External Review Required | Do Not Enforce | Main Reason |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for result in results:
        escalation_queues = sorted({item.queue_id for item in result.escalation_pathways})
        lines.append(
            "| "
            f"{result.scenario_id} | {result.scenario_name} | {result.sector_schedule_id} | "
            f"{', '.join(result.linked_behavioural_response_ids) or 'None'} | "
            f"{', '.join(result.trigger_flags)} | {', '.join(result.requested_review_domains)} | "
            f"{result.evidence_request_bundle.requirement_count} | {result.workflow_decision_band} | "
            f"{result.workflow_status} | {', '.join(escalation_queues) or 'None'} | "
            f"{result.external_review_required} | {result.do_not_enforce} | {result.main_reason} |"
        )
    return lines


def _counts_section(title: str, counts: dict[str, int]) -> list[str]:
    lines = [f"### {title}", ""]
    if not counts:
        lines.append("- None.")
    else:
        for key, value in counts.items():
            lines.append(f"- `{key}`: {value}")
    return lines


def _evidence_bundle_lines(results: list[Any]) -> list[str]:
    lines = [
        "| Scenario ID | Bundle ID | Requirement Count | Requirement IDs |",
        "| --- | --- | --- | --- |",
    ]
    for result in results:
        bundle = result.evidence_request_bundle
        lines.append(
            f"| {result.scenario_id} | {bundle.bundle_id} | {bundle.requirement_count} | "
            f"{', '.join(bundle.requirement_ids) or 'No mapped requirements'} |"
        )
    return lines


def _queue_lines(results: list[Any]) -> list[str]:
    queues = sorted({assignment.queue_id for result in results for assignment in result.queue_assignments})
    if not queues:
        return ["- No queues assigned."]
    lines = []
    for queue in queues:
        grouped = [result.scenario_id for result in results if any(item.queue_id == queue for item in result.queue_assignments)]
        lines.append(f"- `{queue}`: {', '.join(grouped)}")
    return lines


def _escalation_lines(results: list[Any]) -> list[str]:
    lines = []
    for result in results:
        queues = sorted({item.queue_id for item in result.escalation_pathways})
        lines.append(f"- `{result.scenario_id}`: {', '.join(queues) or 'No external escalation queue listed'}")
    return lines


def _behavioural_link_lines(results: list[Any]) -> list[str]:
    lines = []
    for result in results:
        links = ", ".join(result.linked_behavioural_response_ids) or "None"
        lines.append(f"- `{result.scenario_id}` links to: {links}")
    return lines


def _privacy_lines(results: list[Any]) -> list[str]:
    lines = []
    for result in results:
        lines.append(
            f"- `{result.scenario_id}` sensitivity: `{result.privacy_secrecy_sensitivity}`; privacy review queue: "
            f"{any(item.queue_id == 'privacy_review_queue' for item in result.queue_assignments)}"
        )
    return lines


def _locked_lines(results: list[Any]) -> list[str]:
    grouped = [
        result
        for result in results
        if result.workflow_status in {"locked_for_external_review", "suppress_until_calibrated", "external_review_required"}
    ]
    if not grouped:
        return ["- No locked, suppressed, or external-review cases in this synthetic run."]
    return [
        f"- `{result.scenario_id}`: `{result.workflow_status}` ({result.main_reason})"
        for result in grouped
    ]


def build_markdown(results: list[Any], summary: Any, metadata: dict[str, Any]) -> str:
    lines = [
        "# CARSF V1.5 ATO / Administrative Compliance Workflow",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report organises synthetic CARSF cases into prototype evidence requests, review queues, escalation pathways, behavioural-response links, sector schedule review, grouped-entity review, transfer-pricing review, privacy/secrecy review, methods review, and external calibration review.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in ADMINISTRATIVE_WORKFLOW_NON_CLAIMS)
    lines.extend(
        [
            "- Every result has `do_not_enforce: true`.",
            "- Every result has `do_not_issue_notice: true`.",
            "- Every result has `do_not_score_compliance: true`.",
            "- Every result has `do_not_estimate_tax_payable: true`.",
            "- Firm-level CARSF liability logic is not modified.",
            "",
            "## C. Method - Synthetic Administrative Pathways Only",
            "",
            "The workflow uses declared synthetic scenario metadata, existing prototype evidence requirement IDs, synthetic mock packet IDs, behavioural response links, and sector schedule IDs. It organises review pathways only and creates no real action.",
            "",
            "## D. Scenario Coverage",
            "",
        ]
    )
    for result in results:
        lines.append(f"- `{result.scenario_id}`: {result.scenario_name}")
    lines.extend(["", "## E. Administrative Workflow Matrix", ""])
    lines.extend(_workflow_table(results))
    lines.extend(["", "## F. Evidence Request Bundles", ""])
    lines.extend(_evidence_bundle_lines(results))
    lines.extend(["", "## G. Review Queue Assignments", ""])
    lines.extend(_queue_lines(results))
    lines.extend(["", "## H. Escalation Pathways", ""])
    lines.extend(_escalation_lines(results))
    lines.extend(["", "## I. Behavioural Response Links", ""])
    lines.extend(_behavioural_link_lines(results))
    lines.extend(["", "## J. Privacy / Secrecy Review Notes", ""])
    lines.extend(_privacy_lines(results))
    lines.extend(["", "## K. Suppressed / Locked-for-External-Review Cases", ""])
    lines.extend(_locked_lines(results))
    lines.extend(["", "## L. Calibration and Administrative Design Blockers", ""])
    if summary.calibration_blockers:
        lines.extend(f"- {blocker}" for blocker in summary.calibration_blockers)
    else:
        lines.append("- No blockers listed beyond global external review and administrative-design review.")
    lines.extend(["", "## M. Plain-English Interpretation", ""])
    lines.extend(
        [
            "- Workflow decision bands indicate prototype review complexity only.",
            "- Evidence bundles are draft request lists based on existing prototype evidence requirement IDs.",
            "- Escalation queues show where external legal, tax, methods, privacy, calibration, or administrative-design review would be needed.",
            "- Locked or suppressed cases should not be presented as ready for operational use.",
        ]
    )
    lines.extend(["", "## N. Limitations and Future Review Needs", ""])
    lines.extend(_counts_section("Scenarios By Decision Band", summary.scenarios_by_decision_band))
    lines.extend([""])
    lines.extend(_counts_section("Scenarios By Workflow Status", summary.scenarios_by_workflow_status))
    lines.extend([""])
    lines.extend(_counts_section("Scenarios By Sector Schedule", summary.scenarios_by_sector_schedule))
    lines.extend(
        [
            "",
            f"- Total scenarios: {summary.total_scenarios}",
            f"- Scenarios requiring external review: {summary.scenarios_requiring_external_review}",
            f"- Scenarios locked for external review: {summary.scenarios_locked_for_external_review}",
            f"- Scenarios suppressed until calibrated: {summary.scenarios_suppressed_until_calibrated}",
            f"- Scenarios requiring evidence queue: {summary.scenarios_requiring_evidence_queue}",
            f"- Scenarios requiring grouped-entity queue: {summary.scenarios_requiring_grouped_entity_queue}",
            f"- Scenarios requiring transfer-pricing queue: {summary.scenarios_requiring_transfer_pricing_queue}",
            f"- Scenarios requiring sector schedule queue: {summary.scenarios_requiring_sector_schedule_queue}",
            f"- Scenarios requiring AAVA review queue: {summary.scenarios_requiring_aava_review_queue}",
            f"- Scenarios requiring capital-base review queue: {summary.scenarios_requiring_capital_base_review_queue}",
            f"- Scenarios requiring offshore-attribution queue: {summary.scenarios_requiring_offshore_attribution_queue}",
            f"- Scenarios requiring privacy review queue: {summary.scenarios_requiring_privacy_review_queue}",
            f"- Scenarios requiring legal-policy queue: {summary.scenarios_requiring_legal_policy_queue}",
            f"- Scenarios requiring ATO-methods queue: {summary.scenarios_requiring_ato_methods_queue}",
            f"- Scenarios requiring Treasury-methods queue: {summary.scenarios_requiring_treasury_methods_queue}",
            f"- Firm-level liability logic modified: {summary.firm_level_liability_logic_modified}",
            f"- Real enforcement created: {summary.real_enforcement_created}",
            f"- Real ATO power claimed: {summary.real_ato_power_claimed}",
            f"- Compliance scoring created: {summary.compliance_scoring_created}",
            f"- Notices created: {summary.notices_issued}",
            f"- Real data used: {summary.real_data_used}",
            "- Prototype only.",
            "- Placeholder only.",
            "- Synthetic administrative pathways only.",
            "- Not a workflow endorsed by the ATO, not guidance from the ATO, not Treasury modelling, not audit logic, not enforcement, and not compliance scoring.",
            "- No statutory powers, notices, penalties, taxpayer-level data, firm-level data, industry data, ABS/ATO/DSS/Treasury/PBO/HILDA/Census data, legal advice, tax advice, economic validation, conduct forecasting, or elasticity modelling.",
            "- Not usable to estimate actual tax payable.",
            "- Firm-level CARSF liability logic is not modified.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_reports(reports_dir: Path, results: list[Any], summary: Any) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "administrative_compliance_workflow.json"
    md_path = reports_dir / "administrative_compliance_workflow.md"
    json_path.write_text(
        json.dumps(build_json_payload(results, summary, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(results, summary, metadata), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = ArgumentParser(description="Run prototype administrative compliance workflow reports.")
    parser.add_argument("--schedules-dir", type=Path, default=REPO_ROOT / "schedules")
    parser.add_argument("--scenarios-path", type=Path, default=DEFAULT_SCENARIOS_PATH)
    parser.add_argument("--behavioural-scenarios-path", type=Path, default=DEFAULT_BEHAVIOURAL_SCENARIOS_PATH)
    parser.add_argument("--mock-evidence-dir", type=Path, default=REPO_ROOT / "data" / "mock_evidence")
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args()

    results, summary = run_administrative_compliance_workflow(
        args.schedules_dir,
        args.scenarios_path,
        args.behavioural_scenarios_path,
        args.mock_evidence_dir,
    )
    json_path, md_path = write_reports(args.reports_dir, results, summary)
    print(f"evaluated {len(results)} administrative workflow scenarios")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
