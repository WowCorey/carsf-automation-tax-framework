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
