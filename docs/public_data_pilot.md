# Public Data Pilot and Placeholder Anchor Layer

This is a public aggregate-data pilot and realistic-placeholder anchor layer only. It may include small public aggregate extracts or source-reference records. It is not calibration, calibration has not been completed, public data extracts do not prove the model works, public data does not prove the model works, realistic placeholders remain placeholders, realistic placeholders remain realistic placeholders, source references are not loaded datasets, and restricted-data requirements are not data access.

This is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, and not official status. It does not determine actual tax payable, does not use taxpayer-level data, firm-level confidential data, household microdata, ABS DataLab microdata, HILDA microdata, DSS/Services Australia records, ATO taxpayer records, Treasury/PBO confidential material, or restricted government data. It does not modify firm-level CARSF liability.

## Scope

Build 27 tests whether the repo can safely carry small public aggregate/source-reference records and realistic placeholder anchors. It keeps four categories separate:

- loaded public aggregate extracts
- source-reference-only records
- realistic placeholder anchors
- restricted-data blockers and forbidden repo data

The layer writes:

- `reports/public_data_pilot.md`
- `reports/public_data_pilot.json`
- `data/public_pilot/digests/public_data_pilot_digests.json`

Build 29 adds an internal consistency audit over these artefacts at `reports/public_data_consistency_audit.md` and `reports/public_data_consistency_audit.json`. The audit loads no new data, does not externally verify source values, and does not claim calibration, validation, official status, actual tax payable, ATO guidance, Treasury modelling, PBO costing, or firm-level liability changes.

## Public Sources

The pilot uses small source-referenced records from public pages for wage, tax aggregate, fiscal aggregate, superannuation, HELP, payroll-tax, and ABS labour-source contexts. Source-reference-only records do not count as loaded public data.

Loaded public extracts are limited to small values that are manually inspectable and safe to commit as public aggregate or public threshold records. They are sanity-check-only or placeholder-anchor-only inputs.

## Placeholder Anchors

Public extracts may make some placeholders more realistic, but they do not complete calibration. Placeholder anchors must remain labelled as realistic placeholders and must not be labelled as real data or calibrated data.

## Blockers

The following remain blocked outside this repository:

- confidential tax records
- firm confidential records
- person-level records
- household microdata
- restricted government data
- confidential Treasury or PBO material

## Next Step

Build 28 exposes the public-data pilot outputs in a reviewer-facing evidence map and Streamlit dashboard. It shows which assumptions are source-referenced, which are public-aggregate anchored, which remain realistic placeholders, and which remain blocked by restricted data without loading new data or claiming calibration, validation, approval, readiness, actual tax payable, legal sufficiency, official status, or implementation readiness.

Build 29 adds source-reconciliation and internal consistency checks across the public-data pilot and evidence-map reports.

Build 29.5 adds a source-locator verification pack over existing Build 27-29 artefacts. It creates manual-review cards and checklists only. It loads no new data, adds no source values, does not externally verify source values, does not complete calibration, does not prove the model works, does not determine actual tax payable, and does not modify firm-level CARSF liability.

Build 29.6 adds a red-team reviewer objections pack over existing Build 26-29.5 artefacts. It lists likely reviewer criticisms and honest responses only. It loads no new data, adds no public values, does not externally verify source values, does not complete calibration, does not prove the model works, does not determine actual tax payable, does not claim objections are resolved, and does not modify firm-level CARSF liability.

Build 31 adds a controlled public real aggregate-data loader over existing source-located public-pilot values. It records parsed public aggregate values and digest metadata only. Public aggregate data does not equal calibration, does not prove the model works, does not determine actual tax payable, and does not modify firm-level CARSF liability.

Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-31 are included in a later sealed RC.
## Build 32 Placeholder Replacement Follow-On

Build 32 maps Build 31 loaded public aggregate values back to the public-pilot placeholder anchors. It loads no new data and does not change the Build 27 boundary: public aggregate values can support anchor, bound, or context labels only. They do not complete calibration, validate CARSF, prove the model works, determine actual tax payable, create official status, or modify firm-level CARSF liability.

## Build 33 Calibration Boundary Follow-On

Build 33 defines module-level and field-level boundaries for the same public aggregate values and placeholder decisions. It loads no new data and keeps public aggregate uses limited to sanity checks, anchors, bounds, context, placeholder narrowing, and reviewer traceability. It does not complete calibration, validate CARSF, determine actual tax payable, create legal sufficiency, create official status, or modify firm-level CARSF liability.
Build 34 uses the later boundary and scenario constraint layers to prevent public-pilot outputs from being overread as calibration, validation, tax-payable estimates, legal sufficiency, official status, or implementation readiness.
