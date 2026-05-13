from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "model"))

from carsf.repo_guardrails import REQUIRED_WARNING, get_default_repo_guardrail_policy, scan_repo  # noqa: E402


def load_report(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def finding_rows(findings: list[dict]) -> list[dict]:
    return [
        {
            "Path": finding.get("path"),
            "Severity": finding.get("severity"),
            "Type": finding.get("finding_type"),
            "Deny": finding.get("deny"),
            "Message": finding.get("message"),
        }
        for finding in findings
    ]


st.set_page_config(page_title="CARSF Repository Guardrails", layout="wide")
st.title("Repository Guardrails")
st.caption("Prototype CI/repository checks for likely evidence leaks, secret markers, and unsafe storage zones.")
st.warning(REQUIRED_WARNING)

policy = get_default_repo_guardrail_policy()
report = load_report(REPO_ROOT / "reports" / "repo_guardrails.json")

if report:
    result = report.get("result", {})
else:
    result = scan_repo(REPO_ROOT).to_jsonable()

st.markdown("### Latest Summary")
st.write(
    {
        "clean": result.get("clean"),
        "files_scanned": result.get("files_scanned"),
        "files_skipped": result.get("files_skipped"),
        "denied_findings": len(result.get("denied_findings", [])),
        "warning_findings": len(result.get("warning_findings", [])),
    }
)

st.markdown("### Denied Findings")
denied = finding_rows(result.get("denied_findings", []))
if denied:
    st.table(denied)
else:
    st.success("No denied findings in the latest repository guardrail report.")

st.markdown("### Warning Findings")
warnings = finding_rows(result.get("warning_findings", []))
if warnings:
    st.table(warnings)
else:
    st.info("No warning findings in the latest repository guardrail report.")

st.markdown("### Allowlisted Synthetic Fixtures")
allowlisted = [
    finding for finding in result.get("findings", []) if finding.get("finding_type") == "allowlisted_synthetic_marker"
]
if allowlisted:
    st.table(finding_rows(allowlisted))
else:
    st.info("No allowlisted synthetic fixture findings are present in the latest report.")

st.markdown("### Storage Boundary Rules")
st.write(
    {
        "prohibited_paths": policy.prohibited_paths,
        "prohibited_extensions": policy.prohibited_extensions,
        "allowed_mock_paths": policy.allowed_mock_paths,
        "allowed_synthetic_markers": policy.allowed_synthetic_markers,
    }
)

st.markdown("### CI Enforcement")
st.write(
    {
        "workflow": ".github/workflows/ci.yml",
        "guardrail_command": "python scripts/run_repo_guardrails.py",
        "failure_mode": "CI fails when denied findings exist.",
        "pre_commit": "Optional local hook in .pre-commit-config.yaml.",
    }
)

st.markdown("### Limitations")
for item in [
    "This is not a complete DLP or secret-scanning product.",
    "Passing the scan does not prove the repository is free of sensitive material.",
    "The checks are over-blocking by design and require review before any external evidence workflow.",
    "Real evidence, personal data, taxpayer data, business records, restricted data, and secrets must not enter this repository.",
]:
    st.markdown(f"- {item}")
