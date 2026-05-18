# CARSF Automation Tax Framework

Private research/prototype repository for the Commonwealth Automation Revenue Stabilisation Framework (CARSF).

CARSF is a proposed Australian government-facing policy framework for measuring and responding to automation-driven labour-tax-base risk. Its core principle is:

> If productive capacity migrates from labour to capital, the fiscal base must follow it.

This repository does not contain law, tax advice, Treasury advice, ATO guidance, or calibrated Australian liability settings. It separates the policy paper track from a small Python modelling track so the framework can be tested, criticised, revised, and eventually exported into formal policy materials.

## Status

Current status: private research/prototype.

All sector values, schedule values, examples, caps, Fiscal Replacement Value values, AAVA settings, and behavioural assumptions are placeholders unless explicitly labelled as confirmed baseline figures from official sources.

The current Build 22 layer adds a consolidated executive dashboard and report index. It maps the prototype layers, generated reports, Streamlit pages, non-claim profiles, calibration blockers, external-review blockers, reviewer routing, and suggested review navigation without creating a readiness score, operational-readiness claim, legal-sufficiency claim, economic-validation claim, or firm-level liability change.

## Repository Structure

- `paper/` - Markdown policy paper, V1.5 working draft, formulas, glossary, references, and export notes.
- `audits/` - review notes, responses, and red-team register.
- `model/carsf/` - minimal Python concept model for QLC, LIBC/HLE, AII, AAVA, levies, caps, coverage, safe-harbour classification, anti-avoidance heuristics, grouping review flags, transfer-pricing previews, mixed-unit handling, evidence governance, repository guardrails, investment/incidence guardrails, national fiscal trajectory modelling, transition funding, payment interactions, synthetic distributional scenarios, synthetic household weighting, deterministic uncertainty ranges, reviewed scenario display-control classifications, metadata-only sector stress matrix review, synthetic behavioural response simulation, prototype administrative workflow routing, non-operative legislative architecture mapping, and executive dashboard consolidation.
- `model/tests/` - pytest coverage for formula bounds, caps, examples, and avoidance flags.
- `data/` - source-category registry and placeholder policy; no datasets are committed.
- `data/mock_evidence/` - synthetic mock evidence packets for workflow testing only; no real evidence or personal data is committed.
- `schedules/` - prototype sector schedules for automotive repair, logistics / warehousing, call centres / customer support, accounting / administration, retail self-checkout / fulfilment, and software / digital platforms.
- `examples/` - illustrative placeholder firm cases.
- `examples/groups/` - illustrative grouped-entity and apportionment preview cases.
- `examples/investment_guardrails/` - illustrative placeholder stress cases for burden, investment, incidence, and coverage-sensitivity guardrails.
- `examples/fiscal_trajectory/` - illustrative placeholder national fiscal trajectory cases.
- `examples/transition_payments/` - illustrative placeholder transition-payment, UBI-lite, retraining, and automation-dividend funding cases.
- `examples/payment_interactions/` - illustrative placeholder payment targeting, phase, stack, and support-incidence cases.
- `examples/distributional_scenarios/` - synthetic household distributional cases with no real household data.
- `examples/household_weighting/` - synthetic household weighting and subgroup aggregation cases with no real household data.
- `examples/uncertainty_ranges/` - deterministic placeholder uncertainty range cases with no real household data or statistical confidence claims.
- `docs/pre_legislative_hardening.md` - focused hardening note before the non-operative legislative architecture skeleton build.
- `docs/legislative_architecture.md` - non-operative legislative architecture skeleton notes and review blockers.
- `docs/executive_dashboard.md` - consolidated dashboard and report-index notes.
- `simulator/` - Streamlit interface for policy review, tax model inputs, worked examples, red-team tests, and audit log.
- `docs/` - data requirements, limitations, implementation notes, known risks, and V1.5 plan.

## Run Tests

```powershell
python -m pip install -r requirements.txt
python -m pytest
```

## Run Worked Examples

```powershell
python scripts/run_examples.py
```

Generated reports:

- `reports/example_results.md`
- `reports/example_results.json`
- `reports/grouped_entity_results.md`
- `reports/grouped_entity_results.json`
- `reports/transfer_pricing_results.md`
- `reports/transfer_pricing_results.json`
- `reports/evidence_requirements.md`
- `reports/evidence_requirements.json`
- `reports/calibration_requirements.md`
- `reports/calibration_requirements.json`

Run sector schedule expansion validation:

```powershell
python scripts/run_sector_schedule_expansion.py
```

Generated sector-schedule reports:

- `reports/sector_schedule_expansion.md`
- `reports/sector_schedule_expansion.json`

Run metadata-only sector stress matrix:

```powershell
python scripts/run_sector_stress_matrix.py
```

Generated sector-stress reports:

- `reports/sector_stress_matrix.md`
- `reports/sector_stress_matrix.json`

Run behavioural response / gaming simulation:

```powershell
python scripts/run_behavioural_response_simulation.py
```

Generated behavioural-response reports:

- `reports/behavioural_response_simulation.md`
- `reports/behavioural_response_simulation.json`

Run administrative compliance workflow shell:

```powershell
python scripts/run_administrative_compliance_workflow.py
```

Generated administrative workflow reports:

- `reports/administrative_compliance_workflow.md`
- `reports/administrative_compliance_workflow.json`

Run non-operative legislative architecture skeleton:

```powershell
python scripts/run_legislative_architecture.py
```

Generated legislative architecture reports:

- `reports/legislative_architecture.md`
- `reports/legislative_architecture.json`

Run executive dashboard consolidation:

```powershell
python scripts/run_executive_dashboard.py
```

Generated executive dashboard reports:

- `reports/executive_dashboard.md`
- `reports/executive_dashboard.json`

Run controlled mock evidence workflow reports separately:

```powershell
python scripts/run_evidence_workflow.py
```

Generated mock workflow reports:

- `reports/mock_evidence_workflow.md`
- `reports/mock_evidence_workflow.json`

Run secure ingestion-control reports:

```powershell
python scripts/run_ingestion_controls.py
```

Generated secure-ingestion reports:

- `reports/secure_ingestion_controls.md`
- `reports/secure_ingestion_controls.json`

Run repository guardrail enforcement:

```powershell
python scripts/run_repo_guardrails.py
```

Generated repository-guardrail reports:

- `reports/repo_guardrails.md`
- `reports/repo_guardrails.json`

Run investment and tax-incidence guardrails:

```powershell
python scripts/run_investment_guardrails.py
```

Generated investment/incidence reports:

- `reports/investment_guardrails.md`
- `reports/investment_guardrails.json`

Run national fiscal trajectory reports:

```powershell
python scripts/run_fiscal_trajectory.py
```

Generated fiscal trajectory reports:

- `reports/fiscal_trajectory.md`
- `reports/fiscal_trajectory.json`

Run transition-payment funding previews:

```powershell
python scripts/run_transition_funding.py
```

Generated transition-funding reports:

- `reports/transition_funding.md`
- `reports/transition_funding.json`

Run payment interaction and targeting previews:

```powershell
python scripts/run_payment_interactions.py
```

Generated payment-interaction reports:

- `reports/payment_interactions.md`
- `reports/payment_interactions.json`

Run synthetic household distributional scenarios:

```powershell
python scripts/run_distributional_scenarios.py
```

Generated distributional reports:

- `reports/distributional_scenarios.md`
- `reports/distributional_scenarios.json`

Run synthetic household weighting and subgroup aggregation:

```powershell
python scripts/run_household_weighting.py
```

Generated household-weighting reports:

- `reports/household_weighting.md`
- `reports/household_weighting.json`

Run deterministic uncertainty range mechanics:

```powershell
python scripts/run_uncertainty_ranges.py
```

Generated uncertainty reports:

- `reports/uncertainty_ranges.md`
- `reports/uncertainty_ranges.json`

Run reviewed scenario comparison classifications:

```powershell
python scripts/run_reviewed_scenarios.py
```

Generated reviewed-scenario reports:

- `reports/reviewed_scenarios.md`
- `reports/reviewed_scenarios.json`

The reports are illustrative placeholder outputs only. They are not legal grouping findings, transfer-pricing adjustments, ATO findings, tax assessments, Treasury guidance, OECD/BEPS analysis, economic validation, or real liability calculations.
Mock evidence reports use synthetic fixtures only and do not validate any real liability, tax position, audit finding, legal conclusion, Treasury assessment, ATO assessment, or economic claim.
Secure-ingestion reports are prototype governance controls only. Only synthetic mock evidence is allowed in this repository; real evidence must not be committed.
Repository guardrail reports are prototype enforcement checks only. They are not a complete DLP system, secret scanner, cybersecurity control, legal/privacy audit, Treasury control, ATO control, or forensic validation.
Investment and incidence guardrail reports are prototype review outputs only. They are not economic validation, investment advice, Treasury modelling, ATO guidance, legal advice, market forecasting, or tax advice.
Fiscal trajectory reports are prototype national-level outputs only. They are not forecasts, Treasury modelling, ATO estimates, ABS analysis, DSS estimates, PBO costing, legal advice, tax advice, or economic validation.
Transition-funding reports are prototype payment-funding outputs only. They are not UBI policy, welfare advice, DSS modelling, Services Australia modelling, Treasury costing, PBO costing, legal advice, tax advice, or economic validation.
Payment-interaction reports are prototype targeting, phase-rule, baseline-separation, double-counting, and support-incidence outputs only. They are not UBI policy, welfare advice, eligibility law, Centrelink/DSS/Services Australia modelling, Treasury costing, PBO costing, legal advice, tax advice, or economic validation.
Distributional scenario reports are synthetic household outputs only. They are not real household modelling, welfare advice, eligibility law, DSS/Services Australia modelling, ABS analysis, Treasury modelling, PBO costing, legal advice, tax advice, or economic validation.
Household-weighting reports are synthetic household weighting outputs only. They are not population estimates, real distributional modelling, ABS/HILDA/Census analysis, DSS/Services Australia modelling, Treasury modelling, PBO costing, welfare advice, eligibility law, legal advice, tax advice, or economic validation.
Uncertainty range reports are deterministic placeholder outputs only. They are not statistical confidence intervals, forecasts, real uncertainty quantification, population estimates, ABS/HILDA/Census analysis, DSS/Services Australia modelling, Treasury modelling, PBO costing, welfare advice, eligibility law, legal advice, tax advice, or economic validation.
Reviewed scenario reports are prototype display-control outputs only. They are not statistical validation, population estimates, real household modelling, ABS/HILDA/Census analysis, DSS/Services Australia modelling, ATO analysis, Treasury modelling, PBO costing, welfare advice, eligibility law, legal advice, tax advice, or economic validation.
Sector schedule expansion reports are prototype placeholder outputs only. They are not calibrated. They are not legal schedules. They are not Treasury schedules. They are not ATO guidance. They are not ABS/ATO/DSS/PBO analysis. They do not contain real industry data. They must not be used to estimate actual tax payable.
Sector stress matrix reports are prototype metadata review outputs only. They are not calibrated, not sector rankings, not Treasury modelling, not ATO guidance, not ABS/ATO/DSS/PBO analysis, not economic validation, not investment advice, not legal advice, and not tax advice. They do not use real industry data, do not estimate actual tax payable, do not implement legal sector attribution, do not implement real multi-schedule blending, and do not modify firm-level CARSF liability logic.
Behavioural response reports are synthetic pathway review outputs only. They do not predict taxpayer behaviour, estimate behavioural elasticity, implement ATO audit logic, create compliance-risk scoring, implement enforcement, implement penalties, estimate actual tax payable, or modify firm-level CARSF liability logic.
Administrative workflow reports are synthetic pathway-organisation outputs only. They are not a workflow endorsed by the ATO, not guidance from the ATO, not audit logic, not enforcement, not compliance scoring, do not create notices or penalties, and do not modify firm-level CARSF liability logic.
Legislative architecture reports are non-operative architecture maps only. They are not operative law, not a Bill, not legal drafting, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not Parliamentary Counsel drafting, not legally sufficient, and not constitutionally reviewed. They create no rights, obligations, statutory powers, information-gathering powers, notices, penalties, enforcement process, or compliance scoring, do not determine tax payable, and do not modify firm-level CARSF liability logic.
Executive dashboard reports are prototype navigation and report-index outputs only. They are not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare advice, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, and not an official review pathway. They do not determine actual tax payable, do not use taxpayer-level or firm-level data, and do not modify firm-level CARSF liability logic.

## Run the Simulator

```powershell
python -m streamlit run simulator/app.py
```

The simulator is a prototype interface only. It must not be used to estimate actual tax payable.

## What V1.5 Is Trying To Prove

V1.5 is not just an examples update. It is V1.4 plus two prototype sector schedules and a measurement appendix. The working target is to test whether CARSF can:

- prevent QLC inflation through a per-worker cap;
- measure AAVA without treating unverified deductions as settled policy;
- report CoverageRatio alongside CARS-I;
- distinguish worker-assist AI from labour-substituting automation;
- handle automotive repair and logistics / warehousing as prototype schedules;
- expand prototype schedule coverage to call centres / customer support, accounting / administration, retail self-checkout / fulfilment, and software / digital platforms without calibration or real tax usability claims;
- classify prototype safe-harbour, anti-avoidance, and grouped-entity review signals without changing liability;
- preview grouped-entity aggregation and multi-schedule apportionment without implementing tax-law grouping or attribution;
- preview related-party / transfer-pricing adjustment candidates without replacing reported AAVA or calculating any legal addback;
- handle mixed canonical output units by prohibiting direct output/HLE aggregation and showing only standalone liability sums, schedule-level comparison, and a value-weighted exposure index;
- record prototype evidence requirements and decision-log summaries without validating liability;
- test controlled mock evidence packet submission, review states, and privacy/secrecy classification without real evidence;
- enforce a default-deny prototype ingestion policy before any non-synthetic evidence could enter the repo;
- enforce repository-level CI guardrails for likely evidence leaks, secret markers, wrong storage zones, and unsafe generated report content;
- surface effective burden, normal-return preservation, pass-through, investment-risk, under-capture, and over-capture warnings without changing final liability;
- model placeholder national fiscal trajectories for PAYG erosion, transfer pressure, automation revenue captured, and residual fiscal gaps without changing firm-level liability;
- preview transition-payment, UBI-lite, retraining, automation-dividend, and hybrid funding options without changing firm-level liability;
- preview existing transfer baseline separation, targeting, phase-in / phase-out, payment-stack double-counting, and support-payment fiscal incidence without changing firm-level liability;
- preview synthetic household budget stress, re-employment timing, payment cliffs, regional stress, and residual household gaps without using real household data or changing firm-level liability;
- aggregate synthetic household scenarios by placeholder weights and subgroups without claiming representativeness or changing firm-level liability;
- wrap synthetic household and weighted subgroup outputs with deterministic low/base/high uncertainty ranges without claiming confidence intervals, forecasts, or calibration;
- classify reviewed scenario outputs into show, warning, hidden, non-interpretable, and external-review-only display categories without validating them or changing firm-level liability;
- compare prototype sector schedules through a metadata-only stress matrix that uses do-not-rank display controls without calibration or real sector-score claims;
- map synthetic behavioural response and gaming pathways to linked avoidance flags, placeholder pressure bands, countermeasure categories, and review statuses without predicting conduct or changing firm-level liability;
- organise synthetic cases into administrative workflow queues, evidence request bundles, behavioural-response links, locked/suppressed states, and external-review pathways without creating enforcement, notices, compliance scoring, or liability changes;
- map CARSF concepts into a non-operative legislative architecture skeleton with Parts, Divisions, definition placeholders, schedule placeholders, evidence/safeguard placeholders, regulation-making placeholders, commencement/transitional placeholders, and external-review blockers without drafting operative law or changing liability;
- consolidate the full prototype stack into an executive dashboard and report index without creating a readiness score, official review pathway, validation claim, or liability change;
- define a calibration shell and data source registry without collecting real data;
- identify open-source AI and R&D Tax Incentive interaction questions without overclaiming.

## Not Yet Solved

The model still needs real Treasury, ATO, ABS, DSS, HILDA, HELP, superannuation, state payroll tax, industry, and legal data. It also needs calibrated safe-harbour thresholds, legal grouped-entity rules, tax-law attribution, transfer pricing, GST and international tax review, related-party adjustments, behavioural elasticity work, tax incidence modelling, anti-avoidance drafting, privacy review, and independent tax counsel review before any external policy use.

Safe-harbour outputs are prototype classification only. They do not reduce, cap, or erase calculated liability in this build.
Grouped-entity and apportionment outputs are prototype modelling previews only. They do not establish legal grouping, tax attribution, or actual liability.
Adjusted AAVA is preview-only and does not replace reported AAVA. The value-weighted exposure index is not a tax base and is not a replacement for calibrated sector schedules.
Evidence assessments are prototype governance scaffolding only. No calibration has occurred and no real evidence or restricted datasets have been collected.
Controlled mock evidence can upgrade only prototype workflow status, such as `partial` or `sufficient_for_prototype`; it never creates real-world sufficiency.
Secure storage, real redaction, real access control, legal/privacy approval, and audit enforcement remain out of scope.
Repository guardrails are over-blocking by design and cannot prove that the repository is free of sensitive content. Real evidence remains prohibited.
Investment, incidence, pass-through, and burden-balance outputs are uncalibrated placeholders. They do not validate economic effects and do not modify final liability.
National fiscal trajectory outputs are uncalibrated placeholders. They are not forecasts, do not validate public revenue impacts, and do not modify firm-level CARSF liability.
Transition-payment funding outputs are uncalibrated placeholders. They are not UBI or welfare policy, do not validate social-policy effects, and do not modify firm-level CARSF liability.
Payment-interaction outputs are uncalibrated placeholders. They do not implement welfare eligibility law, Centrelink/DSS/Services Australia administration, household means testing, or validated support-payment fiscal incidence.
Distributional scenario outputs are synthetic placeholders. They do not model real Australian households, real household hardship, real welfare eligibility, or validated regional/labour-market outcomes.
Household weighting and subgroup aggregation outputs are synthetic placeholders. They are not population estimates, survey weights, ABS/HILDA/Census analysis, DSS / Services Australia modelling, or real distributional modelling.
Uncertainty range outputs are deterministic placeholders. They are not Monte Carlo, statistical confidence intervals, forecasts, real uncertainty quantification, or validated sensitivity analysis.
Sector stress matrix outputs are metadata-only placeholders. They are not calibrated sector scores, not official schedules, not real industry analysis, and not usable for estimating actual tax payable.
Behavioural response outputs are deterministic synthetic pathway reviews. They do not predict conduct, estimate behavioural elasticity, implement ATO audit logic, create compliance-risk scoring, implement enforcement, model penalties, or score real taxpayers.
Administrative workflow outputs are deterministic synthetic pathway-routing reviews. They are not an operational ATO process, not enforcement, not notices, not penalties, not compliance scoring, and not usable for estimating actual tax payable.
Legislative architecture outputs are non-operative mapping outputs. They are not a Bill, not legal drafting, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not Parliamentary Counsel drafting, not constitutionally reviewed, and not usable to create rights, obligations, powers, notices, penalties, enforcement, compliance scoring, or tax-payable determinations.
Executive dashboard outputs are navigation and index outputs only. They are not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, not a maturity score, not an official review pathway, not validation, and not a basis for determining actual tax payable.
