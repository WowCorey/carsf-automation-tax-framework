# CARSF V1.5 Public Data Pilot Consistency Audit

This is an internal consistency audit and source-reconciliation map only. No new data is loaded by this build. It does not externally verify source values, scrape public sources, or call external APIs.

It is not calibration. Calibration has not been completed. Public data does not prove the model works. Reconciled means internally consistent only. Reconciled does not mean validated or official. Realistic placeholders remain placeholders. Realistic placeholders are not real data and are not calibrated. Source references are not loaded datasets. Restricted-data requirements are not data access.

It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, and not official status. It does not determine actual tax payable, does not use taxpayer-level data, firm-level confidential data, household microdata, ABS DataLab, HILDA microdata, DSS/Services Australia records, ATO taxpayer records, Treasury/PBO confidential material, or restricted government data, and does not modify firm-level CARSF liability.

## What It Audits

- Source-reference-to-extract consistency.
- Loaded-public-extract to evidence-map consistency.
- Source-reference-only count separation.
- Fair Work minimum wage arithmetic: `24.95 * 38 = 948.10`.
- Placeholder-anchor boundaries.
- Module `calibration_possible: false` boundaries.
- Restricted-data blocker preservation.
- Forbidden repo-data rule preservation.
- Public-pilot digest stability and self-hash exclusion.
- Public-pilot report and evidence-map JSON count agreement.
- Streamlit dashboard source consistency.
- Non-claim boundary language and forbidden affirmative claim scanning.

## Commands

```bash
python scripts/run_public_data_pilot.py
python scripts/run_public_data_evidence_map.py
python scripts/run_public_data_consistency_audit.py
```

Generated reports:

- `reports/public_data_consistency_audit.md`
- `reports/public_data_consistency_audit.json`

Dashboard section:

- `simulator/pages/29_Public_Data_Evidence_Map.py`

## Build 29.5 Source-Locator Pack

Build 29.5 uses the consistency audit as an input to create source-locator cards and reviewer checklists. It does not load new data, add new public values, scrape sources, call APIs, externally verify source values, complete calibration, validate CARSF, determine actual tax payable, or modify firm-level CARSF liability.

Build 29.6 uses the consistency audit as one input to create likely reviewer objections and honest responses. It does not load new data, add new public values, scrape sources, call APIs, externally verify source values, complete calibration, validate CARSF, determine actual tax payable, claim objections are resolved, or modify firm-level CARSF liability.

Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-29.6 are included in a later sealed RC.
