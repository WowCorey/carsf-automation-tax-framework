# CI Enforcement

Status: V1.5 prototype CI guardrail integration.

## Purpose

CI now runs the repository guardrail scan so likely evidence leaks, secret markers, wrong storage zones, and unsafe generated report content can block a pull request before merge.

## CI Steps

The workflow in `.github/workflows/ci.yml` runs:

- `python -m pytest`
- `python -m compileall -q model simulator scripts`
- recursive YAML parsing for `schedules/`, `examples/`, and `data/`
- `python scripts/run_examples.py`
- `python scripts/run_evidence_workflow.py`
- `python scripts/run_ingestion_controls.py`
- `python scripts/run_repo_guardrails.py`

CI fails if `scripts/run_repo_guardrails.py` reports denied findings.

## Limitations

The CI guardrail is not a complete DLP system, secret scanner, cybersecurity product, legal/privacy audit, Treasury control, ATO control, or forensic validation. It is an over-blocking repository-level prototype check.

Future external evidence handling would require secure infrastructure, real access controls, formal retention/deletion controls, secret scanning, DLP tooling, legal/privacy review, and audit governance outside this repository.
