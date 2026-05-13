from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
WARNING = (
    "These are prototype payment-interaction outputs only. They are not UBI policy, welfare advice, "
    "eligibility law, Centrelink/DSS/Services Australia modelling, Treasury costing, PBO costing, "
    "legal advice, tax advice, or economic validation."
)


def load_report(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def fmt_money(value) -> str:
    if value is None:
        return "N/A"
    return f"{float(value):,.2f}"


st.set_page_config(page_title="CARSF Payment Interactions", layout="wide")
st.title("Payment Interactions")
st.caption("Prototype targeting, baseline separation, phase rules, payment stacking, and support incidence.")
st.warning(WARNING)

report = load_report(REPO_ROOT / "reports" / "payment_interactions.json")
if not report:
    st.info("Run `python scripts/run_payment_interactions.py` to generate payment interaction reports.")
    st.stop()
    raise SystemExit(0)

examples = report.get("examples", [])
if not examples:
    st.info("No payment interaction examples found in the generated report.")
    st.stop()
    raise SystemExit(0)

selected_name = st.selectbox("Interaction example", [item["name"] for item in examples])
selected = next((item for item in examples if item["name"] == selected_name), examples[0])
inputs = selected["interaction_input"]
result = selected["interaction_result"]
incidence = result["support_incidence"]

st.markdown("### Overview")
st.write(
    {
        "example_id": selected["example_id"],
        "status": selected["status"],
        "interaction_risk_band": result["interaction_risk_band"],
        "targeting_risk_band": result["targeting_risk_band"],
        "firm_level_liability_modified": selected["firm_level_liability_modified"],
    }
)

st.markdown("### Baseline Cost Separation")
st.table(
    [
        {"Metric": "Existing baseline cost", "Value": fmt_money(result["baseline_cost"])},
        {"Metric": "New gross stack cost", "Value": fmt_money(result["gross_stack_cost"])},
        {"Metric": "New net stack cost", "Value": fmt_money(result["net_stack_cost"])},
        {"Metric": "Baseline kept separate", "Value": "true"},
    ]
)

st.markdown("### Targeting")
criteria = inputs["target_population"]["criteria"]
st.write(
    {
        "target_group": criteria.get("target_group"),
        "targeted_eligible_people": result["targeted_eligible_people"],
        "displaced_worker_required": criteria.get("displaced_worker_required"),
        "retraining_required": criteria.get("retraining_required"),
        "household_test_placeholder": criteria.get("household_test_placeholder"),
        "income_test_placeholder": criteria.get("income_test_placeholder"),
    }
)

st.markdown("### Phase and Payment Stack")
st.table(
    [
        {"Metric": "Phase multiplier", "Value": f"{float(result['phase_multiplier']):.2f}"},
        {"Metric": "Gross stack cost", "Value": fmt_money(result["gross_stack_cost"])},
        {"Metric": "Double-count adjustment", "Value": fmt_money(result["double_count_adjustment"])},
        {"Metric": "Net stack cost", "Value": fmt_money(result["net_stack_cost"])},
        {"Metric": "Residual support gap", "Value": fmt_money(result["residual_support_gap"])},
        {"Metric": "Combined Commonwealth/support gap", "Value": fmt_money(result["combined_commonwealth_gap"])},
    ]
)
st.dataframe(
    [
        {
            "Component": component["component_id"],
            "Type": component.get("component_type"),
            "Eligible people": component["eligible_people"],
            "Payment/person": component["payment_per_person"],
            "Priority": component.get("stack_priority"),
            "Mutually exclusive with": ", ".join(component.get("mutually_exclusive_with", [])) or "None",
        }
        for component in inputs["stack_components"]
    ],
    width="stretch",
)

st.markdown("### Support Fiscal Incidence Preview")
st.table(
    [
        {"Metric": "Gross support cost", "Value": fmt_money(incidence["gross_support_cost"])},
        {"Metric": "Household spending flow", "Value": fmt_money(incidence["household_spending_flow"])},
        {"Metric": "Placeholder GST recovery", "Value": fmt_money(incidence["placeholder_gst_recovery"])},
        {"Metric": "Hardship offset preview", "Value": fmt_money(incidence["hardship_offset_preview"])},
        {
            "Metric": "Net fiscal cost after placeholder offsets",
            "Value": fmt_money(incidence["net_fiscal_cost_after_placeholder_offsets"]),
        },
    ]
)
st.write("Support incidence offsets are shown separately and are not validated savings.")

st.markdown("### Plain-English Meaning")
st.write(selected.get("interpretation", ""))
st.write("Firm-level CARSF liability is not automatically modified by this payment-interaction preview.")

st.markdown("### Limitations and Non-Claims")
for item in report.get("metadata", {}).get("non_claims", [WARNING]):
    st.markdown(f"- {item}")
