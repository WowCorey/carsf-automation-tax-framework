from __future__ import annotations

import runpy


def test_public_data_evidence_map_dashboard_reads_public_real_loader(repo_root) -> None:
    page = repo_root / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py"
    text = page.read_text(encoding="utf-8")

    assert "public_real_data_loader.json" in text
    assert "Real Public Aggregate Data Loader" in text
    assert "requests" not in text
    assert "urllib" not in text


def test_public_data_evidence_map_dashboard_has_no_score_widgets_after_public_real_loader(repo_root) -> None:
    page = repo_root / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py"
    lowered = page.read_text(encoding="utf-8").lower()

    assert "st.metric(\"readiness" not in lowered
    assert "st.metric(\"calibration" not in lowered
    assert "st.metric(\"validation" not in lowered
    assert "readiness_score" not in lowered
    assert "calibration_score" not in lowered
    assert "validation_score" not in lowered
    assert "tax payable estimate" not in lowered


def test_public_data_evidence_map_streamlit_page_imports_after_public_real_loader(repo_root) -> None:
    runpy.run_path(str(repo_root / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py"), run_name="__main__")


def test_main_streamlit_app_imports_after_public_real_loader(repo_root) -> None:
    runpy.run_path(str(repo_root / "simulator" / "app.py"), run_name="__main__")
