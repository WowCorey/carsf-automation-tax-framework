# CARSF V1.5 Behavioural Response / Gaming Simulation

Generated at: `2026-05-19T00:02:02+00:00`

## A. Purpose

This report maps synthetic CARSF response pathways to placeholder pressure bands, linked avoidance flags, and review pathways for policy discussion.

## B. Non-Claims

- Behavioural response simulation is prototype-only deterministic placeholder scenario review. It does not predict taxpayer behaviour. It does not estimate behavioural elasticity. It is not ATO audit logic, Treasury modelling, ABS/ATO/DSS/PBO analysis, economic validation, compliance-risk scoring, legal advice, tax advice, or investment advice. It does not estimate actual tax payable, modify firm-level CARSF liability, implement penalties, or implement enforcement.
- The simulation does not use firm-level, taxpayer-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- All response scenarios are synthetic placeholders requiring external calibration, legal review, ATO/Treasury methods review, and behavioural research.
- Scenario pressure bands are review prompts only, not compliance findings or real-world outcome estimates.
- Every result has `do_not_predict: true`.
- Every result has `do_not_score_real_taxpayer: true`.
- Firm-level CARSF liability logic is not modified.

## C. Method - Synthetic Placeholder Pathways Only

The simulation uses declared synthetic scenario metadata, pressure basis labels, capped text modifiers, linked prototype avoidance flags, countermeasure categories, and sector stress display status. It simulates response pathways, not behavioural outcomes.

## D. Scenario Coverage

- `artificial_low_aava_cost_loading`: Artificial low AAVA through cost loading (`artificial_low_profit_or_aava`)
- `cloud_inference_operating_cost_relabelling`: Cloud / inference relabelling as ordinary operating cost (`cloud_inference_relabelling`)
- `customer_self_checkout_labour_relabelling`: Customer self-checkout labour relabelling (`customer_self_service_shift`)
- `fake_qlc_concentrated_roles`: Fake QLC inflation through concentrated high-scored roles (`fake_qlc_inflation`)
- `mixed_unit_apportionment_gaming`: Mixed-unit apportionment gaming (`mixed_unit_apportionment_gaming`)
- `offshore_automation_service_routing`: Offshore automation-as-a-service routing (`offshore_automation_service_routing`)
- `open_source_ai_treatment_gap`: Open-source AI treatment gap (`open_source_ai_treatment_gap`)
- `platform_ip_royalty_routing`: Platform IP royalty routing (`platform_ip_royalty_routing`)
- `related_party_ai_service_fee_routing`: Related-party AI service fee routing (`related_party_ai_service_fees`)
- `robotics_lease_substitution`: Robotics lease substitution for capital ownership (`robotics_leasing_shift`)
- `schedule_classification_arbitrage`: Schedule classification arbitrage (`schedule_classification_arbitrage`)
- `token_oversight_workforce_wrapper`: Token oversight workforce wrapper (`token_human_oversight`)

## E. Behavioural Response Matrix

| Scenario ID | Scenario Name | Sector Schedule | Response Type | Pressure Basis | Linked Avoidance Flags | Response Pressure Band | Review Status | Countermeasure Categories | External Review Required | Do Not Predict | Main Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| artificial_low_aava_cost_loading | Artificial low AAVA through cost loading | accounting_administration | artificial_low_profit_or_aava | multi_pathway | ARTIFICIAL_LOW_PROFIT_OR_AAVA, RELATED_PARTY_AI_SERVICE_FEES | critical_review_required | external_review_required | aava_deductibility_review, grouped_entity_review, transfer_pricing_review | True | True | critical_review_required from deterministic placeholder scoring; Base pressure comes from declared placeholder pressure `high`. |
| cloud_inference_operating_cost_relabelling | Cloud / inference relabelling as ordinary operating cost | software_digital_platforms | cloud_inference_relabelling | unresolved_legal_treatment | ARTIFICIAL_LOW_PROFIT_OR_AAVA, CLOUD_COST_RELABELING | critical_review_required | external_review_required | aava_deductibility_review, evidence_requirement, transfer_pricing_review | True | True | critical_review_required from deterministic placeholder scoring; Base pressure comes from declared placeholder pressure `high`. |
| customer_self_checkout_labour_relabelling | Customer self-checkout labour relabelling | retail_self_checkout_fulfilment | customer_self_service_shift | single_pathway | SECTOR_CLASSIFICATION_ARBITRAGE | high_placeholder_response_pressure | strong_warning_required | customer_self_service_review, legal_policy_review, schedule_authority_review | True | True | high_placeholder_response_pressure from deterministic placeholder scoring; Base pressure comes from declared placeholder pressure `moderate`. |
| fake_qlc_concentrated_roles | Fake QLC inflation through concentrated high-scored roles | call_centres_customer_support | fake_qlc_inflation | single_pathway | FAKE_QLC_INFLATION, TOKEN_HUMAN_OVERSIGHT | high_placeholder_response_pressure | strong_warning_required | evidence_requirement, grouped_entity_review | True | True | high_placeholder_response_pressure from deterministic placeholder scoring; Base pressure comes from declared placeholder pressure `high`. |
| mixed_unit_apportionment_gaming | Mixed-unit apportionment gaming | logistics_warehousing | mixed_unit_apportionment_gaming | multi_pathway | SECTOR_CLASSIFICATION_ARBITRAGE | moderate_placeholder_response_pressure | show_with_warning | evidence_requirement, legal_policy_review, schedule_authority_review | True | True | moderate_placeholder_response_pressure from deterministic placeholder scoring; Base pressure comes from declared placeholder pressure `low`. |
| offshore_automation_service_routing | Offshore automation-as-a-service routing | logistics_warehousing | offshore_automation_service_routing | cross_border | OFFSHORE_AUTOMATION_SERVICE, RELATED_PARTY_AI_SERVICE_FEES | critical_review_required | external_review_required | legal_policy_review, offshore_attribution_review, transfer_pricing_review | True | True | critical_review_required from deterministic placeholder scoring; Base pressure comes from declared placeholder pressure `high`. |
| open_source_ai_treatment_gap | Open-source AI treatment gap | software_digital_platforms | open_source_ai_treatment_gap | calibration_suppressed | OPEN_SOURCE_AI_TREATMENT_GAP | high_placeholder_response_pressure | suppress_until_calibrated | capital_base_review, external_calibration_required, legal_policy_review | True | True | Suppressed until calibration because required dependencies are unresolved. |
| platform_ip_royalty_routing | Platform IP royalty routing | software_digital_platforms | platform_ip_royalty_routing | unresolved_legal_treatment | ARTIFICIAL_LOW_PROFIT_OR_AAVA, OFFSHORE_AUTOMATION_SERVICE, RELATED_PARTY_AI_SERVICE_FEES | critical_review_required | external_review_required | capital_base_review, legal_policy_review, offshore_attribution_review, transfer_pricing_review | True | True | critical_review_required from deterministic placeholder scoring; Base pressure comes from declared placeholder pressure `critical`. |
| related_party_ai_service_fee_routing | Related-party AI service fee routing | accounting_administration | related_party_ai_service_fees | multi_pathway | ARTIFICIAL_LOW_PROFIT_OR_AAVA, RELATED_PARTY_AI_SERVICE_FEES | critical_review_required | external_review_required | aava_deductibility_review, evidence_requirement, transfer_pricing_review | True | True | critical_review_required from deterministic placeholder scoring; Base pressure comes from declared placeholder pressure `high`. |
| robotics_lease_substitution | Robotics lease substitution for capital ownership | automotive_repair | robotics_leasing_shift | multi_pathway | ROBOTICS_LEASING_AVOIDANCE | moderate_placeholder_response_pressure | show_with_warning | aava_deductibility_review, capital_base_review, evidence_requirement | True | True | moderate_placeholder_response_pressure from deterministic placeholder scoring; Base pressure comes from declared placeholder pressure `low`. |
| schedule_classification_arbitrage | Schedule classification arbitrage | retail_self_checkout_fulfilment | schedule_classification_arbitrage | multi_pathway | SECTOR_CLASSIFICATION_ARBITRAGE | critical_review_required | external_review_required | legal_policy_review, schedule_authority_review | True | True | critical_review_required from deterministic placeholder scoring; Base pressure comes from declared placeholder pressure `moderate`. |
| token_oversight_workforce_wrapper | Token oversight workforce wrapper | call_centres_customer_support | token_human_oversight | single_pathway | FAKE_QLC_INFLATION, TOKEN_HUMAN_OVERSIGHT | high_placeholder_response_pressure | strong_warning_required | evidence_requirement, grouped_entity_review, legal_policy_review | True | True | high_placeholder_response_pressure from deterministic placeholder scoring; Base pressure comes from declared placeholder pressure `high`. |

## F. Response Pressure Bands

### Scenarios By Pressure Band

- `critical_review_required`: 6
- `high_placeholder_response_pressure`: 4
- `moderate_placeholder_response_pressure`: 2

## G. Linked Avoidance Flags

- `ARTIFICIAL_LOW_PROFIT_OR_AAVA`: artificial_low_aava_cost_loading, cloud_inference_operating_cost_relabelling, platform_ip_royalty_routing, related_party_ai_service_fee_routing
- `CLOUD_COST_RELABELING`: cloud_inference_operating_cost_relabelling
- `FAKE_QLC_INFLATION`: fake_qlc_concentrated_roles, token_oversight_workforce_wrapper
- `OFFSHORE_AUTOMATION_SERVICE`: offshore_automation_service_routing, platform_ip_royalty_routing
- `OPEN_SOURCE_AI_TREATMENT_GAP`: open_source_ai_treatment_gap
- `RELATED_PARTY_AI_SERVICE_FEES`: artificial_low_aava_cost_loading, offshore_automation_service_routing, platform_ip_royalty_routing, related_party_ai_service_fee_routing
- `ROBOTICS_LEASING_AVOIDANCE`: robotics_lease_substitution
- `SECTOR_CLASSIFICATION_ARBITRAGE`: customer_self_checkout_labour_relabelling, mixed_unit_apportionment_gaming, schedule_classification_arbitrage
- `TOKEN_HUMAN_OVERSIGHT`: fake_qlc_concentrated_roles, token_oversight_workforce_wrapper

## H. Countermeasure / Review Pathways

- `aava_deductibility_review`: artificial_low_aava_cost_loading, cloud_inference_operating_cost_relabelling, related_party_ai_service_fee_routing, robotics_lease_substitution
- `capital_base_review`: open_source_ai_treatment_gap, platform_ip_royalty_routing, robotics_lease_substitution
- `customer_self_service_review`: customer_self_checkout_labour_relabelling
- `evidence_requirement`: cloud_inference_operating_cost_relabelling, fake_qlc_concentrated_roles, mixed_unit_apportionment_gaming, related_party_ai_service_fee_routing, robotics_lease_substitution, token_oversight_workforce_wrapper
- `external_calibration_required`: open_source_ai_treatment_gap
- `grouped_entity_review`: artificial_low_aava_cost_loading, fake_qlc_concentrated_roles, token_oversight_workforce_wrapper
- `legal_policy_review`: customer_self_checkout_labour_relabelling, mixed_unit_apportionment_gaming, offshore_automation_service_routing, open_source_ai_treatment_gap, platform_ip_royalty_routing, schedule_classification_arbitrage, token_oversight_workforce_wrapper
- `offshore_attribution_review`: offshore_automation_service_routing, platform_ip_royalty_routing
- `schedule_authority_review`: customer_self_checkout_labour_relabelling, mixed_unit_apportionment_gaming, schedule_classification_arbitrage
- `transfer_pricing_review`: artificial_low_aava_cost_loading, cloud_inference_operating_cost_relabelling, offshore_automation_service_routing, platform_ip_royalty_routing, related_party_ai_service_fee_routing

## I. Sector Schedule Exposure Notes

- `artificial_low_aava_cost_loading` uses `accounting_administration` as a synthetic schedule context only.
- `cloud_inference_operating_cost_relabelling` uses `software_digital_platforms` as a synthetic schedule context only.
- `customer_self_checkout_labour_relabelling` uses `retail_self_checkout_fulfilment` as a synthetic schedule context only.
- `fake_qlc_concentrated_roles` uses `call_centres_customer_support` as a synthetic schedule context only.
- `mixed_unit_apportionment_gaming` uses `logistics_warehousing` as a synthetic schedule context only.
- `offshore_automation_service_routing` uses `logistics_warehousing` as a synthetic schedule context only.
- `open_source_ai_treatment_gap` uses `software_digital_platforms` as a synthetic schedule context only.
- `platform_ip_royalty_routing` uses `software_digital_platforms` as a synthetic schedule context only.
- `related_party_ai_service_fee_routing` uses `accounting_administration` as a synthetic schedule context only.
- `robotics_lease_substitution` uses `automotive_repair` as a synthetic schedule context only.
- `schedule_classification_arbitrage` uses `retail_self_checkout_fulfilment` as a synthetic schedule context only.
- `token_oversight_workforce_wrapper` uses `call_centres_customer_support` as a synthetic schedule context only.

## J. Suppressed / External-Review Scenarios

- `external_review_required`: artificial_low_aava_cost_loading, cloud_inference_operating_cost_relabelling, offshore_automation_service_routing, platform_ip_royalty_routing, related_party_ai_service_fee_routing, schedule_classification_arbitrage
- `show_with_warning`: mixed_unit_apportionment_gaming, robotics_lease_substitution
- `strong_warning_required`: customer_self_checkout_labour_relabelling, fake_qlc_concentrated_roles, token_oversight_workforce_wrapper
- `suppress_until_calibrated`: open_source_ai_treatment_gap

## K. Calibration and Behavioural Research Blockers

- artificial_low_aava_cost_loading: transfer_pricing_review: external review required before operational use
- cloud_inference_operating_cost_relabelling: transfer_pricing_review: external review required before operational use
- customer_self_checkout_labour_relabelling: legal_policy_review: external review required before operational use
- mixed_unit_apportionment_gaming: legal_policy_review: external review required before operational use
- offshore_automation_service_routing: legal_policy_review: external review required before operational use
- offshore_automation_service_routing: offshore_attribution_review: external review required before operational use
- offshore_automation_service_routing: transfer_pricing_review: external review required before operational use
- open_source_ai_treatment_gap: capital_base_review: external review required before operational use
- open_source_ai_treatment_gap: external_calibration_required: external review required before operational use
- open_source_ai_treatment_gap: legal_policy_review: external review required before operational use
- open_source_ai_treatment_gap: open-source AI treatment requires legal, tax, accounting, Treasury, and Schedules Authority review
- platform_ip_royalty_routing: capital_base_review: external review required before operational use
- platform_ip_royalty_routing: legal_policy_review: external review required before operational use
- platform_ip_royalty_routing: offshore_attribution_review: external review required before operational use
- platform_ip_royalty_routing: transfer_pricing_review: external review required before operational use
- related_party_ai_service_fee_routing: transfer_pricing_review: external review required before operational use
- robotics_lease_substitution: capital_base_review: external review required before operational use
- schedule_classification_arbitrage: legal_policy_review: external review required before operational use
- token_oversight_workforce_wrapper: legal_policy_review: external review required before operational use

## L. Plain-English Interpretation

- Higher pressure bands indicate stronger prototype review pressure, not observed conduct.
- Linked avoidance flags identify which existing prototype review checks a pathway touches.
- Countermeasure categories show where evidence, grouping, transfer-pricing, schedule, AAVA, capital-base, offshore-attribution, or legal-policy review would be needed.
- Suppressed scenarios are not ready for point-estimate presentation until calibration dependencies are resolved.

## M. Limitations and Future Review Needs

### Scenarios By Response Type

- `artificial_low_profit_or_aava`: 1
- `cloud_inference_relabelling`: 1
- `customer_self_service_shift`: 1
- `fake_qlc_inflation`: 1
- `mixed_unit_apportionment_gaming`: 1
- `offshore_automation_service_routing`: 1
- `open_source_ai_treatment_gap`: 1
- `platform_ip_royalty_routing`: 1
- `related_party_ai_service_fees`: 1
- `robotics_leasing_shift`: 1
- `schedule_classification_arbitrage`: 1
- `token_human_oversight`: 1

### Scenarios By Review Status

- `external_review_required`: 6
- `show_with_warning`: 2
- `strong_warning_required`: 3
- `suppress_until_calibrated`: 1

- Total scenarios: 12
- Scenarios requiring external review: 12
- Scenarios requiring transfer-pricing review: 5
- Scenarios requiring grouped-entity review: 3
- Scenarios requiring schedule-authority review: 3
- Scenarios requiring AAVA deductibility review: 4
- Scenarios requiring capital-base review: 3
- Scenarios requiring offshore-attribution review: 2
- Scenarios requiring customer-self-service review: 1
- Scenarios suppress_until_calibrated: 1
- Firm-level liability logic modified: False
- Prototype only.
- Placeholder only.
- Synthetic scenarios only.
- Deterministic scenario review only.
- Does not predict conduct or estimate behavioural elasticity.
- Not ATO audit logic, Treasury modelling, ABS/ATO/DSS/PBO analysis, compliance-risk scoring, legal advice, tax advice, investment advice, enforcement, or penalty modelling.
- No firm-level, taxpayer-level, or industry data is used.
- Not usable to estimate actual tax payable.
