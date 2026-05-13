from __future__ import annotations

import json

from carsf.redaction import create_redaction_plan
from carsf.sensitive_scan import scan_text_for_sensitive_markers


def test_redaction_plan_denies_repo_ingestion_when_sensitive_markers_found() -> None:
    scan = scan_text_for_sensitive_markers("Synthetic FAKE_API_KEY_MARKER")
    plan = create_redaction_plan(scan, "synthetic_mock")

    assert plan.required is True
    assert plan.denied_fields
    assert any("repo ingestion must be denied" in warning for warning in plan.warnings)


def test_redaction_plan_does_not_output_raw_sensitive_values() -> None:
    scan = scan_text_for_sensitive_markers("Synthetic FAKE_API_KEY_VALUE_DO_NOT_OUTPUT")
    plan_text = json.dumps(create_redaction_plan(scan, "synthetic_mock").to_jsonable())

    assert "FAKE_API_KEY_VALUE_DO_NOT_OUTPUT" not in plan_text
    assert "API_KEY" in plan_text


def test_clean_synthetic_mock_redaction_plan_not_required() -> None:
    scan = scan_text_for_sensitive_markers("Synthetic clean mock content.")
    plan = create_redaction_plan(scan, "synthetic_mock")

    assert plan.required is False
    assert plan.denied_fields == []
