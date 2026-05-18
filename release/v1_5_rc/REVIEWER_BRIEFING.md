# CARSF V1.5 Release Candidate Pack - Reviewer Briefing

## Non-Claims

This briefing is for a private research prototype and release-candidate pack only. It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare advice, not statistical validation, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, and not an official review pathway. It does not determine actual tax payable, does not use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, and does not modify firm-level CARSF liability.

## Policy Reviewer

Inspect first: `reports/executive_dashboard.md`, `paper/CARSF_V1_5_WORKING.md`, `docs/current_status.md`, and `docs/known_risks.md`.

Key risks: readers may overread placeholder reports as policy design, validation, or public-sector readiness. Do not infer endorsement, final policy design, or official review status. External policy, legal, tax, Treasury, ATO methods, privacy, economic, statistical, welfare, and Parliamentary Counsel review is required.

## Technical Reviewer

Inspect first: `scripts/run_*.py`, `model/carsf/`, `model/tests/`, `reports/example_results.md`, and `reports/repo_guardrails.md`.

Key risks: generated reports could become stale relative to manifests, and guardrails are prototype-only. Do not infer complete DLP, cybersecurity assurance, or real-data handling readiness.

## Legal Reviewer

Inspect first: `reports/legislative_architecture.md`, `reports/administrative_compliance_workflow.md`, and `release/v1_5_rc/NON_CLAIM_BOUNDARIES.md`.

Key risks: non-operative skeletons must not become operative law, legal sufficiency, powers, obligations, notices, penalties, rights, or enforcement. External legal and Parliamentary Counsel review is required.

## Tax Reviewer

Inspect first: `reports/example_results.md`, `reports/transfer_pricing_results.md`, `reports/sector_schedule_expansion.md`, and `paper/formula_reference.md`.

Key risks: AAVA, grouped entity, transfer-pricing, offshore attribution, caps, credits, and schedules are placeholders. Do not infer tax advice, ATO guidance, tax payable, or legal addbacks.

## ATO Methods Reviewer

Inspect first: `reports/administrative_compliance_workflow.md`, `reports/mock_evidence_workflow.md`, and `reports/secure_ingestion_controls.md`.

Key risks: review queues and evidence bundles are synthetic; they do not create ATO powers, guidance, audit logic, compliance scoring, notices, penalties, or operational readiness.

## Treasury Methods Reviewer

Inspect first: `reports/fiscal_trajectory.md`, `reports/transition_funding.md`, `reports/investment_guardrails.md`, and `reports/calibration_requirements.md`.

Key risks: outputs are placeholder accounting and sensitivity views only, not Treasury modelling, costing, forecasts, or economic validation.

## Privacy Reviewer

Inspect first: `reports/secure_ingestion_controls.md`, `reports/mock_evidence_workflow.md`, `model/carsf/repo_guardrails.py`, and `docs/calibration_shell.md`.

Key risks: no real data should enter the repo. Current controls are not real IAM, secure storage, retention enforcement, redaction tooling, or privacy compliance.

## Statistical Methods Reviewer

Inspect first: `reports/uncertainty_ranges.md`, `reports/household_weighting.md`, and `reports/reviewed_scenarios.md`.

Key risks: ranges are deterministic placeholders and weights are synthetic. Do not infer confidence intervals, forecasts, population estimates, statistical validation, or representativeness.

## Economic Methods Reviewer

Inspect first: `reports/investment_guardrails.md`, `reports/sector_stress_matrix.md`, and `reports/fiscal_trajectory.md`.

Key risks: incidence, investment deterrence, pass-through, sector stress, and fiscal effects are uncalibrated. Do not infer economic validation or investment advice.

## Welfare Policy Reviewer

Inspect first: `reports/transition_funding.md`, `reports/payment_interactions.md`, `reports/distributional_scenarios.md`, and `reports/household_weighting.md`.

Key risks: payment and household layers are synthetic and placeholder-only. Do not infer welfare advice, eligibility law, Services Australia modelling, DSS modelling, payment adequacy, or household hardship validation.

## Parliamentary Counsel Reviewer

Inspect first: `reports/legislative_architecture.md` and `paper/CARSF_V1_5_WORKING.md`.

Key risks: the architecture skeleton is not a Bill, not legal drafting, not legally sufficient, and not ready for operative drafting.

## Hostile / Red-Team Reviewer

Inspect first: `docs/known_risks.md`, `reports/behavioural_response_simulation.md`, `reports/reviewed_scenarios.md`, and `reports/repo_guardrails.md`.

Key risks: attack overclaiming, stale manifests, missing non-claims, hidden calibration assumptions, false precision, and any language implying approval, validation, readiness, or real-world use.
