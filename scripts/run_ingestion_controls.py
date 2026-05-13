"""Generate secure evidence-ingestion control reports for CARSF V1.5."""

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
from carsf.ingestion_audit import create_ingestion_audit_record  # noqa: E402
from carsf.redaction import create_redaction_plan  # noqa: E402
from carsf.retention import get_access_control_policy, get_retention_policy  # noqa: E402
from carsf.secure_ingestion import (  # noqa: E402
    IngestionRequest,
    evaluate_ingestion_request,
    get_default_ingestion_policy,
)
from carsf.sensitive_scan import scan_mapping_for_sensitive_markers  # noqa: E402


REPORT_WARNING = (
    "These controls are prototype governance controls only. They do not create legal, privacy, cybersecurity, "
    "evidentiary, forensic, Treasury, ATO, tax, or audit validation."
)


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def _request_paths(data_dir: Path) -> list[Path]:
    request_dir = data_dir / "mock_ingestion_requests"
    if not request_dir.exists():
        raise FileNotFoundError(f"missing mock ingestion request directory: {request_dir}")
    paths = sorted(request_dir.glob("*.yaml"))
    if not paths:
        raise FileNotFoundError(f"no mock ingestion request fixtures found in {request_dir}")
    return paths


def _load_request(path: Path) -> IngestionRequest:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"ingestion request must be a mapping: {path}")
    return IngestionRequest(
        request_id=str(loaded.get("request_id", "")),
        evidence_mode=str(loaded.get("evidence_mode", "")),
        source_description=str(loaded.get("source_description", "")),
        intended_use=str(loaded.get("intended_use", "")),
        storage_zone=str(loaded.get("storage_zone", "")),
        synthetic_mock_evidence_only=bool(loaded.get("synthetic_mock_evidence_only", False)),
        contains_personal_data=bool(loaded.get("contains_personal_data", False)),
        contains_real_business_data=bool(loaded.get("contains_real_business_data", False)),
        contains_restricted_data=bool(loaded.get("contains_restricted_data", False)),
        contains_secrets=bool(loaded.get("contains_secrets", False)),
        declared_sensitivity=str(loaded.get("declared_sensitivity", "unknown")),
        requested_by=loaded.get("requested_by"),
        metadata=dict(loaded.get("metadata", {}) or {}),
    )


def run_ingestion_controls(data_dir: Path) -> list[dict[str, Any]]:
    policy = get_default_ingestion_policy()
    rows: list[dict[str, Any]] = []
    previous_hash: str | None = None
    for path in _request_paths(data_dir):
        request = _load_request(path)
        scan = scan_mapping_for_sensitive_markers(request.to_jsonable())
        decision = evaluate_ingestion_request(request, policy)
        redaction = create_redaction_plan(scan, request.evidence_mode)
        retention_mode = request.evidence_mode if decision.allowed else "denied_or_non_synthetic"
        retention = get_retention_policy(retention_mode, request.storage_zone)
        access = get_access_control_policy(request.evidence_mode, request.declared_sensitivity)
        audit = create_ingestion_audit_record(decision, previous_hash)
        previous_hash = audit.record_hash
        rows.append(
            {
                "fixture_path": str(path.relative_to(REPO_ROOT)),
                "request": request.to_jsonable(),
                "sensitive_scan": scan.to_jsonable(),
                "decision": decision.to_jsonable(),
                "redaction_plan": redaction.to_jsonable(),
                "retention_policy": retention.to_jsonable(),
                "access_control_policy": access.to_jsonable(),
                "audit_record": audit.to_jsonable(),
            }
        )
    return rows


def build_json_payload(rows: list[dict[str, Any]], metadata: dict[str, Any]) -> dict[str, Any]:
    policy = get_default_ingestion_policy()
    return {
        "metadata": {
            **metadata,
            "status": "prototype_secure_ingestion_controls_only",
            "non_claims": [REPORT_WARNING, *policy.non_claims],
        },
        "policy": policy.to_jsonable(),
        "requests": rows,
    }


def build_markdown(rows: list[dict[str, Any]], metadata: dict[str, Any]) -> str:
    policy = get_default_ingestion_policy()
    denied = [row for row in rows if not row["decision"]["allowed"]]
    lines = [
        "# CARSF V1.5 Secure Evidence Ingestion Controls",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report previews default-deny ingestion controls before any non-synthetic evidence is ever handled.",
        "",
        "## B. Non-Claims",
        "",
        f"- {REPORT_WARNING}",
    ]
    lines.extend(f"- {non_claim}" for non_claim in policy.non_claims)
    lines.extend(
        [
            "",
            "## C. Default-Deny Policy",
            "",
            f"- Policy: `{policy.policy_id}`",
            f"- Default action: `{policy.default_action}`",
            f"- Allowed modes: {', '.join(policy.allowed_modes)}",
            "- Only synthetic mock evidence is allowed in this repository.",
            "- Any real personal, taxpayer, business, restricted, credential, or non-synthetic evidence is denied.",
            "",
            "## D. Storage Zones",
            "",
            f"- Allowed evidence storage zones: {', '.join(policy.allowed_storage_zones)}",
            f"- Prohibited evidence storage zones: {', '.join(policy.prohibited_storage_zones)}",
            "- Reports and docs may contain derived synthetic summary text only; they must not contain evidence payloads.",
            "",
            "## E. Ingestion Request Table",
            "",
            "| Request | Mode | Storage Zone | Synthetic Only | Sensitivity | Decision | Allowed | Required Approvals |",
            "| --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        request = row["request"]
        decision = row["decision"]
        lines.append(
            "| "
            f"{request['request_id']} | {request['evidence_mode']} | {request['storage_zone']} | "
            f"{str(request['synthetic_mock_evidence_only']).lower()} | {request['declared_sensitivity']} | "
            f"{decision['decision']} | {str(decision['allowed']).lower()} | "
            f"{', '.join(decision['required_approvals']) if decision['required_approvals'] else 'none'} |"
        )
    lines.extend(
        [
            "",
            "## F. Sensitive Scan Results",
            "",
            "| Request | Clean | Severity | Markers Found | Deny Ingestion |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        scan = row["sensitive_scan"]
        lines.append(
            "| "
            f"{row['request']['request_id']} | {str(scan['clean']).lower()} | {scan['severity']} | "
            f"{', '.join(scan['markers_found']) if scan['markers_found'] else 'none'} | "
            f"{str(scan['deny_ingestion']).lower()} |"
        )
    lines.extend(
        [
            "",
            "## G. Redaction Handling",
            "",
            "- Sensitive markers deny repo ingestion rather than creating redacted copies inside the repository.",
            "- Redaction plans describe external secure-system handling only and do not output original sensitive values.",
            "",
            "| Request | Redaction Required | Denied Fields | Main Warning |",
            "| --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        plan = row["redaction_plan"]
        lines.append(
            "| "
            f"{row['request']['request_id']} | {str(plan['required']).lower()} | "
            f"{', '.join(plan['denied_fields']) if plan['denied_fields'] else 'none'} | "
            f"{plan['warnings'][0] if plan['warnings'] else 'none'} |"
        )
    lines.extend(
        [
            "",
            "## H. Retention/Access-Control Policy",
            "",
            "| Request | Retention Action | Deletion Required | Access Policy | Approval Required |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        retention = row["retention_policy"]
        access = row["access_control_policy"]
        lines.append(
            "| "
            f"{row['request']['request_id']} | {retention['retention_action']} | "
            f"{str(retention['deletion_required']).lower()} | {access['policy_id']} | "
            f"{str(access['approval_required']).lower()} |"
        )
    lines.extend(
        [
            "",
            "## I. Audit-Record Preview",
            "",
            "| Request | Record ID | Allowed | Previous Hash | Record Hash |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        audit = row["audit_record"]
        lines.append(
            "| "
            f"{audit['request_id']} | {audit['record_id']} | {str(audit['allowed']).lower()} | "
            f"{audit['previous_record_hash'] or 'none'} | {audit['record_hash']} |"
        )
    lines.extend(
        [
            "",
            "## J. Denied Request Explanations",
            "",
        ]
    )
    for row in denied:
        lines.append(f"### {row['request']['request_id']}")
        for reason in row["decision"]["reasons"]:
            lines.append(f"- {reason}")
        lines.append("")
    lines.extend(
        [
            "## K. Why Real Evidence Must Not Enter This Repo",
            "",
            "- The repository is a policy-modelling prototype, not a secure evidence platform.",
            "- Git history is not an appropriate storage mechanism for real personal, taxpayer, restricted, credential, payroll, invoice, contract, or transfer-pricing evidence.",
            "- Any future real evidence workflow requires external secure storage, access controls, legal/privacy review, retention controls, and audit procedures.",
            "",
            "## L. Future Secure-System Requirements",
            "",
            "- External secure evidence store with encryption and access control.",
            "- Intake quarantine, malware scanning, DLP controls, and redaction tooling.",
            "- Role-based approval workflow for legal, tax, privacy, data-owner, and security review.",
            "- Immutable audit logs with retention and deletion controls.",
            "- Clear ban on committing real evidence or secrets to this repository.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_reports(reports_dir: Path, rows: list[dict[str, Any]]) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "secure_ingestion_controls.json"
    md_path = reports_dir / "secure_ingestion_controls.md"
    json_path.write_text(
        json.dumps(build_json_payload(rows, metadata), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(build_markdown(rows, metadata), encoding="utf-8")
    return json_path, md_path


def main() -> int:
    parser = ArgumentParser(description="Run prototype secure evidence-ingestion controls.")
    parser.add_argument("--data-dir", type=Path, default=REPO_ROOT / "data")
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args()
    rows = run_ingestion_controls(args.data_dir)
    json_path, md_path = write_reports(args.reports_dir, rows)
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
