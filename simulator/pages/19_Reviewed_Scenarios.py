from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
WARNING = (
    "Reviewed scenario outputs are prototype display-control signals only. They are not statistical validation, "
    "population estimates, real household modelling, ABS/HILDA/Census analysis, DSS/Services Australia modelling, "
    "ATO analysis, Treasury modelling, PBO costing, welfare advice, eligibility law, legal advice, tax advice, "
    "or economic validation."
)


def load_report(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def review_table(rows: list[dict]) -> list[dict]:
    return [
        {
            "Subject": item.get("subject_name"),
            "Category": item.get("review_category"),
            "Display": item.get("display_level"),
            "Reason": item.get("main_reason"),
            "Suppress Point Estimate": item.get("suppress_point_estimate"),
        }
        for item in rows
    ]


st.set_page_config(page_title="CARSF Reviewed Scenarios", layout="wide")
st.title("Reviewed Scenarios")
st.caption("Display-control classifications for deterministic synthetic uncertainty outputs.")
st.warning(WARNING)

report = load_report(REPO_ROOT / "reports" / "reviewed_scenarios.json")
if not report:
    st.info("Run `python scripts/run_reviewed_scenarios.py` to generate reviewed scenario reports.")
    st.stop()
    raise SystemExit(0)

summary = report.get("summary", {})
household_reviews = report.get("household_reviews", [])
weighted_reviews = report.get("weighted_subgroup_reviews", [])
all_reviews = household_reviews + weighted_reviews

st.markdown("### Summary Counts")
st.table(
    [
        {"Metric": "Prototype discussion signals", "Value": summary.get("prototype_discussion_signal_count")},
        {"Metric": "Discussion with strong warning", "Value": summary.get("discussion_with_strong_warning_count")},
        {"Metric": "Range-sensitive hidden point estimates", "Value": summary.get("range_sensitive_hidden_count")},
        {"Metric": "Fragile suppressed point estimates", "Value": summary.get("fragile_suppressed_count")},
        {"Metric": "Non-interpretable outputs", "Value": summary.get("non_interpretable_count")},
        {"Metric": "Missing uncertainty range outputs", "Value": summary.get("missing_uncertainty_range_count")},
        {"Metric": "External review required outputs", "Value": summary.get("external_review_required_count")},
    ]
)

st.markdown("### Household Scenario Review")
st.table(
    [
        {
            "Scenario": item.get("subject_name"),
            "Risk Signal Stability": item.get("risk_signal_stability"),
            "Low Case": item.get("low_case_shock_band"),
            "Base Case": item.get("base_case_shock_band"),
            "High Case": item.get("high_case_shock_band"),
            "Fragile Metrics": ", ".join(item.get("fragile_metrics", [])) or "None",
            "Review Category": item.get("review_category"),
            "Display Level": item.get("display_level"),
            "Main Reason": item.get("main_reason"),
        }
        for item in household_reviews
    ]
)

st.markdown("### Weighted Subgroup Review")
st.table(
    [
        {
            "Subgroup": item.get("subject_name"),
            "Residual Gap Stability": item.get("residual_gap_stability"),
            "High/Critical Share Stability": item.get("high_critical_share_stability"),
            "Subgroup Sensitivity": item.get("subgroup_range_sensitivity"),
            "Representative": item.get("representative_of_real_population"),
            "Review Category": item.get("review_category"),
            "Display Level": item.get("display_level"),
            "Main Reason": item.get("main_reason"),
        }
        for item in weighted_reviews
    ]
)

prototype = [item for item in all_reviews if item.get("review_category") == "prototype_discussion_signal"]
strong_warning = [item for item in all_reviews if item.get("review_category") == "discussion_with_strong_warning"]
hidden = [item for item in all_reviews if item.get("display_level") in {"hide_point_estimate", "external_review_only"}]
non_interpretable = [
    item
    for item in all_reviews
    if item.get("review_category") in {"non_interpretable_until_calibrated", "missing_uncertainty_range"}
]

left, right = st.columns(2)
with left:
    st.markdown("### Prototype Discussion Signals")
    st.table(review_table(prototype))
    st.markdown("### Warning-Only Signals")
    st.table(review_table(strong_warning))
with right:
    st.markdown("### Hidden / Suppressed Point Estimates")
    st.table(review_table(hidden))
    st.markdown("### Non-Interpretable Outputs")
    st.table(review_table(non_interpretable))

st.markdown("### Limitations and Non-Claims")
for item in report.get("metadata", {}).get("non_claims", [WARNING]):
    st.markdown(f"- {item}")
st.write("Stable prototype discussion signals still require external calibration and methods review.")
st.write("Firm-level CARSF liability is not modified by reviewed scenario classifications.")
