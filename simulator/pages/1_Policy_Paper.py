from __future__ import annotations

from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]


st.set_page_config(page_title="CARSF Policy Paper", layout="wide")
st.title("Policy Paper")
st.caption("Working Markdown paper. Not legislation or official advice.")

paper = REPO_ROOT / "paper" / "CARSF_V1_5_WORKING.md"
st.markdown(paper.read_text(encoding="utf-8"))
