# CARSF V1.5 Synthetic Household Distributional Scenarios

Generated at: `2026-05-18T11:03:55+00:00`

## A. Purpose

This report previews synthetic household-level distributional stress for placeholder automation displacement scenarios.

## B. Non-Claims

- These are synthetic household distributional scenarios only. They are not real household modelling, welfare advice, eligibility law, DSS/Services Australia modelling, ABS analysis, Treasury modelling, PBO costing, legal advice, tax advice, or economic validation.
- All household, regional, re-employment, payment cliff, and support values are illustrative placeholders.
- Synthetic distributional scenario outputs do not modify firm-level CARSF liability.

## C. Why Distributional Scenarios Matter

National fiscal and transition-payment outputs can hide differences between household types. These synthetic scenarios show how composition, savings buffers, re-employment timing, payment cliffs, and regional stress may change household shock severity. They are not representative household modelling.

## D. Synthetic Household Table

| Scenario | Household Type | Adults | Children | Region | Income Band | Pre-Income | Post-Income |
| --- | --- | ---: | ---: | --- | --- | ---: | ---: |
| Dual Income One Displaced Regional | dual_income_one_worker_displaced | 2 | 1 | regional_labour_market_placeholder | middle_placeholder | 120,000.00 | 78,000.00 |
| High Automation Region Cluster | displaced_worker_high_exposure_region | 2 | 2 | high_automation_regional_cluster_placeholder | middle_placeholder | 90,000.00 | 20,000.00 |
| Older Worker Low Re-Employment | older_worker_single_adult | 1 | 0 | mature_industrial_region_placeholder | middle_placeholder | 80,000.00 | 15,000.00 |
| Single Adult Displaced Worker High Rent | single_adult_displaced_worker | 1 | 0 | high_rent_metro_placeholder | lower_middle_placeholder | 65,000.00 | 10,000.00 |
| Single Parent Retraining Gap | single_parent_retraining_delay | 1 | 2 | outer_suburban_placeholder | lower_middle_placeholder | 70,000.00 | 12,000.00 |
| UBI-Lite Payment Cliff Case | single_adult_phase_out_review | 1 | 0 | mixed_metro_placeholder | lower_middle_placeholder | 60,000.00 | 30,000.00 |
| Young Worker Retraining Rebound | young_single_worker_retraining | 1 | 0 | diversified_metro_placeholder | lower_middle_placeholder | 55,000.00 | 20,000.00 |

## E. Household Budget Stress

| Scenario | Income Loss | Existing Support | Basic Costs | Disposable After Costs | Savings Buffer | Immediate Gap | Stress Band |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Dual Income One Displaced Regional | 42,000.00 | 5,000.00 | 80,000.00 | 3,000.00 | 15,000.00 | 0.00 | medium |
| High Automation Region Cluster | 70,000.00 | 10,000.00 | 65,000.00 | -35,000.00 | 1,000.00 | 35,000.00 | critical |
| Older Worker Low Re-Employment | 65,000.00 | 10,000.00 | 51,000.00 | -26,000.00 | 2,000.00 | 26,000.00 | critical |
| Single Adult Displaced Worker High Rent | 55,000.00 | 12,000.00 | 55,000.00 | -33,000.00 | 1,000.00 | 33,000.00 | critical |
| Single Parent Retraining Gap | 58,000.00 | 18,000.00 | 62,000.00 | -32,000.00 | 500.00 | 32,000.00 | critical |
| UBI-Lite Payment Cliff Case | 30,000.00 | 8,000.00 | 47,000.00 | -9,000.00 | 3,000.00 | 9,000.00 | critical |
| Young Worker Retraining Rebound | 35,000.00 | 6,000.00 | 35,000.00 | -9,000.00 | 8,000.00 | 9,000.00 | high |

## F. Re-Employment Timing Risk

| Scenario | Months Without Full Income | Interim Recovery | Full Recovery | Re-Employment Risk |
| --- | ---: | ---: | ---: | --- |
| Dual Income One Displaced Regional | 8 | 14,700.00 | 35,700.00 | medium |
| High Automation Region Cluster | 24 | 14,000.00 | 42,000.00 | critical |
| Older Worker Low Re-Employment | N/A | 6,500.00 | 19,500.00 | critical |
| Single Adult Displaced Worker High Rent | 14 | 11,000.00 | 38,500.00 | high |
| Single Parent Retraining Gap | 18 | 14,500.00 | 43,500.00 | high |
| UBI-Lite Payment Cliff Case | 6 | 15,000.00 | 27,000.00 | medium |
| Young Worker Retraining Rebound | 3 | 17,500.00 | 35,000.00 | low |

## G. Regional Stress

| Scenario | Regional Score | Regional Band | Drivers |
| --- | ---: | --- | --- |
| Dual Income One Displaced Regional | 0.592 | high | limited labour-market depth |
| High Automation Region Cluster | 0.808 | critical | high automation exposure, limited labour-market depth, limited retraining access, high housing cost pressure, limited transport access |
| Older Worker Low Re-Employment | 0.600 | high | high automation exposure, limited labour-market depth, limited retraining access |
| Single Adult Displaced Worker High Rent | 0.533 | high | high housing cost pressure |
| Single Parent Retraining Gap | 0.578 | high | high housing cost pressure |
| UBI-Lite Payment Cliff Case | 0.443 | medium | None |
| Young Worker Retraining Rebound | 0.302 | medium | None |

## H. Payment Cliff Analysis

| Scenario | Support Loss | Income Gain | Net Position Change | Cliff Detected | Cliff Severity |
| --- | ---: | ---: | ---: | --- | --- |
| Dual Income One Displaced Regional | 1,000.00 | 6,000.00 | 5,000.00 | false | none |
| High Automation Region Cluster | 12,000.00 | 4,000.00 | -8,000.00 | true | high |
| Older Worker Low Re-Employment | 6,000.00 | 2,000.00 | -4,000.00 | true | high |
| Single Adult Displaced Worker High Rent | 6,000.00 | 8,000.00 | 2,000.00 | false | none |
| Single Parent Retraining Gap | 10,000.00 | 5,000.00 | -5,000.00 | true | high |
| UBI-Lite Payment Cliff Case | 8,000.00 | 4,000.00 | -4,000.00 | true | high |
| Young Worker Retraining Rebound | 3,000.00 | 8,000.00 | 5,000.00 | false | none |

## I. Transition Support and Residual Household Gap

| Scenario | Transition Support | Residual Household Gap After Support | Household Shock Band | Primary Risk Drivers |
| --- | ---: | ---: | --- | --- |
| Dual Income One Displaced Regional | 8,000.00 | 0.00 | high | regional stress: high |
| High Automation Region Cluster | 15,000.00 | 20,000.00 | critical | budget stress: critical, re-employment risk: critical, regional stress: critical, payment cliff: high, residual household gap after support |
| Older Worker Low Re-Employment | 12,000.00 | 14,000.00 | critical | budget stress: critical, re-employment risk: critical, regional stress: high, payment cliff: high, residual household gap after support |
| Single Adult Displaced Worker High Rent | 20,000.00 | 13,000.00 | critical | budget stress: critical, re-employment risk: high, regional stress: high, residual household gap after support |
| Single Parent Retraining Gap | 18,000.00 | 14,000.00 | critical | budget stress: critical, re-employment risk: high, regional stress: high, payment cliff: high, residual household gap after support |
| UBI-Lite Payment Cliff Case | 7,000.00 | 2,000.00 | critical | budget stress: critical, payment cliff: high, residual household gap after support |
| Young Worker Retraining Rebound | 9,000.00 | 0.00 | medium | budget stress: high |

## J. Payment Interaction Linkage

Payment interaction linkage is optional. Where supplied, payment-interaction risk and residual support gaps are used as additional prototype household shock drivers. They do not modify firm-level CARSF liability.

| Scenario | Payment Interaction Supplied | Interaction Risk Band | Residual Support Gap | Combined Commonwealth/Support Gap |
| --- | --- | --- | ---: | ---: |
| Dual Income One Displaced Regional | false | Not supplied for this synthetic scenario | Not supplied for this synthetic scenario | Not supplied for this synthetic scenario |
| High Automation Region Cluster | false | Not supplied for this synthetic scenario | Not supplied for this synthetic scenario | Not supplied for this synthetic scenario |
| Older Worker Low Re-Employment | false | Not supplied for this synthetic scenario | Not supplied for this synthetic scenario | Not supplied for this synthetic scenario |
| Single Adult Displaced Worker High Rent | false | Not supplied for this synthetic scenario | Not supplied for this synthetic scenario | Not supplied for this synthetic scenario |
| Single Parent Retraining Gap | false | Not supplied for this synthetic scenario | Not supplied for this synthetic scenario | Not supplied for this synthetic scenario |
| UBI-Lite Payment Cliff Case | false | Not supplied for this synthetic scenario | Not supplied for this synthetic scenario | Not supplied for this synthetic scenario |
| Young Worker Retraining Rebound | false | Not supplied for this synthetic scenario | Not supplied for this synthetic scenario | Not supplied for this synthetic scenario |

## K. Household Shock Band

Household shock bands are prototype-only labels that combine budget stress, re-employment timing, regional stress, payment cliff severity, residual gap after support, and any supplied payment-interaction risk.

| Scenario | Budget Stress | Re-Employment Risk | Regional Stress | Cliff Severity | Payment Interaction Risk | Household Shock Band |
| --- | --- | --- | --- | --- | --- | --- |
| Dual Income One Displaced Regional | medium | medium | high | none | not supplied | high |
| High Automation Region Cluster | critical | critical | critical | high | not supplied | critical |
| Older Worker Low Re-Employment | critical | critical | high | high | not supplied | critical |
| Single Adult Displaced Worker High Rent | critical | high | high | none | not supplied | critical |
| Single Parent Retraining Gap | critical | high | high | high | not supplied | critical |
| UBI-Lite Payment Cliff Case | critical | medium | medium | high | not supplied | critical |
| Young Worker Retraining Rebound | high | low | medium | none | not supplied | medium |

## L. Distributional Summary

| Scenario Count | Low | Medium | High | Critical | Average Residual Gap | Highest-Risk Synthetic Households |
| ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 7 | 0 | 1 | 1 | 5 | 9,000.00 | hh_high_automation_region, hh_older_worker_low_reemployment, hh_single_parent_retraining |

## M. Highest-Risk Synthetic Households

hh_high_automation_region, hh_older_worker_low_reemployment, hh_single_parent_retraining

Primary systemic risks: budget stress: critical, residual household gap after support, payment cliff: high, regional stress: high, re-employment risk: critical

## N. Plain-English Interpretation

### Dual Income One Displaced Regional

Household income cushion reduces immediate budget gap, but regional labour-market depth still creates a transition risk.

- Firm-level CARSF liability is not automatically modified by this synthetic distributional scenario.

### High Automation Region Cluster

This synthetic cluster case combines high automation exposure, weak labour-market depth, limited retraining access, a support cliff, and a residual household gap.

- Firm-level CARSF liability is not automatically modified by this synthetic distributional scenario.

### Older Worker Low Re-Employment

Low re-employment recovery creates a high residual shock even where immediate support offsets some annual budget gap.

- Firm-level CARSF liability is not automatically modified by this synthetic distributional scenario.

### Single Adult Displaced Worker High Rent

High rent and low savings create acute budget stress even with placeholder transition support. Re-employment delay remains the main risk driver.

- Firm-level CARSF liability is not automatically modified by this synthetic distributional scenario.

### Single Parent Retraining Gap

Children, low savings, retraining delay, and a support cliff leave a residual gap after support under these placeholders.

- Firm-level CARSF liability is not automatically modified by this synthetic distributional scenario.

### UBI-Lite Payment Cliff Case

This synthetic case shows how a support phase-out can leave a household worse off even as income recovers under placeholder settings.

- Firm-level CARSF liability is not automatically modified by this synthetic distributional scenario.

### Young Worker Retraining Rebound

Faster retraining and deeper labour-market access reduce residual shock under these placeholder settings.

- Firm-level CARSF liability is not automatically modified by this synthetic distributional scenario.

## O. Limitations and Calibration Needs

- All household, income, cost, support, regional, and re-employment values are synthetic illustrative placeholders.
- No real household data, welfare records, income records, ABS, DSS, Services Australia, ATO, Treasury, PBO, HILDA, Census, or household survey data is used.
- Household shock bands, regional stress, and payment cliff warnings are prototype-only labels and not welfare advice, eligibility law, forecasts, or validated distributional modelling.
- Future calibration would require ABS, HILDA, DSS, Services Australia, labour-market, regional, household survey, legal, privacy, Treasury, PBO, and economic review before policy use.
