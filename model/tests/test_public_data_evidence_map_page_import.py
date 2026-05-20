from __future__ import annotations

import runpy


def test_public_data_evidence_map_streamlit_page_imports_cleanly(repo_root) -> None:
    runpy.run_path(str(repo_root / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py"), run_name="__main__")


def test_main_streamlit_app_imports_cleanly_after_evidence_map(repo_root) -> None:
    runpy.run_path(str(repo_root / "simulator" / "app.py"), run_name="__main__")
