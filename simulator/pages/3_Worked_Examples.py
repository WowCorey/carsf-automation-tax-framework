from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "model"))

from carsf.example_runner import ExampleResult, run_all_examples  # noqa: E402


def fmt(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:,.2f}"


@st.cache_data
def load_results() -> list[ExampleResult]:
    return run_all_examples(REPO_ROOT)


st.set_page_config(page_title="CARSF Worked Examples", layout="wide")
st.title("Worked Examples")
st.caption("Illustrative placeholder cases only. These are not tax-payable estimates.")

results = load_results()
selected = st.selectbox("Example", [result.name for result in results])
result = next(item for item in results if item.name == selected)

st.subheader(result.business_description)
st.warning("All values are illustrative placeholders. No legal, tax, Treasury, ATO, or economic validation is implied.")
st.info("Safe harbour and avoidance outputs are prototype review flags, not legal findings.")

left, right = st.columns([1, 1])
with left:
    st.markdown("### Key Inputs")
    st.write(
        {
            "schedule": result.schedule,
            "output": result.inputs["output"],
            "worker_count": len(result.inputs["workers"]),
            "automation_components": result.inputs["automation_components"],
            "aava_inputs": result.inputs["aava_inputs"],
            "capital_base": result.inputs["capital_base"],
            "credits": result.inputs["credits"],
        }
    )

with right:
    st.markdown("### Outputs")
    outputs = result.outputs
    st.table(
        [
            {"Metric": "QLC", "Value": fmt(outputs.qlc)},
            {"Metric": "OPFTE_LIBC", "Value": fmt(outputs.opfte_libc)},
            {"Metric": "HLE", "Value": fmt(outputs.hle)},
            {"Metric": "AII", "Value": fmt(outputs.aii)},
            {"Metric": "NLTG", "Value": fmt(outputs.nltg)},
            {"Metric": "AAVA", "Value": fmt(outputs.aava)},
            {"Metric": "AEL raw", "Value": fmt(outputs.ael_raw)},
            {"Metric": "AEL payable", "Value": fmt(outputs.ael_payable)},
            {"Metric": "AEL shortfall", "Value": fmt(outputs.shortfall)},
            {"Metric": "ARL", "Value": fmt(outputs.arl)},
            {"Metric": "Credits", "Value": fmt(outputs.credits)},
            {"Metric": "Final liability (placeholder)", "Value": fmt(outputs.liability)},
            {"Metric": "CARS-I", "Value": fmt(outputs.cars_i)},
            {"Metric": "CoverageRatio", "Value": outputs.coverage_ratio_display},
        ]
    )

st.markdown("### Formula Trace")
for item in result.formula_trace:
    st.markdown(f"- {item}")

st.markdown("### Plain-English Interpretation")
st.write(result.interpretation)

st.markdown("### Safe Harbour Assessment")
safe_harbour = result.safe_harbour_result
st.write(
    {
        "eligible": safe_harbour.eligible,
        "category": safe_harbour.category,
        "review_required": safe_harbour.review_required,
        "reasons": safe_harbour.reasons,
        "warnings": safe_harbour.warnings,
    }
)
st.caption("Safe harbour classification does not reduce or erase liability in this prototype build.")

st.markdown("### Avoidance Risk")
avoidance = result.avoidance_result
st.write(
    {
        "risk_level": avoidance.risk_level,
        "flags": avoidance.flags,
        "reasons": avoidance.reasons,
        "recommended_review": avoidance.recommended_review,
    }
)

st.markdown("### Grouping Risk")
grouping = result.grouping_risk_result
st.write(
    {
        "risk_level": grouping.risk_level,
        "flags": grouping.flags,
        "reasons": grouping.reasons,
        "recommended_review": grouping.recommended_review,
    }
)

st.markdown("### Red-Team Notes")
st.write(result.red_team_notes)

st.markdown("### Warnings and Limitations")
for warning in result.warnings:
    st.markdown(f"- {warning}")
for note in result.limitation_notes:
    st.markdown(f"- {note}")
