# Statistical Methods Review Attacks

This attack document does not mean external review has been completed, does not mean approval has been granted, and does not mean validation has occurred. It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare validation, not statistical validation, not compliance scoring, not enforcement, and does not modify firm-level CARSF liability.

## What To Inspect First

- `reports/uncertainty_ranges.md`
- `reports/household_weighting.md`
- `reports/reviewed_scenarios.md`

## Attack Questions

- Could deterministic ranges look like confidence intervals?
- Could synthetic household weights look representative?
- Are suppression rules strong enough for fragile outputs?
- Are forecasts and probability claims absent?
- Is subgroup metadata preserved without population claims?

## Likely Failure Modes

- Low/base/high ranges look probabilistic.
- Weights imply population representation.
- Fragile rows show point estimates.
- Reviewed scenario categories imply statistical validation.
- Household metadata drops not-population-estimate warnings.

## Required Evidence / External Review

- Statistical methods review.
- Survey weighting calibration review.
- Uncertainty method review.
- Suppression-rule review.
- Forecast boundary review.

## What Not To Infer

- Do not infer statistical validation, population estimates, confidence intervals, forecasts, real household modelling, approval, validation, or firm-level liability change.

## Locked-Until-Review Items

- Uncertainty method.
- Household representativeness.
- Subgroup inference.
- Confidence treatment.
- Reviewed-scenario suppression.

## Suggested Reviewer Output Format

Use report row, inference risk, missing method, suppression concern, and required external calibration.

