# CARSF V1.5 Payment Interactions and Targeting Preview

Generated at: `2026-05-20T02:07:22+00:00`

## A. Purpose

This report previews how existing transfer baselines, targeting criteria, phase rules, payment stacks, double-counting prevention, and support fiscal incidence may interact in the CARSF transition-payment prototype.

## B. Non-Claims

- These are prototype payment-interaction outputs only. They are not UBI policy, welfare advice, eligibility law, Centrelink/DSS/Services Australia modelling, Treasury costing, PBO costing, legal advice, tax advice, or economic validation.
- All targeting, phase, household, and support-incidence values are illustrative placeholders.
- Support incidence offsets are not validated savings.
- Payment interaction outputs do not modify firm-level CARSF liability.

## C. Why Payment Interactions Matter

Transition funding should not double-count existing transfer support, imply final eligibility law, or treat placeholder fiscal offsets as savings. This layer keeps new transition-payment stack costs separate from existing baselines and shows review flags where targeting or household eligibility is unresolved.

## D. Existing Transfer Baseline Separation

| Example | Existing Eligible Population | Support Per Person | Admin Per Person | Existing Baseline Cost | New Stack Cost |
| --- | ---: | ---: | ---: | ---: | ---: |
| Displaced Worker Targeted Supplement | 300.00 | 1,000.00 | 100.00 | 330,000.00 | 4,000,000.00 |
| High Cliff-Risk Interaction Case | 2,500.00 | 3,500.00 | 250.00 | 9,375,000.00 | 47,000,000.00 |
| Household Eligibility Placeholder Review | 700.00 | 3,000.00 | 200.00 | 2,240,000.00 | 3,375,000.00 |
| Hybrid Stack Double-Counting Review | 1,200.00 | 2,500.00 | 150.00 | 3,180,000.00 | 10,400,000.00 |
| Retraining Income Phase-In | 400.00 | 1,200.00 | 150.00 | 540,000.00 | 2,750,000.00 |
| UBI-Lite With Existing Support Baseline | 3,000.00 | 4,000.00 | 200.00 | 12,600,000.00 | 10,000,000.00 |

## E. Targeting Summary

| Example | Target Group | Displaced Required | Retraining Required | Household Test Placeholder | Income Test Placeholder | Eligible People | Targeting Risk |
| --- | --- | --- | --- | --- | --- | ---: | --- |
| Displaced Worker Targeted Supplement | unreabsorbed automation-displaced workers | True | False | False | False | 800.00 | low |
| High Cliff-Risk Interaction Case | broad automation-transition support with weak displacement linkage | False | True | True | True | 500.00 | critical |
| Household Eligibility Placeholder Review | displaced workers subject to unresolved household and income tests | True | False | True | True | 750.00 | medium |
| Hybrid Stack Double-Counting Review | displaced workers with partial universal component | True | False | True | True | 1,100.00 | medium |
| Retraining Income Phase-In | displaced workers enrolled in retraining | True | True | False | False | 550.00 | medium |
| UBI-Lite With Existing Support Baseline | broad adult population placeholder | False | False | False | False | 10,000.00 | high |

## F. Phase-In / Phase-Out Summary

| Example | Year | Phase-In Start | Phase-In End | Phase-Out Start | Phase-Out End | Phase Multiplier |
| --- | ---: | ---: | ---: | --- | --- | ---: |
| Displaced Worker Targeted Supplement | 2028 | 2026 | 2026 | N/A | N/A | 1.00 |
| High Cliff-Risk Interaction Case | 2029 | 2026 | 2026 | N/A | N/A | 1.00 |
| Household Eligibility Placeholder Review | 2028 | 2026 | 2026 | 2032 | 2034 | 1.00 |
| Hybrid Stack Double-Counting Review | 2028 | 2026 | 2026 | N/A | N/A | 1.00 |
| Retraining Income Phase-In | 2027 | 2026 | 2028 | N/A | N/A | 0.62 |
| UBI-Lite With Existing Support Baseline | 2028 | 2026 | 2026 | N/A | N/A | 1.00 |

## G. Payment Stack and Double-Counting Review

Component costs are phase-adjusted before double-counting adjustments. The effective multiplier equals component multiplier × year phase multiplier.

### Displaced Worker Targeted Supplement

Phase-adjusted gross stack cost before interactions: `4,000,000.00`

Double-count adjustment: `0.00`

Net stack cost after interactions: `4,000,000.00`

| Component | Type | Eligible People | Payment Per Person | Priority | Component Multiplier | Year Phase Multiplier | Effective Multiplier | Phase-Adjusted Cost | Mutually Exclusive With |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| displaced_worker_supplement | DISPLACED_WORKER_SUPPLEMENT | 800.00 | 5,000.00 | 1 | 1.00 | 1.00 | 1.00 | 4,000,000.00 | None |

### High Cliff-Risk Interaction Case

Phase-adjusted gross stack cost before interactions: `47,000,000.00`

Double-count adjustment: `0.00`

Net stack cost after interactions: `47,000,000.00`

| Component | Type | Eligible People | Payment Per Person | Priority | Component Multiplier | Year Phase Multiplier | Effective Multiplier | Phase-Adjusted Cost | Mutually Exclusive With |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| broad_transition_income | TRANSITION_INCOME | 5,000.00 | 9,000.00 | 1 | 1.00 | 1.00 | 1.00 | 45,000,000.00 | None |
| retraining_grant | RETRAINING_GRANT | 500.00 | 4,000.00 | 2 | 1.00 | 1.00 | 1.00 | 2,000,000.00 | None |

### Household Eligibility Placeholder Review

Phase-adjusted gross stack cost before interactions: `3,375,000.00`

Double-count adjustment: `0.00`

Net stack cost after interactions: `3,375,000.00`

| Component | Type | Eligible People | Payment Per Person | Priority | Component Multiplier | Year Phase Multiplier | Effective Multiplier | Phase-Adjusted Cost | Mutually Exclusive With |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| household_review_supplement | DISPLACED_WORKER_SUPPLEMENT | 750.00 | 4,500.00 | 1 | 1.00 | 1.00 | 1.00 | 3,375,000.00 | None |

### Hybrid Stack Double-Counting Review

Phase-adjusted gross stack cost before interactions: `12,200,000.00`

Double-count adjustment: `1,800,000.00`

Net stack cost after interactions: `10,400,000.00`

| Component | Type | Eligible People | Payment Per Person | Priority | Component Multiplier | Year Phase Multiplier | Effective Multiplier | Phase-Adjusted Cost | Mutually Exclusive With |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| ubi_lite | UBI_LITE | 12,000.00 | 500.00 | 1 | 1.00 | 1.00 | 1.00 | 6,000,000.00 | None |
| displaced_worker_supplement | DISPLACED_WORKER_SUPPLEMENT | 1,100.00 | 4,000.00 | 2 | 1.00 | 1.00 | 1.00 | 4,400,000.00 | retraining_grant |
| retraining_grant | RETRAINING_GRANT | 600.00 | 3,000.00 | 3 | 1.00 | 1.00 | 1.00 | 1,800,000.00 | displaced_worker_supplement |

### Retraining Income Phase-In

Phase-adjusted gross stack cost before interactions: `2,750,000.00`

Double-count adjustment: `0.00`

Net stack cost after interactions: `2,750,000.00`

| Component | Type | Eligible People | Payment Per Person | Priority | Component Multiplier | Year Phase Multiplier | Effective Multiplier | Phase-Adjusted Cost | Mutually Exclusive With |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| retraining_income | TRANSITION_INCOME | 550.00 | 8,000.00 | 1 | 1.00 | 0.62 | 0.62 | 2,750,000.00 | None |

### UBI-Lite With Existing Support Baseline

Phase-adjusted gross stack cost before interactions: `10,000,000.00`

Double-count adjustment: `0.00`

Net stack cost after interactions: `10,000,000.00`

| Component | Type | Eligible People | Payment Per Person | Priority | Component Multiplier | Year Phase Multiplier | Effective Multiplier | Phase-Adjusted Cost | Mutually Exclusive With |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| ubi_lite | UBI_LITE | 10,000.00 | 1,000.00 | 1 | 1.00 | 1.00 | 1.00 | 10,000,000.00 | None |

## H. Support Fiscal Incidence Preview

Support incidence offsets are shown separately and are not validated savings.

| Example | Gross Support Cost | Household Spending Flow | Placeholder GST Recovery | Hardship Offset Preview | Net Fiscal Cost After Placeholder Offsets |
| --- | ---: | ---: | ---: | ---: | ---: |
| Displaced Worker Targeted Supplement | 4,000,000.00 | 2,800,000.00 | 112,000.00 | 400,000.00 | 3,488,000.00 |
| High Cliff-Risk Interaction Case | 47,000,000.00 | 35,250,000.00 | 1,410,000.00 | 5,640,000.00 | 39,950,000.00 |
| Household Eligibility Placeholder Review | 3,375,000.00 | 2,295,000.00 | 91,800.00 | 337,500.00 | 2,945,700.00 |
| Hybrid Stack Double-Counting Review | 10,400,000.00 | 7,280,000.00 | 291,200.00 | 832,000.00 | 9,276,800.00 |
| Retraining Income Phase-In | 2,750,000.00 | 2,062,500.00 | 82,500.00 | 330,000.00 | 2,337,500.00 |
| UBI-Lite With Existing Support Baseline | 10,000,000.00 | 6,500,000.00 | 260,000.00 | 500,000.00 | 9,240,000.00 |

## I. Residual Support Gap

Residual support gap is `max(0, net stack cost - automation revenue available)`.

## J. Combined Commonwealth/Support Gap

Combined gap adds the residual support gap to the placeholder Commonwealth gap after CARSF. It is not a budget estimate.

## K. Targeting and Interaction Risk Bands

| Example | Baseline Cost | Targeted Eligible People | Phase Multiplier | Phase-Adjusted Gross Stack Cost | Double-Count Adjustment | Net Stack Cost | Residual Support Gap | Interaction Risk | Final Liability Modified |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Displaced Worker Targeted Supplement | 330,000.00 | 800.00 | 1.00 | 4,000,000.00 | 0.00 | 4,000,000.00 | 0.00 | low | false |
| High Cliff-Risk Interaction Case | 9,375,000.00 | 500.00 | 1.00 | 47,000,000.00 | 0.00 | 47,000,000.00 | 46,000,000.00 | critical | false |
| Household Eligibility Placeholder Review | 2,240,000.00 | 750.00 | 1.00 | 3,375,000.00 | 0.00 | 3,375,000.00 | 875,000.00 | high | false |
| Hybrid Stack Double-Counting Review | 3,180,000.00 | 1,100.00 | 1.00 | 12,200,000.00 | 1,800,000.00 | 10,400,000.00 | 3,400,000.00 | high | false |
| Retraining Income Phase-In | 540,000.00 | 550.00 | 0.62 | 2,750,000.00 | 0.00 | 2,750,000.00 | 0.00 | medium | false |
| UBI-Lite With Existing Support Baseline | 12,600,000.00 | 10,000.00 | 1.00 | 10,000,000.00 | 0.00 | 10,000,000.00 | 6,000,000.00 | critical | false |

## L. Plain-English Interpretation

### Displaced Worker Targeted Supplement

Targeted supplement keeps the existing transfer baseline separate, limits eligibility to directly displaced unreabsorbed workers, and has a low residual support gap under these placeholders.

- Firm-level CARSF liability is not automatically modified by this payment-interaction preview.

### High Cliff-Risk Interaction Case

High displacement and weak automation revenue create a large residual support gap. The weak targeting link and unresolved household/income tests push this into a high or critical review band under placeholders.

- Firm-level CARSF liability is not automatically modified by this payment-interaction preview.

### Household Eligibility Placeholder Review

This case keeps household and income eligibility unresolved. It should require review rather than implying a final welfare eligibility rule.

- Firm-level CARSF liability is not automatically modified by this payment-interaction preview.

### Hybrid Stack Double-Counting Review

The hybrid package shows a gross stack cost, then a prototype double-count adjustment where retraining grants and supplements are mutually exclusive.

- Firm-level CARSF liability is not automatically modified by this payment-interaction preview.

### Retraining Income Phase-In

Retraining-linked income phases in gradually, reducing first-year cost while still showing exclusion risk if retraining capacity is lower than displacement.

- Firm-level CARSF liability is not automatically modified by this payment-interaction preview.

### UBI-Lite With Existing Support Baseline

UBI-lite is shown separately from existing transfer baseline cost. It has broad inclusion risk under placeholders because it is not limited to directly displaced workers.

- Firm-level CARSF liability is not automatically modified by this payment-interaction preview.

## M. Limitations and Calibration Needs

- All payment, eligibility, household, targeting, phase-rule, and support-incidence values are illustrative placeholders.
- No UBI policy, welfare advice, eligibility law, Centrelink/DSS/Services Australia modelling, Treasury costing, PBO costing, legal advice, tax advice, or economic validation is claimed.
- Future work requires welfare, household, population, labour-market, fiscal, legal, privacy, DSS / Services Australia, Treasury, PBO, and economic review before policy use.
