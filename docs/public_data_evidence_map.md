# CARSF V1.5 Public Data Pilot Reviewer Evidence Map

This is a reviewer evidence map and dashboard for the public data pilot only. No new data is loaded by this build. Build 27 public aggregate extracts remain sanity-check-only or placeholder-anchor-only.

It is not calibration. Calibration has not been completed. Public data does not prove the model works. Realistic placeholders remain placeholders. Realistic placeholders are not real data and are not calibrated. Source references are not loaded datasets. Restricted-data requirements are not data access.

It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, and not official status. It does not determine actual tax payable, does not use taxpayer-level data, firm-level confidential data, household microdata, ABS DataLab, HILDA microdata, DSS/Services Australia records, ATO taxpayer records, Treasury/PBO confidential material, or restricted government data, and does not modify firm-level CARSF liability.

## What It Maps

- Source references from the Build 27 public-data pilot.
- Loaded public aggregate extract evidence rows.
- Source-reference-only evidence rows.
- Realistic placeholder anchor evidence rows.
- Field sanity-check evidence rows.
- Module sanity-check evidence rows.
- Restricted-data blocker rows.
- Forbidden repo data rows.
- Reviewer questions grouped by source verification, arithmetic, placeholders, blockers, field checks, module checks, non-claim boundary, external review route, and Build 29 readiness.

## Confidence Labels

Confidence labels are evidence classification labels only. They are not validation scores, not readiness scores, not maturity scores, and not approval.

- `source_locator_recorded`
- `arithmetic_checked`
- `source_reference_only`
- `placeholder_anchor_only`
- `blocked_until_restricted_data_access`
- `external_review_required`

## Commands

```bash
python scripts/run_public_data_pilot.py
python scripts/run_public_data_evidence_map.py
python scripts/run_public_data_consistency_audit.py
```

Generated reports:

- `reports/public_data_evidence_map.md`
- `reports/public_data_evidence_map.json`
- `reports/public_data_consistency_audit.md`
- `reports/public_data_consistency_audit.json`

Streamlit page:

- `simulator/pages/29_Public_Data_Evidence_Map.py`

Build 29 adds the optional "Consistency Audit / Source Reconciliation" section to the dashboard. It loads no new data, does not externally verify source values, and does not claim calibration, validation, official status, actual tax payable, ATO guidance, Treasury modelling, PBO costing, or firm-level liability changes.

Build 29.5 adds an optional "Source-Locator Verification Pack" section to the dashboard when `reports/source_locator_verification_pack.json` exists. It displays loaded value cards, source-reference-only cards, placeholder-anchor cards, restricted-blocker cards, and checklist summaries. Ready for manual review does not mean reviewed or externally verified, and the section does not claim calibration, validation, actual tax payable, legal sufficiency, operational readiness, official status, ATO guidance, Treasury modelling, PBO costing, or firm-level liability changes.

Build 29.6 adds an optional "Red-Team Reviewer Objections" section to the dashboard when `reports/red_team_reviewer_objections.json` exists. It displays objection counts, critical/high objections, category coverage, unresolved blockers, what the project can say, and what the project must not claim. The section acknowledges weaknesses; it does not resolve objections, complete calibration, prove the model works, determine actual tax payable, claim validation, claim legal sufficiency, claim operational readiness, claim official status, or change firm-level liability.

Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-29.6 are included in a later sealed RC.
