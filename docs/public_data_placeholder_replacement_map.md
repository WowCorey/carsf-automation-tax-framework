# Public Data Placeholder Replacement Map

## Purpose

Build 32 maps the Build 31 loaded public aggregate values to existing CARSF realistic placeholders. It classifies each placeholder as replaced by public aggregate anchor, narrowed by public aggregate anchor, informed by public aggregate anchor, still placeholder-only, blocked until restricted data, blocked until external review, or unable to be replaced by public aggregate data.

## Non-Claims

This is a public data placeholder replacement map only. No new data is loaded by this build. Public aggregate data can anchor or narrow some placeholders, but does not calibrate the model. Replaced by public aggregate anchor does not mean validated. Narrowed by public aggregate anchor does not mean statistically estimated. Informed by public aggregate anchor does not mean representative. Placeholder-only items remain placeholders. Restricted-data blockers remain blockers. Calibration has not been completed. Public data does not prove the model works. This is not validation, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, and not official status. It does not determine actual tax payable and does not modify firm-level CARSF liability.

## Artefacts

- `data/public_real/manifests/public_placeholder_replacement_manifest.yaml`
- `model/carsf/public_data_placeholder_replacement_map.py`
- `scripts/run_public_data_placeholder_replacement_map.py`
- `reports/public_data_placeholder_replacement_map.md`
- `reports/public_data_placeholder_replacement_map.json`

## Mapping Behaviour

- Fair Work wage values can replace or narrow labour wage anchor placeholders, but are not representative of all labour costs and do not calibrate automation substitution.
- ATO corporate transparency values can inform corporate tax scale context, but cannot determine firm-level CARSF liability, avoidance, compliance, automation exposure, or actual tax payable.
- ATO taxation statistics and Budget Paper receipt values can narrow fiscal-scale placeholder discussion, but cannot infer taxpayer behaviour, CARSF revenue, Treasury modelling, PBO costing, or fiscal sufficiency.
- The superannuation guarantee rate can anchor contribution/payment context, but cannot estimate individual superannuation, payroll, employer behaviour, or ATO guidance.
- HELP, Queensland payroll tax, and ABS labour source candidates remain not loaded and future-only until safe public values are loaded or reviewed.

## Integrity Boundary

Build 33 adds a public aggregate calibration-boundary map over these replacement decisions. It defines allowed uses for sanity checks, anchors, bounds, context, placeholder narrowing, and reviewer traceability only. It does not load new data, perform calibration, claim validation, determine actual tax payable, or modify firm-level CARSF liability.

Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-33 are included in a later sealed RC.
Build 34 constrains scenario outputs that use these placeholder replacement decisions. Replacement, narrowing, and context labels remain display constraints only; they do not calibrate or validate CARSF and do not determine actual tax payable.

Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-34 are included in a later sealed RC.
