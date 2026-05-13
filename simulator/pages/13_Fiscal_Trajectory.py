from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
WARNING = (
    "These are prototype fiscal trajectory outputs only. They are not forecasts, Treasury modelling, "
    "ATO estimates, ABS analysis, DSS estimates, PBO costing, legal advice, tax advice, or economic validation."
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


def cumulative(trajectory: dict, field: str, year_field: str) -> float:
    if field in trajectory:
        return float(trajectory[field])
    return sum(float(row.get(year_field, 0.0)) for row in trajectory.get("years", []))


st.set_page_config(page_title="CARSF Fiscal Trajectory", layout="wide")
st.title("National Fiscal Trajectory")
st.caption("National-level placeholder trajectory for PAYG erosion, transfer pressure, captured automation revenue, and residual fiscal gaps.")
st.warning(WARNING)

report = load_report(REPO_ROOT / "reports" / "fiscal_trajectory.json")
if not report:
    st.info("Run `python scripts/run_fiscal_trajectory.py` to generate fiscal trajectory reports.")
    st.stop()
    raise SystemExit(0)

examples = report.get("examples", [])
if not examples:
    st.info("No fiscal trajectory examples found in the generated report.")
    st.stop()
    raise SystemExit(0)

selected_name = st.selectbox("Fiscal example", [item["name"] for item in examples])
selected = next((item for item in examples if item["name"] == selected_name), examples[0])
trajectory = selected["trajectory_result"]
sensitivity = selected["sensitivity_result"]

st.markdown("### Overview")
st.write(
    {
        "trajectory_id": selected["trajectory_id"],
        "status": selected["status"],
        "firm_level_liability_modified": selected["firm_level_liability_modified"],
        "years": f"{trajectory['start_year']}-{trajectory['end_year']}",
    }
)

st.markdown("### Cumulative Summary")
st.table(
    [
        {"Metric": "PAYG loss", "Value": fmt_money(trajectory["cumulative_payg_loss"])},
        {
            "Metric": "HELP/HECS repayment loss",
            "Value": fmt_money(cumulative(trajectory, "cumulative_help_repayment_loss", "help_repayment_loss")),
        },
        {
            "Metric": "Retirement-system contribution pressure",
            "Value": fmt_money(
                cumulative(
                    trajectory,
                    "cumulative_retirement_contribution_pressure",
                    "retirement_contribution_pressure",
                )
            ),
        },
        {"Metric": "Transfer pressure", "Value": fmt_money(trajectory["cumulative_transfer_pressure"])},
        {"Metric": "Automation revenue captured", "Value": fmt_money(trajectory["cumulative_automation_revenue_captured"])},
        {"Metric": "Commonwealth gap after CARSF", "Value": fmt_money(trajectory["cumulative_commonwealth_gap_after_carsf"])},
        {
            "Metric": "State revenue pressure",
            "Value": fmt_money(cumulative(trajectory, "cumulative_state_revenue_pressure", "state_payroll_tax_loss")),
        },
        {"Metric": "Total public-sector gap", "Value": fmt_money(trajectory["cumulative_total_public_sector_gap"])},
        {
            "Metric": "Broader labour-linked pressure",
            "Value": fmt_money(
                cumulative(
                    trajectory,
                    "cumulative_broader_labour_linked_pressure",
                    "broader_labour_linked_pressure",
                )
            ),
        },
        {"Metric": "First high warning year", "Value": str(trajectory["first_high_warning_year"] or "N/A")},
        {"Metric": "First critical warning year", "Value": str(trajectory["first_critical_warning_year"] or "N/A")},
    ]
)
st.write("Superannuation contribution loss is tracked as retirement-system contribution pressure, not ordinary Commonwealth revenue loss.")

st.markdown("### Year-by-Year Trajectory")
st.dataframe(
    [
        {
            "Year": row["year"],
            "Net displaced workers": row["net_displaced_workers"],
            "PAYG loss": row["payg_revenue_loss"],
            "HELP/HECS loss": row["help_repayment_loss"],
            "Retirement contribution pressure": row.get("retirement_contribution_pressure", row.get("super_contribution_loss", 0.0)),
            "Transfer pressure": row["transfer_pressure"],
            "Automation revenue captured": row["automation_revenue_captured"],
            "Coverage ratio": fmt_rate(row["coverage_ratio"]),
            "Commonwealth gap": row["commonwealth_gap_after_carsf"],
            "State pressure": row["state_payroll_tax_loss"],
            "Total public-sector gap": row["total_public_sector_gap"],
            "Broader pressure": row.get("broader_labour_linked_pressure", row["total_public_sector_gap"] + row.get("super_contribution_loss", 0.0)),
            "Warning band": row["warning_band"],
        }
        for row in trajectory["years"]
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
                "Cumulative gap": point["cumulative_gap"],
                "First high": str(point["first_high_warning_year"] or "N/A"),
                "First critical": str(point["first_critical_warning_year"] or "N/A"),
            }
            for point in sensitivity["points"]
        ],
        width="stretch",
    )
else:
    st.write("No sensitivity grid configured for this example.")

st.markdown("### Plain-English Meaning")
st.write(selected.get("interpretation", ""))
st.write("Firm-level CARSF liability is not automatically modified by this national trajectory layer.")

st.markdown("### Limitations and Non-Claims")
for item in report.get("metadata", {}).get("non_claims", [WARNING]):
    st.markdown(f"- {item}")
