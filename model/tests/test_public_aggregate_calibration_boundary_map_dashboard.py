from __future__ import annotations

import runpy


def test_public_data_evidence_page_reads_calibration_boundary_report(repo_root) -> None:
    page = repo_root / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py"
    text = page.read_text(encoding="utf-8")

    assert "reports\" / \"public_aggregate_calibration_boundary_map.json" in text
    assert "Public Aggregate Calibration Boundary Map" in text
    assert "scripts/run_public_aggregate_calibration_boundary_map.py" in text
    assert "tax payable" in text
    assert "firm-level CARSF liability" in text


def test_public_data_evidence_page_imports_cleanly(repo_root) -> None:
    runpy.run_path(str(repo_root / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py"), run_name="__main__")


def test_main_streamlit_app_imports_cleanly(repo_root) -> None:
    runpy.run_path(str(repo_root / "simulator" / "app.py"), run_name="__main__")
