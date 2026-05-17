from __future__ import annotations

import json
import subprocess
import sys


REQUIRED_WARNING = (
    "Sector schedules are prototype placeholders only. They are not calibrated. They are not legal schedules. "
    "They are not Treasury schedules. They are not ATO guidance. They are not ABS/ATO/DSS/PBO analysis. "
    "They do not contain real industry data. They must not be used to estimate actual tax payable."
)


def test_sector_schedule_expansion_report_generates(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-sector-schedule-expansion"
    completed = subprocess.run(
        [sys.executable, "scripts/run_sector_schedule_expansion.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
    assert (reports_dir / "sector_schedule_expansion.md").exists()
    assert (reports_dir / "sector_schedule_expansion.json").exists()


def test_sector_schedule_expansion_report_includes_non_claim_language(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-sector-schedule-expansion-nonclaims"
    subprocess.run(
        [sys.executable, "scripts/run_sector_schedule_expansion.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    markdown = (reports_dir / "sector_schedule_expansion.md").read_text(encoding="utf-8")
    payload = json.loads((reports_dir / "sector_schedule_expansion.json").read_text(encoding="utf-8"))

    assert REQUIRED_WARNING in markdown
    assert REQUIRED_WARNING in payload["metadata"]["non_claims"]
    assert payload["metadata"]["firm_level_liability_logic_modified"] is False
    assert payload["metadata"]["real_industry_data_added"] is False


def test_sector_schedule_expansion_report_contains_new_schedules(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-sector-schedule-expansion-coverage"
    subprocess.run(
        [sys.executable, "scripts/run_sector_schedule_expansion.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    payload = json.loads((reports_dir / "sector_schedule_expansion.json").read_text(encoding="utf-8"))
    ids = {item["schedule_id"] for item in payload["schedules"]}

    assert {
        "call_centres_customer_support",
        "accounting_administration",
        "retail_self_checkout_fulfilment",
        "software_digital_platforms",
    } <= ids
    assert payload["summary"]["new_schedule_count"] == 4
    assert payload["summary"]["all_aii_weights_valid"] is True


def test_sector_schedule_expansion_report_does_not_claim_calibration_or_real_tax_use(repo_root) -> None:
    reports_dir = repo_root / "tmp" / "test-sector-schedule-expansion-claims"
    subprocess.run(
        [sys.executable, "scripts/run_sector_schedule_expansion.py", "--reports-dir", str(reports_dir)],
        cwd=repo_root,
        check=True,
    )
    combined = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in reports_dir.glob("sector_schedule_expansion.*")
    )
    forbidden_claims = [
        "schedule is calibrated",
        "official sector benchmark",
        "treasury schedule is implemented",
        "ato guidance is implemented",
        "actual tax payable can be estimated",
        "real industry data has been added",
        "firm-level carsf liability logic is modified",
    ]

    for claim in forbidden_claims:
        assert claim not in combined


def test_ci_runs_sector_schedule_expansion_runner(repo_root) -> None:
    workflow = (repo_root / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    examples_index = workflow.index("python scripts/run_examples.py")
    sector_index = workflow.index("python scripts/run_sector_schedule_expansion.py")
    guardrail_index = workflow.index("python scripts/run_repo_guardrails.py")

    assert examples_index < sector_index < guardrail_index


def test_streamlit_sector_schedules_page_imports_without_error(repo_root) -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-c",
            "import runpy; runpy.run_path('simulator/pages/20_Sector_Schedules.py', run_name='__main__')",
        ],
        cwd=repo_root,
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0, completed.stderr
