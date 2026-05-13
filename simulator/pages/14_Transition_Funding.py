from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
WARNING = (
    "These are prototype transition-payment funding outputs only. They are not UBI policy, welfare advice, "
    "DSS modelling, Services Australia modelling, Treasury costing, PBO costing, legal advice, tax advice, "
    "or economic validation."
)


def load_report(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def fmt_money(value) -> str:
    if value is None:
        return "N/A"
    return f"{float(value):,.2f}"


def fmt_rate(value) -> str:
    if value is None:
        return "N/A"
    return f"{float(value):.2%}"


st.set_page_config(page_title="CARSF Transition Funding", layout="wide")
st.title("Transition Funding")
st.caption("Non-operative placeholder preview for transition payments, UBI-lite, retraining support, and automation-dividend funding.")
st.warning(WARNING)

report = load_report(REPO_ROOT / "reports" / "transition_funding.json")
if not report:
    st.info("Run `python scripts/run_transition_funding.py` to generate transition funding reports.")
    st.stop()
    raise SystemExit(0)

examples = report.get("examples", [])
if not examples:
    st.info("No transition funding examples found in the generated report.")
    st.stop()
    raise SystemExit(0)

selected_name = st.selectbox("Payment design", [item["name"] for item in examples])
selected = next((item for item in examples if item["name"] == selected_name), examples[0])
portfolio = selected["portfolio_result"]
funding = selected["funding_result"]
sensitivity = selected["sensitivity_result"]

st.markdown("### Overview")
st.write(
    {
        "example_id": selected["example_id"],
        "fiscal_trajectory_id": selected["fiscal_trajectory_id"],
        "status": selected["status"],
        "firm_level_liability_modified": selected["firm_level_liability_modified"],
    }
)

st.markdown("### Design Cost Summary")
st.table(
    [
        {
            "Design": design["design_id"],
            "Eligible people": f"{float(design['eligible_people']):,.2f}",
            "Covered people": f"{float(design['covered_people']):,.2f}",
            "Base payment": fmt_money(design["base_payment_cost"]),
            "Retraining": fmt_money(design["retraining_component_cost"]),
            "Admin": fmt_money(design["administrative_cost"]),
            "Total": fmt_money(design["total_program_cost"]),
        }
        for design in portfolio["design_results"]
    ]
)

st.markdown("### Funding Coverage")
st.table(
    [
        {"Metric": "Total program cost", "Value": fmt_money(portfolio["total_program_cost"])},
        {"Metric": "Automation revenue available", "Value": fmt_money(portfolio["automation_revenue_available"])},
        {"Metric": "Funding coverage ratio", "Value": fmt_rate(portfolio["funding_coverage_ratio"])},
        {"Metric": "Residual payment gap", "Value": fmt_money(portfolio["residual_funding_gap"])},
        {"Metric": "Combined Commonwealth/payment gap", "Value": fmt_money(portfolio["residual_commonwealth_gap_plus_payment_gap"])},
        {"Metric": "Affordability band", "Value": portfolio["affordability_band"]},
        {"Metric": "First high cliff-risk year", "Value": str(funding["first_high_cliff_risk_year"] or "N/A")},
        {"Metric": "First critical cliff-risk year", "Value": str(funding["first_critical_cliff_risk_year"] or "N/A")},
    ]
)

st.markdown("### Year-by-Year Funding Trajectory")
st.dataframe(
    [
        {
            "Year": row["year"],
            "Net displaced workers": row["net_displaced_workers"],
            "Automation revenue": row["automation_revenue_captured"],
            "Payment cost": row["total_payment_cost"],
            "Coverage": fmt_rate(row["funding_coverage_ratio"]),
            "Residual payment gap": row["residual_payment_gap"],
            "Combined gap": row["combined_gap"],
            "Cliff risk": row["cliff_risk_band"],
        }
        for row in funding["years"]
    ],
    width="stretch",
)

st.markdown("### Sensitivity Summary")
if sensitivity.get("points"):
    st.dataframe(
        [
            {
                "Parameter": point["parameter_name"],
                "Value": point["parameter_value"],
                "Program cost": point["total_program_cost"],
                "Coverage": fmt_rate(point["funding_coverage_ratio"]),
                "Residual gap": point["residual_funding_gap"],
                "Affordability band": point["affordability_band"],
            }
            for point in sensitivity["points"]
        ],
        width="stretch",
    )
else:
    st.write("No sensitivity grid configured for this example.")

st.markdown("### Plain-English Meaning")
st.write(selected.get("interpretation", ""))
st.write("Firm-level CARSF liability is not automatically modified by this transition-funding preview.")

st.markdown("### Limitations and Non-Claims")
for item in report.get("metadata", {}).get("non_claims", [WARNING]):
    st.markdown(f"- {item}")
