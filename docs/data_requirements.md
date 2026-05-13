# Data Requirements

## Confirmed Baseline Figures

Confirmed baseline figures must come from official sources such as Treasury, PBO, ABS, ATO, DSS, Services Australia, Fair Work, or state and territory Treasuries. Each figure needs a source, date, and use case.

## Required Calibration Inputs

- ATO income tax and company tax data by sector, occupation, firm size, and entity group.
- ABS labour force, industry output, productivity, and business characteristics data.
- HILDA longitudinal wage, re-employment, underemployment, and career-scarring data.
- DSS and Services Australia transfer-system data.
- HELP repayment data and superannuation guarantee contribution effects.
- State payroll tax, TAFE, health, housing, and regional transition data.
- Industry automation adoption data, robotics capital data, compute-spend data, and automated-decision counts.

## Current Repository Values

The schedules and examples in this repository use illustrative placeholder values only. They are intended to test formula mechanics and red-team behaviour, not to estimate real Australian fiscal exposure.

## Source Registry

The prototype source registry lives at `data/source_registry.yaml`. It lists future source categories only. No datasets have been collected, downloaded, or committed.

## Evidence and Calibration Reports

Run:

```powershell
python scripts/run_examples.py
```

Then review:

- `reports/evidence_requirements.md`
- `reports/evidence_requirements.json`
- `reports/calibration_requirements.md`
- `reports/calibration_requirements.json`

These reports do not validate evidence, liability, law, tax, Treasury, ATO, ABS, Fair Work, OECD/BEPS, audit, forensic, or economic claims.
