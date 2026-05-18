# CARSF V1.5 Controlled Mock Evidence Workflow

Generated at: `2026-05-18T09:37:04+00:00`

## A. Purpose

This report tests how synthetic evidence packets can be submitted, summarised, classified, and moved through prototype review states.

## B. Non-Claims

- These packets are synthetic mock evidence only. They do not validate any real liability, tax position, audit finding, legal conclusion, Treasury assessment, ATO assessment, or economic claim.
- Mock sufficiency is not legal, tax, Treasury, ATO, ABS, Fair Work, audit, forensic, or economic validation.
- No personal data, restricted government data, real taxpayer data, or real business evidence is included.

## C. Evidence Packet Summary Table

| Packet | Linked Example | Items | Sufficient | Partial | Missing | Low Confidence | Review State | Privacy | Secrecy |
| --- | --- | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| ai_logistics_platform_mock_packet | logistics_ai_platform | 7 | 5 | 2 | 0 | 2 | submitted_mock | high | confidential_placeholder |
| mechanic_ai_admin_mock_packet | mechanic_ai_admin | 8 | 7 | 1 | 0 | 1 | submitted_mock | high | confidential_placeholder |
| mechanic_robotic_review_packet | mechanic_robotic | 5 | 4 | 1 | 0 | 1 | submitted_mock | high | confidential_placeholder |
| mixed_unit_platform_mock_packet | mixed_unit_platform_group | 5 | 2 | 2 | 1 | 2 | submitted_mock | moderate | internal_research |

## D. Review-State Transitions

| Packet | Placeholder -> Submitted | Target State | Allowed | Approved State | Main Reason |
| --- | --- | --- | --- | --- | --- |
| ai_logistics_platform_mock_packet | submitted_mock | needs_privacy_review | true | needs_privacy_review | Manual review state is allowed as a prototype workflow flag. |
| mechanic_ai_admin_mock_packet | submitted_mock | needs_privacy_review | true | needs_privacy_review | Manual review state is allowed as a prototype workflow flag. |
| mechanic_robotic_review_packet | submitted_mock | needs_privacy_review | true | needs_privacy_review | Manual review state is allowed as a prototype workflow flag. |
| mixed_unit_platform_mock_packet | submitted_mock | needs_calibration | true | needs_calibration | Manual review state is allowed as a prototype workflow flag. |

## E. Privacy/Secrecy Classifications

| Packet | Privacy | Secrecy | Review Required | Review Flags |
| --- | --- | --- | --- | --- |
| ai_logistics_platform_mock_packet | high | confidential_placeholder | true | needs_legal_review, needs_privacy_review, needs_tax_review |
| mechanic_ai_admin_mock_packet | high | confidential_placeholder | true | needs_privacy_review |
| mechanic_robotic_review_packet | high | confidential_placeholder | true | needs_legal_review, needs_privacy_review, needs_tax_review |
| mixed_unit_platform_mock_packet | moderate | internal_research | false | needs_calibration |

## F. Example-by-Example Mock Evidence Outcomes

| Packet | Evidence Status | Missing Requirements | Low Confidence Items | Outcome Meaning |
| --- | --- | ---: | ---: | --- |
| ai_logistics_platform_mock_packet | partial | 31 | 2 | Prototype-only mock evidence has gaps. |
| mechanic_ai_admin_mock_packet | partial | 19 | 1 | Prototype-only mock evidence has gaps. |
| mechanic_robotic_review_packet | partial | 28 | 1 | Prototype-only mock evidence has gaps. |
| mixed_unit_platform_mock_packet | partial | 16 | 2 | Prototype-only mock evidence has gaps. |

## G. What Evidence Is Still Missing

### ai_logistics_platform_mock_packet
- `core_output_value`
- `core_output_unit`
- `core_opfte_libc`
- `core_worker_hours`
- `core_wage_quality`
- `core_job_security`
- `core_skill_development`
- `core_australian_nexus`
- `core_aii_components`
- `core_frv`
- `core_capital_base`
- `core_rates`
- `core_credits`
- `safe_harbour_worker_assist`
- `safe_harbour_startup`
- `avoid_token_oversight`
- `avoid_fake_qlc`
- `avoid_related_party_fees`
- `avoid_cloud_relabelling`
- `avoid_robotics_leasing`
- ... 11 more omitted for readability.

### mechanic_ai_admin_mock_packet
- `core_opfte_libc`
- `core_wage_quality`
- `core_job_security`
- `core_skill_development`
- `core_frv`
- `core_capital_base`
- `core_rates`
- `core_credits`
- `safe_harbour_revenue`
- `safe_harbour_startup`
- `safe_harbour_essential_service`
- `avoid_token_oversight`
- `avoid_fake_qlc`
- `avoid_offshore_ai`
- `avoid_related_party_fees`
- `avoid_cloud_relabelling`
- `avoid_robotics_leasing`
- `avoid_entity_splitting`
- `avoid_sector_classification`

### mechanic_robotic_review_packet
- `core_output_value`
- `core_output_unit`
- `core_opfte_libc`
- `core_wage_quality`
- `core_job_security`
- `core_skill_development`
- `core_australian_nexus`
- `core_frv`
- `core_capital_base`
- `core_rates`
- `core_credits`
- `safe_harbour_worker_assist`
- `avoid_fake_qlc`
- `avoid_offshore_ai`
- `avoid_related_party_fees`
- `avoid_cloud_relabelling`
- `avoid_robotics_leasing`
- `avoid_entity_splitting`
- `avoid_sector_classification`
- `group_ip_owner`
- ... 8 more omitted for readability.

### mixed_unit_platform_mock_packet
- `core_output_value`
- `core_output_unit`
- `core_opfte_libc`
- `core_australian_nexus`
- `core_frv`
- `core_rates`
- `safe_harbour_startup`
- `avoid_entity_splitting`
- `avoid_sector_classification`
- `group_common_control`
- `group_ip_owner`
- `group_service_provider`
- `group_customer_facing`
- `group_employer`
- `group_offshore_provider`
- `mixed_conversion_metadata`

## H. Legal/Tax/Privacy Review Triggers

| Packet | Triggers |
| --- | --- |
| ai_logistics_platform_mock_packet | needs_legal_review, needs_privacy_review, needs_tax_review |
| mechanic_ai_admin_mock_packet | needs_privacy_review |
| mechanic_robotic_review_packet | needs_legal_review, needs_privacy_review, needs_tax_review |
| mixed_unit_platform_mock_packet | needs_calibration |

## I. Why Mock Sufficiency Is Not Real Sufficiency

- The packets are deliberately synthetic and exist only to test workflow state changes.
- They do not contain audited source records, government data, personal data, restricted data, or final calibration values.
- A prototype status such as `partial` or `sufficient_for_prototype` is not a legal conclusion, tax position, audit finding, Treasury assessment, ATO assessment, or economic claim.

Status counts:

- `partial`: 4

## J. Secure Ingestion Controls

- Mock evidence is allowed only because it is synthetic.
- Non-synthetic evidence requires secure ingestion controls and external secure-system design.
- Real evidence, personal data, taxpayer data, business records, restricted government data, secrets, credentials, invoices, contracts, and employment records must not be committed to this repo.
- Run `python scripts/run_ingestion_controls.py` to generate `reports/secure_ingestion_controls.md` and `reports/secure_ingestion_controls.json`.
