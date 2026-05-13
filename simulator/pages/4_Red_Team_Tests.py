from __future__ import annotations

from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]


st.set_page_config(page_title="CARSF Red-Team Tests", layout="wide")
st.title("Red-Team Tests")
st.caption("Known gaming attempts and current prototype controls.")

register = REPO_ROOT / "audits" / "red_team_register.md"
st.markdown(register.read_text(encoding="utf-8"))
