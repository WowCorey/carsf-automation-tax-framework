"""Generate synthetic mock evidence workflow reports for CARSF V1.5."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from dataclasses import asdict, replace
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = REPO_ROOT / "model"
if str(MODEL_ROOT) not in sys.path:
    sys.path.insert(0, str(MODEL_ROOT))

from carsf.classification import classify_packet  # noqa: E402
from carsf.evidence import assess_evidence  # noqa: E402
from carsf.evidence_packet import (  # noqa: E402
    MOCK_PACKET_NON_CLAIM,
    EvidencePacket,
    EvidencePacketSummary,
    load_evidence_packet,
    summarise_evidence_packet,
)
from carsf.example_runner import report_metadata  # noqa: E402
from carsf.review_workflow import evaluate_review_transition  # noqa: E402


WORKFLOW_WARNING = (
    "These packets are synthetic mock evidence only. They do not validate any real liability, "
    "tax position, audit finding, legal conclusion, Treasury assessment, ATO assessment, or economic claim."
)


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def _target_state(summary: EvidencePacketSummary) -> str:
    flags = set(summary.review_flags)
    if "needs_privacy_review" in flags:
        return "needs_privacy_review"
    if "needs_tax_review" in flags:
        return "needs_tax_review"
    if "needs_legal_review" in flags:
        return "needs_legal_review"
    if "needs_calibration" in flags:
        return "needs_calibration"
    if summary.missing_items or summary.low_confidence_items:
        return "partial"
    return "sufficient_for_prototype"


def _packet_paths(data_dir: Path) -> list[Path]:
    mock_dir = data_dir / "mock_evidence"
    if not mock_dir.exists():
        raise FileNotFoundError(f"missing mock evidence directory: {mock_dir}")
    paths = sorted(mock_dir.glob("*.yaml"))
    if not paths:
        raise FileNotFoundError(f"no mock evidence packets found in {mock_dir}")
    return paths


def run_mock_evidence_workflow(data_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in _packet_paths(data_dir):
        packet = load_evidence_packet(path)
        summary = summarise_evidence_packet(packet)
        classification = classify_packet(packet)
        placeholder_summary = replace(summary, review_state="placeholder_only")
        submit_transition = evaluate_review_transition(placeholder_summary, "submitted_mock")
        target = _target_state(summary)
        target_transition = evaluate_review_transition(summary, target)
        assessment = assess_evidence(
            {
                "status": "illustrative_placeholder",
                "placeholder_notice": "synthetic mock evidence workflow only",
            },
            packet.created_for,
            evidence_packet=packet,
        )
        rows.append(
            {
                "packet_path": str(path.relative_to(REPO_ROOT)),
                "packet": packet.to_jsonable(),
                "summary": summary.to_jsonable(),
                "classification": classification,
                "placeholder_to_submitted": submit_transition.to_jsonable(),
                "target_transition": target_transition.to_jsonable(),
                "evidence_assessment": assessment.to_jsonable(),
                "missing_evidence": assessment.missing_requirements,
            }
        )
    return rows


def build_json_payload(rows: list[dict[str, Any]], metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": "synthetic_mock_evidence_workflow_only",
            "non_claims": [
                WORKFLOW_WARNING,
                MOCK_PACKET_NON_CLAIM,
                "Mock evidence can support prototype workflow testing only; it cannot create real-world sufficiency.",
            ],
            "secure_ingestion_controls": {
                "report_markdown": "reports/secure_ingestion_controls.md",
                "report_json": "reports/secure_ingestion_controls.json",
                "rule": "Only synthetic mock evidence is allowed in this repo; non-synthetic evidence requires external secure-system design.",
            },
        },
        "packets": rows,
    }


def _count_by_status(rows: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for row in rows:
        status = row["evidence_assessment"]["status"]
        counts[status] = counts.get(status, 0) + 1
    return counts


def build_markdown(rows: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    lines = [
        "# CARSF V1.5 Controlled Mock Evidence Workflow",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report tests how synthetic evidence packets can be submitted, summarised, classified, and moved through prototype review states.",
        "",
        "## B. Non-Claims",
        "",
        f"- {WORKFLOW_WARNING}",
        "- Mock sufficiency is not legal, tax, Treasury, ATO, ABS, Fair Work, audit, forensic, or economic validation.",
        "- No personal data, restricted government data, real taxpayer data, or real business evidence is included.",
        "",
        "## C. Evidence Packet Summary Table",
        "",
        "| Packet | Linked Example | Items | Sufficient | Partial | Missing | Low Confidence | Review State | Privacy | Secrecy |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |",
    ]
    for row in rows:
        summary = row["summary"]
        lines.append(
            "| "
            f"{summary['packet_id']} | {summary['linked_example_id']} | {summary['item_count']} | "
            f"{summary['sufficient_items']} | {summary['partial_items']} | {summary['missing_items']} | "
            f"{summary['low_confidence_items']} | {summary['review_state']} | "
            f"{summary['privacy_classification']} | {summary['secrecy_classification']} |"
        )
    lines.extend(
        [
            "",
            "## D. Review-State Transitions",
            "",
            "| Packet | Placeholder -> Submitted | Target State | Allowed | Approved State | Main Reason |",
            "| --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        submit = row["placeholder_to_submitted"]
        target = row["target_transition"]
        lines.append(
            "| "
            f"{row['summary']['packet_id']} | {submit['approved_state']} | {target['requested_state']} | "
            f"{str(target['allowed']).lower()} | {target['approved_state']} | {target['reasons'][-1]} |"
        )
    lines.extend(
        [
            "",
            "## E. Privacy/Secrecy Classifications",
            "",
            "| Packet | Privacy | Secrecy | Review Required | Review Flags |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        classification = row["classification"]
        summary = row["summary"]
        lines.append(
            "| "
            f"{summary['packet_id']} | {classification['privacy_classification']} | "
            f"{classification['secrecy_classification']} | {str(classification['review_required']).lower()} | "
            f"{', '.join(summary['review_flags']) if summary['review_flags'] else 'none'} |"
        )
    lines.extend(
        [
            "",
            "## F. Example-by-Example Mock Evidence Outcomes",
            "",
            "| Packet | Evidence Status | Missing Requirements | Low Confidence Items | Outcome Meaning |",
            "| --- | --- | ---: | ---: | --- |",
        ]
    )
    for row in rows:
        assessment = row["evidence_assessment"]
        outcome = (
            "Prototype-only mock evidence has gaps."
            if assessment["status"] == "partial"
            else "Prototype-only mock evidence covers the requested packet requirements."
        )
        lines.append(
            "| "
            f"{row['summary']['packet_id']} | {assessment['status']} | "
            f"{len(assessment['missing_requirements'])} | {len(assessment['low_confidence_items'])} | {outcome} |"
        )
    lines.extend(
        [
            "",
            "## G. What Evidence Is Still Missing",
            "",
        ]
    )
    for row in rows:
        missing = row["missing_evidence"]
        lines.append(f"### {row['summary']['packet_id']}")
        if not missing:
            lines.append("- No missing requirements for the requested mock scope, but this is not real-world sufficiency.")
        else:
            for requirement in missing[:20]:
                lines.append(f"- `{requirement}`")
            if len(missing) > 20:
                lines.append(f"- ... {len(missing) - 20} more omitted for readability.")
        lines.append("")
    lines.extend(
        [
            "## H. Legal/Tax/Privacy Review Triggers",
            "",
            "| Packet | Triggers |",
            "| --- | --- |",
        ]
    )
    for row in rows:
        flags = row["summary"]["review_flags"]
        lines.append(f"| {row['summary']['packet_id']} | {', '.join(flags) if flags else 'none'} |")
    lines.extend(
        [
            "",
            "## I. Why Mock Sufficiency Is Not Real Sufficiency",
            "",
            "- The packets are deliberately synthetic and exist only to test workflow state changes.",
            "- They do not contain audited source records, government data, personal data, restricted data, or final calibration values.",
            "- A prototype status such as `partial` or `sufficient_for_prototype` is not a legal conclusion, tax position, audit finding, Treasury assessment, ATO assessment, or economic claim.",
            "",
            "Status counts:",
            "",
        ]
    )
    for status, count in sorted(_count_by_status(rows).items()):
        lines.append(f"- `{status}`: {count}")
    lines.extend(
        [
            "",
            "## J. Secure Ingestion Controls",
            "",
            "- Mock evidence is allowed only because it is synthetic.",
            "- Non-synthetic evidence requires secure ingestion controls and external secure-system design.",
            "- Real evidence, personal data, taxpayer data, business records, restricted government data, secrets, credentials, invoices, contracts, and employment records must not be committed to this repo.",
            "- Run `python scripts/run_ingestion_controls.py` to generate `reports/secure_ingestion_controls.md` and `reports/secure_ingestion_controls.json`.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_reports(reports_dir: Path, rows: list[dict[str, Any]]) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "mock_evidence_workflow.json"
    md_path = reports_dir / "mock_evidence_workflow.md"
    json_path.write_text(
        json.dumps(build_json_payload(rows, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(rows, metadata), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = ArgumentParser(description="Run synthetic mock evidence workflow reports.")
    parser.add_argument("--data-dir", type=Path, default=REPO_ROOT / "data")
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args()
    rows = run_mock_evidence_workflow(args.data_dir)
    json_path, md_path = write_reports(args.reports_dir, rows)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
