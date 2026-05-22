"""Run the CARSF V1.5 full repo integrity upgrade and gap audit."""

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
from carsf.full_repo_integrity_upgrade_audit import (  # noqa: E402
    FINDING_CATEGORY_VALUES,
    FINDING_SEVERITY_VALUES,
    FINDING_STATUS_VALUES,
    FULL_REPO_AUDIT_NON_CLAIMS,
    build_full_repo_integrity_audit_result,
    find_forbidden_affirmative_repo_claims,
)


DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "audit" / "full_repo_integrity_upgrade_manifest.yaml"
DEFAULT_REPORTS_DIR = REPO_ROOT / "reports"
REPORT_STATUS = "full_repo_integrity_upgrade_gap_audit_only"


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"manifest must be a mapping: {path}")
    return payload


def _join(values: list[str] | None) -> str:
    if not values:
        return "None"
    return ", ".join(str(item) for item in values)


def _simple_table(headers: list[str], rows: list[list[Any]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(item) for item in row) + " |")
    return lines


def _coverage_table(rows: list[Any], fields: list[str]) -> list[str]:
    output = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        data = _jsonable(row)
        output.append("| " + " | ".join(str(data.get(field, "")) for field in fields) + " |")
    return output


def _summary_lines(summary: Any) -> list[str]:
    return [f"- {key}: {value}" for key, value in _jsonable(summary).items()]


def _build_json_payload(result: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": FULL_REPO_AUDIT_NON_CLAIMS,
            "finding_severity_values": sorted(FINDING_SEVERITY_VALUES),
            "finding_status_values": sorted(FINDING_STATUS_VALUES),
            "finding_category_values": sorted(FINDING_CATEGORY_VALUES),
        },
        "summary": _jsonable(result.summary),
        "full_repo_integrity_upgrade_audit": _jsonable(result),
    }


def _build_markdown(result: Any, metadata: dict[str, Any]) -> str:
    lines: list[str] = [
        "# CARSF V1.5 Full Repo Integrity Upgrade / Bug Check / Gap Audit",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "Build 34.5 audits the repository-wide runner, report, manifest, dashboard, documentation, data-boundary, placeholder-boundary, calibration-boundary, scenario-constraint, guardrail, and non-claim state before the next reviewer handoff pack.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in result.non_claims)
    lines.extend(["", "## C. Audit Scope", ""])
    lines.extend(f"- {item}" for item in ["repo structure", "Python modules", "runners", "reports", "JSON outputs", "manifests", "dashboards", "CI", "tests", "guardrails", "missing factors"])
    lines.extend(["", "## D. Repo-Wide Build Coverage Matrix", ""])
    lines.extend(_simple_table(["Build or Layer", "Runner Exists", "CI Referenced", "Markdown", "JSON", "Status"], [[row["build_or_layer"], row["runner_exists"], row["ci_referenced"], row["markdown_report_exists"], row["json_report_exists"], row["status"]] for row in result.build_coverage_matrix]))
    lines.extend(["", "## E. Runner Coverage Matrix", ""])
    lines.extend(_coverage_table(result.runner_coverage_matrix, ["runner_path", "exists", "ci_referenced", "status"]))
    lines.extend(["", "## F. Report Coverage Matrix", ""])
    lines.extend(_coverage_table(result.report_coverage_matrix, ["report_stem", "markdown_report", "json_report", "markdown_exists", "json_exists", "status"]))
    lines.extend(["", "## G. JSON/Markdown Result Coverage", ""])
    lines.extend(_coverage_table(result.result_coverage_matrix, ["report_path", "false_flags_clean", "status"]))
    lines.extend(["", "## H. CI Coverage", ""])
    lines.extend(["- CI references the full repo audit runner after the public aggregate scenario constraint layer and before repository guardrails.", "- CI YAML parsing now covers schedules, examples, data, and release."])
    lines.extend(["", "## I. Dashboard Coverage", ""])
    lines.extend(_coverage_table(result.dashboard_coverage_matrix, ["artifact", "expected_reference", "reference_present", "status"]))
    lines.extend(["", "## J. Release Manifest Coverage", ""])
    lines.extend(_coverage_table(result.release_manifest_coverage, ["artifact", "expected_reference", "reference_present", "status"]))
    lines.extend(["", "## K. Documentation Coverage", ""])
    lines.extend(_coverage_table(result.docs_coverage, ["artifact", "expected_reference", "reference_present", "status"]))
    lines.extend(["", "## L. Public Data Boundary Audit", ""])
    lines.extend(_coverage_table(result.public_data_boundary_audit, ["guardrail_id", "category", "covered", "evidence", "status"]))
    lines.extend(["", "## M. Placeholder Boundary Audit", ""])
    lines.extend(_coverage_table(result.placeholder_boundary_audit, ["guardrail_id", "category", "covered", "evidence", "status"]))
    lines.extend(["", "## N. Calibration Boundary Audit", ""])
    lines.extend(_coverage_table(result.calibration_boundary_audit, ["guardrail_id", "category", "covered", "evidence", "status"]))
    lines.extend(["", "## O. Scenario Constraint Audit", ""])
    lines.extend(_coverage_table(result.scenario_constraint_audit, ["guardrail_id", "category", "covered", "evidence", "status"]))
    lines.extend(["", "## P. Guardrail Audit", ""])
    lines.extend(_coverage_table(result.guardrail_audit, ["guardrail_id", "category", "covered", "evidence", "status"]))
    lines.extend(["", "## Q. Non-Claim Boundary Audit", ""])
    lines.extend(_coverage_table(result.non_claim_boundary_audit, ["artifact", "required_phrases_present", "missing_phrases", "status"]))
    lines.extend(["", "## R. Safe Fixes Applied", ""])
    lines.extend(_coverage_table(result.safe_fixes, ["fix_id", "description", "files_changed", "status"]))
    lines.extend(["", "## S. Bugs Fixed", ""])
    lines.extend(_coverage_table([item for item in result.findings if item.status == "fixed"], ["finding_id", "severity", "category", "title", "details"]))
    lines.extend(["", "## T. Missing Factors Identified", ""])
    lines.extend(_coverage_table(result.missing_factors, ["missing_factor_id", "factor_name", "category", "gap_description", "blocking_status"]))
    lines.extend(["", "## U. Missing Data Dependencies", ""])
    lines.extend(_coverage_table(result.data_dependencies, ["dependency_id", "data_needed", "current_status", "restricted_data_required", "can_be_loaded_now", "why_not_loaded"]))
    lines.extend(["", "## V. External Review Dependencies", ""])
    lines.extend(_coverage_table(result.external_review_dependencies, ["review_id", "review_type", "why_required", "blocking_status", "recommended_reviewer_profile"]))
    lines.extend(["", "## W. Items Blocked Inside Repo", ""])
    lines.extend(_coverage_table(result.items_blocked_inside_repo, ["gap_id", "category", "description", "status", "recommended_action"]))
    lines.extend(["", "## X. What The Repo Can Currently Claim", ""])
    lines.extend(f"- {item}" for item in result.what_repo_can_currently_claim)
    lines.extend(["", "## Y. What The Repo Must Not Claim", ""])
    lines.extend(f"- {item}" for item in result.what_repo_must_not_claim)
    lines.extend(["", "## Z. Recommended Next Builds", ""])
    lines.extend(f"- {item}" for item in result.recommended_next_builds)
    lines.extend(["", "## Summary Flags", ""])
    lines.extend(_summary_lines(result.summary))
    lines.append("")
    return "\n".join(lines)


def run(manifest_path: Path, reports_dir: Path) -> dict[str, Any]:
    result = build_full_repo_integrity_audit_result(_load_yaml(manifest_path), REPO_ROOT)
    metadata = report_metadata()
    reports_dir.mkdir(parents=True, exist_ok=True)
    payload = _build_json_payload(result, metadata)
    markdown = _build_markdown(result, metadata)
    combined = markdown + "\n" + json.dumps(payload, sort_keys=True)
    findings = find_forbidden_affirmative_repo_claims(combined)
    source_finding_count = int(payload["summary"].get("forbidden_claim_findings", 0))
    if findings or source_finding_count:
        raise ValueError(
            "forbidden affirmative full-repo audit claims found: "
            f"source_scan={source_finding_count}, generated_report_scan={findings}"
        )
    json_path = reports_dir / "full_repo_integrity_upgrade_audit.json"
    md_path = reports_dir / "full_repo_integrity_upgrade_audit.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return payload


def parse_args() -> ArgumentParser:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS_DIR)
    return parser


def main() -> int:
    args = parse_args().parse_args()
    payload = run(args.manifest, args.reports_dir)
    summary = payload["summary"]
    print(f"full repo integrity audit created: {summary['full_repo_integrity_audit_created']}")
    print(f"safe fixes applied: {summary['safe_fixes_applied']}")
    print(f"runner coverage complete: {summary['runner_coverage_complete']}")
    print(f"report coverage complete: {summary['report_coverage_complete']}")
    print(f"json report coverage complete: {summary['json_report_coverage_complete']}")
    print(f"dashboard coverage complete: {summary['dashboard_coverage_complete']}")
    print(f"release manifest coverage complete: {summary['release_manifest_coverage_complete']}")
    print(f"docs coverage complete: {summary['docs_coverage_complete']}")
    print(f"public data boundary clean: {summary['public_data_boundary_clean']}")
    print(f"placeholder boundary clean: {summary['placeholder_boundary_clean']}")
    print(f"calibration boundary clean: {summary['calibration_boundary_clean']}")
    print(f"scenario constraint boundary clean: {summary['scenario_constraint_boundary_clean']}")
    print(f"guardrails clean: {summary['guardrails_clean']}")
    print(f"forbidden claim findings: {summary['forbidden_claim_findings']}")
    print(f"new data loaded: {summary['new_data_loaded']}")
    print(f"calibration completed: {summary['calibration_completed']}")
    print(f"validation claimed: {summary['validation_claimed']}")
    print(f"actual tax payable determined: {summary['actual_tax_payable_determined']}")
    print(f"firm-level liability logic modified: {summary['firm_level_liability_logic_modified']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
