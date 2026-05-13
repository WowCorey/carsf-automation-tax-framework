# CARSF V1.5 Grouped-Entity and Apportionment Results

Generated at: `2026-05-13T10:14:35+00:00`

Version: CARSF V1.5 prototype

Status: `illustrative_grouped_entity_and_apportionment_previews_only`

These outputs are prototype review previews only. They are not legal grouping findings, tax assessments, Treasury guidance, ATO guidance, or economic validation.

## A. Grouped-Entity Aggregation Overview

This report shows non-operative modelling previews for related-entity aggregation, mixed-activity apportionment, and a hybrid logistics stress case. It does not alter any final liability calculation in the single-entity examples.

Evidence status: `placeholder_only`. Decision-log entries: `4`.

Related-party and mixed-unit previews are generated in `reports/transfer_pricing_results.md` and `reports/transfer_pricing_results.json`.

## B. Why Grouping Matters

A split structure can make each standalone entity look lower-risk while the economic group still contains high automated output, thin Australian QLC, offshore automation services, and related-party fee paths. The preview aggregates only where output units are comparable and flags review where they are not.

| Example | Standalone Risk | Group Risk | Aggregation Needed | Apportionment Needed | Main Reason |
| --- | --- | --- | --- | --- | --- |
| Split AI logistics platform structure | low | high | yes | no | Split entities share Australian-facing automated logistics output. |
| Mixed logistics, warehousing, platform dispatch, and customer support activity mix | N/A | low | no | yes | Mixed activities require schedule-share review rather than unreviewed single classification. |
| Logistics Hybrid Stress | medium | N/A | no | no | Stress variant tests non-zero but intermediate NLTG for hybrid automation. |

## C. Split Logistics Structure Example

Show that standalone fragments may appear lower risk while the grouped preview raises review concern.

## D. Standalone Entity View

| Entity | Role | Standalone Risk | Revenue | Output | QLC | HLE | AII | NLTG | AAVA | Liability | Flags |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| au_customer_facing_entity | customer_facing_revenue_entity | low | 2,200,000.00 | 800,000.00 | 2.00 | 8.00 | 0.12 | 0.00 | 700,000.00 | 0.00 | none |
| offshore_ai_service_provider | offshore_automation_service_provider | low | 3,500,000.00 | 2,400,000.00 | 0.10 | 24.00 | 0.86 | 20.54 | 1,700,000.00 | 0.00 | OFFSHORE_AUTOMATION_SERVICE, RELATED_PARTY_AI_SERVICE_FEES |
| platform_ip_owner | platform_ip_owner | low | 1,900,000.00 | 600,000.00 | 0.20 | 6.00 | 0.80 | 4.60 | 950,000.00 | 0.00 | ENTITY_SPLITTING_PREVIEW, SECTOR_CLASSIFICATION_ARBITRAGE |
| small_au_employer_entity | australian_employing_entity | low | 900,000.00 | 200,000.00 | 1.10 | 2.00 | 0.10 | 0.00 | 350,000.00 | 0.00 | none |

## E. Aggregated Group Preview

| Metric | Value |
| --- | ---: |
| Entity count | 4 |
| Aggregate revenue | 8,500,000.00 |
| Aggregate output | 4,000,000.00 |
| Aggregate QLC | 3.40 |
| Aggregate HLE | 40.00 |
| Weighted AII | 0.67 |
| Aggregate NLTG preview | 23.20 |
| Aggregate AAVA | 3,700,000.00 |
| Standalone entity liability sum | 0.00 |
| Group recomputed liability preview | 863,360.00 |
| Group risk | high |

## F. Difference Between Standalone and Group-Level Preview

- Standalone entity liability sum: 0.00
- Group recomputed liability preview: 863,360.00
- Difference: 863,360.00
- Aggregation flags: OFFSHORE_AUTOMATION_SERVICE, RELATED_PARTY_AI_SERVICE_FEES, ENTITY_SPLITTING_PREVIEW, SECTOR_CLASSIFICATION_ARBITRAGE

## G. Mixed-Activity / Prototype Apportionment Example

Show prototype apportionment by activity rather than forcing a mixed firm into a single unreviewed classification.

This example currently uses the combined logistics_warehousing prototype schedule for all activity slices. It tests apportionment plumbing and share-validation logic, not final cross-sector schedule blending. True multi-schedule blending requires additional calibrated sector schedules.

- Valid: true
- Review required: false

Weighted placeholder parameters:

- opfte_libc: 100000.000000
- frv_floor: 26000.000000
- frv_standard: 47000.000000
- frv_full: 90000.000000
- lambda_sector: 0.200000
- LAMBDA_sector: 0.270000
- theta: 0.600000
- qlc_max_multiplier: 1.250000
- aii_weights: {"auto_decision_ratio": 0.3, "auto_process_share": 0.3, "compute_ratio": 0.2, "robotics_capital_ratio": 0.2}

## H. Apportionment Basis Table

| Activity | Schedule | Share | Basis | Placeholder Basis |
| --- | --- | ---: | --- | --- |
| logistics_transport | logistics_warehousing | 0.60 | audited_placeholder_output_and_revenue_share | illustrative_placeholder_only; would require transport-management records and revenue attribution in a real schedule |
| warehousing | logistics_warehousing | 0.25 | audited_placeholder_pallet_movement_share | illustrative_placeholder_only; current prototype schedule combines logistics and warehousing until calibrated split exists |
| platform_dispatch | logistics_warehousing | 0.10 | audited_placeholder_platform_dispatch_share | illustrative_placeholder_only; platform dispatch remains inside Prototype Schedule B pending schedule split |
| customer_support_admin | logistics_warehousing | 0.05 | audited_placeholder_support_workshare | illustrative_placeholder_only; support/admin allocation requires policy review before any real use |

## I. Hybrid Logistics Stress Variant

Hybrid logistics operator with meaningful route automation and warehouse automation while retaining substantial Australian driving, dispatch, and warehouse labour.

| Metric | Value |
| --- | ---: |
| QLC | 8.75 |
| HLE | 30.00 |
| AII | 0.53 |
| NLTG | 7.15 |
| AAVA | 1,850,000.00 |
| Final liability preview | 256,050.00 |

Hybrid logistics stress variant: automation is meaningful and NLTG is non-zero, but the result remains below the thin-labour AI logistics platform because substantial Australian labour is still present.

## J. Limitations and Non-Claims

Evidence and decision-log summary:

- Evidence status: placeholder_only
- Missing evidence requirements: 28
- Decision-log steps: evidence_assessment, group_aggregation, apportionment, mixed_unit_handling

- Prototype grouped-entity preview only; no legal, tax, Treasury, or ATO validation is provided.
- This is not full tax-law grouping, transfer-pricing, or attribution logic.
- Prototype apportionment preview only; no legal, tax, Treasury, or ATO validation is provided.
- Illustrative placeholder output only.
- Do not use this result to estimate real tax payable.
- No legal, tax, Treasury, ATO, or economic validation is implied.
- Safe harbour and avoidance outputs are prototype review flags, not legal findings.
- Coverage metrics not calculated because this example has no national monitoring inputs.
- Evidence assessment is prototype-only and does not validate any liability, legal position, tax position, or audit finding.
- Evidence remains insufficient for real calibration, legal use, or actual tax-payable claims.
- Grouped aggregation is a prototype modelling preview only.
- Numbers are illustrative placeholders and are not Australian logistics, tax, or transfer-pricing data.
- Do not use this result as legal grouping, tax assessment, Treasury guidance, or ATO guidance.
- Apportionment is a prototype schedule-blending model only.
- It is not legal attribution, tax-law apportionment, Treasury guidance, or ATO guidance.
- All shares and weighted parameters are illustrative placeholders unless separately calibrated.
- Shares are illustrative placeholders and are not Australian industry data.
- Numbers are illustrative placeholders and are not Australian logistics data.
- Schedule values are not calibrated.
- AAVA deductibility remains a prototype taxonomy.
- Safe harbour, anti-avoidance, and grouping checks are executable review flags only.
- Safe harbour classification does not automatically reduce or erase liability in this build.
- Related-party, offshore, and sector-classification outputs are not legal or tax conclusions.
- These outputs are prototype review previews only. They are not legal grouping findings, tax assessments, Treasury guidance, ATO guidance, or economic validation.
