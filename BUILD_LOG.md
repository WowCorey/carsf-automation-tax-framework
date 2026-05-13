# Build Log

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
