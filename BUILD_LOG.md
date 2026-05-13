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
