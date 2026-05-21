# CARSF V1.5 Public Real Aggregate Data Loader

This loads real public aggregate data only. It does not load restricted data, personal data, taxpayer-level data, firm-confidential data, or household microdata.

Public aggregate data does not equal calibration. Calibration has not been completed. Public data does not prove the model works. This is not validation, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, and not official status. It does not determine actual tax payable and does not modify firm-level CARSF liability.

## What It Adds

- A public real-data source manifest at `data/public_real/manifests/public_real_data_sources.yaml`.
- A parsed public aggregate value file at `data/public_real/parsed/public_real_aggregate_values.json`.
- Digest metadata at `data/public_real/digests/public_real_data_digests.json`.
- A loader runner at `scripts/run_public_real_data_loader.py`.
- Generated reports at `reports/public_real_data_loader.md` and `reports/public_real_data_loader.json`.

## Loaded Public Aggregate Values

Build 31 loads only values already represented in the public-pilot source-locator chain: Fair Work minimum wage thresholds, ATO public corporate/taxation aggregate summaries, Budget Paper receipt aggregates, and the super guarantee public rate setting.

HELP/HECS, Queensland payroll tax, and ABS labour aggregate references remain `source_candidate_not_loaded` because exact safe local values are not recorded in this build.

## Guardrails

Loaded sources must be public, aggregate-level, non-personal, non-confidential, source-located, and safe for repository use. The loader fails closed on restricted data, personal data, taxpayer-level data, firm-confidential data, household microdata, missing source URL, missing source locator, missing licence/access note, or missing value/unit/period/geography metadata.

## Runner

Run:

```bash
python scripts/run_public_real_data_loader.py
```

## Current Limits

The loader is not a calibrated model. It does not externally verify source values, does not scrape sources, does not call external APIs, does not determine actual tax payable, does not create official status, and does not change firm-level CARSF liability.

Build 32 uses these loaded public aggregate values to map placeholder replacement, narrowing, and context decisions. It loads no new data and does not convert public aggregate anchors into calibration, validation, actual tax payable, official status, legal sufficiency, Treasury modelling, ATO guidance, PBO costing, or firm-level CARSF liability logic.

Build 33 uses these loaded public aggregate values to define allowed boundary uses across modules and fields. Allowed uses are limited to sanity checks, public aggregate anchors, public aggregate bounds, contextual references, placeholder narrowing, and reviewer traceability. It loads no new data and does not perform calibration, claim validation, determine actual tax payable, create official status, or modify firm-level CARSF liability.

Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-33 are included in a later sealed RC.
