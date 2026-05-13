# CARSF V1.5 Development Plan

V1.5 is V1.4 plus two prototype sector schedules and a measurement appendix. It is not only an examples update.

## Scope

1. Add QLC per-worker cap.
2. Add AAVA deductibility appendix.
3. Add CoverageRatio alongside CARS-I.
4. Rename "PRRT-style" to "PRRT-inspired uplift logic."
5. Clean up LIBC / labour-intensity terminology.
6. Change title away from "Treasury Exposure Draft" to "Pre-Consultation Concept Paper."
7. Build Prototype Schedule A: Automotive Repair.
8. Build Prototype Schedule B: Logistics / Warehousing.
9. Add open-source AI treatment.
10. Add R&D Tax Incentive interaction policy position.

## Measurement Appendix Work

- Define worker-level QLC cap in policy text and code.
- Define AAVA deductions as confirmed, illustrative, placeholder, or unresolved. Initial taxonomy lives in `paper/aava_deductibility_appendix.md`.
- Define zero-damage and zero-revenue handling for CARS-I and CoverageRatio.
- Add schedule-specific canonical output units and AII component mappings.
- Add anti-avoidance examples for entity splitting, offshore automation services, sector arbitrage, token oversight jobs, and related-party AI service fees.
- Add executable prototype safe-harbour, anti-avoidance, and grouped-entity review flags without modifying liability.

## Data Separation

- Confirmed baseline figures must cite official sources.
- Illustrative assumptions must be labelled as modelling assumptions.
- Placeholder values must not be presented as calibrated settings.
- Future research requirements must identify the missing data owner or review pathway.

## Exit Criteria

- Automotive and logistics prototype schedules exist.
- Six illustrative examples calculate through the Python engine.
- End-to-end example reports can be generated with `python scripts/run_examples.py`.
- Tests prove cap, bounds, zero handling, and avoidance metadata.
- Tests prove AI-admin repair is not classified like robotic repair and AI logistics is riskier than human-heavy logistics.
- Reports include safe-harbour, avoidance, and grouping review outputs.
- V1.5 working paper contains TODO markers where policy drafting remains open.
- Limitations document clearly blocks actual tax-payable claims.

## Next Build Candidates

- Add multi-schedule apportionment for mixed-activity firms.
- Add calibrated-threshold placeholders that can later be replaced by official data.
- Convert grouping review flags into a prototype aggregation calculation.
- Add non-zero but intermediate hybrid logistics stress variants.
