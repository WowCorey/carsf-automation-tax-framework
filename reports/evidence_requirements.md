# CARSF V1.5 Evidence Requirements Report

Generated at: `2026-05-13T10:04:04+00:00`

## A. Purpose

This report defines prototype evidence requirements for model inputs, review flags, transfer-pricing previews, mixed-unit handling, and future calibration.

## B. Non-Claims

- This is a prototype evidence assessment only. It is not legal, tax, Treasury, ATO, evidentiary, forensic, or audit validation.
- It does not validate liability, evidence sufficiency for real enforcement, or calibration.

## C. Evidence Requirement Table

| Requirement | Category | Field | Minimum Confidence | Required For | Legal Sensitivity | Privacy Sensitivity |
| --- | --- | --- | --- | --- | --- | --- |
| core_output_value | core_formula | output.value | medium | core_formula, mixed_units | medium | medium |
| core_output_unit | core_formula | output.unit | medium | core_formula, mixed_units | medium | medium |
| core_opfte_libc | core_formula | schedule.opfte_libc_placeholder | medium | core_formula, calibration | high | low |
| core_worker_hours | core_formula | workers.annual_hours | medium | core_formula, safe_harbour | medium | high |
| core_wage_quality | core_formula | workers.wage_quality | medium | core_formula, safe_harbour | medium | high |
| core_job_security | core_formula | workers.job_security | medium | core_formula, safe_harbour | medium | high |
| core_skill_development | core_formula | workers.skill_development | medium | core_formula, safe_harbour | medium | high |
| core_australian_nexus | core_formula | workers.australian_nexus | medium | core_formula, grouping | high | high |
| core_aii_components | core_formula | automation_components | medium | core_formula, avoidance | medium | medium |
| core_aava_revenue_costs | core_formula | aava_inputs | medium | core_formula, transfer_pricing | high | medium |
| core_frv | core_formula | schedule.frv | medium | core_formula, calibration | high | medium |
| core_capital_base | core_formula | capital_base | medium | core_formula, transfer_pricing | medium | medium |
| core_rates | core_formula | caps.uplift_rate/rent_tax_rate | medium | core_formula, calibration | high | low |
| core_credits | core_formula | credits | medium | core_formula, safe_harbour | medium | medium |
| safe_harbour_revenue | safe_harbour | safe_harbours.revenue_threshold | medium | safe_harbour | medium | medium |
| safe_harbour_worker_assist | safe_harbour | risk_metadata.worker_assist_admin_ai | medium | safe_harbour, avoidance | medium | medium |
| safe_harbour_low_nltg | safe_harbour | outputs.nltg | medium | safe_harbour | medium | medium |
| safe_harbour_startup | safe_harbour | risk_metadata.startup_placeholder | medium | safe_harbour, grouping | medium | medium |
| safe_harbour_essential_service | safe_harbour | risk_metadata.essential_service_review | medium | safe_harbour | medium | medium |
| avoid_token_oversight | avoidance | risk_metadata.token_human_oversight_risk | medium | avoidance | medium | medium |
| avoid_fake_qlc | avoidance | risk_metadata.fake_qlc_inflation_risk | medium | avoidance | medium | medium |
| avoid_offshore_ai | avoidance | risk_metadata.offshore_automation_service | medium | avoidance, transfer_pricing | high | medium |
| avoid_related_party_fees | avoidance | risk_metadata.related_party_ai_service_fees | medium | avoidance, transfer_pricing | high | medium |
| avoid_cloud_relabelling | avoidance | risk_metadata.cloud_cost_relabeling_risk | medium | avoidance, transfer_pricing | medium | medium |
| avoid_robotics_leasing | avoidance | risk_metadata.robotics_leasing_risk | medium | avoidance, transfer_pricing | medium | medium |
| avoid_entity_splitting | avoidance | risk_metadata.entity_splitting_risk | medium | avoidance, grouping | high | medium |
| avoid_sector_classification | avoidance | risk_metadata.sector_classification_risk | medium | avoidance, mixed_units | medium | medium |
| group_common_control | grouping | group.common_ownership_control | medium | grouping | high | medium |
| group_ip_owner | grouping | entities.role.platform_ip_owner | medium | grouping, transfer_pricing | high | medium |
| group_service_provider | grouping | entities.role.service_provider | medium | grouping | medium | medium |
| group_customer_facing | grouping | entities.role.customer_facing | medium | grouping | medium | medium |
| group_employer | grouping | entities.role.australian_employer | medium | grouping | medium | high |
| group_offshore_provider | grouping | entities.role.offshore_service_provider | medium | grouping, transfer_pricing | high | medium |
| tp_related_party_agreements | transfer_pricing | related_party_transactions.agreements | medium | transfer_pricing | high | medium |
| tp_service_fee_invoices | transfer_pricing | related_party_transactions.service_fees | medium | transfer_pricing | medium | medium |
| tp_royalty_licence | transfer_pricing | related_party_transactions.royalties | medium | transfer_pricing | high | medium |
| tp_cost_sharing | transfer_pricing | related_party_transactions.cost_sharing | medium | transfer_pricing | medium | medium |
| tp_cloud_inference | transfer_pricing | related_party_transactions.cloud_inference | medium | transfer_pricing | medium | medium |
| tp_robotics_leasing | transfer_pricing | related_party_transactions.robotics_leasing | medium | transfer_pricing | medium | medium |
| tp_data_model_access | transfer_pricing | related_party_transactions.data_model_access | medium | transfer_pricing | medium | medium |
| tp_management_technical | transfer_pricing | related_party_transactions.management_service | medium | transfer_pricing | medium | medium |
| mixed_unit_evidence | mixed_units | canonical_output_unit | medium | mixed_units | medium | medium |
| mixed_conversion_metadata | mixed_units | conversion_metadata | medium | mixed_units | high | medium |
| mixed_activity_shares | mixed_units | apportionment.activities.share | medium | mixed_units | medium | medium |
| mixed_revenue_aava_basis | mixed_units | revenue_or_aava_share_basis | medium | mixed_units | medium | medium |
| mixed_schedule_classification | mixed_units | schedule_id | medium | mixed_units | high | medium |

## D. Missing Evidence by Model Component

| Component | Missing Requirements |
| --- | ---: |
| Mechanic Traditional | 33 |
| Mechanic Ai Admin | 33 |
| Mechanic Robotic | 33 |
| Logistics Human Heavy | 33 |
| Logistics Hybrid | 33 |
| Logistics Ai Platform | 33 |
| Grouped-entity preview | 28 |
| Transfer-pricing preview | 24 |

## E. Example-Level Evidence Status Summary

| Example | Status | Missing Requirements | Review Required |
| --- | --- | ---: | --- |
| Mechanic Traditional | placeholder_only | 33 | true |
| Mechanic Ai Admin | placeholder_only | 33 | true |
| Mechanic Robotic | placeholder_only | 33 | true |
| Logistics Human Heavy | placeholder_only | 33 | true |
| Logistics Hybrid | placeholder_only | 33 | true |
| Logistics Ai Platform | placeholder_only | 33 | true |

## F. Group/Transfer-Pricing Evidence Status Summary

| Report | Status | Missing Requirements | Decision-Log Entries |
| --- | --- | ---: | ---: |
| Grouped entity preview | placeholder_only | 28 | 4 |
| Transfer-pricing preview | placeholder_only | 24 | 3 |

## G. High-Sensitivity Evidence Categories

- avoidance
- core_formula
- grouping
- mixed_units
- transfer_pricing

## H. Calibration Dependencies

- OPFTE_LIBC, FRV, QLC weights, AII weights, AAVA deductibility, caps, safe-harbour thresholds, avoidance thresholds, transfer-pricing review shares, mixed-unit weighting, and labour-market modules remain uncalibrated.
- Required source categories include ABS, ATO, PBO, DSS, Fair Work, HILDA, HELP/HECS, superannuation, state payroll tax, industry productivity, business survey, Treasury modelling, and independent legal/tax review.

## I. Future Review Needs

- Legal, tax, privacy, economic, Treasury/ATO-style, and sector-specific review before any external use.

## J. Controlled Mock Evidence Workflow

Synthetic mock evidence packets can be generated and reviewed with `python scripts/run_evidence_workflow.py`.

- Markdown report: `reports/mock_evidence_workflow.md`
- JSON report: `reports/mock_evidence_workflow.json`
- Mock evidence can support prototype workflow testing only; it cannot create real-world sufficiency.
