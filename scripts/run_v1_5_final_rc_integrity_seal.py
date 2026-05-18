"""Run the CARSF V1.5 final RC integrity seal report."""

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
from carsf.final_rc_integrity_seal import (  # noqa: E402
    FINAL_RC_INTEGRITY_SEAL_NON_CLAIMS,
    build_final_rc_integrity_seal_result,
    find_forbidden_affirmative_seal_claims,
)


REPORT_STATUS = "internal_integrity_seal_only"
DEFAULT_MANIFEST_PATH = REPO_ROOT / "data" / "seal" / "v1_5_final_rc_integrity_seal.yaml"


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def load_seal_manifest(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"seal manifest must be a mapping: {path}")
    return loaded


def run_final_rc_integrity_seal(manifest_path: Path, repo_root: Path = REPO_ROOT) -> Any:
    payload = load_seal_manifest(manifest_path)
    return build_final_rc_integrity_seal_result(payload, repo_root)


def build_json_payload(result: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": FINAL_RC_INTEGRITY_SEAL_NON_CLAIMS,
            "review_completed": False,
            "approval_claimed": False,
            "validation_claimed": False,
            "readiness_score_created": False,
            "maturity_score_created": False,
            "operational_readiness_claimed": False,
            "legal_sufficiency_claimed": False,
            "legislative_readiness_claimed": False,
            "economic_validation_claimed": False,
            "welfare_validation_claimed": False,
            "statistical_validation_claimed": False,
            "official_status_claimed": False,
            "official_review_pathway_claimed": False,
            "real_data_used": False,
            "actual_tax_payable_determined": False,
            "compliance_scoring_created": False,
            "enforcement_created": False,
            "notices_created": False,
            "penalties_created": False,
            "operative_law_created": False,
            "firm_level_liability_logic_modified": False,
        },
        "summary": _jsonable(result.summary),
        "final_rc_integrity_seal": _jsonable(result),
    }


def _join(values: list[str] | None) -> str:
    if not values:
        return "None"
    return ", ".join(str(value) for value in values)


def _summary_lines(summary: Any) -> list[str]:
    return [
        f"- Total release documents required: {summary.total_release_documents_required}",
        f"- Release documents present: {summary.release_documents_present}",
        f"- Release documents missing: {summary.release_documents_missing}",
        f"- Total attack-pack documents required: {summary.total_attack_pack_documents_required}",
        f"- Attack-pack documents present: {summary.attack_pack_documents_present}",
        f"- Attack-pack documents missing: {summary.attack_pack_documents_missing}",
        f"- Total generated reports required: {summary.total_generated_reports_required}",
        f"- Generated reports present: {summary.generated_reports_present}",
        f"- Generated reports missing: {summary.generated_reports_missing}",
        f"- Total required manifests: {summary.total_required_manifests}",
        f"- Manifests present: {summary.manifests_present}",
        f"- Manifests missing: {summary.manifests_missing}",
        f"- Total required scripts: {summary.total_required_scripts}",
        f"- Scripts present: {summary.scripts_present}",
        f"- Scripts missing: {summary.scripts_missing}",
        f"- Digest targets total: {summary.digest_targets_total}",
        f"- Digests written: {summary.digests_written}",
        f"- Forbidden claim findings: {summary.forbidden_claim_findings}",
        f"- Boundary phrase failures: {summary.boundary_phrase_failures}",
        f"- False flag failures: {summary.false_flag_failures}",
        f"- Guardrail denied findings: {summary.guardrail_denied_findings}",
        f"- seal_passed: {summary.seal_passed}",
        f"- review_completed: {summary.review_completed}",
        f"- approval_claimed: {summary.approval_claimed}",
        f"- validation_claimed: {summary.validation_claimed}",
        f"- readiness_score_created: {summary.readiness_score_created}",
        f"- maturity_score_created: {summary.maturity_score_created}",
        f"- operational_readiness_claimed: {summary.operational_readiness_claimed}",
        f"- legal_sufficiency_claimed: {summary.legal_sufficiency_claimed}",
        f"- legislative_readiness_claimed: {summary.legislative_readiness_claimed}",
        f"- economic_validation_claimed: {summary.economic_validation_claimed}",
        f"- welfare_validation_claimed: {summary.welfare_validation_claimed}",
        f"- statistical_validation_claimed: {summary.statistical_validation_claimed}",
        f"- official_status_claimed: {summary.official_status_claimed}",
        f"- official_review_pathway_claimed: {summary.official_review_pathway_claimed}",
        f"- real_data_used: {summary.real_data_used}",
        f"- actual_tax_payable_determined: {summary.actual_tax_payable_determined}",
        f"- compliance_scoring_created: {summary.compliance_scoring_created}",
        f"- enforcement_created: {summary.enforcement_created}",
        f"- notices_created: {summary.notices_created}",
        f"- penalties_created: {summary.penalties_created}",
        f"- operative_law_created: {summary.operative_law_created}",
        f"- firm_level_liability_logic_modified: {summary.firm_level_liability_logic_modified}",
    ]


def _artefact_table(rows: list[Any]) -> list[str]:
    lines = [
        "| Artefact | Group | Exists | Status | Main Reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| {row.artefact_path} | {row.artefact_group} | {row.exists} | {row.status} | {row.main_reason} |")
    return lines


def _document_table(rows: list[Any]) -> list[str]:
    lines = [
        "| Document | Group | Exists | Boundary Phrases Present | Missing Boundary Phrases | Forbidden Claims | Status |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row.document_path} | {row.document_group} | {row.exists} | {row.contains_boundary_phrases} | "
            f"{_join(row.missing_boundary_phrases)} | {_join(row.forbidden_claim_findings)} | {row.status} |"
        )
    return lines


def _report_table(rows: list[Any]) -> list[str]:
    lines = [
        "| Report | Exists | Forbidden Claims | Status | Main Reason |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| {row.report_path} | {row.exists} | {_join(row.forbidden_claim_findings)} | {row.status} | {row.main_reason} |")
    return lines


def _manifest_table(rows: list[Any]) -> list[str]:
    lines = [
        "| Manifest | Exists | Aligned | Checked Items | Missing Items | Main Reason |",
        "| --- | --- | --- | ---: | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| {row.manifest_path} | {row.exists} | {row.aligned} | {row.checked_items} | {_join(row.missing_items)} | {row.main_reason} |")
    return lines


def _digest_table(rows: list[Any]) -> list[str]:
    lines = [
        "| Artefact | Exists | SHA-256 | Bytes | Status |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(f"| {row.artefact_path} | {row.exists} | {row.sha256 or 'None'} | {row.byte_count or 0} | {row.status} |")
    return lines


def _false_flag_table(rows: list[Any]) -> list[str]:
    lines = [
        "| Flag | Expected | Actual | Source | Passed | Main Reason |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| {row.flag_name} | {row.expected_value} | {row.actual_value} | {row.source_path} | {row.passed} | {row.main_reason} |")
    return lines


def _boundary_table(rows: list[Any]) -> list[str]:
    lines = [
        "| Boundary Phrase | Checked Locations | Missing Locations | Passed |",
        "| --- | --- | --- | --- |",
    ]
    for row in rows:
        lines.append(f"| {row.boundary_phrase} | {len(row.checked_locations)} | {_join(row.missing_locations)} | {row.passed} |")
    return lines


def build_markdown(result: Any, metadata: dict[str, Any]) -> str:
    lines = [
        "# CARSF V1.5 Final RC Integrity Seal",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report records an internal final release-candidate integrity check for the CARSF V1.5 private research prototype. It checks artefact presence, manifest alignment, report availability, boundary language, digest metadata, guardrail expectations, CI expectations, and false readiness/legal/validation flags.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in FINAL_RC_INTEGRITY_SEAL_NON_CLAIMS)
    lines.extend(
        [
            "- This is not approval.",
            "- This is not validation.",
            "- External review has not been completed.",
            "- This is not legal advice.",
            "- This is not tax advice.",
            "- This is not ATO guidance.",
            "- This is not Treasury modelling.",
            "- This is not economic validation.",
            "- This is not welfare validation.",
            "- This is not statistical validation.",
            "- This is not compliance scoring.",
            "- This is not enforcement.",
            "- This is not operational readiness.",
            "- This is not legal sufficiency.",
            "- This is not legislative readiness.",
            "- This is not a readiness score.",
            "- This is not a maturity score.",
            "- This is not official status.",
            "- This is not an official review pathway.",
            "- It does not determine actual tax payable.",
            "- It does not use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.",
            "- It does not modify firm-level CARSF liability.",
            "",
            "## C. Seal Method",
            "",
        ]
    )
    lines.extend(_summary_lines(result.summary))
    lines.extend(["", "## D. Release Document Inventory", ""])
    lines.extend(_document_table(result.release_document_checks))
    lines.extend(["", "## E. Attack-Pack Document Inventory", ""])
    lines.extend(_document_table(result.attack_pack_document_checks))
    lines.extend(["", "## F. Generated Report Inventory", ""])
    lines.extend(_report_table(result.generated_report_checks))
    lines.extend(["", "## G. Manifest Alignment", ""])
    lines.extend(_manifest_table(result.manifest_alignment_checks))
    lines.extend(["", "## H. Digest Summary", ""])
    lines.extend(_digest_table(result.digest_manifest))
    lines.extend(["", "## I. False Flag Verification", ""])
    lines.extend(_false_flag_table(result.false_flag_checks))
    lines.extend(["", "## J. Boundary Phrase Verification", ""])
    lines.extend(_boundary_table(result.boundary_phrase_checks))
    lines.extend(["", "## K. Forbidden Claim Scan", ""])
    lines.append(f"- Forbidden affirmative claim findings: {result.summary.forbidden_claim_findings}")
    lines.append("- Forbidden claim scanning is fail-closed and allows required negative warnings such as not approval, not validation, and not legally sufficient.")
    lines.extend(["", "## L. Guardrail Status", ""])
    lines.extend(
        [
            f"- Source report: {result.guardrail_status.source_report}",
            f"- Exists: {result.guardrail_status.exists}",
            f"- Readable: {result.guardrail_status.readable}",
            f"- Clean: {result.guardrail_status.clean}",
            f"- Denied findings: {result.guardrail_status.denied_findings}",
            f"- Warning findings: {result.guardrail_status.warning_findings}",
            f"- Status: {result.guardrail_status.status}",
            f"- Main reason: {result.guardrail_status.main_reason}",
        ]
    )
    lines.extend(["", "## M. CI Expectations", ""])
    lines.extend(
        [
            f"- Workflow path: {result.ci_expectations.get('workflow_path')}",
            f"- Workflow exists: {result.ci_expectations.get('exists')}",
            f"- Commands present: {result.ci_expectations.get('commands_present')}",
            f"- Commands missing: {_join(result.ci_expectations.get('commands_missing', []))}",
            f"- Aligned: {result.ci_expectations.get('aligned')}",
            f"- Interpretation warning: {result.ci_expectations.get('interpretation_warning')}",
        ]
    )
    lines.extend(["", "## N. Known Blockers Preserved", ""])
    if result.known_blockers_preserved:
        lines.extend(f"- {item}" for item in result.known_blockers_preserved)
    else:
        lines.append("- No blocker preservation entries were found.")
    lines.extend(["", "## O. Missing Artefacts / Seal Gaps", ""])
    if result.missing_artefacts_or_seal_gaps:
        lines.extend(f"- {item}" for item in result.missing_artefacts_or_seal_gaps)
    else:
        lines.append("- No required artefacts or seal gaps were detected.")
    lines.extend(
        [
            "",
            "## P. What This Seal Does Not Mean",
            "",
            "- It does not mean approval.",
            "- It does not mean validation.",
            "- It does not mean external review has been completed.",
            "- It does not mean legal sufficiency.",
            "- It does not mean operational readiness.",
            "- It does not mean legislative readiness.",
            "- It does not mean official status.",
            "- It does not mean the proposal is ready for government, ATO, Treasury, Parliament, public release, implementation, or any real-world use.",
            "",
            "## Q. Suggested Next External Review Step",
            "",
            "- Pause feature work and hand the release-candidate pack, attack pack, final RC integrity seal, and reviewer-specific documents to external legal, tax, Treasury methods, ATO methods, privacy, statistical, economic, welfare, Parliamentary Counsel, technical, policy, and hostile-review reviewers.",
            "- Treat this handoff as a request for challenge, not as approval, validation, readiness, legal sufficiency, official status, or external review completion.",
        ]
    )
    markdown = "\n".join(lines).rstrip() + "\n"
    forbidden = find_forbidden_affirmative_seal_claims(markdown)
    if forbidden:
        raise ValueError(f"generated final RC integrity seal Markdown contains forbidden affirmative claims: {', '.join(forbidden)}")
    return markdown


def _digest_payload(result: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    deterministic_metadata = {key: value for key, value in metadata.items() if key != "generated_at"}
    return {
        "metadata": {
            **deterministic_metadata,
            "generated_at": "not_timestamped_for_idempotent_digest_manifest",
            "status": "digest_metadata_only_not_signature_not_approval",
            "non_claims": [
                FINAL_RC_INTEGRITY_SEAL_NON_CLAIMS[0],
                "Digests are integrity metadata only.",
                "They are not signatures.",
                "They are not legal seals.",
                "They are not external attestation.",
                "They are not approval.",
            ],
        },
        "summary": {
            "digest_targets_total": result.summary.digest_targets_total,
            "digests_written": result.summary.digests_written,
        },
        "digests": [_jsonable(item) for item in result.digest_manifest],
    }


def write_reports(reports_dir: Path, release_dir: Path, result: Any) -> tuple[Path, Path, Path, Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    release_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    payload = build_json_payload(result, metadata)
    markdown = build_markdown(result, metadata)
    digest_payload = _digest_payload(result, metadata)
    forbidden = find_forbidden_affirmative_seal_claims(json.dumps(payload, sort_keys=True))
    if forbidden:
        raise ValueError(f"generated final RC integrity seal JSON contains forbidden affirmative claims: {', '.join(forbidden)}")
    reports_json_path = reports_dir / "v1_5_final_rc_integrity_seal.json"
    reports_md_path = reports_dir / "v1_5_final_rc_integrity_seal.md"
    release_json_path = release_dir / "FINAL_RC_INTEGRITY_SEAL.json"
    release_md_path = release_dir / "FINAL_RC_INTEGRITY_SEAL.md"
    digest_path = release_dir / "FINAL_RC_DIGESTS.json"
    reports_json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    reports_md_path.write_text(markdown, encoding="utf-8")
    release_json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    release_md_path.write_text(markdown, encoding="utf-8")
    digest_path.write_text(json.dumps(digest_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return reports_json_path, reports_md_path, release_json_path, release_md_path, digest_path


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--manifest-path", type=Path, default=DEFAULT_MANIFEST_PATH)
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    parser.add_argument("--release-dir", type=Path, default=REPO_ROOT / "release" / "v1_5_rc")
    args = parser.parse_args(argv)

    result = run_final_rc_integrity_seal(args.manifest_path)
    paths = write_reports(args.reports_dir, args.release_dir, result)
    print(f"wrote {paths[0]}")
    print(f"wrote {paths[1]}")
    print(f"wrote {paths[2]}")
    print(f"wrote {paths[3]}")
    print(f"wrote {paths[4]}")
    print(f"release documents present: {result.summary.release_documents_present}")
    print(f"attack-pack documents present: {result.summary.attack_pack_documents_present}")
    print(f"generated reports present: {result.summary.generated_reports_present}")
    print(f"digests written: {result.summary.digests_written}")
    print(f"forbidden claim findings: {result.summary.forbidden_claim_findings}")
    print(f"boundary phrase failures: {result.summary.boundary_phrase_failures}")
    print(f"false flag failures: {result.summary.false_flag_failures}")
    print(f"guardrail denied findings: {result.summary.guardrail_denied_findings}")
    print(f"seal_passed: {result.summary.seal_passed}")
    print(f"review_completed: {result.summary.review_completed}")
    print(f"approval_claimed: {result.summary.approval_claimed}")
    print(f"validation_claimed: {result.summary.validation_claimed}")
    print(f"readiness_score_created: {result.summary.readiness_score_created}")
    print(f"maturity_score_created: {result.summary.maturity_score_created}")
    print(f"firm_level_liability_logic_modified: {result.summary.firm_level_liability_logic_modified}")
    if not result.summary.seal_passed:
        print("final RC integrity seal failed closed")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
