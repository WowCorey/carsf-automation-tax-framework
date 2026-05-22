# Full Repo Integrity Upgrade Audit

Build 34.5 adds a full repo integrity audit, bug-check register, result-coverage matrix, missing-factor register, data-dependency register, and external-review dependency register for CARSF V1.5.

This is a full repo integrity audit only. No new data is loaded by this build. This is not calibration. This does not fake missing data, does not calibrate the model, does not validate the model, does not prove the model works, does not determine actual tax payable, and does not modify firm-level CARSF liability.

The audit checks runners, reports, JSON outputs, manifests, dashboard references, CI wiring, documentation links, public-data boundaries, placeholder boundaries, calibration boundaries, scenario constraints, guardrails, and non-claim language. It identifies safe internal fixes where possible and records data or review gaps when a fix would require restricted data, private data, legal judgement, tax judgement, economic review, statistical review, public finance review, welfare review, domain review, or data governance review.

## Generated Reports

- `reports/full_repo_integrity_upgrade_audit.md`
- `reports/full_repo_integrity_upgrade_audit.json`

## Safe Fixes Covered

- CI YAML parsing includes `release/` alongside `schedules/`, `examples/`, and `data/`.
- The full repo audit runner is included in CI before repository guardrails.
- The full repo audit reports are referenced from release, report-map, and dashboard manifests.
- Documentation cross-links make the audit discoverable before the next reviewer handoff pack.

## Non-Claims

- This is a full repo integrity audit only.
- No new data is loaded by this build.
- This does not fake missing data.
- This does not calibrate the model.
- This does not validate the model.
- This does not prove the model works.
- This does not determine actual tax payable.
- This does not modify firm-level CARSF liability.
- Missing factors requiring data or review remain blocked.
- Public aggregate values remain boundary-limited.
- Placeholders remain placeholders unless already mapped otherwise.
- Scenario constraints remain constraints, not validation.
- This is not legal advice, tax advice, ATO guidance, Treasury modelling, PBO costing, economic validation, welfare validation, statistical validation, operational readiness, legal sufficiency, or official status.

## Seal Boundary

Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-34.5 are included in a later sealed RC.
