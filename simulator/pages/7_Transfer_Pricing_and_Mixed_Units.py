from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "model"))

from carsf.transfer_runner import TRANSFER_PRICING_REPORT_WARNING, run_transfer_pricing_previews  # noqa: E402


def fmt(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:,.2f}"


@st.cache_data
def load_preview():
    return run_transfer_pricing_previews(REPO_ROOT)


def scenario_table(scenario):
    adjusted_liability = scenario.liability_preview.adjusted_aava_liability_preview
    return [
        {"Metric": "Reported AAVA", "Value": fmt(scenario.reported_aava)},
        {"Metric": "Preview adjustments total", "Value": fmt(scenario.adjusted_aava_preview.preview_adjustments_total)},
        {"Metric": "Adjusted AAVA preview", "Value": fmt(scenario.adjusted_aava_preview.adjusted_aava_preview)},
        {"Metric": "Original final liability", "Value": fmt(scenario.liability_preview.original_final_liability)},
        {"Metric": "Adjusted-AAVA liability preview", "Value": fmt(adjusted_liability)},
        {"Metric": "Risk level", "Value": scenario.transfer_pricing_result.risk_level},
        {"Metric": "Review required", "Value": str(scenario.transfer_pricing_result.review_required).lower()},
    ]


def candidate_table(scenario):
    return [
        {
            "Transaction": candidate.transaction_id,
            "Type": candidate.transaction_type,
            "Amount": fmt(candidate.amount),
            "Review Share": f"{candidate.review_share:.2f}",
            "Preview Addback": fmt(candidate.preview_addback_amount),
            "Confidence": candidate.confidence,
        }
        for candidate in scenario.transfer_pricing_result.candidates
    ]


st.set_page_config(page_title="CARSF Transfer Pricing and Mixed Units", layout="wide")
st.title("Transfer Pricing and Mixed Units")
st.caption("Prototype review previews only. These are not transfer-pricing adjustments, legal findings, or tax assessments.")
st.warning(TRANSFER_PRICING_REPORT_WARNING)

preview = load_preview()

st.markdown("### Transfer-Pricing Preview Overview")
st.write(
    "The preview identifies related-party automation charges and adjusted-AAVA review candidates without changing "
    "reported AAVA or final liability calculations."
)

st.markdown("### Related-Party AI Fee Structure")
st.write(preview.related_party_ai_fee.source["purpose"])
st.table(scenario_table(preview.related_party_ai_fee))
st.table(candidate_table(preview.related_party_ai_fee))

st.markdown("### Robotics Leasing Structure")
st.write(preview.robotics_leasing.source["purpose"])
st.table(scenario_table(preview.robotics_leasing))
st.table(candidate_table(preview.robotics_leasing))

st.markdown("### Mixed-Unit Compatibility")
compatibility = preview.unit_compatibility
st.write(preview.mixed_unit_group["purpose"])
st.write(
    {
        "compatible": compatibility.compatible,
        "units": compatibility.unit_set,
        "comparable_unit": compatibility.comparable_unit,
        "reason": compatibility.reason,
        "review_required": compatibility.review_required,
    }
)
st.table(
    [
        {
            "Entity": entity["entity_id"],
            "Schedule": entity["schedule_id"],
            "Canonical Output Unit": entity["canonical_output_unit"],
            "Revenue": fmt(entity["revenue"]),
            "AAVA": fmt(entity["aava"]),
            "Standalone Liability": fmt(entity["liability"]),
            "Risk": entity.get("risk_level", "unknown"),
        }
        for entity in preview.mixed_unit_group["entities"]
    ]
)

st.markdown("### Value-Weighted Exposure Index")
exposure = preview.mixed_unit_exposure
st.write(
    {
        "method": exposure.method,
        "standalone_liability_sum": fmt(exposure.standalone_liability_sum),
        "value_weighted_exposure_index": fmt(exposure.value_weighted_exposure_index),
        "review_required": exposure.review_required,
    }
)
st.info("Value-weighted exposure index is prototype-only, not a tax base, and not a replacement for sector schedules.")

st.markdown("### Limitations and Non-Claims")
for warning in exposure.warnings + compatibility.warnings:
    st.markdown(f"- {warning}")
for non_claim in exposure.non_claims + preview.related_party_ai_fee.transfer_pricing_result.non_claims:
    st.markdown(f"- {non_claim}")
