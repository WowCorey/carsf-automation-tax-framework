from __future__ import annotations

import copy
import json

import pytest
import yaml

from carsf.public_real_data_loader import (
    CLAIM_LEVEL_VALUES,
    GUARDRAIL_STATUS_VALUES,
    PUBLIC_REAL_DATA_NON_CLAIMS,
    SOURCE_LOAD_STATUS_VALUES,
    VALUE_REVIEW_STATUS_VALUES,
    build_public_real_data_load_result,
)


def load_manifest(repo_root):
    path = repo_root / "data" / "public_real" / "manifests" / "public_real_data_sources.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def build_result(repo_root):
    return build_public_real_data_load_result(
        load_manifest(repo_root),
        repo_root,
        digest_targets_total=5,
        digests_written=5,
    )


def test_public_real_data_manifest_parses_and_has_required_fields(repo_root) -> None:
    payload = load_manifest(repo_root)

    for field in [
        "manifest_id",
        "manifest_name",
        "status",
        "non_claims",
        "source_load_status_taxonomy",
        "value_review_status_taxonomy",
        "claim_level_taxonomy",
        "guardrail_status_taxonomy",
        "sources",
        "build_31_flags",
        "forbidden_claims",
        "future_build_32_requirements",
    ]:
        assert field in payload

    for non_claim in PUBLIC_REAL_DATA_NON_CLAIMS:
        assert non_claim in payload["non_claims"]


def test_public_real_data_taxonomies_contain_required_values(repo_root) -> None:
    payload = load_manifest(repo_root)

    assert set(payload["source_load_status_taxonomy"]) == SOURCE_LOAD_STATUS_VALUES
    assert set(payload["value_review_status_taxonomy"]) == VALUE_REVIEW_STATUS_VALUES
    assert set(payload["claim_level_taxonomy"]) == CLAIM_LEVEL_VALUES
    assert set(payload["guardrail_status_taxonomy"]) == GUARDRAIL_STATUS_VALUES


def test_loaded_sources_are_public_aggregate_and_safe(repo_root) -> None:
    result = build_result(repo_root)
    loaded_sources = [item for item in result.sources if item.loaded_status == "loaded"]

    assert len(loaded_sources) == 5
    for source in loaded_sources:
        assert source.public_aggregate_only is True
        assert source.restricted_data is False
        assert source.personal_data is False
        assert source.taxpayer_level_data is False
        assert source.firm_confidential_data is False
        assert source.household_microdata is False
        assert source.safe_for_repo_use is True
        assert source.source_url.startswith("https://")
        assert source.source_locator
        assert source.licence_or_access_note


def test_loaded_values_have_required_provenance_and_boundaries(repo_root) -> None:
    result = build_result(repo_root)

    assert result.loaded_public_aggregate_values
    assert result.summary.loaded_values_total == 10
    for value in result.loaded_public_aggregate_values:
        assert value.data_status == "loaded_public_aggregate"
        assert value.claim_level == "real_public_aggregate_data"
        assert value.source_url.startswith("https://")
        assert value.source_locator
        assert value.metric_name
        assert value.value is not None
        assert value.unit
        assert value.period
        assert value.geography
        assert value.public_aggregate_only is True
        assert value.restricted_data is False
        assert value.personal_data is False
        assert value.safe_for_repo_use is True
        assert value.used_for
        assert value.not_used_for
        assert value.must_not_infer


def test_source_candidates_not_loaded_are_separated(repo_root) -> None:
    result = build_result(repo_root)

    assert result.summary.source_candidates_not_loaded == 3
    assert {item.source_id for item in result.source_candidates_not_loaded} == {
        "study_assist_help_thresholds_2025_26",
        "qld_payroll_tax_threshold_2025_26",
        "abs_labour_wage_aggregate_source_reference",
    }
    assert all(item.loaded_status == "source_candidate_not_loaded" for item in result.source_candidates_not_loaded)


def test_public_real_data_summary_flags_are_bounded(repo_root) -> None:
    summary = build_result(repo_root).summary

    assert summary.public_real_data_loader_created is True
    assert summary.real_public_aggregate_data_loaded is True
    assert summary.new_public_aggregate_values_loaded == 10
    assert summary.restricted_data_loaded is False
    assert summary.personal_data_loaded is False
    assert summary.taxpayer_level_data_loaded is False
    assert summary.firm_confidential_data_loaded is False
    assert summary.household_microdata_loaded is False
    assert summary.calibration_completed is False
    assert summary.validation_claimed is False
    assert summary.actual_tax_payable_determined is False
    assert summary.official_status_claimed is False
    assert summary.firm_level_liability_logic_modified is False


def test_guardrails_fail_closed_on_restricted_loaded_source(repo_root) -> None:
    manifest = copy.deepcopy(load_manifest(repo_root))
    manifest["sources"][0]["restricted_data"] = True

    with pytest.raises(ValueError, match="restricted_data"):
        build_public_real_data_load_result(manifest, repo_root, 5, 5)


def test_guardrails_fail_closed_on_missing_source_locator(repo_root) -> None:
    manifest = copy.deepcopy(load_manifest(repo_root))
    manifest["sources"][0]["source_locator"] = ""

    with pytest.raises(ValueError, match="source_locator"):
        build_public_real_data_load_result(manifest, repo_root, 5, 5)


def test_guardrails_fail_closed_on_missing_value_unit_period_or_geography(repo_root) -> None:
    manifest = copy.deepcopy(load_manifest(repo_root))
    manifest["sources"][0]["values"][0]["unit"] = ""

    with pytest.raises(ValueError, match="unit"):
        build_public_real_data_load_result(manifest, repo_root, 5, 5)

    manifest = copy.deepcopy(load_manifest(repo_root))
    manifest["sources"][0]["values"][0]["period"] = ""
    with pytest.raises(ValueError, match="period"):
        build_public_real_data_load_result(manifest, repo_root, 5, 5)

    manifest = copy.deepcopy(load_manifest(repo_root))
    manifest["sources"][0]["values"][0]["geography"] = ""
    with pytest.raises(ValueError, match="geography"):
        build_public_real_data_load_result(manifest, repo_root, 5, 5)


def test_public_real_digest_manifest_exists_and_does_not_hash_itself(repo_root) -> None:
    path = repo_root / "data" / "public_real" / "digests" / "public_real_data_digests.json"
    payload = json.loads(path.read_text(encoding="utf-8"))
    paths = {item["path"] for item in payload["digests"]}

    assert "data/public_real/digests/public_real_data_digests.json" not in paths
    assert payload["metadata"]["digest_file_hashes_itself"] is False
    assert all(item["sha256"] for item in payload["digests"])
