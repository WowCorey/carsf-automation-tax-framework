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
- Add prototype evidence requirements for formula inputs, review flags, transfer-pricing, mixed units, and calibration fields.
- Add decision-log summaries for example, grouped, and transfer-pricing runs.
- Add a calibration shell and data source registry without collecting real data.
- Add controlled synthetic mock evidence packets, review-state workflow transitions, and privacy/secrecy classification for workflow testing only.
- Add default-deny secure ingestion controls, sensitive-marker scanning, redaction metadata, retention/access policy scaffolding, and immutable-style ingestion audit records.
- Add repository-level enforcement gates for prohibited evidence paths, secret-like file extensions, sensitive markers, generated-report non-claims, and raw evidence payload checks.
- Add non-operative investment, tax-incidence, burden-balance, and sensitivity guardrails without modifying final liability.
- Add a national fiscal trajectory engine for placeholder PAYG erosion, transfer pressure, automation revenue captured, and residual public-sector gaps without modifying firm-level liability.
- Add a non-operative transition-payment funding module for displaced-worker supplements, UBI-lite placeholders, retraining grants, automation-dividend previews, and hybrid support packages.
- Add prototype payment-interaction mechanics for existing transfer baseline separation, targeting, phase-in / phase-out, payment-stack double-counting, support incidence, and residual support gaps without modifying firm-level liability.
- Add synthetic household distributional scenarios for household composition, income bands, regional stress, re-employment timing, payment cliffs, residual household gaps, and shock-band summaries without using real household data or modifying firm-level liability.
- Add a synthetic household weighting and subgroup aggregation shell without claiming representativeness or modifying firm-level liability.

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
- Evidence and calibration reports can be generated with `python scripts/run_examples.py`.
- Mock evidence workflow reports can be generated with `python scripts/run_evidence_workflow.py`.
- Secure ingestion-control reports can be generated with `python scripts/run_ingestion_controls.py`.
- Repository guardrail reports can be generated with `python scripts/run_repo_guardrails.py` and CI fails on denied findings.
- Investment and incidence guardrail reports can be generated with `python scripts/run_investment_guardrails.py`.
- Fiscal trajectory reports can be generated with `python scripts/run_fiscal_trajectory.py`.
- Transition funding reports can be generated with `python scripts/run_transition_funding.py`.
- Payment interaction reports can be generated with `python scripts/run_payment_interactions.py`.
- Synthetic household distributional scenario reports can be generated with `python scripts/run_distributional_scenarios.py`.
- Synthetic household weighting reports can be generated with `python scripts/run_household_weighting.py`.
- Hybrid logistics stress variant demonstrates non-zero but intermediate NLTG.
- V1.5 working paper contains TODO markers where policy drafting remains open.
- Limitations document clearly blocks actual tax-payable claims.

## Next Build Candidates

- Add calibrated-threshold placeholders that can later be replaced by official data.
- Replace preview apportionment shares with evidence-backed activity allocation once official data and legal review exist.
- Extend grouped aggregation to recompute full group-level outputs only after legal grouping and attribution rules are drafted.
- Extend transfer-pricing, GST, and international tax review stubs into legally reviewed policy options.
- Draft treatment for value-weighted exposure metrics so they cannot be mistaken for a tax base.
- Add evidence ingestion schemas and review workflows once legal/privacy constraints are known.
- Harden mock evidence workflow against accidental real data ingestion before any external review.
- Tune repository guardrail allowlists and integrate external DLP/secret-scanning tooling before any evidence-adjacent external review.
- Calibrate investment deterrence, pass-through, normal-return preservation, and public-revenue coverage using Treasury/economic/tax-incidence review.
- Replace calibration shell placeholders with authorised datasets only after formal source review.
- Add deeper welfare-program interaction, household eligibility, phase-out mechanics, and support-incidence calibration only after legal, DSS / Services Australia, Treasury, PBO, and labour-market review.
- Add calibrated household distributional analysis only after ABS/HILDA/DSS/Services Australia, privacy, legal, Treasury, PBO, and labour-market review.
- Replace synthetic household weights and subgroup filters only after authorised survey weighting, representativeness, uncertainty, and data-governance review.
