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
- Add deterministic low/base/high uncertainty range mechanics without claiming Monte Carlo, confidence intervals, forecasts, representativeness, or calibration.
- Add a reviewed scenario comparison layer that hides fragile, range-sensitive, missing-range, or non-interpretable synthetic outputs from clean point-estimate presentation.
- Expand the prototype sector schedule library to call centres / customer support, accounting / administration, retail self-checkout / fulfilment, and software / digital platforms without calibration or legal schedule claims.
- Add a sector stress matrix that compares placeholder schedules across metadata-only stress dimensions, display-control statuses, and do-not-rank warnings without calibration or real-world sector ranking claims.
- Add a behavioural response / gaming simulation layer that maps synthetic response pathways to linked avoidance flags, pressure bands, countermeasure categories, review statuses, and calibration blockers without conduct forecasting or liability modification.
- Add a prototype administrative compliance workflow shell that organises synthetic cases into evidence request bundles, review queues, escalation pathways, behavioural-response links, locked/suppressed states, and external-review blockers without enforcement, notices, compliance scoring, or liability modification.
- Add a pre-Build 21 hardening pass that preserves subgroup metadata, clarifies automation-intensity component explanations, improves behavioural response band spread, and adds routine/enhanced administrative workflow demonstration paths without adding legislative architecture or changing liability.
- Add a non-operative legislative architecture skeleton that maps CARSF concepts into proposed Parts, Divisions, definitions, sector schedules, evidence placeholders, safeguards, regulation-making placeholders, commencement/transitional placeholders, and external-review blockers without drafting operative law or changing liability.
- Add an executive dashboard and report index that consolidates prototype layers, generated reports, Streamlit pages, non-claim profiles, calibration blockers, external-review blockers, suggested review navigation, and reviewer routing without creating a readiness score or validation claim.
- Add a V1.5 working paper release-candidate pack that updates working-paper references and packages release notes, reviewer briefing, report map, calibration blockers, non-claim boundaries, external-review routing, and manifest metadata without creating official status, legal sufficiency, operational readiness, validation, or liability changes.
- Add a V1.5 external review attack pack that gives discipline-specific reviewers challenge questions, failure modes, required external inputs, boundary checks, report attack matrices, and layer attack matrices without implying review completion, approval, validation, legal sufficiency, operational readiness, official status, or liability changes.
- Add a V1.5 final RC integrity seal that checks release documents, attack-pack documents, generated reports, manifests, scripts, digest metadata, non-claim boundaries, repo guardrail expectations, CI expectations, and false readiness/legal/validation flags without implying approval, validation, external review completion, legal sufficiency, operational readiness, official status, or liability changes.
- Add a public aggregate-data pilot and realistic-placeholder anchor layer that keeps loaded public extracts, source-reference-only records, realistic placeholders, restricted-data blockers, and forbidden repo data separate without completing calibration or changing liability.
- Add a public data pilot reviewer evidence map and dashboard that makes Build 27 source references, loaded extracts, source-reference-only rows, placeholder anchors, field sanity checks, module sanity checks, restricted blockers, and reviewer questions inspectable without loading new data, completing calibration, claiming validation, or changing liability.
- Add a public data pilot consistency audit and source-reconciliation layer that checks existing Build 27 and Build 28 artefacts, digests, reports, dashboard source, non-claim boundaries, Fair Work wage arithmetic, and source-reference-only counting without loading new data, externally verifying source values, completing calibration, claiming validation, or changing liability.
- Add a public data source-locator verification pack that packages existing Build 27-29 source URLs, locators, value notes, source-reference-only records, placeholder anchors, blocker cards, and manual-review checklists without loading new data, claiming external source verification, completing calibration, claiming validation, or changing liability.
- Add a red-team reviewer objections pack that packages likely reviewer criticisms, valid concern explanations, bounded project responses, unresolved blockers, evidence needs, and must-not-claim boundaries without loading new data, resolving objections, completing calibration, claiming validation, or changing liability.

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
- Uncertainty range reports can be generated with `python scripts/run_uncertainty_ranges.py`.
- Reviewed scenario reports can be generated with `python scripts/run_reviewed_scenarios.py`.
- Sector schedule expansion reports can be generated with `python scripts/run_sector_schedule_expansion.py`.
- Sector stress matrix reports can be generated with `python scripts/run_sector_stress_matrix.py`.
- Behavioural response simulation reports can be generated with `python scripts/run_behavioural_response_simulation.py`.
- Administrative compliance workflow reports can be generated with `python scripts/run_administrative_compliance_workflow.py`.
- Pre-Build 21 hardening is documented in `docs/pre_legislative_hardening.md` and covered by regenerated uncertainty, reviewed-scenario, sector-stress, behavioural-response, and administrative-workflow reports.
- Legislative architecture reports can be generated with `python scripts/run_legislative_architecture.py`.
- Executive dashboard reports can be generated with `python scripts/run_executive_dashboard.py`.
- V1.5 release-candidate pack reports can be generated with `python scripts/run_v1_5_release_candidate_pack.py`.
- V1.5 external review attack-pack reports can be generated with `python scripts/run_external_review_attack_pack.py`.
- V1.5 final RC integrity seal reports can be generated with `python scripts/run_v1_5_final_rc_integrity_seal.py`.
- Real-data feasibility and calibration-intake reports can be generated with `python scripts/run_real_data_feasibility.py`.
- Public data pilot and realistic-placeholder anchor reports can be generated with `python scripts/run_public_data_pilot.py`.
- Public data pilot reviewer evidence-map reports can be generated with `python scripts/run_public_data_evidence_map.py`.
- Public data source-locator verification-pack reports can be generated with `python scripts/run_source_locator_verification_pack.py`.
- Red-team reviewer objections reports can be generated with `python scripts/run_red_team_reviewer_objections.py`.
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
- Replace deterministic placeholder uncertainty ranges only after external statistical methods, calibration, and data-governance review.
- Expand sector schedules only after reviewed scenario display-control rules are in place so new sector outputs inherit suppression and external-review handling.
- Build a sector stress matrix only after expanded schedule placeholders are present, and do not present it as a real-world sector ranking.
- Add behavioural response and gaming simulation only after sector stress bands exist, so relabelling, entity splitting, offshore routing, customer self-service shifting, related-party software fees, and schedule arbitrage can be shown as prototype responses without real conduct-forecast claims.
- Build an administrative compliance workflow only after behavioural response flags exist, so evidence requests, review states, sector schedule review, grouped-entity review, transfer-pricing review, and escalation pathways can be organised without claiming real ATO enforcement powers.
- Build a legislative architecture skeleton only after administrative workflow routing exists, so any future Parts, Divisions, schedules, evidence-power placeholders, safeguards, and review mechanisms inherit clear non-operative limits.
- Consolidate the full prototype stack into an executive dashboard only after the legislative architecture skeleton exists, so reviewers can navigate formulas, schedules, stress, behavioural, administrative, legislative, uncertainty, household, fiscal, guardrail, and calibration outputs without implying operational readiness or legal sufficiency.
- Update the V1.5 working paper and release-candidate pack only after the dashboard exists, so the paper can point reviewers to the complete prototype stack without implying legal, economic, Treasury, ATO, welfare, or operational validation.
- Create an external review attack pack after the V1.5 release-candidate pack exists, so legal, tax, Treasury, ATO methods, privacy, economic, statistical, welfare, Parliamentary Counsel, technical, and hostile reviewers can challenge the release candidate without implying validation, approval, legal sufficiency, operational readiness, or real-world policy readiness.
- Create a final RC integrity seal after the external review attack pack exists, so release documents, attack-pack documents, report paths, manifests, scripts, false flags, digest metadata, CI expectations, and non-claim boundaries can be checked without implying approval, validation, external review completion, legal sufficiency, operational readiness, official status, or implementation readiness.
- Add a real-data feasibility and calibration-intake map after the final RC seal exists, so public aggregate candidates, restricted-data needs, realistic placeholders, forbidden repo data, and Build 27 pilot candidates are visible without loading data, completing calibration, weakening non-claims, or changing firm-level liability.
- Add a public data pilot sanity-check dashboard / reviewer evidence map after the public-data pilot exists, so reviewers can see which assumptions are source-referenced, public-aggregate anchored, realistic-placeholder-only, or blocked by restricted data without implying calibration, validation, actual tax payable, official status, or implementation readiness.
