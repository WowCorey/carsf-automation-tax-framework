from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
WARNING = (
    "These are deterministic placeholder uncertainty ranges only. They are not statistical confidence "
    "intervals, forecasts, real uncertainty quantification, population estimates, ABS/HILDA/Census analysis, "
    "DSS/Services Australia modelling, Treasury modelling, PBO costing, welfare advice, eligibility law, legal "
    "advice, tax advice, or economic validation."
)


def load_report(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def fmt(value) -> str:
    if value is None:
        return "N/A"
    return f"{float(value):,.3f}"


st.set_page_config(page_title="CARSF Uncertainty Ranges", layout="wide")
st.title("Uncertainty Ranges")
st.caption("Deterministic low/base/high placeholder ranges for household and weighted subgroup outputs.")
st.warning(WARNING)

report = load_report(REPO_ROOT / "reports" / "uncertainty_ranges.json")
if not report:
    st.info("Run `python scripts/run_uncertainty_ranges.py` to generate uncertainty range reports.")
    st.stop()
    raise SystemExit(0)

examples = report.get("examples", [])
if not examples:
    st.info("No uncertainty range examples found in the generated report.")
    st.stop()
    raise SystemExit(0)

selected_name = st.selectbox("Uncertainty example", [item["name"] for item in examples])
selected = next((item for item in examples if item["name"] == selected_name), examples[0])
result = selected["uncertainty_result"]

st.markdown("### Overview")
st.write(
    {
        "example_id": selected["example_id"],
        "uncertainty_type": selected["uncertainty_type"],
        "status": selected["status"],
        "firm_level_liability_modified": selected["firm_level_liability_modified"],
    }
)

st.markdown("### Low/Base/High Values")
st.table(
    [
        {
            "Metric": item["metric_name"],
            "Low": fmt(item["low"]),
            "Base": fmt(item["base"]),
            "High": fmt(item["high"]),
            "Abs Width": fmt(item["absolute_range_width"]),
            "Rel Width": "N/A" if item["relative_range_width"] is None else f"{float(item['relative_range_width']):.2%}",
            "Stability": item["stability_band"],
        }
        for item in selected.get("range_results", [])
    ]
)

if selected["uncertainty_type"] == "household":
    st.markdown("### Household Uncertainty Result")
    st.table(
        [
            {"Metric": "Scenario", "Value": result["scenario_id"]},
            {"Metric": "Low case shock band", "Value": result["low_case_shock_band"]},
            {"Metric": "Base case shock band", "Value": result["base_case_shock_band"]},
            {"Metric": "High case shock band", "Value": result["high_case_shock_band"]},
            {"Metric": "Risk signal stability", "Value": result["risk_signal_stability"]},
            {"Metric": "Primary drivers", "Value": ", ".join(result.get("primary_uncertainty_drivers", [])) or "None"},
        ]
    )
else:
    st.markdown("### Weighted Subgroup Uncertainty Result")
    st.table(
        [
            {
                "Subgroup": subgroup["subgroup_id"],
                "Residual Gap Stability": (subgroup.get("residual_gap_range") or {}).get("stability_band", "missing"),
                "High/Critical Share Stability": (subgroup.get("high_critical_share_range") or {}).get("stability_band", "missing"),
                "Sensitivity": subgroup["subgroup_range_sensitivity"],
            }
            for subgroup in result.get("subgroup_results", [])
        ]
    )

st.markdown("### Summary Signals")
summary = report.get("summary", {})
st.table(
    [
        {"Metric": "Stable high-risk count", "Value": str(summary.get("stable_high_risk_count"))},
        {"Metric": "Stable low-risk count", "Value": str(summary.get("stable_low_risk_count"))},
        {"Metric": "Range-sensitive count", "Value": str(summary.get("range_sensitive_count"))},
        {"Metric": "Fragile metric count", "Value": str(summary.get("fragile_metric_count"))},
        {"Metric": "Stable high-risk signals", "Value": ", ".join(summary.get("strongest_stable_risk_signals", [])) or "None"},
        {"Metric": "Highest uncertainty items", "Value": ", ".join(summary.get("highest_uncertainty_items", [])) or "None"},
    ]
)

st.markdown("### Calibration Blockers")
for blocker in summary.get("calibration_blockers", []):
    st.markdown(f"- {blocker}")

st.markdown("### Plain-English Meaning")
st.write(selected.get("interpretation", ""))
st.write("Firm-level CARSF liability is not automatically modified by uncertainty range outputs.")

st.markdown("### Limitations and Non-Claims")
for item in report.get("metadata", {}).get("non_claims", [WARNING]):
    st.markdown(f"- {item}")
