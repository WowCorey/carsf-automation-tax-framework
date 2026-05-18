# CARSF V1.5 Release Candidate Pack - Release Notes

Status: private research prototype / release-candidate pack.

## Non-Claims

This is a private research prototype and release-candidate pack only. It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare advice, not statistical validation, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, and not an official review pathway. It does not determine actual tax payable, does not use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, and does not modify firm-level CARSF liability.

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
- No real data is added.
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
