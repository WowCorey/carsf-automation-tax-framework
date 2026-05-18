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
