from __future__ import annotations

from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[1]


st.set_page_config(page_title="CARSF Simulator", layout="wide")
st.title("CARSF Simulator")
st.caption("Private research prototype. Not legal, tax, Treasury, or ATO advice.")

paper_path = REPO_ROOT / "paper" / "executive_summary.md"
st.markdown(paper_path.read_text(encoding="utf-8"))

st.info(
    "Start with the Executive Dashboard page for a consolidated report index and "
    "non-claim summary, then use the sidebar pages for the policy paper, tax "
    "model, worked examples, red-team tests, and audit log."
)
