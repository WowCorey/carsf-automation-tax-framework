# CARSF V1.5 Release Candidate Pack - Release Notes

Status: private research prototype / release-candidate pack.

## Non-Claims

This is a private research prototype and release-candidate pack only. It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare advice, not statistical validation, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, and not an official review pathway. It does not determine actual tax payable, does not use taxpayer-level data, firm-level confidential data, household microdata, restricted government data, confidential Treasury/PBO material, or unauthorised data, and does not modify firm-level CARSF liability.

## Release Name

CARSF V1.5 Release Candidate Pack.

## What Changed Since Earlier V1.5 Drafts

- The working paper now points to the full V1.5 prototype stack rather than only the early formula and two-schedule prototype.
- The schedule library now includes six placeholder sector schedules and a metadata-only sector stress matrix.
- Synthetic behavioural response, administrative workflow, and non-operative legislative architecture layers are included as review objects only.
- Fiscal trajectory, transition funding, payment interaction, household distributional, weighting, uncertainty, and reviewed-scenario layers are included as placeholder or synthetic outputs only.
- The executive dashboard is the preferred navigation entry point for generated reports, non-claim profiles, calibration blockers, and external-review routing.

## Generated Reports

The release pack indexes generated reports under `reports/`, including examples, schedules, sector stress, behavioural response, administrative workflow, legislative architecture, executive dashboard, evidence workflow, secure ingestion, repository guardrails, investment/incidence, fiscal trajectory, transition funding, payment interactions, distributional scenarios, household weighting, uncertainty ranges, and reviewed scenarios.

## Guardrail Expectations

The release candidate expects CI to run all existing report runners plus `python scripts/run_v1_5_release_candidate_pack.py`, followed by repository guardrails. Passing those checks is a prototype repository-safety signal only and is not privacy, cybersecurity, legal, tax, ATO, Treasury, or operational validation.

## Known Limitations

- Prototype only and placeholder only unless explicitly labelled otherwise.
- No restricted, confidential, taxpayer-level, firm-level confidential, household microdata, real evidence, or unauthorised data is added.
- No readiness score, official status, policy approval, legal sufficiency, operational readiness, economic validation, welfare validation, statistical validation, enforcement, notices, penalties, or compliance scoring is created.
- The pack only consolidates existing prototype reports, warnings, navigation, review blockers, and working-paper material for external review.

## Next Recommended Review Steps

Start with `reports/executive_dashboard.md`, then read this release pack, the working paper, `docs/current_status.md`, `docs/known_risks.md`, `docs/calibration_shell.md`, and the layer-specific generated reports.

## Build 24 Attack-Pack Addendum

The external review attack pack under `release/v1_5_rc/attack_pack/` adds discipline-specific challenge prompts, failure modes, required external inputs, boundary checks, report attack matrices, and layer attack matrices.

It does not mean external review has been completed. It does not mean approval has been granted. It does not mean validation has occurred. It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare validation, not statistical validation, not compliance scoring, not enforcement, and does not modify firm-level CARSF liability.

## Build 25 Final RC Integrity Seal Addendum

The final RC integrity seal under `release/v1_5_rc/` verifies release documents, attack-pack documents, generated reports, required manifests, required scripts, digest metadata, non-claim boundaries, forbidden affirmative claim scanning, repo guardrail status expectations, CI expectations, and false readiness/legal/validation flags.

It is an internal integrity seal only. It is not approval, not validation, not external review completion, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare validation, not statistical validation, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, not a maturity score, not official status, and not an official review pathway. It does not determine actual tax payable, use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, or modify firm-level CARSF liability.

## Build 26 Real-Data Feasibility Addendum

Build 26 adds a real-data feasibility and calibration-intake map that identifies public aggregate data candidates, restricted-data requirements, realistic placeholders, forbidden repo data, module data needs, and Build 27 pilot candidates.

No real data has been loaded by Build 26. No calibration has occurred. Realistic placeholders are not real data and are not calibrated. Public-data candidates are not loaded datasets. Restricted-data requirements are not data access. This is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, not official status, and does not determine actual tax payable or modify firm-level CARSF liability.

Build 25 sealed the previous RC state. If Build 26 is included in a later sealed RC, the final RC integrity seal must be regenerated for that later state rather than described as already covering these feasibility artefacts.

## Build 27 Public-Data Pilot Addendum

Build 27 adds a public aggregate-data pilot and realistic-placeholder anchor layer. It may include small public aggregate extracts and source-reference records that are safe to commit, with source provenance, licence/access notes, field sanity checks, module sanity checks, restricted-data blockers, forbidden repo data rules, and digest metadata.

This is not calibration. Calibration has not been completed. Public data extracts do not prove the model works. Realistic placeholders remain placeholders and are not real data or calibrated. Source references are not loaded datasets. Restricted-data requirements are not data access. The layer does not determine actual tax payable, does not use taxpayer-level data, firm-level confidential data, household microdata, ABS DataLab microdata, HILDA microdata, DSS/Services Australia records, ATO taxpayer records, confidential Treasury/PBO material, restricted government data, real evidence, or unauthorised data, and does not modify firm-level CARSF liability.

Build 25 sealed the previous RC state. A new integrity seal must be regenerated if Build 27 is included in a later sealed RC.

## Build 28 Public-Data Evidence Map Addendum

Build 28 adds a reviewer evidence map and Streamlit dashboard for the Build 27 public-data pilot. It maps source references, loaded public aggregate extracts, source-reference-only records, realistic placeholder anchors, field sanity checks, module sanity checks, restricted-data blockers, forbidden repo data, and reviewer questions.

No new data is loaded by Build 28. Build 27 public aggregate extracts remain sanity-check-only or placeholder-anchor-only. This is not calibration, calibration has not been completed, public data does not prove the model works, realistic placeholders remain placeholders, source references are not loaded datasets, and restricted-data requirements are not data access. The layer does not determine actual tax payable, does not claim validation, approval, legal sufficiency, operational readiness, official status, ATO guidance, Treasury modelling, PBO costing, or modify firm-level CARSF liability.

Build 25 sealed the previous RC state. A new integrity seal must be regenerated if Builds 26-29 are included in a later sealed RC.

## Build 29 Public-Data Consistency Audit Addendum

Build 29 adds an internal consistency audit and source-reconciliation layer for the Build 27 public-data pilot and Build 28 evidence map. It reconciles source references, loaded public extracts, source-reference-only records, placeholder anchors, field sanity checks, module sanity checks, digest metadata, generated reports, dashboard source, restricted blockers, forbidden repo data, and non-claim boundaries.

No new data is loaded by Build 29. It does not externally verify source values, scrape public sources, call external APIs, complete calibration, prove the model works, determine actual tax payable, claim validation, approval, legal sufficiency, operational readiness, official status, ATO guidance, Treasury modelling, PBO costing, or modify firm-level CARSF liability. Reconciled means internally consistent only.

Build 25 sealed the previous RC state. A new integrity seal must be regenerated if Builds 26-29 are included in a later sealed RC.

## Build 29.5 Public-Data Source-Locator Verification Pack Addendum

Build 29.5 adds a source-locator verification pack for the existing Build 27-29 public-data pilot artefacts. It creates reviewer-facing source/value cards, source-reference-only cards, placeholder-anchor cards, restricted-blocker cards, and manual-review checklists.

No new data is loaded by Build 29.5. It does not add public values, externally verify source values, scrape public sources, call APIs, complete calibration, prove the model works, determine actual tax payable, claim validation, approval, legal sufficiency, operational readiness, official status, ATO guidance, Treasury modelling, PBO costing, or modify firm-level CARSF liability. Ready for manual review does not mean reviewed or externally verified.

Build 25 sealed the previous RC state. A new integrity seal must be regenerated if Builds 26-29.5 are included in a later sealed RC.

## Build 29.6 Red-Team Reviewer Objections Pack Addendum

Build 29.6 adds a red-team reviewer objections pack for the existing Build 26-29.5 public-data pilot and reviewer materials. It lists likely reviewer criticisms, explains why each concern is valid, maps affected artefacts, gives bounded project responses, preserves unresolved blockers, and states what evidence would be needed to resolve each objection.

No new data is loaded by Build 29.6. It does not add public values, externally verify source values, scrape public sources, call APIs, resolve objections, complete calibration, prove the model works, determine actual tax payable, claim validation, approval, legal sufficiency, operational readiness, official status, ATO guidance, Treasury modelling, PBO costing, or modify firm-level CARSF liability. Objections being acknowledged does not mean they are resolved, and partially mitigated does not mean solved.

Build 25 sealed the previous RC state. A new integrity seal must be regenerated if Builds 26-29.6 are included in a later sealed RC.

## Build 31 Public Real Aggregate Data Loader Addendum

Build 31 adds a controlled public real aggregate-data loader over existing public-pilot source records. It records source-located, public, aggregate-level, non-personal, non-confidential values that are safe for repository use, writes parsed values and digest metadata, and keeps source candidates not loaded where exact safe local values are unavailable.

This loads real public aggregate data only. It does not load restricted data, personal data, taxpayer-level data, firm-confidential data, household microdata, raw downloaded datasets, confidential source material, scrape public sources, or call external APIs. Public aggregate data does not equal calibration. Calibration has not been completed. Public data does not prove the model works. This is not validation, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, and not official status. It does not determine actual tax payable and does not modify firm-level CARSF liability.

Build 25 sealed the previous RC state. A new integrity seal must be regenerated if Builds 26-31 are included in a later sealed RC.

## Build 32 Public Data Placeholder Replacement Map Addendum

Build 32 adds a public data placeholder replacement map over the Build 31 loaded public aggregate values. It classifies existing realistic placeholders as replaced by public aggregate anchor, narrowed by public aggregate anchor, informed by public aggregate anchor, still placeholder-only, blocked until restricted data, blocked until external review, or unable to be replaced by public aggregate data.

No new data is loaded by Build 32. Public aggregate data can anchor or narrow some placeholders, but it does not calibrate the model. Replaced by public aggregate anchor does not mean validated. Narrowed by public aggregate anchor does not mean statistically estimated. Informed by public aggregate anchor does not mean representative. Placeholder-only items remain placeholders and restricted-data blockers remain blockers. This is not validation, legal advice, tax advice, ATO guidance, Treasury modelling, PBO costing, economic validation, welfare validation, statistical validation, operational readiness, legal sufficiency, official status, actual tax payable, or firm-level CARSF liability modification.

Build 25 sealed the previous RC state. A new integrity seal must be regenerated if Builds 26-32 are included in a later sealed RC.
