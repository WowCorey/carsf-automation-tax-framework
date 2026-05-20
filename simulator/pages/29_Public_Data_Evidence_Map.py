from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = REPO_ROOT / "reports" / "public_data_evidence_map.json"
WARNING = (
    "This is a reviewer evidence map and dashboard for the public data pilot only. No new data is loaded by this build. "
    "Build 27 public aggregate extracts remain sanity-check-only or placeholder-anchor-only. This is not calibration, "
    "not validation, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, "
    "not operational readiness, not legal sufficiency, and not official status. It does not determine actual tax payable "
    "or modify firm-level CARSF liability."
)


def load_report(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def rows(items: list[dict], keys: list[str]) -> list[dict]:
    return [{key: item.get(key) for key in keys} for item in items]


def rows_with_lists(items: list[dict], keys: list[str]) -> list[dict]:
    output = []
    for item in items:
        row = {}
        for key in keys:
            value = item.get(key)
            row[key] = ", ".join(value) if isinstance(value, list) else value
        output.append(row)
    return output


st.set_page_config(page_title="CARSF Public Data Evidence Map", layout="wide")
st.title("Public Data Evidence Map")
st.caption("Reviewer-facing map for existing Build 27 public-data pilot artefacts.")
st.warning(WARNING)
st.error("No readiness score, calibration score, validation score, approval, official-status claim, or tax-payable result is created.")

report = load_report(REPORT_PATH)
if not report:
    st.info("Run `python scripts/run_public_data_evidence_map.py` to generate the evidence-map report.")
    st.stop()
    raise SystemExit(0)

metadata = report.get("metadata", {})
payload = report.get("public_data_evidence_map", {})
summary = report.get("summary", {})

st.markdown("### Summary")
st.table(
    [
        {"Metric": key, "Value": str(value)}
        for key, value in summary.items()
        if isinstance(value, (int, bool, str))
    ]
)

st.markdown("### Evidence Status Explanation")
st.table([{"Evidence Status": value} for value in metadata.get("evidence_status_values", [])])

st.markdown("### Confidence Labels")
st.caption("Confidence labels classify evidence type only. They are not validation, readiness, or maturity scores.")
st.table([{"Confidence Label": value} for value in metadata.get("confidence_label_values", [])])

st.markdown("### Source References")
st.table(
    rows_with_lists(
        payload.get("source_evidence", []),
        ["source_reference_id", "publisher", "source_kind", "source_url", "evidence_status", "confidence_label", "linked_extract_ids"],
    )
)

st.markdown("### Loaded Public Extracts")
st.table(
    rows_with_lists(
        payload.get("loaded_extract_evidence", []),
        ["extract_id", "evidence_status", "confidence_label", "values_summary", "source_locator", "value_review_status", "reviewer_interpretation"],
    )
)

st.markdown("### Source-Reference-Only Records")
st.table(
    rows_with_lists(
        payload.get("source_reference_only_evidence", []),
        ["extract_id", "evidence_status", "confidence_label", "source_locator", "value_review_status", "reviewer_interpretation"],
    )
)

st.markdown("### Realistic Placeholder Anchors")
st.table(
    rows_with_lists(
        payload.get("placeholder_evidence", []),
        ["anchor_id", "field_id", "anchored_to_public_data", "anchor_strength", "confidence_label", "blocked_by_restricted_data"],
    )
)

st.markdown("### Field Sanity Checks")
st.table(
    rows_with_lists(
        payload.get("field_sanity_evidence", []),
        ["check_id", "field_id", "check_status", "evidence_status", "confidence_label", "linked_extract_ids", "linked_anchor_ids"],
    )
)

st.markdown("### Module Sanity Checks")
st.table(
    rows_with_lists(
        payload.get("module_sanity_evidence", []),
        ["module_id", "result_status", "sanity_check_possible", "calibration_possible", "evidence_status", "confidence_label", "main_blockers"],
    )
)

st.markdown("### Restricted Blockers")
st.table(
    rows_with_lists(
        payload.get("restricted_blocker_evidence", []),
        ["blocker_id", "description", "evidence_status", "confidence_label", "affected_modules", "required_access_or_review"],
    )
)

st.markdown("### Forbidden Repo Data")
st.table(
    rows(
        payload.get("forbidden_repo_data_evidence", []),
        ["blocker_id", "description", "evidence_status", "confidence_label"],
    )
)

st.markdown("### Reviewer Questions")
st.table(
    rows_with_lists(
        payload.get("reviewer_questions", []),
        ["category", "question", "reviewer_interpretation", "target_evidence_status", "must_not_infer"],
    )
)

st.markdown("### What Cannot Be Claimed")
for item in metadata.get("non_claims", [WARNING]):
    st.markdown(f"- {item}")
