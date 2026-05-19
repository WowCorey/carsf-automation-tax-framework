# Real Data Feasibility and Calibration Intake Map

This is a feasibility and calibration-intake map only. No real data has been loaded by this build. No calibration has occurred. Realistic placeholders are not real data and are not calibrated. Public-data candidates are not loaded datasets. Restricted-data requirements are not data access.

It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, not official status, and does not determine actual tax payable. It does not use taxpayer-level, firm-level confidential, household microdata, ABS DataLab, HILDA microdata, DSS/Services Australia records, ATO records, Treasury/PBO confidential material, or restricted government data. It does not modify firm-level CARSF liability.

## Purpose

Build 26 adds a real-data feasibility and calibration-intake map for the V1.5 release candidate. It separates:

- public aggregate data candidates that may be suitable for a future Build 27 pilot;
- restricted or confidential data requirements that cannot enter the repository;
- realistic placeholders that can be anchored only as placeholder context;
- synthetic fixtures that remain discussion and test artefacts only;
- forbidden repo data such as taxpayer records, firm-confidential records, household microdata, real evidence packets, and unauthorised records;
- module-level blockers and review routes.

## Artefacts

- `data/calibration/real_data_feasibility_map.yaml`
- `model/carsf/real_data_feasibility.py`
- `scripts/run_real_data_feasibility.py`
- `reports/real_data_feasibility.md`
- `reports/real_data_feasibility.json`

Run:

```powershell
python scripts/run_real_data_feasibility.py
```

## Build 27 Boundary

Build 27 may load a small public aggregate-data pilot only after public licence/source handling is checked. Loaded public aggregates must remain separate from realistic placeholders and restricted-data needs. The Build 26 map does not load datasets and does not create calibration values.

Build 25 sealed the previous RC state. If Build 26 becomes part of a later sealed RC, the final RC integrity seal must be regenerated for that new state; the prior seal should not be described as covering Build 26.

## Build 27 Update

Build 27 adds `data/public_pilot/`, `model/carsf/public_data_pilot.py`, `scripts/run_public_data_pilot.py`, `reports/public_data_pilot.md`, `reports/public_data_pilot.json`, and `data/public_pilot/digests/public_data_pilot_digests.json`.

The Build 27 pilot may include small public aggregate extracts and source-reference records, but it is not calibration. Calibration has not been completed. Public data extracts do not prove the model works. Realistic placeholders remain placeholders, source references are not loaded datasets, and restricted-data requirements are not data access. No taxpayer-level, firm-level confidential, household microdata, ABS DataLab, HILDA microdata, DSS/Services Australia records, ATO taxpayer records, confidential Treasury/PBO material, restricted government data, or real evidence is committed.

Build 25 sealed the previous RC state. A new integrity seal must be regenerated if Build 27 is included in a later sealed RC.
