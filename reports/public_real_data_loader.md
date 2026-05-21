# CARSF V1.5 Public Real Aggregate Data Loader

Generated at: `2026-05-21T00:29:02+00:00`

## A. Purpose

This report records the first controlled repo-local public aggregate data loader for CARSF V1.5.

## B. Non-Claims

- This loads real public aggregate data only. This does not load restricted data, personal data, taxpayer-level data, firm-confidential data, or household microdata. Public aggregate data does not equal calibration; calibration has not been completed. Public data does not prove the model works. This is not validation, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, and not official status. It does not determine actual tax payable and does not modify firm-level CARSF liability.
- Loaded records are public aggregate/source-located values only and do not create a calibrated model.
- Source candidates without safe local values remain source_candidate_not_loaded and are not counted as loaded data.
- The loader only supports sanity-check context and placeholder replacement review; it does not replace legal, tax, Treasury, ATO, statistical, welfare, or economic review.

## C. Source Inclusion Rules

- A loaded source must be public, aggregate-level, non-personal, non-confidential, source-located, and safe for repository use.
- A source candidate without a safe exact local value remains source_candidate_not_loaded.
- No raw downloaded datasets are committed by this build.

## D. Loaded Public Aggregate Sources

| Source ID | Publisher | Status | URL | Locator | Public Aggregate Only | Safe For Repo | Allowed Use | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fair_work_minimum_wage_2025 | Fair Work Ombudsman | loaded | https://www.fairwork.gov.au/how-we-will-help/templates-and-guides/fact-sheets/minimum-workplace-entitlements/minimum-wages | Fair Work Ombudsman minimum wages fact sheet, national minimum wage paragraph for the 1 July 2025 rate and 38-hour week reference. | True | True | sanity_check_context, placeholder_anchor_review | not_calibration, not_validation, not_legal_advice, not_tax_advice, not_tax_payable, not_official_status |
| ato_corporate_tax_transparency_2022_23 | Australian Taxation Office | loaded | https://www.ato.gov.au/media-centre/ato-collects-100-billion-dollars-from-large-corporates | ATO media-centre article "ATO collects $100 billion dollars from large corporates", public summary of 2022-23 corporate tax transparency results. | True | True | sanity_check_context, fiscal_scale_context | not_ato_validation, not_firm_liability, not_actual_tax_payable, not_calibration, not_official_status |
| ato_taxation_statistics_2022_23 | Australian Taxation Office | loaded | https://www.ato.gov.au/media-centre/2022-23-taxation-statistics-released | ATO media-centre article "2022-23 taxation statistics released", public headline aggregate values. | True | True | sanity_check_context, fiscal_scale_context | not_taxpayer_level_inference, not_actual_tax_payable, not_calibration, not_validation |
| treasury_budget_2026_27_bp1 | Australian Government Treasury | loaded | https://budget.gov.au/content/bp1/ | Budget Paper No. 1 2026-27, Statement 5 Revenue, Table 5.1 Australian Government general government receipts, 2025-26 estimates. | True | True | sanity_check_context, fiscal_scale_context, transition_funding_context | not_treasury_modelling, not_pbo_costing, not_calibration, not_validation, not_official_status |
| ato_super_guarantee_2025_26 | Australian Taxation Office | loaded | https://www.ato.gov.au/tax-rates-and-codes/key-superannuation-rates-and-thresholds/super-guarantee | ATO key superannuation rates and thresholds page, super guarantee percentage table for the period from 1 July 2025. | True | True | placeholder_anchor_review, payment_interaction_context | not_ato_guidance, not_individual_estimate, not_calibration, not_actual_tax_payable |

## E. Source Candidates Not Loaded

| Source ID | Publisher | Status | URL | Locator | Public Aggregate Only | Safe For Repo | Allowed Use | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| study_assist_help_thresholds_2025_26 | Australian Government StudyAssist | source_candidate_not_loaded | https://www.studyassist.gov.au/paying-back-your-loan/loan-repayment | Source page only; exact threshold value is not loaded in Build 31. | True | True | source_candidate_review | not_loaded_data, not_individual_repayment_estimate, not_calibration, not_tax_advice |
| qld_payroll_tax_threshold_2025_26 | Queensland Revenue Office | source_candidate_not_loaded | https://qro.qld.gov.au/payroll-tax/ | Source page only; exact threshold value is not loaded in Build 31. | True | True | source_candidate_review | not_loaded_data, not_state_tax_advice, not_actual_tax_payable, not_calibration |
| abs_labour_wage_aggregate_source_reference | Australian Bureau of Statistics | source_candidate_not_loaded | https://www.abs.gov.au/statistics/labour | ABS labour statistics landing source only; no selected aggregate table is loaded in Build 31. | True | True | source_candidate_review | not_loaded_data, not_population_estimate, not_sector_ranking, not_calibration |

## F. Loaded Public Aggregate Values

| Value ID | Source | Metric | Value | Unit | Period | Geography | Review Status | Used For | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fair_work_national_minimum_wage_hourly_2025 | fair_work_minimum_wage_2025 | National minimum wage hourly rate | 24.95 | AUD_per_hour | from 2025-07-01 | Australia | manually_recorded_public_source_value | opfTE_hle_qlc_placeholder_anchor_context | not_calibration, not_validation, not_actual_tax_payable, not_official_status |
| fair_work_national_minimum_wage_weekly_2025 | fair_work_minimum_wage_2025 | National minimum wage weekly rate | 948.1 | AUD_per_week | from 2025-07-01 | Australia | arithmetic_checked_only | opfTE_hle_qlc_placeholder_anchor_context | not_calibration, not_validation, not_actual_tax_payable, not_official_status |
| fair_work_casual_loading_2025 | fair_work_minimum_wage_2025 | Casual loading percentage | 25.0 | percent | from 2025-07-01 | Australia | manually_recorded_public_source_value | labour_cost_placeholder_anchor_context | not_calibration, not_validation, not_actual_tax_payable, not_official_status |
| ato_large_corporate_income_tax_received_2022_23 | ato_corporate_tax_transparency_2022_23 | Income tax received from large corporates | 97.9 | AUD_billion | 2022-23 | Australia | manually_recorded_public_source_value | fiscal_trajectory_sanity_context, corporate_tax_scale_context | not_firm_liability, not_actual_tax_payable, not_compliance_score, not_calibration |
| ato_large_corporate_entities_no_income_tax_percent_2022_23 | ato_corporate_tax_transparency_2022_23 | Entities with no income tax payable in public report | 31.0 | percent | 2022-23 | Australia | manually_recorded_public_source_value | corporate_tax_scale_context | not_firm_liability, not_actual_tax_payable, not_compliance_score, not_calibration |
| ato_total_tax_revenue_collected_2022_23 | ato_taxation_statistics_2022_23 | Total tax revenue collected | 577.4 | AUD_billion | 2022-23 | Australia | manually_recorded_public_source_value | fiscal_trajectory_sanity_context | not_taxpayer_level_inference, not_actual_tax_payable, not_calibration, not_validation |
| ato_company_tax_revenue_2022_23 | ato_taxation_statistics_2022_23 | Company tax revenue | 140.0 | AUD_billion | 2022-23 | Australia | manually_recorded_public_source_value | fiscal_trajectory_sanity_context, corporate_tax_scale_context | not_taxpayer_level_inference, not_actual_tax_payable, not_calibration, not_validation |
| treasury_total_receipts_2025_26_estimate | treasury_budget_2026_27_bp1 | Total receipts estimate | 759.8 | AUD_billion | 2025-26 estimate in Budget Paper No. 1 2026-27 | Australia | manually_recorded_public_source_value | fiscal_trajectory_sanity_context, transition_funding_context | not_treasury_modelling, not_pbo_costing, not_calibration, not_actual_tax_payable |
| treasury_taxation_receipts_2025_26_estimate | treasury_budget_2026_27_bp1 | Taxation receipts estimate | 699.5 | AUD_billion | 2025-26 estimate in Budget Paper No. 1 2026-27 | Australia | manually_recorded_public_source_value | fiscal_trajectory_sanity_context, transition_funding_context | not_treasury_modelling, not_pbo_costing, not_calibration, not_actual_tax_payable |
| ato_super_guarantee_rate_2025_26 | ato_super_guarantee_2025_26 | Super guarantee percentage | 12.0 | percent | from 2025-07-01 | Australia | manually_recorded_public_source_value | superannuation_contribution_pressure_placeholder_context | not_ato_guidance, not_individual_estimate, not_calibration, not_actual_tax_payable |

## G. Guardrail Checks

| Finding ID | Guardrail | Status | Finding |
| --- | --- | --- | --- |
| public_real_restricted_path_scan | No restricted/private public-real paths are present. | clean | no restricted public-real paths found |
| public_real_dataset_extension_scan | No raw dataset file types are committed in Build 31. | clean | no unapproved raw dataset-like files found |

## H. Digest Manifest

- Digest targets total: 5
- Digests written: 5
- Digest file does not hash itself.
- Digests are integrity metadata only, not signatures, not external attestation, not approval, not validation, and not calibration.

## I. What This Data Can Support

- Sanity-check context for fiscal scale, wage thresholds, corporate tax aggregate context, and public rate settings.
- Placeholder replacement review candidates for a later build.
- Reviewer inspection of source URL, locator, unit, period, and geography metadata.

## J. What This Data Cannot Support

- It cannot support calibration completion, validation, official status, tax-payable determination, legal advice, tax advice, ATO guidance, Treasury modelling, PBO costing, or firm-level CARSF liability changes.
- It cannot support restricted-data, taxpayer-level, person-level, firm-confidential, or household-microdata analysis.

## K. Placeholder Replacement Candidates

Fair Work wage thresholds, ATO aggregate tax context, Budget Paper receipt aggregates, and super guarantee rate settings can be mapped to placeholder replacement candidates in Build 32 without claiming calibration.

## L. Calibration Blockers Still Remaining

Restricted tax records, firm-confidential records, household microdata, person-level welfare/payment records, behavioural elasticity evidence, legal drafting review, and external statistical review remain blockers.

## M. Build 32 Readiness

- Map which placeholders can be narrowed using loaded public aggregate values.
- Keep all replacement candidates labelled as public aggregate anchors until external review and calibration design are complete.
- Preserve no-restricted-data, no-personal-data, no-taxpayer-data, no-firm-confidential-data, no-household-microdata, no-tax-payable, and no-liability-change boundaries.

## N. Limitations and Future Work

- total_sources: 8
- loaded_sources: 5
- source_candidates_not_loaded: 3
- blocked_sources: 0
- rejected_sources: 0
- loaded_values_total: 10
- loaded_value_units_present: 10
- loaded_value_periods_present: 10
- loaded_value_geographies_present: 10
- guardrail_findings_total: 2
- guardrail_fail_closed_findings: 0
- digest_targets_total: 5
- digests_written: 5
- forbidden_claim_findings: 0
- public_real_data_loader_created: True
- real_public_aggregate_data_loaded: True
- new_public_aggregate_values_loaded: 10
- restricted_data_loaded: False
- personal_data_loaded: False
- taxpayer_level_data_loaded: False
- firm_confidential_data_loaded: False
- household_microdata_loaded: False
- calibration_completed: False
- validation_claimed: False
- actual_tax_payable_determined: False
- official_status_claimed: False
- firm_level_liability_logic_modified: False
