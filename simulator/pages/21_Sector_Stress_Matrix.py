from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = REPO_ROOT / "reports" / "sector_stress_matrix.json"
WARNING = (
    "The sector stress matrix is prototype metadata review only. It is not calibrated. "
    "It is not a real-world ranking of sectors. It is not Treasury modelling, ATO guidance, "
    "ABS/ATO/DSS/PBO analysis, economic validation, investment advice, legal advice, or tax advice. "
    "It does not use real industry data, does not estimate actual tax payable, and does not modify "
    "firm-level CARSF liability logic."
)


def load_report(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def matrix_rows(rows: list[dict]) -> list[dict]:
    return [
        {
            "Schedule ID": item.get("schedule_id"),
            "Schedule Name": item.get("schedule_name"),
            "Automation Intensity": item.get("automation_intensity_placeholder"),
            "QLC Vulnerability": item.get("qlc_vulnerability_placeholder"),
            "AAVA Sensitivity": item.get("aava_sensitivity_placeholder"),
            "Incidence Risk": item.get("incidence_risk_placeholder"),
            "Investment Risk": item.get("investment_deterrence_risk_placeholder"),
            "Avoidance / Gaming Risk": item.get("avoidance_gaming_risk_placeholder"),
            "Calibration Difficulty": item.get("calibration_difficulty_placeholder"),
            "Legal Attribution Difficulty": item.get("legal_attribution_difficulty_placeholder"),
            "Display Status": item.get("display_control_status"),
            "Do Not Rank": item.get("do_not_rank"),
            "Main Reason": item.get("main_reason"),
        }
        for item in rows
    ]


st.set_page_config(page_title="CARSF Sector Stress Matrix", layout="wide")
st.title("Sector Stress Matrix")
st.caption("Metadata-only placeholder review bands for prototype sector schedules.")
st.warning(WARNING)
st.error("Do not rank sectors using this matrix. Every row remains prototype-only and marked do-not-rank.")

report = load_report(REPORT_PATH)
if not report:
    st.info("Run `python scripts/run_sector_stress_matrix.py` to generate sector stress matrix reports.")
    st.stop()
    raise SystemExit(0)

summary = report.get("summary", {})
rows = report.get("stress_matrix", [])

st.markdown("### Summary Counts")
band_counts = summary.get("stress_band_counts", {})
display_counts = summary.get("display_status_counts", {})
left, right = st.columns(2)
with left:
    st.table([{"Stress Band": key, "Count": value} for key, value in band_counts.items()])
with right:
    st.table([{"Display Status": key, "Count": value} for key, value in display_counts.items()])

st.markdown("### Sector Stress Matrix")
st.table(matrix_rows(rows))

st.markdown("### Display-Control Groups")
for status in sorted({item.get("display_control_status") for item in rows}):
    grouped = [item.get("schedule_id") for item in rows if item.get("display_control_status") == status]
    st.markdown(f"- `{status}`: {', '.join(grouped)}")

st.markdown("### Calibration Blockers")
blockers = summary.get("calibration_blockers", [])
if blockers:
    for blocker in blockers:
        st.markdown(f"- {blocker}")
else:
    st.write("No blockers listed in the generated report.")

st.markdown("### Non-Claims")
for item in report.get("metadata", {}).get("non_claims", [WARNING]):
    st.markdown(f"- {item}")
st.write("All schedules remain placeholder-only and subject to external calibration, legal review, and methods review.")
