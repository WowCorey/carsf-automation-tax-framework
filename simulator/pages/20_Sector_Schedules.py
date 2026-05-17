from __future__ import annotations

from pathlib import Path

import streamlit as st
import yaml


REPO_ROOT = Path(__file__).resolve().parents[2]
WARNING = (
    "Sector schedules are prototype placeholders only. They are not calibrated. They are not legal schedules. "
    "They are not Treasury schedules. They are not ATO guidance. They are not ABS/ATO/DSS/PBO analysis. "
    "They do not contain real industry data. They must not be used to estimate actual tax payable."
)


def load_schedules() -> list[dict]:
    schedules = []
    for path in sorted((REPO_ROOT / "schedules").glob("*.yaml")):
        if path.name == "schedule_schema.yaml":
            continue
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict):
            loaded["_path"] = str(path.relative_to(REPO_ROOT))
            schedules.append(loaded)
    return schedules


def fmt(value) -> str:
    try:
        return f"{float(value):,.3f}"
    except (TypeError, ValueError):
        return "N/A"


st.set_page_config(page_title="CARSF Sector Schedules", layout="wide")
st.title("Sector Schedules")
st.caption("Prototype-only sector schedule coverage and placeholder measurement controls.")
st.warning(WARNING)

schedules = load_schedules()
if not schedules:
    st.info("No schedule YAML files found.")
    st.stop()
    raise SystemExit(0)

st.markdown("### Schedule Coverage")
st.table(
    [
        {
            "Schedule": schedule["schedule_name"],
            "Schedule ID": schedule["schedule_id"],
            "Canonical Output Unit": schedule["canonical_output_unit"],
            "Status": schedule["status"],
            "Calibration": schedule["calibration_status"],
        }
        for schedule in schedules
    ]
)

selected_name = st.selectbox("Schedule", [schedule["schedule_name"] for schedule in schedules])
selected = next((schedule for schedule in schedules if schedule["schedule_name"] == selected_name), schedules[0])

st.markdown("### Selected Schedule")
st.write(
    {
        "schedule_id": selected["schedule_id"],
        "canonical_output_unit": selected["canonical_output_unit"],
        "calibration_status": selected["calibration_status"],
        "placeholder_notice": selected.get("measurement_scope", {}).get("placeholder_notice"),
    }
)

left, right = st.columns(2)
with left:
    st.markdown("### AII Weights")
    st.table(
        [
            {"Component": name, "Weight": fmt(value)}
            for name, value in selected.get("aii", {}).get("weights", {}).items()
        ]
    )
with right:
    st.markdown("### QLC Weights")
    st.table(
        [
            {"Component": name, "Weight": fmt(value)}
            for name, value in selected.get("qlc", {}).get("weights", {}).items()
        ]
    )

st.markdown("### OPFTE / FRV / Caps")
st.table(
    [
        {"Metric": "OPFTE placeholder", "Value": fmt(selected.get("opfte_libc_placeholder", {}).get("value"))},
        {"Metric": "OPFTE unit", "Value": selected.get("opfte_libc_placeholder", {}).get("unit", "N/A")},
        {"Metric": "FRV floor", "Value": fmt(selected.get("frv", {}).get("floor_placeholder"))},
        {"Metric": "FRV standard", "Value": fmt(selected.get("frv", {}).get("standard_placeholder"))},
        {"Metric": "FRV full", "Value": fmt(selected.get("frv", {}).get("full_placeholder"))},
        {"Metric": "lambda_sector", "Value": fmt(selected.get("caps", {}).get("lambda_sector"))},
        {"Metric": "LAMBDA_sector", "Value": fmt(selected.get("caps", {}).get("LAMBDA_sector"))},
        {"Metric": "theta", "Value": fmt(selected.get("caps", {}).get("theta"))},
    ]
)

st.markdown("### Covered Activity Examples")
for item in selected.get("measurement_scope", {}).get("covered_activity_examples", []):
    st.markdown(f"- {item}")

st.markdown("### Placeholder Warnings")
for item in selected.get("placeholder_assumptions", []):
    st.markdown(f"- {item}")
if selected["schedule_id"] == "software_digital_platforms":
    st.error("Capital-base treatment for software firms remains unresolved and subject to AASB 138, tax counsel, and Treasury review.")

st.markdown("### Data Required For Real Calibration")
for item in selected.get("data_required_for_real_calibration", []):
    st.markdown(f"- {item}")

st.markdown("### Avoidance / Gaming Controls")
for key, value in selected.get("avoidance_controls", {}).items():
    st.markdown(f"- `{key}`: {value.get('placeholder_response', value)}")

st.markdown("### Non-Claims")
st.write("Values are placeholder-only and not calibrated benchmarks.")
st.write("Schedules do not modify firm-level CARSF liability logic.")
st.write("Schedules do not implement real multi-schedule attribution.")
