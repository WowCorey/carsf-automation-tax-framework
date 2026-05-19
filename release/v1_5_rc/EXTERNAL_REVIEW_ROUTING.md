# CARSF V1.5 Release Candidate Pack - External Review Routing

## Non-Claims

This routing note is for a private research prototype and release-candidate pack only. It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare advice, not statistical validation, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, and not an official review pathway. It does not determine actual tax payable, does not use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, and does not modify firm-level CARSF liability.

Suggested routing is review navigation only and is not an official process.

| Reviewer | Primary Layers | First Materials | Main Questions |
| --- | --- | --- | --- |
| Legal | legislative architecture, administrative workflow, payment interactions, behavioural response | `reports/legislative_architecture.md`, `reports/administrative_compliance_workflow.md` | Are any placeholders too close to operative law, powers, obligations, notices, penalties, or legal sufficiency claims? |
| Tax | formula core, schedules, transfer-pricing previews, AAVA, caps | `paper/formula_reference.md`, `reports/transfer_pricing_results.md` | Where do legal/tax-law attribution, deductibility, grouping, and transfer-pricing problems arise? |
| Treasury | fiscal trajectory, transition funding, incidence, calibration shell | `reports/fiscal_trajectory.md`, `reports/transition_funding.md` | Which assumptions require external costing, public-finance, and fiscal-risk review? |
| ATO methods | administrative workflow, evidence workflow, ingestion, guardrails | `reports/administrative_compliance_workflow.md`, `reports/mock_evidence_workflow.md` | What must remain outside scope to avoid guidance, audit logic, or operational-readiness claims? |
| Privacy / secrecy | secure ingestion, evidence workflow, household layers | `reports/secure_ingestion_controls.md`, `docs/calibration_shell.md` | How should real data, protected information, redaction, retention, and access be kept out of repo? |
| Statistical methods | household weighting, uncertainty ranges, reviewed scenarios | `reports/uncertainty_ranges.md`, `reports/reviewed_scenarios.md` | Which outputs are fragile, non-representative, or missing valid uncertainty methods? |
| Economic methods | investment/incidence, sector stress, fiscal trajectory | `reports/investment_guardrails.md`, `reports/sector_stress_matrix.md` | Which assumptions create false precision or unsupported economic conclusions? |
| Welfare policy | transition funding, payment interactions, household scenarios | `reports/payment_interactions.md`, `reports/distributional_scenarios.md` | Which outputs risk being mistaken for welfare advice, eligibility law, or Services Australia/DSS modelling? |
| Parliamentary Counsel | legislative architecture skeleton and working paper | `reports/legislative_architecture.md`, `paper/CARSF_V1_5_WORKING.md` | Which areas must remain reserved for external drafting counsel? |
| Cybersecurity / DLP / repository controls | ingestion controls and repo guardrails | `reports/secure_ingestion_controls.md`, `reports/repo_guardrails.md` | What external controls are required before any evidence-adjacent use? |
| Hostile red-team | all boundary layers | `docs/known_risks.md`, `reports/executive_dashboard.md` | Where could a reader overclaim validation, readiness, official status, or real-world use? |
| Real-data feasibility | data-source intake, forbidden-data rules, placeholder provenance, Build 27 pilot candidates | `reports/real_data_feasibility.md`, `docs/real_data_feasibility.md` | Are public-source licensing, aggregate-only handling, restricted-data exclusion, realistic-placeholder labels, and no-calibration boundaries strong enough? |

## Attack-Pack Routing Addendum

Inspect:

- `release/v1_5_rc/attack_pack/`
- `reports/external_review_attack_pack.md`

Required challenge:

- Use the attack pack to structure discipline-specific objections, missing-evidence requests, and boundary checks.
- Treat attack-pack severity labels as challenge labels only. They are not risk scores, not validation outcomes, not approval statuses, and not readiness ratings.

Non-claim:

- The attack pack does not mean external review has been completed, does not mean approval has been granted, does not mean validation has occurred, and does not modify firm-level CARSF liability.

## Final RC Integrity Seal Routing Addendum

Inspect:

- `release/v1_5_rc/FINAL_RC_INTEGRITY_SEAL.md`
- `release/v1_5_rc/FINAL_RC_DIGESTS.json`
- `reports/v1_5_final_rc_integrity_seal.md`

Required challenge:

- Treat the seal as an internal artefact completeness check only.
- Use the seal to find missing documents, missing reports, manifest drift, false readiness/legal/validation flag failures, boundary phrase failures, guardrail denied findings, and CI expectation gaps.
- Do not treat `seal_passed` as approval, validation, external review completion, legal sufficiency, operational readiness, official status, or implementation readiness.

Non-claim:

- The final RC integrity seal is not approval, not validation, not external review completion, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare validation, not statistical validation, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, not a maturity score, not official status, and not an official review pathway. It does not determine actual tax payable or modify firm-level CARSF liability.

## Build 26 Real-Data Feasibility Routing Addendum

Build 26 does not load real data, does not complete calibration, and does not grant restricted-data access. Public-data candidates are not loaded datasets. Restricted-data requirements are not data access. Realistic placeholders are not real data and are not calibrated.

Build 25 sealed the previous RC state. If Build 26 is included in a later sealed RC, the integrity seal must be regenerated for that later state rather than treated as already covering Build 26.
