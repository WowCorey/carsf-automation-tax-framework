from __future__ import annotations

import json
from pathlib import Path

import streamlit as st


REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_PATH = REPO_ROOT / "reports" / "public_data_evidence_map.json"
CONSISTENCY_AUDIT_PATH = REPO_ROOT / "reports" / "public_data_consistency_audit.json"
SOURCE_LOCATOR_PACK_PATH = REPO_ROOT / "reports" / "source_locator_verification_pack.json"
RED_TEAM_OBJECTIONS_PATH = REPO_ROOT / "reports" / "red_team_reviewer_objections.json"
PUBLIC_REAL_DATA_LOADER_PATH = REPO_ROOT / "reports" / "public_real_data_loader.json"
PLACEHOLDER_REPLACEMENT_MAP_PATH = REPO_ROOT / "reports" / "public_data_placeholder_replacement_map.json"
WARNING = (
    "This is a reviewer evidence map and dashboard for the public data pilot only. No new data is loaded by this build. "
    "Build 27 public aggregate extracts remain sanity-check-only or placeholder-anchor-only. This is not calibration, "
    "calibration has not been completed, public data does not prove the model works, realistic placeholders remain placeholders, "
    "source references are not loaded datasets, and restricted-data requirements are not data access. It is not validation, "
    "not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, "
    "not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, and not official status. "
    "It does not determine actual tax payable and does not modify firm-level CARSF liability."
)


def load_report(path: Path) -> dict:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def rows(items: list[dict], keys: list[str]) -> list[dict]:
    return [{key: item.get(key) for key in keys} for item in items]


def rows_with_lists(items: list[dict], keys: list[str]) -> list[dict]:
    output = []
    for item in items:
        row = {}
        for key in keys:
            value = item.get(key)
            row[key] = ", ".join(value) if isinstance(value, list) else value
        output.append(row)
    return output


st.set_page_config(page_title="CARSF Public Data Evidence Map", layout="wide")
st.title("Public Data Evidence Map")
st.caption("Reviewer-facing map for existing Build 27 public-data pilot artefacts.")
st.warning(WARNING)
st.error("No readiness score, calibration score, validation score, approval, official-status claim, or tax-payable result is created.")

report = load_report(REPORT_PATH)
if not report:
    st.info("Run `python scripts/run_public_data_evidence_map.py` to generate the evidence-map report.")
    st.stop()
    raise SystemExit(0)
audit_report = load_report(CONSISTENCY_AUDIT_PATH)
source_locator_report = load_report(SOURCE_LOCATOR_PACK_PATH)
red_team_report = load_report(RED_TEAM_OBJECTIONS_PATH)
public_real_report = load_report(PUBLIC_REAL_DATA_LOADER_PATH)
placeholder_replacement_report = load_report(PLACEHOLDER_REPLACEMENT_MAP_PATH)

metadata = report.get("metadata", {})
payload = report.get("public_data_evidence_map", {})
summary = report.get("summary", {})

st.markdown("### Summary")
st.table(
    [
        {"Metric": key, "Value": str(value)}
        for key, value in summary.items()
        if isinstance(value, (int, bool, str))
    ]
)

st.markdown("### Evidence Status Explanation")
st.table([{"Evidence Status": value} for value in metadata.get("evidence_status_values", [])])

st.markdown("### Confidence Labels")
st.caption("Confidence labels classify evidence type only. They are not validation, readiness, or maturity scores.")
st.table([{"Confidence Label": value} for value in metadata.get("confidence_label_values", [])])

st.markdown("### Source References")
st.table(
    rows_with_lists(
        payload.get("source_evidence", []),
        ["source_reference_id", "publisher", "source_kind", "source_url", "evidence_status", "confidence_label", "linked_extract_ids"],
    )
)

st.markdown("### Loaded Public Extracts")
st.table(
    rows_with_lists(
        payload.get("loaded_extract_evidence", []),
        ["extract_id", "evidence_status", "confidence_label", "values_summary", "source_locator", "value_review_status", "reviewer_interpretation"],
    )
)

st.markdown("### Source-Reference-Only Records")
st.table(
    rows_with_lists(
        payload.get("source_reference_only_evidence", []),
        ["extract_id", "evidence_status", "confidence_label", "source_locator", "value_review_status", "reviewer_interpretation"],
    )
)

st.markdown("### Realistic Placeholder Anchors")
st.table(
    rows_with_lists(
        payload.get("placeholder_evidence", []),
        ["anchor_id", "field_id", "anchored_to_public_data", "anchor_strength", "confidence_label", "blocked_by_restricted_data"],
    )
)

st.markdown("### Field Sanity Checks")
st.table(
    rows_with_lists(
        payload.get("field_sanity_evidence", []),
        ["check_id", "field_id", "check_status", "evidence_status", "confidence_label", "linked_extract_ids", "linked_anchor_ids"],
    )
)

st.markdown("### Module Sanity Checks")
st.table(
    rows_with_lists(
        payload.get("module_sanity_evidence", []),
        ["module_id", "result_status", "sanity_check_possible", "calibration_possible", "evidence_status", "confidence_label", "main_blockers"],
    )
)

st.markdown("### Restricted Blockers")
st.table(
    rows_with_lists(
        payload.get("restricted_blocker_evidence", []),
        ["blocker_id", "description", "evidence_status", "confidence_label", "affected_modules", "required_access_or_review"],
    )
)

st.markdown("### Forbidden Repo Data")
st.table(
    rows(
        payload.get("forbidden_repo_data_evidence", []),
        ["blocker_id", "description", "evidence_status", "confidence_label"],
    )
)

st.markdown("### Reviewer Questions")
st.table(
    rows_with_lists(
        payload.get("reviewer_questions", []),
        ["category", "question", "reviewer_interpretation", "target_evidence_status", "must_not_infer"],
    )
)

st.markdown("### What Cannot Be Claimed")
for item in metadata.get("non_claims", [WARNING]):
    st.markdown(f"- {item}")

st.markdown("### Consistency Audit / Source Reconciliation")
st.caption(
    "Internal consistency audit only. Reconciled means internally consistent only; it is not external source verification, "
    "calibration, validation, legal sufficiency, operational readiness, official status, or actual tax-payable evidence."
)
if audit_report:
    audit_payload = audit_report.get("public_data_consistency_audit", {})
    audit_summary = audit_report.get("summary", {})
    st.table(
        [
            {"Metric": key, "Value": str(value)}
            for key, value in audit_summary.items()
            if key
            in {
                "total_audit_findings",
                "findings_reconciled",
                "findings_warning",
                "findings_blocked",
                "findings_fail_closed",
                "source_references_total",
                "loaded_public_extracts_total",
                "source_reference_only_extracts_total",
                "digest_self_hash_findings",
                "forbidden_claim_findings",
                "non_claim_boundary_failures",
                "new_data_loaded",
                "external_source_verification_claimed",
                "real_calibration_completed",
                "actual_tax_payable_determined",
                "validation_claimed",
                "approval_claimed",
                "operational_readiness_claimed",
                "legal_sufficiency_claimed",
                "official_status_claimed",
                "firm_level_liability_logic_modified",
            }
        ]
    )
    st.markdown("#### Audit Findings")
    st.table(
        rows_with_lists(
            audit_payload.get("findings", []),
            [
                "finding_id",
                "audit_type",
                "audit_status",
                "reconciliation_scope",
                "what_was_checked",
                "what_failed",
                "what_reviewer_should_inspect_next",
            ],
        )
    )
else:
    st.info("Run `python scripts/run_public_data_consistency_audit.py` to generate the optional consistency-audit section.")

st.markdown("### Source-Locator Verification Pack")
st.caption(
    "Manual-review pack only. Ready for manual review means locator metadata is present; it does not mean reviewed, "
    "externally checked, calibrated, validated, official, legally sufficient, operationally ready, or tax-payable evidence."
)
if source_locator_report:
    locator_payload = source_locator_report.get("source_locator_verification_pack", {})
    locator_summary = source_locator_report.get("summary", {})
    st.table(
        [
            {"Metric": key, "Value": str(value)}
            for key, value in locator_summary.items()
            if key
            in {
                "total_loaded_value_cards",
                "complete_locator_cards",
                "partial_locator_cards",
                "source_reference_only_cards",
                "placeholder_anchor_cards",
                "restricted_blocker_cards",
                "reviewer_checklist_items_total",
                "fair_work_arithmetic_cards",
                "cards_ready_for_manual_review",
                "cards_source_locator_recorded_only",
                "cards_source_reference_only_not_loaded",
                "cards_placeholder_not_real_data",
                "cards_blocked_until_authorised_access",
                "forbidden_claim_findings",
                "new_data_loaded",
                "external_source_verification_claimed",
                "manual_review_pack_only",
                "real_calibration_completed",
                "actual_tax_payable_determined",
                "validation_claimed",
                "approval_claimed",
                "operational_readiness_claimed",
                "legal_sufficiency_claimed",
                "official_status_claimed",
                "firm_level_liability_logic_modified",
            }
        ]
    )
    st.markdown("#### Loaded Value Cards")
    st.table(
        rows_with_lists(
            locator_payload.get("loaded_value_cards", []),
            [
                "card_id",
                "extract_id",
                "publisher",
                "locator_status",
                "verification_status",
                "values_summary",
                "source_locator",
                "arithmetic_check_summary",
                "reviewer_must_not_infer",
            ],
        )
    )
    st.markdown("#### Source-Reference-Only Cards")
    st.table(
        rows_with_lists(
            locator_payload.get("source_reference_only_cards", []),
            ["card_id", "extract_id", "publisher", "locator_status", "verification_status", "why_not_loaded"],
        )
    )
    st.markdown("#### Placeholder Anchor Cards")
    st.table(
        rows_with_lists(
            locator_payload.get("placeholder_anchor_cards", []),
            ["card_id", "anchor_id", "field_id", "anchor_strength", "verification_status", "reviewer_must_not_infer"],
        )
    )
    st.markdown("#### Restricted Blocker Cards")
    st.table(
        rows_with_lists(
            locator_payload.get("restricted_blocker_cards", []),
            ["card_id", "blocker_id", "blocker_type", "locator_status", "verification_status", "description"],
        )
    )
else:
    st.info("Run `python scripts/run_source_locator_verification_pack.py` to generate the optional source-locator section.")

st.markdown("### Red-Team Reviewer Objections")
st.caption(
    "Objections pack only. Acknowledging an objection does not mean it is resolved, and partially mitigated does not mean solved. "
    "This section does not load data, complete calibration, validate CARSF, create legal sufficiency, or determine tax payable."
)
if red_team_report:
    red_payload = red_team_report.get("red_team_reviewer_objections", {})
    red_summary = red_team_report.get("summary", {})
    st.table(
        [
            {"Metric": key, "Value": str(value)}
            for key, value in red_summary.items()
            if key
            in {
                "total_objections",
                "critical_objections",
                "high_objections",
                "medium_objections",
                "categories_covered",
                "unresolved_blockers_total",
                "future_evidence_needs_total",
                "forbidden_claim_findings",
                "new_data_loaded",
                "external_source_verification_claimed",
                "objections_acknowledged",
                "unresolved_blockers_visible",
                "calibration_limitations_visible",
                "legal_limitations_visible",
                "statistical_limitations_visible",
                "dashboard_misinterpretation_risks_visible",
                "real_calibration_completed",
                "actual_tax_payable_determined",
                "validation_claimed",
                "approval_claimed",
                "operational_readiness_claimed",
                "legal_sufficiency_claimed",
                "official_status_claimed",
                "firm_level_liability_logic_modified",
            }
        ]
    )
    objection_rows = red_payload.get("objections", [])
    st.markdown("#### Critical And High Objections")
    st.table(
        rows_with_lists(
            [item for item in objection_rows if item.get("severity") in {"critical", "high"}],
            [
                "objection_id",
                "severity",
                "status",
                "objection_category",
                "objection_title",
                "why_the_concern_is_valid",
                "current_project_response",
                "unresolved_blockers",
            ],
        )
    )
    st.markdown("#### Category Coverage")
    st.table(rows(red_payload.get("category_summaries", []), ["objection_category", "count"]))
    st.markdown("#### Unresolved Blockers")
    st.table(rows_with_lists(red_payload.get("unresolved_blockers", []), ["blocker", "affected_objection_ids"]))
    st.markdown("#### What The Project Can Say")
    st.table(rows_with_lists(red_payload.get("responses", []), ["objection_id", "can_say"]))
    st.markdown("#### What The Project Must Not Claim")
    st.table(rows_with_lists(red_payload.get("responses", []), ["objection_id", "must_not_claim"]))
else:
    st.info("Run `python scripts/run_red_team_reviewer_objections.py` to generate the optional red-team objections section.")

st.markdown("### Real Public Aggregate Data Loader")
st.caption(
    "Controlled public aggregate loader only. Loaded public aggregate data does not equal calibration, validation, "
    "legal advice, tax advice, ATO guidance, Treasury modelling, PBO costing, operational readiness, legal sufficiency, "
    "official status, actual tax payable, or firm-level CARSF liability logic."
)
if public_real_report:
    real_payload = public_real_report.get("public_real_data_loader", {})
    real_summary = public_real_report.get("summary", {})
    st.table(
        [
            {"Metric": key, "Value": str(value)}
            for key, value in real_summary.items()
            if key
            in {
                "loaded_sources",
                "source_candidates_not_loaded",
                "loaded_values_total",
                "new_public_aggregate_values_loaded",
                "guardrail_fail_closed_findings",
                "real_public_aggregate_data_loaded",
                "restricted_data_loaded",
                "personal_data_loaded",
                "taxpayer_level_data_loaded",
                "firm_confidential_data_loaded",
                "household_microdata_loaded",
                "calibration_completed",
                "validation_claimed",
                "actual_tax_payable_determined",
                "official_status_claimed",
                "firm_level_liability_logic_modified",
            }
        ]
    )
    st.markdown("#### Loaded Public Aggregate Values")
    st.table(
        rows_with_lists(
            real_payload.get("loaded_public_aggregate_values", []),
            [
                "value_id",
                "source_id",
                "metric_name",
                "value",
                "unit",
                "period",
                "geography",
                "value_review_status",
                "must_not_infer",
            ],
        )
    )
    st.markdown("#### Source Candidates Not Loaded")
    st.table(
        rows_with_lists(
            real_payload.get("source_candidates_not_loaded", []),
            ["source_id", "publisher", "source_name", "loaded_status", "reason_if_not_loaded", "must_not_infer"],
        )
    )
    st.markdown("#### Public Real Data Guardrails")
    st.table(rows(real_payload.get("guardrail_findings", []), ["finding_id", "guardrail", "status", "finding"]))
else:
    st.info("Run `python scripts/run_public_real_data_loader.py` to generate the optional public-real-data loader section.")

st.markdown("### Public Data Placeholder Replacement Map")
st.caption(
    "Placeholder replacement map only. No new data is loaded. Public aggregate anchors can replace, narrow, or inform "
    "some placeholders, but this is not calibration, validation, legal advice, tax advice, ATO guidance, Treasury "
    "modelling, PBO costing, operational readiness, legal sufficiency, official status, actual tax payable, or "
    "firm-level CARSF liability logic."
)
if placeholder_replacement_report:
    replacement_payload = placeholder_replacement_report.get("public_data_placeholder_replacement_map", {})
    replacement_summary = placeholder_replacement_report.get("summary", {})
    st.table(
        [
            {"Metric": key, "Value": str(value)}
            for key, value in replacement_summary.items()
            if key
            in {
                "placeholder_replacement_map_created",
                "new_data_loaded",
                "loaded_public_values_used",
                "placeholders_mapped",
                "placeholders_replaced_by_public_anchor",
                "placeholders_narrowed_by_public_anchor",
                "placeholders_informed_by_public_anchor",
                "placeholders_still_placeholder_only",
                "placeholders_blocked_until_restricted_data",
                "placeholders_blocked_until_external_review",
                "placeholders_cannot_replace_with_public_aggregate_data",
                "public_source_candidates_treated_as_loaded",
                "restricted_data_loaded",
                "personal_data_loaded",
                "taxpayer_level_data_loaded",
                "firm_confidential_data_loaded",
                "household_microdata_loaded",
                "calibration_completed",
                "validation_claimed",
                "actual_tax_payable_determined",
                "official_status_claimed",
                "firm_level_liability_logic_modified",
            }
        ]
    )
    st.markdown("#### Replacement Decisions")
    st.table(
        rows_with_lists(
            replacement_payload.get("replacement_decisions", []),
            [
                "placeholder_id",
                "field_id",
                "replacement_status",
                "replacement_confidence",
                "claim_level",
                "linked_public_value_ids",
                "what_changed",
                "what_did_not_change",
                "remaining_blockers",
            ],
        )
    )
    st.markdown("#### Source Candidates Not Loaded")
    st.table(
        rows(
            replacement_payload.get("source_candidates_not_loaded", []),
            ["source_id", "publisher", "source_name", "loaded_status", "treated_as_loaded"],
        )
    )
else:
    st.info("Run `python scripts/run_public_data_placeholder_replacement_map.py` to generate the optional placeholder replacement map section.")
