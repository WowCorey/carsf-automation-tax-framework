from __future__ import annotations

import json
import sys
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "model"))

from carsf.calibration import get_calibration_registry, validate_no_fake_calibration_values  # noqa: E402
from carsf.evidence import get_default_evidence_requirements, requirements_by_category  # noqa: E402


def load_report(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


st.set_page_config(page_title="CARSF Evidence and Calibration", layout="wide")
st.title("Evidence and Calibration")
st.caption("Prototype evidence and calibration scaffolding only. No validation or official data is implied.")
st.warning(
    "This page shows prototype evidence requirements, decision-log summaries, and calibration dependencies. "
    "It is not legal, tax, Treasury, ATO, ABS, Fair Work, OECD, BEPS, audit, forensic, or economic validation."
)

requirements = get_default_evidence_requirements()
registry = get_calibration_registry()
evidence_report = load_report(REPO_ROOT / "reports" / "evidence_requirements.json")
calibration_report = load_report(REPO_ROOT / "reports" / "calibration_requirements.json")

st.markdown("### Evidence Requirements Overview")
category_counts = {category: len(items) for category, items in requirements_by_category().items()}
st.write(category_counts)
st.table(
    [
        {
            "Requirement": requirement.requirement_id,
            "Category": requirement.category,
            "Field": requirement.field,
            "Minimum Confidence": requirement.minimum_confidence,
            "Required For": ", ".join(requirement.required_for),
        }
        for requirement in requirements[:20]
    ]
)

st.markdown("### Evidence Status Summary")
if evidence_report:
    st.table(evidence_report.get("example_evidence_summary", []))
    st.write(
        {
            "grouped": evidence_report.get("grouped_evidence_summary", {}),
            "transfer_pricing": evidence_report.get("transfer_pricing_evidence_summary", {}),
        }
    )
else:
    st.info("Run `python scripts/run_examples.py` to generate evidence report summaries.")

st.markdown("### Decision-Log Explanation")
st.write(
    "Decision logs record compact step summaries for evidence assessment, formula flow, review flags, "
    "transfer-pricing previews, and mixed-unit handling. They do not store raw records or create legal findings."
)

st.markdown("### Calibration Requirements")
st.write(
    {
        "version": registry.version,
        "requirement_count": len(registry.requirements),
        "no_fake_calibration_values": validate_no_fake_calibration_values(registry),
    }
)
st.table(
    [
        {
            "Component": requirement.model_component,
            "Preferred Source": requirement.preferred_source,
            "Fallback Source": requirement.fallback_source,
            "Status": requirement.calibration_status,
        }
        for requirement in registry.requirements
    ]
)

st.markdown("### Missing Datasets")
if calibration_report:
    unresolved = calibration_report.get("registry", {}).get("unresolved_dependencies", [])
else:
    unresolved = registry.unresolved_dependencies
for dependency in unresolved:
    st.markdown(f"- {dependency}")

st.markdown("### Placeholder-Only Warning")
for non_claim in registry.non_claims:
    st.markdown(f"- {non_claim}")
