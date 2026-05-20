# CARSF V1.5 Public Data Pilot Reviewer Evidence Map

Generated at: `2026-05-20T02:07:20+00:00`

## A. Purpose

This report maps Build 27 public-data pilot evidence into reviewer-facing rows without loading new data.

## B. Non-Claims

- This is a reviewer evidence map and dashboard for the public data pilot only. No new data is loaded by this build. Build 27 public aggregate extracts remain sanity-check-only or placeholder-anchor-only. This is not calibration, calibration has not been completed, public data does not prove the model works, realistic placeholders remain placeholders, realistic placeholders are not real data, realistic placeholders are not calibrated, source references are not loaded datasets, and restricted-data requirements are not data access. It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, and not official status. It does not determine actual tax payable, does not use taxpayer-level data, firm-level confidential data, household microdata, ABS DataLab, HILDA microdata, DSS/Services Australia records, ATO taxpayer records, Treasury/PBO confidential material, or restricted government data, and does not modify firm-level CARSF liability. It only maps evidence for reviewer inspection.
- Confidence labels are evidence classification labels only; they are not validation scores, not readiness scores, not maturity scores, and not approval.
- Source-reference-only records are mapped for review but are not counted as loaded public data.
- Reviewer questions are prompts for inspection and do not mean external review has occurred.

## C. How Reviewers Should Use This Map

- Treat each row as a prompt for source, arithmetic, placeholder, blocker, or boundary inspection.
- Treat confidence labels as evidence classifications only.
- Do not treat this map as calibration, validation, readiness, or approval.

## D. Evidence Status Taxonomy

- `blocked_by_restricted_data`
- `forbidden_for_repo_use`
- `loaded_public_aggregate`
- `realistic_placeholder_anchor`
- `source_reference_only`
- `synthetic_fixture`

## E. Reviewer Interpretation Taxonomy

- `inspect_arithmetic`
- `inspect_blocker`
- `inspect_non_claim_boundary`
- `inspect_placeholder_basis`
- `inspect_source`
- `not_evidence_for_calibration`
- `not_evidence_for_tax_payable`
- `not_evidence_for_validation`

## F. Confidence Labels

- `arithmetic_checked`
- `blocked_until_restricted_data_access`
- `external_review_required`
- `placeholder_anchor_only`
- `source_locator_recorded`
- `source_reference_only`

## G. Source Evidence Map

| Evidence ID | Source Reference | Publisher | Kind | URL | Evidence Status | Confidence Label | Linked Extracts | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| source_fair_work_minimum_wage_2025 | fair_work_minimum_wage_2025 | Fair Work Ombudsman | Fair_Work_public_wage_anchor | https://www.fairwork.gov.au/how-we-will-help/templates-and-guides/fact-sheets/minimum-workplace-entitlements/minimum-wages | source_reference_only | source_locator_recorded | fair_work_minimum_wage_2025_extract | calibration, validation, official_status, actual_tax_payable |
| source_ato_corporate_tax_transparency_2022_23 | ato_corporate_tax_transparency_2022_23 | Australian Taxation Office | ATO_public_aggregate | https://www.ato.gov.au/media-centre/ato-collects-100-billion-dollars-from-large-corporates | source_reference_only | source_locator_recorded | ato_corporate_transparency_2022_23_extract | calibration, validation, official_status, actual_tax_payable |
| source_ato_taxation_statistics_2022_23 | ato_taxation_statistics_2022_23 | Australian Taxation Office | ATO_public_aggregate | https://www.ato.gov.au/media-centre/2022-23-taxation-statistics-released | source_reference_only | source_locator_recorded | ato_taxation_statistics_2022_23_extract | calibration, validation, official_status, actual_tax_payable |
| source_treasury_budget_2026_27_bp1 | treasury_budget_2026_27_bp1 | Australian Government Treasury | Treasury_public_fiscal | https://budget.gov.au/content/bp1/ | source_reference_only | source_locator_recorded | treasury_budget_2026_27_receipts_extract | calibration, validation, official_status, actual_tax_payable |
| source_study_assist_help_thresholds_2025_26 | study_assist_help_thresholds_2025_26 | Australian Government StudyAssist | HELP_HECS_public_threshold | https://www.studyassist.gov.au/paying-back-your-loan/loan-repayment | source_reference_only | source_locator_recorded | help_threshold_source_reference_extract | calibration, validation, official_status, actual_tax_payable |
| source_ato_super_guarantee_2025_26 | ato_super_guarantee_2025_26 | Australian Taxation Office | Super_Guarantee_public_setting | https://www.ato.gov.au/tax-rates-and-codes/key-superannuation-rates-and-thresholds/super-guarantee | source_reference_only | source_locator_recorded | super_guarantee_2025_26_extract | calibration, validation, official_status, actual_tax_payable |
| source_qld_payroll_tax_threshold_2025_26 | qld_payroll_tax_threshold_2025_26 | Queensland Revenue Office | State_payroll_tax_public_threshold | https://qro.qld.gov.au/payroll-tax/ | source_reference_only | source_locator_recorded | qld_payroll_tax_source_reference_extract | calibration, validation, official_status, actual_tax_payable |
| source_abs_labour_wage_aggregate_source_reference | abs_labour_wage_aggregate_source_reference | Australian Bureau of Statistics | ABS_public_aggregate | https://www.abs.gov.au/statistics/labour | source_reference_only | source_locator_recorded | abs_labour_source_reference_extract | calibration, validation, official_status, actual_tax_payable |

## H. Loaded Public Extract Evidence Map

| Evidence ID | Extract | Evidence Status | Confidence Label | Claim Level | Values | Source Locator | Value Review Status | Reviewer Interpretation | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| extract_fair_work_minimum_wage_2025_extract | fair_work_minimum_wage_2025_extract | loaded_public_aggregate | arithmetic_checked | placeholder_anchor_only | national_minimum_wage_hourly=24.95 AUD_per_hour; national_minimum_wage_weekly=948.1 AUD_per_week; casual_loading=25.0 percent | Fair Work Ombudsman minimum wages fact sheet, national minimum wage paragraph for the 1 July 2025 rate and 38-hour week reference. | maintainer_arithmetic_consistency_review_not_external_validation | inspect_arithmetic, inspect_source, not_evidence_for_calibration | calibration, validation, ATO_guidance, Treasury_modelling, actual_tax_payable |
| extract_ato_corporate_transparency_2022_23_extract | ato_corporate_transparency_2022_23_extract | loaded_public_aggregate | source_locator_recorded | sanity_check_only | income_tax_received_large_corporates=97.9 AUD_billion; entities_with_no_income_tax_percent=31.0 percent | ATO media-centre article "ATO collects $100 billion dollars from large corporates", public summary of 2022-23 corporate tax transparency results. | source_locator_recorded_not_external_validation | inspect_source, not_evidence_for_calibration, not_evidence_for_tax_payable | calibration, validation, ATO_guidance, Treasury_modelling, actual_tax_payable |
| extract_ato_taxation_statistics_2022_23_extract | ato_taxation_statistics_2022_23_extract | loaded_public_aggregate | source_locator_recorded | sanity_check_only | total_tax_revenue_collected=577.4 AUD_billion; company_tax_revenue=140.0 AUD_billion | ATO media-centre article "2022-23 taxation statistics released", public headline aggregate values. | source_locator_recorded_not_external_validation | inspect_source, not_evidence_for_calibration, not_evidence_for_tax_payable | calibration, validation, ATO_guidance, Treasury_modelling, actual_tax_payable |
| extract_treasury_budget_2026_27_receipts_extract | treasury_budget_2026_27_receipts_extract | loaded_public_aggregate | source_locator_recorded | sanity_check_only | total_receipts_estimate=759.8 AUD_billion; taxation_receipts_estimate=699.5 AUD_billion | Budget Paper No. 1 2026-27, Statement 5 Revenue, Table 5.1 Australian Government general government receipts, 2025-26 estimates. | exact_table_locator_recorded_not_external_validation | inspect_source, not_evidence_for_calibration, not_evidence_for_tax_payable | calibration, validation, ATO_guidance, Treasury_modelling, actual_tax_payable |
| extract_super_guarantee_2025_26_extract | super_guarantee_2025_26_extract | loaded_public_aggregate | source_locator_recorded | placeholder_anchor_only | super_guarantee_rate=12.0 percent | ATO key superannuation rates and thresholds page, super guarantee percentage table for the period from 1 July 2025. | source_locator_recorded_not_external_validation | inspect_source, not_evidence_for_calibration, not_evidence_for_tax_payable | calibration, validation, ATO_guidance, Treasury_modelling, actual_tax_payable |

## I. Source-Reference-Only Evidence Map

| Evidence ID | Extract | Evidence Status | Confidence Label | Claim Level | Values | Source Locator | Value Review Status | Reviewer Interpretation | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| extract_help_threshold_source_reference_extract | help_threshold_source_reference_extract | source_reference_only | source_reference_only | source_reference_only | source reference only | source reference only | source reference only | inspect_source, not_evidence_for_calibration, not_evidence_for_tax_payable | calibration, validation, ATO_guidance, Treasury_modelling, actual_tax_payable |
| extract_qld_payroll_tax_source_reference_extract | qld_payroll_tax_source_reference_extract | source_reference_only | source_reference_only | source_reference_only | source reference only | source reference only | source reference only | inspect_source, not_evidence_for_calibration, not_evidence_for_tax_payable | calibration, validation, ATO_guidance, Treasury_modelling, actual_tax_payable |
| extract_abs_labour_source_reference_extract | abs_labour_source_reference_extract | source_reference_only | source_reference_only | source_reference_only | source reference only | source reference only | source reference only | inspect_source, not_evidence_for_calibration, not_evidence_for_tax_payable | calibration, validation, ATO_guidance, Treasury_modelling, actual_tax_payable |

## J. Realistic Placeholder Evidence Map

| Evidence ID | Anchor | Field | Public Data Anchored | Strength | Confidence Label | Blocked By Restricted Data | Missing Data For Calibration | Must Not Infer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| placeholder_anchor_opfte_minimum_wage | anchor_opfte_minimum_wage | opfte_benchmarks | True | moderate | placeholder_anchor_only | True | occupation-specific hours, sector-specific labour requirements, schedule authority method | real_data_replacement, calibration, validation, actual_tax_payable |
| placeholder_anchor_hle_minimum_wage | anchor_hle_minimum_wage | hle_assumptions | True | weak | placeholder_anchor_only | True | human labour equivalent method, occupation mix, worker-hour evidence | real_data_replacement, calibration, validation, actual_tax_payable |
| placeholder_anchor_qlc_minimum_wage | anchor_qlc_minimum_wage | qlc_weights | True | weak | placeholder_anchor_only | True | qualified labour contribution method, task allocation evidence, sector labour mix | real_data_replacement, calibration, validation, actual_tax_payable |
| placeholder_anchor_sector_schedule_source_reference | anchor_sector_schedule_source_reference | sector_schedule_values | True | weak | placeholder_anchor_only | True | sector schedule authority method, mixed-unit attribution, sector-specific output units | real_data_replacement, calibration, validation, actual_tax_payable |
| placeholder_anchor_fiscal_public_aggregates | anchor_fiscal_public_aggregates | fiscal_trajectory_assumptions | True | moderate | placeholder_anchor_only | True | CARSF behavioural response method, revenue capture method, fiscal incidence method | real_data_replacement, calibration, validation, actual_tax_payable |
| placeholder_anchor_payg_public_tax_stats | anchor_payg_public_tax_stats | payg_erosion_assumptions | True | weak | placeholder_anchor_only | True | employment-tax pathway method, sector attribution, behavioural response method | real_data_replacement, calibration, validation, actual_tax_payable |
| placeholder_anchor_super_guarantee_rate | anchor_super_guarantee_rate | superannuation_contribution_pressure | True | moderate | placeholder_anchor_only | True | wage base, employer contribution records, payment interaction method | real_data_replacement, calibration, validation, actual_tax_payable |
| placeholder_anchor_help_source_reference | anchor_help_source_reference | help_hecs_repayment_pressure | False | source_reference_only | source_reference_only | True | income distribution, individual repayment records, eligibility law review | real_data_replacement, calibration, validation, actual_tax_payable |
| placeholder_anchor_payroll_tax_source_reference | anchor_payroll_tax_source_reference | state_payroll_tax_pressure | False | source_reference_only | source_reference_only | True | jurisdiction-specific payroll base, employer records, tax-law review | real_data_replacement, calibration, validation, actual_tax_payable |
| placeholder_anchor_transition_public_reference | anchor_transition_public_reference | transition_payment_assumptions | True | weak | placeholder_anchor_only | True | transition eligibility method, payment administrative data, fiscal design review | real_data_replacement, calibration, validation, actual_tax_payable |
| placeholder_anchor_uncertainty_source_reference_only | anchor_uncertainty_source_reference_only | uncertainty_range_assumptions | False | source_reference_only | source_reference_only | True | statistical sampling frame, confidence method, authorised microdata | real_data_replacement, calibration, validation, actual_tax_payable |

## K. Field Sanity Evidence Map

| Evidence ID | Field | Check Type | Check Status | Evidence Status | Confidence Label | Extracts | Anchors | Finding |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| field_check_opfte_public_wage_anchor | opfte_benchmarks | value_presence_check | passed | loaded_public_aggregate | arithmetic_checked | fair_work_minimum_wage_2025_extract | anchor_opfte_minimum_wage | A public wage threshold exists as a small placeholder anchor; it does not calibrate OPFTE. |
| field_check_hle_public_wage_anchor | hle_assumptions | range_plausibility_check | warning | loaded_public_aggregate | arithmetic_checked | fair_work_minimum_wage_2025_extract | anchor_hle_minimum_wage | The public wage anchor can make HLE placeholders more realistic but cannot model actual human labour equivalents. |
| field_check_qlc_public_wage_anchor | qlc_weights | value_presence_check | passed | loaded_public_aggregate | arithmetic_checked | fair_work_minimum_wage_2025_extract | anchor_qlc_minimum_wage | A public wage threshold can anchor QLC placeholder units only. |
| field_check_fiscal_public_aggregate | fiscal_trajectory_assumptions | value_presence_check | passed | loaded_public_aggregate | source_locator_recorded | ato_taxation_statistics_2022_23_extract, treasury_budget_2026_27_receipts_extract | anchor_fiscal_public_aggregates | Public aggregate values can sanity-check scale only and do not produce fiscal modelling. |
| field_check_payg_public_tax_stats | payg_erosion_assumptions | range_plausibility_check | warning | loaded_public_aggregate | source_locator_recorded | ato_taxation_statistics_2022_23_extract | anchor_payg_public_tax_stats | Public tax totals provide context but do not identify CARSF-related PAYG erosion. |
| field_check_super_public_threshold | superannuation_contribution_pressure | value_presence_check | passed | loaded_public_aggregate | source_locator_recorded | super_guarantee_2025_26_extract | anchor_super_guarantee_rate | Public rate setting can anchor a placeholder pressure field only. |
| field_check_help_source_reference | help_hecs_repayment_pressure | source_reference_check | warning | source_reference_only | source_reference_only | help_threshold_source_reference_extract | anchor_help_source_reference | HELP threshold source is referenced but not extracted as a loaded public value in this build. |
| field_check_payroll_tax_source_reference | state_payroll_tax_pressure | source_reference_check | warning | source_reference_only | source_reference_only | qld_payroll_tax_source_reference_extract | anchor_payroll_tax_source_reference | State payroll threshold source is referenced but not used as a loaded value in this build. |
| field_check_household_microdata_blocked | household_weighting_assumptions | blocked_by_restricted_data_check | blocked | blocked_by_restricted_data | blocked_until_restricted_data_access | None | None | Household weighting cannot be calibrated without authorised microdata methods outside the repo. |
| field_check_uncertainty_microdata_blocked | uncertainty_range_assumptions | blocked_by_restricted_data_check | blocked | blocked_by_restricted_data | blocked_until_restricted_data_access | None | anchor_uncertainty_source_reference_only | Public aggregates cannot create confidence intervals or calibrated uncertainty ranges. |

## L. Module Sanity Evidence Map

| Evidence ID | Module | Result Status | Sanity Check Possible | Calibration Possible | Evidence Status | Confidence Label | Main Blockers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| module_core_formula_model | core_formula_model | placeholder_anchor_possible | True | False | blocked_by_restricted_data | blocked_until_restricted_data_access | AAVA and firm inputs remain placeholder or restricted |
| module_sector_schedules | sector_schedules | placeholder_anchor_possible | True | False | blocked_by_restricted_data | blocked_until_restricted_data_access | schedule authority calibration and sector attribution remain unresolved |
| module_sector_stress_matrix | sector_stress_matrix | source_reference_only | True | False | blocked_by_restricted_data | blocked_until_restricted_data_access | automation intensity remains metadata-only |
| module_fiscal_trajectory | fiscal_trajectory | sanity_check_possible | True | False | blocked_by_restricted_data | blocked_until_restricted_data_access | CARSF revenue pathway is not calibrated |
| module_transition_funding | transition_funding | placeholder_anchor_possible | True | False | blocked_by_restricted_data | blocked_until_restricted_data_access | payment eligibility and fiscal design require external review |
| module_payment_interactions | payment_interactions | placeholder_anchor_possible | True | False | blocked_by_restricted_data | blocked_until_restricted_data_access | no person-level records and no eligibility law modelling |
| module_household_distributional | household_distributional | blocked_by_restricted_data | False | False | blocked_by_restricted_data | blocked_until_restricted_data_access | household microdata remains excluded |
| module_household_weighting | household_weighting | blocked_by_restricted_data | False | False | blocked_by_restricted_data | blocked_until_restricted_data_access | weighted population inference remains blocked |
| module_uncertainty_ranges | uncertainty_ranges | blocked_by_restricted_data | False | False | blocked_by_restricted_data | blocked_until_restricted_data_access | public aggregates cannot create confidence intervals |
| module_reviewed_scenarios | reviewed_scenarios | source_reference_only | True | False | blocked_by_restricted_data | blocked_until_restricted_data_access | display controls remain review-state placeholders |
| module_executive_dashboard | executive_dashboard | source_reference_only | True | False | source_reference_only | source_reference_only | dashboard remains navigation only |

## M. Restricted Blocker Evidence Map

| Evidence ID | Blocker ID | Type | Evidence Status | Confidence Label | Description | Required Access Or Review |
| --- | --- | --- | --- | --- | --- | --- |
| restricted_restricted_tax_records | restricted_tax_records | restricted_data_blocker | blocked_by_restricted_data | blocked_until_restricted_data_access | Confidential tax records remain excluded | authorised external data access process, privacy and legal review |
| restricted_restricted_household_microdata | restricted_household_microdata | restricted_data_blocker | blocked_by_restricted_data | blocked_until_restricted_data_access | Household microdata remains excluded | authorised external data access process, privacy and legal review |
| restricted_restricted_welfare_records | restricted_welfare_records | restricted_data_blocker | blocked_by_restricted_data | blocked_until_restricted_data_access | Welfare and payment records remain excluded | authorised external data access process, privacy and legal review |

## N. Forbidden Repo Data Evidence Map

| Evidence ID | Blocker ID | Type | Evidence Status | Confidence Label | Description | Required Access Or Review |
| --- | --- | --- | --- | --- | --- | --- |
| forbidden_fd_tax_records | fd_tax_records | forbidden_repo_data | forbidden_for_repo_use | external_review_required | confidential tax records | external system design if ever authorised, legal and privacy review |
| forbidden_fd_firm_confidential_records | fd_firm_confidential_records | forbidden_repo_data | forbidden_for_repo_use | external_review_required | firm confidential records | external system design if ever authorised, legal and privacy review |
| forbidden_fd_person_level_records | fd_person_level_records | forbidden_repo_data | forbidden_for_repo_use | external_review_required | person-level records | external system design if ever authorised, legal and privacy review |
| forbidden_fd_household_microdata | fd_household_microdata | forbidden_repo_data | forbidden_for_repo_use | external_review_required | household microdata | external system design if ever authorised, legal and privacy review |
| forbidden_fd_restricted_government_data | fd_restricted_government_data | forbidden_repo_data | forbidden_for_repo_use | external_review_required | restricted government data | external system design if ever authorised, legal and privacy review |

## O. Reviewer Questions

| Question ID | Category | Question | Interpretation | Target Evidence Status | Must Not Infer |
| --- | --- | --- | --- | --- | --- |
| source_001 | Source verification | Can the source URL and source locator be independently found? | inspect_source | source_reference_only | calibration, validation, official_status |
| source_002 | Source verification | Does the source reference remain aggregate-only or source-reference-only? | inspect_source | source_reference_only | taxpayer_data, firm_confidential_data, household_microdata |
| source_003 | Source verification | Is the source release name specific enough for a reviewer to locate it? | inspect_source | source_reference_only | approval, validation, calibration |
| source_004 | Source verification | Are source-reference-only records excluded from loaded public data counts? | inspect_source | source_reference_only | loaded_data, calibration, validation |
| source_005 | Source verification | Is the source being overread as official guidance or methods approval? | inspect_non_claim_boundary | source_reference_only | ATO_guidance, Treasury_modelling, PBO_costing |
| arithmetic_001 | Value arithmetic | Does the Fair Work weekly wage row equal hourly value times 38? | inspect_arithmetic | loaded_public_aggregate | calibration, validation, legal_advice |
| arithmetic_002 | Value arithmetic | Does the evidence row show arithmetic_checked only for the wage arithmetic check? | inspect_arithmetic | loaded_public_aggregate | validation_score, readiness_score, maturity_score |
| arithmetic_003 | Value arithmetic | Are rounded values clearly marked as source summaries or arithmetic checks? | inspect_arithmetic | loaded_public_aggregate | precision, forecast, actual_tax_payable |
| arithmetic_004 | Value arithmetic | Are value notes visible before interpreting each loaded row? | inspect_source | loaded_public_aggregate | calibration, validation, official_status |
| arithmetic_005 | Value arithmetic | Is any arithmetic check being overread as model evidence? | inspect_non_claim_boundary | loaded_public_aggregate | model_proof, economic_validation, statistical_validation |
| placeholder_001 | Placeholder anchoring | Is each placeholder clearly labelled as a realistic placeholder? | inspect_placeholder_basis | realistic_placeholder_anchor | real_data, calibration, validation |
| placeholder_002 | Placeholder anchoring | Does the anchor strength match the source record actually available? | inspect_placeholder_basis | realistic_placeholder_anchor | calibration, actual_tax_payable, official_status |
| placeholder_003 | Placeholder anchoring | Are missing data for calibration still listed? | inspect_placeholder_basis | realistic_placeholder_anchor | calibration_completed, validation, readiness |
| placeholder_004 | Placeholder anchoring | Does any placeholder anchor imply replacement of a placeholder? | inspect_non_claim_boundary | realistic_placeholder_anchor | real_data_replacement, calibrated_value, model_proof |
| placeholder_005 | Placeholder anchoring | Are reviewer tracks listed before any future replacement? | inspect_placeholder_basis | realistic_placeholder_anchor | approval, validation, official_status |
| blocker_001 | Restricted-data blockers | Are taxpayer-level data blockers still visible? | inspect_blocker | blocked_by_restricted_data | data_access, calibration, actual_tax_payable |
| blocker_002 | Restricted-data blockers | Are firm-confidential blockers still visible? | inspect_blocker | blocked_by_restricted_data | firm-level_liability, confidential_data_use, validation |
| blocker_003 | Restricted-data blockers | Are household microdata blockers still visible? | inspect_blocker | blocked_by_restricted_data | population_estimate, real_household_estimate, welfare_validation |
| blocker_004 | Restricted-data blockers | Are restricted government data blockers preserved in the report? | inspect_blocker | blocked_by_restricted_data | restricted_access, official_status, approval |
| blocker_005 | Restricted-data blockers | Is forbidden repo data still explicitly forbidden? | inspect_blocker | forbidden_for_repo_use | safe_repo_use, data_access, calibration |
| field_001 | Field sanity checks | Which field checks are mapped as warning rather than blocked? | inspect_source | loaded_public_aggregate | calibration, validation, actual_tax_payable |
| field_002 | Field sanity checks | Which field checks depend on source-reference-only records? | inspect_source | source_reference_only | loaded_data, calibration, validation |
| field_003 | Field sanity checks | Which field checks remain blocked by restricted data? | inspect_blocker | blocked_by_restricted_data | data_access, calibration, official_status |
| field_004 | Field sanity checks | Are field findings written as review prompts rather than conclusions? | inspect_non_claim_boundary | realistic_placeholder_anchor | model_proof, economic_validation, statistical_validation |
| field_005 | Field sanity checks | Are linked extracts and anchors traceable from each field row? | inspect_source | loaded_public_aggregate | tax_payable, calibration, validation |
| module_001 | Module sanity checks | Does every module keep calibration_possible false? | inspect_non_claim_boundary | realistic_placeholder_anchor | calibration, readiness, validation |
| module_002 | Module sanity checks | Which modules are only placeholder-anchor possible? | inspect_placeholder_basis | realistic_placeholder_anchor | model_proof, actual_tax_payable, operational_readiness |
| module_003 | Module sanity checks | Which modules remain blocked by restricted data? | inspect_blocker | blocked_by_restricted_data | data_access, calibration, validation |
| module_004 | Module sanity checks | Are source-reference-only modules separated from loaded-public-extract modules? | inspect_source | source_reference_only | loaded_data, calibration, validation |
| module_005 | Module sanity checks | Does any module text imply operational use? | inspect_non_claim_boundary | realistic_placeholder_anchor | operational_readiness, official_status, government_readiness |
| boundary_001 | Non-claim boundary | Does any output imply calibration is complete? | inspect_non_claim_boundary | realistic_placeholder_anchor | calibration_completed, validation, readiness |
| boundary_002 | Non-claim boundary | Does any output imply public data proves the model works? | inspect_non_claim_boundary | loaded_public_aggregate | model_proof, economic_validation, statistical_validation |
| boundary_003 | Non-claim boundary | Does any output imply actual tax payable? | inspect_non_claim_boundary | loaded_public_aggregate | actual_tax_payable, tax_advice, legal_advice |
| boundary_004 | Non-claim boundary | Does any output imply ATO guidance or Treasury modelling? | inspect_non_claim_boundary | source_reference_only | ATO_guidance, Treasury_modelling, PBO_costing |
| boundary_005 | Non-claim boundary | Does any output imply official status or approval? | inspect_non_claim_boundary | realistic_placeholder_anchor | official_status, approval, validation |
| route_001 | External review route | Which fields require statistical methods review? | inspect_blocker | blocked_by_restricted_data | statistical_validation, calibration, confidence_interval |
| route_002 | External review route | Which fields require economic methods review? | inspect_blocker | blocked_by_restricted_data | economic_validation, forecast, policy_result |
| route_003 | External review route | Which fields require legal or tax review? | inspect_blocker | blocked_by_restricted_data | legal_sufficiency, tax_advice, operative_law |
| route_004 | External review route | Which source rows require source review before Build 29 reconciliation? | inspect_source | source_reference_only | approval, validation, official_pathway |
| route_005 | External review route | Are review routes framed as suggested review prompts only? | inspect_non_claim_boundary | realistic_placeholder_anchor | official_review_pathway, approval, validation |
| build29_001 | Build 29 readiness | Are source locators present for loaded public extracts? | inspect_source | loaded_public_aggregate | validation, calibration, approval |
| build29_002 | Build 29 readiness | Are arithmetic checks represented without claiming model evidence? | inspect_arithmetic | loaded_public_aggregate | model_proof, validation, readiness |
| build29_003 | Build 29 readiness | Are source-reference-only rows preserved for reconciliation? | inspect_source | source_reference_only | loaded_data, calibration, validation |
| build29_004 | Build 29 readiness | Are digest and report paths visible for later reconciliation? | inspect_source | loaded_public_aggregate | external_attestation, approval, validation |
| build29_005 | Build 29 readiness | Are non-claim boundaries visible before any source reconciliation audit? | inspect_non_claim_boundary | realistic_placeholder_anchor | readiness, official_status, legal_sufficiency |

## P. What Became More Reviewable

Reviewers can now inspect source locators, arithmetic classification, placeholder anchors, field rows, module rows, and blocker rows in one report.

## Q. What Still Cannot Be Claimed

This evidence map is not calibration, not validation, not tax-payable use, not legal sufficiency, not operational readiness, not official status, and not a firm-level liability change.

## R. Build 29 Readiness

- Source-reconciliation audit should check source locator metadata against public source references without loading new data.
- Source-reference-only records should remain excluded from loaded public data counts.
- Placeholder anchors should remain labelled as placeholders until external review and authorised calibration design.
- Restricted-data blockers and forbidden repo data rules should remain visible.

## S. Limitations and Future Work

- Total source evidence items: 8
- Total loaded public extract evidence items: 5
- Total source-reference-only evidence items: 3
- Total placeholder evidence items: 11
- Total field sanity evidence items: 10
- Field sanity passed: 4
- Field sanity warning: 4
- Field sanity blocked: 2
- Total module sanity evidence items: 11
- Modules sanity check possible: 1
- Modules placeholder anchor possible: 4
- Modules blocked by restricted data: 10
- Total restricted blocker items: 3
- Total forbidden repo data items: 5
- Total reviewer questions: 45
- Forbidden claim findings: 0
- evidence_map_created: True
- new_data_loaded: False
- real_public_data_loaded_from_build_27_only: True
- source_references_mapped: True
- loaded_public_extracts_mapped: True
- source_reference_only_records_mapped: True
- realistic_placeholders_mapped: True
- restricted_blockers_mapped: True
- real_calibration_completed: False
- actual_tax_payable_determined: False
- validation_claimed: False
- approval_claimed: False
- operational_readiness_claimed: False
- legal_sufficiency_claimed: False
- official_status_claimed: False
- firm_level_liability_logic_modified: False
