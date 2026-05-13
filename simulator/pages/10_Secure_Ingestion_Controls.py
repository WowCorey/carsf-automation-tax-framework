from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st
import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "model"))

from carsf.ingestion_audit import create_ingestion_audit_record  # noqa: E402
from carsf.redaction import create_redaction_plan  # noqa: E402
from carsf.retention import get_access_control_policy, get_retention_policy  # noqa: E402
from carsf.secure_ingestion import IngestionRequest, evaluate_ingestion_request, get_default_ingestion_policy  # noqa: E402
from carsf.sensitive_scan import scan_mapping_for_sensitive_markers  # noqa: E402


WARNING = (
    "These controls are prototype governance controls only. They do not create legal, privacy, cybersecurity, "
    "evidentiary, forensic, Treasury, ATO, tax, or audit validation."
)


def load_report(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def request_paths() -> list[Path]:
    fixture_dir = REPO_ROOT / "data" / "mock_ingestion_requests"
    if not fixture_dir.exists():
        return []
    return sorted(fixture_dir.glob("*.yaml"))


def load_request(path: Path) -> IngestionRequest:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
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


st.set_page_config(page_title="CARSF Secure Ingestion Controls", layout="wide")
st.title("Secure Ingestion Controls")
st.caption("Default-deny prototype controls before any non-synthetic evidence is handled.")
st.warning(WARNING)

policy = get_default_ingestion_policy()
report = load_report(REPO_ROOT / "reports" / "secure_ingestion_controls.json")
paths = request_paths()

st.markdown("### Default-Deny Policy")
st.write(policy.to_jsonable())

st.markdown("### Storage Zone Rules")
st.write(
    {
        "allowed_storage_zones": policy.allowed_storage_zones,
        "prohibited_storage_zones": policy.prohibited_storage_zones,
        "rule": "Only synthetic mock evidence is allowed under data/mock_evidence/.",
    }
)

st.markdown("### Fixture Request Outcomes")
if report:
    st.table(
        [
            {
                "Request": row["request"]["request_id"],
                "Mode": row["request"]["evidence_mode"],
                "Storage": row["request"]["storage_zone"],
                "Decision": row["decision"]["decision"],
                "Allowed": row["decision"]["allowed"],
                "Approvals": ", ".join(row["decision"]["required_approvals"]) or "none",
            }
            for row in report.get("requests", [])
        ]
    )
else:
    st.info("Run `python scripts/run_ingestion_controls.py` to generate secure ingestion reports.")

if not paths:
    st.stop()

selected = st.selectbox("Mock ingestion request", [path.name for path in paths])
request = load_request(next(path for path in paths if path.name == selected))
scan = scan_mapping_for_sensitive_markers(request.to_jsonable())
decision = evaluate_ingestion_request(request, policy)
redaction = create_redaction_plan(scan, request.evidence_mode)
retention = get_retention_policy(request.evidence_mode, request.storage_zone)
access = get_access_control_policy(request.evidence_mode, request.declared_sensitivity)
audit = create_ingestion_audit_record(decision)

st.markdown("### Sensitive Scan Results")
st.write(scan.to_jsonable())

st.markdown("### Redaction Plan Preview")
st.write(redaction.to_jsonable())

st.markdown("### Retention and Access Policy")
st.write({"retention": retention.to_jsonable(), "access": access.to_jsonable()})

st.markdown("### Audit Record Preview")
st.write(audit.to_jsonable())

st.markdown("### Warnings and Non-Claims")
for warning in decision.warnings + redaction.warnings + retention.warnings + policy.non_claims:
    st.markdown(f"- {warning}")
