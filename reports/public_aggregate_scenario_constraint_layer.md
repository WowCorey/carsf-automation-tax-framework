# CARSF V1.5 Public Aggregate Scenario Constraint Layer

Generated at: `2026-05-22T01:44:38+00:00`

## A. Purpose

This report constrains scenario outputs using the Build 33 public aggregate calibration-boundary map.

## B. Non-Claims

- This is a public aggregate scenario constraint layer only. No new data is loaded by this build. Scenario constraints do not calibrate the model and do not validate the model. Public aggregate data can only appear as sanity checks, anchors, bounds, context, placeholder narrowing, or reviewer traceability. Public aggregate data does not prove the model works. Outputs marked non-interpretable are not usable as evidence. Hidden outputs are hidden to prevent overclaiming. Source candidates not loaded remain not loaded. Restricted-data blockers remain blockers. This is not validation, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, and not official status. It does not determine actual tax payable and does not modify firm-level CARSF liability.
- Build 34 uses existing Build 31 public aggregate values, Build 32 placeholder decisions, and Build 33 boundary decisions only.
- Scenario output labels are display constraints only; they are not calibration, validation, legal sufficiency, official status, readiness, or liability determinations.
- Outputs marked non-interpretable or hidden remain unavailable as reviewer-facing evidence until required data and reviews exist.

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

## D. Scenario Output Status Taxonomy

- `display_as_context_only`
- `display_as_placeholder_narrowing_only`
- `display_as_public_aggregate_anchor_only`
- `display_as_public_aggregate_bound_only`
- `display_as_reviewer_traceability_only`
- `display_as_sanity_check_only`
- `fail_closed_forbidden_claim`
- `hide_from_reviewer_dashboard`
- `mark_non_interpretable`

## E. Display Rule Taxonomy

- `fail_closed`
- `hide`
- `show_as_boundary_only`
- `show_as_context_only`
- `show_as_traceability_only`
- `show_blocked`
- `show_placeholder_only`
- `show_with_non_claim_warning`

## F. Forbidden Implication Taxonomy

- `actual_tax_payable`
- `ato_guidance`
- `calibration_completed`
- `causal_inference`
- `compliance_scoring`
- `firm_liability_determination`
- `household_population_estimate`
- `implementation_readiness`
- `legal_sufficiency`
- `maturity_scoring`
- `model_validation`
- `official_policy_status`
- `pbo_costing`
- `readiness_scoring`
- `statistical_validation`
- `taxpayer_behaviour_estimate`
- `treasury_modelling`

## G. Constraint Status Taxonomy

- `compliant_boundary_output`
- `fail_closed`
- `hidden_for_reviewer_safety`
- `non_interpretable`
- `warning_boundary_limited`

## H. Claim Level Taxonomy

- `no_scenario_claim_allowed`
- `scenario_context_only`
- `scenario_non_interpretable`
- `scenario_placeholder_narrowing_only`
- `scenario_public_anchor_only`
- `scenario_public_bound_only`
- `scenario_sanity_check_only`
- `scenario_traceability_only`

## I. Module Scenario Constraints

| Module | Output Status | Display Rule | Constraint Status | Claim Level | Allowed Display | Hidden Or Non-Interpretable | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Administrative compliance workflow | display_as_reviewer_traceability_only | show_as_traceability_only | warning_boundary_limited | scenario_traceability_only | traceability and pathway concept only | Administrative compliance workflow must hide or mark non-interpretable any output implying ATO workflow, compliance scoring, enforcement, notices, operational readiness. | ATO methods review, legal review, secure operational design |
| Behavioural response / gaming simulation | mark_non_interpretable | show_blocked | non_interpretable | scenario_non_interpretable | context only, blocked warning | Behavioural response / gaming simulation must hide or mark non-interpretable any output implying behavioural elasticity, avoidance estimate, gaming prediction, causal response. | behavioural elasticity evidence, authorised administrative data, economic review |
| Executive dashboard consolidation | display_as_reviewer_traceability_only | show_as_traceability_only | warning_boundary_limited | scenario_traceability_only | boundary labels, non-claim warnings, source traceability | Executive dashboard consolidation must hide or mark non-interpretable any output implying readiness scoring, calibration scoring, validation scoring, tax payable estimate, liability estimate. | reviewer feedback, dashboard interpretation testing, guardrail review |
| Fiscal trajectory assumptions | display_as_public_aggregate_bound_only | show_as_boundary_only | warning_boundary_limited | scenario_public_bound_only | fiscal context, public aggregate fiscal bounds | Fiscal trajectory assumptions must hide or mark non-interpretable any output implying Treasury modelling, PBO costing, fiscal sufficiency, CARSF revenue estimate. | revenue incidence method, behavioural response method, economic review |
| HLE assumptions module | display_as_public_aggregate_bound_only | show_as_boundary_only | warning_boundary_limited | scenario_public_bound_only | wage boundary display, placeholder narrowing display | HLE assumptions module must hide or mark non-interpretable any output implying representative labour-cost estimate, occupation-specific wage model, automation substitution calibration. | human labour equivalent method, occupation mix evidence, behavioural elasticity review |
| Household distributional scenarios | hide_from_reviewer_dashboard | hide | hidden_for_reviewer_safety | no_scenario_claim_allowed | synthetic placeholder context only | Household distributional scenarios must hide or mark non-interpretable any output implying real household estimate, population estimate, welfare impact estimate, distributional calibration. | authorised household microdata, welfare payment evidence, statistical review |
| Household weighting | mark_non_interpretable | show_blocked | non_interpretable | scenario_non_interpretable | synthetic placeholder context only | Household weighting must hide or mark non-interpretable any output implying representative weighting, population estimate, household distributional estimate. | authorised household sample frame, weighting method, statistical review |
| Legislative architecture skeleton | display_as_reviewer_traceability_only | show_as_traceability_only | warning_boundary_limited | scenario_traceability_only | non-operative architecture traceability | Legislative architecture skeleton must hide or mark non-interpretable any output implying operative law, legal sufficiency, drafting readiness, official policy. | legal drafting review, tax review, Parliamentary Counsel review |
| OPFTE benchmark module | display_as_public_aggregate_anchor_only | show_as_boundary_only | warning_boundary_limited | scenario_public_anchor_only | Fair Work public wage anchors, visible sanity checks, public aggregate wage bounds | OPFTE benchmark module must hide or mark non-interpretable any output implying OPFTE calibration, representative labour-cost estimate, firm liability determination, actual tax payable. | occupation-specific labour evidence, sector schedule authority method, statistical review |
| PAYG erosion assumptions | mark_non_interpretable | show_blocked | non_interpretable | scenario_non_interpretable | tax aggregate context only | PAYG erosion assumptions must hide or mark non-interpretable any output implying PAYG erosion calibration, taxpayer behaviour estimate, CARSF revenue estimate. | taxpayer behaviour evidence, employment tax pathway method, authorised tax data governance |
| Public data evidence map | display_as_reviewer_traceability_only | show_as_traceability_only | compliant_boundary_output | scenario_traceability_only | evidence map traceability, source-reference labels | Public data evidence map must hide or mark non-interpretable any output implying validation evidence, calibration evidence, policy readiness evidence. | manual reviewer inspection, statistical review where relevant |
| Public data placeholder replacement map | display_as_placeholder_narrowing_only | show_placeholder_only | warning_boundary_limited | scenario_placeholder_narrowing_only | placeholder replacement labels, placeholder narrowing labels, context labels | Public data placeholder replacement map must hide or mark non-interpretable any output implying calibration replacement, validation replacement, liability replacement. | reviewer inspection, restricted-data governance, statistical review |
| QLC weights module | display_as_placeholder_narrowing_only | show_placeholder_only | warning_boundary_limited | scenario_placeholder_narrowing_only | placeholder narrowing display, wage-threshold context | QLC weights module must hide or mark non-interpretable any output implying QLC calibration, labour-quality validation, legal attribution. | QLC weighting method, sector labour evidence, tax-method review |
| Reviewed scenario comparison layer | display_as_reviewer_traceability_only | show_as_traceability_only | warning_boundary_limited | scenario_traceability_only | reviewer-facing comparison labels, non-claim warnings | Reviewed scenario comparison layer must hide or mark non-interpretable any output implying policy ranking, validation ranking, implementation recommendation. | scenario review protocol, statistical review, economic review |
| Sector schedule values | display_as_context_only | show_as_context_only | warning_boundary_limited | scenario_context_only | sector schedule context, reviewer traceability | Sector schedule values must hide or mark non-interpretable any output implying official sector ranking, schedule calibration, legal attribution. | sector-specific public aggregates, schedule authority method, legal review |
| Sector stress matrix | display_as_sanity_check_only | show_with_non_claim_warning | warning_boundary_limited | scenario_sanity_check_only | stress assumption sanity checks, public aggregate context | Sector stress matrix must hide or mark non-interpretable any output implying validated sector stress, official sector ranking, population estimate. | sector exposure evidence, economic incidence review, statistical review |
| Superannuation contribution pressure | display_as_public_aggregate_anchor_only | show_as_boundary_only | warning_boundary_limited | scenario_public_anchor_only | public contribution-rate anchor, payment interaction context | Superannuation contribution pressure must hide or mark non-interpretable any output implying individual super estimate, employer behaviour estimate, payroll estimate, ATO guidance claim. | wage base evidence, employer contribution behaviour evidence, tax review |
| Transition funding assumptions | display_as_context_only | show_as_context_only | warning_boundary_limited | scenario_context_only | transition funding scale context, public aggregate fiscal bounds | Transition funding assumptions must hide or mark non-interpretable any output implying fiscal sufficiency, welfare impact estimate, policy implementation readiness. | transition design review, welfare payment evidence, economic review |
| Uncertainty ranges | display_as_context_only | show_as_context_only | warning_boundary_limited | scenario_context_only | uncertainty label context, blocked evidence traceability | Uncertainty ranges must hide or mark non-interpretable any output implying real uncertainty quantification, confidence interval, statistical estimation. | uncertainty method, sample design, statistical review |
| Public aggregate calibration boundary map | display_as_reviewer_traceability_only | show_as_traceability_only | compliant_boundary_output | scenario_traceability_only | boundary labels, allowed-use labels, forbidden-use labels, reviewer traceability | The boundary map must hide or mark non-interpretable any output implying calibration satisfaction, validation, legal sufficiency, official status, implementation readiness, tax payable, or firm liability. | restricted data governance, legal review, economic review, statistical review, external domain review |

## J. Field Scenario Constraints

| Field | Placeholder | Output Status | Display Rule | Constraint Status | Claim Level | Linked Values | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| fiscal_trajectory_assumptions | anchor_fiscal_public_aggregates | display_as_public_aggregate_bound_only | show_as_boundary_only | warning_boundary_limited | scenario_public_bound_only | ato_large_corporate_income_tax_received_2022_23, ato_large_corporate_entities_no_income_tax_percent_2022_23, ato_total_tax_revenue_collected_2022_23, ato_company_tax_revenue_2022_23, treasury_total_receipts_2025_26_estimate, treasury_taxation_receipts_2025_26_estimate | CARSF behavioural response method, revenue capture method, fiscal incidence method |
| help_hecs_repayment_pressure | anchor_help_source_reference | mark_non_interpretable | show_blocked | non_interpretable | scenario_non_interpretable | None | income distribution, individual repayment records, eligibility law review |
| hle_assumptions | anchor_hle_minimum_wage | display_as_public_aggregate_bound_only | show_as_boundary_only | warning_boundary_limited | scenario_public_bound_only | fair_work_national_minimum_wage_hourly_2025, fair_work_national_minimum_wage_weekly_2025, fair_work_casual_loading_2025 | human labour equivalent method, occupation mix, worker-hour evidence |
| opfte_benchmarks | anchor_opfte_minimum_wage | display_as_public_aggregate_anchor_only | show_as_boundary_only | warning_boundary_limited | scenario_public_anchor_only | fair_work_national_minimum_wage_hourly_2025, fair_work_national_minimum_wage_weekly_2025 | occupation-specific hours, sector-specific labour requirements, schedule authority method |
| payg_erosion_assumptions | anchor_payg_public_tax_stats | display_as_context_only | show_as_context_only | warning_boundary_limited | scenario_context_only | ato_total_tax_revenue_collected_2022_23, ato_company_tax_revenue_2022_23 | employment-tax pathway method, sector attribution, behavioural response method |
| state_payroll_tax_pressure | anchor_payroll_tax_source_reference | display_as_reviewer_traceability_only | show_as_traceability_only | warning_boundary_limited | scenario_traceability_only | None | jurisdiction-specific payroll base, employer records, tax-law review |
| qlc_weights | anchor_qlc_minimum_wage | display_as_public_aggregate_bound_only | show_as_boundary_only | warning_boundary_limited | scenario_public_bound_only | fair_work_national_minimum_wage_hourly_2025, fair_work_national_minimum_wage_weekly_2025 | qualified labour contribution method, task allocation evidence, sector labour mix |
| sector_schedule_values | anchor_sector_schedule_source_reference | display_as_context_only | show_as_context_only | warning_boundary_limited | scenario_context_only | fair_work_national_minimum_wage_hourly_2025, fair_work_casual_loading_2025 | ABS public aggregate table extraction, sector schedule authority method, mixed-unit attribution |
| superannuation_contribution_pressure | anchor_super_guarantee_rate | display_as_public_aggregate_anchor_only | show_as_boundary_only | warning_boundary_limited | scenario_public_anchor_only | ato_super_guarantee_rate_2025_26 | wage base, employer contribution records, payment interaction method |
| transition_payment_assumptions | anchor_transition_public_reference | display_as_context_only | show_as_context_only | warning_boundary_limited | scenario_context_only | treasury_total_receipts_2025_26_estimate, treasury_taxation_receipts_2025_26_estimate, ato_super_guarantee_rate_2025_26 | transition eligibility method, payment administrative data, fiscal design review |
| uncertainty_range_assumptions | anchor_uncertainty_source_reference_only | display_as_context_only | show_as_context_only | warning_boundary_limited | scenario_context_only | ato_total_tax_revenue_collected_2022_23, ato_company_tax_revenue_2022_23 | statistical sampling frame, confidence method, authorised microdata |

## K. Outputs Displayed As Sanity Check Only

| Module | Output Status | Display Rule | Constraint Status | Claim Level | Allowed Display | Hidden Or Non-Interpretable | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sector stress matrix | display_as_sanity_check_only | show_with_non_claim_warning | warning_boundary_limited | scenario_sanity_check_only | stress assumption sanity checks, public aggregate context | Sector stress matrix must hide or mark non-interpretable any output implying validated sector stress, official sector ranking, population estimate. | sector exposure evidence, economic incidence review, statistical review |

## L. Outputs Displayed As Public Aggregate Anchor Only

| Module | Output Status | Display Rule | Constraint Status | Claim Level | Allowed Display | Hidden Or Non-Interpretable | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPFTE benchmark module | display_as_public_aggregate_anchor_only | show_as_boundary_only | warning_boundary_limited | scenario_public_anchor_only | Fair Work public wage anchors, visible sanity checks, public aggregate wage bounds | OPFTE benchmark module must hide or mark non-interpretable any output implying OPFTE calibration, representative labour-cost estimate, firm liability determination, actual tax payable. | occupation-specific labour evidence, sector schedule authority method, statistical review |
| Superannuation contribution pressure | display_as_public_aggregate_anchor_only | show_as_boundary_only | warning_boundary_limited | scenario_public_anchor_only | public contribution-rate anchor, payment interaction context | Superannuation contribution pressure must hide or mark non-interpretable any output implying individual super estimate, employer behaviour estimate, payroll estimate, ATO guidance claim. | wage base evidence, employer contribution behaviour evidence, tax review |

## M. Outputs Displayed As Public Aggregate Bound Only

| Module | Output Status | Display Rule | Constraint Status | Claim Level | Allowed Display | Hidden Or Non-Interpretable | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Fiscal trajectory assumptions | display_as_public_aggregate_bound_only | show_as_boundary_only | warning_boundary_limited | scenario_public_bound_only | fiscal context, public aggregate fiscal bounds | Fiscal trajectory assumptions must hide or mark non-interpretable any output implying Treasury modelling, PBO costing, fiscal sufficiency, CARSF revenue estimate. | revenue incidence method, behavioural response method, economic review |
| HLE assumptions module | display_as_public_aggregate_bound_only | show_as_boundary_only | warning_boundary_limited | scenario_public_bound_only | wage boundary display, placeholder narrowing display | HLE assumptions module must hide or mark non-interpretable any output implying representative labour-cost estimate, occupation-specific wage model, automation substitution calibration. | human labour equivalent method, occupation mix evidence, behavioural elasticity review |

## N. Outputs Displayed As Context Only

| Module | Output Status | Display Rule | Constraint Status | Claim Level | Allowed Display | Hidden Or Non-Interpretable | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Sector schedule values | display_as_context_only | show_as_context_only | warning_boundary_limited | scenario_context_only | sector schedule context, reviewer traceability | Sector schedule values must hide or mark non-interpretable any output implying official sector ranking, schedule calibration, legal attribution. | sector-specific public aggregates, schedule authority method, legal review |
| Transition funding assumptions | display_as_context_only | show_as_context_only | warning_boundary_limited | scenario_context_only | transition funding scale context, public aggregate fiscal bounds | Transition funding assumptions must hide or mark non-interpretable any output implying fiscal sufficiency, welfare impact estimate, policy implementation readiness. | transition design review, welfare payment evidence, economic review |
| Uncertainty ranges | display_as_context_only | show_as_context_only | warning_boundary_limited | scenario_context_only | uncertainty label context, blocked evidence traceability | Uncertainty ranges must hide or mark non-interpretable any output implying real uncertainty quantification, confidence interval, statistical estimation. | uncertainty method, sample design, statistical review |

## O. Outputs Displayed As Placeholder Narrowing Only

| Module | Output Status | Display Rule | Constraint Status | Claim Level | Allowed Display | Hidden Or Non-Interpretable | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Public data placeholder replacement map | display_as_placeholder_narrowing_only | show_placeholder_only | warning_boundary_limited | scenario_placeholder_narrowing_only | placeholder replacement labels, placeholder narrowing labels, context labels | Public data placeholder replacement map must hide or mark non-interpretable any output implying calibration replacement, validation replacement, liability replacement. | reviewer inspection, restricted-data governance, statistical review |
| QLC weights module | display_as_placeholder_narrowing_only | show_placeholder_only | warning_boundary_limited | scenario_placeholder_narrowing_only | placeholder narrowing display, wage-threshold context | QLC weights module must hide or mark non-interpretable any output implying QLC calibration, labour-quality validation, legal attribution. | QLC weighting method, sector labour evidence, tax-method review |

## P. Outputs Displayed As Reviewer Traceability Only

| Module | Output Status | Display Rule | Constraint Status | Claim Level | Allowed Display | Hidden Or Non-Interpretable | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Administrative compliance workflow | display_as_reviewer_traceability_only | show_as_traceability_only | warning_boundary_limited | scenario_traceability_only | traceability and pathway concept only | Administrative compliance workflow must hide or mark non-interpretable any output implying ATO workflow, compliance scoring, enforcement, notices, operational readiness. | ATO methods review, legal review, secure operational design |
| Executive dashboard consolidation | display_as_reviewer_traceability_only | show_as_traceability_only | warning_boundary_limited | scenario_traceability_only | boundary labels, non-claim warnings, source traceability | Executive dashboard consolidation must hide or mark non-interpretable any output implying readiness scoring, calibration scoring, validation scoring, tax payable estimate, liability estimate. | reviewer feedback, dashboard interpretation testing, guardrail review |
| Legislative architecture skeleton | display_as_reviewer_traceability_only | show_as_traceability_only | warning_boundary_limited | scenario_traceability_only | non-operative architecture traceability | Legislative architecture skeleton must hide or mark non-interpretable any output implying operative law, legal sufficiency, drafting readiness, official policy. | legal drafting review, tax review, Parliamentary Counsel review |
| Public data evidence map | display_as_reviewer_traceability_only | show_as_traceability_only | compliant_boundary_output | scenario_traceability_only | evidence map traceability, source-reference labels | Public data evidence map must hide or mark non-interpretable any output implying validation evidence, calibration evidence, policy readiness evidence. | manual reviewer inspection, statistical review where relevant |
| Reviewed scenario comparison layer | display_as_reviewer_traceability_only | show_as_traceability_only | warning_boundary_limited | scenario_traceability_only | reviewer-facing comparison labels, non-claim warnings | Reviewed scenario comparison layer must hide or mark non-interpretable any output implying policy ranking, validation ranking, implementation recommendation. | scenario review protocol, statistical review, economic review |
| Public aggregate calibration boundary map | display_as_reviewer_traceability_only | show_as_traceability_only | compliant_boundary_output | scenario_traceability_only | boundary labels, allowed-use labels, forbidden-use labels, reviewer traceability | The boundary map must hide or mark non-interpretable any output implying calibration satisfaction, validation, legal sufficiency, official status, implementation readiness, tax payable, or firm liability. | restricted data governance, legal review, economic review, statistical review, external domain review |

## Q. Outputs Marked Non-Interpretable

| Module | Output Status | Display Rule | Constraint Status | Claim Level | Allowed Display | Hidden Or Non-Interpretable | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Behavioural response / gaming simulation | mark_non_interpretable | show_blocked | non_interpretable | scenario_non_interpretable | context only, blocked warning | Behavioural response / gaming simulation must hide or mark non-interpretable any output implying behavioural elasticity, avoidance estimate, gaming prediction, causal response. | behavioural elasticity evidence, authorised administrative data, economic review |
| Household weighting | mark_non_interpretable | show_blocked | non_interpretable | scenario_non_interpretable | synthetic placeholder context only | Household weighting must hide or mark non-interpretable any output implying representative weighting, population estimate, household distributional estimate. | authorised household sample frame, weighting method, statistical review |
| PAYG erosion assumptions | mark_non_interpretable | show_blocked | non_interpretable | scenario_non_interpretable | tax aggregate context only | PAYG erosion assumptions must hide or mark non-interpretable any output implying PAYG erosion calibration, taxpayer behaviour estimate, CARSF revenue estimate. | taxpayer behaviour evidence, employment tax pathway method, authorised tax data governance |

## R. Outputs Hidden From Reviewer Dashboard

| Module | Output Status | Display Rule | Constraint Status | Claim Level | Allowed Display | Hidden Or Non-Interpretable | Evidence Needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Household distributional scenarios | hide_from_reviewer_dashboard | hide | hidden_for_reviewer_safety | no_scenario_claim_allowed | synthetic placeholder context only | Household distributional scenarios must hide or mark non-interpretable any output implying real household estimate, population estimate, welfare impact estimate, distributional calibration. | authorised household microdata, welfare payment evidence, statistical review |

## S. Forbidden Implications Mapped

| Implication | Constraint Action | Reviewer Warning |
| --- | --- | --- |
| actual_tax_payable | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply actual_tax_payable; if it does, the layer must fail closed or hide the output. |
| ato_guidance | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply ato_guidance; if it does, the layer must fail closed or hide the output. |
| calibration_completed | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply calibration_completed; if it does, the layer must fail closed or hide the output. |
| causal_inference | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply causal_inference; if it does, the layer must fail closed or hide the output. |
| compliance_scoring | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply compliance_scoring; if it does, the layer must fail closed or hide the output. |
| firm_liability_determination | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply firm_liability_determination; if it does, the layer must fail closed or hide the output. |
| household_population_estimate | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply household_population_estimate; if it does, the layer must fail closed or hide the output. |
| implementation_readiness | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply implementation_readiness; if it does, the layer must fail closed or hide the output. |
| legal_sufficiency | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply legal_sufficiency; if it does, the layer must fail closed or hide the output. |
| maturity_scoring | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply maturity_scoring; if it does, the layer must fail closed or hide the output. |
| model_validation | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply model_validation; if it does, the layer must fail closed or hide the output. |
| official_policy_status | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply official_policy_status; if it does, the layer must fail closed or hide the output. |
| pbo_costing | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply pbo_costing; if it does, the layer must fail closed or hide the output. |
| readiness_scoring | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply readiness_scoring; if it does, the layer must fail closed or hide the output. |
| statistical_validation | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply statistical_validation; if it does, the layer must fail closed or hide the output. |
| taxpayer_behaviour_estimate | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply taxpayer_behaviour_estimate; if it does, the layer must fail closed or hide the output. |
| treasury_modelling | flag_hide_downgrade_or_mark_non_interpretable | Scenario output must not imply treasury_modelling; if it does, the layer must fail closed or hide the output. |

## T. What Can Be Displayed

- `administrative_compliance_workflow`: Administrative compliance workflow may display traceability and pathway concept only only with non-claim warnings.
- `behavioural_response_gaming_simulation`: Behavioural response / gaming simulation may display context only, blocked warning only with non-claim warnings.
- `executive_dashboard_consolidation`: Executive dashboard consolidation may display boundary labels, non-claim warnings, source traceability only with non-claim warnings.
- `fiscal_trajectory_assumptions`: Fiscal trajectory assumptions may display fiscal context, public aggregate fiscal bounds only with non-claim warnings.
- `hle_assumptions_module`: HLE assumptions module may display wage boundary display, placeholder narrowing display only with non-claim warnings.
- `household_distributional_scenarios`: Household distributional scenarios may display synthetic placeholder context only only with non-claim warnings.
- `household_weighting`: Household weighting may display synthetic placeholder context only only with non-claim warnings.
- `legislative_architecture_skeleton`: Legislative architecture skeleton may display non-operative architecture traceability only with non-claim warnings.
- `opfte_benchmark_module`: OPFTE benchmark module may display Fair Work public wage anchors, visible sanity checks, public aggregate wage bounds only with non-claim warnings.
- `payg_erosion_assumptions`: PAYG erosion assumptions may display tax aggregate context only only with non-claim warnings.
- `public_data_evidence_map`: Public data evidence map may display evidence map traceability, source-reference labels only with non-claim warnings.
- `public_data_placeholder_replacement_map`: Public data placeholder replacement map may display placeholder replacement labels, placeholder narrowing labels, context labels only with non-claim warnings.
- `qlc_weights_module`: QLC weights module may display placeholder narrowing display, wage-threshold context only with non-claim warnings.
- `reviewed_scenario_comparison_layer`: Reviewed scenario comparison layer may display reviewer-facing comparison labels, non-claim warnings only with non-claim warnings.
- `sector_schedule_values`: Sector schedule values may display sector schedule context, reviewer traceability only with non-claim warnings.
- `sector_stress_matrix`: Sector stress matrix may display stress assumption sanity checks, public aggregate context only with non-claim warnings.
- `superannuation_contribution_pressure`: Superannuation contribution pressure may display public contribution-rate anchor, payment interaction context only with non-claim warnings.
- `transition_funding_assumptions`: Transition funding assumptions may display transition funding scale context, public aggregate fiscal bounds only with non-claim warnings.
- `uncertainty_ranges`: Uncertainty ranges may display uncertainty label context, blocked evidence traceability only with non-claim warnings.
- `public_aggregate_calibration_boundary_map`: The boundary map may display allowed-use labels, forbidden-use labels, blockers, and reviewer traceability.

## U. What Must Be Hidden Or Marked Non-Interpretable

- `administrative_compliance_workflow`: Administrative compliance workflow must hide or mark non-interpretable any output implying ATO workflow, compliance scoring, enforcement, notices, operational readiness.
- `behavioural_response_gaming_simulation`: Behavioural response / gaming simulation must hide or mark non-interpretable any output implying behavioural elasticity, avoidance estimate, gaming prediction, causal response.
- `executive_dashboard_consolidation`: Executive dashboard consolidation must hide or mark non-interpretable any output implying readiness scoring, calibration scoring, validation scoring, tax payable estimate, liability estimate.
- `fiscal_trajectory_assumptions`: Fiscal trajectory assumptions must hide or mark non-interpretable any output implying Treasury modelling, PBO costing, fiscal sufficiency, CARSF revenue estimate.
- `hle_assumptions_module`: HLE assumptions module must hide or mark non-interpretable any output implying representative labour-cost estimate, occupation-specific wage model, automation substitution calibration.
- `household_distributional_scenarios`: Household distributional scenarios must hide or mark non-interpretable any output implying real household estimate, population estimate, welfare impact estimate, distributional calibration.
- `household_weighting`: Household weighting must hide or mark non-interpretable any output implying representative weighting, population estimate, household distributional estimate.
- `legislative_architecture_skeleton`: Legislative architecture skeleton must hide or mark non-interpretable any output implying operative law, legal sufficiency, drafting readiness, official policy.
- `opfte_benchmark_module`: OPFTE benchmark module must hide or mark non-interpretable any output implying OPFTE calibration, representative labour-cost estimate, firm liability determination, actual tax payable.
- `payg_erosion_assumptions`: PAYG erosion assumptions must hide or mark non-interpretable any output implying PAYG erosion calibration, taxpayer behaviour estimate, CARSF revenue estimate.
- `public_data_evidence_map`: Public data evidence map must hide or mark non-interpretable any output implying validation evidence, calibration evidence, policy readiness evidence.
- `public_data_placeholder_replacement_map`: Public data placeholder replacement map must hide or mark non-interpretable any output implying calibration replacement, validation replacement, liability replacement.
- `qlc_weights_module`: QLC weights module must hide or mark non-interpretable any output implying QLC calibration, labour-quality validation, legal attribution.
- `reviewed_scenario_comparison_layer`: Reviewed scenario comparison layer must hide or mark non-interpretable any output implying policy ranking, validation ranking, implementation recommendation.
- `sector_schedule_values`: Sector schedule values must hide or mark non-interpretable any output implying official sector ranking, schedule calibration, legal attribution.
- `sector_stress_matrix`: Sector stress matrix must hide or mark non-interpretable any output implying validated sector stress, official sector ranking, population estimate.
- `superannuation_contribution_pressure`: Superannuation contribution pressure must hide or mark non-interpretable any output implying individual super estimate, employer behaviour estimate, payroll estimate, ATO guidance claim.
- `transition_funding_assumptions`: Transition funding assumptions must hide or mark non-interpretable any output implying fiscal sufficiency, welfare impact estimate, policy implementation readiness.
- `uncertainty_ranges`: Uncertainty ranges must hide or mark non-interpretable any output implying real uncertainty quantification, confidence interval, statistical estimation.
- `public_aggregate_calibration_boundary_map`: The boundary map must hide or mark non-interpretable any output implying calibration satisfaction, validation, legal sufficiency, official status, implementation readiness, tax payable, or firm liability.

## V. Evidence Needed To Lift Constraints

- `administrative_compliance_workflow`: ATO methods review, legal review, secure operational design
- `behavioural_response_gaming_simulation`: behavioural elasticity evidence, authorised administrative data, economic review
- `executive_dashboard_consolidation`: reviewer feedback, dashboard interpretation testing, guardrail review
- `fiscal_trajectory_assumptions`: revenue incidence method, behavioural response method, economic review
- `hle_assumptions_module`: human labour equivalent method, occupation mix evidence, behavioural elasticity review
- `household_distributional_scenarios`: authorised household microdata, welfare payment evidence, statistical review
- `household_weighting`: authorised household sample frame, weighting method, statistical review
- `legislative_architecture_skeleton`: legal drafting review, tax review, Parliamentary Counsel review
- `opfte_benchmark_module`: occupation-specific labour evidence, sector schedule authority method, statistical review
- `payg_erosion_assumptions`: taxpayer behaviour evidence, employment tax pathway method, authorised tax data governance
- `public_data_evidence_map`: manual reviewer inspection, statistical review where relevant
- `public_data_placeholder_replacement_map`: reviewer inspection, restricted-data governance, statistical review
- `qlc_weights_module`: QLC weighting method, sector labour evidence, tax-method review
- `reviewed_scenario_comparison_layer`: scenario review protocol, statistical review, economic review
- `sector_schedule_values`: sector-specific public aggregates, schedule authority method, legal review
- `sector_stress_matrix`: sector exposure evidence, economic incidence review, statistical review
- `superannuation_contribution_pressure`: wage base evidence, employer contribution behaviour evidence, tax review
- `transition_funding_assumptions`: transition design review, welfare payment evidence, economic review
- `uncertainty_ranges`: uncertainty method, sample design, statistical review
- `public_aggregate_calibration_boundary_map`: restricted data governance, legal review, economic review, statistical review, external domain review

## W. Build 35 Readiness

- Package public aggregate values, placeholder replacement, calibration boundaries, and scenario constraints into a reviewer-facing handoff bundle.
- Keep hidden and non-interpretable outputs clearly separated from reviewer-facing evidence.
- Preserve no-calibration, no-validation, no-tax-payable, no-official-status, no-legal-sufficiency, no-readiness-score, and no-liability-change boundaries.

## X. Limitations and Future Work

- Build 34 does not load new data.
- Scenario constraints do not create calibration or validation.
- Hidden and non-interpretable outputs remain unavailable as reviewer-facing evidence.
- Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-34 are included in a later sealed RC.

## Summary Counts

- public_aggregate_scenario_constraint_layer_created: True
- new_data_loaded: False
- loaded_public_values_used: 10
- module_constraints_mapped: 20
- field_constraints_mapped: 11
- outputs_display_as_sanity_check_only: 1
- outputs_display_as_public_anchor_only: 2
- outputs_display_as_public_bound_only: 2
- outputs_display_as_context_only: 3
- outputs_display_as_placeholder_narrowing_only: 2
- outputs_display_as_reviewer_traceability_only: 6
- outputs_marked_non_interpretable: 3
- outputs_hidden_from_reviewer_dashboard: 1
- outputs_fail_closed_forbidden_claim: 0
- forbidden_implications_mapped: 17
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
