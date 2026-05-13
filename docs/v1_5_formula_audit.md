# V1.5 Formula Implementation Audit

Status: hostile implementation audit for the prototype branch.

This audit does not legally, economically, or empirically validate CARSF. It checks whether the current code behaves defensively against obvious V1.5 prototype failure modes.

## Baseline

- Baseline suite on `main`: 18 passed, 1 pytest-asyncio deprecation warning.
- Hardened suite on this branch: expanded to cover edge cases and red-team metadata.

## Findings and Hardening

| Area | Audit finding | V1.5 hardening |
| --- | --- | --- |
| QLC cap | Cap existed, but hostile edge cases for fake score inflation and zero-hour workers were thin. | Added finite checks, non-negative weight validation, fake-inflation tests, zero-hour test, and negative-weight rejection. |
| AII | Bounds and weight-sum validation existed, but non-finite component checks were not explicit. | Added finite checks for components and weights; expanded tests. |
| NLTG | Formula correctly used `max(0, ...)`. | Existing non-negative test retained. |
| AAVA | Formula allowed negative AAVA result when verified costs exceed revenue, but tests did not prove downstream cap safety. | Added zero-AAVA and negative-AAVA tests proving payable liability and caps fall to zero while raw shortfall remains recordable. |
| AEL cap | Cap used non-negative AAVA base, which is appropriate for zero/negative AAVA. | Added cap-rate finite and `[0, 1]` validation plus zero/negative AAVA tests. |
| Combined cap | Combined liability cap used non-negative AAVA base. | Added explicit zero/negative AAVA tests. |
| CoverageRatio | Returned `1.0` when measured fiscal damage was zero, which could imply 100% coverage. | Changed zero-damage result to `None`; UI formatter displays `N/A - no measured damage`. |
| CARS-I | Used epsilon for zero captured revenue. | Existing safe handling retained and tested. |
| Schedules | Prototype schedules lacked enough measurement controls for avoidance vectors. | Added measurement scope, evidence requirements, AAVA appendix reference, classification controls, and avoidance controls. |

## Remaining Prototype Risks

- No real calibration values exist in this repo.
- AAVA deductibility taxonomy is not legal drafting.
- Grouped-entity aggregation and schedule apportionment now exist only as executable modelling previews; they are not legal grouping, tax-law attribution, transfer-pricing, or calibrated policy logic.
- Related-party adjustments and transfer-pricing checks remain review flags only.
- Coverage metrics are national-monitoring aids, not fiscal validation.
- Streamlit UI remains a prototype and must not be used for actual liability estimates.
