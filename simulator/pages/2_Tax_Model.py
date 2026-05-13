from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "model"))

from carsf import (  # noqa: E402
    AIIWeights,
    LevyParameters,
    QLCWeights,
    Worker,
    automation_intensity_index,
    australian_automated_value_added,
    calculate_liability,
    coverage_measures,
    format_coverage_ratio,
    human_labour_equivalent,
    net_labour_tax_gap,
    qualified_labour_contribution_firm,
)


st.set_page_config(page_title="CARSF Tax Model", layout="wide")
st.title("Tax Model")
st.caption("Concept-level calculator using placeholder inputs.")

with st.sidebar:
    st.header("Schedule Parameters")
    full_time_hours = st.number_input("Full-time hours", min_value=1.0, value=1820.0)
    qlc_max_multiplier = st.number_input("QLC max multiplier", min_value=1.0, value=1.25)
    frv = st.number_input("FRV standard", min_value=0.0, value=45000.0)
    lambda_sector = st.number_input("lambda_sector", min_value=0.0, max_value=1.0, value=0.18)
    lambda_combined = st.number_input("LAMBDA_sector", min_value=0.0, max_value=1.0, value=0.25)
    theta = st.number_input("theta", min_value=0.0, max_value=1.0, value=0.60)
    uplift_rate = st.number_input("Uplift rate", min_value=0.0, value=1.12)
    rent_tax_rate = st.number_input("Rent tax rate", min_value=0.0, max_value=1.0, value=0.20)

left, right = st.columns(2)

with left:
    st.subheader("Output and Labour")
    output = st.number_input("Output", min_value=0.0, value=4800.0)
    opfte = st.number_input("OPFTE benchmark", min_value=0.0001, value=900.0)
    worker_count = st.number_input("Worker count", min_value=0, max_value=500, value=4)
    annual_hours = st.number_input("Annual hours per worker", min_value=0.0, value=1820.0)
    wage_quality = st.slider("Wage quality", 0.0, 1.0, 0.65)
    job_security = st.slider("Job security", 0.0, 1.0, 0.75)
    skill_development = st.slider("Skill development", 0.0, 1.0, 0.60)
    australian_nexus = st.slider("Australian nexus", 0.0, 1.0, 1.0)

with right:
    st.subheader("Automation and Value")
    compute_ratio = st.slider("Compute ratio", 0.0, 1.0, 0.12)
    auto_decision_ratio = st.slider("Automated decision ratio", 0.0, 1.0, 0.18)
    robotics_capital_ratio = st.slider("Robotics capital ratio", 0.0, 1.0, 0.02)
    auto_process_share = st.slider("Automated process share", 0.0, 1.0, 0.16)
    revenue = st.number_input("Australian attributable revenue", min_value=0.0, value=940000.0)
    non_auto_costs = st.number_input("Verified non-automation input costs", min_value=0.0, value=440000.0)
    qlc_wage_cost = st.number_input("Verified QLC wage cost", min_value=0.0, value=330000.0)
    capital_base = st.number_input("Capital base", min_value=0.0, value=220000.0)
    verified_credits = st.number_input("Verified credits", min_value=0.0, value=22000.0)
    national_damage = st.number_input(
        "National automation fiscal damage",
        min_value=0.0,
        value=0.0,
        help="Prototype national-monitoring input. Placeholder only.",
    )
    revenue_captured = st.number_input(
        "Automation revenue captured",
        min_value=0.0,
        value=0.0,
        help="Prototype national-monitoring input. Placeholder only.",
    )

weights = QLCWeights(qlc_max_multiplier=qlc_max_multiplier)
workers = [
    Worker(
        annual_hours=annual_hours,
        full_time_hours=full_time_hours,
        wage_quality=wage_quality,
        job_security=job_security,
        skill_development=skill_development,
        australian_nexus=australian_nexus,
    )
    for _ in range(worker_count)
]
qlc = qualified_labour_contribution_firm(workers, weights)
hle = human_labour_equivalent(output, opfte)
aii = automation_intensity_index(
    compute_ratio,
    auto_decision_ratio,
    robotics_capital_ratio,
    auto_process_share,
    AIIWeights(),
)
nltg = net_labour_tax_gap(hle, aii, qlc)
aava = australian_automated_value_added(revenue, non_auto_costs, qlc_wage_cost)
result = calculate_liability(
    nltg=nltg,
    aava=aava,
    capital_base=capital_base,
    verified_credits=verified_credits,
    params=LevyParameters(
        frv_standard=frv,
        lambda_sector=lambda_sector,
        lambda_combined=lambda_combined,
        theta=theta,
        uplift_rate=uplift_rate,
        rent_tax_rate=rent_tax_rate,
    ),
)
coverage = coverage_measures(national_damage, revenue_captured)

st.subheader("Outputs")
metrics = {
    "QLC": qlc,
    "HLE": hle,
    "AII": aii,
    "NLTG": nltg,
    "AAVA": aava,
    "AEL raw": result.ael_raw,
    "AEL payable": result.ael_payable,
    "ARL": result.arl,
    "Credits": result.credits,
    "Final liability": result.liability,
    "Shortfall": result.shortfall,
    "CARS-I": coverage.cars_i,
}
cols = st.columns(4)
for index, (label, value) in enumerate(metrics.items()):
    cols[index % 4].metric(label, f"{value:,.2f}")

cols[len(metrics) % 4].metric("CoverageRatio", format_coverage_ratio(coverage.coverage_ratio))
if coverage.notes:
    st.caption(" ".join(coverage.notes))
