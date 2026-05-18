# Sector Stress Matrix

The sector stress matrix is a prototype metadata review layer for CARSF V1.5 schedules.

It compares placeholder sector schedules across automation intensity, QLC vulnerability, AAVA sensitivity, incidence risk, investment risk, avoidance / gaming risk, calibration difficulty, legal attribution difficulty, and display-control status.

## Inputs

The matrix reads schedule YAML files from `schedules/` and excludes `schedule_schema.yaml`.

The scoring uses schedule-internal placeholder metadata only, including:

- AII weights
- QLC weights
- cap placeholders
- avoidance controls
- calibration data requirements
- unresolved attribution and capital-base warning text
- cross-border, related-party, customer self-service, token-worker, software, platform, and intangible review wording

Automation intensity now preserves explanatory components separately:

- `digital_automation_emphasis`
- `physical_automation_emphasis`
- `decision_automation_emphasis`
- `compute_dependency_emphasis`
- `robotics_dependency_note`

These fields are interpretation aids only. They are not real sector scores and must not be used to rank schedules.

## Output Statuses

- `prototype_discussion_only`
- `show_with_warning`
- `strong_warning_required`
- `external_review_required`
- `do_not_rank`

Every row is marked `do_not_rank: true`.

## Non-Claims

The sector stress matrix is prototype metadata review only. It is not calibrated. It is not a real-world ranking of sectors. It is not Treasury modelling. It is not ATO guidance. It is not ABS/ATO/DSS/PBO analysis. It does not use real industry data. It does not estimate actual tax payable.

The matrix does not modify firm-level CARSF liability logic, does not implement legal sector attribution, does not implement real multi-schedule blending, and is not economic validation, investment advice, legal advice, or tax advice.

All schedules remain placeholder-only and subject to external calibration, legal review, and methods review.

## Run Command

```powershell
python scripts/run_sector_stress_matrix.py
```

Generated reports:

- `reports/sector_stress_matrix.md`
- `reports/sector_stress_matrix.json`

## Future Work

Future calibration must review the component method before any sector use. The current matrix remains metadata-only and do-not-rank.
