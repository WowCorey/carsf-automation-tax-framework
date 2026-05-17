# Reviewed Scenario Comparison Layer

The reviewed scenario comparison layer is a prototype display-control screen for deterministic synthetic uncertainty outputs.

It answers which synthetic household and weighted subgroup signals can be shown for prototype policy discussion, which must carry strong warnings, which point estimates should be hidden, and which outputs are non-interpretable until external calibration and methods review exists.

## What It Reviews

- household uncertainty outputs from `model/carsf/distributional_uncertainty.py`
- weighted subgroup uncertainty outputs from `model/carsf/weighted_uncertainty.py`
- fragile low/base/high range mechanics
- missing required uncertainty ranges
- non-representative subgroup outputs
- zero-weight or unmatched subgroup outputs
- available subgroup metadata, including scenario counts, synthetic weights, subgroup filters, matched scenarios, and unmatched scenarios

## Display Categories

- `prototype_discussion_signal`
- `discussion_with_strong_warning`
- `range_sensitive_do_not_use_as_point_estimate`
- `fragile_suppress_point_estimate`
- `non_interpretable_until_calibrated`
- `missing_uncertainty_range`
- `external_review_required`

## Display Levels

- `show`
- `show_with_warning`
- `deemphasise`
- `hide_point_estimate`
- `hide_until_calibrated`
- `external_review_only`

The current implementation uses the warning and hiding levels to prevent fragile synthetic outputs from being presented as clean findings.

## Non-Claims

Reviewed scenario outputs are prototype display-control signals only. They are not statistical validation, population estimates, real household modelling, ABS/HILDA/Census analysis, DSS/Services Australia modelling, ATO analysis, Treasury modelling, PBO costing, welfare advice, eligibility law, legal advice, tax advice, or economic validation.

Stable prototype discussion signals still require external calibration and methods review. This layer does not modify firm-level CARSF liability.

## Run Command

```powershell
python scripts/run_reviewed_scenarios.py
```

Generated reports:

- `reports/reviewed_scenarios.md`
- `reports/reviewed_scenarios.json`

## Future Work

Future review should keep subgroup metadata visible wherever weighted subgroup outputs are displayed, while preserving the non-representative and not-population-estimate warnings.
