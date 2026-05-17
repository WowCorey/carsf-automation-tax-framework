from __future__ import annotations

import json
import subprocess
import sys


REQUIRED_WARNING = (
    "The sector stress matrix is prototype metadata review only. It is not calibrated. "
    "It is not a real-world ranking of sectors. It is not Treasury modelling. It is not ATO guidance. "
    "It is not ABS/ATO/DSS/PBO analysis. It does not use real industry data. "
    "It does not estimate actual tax payable."
)
FORBIDDEN_RANKING_PHRASES = [
    "highest risk sector",
    "lowest risk sector",
    "safest sector",
    "most dangerous sector",
    "best sector",
    "worst sector",
    "real sector ranking",
    "official ranking",
    "treasury ranking",
    "ato ranking",
    "validated sector risk",
    "actual tax payable can be estimated",
    "economic validation is complete",
]


def test_sector_stress_matrix_report_generates(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-sector-stress-matrix"
    completed = subprocess.run(
        [sys.executable, "scripts/run_sector_stress_matrix.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "sector_stress_matrix.md").exists()
    assert (reports_dir / "sector_stress_matrix.json").exists()


def test_sector_stress_matrix_report_includes_non_claim_language(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-sector-stress-matrix-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_sector_stress_matrix.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "sector_stress_matrix.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "sector_stress_matrix.json").read_text(encoding="utf-8"))

    assert REQUIRED_WARNING in markdown
    assert REQUIRED_WARNING in payload["metadata"]["non_claims"]
    assert "Scores are deterministic placeholders derived only from schedule metadata" in markdown
    assert payload["metadata"]["firm_level_liability_logic_modified"] is False
    assert payload["metadata"]["real_industry_data_added"] is False


def test_sector_stress_matrix_report_contains_required_matrix_fields(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-sector-stress-matrix-fields"
    subprocess.run(
        [sys.executable, "scripts/run_sector_stress_matrix.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    payload = json.loads((reports_dir / "sector_stress_matrix.json").read_text(encoding="utf-8"))
    markdown = (reports_dir / "sector_stress_matrix.md").read_text(encoding="utf-8")

    assert "Schedule ID | Schedule Name | Canonical Output Unit | Automation Intensity" in markdown
    assert len(payload["stress_matrix"]) == 6
    for row in payload["stress_matrix"]:
        assert row["do_not_rank"] is True
        assert row["display_control_status"]
        assert row["automation_intensity_placeholder"]
        assert row["calibration_difficulty_placeholder"]
        assert row["legal_attribution_difficulty_placeholder"]


def test_sector_stress_matrix_report_has_no_forbidden_ranking_phrases(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-sector-stress-matrix-ranking-phrases"
    subprocess.run(
        [sys.executable, "scripts/run_sector_stress_matrix.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in reports_dir.glob("sector_stress_matrix.*"))

    for phrase in FORBIDDEN_RANKING_PHRASES:
        assert phrase not in combined


def test_sector_stress_matrix_report_does_not_claim_validation_or_tax_use(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-sector-stress-matrix-claims"
    subprocess.run(
        [sys.executable, "scripts/run_sector_stress_matrix.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in reports_dir.glob("sector_stress_matrix.*"))
    forbidden_claims = [
        "treasury validation",
        "ato validation",
        "abs validation",
        "pbo validation",
        "official sector scores",
        "calibrated opfte values",
        "real industry data has been added",
        "firm-level carsf liability logic is modified",
    ]

    for claim in forbidden_claims:
        assert claim not in combined


def test_streamlit_sector_stress_matrix_page_imports_without_error(repo_root) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('simulator/pages/21_Sector_Stress_Matrix.py', run_name='__main__')",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr


def test_ci_runs_sector_stress_matrix_after_schedule_expansion(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    schedule_index = workflow.index("python scripts/run_sector_schedule_expansion.py")
    stress_index = workflow.index("python scripts/run_sector_stress_matrix.py")
    guardrail_index = workflow.index("python scripts/run_repo_guardrails.py")

    assert schedule_index < stress_index < guardrail_index


def test_sector_stress_matrix_report_deterministic_summary(repo_root) -> None:
    first_dir = repo_root / "tmp" / "test-sector-stress-matrix-deterministic-1"
    second_dir = repo_root / "tmp" / "test-sector-stress-matrix-deterministic-2"
    subprocess.run(
        [sys.executable, "scripts/run_sector_stress_matrix.py", "--reports-dir", str(first_dir)],
        cwd=repo_root,
        check=True,
    )
    subprocess.run(
        [sys.executable, "scripts/run_sector_stress_matrix.py", "--reports-dir", str(second_dir)],
        cwd=repo_root,
        check=True,
    )

    first = json.loads((first_dir / "sector_stress_matrix.json").read_text(encoding="utf-8"))
    second = json.loads((second_dir / "sector_stress_matrix.json").read_text(encoding="utf-8"))

    assert first["summary"] == second["summary"]
    assert [row["schedule_id"] for row in first["stress_matrix"]] == [
        row["schedule_id"] for row in second["stress_matrix"]
    ]
