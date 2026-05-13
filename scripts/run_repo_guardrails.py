"""Run repository-level CARSF guardrails and write reports."""

from __future__ import annotations

import json
import sys
from argparse import ArgumentParser
from dataclasses import asdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = REPO_ROOT / "model"
if str(MODEL_ROOT) not in sys.path:
    sys.path.insert(0, str(MODEL_ROOT))

from carsf.example_runner import report_metadata  # noqa: E402
from carsf.repo_guardrails import (  # noqa: E402
    REQUIRED_WARNING,
    RepoScanFinding,
    RepoScanResult,
    get_default_repo_guardrail_policy,
    scan_repo,
)


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def build_json_payload(result: RepoScanResult, metadata: dict[str, Any]) -> dict[str, Any]:
    policy = get_default_repo_guardrail_policy()
    return {
        "metadata": {
            **metadata,
            "status": "prototype_repository_guardrails_only",
            "non_claims": [REQUIRED_WARNING, *policy.non_claims],
        },
        "policy": policy.to_jsonable(),
        "result": result.to_jsonable(),
    }


def _finding_rows(findings: list[RepoScanFinding]) -> list[str]:
    if not findings:
        return ["| none | none | none | none | none |"]
    rows = []
    for finding in findings:
        rows.append(
            "| "
            f"{finding.path} | {finding.severity} | {finding.finding_type} | "
            f"{finding.line_number or 'N/A'} | {finding.message} |"
        )
    return rows


def build_markdown(result: RepoScanResult, metadata: dict[str, Any]) -> str:
    policy = get_default_repo_guardrail_policy()
    allowlisted = [finding for finding in result.findings if finding.finding_type == "allowlisted_synthetic_marker"]
    storage_findings = [
        finding for finding in result.findings if finding.finding_type in {"prohibited_path", "mock_missing_synthetic_flag"}
    ]
    report_findings = [
        finding for finding in result.findings if finding.finding_type in {"missing_report_non_claim", "raw_evidence_payload"}
    ]
    secret_findings = [
        finding for finding in result.findings if finding.finding_type in {"sensitive_marker", "prohibited_extension"}
    ]

    lines = [
        "# CARSF V1.5 Repository Guardrails",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report runs prototype repository-level guardrails for likely evidence leaks, secret markers, wrong storage zones, generated-report non-claims, and accidental real-data commits.",
        "",
        "## B. Non-Claims",
        "",
        f"- {REQUIRED_WARNING}",
    ]
    lines.extend(f"- {non_claim}" for non_claim in policy.non_claims)
    lines.extend(
        [
            "",
            "## C. Files Scanned/Skipped",
            "",
            f"- Files scanned: {result.files_scanned}",
            f"- Files skipped: {result.files_skipped}",
            f"- Clean: {str(result.clean).lower()}",
            "",
            "## D. Denied Findings",
            "",
            "| Path | Severity | Type | Line | Message |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    lines.extend(_finding_rows(result.denied_findings))
    lines.extend(
        [
            "",
            "## E. Warning Findings",
            "",
            "| Path | Severity | Type | Line | Message |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    lines.extend(_finding_rows(result.warning_findings))
    lines.extend(
        [
            "",
            "## F. Allowlisted Synthetic Fixture Findings",
            "",
            "| Path | Severity | Type | Line | Message |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    lines.extend(_finding_rows(allowlisted))
    lines.extend(
        [
            "",
            "## G. Storage Boundary Checks",
            "",
            f"- Prohibited paths: {', '.join(policy.prohibited_paths)}",
            f"- Allowed mock paths: {', '.join(policy.allowed_mock_paths)}",
            "",
            "| Path | Severity | Type | Line | Message |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    lines.extend(_finding_rows(storage_findings))
    lines.extend(
        [
            "",
            "## H. Generated Report Checks",
            "",
            "- Generated reports must include prototype/non-claim language.",
            "- Generated reports must not include raw evidence packet payload markers.",
            "",
            "| Path | Severity | Type | Line | Message |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    lines.extend(_finding_rows(report_findings))
    lines.extend(
        [
            "",
            "## I. Secret/Evidence Path Checks",
            "",
            f"- Prohibited extensions: {', '.join(policy.prohibited_extensions)}",
            "",
            "| Path | Severity | Type | Line | Message |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    lines.extend(_finding_rows(secret_findings))
    lines.extend(
        [
            "",
            "## J. Required Non-Claim Checks",
            "",
            "Required non-claim patterns are intentionally broad and prototype-only:",
            "",
        ]
    )
    lines.extend(f"- `{item}`" for item in policy.required_non_claims)
    lines.extend(
        [
            "",
            "## K. Limitations",
            "",
            "- These guardrails are over-blocking by design.",
            "- They are not a complete DLP, secret scanner, cybersecurity product, legal/privacy audit, Treasury control, ATO control, or forensic validation.",
            "- Passing this scan does not prove that the repository is free of sensitive content.",
            "- Real evidence must not enter this repository.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_reports(reports_dir: Path, result: RepoScanResult) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "repo_guardrails.json"
    md_path = reports_dir / "repo_guardrails.md"
    json_path.write_text(
        json.dumps(build_json_payload(result, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(result, metadata), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = ArgumentParser(description="Run CARSF repository guardrails.")
    parser.add_argument("--root", type=Path, default=REPO_ROOT)
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args()

    result = scan_repo(args.root)
    json_path, md_path = write_reports(args.reports_dir, result)
    print(f"repo guardrails clean: {str(result.clean).lower()}")
    print(f"files scanned: {result.files_scanned}")
    print(f"files skipped: {result.files_skipped}")
    print(f"denied findings: {len(result.denied_findings)}")
    print(f"warning findings: {len(result.warning_findings)}")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    if result.denied_findings:
        for finding in result.denied_findings[:20]:
            print(f"DENY {finding.path}:{finding.line_number or 0} {finding.finding_type}: {finding.message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
