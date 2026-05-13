# Appendix D - AAVA Deductibility Taxonomy

Status: V1.5 prototype measurement appendix.

This appendix is a drafting aid only. It is not legislation, legal advice, tax advice, Treasury advice, ATO guidance, or a calibrated deductibility schedule. All treatments below are placeholder policy positions for testing the model and identifying unresolved measurement questions.

## Purpose

Australian Automated Value Added (AAVA) is intended to measure Australian-attributable value added by automated productive capacity:

```text
AAVA = AustralianAttributableRevenue
     - VerifiedNonAutomationInputCosts
     - VerifiedQLC_WageCost
```

The hard implementation problem is deciding which costs are verified non-automation inputs, which wages are already recognised through QLC, and which automation costs should be capital-base or rent-levy inputs instead of ordinary AAVA deductions.

## Evidence Labels

Every schedule value or firm input should be labelled as one of:

- confirmed_baseline: sourced from official data or audited firm records.
- illustrative_assumption: used only for scenario testing.
- placeholder_policy: provisional policy treatment requiring review.
- future_research: unresolved and not safe for external claims.

## Initial Deductibility Taxonomy

| Cost category | Prototype AAVA treatment | Evidence label | V1.5 rationale | Open issue |
| --- | --- | --- | --- | --- |
| Human wages counted in QLC | Deduct as `VerifiedQLC_WageCost` only where the worker is included in QLC and Australian nexus is verified. | placeholder_policy | Prevents double-counting by recognising qualifying human labour before assessing automated value. | Needs payroll, contractor, related-party labour, and award-classification rules. |
| Ordinary rent/utilities | Generally deductible as verified non-automation input costs where not directly part of automated productive capacity. | placeholder_policy | Ordinary premises and utilities are not automation rent by themselves. | High-energy data-centre or robotics utilities may need allocation rules. |
| AI cloud inference | Not automatically deductible as ordinary non-automation input. Allocate between automation operating cost, capital-base proxy, and related-party service where applicable. | future_research | Inference spend may be the core automated productive capacity rather than a neutral input. | Requires cloud invoice taxonomy, compute attribution, and transfer-pricing review. |
| AI licensing | Not automatically deductible as ordinary non-automation input. Treat as automation service, intangible access, or capital-base proxy depending on schedule rules. | future_research | Licence fees can substitute for owning automation capital. | Needs domestic/offshore, related-party, and open-source treatment. |
| Robotics depreciation | Not deducted as an ordinary non-automation input where robotics is the automated productive capacity. Consider in CapitalBase for PRRT-inspired uplift logic. | placeholder_policy | Avoids deducting the same automated capital from AAVA while also using it to calculate normal return. | Needs alignment with tax depreciation and AASB asset treatment. |
| Related-party service charges | Deduct only after enhanced verification and arm's-length attribution. Disallow or adjust where dominant purpose is reducing AAVA. | placeholder_policy | Related-party fees are a primary avoidance vector. | Needs transfer-pricing, diverted profits tax, and significant global entity alignment. |
| Platform fees | Split between ordinary market-access fees and automation service fees where evidence supports allocation. | future_research | Platform fees may embed automated dispatch, pricing, matching, or fulfilment capacity. | Needs schedule-specific allocation and audit evidence. |
| Human training | Potentially deductible or creditable where tied to verified Australian worker training, transition, apprenticeships, or skill development. | placeholder_policy | Training supports QLC and transition objectives. | Must prevent relabelling ordinary onboarding as transition credit. |
| Offshore AI services | Not deductible merely because invoiced offshore. Attribute Australian-facing automated value by destination and activity. | placeholder_policy | Prevents imported automation-as-a-service from eroding AAVA. | Requires treaty, transfer-pricing, and trade-law review. |

## Minimum Audit Trail

Firms should retain, at minimum:

- audited revenue attribution by Australian destination and activity;
- payroll records linking QLC workers to wage-cost deductions;
- invoices and contracts separating human services, ordinary inputs, AI services, cloud inference, robotics, and platform fees;
- related-party service agreements and transfer-pricing support;
- offshore service descriptions identifying whether automated productive capacity served Australian output;
- capital-base schedules for robotics, software, compute, recognised intangibles, and imputed intangibles;
- credit evidence for training, transition, apprenticeships, and verified worker support.

## Explicit Non-Claims

This appendix does not validate any real deduction, credit, liability, or tax position. It identifies measurement choices that require Treasury, ATO, legal, accounting, and economic review before external use.
