from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = REPO_ROOT / "reports" / "administrative_compliance_workflow.json"
WARNING = (
    "This is a prototype administrative workflow only. It is not a workflow endorsed by the ATO, "
    "not guidance from the ATO, not audit logic, not enforcement, not compliance scoring, and it "
    "does not estimate actual tax payable or modify firm-level CARSF liability."
)


def load_report(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def workflow_rows(rows: list[dict]) -> list[dict]:
    return [
        {
            "Scenario ID": item.get("scenario_id"),
            "Scenario Name": item.get("scenario_name"),
            "Sector": item.get("sector_schedule_id"),
            "Decision Band": item.get("workflow_decision_band"),
            "Status": item.get("workflow_status"),
            "Evidence Items": item.get("evidence_request_bundle", {}).get("requirement_count"),
            "External Review": item.get("external_review_required"),
            "Do Not Enforce": item.get("do_not_enforce"),
            "Main Reason": item.get("main_reason"),
        }
        for item in rows
    ]


st.set_page_config(page_title="CARSF Administrative Workflow", layout="wide")
st.title("Administrative Compliance Workflow")
st.caption("Synthetic administrative pathway review for CARSF prototype scenarios.")
st.warning(WARNING)
st.error("Do not use this page for real action, notices, penalties, compliance scoring, or liability changes.")

report = load_report(REPORT_PATH)
if not report:
    st.info("Run `python scripts/run_administrative_compliance_workflow.py` to generate administrative workflow reports.")
    st.stop()
    raise SystemExit(0)

summary = report.get("summary", {})
rows = report.get("administrative_workflow_results", [])

st.markdown("### Summary Counts")
left, right = st.columns(2)
with left:
    st.table([{"Decision Band": key, "Count": value} for key, value in summary.get("scenarios_by_decision_band", {}).items()])
with right:
    st.table([{"Workflow Status": key, "Count": value} for key, value in summary.get("scenarios_by_workflow_status", {}).items()])

st.markdown("### Administrative Workflow Matrix")
st.table(workflow_rows(rows))

st.markdown("### Scenarios By Workflow Status")
for status in sorted({item.get("workflow_status") for item in rows}):
    grouped = [item.get("scenario_id") for item in rows if item.get("workflow_status") == status]
    st.markdown(f"- `{status}`: {', '.join(grouped)}")

st.markdown("### Escalation Queues")
queues = sorted({assignment.get("queue_id") for item in rows for assignment in item.get("queue_assignments", [])})
for queue in queues:
    grouped = [
        item.get("scenario_id")
        for item in rows
        if any(assignment.get("queue_id") == queue for assignment in item.get("queue_assignments", []))
    ]
    st.markdown(f"- `{queue}`: {', '.join(grouped)}")

st.markdown("### Evidence Request Bundles")
for item in rows:
    bundle = item.get("evidence_request_bundle", {})
    st.markdown(
        f"- `{item.get('scenario_id')}`: {bundle.get('requirement_count', 0)} requirement(s) "
        f"({', '.join(bundle.get('requirement_ids', [])) or 'no mapped requirements'})"
    )

st.markdown("### Locked / Suppressed Cases")
locked = [
    item for item in rows if item.get("workflow_status") in {"locked_for_external_review", "suppress_until_calibrated", "external_review_required"}
]
if locked:
    for item in locked:
        st.markdown(f"- `{item.get('scenario_id')}`: `{item.get('workflow_status')}`")
else:
    st.write("No locked or suppressed cases in the generated report.")

st.markdown("### Calibration and External-Review Blockers")
blockers = summary.get("calibration_blockers", [])
if blockers:
    for blocker in blockers:
        st.markdown(f"- {blocker}")
else:
    st.write("No blockers listed beyond global external review and administrative-design review.")

st.markdown("### Non-Claims")
for item in report.get("metadata", {}).get("non_claims", [WARNING]):
    st.markdown(f"- {item}")
st.write("Every result is do-not-enforce, do-not-issue-notice, do-not-score-compliance, and does not modify firm-level CARSF liability.")
