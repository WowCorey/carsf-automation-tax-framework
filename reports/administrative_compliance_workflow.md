# CARSF V1.5 ATO / Administrative Compliance Workflow

Generated at: `2026-05-19T00:02:03+00:00`

## A. Purpose

This report organises synthetic CARSF cases into prototype evidence requests, review queues, escalation pathways, behavioural-response links, sector schedule review, grouped-entity review, transfer-pricing review, privacy/secrecy review, methods review, and external calibration review.

## B. Non-Claims

- This is a prototype administrative workflow only. It is not an official workflow of the ATO. It is not guidance from the ATO, Treasury modelling, legal advice, tax advice, compliance scoring, audit logic, or enforcement. It does not create notices, implement penalties, use statutory information-gathering powers, determine non-compliance, estimate actual tax payable, predict taxpayer behaviour, estimate behavioural elasticity, use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, or modify firm-level CARSF liability.
- The workflow only organises synthetic placeholder review pathways for policy discussion.
- All workflow steps require external legal, tax, ATO-methods, Treasury-methods, privacy, calibration, and administrative-design review before any real use.
- Every result has `do_not_enforce: true`.
- Every result has `do_not_issue_notice: true`.
- Every result has `do_not_score_compliance: true`.
- Every result has `do_not_estimate_tax_payable: true`.
- Firm-level CARSF liability logic is not modified.

## C. Method - Synthetic Administrative Pathways Only

The workflow uses declared synthetic scenario metadata, existing prototype evidence requirement IDs, synthetic mock packet IDs, behavioural response links, and sector schedule IDs. It organises review pathways only and creates no real action.

## D. Scenario Coverage

- `artificial_low_aava_cost_loading_review`: Artificial low AAVA cost-loading review
- `call_centre_token_oversight_triage`: Call-centre token oversight triage
- `enhanced_privacy_evidence_handling_check`: Enhanced privacy evidence handling check
- `enhanced_sector_schedule_documentation_check`: Enhanced sector schedule documentation check
- `grouped_entity_thin_australian_employer_review`: Grouped-entity thin Australian employer review
- `mixed_unit_schedule_classification_review`: Mixed-unit schedule classification review
- `offshore_automation_service_attribution_review`: Offshore automation service attribution review
- `open_source_ai_treatment_locked_calibration_review`: Open-source AI treatment locked-for-calibration review
- `related_party_ai_service_fee_review`: Related-party AI service fee review
- `retail_self_checkout_labour_relabelling_review`: Retail self-checkout labour relabelling review
- `robotics_leasing_capital_base_review`: Robotics leasing capital-base review
- `routine_formula_completeness_check`: Routine formula completeness check
- `software_platform_ip_royalty_aasb_review`: Software platform IP royalty / AASB 138 review

## E. Administrative Workflow Matrix

| Scenario ID | Scenario Name | Sector Schedule | Linked Behavioural Responses | Trigger Flags | Review Domains | Evidence Bundle Size | Workflow Decision Band | Workflow Status | Escalation Queues | External Review Required | Do Not Enforce | Main Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| artificial_low_aava_cost_loading_review | Artificial low AAVA cost-loading review | accounting_administration | artificial_low_aava_cost_loading, cloud_inference_operating_cost_relabelling | ARTIFICIAL_LOW_PROFIT_OR_AAVA, CLOUD_COST_RELABELING | aava_deductibility_review, behavioural_response_review, core_formula, legal_policy_review, transfer_pricing_review | 21 | external_review_required | locked_for_external_review | legal_policy_queue | True | True | Locked for external review because the scenario explicitly requires external review. |
| call_centre_token_oversight_triage | Call-centre token oversight triage | call_centres_customer_support | fake_qlc_concentrated_roles, token_oversight_workforce_wrapper | FAKE_QLC_INFLATION, TOKEN_HUMAN_OVERSIGHT | behavioural_response_review, core_formula, grouped_entity_review, privacy_secrecy_review | 23 | external_review_required | locked_for_external_review | legal_policy_queue | True | True | Locked for external review because the scenario explicitly requires external review. |
| enhanced_privacy_evidence_handling_check | Enhanced privacy evidence handling check | call_centres_customer_support | None | CORE_FORMULA_COMPLETENESS, PRIVACY_EVIDENCE_HANDLING | core_formula, privacy_secrecy_review | 9 | enhanced_placeholder_review | show_with_warning | None | False | True | enhanced_placeholder_review from deterministic placeholder workflow scoring; Base complexity is enhanced because specialist prototype review domains are present. |
| enhanced_sector_schedule_documentation_check | Enhanced sector schedule documentation check | call_centres_customer_support | None | CORE_FORMULA_COMPLETENESS, SECTOR_SCHEDULE_DOCUMENTATION | core_formula, sector_schedule_review | 8 | enhanced_placeholder_review | show_with_warning | ato_methods_queue, treasury_methods_queue | False | True | enhanced_placeholder_review from deterministic placeholder workflow scoring; Base complexity is enhanced because specialist prototype review domains are present. |
| grouped_entity_thin_australian_employer_review | Grouped-entity thin Australian employer review | logistics_warehousing | offshore_automation_service_routing, related_party_ai_service_fee_routing | ENTITY_SPLITTING, OFFSHORE_AUTOMATION_SERVICE, RELATED_PARTY_AI_SERVICE_FEES | behavioural_response_review, core_formula, grouped_entity_review, legal_policy_review, offshore_attribution_review, privacy_secrecy_review, transfer_pricing_review | 31 | external_review_required | locked_for_external_review | legal_policy_queue | True | True | Locked for external review because the scenario explicitly requires external review. |
| mixed_unit_schedule_classification_review | Mixed-unit schedule classification review | logistics_warehousing | mixed_unit_apportionment_gaming, schedule_classification_arbitrage | SECTOR_CLASSIFICATION_ARBITRAGE | behavioural_response_review, core_formula, external_calibration_review, sector_schedule_review | 20 | external_review_required | locked_for_external_review | ato_methods_queue, external_calibration_queue, treasury_methods_queue | True | True | Locked for external review because the scenario explicitly requires external review. |
| offshore_automation_service_attribution_review | Offshore automation service attribution review | logistics_warehousing | offshore_automation_service_routing | OFFSHORE_AUTOMATION_SERVICE, RELATED_PARTY_AI_SERVICE_FEES | behavioural_response_review, core_formula, grouped_entity_review, legal_policy_review, offshore_attribution_review, transfer_pricing_review | 27 | external_review_required | locked_for_external_review | legal_policy_queue | True | True | Locked for external review because the scenario explicitly requires external review. |
| open_source_ai_treatment_locked_calibration_review | Open-source AI treatment locked-for-calibration review | software_digital_platforms | open_source_ai_treatment_gap | OPEN_SOURCE_AI_TREATMENT_GAP | behavioural_response_review, capital_base_review, external_calibration_review, legal_policy_review, sector_schedule_review, treasury_methods_review | 20 | suppress_until_calibrated | suppress_until_calibrated | ato_methods_queue, external_calibration_queue, legal_policy_queue, suppression_queue, treasury_methods_queue | True | True | Suppressed until calibrated because the scenario declares unresolved external dependencies. |
| related_party_ai_service_fee_review | Related-party AI service fee review | accounting_administration | related_party_ai_service_fee_routing | ARTIFICIAL_LOW_PROFIT_OR_AAVA, RELATED_PARTY_AI_SERVICE_FEES | aava_deductibility_review, behavioural_response_review, core_formula, legal_policy_review, transfer_pricing_review | 21 | external_review_required | locked_for_external_review | legal_policy_queue | True | True | Locked for external review because the scenario explicitly requires external review. |
| retail_self_checkout_labour_relabelling_review | Retail self-checkout labour relabelling review | retail_self_checkout_fulfilment | customer_self_checkout_labour_relabelling | CUSTOMER_SELF_SERVICE_REVIEW, SECTOR_CLASSIFICATION_ARBITRAGE | behavioural_response_review, core_formula, legal_policy_review, privacy_secrecy_review, sector_schedule_review | 20 | external_review_required | external_review_required | ato_methods_queue, legal_policy_queue, treasury_methods_queue | True | True | external_review_required from deterministic placeholder workflow scoring; Base complexity is complex because tax-sensitive review domains are present. |
| robotics_leasing_capital_base_review | Robotics leasing capital-base review | automotive_repair | robotics_lease_substitution | ROBOTICS_LEASING_AVOIDANCE | aava_deductibility_review, behavioural_response_review, capital_base_review, core_formula, transfer_pricing_review | 22 | external_review_required | locked_for_external_review | legal_policy_queue, treasury_methods_queue | True | True | Locked for external review because the scenario explicitly requires external review. |
| routine_formula_completeness_check | Routine formula completeness check | automotive_repair | None | CORE_FORMULA_COMPLETENESS | core_formula | 5 | routine_placeholder_review | prototype_discussion_only | None | False | True | routine_placeholder_review from deterministic placeholder workflow scoring; Base complexity is routine for a synthetic intake and evidence request. |
| software_platform_ip_royalty_aasb_review | Software platform IP royalty / AASB 138 review | software_digital_platforms | cloud_inference_operating_cost_relabelling, platform_ip_royalty_routing | ARTIFICIAL_LOW_PROFIT_OR_AAVA, OFFSHORE_AUTOMATION_SERVICE, RELATED_PARTY_AI_SERVICE_FEES | aava_deductibility_review, ato_methods_review, behavioural_response_review, capital_base_review, core_formula, legal_policy_review, offshore_attribution_review, sector_schedule_review, transfer_pricing_review, treasury_methods_review | 26 | external_review_required | locked_for_external_review | ato_methods_queue, legal_policy_queue, treasury_methods_queue | True | True | Locked for external review because the scenario explicitly requires external review. |

## F. Evidence Request Bundles

| Scenario ID | Bundle ID | Requirement Count | Requirement IDs |
| --- | --- | --- | --- |
| artificial_low_aava_cost_loading_review | artificial_low_aava_cost_loading_review_evidence_bundle | 21 | avoid_cloud_relabelling, avoid_entity_splitting, avoid_fake_qlc, avoid_offshore_ai, avoid_related_party_fees, avoid_robotics_leasing, avoid_sector_classification, avoid_token_oversight, core_aava_revenue_costs, core_aii_components, core_output_unit, core_output_value, core_worker_hours, tp_cloud_inference, tp_cost_sharing, tp_data_model_access, tp_management_technical, tp_related_party_agreements, tp_robotics_leasing, tp_royalty_licence, tp_service_fee_invoices |
| call_centre_token_oversight_triage | call_centre_token_oversight_triage_evidence_bundle | 23 | avoid_cloud_relabelling, avoid_entity_splitting, avoid_fake_qlc, avoid_offshore_ai, avoid_related_party_fees, avoid_robotics_leasing, avoid_sector_classification, avoid_token_oversight, core_aava_revenue_costs, core_aii_components, core_australian_nexus, core_job_security, core_output_unit, core_output_value, core_skill_development, core_wage_quality, core_worker_hours, group_common_control, group_customer_facing, group_employer, group_ip_owner, group_offshore_provider, group_service_provider |
| enhanced_privacy_evidence_handling_check | enhanced_privacy_evidence_handling_check_evidence_bundle | 9 | core_aava_revenue_costs, core_aii_components, core_australian_nexus, core_job_security, core_output_unit, core_output_value, core_skill_development, core_wage_quality, core_worker_hours |
| enhanced_sector_schedule_documentation_check | enhanced_sector_schedule_documentation_check_evidence_bundle | 8 | core_aava_revenue_costs, core_aii_components, core_output_unit, core_output_value, core_worker_hours, mixed_activity_shares, mixed_schedule_classification, mixed_unit_evidence |
| grouped_entity_thin_australian_employer_review | grouped_entity_thin_australian_employer_review_evidence_bundle | 31 | avoid_cloud_relabelling, avoid_entity_splitting, avoid_fake_qlc, avoid_offshore_ai, avoid_related_party_fees, avoid_robotics_leasing, avoid_sector_classification, avoid_token_oversight, core_aava_revenue_costs, core_aii_components, core_australian_nexus, core_job_security, core_output_unit, core_output_value, core_skill_development, core_wage_quality, core_worker_hours, group_common_control, group_customer_facing, group_employer, group_ip_owner, group_offshore_provider, group_service_provider, tp_cloud_inference, tp_cost_sharing, tp_data_model_access, tp_management_technical, tp_related_party_agreements, tp_robotics_leasing, tp_royalty_licence, tp_service_fee_invoices |
| mixed_unit_schedule_classification_review | mixed_unit_schedule_classification_review_evidence_bundle | 20 | avoid_cloud_relabelling, avoid_entity_splitting, avoid_fake_qlc, avoid_offshore_ai, avoid_related_party_fees, avoid_robotics_leasing, avoid_sector_classification, avoid_token_oversight, core_aava_revenue_costs, core_aii_components, core_frv, core_opfte_libc, core_output_unit, core_output_value, core_rates, core_worker_hours, mixed_activity_shares, mixed_conversion_metadata, mixed_schedule_classification, mixed_unit_evidence |
| offshore_automation_service_attribution_review | offshore_automation_service_attribution_review_evidence_bundle | 27 | avoid_cloud_relabelling, avoid_entity_splitting, avoid_fake_qlc, avoid_offshore_ai, avoid_related_party_fees, avoid_robotics_leasing, avoid_sector_classification, avoid_token_oversight, core_aava_revenue_costs, core_aii_components, core_output_unit, core_output_value, core_worker_hours, group_common_control, group_customer_facing, group_employer, group_ip_owner, group_offshore_provider, group_service_provider, tp_cloud_inference, tp_cost_sharing, tp_data_model_access, tp_management_technical, tp_related_party_agreements, tp_robotics_leasing, tp_royalty_licence, tp_service_fee_invoices |
| open_source_ai_treatment_locked_calibration_review | open_source_ai_treatment_locked_calibration_review_evidence_bundle | 20 | avoid_cloud_relabelling, avoid_entity_splitting, avoid_fake_qlc, avoid_offshore_ai, avoid_related_party_fees, avoid_robotics_leasing, avoid_sector_classification, avoid_token_oversight, core_capital_base, core_frv, core_opfte_libc, core_output_unit, core_rates, mixed_activity_shares, mixed_conversion_metadata, mixed_schedule_classification, mixed_unit_evidence, tp_data_model_access, tp_robotics_leasing, tp_royalty_licence |
| related_party_ai_service_fee_review | related_party_ai_service_fee_review_evidence_bundle | 21 | avoid_cloud_relabelling, avoid_entity_splitting, avoid_fake_qlc, avoid_offshore_ai, avoid_related_party_fees, avoid_robotics_leasing, avoid_sector_classification, avoid_token_oversight, core_aava_revenue_costs, core_aii_components, core_output_unit, core_output_value, core_worker_hours, tp_cloud_inference, tp_cost_sharing, tp_data_model_access, tp_management_technical, tp_related_party_agreements, tp_robotics_leasing, tp_royalty_licence, tp_service_fee_invoices |
| retail_self_checkout_labour_relabelling_review | retail_self_checkout_labour_relabelling_review_evidence_bundle | 20 | avoid_cloud_relabelling, avoid_entity_splitting, avoid_fake_qlc, avoid_offshore_ai, avoid_related_party_fees, avoid_robotics_leasing, avoid_sector_classification, avoid_token_oversight, core_aava_revenue_costs, core_aii_components, core_australian_nexus, core_job_security, core_output_unit, core_output_value, core_skill_development, core_wage_quality, core_worker_hours, mixed_activity_shares, mixed_schedule_classification, mixed_unit_evidence |
| robotics_leasing_capital_base_review | robotics_leasing_capital_base_review_evidence_bundle | 22 | avoid_cloud_relabelling, avoid_entity_splitting, avoid_fake_qlc, avoid_offshore_ai, avoid_related_party_fees, avoid_robotics_leasing, avoid_sector_classification, avoid_token_oversight, core_aava_revenue_costs, core_aii_components, core_capital_base, core_output_unit, core_output_value, core_worker_hours, tp_cloud_inference, tp_cost_sharing, tp_data_model_access, tp_management_technical, tp_related_party_agreements, tp_robotics_leasing, tp_royalty_licence, tp_service_fee_invoices |
| routine_formula_completeness_check | routine_formula_completeness_check_evidence_bundle | 5 | core_aava_revenue_costs, core_aii_components, core_output_unit, core_output_value, core_worker_hours |
| software_platform_ip_royalty_aasb_review | software_platform_ip_royalty_aasb_review_evidence_bundle | 26 | avoid_cloud_relabelling, avoid_entity_splitting, avoid_fake_qlc, avoid_offshore_ai, avoid_related_party_fees, avoid_robotics_leasing, avoid_sector_classification, avoid_token_oversight, core_aava_revenue_costs, core_aii_components, core_capital_base, core_output_unit, core_output_value, core_worker_hours, group_offshore_provider, mixed_activity_shares, mixed_schedule_classification, mixed_unit_evidence, tp_cloud_inference, tp_cost_sharing, tp_data_model_access, tp_management_technical, tp_related_party_agreements, tp_robotics_leasing, tp_royalty_licence, tp_service_fee_invoices |

## G. Review Queue Assignments

- `aava_review_queue`: artificial_low_aava_cost_loading_review, related_party_ai_service_fee_review, robotics_leasing_capital_base_review, software_platform_ip_royalty_aasb_review
- `ato_methods_queue`: enhanced_sector_schedule_documentation_check, mixed_unit_schedule_classification_review, open_source_ai_treatment_locked_calibration_review, retail_self_checkout_labour_relabelling_review, software_platform_ip_royalty_aasb_review
- `behavioural_response_queue`: artificial_low_aava_cost_loading_review, call_centre_token_oversight_triage, grouped_entity_thin_australian_employer_review, mixed_unit_schedule_classification_review, offshore_automation_service_attribution_review, open_source_ai_treatment_locked_calibration_review, related_party_ai_service_fee_review, retail_self_checkout_labour_relabelling_review, robotics_leasing_capital_base_review, software_platform_ip_royalty_aasb_review
- `capital_base_review_queue`: open_source_ai_treatment_locked_calibration_review, robotics_leasing_capital_base_review, software_platform_ip_royalty_aasb_review
- `evidence_queue`: artificial_low_aava_cost_loading_review, call_centre_token_oversight_triage, enhanced_privacy_evidence_handling_check, enhanced_sector_schedule_documentation_check, grouped_entity_thin_australian_employer_review, mixed_unit_schedule_classification_review, offshore_automation_service_attribution_review, open_source_ai_treatment_locked_calibration_review, related_party_ai_service_fee_review, retail_self_checkout_labour_relabelling_review, robotics_leasing_capital_base_review, routine_formula_completeness_check, software_platform_ip_royalty_aasb_review
- `external_calibration_queue`: mixed_unit_schedule_classification_review, open_source_ai_treatment_locked_calibration_review
- `grouped_entity_queue`: call_centre_token_oversight_triage, grouped_entity_thin_australian_employer_review, offshore_automation_service_attribution_review
- `intake_queue`: artificial_low_aava_cost_loading_review, call_centre_token_oversight_triage, enhanced_privacy_evidence_handling_check, enhanced_sector_schedule_documentation_check, grouped_entity_thin_australian_employer_review, mixed_unit_schedule_classification_review, offshore_automation_service_attribution_review, related_party_ai_service_fee_review, retail_self_checkout_labour_relabelling_review, robotics_leasing_capital_base_review, routine_formula_completeness_check, software_platform_ip_royalty_aasb_review
- `legal_policy_queue`: artificial_low_aava_cost_loading_review, call_centre_token_oversight_triage, grouped_entity_thin_australian_employer_review, offshore_automation_service_attribution_review, open_source_ai_treatment_locked_calibration_review, related_party_ai_service_fee_review, retail_self_checkout_labour_relabelling_review, robotics_leasing_capital_base_review, software_platform_ip_royalty_aasb_review
- `offshore_attribution_queue`: grouped_entity_thin_australian_employer_review, offshore_automation_service_attribution_review, software_platform_ip_royalty_aasb_review
- `privacy_review_queue`: call_centre_token_oversight_triage, enhanced_privacy_evidence_handling_check, grouped_entity_thin_australian_employer_review, retail_self_checkout_labour_relabelling_review
- `prototype_closure_queue`: artificial_low_aava_cost_loading_review, call_centre_token_oversight_triage, enhanced_privacy_evidence_handling_check, enhanced_sector_schedule_documentation_check, grouped_entity_thin_australian_employer_review, mixed_unit_schedule_classification_review, offshore_automation_service_attribution_review, open_source_ai_treatment_locked_calibration_review, related_party_ai_service_fee_review, retail_self_checkout_labour_relabelling_review, robotics_leasing_capital_base_review, routine_formula_completeness_check, software_platform_ip_royalty_aasb_review
- `sector_schedule_queue`: enhanced_sector_schedule_documentation_check, mixed_unit_schedule_classification_review, open_source_ai_treatment_locked_calibration_review, retail_self_checkout_labour_relabelling_review, software_platform_ip_royalty_aasb_review
- `suppression_queue`: open_source_ai_treatment_locked_calibration_review
- `transfer_pricing_queue`: artificial_low_aava_cost_loading_review, grouped_entity_thin_australian_employer_review, offshore_automation_service_attribution_review, related_party_ai_service_fee_review, robotics_leasing_capital_base_review, software_platform_ip_royalty_aasb_review
- `treasury_methods_queue`: enhanced_sector_schedule_documentation_check, mixed_unit_schedule_classification_review, open_source_ai_treatment_locked_calibration_review, retail_self_checkout_labour_relabelling_review, robotics_leasing_capital_base_review, software_platform_ip_royalty_aasb_review

## H. Escalation Pathways

- `artificial_low_aava_cost_loading_review`: legal_policy_queue
- `call_centre_token_oversight_triage`: legal_policy_queue
- `enhanced_privacy_evidence_handling_check`: No external escalation queue listed
- `enhanced_sector_schedule_documentation_check`: ato_methods_queue, treasury_methods_queue
- `grouped_entity_thin_australian_employer_review`: legal_policy_queue
- `mixed_unit_schedule_classification_review`: ato_methods_queue, external_calibration_queue, treasury_methods_queue
- `offshore_automation_service_attribution_review`: legal_policy_queue
- `open_source_ai_treatment_locked_calibration_review`: ato_methods_queue, external_calibration_queue, legal_policy_queue, suppression_queue, treasury_methods_queue
- `related_party_ai_service_fee_review`: legal_policy_queue
- `retail_self_checkout_labour_relabelling_review`: ato_methods_queue, legal_policy_queue, treasury_methods_queue
- `robotics_leasing_capital_base_review`: legal_policy_queue, treasury_methods_queue
- `routine_formula_completeness_check`: No external escalation queue listed
- `software_platform_ip_royalty_aasb_review`: ato_methods_queue, legal_policy_queue, treasury_methods_queue

## I. Behavioural Response Links

- `artificial_low_aava_cost_loading_review` links to: artificial_low_aava_cost_loading, cloud_inference_operating_cost_relabelling
- `call_centre_token_oversight_triage` links to: fake_qlc_concentrated_roles, token_oversight_workforce_wrapper
- `enhanced_privacy_evidence_handling_check` links to: None
- `enhanced_sector_schedule_documentation_check` links to: None
- `grouped_entity_thin_australian_employer_review` links to: offshore_automation_service_routing, related_party_ai_service_fee_routing
- `mixed_unit_schedule_classification_review` links to: mixed_unit_apportionment_gaming, schedule_classification_arbitrage
- `offshore_automation_service_attribution_review` links to: offshore_automation_service_routing
- `open_source_ai_treatment_locked_calibration_review` links to: open_source_ai_treatment_gap
- `related_party_ai_service_fee_review` links to: related_party_ai_service_fee_routing
- `retail_self_checkout_labour_relabelling_review` links to: customer_self_checkout_labour_relabelling
- `robotics_leasing_capital_base_review` links to: robotics_lease_substitution
- `routine_formula_completeness_check` links to: None
- `software_platform_ip_royalty_aasb_review` links to: cloud_inference_operating_cost_relabelling, platform_ip_royalty_routing

## J. Privacy / Secrecy Review Notes

- `artificial_low_aava_cost_loading_review` sensitivity: `high`; privacy review queue: False
- `call_centre_token_oversight_triage` sensitivity: `high`; privacy review queue: True
- `enhanced_privacy_evidence_handling_check` sensitivity: `moderate`; privacy review queue: True
- `enhanced_sector_schedule_documentation_check` sensitivity: `low`; privacy review queue: False
- `grouped_entity_thin_australian_employer_review` sensitivity: `high`; privacy review queue: True
- `mixed_unit_schedule_classification_review` sensitivity: `moderate`; privacy review queue: False
- `offshore_automation_service_attribution_review` sensitivity: `high`; privacy review queue: False
- `open_source_ai_treatment_locked_calibration_review` sensitivity: `low`; privacy review queue: False
- `related_party_ai_service_fee_review` sensitivity: `high`; privacy review queue: False
- `retail_self_checkout_labour_relabelling_review` sensitivity: `moderate`; privacy review queue: True
- `robotics_leasing_capital_base_review` sensitivity: `moderate`; privacy review queue: False
- `routine_formula_completeness_check` sensitivity: `low`; privacy review queue: False
- `software_platform_ip_royalty_aasb_review` sensitivity: `high`; privacy review queue: False

## K. Suppressed / Locked-for-External-Review Cases

- `artificial_low_aava_cost_loading_review`: `locked_for_external_review` (Locked for external review because the scenario explicitly requires external review.)
- `call_centre_token_oversight_triage`: `locked_for_external_review` (Locked for external review because the scenario explicitly requires external review.)
- `grouped_entity_thin_australian_employer_review`: `locked_for_external_review` (Locked for external review because the scenario explicitly requires external review.)
- `mixed_unit_schedule_classification_review`: `locked_for_external_review` (Locked for external review because the scenario explicitly requires external review.)
- `offshore_automation_service_attribution_review`: `locked_for_external_review` (Locked for external review because the scenario explicitly requires external review.)
- `open_source_ai_treatment_locked_calibration_review`: `suppress_until_calibrated` (Suppressed until calibrated because the scenario declares unresolved external dependencies.)
- `related_party_ai_service_fee_review`: `locked_for_external_review` (Locked for external review because the scenario explicitly requires external review.)
- `retail_self_checkout_labour_relabelling_review`: `external_review_required` (external_review_required from deterministic placeholder workflow scoring; Base complexity is complex because tax-sensitive review domains are present.)
- `robotics_leasing_capital_base_review`: `locked_for_external_review` (Locked for external review because the scenario explicitly requires external review.)
- `software_platform_ip_royalty_aasb_review`: `locked_for_external_review` (Locked for external review because the scenario explicitly requires external review.)

## L. Calibration and Administrative Design Blockers

- artificial_low_aava_cost_loading_review: legal_policy_queue requires external review
- call_centre_token_oversight_triage: legal_policy_queue requires external review
- enhanced_sector_schedule_documentation_check: ato_methods_queue requires external review
- enhanced_sector_schedule_documentation_check: treasury_methods_queue requires external review
- grouped_entity_thin_australian_employer_review: legal_policy_queue requires external review
- mixed_unit_schedule_classification_review: ato_methods_queue requires external review
- mixed_unit_schedule_classification_review: external_calibration_queue requires external review
- mixed_unit_schedule_classification_review: treasury_methods_queue requires external review
- offshore_automation_service_attribution_review: legal_policy_queue requires external review
- open_source_ai_treatment_locked_calibration_review: ato_methods_queue requires external review
- open_source_ai_treatment_locked_calibration_review: external_calibration_queue requires external review
- open_source_ai_treatment_locked_calibration_review: legal_policy_queue requires external review
- open_source_ai_treatment_locked_calibration_review: suppressed until calibration and external methods review
- open_source_ai_treatment_locked_calibration_review: suppression_queue requires external review
- open_source_ai_treatment_locked_calibration_review: treasury_methods_queue requires external review
- related_party_ai_service_fee_review: legal_policy_queue requires external review
- retail_self_checkout_labour_relabelling_review: ato_methods_queue requires external review
- retail_self_checkout_labour_relabelling_review: legal_policy_queue requires external review
- retail_self_checkout_labour_relabelling_review: treasury_methods_queue requires external review
- robotics_leasing_capital_base_review: legal_policy_queue requires external review
- robotics_leasing_capital_base_review: treasury_methods_queue requires external review
- software_platform_ip_royalty_aasb_review: ato_methods_queue requires external review
- software_platform_ip_royalty_aasb_review: legal_policy_queue requires external review
- software_platform_ip_royalty_aasb_review: treasury_methods_queue requires external review

## M. Plain-English Interpretation

- Workflow decision bands indicate prototype review complexity only.
- Evidence bundles are draft request lists based on existing prototype evidence requirement IDs.
- Escalation queues show where external legal, tax, methods, privacy, calibration, or administrative-design review would be needed.
- Locked or suppressed cases should not be presented as ready for operational use.

## N. Limitations and Future Review Needs

### Scenarios By Decision Band

- `enhanced_placeholder_review`: 2
- `external_review_required`: 9
- `routine_placeholder_review`: 1
- `suppress_until_calibrated`: 1

### Scenarios By Workflow Status

- `external_review_required`: 1
- `locked_for_external_review`: 8
- `prototype_discussion_only`: 1
- `show_with_warning`: 2
- `suppress_until_calibrated`: 1

### Scenarios By Sector Schedule

- `accounting_administration`: 2
- `automotive_repair`: 2
- `call_centres_customer_support`: 3
- `logistics_warehousing`: 3
- `retail_self_checkout_fulfilment`: 1
- `software_digital_platforms`: 2

- Total scenarios: 13
- Scenarios requiring external review: 10
- Scenarios locked for external review: 8
- Scenarios suppressed until calibrated: 1
- Scenarios requiring evidence queue: 13
- Scenarios requiring grouped-entity queue: 3
- Scenarios requiring transfer-pricing queue: 6
- Scenarios requiring sector schedule queue: 5
- Scenarios requiring AAVA review queue: 4
- Scenarios requiring capital-base review queue: 3
- Scenarios requiring offshore-attribution queue: 3
- Scenarios requiring privacy review queue: 4
- Scenarios requiring legal-policy queue: 9
- Scenarios requiring ATO-methods queue: 5
- Scenarios requiring Treasury-methods queue: 6
- Firm-level liability logic modified: False
- Real enforcement created: False
- Real ATO power claimed: False
- Compliance scoring created: False
- Notices created: False
- Real data used: False
- Prototype only.
- Placeholder only.
- Synthetic administrative pathways only.
- Not a workflow endorsed by the ATO, not guidance from the ATO, not Treasury modelling, not audit logic, not enforcement, and not compliance scoring.
- No statutory powers, notices, penalties, taxpayer-level data, firm-level data, industry data, ABS/ATO/DSS/Treasury/PBO/HILDA/Census data, legal advice, tax advice, economic validation, conduct forecasting, or elasticity modelling.
- Not usable to estimate actual tax payable.
- Firm-level CARSF liability logic is not modified.
