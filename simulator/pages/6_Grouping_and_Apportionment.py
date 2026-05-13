from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "model"))

from carsf.group_runner import APPORTIONMENT_SCOPE_NOTE, run_grouped_previews, standalone_max_risk  # noqa: E402


def fmt(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:,.2f}"


@st.cache_data
def load_preview():
    return run_grouped_previews(REPO_ROOT)


st.set_page_config(page_title="CARSF Grouping and Apportionment", layout="wide")
st.title("Grouping and Apportionment")
st.caption("Prototype review previews only. These are not legal grouping findings or tax assessments.")
st.warning(
    "These outputs are prototype review previews only. They are not legal grouping findings, tax assessments, "
    "Treasury guidance, ATO guidance, or economic validation."
)

preview = load_preview()
aggregation = preview.aggregation_result
apportionment = preview.apportionment_result
stress = preview.hybrid_stress_result

st.markdown("### Grouped-Entity Overview")
st.write(
    {
        "group_id": aggregation.group_id,
        "entity_count": aggregation.entity_count,
        "standalone_max_risk": standalone_max_risk(preview.split_entities),
        "group_risk": aggregation.risk_level,
        "review_required": aggregation.review_required,
        "flags": aggregation.flags,
    }
)

st.markdown("### Split Logistics Structure")
st.write(preview.split_structure["purpose"])
st.table(
    [
        {
            "Entity": entity.entity_id,
            "Role": entity.role,
            "Standalone Risk": entity.standalone_risk,
            "Revenue": fmt(entity.revenue),
            "Output": fmt(entity.output_value),
            "QLC": fmt(entity.qlc),
            "HLE": fmt(entity.hle),
            "AII": fmt(entity.aii),
            "NLTG": fmt(entity.nltg),
            "AAVA": fmt(entity.aava),
            "Liability": fmt(entity.liability),
        }
        for entity in preview.split_entities
    ]
)

st.markdown("### Standalone vs Grouped Preview")
st.table(
    [
        {"Metric": "Standalone entity liability sum", "Value": fmt(aggregation.standalone_entity_liability_sum)},
        {"Metric": "Group recomputed liability preview", "Value": fmt(aggregation.group_recomputed_liability_preview)},
        {"Metric": "Aggregate QLC", "Value": fmt(aggregation.aggregate_qlc)},
        {"Metric": "Aggregate HLE", "Value": fmt(aggregation.aggregate_hle)},
        {"Metric": "Weighted AII", "Value": fmt(aggregation.weighted_aii)},
        {"Metric": "Aggregate NLTG preview", "Value": fmt(aggregation.aggregate_nltg_preview)},
        {"Metric": "Aggregate AAVA", "Value": fmt(aggregation.aggregate_aava)},
    ]
)

st.markdown("### Mixed-Activity / Prototype Apportionment Example")
st.write(preview.mixed_apportionment["purpose"])
st.info(APPORTIONMENT_SCOPE_NOTE)
st.write(
    {
        "valid": apportionment.valid,
        "review_required": apportionment.review_required,
        "weighted_parameters": apportionment.weighted_parameters,
        "warnings": apportionment.warnings,
    }
)
st.table(
    [
        {
            "Activity": activity.activity_id,
            "Schedule": activity.schedule_id,
            "Share": f"{activity.share:.2f}",
            "Basis": activity.basis,
        }
        for activity in apportionment.activities
    ]
)

st.markdown("### Hybrid Logistics Stress Variant")
st.write(stress.business_description)
st.table(
    [
        {"Metric": "QLC", "Value": fmt(stress.outputs.qlc)},
        {"Metric": "HLE", "Value": fmt(stress.outputs.hle)},
        {"Metric": "AII", "Value": fmt(stress.outputs.aii)},
        {"Metric": "NLTG", "Value": fmt(stress.outputs.nltg)},
        {"Metric": "AAVA", "Value": fmt(stress.outputs.aava)},
        {"Metric": "Final liability preview", "Value": fmt(stress.outputs.liability)},
    ]
)
st.write(stress.interpretation)

st.markdown("### Warnings and Limitations")
for warning in aggregation.warnings + apportionment.warnings + stress.warnings:
    st.markdown(f"- {warning}")
for basis in aggregation.placeholder_basis + apportionment.placeholder_basis:
    st.markdown(f"- {basis}")
