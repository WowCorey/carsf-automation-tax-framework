"""Run the CARSF V1.5 real-data feasibility and calibration-intake report."""

from __future__ import annotations

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
from carsf.real_data_feasibility import (  # noqa: E402
    REAL_DATA_FEASIBILITY_NON_CLAIMS,
    build_calibration_intake_result,
    find_forbidden_affirmative_real_data_claims,
)


REPORT_STATUS = "prototype_real_data_feasibility_calibration_intake_map_only"
DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "calibration" / "real_data_feasibility_map.yaml"


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def load_real_data_feasibility_manifest(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"real data feasibility manifest must be a mapping: {path}")
    return loaded


def run_real_data_feasibility(manifest_path: Path, repo_root: Path = REPO_ROOT) -> Any:
    payload = load_real_data_feasibility_manifest(manifest_path)
    return build_calibration_intake_result(payload, repo_root)


def build_json_payload(result: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": REAL_DATA_FEASIBILITY_NON_CLAIMS,
            "real_data_loaded": False,
            "real_calibration_completed": False,
            "restricted_data_loaded": False,
            "taxpayer_data_loaded": False,
            "firm_level_confidential_data_loaded": False,
            "household_microdata_loaded": False,
            "validation_claimed": False,
            "approval_claimed": False,
            "operational_readiness_claimed": False,
            "legal_sufficiency_claimed": False,
            "official_status_claimed": False,
            "firm_level_liability_logic_modified": False,
        },
        "summary": _jsonable(result.summary),
        "real_data_feasibility": _jsonable(result),
    }


def _join(values: list[str] | None) -> str:
    if not values:
        return "None"
    return ", ".join(values)


def _summary_lines(summary: Any) -> list[str]:
    return [
        f"- Total source candidates: {summary.total_source_candidates}",
        f"- Public source candidates: {summary.public_source_candidates}",
        f"- Restricted source candidates: {summary.restricted_source_candidates}",
        f"- Forbidden repo sources: {summary.forbidden_repo_sources}",
        f"- Total calibration fields: {summary.total_calibration_fields}",
        f"- Fields public sanity check possible: {summary.fields_public_sanity_check_possible}",
        f"- Fields public calibration possible: {summary.fields_public_calibration_possible}",
        f"- Fields requiring restricted data: {summary.fields_requiring_restricted_data}",
        f"- Total realistic placeholders: {summary.total_realistic_placeholders}",
        f"- Total forbidden data rules: {summary.total_forbidden_data_rules}",
        f"- Total public data pilot candidates: {summary.total_public_data_pilot_candidates}",
        f"- Build 27 ready candidates: {summary.build_27_ready_candidates}",
        f"- real_data_loaded: {summary.real_data_loaded}",
        f"- real_calibration_completed: {summary.real_calibration_completed}",
        f"- restricted_data_loaded: {summary.restricted_data_loaded}",
        f"- taxpayer_data_loaded: {summary.taxpayer_data_loaded}",
        f"- firm_level_confidential_data_loaded: {summary.firm_level_confidential_data_loaded}",
        f"- household_microdata_loaded: {summary.household_microdata_loaded}",
        f"- realistic_placeholders_created: {summary.realistic_placeholders_created}",
        f"- placeholders_labelled: {summary.placeholders_labelled}",
        f"- public_data_pilot_ready: {summary.public_data_pilot_ready}",
        f"- validation_claimed: {summary.validation_claimed}",
        f"- approval_claimed: {summary.approval_claimed}",
        f"- operational_readiness_claimed: {summary.operational_readiness_claimed}",
        f"- legal_sufficiency_claimed: {summary.legal_sufficiency_claimed}",
        f"- official_status_claimed: {summary.official_status_claimed}",
        f"- firm_level_liability_logic_modified: {summary.firm_level_liability_logic_modified}",
    ]


def _source_table(items: list[Any]) -> list[str]:
    lines = [
        "| Source ID | Source Name | Publisher | Access Class | Data Status | Claim Level | Commit to Repo | Main Use | Must Not Be Used For |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            "| "
            f"{item.source_id} | {item.source_name} | {item.publisher} | {item.access_class} | {item.data_status} | "
            f"{item.claim_level} | {item.can_be_committed_to_repo} | {item.main_use} | must not use for: {_join(item.must_not_be_used_for)} |"
        )
    return lines


def _field_table(items: list[Any]) -> list[str]:
    lines = [
        "| Field ID | Field Name | Current Status | Required Data Status | Candidate Sources | Restricted Sources Needed | Public Sanity Check | Public Calibration Only | External Review | Must Not Claim |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            "| "
            f"{item.field_id} | {item.field_name} | {item.current_status} | {item.required_data_status} | "
            f"{_join(item.candidate_sources)} | {_join(item.restricted_sources_needed)} | "
            f"{item.can_be_publicly_sanity_checked} | {item.can_be_calibrated_from_public_data_only} | "
            f"{item.requires_external_review} | must not claim: {_join(item.must_not_claim)} |"
        )
    return lines


def _module_table(items: list[Any]) -> list[str]:
    lines = [
        "| Module ID | Module Name | Current Data Status | Public Aggregates | Synthetic Only | Restricted Calibration Needed | Sanity Check Possible | Calibration Possible Now | Main Blockers | Must Not Claim |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            "| "
            f"{item.module_id} | {item.module_name} | {item.current_data_status} | {item.can_use_public_aggregate_data} | "
            f"{item.can_only_use_synthetic_data} | {item.requires_restricted_data_for_calibration} | "
            f"{item.sanity_check_possible} | {item.calibration_possible_now} | {_join(item.main_blockers)} | "
            f"must not claim: {_join(item.must_not_claim)} |"
        )
    return lines


def _placeholder_table(items: list[Any]) -> list[str]:
    lines = [
        "| Placeholder ID | Field ID | Basis Type | Allowed Anchor Sources | Missing Real Source | Labelled Placeholder | Not Real Data | Not Calibrated |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            "| "
            f"{item.placeholder_id} | {item.field_id} | {item.basis_type} | {_join(item.allowed_anchor_sources)} | "
            f"{item.missing_real_source} | {item.must_be_labelled_realistic_placeholder} | "
            f"{item.must_not_be_labelled_real_data} | {item.must_not_be_labelled_calibrated} |"
        )
    return lines


def _restricted_table(items: list[Any]) -> list[str]:
    lines = [
        "| Requirement ID | Data Need | Restricted Sources | Affected Fields | Affected Modules | Access Class | Commit to Repo | Reason |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            "| "
            f"{item.requirement_id} | {item.data_need} | {_join(item.restricted_sources)} | {_join(item.affected_fields)} | "
            f"{_join(item.affected_modules)} | {item.access_class} | {item.can_be_committed_to_repo} | {item.reason} |"
        )
    return lines


def _forbidden_table(items: list[Any]) -> list[str]:
    lines = [
        "| Rule ID | Forbidden Data Type | Reason | Allowed Handling | Must Not Commit | Must Not Use In Tests | Guardrail Expected |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            "| "
            f"{item.rule_id} | {item.forbidden_data_type} | {item.reason} | {item.allowed_handling} | "
            f"{item.must_not_commit_to_repo} | {item.must_not_use_in_tests} | {item.guardrail_expected} |"
        )
    return lines


def _pilot_table(items: list[Any]) -> list[str]:
    lines = [
        "| Pilot ID | Source Candidate | Pilot Name | Candidate Modules | File Type | Download/API | Claim Level | Build 27 Ready | Blockers Before Loading |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        lines.append(
            "| "
            f"{item.pilot_id} | {item.source_candidate_id} | {item.pilot_name} | {_join(item.candidate_modules)} | "
            f"{item.expected_file_type} | {item.manual_download_or_api} | {item.claim_level} | "
            f"{item.build_27_ready} | {_join(item.blockers_before_loading)} |"
        )
    return lines


def _route_table(items: list[dict[str, Any]]) -> list[str]:
    lines = ["| Review Track | Scope | Main Reason |", "| --- | --- | --- |"]
    for item in items:
        lines.append(f"| {item.get('review_track')} | {_join(item.get('scope', []))} | {item.get('main_reason')} |")
    return lines


def build_markdown(result: Any, metadata: dict[str, Any]) -> str:
    lines: list[str] = [
        "# CARSF V1.5 Real Data Feasibility & Calibration Intake Map",
        "",
        "## A. Purpose",
        "",
        "This report maps potential data-source feasibility, calibration-intake needs, placeholder provenance, restricted-data blockers, forbidden repo data, and public-data pilot readiness for CARSF V1.5.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in REAL_DATA_FEASIBILITY_NON_CLAIMS)
    lines.extend(["", "## C. Data Status Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in result.data_status_taxonomy)
    lines.extend(["", "## D. Access Class Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in result.access_class_taxonomy)
    lines.extend(["", "## E. Claim Level Taxonomy", ""])
    lines.extend(f"- `{item}`" for item in result.claim_level_taxonomy)
    lines.extend(["", "## F. Source Candidate Registry", ""])
    lines.extend(_source_table(result.source_candidates))
    lines.extend(["", "## G. Calibration Field Map", ""])
    lines.extend(_field_table(result.calibration_fields))
    lines.extend(["", "## H. Module Data Needs", ""])
    lines.extend(_module_table(result.module_data_needs))
    lines.extend(["", "## I. Realistic Placeholder Rules", ""])
    lines.extend(_placeholder_table(result.realistic_placeholders))
    lines.extend(["", "## J. Restricted Data Requirements", ""])
    lines.extend(_restricted_table(result.restricted_data_requirements))
    lines.extend(["", "## K. Forbidden Repo Data Rules", ""])
    lines.extend(_forbidden_table(result.forbidden_data_rules))
    lines.extend(["", "## L. Public Data Pilot Candidates", ""])
    lines.extend(_pilot_table(result.public_data_pilot_candidates))
    lines.extend(["", "## M. What Can Be Sanity-Checked Now", ""])
    lines.append("Public aggregate candidates can support sanity-check-only comparisons and placeholder-anchor checks where public licence and source handling are reviewed before loading.")
    lines.extend(["", "## N. What Cannot Be Calibrated Yet", ""])
    lines.append("Fields requiring taxpayer, firm-level confidential, household microdata, restricted research, government-internal, or confidential material cannot be calibrated in this repo path.")
    lines.extend(["", "## O. What Must Remain Placeholder-Only", ""])
    lines.append("Behavioural response pressure bands, administrative workflow routing, anti-avoidance thresholds, legal attribution, and household microdata-dependent pathways remain placeholder-only until external review and authorised data access.")
    lines.extend(["", "## P. External Review Routes", ""])
    lines.extend(_route_table(result.external_review_routes))
    lines.extend(["", "## Q. Build 27 Public Data Pilot Readiness", ""])
    lines.extend(_summary_lines(result.summary))
    lines.extend(["", "## R. Limitations and Future Work", ""])
    lines.extend(
        [
            "- Build 26 loads no real datasets and creates no calibration values.",
            "- Realistic placeholders must remain labelled as placeholders and must not be described as real data.",
            "- Build 25 sealed the previous RC state; if Build 26 is included in a later sealed RC, the integrity seal should be regenerated for that state.",
            f"- Report generated at: {metadata.get('generated_at')}",
        ]
    )
    return "\n".join(lines) + "\n"


def write_reports(reports_dir: Path, result: Any) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    payload = build_json_payload(result, metadata)
    markdown = build_markdown(result, metadata)
    combined = json.dumps(payload, sort_keys=True) + "\n" + markdown
    forbidden = find_forbidden_affirmative_real_data_claims(combined)
    if forbidden:
        raise ValueError(f"generated real-data feasibility reports contain forbidden affirmative claims: {', '.join(forbidden)}")
    json_path = reports_dir / "real_data_feasibility.json"
    md_path = reports_dir / "real_data_feasibility.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return json_path, md_path


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-path", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args(argv)

    result = run_real_data_feasibility(args.manifest_path)
    json_path, md_path = write_reports(args.reports_dir, result)
    print(f"source candidates: {result.summary.total_source_candidates}")
    print(f"public source candidates: {result.summary.public_source_candidates}")
    print(f"restricted source candidates: {result.summary.restricted_source_candidates}")
    print(f"calibration fields: {result.summary.total_calibration_fields}")
    print(f"public data pilot candidates: {result.summary.total_public_data_pilot_candidates}")
    print(f"build 27 ready candidates: {result.summary.build_27_ready_candidates}")
    print(f"real_data_loaded: {result.summary.real_data_loaded}")
    print(f"real_calibration_completed: {result.summary.real_calibration_completed}")
    print(f"restricted_data_loaded: {result.summary.restricted_data_loaded}")
    print(f"validation_claimed: {result.summary.validation_claimed}")
    print(f"approval_claimed: {result.summary.approval_claimed}")
    print(f"firm_level_liability_logic_modified: {result.summary.firm_level_liability_logic_modified}")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
