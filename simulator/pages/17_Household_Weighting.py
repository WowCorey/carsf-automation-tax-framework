from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
WARNING = (
    "These are synthetic household weighting outputs only. They are not population estimates, real "
    "distributional modelling, ABS/HILDA/Census analysis, DSS/Services Australia modelling, Treasury "
    "modelling, PBO costing, welfare advice, eligibility law, legal advice, tax advice, or economic validation."
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


st.set_page_config(page_title="CARSF Household Weighting", layout="wide")
st.title("Household Weighting")
st.caption("Synthetic household weights, subgroup aggregation, and calibration-readiness warnings.")
st.warning(WARNING)

report = load_report(REPO_ROOT / "reports" / "household_weighting.json")
if not report:
    st.info("Run `python scripts/run_household_weighting.py` to generate household weighting reports.")
    st.stop()
    raise SystemExit(0)

examples = report.get("examples", [])
if not examples:
    st.info("No household weighting examples found in the generated report.")
    st.stop()
    raise SystemExit(0)

selected_name = st.selectbox("Household weighting example", [item["name"] for item in examples])
selected = next((item for item in examples if item["name"] == selected_name), examples[0])
aggregation = selected["aggregation_result"]

st.markdown("### Overview")
st.write(
    {
        "example_id": selected["example_id"],
        "status": selected["status"],
        "total_synthetic_weight": aggregation["total_synthetic_weight"],
        "representative_of_real_population": aggregation["representative_of_real_population"],
        "firm_level_liability_modified": selected["firm_level_liability_modified"],
    }
)

st.markdown("### Synthetic Weight Table")
st.table(
    [
        {
            "Scenario": weight["scenario_id"],
            "Subgroup": weight["subgroup_id"],
            "Weight": f"{float(weight['weight_value']):.4f}",
            "Calibrated": str(weight["calibrated"]).lower(),
            "Usable for Real-World Claims": str(weight["usable_for_real_world_claims"]).lower(),
        }
        for weight in selected.get("weight_results", [])
    ]
)

st.markdown("### Subgroup Aggregation")
st.table(
    [
        {
            "Subgroup": subgroup["subgroup_name"],
            "Scenarios": str(subgroup["scenario_count"]),
            "Synthetic Weight": f"{float(subgroup['total_synthetic_weight']):.4f}",
            "Weighted Avg Residual Gap": fmt_money(subgroup["weighted_average_residual_gap"]),
            "High/Critical Share": fmt_rate(subgroup["weighted_high_or_critical_share"]),
            "Highest-Risk Scenarios": ", ".join(subgroup.get("highest_risk_scenarios", [])) or "None",
        }
        for subgroup in aggregation.get("subgroup_results", [])
    ]
)

st.markdown("### Weighted Summary")
st.table(
    [
        {"Metric": "Aggregation basis", "Value": aggregation.get("aggregation_basis", "synthetic_weight_record_aggregate_not_unique_population_weight")},
        {"Metric": "Duplicate scenario weight records", "Value": ", ".join(aggregation.get("duplicate_scenario_weight_records", [])) or "None"},
        {"Metric": "Overall synthetic weight-record average residual gap", "Value": fmt_money(aggregation["overall_weighted_average_residual_gap"])},
        {"Metric": "Overall synthetic weight-record high/critical share", "Value": fmt_rate(aggregation["overall_weighted_high_or_critical_share"])},
        {"Metric": "Highest-risk synthetic subgroups", "Value": ", ".join(aggregation.get("highest_risk_subgroups", [])) or "None"},
        {"Metric": "Representative of real population", "Value": str(aggregation["representative_of_real_population"]).lower()},
        {"Metric": "Calibration status", "Value": aggregation["calibration_status"]},
    ]
)
st.caption(
    "Overall metrics aggregate synthetic weight records. If the same scenario appears in multiple subgroup weights, "
    "it may contribute more than once. These outputs are stress-test summaries, not unique-household or "
    "population-weighted estimates."
)

st.markdown("### Calibration Readiness")
calibration = report.get("calibration_shell", {})
st.write(
    {
        "requirement_count": calibration.get("requirement_count"),
        "unmet_requirement_count": calibration.get("unmet_requirement_count"),
        "ready_for_real_distributional_claims": calibration.get("ready_for_real_distributional_claims"),
    }
)
st.table(
    [
        {
            "Requirement": item["requirement_id"],
            "Category": item["category"],
            "Status": item["status"],
            "Real Data In Repo Allowed": str(item["real_data_in_repo_allowed"]).lower(),
        }
        for item in calibration.get("requirements", [])
    ]
)

st.markdown("### Representativeness Warnings")
for warning in aggregation.get("warnings", []):
    st.markdown(f"- {warning}")

st.markdown("### Plain-English Meaning")
st.write(selected.get("interpretation", ""))
st.write("Firm-level CARSF liability is not automatically modified by this household weighting shell.")

st.markdown("### Limitations and Non-Claims")
for item in report.get("metadata", {}).get("non_claims", [WARNING]):
    st.markdown(f"- {item}")
