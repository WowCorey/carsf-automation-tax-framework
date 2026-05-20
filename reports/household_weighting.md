# CARSF V1.5 Household Weighting and Subgroup Aggregation Shell

Generated at: `2026-05-20T07:07:49+00:00`

## A. Purpose

This report previews synthetic household weighting and subgroup aggregation over existing synthetic distributional scenarios.

## B. Non-Claims

- These are synthetic household weighting outputs only. They are not population estimates, real distributional modelling, ABS/HILDA/Census analysis, DSS/Services Australia modelling, Treasury modelling, PBO costing, welfare advice, eligibility law, legal advice, tax advice, or economic validation.
- This is a prototype weighting and subgroup aggregation shell only; it is not a validated distributional model.
- All household weights and subgroup aggregations are illustrative placeholders and are not representative.
- Household weighting outputs do not modify firm-level CARSF liability.

## C. Why Weighting and Subgroup Aggregation Matter

Individual synthetic scenarios can show household mechanics, but policy review also needs a controlled shell for subgroup aggregation. This shell validates placeholder weights, groups scenarios, and makes representativeness warnings explicit. It is not population weighting.

## D. Synthetic Weight Summary

### Low-Income Household Weighting

| Scenario | Subgroup | Weight | Calibrated | Usable for Real-World Claims | Basis |
| --- | --- | ---: | --- | --- | --- |
| single_adult_displaced_worker_high_rent | lower_middle_income | 2.0000 | false | false | lower-income synthetic placeholder stress weight |
| single_parent_retraining_gap | lower_middle_income | 2.0000 | false | false | lower-income synthetic placeholder stress weight |
| ubi_lite_payment_cliff_case | lower_middle_income | 1.5000 | false | false | lower-income synthetic placeholder stress weight |
| single_parent_retraining_gap | critical_budget_stress | 1.0000 | false | false | critical-stress placeholder comparison |

### Placeholder Weights Basic

| Scenario | Subgroup | Weight | Calibrated | Usable for Real-World Claims | Basis |
| --- | --- | ---: | --- | --- | --- |
| single_adult_displaced_worker_high_rent | all_synthetic_households | 1.0000 | false | false | equal synthetic placeholder weight |
| single_parent_retraining_gap | all_synthetic_households | 1.0000 | false | false | equal synthetic placeholder weight |
| dual_income_one_displaced_regional | all_synthetic_households | 1.0000 | false | false | equal synthetic placeholder weight |
| older_worker_low_reemployment | critical_budget_stress | 1.0000 | false | false | equal synthetic placeholder weight |
| high_automation_region_cluster | regional_high_stress | 1.0000 | false | false | equal synthetic placeholder weight |

### Re-Employment Delay Weighting

| Scenario | Subgroup | Weight | Calibrated | Usable for Real-World Claims | Basis |
| --- | --- | ---: | --- | --- | --- |
| single_adult_displaced_worker_high_rent | high_reemployment_risk | 1.5000 | false | false | re-employment delay placeholder stress weight |
| single_parent_retraining_gap | high_reemployment_risk | 1.5000 | false | false | re-employment delay placeholder stress weight |
| older_worker_low_reemployment | critical_reemployment_risk | 3.0000 | false | false | re-employment delay placeholder stress weight |
| high_automation_region_cluster | critical_reemployment_risk | 3.0000 | false | false | re-employment delay placeholder stress weight |

### Regional High-Stress Weighting

| Scenario | Subgroup | Weight | Calibrated | Usable for Real-World Claims | Basis |
| --- | --- | ---: | --- | --- | --- |
| high_automation_region_cluster | regional_critical_stress | 4.0000 | false | false | stress-test placeholder overweighting |
| dual_income_one_displaced_regional | regional_high_stress | 2.0000 | false | false | stress-test placeholder overweighting |
| older_worker_low_reemployment | regional_high_stress | 2.0000 | false | false | stress-test placeholder overweighting |
| young_worker_retraining_rebound | all_synthetic_households | 0.5000 | false | false | stress-test placeholder comparison |

### Zero Weight Not Representative

| Scenario | Subgroup | Weight | Calibrated | Usable for Real-World Claims | Basis |
| --- | --- | ---: | --- | --- | --- |
| single_adult_displaced_worker_high_rent | all_synthetic_households | 0.0000 | false | false | zero-weight not-assessable placeholder |
| young_worker_retraining_rebound | all_synthetic_households | 0.0000 | false | false | zero-weight not-assessable placeholder |

## E. Subgroup Definitions

### Low-Income Household Weighting

| Subgroup | Name | Household Type | Income Band | Region | Re-Employment Risk | Budget Stress | Regional Stress |
| --- | --- | --- | --- | --- | --- | --- | --- |
| lower_middle_income | Lower-Middle Placeholder Income Band | Any | lower_middle_placeholder | Any | Any | Any | Any |
| critical_budget_stress | Critical Budget Stress | Any | Any | Any | Any | critical | Any |

### Placeholder Weights Basic

| Subgroup | Name | Household Type | Income Band | Region | Re-Employment Risk | Budget Stress | Regional Stress |
| --- | --- | --- | --- | --- | --- | --- | --- |
| all_synthetic_households | All Synthetic Households | Any | Any | Any | Any | Any | Any |
| critical_budget_stress | Critical Budget Stress | Any | Any | Any | Any | critical | Any |
| regional_high_stress | High Regional Stress | Any | Any | Any | Any | Any | high |

### Re-Employment Delay Weighting

| Subgroup | Name | Household Type | Income Band | Region | Re-Employment Risk | Budget Stress | Regional Stress |
| --- | --- | --- | --- | --- | --- | --- | --- |
| high_reemployment_risk | High Re-Employment Risk | Any | Any | Any | high | Any | Any |
| critical_reemployment_risk | Critical Re-Employment Risk | Any | Any | Any | critical | Any | Any |

### Regional High-Stress Weighting

| Subgroup | Name | Household Type | Income Band | Region | Re-Employment Risk | Budget Stress | Regional Stress |
| --- | --- | --- | --- | --- | --- | --- | --- |
| regional_high_stress | High Regional Stress | Any | Any | Any | Any | Any | high |
| regional_critical_stress | Critical Regional Stress | Any | Any | Any | Any | Any | critical |
| all_synthetic_households | All Synthetic Households | Any | Any | Any | Any | Any | Any |

### Zero Weight Not Representative

| Subgroup | Name | Household Type | Income Band | Region | Re-Employment Risk | Budget Stress | Regional Stress |
| --- | --- | --- | --- | --- | --- | --- | --- |
| all_synthetic_households | All Synthetic Households | Any | Any | Any | Any | Any | Any |

## F. Weighted Aggregation Results

Overall metrics aggregate synthetic weight records. If the same scenario appears in multiple subgroup weights, it may contribute more than once. These outputs are stress-test summaries, not unique-household or population-weighted estimates.

### Low-Income Household Weighting

| Metric | Value |
| --- | ---: |
| Total synthetic weight | 6.5000 |
| Aggregation basis | synthetic_weight_record_aggregate_not_unique_population_weight |
| Duplicate scenario weight records | single_parent_retraining_gap |
| Overall synthetic weight-record average residual gap | 10,923.08 |
| Overall synthetic weight-record high/critical share | 100.00% |
| Representative of real population | false |

| Subgroup | Scenarios | Weight | Weighted Avg Residual Gap | High/Critical Share | Highest-Risk Scenarios | Representativeness Warning |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| Critical Budget Stress | 1 | 1.0000 | 14,000.00 | 100.00% | single_parent_retraining_gap | true |
| Lower-Middle Placeholder Income Band | 3 | 5.5000 | 10,363.64 | 100.00% | single_parent_retraining_gap, single_adult_displaced_worker_high_rent, ubi_lite_payment_cliff_case | true |

### Placeholder Weights Basic

| Metric | Value |
| --- | ---: |
| Total synthetic weight | 5.0000 |
| Aggregation basis | synthetic_weight_record_aggregate_not_unique_population_weight |
| Duplicate scenario weight records | None |
| Overall synthetic weight-record average residual gap | 12,200.00 |
| Overall synthetic weight-record high/critical share | 100.00% |
| Representative of real population | false |

| Subgroup | Scenarios | Weight | Weighted Avg Residual Gap | High/Critical Share | Highest-Risk Scenarios | Representativeness Warning |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| All Synthetic Households | 3 | 3.0000 | 9,000.00 | 100.00% | single_parent_retraining_gap, single_adult_displaced_worker_high_rent, dual_income_one_displaced_regional | true |
| Critical Budget Stress | 1 | 1.0000 | 14,000.00 | 100.00% | older_worker_low_reemployment | true |
| High Regional Stress | 1 | 1.0000 | 20,000.00 | 100.00% | high_automation_region_cluster | true |

### Re-Employment Delay Weighting

| Metric | Value |
| --- | ---: |
| Total synthetic weight | 9.0000 |
| Aggregation basis | synthetic_weight_record_aggregate_not_unique_population_weight |
| Duplicate scenario weight records | None |
| Overall synthetic weight-record average residual gap | 15,833.33 |
| Overall synthetic weight-record high/critical share | 100.00% |
| Representative of real population | false |

| Subgroup | Scenarios | Weight | Weighted Avg Residual Gap | High/Critical Share | Highest-Risk Scenarios | Representativeness Warning |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| Critical Re-Employment Risk | 2 | 6.0000 | 17,000.00 | 100.00% | high_automation_region_cluster, older_worker_low_reemployment | true |
| High Re-Employment Risk | 2 | 3.0000 | 13,500.00 | 100.00% | single_parent_retraining_gap, single_adult_displaced_worker_high_rent | true |

### Regional High-Stress Weighting

| Metric | Value |
| --- | ---: |
| Total synthetic weight | 8.5000 |
| Aggregation basis | synthetic_weight_record_aggregate_not_unique_population_weight |
| Duplicate scenario weight records | None |
| Overall synthetic weight-record average residual gap | 12,705.88 |
| Overall synthetic weight-record high/critical share | 94.12% |
| Representative of real population | false |

| Subgroup | Scenarios | Weight | Weighted Avg Residual Gap | High/Critical Share | Highest-Risk Scenarios | Representativeness Warning |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| All Synthetic Households | 1 | 0.5000 | 0.00 | 0.00% | young_worker_retraining_rebound | true |
| Critical Regional Stress | 1 | 4.0000 | 20,000.00 | 100.00% | high_automation_region_cluster | true |
| High Regional Stress | 2 | 4.0000 | 7,000.00 | 100.00% | older_worker_low_reemployment, dual_income_one_displaced_regional | true |

### Zero Weight Not Representative

| Metric | Value |
| --- | ---: |
| Total synthetic weight | 0.0000 |
| Aggregation basis | synthetic_weight_record_aggregate_not_unique_population_weight |
| Duplicate scenario weight records | None |
| Overall synthetic weight-record average residual gap | N/A |
| Overall synthetic weight-record high/critical share | N/A |
| Representative of real population | false |

| Subgroup | Scenarios | Weight | Weighted Avg Residual Gap | High/Critical Share | Highest-Risk Scenarios | Representativeness Warning |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| All Synthetic Households | 2 | 0.0000 | N/A | N/A | single_adult_displaced_worker_high_rent, young_worker_retraining_rebound | true |

## G. Highest-Risk Synthetic Subgroups

| Example | Highest-Risk Subgroups |
| --- | --- |
| Low-Income Household Weighting | critical_budget_stress, lower_middle_income |
| Placeholder Weights Basic | regional_high_stress, critical_budget_stress, all_synthetic_households |
| Re-Employment Delay Weighting | critical_reemployment_risk, high_reemployment_risk |
| Regional High-Stress Weighting | regional_critical_stress, regional_high_stress, all_synthetic_households |
| Zero Weight Not Representative | all_synthetic_households |

## H. Representativeness Warnings

### Low-Income Household Weighting

- Weighted distributional aggregation uses synthetic placeholder weights only.
- Results are not representative of real Australian households.
- Firm-level CARSF liability is not modified by weighted distributional outputs.
- One or more synthetic scenarios appear in multiple weight records. Overall weighted outputs are weight-record aggregates, not unique-household or population estimates.
- Calibration status does not support real-world representativeness claims.
- representative_of_real_population: false

### Placeholder Weights Basic

- Weighted distributional aggregation uses synthetic placeholder weights only.
- Results are not representative of real Australian households.
- Firm-level CARSF liability is not modified by weighted distributional outputs.
- Calibration status does not support real-world representativeness claims.
- representative_of_real_population: false

### Re-Employment Delay Weighting

- Weighted distributional aggregation uses synthetic placeholder weights only.
- Results are not representative of real Australian households.
- Firm-level CARSF liability is not modified by weighted distributional outputs.
- Calibration status does not support real-world representativeness claims.
- representative_of_real_population: false

### Regional High-Stress Weighting

- Weighted distributional aggregation uses synthetic placeholder weights only.
- Results are not representative of real Australian households.
- Firm-level CARSF liability is not modified by weighted distributional outputs.
- Calibration status does not support real-world representativeness claims.
- representative_of_real_population: false

### Zero Weight Not Representative

- Weighted distributional aggregation uses synthetic placeholder weights only.
- Results are not representative of real Australian households.
- Firm-level CARSF liability is not modified by weighted distributional outputs.
- Total synthetic weight is zero; weighted averages are not assessable.
- Calibration status does not support real-world representativeness claims.
- representative_of_real_population: false

## I. Calibration Readiness Requirements

Ready for real distributional claims: `false`

| Requirement | Category | Required For | Source Type | Status | Real Data In Repo Allowed |
| --- | --- | --- | --- | --- | --- |
| hh_comp | household composition | subgroup weighting | ABS/Census/HILDA category only | unmet | false |
| income_dist | income distribution | budget stress, subgroup weighting | ATO/ABS/HILDA category only | unmet | false |
| employment_disp | employment displacement | shock weighting | Treasury/ABS/labour-market category only | unmet | false |
| regional_depth | regional labour-market depth | regional stress | ABS/regional labour-market category only | unmet | false |
| housing_costs | housing costs | budget stress | ABS/housing survey category only | unmet | false |
| essential_costs | essential costs | budget stress | household expenditure survey category only | unmet | false |
| buffers | savings/debt buffers | shock severity | HILDA/household survey category only | unmet | false |
| welfare_baseline | welfare/transfer baseline | support adequacy | DSS/Services Australia category only | unmet | false |
| reemployment | re-employment timing | reemployment risk | HILDA/labour-market transition category only | unmet | false |
| eligibility | payment eligibility | payment cliff, support targeting | DSS/legal policy category only | unmet | false |
| survey_weights | survey weighting | weighted aggregation | ABS/HILDA/Census category only | unmet | false |
| uncertainty | uncertainty/confidence intervals | reporting | Treasury/PBO/statistical review category only | unmet | false |

## J. Plain-English Interpretation

### Low-Income Household Weighting

Lower-income placeholder weighting highlights support adequacy risks without claiming real income distribution effects.

- Firm-level CARSF liability is not automatically modified by this household weighting shell.

### Placeholder Weights Basic

Basic placeholder weighting checks the aggregation plumbing without claiming any population representativeness.

- Firm-level CARSF liability is not automatically modified by this household weighting shell.

### Re-Employment Delay Weighting

Re-employment delay weighting tests whether longer displacement timing dominates synthetic residual hardship.

- Firm-level CARSF liability is not automatically modified by this household weighting shell.

### Regional High-Stress Weighting

This stress case makes regional and high-automation synthetic scenarios more visible, but it is not representative weighting.

- Firm-level CARSF liability is not automatically modified by this household weighting shell.

### Zero Weight Not Representative

Zero total synthetic weight deliberately produces not-assessable weighted averages and no representativeness claim.

- Firm-level CARSF liability is not automatically modified by this household weighting shell.

## K. Limitations and Future Data Needs

- All weights, subgroup definitions, and aggregation outputs are synthetic illustrative placeholders.
- These outputs are not population estimates and are not representative of real Australian households.
- No real household data, ABS, HILDA, Census, DSS, Services Australia, ATO, Treasury, PBO, welfare, income, or survey data is used.
- Future calibration requires a controlled external data environment and legal, privacy, DSS / Services Australia, ABS, HILDA, Treasury, PBO, and economic review.
