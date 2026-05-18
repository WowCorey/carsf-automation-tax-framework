# Build Log

## V1.5 Working Paper Release Candidate Pack

Branch: `v1.5-working-paper-release-candidate-pack`

Baseline: PR #24 merged into `main`, including the executive dashboard consolidation.

Purpose of this build:

- Update the V1.5 working paper with a release-candidate stack map.
- Add `release/v1_5_rc/` release notes, reviewer briefing, report map, calibration blockers, non-claim boundaries, external-review routing, and release manifest snapshot.
- Add a release manifest and runner for `reports/v1_5_release_candidate_pack.md` and `reports/v1_5_release_candidate_pack.json`.
- Add tests and CI integration for release-pack validation.

Limitations:

- Private research prototype only.
- Release-candidate pack only.
- Not legal advice, tax advice, ATO guidance, Treasury modelling, economic validation, welfare advice, statistical validation, compliance scoring, enforcement, operational readiness, legal sufficiency, legislative readiness, a readiness score, official status, or an official review pathway.
- Does not determine actual tax payable.
- Uses no taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- Does not modify firm-level CARSF liability.

## V1.5 End-to-End Example Runner

Branch: `v1.5-end-to-end-example-runner`

Baseline: PR #1 merged into `main`, including prototype schedule hardening, AAVA appendix, hostile tests, numeric fail-closed validation, CI, and prototype automotive/logistics schedules.

Purpose of this build:

- Add the first end-to-end worked example runner.
- Run all six illustrative YAML examples through the current model formulas.
- Generate machine-readable JSON and policy-readable Markdown reports.
- Update the Streamlit Worked Examples page to use the same pipeline.

Tests run:

- `python -m pytest` - 109 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- YAML parse check for all schedules/examples - passed.
- `python scripts/run_examples.py` - generated JSON and Markdown reports.
- Headless Streamlit probe - HTTP 200.

Reports generated:

- `reports/example_results.json`
- `reports/example_results.md`

Limitations:

- Outputs are illustrative placeholders only.
- No legal, tax, Treasury, ATO, or economic validation is implied.
- No real calibration values are introduced.

## V1.5 Safe Harbour and Avoidance Review Engine

Branch: `v1.5-safe-harbour-and-avoidance-engine`

Baseline: PR #2 merged into `main`, including the end-to-end example runner, reports, and Streamlit worked examples integration.

Purpose of this build:

- Add executable prototype safe-harbour classification.
- Add executable anti-avoidance heuristics.
- Add grouped-entity review flags.
- Emit risk outputs into JSON reports, Markdown reports, and Streamlit worked examples.
- Keep all risk outputs as review signals only; no safe harbour modifies liability.

Tests run:

- `python -m pytest` - 130 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- YAML parse check for all schedules/examples - passed.
- `python scripts/run_examples.py` - regenerated JSON and Markdown reports.
- Streamlit probe - HTTP 200.

Reports generated:

- `reports/example_results.json`
- `reports/example_results.md`

Limitations:

- Safe-harbour thresholds are illustrative placeholders.
- Anti-avoidance checks are heuristics, not legal findings.
- Grouping checks do not perform full aggregation.
- No legal, tax, Treasury, ATO, or economic validation is implied.

## V1.5 Grouped-Entity and Apportionment Previews

Branch: `v1.5-grouped-entity-and-apportionment`

Baseline: PR #3 merged into `main`, including executable safe-harbour classification, anti-avoidance review flags, and grouped-entity review flags.

Purpose of this build:

- Add a prototype grouped-entity aggregation preview.
- Add a prototype multi-schedule apportionment preview.
- Add grouped example YAML files and a hybrid logistics stress variant.
- Generate grouped preview JSON and Markdown reports.
- Add a Streamlit grouping/apportionment page.

Tests run:

- `python -m pytest` - 146 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse check for schedules/examples, including `examples/groups`, passed.
- `python scripts/run_examples.py` - regenerated single-entity and grouped preview reports.
- Streamlit probe - HTTP 200.

Reports generated:

- `reports/example_results.json`
- `reports/example_results.md`
- `reports/grouped_entity_results.json`
- `reports/grouped_entity_results.md`

Limitations:

- Grouped aggregation is not legal grouping logic.
- Apportionment is not tax-law attribution.
- Transfer pricing, GST, international tax, and legal advice remain future work.
- No legal, tax, Treasury, ATO, or economic validation is implied.

## V1.5 Transfer-Pricing and Mixed-Unit Handling

Branch: `v1.5-transfer-pricing-and-mixed-unit-handling`

Baseline: PR #4 merged into `main`, including grouped-entity aggregation previews, mixed-activity apportionment plumbing, grouped reports, and the hybrid logistics stress variant.

Purpose of this build:

- Add non-operative transfer-pricing / related-party review previews.
- Add adjusted-AAVA preview calculations that do not mutate reported AAVA.
- Add optional adjusted-AAVA liability preview where existing inputs allow safe recomputation.
- Add mixed-unit handling that prohibits direct output/HLE aggregation where canonical output units differ.
- Generate transfer-pricing and mixed-unit JSON/Markdown reports.

Tests run:

- `python -m pytest` - 208 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse check for schedules/examples, including `examples/groups`, passed.
- `python scripts/run_examples.py` - regenerated single-entity, grouped, transfer-pricing, and mixed-unit preview reports.
- Streamlit probe - HTTP 200.

Reports generated:

- `reports/transfer_pricing_results.json`
- `reports/transfer_pricing_results.md`

Limitations:

- No transfer-pricing law, OECD/BEPS analysis, ATO finding, Treasury guidance, legal finding, or tax assessment is implemented.
- Adjusted AAVA is preview-only.
- Mixed-unit value-weighted exposure is not a tax base.
- Future work requires international tax, GST, transfer-pricing, legal, and calibrated sector-schedule review.

## V1.5 Evidence, Decision Log, and Calibration Shell

Branch: `v1.5-evidence-decision-log-calibration-shell`

Baseline: PR #5 merged into `main`, including transfer-pricing previews, adjusted-AAVA preview logic, mixed-unit handling, transfer-pricing reports, and Streamlit transfer-pricing/mixed-unit page.

Purpose of this build:

- Add prototype evidence requirements for formula inputs and review flags.
- Add deterministic decision-log summaries for example, grouped, and transfer-pricing runs.
- Add a calibration registry shell without real values.
- Add data source registry and placeholder policy.
- Generate evidence and calibration JSON/Markdown reports.

Tests run:

- `python -m pytest` - 226 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse check for schedules/examples/data - passed.
- `python scripts/run_examples.py` - regenerated example, grouped, transfer-pricing, evidence, and calibration reports.
- Streamlit probe - HTTP 200.

Reports generated:

- `reports/evidence_requirements.json`
- `reports/evidence_requirements.md`
- `reports/calibration_requirements.json`
- `reports/calibration_requirements.md`

Limitations:

- Evidence assessment does not validate liability, law, tax, audit, or forensic sufficiency.
- No real data has been collected.
- No calibration has occurred.
- Legal, tax, privacy, economic, Treasury/ATO-style, and sector-specific review remains required.

## V1.5 Controlled Mock Evidence and Review Workflow

Branch: `v1.5-controlled-mock-evidence-and-review-workflow`

Baseline: PR #6 merged into `main`, including evidence requirements, decision-log summaries, calibration shell, data source registry, evidence/calibration reports, and Streamlit evidence page.

Purpose of this build:

- Add synthetic mock evidence packet models.
- Add prototype review-state workflow transitions.
- Add privacy/secrecy classification helpers.
- Add controlled mock evidence fixtures with `synthetic_mock_evidence_only: true`.
- Generate mock evidence workflow JSON/Markdown reports.
- Add Streamlit mock evidence workflow page.

Tests run:

- `python -m pytest` - 246 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse check for schedules/examples/data - parsed 20 YAML files.
- `python scripts/run_examples.py` - regenerated example, grouped, transfer-pricing, evidence, and calibration reports.
- `python scripts/run_evidence_workflow.py` - generated mock evidence workflow reports.
- Streamlit bare import probe for `simulator/app.py`, evidence page, and mock evidence workflow page - passed. HTTP probe timed out locally and no lingering Streamlit process remained.

Reports generated:

- `reports/mock_evidence_workflow.json`
- `reports/mock_evidence_workflow.md`

Limitations:

- Mock evidence is workflow scaffolding only.
- It does not validate real data, liability, tax positions, audit findings, legal conclusions, Treasury assessments, ATO assessments, or economic claims.
- Future real evidence handling requires privacy, secrecy, legal, ATO/Treasury, data-owner, and governance controls.

## V1.5 Secure Evidence Ingestion Controls

Branch: `v1.5-secure-evidence-ingestion-controls`

Baseline: PR #7 merged into `main`, including controlled synthetic mock evidence workflow, review-state workflow, privacy/secrecy classification, mock evidence reports, and Streamlit mock evidence page.

Purpose of this build:

- Add default-deny secure ingestion policy scaffolding.
- Add heuristic sensitive-marker scanning.
- Add redaction-plan metadata for external secure-system handling.
- Add retention/access-control policy helpers.
- Add immutable-style ingestion audit records.
- Add mock ingestion request fixtures and secure-ingestion reports.

Tests run:

- `python -m pytest` - 272 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse check for schedules/examples/data - parsed 27 YAML files.
- `python scripts/run_examples.py` - regenerated example, grouped, transfer-pricing, evidence, and calibration reports.
- `python scripts/run_evidence_workflow.py` - regenerated mock evidence workflow reports.
- `python scripts/run_ingestion_controls.py` - generated secure-ingestion control reports.
- Streamlit bare import probe for `simulator/app.py`, mock evidence workflow page, and secure ingestion controls page - passed.

Reports generated:

- `reports/secure_ingestion_controls.json`
- `reports/secure_ingestion_controls.md`

Limitations:

- Controls are prototype governance controls only.
- They do not implement real secure storage, IAM, redaction, deletion, cybersecurity assurance, legal validation, privacy validation, tax validation, Treasury/ATO guidance, forensic validation, or audit enforcement.

## V1.5 Repository-Level Enforcement Gates

Branch: `v1.5-repository-enforcement-gates`

Baseline: PR #8 merged into `main`, including secure evidence-ingestion controls, default-deny ingestion policy, sensitive scanning, redaction metadata, retention/access policy, immutable-style ingestion audit records, and `.gitignore` guardrails.

Purpose of this build:

- Add reusable repository guardrail scanning.
- Add a CI enforcement step that fails on denied guardrail findings.
- Add optional local pre-commit hook configuration.
- Add synthetic guardrail test fixtures for prohibited paths, extensions, marker handling, report non-claims, and raw evidence payload checks.
- Generate repository guardrail JSON/Markdown reports.

Tests run:

- `python -m pytest` - 287 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse check for schedules/examples/data - parsed 27 YAML files.
- `python scripts/run_examples.py` - regenerated example, grouped, transfer-pricing, evidence, and calibration reports.
- `python scripts/run_evidence_workflow.py` - regenerated mock evidence workflow reports.
- `python scripts/run_ingestion_controls.py` - regenerated secure-ingestion control reports.
- `python scripts/run_repo_guardrails.py` - generated repository guardrail reports with zero denied findings.
- Streamlit bare import probe for `simulator/pages/11_Repository_Guardrails.py` - passed.

Reports generated:

- `reports/repo_guardrails.json`
- `reports/repo_guardrails.md`

Limitations:

- Repository guardrails are prototype checks only.
- They are not complete DLP, secret scanning, cybersecurity control, legal/privacy audit, Treasury control, ATO control, or forensic validation.
- Passing the guardrails does not prove that the repository is free of sensitive content.

## V1.5 Investment and Incidence Guardrails

Branch: `v1.5-investment-incidence-and-burden-guardrails`

Baseline: PR #9 merged into `main`, including repository-level enforcement gates and CI guardrails.

Purpose of this build:

- Add non-operative investment burden review guardrails.
- Add tax-incidence / pass-through placeholder previews.
- Add under-capture and over-capture burden-balance checks.
- Add placeholder sensitivity sweeps for pass-through rates, cap rates, and AAVA values.
- Add illustrative investment guardrail stress examples and reports.

Tests run:

- `python -m pytest` - 310 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse check for schedules/examples/data - parsed 32 YAML files.
- `python scripts/run_examples.py` - regenerated example, grouped, transfer-pricing, evidence, and calibration reports.
- `python scripts/run_evidence_workflow.py` - regenerated mock evidence workflow reports.
- `python scripts/run_ingestion_controls.py` - regenerated secure-ingestion control reports.
- `python scripts/run_investment_guardrails.py` - generated investment and incidence guardrail reports.
- `python scripts/run_repo_guardrails.py` - generated repository guardrail reports with zero denied findings.
- Streamlit bare import probe for `simulator/pages/12_Investment_and_Incidence_Guardrails.py` - passed.

Reports generated:

- `reports/investment_guardrails.json`
- `reports/investment_guardrails.md`

Limitations:

- Investment and incidence guardrails are prototype review outputs only.
- They are not economic validation, investment advice, Treasury modelling, ATO guidance, legal advice, market forecasting, or tax advice.
- Guardrail outputs do not automatically modify final liability.

## V1.5 National Fiscal Trajectory Engine

Branch: `v1.5-national-fiscal-trajectory-engine`

Baseline: PR #10 merged into `main`, including investment guardrails, tax-incidence previews, burden-balance checks, and sensitivity sweeps.

Purpose of this build:

- Add deterministic placeholder workforce displacement trajectories.
- Add placeholder public-revenue and transfer-pressure calculations.
- Add national fiscal trajectory outputs for PAYG loss, support pressure, automation revenue captured, and residual public-sector gaps.
- Add fiscal sensitivity sweeps.
- Add fiscal trajectory examples, reports, CI step, tests, and Streamlit page.

Tests run:

- `python -m pytest` - 358 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse check for schedules/examples/data - parsed 37 YAML files.
- `python scripts/run_examples.py` - regenerated example, grouped, transfer-pricing, evidence, and calibration reports.
- `python scripts/run_evidence_workflow.py` - regenerated mock evidence workflow reports.
- `python scripts/run_ingestion_controls.py` - regenerated secure-ingestion control reports.
- `python scripts/run_investment_guardrails.py` - regenerated investment and incidence guardrail reports.
- `python scripts/run_fiscal_trajectory.py` - generated fiscal trajectory reports.
- `python scripts/run_repo_guardrails.py` - generated repository guardrail reports with zero denied findings.
- Streamlit bare import probe for `simulator/app.py` and `simulator/pages/13_Fiscal_Trajectory.py` - passed.

Fiscal-accounting hardening added before merge:

- Superannuation contribution loss is tracked as retirement-system contribution pressure, not ordinary Commonwealth revenue loss.
- Commonwealth gap and total public-sector gap exclude superannuation contribution pressure.
- Broader labour-linked pressure reports superannuation contribution pressure separately.
- Offsetting company tax, GST, and other Commonwealth revenue gains are allowed only when `allow_revenue_gains: true`.

## V1.5 Transition-Payment Funding Module

Branch: `v1.5-transition-payment-funding-module`

Baseline: PR #11 merged into `main`, including national fiscal trajectory, workforce displacement, public revenue, transfer pressure, and fiscal sensitivity sweeps.

Purpose of this build:

- Add non-operative transition-payment design calculations.
- Add placeholder payment portfolio comparisons.
- Link fiscal trajectory outputs to year-by-year transition funding status.
- Add payment sensitivity sweeps.
- Add transition-payment examples, reports, tests, CI step, and Streamlit page.

Tests run:

- `python -m pytest` - 390 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse check for schedules/examples/data - parsed 43 YAML files.
- `python scripts/run_examples.py` - regenerated existing example report outputs successfully.
- `python scripts/run_evidence_workflow.py` - regenerated mock evidence workflow reports successfully.
- `python scripts/run_ingestion_controls.py` - regenerated secure-ingestion control reports successfully.
- `python scripts/run_repo_guardrails.py` - passed with zero denied findings and 48 warning findings.
- `python scripts/run_investment_guardrails.py` - regenerated investment guardrail reports successfully.
- `python scripts/run_fiscal_trajectory.py` - regenerated fiscal trajectory reports successfully.
- `python scripts/run_transition_funding.py` - generated transition funding reports successfully.
- Streamlit bare import probe for `simulator/pages/14_Transition_Funding.py` - passed.

Reports generated:

- `reports/transition_funding.json`
- `reports/transition_funding.md`

Limitations:

- Transition-payment outputs are illustrative placeholders only.
- They are not UBI policy, welfare advice, DSS modelling, Services Australia modelling, Treasury costing, PBO costing, legal advice, tax advice, or economic validation.
- The transition funding layer does not modify firm-level CARSF liability.

## V1.5 Payment Interactions and Targeting Mechanics

Branch: `v1.5-payment-interaction-and-targeting-mechanics`

Baseline: PR #12 merged into `main`, including transition-payment funding, payment portfolio coverage, fiscal trajectory linkage, cliff-risk preview, and payment sensitivity sweeps.

Purpose of this build:

- Add existing transfer baseline separation.
- Add placeholder targeting mechanics for displaced-worker and retraining eligibility.
- Add phase-in and phase-out mechanics.
- Add payment-stack double-counting previews.
- Add support fiscal-incidence previews without treating offsets as validated savings.
- Add payment interaction examples, reports, tests, CI step, and Streamlit page.

Tests run:

- `python -m pytest` - 413 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse check for schedules/examples/data - parsed 49 YAML files.
- `python scripts/run_examples.py` - regenerated existing example report outputs successfully.
- `python scripts/run_evidence_workflow.py` - regenerated mock evidence workflow reports successfully.
- `python scripts/run_ingestion_controls.py` - regenerated secure-ingestion control reports successfully.
- `python scripts/run_repo_guardrails.py` - passed with zero denied findings and 48 warning findings.
- `python scripts/run_investment_guardrails.py` - regenerated investment guardrail reports successfully.
- `python scripts/run_fiscal_trajectory.py` - regenerated fiscal trajectory reports successfully.
- `python scripts/run_transition_funding.py` - regenerated transition funding reports successfully.
- `python scripts/run_payment_interactions.py` - generated payment interaction reports successfully.
- Streamlit bare import probe for `simulator/pages/15_Payment_Interactions.py` - passed.

Reports generated:

- `reports/payment_interactions.json`
- `reports/payment_interactions.md`

Limitations:

- Payment-interaction outputs are illustrative placeholders only.
- They are not UBI policy, welfare advice, eligibility law, Centrelink/DSS/Services Australia modelling, Treasury costing, PBO costing, legal advice, tax advice, or economic validation.
- The payment interaction layer does not modify firm-level CARSF liability.

## V1.5 Synthetic Household Distributional Scenarios

Branch: `v1.5-synthetic-household-distributional-scenarios`

Baseline: PR #13 merged into `main`, including payment interaction and targeting mechanics, existing transfer baseline separation, phase-in / phase-out mechanics, payment-stack double-counting review, and support fiscal-incidence preview.

Purpose of this build:

- Add synthetic household archetype budget-stress previews.
- Add re-employment timing, payment cliff, and regional stress modules.
- Add distributional scenario and summary orchestration.
- Add synthetic household examples, reports, tests, CI step, and Streamlit page.

Tests run:

- `python -m pytest` - 448 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse check for schedules/examples/data - parsed 56 YAML files.
- `python scripts/run_examples.py` - regenerated existing example report outputs successfully.
- `python scripts/run_evidence_workflow.py` - regenerated mock evidence workflow reports successfully.
- `python scripts/run_ingestion_controls.py` - regenerated secure-ingestion control reports successfully.
- `python scripts/run_repo_guardrails.py` - passed with zero denied findings and 48 warning findings.
- `python scripts/run_investment_guardrails.py` - regenerated investment guardrail reports successfully.
- `python scripts/run_fiscal_trajectory.py` - regenerated fiscal trajectory reports successfully.
- `python scripts/run_transition_funding.py` - regenerated transition funding reports successfully.
- `python scripts/run_payment_interactions.py` - regenerated payment interaction reports successfully.
- `python scripts/run_distributional_scenarios.py` - generated distributional scenario reports successfully.
- Streamlit bare import probe for `simulator/pages/16_Distributional_Scenarios.py` - passed.

Reports generated:

- `reports/distributional_scenarios.json`
- `reports/distributional_scenarios.md`

Limitations:

- Distributional scenario outputs are synthetic placeholders only.
- They are not real household modelling, welfare advice, eligibility law, DSS/Services Australia modelling, ABS analysis, Treasury modelling, PBO costing, legal advice, tax advice, or economic validation.
- The distributional scenario layer does not modify firm-level CARSF liability.

## V1.5 Household Weighting and Subgroup Aggregation Shell

Branch: `v1.5-household-weighting-subgroup-aggregation`

Baseline: PR #14 merged into `main`, including synthetic household distributional scenarios and payment-interaction linkage.

Purpose of this build:

- Add synthetic household weight validation.
- Add synthetic subgroup definitions and deterministic subgroup assignment.
- Add weighted distributional aggregation for residual household gaps and high/critical shock shares.
- Add household calibration-readiness requirements.
- Add household weighting examples, reports, tests, CI step, documentation, and Streamlit page.

Tests run:

- `python -m pytest` - 478 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse check for schedules/examples/data - parsed 61 YAML files.
- `python scripts/run_examples.py` - regenerated existing example report outputs successfully.
- `python scripts/run_evidence_workflow.py` - regenerated mock evidence workflow reports successfully.
- `python scripts/run_ingestion_controls.py` - regenerated secure-ingestion control reports successfully.
- `python scripts/run_repo_guardrails.py` - passed with zero denied findings and 48 warning findings.
- `python scripts/run_investment_guardrails.py` - regenerated investment guardrail reports successfully.
- `python scripts/run_fiscal_trajectory.py` - regenerated fiscal trajectory reports successfully.
- `python scripts/run_transition_funding.py` - regenerated transition funding reports successfully.
- `python scripts/run_payment_interactions.py` - regenerated payment interaction reports successfully.
- `python scripts/run_distributional_scenarios.py` - regenerated distributional scenario reports successfully.
- `python scripts/run_household_weighting.py` - generated household weighting reports successfully.
- Streamlit bare import probe for `simulator/app.py` and `simulator/pages/17_Household_Weighting.py` - passed.

Reports generated:

- `reports/household_weighting.json`
- `reports/household_weighting.md`

Limitations:

- Household weighting outputs are synthetic placeholders only.
- They are not population estimates, real distributional modelling, ABS/HILDA/Census analysis, DSS/Services Australia modelling, Treasury modelling, PBO costing, welfare advice, eligibility law, legal advice, tax advice, or economic validation.
- The household weighting layer does not modify firm-level CARSF liability.

## V1.5 Uncertainty Range Mechanics

Branch: `v1.5-uncertainty-range-mechanics`

Baseline: PR #15 merged into `main`, including household weighting and subgroup aggregation, calibration readiness, and real-data exclusion guardrails.

Purpose of this build:

- Add deterministic low/base/high uncertainty range validation.
- Add household uncertainty wrappers for synthetic distributional scenario outputs.
- Add weighted subgroup uncertainty wrappers.
- Add uncertainty summary counts for stable, sensitive, and fragile outputs.
- Add uncertainty examples, reports, tests, CI step, documentation, and Streamlit page.

Tests run:

- `python -m pytest` - 508 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse check for schedules/examples/data - parsed 67 YAML files.
- `python scripts/run_examples.py` - regenerated existing example report outputs successfully.
- `python scripts/run_evidence_workflow.py` - regenerated mock evidence workflow reports successfully.
- `python scripts/run_ingestion_controls.py` - regenerated secure-ingestion control reports successfully.
- `python scripts/run_repo_guardrails.py` - passed with zero denied findings and 48 warning findings.
- `python scripts/run_investment_guardrails.py` - regenerated investment guardrail reports successfully.
- `python scripts/run_fiscal_trajectory.py` - regenerated fiscal trajectory reports successfully.
- `python scripts/run_transition_funding.py` - regenerated transition funding reports successfully.
- `python scripts/run_payment_interactions.py` - regenerated payment interaction reports successfully.
- `python scripts/run_distributional_scenarios.py` - regenerated distributional scenario reports successfully.
- `python scripts/run_household_weighting.py` - regenerated household weighting reports successfully.
- `python scripts/run_uncertainty_ranges.py` - generated uncertainty range reports successfully.
- Streamlit bare import probe for `simulator/app.py` and `simulator/pages/18_Uncertainty_Ranges.py` - passed.

Reports generated:

- `reports/uncertainty_ranges.json`
- `reports/uncertainty_ranges.md`

Limitations:

- Uncertainty ranges are deterministic placeholders only.
- They are not Monte Carlo, statistical confidence intervals, forecasts, real uncertainty quantification, population estimates, ABS/HILDA/Census analysis, DSS/Services Australia modelling, Treasury modelling, PBO costing, welfare advice, eligibility law, legal advice, tax advice, or economic validation.
- The uncertainty range layer does not modify firm-level CARSF liability.

## V1.5 Reviewed Scenario Comparison Layer

Branch: `v1.5-reviewed-scenario-comparison-layer`

Baseline: PR #16 merged into `main`, including deterministic uncertainty range mechanics for synthetic household and weighted subgroup outputs.

Purpose of this build:

- Add a reviewed scenario display-control layer.
- Classify household uncertainty outputs into discussion, strong-warning, hidden, non-interpretable, and external-review-only categories.
- Classify weighted subgroup uncertainty outputs while preserving non-representativeness warnings.
- Add reviewed scenario reports, tests, CI step, documentation, and Streamlit page.

Tests run:

- `python -m pytest` - 541 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse check for schedules/examples/data - parsed 71 YAML files.
- `python scripts/run_examples.py` - regenerated existing example report outputs successfully.
- `python scripts/run_sector_schedule_expansion.py` - generated sector schedule expansion reports successfully.
- `python scripts/run_evidence_workflow.py` - regenerated mock evidence workflow reports successfully.
- `python scripts/run_ingestion_controls.py` - regenerated secure-ingestion control reports successfully.
- `python scripts/run_investment_guardrails.py` - regenerated investment guardrail reports successfully.
- `python scripts/run_fiscal_trajectory.py` - regenerated fiscal trajectory reports successfully.
- `python scripts/run_transition_funding.py` - regenerated transition funding reports successfully.
- `python scripts/run_payment_interactions.py` - regenerated payment interaction reports successfully.
- `python scripts/run_distributional_scenarios.py` - regenerated distributional scenario reports successfully.
- `python scripts/run_household_weighting.py` - regenerated household weighting reports successfully.
- `python scripts/run_uncertainty_ranges.py` - regenerated uncertainty range reports successfully.
- `python scripts/run_reviewed_scenarios.py` - regenerated reviewed scenario reports successfully.
- `python scripts/run_repo_guardrails.py` - passed with zero denied findings and 49 warning findings.
- Streamlit bare import probe for `simulator/app.py` and `simulator/pages/20_Sector_Schedules.py` - passed.

Reports generated:

- `reports/reviewed_scenarios.json`
- `reports/reviewed_scenarios.md`

Limitations:

- Reviewed scenario outputs are prototype display-control signals only.
- They are not statistical validation, population estimates, real household modelling, ABS/HILDA/Census analysis, DSS/Services Australia modelling, ATO analysis, Treasury modelling, PBO costing, welfare advice, eligibility law, legal advice, tax advice, or economic validation.
- The reviewed scenario layer does not modify firm-level CARSF liability.

## V1.5 Sector Schedule Expansion

Branch: `v1.5-sector-schedule-expansion`

Baseline: PR #17 merged into `main`, including reviewed scenario comparison and display-control rules.

Purpose of this build:

- Add four new placeholder prototype sector schedules.
- Add schedule validation for required fields, AII weights, QLC weights, OPFTE, FRV, caps, placeholder labels, and calibration requirements.
- Add sector schedule expansion reports, tests, CI step, documentation, and Streamlit page.

New schedules:

- `call_centres_customer_support`
- `accounting_administration`
- `retail_self_checkout_fulfilment`
- `software_digital_platforms`

Tests run:

- `python -m pytest` - 557 passed, 1 pytest-asyncio deprecation warning under Python 3.14.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse check for schedules/examples/data - parsed 71 YAML files.
- `python scripts/run_examples.py` - regenerated existing example report outputs successfully.
- `python scripts/run_sector_schedule_expansion.py` - regenerated sector schedule expansion reports successfully.
- `python scripts/run_sector_stress_matrix.py` - generated sector stress matrix reports successfully.
- `python scripts/run_evidence_workflow.py` - regenerated mock evidence workflow reports successfully.
- `python scripts/run_ingestion_controls.py` - regenerated secure-ingestion control reports successfully.
- `python scripts/run_investment_guardrails.py` - regenerated investment guardrail reports successfully.
- `python scripts/run_fiscal_trajectory.py` - regenerated fiscal trajectory reports successfully.
- `python scripts/run_transition_funding.py` - regenerated transition funding reports successfully.
- `python scripts/run_payment_interactions.py` - regenerated payment interaction reports successfully.
- `python scripts/run_distributional_scenarios.py` - regenerated distributional scenario reports successfully.
- `python scripts/run_household_weighting.py` - regenerated household weighting reports successfully.
- `python scripts/run_uncertainty_ranges.py` - regenerated uncertainty range reports successfully.
- `python scripts/run_reviewed_scenarios.py` - regenerated reviewed scenario reports successfully.
- `python scripts/run_repo_guardrails.py` - passed with zero denied findings and 49 warning findings.
- Streamlit bare import probes for `simulator/app.py` and `simulator/pages/21_Sector_Stress_Matrix.py` - passed.

Reports generated:

- `reports/sector_schedule_expansion.json`
- `reports/sector_schedule_expansion.md`

Limitations:

- Sector schedules are prototype placeholders only.
- They are not calibrated, not legal schedules, not Treasury schedules, not ATO guidance, not ABS/ATO/DSS/PBO analysis, do not contain real industry data, and must not be used to estimate actual tax payable.
- They do not modify firm-level CARSF liability logic and do not implement real multi-schedule attribution.
- Software / digital platform capital-base treatment remains unresolved and subject to AASB 138, tax counsel, and Treasury review.

## V1.5 Sector Stress Matrix

Branch: `v1.5-sector-stress-matrix`

Baseline: PR #17 merged into `main`, including expanded placeholder sector schedules.

Purpose of this build:

- Add a metadata-only sector stress matrix across all prototype schedules.
- Compare placeholder schedules across automation intensity, QLC vulnerability, AAVA sensitivity, incidence risk, investment risk, avoidance / gaming risk, calibration difficulty, legal attribution difficulty, and display-control status.
- Mark every row do-not-rank and preserve non-claim language.
- Add sector stress matrix reports, tests, CI step, documentation, and Streamlit page.

Tests run:

- `python -m pytest` - 579 passed, 1 pytest-asyncio deprecation warning.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse for `schedules/`, `examples/`, and `data/` - parsed 72 YAML files.
- Report runners passed: examples, sector schedule expansion, sector stress matrix, behavioural response simulation, evidence workflow, ingestion controls, investment guardrails, fiscal trajectory, transition funding, payment interactions, distributional scenarios, household weighting, uncertainty ranges, reviewed scenarios, and repo guardrails.
- Repo guardrails passed with zero denied findings.
- Bare Streamlit import probes passed for `simulator/app.py` and `simulator/pages/22_Behavioural_Response.py`.

Reports generated:

- `reports/sector_stress_matrix.json`
- `reports/sector_stress_matrix.md`

Limitations:

- Sector stress matrix outputs are prototype metadata review outputs only.
- They are not calibrated, not government sector assessments, not Treasury modelling, not ATO guidance, not ABS/ATO/DSS/PBO analysis, not economic validation, not investment advice, not legal advice, and not tax advice.
- They do not use real industry data, do not estimate actual tax payable, do not modify firm-level CARSF liability logic, do not implement legal sector attribution, and do not implement real multi-schedule blending.

## V1.5 Behavioural Response / Gaming Simulation

Branch: `v1.5-behavioural-response-gaming-simulation`

Baseline: PR #19 merged into `main`, including the sector stress matrix.

Purpose of this build:

- Add synthetic behavioural response / gaming pathway scenarios.
- Map response pathways to linked avoidance flags, placeholder pressure bands, countermeasure categories, review statuses, external-review flags, and calibration blockers.
- Add behavioural response reports, tests, CI step, documentation, and Streamlit page.

Tests run:

- `python -m pytest` - 579 passed, 1 pytest-asyncio deprecation warning.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse for `schedules/`, `examples/`, and `data/` - parsed 72 YAML files.
- Report runners passed: examples, sector schedule expansion, sector stress matrix, behavioural response simulation, evidence workflow, ingestion controls, investment guardrails, fiscal trajectory, transition funding, payment interactions, distributional scenarios, household weighting, uncertainty ranges, reviewed scenarios, and repo guardrails.
- Repo guardrails passed with zero denied findings.
- Bare Streamlit import probes passed for `simulator/app.py` and `simulator/pages/22_Behavioural_Response.py`.

Reports generated:

- `reports/behavioural_response_simulation.json`
- `reports/behavioural_response_simulation.md`

Limitations:

- Behavioural response outputs are prototype deterministic synthetic pathway reviews only.
- They do not predict conduct, estimate behavioural elasticity, implement ATO audit logic, perform Treasury modelling, perform ABS/ATO/DSS/PBO analysis, create compliance-risk scoring, implement enforcement, model penalties, provide legal advice, provide tax advice, provide investment advice, or provide economic validation.
- They do not use firm-level, taxpayer-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- They do not estimate actual tax payable and do not modify firm-level CARSF liability logic.

## V1.5 Administrative Compliance Workflow

Branch: `v1.5-administrative-compliance-workflow`

Baseline: PR #20 merged into `main`, including behavioural response simulation.

Purpose of this build:

- Add synthetic administrative workflow scenarios.
- Organise synthetic cases into evidence request bundles, review queues, escalation pathways, behavioural-response links, privacy/secrecy review notes, locked cases, suppressed cases, and external-review blockers.
- Add administrative workflow reports, tests, CI step, documentation, and Streamlit page.

Tests run:

- `python -m pytest` - 598 passed, 1 pytest-asyncio deprecation warning.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse for `schedules/`, `examples/`, and `data/` - parsed 73 YAML files.
- Report runners passed: examples, sector schedule expansion, sector stress matrix, behavioural response simulation, administrative compliance workflow, evidence workflow, ingestion controls, investment guardrails, fiscal trajectory, transition funding, payment interactions, distributional scenarios, household weighting, uncertainty ranges, reviewed scenarios, and repo guardrails.
- Repo guardrails passed with zero denied findings.
- Bare Streamlit import probes passed for `simulator/app.py` and `simulator/pages/23_Administrative_Workflow.py`.

Reports generated:

- `reports/administrative_compliance_workflow.json`
- `reports/administrative_compliance_workflow.md`

Limitations:

- Administrative workflow outputs are prototype deterministic synthetic pathway-organisation reviews only.
- They are not a workflow endorsed by the ATO, not guidance from the ATO, not Treasury modelling, not audit logic, not enforcement, not compliance scoring, not legal advice, not tax advice, and not economic validation.
- They do not create notices, implement penalties, use statutory information-gathering powers, determine non-compliance, predict taxpayer behaviour, estimate behavioural elasticity, use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, estimate actual tax payable, or modify firm-level CARSF liability logic.

## V1.5 Pre-Build 21 Hardening Pass

Branch: `v1.5-pre-legislative-hardening`

Baseline: PR #21 merged into `main`, including the administrative compliance workflow shell.

Purpose of this build:

- Preserve subgroup metadata through weighted uncertainty and reviewed-scenario outputs where available.
- Clarify sector stress matrix automation-intensity explanations by separating digital, physical, decision, and compute metadata components.
- Tune behavioural response pressure-band spread across moderate, high, critical, and suppressed synthetic pathways.
- Add routine and enhanced administrative workflow demonstration rows before the future legislative architecture skeleton.

Tests run:

- `python -m pytest` - 605 passed, 1 pytest-asyncio deprecation warning.
- `python -m compileall -q model simulator scripts` - passed.
- Recursive YAML parse for `schedules/`, `examples/`, and `data/` - parsed 73 YAML files.
- Report runners passed: examples, sector schedule expansion, sector stress matrix, behavioural response simulation, administrative compliance workflow, evidence workflow, ingestion controls, investment guardrails, fiscal trajectory, transition funding, payment interactions, distributional scenarios, household weighting, uncertainty ranges, reviewed scenarios, and repo guardrails.
- Repo guardrails passed with zero denied findings.
- Bare Streamlit import probes passed for `simulator/app.py`, `simulator/pages/21_Sector_Stress_Matrix.py`, `simulator/pages/22_Behavioural_Response.py`, and `simulator/pages/23_Administrative_Workflow.py`.

Reports regenerated:

- `reports/uncertainty_ranges.json`
- `reports/uncertainty_ranges.md`
- `reports/reviewed_scenarios.json`
- `reports/reviewed_scenarios.md`
- `reports/sector_stress_matrix.json`
- `reports/sector_stress_matrix.md`
- `reports/behavioural_response_simulation.json`
- `reports/behavioural_response_simulation.md`
- `reports/administrative_compliance_workflow.json`
- `reports/administrative_compliance_workflow.md`

Limitations:

- This hardening pass is prototype-only and placeholder-only.
- It does not add legislative architecture, draft operative law, establish legal sufficiency, create real data, create compliance scoring, create enforcement, create notices, implement penalties, or modify firm-level CARSF liability.
- All affected outputs remain subject to external legal, tax, ATO-methods, Treasury-methods, privacy, calibration, methods, and administrative-design review before any real use.

## V1.5 Legislative Architecture Skeleton

Branch: `v1.5-legislative-architecture-skeleton`

Baseline: PR #22 merged into `main`, including the pre-Build 21 hardening pass.

Purpose of this build:

- Add a non-operative legislative architecture skeleton.
- Map CARSF concepts into proposed Parts, Divisions, definition placeholders, sector schedule placeholders, formula/liability placeholders, safe-harbour placeholders, anti-avoidance placeholders, grouped-entity and related-party placeholders, evidence and information placeholders, safeguards, regulation-making placeholders, commencement/transitional placeholders, and external-review blockers.
- Add legislative architecture data, model validation, reports, tests, CI step, documentation, and Streamlit page.

Reports generated:

- `reports/legislative_architecture.json`
- `reports/legislative_architecture.md`

Limitations:

- Legislative architecture outputs are non-operative mapping outputs only.
- They are not operative law, not a Bill, not legal drafting, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not Parliamentary Counsel drafting, not legally sufficient, and not constitutionally reviewed.
- They create no rights, obligations, statutory powers, information-gathering powers, notices, penalties, enforcement process, or compliance scoring.
- They do not determine tax payable, use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, or modify firm-level CARSF liability logic.

## V1.5 Executive Dashboard Consolidation

Branch: `v1.5-executive-dashboard-consolidation`

Baseline: PR #23 merged into `main`, including the legislative architecture skeleton.

Purpose of this build:

- Add a consolidated executive dashboard and report index for the CARSF V1.5 prototype stack.
- Map prototype layers, generated reports, Streamlit pages, non-claim profiles, calibration blockers, external-review blockers, suggested review navigation, and reviewer routing.
- Add dashboard manifest, model validation, reports, tests, CI step, documentation, and Streamlit page.

Reports generated:

- `reports/executive_dashboard.json`
- `reports/executive_dashboard.md`

Limitations:

- Executive dashboard outputs are prototype navigation and report-index outputs only.
- They are not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare advice, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, not a maturity score, not an official review pathway, not approval, and not validation.
- They do not determine actual tax payable, use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, or modify firm-level CARSF liability logic.

## V1.5 External Review Attack Pack

Branch: `v1.5-external-review-attack-pack`

Baseline: PR #25 merged into `main`, including the V1.5 working paper release-candidate pack.

Purpose of this build:

- Add a structured external review attack pack for the V1.5 release candidate.
- Provide policy, technical, legal, tax, ATO methods, Treasury methods, privacy/secrecy, statistical, economic, welfare, Parliamentary Counsel, and hostile/red-team challenge tracks.
- Add attack questions, failure modes, required external inputs, must-not-infer warnings, boundary checks, report attack matrix, layer attack matrix, release attack-pack documents, model validation, generated reports, tests, documentation, and CI step.

Reports generated:

- `reports/external_review_attack_pack.json`
- `reports/external_review_attack_pack.md`

Limitations:

- External review attack-pack outputs are challenge-organisation outputs only.
- They do not mean external review has been completed, do not mean approval has been granted, and do not mean validation has occurred.
- They are not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare validation, not statistical validation, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, not official status, and not an official review pathway.
- They do not determine actual tax payable, use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, or modify firm-level CARSF liability logic.

## V1.5 Final RC Integrity Seal

Branch: `v1.5-final-rc-integrity-seal`

Baseline: PR #26 merged into `main`, including the external review attack pack.

Purpose of this build:

- Add a final internal integrity seal for the V1.5 release candidate.
- Verify release documents, attack-pack documents, generated reports, required manifests, required scripts, digest metadata, non-claim boundaries, forbidden affirmative claim scanning, repo guardrail status expectations, CI expectations, and false readiness/legal/validation flags.
- Add seal manifest, model validation, release seal documents, generated reports, tests, documentation, and CI step.

Reports generated:

- `reports/v1_5_final_rc_integrity_seal.json`
- `reports/v1_5_final_rc_integrity_seal.md`
- `release/v1_5_rc/FINAL_RC_INTEGRITY_SEAL.json`
- `release/v1_5_rc/FINAL_RC_INTEGRITY_SEAL.md`
- `release/v1_5_rc/FINAL_RC_DIGESTS.json`

Limitations:

- Final RC integrity seal outputs are internal artefact integrity checks only.
- They are not approval, not validation, and do not mean external review has been completed.
- They are not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare validation, not statistical validation, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, not a maturity score, not official status, and not an official review pathway.
- They do not determine actual tax payable, use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, or modify firm-level CARSF liability logic.
