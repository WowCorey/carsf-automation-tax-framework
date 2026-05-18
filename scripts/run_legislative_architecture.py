"""Run the CARSF V1.5 non-operative legislative architecture report."""

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
from carsf.legislative_architecture import (  # noqa: E402
    LEGISLATIVE_ARCHITECTURE_NON_CLAIMS,
    LEGISLATIVE_ARCHITECTURE_WARNING,
    build_legislative_architecture_result,
    find_forbidden_affirmative_claims,
)


REPORT_STATUS = "non_operative_legislative_architecture_skeleton_only"
DEFAULT_ARCHITECTURE_PATH = REPO_ROOT / "data" / "legislative_architecture" / "legislative_architecture_skeleton.yaml"


def _jsonable(value: Any) -> Any:
    if hasattr(value, "to_jsonable"):
        return value.to_jsonable()
    if hasattr(value, "__dataclass_fields__"):
        return asdict(value)
    return value


def load_legislative_architecture(path: Path) -> dict[str, Any]:
    loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(loaded, dict):
        raise ValueError(f"legislative architecture YAML must be a mapping: {path}")
    return loaded


def run_legislative_architecture(architecture_path: Path, repo_root: Path = REPO_ROOT) -> Any:
    payload = load_legislative_architecture(architecture_path)
    return build_legislative_architecture_result(payload, repo_root)


def build_json_payload(result: Any, metadata: dict[str, Any]) -> dict[str, Any]:
    summary = result.summary
    return {
        "metadata": {
            **metadata,
            "status": REPORT_STATUS,
            "non_claims": LEGISLATIVE_ARCHITECTURE_NON_CLAIMS,
            "operative_law_created": False,
            "legal_sufficiency_claimed": False,
            "statutory_power_created": False,
            "notices_created": False,
            "penalties_created": False,
            "enforcement_created": False,
            "real_data_used": False,
            "firm_level_liability_logic_modified": False,
        },
        "summary": _jsonable(summary),
        "legislative_architecture": _jsonable(result),
    }


def _parts_table(parts: list[Any]) -> list[str]:
    lines = [
        "| Part ID | Part Title | Purpose | Linked CARSF Modules | Linked Reports | Division Count | External Review Required | Drafting Risk | Main Reason |",
        "| --- | --- | --- | --- | --- | ---: | --- | --- | --- |",
    ]
    for part in parts:
        lines.append(
            "| "
            f"{part.part_id} | {part.part_title} | {part.purpose} | "
            f"{', '.join(part.linked_carsf_modules) or 'None'} | "
            f"{', '.join(part.linked_reports) or 'None'} | {len(part.divisions)} | "
            f"{part.external_review_required} | {part.drafting_risk} | {part.main_reason} |"
        )
    return lines


def _division_table(parts: list[Any]) -> list[str]:
    lines = [
        "| Part ID | Division ID | Division Title | Conceptual Scope | Existing Layer | Placeholder Types | Legal | Tax | ATO Methods | Treasury | Privacy | Calibration |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for part in parts:
        for division in part.divisions:
            lines.append(
                "| "
                f"{part.part_id} | {division.division_id} | {division.division_title} | "
                f"{division.conceptual_scope} | {division.linked_existing_layer} | "
                f"{', '.join(division.placeholder_provision_types)} | {division.requires_legal_review} | "
                f"{division.requires_tax_review} | {division.requires_ato_methods_review} | "
                f"{division.requires_treasury_review} | {division.requires_privacy_review} | "
                f"{division.requires_external_calibration} |"
            )
    return lines


def _definition_table(definitions: list[Any]) -> list[str]:
    lines = [
        "| Term | Plain-English Description | Linked Module or Doc | Drafting Status | Legal Review Required | Tax Review Required | Policy Review Required | Must Not Be Used As Operative Definition |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in definitions:
        lines.append(
            "| "
            f"{item.term} | {item.plain_english_description} | {item.linked_module_or_doc} | "
            f"{item.drafting_status} | {item.requires_legal_review} | {item.requires_tax_review} | "
            f"{item.requires_policy_review} | {item.must_not_be_used_as_operative_definition} |"
        )
    return lines


def _schedule_table(schedules: list[Any]) -> list[str]:
    lines = [
        "| Schedule ID | Schedule Name | Source YAML | Calibration Status | Legal Attribution Status | Capital-Base Issue | Multi-Schedule Attribution Issue | External Calibration Required | Must Not Be Treated As Official Schedule |",
        "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in schedules:
        lines.append(
            "| "
            f"{item.schedule_id} | {item.schedule_name} | {item.source_yaml} | {item.calibration_status} | "
            f"{item.legal_attribution_status} | {item.capital_base_issue} | {item.multi_schedule_attribution_issue} | "
            f"{item.requires_external_calibration} | {item.must_not_be_treated_as_official_schedule} |"
        )
    return lines


def _provision_table(items: list[Any]) -> list[str]:
    lines = [
        "| Placeholder ID | Title | Type | Conceptual Scope | Key Flags | Review Requirements | Non-Claims |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in items:
        true_flags = [key for key, value in item.flags.items() if value is True]
        lines.append(
            "| "
            f"{item.placeholder_id} | {item.placeholder_title} | {item.placeholder_type} | "
            f"{item.conceptual_scope} | {', '.join(true_flags)} | "
            f"{', '.join(item.review_requirements)} | {'; '.join(item.non_claims)} |"
        )
    return lines


def _blocker_lines(blockers: list[Any]) -> list[str]:
    lines = [
        "| Blocker ID | Title | Type | Affected Parts | Required Review | Reserved for Counsel | Main Reason |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for blocker in blockers:
        lines.append(
            "| "
            f"{blocker.blocker_id} | {blocker.blocker_title} | {blocker.blocker_type} | "
            f"{', '.join(blocker.affected_parts)} | {', '.join(blocker.required_review)} | "
            f"{blocker.locked_or_reserved_for_counsel} | {blocker.main_reason} |"
        )
    return lines


def _summary_lines(summary: Any) -> list[str]:
    return [
        f"- Total Parts: {summary.total_parts}",
        f"- Total Divisions: {summary.total_divisions}",
        f"- Total definition placeholders: {summary.total_definition_placeholders}",
        f"- Total schedule placeholders: {summary.total_schedule_placeholders}",
        f"- Total regulation-making placeholders: {summary.total_regulation_making_placeholders}",
        f"- Total safeguard placeholders: {summary.total_safeguard_placeholders}",
        f"- Total evidence-power placeholders: {summary.total_evidence_power_placeholders}",
        f"- Total anti-avoidance placeholders: {summary.total_anti_avoidance_placeholders}",
        f"- Parts requiring legal review: {summary.parts_requiring_legal_review}",
        f"- Parts requiring tax review: {summary.parts_requiring_tax_review}",
        f"- Parts requiring ATO methods review: {summary.parts_requiring_ato_methods_review}",
        f"- Parts requiring Treasury review: {summary.parts_requiring_treasury_review}",
        f"- Parts requiring privacy review: {summary.parts_requiring_privacy_review}",
        f"- Parts requiring external calibration: {summary.parts_requiring_external_calibration}",
        f"- Locked or reserved for counsel areas: {summary.locked_or_reserved_for_counsel_count}",
        f"- operative_law_created: {summary.operative_law_created}",
        f"- legal_sufficiency_claimed: {summary.legal_sufficiency_claimed}",
        f"- statutory_power_created: {summary.statutory_power_created}",
        f"- notices_created: {summary.notices_created}",
        f"- penalties_created: {summary.penalties_created}",
        f"- enforcement_created: {summary.enforcement_created}",
        f"- real_data_used: {summary.real_data_used}",
        f"- firm_level_liability_logic_modified: {summary.firm_level_liability_logic_modified}",
    ]


def build_markdown(result: Any, metadata: dict[str, Any]) -> str:
    summary = result.summary
    lines = [
        "# CARSF V1.5 Legislative Architecture Skeleton",
        "",
        f"Generated at: `{metadata['generated_at']}`",
        "",
        "## A. Purpose",
        "",
        "This report maps CARSF concepts into a non-operative legislative-style architecture for external review. It is a conceptual location map only, not provision text.",
        "",
        "## B. Non-Claims",
        "",
    ]
    lines.extend(f"- {item}" for item in LEGISLATIVE_ARCHITECTURE_NON_CLAIMS)
    lines.extend(
        [
            "",
            "## C. Method - Non-Operative Architecture Only",
            "",
            "The runner loads project metadata, validates non-operative flags, checks linked schedule and report references, checks required definition placeholders, and confirms that sensitive areas remain reserved for external legal, tax, Treasury, ATO, Parliamentary Counsel, privacy, calibration, administrative-design, and policy review.",
            "",
            "## D. Architecture Overview",
            "",
        ]
    )
    lines.extend(_summary_lines(summary))
    lines.extend(["", "## E. Proposed Parts", ""])
    lines.extend(_parts_table(result.parts))
    lines.extend(["", "## F. Proposed Divisions", ""])
    lines.extend(_division_table(result.parts))
    lines.extend(["", "## G. Definition Placeholders", ""])
    lines.extend(_definition_table(result.definitions))
    lines.extend(["", "## H. Sector Schedule Placeholders", ""])
    lines.extend(_schedule_table(result.schedules))
    lines.extend(["", "## I. Formula / Liability Placeholder Map", ""])
    formula_parts = [part for part in result.parts if part.part_id in {"part_02", "part_03", "part_07", "part_08", "part_09"}]
    lines.extend(_parts_table(formula_parts))
    lines.extend(["", "## J. Safe Harbour Placeholder Map", ""])
    lines.extend(_parts_table([part for part in result.parts if part.part_id == "part_10"]))
    lines.extend(["", "## K. Anti-Avoidance and Integrity Placeholder Map", ""])
    lines.extend(_provision_table(result.anti_avoidance_placeholders))
    lines.extend(["", "## L. Grouped Entity / Related Party Placeholder Map", ""])
    lines.extend(_parts_table([part for part in result.parts if part.part_id in {"part_12", "part_13"}]))
    lines.extend(["", "## M. Evidence and Information Architecture Placeholders", ""])
    lines.extend(_provision_table(result.evidence_power_placeholders))
    lines.extend(["", "## N. Review Rights and Safeguards Placeholders", ""])
    lines.extend(_provision_table(result.safeguards))
    lines.extend(["", "## O. Privacy / Secrecy / Data Handling Placeholders", ""])
    lines.extend(_parts_table([part for part in result.parts if part.part_id == "part_16"]))
    lines.extend(["", "## P. Regulation-Making Placeholders", ""])
    lines.extend(_provision_table(result.regulation_making_placeholders))
    lines.extend(["", "## Q. Commencement and Transitional Placeholders", ""])
    lines.extend(_provision_table(result.commencement_transition_placeholders))
    lines.extend(["", "## R. External Review Blockers", ""])
    lines.extend(_blocker_lines(result.external_review_blockers))
    lines.extend(["", "## S. Locked / Reserved for Counsel Areas", ""])
    for area in result.locked_or_reserved_for_counsel_areas:
        lines.append(f"- {area}")
    lines.extend(
        [
            "",
            "## T. Plain-English Interpretation",
            "",
            "The skeleton shows where CARSF concepts might be located in a future legal architecture, while deliberately locking operative definitions, liability architecture, evidence powers, anti-avoidance rules, review rights, regulation-making mechanisms, commencement, and transitional rules for external drafting review.",
            "",
            "Stable report generation does not mean legal readiness. The result remains a policy-review map only and does not change the Python formula model or any firm-level liability output.",
            "",
            "## U. Limitations and Future Review Needs",
            "",
            "- Non-operative only.",
            "- Not a Bill.",
            "- Not legal drafting.",
            "- Not legal advice or tax advice.",
            "- Not ATO guidance or Treasury modelling.",
            "- Not Parliamentary Counsel drafting.",
            "- Not constitutionally reviewed.",
            "- Creates no rights, obligations, powers, notices, penalties, enforcement process, or compliance scoring.",
            "- Does not determine tax payable.",
            "- Uses no taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.",
            "- Does not modify firm-level CARSF liability logic.",
            "- Requires external legal, tax, Treasury, ATO, Parliamentary Counsel, privacy, calibration, administrative-design, and policy review before any real use.",
        ]
    )
    markdown = "\n".join(lines).rstrip() + "\n"
    forbidden = find_forbidden_affirmative_claims(markdown)
    if forbidden:
        raise ValueError(f"generated legislative architecture report contains forbidden affirmative claims: {', '.join(forbidden)}")
    return markdown


def write_reports(reports_dir: Path, result: Any) -> tuple[Path, Path]:
    reports_dir.mkdir(parents=True, exist_ok=True)
    metadata = report_metadata()
    json_path = reports_dir / "legislative_architecture.json"
    md_path = reports_dir / "legislative_architecture.md"
    payload = build_json_payload(result, metadata)
    markdown = build_markdown(result, metadata)
    forbidden = find_forbidden_affirmative_claims(json.dumps(payload, sort_keys=True))
    if forbidden:
        raise ValueError(f"generated legislative architecture JSON contains forbidden affirmative claims: {', '.join(forbidden)}")
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(markdown, encoding="utf-8")
    return json_path, md_path


def main(argv: list[str] | None = None) -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--architecture-path", type=Path, default=DEFAULT_ARCHITECTURE_PATH)
    parser.add_argument("--reports-dir", type=Path, default=REPO_ROOT / "reports")
    args = parser.parse_args(argv)

    result = run_legislative_architecture(args.architecture_path)
    json_path, md_path = write_reports(args.reports_dir, result)
    print(f"validated {result.summary.total_parts} legislative architecture Parts")
    print(f"wrote {json_path}")
    print(f"wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
