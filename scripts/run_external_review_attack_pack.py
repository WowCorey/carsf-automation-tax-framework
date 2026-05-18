"""Run the CARSF V1.5 external review attack-pack report."""

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
from carsf.external_review_attack_pack import (  # noqa: E402
    EXTERNAL_REVIEW_ATTACK_PACK_NON_CLAIMS,
    build_external_review_attack_pack_result,
    find_forbidden_affirmative_attack_pack_claims,
)


REPORT_STATUS = "prototype_external_review_attack_pack_only"
DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "review" / "v1_5_external_review_attack_pack.yaml"


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def load_attack_pack_manifest(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"attack pack manifest must be a mapping: {path}")
    return loaded


def run_external_review_attack_pack(manifest_path: Path, repo_root: Path = REPO_ROOT) -> Any:
    payload = load_attack_pack_manifest(manifest_path)
    return build_external_review_attack_pack_result(payload, repo_root)


def build_json_payload(result: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": EXTERNAL_REVIEW_ATTACK_PACK_NON_CLAIMS,
            "review_completed": False,
            "approval_claimed": False,
            "validation_claimed": False,
            "readiness_score_created": False,
            "legal_sufficiency_claimed": False,
            "operational_readiness_claimed": False,
            "legislative_readiness_claimed": False,
            "official_status_claimed": False,
            "real_data_used": False,
            "firm_level_liability_logic_modified": False,
        },
        "summary": _jsonable(result.summary),
        "external_review_attack_pack": _jsonable(result),
    }


def _join(values: list[str] | None) -> str:
    if not values:
        return "None"
    return ", ".join(values)


def _join_must_not(values: list[str] | None) -> str:
    if not values:
        return "None"
    return "; ".join(f"must not be used for: {item}" for item in values)


def _summary_lines(summary: Any) -> list[str]:
    return [
        f"- Total review tracks: {summary.total_review_tracks}",
        f"- Total attack questions: {summary.total_attack_questions}",
        f"- Total failure modes: {summary.total_failure_modes}",
        f"- Total boundary checks: {summary.total_boundary_checks}",
        f"- Total report attack rows: {summary.total_report_attack_rows}",
        f"- Total layer attack rows: {summary.total_layer_attack_rows}",
        f"- Total release documents: {summary.total_release_documents}",
        f"- Release documents present: {summary.release_documents_present}",
        f"- Release documents missing: {summary.release_documents_missing}",
        f"- Reports referenced: {summary.reports_referenced}",
        f"- Reports missing: {summary.reports_missing}",
        f"- Layers referenced: {summary.layers_referenced}",
        f"- Unknown layers: {summary.unknown_layers}",
        f"- Tracks with required question count: {summary.tracks_with_required_question_count}",
        f"- Tracks missing required question count: {summary.tracks_missing_required_question_count}",
        f"- review_completed: {summary.review_completed}",
        f"- approval_claimed: {summary.approval_claimed}",
        f"- validation_claimed: {summary.validation_claimed}",
        f"- readiness_score_created: {summary.readiness_score_created}",
        f"- legal_sufficiency_claimed: {summary.legal_sufficiency_claimed}",
        f"- operational_readiness_claimed: {summary.operational_readiness_claimed}",
        f"- legislative_readiness_claimed: {summary.legislative_readiness_claimed}",
        f"- official_status_claimed: {summary.official_status_claimed}",
        f"- real_data_used: {summary.real_data_used}",
        f"- firm_level_liability_logic_modified: {summary.firm_level_liability_logic_modified}",
    ]


def _track_index_table(tracks: list[Any]) -> list[str]:
    lines = [
        "| Track | Reviewer Type | Inspect First | Layers | Reports | Questions | Failure Modes |",
        "| --- | --- | --- | --- | --- | ---: | ---: |",
    ]
    for track in tracks:
        lines.append(
            "| "
            f"{track.track_name} | {track.reviewer_type} | {_join(track.inspect_first)} | "
            f"{_join(track.relevant_layers)} | {_join(track.relevant_reports)} | "
            f"{len(track.core_attack_questions)} | {len(track.failure_modes)} |"
        )
    return lines


def _question_table(questions: list[Any]) -> list[str]:
    lines = [
        "| Question ID | Category | Severity | Question | Targets | What Would Fail | Required Evidence / Review |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for question in questions:
        lines.append(
            "| "
            f"{question.question_id} | {question.attack_category} | {question.severity_label} | "
            f"{question.question} | {_join(question.target_layers)} | {question.what_would_fail} | "
            f"{question.required_evidence_or_review} |"
        )
    return lines


def _failure_table(failures: list[Any]) -> list[str]:
    lines = [
        "| Failure ID | Severity | Failure Mode | Affected Layers | Boundary At Risk | Required Follow-Up | Not Actual Error Finding |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for failure in failures:
        lines.append(
            "| "
            f"{failure.failure_id} | {failure.severity_label} | {failure.failure_mode} | "
            f"{_join(failure.affected_layers)} | {failure.boundary_at_risk} | {failure.required_follow_up} | "
            f"{failure.not_a_finding_of_actual_error} |"
        )
    return lines


def _track_section(track: Any) -> list[str]:
    lines = [
        f"### {track.track_name}",
        "",
        f"Purpose: {track.purpose}",
        "",
        "Inspect first: " + _join(track.inspect_first),
        "",
        "Attack questions:",
        "",
    ]
    lines.extend(_question_table(track.core_attack_questions))
    lines.extend(["", "Failure modes:", ""])
    lines.extend(_failure_table(track.failure_modes))
    lines.extend(["", "Required external inputs or reviews:", ""])
    lines.extend(f"- {item}" for item in track.required_external_inputs)
    lines.extend(["", "Must not infer:", ""])
    lines.extend(f"- {item}" for item in track.must_not_infer)
    lines.extend(["", f"Suggested reviewer output format: {track.recommended_output_format}", ""])
    return lines


def _boundary_table(boundary_checks: list[Any]) -> list[str]:
    lines = [
        "| Boundary ID | Boundary Question | Prohibited Claims | Allowed Negative Warnings | Affected Layers | Fail Closed |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for check in boundary_checks:
        lines.append(
            "| "
            f"{check.boundary_id} | {check.boundary_question} | {_join(check.prohibited_affirmative_claims)} | "
            f"{_join(check.allowed_negative_warnings)} | {_join(check.affected_layers)} | {check.fail_closed_if_found} |"
        )
    return lines


def _report_attack_table(rows: list[Any]) -> list[str]:
    lines = [
        "| Report | Layer | Reviewer Tracks | Attack Questions | Likely Overread Risk | Blockers | Must Not Be Used For | Required Follow-Up |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row.report_path} | {row.layer_id} | {_join(row.primary_reviewer_tracks)} | "
            f"{_join(row.attack_question_ids)} | {row.likely_overread_risk} | "
            f"{_join(row.calibration_or_review_blockers)} | {_join_must_not(row.must_not_be_used_for)} | "
            f"{row.required_follow_up} |"
        )
    return lines


def _layer_attack_table(rows: list[Any]) -> list[str]:
    lines = [
        "| Layer ID | Layer Name | Attack Tracks | Categories | Known Blockers | Missing External Inputs | Failure Modes | Must Not Infer | Locked Until Review |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row.layer_id} | {row.layer_name} | {_join(row.attack_tracks)} | {_join(row.attack_categories)} | "
            f"{_join(row.known_blockers)} | {_join(row.missing_external_inputs)} | {_join(row.failure_mode_ids)} | "
            f"{_join_must_not(row.must_not_infer)} | {_join(row.locked_until_review)} |"
        )
    return lines


def _document_table(documents: list[Any]) -> list[str]:
    lines = [
        "| Document | Exists | Contains Non-Claims |",
        "| --- | --- | --- |",
    ]
    for document in documents:
        lines.append(f"| {document.document_path} | {document.exists} | {document.contains_non_claims} |")
    return lines


TRACK_SECTION_HEADINGS = {
    "policy_review": "## F. Policy Review Attacks",
    "technical_review": "## G. Technical Review Attacks",
    "legal_review": "## H. Legal Review Attacks",
    "tax_review": "## I. Tax Review Attacks",
    "ato_methods_review": "## J. ATO Methods Review Attacks",
    "treasury_methods_review": "## K. Treasury Methods Review Attacks",
    "privacy_review": "## L. Privacy / Secrecy Review Attacks",
    "statistical_methods_review": "## M. Statistical Methods Review Attacks",
    "economic_methods_review": "## N. Economic Methods Review Attacks",
    "welfare_policy_review": "## O. Welfare Policy Review Attacks",
    "parliamentary_counsel_review": "## P. Parliamentary Counsel Review Attacks",
    "hostile_red_team_review": "## Q. Hostile / Red-Team Attacks",
}


def build_markdown(result: Any, metadata: dict[str, Any]) -> str:
    lines = [
        "# CARSF V1.5 External Review Attack Pack",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report turns V1.5 release-candidate limitations into reviewer challenge questions, failure modes, boundary checks, report attack rows, and layer attack rows.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in EXTERNAL_REVIEW_ATTACK_PACK_NON_CLAIMS)
    lines.extend(
        [
            "- review_completed: False",
            "- approval_claimed: False",
            "- validation_claimed: False",
            "- readiness_score_created: False",
            "- legal_sufficiency_claimed: False",
            "- operational_readiness_claimed: False",
            "- legislative_readiness_claimed: False",
            "- official_status_claimed: False",
            "- real_data_used: False",
            "- firm_level_liability_logic_modified: False",
            "",
            "## C. How to Use the Attack Pack",
            "",
            "Use this as a challenge map. Reviewers should record issues, missing evidence, and required follow-up; they should not treat challenge severity as validation, approval, readiness, or a score.",
            "",
        ]
    )
    lines.extend(_summary_lines(result.summary))
    lines.extend(["", "## D. Review Track Index", ""])
    lines.extend(_track_index_table(result.review_tracks))
    lines.extend(["", "## E. Cross-Cutting Boundary Checks", ""])
    lines.extend(_boundary_table(result.boundary_checks))

    tracks_by_id = {track.track_id: track for track in result.review_tracks}
    for track_id, heading in TRACK_SECTION_HEADINGS.items():
        lines.extend(["", heading, ""])
        lines.extend(_track_section(tracks_by_id[track_id]))

    lines.extend(["", "## R. Report-by-Report Attack Matrix", ""])
    lines.extend(_report_attack_table(result.report_attack_matrix))
    lines.extend(["", "## S. Layer-by-Layer Attack Matrix", ""])
    lines.extend(_layer_attack_table(result.layer_attack_matrix))
    lines.extend(["", "## T. Locked-Until-Review Items", ""])
    lines.extend(f"- {item}" for item in result.locked_until_review_items)
    lines.extend(["", "## U. Required External Inputs", ""])
    lines.extend(f"- {item}" for item in result.required_external_inputs)
    lines.extend(["", "## V. Suggested Reviewer Output Format", ""])
    lines.append(result.suggested_reviewer_output_format)
    lines.extend(["", "Attack-pack release documents:", ""])
    lines.extend(_document_table(result.release_documents))
    lines.extend(
        [
            "",
            "## W. Limitations and Future Work",
            "",
            "- Attack pack only.",
            "- External review has not been completed.",
            "- Approval has not been granted.",
            "- Validation has not occurred.",
            "- Not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare validation, not statistical validation, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, not official status, and not an official review pathway.",
            "- It does not determine actual tax payable, does not use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, and does not modify firm-level CARSF liability.",
        ]
    )
    return "\n".join(lines) + "\n"


def write_reports(result: Any, reports_dir: Path, metadata: dict[str, Any]) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = reports_dir / "external_review_attack_pack.json"
    md_path = reports_dir / "external_review_attack_pack.md"
    payload = build_json_payload(result, metadata)
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    markdown = build_markdown(result, metadata)
    forbidden = find_forbidden_affirmative_attack_pack_claims(markdown)
    if forbidden:
        raise ValueError(f"external review attack-pack report contains forbidden affirmative claims: {', '.join(forbidden)}")
    md_path.write_text(markdown, encoding="utf-8")
    return json_path, md_path


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args(argv)

    metadata = report_metadata()
    result = run_external_review_attack_pack(args.manifest)
    json_path, md_path = write_reports(result, args.reports_dir, metadata)
    print(f"external review attack pack report written: {json_path}")
    print(f"external review attack pack report written: {md_path}")
    print(f"review tracks: {result.summary.total_review_tracks}")
    print(f"attack questions: {result.summary.total_attack_questions}")
    print(f"report attack rows: {result.summary.total_report_attack_rows}")
    print(f"layer attack rows: {result.summary.total_layer_attack_rows}")
    print(f"review_completed: {result.summary.review_completed}")
    print(f"approval_claimed: {result.summary.approval_claimed}")
    print(f"validation_claimed: {result.summary.validation_claimed}")
    print(f"readiness_score_created: {result.summary.readiness_score_created}")
    print(f"firm_level_liability_logic_modified: {result.summary.firm_level_liability_logic_modified}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
