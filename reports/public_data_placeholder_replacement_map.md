# CARSF V1.5 Public Data Placeholder Replacement Map

Generated at: `2026-05-21T05:10:33+00:00`

## A. Purpose

This report maps Build 31 public aggregate values to existing realistic placeholders.

## B. Non-Claims

- This is a public data placeholder replacement map only. No new data is loaded by this build. Public aggregate data can anchor or narrow some placeholders, but does not calibrate the model. Replaced by public aggregate anchor does not mean validated. Narrowed by public aggregate anchor does not mean statistically estimated. Informed by public aggregate anchor does not mean representative. Placeholder-only items remain placeholders. Restricted-data blockers remain blockers. Calibration has not been completed. Public data does not prove the model works. This is not validation, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, and not official status. It does not determine actual tax payable and does not modify firm-level CARSF liability.
- Build 32 uses Build 31 loaded public aggregate values only and does not add new public source values.
- Replacement, narrowing, and context labels are mapping labels only; they are not calibration or validation.
- Source candidates not loaded in Build 31 remain not loaded and future-only.

## C. Input Public Aggregate Values

| Value ID | Source | Metric | Value | Unit | Period | Geography |
| --- | --- | --- | --- | --- | --- | --- |
| fair_work_national_minimum_wage_hourly_2025 | fair_work_minimum_wage_2025 | National minimum wage hourly rate | 24.95 | AUD_per_hour | from 2025-07-01 | Australia |
| fair_work_national_minimum_wage_weekly_2025 | fair_work_minimum_wage_2025 | National minimum wage weekly rate | 948.1 | AUD_per_week | from 2025-07-01 | Australia |
| fair_work_casual_loading_2025 | fair_work_minimum_wage_2025 | Casual loading percentage | 25.0 | percent | from 2025-07-01 | Australia |
| ato_large_corporate_income_tax_received_2022_23 | ato_corporate_tax_transparency_2022_23 | Income tax received from large corporates | 97.9 | AUD_billion | 2022-23 | Australia |
| ato_large_corporate_entities_no_income_tax_percent_2022_23 | ato_corporate_tax_transparency_2022_23 | Entities with no income tax payable in public report | 31.0 | percent | 2022-23 | Australia |
| ato_total_tax_revenue_collected_2022_23 | ato_taxation_statistics_2022_23 | Total tax revenue collected | 577.4 | AUD_billion | 2022-23 | Australia |
| ato_company_tax_revenue_2022_23 | ato_taxation_statistics_2022_23 | Company tax revenue | 140.0 | AUD_billion | 2022-23 | Australia |
| treasury_total_receipts_2025_26_estimate | treasury_budget_2026_27_bp1 | Total receipts estimate | 759.8 | AUD_billion | 2025-26 estimate in Budget Paper No. 1 2026-27 | Australia |
| treasury_taxation_receipts_2025_26_estimate | treasury_budget_2026_27_bp1 | Taxation receipts estimate | 699.5 | AUD_billion | 2025-26 estimate in Budget Paper No. 1 2026-27 | Australia |
| ato_super_guarantee_rate_2025_26 | ato_super_guarantee_2025_26 | Super guarantee percentage | 12.0 | percent | from 2025-07-01 | Australia |

## D. Replacement Status Taxonomy

- `blocked_until_external_review`
- `blocked_until_restricted_data`
- `cannot_replace_with_public_aggregate_data`
- `informed_by_public_aggregate_anchor`
- `narrowed_by_public_aggregate_anchor`
- `replaced_by_public_aggregate_anchor`
- `still_placeholder_only`

## E. Replacement Confidence Taxonomy

- `blocked_by_required_restricted_data`
- `contextual_public_aggregate_only`
- `direct_public_aggregate_anchor`
- `external_review_required`
- `placeholder_only`
- `public_aggregate_bound_only`

## F. Placeholder Replacement Decisions

| Decision | Placeholder | Field | Status | Confidence | Claim Level | Linked Values | What Changed | Remaining Blockers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| decision_anchor_fiscal_public_aggregates | Fiscal public aggregate sanity anchor | fiscal_trajectory_assumptions | narrowed_by_public_aggregate_anchor | public_aggregate_bound_only | placeholder_narrowing_only | ato_large_corporate_income_tax_received_2022_23, ato_large_corporate_entities_no_income_tax_percent_2022_23, ato_total_tax_revenue_collected_2022_23, ato_company_tax_revenue_2022_23, treasury_total_receipts_2025_26_estimate, treasury_taxation_receipts_2025_26_estimate | Fiscal placeholders now link to loaded ATO and Budget receipt scale anchors. | economic_review_required, restricted_tax_data_required, behavioural_elasticity_required |
| decision_anchor_help_source_reference | HELP threshold source-reference anchor | help_hecs_repayment_pressure | blocked_until_restricted_data | blocked_by_required_restricted_data | blocked_placeholder | None | No Build 31 public HELP value was loaded; the HELP threshold source remains future-only. | welfare_payment_records_required, household_microdata_required, legal_review_required |
| decision_anchor_hle_minimum_wage | HLE public wage anchor | hle_assumptions | narrowed_by_public_aggregate_anchor | public_aggregate_bound_only | placeholder_narrowing_only | fair_work_national_minimum_wage_hourly_2025, fair_work_national_minimum_wage_weekly_2025, fair_work_casual_loading_2025 | The HLE labour-cost placeholder can be bounded by loaded wage and casual-loading public anchors. | statistical_review_required, behavioural_elasticity_required, public_aggregate_data_insufficient |
| decision_anchor_opfte_minimum_wage | OPFTE public wage anchor | opfte_benchmarks | replaced_by_public_aggregate_anchor | direct_public_aggregate_anchor | public_aggregate_anchor_only | fair_work_national_minimum_wage_hourly_2025, fair_work_national_minimum_wage_weekly_2025 | The OPFTE wage placeholder is now linked to loaded public hourly and weekly national minimum wage anchors. | statistical_review_required, restricted_tax_data_required, public_aggregate_data_insufficient |
| decision_anchor_payg_public_tax_stats | PAYG public tax-statistics sanity anchor | payg_erosion_assumptions | informed_by_public_aggregate_anchor | contextual_public_aggregate_only | contextual_anchor_only | ato_total_tax_revenue_collected_2022_23, ato_company_tax_revenue_2022_23 | PAYG erosion placeholders now reference loaded public tax aggregate context. | restricted_tax_data_required, statistical_review_required, public_aggregate_data_insufficient |
| decision_anchor_payroll_tax_source_reference | State payroll threshold source-reference anchor | state_payroll_tax_pressure | blocked_until_external_review | external_review_required | blocked_placeholder | None | No Build 31 public state payroll threshold value was loaded; the source remains future-only. | firm_confidential_data_required, tax_review_required, public_aggregate_data_insufficient |
| decision_anchor_qlc_minimum_wage | QLC public wage anchor | qlc_weights | narrowed_by_public_aggregate_anchor | public_aggregate_bound_only | placeholder_narrowing_only | fair_work_national_minimum_wage_hourly_2025, fair_work_national_minimum_wage_weekly_2025 | The QLC wage component can be bounded by loaded public wage thresholds. | statistical_review_required, tax_review_required, public_aggregate_data_insufficient |
| decision_anchor_sector_schedule_source_reference | Sector schedule public source-reference anchor | sector_schedule_values | informed_by_public_aggregate_anchor | contextual_public_aggregate_only | contextual_anchor_only | fair_work_national_minimum_wage_hourly_2025, fair_work_casual_loading_2025 | Loaded wage anchors give sector-schedule placeholders labour-cost context. | statistical_review_required, legal_review_required, public_aggregate_data_insufficient |
| decision_anchor_super_guarantee_rate | Superannuation Guarantee public setting anchor | superannuation_contribution_pressure | replaced_by_public_aggregate_anchor | direct_public_aggregate_anchor | public_aggregate_anchor_only | ato_super_guarantee_rate_2025_26 | The superannuation guarantee placeholder now links to a loaded public rate setting. | firm_confidential_data_required, welfare_payment_records_required, tax_review_required |
| decision_anchor_transition_public_reference | Transition funding public aggregate reference anchor | transition_payment_assumptions | informed_by_public_aggregate_anchor | contextual_public_aggregate_only | contextual_anchor_only | treasury_total_receipts_2025_26_estimate, treasury_taxation_receipts_2025_26_estimate, ato_super_guarantee_rate_2025_26 | Transition funding placeholders now link to loaded fiscal receipt and superannuation context anchors. | welfare_payment_records_required, economic_review_required, legal_review_required |
| decision_anchor_uncertainty_source_reference_only | Uncertainty source-reference-only anchor | uncertainty_range_assumptions | cannot_replace_with_public_aggregate_data | blocked_by_required_restricted_data | cannot_support_replacement | ato_total_tax_revenue_collected_2022_23, ato_company_tax_revenue_2022_23 | Public aggregate tax values provide context but cannot replace uncertainty placeholders. | household_microdata_required, statistical_review_required, public_aggregate_data_insufficient |

## G. Replaced By Public Aggregate Anchor

| Decision | Placeholder | Field | Status | Confidence | Claim Level | Linked Values | What Changed | Remaining Blockers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| decision_anchor_opfte_minimum_wage | OPFTE public wage anchor | opfte_benchmarks | replaced_by_public_aggregate_anchor | direct_public_aggregate_anchor | public_aggregate_anchor_only | fair_work_national_minimum_wage_hourly_2025, fair_work_national_minimum_wage_weekly_2025 | The OPFTE wage placeholder is now linked to loaded public hourly and weekly national minimum wage anchors. | statistical_review_required, restricted_tax_data_required, public_aggregate_data_insufficient |
| decision_anchor_super_guarantee_rate | Superannuation Guarantee public setting anchor | superannuation_contribution_pressure | replaced_by_public_aggregate_anchor | direct_public_aggregate_anchor | public_aggregate_anchor_only | ato_super_guarantee_rate_2025_26 | The superannuation guarantee placeholder now links to a loaded public rate setting. | firm_confidential_data_required, welfare_payment_records_required, tax_review_required |

## H. Narrowed By Public Aggregate Anchor

| Decision | Placeholder | Field | Status | Confidence | Claim Level | Linked Values | What Changed | Remaining Blockers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| decision_anchor_fiscal_public_aggregates | Fiscal public aggregate sanity anchor | fiscal_trajectory_assumptions | narrowed_by_public_aggregate_anchor | public_aggregate_bound_only | placeholder_narrowing_only | ato_large_corporate_income_tax_received_2022_23, ato_large_corporate_entities_no_income_tax_percent_2022_23, ato_total_tax_revenue_collected_2022_23, ato_company_tax_revenue_2022_23, treasury_total_receipts_2025_26_estimate, treasury_taxation_receipts_2025_26_estimate | Fiscal placeholders now link to loaded ATO and Budget receipt scale anchors. | economic_review_required, restricted_tax_data_required, behavioural_elasticity_required |
| decision_anchor_hle_minimum_wage | HLE public wage anchor | hle_assumptions | narrowed_by_public_aggregate_anchor | public_aggregate_bound_only | placeholder_narrowing_only | fair_work_national_minimum_wage_hourly_2025, fair_work_national_minimum_wage_weekly_2025, fair_work_casual_loading_2025 | The HLE labour-cost placeholder can be bounded by loaded wage and casual-loading public anchors. | statistical_review_required, behavioural_elasticity_required, public_aggregate_data_insufficient |
| decision_anchor_qlc_minimum_wage | QLC public wage anchor | qlc_weights | narrowed_by_public_aggregate_anchor | public_aggregate_bound_only | placeholder_narrowing_only | fair_work_national_minimum_wage_hourly_2025, fair_work_national_minimum_wage_weekly_2025 | The QLC wage component can be bounded by loaded public wage thresholds. | statistical_review_required, tax_review_required, public_aggregate_data_insufficient |

## I. Informed By Public Aggregate Anchor

| Decision | Placeholder | Field | Status | Confidence | Claim Level | Linked Values | What Changed | Remaining Blockers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| decision_anchor_payg_public_tax_stats | PAYG public tax-statistics sanity anchor | payg_erosion_assumptions | informed_by_public_aggregate_anchor | contextual_public_aggregate_only | contextual_anchor_only | ato_total_tax_revenue_collected_2022_23, ato_company_tax_revenue_2022_23 | PAYG erosion placeholders now reference loaded public tax aggregate context. | restricted_tax_data_required, statistical_review_required, public_aggregate_data_insufficient |
| decision_anchor_sector_schedule_source_reference | Sector schedule public source-reference anchor | sector_schedule_values | informed_by_public_aggregate_anchor | contextual_public_aggregate_only | contextual_anchor_only | fair_work_national_minimum_wage_hourly_2025, fair_work_casual_loading_2025 | Loaded wage anchors give sector-schedule placeholders labour-cost context. | statistical_review_required, legal_review_required, public_aggregate_data_insufficient |
| decision_anchor_transition_public_reference | Transition funding public aggregate reference anchor | transition_payment_assumptions | informed_by_public_aggregate_anchor | contextual_public_aggregate_only | contextual_anchor_only | treasury_total_receipts_2025_26_estimate, treasury_taxation_receipts_2025_26_estimate, ato_super_guarantee_rate_2025_26 | Transition funding placeholders now link to loaded fiscal receipt and superannuation context anchors. | welfare_payment_records_required, economic_review_required, legal_review_required |

## J. Still Placeholder Only

| Decision | Placeholder | Field | Status | Confidence | Claim Level | Linked Values | What Changed | Remaining Blockers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

## K. Blocked Until Restricted Data

| Decision | Placeholder | Field | Status | Confidence | Claim Level | Linked Values | What Changed | Remaining Blockers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| decision_anchor_help_source_reference | HELP threshold source-reference anchor | help_hecs_repayment_pressure | blocked_until_restricted_data | blocked_by_required_restricted_data | blocked_placeholder | None | No Build 31 public HELP value was loaded; the HELP threshold source remains future-only. | welfare_payment_records_required, household_microdata_required, legal_review_required |

## L. Blocked Until External Review

| Decision | Placeholder | Field | Status | Confidence | Claim Level | Linked Values | What Changed | Remaining Blockers |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| decision_anchor_fiscal_public_aggregates | Fiscal public aggregate sanity anchor | fiscal_trajectory_assumptions | narrowed_by_public_aggregate_anchor | public_aggregate_bound_only | placeholder_narrowing_only | ato_large_corporate_income_tax_received_2022_23, ato_large_corporate_entities_no_income_tax_percent_2022_23, ato_total_tax_revenue_collected_2022_23, ato_company_tax_revenue_2022_23, treasury_total_receipts_2025_26_estimate, treasury_taxation_receipts_2025_26_estimate | Fiscal placeholders now link to loaded ATO and Budget receipt scale anchors. | economic_review_required, restricted_tax_data_required, behavioural_elasticity_required |
| decision_anchor_help_source_reference | HELP threshold source-reference anchor | help_hecs_repayment_pressure | blocked_until_restricted_data | blocked_by_required_restricted_data | blocked_placeholder | None | No Build 31 public HELP value was loaded; the HELP threshold source remains future-only. | welfare_payment_records_required, household_microdata_required, legal_review_required |
| decision_anchor_hle_minimum_wage | HLE public wage anchor | hle_assumptions | narrowed_by_public_aggregate_anchor | public_aggregate_bound_only | placeholder_narrowing_only | fair_work_national_minimum_wage_hourly_2025, fair_work_national_minimum_wage_weekly_2025, fair_work_casual_loading_2025 | The HLE labour-cost placeholder can be bounded by loaded wage and casual-loading public anchors. | statistical_review_required, behavioural_elasticity_required, public_aggregate_data_insufficient |
| decision_anchor_opfte_minimum_wage | OPFTE public wage anchor | opfte_benchmarks | replaced_by_public_aggregate_anchor | direct_public_aggregate_anchor | public_aggregate_anchor_only | fair_work_national_minimum_wage_hourly_2025, fair_work_national_minimum_wage_weekly_2025 | The OPFTE wage placeholder is now linked to loaded public hourly and weekly national minimum wage anchors. | statistical_review_required, restricted_tax_data_required, public_aggregate_data_insufficient |
| decision_anchor_payg_public_tax_stats | PAYG public tax-statistics sanity anchor | payg_erosion_assumptions | informed_by_public_aggregate_anchor | contextual_public_aggregate_only | contextual_anchor_only | ato_total_tax_revenue_collected_2022_23, ato_company_tax_revenue_2022_23 | PAYG erosion placeholders now reference loaded public tax aggregate context. | restricted_tax_data_required, statistical_review_required, public_aggregate_data_insufficient |
| decision_anchor_payroll_tax_source_reference | State payroll threshold source-reference anchor | state_payroll_tax_pressure | blocked_until_external_review | external_review_required | blocked_placeholder | None | No Build 31 public state payroll threshold value was loaded; the source remains future-only. | firm_confidential_data_required, tax_review_required, public_aggregate_data_insufficient |
| decision_anchor_qlc_minimum_wage | QLC public wage anchor | qlc_weights | narrowed_by_public_aggregate_anchor | public_aggregate_bound_only | placeholder_narrowing_only | fair_work_national_minimum_wage_hourly_2025, fair_work_national_minimum_wage_weekly_2025 | The QLC wage component can be bounded by loaded public wage thresholds. | statistical_review_required, tax_review_required, public_aggregate_data_insufficient |
| decision_anchor_sector_schedule_source_reference | Sector schedule public source-reference anchor | sector_schedule_values | informed_by_public_aggregate_anchor | contextual_public_aggregate_only | contextual_anchor_only | fair_work_national_minimum_wage_hourly_2025, fair_work_casual_loading_2025 | Loaded wage anchors give sector-schedule placeholders labour-cost context. | statistical_review_required, legal_review_required, public_aggregate_data_insufficient |
| decision_anchor_super_guarantee_rate | Superannuation Guarantee public setting anchor | superannuation_contribution_pressure | replaced_by_public_aggregate_anchor | direct_public_aggregate_anchor | public_aggregate_anchor_only | ato_super_guarantee_rate_2025_26 | The superannuation guarantee placeholder now links to a loaded public rate setting. | firm_confidential_data_required, welfare_payment_records_required, tax_review_required |
| decision_anchor_transition_public_reference | Transition funding public aggregate reference anchor | transition_payment_assumptions | informed_by_public_aggregate_anchor | contextual_public_aggregate_only | contextual_anchor_only | treasury_total_receipts_2025_26_estimate, treasury_taxation_receipts_2025_26_estimate, ato_super_guarantee_rate_2025_26 | Transition funding placeholders now link to loaded fiscal receipt and superannuation context anchors. | welfare_payment_records_required, economic_review_required, legal_review_required |
| decision_anchor_uncertainty_source_reference_only | Uncertainty source-reference-only anchor | uncertainty_range_assumptions | cannot_replace_with_public_aggregate_data | blocked_by_required_restricted_data | cannot_support_replacement | ato_total_tax_revenue_collected_2022_23, ato_company_tax_revenue_2022_23 | Public aggregate tax values provide context but cannot replace uncertainty placeholders. | household_microdata_required, statistical_review_required, public_aggregate_data_insufficient |

## M. Source Candidates Not Loaded

| Source ID | Publisher | Source | Status | Reason | Treated As Loaded |
| --- | --- | --- | --- | --- | --- |
| study_assist_help_thresholds_2025_26 | Australian Government StudyAssist | HELP repayment public threshold source | source_candidate_not_loaded | Exact public threshold value was not safely recorded in local Build 31 source metadata. | False |
| qld_payroll_tax_threshold_2025_26 | Queensland Revenue Office | Queensland payroll tax public threshold source | source_candidate_not_loaded | Exact jurisdiction threshold value was not safely recorded in local Build 31 source metadata. | False |
| abs_labour_wage_aggregate_source_reference | Australian Bureau of Statistics | ABS labour aggregate source candidate | source_candidate_not_loaded | Exact public aggregate table selection remains deferred until a later loader expansion. | False |

## N. What Changed

- `anchor_fiscal_public_aggregates`: Fiscal placeholders now link to loaded ATO and Budget receipt scale anchors.
- `anchor_help_source_reference`: No Build 31 public HELP value was loaded; the HELP threshold source remains future-only.
- `anchor_hle_minimum_wage`: The HLE labour-cost placeholder can be bounded by loaded wage and casual-loading public anchors.
- `anchor_opfte_minimum_wage`: The OPFTE wage placeholder is now linked to loaded public hourly and weekly national minimum wage anchors.
- `anchor_payg_public_tax_stats`: PAYG erosion placeholders now reference loaded public tax aggregate context.
- `anchor_payroll_tax_source_reference`: No Build 31 public state payroll threshold value was loaded; the source remains future-only.
- `anchor_qlc_minimum_wage`: The QLC wage component can be bounded by loaded public wage thresholds.
- `anchor_sector_schedule_source_reference`: Loaded wage anchors give sector-schedule placeholders labour-cost context.
- `anchor_super_guarantee_rate`: The superannuation guarantee placeholder now links to a loaded public rate setting.
- `anchor_transition_public_reference`: Transition funding placeholders now link to loaded fiscal receipt and superannuation context anchors.
- `anchor_uncertainty_source_reference_only`: Public aggregate tax values provide context but cannot replace uncertainty placeholders.

## O. What Did Not Change

- `anchor_fiscal_public_aggregates`: The fiscal trajectory remains a placeholder; no CARSF revenue pathway, fiscal incidence, Treasury modelling, or PBO costing is created.
- `anchor_help_source_reference`: HELP repayment pressure remains placeholder-only and cannot estimate individual repayment pressure.
- `anchor_hle_minimum_wage`: The HLE method remains unresolved and does not model actual human labour equivalents.
- `anchor_opfte_minimum_wage`: OPFTE remains a placeholder benchmark; occupation mix, sector labour requirements, and schedule authority methods remain unresolved.
- `anchor_payg_public_tax_stats`: Public tax totals do not identify AI-related PAYG erosion, taxpayer behaviour, or CARSF revenue.
- `anchor_payroll_tax_source_reference`: State payroll tax pressure remains placeholder-only and does not provide state tax advice or employer incidence.
- `anchor_qlc_minimum_wage`: QLC weighting remains a realistic placeholder and does not establish task allocation, sector labour mix, or tax treatment.
- `anchor_sector_schedule_source_reference`: ABS labour source remains not loaded and sector schedules are not official rankings, calibrated schedules, or legal attribution rules.
- `anchor_super_guarantee_rate`: The field does not estimate individual superannuation, payroll, employer behaviour, or ATO guidance.
- `anchor_transition_public_reference`: Transition eligibility, payment design, welfare effects, and fiscal sufficiency remain unresolved.
- `anchor_uncertainty_source_reference_only`: Uncertainty ranges remain deterministic placeholders and are not confidence intervals or statistical estimates.

## P. Calibration Blockers Still Remaining

- `anchor_fiscal_public_aggregates` still needs: CARSF behavioural response method, revenue capture method, fiscal incidence method
- `anchor_help_source_reference` still needs: income distribution, individual repayment records, eligibility law review
- `anchor_hle_minimum_wage` still needs: human labour equivalent method, occupation mix, worker-hour evidence
- `anchor_opfte_minimum_wage` still needs: occupation-specific hours, sector-specific labour requirements, schedule authority method
- `anchor_payg_public_tax_stats` still needs: employment-tax pathway method, sector attribution, behavioural response method
- `anchor_payroll_tax_source_reference` still needs: jurisdiction-specific payroll base, employer records, tax-law review
- `anchor_qlc_minimum_wage` still needs: qualified labour contribution method, task allocation evidence, sector labour mix
- `anchor_sector_schedule_source_reference` still needs: ABS public aggregate table extraction, sector schedule authority method, mixed-unit attribution
- `anchor_super_guarantee_rate` still needs: wage base, employer contribution records, payment interaction method
- `anchor_transition_public_reference` still needs: transition eligibility method, payment administrative data, fiscal design review
- `anchor_uncertainty_source_reference_only` still needs: statistical sampling frame, confidence method, authorised microdata

## Q. Build 33 Readiness

- Define public aggregate calibration boundaries separately from placeholder replacement mapping.
- Keep public aggregate values limited to anchors, bounds, context, or sanity checks unless external review and restricted-data governance exist.
- Preserve no-calibration, no-validation, no-tax-payable, no-official-status, no-legal-sufficiency, no-readiness-score, and no-liability-change boundaries.

## R. Limitations and Future Work

- Build 32 does not load new data.
- Public aggregate anchors can make placeholder treatment clearer but cannot create calibration or validation.
- Restricted-data and external-review blockers remain visible.
- Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-32 are included in a later sealed RC.

## Summary Counts

- placeholder_replacement_map_created: True
- new_data_loaded: False
- loaded_public_values_used: 10
- placeholders_mapped: 11
- placeholders_replaced_by_public_anchor: 2
- placeholders_narrowed_by_public_anchor: 3
- placeholders_informed_by_public_anchor: 3
- placeholders_still_placeholder_only: 0
- placeholders_blocked_until_restricted_data: 1
- placeholders_blocked_until_external_review: 1
- placeholders_cannot_replace_with_public_aggregate_data: 1
- public_source_candidates_treated_as_loaded: False
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
- forbidden_claim_findings: 0
