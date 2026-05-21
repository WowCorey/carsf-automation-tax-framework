"""Run the CARSF V1.5 public real aggregate-data loader."""

from __future__ import annotations

import hashlib
import json
import sys
from argparse import ArgumentParser
from dataclasses import asdict
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
MODEL_ROOT = REPO_ROOT / "model"
if str(MODEL_ROOT) not in sys.path:
    sys.path.insert(0, str(MODEL_ROOT))

from carsf.example_runner import report_metadata  # noqa: E402
from carsf.public_real_data_loader import (  # noqa: E402
    CLAIM_LEVEL_VALUES,
    GUARDRAIL_STATUS_VALUES,
    PUBLIC_REAL_DATA_NON_CLAIMS,
    SOURCE_LOAD_STATUS_VALUES,
    VALUE_REVIEW_STATUS_VALUES,
    build_public_real_data_load_result,
    find_forbidden_affirmative_public_real_claims,
)


REPORT_STATUS = "public_real_aggregate_data_loader_only"
DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "public_real" / "manifests" / "public_real_data_sources.yaml"
DEFAULT_PARSED_PATH = REPO_ROOT / "data" / "public_real" / "parsed" / "public_real_aggregate_values.json"
DEFAULT_DIGEST_PATH = REPO_ROOT / "data" / "public_real" / "digests" / "public_real_data_digests.json"
DEFAULT_RAW_README_PATH = REPO_ROOT / "data" / "public_real" / "raw" / "README.md"
DEFAULT_REPORTS_DIR = REPO_ROOT / "reports"


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def _load_yaml(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"YAML file must be a mapping: {path}")
    return payload


def _digest_targets(reports_dir: Path, parsed_path: Path) -> list[Path]:
    return [
        DEFAULT_MANIFEST_PATH,
        DEFAULT_RAW_README_PATH,
        parsed_path,
        reports_dir / "public_real_data_loader.md",
        reports_dir / "public_real_data_loader.json",
    ]


def _write_digest_manifest(targets: list[Path], digest_path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    digest_path.parent.mkdir(parents=True, exist_ok=True)
    resolved_digest = digest_path.resolve()
    for path in targets:
        resolved = path.resolve()
        if resolved == resolved_digest:
            continue
        if not resolved.exists():
            raise ValueError(f"digest target missing: {path}")
        payload = resolved.read_bytes()
        try:
            path_label = str(resolved.relative_to(REPO_ROOT)).replace("\\", "/")
        except ValueError:
            path_label = str(resolved).replace("\\", "/")
        entries.append(
            {
                "path": path_label,
                "sha256": hashlib.sha256(payload).hexdigest(),
                "bytes": len(payload),
                "digest_scope": "public_real_data_loader_integrity_metadata_only",
            }
        )
    payload = {
        "metadata": {
            "non_claims": [
                "Public real-data loader digests are integrity metadata only.",
                "They are not signatures, not external attestation, not approval, not validation, and not calibration.",
            ],
            "digest_file_hashes_itself": False,
        },
        "digests": entries,
    }
    digest_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return entries


def _join(values: list[str] | None) -> str:
    if not values:
        return "None"
    return ", ".join(str(item) for item in values)


def _summary_lines(summary: Any) -> list[str]:
    return [
        f"- total_sources: {summary.total_sources}",
        f"- loaded_sources: {summary.loaded_sources}",
        f"- source_candidates_not_loaded: {summary.source_candidates_not_loaded}",
        f"- blocked_sources: {summary.blocked_sources}",
        f"- rejected_sources: {summary.rejected_sources}",
        f"- loaded_values_total: {summary.loaded_values_total}",
        f"- loaded_value_units_present: {summary.loaded_value_units_present}",
        f"- loaded_value_periods_present: {summary.loaded_value_periods_present}",
        f"- loaded_value_geographies_present: {summary.loaded_value_geographies_present}",
        f"- guardrail_findings_total: {summary.guardrail_findings_total}",
        f"- guardrail_fail_closed_findings: {summary.guardrail_fail_closed_findings}",
        f"- digest_targets_total: {summary.digest_targets_total}",
        f"- digests_written: {summary.digests_written}",
        f"- forbidden_claim_findings: {summary.forbidden_claim_findings}",
        f"- public_real_data_loader_created: {summary.public_real_data_loader_created}",
        f"- real_public_aggregate_data_loaded: {summary.real_public_aggregate_data_loaded}",
        f"- new_public_aggregate_values_loaded: {summary.new_public_aggregate_values_loaded}",
        f"- restricted_data_loaded: {summary.restricted_data_loaded}",
        f"- personal_data_loaded: {summary.personal_data_loaded}",
        f"- taxpayer_level_data_loaded: {summary.taxpayer_level_data_loaded}",
        f"- firm_confidential_data_loaded: {summary.firm_confidential_data_loaded}",
        f"- household_microdata_loaded: {summary.household_microdata_loaded}",
        f"- calibration_completed: {summary.calibration_completed}",
        f"- validation_claimed: {summary.validation_claimed}",
        f"- actual_tax_payable_determined: {summary.actual_tax_payable_determined}",
        f"- official_status_claimed: {summary.official_status_claimed}",
        f"- firm_level_liability_logic_modified: {summary.firm_level_liability_logic_modified}",
    ]


def _source_table(items: list[Any]) -> list[str]:
    lines = [
        "| Source ID | Publisher | Status | URL | Locator | Public Aggregate Only | Safe For Repo | Allowed Use | Must Not Infer |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.source_id} | {item.publisher} | {item.loaded_status} | {item.source_url} | {item.source_locator} | "
            f"{item.public_aggregate_only} | {item.safe_for_repo_use} | {_join(item.allowed_use)} | {_join(item.must_not_infer)} |"
        )
    return lines


def _value_table(items: list[Any]) -> list[str]:
    lines = [
        "| Value ID | Source | Metric | Value | Unit | Period | Geography | Review Status | Used For | Must Not Infer |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.value_id} | {item.source_id} | {item.metric_name} | {item.value} | {item.unit} | {item.period} | "
            f"{item.geography} | {item.value_review_status} | {_join(item.used_for)} | {_join(item.must_not_infer)} |"
        )
    return lines


def _guardrail_table(items: list[Any]) -> list[str]:
    lines = [
        "| Finding ID | Guardrail | Status | Finding |",
        "| --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(f"| {item.finding_id} | {item.guardrail} | {item.status} | {item.finding} |")
    return lines


def _write_parsed_values(result: Any, parsed_path: Path) -> None:
    parsed_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "metadata": {
            "status": REPORT_STATUS,
            "non_claims": PUBLIC_REAL_DATA_NON_CLAIMS,
            "data_status": "loaded_public_aggregate",
        },
        "summary": {
            "loaded_values_total": result.summary.loaded_values_total,
            "real_public_aggregate_data_loaded": result.summary.real_public_aggregate_data_loaded,
            "calibration_completed": False,
            "validation_claimed": False,
            "actual_tax_payable_determined": False,
            "firm_level_liability_logic_modified": False,
        },
        "values": [_jsonable(item) for item in result.loaded_public_aggregate_values],
    }
    parsed_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _build_json_payload(result: Any, metadata: dict[str, Any], digest_targets_total: int) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": PUBLIC_REAL_DATA_NON_CLAIMS,
            "source_load_status_values": sorted(SOURCE_LOAD_STATUS_VALUES),
            "value_review_status_values": sorted(VALUE_REVIEW_STATUS_VALUES),
            "claim_level_values": sorted(CLAIM_LEVEL_VALUES),
            "guardrail_status_values": sorted(GUARDRAIL_STATUS_VALUES),
        },
        "summary": _jsonable(result.summary),
        "public_real_data_loader": _jsonable(result),
        "digest_manifest_summary": {
            "digest_manifest_path": "data/public_real/digests/public_real_data_digests.json",
            "digest_targets_total": digest_targets_total,
            "digests_written": digest_targets_total,
            "digest_file_hashes_itself": False,
        },
    }


def _build_markdown(result: Any, metadata: dict[str, Any], digest_targets_total: int) -> str:
    loaded_sources = [item for item in result.sources if item.loaded_status == "loaded"]
    lines: list[str] = [
        "# CARSF V1.5 Public Real Aggregate Data Loader",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report records the first controlled repo-local public aggregate data loader for CARSF V1.5.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in PUBLIC_REAL_DATA_NON_CLAIMS)
    lines.extend(["", "## C. Source Inclusion Rules", ""])
    lines.extend(
        [
            "- A loaded source must be public, aggregate-level, non-personal, non-confidential, source-located, and safe for repository use.",
            "- A source candidate without a safe exact local value remains source_candidate_not_loaded.",
            "- No raw downloaded datasets are committed by this build.",
        ]
    )
    lines.extend(["", "## D. Loaded Public Aggregate Sources", ""])
    lines.extend(_source_table(loaded_sources))
    lines.extend(["", "## E. Source Candidates Not Loaded", ""])
    lines.extend(_source_table(result.source_candidates_not_loaded))
    lines.extend(["", "## F. Loaded Public Aggregate Values", ""])
    lines.extend(_value_table(result.loaded_public_aggregate_values))
    lines.extend(["", "## G. Guardrail Checks", ""])
    lines.extend(_guardrail_table(result.guardrail_findings))
    lines.extend(["", "## H. Digest Manifest", ""])
    lines.extend(
        [
            f"- Digest targets total: {digest_targets_total}",
            f"- Digests written: {digest_targets_total}",
            "- Digest file does not hash itself.",
            "- Digests are integrity metadata only, not signatures, not external attestation, not approval, not validation, and not calibration.",
        ]
    )
    lines.extend(["", "## I. What This Data Can Support", ""])
    lines.extend(
        [
            "- Sanity-check context for fiscal scale, wage thresholds, corporate tax aggregate context, and public rate settings.",
            "- Placeholder replacement review candidates for a later build.",
            "- Reviewer inspection of source URL, locator, unit, period, and geography metadata.",
        ]
    )
    lines.extend(["", "## J. What This Data Cannot Support", ""])
    lines.extend(
        [
            "- It cannot support calibration completion, validation, official status, tax-payable determination, legal advice, tax advice, ATO guidance, Treasury modelling, PBO costing, or firm-level CARSF liability changes.",
            "- It cannot support restricted-data, taxpayer-level, person-level, firm-confidential, or household-microdata analysis.",
        ]
    )
    lines.extend(["", "## K. Placeholder Replacement Candidates", ""])
    lines.append("Fair Work wage thresholds, ATO aggregate tax context, Budget Paper receipt aggregates, and super guarantee rate settings can be mapped to placeholder replacement candidates in Build 32 without claiming calibration.")
    lines.extend(["", "## L. Calibration Blockers Still Remaining", ""])
    lines.append("Restricted tax records, firm-confidential records, household microdata, person-level welfare/payment records, behavioural elasticity evidence, legal drafting review, and external statistical review remain blockers.")
    lines.extend(["", "## M. Build 32 Readiness", ""])
    lines.extend(f"- {item}" for item in result.future_build_32_requirements)
    lines.extend(["", "## N. Limitations and Future Work", ""])
    lines.extend(_summary_lines(result.summary))
    text = "\n".join(lines) + "\n"
    forbidden = find_forbidden_affirmative_public_real_claims(text)
    if forbidden:
        raise ValueError(f"generated public real data Markdown contains forbidden affirmative claims: {', '.join(forbidden)}")
    return text


def run_public_real_data_loader(
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
    parsed_path: Path = DEFAULT_PARSED_PATH,
    reports_dir: Path = DEFAULT_REPORTS_DIR,
    digest_path: Path = DEFAULT_DIGEST_PATH,
) -> tuple[Path, Path, Path, Path, dict[str, Any]]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    manifest = _load_yaml(manifest_path)
    digest_targets = _digest_targets(reports_dir, parsed_path)
    result = build_public_real_data_load_result(
        manifest,
        REPO_ROOT,
        digest_targets_total=len(digest_targets),
        digests_written=len(digest_targets),
    )
    _write_parsed_values(result, parsed_path)
    metadata = report_metadata()
    json_payload = _build_json_payload(result, metadata, len(digest_targets))
    json_text = json.dumps(json_payload, indent=2, sort_keys=True) + "\n"
    forbidden_json = find_forbidden_affirmative_public_real_claims(json_text)
    if forbidden_json:
        raise ValueError(f"generated public real data JSON contains forbidden affirmative claims: {', '.join(forbidden_json)}")
    json_path = reports_dir / "public_real_data_loader.json"
    md_path = reports_dir / "public_real_data_loader.md"
    json_path.write_text(json_text, encoding="utf-8")
    md_path.write_text(_build_markdown(result, metadata, len(digest_targets)), encoding="utf-8")
    _write_digest_manifest(_digest_targets(reports_dir, parsed_path), digest_path)
    return json_path, md_path, parsed_path, digest_path, json_payload


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--parsed-path", type=Path, default=DEFAULT_PARSED_PATH)
    parser.add_argument("--reports-dir", type=Path, default=DEFAULT_REPORTS_DIR)
    parser.add_argument("--digest-path", type=Path, default=DEFAULT_DIGEST_PATH)
    args = parser.parse_args(argv)

    json_path, md_path, parsed_path, digest_path, payload = run_public_real_data_loader(
        args.manifest,
        args.parsed_path,
        args.reports_dir,
        args.digest_path,
    )
    summary = payload["summary"]
    print(f"loaded sources: {summary['loaded_sources']}")
    print(f"source candidates not loaded: {summary['source_candidates_not_loaded']}")
    print(f"loaded public aggregate values: {summary['loaded_values_total']}")
    print(f"new_public_aggregate_values_loaded: {summary['new_public_aggregate_values_loaded']}")
    print(f"restricted_data_loaded: {summary['restricted_data_loaded']}")
    print(f"personal_data_loaded: {summary['personal_data_loaded']}")
    print(f"taxpayer_level_data_loaded: {summary['taxpayer_level_data_loaded']}")
    print(f"firm_confidential_data_loaded: {summary['firm_confidential_data_loaded']}")
    print(f"household_microdata_loaded: {summary['household_microdata_loaded']}")
    print(f"calibration_completed: {summary['calibration_completed']}")
    print(f"validation_claimed: {summary['validation_claimed']}")
    print(f"actual_tax_payable_determined: {summary['actual_tax_payable_determined']}")
    print(f"official_status_claimed: {summary['official_status_claimed']}")
    print(f"firm_level_liability_logic_modified: {summary['firm_level_liability_logic_modified']}")
    print(f"wrote {parsed_path}")
    print(f"wrote {digest_path}")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
