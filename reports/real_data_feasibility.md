# CARSF V1.5 Real Data Feasibility & Calibration Intake Map

## A. Purpose

This report maps potential data-source feasibility, calibration-intake needs, placeholder provenance, restricted-data blockers, forbidden repo data, and public-data pilot readiness for CARSF V1.5.

## B. Non-Claims

- This is a feasibility and calibration-intake map only. No real data has been loaded by this build, no calibration has occurred, realistic placeholders are not real data and are not calibrated, public-data candidates are not loaded datasets, and restricted-data requirements are not data access. It is not legal advice, tax advice, ATO guidance, Treasury modelling, economic validation, welfare validation, statistical validation, operational readiness, legal sufficiency, official status, and does not determine actual tax payable. It does not use taxpayer-level, firm-level confidential, household microdata, ABS DataLab, HILDA microdata, DSS/Services Australia records, ATO records, Treasury/PBO confidential material, or restricted government data, and does not modify firm-level CARSF liability.
- The map only separates public-data candidates, restricted-data requirements, realistic placeholders, synthetic fixtures, forbidden repo data, and public-data pilot readiness.
- Build 26 performs feasibility mapping only; any future public-data pilot must keep loaded public aggregates separate from placeholders and restricted-data needs.

## C. Data Status Taxonomy

- `real_public_data_candidate`
- `real_public_data_loaded`
- `restricted_data_required`
- `realistic_placeholder`
- `synthetic_fixture`
- `forbidden_repo_data`
- `not_collected`
- `external_review_required`

## D. Access Class Taxonomy

- `public_open`
- `public_manual_download`
- `public_api_available`
- `licence_required`
- `restricted_research_access`
- `government_internal_only`
- `confidential_or_prohibited`
- `unknown`

## E. Claim Level Taxonomy

- `inventory_only`
- `feasibility_only`
- `sanity_check_only`
- `placeholder_anchor_only`
- `calibration_candidate_only`
- `external_review_only`
- `forbidden_for_model_use`

## F. Source Candidate Registry

| Source ID | Source Name | Publisher | Access Class | Data Status | Claim Level | Commit to Repo | Main Use | Must Not Be Used For |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| abs_census_aggregates | ABS Census regional and household aggregates | Australian Bureau of Statistics | public_manual_download | real_public_data_candidate | sanity_check_only | True | Household and subgroup aggregate sanity-check candidate | must not use for: population estimate, real household estimate, welfare validation, calibration completed |
| abs_datalab_microdata | ABS DataLab microdata | Australian Bureau of Statistics restricted access | restricted_research_access | restricted_data_required | external_review_only | False | External restricted methods review only | must not use for: repo data, population estimate, calibration completed |
| abs_household_expenditure_income | ABS household expenditure and income aggregate products | Australian Bureau of Statistics | public_manual_download | real_public_data_candidate | sanity_check_only | True | Household aggregate plausibility checks | must not use for: real household estimate, population estimate, welfare validation, calibration completed |
| abs_industry_wages_hours | ABS industry employment wages and hours aggregates | Australian Bureau of Statistics | public_manual_download | real_public_data_candidate | placeholder_anchor_only | True | Wage and hours anchor candidate | must not use for: calibration completed, validation, official status, actual tax payable, operational readiness |
| abs_labour_force | ABS labour force and employment aggregates | Australian Bureau of Statistics | public_open | real_public_data_candidate | sanity_check_only | True | Public aggregate labour sanity-check candidate | must not use for: calibration completed, validation, official status, actual tax payable, operational readiness |
| ato_corporate_tax_transparency | ATO corporate tax transparency public data | Australian Taxation Office | public_manual_download | real_public_data_candidate | sanity_check_only | True | Public corporate-tax aggregate sanity-check candidate | must not use for: taxpayer record, actual tax payable, compliance score, calibration completed |
| ato_taxation_statistics | ATO taxation statistics aggregate tables | Australian Taxation Office | public_manual_download | real_public_data_candidate | sanity_check_only | True | Public tax aggregate plausibility checks | must not use for: taxpayer-level inference, actual tax payable, calibration completed |
| ato_taxpayer_records | ATO taxpayer records | Australian Taxation Office restricted records | confidential_or_prohibited | forbidden_repo_data | forbidden_for_model_use | False | Forbidden in repo; external legal authorisation would be required elsewhere | must not use for: repo data, tests, calibration completed |
| dss_services_payment_data | DSS and Services Australia payment data | DSS or Services Australia restricted records | government_internal_only | restricted_data_required | external_review_only | False | Restricted welfare calibration would require authorised external system | must not use for: repo data, welfare validation, calibration completed |
| fair_work_awards | Fair Work award and wage classification data | Fair Work Ombudsman or Fair Work Commission public sources | public_open | real_public_data_candidate | placeholder_anchor_only | True | Realistic wage-band placeholder anchor candidate | must not use for: legal wage sufficiency, tax advice, calibration completed |
| help_hecs_thresholds | HELP HECS repayment public threshold data | Australian Government public sources | public_open | real_public_data_candidate | placeholder_anchor_only | True | Public repayment threshold anchor candidate | must not use for: individual repayment estimate, welfare validation, calibration completed |
| hilda_microdata | HILDA microdata | Melbourne Institute restricted/licensed access | licence_required | restricted_data_required | external_review_only | False | Restricted household calibration would require authorised external environment | must not use for: repo data, public release, calibration completed |
| industry_association_reports | Industry association public reports | Industry associations | public_manual_download | real_public_data_candidate | inventory_only | False | Sector context candidate | must not use for: official sector ranking, economic validation, calibration completed |
| jobs_skills_labour_market | Jobs and Skills Australia public labour market data | Jobs and Skills Australia | public_open | real_public_data_candidate | sanity_check_only | True | Labour market plausibility candidate | must not use for: official sector ranking, labour market forecast, calibration completed |
| pbo_public_costings | PBO public costing and budget analysis material | Parliamentary Budget Office | public_open | real_public_data_candidate | inventory_only | True | Public fiscal-method context candidate | must not use for: PBO validation, official costing, calibration completed |
| public_company_reports | Public listed-company annual reports | Public companies and exchanges | public_manual_download | real_public_data_candidate | inventory_only | False | Qualitative public-document feasibility candidate | must not use for: firm-level liability, real firm data, calibration completed |
| services_australia_records | Services Australia administrative records | Services Australia restricted records | government_internal_only | forbidden_repo_data | forbidden_for_model_use | False | Forbidden in repo; external lawful authorisation required elsewhere | must not use for: repo data, tests, welfare validation |
| state_payroll_tax_thresholds | State payroll tax public thresholds and rates | State and territory revenue offices | public_manual_download | real_public_data_candidate | placeholder_anchor_only | True | Public threshold anchor candidate | must not use for: state tax advice, actual tax payable, calibration completed |
| super_guarantee_settings | Superannuation Guarantee public rate and contribution settings | ATO public guidance or legislation reference sources | public_open | real_public_data_candidate | placeholder_anchor_only | True | Public threshold placeholder anchor candidate | must not use for: ATO guidance, individual estimate, calibration completed |
| treasury_budget_papers | Budget papers and Treasury public fiscal aggregates | Treasury | public_open | real_public_data_candidate | sanity_check_only | True | Public fiscal aggregate sanity-check candidate | must not use for: Treasury modelling, official costing, calibration completed |

## G. Calibration Field Map

| Field ID | Field Name | Current Status | Required Data Status | Candidate Sources | Restricted Sources Needed | Public Sanity Check | Public Calibration Only | External Review | Must Not Claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| aava_deductibility_treatment | AAVA deductibility treatment | external_review_required | restricted_data_required | ato_corporate_tax_transparency, public_company_reports | ato_taxpayer_records | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| administrative_workflow_routing | Administrative workflow routing | synthetic_fixture | external_review_required | ato_taxation_statistics | ato_taxpayer_records | False | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| ael_arl_rate_settings | AEL and ARL rate settings | realistic_placeholder | external_review_required | treasury_budget_papers, pbo_public_costings | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| aii_component_weights | AII component weights | realistic_placeholder | external_review_required | industry_association_reports, public_company_reports | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| anti_avoidance_thresholds | Anti-avoidance thresholds | synthetic_fixture | external_review_required | public_company_reports | ato_taxpayer_records | False | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| behavioural_response_pressure_bands | Behavioural response pressure bands | synthetic_fixture | external_review_required | public_company_reports, industry_association_reports | ato_taxpayer_records | False | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| cap_credit_settings | cap and credit settings | realistic_placeholder | external_review_required | treasury_budget_papers, pbo_public_costings | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| fiscal_trajectory_assumptions | Fiscal trajectory assumptions | realistic_placeholder | real_public_data_candidate | treasury_budget_papers, pbo_public_costings, ato_taxation_statistics | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| grouped_entity_attribution | Grouped-entity attribution | synthetic_fixture | restricted_data_required | public_company_reports | ato_taxpayer_records | False | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| gst_consumption_effects | GST consumption effects | realistic_placeholder | real_public_data_candidate | abs_household_expenditure_income | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| help_hecs_repayment_pressure | HELP HECS repayment pressure | realistic_placeholder | real_public_data_candidate | help_hecs_thresholds | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| hle_assumptions | HLE assumptions | realistic_placeholder | real_public_data_candidate | abs_labour_force, fair_work_awards | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| household_distributional_scenario_assumptions | Household distributional scenario assumptions | synthetic_fixture | restricted_data_required | abs_census_aggregates, abs_household_expenditure_income | hilda_microdata, abs_datalab_microdata | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| household_weighting_assumptions | Household weighting assumptions | synthetic_fixture | restricted_data_required | abs_census_aggregates | hilda_microdata, abs_datalab_microdata | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| investment_incidence_assumptions | Investment and incidence assumptions | realistic_placeholder | external_review_required | public_company_reports, treasury_budget_papers, industry_association_reports | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| mixed_unit_weighting | Mixed-unit weighting | realistic_placeholder | real_public_data_candidate | abs_industry_wages_hours, industry_association_reports | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| nltg_labour_displacement_assumptions | NLTG labour displacement assumptions | realistic_placeholder | restricted_data_required | abs_labour_force, ato_taxation_statistics | ato_taxpayer_records | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| normal_return_preservation_thresholds | Normal return preservation thresholds | realistic_placeholder | external_review_required | treasury_budget_papers, public_company_reports | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| offshore_ai_service_attribution | Offshore AI service attribution | synthetic_fixture | restricted_data_required | public_company_reports | ato_taxpayer_records | False | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| opfte_benchmarks | OPFTE benchmarks | realistic_placeholder | real_public_data_candidate | abs_labour_force, abs_industry_wages_hours, fair_work_awards, jobs_skills_labour_market | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| pass_through_assumptions | Pass-through assumptions | realistic_placeholder | external_review_required | abs_household_expenditure_income, industry_association_reports | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| payg_erosion_assumptions | PAYG erosion assumptions | realistic_placeholder | restricted_data_required | ato_taxation_statistics, abs_labour_force | ato_taxpayer_records | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| qlc_weights | QLC weights | realistic_placeholder | external_review_required | abs_industry_wages_hours, fair_work_awards | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| reviewed_scenario_display_control_thresholds | Reviewed scenario display-control thresholds | synthetic_fixture | external_review_required | abs_census_aggregates, treasury_budget_papers | None | False | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| safe_harbour_thresholds | Safe-harbour thresholds | realistic_placeholder | external_review_required | fair_work_awards, treasury_budget_papers | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| sector_schedule_values | Sector schedule values | realistic_placeholder | real_public_data_candidate | abs_industry_wages_hours, jobs_skills_labour_market, industry_association_reports | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| sector_stress_metadata_bands | Sector stress metadata bands | realistic_placeholder | external_review_required | jobs_skills_labour_market, industry_association_reports | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| state_payroll_tax_pressure | State payroll tax pressure | realistic_placeholder | real_public_data_candidate | state_payroll_tax_thresholds | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| superannuation_contribution_pressure | Superannuation contribution pressure | realistic_placeholder | real_public_data_candidate | super_guarantee_settings, ato_taxation_statistics | None | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| transfer_pricing_review_shares | Transfer-pricing review shares | synthetic_fixture | restricted_data_required | public_company_reports | ato_taxpayer_records | False | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| transition_payment_assumptions | Transition payment assumptions | realistic_placeholder | restricted_data_required | treasury_budget_papers, pbo_public_costings | dss_services_payment_data, services_australia_records | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| uncertainty_range_assumptions | Uncertainty range assumptions | realistic_placeholder | restricted_data_required | abs_census_aggregates, treasury_budget_papers | abs_datalab_microdata, hilda_microdata | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| welfare_payment_interaction_assumptions | Welfare payment interaction assumptions | realistic_placeholder | restricted_data_required | abs_household_expenditure_income, help_hecs_thresholds | dss_services_payment_data, services_australia_records, hilda_microdata | True | False | True | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |

## H. Module Data Needs

| Module ID | Module Name | Current Data Status | Public Aggregates | Synthetic Only | Restricted Calibration Needed | Sanity Check Possible | Calibration Possible Now | Main Blockers | Must Not Claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| administrative_workflow | Administrative workflow | synthetic_fixture | False | True | True | False | False | ATO methods and legal review | must not claim: ATO guidance, enforcement, calibration completed |
| behavioural_response | Behavioural response | synthetic_fixture | False | True | True | False | False | behavioural elasticity gap, tax/legal review | must not claim: behaviour prediction, calibration completed, compliance score |
| core_formula_model | Core formula model | realistic_placeholder | True | False | True | True | False | legal attribution, AAVA deductibility, restricted taxpayer data | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| evidence_workflow | Evidence workflow | synthetic_fixture | False | True | True | False | False | real evidence forbidden in repo | must not claim: evidence sufficiency, enforcement, calibration completed |
| examples | Worked examples | synthetic_fixture | True | False | False | True | False | examples remain illustrative | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| executive_dashboard | Executive dashboard | not_collected | False | False | False | False | False | navigation only | must not claim: readiness score, validation, official status |
| external_review_attack_pack | External review attack pack | not_collected | False | False | False | False | False | questions only | must not claim: approval, validation, review completed |
| final_rc_integrity_seal | Final RC integrity seal | not_collected | False | False | False | False | False | integrity only | must not claim: approval, validation, operational readiness |
| fiscal_trajectory | Fiscal trajectory | realistic_placeholder | True | False | False | True | False | Treasury methods review | must not claim: Treasury modelling, official costing, calibration completed |
| household_distributional | Household distributional scenarios | synthetic_fixture | True | False | True | True | False | microdata not permitted in repo | must not claim: real household estimate, population estimate, calibration completed |
| household_weighting | Household weighting | synthetic_fixture | True | False | True | True | False | representativeness requires restricted methods review | must not claim: population estimate, representative sample, calibration completed |
| investment_incidence | Investment and incidence guardrails | realistic_placeholder | True | False | False | True | False | economic methods review | must not claim: economic validation, investment advice, calibration completed |
| legislative_architecture | Legislative architecture | not_collected | False | False | False | False | False | legal drafting review | must not claim: legal sufficiency, official status, operational readiness |
| payment_interactions | Payment interactions | realistic_placeholder | True | False | True | True | False | person-level data forbidden in repo | must not claim: welfare advice, individual estimate, calibration completed |
| release_candidate_pack | Release candidate pack | not_collected | False | False | False | False | False | packaging only | must not claim: official status, validation, calibration completed |
| repo_guardrails | Repository guardrails | synthetic_fixture | False | True | False | True | False | guardrail scan is not complete DLP | must not claim: complete DLP, cybersecurity validation, approval |
| reviewed_scenarios | Reviewed scenarios | synthetic_fixture | False | True | False | False | False | display controls only | must not claim: approval, validation, calibration completed |
| sector_schedules | Sector schedules | realistic_placeholder | True | False | False | True | False | source mapping and schedule authority review | must not claim: calibration completed, validation, official status, actual tax payable, operational readiness |
| sector_stress_matrix | Sector stress matrix | realistic_placeholder | True | False | False | True | False | do-not-rank metadata boundary | must not claim: official sector ranking, economic validation, calibration completed |
| secure_ingestion_controls | Secure ingestion controls | synthetic_fixture | False | True | False | True | False | prototype default-deny controls only | must not claim: cybersecurity validation, operational readiness, approval |
| transition_funding | Transition funding | realistic_placeholder | True | False | True | True | False | welfare and fiscal restricted data | must not claim: welfare validation, official costing, calibration completed |
| uncertainty_ranges | Uncertainty ranges | realistic_placeholder | True | False | True | True | False | not confidence intervals | must not claim: confidence interval, forecast, calibration completed |

## I. Realistic Placeholder Rules

| Placeholder ID | Field ID | Basis Type | Allowed Anchor Sources | Missing Real Source | Labelled Placeholder | Not Real Data | Not Calibrated |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ph_cannot_anchor_behaviour | behavioural_response_pressure_bands | cannot_anchor_yet | public_company_reports | behavioural elasticity study and authorised data | True | True | True |
| ph_fiscal_public_aggregate | fiscal_trajectory_assumptions | anchored_to_public_fiscal_aggregate | treasury_budget_papers, pbo_public_costings | Treasury/PBO methods review | True | True | True |
| ph_help_threshold | help_hecs_repayment_pressure | anchored_to_public_threshold | help_hecs_thresholds | household-level interaction data | True | True | True |
| ph_hle_labour_aggregate | hle_assumptions | anchored_to_public_industry_category | abs_labour_force | external HLE method review | True | True | True |
| ph_household_public_aggregate | household_distributional_scenario_assumptions | anchored_to_public_industry_category | abs_census_aggregates, abs_household_expenditure_income | authorised household microdata method | True | True | True |
| ph_incidence_public_report | investment_incidence_assumptions | anchored_to_public_fiscal_aggregate | treasury_budget_papers, industry_association_reports | economic incidence study | True | True | True |
| ph_opfte_public_wage_band | opfte_benchmarks | anchored_to_public_wage_band | abs_industry_wages_hours, fair_work_awards | external OPFTE benchmark study | True | True | True |
| ph_qlc_award_anchor | qlc_weights | anchored_to_public_wage_band | fair_work_awards | reviewed QLC weighting method | True | True | True |
| ph_sector_schedule_public_category | sector_schedule_values | anchored_to_public_industry_category | abs_industry_wages_hours, jobs_skills_labour_market | schedule authority calibration | True | True | True |
| ph_super_threshold | superannuation_contribution_pressure | anchored_to_public_threshold | super_guarantee_settings | wage and contribution microdata | True | True | True |

## J. Restricted Data Requirements

| Requirement ID | Data Need | Restricted Sources | Affected Fields | Affected Modules | Access Class | Commit to Repo | Reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| rd_ato_taxpayer_records | Taxpayer-level tax base and deductibility data | ato_taxpayer_records | aava_deductibility_treatment, transfer_pricing_review_shares, grouped_entity_attribution | core_formula_model, behavioural_response, administrative_workflow | confidential_or_prohibited | False | Confidential taxpayer records are forbidden repo data. |
| rd_behavioural_tax_response | Behavioural and compliance-response calibration | ato_taxpayer_records | behavioural_response_pressure_bands, anti_avoidance_thresholds | behavioural_response | confidential_or_prohibited | False | Behavioural tax response evidence cannot be inferred from repo data. |
| rd_household_microdata | Household-level distributional calibration | hilda_microdata, abs_datalab_microdata | household_distributional_scenario_assumptions, household_weighting_assumptions, uncertainty_range_assumptions | household_distributional, household_weighting, uncertainty_ranges | restricted_research_access | False | Licensed or restricted microdata cannot enter the repo. |
| rd_services_payment_records | Payment interaction and transition funding calibration | dss_services_payment_data, services_australia_records | welfare_payment_interaction_assumptions, transition_payment_assumptions | payment_interactions, transition_funding | government_internal_only | False | Person-level government records are forbidden repo data. |

## K. Forbidden Repo Data Rules

| Rule ID | Forbidden Data Type | Reason | Allowed Handling | Must Not Commit | Must Not Use In Tests | Guardrail Expected |
| --- | --- | --- | --- | --- | --- | --- |
| fd_abs_datalab | ABS DataLab microdata | Restricted microdata must remain in authorised systems | Do not commit; use public aggregates only | True | True | default-deny sensitive scan |
| fd_dss_restricted | DSS restricted records | Restricted welfare records are prohibited | External authorised environment only if ever approved | True | True | default-deny sensitive scan |
| fd_employee_records | employee records | Person-level employee records are prohibited | Use public aggregates only | True | True | default-deny sensitive scan |
| fd_firm_confidential_tax | firm-level confidential tax data | Confidential firm tax material is prohibited | Use synthetic fixtures or public aggregates only | True | True | default-deny sensitive scan |
| fd_hilda_microdata | HILDA licensed microdata | Licensed microdata cannot be placed in repo | Do not commit; source-route only | True | True | default-deny sensitive scan |
| fd_leaked_documents | leaked documents | Leaked material is prohibited | Do not collect or commit | True | True | default-deny sensitive scan |
| fd_payslips | payslips | Private payroll documents are prohibited | Use synthetic examples only | True | True | default-deny sensitive scan |
| fd_private_abn_tax_material | ABNs tied to private unpublished tax material | Private tax material is prohibited | Public ABN context is not enough to commit private tax records | True | True | default-deny sensitive scan |
| fd_private_payroll_records | private payroll records | Payroll records are confidential | Use public wage bands or synthetic fixtures | True | True | default-deny sensitive scan |
| fd_raw_bank_records | raw bank records | Private financial records are prohibited | Do not collect or commit | True | True | default-deny sensitive scan |
| fd_real_evidence_packets | real evidence packets and redacted real evidence copies | Real evidence cannot enter prototype repo | Use mock evidence packets only | True | True | default-deny evidence boundary |
| fd_scraped_personal | scraped personal data | Unauthorised scraped personal data is prohibited | Do not scrape or commit | True | True | default-deny sensitive scan |
| fd_sensitive_personal | medical or sensitive personal information | Sensitive personal information is prohibited | Do not collect or commit | True | True | default-deny sensitive scan |
| fd_services_person_records | Services Australia person-level records | Person-level administrative records are prohibited | Do not collect or commit | True | True | default-deny sensitive scan |
| fd_taxpayer_ato_data | taxpayer-level ATO data | Confidential taxpayer material is prohibited in repo | Do not collect or commit; external authorised system required if ever approved | True | True | default-deny sensitive scan |
| fd_tfns | TFNs | Tax file numbers are prohibited identifiers | Do not collect or commit | True | True | default-deny sensitive scan |
| fd_unauthorised_government_records | unauthorised government records | Unauthorised records are prohibited | Do not collect or commit | True | True | default-deny sensitive scan |

## L. Public Data Pilot Candidates

| Pilot ID | Source Candidate | Pilot Name | Candidate Modules | File Type | Download/API | Claim Level | Build 27 Ready | Blockers Before Loading |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| pilot_abs_labour_wage | abs_industry_wages_hours | ABS public aggregate labour wage table pilot | core_formula_model, sector_schedules | csv_or_xlsx_public_aggregate | manual_download | placeholder_anchor_only | True | confirm public licence, record source URL, keep aggregate-only |
| pilot_ato_corporate_public | ato_corporate_tax_transparency | ATO corporate transparency public table pilot | fiscal_trajectory, investment_incidence | csv_or_xlsx_public_table | manual_download | sanity_check_only | True | confirm public licence, avoid firm-level liability inference |
| pilot_ato_tax_stats | ato_taxation_statistics | ATO taxation statistics aggregate pilot | fiscal_trajectory, payment_interactions | public_aggregate_table | manual_download | sanity_check_only | True | confirm source licence, keep aggregate-only |
| pilot_budget_public | treasury_budget_papers | Budget paper public fiscal aggregate pilot | fiscal_trajectory, transition_funding | public_document_extract | manual_download | sanity_check_only | True | source citation and extract control |
| pilot_fair_work_awards | fair_work_awards | Fair Work wage and award anchor pilot | core_formula_model, sector_schedules | public_threshold_table | manual_download | placeholder_anchor_only | True | legal/source terms review |
| pilot_help_thresholds | help_hecs_thresholds | HELP HECS public thresholds pilot | payment_interactions | public_threshold_table | manual_download | placeholder_anchor_only | True | source citation and no individual estimates |
| pilot_state_payroll_tax | state_payroll_tax_thresholds | State payroll tax threshold public pilot | payment_interactions, fiscal_trajectory | public_threshold_table | manual_download | placeholder_anchor_only | True | jurisdiction source review and no tax advice |
| pilot_super_guarantee | super_guarantee_settings | Superannuation Guarantee public settings pilot | payment_interactions, transition_funding | public_threshold_table | manual_download | placeholder_anchor_only | True | source citation and tax review |

## M. What Can Be Sanity-Checked Now

Public aggregate candidates can support sanity-check-only comparisons and placeholder-anchor checks where public licence and source handling are reviewed before loading.

## N. What Cannot Be Calibrated Yet

Fields requiring taxpayer, firm-level confidential, household microdata, restricted research, government-internal, or confidential material cannot be calibrated in this repo path.

## O. What Must Remain Placeholder-Only

Behavioural response pressure bands, administrative workflow routing, anti-avoidance thresholds, legal attribution, and household microdata-dependent pathways remain placeholder-only until external review and authorised data access.

## P. External Review Routes

| Review Track | Scope | Main Reason |
| --- | --- | --- |
| legal_reviewer | forbidden data, evidence boundaries, public source terms | Confirm Build 27 loading does not create legal |
| tax_reviewer | AAVA, ATO public sources, payroll tax, transfer pricing | Prevent public tax tables being overread as real tax-payable support. |
| treasury_methods_reviewer | fiscal aggregates, Budget papers, PBO public material | Prevent public fiscal documents being overread as official costing. |
| ato_methods_reviewer | ATO public aggregates, taxpayer-record boundary | Keep ATO public data separate from ATO records |
| privacy_reviewer | restricted data, forbidden repo data, household microdata | Ensure no person-level or restricted data enters the repository. |
| statistical_methods_reviewer | aggregate sanity checks, household weighting, uncertainty | Prevent public aggregates being overread as population estimates or confidence intervals. |

## Q. Build 27 Public Data Pilot Readiness

- Total source candidates: 20
- Public source candidates: 15
- Restricted source candidates: 5
- Forbidden repo sources: 7
- Total calibration fields: 33
- Fields public sanity check possible: 26
- Fields public calibration possible: 0
- Fields requiring restricted data: 14
- Total realistic placeholders: 10
- Total forbidden data rules: 17
- Total public data pilot candidates: 8
- Build 27 ready candidates: 8
- real_data_loaded: False
- real_calibration_completed: False
- restricted_data_loaded: False
- taxpayer_data_loaded: False
- firm_level_confidential_data_loaded: False
- household_microdata_loaded: False
- realistic_placeholders_created: True
- placeholders_labelled: True
- public_data_pilot_ready: True
- validation_claimed: False
- approval_claimed: False
- operational_readiness_claimed: False
- legal_sufficiency_claimed: False
- official_status_claimed: False
- firm_level_liability_logic_modified: False

## R. Limitations and Future Work

- Build 26 loads no real datasets and creates no calibration values.
- Realistic placeholders must remain labelled as placeholders and must not be described as real data.
- Build 25 sealed the previous RC state; if Build 26 is included in a later sealed RC, the integrity seal should be regenerated for that state.
- Report generated at: 2026-05-19T04:39:23+00:00
