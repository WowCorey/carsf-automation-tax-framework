# Implementation Notes

The Python model intentionally implements only concept-level formulas.

## Current Choices

- Inputs are validated for obvious negative values.
- Worker-level QLC scores and AII components are bounded in `[0, 1]`.
- AII weights must sum to 1.
- AAVA is calculated as specified, while caps use a non-negative AAVA base.
- ARL uses "PRRT-inspired uplift logic" and is not a full PRRT model.
- CoverageRatio treats zero measured fiscal damage as fully covered by convention.
- CARS-I uses epsilon to avoid divide-by-zero when captured revenue is zero.

## Not Implemented Yet

- Real schedule calibration.
- Safe-harbour eligibility engine.
- Multi-schedule apportionment.
- Grouped-entity aggregation.
- Related-party pricing adjustments.
- International tax treaty logic.
- Privacy-preserving disclosure schema.
- Behavioural elasticity and deadweight-loss modelling.
