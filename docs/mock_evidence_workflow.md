# Mock Evidence Workflow

Status: V1.5 prototype workflow scaffolding.

## Purpose

The mock evidence workflow shows how a CARSF example could move from placeholder-only modelling into a reviewed prototype state using synthetic evidence packets. It tests packet loading, validation, evidence summaries, privacy/secrecy classification, and review-state transitions.

## Fixture Rule

Every fixture in `data/mock_evidence/` must include:

```yaml
synthetic_mock_evidence_only: true
```

The fixtures contain no real evidence, no personal data, no restricted government data, no real taxpayer data, and no real business records.

## Review States

Prototype states include `placeholder_only`, `submitted_mock`, `incomplete`, `partial`, `sufficient_for_prototype`, `rejected`, `needs_legal_review`, `needs_tax_review`, `needs_privacy_review`, `needs_calibration`, and `locked_for_external_review`.

These are workflow states only. They do not create real-world sufficiency, approval, validation, or liability outcomes.

## Reports

Run:

```powershell
python scripts/run_evidence_workflow.py
```

Generated reports:

- `reports/mock_evidence_workflow.md`
- `reports/mock_evidence_workflow.json`

## Non-Claims

These packets are synthetic mock evidence only. They do not validate any real liability, tax position, audit finding, legal conclusion, Treasury assessment, ATO assessment, or economic claim.

Future real evidence handling would require strict privacy, secrecy, legal, ATO/Treasury, data-owner, and governance controls before any external use.
