# CARSF V1.5 Uncertainty Range Mechanics

Generated at: `2026-05-20T02:07:23+00:00`

## A. Purpose

This report applies deterministic low/base/high placeholder ranges to synthetic household and weighted subgroup outputs.

## B. Non-Claims

- These are deterministic placeholder uncertainty ranges only. They are not statistical confidence intervals, forecasts, real uncertainty quantification, population estimates, ABS/HILDA/Census analysis, DSS/Services Australia modelling, Treasury modelling, PBO costing, welfare advice, eligibility law, legal advice, tax advice, or economic validation.
- This is a prototype deterministic range wrapper only; it is not Monte Carlo, calibration, forecasting, or statistical inference.
- Uncertainty range outputs do not modify firm-level CARSF liability.

## C. Why Uncertainty Ranges Matter

Point estimates can imply false precision. These deterministic ranges show where synthetic household and subgroup signals are stable, sensitive, or too fragile to interpret without external calibration.

## D. Low/Base/High Range Summary

| Example | Metric | Low | Base | High | Abs Width | Rel Width | Stability |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| Fragile Result Requires Calibration | residual_household_gap_after_support | 0.000 | 4,500.000 | 22,000.000 | 22,000.000 | 488.89% | fragile |
| Fragile Result Requires Calibration | transition_support_amount | 6,000.000 | 12,000.000 | 20,000.000 | 14,000.000 | 116.67% | fragile |
| Fragile Result Requires Calibration | support_loss | 0.000 | 6,000.000 | 18,000.000 | 18,000.000 | 300.00% | fragile |
| High Rent Low Savings Range | residual_household_gap_after_support | 6,000.000 | 13,000.000 | 24,000.000 | 18,000.000 | 138.46% | fragile |
| High Rent Low Savings Range | transition_support_amount | 10,000.000 | 16,000.000 | 20,000.000 | 10,000.000 | 62.50% | fragile |
| High Rent Low Savings Range | support_loss | 0.000 | 3,000.000 | 8,000.000 | 8,000.000 | 266.67% | fragile |
| Payment Support Low Mid High Range | residual_household_gap_after_support | 0.000 | 0.000 | 3,000.000 | 3,000.000 | N/A | not_assessable |
| Payment Support Low Mid High Range | transition_support_amount | 8,000.000 | 12,000.000 | 18,000.000 | 10,000.000 | 83.33% | fragile |
| Payment Support Low Mid High Range | expected_reemployment_months | 2.000 | 6.000 | 10.000 | 8.000 | 133.33% | fragile |
| Regional Re-Employment Delay Range | residual_household_gap_after_support | 8,000.000 | 14,000.000 | 26,000.000 | 18,000.000 | 128.57% | fragile |
| Regional Re-Employment Delay Range | transition_support_amount | 12,000.000 | 18,000.000 | 24,000.000 | 12,000.000 | 66.67% | fragile |
| Regional Re-Employment Delay Range | expected_reemployment_months | 24.000 | 36.000 | 48.000 | 24.000 | 66.67% | fragile |
| Regional Re-Employment Delay Range | regional_stress_score | 0.550 | 0.700 | 0.860 | 0.310 | 44.29% | moderately_sensitive |
| Single Parent Cost Pressure Range | residual_household_gap_after_support | 9,000.000 | 14,000.000 | 22,000.000 | 13,000.000 | 92.86% | fragile |
| Single Parent Cost Pressure Range | transition_support_amount | 15,000.000 | 18,000.000 | 22,000.000 | 7,000.000 | 38.89% | moderately_sensitive |
| Single Parent Cost Pressure Range | expected_reemployment_months | 12.000 | 18.000 | 24.000 | 12.000 | 66.67% | fragile |
| Weighted Subgroup Uncertainty Range | weighted_average_residual_gap | 7,000.000 | 9,000.000 | 12,000.000 | 5,000.000 | 55.56% | moderately_sensitive |
| Weighted Subgroup Uncertainty Range | weighted_average_residual_gap | 9,000.000 | 14,000.000 | 26,000.000 | 17,000.000 | 121.43% | fragile |
| Weighted Subgroup Uncertainty Range | weighted_high_or_critical_share | 0.800 | 1.000 | 1.000 | 0.200 | 20.00% | stable |
| Weighted Subgroup Uncertainty Range | weighted_high_or_critical_share | 0.750 | 1.000 | 1.000 | 0.250 | 25.00% | moderately_sensitive |

## E. Household Uncertainty Results

| Example | Scenario | Low Case | Base Case | High Case | Risk Signal Stability | Drivers |
| --- | --- | --- | --- | --- | --- | --- |
| Fragile Result Requires Calibration | ubi_lite_payment_cliff_case | low | high | critical | range_sensitive | household cost pressure, payment cliff, phase-out cliff placeholder, support phase-out, universal-lite support placeholder |
| High Rent Low Savings Range | single_adult_displaced_worker_high_rent | high | high | critical | stable_high_risk | essential cost pressure, high rent, low savings buffer, support level placeholder, support phase-out placeholder |
| Payment Support Low Mid High Range | young_worker_retraining_rebound | low | low | medium | stable_low_risk | payment support adequacy, retraining rebound placeholder, support amount placeholder |
| Regional Re-Employment Delay Range | older_worker_low_reemployment | high | high | critical | stable_high_risk | older-worker re-employment delay placeholder, re-employment delay, regional labour-market depth, support duration placeholder, transport access |
| Single Parent Cost Pressure Range | single_parent_retraining_gap | high | high | critical | stable_high_risk | childcare and basic costs, housing cost pressure, retraining delay, retraining duration, support adequacy placeholder |

## F. Weighted Subgroup Uncertainty Results

| Example | Subgroup | Scenario Count | Synthetic Weight | Matched Scenarios | Unmatched Scenarios | Not Population Estimate | Residual Gap Stability | High/Critical Share Stability | Subgroup Sensitivity |
| --- | --- | ---: | ---: | --- | --- | --- | --- | --- | --- |
| Weighted Subgroup Uncertainty Range | all_synthetic_households | 3 | 3.000 | dual_income_one_displaced_regional, single_adult_displaced_worker_high_rent, single_parent_retraining_gap | None | True | moderately_sensitive | stable | moderately_sensitive |
| Weighted Subgroup Uncertainty Range | critical_budget_stress | 1 | 1.000 | older_worker_low_reemployment | None | True | fragile | moderately_sensitive | fragile |
| Weighted Subgroup Uncertainty Range | regional_high_stress | 1 | 1.000 | None | high_automation_region_cluster | True | missing | missing | not_assessable |

## G. Stable High-Risk Signals

all_synthetic_households, critical_budget_stress, older_worker_low_reemployment, single_adult_displaced_worker_high_rent, single_parent_retraining_gap

## H. Range-Sensitive / Fragile Outputs

- Range-sensitive household count: 1
- Fragile metric count: 14
- Highest uncertainty items: critical_budget_stress:residual_gap_range, older_worker_low_reemployment:reemployment_months_range, older_worker_low_reemployment:residual_gap_range, older_worker_low_reemployment:transition_support_range, single_adult_displaced_worker_high_rent:payment_cliff_loss_range, single_adult_displaced_worker_high_rent:residual_gap_range, single_adult_displaced_worker_high_rent:transition_support_range, single_parent_retraining_gap:reemployment_months_range, single_parent_retraining_gap:residual_gap_range, ubi_lite_payment_cliff_case, ubi_lite_payment_cliff_case:payment_cliff_loss_range, ubi_lite_payment_cliff_case:residual_gap_range, ubi_lite_payment_cliff_case:transition_support_range, young_worker_retraining_rebound:reemployment_months_range, young_worker_retraining_rebound:transition_support_range

## I. Calibration Blockers

- household ranges are not calibrated
- weighted subgroup ranges are not representative
- no real ABS/HILDA/Census/DSS/Services Australia/Treasury/PBO data is used
- no statistical confidence intervals or forecasts are produced

## J. Plain-English Interpretation

### Fragile Result Requires Calibration

This case is intentionally fragile; the signal changes across low/base/high and should not be treated as a point estimate.

### High Rent Low Savings Range

The high-rent case checks whether residual hardship remains visible when support and cliff assumptions vary.

### Payment Support Low Mid High Range

The young-worker case tests whether a lower-stress scenario remains low or medium under deterministic support ranges.

### Regional Re-Employment Delay Range

The regional older-worker case tests whether risk remains visible when re-employment timing and regional stress are varied.

### Single Parent Cost Pressure Range

The single-parent case remains high risk across the placeholder residual-gap range, but the range is still not calibrated.

### Weighted Subgroup Uncertainty Range

Weighted subgroup uncertainty checks whether stress-test subgroup signals remain visible across deterministic placeholder ranges.

## K. Limitations and Future Calibration Needs

- Low/base/high values are deterministic placeholders, not Monte Carlo outputs or confidence intervals.
- Stable high-risk signals still require external validation before policy use.
- Fragile outputs require calibration before they should be interpreted.
- No real household, ABS, HILDA, Census, DSS, Services Australia, ATO, Treasury, PBO, welfare, income, or survey data is used.
- Firm-level CARSF liability is not automatically modified by uncertainty range outputs.
