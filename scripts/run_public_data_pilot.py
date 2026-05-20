"""Run the CARSF V1.5 public-data pilot and placeholder-anchor report."""

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
from carsf.public_data_pilot import (  # noqa: E402
    DATA_STATUS_VALUES,
    CLAIM_LEVEL_VALUES,
    PUBLIC_DATA_PILOT_NON_CLAIMS,
    build_public_data_pilot_result,
    find_forbidden_affirmative_public_data_claims,
)


REPORT_STATUS = "prototype_public_data_pilot_placeholder_anchor_layer_only"
DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "public_pilot" / "public_data_pilot_manifest.yaml"
DEFAULT_EXTRACT_PATH = REPO_ROOT / "data" / "public_pilot" / "extracts" / "public_aggregate_extracts.yaml"
DEFAULT_ANCHOR_PATH = REPO_ROOT / "data" / "public_pilot" / "placeholders" / "realistic_placeholder_anchors.yaml"
DEFAULT_DIGEST_PATH = REPO_ROOT / "data" / "public_pilot" / "digests" / "public_data_pilot_digests.json"


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def _load_yaml(path: Path) -> Any:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if loaded is None:
        raise ValueError(f"YAML file is empty: {path}")
    return loaded


def _load_manifest(path: Path) -> dict[str, Any]:
    loaded = _load_yaml(path)
    if not isinstance(loaded, dict):
        raise ValueError(f"public data pilot manifest must be a mapping: {path}")
    return loaded


def _load_list(path: Path, label: str) -> list[dict[str, Any]]:
    loaded = _load_yaml(path)
    if not isinstance(loaded, list) or not all(isinstance(item, dict) for item in loaded):
        raise ValueError(f"{label} must be a list of mappings: {path}")
    return loaded


def _digest_targets(reports_dir: Path) -> list[Path]:
    return [
        DEFAULT_MANIFEST_PATH,
        DEFAULT_EXTRACT_PATH,
        DEFAULT_ANCHOR_PATH,
        reports_dir / "public_data_pilot.md",
        reports_dir / "public_data_pilot.json",
    ]


def _write_digest_manifest(targets: list[Path], digest_path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    digest_path.parent.mkdir(parents=True, exist_ok=True)
    for path in targets:
        resolved = path.resolve()
        if resolved == digest_path.resolve():
            continue
        if not resolved.exists():
            raise ValueError(f"digest target missing: {path}")
        payload = resolved.read_bytes()
        entries.append(
            {
                "path": str(resolved.relative_to(REPO_ROOT)).replace("\\", "/"),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "bytes": len(payload),
                "digest_scope": "public_data_pilot_integrity_metadata_only",
            }
        )
    payload = {
        "metadata": {
            "non_claims": [
                "Public-data pilot digests are integrity metadata only.",
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
        f"- Total source references: {summary.total_source_references}",
        f"- Source references created: {summary.source_references_created}",
        f"- Total public aggregate extracts: {summary.total_public_aggregate_extracts}",
        f"- Real public data loaded extracts: {summary.real_public_data_loaded_extracts}",
        f"- Source-reference-only extracts: {summary.source_reference_only_extracts}",
        f"- Total placeholder anchors: {summary.total_placeholder_anchors}",
        f"- Placeholders anchored to public data: {summary.placeholders_anchored_to_public_data}",
        f"- Placeholders source-reference only: {summary.placeholders_source_reference_only}",
        f"- Total field sanity checks: {summary.total_field_sanity_checks}",
        f"- Field sanity checks passed: {summary.field_sanity_checks_passed}",
        f"- Field sanity checks warning: {summary.field_sanity_checks_warning}",
        f"- Field sanity checks blocked: {summary.field_sanity_checks_blocked}",
        f"- Total module sanity checks: {summary.total_module_sanity_checks}",
        f"- Modules sanity check possible: {summary.modules_sanity_check_possible}",
        f"- Modules placeholder anchor possible: {summary.modules_placeholder_anchor_possible}",
        f"- Modules blocked by restricted data: {summary.modules_blocked_by_restricted_data}",
        f"- Digest targets total: {summary.digest_targets_total}",
        f"- Digests written: {summary.digests_written}",
        f"- Forbidden claim findings: {summary.forbidden_claim_findings}",
        f"- Restricted data findings: {summary.restricted_data_findings}",
        f"- public_data_pilot_created: {summary.public_data_pilot_created}",
        f"- real_public_data_loaded: {summary.real_public_data_loaded}",
        f"- source_references_created: {summary.source_references_created}",
        f"- realistic_placeholders_anchored: {summary.realistic_placeholders_anchored}",
        f"- real_calibration_completed: {summary.real_calibration_completed}",
        f"- restricted_data_loaded: {summary.restricted_data_loaded}",
        f"- taxpayer_data_loaded: {summary.taxpayer_data_loaded}",
        f"- firm_level_confidential_data_loaded: {summary.firm_level_confidential_data_loaded}",
        f"- household_microdata_loaded: {summary.household_microdata_loaded}",
        f"- actual_tax_payable_determined: {summary.actual_tax_payable_determined}",
        f"- validation_claimed: {summary.validation_claimed}",
        f"- approval_claimed: {summary.approval_claimed}",
        f"- operational_readiness_claimed: {summary.operational_readiness_claimed}",
        f"- legal_sufficiency_claimed: {summary.legal_sufficiency_claimed}",
        f"- official_status_claimed: {summary.official_status_claimed}",
        f"- firm_level_liability_logic_modified: {summary.firm_level_liability_logic_modified}",
    ]


def _source_table(items: list[Any]) -> list[str]:
    lines = [
        "| Source Reference ID | Publisher | Kind | URL | Access | Extract Committed | Claim Level | Candidate Fields | Must Not Claim |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.source_reference_id} | {item.publisher} | {item.source_kind} | {item.source_url} | "
            f"{item.access_class} | {item.extract_committed} | {item.claim_level} | {_join(item.candidate_fields)} | "
            f"must not claim: {_join(item.must_not_claim)} |"
        )
    return lines


def _extract_table(items: list[Any]) -> list[str]:
    lines = [
        "| Extract ID | Source | Status | Claim Level | Period | Values | Safe To Commit | Source Locator | Value Review Status | Source Note |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        value_text = "; ".join(f"{value.get('value_id')}={value.get('value')} {value.get('unit')}" for value in item.values) or "source reference only"
        lines.append(
            f"| {item.extract_id} | {item.source_reference_id} | {item.data_status} | {item.claim_level} | "
            f"{item.period} | {value_text} | {item.safe_to_commit} | {item.source_locator} | "
            f"{item.value_review_status} | {item.source_note} |"
        )
    return lines


def _anchor_table(items: list[Any]) -> list[str]:
    lines = [
        "| Anchor ID | Field | Public Data Anchored | Strength | Blocked By Restricted Data | Missing Data For Calibration | Must Remain Placeholder |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.anchor_id} | {item.field_id} | {item.anchored_to_public_data} | {item.anchor_strength} | "
            f"{item.blocked_by_restricted_data} | {_join(item.missing_data_for_calibration)} | {item.must_be_labelled_realistic_placeholder} |"
        )
    return lines


def _field_check_table(items: list[Any]) -> list[str]:
    lines = [
        "| Check ID | Field | Type | Status | Claim Level | Extracts | Anchors | Finding |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.check_id} | {item.field_id} | {item.check_type} | {item.check_status} | {item.claim_level} | "
            f"{_join(item.public_extract_ids)} | {_join(item.placeholder_anchor_ids)} | {item.finding} |"
        )
    return lines


def _module_check_table(items: list[Any]) -> list[str]:
    lines = [
        "| Module | Status | Sanity Check Possible | Calibration Possible | Blocked By Restricted Data | Claim Level | Main Blockers |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            f"| {item.module_id} | {item.result_status} | {item.sanity_check_possible} | {item.calibration_possible} | "
            f"{item.blocked_by_restricted_data} | {item.claim_level} | {_join(item.main_blockers)} |"
        )
    return lines


def _simple_table(items: list[dict[str, Any]], columns: list[str]) -> list[str]:
    lines = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for item in items:
        lines.append("| " + " | ".join(str(item.get(column, "")) for column in columns) + " |")
    return lines


def _build_json_payload(result: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": PUBLIC_DATA_PILOT_NON_CLAIMS,
            "data_status_values": sorted(DATA_STATUS_VALUES),
            "claim_level_values": sorted(CLAIM_LEVEL_VALUES),
        },
        "summary": _jsonable(result.summary),
        "public_data_pilot": _jsonable(result),
    }


def _build_markdown(result: Any, metadata: dict[str, Any]) -> str:
    lines: list[str] = [
        "# CARSF V1.5 Public Data Pilot & Realistic Placeholder Anchor Layer",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report records the first small public aggregate-data pilot and realistic-placeholder anchor layer for CARSF V1.5.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in PUBLIC_DATA_PILOT_NON_CLAIMS)
    lines.extend(["", "## C. Public Data Loading Rules", ""])
    lines.extend(
        [
            "- Only small YAML/JSON source-reference or aggregate extract records are committed.",
            "- Loaded public records must carry source URL, publisher, licence/access notes, source note, data status, and claim level.",
            "- Source-reference-only records do not count as loaded public data.",
            "- Realistic placeholders may be anchored to public extracts, but they remain placeholders.",
        ]
    )
    lines.extend(["", "## D. Source Reference Registry", ""])
    lines.extend(_source_table(result.source_references))
    lines.extend(["", "## E. Public Aggregate Extracts", ""])
    lines.extend(_extract_table(result.public_aggregate_extracts))
    lines.extend(["", "## F. Realistic Placeholder Anchors", ""])
    lines.extend(_anchor_table(result.placeholder_anchors))
    lines.extend(["", "## G. Field Sanity Checks", ""])
    lines.extend(_field_check_table(result.field_sanity_checks))
    lines.extend(["", "## H. Module Sanity Checks", ""])
    lines.extend(_module_check_table(result.module_sanity_checks))
    lines.extend(["", "## I. Restricted Data Still Required", ""])
    lines.extend(_simple_table(result.restricted_data_blockers, ["blocker_id", "blocker", "claim_level"]))
    lines.extend(["", "## J. Forbidden Repo Data Rules", ""])
    lines.extend(_simple_table(result.forbidden_data_rules, ["rule_id", "forbidden_data_type", "must_not_commit_to_repo", "must_not_use_in_tests"]))
    lines.extend(["", "## K. What Became More Realistic", ""])
    lines.append("Wage, superannuation, corporate-tax aggregate, taxation-statistics, and fiscal aggregate placeholders now have small public-source anchors for sanity-check-only or placeholder-anchor-only review.")
    lines.extend(["", "## L. What Remains Placeholder-Only", ""])
    lines.append("OPFTE, HLE, QLC, sector schedule values, PAYG pressure, transition funding, payment interactions, and uncertainty assumptions remain realistic placeholders where used.")
    lines.extend(["", "## M. What Remains Blocked", ""])
    lines.append("Tax records, firm confidential records, person-level records, household microdata, and restricted government data remain excluded from the repository.")
    lines.extend(["", "## N. Digest Summary", ""])
    lines.extend([f"- Digest targets total: {result.summary.digest_targets_total}", f"- Digests written: {result.summary.digests_written}", "- Digest file does not hash itself."])
    lines.extend(["", "## O. Build 28 Readiness", ""])
    lines.extend(f"- {item}" for item in result.future_build_28_requirements)
    lines.extend(["", "## P. Limitations and Future Work", ""])
    lines.extend(_summary_lines(result.summary))
    text = "\n".join(lines) + "\n"
    forbidden = find_forbidden_affirmative_public_data_claims(text)
    if forbidden:
        raise ValueError(f"generated public data pilot Markdown contains forbidden affirmative claims: {', '.join(forbidden)}")
    return text


def run_public_data_pilot(
    manifest_path: Path = DEFAULT_MANIFEST_PATH,
    extracts_path: Path = DEFAULT_EXTRACT_PATH,
    anchors_path: Path = DEFAULT_ANCHOR_PATH,
    reports_dir: Path | None = None,
) -> Any:
    reports_dir = reports_dir or (REPO_ROOT / "reports")
    manifest = _load_manifest(manifest_path)
    extracts = _load_list(extracts_path, "public aggregate extracts")
    anchors = _load_list(anchors_path, "realistic placeholder anchors")
    digest_targets = _digest_targets(reports_dir)
    return build_public_data_pilot_result(
        manifest,
        extracts,
        anchors,
        REPO_ROOT,
        digest_targets_total=len(digest_targets),
        digests_written=len(digest_targets),
    )


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--extracts", type=Path, default=DEFAULT_EXTRACT_PATH)
    parser.add_argument("--anchors", type=Path, default=DEFAULT_ANCHOR_PATH)
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    parser.add_argument("--digest-path", type=Path, default=DEFAULT_DIGEST_PATH)
    args = parser.parse_args(argv)

    reports_dir = args.reports_dir
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    result = run_public_data_pilot(args.manifest, args.extracts, args.anchors, reports_dir)
    json_payload = _build_json_payload(result, metadata)
    json_text = json.dumps(json_payload, indent=2, sort_keys=True) + "\n"
    forbidden_json = find_forbidden_affirmative_public_data_claims(json_text)
    if forbidden_json:
        raise ValueError(f"generated public data pilot JSON contains forbidden affirmative claims: {', '.join(forbidden_json)}")
    json_path = reports_dir / "public_data_pilot.json"
    md_path = reports_dir / "public_data_pilot.md"
    json_path.write_text(json_text, encoding="utf-8")
    md_path.write_text(_build_markdown(result, metadata), encoding="utf-8")
    digests = _write_digest_manifest(_digest_targets(reports_dir), args.digest_path)

    print(f"source references: {result.summary.total_source_references}")
    print(f"public aggregate extracts: {result.summary.total_public_aggregate_extracts}")
    print(f"real public data loaded extracts: {result.summary.real_public_data_loaded_extracts}")
    print(f"source-reference-only extracts: {result.summary.source_reference_only_extracts}")
    print(f"placeholder anchors: {result.summary.total_placeholder_anchors}")
    print(f"digests written: {len(digests)}")
    print(f"real_public_data_loaded: {result.summary.real_public_data_loaded}")
    print(f"real_calibration_completed: {result.summary.real_calibration_completed}")
    print(f"restricted_data_loaded: {result.summary.restricted_data_loaded}")
    print(f"validation_claimed: {result.summary.validation_claimed}")
    print(f"firm_level_liability_logic_modified: {result.summary.firm_level_liability_logic_modified}")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    print(f"wrote {args.digest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
