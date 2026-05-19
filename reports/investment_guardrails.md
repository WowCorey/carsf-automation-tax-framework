# CARSF V1.5 Investment and Tax-Incidence Guardrails

Generated at: `2026-05-19T00:02:06+00:00`

## A. Purpose

This report previews non-operative guardrails for effective automation burden, normal-return preservation, tax-incidence pressure, investment-deterrence review, and under-capture / over-capture risk.

## B. Non-Claims

- These are prototype investment and tax-incidence guardrails only. They are not economic validation, investment advice, Treasury modelling, ATO guidance, legal advice, market forecasting, or tax advice.
- Guardrail outputs do not automatically modify final liability.
- Pass-through, burden, normal-return, and sensitivity values are illustrative placeholders requiring calibration.

## C. Why Investment/Tax-Incidence Guardrails Matter

A prototype automation fiscal framework can be too weak, too punitive, or shifted onto consumers, workers, suppliers, or ordinary capital. These checks are designed to surface that review problem without changing final liability.

## D. Effective Burden Table

| Example | Sector | Liability | AAVA | Effective Burden | Liability/Revenue | Investment Risk | Incidence Risk | Burden Balance | Final Liability Modified |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- | --- | --- |
| AI Logistics Pass-Through Risk Case | logistics_warehousing | 1,800,000.00 | 9,000,000.00 | 20.00% | 6.00% | medium | medium | not_assessable | false |
| Low-AAVA High-Liability Warning Case | automotive_repair | 250,000.00 | 0.00 | N/A | 5.00% | critical | medium | over_capture | false |
| Productive Hybrid Low-Burden Case | logistics_warehousing | 180,000.00 | 3,200,000.00 | 5.62% | 1.29% | low | low | not_assessable | false |
| Robotic High-Burden Review Case | automotive_repair | 950,000.00 | 1,800,000.00 | 52.78% | 13.57% | high | medium | not_assessable | false |
| Under-Capture Public Revenue Gap Case | national_placeholder | 500,000.00 | 15,000,000.00 | 3.33% | 0.83% | low | medium | under_capture | false |

## E. Normal Return Preservation Preview

| Example | Preserved Return Amount | Normal Return Preserved | Main Reason |
| --- | ---: | --- | --- |
| AI Logistics Pass-Through Risk Case | 7,200,000.00 | True | Placeholder burden is material but below high-review thresholds. |
| Low-AAVA High-Liability Warning Case | N/A | False | Positive liability with zero AAVA suggests possible over-capture or cap failure. |
| Productive Hybrid Low-Burden Case | 3,020,000.00 | True | Placeholder burden is low under illustrative thresholds. |
| Robotic High-Burden Review Case | 850,000.00 | True | Placeholder effective burden may warrant investment-deterrence review. |
| Under-Capture Public Revenue Gap Case | 14,500,000.00 | True | Placeholder burden is low under illustrative thresholds. |

## F. Consumer/Worker/Supplier/Capital Incidence Preview

| Example | Consumer | Worker | Supplier | Capital | Allocation Gap | Risk Band |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| AI Logistics Pass-Through Risk Case | 810,000.00 | 180,000.00 | 90,000.00 | 360,000.00 | 360,000.00 | medium |
| Low-AAVA High-Liability Warning Case | 87,500.00 | 37,500.00 | 25,000.00 | 50,000.00 | 50,000.00 | medium |
| Productive Hybrid Low-Burden Case | 18,000.00 | 9,000.00 | 9,000.00 | 54,000.00 | 90,000.00 | low |
| Robotic High-Burden Review Case | 237,500.00 | 95,000.00 | 47,500.00 | 237,500.00 | 332,500.00 | medium |
| Under-Capture Public Revenue Gap Case | 100,000.00 | 25,000.00 | 25,000.00 | 100,000.00 | 250,000.00 | medium |

## G. Under-Capture / Over-Capture Review

Firm-level zero-liability under-capture warning and public-revenue burden-balance are separate prototype checks. A case can have no firm-level zero-liability warning while still showing public-revenue under-capture.

| Example | Coverage Ratio | Capture Gap | Band | Review Required |
| --- | ---: | ---: | --- | --- |
| AI Logistics Pass-Through Risk Case | N/A | N/A | not_assessable | true |
| Low-AAVA High-Liability Warning Case | 166.67% | -100,000.00 | over_capture | true |
| Productive Hybrid Low-Burden Case | N/A | N/A | not_assessable | true |
| Robotic High-Burden Review Case | N/A | N/A | not_assessable | true |
| Under-Capture Public Revenue Gap Case | 12.50% | 3,500,000.00 | under_capture | true |

## H. Sensitivity Sweep Summary

### AI Logistics Pass-Through Risk Case

| Sweep | Points | Min Liability | Max Liability |
| --- | ---: | ---: | ---: |
| pass_through_rate_sweep | 4 | 1,800,000.00 | 1,800,000.00 |
| liability_cap_rate_sweep | 3 | 900,000.00 | 2,400,000.00 |
| aava_sweep | 3 | 1,800,000.00 | 1,800,000.00 |

### Low-AAVA High-Liability Warning Case

| Sweep | Points | Min Liability | Max Liability |
| --- | ---: | ---: | ---: |
| pass_through_rate_sweep | 3 | 250,000.00 | 250,000.00 |
| liability_cap_rate_sweep | 3 | 0.00 | 0.00 |
| aava_sweep | 3 | 250,000.00 | 250,000.00 |

### Productive Hybrid Low-Burden Case

| Sweep | Points | Min Liability | Max Liability |
| --- | ---: | ---: | ---: |
| pass_through_rate_sweep | 4 | 180,000.00 | 180,000.00 |
| liability_cap_rate_sweep | 3 | 160,000.00 | 240,000.00 |
| aava_sweep | 3 | 180,000.00 | 180,000.00 |

### Robotic High-Burden Review Case

| Sweep | Points | Min Liability | Max Liability |
| --- | ---: | ---: | ---: |
| pass_through_rate_sweep | 4 | 950,000.00 | 950,000.00 |
| liability_cap_rate_sweep | 3 | 270,000.00 | 900,000.00 |
| aava_sweep | 3 | 950,000.00 | 950,000.00 |

### Under-Capture Public Revenue Gap Case

| Sweep | Points | Min Liability | Max Liability |
| --- | ---: | ---: | ---: |
| pass_through_rate_sweep | 3 | 500,000.00 | 500,000.00 |
| liability_cap_rate_sweep | 3 | 300,000.00 | 900,000.00 |
| aava_sweep | 3 | 500,000.00 | 500,000.00 |

## I. Example-by-Example Plain-English Interpretation

Firm-level zero-liability under-capture warning and public-revenue burden-balance are separate prototype checks. A case can have no firm-level zero-liability warning while still showing public-revenue under-capture.

### AI Logistics Pass-Through Risk Case

Pass-through risk is material under placeholders and requires incidence calibration before external use.

- Investment risk band: `medium`
- Over-capture warning: `false`
- Firm-level zero-liability under-capture warning: `false`
- Public-revenue burden-balance band: `not_assessable`
- Final liability modified by this report: `false`

### Low-AAVA High-Liability Warning Case

Positive liability with zero AAVA is a critical prototype warning, not a validated policy outcome.

- Investment risk band: `critical`
- Over-capture warning: `true`
- Firm-level zero-liability under-capture warning: `false`
- Public-revenue burden-balance band: `over_capture`
- Final liability modified by this report: `false`

### Productive Hybrid Low-Burden Case

Low placeholder burden suggests ordinary hybrid investment is not automatically treated as punitive.

- Investment risk band: `low`
- Over-capture warning: `false`
- Firm-level zero-liability under-capture warning: `false`
- Public-revenue burden-balance band: `not_assessable`
- Final liability modified by this report: `false`

### Robotic High-Burden Review Case

High placeholder burden does not prove deterrence, but it should trigger review before any operative design.

- Investment risk band: `high`
- Over-capture warning: `true`
- Firm-level zero-liability under-capture warning: `false`
- Public-revenue burden-balance band: `not_assessable`
- Final liability modified by this report: `false`

### Under-Capture Public Revenue Gap Case

Captured revenue is below placeholder fiscal damage, showing under-capture review rather than calibrated coverage.

- Investment risk band: `low`
- Over-capture warning: `false`
- Firm-level zero-liability under-capture warning: `false`
- Public-revenue burden-balance band: `under_capture`
- Final liability modified by this report: `false`

## J. Limitations and Future Calibration Needs

- Pass-through, worker pressure, supplier pressure, and capital absorption rates are illustrative placeholders.
- Normal-return proxies are placeholders and are not calibrated sector returns.
- Public-revenue coverage inputs are not official national damage estimates.
- The guardrails do not prove investment deterrence, over-capture, under-capture, or pass-through.
- Future calibration requires Treasury/economic/tax-incidence modelling and legal/tax review.
- Final liability is not automatically modified by these guardrails.
