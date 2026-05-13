from __future__ import annotations

from pathlib import Path

from carsf.repo_guardrails import scan_repo


PROJECT_ROOT = Path(__file__).resolve().parents[2]
FIXTURES = PROJECT_ROOT / "model" / "tests" / "fixtures" / "repo_guardrails"


def finding_types(result):
    return {finding.finding_type for finding in result.denied_findings}


def test_clean_fixture_passes():
    result = scan_repo(FIXTURES / "clean_repo_fixture")

    assert result.clean is True
    assert result.denied_findings == []


def test_prohibited_path_fails():
    result = scan_repo(FIXTURES / "bad_prohibited_path_fixture")

    assert result.clean is False
    assert "prohibited_path" in finding_types(result)


def test_prohibited_extension_fails():
    result = scan_repo(FIXTURES / "bad_secret_extension_fixture")

    assert result.clean is False
    assert "prohibited_extension" in finding_types(result)


def test_secret_marker_fails_outside_allowlisted_mock_path():
    result = scan_repo(FIXTURES / "bad_secret_marker_fixture")

    assert result.clean is False
    assert "sensitive_marker" in finding_types(result)


def test_sensitive_marker_in_non_guardrail_model_file_fails():
    result = scan_repo(FIXTURES / "bad_model_file_marker_fixture")

    assert result.clean is False
    assert "sensitive_marker" in finding_types(result)


def test_fake_marker_passes_inside_allowed_synthetic_mock_fixture():
    result = scan_repo(FIXTURES / "allowed_mock_fixture")

    assert result.clean is True
    assert any(finding.finding_type == "allowlisted_synthetic_marker" for finding in result.warning_findings)


def test_mock_fixture_without_synthetic_flag_fails():
    result = scan_repo(FIXTURES / "bad_mock_missing_synthetic_fixture")

    assert result.clean is False
    assert "mock_missing_synthetic_flag" in finding_types(result)


def test_generated_report_missing_non_claim_fails():
    result = scan_repo(FIXTURES / "bad_report_missing_non_claim_fixture")

    assert result.clean is False
    assert "missing_report_non_claim" in finding_types(result)


def test_generated_report_containing_raw_evidence_payload_fails():
    result = scan_repo(FIXTURES / "bad_raw_evidence_report_fixture")

    assert result.clean is False
    assert "raw_evidence_payload" in finding_types(result)


def test_repo_scan_result_is_deterministic():
    first = scan_repo(FIXTURES / "allowed_mock_fixture").to_jsonable()
    second = scan_repo(FIXTURES / "allowed_mock_fixture").to_jsonable()

    assert first == second


def test_actual_current_repo_passes_guardrails():
    result = scan_repo(PROJECT_ROOT)

    assert result.clean is True
    assert result.denied_findings == []
