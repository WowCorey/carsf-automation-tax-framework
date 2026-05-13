from __future__ import annotations

from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]


st.set_page_config(page_title="CARSF Audit Log", layout="wide")
st.title("Audit Log")
st.caption("Limitations and future research requirements.")

for rel in [
    "docs/limitations.md",
    "docs/data_requirements.md",
    "docs/known_risks.md",
    "audits/chatgpt_v14_review.md",
]:
    st.markdown((REPO_ROOT / rel).read_text(encoding="utf-8"))
    st.divider()
