# CARSF Automation Tax Framework

Private research/prototype repository for the Commonwealth Automation Revenue Stabilisation Framework (CARSF).

CARSF is a proposed Australian government-facing policy framework for measuring and responding to automation-driven labour-tax-base risk. Its core principle is:

> If productive capacity migrates from labour to capital, the fiscal base must follow it.

This repository does not contain law, tax advice, Treasury advice, ATO guidance, or calibrated Australian liability settings. It separates the policy paper track from a small Python modelling track so the framework can be tested, criticised, revised, and eventually exported into formal policy materials.

## Status

Current status: private research/prototype.

All sector values, schedule values, examples, caps, Fiscal Replacement Value values, AAVA settings, and behavioural assumptions are placeholders unless explicitly labelled as confirmed baseline figures from official sources.

## Repository Structure

- `paper/` - Markdown policy paper, V1.5 working draft, formulas, glossary, references, and export notes.
- `audits/` - review notes, responses, and red-team register.
- `model/carsf/` - minimal Python concept model for QLC, LIBC/HLE, AII, AAVA, levies, caps, coverage, safe-harbour classification, anti-avoidance heuristics, grouping review flags, transfer-pricing previews, mixed-unit handling, evidence governance, repository guardrails, investment/incidence guardrails, and national fiscal trajectory modelling.
- `model/tests/` - pytest coverage for formula bounds, caps, examples, and avoidance flags.
- `data/` - source-category registry and placeholder policy; no datasets are committed.
- `data/mock_evidence/` - synthetic mock evidence packets for workflow testing only; no real evidence or personal data is committed.
- `schedules/` - prototype sector schedules for automotive repair and logistics / warehousing.
- `examples/` - illustrative placeholder firm cases.
- `examples/groups/` - illustrative grouped-entity and apportionment preview cases.
- `examples/investment_guardrails/` - illustrative placeholder stress cases for burden, investment, incidence, and coverage-sensitivity guardrails.
- `examples/fiscal_trajectory/` - illustrative placeholder national fiscal trajectory cases.
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

The reports are illustrative placeholder outputs only. They are not legal grouping findings, transfer-pricing adjustments, ATO findings, tax assessments, Treasury guidance, OECD/BEPS analysis, economic validation, or real liability calculations.
Mock evidence reports use synthetic fixtures only and do not validate any real liability, tax position, audit finding, legal conclusion, Treasury assessment, ATO assessment, or economic claim.
Secure-ingestion reports are prototype governance controls only. Only synthetic mock evidence is allowed in this repository; real evidence must not be committed.
Repository guardrail reports are prototype enforcement checks only. They are not a complete DLP system, secret scanner, cybersecurity control, legal/privacy audit, Treasury control, ATO control, or forensic validation.
Investment and incidence guardrail reports are prototype review outputs only. They are not economic validation, investment advice, Treasury modelling, ATO guidance, legal advice, market forecasting, or tax advice.
Fiscal trajectory reports are prototype national-level outputs only. They are not forecasts, Treasury modelling, ATO estimates, ABS analysis, DSS estimates, PBO costing, legal advice, tax advice, or economic validation.

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
- define a calibration shell and data source registry without collecting real data;
- identify open-source AI and R&D Tax Incentive interaction questions without overclaiming.

## Not Yet Solved

The model still needs real Treasury, ATO, ABS, DSS, HILDA, HELP, superannuation, state payroll tax, industry, and legal data. It also needs calibrated safe-harbour thresholds, legal grouped-entity rules, tax-law attribution, transfer pricing, GST and international tax review, related-party adjustments, behavioural elasticity estimates, tax incidence modelling, anti-avoidance drafting, privacy review, and independent tax counsel review before any external policy use.

Safe-harbour outputs are prototype classification only. They do not reduce, cap, or erase calculated liability in this build.
Grouped-entity and apportionment outputs are prototype modelling previews only. They do not establish legal grouping, tax attribution, or actual liability.
Adjusted AAVA is preview-only and does not replace reported AAVA. The value-weighted exposure index is not a tax base and is not a replacement for calibrated sector schedules.
Evidence assessments are prototype governance scaffolding only. No calibration has occurred and no real evidence or restricted datasets have been collected.
Controlled mock evidence can upgrade only prototype workflow status, such as `partial` or `sufficient_for_prototype`; it never creates real-world sufficiency.
Secure storage, real redaction, real access control, legal/privacy approval, and audit enforcement remain out of scope.
Repository guardrails are over-blocking by design and cannot prove that the repository is free of sensitive content. Real evidence remains prohibited.
Investment, incidence, pass-through, and burden-balance outputs are uncalibrated placeholders. They do not validate economic effects and do not modify final liability.
National fiscal trajectory outputs are uncalibrated placeholders. They are not forecasts, do not validate public revenue impacts, and do not modify firm-level CARSF liability.
