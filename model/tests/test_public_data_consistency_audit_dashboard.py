from __future__ import annotations

import runpy


def test_public_data_evidence_map_dashboard_reads_evidence_and_audit_reports(repo_root) -> None:
    page = repo_root / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py"
    text = page.read_text(encoding="utf-8")
    assert "public_data_evidence_map.json" in text
    assert "public_data_consistency_audit.json" in text
    assert "Consistency Audit / Source Reconciliation" in text
    assert "requests" not in text
    assert "urllib" not in text


def test_public_data_evidence_map_dashboard_avoids_score_widgets(repo_root) -> None:
    page = repo_root / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py"
    lowered = page.read_text(encoding="utf-8").lower()
    assert "st.metric(\"readiness" not in lowered
    assert "st.metric(\"calibration" not in lowered
    assert "st.metric(\"validation" not in lowered
    assert "readiness_score" not in lowered
    assert "calibration_score" not in lowered
    assert "validation_score" not in lowered


def test_public_data_evidence_map_streamlit_page_imports_after_audit_update(repo_root) -> None:
    runpy.run_path(str(repo_root / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py"), run_name="__main__")


def test_main_streamlit_app_imports_after_audit_update(repo_root) -> None:
    runpy.run_path(str(repo_root / "simulator" / "app.py"), run_name="__main__")
