# CARSF V1.5 Public Data Pilot Consistency Audit & Source Reconciliation

Generated at: `2026-05-20T07:07:47+00:00`

## A. Purpose

This report audits internal consistency across existing Build 27 and Build 28 public-data pilot artefacts without loading new data.

## B. Non-Claims

- This is an internal consistency audit and source-reconciliation map only. No new data is loaded by this build. This does not externally verify source values, does not scrape public sources, and does not call external APIs. This is not calibration; calibration has not been completed. Public data does not prove the model works. Reconciled means internally consistent only; reconciled does not mean validated, official, or ready. Realistic placeholders remain placeholders, realistic placeholders are not real data, realistic placeholders are not calibrated, source references are not loaded datasets, and restricted-data requirements are not data access. This is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, and not official status. It does not determine actual tax payable, does not use taxpayer-level data, firm-level confidential data, household microdata, ABS DataLab, HILDA microdata, DSS/Services Australia records, ATO taxpayer records, Treasury/PBO confidential material, or restricted government data, and does not modify firm-level CARSF liability. It only checks internal consistency across source records, extracts, reports, digests, dashboard source, and non-claim boundaries.
- Audit statuses are internal consistency statuses only; they are not validation, approval, calibration, readiness, or official status.
- Source locators and value notes are metadata for reviewer inspection only and do not mean external source verification has occurred.
- Digest checks are repository integrity metadata only and are not signatures, external attestation, approval, validation, or calibration.

## C. Audit Method

- Reconcile source references, loaded extracts, source-reference-only rows, placeholder anchors, field checks, module checks, digests, generated reports, and dashboard source.
- Treat `reconciled` as internal consistency only, not external source verification.
- Raise fail-closed if required boundaries or count agreements break.

## D. Audit Status Taxonomy

- `blocked`
- `fail_closed`
- `not_applicable`
- `reconciled`
- `warning`

## E. Source Reference To Extract Audit

| Finding ID | Audit Type | Status | Scope | Checked | Passed | Failed | Reviewer Next Step | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source_reference_to_extract | source_reference_to_extract | reconciled | source_locator_metadata_only | Every extract source reference and loaded-extract source metadata field. | All extract source_reference_id values are present and loaded extracts carry source locator metadata. | None | Inspect source locators and value review status text before relying on any row as a review input. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |

## F. Loaded Extract To Evidence Map Audit

| Finding ID | Audit Type | Status | Scope | Checked | Passed | Failed | Reviewer Next Step | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| extract_to_evidence_map | extract_to_evidence_map | reconciled | internal_repo_only | Loaded and source-reference-only extract rows against evidence-map rows. | Loaded extracts map to loaded public aggregate evidence and source-reference-only rows remain separate. | None | Inspect the evidence-map JSON before presenting loaded-public-extract counts. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |

## G. Source-Reference-Only Count Audit

| Finding ID | Audit Type | Status | Scope | Checked | Passed | Failed | Reviewer Next Step | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source_reference_only_counting | source_reference_only_counting | reconciled | count_consistency_only | Source counts against pilot JSON and evidence-map JSON summary counts. | Source-reference-only rows are excluded from loaded public data counts and JSON counts agree. | None | Inspect generated summaries whenever source files or report JSONs change. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |

## H. Fair Work Wage Arithmetic Audit

| Finding ID | Audit Type | Status | Scope | Checked | Passed | Failed | Reviewer Next Step | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fair_work_wage_arithmetic | arithmetic_consistency | reconciled | arithmetic_only | Fair Work hourly and weekly national minimum wage values in the loaded public extract. | 24.95 * 38 = 948.10, matching the weekly value. | None | Inspect the source locator and arithmetic if either wage value changes. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |
- Fair Work arithmetic: 24.95 * 38 = 948.10; stored weekly value 948.10.

## I. Placeholder Boundary Audit

| Finding ID | Audit Type | Status | Scope | Checked | Passed | Failed | Reviewer Next Step | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| placeholder_boundary | placeholder_boundary | reconciled | boundary_consistency_only | Placeholder source rows and evidence rows for real-data or calibration overread. | All placeholder anchors remain realistic placeholders and are not labelled loaded public data. | None | Inspect placeholder evidence rows before using any anchor in a later calibration design. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |

## J. Module Calibration Boundary Audit

| Finding ID | Audit Type | Status | Scope | Checked | Passed | Failed | Reviewer Next Step | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| module_calibration_boundary | module_calibration_boundary | reconciled | boundary_consistency_only | Module sanity-check rows and evidence rows for calibration_possible false and blocker visibility. | Every module sanity-check row keeps calibration_possible false and preserves blockers. | None | Inspect module rows before using public-pilot evidence as calibration input. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |

## K. Restricted Blocker Preservation Audit

| Finding ID | Audit Type | Status | Scope | Checked | Passed | Failed | Reviewer Next Step | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| restricted_blocker_preservation | restricted_blocker_preservation | reconciled | boundary_consistency_only | Restricted-data blocker IDs and evidence-map blocker rows. | Restricted tax, household microdata, and welfare/payment blockers remain visible and blocked. | None | Inspect blocker rows before planning any future data access process. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |

## L. Forbidden Repo Data Preservation Audit

| Finding ID | Audit Type | Status | Scope | Checked | Passed | Failed | Reviewer Next Step | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| forbidden_repo_data_preservation | forbidden_repo_data_preservation | reconciled | boundary_consistency_only | Forbidden repo data rules and evidence-map forbidden rows. | Forbidden categories remain excluded and marked forbidden for repo use. | None | Inspect forbidden data rules before adding any public-pilot file type. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |

## M. Digest Consistency Audit

| Finding ID | Audit Type | Status | Scope | Checked | Passed | Failed | Reviewer Next Step | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| digest_consistency | digest_consistency | reconciled | internal_repo_only | Public-pilot digest entries, target paths, sha256 fields, and self-hash exclusion. | Digest entries include sha256, target files exist, and the digest file does not hash itself. | None | Inspect digest entries after regenerating public-pilot reports. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |

## N. Report / JSON Consistency Audit

| Finding ID | Audit Type | Status | Scope | Checked | Passed | Failed | Reviewer Next Step | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| report_json_consistency | report_json_consistency | reconciled | internal_repo_only | Public-pilot and evidence-map JSON flags plus Markdown non-claim language. | JSON false flags remain false and Markdown reports retain non-claim warnings. | None | Inspect generated report JSON and Markdown together after any runner change. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |

## O. Dashboard Source Consistency Audit

| Finding ID | Audit Type | Status | Scope | Checked | Passed | Failed | Reviewer Next Step | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| dashboard_source_consistency | dashboard_source_consistency | reconciled | internal_repo_only | Streamlit evidence-map page source for report source, external-source reads, and score-like widgets. | Dashboard reads generated evidence-map JSON, does not read external sources, and does not create score-style metrics. | None | Inspect the Streamlit page whenever evidence-map or audit sections are changed. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |

## P. Non-Claim Boundary Audit

| Finding ID | Audit Type | Status | Scope | Checked | Passed | Failed | Reviewer Next Step | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| non_claim_boundary | non_claim_boundary | reconciled | boundary_consistency_only | Required non-claim phrases across generated public-data reports and dashboard text. | Required non-claim boundaries remain visible. | None | Inspect non-claim language before reviewer handoff. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |

## Q. Forbidden Claim Scan

| Finding ID | Audit Type | Status | Scope | Checked | Passed | Failed | Reviewer Next Step | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| forbidden_claim_scan | forbidden_claim_scan | reconciled | boundary_consistency_only | Generated reports, manifest text, and dashboard source for forbidden affirmative public-data claims. | No forbidden affirmative claims were found. | None | Inspect any finding manually for negative-warning context before changing the scanner. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |

## R. Audit Findings

| Finding ID | Audit Type | Status | Scope | Checked | Passed | Failed | Reviewer Next Step | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source_reference_to_extract | source_reference_to_extract | reconciled | source_locator_metadata_only | Every extract source reference and loaded-extract source metadata field. | All extract source_reference_id values are present and loaded extracts carry source locator metadata. | None | Inspect source locators and value review status text before relying on any row as a review input. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |
| extract_to_evidence_map | extract_to_evidence_map | reconciled | internal_repo_only | Loaded and source-reference-only extract rows against evidence-map rows. | Loaded extracts map to loaded public aggregate evidence and source-reference-only rows remain separate. | None | Inspect the evidence-map JSON before presenting loaded-public-extract counts. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |
| source_reference_only_counting | source_reference_only_counting | reconciled | count_consistency_only | Source counts against pilot JSON and evidence-map JSON summary counts. | Source-reference-only rows are excluded from loaded public data counts and JSON counts agree. | None | Inspect generated summaries whenever source files or report JSONs change. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |
| fair_work_wage_arithmetic | arithmetic_consistency | reconciled | arithmetic_only | Fair Work hourly and weekly national minimum wage values in the loaded public extract. | 24.95 * 38 = 948.10, matching the weekly value. | None | Inspect the source locator and arithmetic if either wage value changes. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |
| placeholder_boundary | placeholder_boundary | reconciled | boundary_consistency_only | Placeholder source rows and evidence rows for real-data or calibration overread. | All placeholder anchors remain realistic placeholders and are not labelled loaded public data. | None | Inspect placeholder evidence rows before using any anchor in a later calibration design. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |
| module_calibration_boundary | module_calibration_boundary | reconciled | boundary_consistency_only | Module sanity-check rows and evidence rows for calibration_possible false and blocker visibility. | Every module sanity-check row keeps calibration_possible false and preserves blockers. | None | Inspect module rows before using public-pilot evidence as calibration input. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |
| restricted_blocker_preservation | restricted_blocker_preservation | reconciled | boundary_consistency_only | Restricted-data blocker IDs and evidence-map blocker rows. | Restricted tax, household microdata, and welfare/payment blockers remain visible and blocked. | None | Inspect blocker rows before planning any future data access process. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |
| forbidden_repo_data_preservation | forbidden_repo_data_preservation | reconciled | boundary_consistency_only | Forbidden repo data rules and evidence-map forbidden rows. | Forbidden categories remain excluded and marked forbidden for repo use. | None | Inspect forbidden data rules before adding any public-pilot file type. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |
| digest_consistency | digest_consistency | reconciled | internal_repo_only | Public-pilot digest entries, target paths, sha256 fields, and self-hash exclusion. | Digest entries include sha256, target files exist, and the digest file does not hash itself. | None | Inspect digest entries after regenerating public-pilot reports. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |
| report_json_consistency | report_json_consistency | reconciled | internal_repo_only | Public-pilot and evidence-map JSON flags plus Markdown non-claim language. | JSON false flags remain false and Markdown reports retain non-claim warnings. | None | Inspect generated report JSON and Markdown together after any runner change. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |
| dashboard_source_consistency | dashboard_source_consistency | reconciled | internal_repo_only | Streamlit evidence-map page source for report source, external-source reads, and score-like widgets. | Dashboard reads generated evidence-map JSON, does not read external sources, and does not create score-style metrics. | None | Inspect the Streamlit page whenever evidence-map or audit sections are changed. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |
| non_claim_boundary | non_claim_boundary | reconciled | boundary_consistency_only | Required non-claim phrases across generated public-data reports and dashboard text. | Required non-claim boundaries remain visible. | None | Inspect non-claim language before reviewer handoff. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |
| forbidden_claim_scan | forbidden_claim_scan | reconciled | boundary_consistency_only | Generated reports, manifest text, and dashboard source for forbidden affirmative public-data claims. | No forbidden affirmative claims were found. | None | Inspect any finding manually for negative-warning context before changing the scanner. | must_not_infer: external_source_verification, calibration, validation, actual_tax_payable, legal_sufficiency, operational_readiness, official_status |

## S. Reconciliation Summary

- Total audit findings: 13
- Findings reconciled: 13
- Findings warning: 0
- Findings blocked: 0
- Findings not applicable: 0
- Findings fail closed: 0
- Source references total: 8
- Loaded public extracts total: 5
- Source-reference-only extracts total: 3
- Placeholder anchors total: 11
- Field sanity checks total: 10
- Module sanity checks total: 11
- Restricted blockers total: 3
- Forbidden repo data items total: 5
- Digest targets total: 5
- Digest self-hash findings: 0
- Forbidden claim findings: 0
- Non-claim boundary failures: 0
- consistency_audit_created: True
- new_data_loaded: False
- external_source_verification_claimed: False
- source_references_reconciled: True
- extract_evidence_reconciled: True
- source_reference_only_counts_reconciled: True
- arithmetic_checks_reconciled: True
- placeholder_boundaries_preserved: True
- module_calibration_boundaries_preserved: True
- restricted_blockers_preserved: True
- forbidden_repo_data_preserved: True
- digest_consistency_checked: True
- report_json_consistency_checked: True
- dashboard_source_consistency_checked: True
- real_calibration_completed: False
- actual_tax_payable_determined: False
- validation_claimed: False
- approval_claimed: False
- operational_readiness_claimed: False
- legal_sufficiency_claimed: False
- official_status_claimed: False
- firm_level_liability_logic_modified: False

## T. What This Audit Does Not Mean

- It does not mean external source verification has occurred.
- It is not calibration, validation, legal advice, tax advice, ATO guidance, Treasury modelling, PBO costing, legal sufficiency, operational readiness, or official status.
- It does not determine actual tax payable and does not modify firm-level CARSF liability.

## U. Build 30 Readiness

- Package the feasibility map, public-data pilot, evidence map, and consistency audit into a concise reviewer handoff bundle.
- Do not add new data, source values, scraping, API calls, external source verification claims, calibration claims, validation claims, tax-payable claims, or official-status claims.
- Preserve source-reference-only, placeholder, restricted-blocker, and forbidden-repo-data boundaries.

## V. Limitations and Future Work

Build 30 can package the feasibility map, public-data pilot, evidence map, and consistency audit into a reviewer handoff bundle without adding data or claiming calibration.
