# Tax Review Attacks

This attack document does not mean external review has been completed, does not mean approval has been granted, and does not mean validation has occurred. It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare validation, not statistical validation, not compliance scoring, not enforcement, and does not modify firm-level CARSF liability.

## What To Inspect First

- `reports/example_results.md`
- `reports/transfer_pricing_results.md`
- `reports/grouped_entity_results.md`
- `reports/sector_schedule_expansion.md`

## Attack Questions

- Are AAVA and deductibility treatments visibly unresolved?
- Do transfer-pricing previews avoid implying addbacks?
- Do grouped-entity previews avoid implying legal grouping?
- Are safe harbours, caps, credits, OPFTE, and FRV placeholders?
- Could any output be read as tax payable?

## Likely Failure Modes

- A transfer-pricing preview sounds like a tax adjustment.
- A grouped-entity row sounds like legal aggregation.
- AAVA appears as a settled tax base.
- Caps or credits look calibrated.
- Software intangible treatment is understated.

## Required Evidence / External Review

- Tax counsel review.
- Transfer-pricing review.
- AAVA deductibility review.
- Grouped-entity legal review.
- Safe-harbour and cap calibration review.

## What Not To Infer

- Do not infer tax advice, actual tax payable, addbacks, legal grouping, official schedule treatment, validation, approval, or firm-level liability change.

## Locked-Until-Review Items

- AAVA deductibility.
- Transfer-pricing attribution.
- Grouping.
- Caps and credits.
- Software and digital platform intangible treatment.

## Suggested Reviewer Output Format

Use issue, formula/report location, tax-law gap, missing external evidence, and required legal/tax review.

