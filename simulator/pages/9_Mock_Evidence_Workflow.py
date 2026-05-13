from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "model"))

from carsf.classification import classify_packet  # noqa: E402
from carsf.evidence import assess_evidence  # noqa: E402
from carsf.evidence_packet import load_evidence_packet, summarise_evidence_packet  # noqa: E402
from carsf.review_workflow import evaluate_review_transition  # noqa: E402


MOCK_WARNING = (
    "These packets are synthetic mock evidence only. They do not validate any real liability, "
    "tax position, audit finding, legal conclusion, Treasury assessment, ATO assessment, or economic claim."
)


def load_report(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def packet_paths() -> list[Path]:
    mock_dir = REPO_ROOT / "data" / "mock_evidence"
    if not mock_dir.exists():
        return []
    return sorted(mock_dir.glob("*.yaml"))


st.set_page_config(page_title="CARSF Mock Evidence Workflow", layout="wide")
st.title("Mock Evidence Workflow")
st.caption("Prototype workflow testing with synthetic mock evidence only.")
st.warning(MOCK_WARNING)

report = load_report(REPO_ROOT / "reports" / "mock_evidence_workflow.json")
paths = packet_paths()

st.markdown("### Packet Overview")
if report:
    st.table(
        [
            {
                "Packet": packet["summary"]["packet_id"],
                "Linked Example": packet["summary"]["linked_example_id"],
                "Evidence Status": packet["evidence_assessment"]["status"],
                "Privacy": packet["summary"]["privacy_classification"],
                "Secrecy": packet["summary"]["secrecy_classification"],
                "Review Flags": ", ".join(packet["summary"]["review_flags"]) or "none",
            }
            for packet in report.get("packets", [])
        ]
    )
else:
    st.info("Run `python scripts/run_evidence_workflow.py` to generate mock evidence workflow reports.")

if not paths:
    st.stop()

selected = st.selectbox("Evidence packet", [path.name for path in paths])
packet = load_evidence_packet(next(path for path in paths if path.name == selected))
summary = summarise_evidence_packet(packet)
classification = classify_packet(packet)
target_state = "partial" if summary.missing_items or summary.low_confidence_items else "sufficient_for_prototype"
if "needs_privacy_review" in summary.review_flags:
    target_state = "needs_privacy_review"
elif "needs_tax_review" in summary.review_flags:
    target_state = "needs_tax_review"
elif "needs_legal_review" in summary.review_flags:
    target_state = "needs_legal_review"
elif "needs_calibration" in summary.review_flags:
    target_state = "needs_calibration"
transition = evaluate_review_transition(summary, target_state)
assessment = assess_evidence(
    {"status": "illustrative_placeholder", "placeholder_notice": "synthetic mock evidence workflow only"},
    packet.created_for,
    evidence_packet=packet,
)

st.markdown("### Packet Summary")
st.write(summary.to_jsonable())

st.markdown("### Review Transition Result")
st.write(transition.to_jsonable())

st.markdown("### Privacy/Secrecy Classification")
st.write(classification)

st.markdown("### Missing Evidence")
missing = assessment.missing_requirements
if missing:
    st.write(missing)
else:
    st.write("No missing requirements for the selected mock scope. This is not real-world sufficiency.")

st.markdown("### Warnings and Non-Claims")
for warning in summary.warnings + transition.warnings + assessment.warnings:
    st.markdown(f"- {warning}")
for non_claim in packet.non_claims:
    st.markdown(f"- {non_claim}")
