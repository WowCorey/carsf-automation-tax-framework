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

Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-29.5 are included in a later sealed RC.
