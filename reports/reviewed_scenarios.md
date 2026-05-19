# CARSF V1.5 Reviewed Scenario Comparison Layer

Generated at: `2026-05-19T00:02:08+00:00`

## A. Purpose

This report classifies deterministic synthetic uncertainty outputs into prototype display-control categories. It separates discussion-ready signals from fragile, range-sensitive, missing-range, or non-interpretable outputs.

## B. Non-Claims

- Reviewed scenario outputs are prototype display-control signals only. They are not statistical validation, population estimates, real household modelling, ABS/HILDA/Census analysis, DSS/Services Australia modelling, ATO analysis, Treasury modelling, PBO costing, welfare advice, eligibility law, legal advice, tax advice, or economic validation.
- Stable prototype discussion signals still require external calibration and methods review.
- Reviewed scenario outputs do not modify firm-level CARSF liability.
- Reviewed scenario outputs are not population representative.
- Fragile or missing-range outputs must not be presented as clean point estimates.

## C. Review Category Rules

- Stable high-risk or stable low-risk household signals can be shown with warnings when primary metrics are not fragile.
- Stable household signals with fragile primary metrics are discussion signals only with strong warnings.
- Range-sensitive household outputs hide point estimates.
- Missing or non-assessable required ranges are hidden until calibrated or routed to external review.
- Weighted subgroup outputs are always marked non-representative of a real population.
- Fragile weighted subgroup ranges suppress point estimates.

### Summary Counts

- Prototype discussion signals: 1
- Discussion with strong warning: 3
- Range-sensitive hidden point estimates: 1
- Fragile suppressed point estimates: 1
- Non-interpretable outputs: 1
- Missing uncertainty range outputs: 1
- External review required outputs: 8

## D. Household Scenario Review Table

| Scenario | Risk Signal Stability | Low Case | Base Case | High Case | Fragile Metrics | Review Category | Display Level | Main Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Fragile Result Requires Calibration | range_sensitive | low | high | critical | residual_household_gap_after_support, support_loss, transition_support_amount | range_sensitive_do_not_use_as_point_estimate | hide_point_estimate | Low/base/high cases cross risk bands, so the point estimate should not be used. |
| High Rent Low Savings Range | stable_high_risk | high | high | critical | residual_household_gap_after_support, support_loss, transition_support_amount | discussion_with_strong_warning | show_with_warning | Stable high-risk signal exists, but primary uncertainty metrics include fragile ranges. |
| Payment Support Low Mid High Range | stable_low_risk | low | low | medium | expected_reemployment_months, transition_support_amount | non_interpretable_until_calibrated | hide_until_calibrated | One or more required household uncertainty ranges is not assessable without calibration. |
| Regional Re-Employment Delay Range | stable_high_risk | high | high | critical | expected_reemployment_months, residual_household_gap_after_support, transition_support_amount | discussion_with_strong_warning | show_with_warning | Stable high-risk signal exists, but primary uncertainty metrics include fragile ranges. |
| Single Parent Cost Pressure Range | stable_high_risk | high | high | critical | expected_reemployment_months, residual_household_gap_after_support | discussion_with_strong_warning | show_with_warning | Stable high-risk signal exists, but primary uncertainty metrics include fragile ranges. |

## E. Weighted Subgroup Review Table

| Subgroup | Scenario Count | Synthetic Weight | Not Population Estimate | Residual Gap Stability | High/Critical Share Stability | Subgroup Sensitivity | Representative of Real Population | Review Category | Display Level | Main Reason |
| --- | ---: | ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| All Synthetic Households | 3 | 3.000 | True | moderately_sensitive | stable | moderately_sensitive | False | prototype_discussion_signal | show_with_warning | Required subgroup ranges are stable or moderately sensitive and no required range is missing. |
| Critical Budget Stress | 1 | 1.000 | True | fragile | moderately_sensitive | fragile | False | fragile_suppress_point_estimate | hide_point_estimate | Weighted subgroup range sensitivity is fragile; suppress the point estimate. |
| High Regional Stress | 1 | 1.000 | True | N/A | N/A | not_assessable | False | missing_uncertainty_range | external_review_only | Required weighted subgroup uncertainty range is missing. |

## F. Prototype Discussion Signals

### Show With Warning

- All Synthetic Households: `prototype_discussion_signal` / `show_with_warning` - Required subgroup ranges are stable or moderately sensitive and no required range is missing.

### Strong Warning

- High Rent Low Savings Range: `discussion_with_strong_warning` / `show_with_warning` - Stable high-risk signal exists, but primary uncertainty metrics include fragile ranges.
- Regional Re-Employment Delay Range: `discussion_with_strong_warning` / `show_with_warning` - Stable high-risk signal exists, but primary uncertainty metrics include fragile ranges.
- Single Parent Cost Pressure Range: `discussion_with_strong_warning` / `show_with_warning` - Stable high-risk signal exists, but primary uncertainty metrics include fragile ranges.

## G. Suppressed / Hidden Point Estimates

### Hidden or Suppressed

- Fragile Result Requires Calibration: `range_sensitive_do_not_use_as_point_estimate` / `hide_point_estimate` - Low/base/high cases cross risk bands, so the point estimate should not be used.
- Critical Budget Stress: `fragile_suppress_point_estimate` / `hide_point_estimate` - Weighted subgroup range sensitivity is fragile; suppress the point estimate.
- High Regional Stress: `missing_uncertainty_range` / `external_review_only` - Required weighted subgroup uncertainty range is missing.

## H. Non-Interpretable Outputs

### Non-Interpretable

- Payment Support Low Mid High Range: `non_interpretable_until_calibrated` / `hide_until_calibrated` - One or more required household uncertainty ranges is not assessable without calibration.
- High Regional Stress: `missing_uncertainty_range` / `external_review_only` - Required weighted subgroup uncertainty range is missing.

## I. Missing Calibration / External Review Blockers

- Critical Budget Stress
- Fragile Result Requires Calibration
- High Regional Stress
- Payment Support Low Mid High Range

## J. Plain-English Interpretation

This layer is a review screen for presentation discipline. It keeps stable synthetic signals visible with warnings, hides point estimates where low/base/high cases are unstable, and routes missing or non-assessable uncertainty outputs away from policy interpretation until external calibration and methods review exists.

## K. Limitations and Future Review Needs

- This is synthetic only and placeholder only.
- It is not statistical validation, confidence intervals, forecasting, real distributional modelling, or population estimation.
- It is not ABS/HILDA/Census analysis, DSS/Services Australia modelling, ATO analysis, Treasury modelling, or PBO costing.
- It is not welfare advice, eligibility law, legal advice, tax advice, or economic validation.
- Stable prototype discussion signals still require external calibration and methods review.
- Firm-level CARSF liability is not modified.
