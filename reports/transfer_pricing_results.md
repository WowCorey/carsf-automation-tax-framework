# CARSF V1.5 Transfer-Pricing and Mixed-Unit Preview Results

Generated at: `2026-05-18T11:03:51+00:00`

Version: CARSF V1.5 prototype

Status: `illustrative_transfer_pricing_and_mixed_unit_previews_only`

These outputs are prototype review previews only. They are not transfer-pricing adjustments, ATO findings, legal findings, Treasury guidance, OECD/BEPS analysis, or economic validation.

Evidence status: `placeholder_only`. Decision-log entries: `3`.

## A. Purpose and Non-Claims

This report adds non-operative review previews for related-party automation charges, adjusted AAVA review candidates, and mixed-unit output handling. It does not change the reported-AAVA pathway or any existing final liability calculation.

- Not transfer-pricing adjustments.
- Not ATO findings.
- Not legal findings.
- Not Treasury guidance.
- Not OECD/BEPS analysis.
- Not economic validation.
- Not real tax assessments.
- Adjusted AAVA is preview-only and does not replace reported AAVA.
- Value-weighted exposure index is not a tax base.

## B. Why Related-Party / Offshore Fees Matter

AAVA can be suppressed in a prototype scenario where automated Australian-facing output is paired with offshore AI service fees, IP royalties, platform licences, cloud/inference relabelling, or robotics leasing charges. The preview only identifies review candidates and illustrative addback amounts.

## C. Related-Party AI Fee Example

### Related-party offshore AI service fee structure

Show a non-operative review preview where offshore AI service fees and platform licences may suppress reported AAVA.

| Metric | Value |
| --- | ---: |
| Reported AAVA | 260,000.00 |
| Preview adjustments total | 1,107,000.00 |
| Adjusted AAVA preview | 1,367,000.00 |
| Original final liability | 70,200.00 |
| Adjusted-AAVA liability preview | 369,090.00 |
| Liability preview difference | 298,890.00 |
| Risk level | high |
| Review required | true |

Adjustment candidates:

| Transaction | Type | Amount | Review Share | Preview Addback | Confidence | Reason |
| --- | --- | ---: | ---: | ---: | --- | --- |
| offshore_ai_dispatch_fee | OFFSHORE_AI_SERVICE_FEE | 900,000.00 | 0.75 | 675,000.00 | high | Offshore AI service fee may suppress reported AAVA where automated capacity serves Australian output. |
| platform_ip_royalty | IP_ROYALTY_OR_PLATFORM_LICENSE | 520,000.00 | 0.60 | 312,000.00 | medium | IP or platform licence fee may extract automated value through a related counterparty. |
| relabelled_cloud_inference_cost | CLOUD_INFERENCE_RELABELLED_AS_ORDINARY_COST | 240,000.00 | 0.50 | 120,000.00 | medium | Cloud or inference costs may be relabelled as ordinary non-automation inputs. |

Warnings and non-claims:

- This is a non-operative transfer-pricing / related-party review preview only. It is not a legal, tax, ATO, Treasury, OECD, BEPS, or economic finding.
- Adjusted AAVA is preview-only and does not mutate reported AAVA.
- Adjusted-AAVA liability is non-operative preview only.
- Adjusted AAVA is preview-only and does not replace reported AAVA.
- No arm's-length price, transfer-pricing adjustment, tax assessment, or legal conclusion is calculated.

Limitations:

- This is not a transfer-pricing adjustment.
- This is not an ATO, Treasury, OECD, BEPS, legal, tax, or economic finding.
- No arm's-length price or real deductibility conclusion is calculated.

## D. Reported AAVA vs Adjusted AAVA Preview

| Scenario | Reported AAVA | Preview Adjustments | Adjusted AAVA Preview | Original Liability | Adjusted-AAVA Liability Preview |
| --- | ---: | ---: | ---: | ---: | ---: |
| Related-party offshore AI service fee structure | 260,000.00 | 1,107,000.00 | 1,367,000.00 | 70,200.00 | 369,090.00 |
| Related-party robotics leasing structure | 140,000.00 | 506,000.00 | 646,000.00 | 35,000.00 | 161,500.00 |

## E. Adjustment Candidate Table

| Scenario | Transaction | Type | Amount | Preview Addback | Confidence |
| --- | --- | --- | ---: | ---: | --- |
| Related-party offshore AI service fee structure | offshore_ai_dispatch_fee | OFFSHORE_AI_SERVICE_FEE | 900,000.00 | 675,000.00 | high |
| Related-party offshore AI service fee structure | platform_ip_royalty | IP_ROYALTY_OR_PLATFORM_LICENSE | 520,000.00 | 312,000.00 | medium |
| Related-party offshore AI service fee structure | relabelled_cloud_inference_cost | CLOUD_INFERENCE_RELABELLED_AS_ORDINARY_COST | 240,000.00 | 120,000.00 | medium |
| Related-party robotics leasing structure | robotics_lease_fee | ROBOTICS_LEASE_OR_SERVICE_CONTRACT | 620,000.00 | 434,000.00 | high |
| Related-party robotics leasing structure | technical_support_fee | MANAGEMENT_OR_TECHNICAL_SERVICE_FEE | 180,000.00 | 72,000.00 | medium |

## F. Robotics Leasing Example

### Related-party robotics leasing structure

Show a non-operative review preview where a robotics-heavy firm leases automation assets from a related offshore or finance entity.

| Metric | Value |
| --- | ---: |
| Reported AAVA | 140,000.00 |
| Preview adjustments total | 506,000.00 |
| Adjusted AAVA preview | 646,000.00 |
| Original final liability | 35,000.00 |
| Adjusted-AAVA liability preview | 161,500.00 |
| Liability preview difference | 126,500.00 |
| Risk level | high |
| Review required | true |

Adjustment candidates:

| Transaction | Type | Amount | Review Share | Preview Addback | Confidence | Reason |
| --- | --- | ---: | ---: | ---: | --- | --- |
| robotics_lease_fee | ROBOTICS_LEASE_OR_SERVICE_CONTRACT | 620,000.00 | 0.70 | 434,000.00 | high | Robotics lease or service contract may keep capital base low while shifting automation costs. |
| technical_support_fee | MANAGEMENT_OR_TECHNICAL_SERVICE_FEE | 180,000.00 | 0.40 | 72,000.00 | medium | Related-party automation-linked charge requires AAVA deductibility and transfer-pricing review. |

Warnings and non-claims:

- This is a non-operative transfer-pricing / related-party review preview only. It is not a legal, tax, ATO, Treasury, OECD, BEPS, or economic finding.
- Adjusted AAVA is preview-only and does not mutate reported AAVA.
- Adjusted-AAVA liability is non-operative preview only.
- Adjusted AAVA is preview-only and does not replace reported AAVA.
- No arm's-length price, transfer-pricing adjustment, tax assessment, or legal conclusion is calculated.

Limitations:

- This is not a lease classification finding.
- This is not a transfer-pricing adjustment or tax assessment.
- Capital allowance, depreciation, GST, and legal ownership rules are not modelled.

## G. Mixed-Unit Platform Group

Show that output and HLE cannot be directly aggregated when canonical output units differ.

| Entity | Schedule | Canonical Output Unit | Revenue | AAVA | Standalone Liability | Risk |
| --- | --- | --- | ---: | ---: | ---: | --- |
| logistics_operations | logistics_warehousing | tonne_kilometres_or_pallet_movements | 2,600,000.00 | 700,000.00 | 85,000.00 | medium |
| digital_dispatch_platform | digital_platform_services_placeholder | automated_decisions_or_accounts_served | 1,700,000.00 | 950,000.00 | 120,000.00 | high |
| repair_admin_support | automotive_repair | book_hour_equivalent_jobs_completed | 500,000.00 | 160,000.00 | 0.00 | low |

## H. Mixed-Unit Compatibility Result

- Compatible: false
- Units: automated_decisions_or_accounts_served, book_hour_equivalent_jobs_completed, tonne_kilometres_or_pallet_movements
- Comparable unit: N/A
- Reason: Canonical output units differ; direct output/HLE aggregation is prohibited.
- Review required: true

- Mixed-unit compatibility is a prototype review check only.
- Output and HLE aggregation are prohibited while canonical output units differ.

## I. Value-Weighted Exposure Index Explanation

Where units differ, the prototype prohibits direct output and HLE aggregation. It can still show standalone liability sum, schedule-level comparison, and a value-weighted exposure index. That index is not a tax base and is not a replacement for calibrated sector schedules.

| Metric | Value |
| --- | ---: |
| Method | mixed_units_no_direct_output_or_hle_aggregation |
| Standalone liability sum | 205,000.00 |
| Value-weighted exposure index | 0.6144 |
| Review required | true |

- Mixed-unit compatibility is a prototype review check only.
- Output and HLE aggregation are prohibited while canonical output units differ.
- Value-weighted exposure index is prototype-only, not a tax base, and not a replacement for sector schedules.
- Standalone liability summation and schedule-level comparison are allowed; direct output/HLE aggregation is not.
- Mixed-unit exposure outputs are prototype-only and are not a tax base.
- Value-weighted exposure index is not a replacement for sector schedules.
- No legal, tax, ATO, Treasury, OECD, BEPS, or economic validation is implied.

## J. Limitations and Required Legal/Tax Review

Evidence and decision-log summary:

- Evidence status: placeholder_only
- Missing evidence requirements: 24
- Decision-log steps: evidence_assessment, transfer_pricing_preview, mixed_unit_handling

- Value-weighted exposure index is not a tax base.
- Direct output and HLE aggregation are prohibited until units are compatible or a reviewed conversion method exists.
- Digital platform services schedule is a placeholder need, not a calibrated schedule.
- These outputs are prototype review previews only. They are not transfer-pricing adjustments, ATO findings, legal findings, Treasury guidance, OECD/BEPS analysis, or economic validation.
