from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
WARNING = (
    "These are synthetic household distributional scenarios only. They are not real household modelling, "
    "welfare advice, eligibility law, DSS/Services Australia modelling, ABS analysis, Treasury modelling, "
    "PBO costing, legal advice, tax advice, or economic validation."
)


def load_report(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def fmt_money(value) -> str:
    if value is None:
        return "N/A"
    return f"{float(value):,.2f}"


st.set_page_config(page_title="CARSF Distributional Scenarios", layout="wide")
st.title("Distributional Scenarios")
st.caption("Synthetic household budget, re-employment, payment cliff, regional stress, and shock-band preview.")
st.warning(WARNING)

report = load_report(REPO_ROOT / "reports" / "distributional_scenarios.json")
if not report:
    st.info("Run `python scripts/run_distributional_scenarios.py` to generate distributional scenario reports.")
    st.stop()
    raise SystemExit(0)

examples = report.get("examples", [])
if not examples:
    st.info("No distributional scenarios found in the generated report.")
    st.stop()
    raise SystemExit(0)

selected_name = st.selectbox("Synthetic household scenario", [item["name"] for item in examples])
selected = next((item for item in examples if item["name"] == selected_name), examples[0])
budget = selected["household_budget_result"]
reemployment = selected["reemployment_result"]
regional = selected["regional_stress_result"]
cliff = selected["payment_cliff_result"]
scenario = selected["scenario_result"]

st.markdown("### Overview")
st.write(
    {
        "scenario_id": selected["scenario_id"],
        "status": selected["status"],
        "household_type": selected["household"]["household_type"],
        "household_shock_band": scenario["household_shock_band"],
        "firm_level_liability_modified": selected["firm_level_liability_modified"],
    }
)

st.markdown("### Household Budget Result")
st.table(
    [
        {"Metric": "Pre-displacement income", "Value": fmt_money(budget["pre_displacement_income"])},
        {"Metric": "Post-displacement income", "Value": fmt_money(budget["post_displacement_income"])},
        {"Metric": "Income loss", "Value": fmt_money(budget["income_loss"])},
        {"Metric": "Existing support baseline", "Value": fmt_money(budget["existing_support_baseline"])},
        {"Metric": "Total basic costs", "Value": fmt_money(budget["total_basic_costs"])},
        {"Metric": "Immediate budget gap", "Value": fmt_money(budget["immediate_budget_gap"])},
        {"Metric": "Budget stress band", "Value": budget["budget_stress_band"]},
    ]
)

st.markdown("### Re-Employment Timing")
st.table(
    [
        {"Metric": "Months without full income", "Value": str(reemployment["months_without_full_income"] or "N/A")},
        {"Metric": "Interim recovery amount", "Value": fmt_money(reemployment["interim_income_recovery_amount"])},
        {"Metric": "Full recovery amount", "Value": fmt_money(reemployment["full_income_recovery_amount"])},
        {"Metric": "Re-employment risk band", "Value": reemployment["reemployment_risk_band"]},
    ]
)

st.markdown("### Regional Stress")
st.table(
    [
        {"Metric": "Regional stress score", "Value": f"{float(regional['regional_stress_score']):.3f}"},
        {"Metric": "Regional stress band", "Value": regional["regional_stress_band"]},
        {"Metric": "Drivers", "Value": ", ".join(regional.get("drivers", [])) or "None"},
    ]
)

st.markdown("### Payment Cliff Result")
if cliff:
    st.table(
        [
            {"Metric": "Support loss", "Value": fmt_money(cliff["support_loss"])},
            {"Metric": "Income gain", "Value": fmt_money(cliff["income_gain"])},
            {"Metric": "Net position change", "Value": fmt_money(cliff["net_position_change"])},
            {"Metric": "Cliff detected", "Value": str(cliff["cliff_detected"]).lower()},
            {"Metric": "Cliff severity band", "Value": cliff["cliff_severity_band"]},
        ]
    )
else:
    st.write("No payment cliff configured for this scenario.")

st.markdown("### Residual Household Gap After Support")
st.table(
    [
        {"Metric": "Transition support amount", "Value": fmt_money(scenario["transition_support_amount"])},
        {"Metric": "Residual household gap", "Value": fmt_money(scenario["residual_household_gap_after_support"])},
        {"Metric": "Household shock band", "Value": scenario["household_shock_band"]},
        {"Metric": "Primary risk drivers", "Value": ", ".join(scenario.get("primary_risk_drivers", [])) or "None"},
    ]
)

st.markdown("### Distributional Summary")
summary = report.get("summary", {})
st.table(
    [
        {"Metric": "Scenario count", "Value": str(summary.get("scenario_count"))},
        {"Metric": "Low shock count", "Value": str(summary.get("low_shock_count"))},
        {"Metric": "Medium shock count", "Value": str(summary.get("medium_shock_count"))},
        {"Metric": "High shock count", "Value": str(summary.get("high_shock_count"))},
        {"Metric": "Critical shock count", "Value": str(summary.get("critical_shock_count"))},
        {"Metric": "Average residual gap", "Value": fmt_money(summary.get("average_residual_gap_placeholder"))},
        {"Metric": "Highest-risk households", "Value": ", ".join(summary.get("highest_risk_households", [])) or "None"},
    ]
)

st.markdown("### Plain-English Meaning")
st.write(selected.get("interpretation", ""))
st.write("Firm-level CARSF liability is not automatically modified by this distributional scenario preview.")

st.markdown("### Limitations and Non-Claims")
for item in report.get("metadata", {}).get("non_claims", [WARNING]):
    st.markdown(f"- {item}")
