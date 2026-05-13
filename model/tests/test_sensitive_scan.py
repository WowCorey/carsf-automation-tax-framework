from __future__ import annotations

from carsf.sensitive_scan import scan_mapping_for_sensitive_markers, scan_text_for_sensitive_markers


def test_sensitive_scanner_finds_forbidden_markers() -> None:
    result = scan_text_for_sensitive_markers("Synthetic FAKE_TFN_MARKER with bank account marker.")

    assert result.clean is False
    assert result.deny_ingestion is True
    assert "TFN" in result.markers_found
    assert "BANK_ACCOUNT" in result.markers_found


def test_sensitive_scanner_is_case_insensitive() -> None:
    result = scan_text_for_sensitive_markers("Synthetic fake MeDiCaRe NuMbEr marker.")

    assert result.clean is False
    assert "MEDICARE_NUMBER" in result.markers_found


def test_mapping_scan_uses_values_not_schema_keys() -> None:
    result = scan_mapping_for_sensitive_markers(
        {
            "contains_secrets": False,
            "source_description": "Synthetic clean mock description.",
        }
    )

    assert result.clean is True
    assert result.markers_found == []
