from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = REPO_ROOT / "reports" / "behavioural_response_simulation.json"
WARNING = (
    "Behavioural response simulation is prototype-only deterministic placeholder scenario review. "
    "It does not predict taxpayer behaviour, estimate behavioural elasticity, implement ATO audit logic, "
    "create compliance-risk scoring, estimate actual tax payable, or modify firm-level CARSF liability."
)


def load_report(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def matrix_rows(rows: list[dict]) -> list[dict]:
    return [
        {
            "Scenario ID": item.get("scenario_id"),
            "Scenario Name": item.get("scenario_name"),
            "Sector Schedule": item.get("sector_schedule_id"),
            "Response Type": item.get("response_type"),
            "Pressure Band": item.get("response_pressure_band"),
            "Review Status": item.get("review_status"),
            "Countermeasures": ", ".join(item.get("countermeasure_categories", [])),
            "External Review": item.get("external_review_required"),
            "Do Not Predict": item.get("do_not_predict"),
            "Main Reason": item.get("main_reason"),
        }
        for item in rows
    ]


st.set_page_config(page_title="CARSF Behavioural Response", layout="wide")
st.title("Behavioural Response / Gaming Simulation")
st.caption("Synthetic pathway review for possible CARSF response pressure.")
st.warning(WARNING)
st.error("Do not use this page to predict conduct, score taxpayers, estimate compliance risk, or change liability.")

report = load_report(REPORT_PATH)
if not report:
    st.info("Run `python scripts/run_behavioural_response_simulation.py` to generate behavioural response reports.")
    st.stop()
    raise SystemExit(0)

summary = report.get("summary", {})
rows = report.get("behavioural_response_results", [])

st.markdown("### Summary Counts")
left, right = st.columns(2)
with left:
    st.table([{"Pressure Band": key, "Count": value} for key, value in summary.get("scenarios_by_pressure_band", {}).items()])
with right:
    st.table([{"Review Status": key, "Count": value} for key, value in summary.get("scenarios_by_review_status", {}).items()])

st.markdown("### Behavioural Response Matrix")
st.table(matrix_rows(rows))

st.markdown("### Scenarios By Review Status")
for status in sorted({item.get("review_status") for item in rows}):
    grouped = [item.get("scenario_id") for item in rows if item.get("review_status") == status]
    st.markdown(f"- `{status}`: {', '.join(grouped)}")

st.markdown("### Scenarios By Countermeasure Category")
categories = sorted({category for item in rows for category in item.get("countermeasure_categories", [])})
for category in categories:
    grouped = [item.get("scenario_id") for item in rows if category in item.get("countermeasure_categories", [])]
    st.markdown(f"- `{category}`: {', '.join(grouped)}")

st.markdown("### Calibration Blockers")
blockers = summary.get("calibration_blockers", [])
if blockers:
    for blocker in blockers:
        st.markdown(f"- {blocker}")
else:
    st.write("No blockers listed beyond global external calibration and methods review.")

st.markdown("### Non-Claims")
for item in report.get("metadata", {}).get("non_claims", [WARNING]):
    st.markdown(f"- {item}")
st.write("Every result is synthetic, do-not-predict, and does not modify firm-level CARSF liability.")
