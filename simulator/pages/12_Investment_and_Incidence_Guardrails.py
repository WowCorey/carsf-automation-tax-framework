from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "model"))

from carsf.investment import INVESTMENT_NON_CLAIMS  # noqa: E402


WARNING = (
    "These are prototype investment and tax-incidence guardrails only. They are not economic validation, "
    "investment advice, Treasury modelling, ATO guidance, legal advice, market forecasting, or tax advice."
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


st.set_page_config(page_title="CARSF Investment and Incidence Guardrails", layout="wide")
st.title("Investment and Incidence Guardrails")
st.caption("Non-operative review checks for burden, pass-through, investment risk, and public-revenue capture.")
st.warning(WARNING)

report = load_report(REPO_ROOT / "reports" / "investment_guardrails.json")
if not report:
    st.info("Run `python scripts/run_investment_guardrails.py` to generate investment guardrail reports.")
    st.stop()

examples = report.get("examples", [])
if not examples:
    st.info("No investment guardrail examples found in the generated report.")
    st.stop()

st.markdown("### Overview")
st.write(
    {
        "status": report.get("metadata", {}).get("status"),
        "examples": len(examples),
        "final_liability_modified": any(item.get("final_liability_modified") for item in examples),
    }
)

selected_name = st.selectbox("Stress case", [item["name"] for item in examples])
selected = next(item for item in examples if item["name"] == selected_name)
investment = selected["investment_result"]
incidence = selected["incidence_result"]
burden = selected["burden_balance_result"]

st.markdown("### Effective Burden")
st.table(
    [
        {
            "Metric": "Final liability",
            "Value": fmt_money(selected["investment_inputs"]["final_liability"]),
        },
        {
            "Metric": "AAVA",
            "Value": fmt_money(selected["investment_inputs"]["aava"]),
        },
        {
            "Metric": "Effective burden",
            "Value": fmt_rate(investment["effective_burden_rate"]),
        },
        {
            "Metric": "Liability/revenue",
            "Value": fmt_rate(investment["liability_to_revenue_rate"]),
        },
        {
            "Metric": "Investment risk band",
            "Value": investment["investment_risk_band"],
        },
    ]
)

st.markdown("### Normal Return Preservation Preview")
st.write(
    {
        "normal_return_preserved": investment["normal_return_preserved"],
        "preserved_return_amount": fmt_money(investment["preserved_return_amount"]),
        "over_capture_warning": investment["over_capture_warning"],
        "under_capture_warning": investment["under_capture_warning"],
        "reasons": investment["reasons"],
    }
)

st.markdown("### Incidence Allocation Preview")
st.table(
    [
        {"Channel": "consumer", "Amount": fmt_money(incidence["consumer_pass_through_amount"])},
        {"Channel": "worker", "Amount": fmt_money(incidence["worker_pressure_amount"])},
        {"Channel": "supplier", "Amount": fmt_money(incidence["supplier_pressure_amount"])},
        {"Channel": "capital", "Amount": fmt_money(incidence["capital_absorption_amount"])},
        {"Channel": "allocation gap", "Amount": fmt_money(incidence["allocation_gap"])},
    ]
)
st.write({"incidence_risk_band": incidence["incidence_risk_band"]})

st.markdown("### Under/Over-Capture Warning")
st.write(
    {
        "coverage_ratio": fmt_rate(burden["coverage_ratio"]),
        "capture_gap": fmt_money(burden["capture_gap"]),
        "burden_balance_band": burden["burden_balance_band"],
        "review_required": burden["review_required"],
        "reasons": burden["reasons"],
    }
)

st.markdown("### Sensitivity Sweep Summary")
st.table(
    [
        {
            "Sweep": sweep["sweep_name"],
            "Points": len(sweep["points"]),
            "Min liability": fmt_money(sweep["min_liability"]),
            "Max liability": fmt_money(sweep["max_liability"]),
        }
        for sweep in selected["sensitivity_sweeps"]
    ]
)

st.markdown("### Plain-English Meaning")
st.write(selected.get("interpretation", ""))
st.write("Final liability is not automatically modified by these guardrails.")

st.markdown("### Limitations and Non-Claims")
for item in [WARNING, *INVESTMENT_NON_CLAIMS]:
    st.markdown(f"- {item}")

