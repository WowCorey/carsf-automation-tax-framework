# V1.5 Release Candidate Pack

Status: private research prototype release-candidate packaging.

## Purpose

The V1.5 release-candidate pack consolidates the current CARSF prototype stack into a working-paper and reviewer-navigation package. It indexes prototype layers, generated reports, release notes, reviewer briefing, report map, calibration blockers, non-claim boundaries, external-review routing, and release manifest metadata.

## Non-Claims

- This is a private research prototype and release-candidate pack only.
- It is not legal advice.
- It is not tax advice.
- It is not ATO guidance.
- It is not Treasury modelling.
- It is not economic validation.
- It is not welfare advice.
- It is not statistical validation.
- It is not compliance scoring.
- It is not enforcement.
- It is not operational readiness.
- It is not legal sufficiency.
- It is not legislative readiness.
- It is not a readiness score.
- It is not a maturity score.
- It is not an official review pathway.
- It is not approval.
- It is not validation.
- External review has not been completed.
- It does not determine actual tax payable.
- It does not use taxpayer-level data, firm-level confidential data, household microdata, restricted government data, confidential Treasury/PBO material, or unauthorised data.
- It does not modify firm-level CARSF liability.

## Files

- `data/release/v1_5_release_manifest.yaml`
- `release/v1_5_rc/RELEASE_NOTES.md`
- `release/v1_5_rc/REVIEWER_BRIEFING.md`
- `release/v1_5_rc/REPORT_MAP.md`
- `release/v1_5_rc/CALIBRATION_BLOCKERS.md`
- `release/v1_5_rc/NON_CLAIM_BOUNDARIES.md`
- `release/v1_5_rc/EXTERNAL_REVIEW_ROUTING.md`
- `release/v1_5_rc/RELEASE_MANIFEST.json`
- `release/v1_5_rc/FINAL_RC_INTEGRITY_SEAL.md`
- `release/v1_5_rc/FINAL_RC_INTEGRITY_SEAL.json`
- `release/v1_5_rc/FINAL_RC_DIGESTS.json`
- `reports/public_data_pilot.md`
- `reports/public_data_pilot.json`
- `reports/public_data_evidence_map.md`
- `reports/public_data_evidence_map.json`
- `reports/public_data_consistency_audit.md`
- `reports/public_data_consistency_audit.json`

## Runner

Generate release-candidate pack reports with:

```powershell
python scripts/run_v1_5_release_candidate_pack.py
```

Generated reports:

- `reports/v1_5_release_candidate_pack.md`
- `reports/v1_5_release_candidate_pack.json`
- `reports/v1_5_final_rc_integrity_seal.md`
- `reports/v1_5_final_rc_integrity_seal.json`

## Working Paper Link

The V1.5 working paper remains `paper/CARSF_V1_5_WORKING.md`. The release-candidate update adds a stack map and cross-references to current prototype layers; it does not convert the paper into legal drafting, official policy, or validation.

## Review Use

Use the release pack after the executive dashboard. The pack is useful for routing external review, identifying calibration blockers, and checking report boundaries. It must not be used as a readiness finding, official review pathway, legal sufficiency claim, operational readiness claim, economic validation, welfare validation, statistical validation, or actual-tax-payable analysis.

Build 27 adds a public aggregate-data pilot and realistic-placeholder anchor layer. It may include small public aggregate extracts and source-reference records, but it is not calibration, public data extracts do not prove the model works, realistic placeholders remain placeholders, source references are not loaded datasets, and restricted-data requirements are not data access.

Build 28 adds a reviewer evidence map and dashboard for the public-data pilot. It loads no new data, adds no new public extracts, and only maps source references, loaded public extracts, source-reference-only rows, placeholder anchors, sanity checks, restricted blockers, forbidden repo data, and reviewer questions. It is not calibration, validation, approval, actual tax payable, legal sufficiency, operational readiness, official status, ATO guidance, Treasury modelling, or PBO costing.

Build 29 adds an internal consistency audit and source-reconciliation layer for the public-data pilot and evidence map. It loads no new data, adds no new public extracts, does not externally verify source values, and only checks internal agreement across source records, extracts, evidence rows, placeholders, sanity checks, digests, reports, dashboard source, and non-claim boundaries. It is not calibration, validation, approval, actual tax payable, legal sufficiency, operational readiness, official status, ATO guidance, Treasury modelling, or PBO costing.

Build 29.5 adds a source-locator verification pack for existing Build 27-29 artefacts. It loads no new data, adds no values, does not scrape sources, does not call APIs, does not externally verify source values, and only creates manual-review cards and checklists. Ready for manual review does not mean reviewed or externally verified. It is not calibration, validation, approval, actual tax payable, legal sufficiency, operational readiness, official status, ATO guidance, Treasury modelling, or PBO costing.

Build 29.6 adds a red-team reviewer objections pack for existing Build 26-29.5 artefacts. It loads no new data, adds no public values, does not scrape sources, does not call APIs, does not externally verify source values, does not resolve objections, and only packages likely reviewer criticisms, valid concern explanations, bounded responses, unresolved blockers, evidence needs, and must-not-claim boundaries. It is not calibration, validation, approval, actual tax payable, legal sufficiency, operational readiness, official status, ATO guidance, Treasury modelling, or PBO costing.

## Final RC Integrity Seal Link

The final RC integrity seal checks release documents, attack-pack documents, generated reports, manifests, scripts, digest metadata, non-claim boundaries, repo guardrail expectations, CI expectations, and false readiness/legal/validation flags. `seal_passed` is an internal integrity status only and must not be read as approval, validation, external review completion, operational readiness, legal sufficiency, legislative readiness, official status, or implementation readiness.

Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-29.6 are included in a later sealed RC.
