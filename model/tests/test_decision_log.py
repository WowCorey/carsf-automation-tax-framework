from __future__ import annotations

from carsf.decision_log import add_decision_entry, build_standard_decision_log, create_decision_log, summarise_decision_log


def test_decision_logs_can_be_created_deterministically_except_generated_at() -> None:
    first = create_decision_log("example_a")
    second = create_decision_log("example_a")

    assert first.run_id == second.run_id
    assert first.example_id == second.example_id
    assert first.generated_at
    assert second.generated_at


def test_decision_log_includes_major_step_entries() -> None:
    log = build_standard_decision_log(
        "example_a",
        "placeholder_only",
        {
            "qlc": 1.0,
            "hle": 2.0,
            "aii": 0.5,
            "nltg": 0.0,
            "aava": 100.0,
            "ael": 0.0,
            "arl": 0.0,
            "caps": 0.0,
            "safe_harbour": "LOW_NLTG_EXCLUSION",
            "avoidance": "low",
            "grouping": "low",
        },
    )
    summary = summarise_decision_log(log)

    assert {
        "evidence_assessment",
        "qlc",
        "hle",
        "aii",
        "nltg",
        "aava",
        "ael",
        "arl",
        "caps",
        "safe_harbour",
        "avoidance",
        "grouping",
    }.issubset(set(summary["steps"]))


def test_decision_logs_include_non_claims() -> None:
    summary = summarise_decision_log(create_decision_log("example_a"))

    assert any("do not create legal findings" in claim for claim in summary["non_claims"])


def test_decision_logs_do_not_include_secret_or_personal_data_markers() -> None:
    log = create_decision_log("example_a")
    add_decision_entry(log, "qlc", "QLC", {}, {"value": 1.0}, "Recorded QLC")
    summary_text = str(summarise_decision_log(log)).lower()

    assert "password" not in summary_text
    assert "api_key" not in summary_text
    assert "personal_data" not in summary_text
    assert "tax_file_number" not in summary_text
