# CARSF V1.5 Public Data Pilot & Realistic Placeholder Anchor Layer

Generated at: `2026-05-19T04:39:23+00:00`

## A. Purpose

This report records the first small public aggregate-data pilot and realistic-placeholder anchor layer for CARSF V1.5.

## B. Non-Claims

- This is a public aggregate-data pilot and realistic-placeholder anchor layer only. It may include small public aggregate extracts or source-reference records, but it is not calibration, calibration has not been completed, public data extracts do not prove the model works, realistic placeholders remain realistic placeholders, source references are not loaded datasets, and restricted-data requirements are not data access. It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, or official status. It does not determine actual tax payable, does not use taxpayer-level data, firm-level confidential data, household microdata, ABS DataLab, HILDA microdata, DSS/Services Australia records, ATO taxpayer records, Treasury/PBO confidential material, or restricted government data, and does not modify firm-level CARSF liability.
- Loaded public aggregate extracts are sanity-check-only or placeholder-anchor-only records, not completed calibration.
- Realistic placeholders anchored to public sources remain placeholders and must not be labelled as real data or calibrated.
- The pilot only tests whether small public aggregates can support sanity checks and placeholder anchors.

## C. Public Data Loading Rules

- Only small YAML/JSON source-reference or aggregate extract records are committed.
- Loaded public records must carry source URL, publisher, licence/access notes, source note, data status, and claim level.
- Source-reference-only records do not count as loaded public data.
- Realistic placeholders may be anchored to public extracts, but they remain placeholders.

## D. Source Reference Registry

| Source Reference ID | Publisher | Kind | URL | Access | Extract Committed | Claim Level | Candidate Fields | Must Not Claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| fair_work_minimum_wage_2025 | Fair Work Ombudsman | Fair_Work_public_wage_anchor | https://www.fairwork.gov.au/how-we-will-help/templates-and-guides/fact-sheets/minimum-workplace-entitlements/minimum-wages | public_open | True | placeholder_anchor_only | opfte_benchmarks, hle_assumptions, qlc_weights | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| ato_corporate_tax_transparency_2022_23 | Australian Taxation Office | ATO_public_aggregate | https://www.ato.gov.au/media-centre/ato-collects-100-billion-dollars-from-large-corporates | public_open | True | sanity_check_only | aava_deductibility_treatment, fiscal_trajectory_assumptions | must not claim: firm-level liability, actual tax payable, compliance score, calibration completed |
| ato_taxation_statistics_2022_23 | Australian Taxation Office | ATO_public_aggregate | https://www.ato.gov.au/media-centre/2022-23-taxation-statistics-released | public_open | True | sanity_check_only | payg_erosion_assumptions, fiscal_trajectory_assumptions, superannuation_contribution_pressure | must not claim: taxpayer-level inference, actual tax payable, calibration completed |
| treasury_budget_2026_27_bp1 | Australian Government Treasury | Treasury_public_fiscal | https://budget.gov.au/content/bp1/ | public_open | True | sanity_check_only | fiscal_trajectory_assumptions, transition_payment_assumptions | must not claim: Treasury modelling, PBO costing, calibration completed |
| study_assist_help_thresholds_2025_26 | Australian Government StudyAssist | HELP_HECS_public_threshold | https://www.studyassist.gov.au/paying-back-your-loan/loan-repayment | public_open | True | source_reference_only | help_hecs_repayment_pressure, welfare_payment_interaction_assumptions | must not claim: individual repayment estimate, welfare validation, calibration completed |
| ato_super_guarantee_2025_26 | Australian Taxation Office | Super_Guarantee_public_setting | https://www.ato.gov.au/tax-rates-and-codes/key-superannuation-rates-and-thresholds/super-guarantee | public_open | True | placeholder_anchor_only | superannuation_contribution_pressure, transition_payment_assumptions | must not claim: ATO guidance, individual estimate, calibration completed |
| qld_payroll_tax_threshold_2025_26 | Queensland Revenue Office | State_payroll_tax_public_threshold | https://qro.qld.gov.au/payroll-tax/ | public_open | True | source_reference_only | state_payroll_tax_pressure, fiscal_trajectory_assumptions | must not claim: state tax advice, actual tax payable, calibration completed |
| abs_labour_wage_aggregate_source_reference | Australian Bureau of Statistics | ABS_public_aggregate | https://www.abs.gov.au/statistics/labour | public_open | True | source_reference_only | opfte_benchmarks, qlc_weights, sector_schedule_values | must not claim: population estimate, official sector ranking, calibration completed |

## E. Public Aggregate Extracts

| Extract ID | Source | Status | Claim Level | Period | Values | Safe To Commit | Source Note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fair_work_minimum_wage_2025_extract | fair_work_minimum_wage_2025 | real_public_data_loaded | placeholder_anchor_only | from 2025-07-01 | national_minimum_wage_hourly=24.95 AUD_per_hour; national_minimum_wage_weekly=948.0 AUD_per_week; casual_loading=25.0 percent | True | Small public wage threshold extract used only to anchor OPFTE, HLE, and QLC realistic placeholders. |
| ato_corporate_transparency_2022_23_extract | ato_corporate_tax_transparency_2022_23 | real_public_data_loaded | sanity_check_only | 2022-23 | income_tax_received_large_corporates=97.9 AUD_billion; entities_with_no_income_tax_percent=31.0 percent | True | Public corporate tax transparency aggregate used only for fiscal scale context; no firm-level CARSF liability inference is allowed. |
| ato_taxation_statistics_2022_23_extract | ato_taxation_statistics_2022_23 | real_public_data_loaded | sanity_check_only | 2022-23 | total_tax_revenue_collected=577.4 AUD_billion; company_tax_revenue=140.0 AUD_billion | True | Public ATO aggregate used for sanity-check-only fiscal scale context. |
| treasury_budget_2026_27_receipts_extract | treasury_budget_2026_27_bp1 | real_public_data_loaded | sanity_check_only | 2025-26 estimate in Budget Paper No. 1 2026-27 | total_receipts_estimate=759.8 AUD_billion; taxation_receipts_estimate=699.5 AUD_billion | True | Public budget aggregate used only for fiscal trajectory sanity-check context. |
| super_guarantee_2025_26_extract | ato_super_guarantee_2025_26 | real_public_data_loaded | placeholder_anchor_only | from 2025-07-01 | super_guarantee_rate=12.0 percent | True | Public rate setting used only to anchor a superannuation contribution pressure placeholder. |
| help_threshold_source_reference_extract | study_assist_help_thresholds_2025_26 | source_reference_only | source_reference_only | 2025-26 | source reference only | True | Source-reference-only record; no threshold value is loaded in this build. |
| qld_payroll_tax_source_reference_extract | qld_payroll_tax_threshold_2025_26 | source_reference_only | source_reference_only | 2025-26 | source reference only | True | Source-reference-only record; no payroll threshold value is loaded in this build. |
| abs_labour_source_reference_extract | abs_labour_wage_aggregate_source_reference | source_reference_only | source_reference_only | 2026 | source reference only | True | Source-reference-only record; no ABS aggregate table is loaded in this build. |

## F. Realistic Placeholder Anchors

| Anchor ID | Field | Public Data Anchored | Strength | Blocked By Restricted Data | Missing Data For Calibration | Must Remain Placeholder |
| --- | --- | --- | --- | --- | --- | --- |
| anchor_opfte_minimum_wage | opfte_benchmarks | True | moderate | True | occupation-specific hours, sector-specific labour requirements, schedule authority method | True |
| anchor_hle_minimum_wage | hle_assumptions | True | weak | True | human labour equivalent method, occupation mix, worker-hour evidence | True |
| anchor_qlc_minimum_wage | qlc_weights | True | weak | True | qualified labour contribution method, task allocation evidence, sector labour mix | True |
| anchor_sector_schedule_source_reference | sector_schedule_values | True | weak | True | sector schedule authority method, mixed-unit attribution, sector-specific output units | True |
| anchor_fiscal_public_aggregates | fiscal_trajectory_assumptions | True | moderate | True | CARSF behavioural response method, revenue capture method, fiscal incidence method | True |
| anchor_payg_public_tax_stats | payg_erosion_assumptions | True | weak | True | employment-tax pathway method, sector attribution, behavioural response method | True |
| anchor_super_guarantee_rate | superannuation_contribution_pressure | True | moderate | True | wage base, employer contribution records, payment interaction method | True |
| anchor_help_source_reference | help_hecs_repayment_pressure | False | source_reference_only | True | income distribution, individual repayment records, eligibility law review | True |
| anchor_payroll_tax_source_reference | state_payroll_tax_pressure | False | source_reference_only | True | jurisdiction-specific payroll base, employer records, tax-law review | True |
| anchor_transition_public_reference | transition_payment_assumptions | True | weak | True | transition eligibility method, payment administrative data, fiscal design review | True |
| anchor_uncertainty_source_reference_only | uncertainty_range_assumptions | False | source_reference_only | True | statistical sampling frame, confidence method, authorised microdata | True |

## G. Field Sanity Checks

| Check ID | Field | Type | Status | Claim Level | Extracts | Anchors | Finding |
| --- | --- | --- | --- | --- | --- | --- | --- |
| check_opfte_public_wage_anchor | opfte_benchmarks | value_presence_check | passed | placeholder_anchor_only | fair_work_minimum_wage_2025_extract | anchor_opfte_minimum_wage | A public wage threshold exists as a small placeholder anchor; it does not calibrate OPFTE. |
| check_hle_public_wage_anchor | hle_assumptions | range_plausibility_check | warning | placeholder_anchor_only | fair_work_minimum_wage_2025_extract | anchor_hle_minimum_wage | The public wage anchor can make HLE placeholders more realistic but cannot model actual human labour equivalents. |
| check_qlc_public_wage_anchor | qlc_weights | value_presence_check | passed | placeholder_anchor_only | fair_work_minimum_wage_2025_extract | anchor_qlc_minimum_wage | A public wage threshold can anchor QLC placeholder units only. |
| check_fiscal_public_aggregate | fiscal_trajectory_assumptions | value_presence_check | passed | sanity_check_only | ato_taxation_statistics_2022_23_extract, treasury_budget_2026_27_receipts_extract | anchor_fiscal_public_aggregates | Public aggregate values can sanity-check scale only and do not produce fiscal modelling. |
| check_payg_public_tax_stats | payg_erosion_assumptions | range_plausibility_check | warning | sanity_check_only | ato_taxation_statistics_2022_23_extract | anchor_payg_public_tax_stats | Public tax totals provide context but do not identify CARSF-related PAYG erosion. |
| check_super_public_threshold | superannuation_contribution_pressure | value_presence_check | passed | placeholder_anchor_only | super_guarantee_2025_26_extract | anchor_super_guarantee_rate | Public rate setting can anchor a placeholder pressure field only. |
| check_help_source_reference | help_hecs_repayment_pressure | source_reference_check | warning | source_reference_only | help_threshold_source_reference_extract | anchor_help_source_reference | HELP threshold source is referenced but not extracted as a loaded public value in this build. |
| check_payroll_tax_source_reference | state_payroll_tax_pressure | source_reference_check | warning | source_reference_only | qld_payroll_tax_source_reference_extract | anchor_payroll_tax_source_reference | State payroll threshold source is referenced but not used as a loaded value in this build. |
| check_household_microdata_blocked | household_weighting_assumptions | blocked_by_restricted_data_check | blocked | blocked_by_restricted_data | None | None | Household weighting cannot be calibrated without authorised microdata methods outside the repo. |
| check_uncertainty_microdata_blocked | uncertainty_range_assumptions | blocked_by_restricted_data_check | blocked | blocked_by_restricted_data | None | anchor_uncertainty_source_reference_only | Public aggregates cannot create confidence intervals or calibrated uncertainty ranges. |

## H. Module Sanity Checks

| Module | Status | Sanity Check Possible | Calibration Possible | Blocked By Restricted Data | Claim Level | Main Blockers |
| --- | --- | --- | --- | --- | --- | --- |
| core_formula_model | placeholder_anchor_possible | True | False | True | placeholder_anchor_only | AAVA and firm inputs remain placeholder or restricted |
| sector_schedules | placeholder_anchor_possible | True | False | True | placeholder_anchor_only | schedule authority calibration and sector attribution remain unresolved |
| sector_stress_matrix | source_reference_only | True | False | True | source_reference_only | automation intensity remains metadata-only |
| fiscal_trajectory | sanity_check_possible | True | False | True | sanity_check_only | CARSF revenue pathway is not calibrated |
| transition_funding | placeholder_anchor_possible | True | False | True | placeholder_anchor_only | payment eligibility and fiscal design require external review |
| payment_interactions | placeholder_anchor_possible | True | False | True | placeholder_anchor_only | no person-level records and no eligibility law modelling |
| household_distributional | blocked_by_restricted_data | False | False | True | blocked_by_restricted_data | household microdata remains excluded |
| household_weighting | blocked_by_restricted_data | False | False | True | blocked_by_restricted_data | weighted population inference remains blocked |
| uncertainty_ranges | blocked_by_restricted_data | False | False | True | blocked_by_restricted_data | public aggregates cannot create confidence intervals |
| reviewed_scenarios | source_reference_only | True | False | True | source_reference_only | display controls remain review-state placeholders |
| executive_dashboard | source_reference_only | True | False | False | source_reference_only | dashboard remains navigation only |

## I. Restricted Data Still Required

| blocker_id | blocker | claim_level |
| --- | --- | --- |
| restricted_tax_records | Confidential tax records remain excluded | blocked_by_restricted_data |
| restricted_household_microdata | Household microdata remains excluded | blocked_by_restricted_data |
| restricted_welfare_records | Welfare and payment records remain excluded | blocked_by_restricted_data |

## J. Forbidden Repo Data Rules

| rule_id | forbidden_data_type | must_not_commit_to_repo | must_not_use_in_tests |
| --- | --- | --- | --- |
| fd_tax_records | confidential tax records | True | True |
| fd_firm_confidential_records | firm confidential records | True | True |
| fd_person_level_records | person-level records | True | True |
| fd_household_microdata | household microdata | True | True |
| fd_restricted_government_data | restricted government data | True | True |

## K. What Became More Realistic

Wage, superannuation, corporate-tax aggregate, taxation-statistics, and fiscal aggregate placeholders now have small public-source anchors for sanity-check-only or placeholder-anchor-only review.

## L. What Remains Placeholder-Only

OPFTE, HLE, QLC, sector schedule values, PAYG pressure, transition funding, payment interactions, and uncertainty assumptions remain realistic placeholders where used.

## M. What Remains Blocked

Tax records, firm confidential records, person-level records, household microdata, and restricted government data remain excluded from the repository.

## N. Digest Summary

- Digest targets total: 5
- Digests written: 5
- Digest file does not hash itself.

## O. Build 28 Readiness

- Add reviewer-facing public-data evidence map without claiming calibration.
- Keep loaded public extracts separate from source references and placeholders.
- Preserve restricted-data blockers and forbidden repo data rules.

## P. Limitations and Future Work

- Total source references: 8
- Source references created: True
- Total public aggregate extracts: 8
- Real public data loaded extracts: 5
- Source-reference-only extracts: 3
- Total placeholder anchors: 11
- Placeholders anchored to public data: 8
- Placeholders source-reference only: 3
- Total field sanity checks: 10
- Field sanity checks passed: 4
- Field sanity checks warning: 4
- Field sanity checks blocked: 2
- Total module sanity checks: 11
- Modules sanity check possible: 1
- Modules placeholder anchor possible: 4
- Modules blocked by restricted data: 10
- Digest targets total: 5
- Digests written: 5
- Forbidden claim findings: 0
- Restricted data findings: 0
- public_data_pilot_created: True
- real_public_data_loaded: True
- source_references_created: True
- realistic_placeholders_anchored: True
- real_calibration_completed: False
- restricted_data_loaded: False
- taxpayer_data_loaded: False
- firm_level_confidential_data_loaded: False
- household_microdata_loaded: False
- actual_tax_payable_determined: False
- validation_claimed: False
- approval_claimed: False
- operational_readiness_claimed: False
- legal_sufficiency_claimed: False
- official_status_claimed: False
- firm_level_liability_logic_modified: False
