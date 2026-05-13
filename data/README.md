# CARSF Data Directory

This directory is a placeholder for future data governance material only.

No datasets are stored here. No restricted data, personal data, tax file numbers, payroll extracts, ATO data, DSS data, HILDA data, HELP/HECS data, superannuation data, state payroll tax data, or private business records should be committed to this repository.

The current files define the source categories required for future calibration and review.
Synthetic mock packets under `mock_evidence/` exist only to test workflow states. They are not real evidence and must not contain personal data, restricted data, real taxpayer data, or real business records.
Mock ingestion requests under `mock_ingestion_requests/` test default-deny ingestion controls. They are synthetic fixtures only.

## Files

- `source_registry.yaml` - prototype registry of future data-source categories.
- `placeholder_policy.md` - rules for separating placeholders from calibratable inputs.
- `mock_evidence/` - synthetic mock evidence packet fixtures for workflow testing only.
- `mock_ingestion_requests/` - synthetic request fixtures for ingestion-control testing only.

## Prohibited Local Evidence Folders

The repository ignores likely real-evidence paths such as `data/incoming/`, `data/private/`, `data/restricted/`, and `data/real_evidence/`. These folders are intentionally not used by the prototype.

## Non-Claims

This directory does not contain legal, tax, Treasury, ATO, ABS, Fair Work, OECD, BEPS, audit, forensic, or economic validation.
