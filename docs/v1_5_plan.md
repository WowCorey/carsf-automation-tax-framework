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
- Add prototype grouped-entity aggregation previews and mixed-activity / prototype apportionment previews without implementing legal grouping or tax-law attribution.
- The current mixed-activity example uses the combined `logistics_warehousing` prototype schedule for all activity slices. It tests apportionment plumbing and share-validation logic, not final cross-sector schedule blending. True multi-schedule blending requires additional calibrated sector schedules.
- Add non-operative transfer-pricing / related-party preview stubs for offshore AI services, IP/platform royalties, cloud/inference relabelling, robotics leasing, service fees, data/model licences, cost sharing, and other automation-linked related-party costs.
- Add adjusted-AAVA preview calculations that do not mutate reported AAVA or replace existing final liability.
- Add mixed-unit handling so output/HLE aggregation is prohibited where canonical output units differ unless reviewed conversion metadata exists.

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
- Grouped reports can be generated with `python scripts/run_examples.py`.
- Transfer-pricing and mixed-unit preview reports can be generated with `python scripts/run_examples.py`.
- Hybrid logistics stress variant demonstrates non-zero but intermediate NLTG.
- V1.5 working paper contains TODO markers where policy drafting remains open.
- Limitations document clearly blocks actual tax-payable claims.

## Next Build Candidates

- Add calibrated-threshold placeholders that can later be replaced by official data.
- Replace preview apportionment shares with evidence-backed activity allocation once official data and legal review exist.
- Extend grouped aggregation to recompute full group-level outputs only after legal grouping and attribution rules are drafted.
- Extend transfer-pricing, GST, and international tax review stubs into legally reviewed policy options.
- Draft treatment for value-weighted exposure metrics so they cannot be mistaken for a tax base.
