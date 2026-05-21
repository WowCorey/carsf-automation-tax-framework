# Public Real Raw Data Staging

This directory is reserved for manually saved public aggregate files if a later build needs them.

Build 31 does not commit raw downloaded datasets. It records small public aggregate/source-located values in `data/public_real/manifests/public_real_data_sources.yaml` and writes parsed values to `data/public_real/parsed/public_real_aggregate_values.json`.

This directory must not contain restricted data, personal data, taxpayer-level data, firm-confidential data, household microdata, ABS DataLab microdata, HILDA microdata, DSS/Services Australia records, ATO taxpayer records, confidential Treasury/PBO material, private payroll records, bank records, pay records, tax file identifiers, or any other confidential source material.

Public aggregate data does not equal calibration, validation, legal advice, tax advice, ATO guidance, Treasury modelling, PBO costing, official status, operational readiness, legal sufficiency, actual tax payable, or firm-level CARSF liability logic.
