from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = REPO_ROOT / "reports" / "legislative_architecture.json"
WARNING = (
    "This is a non-operative legislative architecture skeleton only. It is not a Bill, not legal drafting, "
    "not legal advice, not tax advice, not ATO guidance, not Treasury modelling, and not Parliamentary Counsel drafting. "
    "It creates no rights, obligations, powers, notices, penalties, enforcement process, or compliance scoring."
)


def load_report(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def part_rows(parts: list[dict]) -> list[dict]:
    return [
        {
            "Part ID": item.get("part_id"),
            "Part Title": item.get("part_title"),
            "Division Count": len(item.get("divisions", [])),
            "External Review": item.get("external_review_required"),
            "Drafting Risk": item.get("drafting_risk"),
            "Main Reason": item.get("main_reason"),
        }
        for item in parts
    ]


def division_rows(parts: list[dict]) -> list[dict]:
    rows = []
    for part in parts:
        for division in part.get("divisions", []):
            rows.append(
                {
                    "Part ID": part.get("part_id"),
                    "Division ID": division.get("division_id"),
                    "Division Title": division.get("division_title"),
                    "Placeholder Types": ", ".join(division.get("placeholder_provision_types", [])),
                    "Legal Review": division.get("requires_legal_review"),
                    "Tax Review": division.get("requires_tax_review"),
                    "ATO Methods": division.get("requires_ato_methods_review"),
                    "Treasury": division.get("requires_treasury_review"),
                    "Privacy": division.get("requires_privacy_review"),
                    "Calibration": division.get("requires_external_calibration"),
                }
            )
    return rows


def definition_rows(definitions: list[dict]) -> list[dict]:
    return [
        {
            "Term": item.get("term"),
            "Description": item.get("plain_english_description"),
            "Drafting Status": item.get("drafting_status"),
            "Not Operative": item.get("must_not_be_used_as_operative_definition"),
        }
        for item in definitions
    ]


def schedule_rows(schedules: list[dict]) -> list[dict]:
    return [
        {
            "Schedule ID": item.get("schedule_id"),
            "Schedule Name": item.get("schedule_name"),
            "Source YAML": item.get("source_yaml"),
            "Calibration Status": item.get("calibration_status"),
            "Not Official": item.get("must_not_be_treated_as_official_schedule"),
            "Capital-Base Issue": item.get("capital_base_issue"),
        }
        for item in schedules
    ]


def placeholder_rows(items: list[dict]) -> list[dict]:
    rows = []
    for item in items:
        flags = item.get("flags", {})
        rows.append(
            {
                "Placeholder ID": item.get("placeholder_id"),
                "Title": item.get("placeholder_title"),
                "Type": item.get("placeholder_type"),
                "True Flags": ", ".join(sorted(key for key, value in flags.items() if value is True)),
                "Review Requirements": ", ".join(item.get("review_requirements", [])),
            }
        )
    return rows


st.set_page_config(page_title="CARSF Legislative Architecture", layout="wide")
st.title("Legislative Architecture Skeleton")
st.caption("Non-operative architecture map for CARSF prototype review.")
st.warning(WARNING)
st.error("Do not use this page as operative law, legal drafting, ATO guidance, enforcement, notices, penalties, or liability logic.")

report = load_report(REPORT_PATH)
if not report:
    st.info("Run `python scripts/run_legislative_architecture.py` to generate legislative architecture reports.")
    st.stop()
    raise SystemExit(0)

metadata = report.get("metadata", {})
architecture = report.get("legislative_architecture", {})
summary = report.get("summary", {})

st.markdown("### Architecture Summary")
st.table(
    [
        {"Metric": key, "Value": str(value)}
        for key, value in summary.items()
        if isinstance(value, (int, bool, str))
    ]
)

st.markdown("### Required False Flags")
st.table(
    [
        {"Flag": key, "Value": metadata.get(key)}
        for key in [
            "operative_law_created",
            "legal_sufficiency_claimed",
            "statutory_power_created",
            "enforcement_created",
            "firm_level_liability_logic_modified",
        ]
    ]
)

st.markdown("### Proposed Parts")
st.table(part_rows(architecture.get("parts", [])))

st.markdown("### Proposed Divisions")
st.table(division_rows(architecture.get("parts", [])))

st.markdown("### Definition Placeholders")
st.table(definition_rows(architecture.get("definitions", [])))

st.markdown("### Schedule Placeholders")
st.table(schedule_rows(architecture.get("schedules", [])))

st.markdown("### External-Review Blockers")
blockers = architecture.get("external_review_blockers", [])
st.table(
    [
        {
            "Blocker": item.get("blocker_title"),
            "Type": item.get("blocker_type"),
            "Affected Parts": ", ".join(item.get("affected_parts", [])),
            "Reserved": item.get("locked_or_reserved_for_counsel"),
            "Main Reason": item.get("main_reason"),
        }
        for item in blockers
    ]
)

st.markdown("### Locked / Reserved for Counsel Areas")
for area in architecture.get("locked_or_reserved_for_counsel_areas", []):
    st.markdown(f"- {area}")

st.markdown("### Safeguards and Evidence-Power Placeholders")
st.table(placeholder_rows(architecture.get("safeguards", [])))
st.table(placeholder_rows(architecture.get("evidence_power_placeholders", [])))

st.markdown("### Regulation-Making Placeholders")
st.table(placeholder_rows(architecture.get("regulation_making_placeholders", [])))

st.markdown("### Non-Claims")
for item in metadata.get("non_claims", [WARNING]):
    st.markdown(f"- {item}")
