from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st
import yaml


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
    human_labour_equivalent,
    net_labour_tax_gap,
    qualified_labour_contribution_firm,
)


def load_yaml(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def qlc_weights(schedule: dict) -> QLCWeights:
    weights = schedule["qlc"]["weights"]
    return QLCWeights(
        alpha=weights["alpha_wage_quality"],
        beta=weights["beta_job_security"],
        gamma=weights["gamma_skill_development"],
        delta=weights["delta_australian_nexus"],
        qlc_max_multiplier=schedule["qlc"]["qlc_max_multiplier"],
    )


def aii_weights(schedule: dict) -> AIIWeights:
    weights = schedule["aii"]["weights"]
    return AIIWeights(
        compute_ratio=weights["compute_ratio"],
        auto_decision_ratio=weights["auto_decision_ratio"],
        robotics_capital_ratio=weights["robotics_capital_ratio"],
        auto_process_share=weights["auto_process_share"],
    )


def calculate(example: dict, schedule: dict) -> dict:
    workers = [
        Worker(**{key: value for key, value in worker.items() if key != "role"})
        for worker in example["workers"]
    ]
    qlc = qualified_labour_contribution_firm(workers, qlc_weights(schedule))
    hle = human_labour_equivalent(
        example["output"]["value"],
        schedule["opfte_libc_placeholder"]["value"],
    )
    automation = example["automation_components"]
    aii = automation_intensity_index(
        automation["compute_ratio"],
        automation["auto_decision_ratio"],
        automation["robotics_capital_ratio"],
        automation["auto_process_share"],
        aii_weights(schedule),
    )
    nltg = net_labour_tax_gap(hle, aii, qlc)
    aava_inputs = example["aava_inputs"]
    aava = australian_automated_value_added(
        aava_inputs["australian_attributable_revenue"],
        aava_inputs["verified_non_automation_input_costs"],
        aava_inputs["verified_qlc_wage_cost"],
    )
    caps = schedule["caps"]
    levy = calculate_liability(
        nltg=nltg,
        aava=aava,
        capital_base=example["capital_base"],
        verified_credits=example["credits"]["verified_credits"],
        params=LevyParameters(
            frv_standard=schedule["frv"]["standard_placeholder"],
            lambda_sector=caps["lambda_sector"],
            lambda_combined=caps["LAMBDA_sector"],
            theta=caps["theta"],
            uplift_rate=caps["uplift_rate"],
            rent_tax_rate=caps["rent_tax_rate"],
        ),
    )
    return {"qlc": qlc, "hle": hle, "aii": aii, "nltg": nltg, "aava": aava, "levy": levy}


st.set_page_config(page_title="CARSF Worked Examples", layout="wide")
st.title("Worked Examples")
st.caption("Illustrative placeholder cases only.")

examples = sorted(path.stem for path in (REPO_ROOT / "examples").glob("*.yaml"))
selected = st.selectbox("Example", examples)
example = load_yaml(REPO_ROOT / "examples" / f"{selected}.yaml")
schedule = load_yaml(REPO_ROOT / "schedules" / f"{example['schedule_used']}.yaml")
calc = calculate(example, schedule)

st.subheader(example["business_description"])
st.write(example["expected_behaviour"])

cols = st.columns(4)
values = {
    "QLC": calc["qlc"],
    "HLE": calc["hle"],
    "AII": calc["aii"],
    "NLTG": calc["nltg"],
    "AAVA": calc["aava"],
    "AEL payable": calc["levy"].ael_payable,
    "ARL": calc["levy"].arl,
    "Final liability": calc["levy"].liability,
}
for index, (label, value) in enumerate(values.items()):
    cols[index % 4].metric(label, f"{value:,.2f}")

st.subheader("Red-Team Notes")
st.write(example["red_team_notes"])
