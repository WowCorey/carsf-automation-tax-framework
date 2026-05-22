from __future__ import annotations

import runpy


def test_public_data_evidence_page_reads_scenario_constraint_report(repo_root) -> None:
    page = repo_root / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py"
    text = page.read_text(encoding="utf-8")

    assert "reports\" / \"public_aggregate_scenario_constraint_layer.json" in text
    assert "Public Aggregate Scenario Constraint Layer" in text
    assert "scripts/run_public_aggregate_scenario_constraint_layer.py" in text
    assert "outputs_marked_non_interpretable" in text
    assert "outputs_hidden_from_reviewer_dashboard" in text
    assert "tax payable" in text
    assert "firm-level liability" in text


def test_public_data_evidence_page_imports_cleanly(repo_root) -> None:
    runpy.run_path(str(repo_root / "simulator" / "pages" / "29_Public_Data_Evidence_Map.py"), run_name="__main__")


def test_main_streamlit_app_imports_cleanly(repo_root) -> None:
    runpy.run_path(str(repo_root / "simulator" / "app.py"), run_name="__main__")
