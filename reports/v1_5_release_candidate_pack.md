# CARSF V1.5 Release Candidate Pack

Generated at: `2026-05-18T09:37:04+00:00`

## A. Purpose

This release-candidate pack consolidates the CARSF V1.5 private research prototype into a working-paper, report, reviewer-routing, calibration-blocker, and non-claim package for external review.

## B. Non-Claims

- This is a private research prototype and release-candidate pack only. It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare advice, not statistical validation, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, and not an official review pathway. It does not determine actual tax payable, does not use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, and does not modify firm-level CARSF liability.
- The release-candidate pack only packages existing prototype reports, warnings, navigation, review blockers, and working-paper material for external review.
- Suggested reviewer routing is review navigation only and is not an official process.
- It creates no readiness score, official status, validation claim, legal sufficiency, operational readiness, legislative readiness, enforcement pathway, or firm-level liability change.

## C. Release Pack Contents

- Total layers: 24
- Total reports indexed: 46
- Reports present: 46
- Reports missing: 0
- Total release documents: 7
- Release documents present: 7
- Release documents missing: 0
- Paper files checked: 6
- Working paper updated: True
- Layers requiring calibration: 7
- Layers requiring legal review: 11
- Layers requiring tax review: 8
- Layers requiring ATO methods review: 5
- Layers requiring Treasury methods review: 16
- Layers requiring privacy review: 11
- Layers requiring statistical review: 7
- Layers requiring economic review: 10
- Layers requiring welfare review: 8
- Layers requiring Parliamentary Counsel review: 3
- real_data_used: False
- readiness_score_created: False
- operational_readiness_claimed: False
- legal_sufficiency_claimed: False
- legislative_readiness_claimed: False
- economic_validation_claimed: False
- welfare_validation_claimed: False
- statistical_validation_claimed: False
- official_status_claimed: False
- firm_level_liability_logic_modified: False

## D. Working Paper Update Summary

- Checked source working paper and paper support files: paper/CARSF_V1_5_WORKING.md, paper/executive_summary.md, paper/formula_reference.md, paper/glossary.md, paper/references.md, paper/export_notes.md
- Working paper updated with current V1.5 layer references: True
- Working-paper updates are additive and do not convert the paper into law, legal drafting, official policy, or validation.

## E. Prototype Stack Summary

| Layer ID | Layer Name | Group | Summary | Status Labels | Primary Reports | Streamlit Pages | Reviewer Routing | Main Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| administrative_workflow | Administrative Compliance Workflow | administrative_workflow | Synthetic evidence request, review queue, escalation, locked, and suppressed workflow routing. | prototype_only, synthetic_only, non_operative, external_review_required | reports/administrative_compliance_workflow.md, reports/administrative_compliance_workflow.json | simulator/pages/23_Administrative_Workflow.py | ato_methods_reviewer, legal_reviewer, privacy_reviewer | Workflow routing organises synthetic cases only. |
| behavioural_response | Behavioural Response Simulation | behavioural_response | Synthetic gaming pathway review for relabelling, routing, schedule arbitrage, fees, and unresolved treatment gaps. | prototype_only, synthetic_only, external_review_required | reports/behavioural_response_simulation.md, reports/behavioural_response_simulation.json | simulator/pages/22_Behavioural_Response.py | legal_reviewer, tax_reviewer, ato_methods_reviewer, hostile_red_team_reviewer | Pathways are synthetic review prompts only. |
| calibration_shell | Calibration Shell | calibration | Documentation and generated report of data categories and external review requirements needed before calibration. | prototype_only, calibration_required, external_review_required | reports/calibration_requirements.md, reports/calibration_requirements.json | simulator/pages/8_Evidence_and_Calibration.py | technical_reviewer, statistical_methods_reviewer, treasury_methods_reviewer | Shell lists unresolved data needs only. |
| core_formula_model | Core Formula Model | formula_core | Prototype QLC, HLE, AII, NLTG, AAVA, levy, credit, cap, CARS-I, and CoverageRatio mechanics. | prototype_only, placeholder_only, not_for_real_world_use | reports/example_results.md, reports/example_results.json | simulator/pages/2_Tax_Model.py | legal_reviewer, tax_reviewer, treasury_methods_reviewer, ato_methods_reviewer | Core formula outputs remain prototype calculations and do not determine tax payable. |
| evidence_workflow | Evidence Workflow | evidence_workflow | Synthetic mock evidence packet, review-state, confidence, and privacy/secrecy workflow. | prototype_only, synthetic_only, privacy_review_required | reports/mock_evidence_workflow.md, reports/mock_evidence_workflow.json, reports/evidence_requirements.md, reports/evidence_requirements.json | simulator/pages/9_Mock_Evidence_Workflow.py | privacy_reviewer, ato_methods_reviewer, legal_reviewer | Mock evidence workflow uses synthetic packets only. |
| executive_dashboard | Executive Dashboard | executive_dashboard | Consolidated dashboard and report index for navigating the V1.5 prototype stack. | prototype_only, placeholder_only, generated_report_available | reports/executive_dashboard.md, reports/executive_dashboard.json | simulator/pages/25_Executive_Dashboard.py | policy_reviewer, technical_reviewer | Dashboard is navigation only. |
| fiscal_trajectory | Fiscal Trajectory | fiscal_trajectory | Placeholder national fiscal trajectory for PAYG erosion, support pressure, automation revenue capture, and residual gaps. | prototype_only, placeholder_only, calibration_required | reports/fiscal_trajectory.md, reports/fiscal_trajectory.json | simulator/pages/13_Fiscal_Trajectory.py | treasury_methods_reviewer, economic_methods_reviewer, technical_reviewer | Fiscal trajectory is placeholder accounting only. |
| household_distributional | Household Distributional Scenarios | household_distributional | Synthetic household budget, re-employment, regional stress, payment cliff, and shock-band scenarios. | prototype_only, synthetic_only, statistical_methods_review_required | reports/distributional_scenarios.md, reports/distributional_scenarios.json | simulator/pages/16_Distributional_Scenarios.py | statistical_methods_reviewer, welfare_policy_reviewer, privacy_reviewer | Household cases are synthetic only. |
| household_weighting | Household Weighting | household_weighting | Synthetic subgroup weights, weighted residual gaps, high/critical shares, and calibration-readiness shell. | prototype_only, synthetic_only, not_population_estimate | reports/household_weighting.md, reports/household_weighting.json | simulator/pages/17_Household_Weighting.py | statistical_methods_reviewer, privacy_reviewer, welfare_policy_reviewer | Weighting shell is synthetic and not representative. |
| investment_incidence | Investment and Incidence Guardrails | investment_incidence | Placeholder burden, pass-through, investment, incidence, under-capture, and over-capture guardrails. | prototype_only, placeholder_only, economic_methods_review_required | reports/investment_guardrails.md, reports/investment_guardrails.json | simulator/pages/12_Investment_and_Incidence_Guardrails.py | economic_methods_reviewer, treasury_methods_reviewer, tax_reviewer | Guardrails flag sensitivity only. |
| legislative_architecture | Legislative Architecture Skeleton | legislative_architecture | Non-operative architecture skeleton for proposed Parts, Divisions, definitions, schedules, safeguards, and placeholders. | prototype_only, non_operative, legal_review_required, parliamentary_counsel_review_required | reports/legislative_architecture.md, reports/legislative_architecture.json | simulator/pages/24_Legislative_Architecture.py | legal_reviewer, tax_reviewer, parliamentary_counsel_reviewer | Architecture maps conceptual locations only. |
| payment_interactions | Payment Interactions | payment_interactions | Placeholder baseline transfer separation, targeting, phase rules, payment stacks, double-counting, and support-incidence previews. | prototype_only, placeholder_only, welfare_policy_review_required | reports/payment_interactions.md, reports/payment_interactions.json | simulator/pages/15_Payment_Interactions.py | welfare_policy_reviewer, legal_reviewer, treasury_methods_reviewer | Payment interaction outputs are placeholders only. |
| release_candidate_pack | V1.5 Release Candidate Pack | overview | Working-paper and release-document package that consolidates current prototype reports, non-claims, calibration blockers, and reviewer routing. | prototype_only, generated_report_available, not_for_real_world_use | None | simulator/pages/25_Executive_Dashboard.py | policy_reviewer, technical_reviewer, hostile_red_team_reviewer | Release pack consolidates existing materials only. |
| repo_guardrails | Repository Guardrails | repo_guardrails | Repository scanning for prohibited paths, credential-like extensions, marker examples, report non-claims, and raw evidence payload markers. | prototype_only, generated_report_available | reports/repo_guardrails.md, reports/repo_guardrails.json | simulator/pages/11_Repository_Guardrails.py | technical_reviewer, privacy_reviewer, cybersecurity_reviewer | Guardrails are repository safety checks only. |
| reviewed_scenarios | Reviewed Scenarios | reviewed_scenarios | Display-control classification for discussion, warning, hidden, non-interpretable, and external-review outputs. | prototype_only, placeholder_only, external_review_required | reports/reviewed_scenarios.md, reports/reviewed_scenarios.json | simulator/pages/19_Reviewed_Scenarios.py | statistical_methods_reviewer, policy_reviewer, hostile_red_team_reviewer | Reviewed scenarios control display only. |
| sector_schedule_expansion | Sector Schedule Expansion | sector_schedules | Validation and report layer for the expanded placeholder schedule library. | prototype_only, generated_report_available, calibration_required | reports/sector_schedule_expansion.md, reports/sector_schedule_expansion.json | simulator/pages/20_Sector_Schedules.py | sector_methods_reviewer, legal_reviewer, tax_reviewer | Expansion report checks placeholders only. |
| sector_schedules | Sector Schedules | sector_schedules | Placeholder YAML sector schedules for automotive, logistics, call centres, accounting, retail fulfilment, and software platforms. | prototype_only, placeholder_only, calibration_required | reports/sector_schedule_expansion.md | simulator/pages/20_Sector_Schedules.py | policy_reviewer, sector_methods_reviewer, legal_reviewer, tax_reviewer | Schedules are placeholders and not legal schedules. |
| sector_stress_matrix | Sector Stress Matrix | sector_stress | Metadata-only cross-sector stress bands, display controls, and do-not-rank warnings. | prototype_only, placeholder_only, external_review_required | reports/sector_stress_matrix.md, reports/sector_stress_matrix.json | simulator/pages/21_Sector_Stress_Matrix.py | policy_reviewer, economic_methods_reviewer, sector_methods_reviewer | Matrix helps review fragility but does not rank sectors. |
| secure_ingestion | Secure Ingestion Controls | secure_ingestion | Default-deny synthetic ingestion controls, marker scanning, redaction metadata, retention metadata, and audit records. | prototype_only, placeholder_only, privacy_review_required | reports/secure_ingestion_controls.md, reports/secure_ingestion_controls.json | simulator/pages/10_Secure_Ingestion_Controls.py | privacy_reviewer, cybersecurity_reviewer, technical_reviewer | Ingestion controls prevent real data from entering the repo. |
| status_risks_docs | Status and Risk Documentation | documentation | Current status, known risks, plan, build log, and release-pack documentation. | prototype_only, documentation, external_review_required | None | None | policy_reviewer, hostile_red_team_reviewer, technical_reviewer | Documentation records blockers and should not be read as approval. |
| transition_funding | Transition Funding | transition_funding | Placeholder transition-payment funding coverage and fiscal linkage previews. | prototype_only, placeholder_only, welfare_policy_review_required | reports/transition_funding.md, reports/transition_funding.json | simulator/pages/14_Transition_Funding.py | welfare_policy_reviewer, treasury_methods_reviewer, legal_reviewer | Transition funding is illustrative only. |
| uncertainty_ranges | Uncertainty Ranges | uncertainty_ranges | Deterministic low/base/high placeholder ranges, stability bands, fragile-output flags, and calibration blockers. | prototype_only, placeholder_only, statistical_methods_review_required | reports/uncertainty_ranges.md, reports/uncertainty_ranges.json | simulator/pages/18_Uncertainty_Ranges.py | statistical_methods_reviewer, technical_reviewer | Ranges prevent false precision but are not calibrated uncertainty. |
| worked_examples | Worked Examples | worked_examples | Illustrative firm examples and generated example, grouped-entity, transfer-pricing, evidence, and calibration reports. | prototype_only, placeholder_only, generated_report_available | reports/example_results.md, reports/grouped_entity_results.md, reports/transfer_pricing_results.md, reports/evidence_requirements.md, reports/calibration_requirements.md | simulator/pages/3_Worked_Examples.py | policy_reviewer, technical_reviewer | Worked examples demonstrate plumbing only. |
| working_paper | V1.5 Working Paper | paper | Working concept paper updated to reference the current V1.5 prototype stack and release-candidate pack. | prototype_only, non_operative, not_for_real_world_use | None | simulator/pages/1_Policy_Paper.py | policy_reviewer, legal_reviewer, tax_reviewer, parliamentary_counsel_reviewer | Paper explains the concept but does not make operative claims. |

## F. Generated Report Map

| Report | Layer | Exists | Generated By | What It Shows | What It Does Not Show | Primary Non-Claim | Reviewer | Read Order |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: |
| reports/executive_dashboard.json | executive_dashboard | True | python scripts/run_executive_dashboard.py | dashboard index data | does not show: readiness score | dashboard navigation only | technical_reviewer | 1 |
| reports/executive_dashboard.md | executive_dashboard | True | python scripts/run_executive_dashboard.py | dashboard and report index | does not show: readiness score | dashboard navigation only | policy_reviewer, technical_reviewer | 1 |
| reports/v1_5_release_candidate_pack.json | release_candidate_pack | True | python scripts/run_v1_5_release_candidate_pack.py | release-candidate pack data | does not show: no readiness score or official status | release packaging only | technical_reviewer | 2 |
| reports/v1_5_release_candidate_pack.md | release_candidate_pack | True | python scripts/run_v1_5_release_candidate_pack.py | release-candidate pack summary | does not show: no readiness score or official status | release packaging only | policy_reviewer, technical_reviewer | 2 |
| reports/example_results.json | worked_examples | True | python scripts/run_examples.py | machine-readable worked example outputs | does not show: calibrated firm outcomes | prototype placeholders only | technical_reviewer | 5 |
| reports/example_results.md | worked_examples | True | python scripts/run_examples.py | worked example formula outputs | does not show: calibrated firm outcomes | prototype placeholders only | technical_reviewer, policy_reviewer | 5 |
| reports/grouped_entity_results.json | worked_examples | True | python scripts/run_examples.py | grouped preview data | does not show: legal grouping results | non-operative preview only | technical_reviewer | 6 |
| reports/grouped_entity_results.md | worked_examples | True | python scripts/run_examples.py | grouped-entity preview outputs | does not show: legal grouping results | non-operative preview only | legal_reviewer, tax_reviewer | 6 |
| reports/transfer_pricing_results.json | worked_examples | True | python scripts/run_examples.py | transfer-pricing preview data | does not show: legal addbacks | non-operative preview only | technical_reviewer | 7 |
| reports/transfer_pricing_results.md | worked_examples | True | python scripts/run_examples.py | transfer-pricing preview outputs | does not show: legal addbacks | non-operative preview only | tax_reviewer, legal_reviewer | 7 |
| reports/sector_schedule_expansion.json | sector_schedule_expansion | True | python scripts/run_sector_schedule_expansion.py | schedule validation data | does not show: official schedule calibration | placeholder schedules only | technical_reviewer | 8 |
| reports/sector_schedule_expansion.md | sector_schedule_expansion | True | python scripts/run_sector_schedule_expansion.py | schedule validation and coverage | does not show: official schedule calibration | placeholder schedules only | sector_methods_reviewer, legal_reviewer | 8 |
| reports/sector_stress_matrix.json | sector_stress_matrix | True | python scripts/run_sector_stress_matrix.py | stress matrix data | does not show: real sector ranking | do-not-rank metadata only | technical_reviewer | 9 |
| reports/sector_stress_matrix.md | sector_stress_matrix | True | python scripts/run_sector_stress_matrix.py | metadata-only sector stress bands | does not show: real sector ranking | do-not-rank metadata only | economic_methods_reviewer, policy_reviewer | 9 |
| reports/behavioural_response_simulation.json | behavioural_response | True | python scripts/run_behavioural_response_simulation.py | response pathway data | does not show: behaviour prediction | do-not-predict synthetic pathways only | technical_reviewer | 10 |
| reports/behavioural_response_simulation.md | behavioural_response | True | python scripts/run_behavioural_response_simulation.py | synthetic response pathways | does not show: behaviour prediction | do-not-predict synthetic pathways only | legal_reviewer, tax_reviewer, hostile_red_team_reviewer | 10 |
| reports/administrative_compliance_workflow.json | administrative_workflow | True | python scripts/run_administrative_compliance_workflow.py | workflow routing data | does not show: ATO enforcement or audit logic | no-enforcement workflow shell only | technical_reviewer | 11 |
| reports/administrative_compliance_workflow.md | administrative_workflow | True | python scripts/run_administrative_compliance_workflow.py | synthetic workflow routing | does not show: ATO enforcement or audit logic | no-enforcement workflow shell only | ato_methods_reviewer, legal_reviewer, privacy_reviewer | 11 |
| reports/legislative_architecture.json | legislative_architecture | True | python scripts/run_legislative_architecture.py | architecture skeleton data | does not show: operative law or legal sufficiency | non-operative skeleton only | technical_reviewer | 12 |
| reports/legislative_architecture.md | legislative_architecture | True | python scripts/run_legislative_architecture.py | non-operative architecture skeleton | does not show: operative law or legal sufficiency | non-operative skeleton only | legal_reviewer, parliamentary_counsel_reviewer | 12 |
| reports/investment_guardrails.json | investment_incidence | True | python scripts/run_investment_guardrails.py | investment and incidence data | does not show: economic validation | placeholder incidence guardrails only | technical_reviewer | 13 |
| reports/investment_guardrails.md | investment_incidence | True | python scripts/run_investment_guardrails.py | investment and incidence guardrails | does not show: economic validation | placeholder incidence guardrails only | economic_methods_reviewer | 13 |
| reports/fiscal_trajectory.json | fiscal_trajectory | True | python scripts/run_fiscal_trajectory.py | fiscal trajectory data | does not show: fiscal forecasts | placeholder fiscal accounting only | technical_reviewer | 14 |
| reports/fiscal_trajectory.md | fiscal_trajectory | True | python scripts/run_fiscal_trajectory.py | placeholder fiscal trajectory outputs | does not show: fiscal forecasts | placeholder fiscal accounting only | treasury_methods_reviewer, economic_methods_reviewer | 14 |
| reports/transition_funding.json | transition_funding | True | python scripts/run_transition_funding.py | transition funding data | does not show: welfare policy or costing | placeholder transition funding only | technical_reviewer | 15 |
| reports/transition_funding.md | transition_funding | True | python scripts/run_transition_funding.py | transition funding coverage previews | does not show: welfare policy or costing | placeholder transition funding only | welfare_policy_reviewer, treasury_methods_reviewer | 15 |
| reports/payment_interactions.json | payment_interactions | True | python scripts/run_payment_interactions.py | payment interaction data | does not show: welfare advice or eligibility law | placeholder payment interactions only | technical_reviewer | 16 |
| reports/payment_interactions.md | payment_interactions | True | python scripts/run_payment_interactions.py | payment interaction previews | does not show: welfare advice or eligibility law | placeholder payment interactions only | welfare_policy_reviewer, legal_reviewer | 16 |
| reports/distributional_scenarios.json | household_distributional | True | python scripts/run_distributional_scenarios.py | synthetic household data | does not show: real household modelling | synthetic household scenarios only | technical_reviewer | 17 |
| reports/distributional_scenarios.md | household_distributional | True | python scripts/run_distributional_scenarios.py | synthetic household scenarios | does not show: real household modelling | synthetic household scenarios only | welfare_policy_reviewer, statistical_methods_reviewer | 17 |
| reports/evidence_requirements.json | evidence_workflow | True | python scripts/run_examples.py | evidence requirement data | does not show: statutory powers or sufficiency | evidence placeholder only | technical_reviewer | 18 |
| reports/evidence_requirements.md | evidence_workflow | True | python scripts/run_examples.py | prototype evidence requirement registry | does not show: statutory powers or sufficiency | evidence placeholder only | legal_reviewer, privacy_reviewer | 18 |
| reports/household_weighting.json | household_weighting | True | python scripts/run_household_weighting.py | synthetic subgroup weighting data | does not show: representative population estimates | synthetic weights only | technical_reviewer | 18 |
| reports/household_weighting.md | household_weighting | True | python scripts/run_household_weighting.py | synthetic subgroup weighting | does not show: representative population estimates | synthetic weights only | statistical_methods_reviewer, welfare_policy_reviewer | 18 |
| reports/mock_evidence_workflow.json | evidence_workflow | True | python scripts/run_evidence_workflow.py | mock workflow data | does not show: real evidence sufficiency | synthetic mock workflow only | technical_reviewer | 19 |
| reports/mock_evidence_workflow.md | evidence_workflow | True | python scripts/run_evidence_workflow.py | synthetic mock evidence workflow | does not show: real evidence sufficiency | synthetic mock workflow only | privacy_reviewer, legal_reviewer | 19 |
| reports/uncertainty_ranges.json | uncertainty_ranges | True | python scripts/run_uncertainty_ranges.py | uncertainty range data | does not show: confidence intervals or forecasts | placeholder uncertainty ranges only | technical_reviewer | 19 |
| reports/uncertainty_ranges.md | uncertainty_ranges | True | python scripts/run_uncertainty_ranges.py | deterministic low/base/high ranges | does not show: confidence intervals or forecasts | placeholder uncertainty ranges only | statistical_methods_reviewer | 19 |
| reports/reviewed_scenarios.json | reviewed_scenarios | True | python scripts/run_reviewed_scenarios.py | reviewed scenario data | does not show: validation or approval | display controls only | technical_reviewer | 20 |
| reports/reviewed_scenarios.md | reviewed_scenarios | True | python scripts/run_reviewed_scenarios.py | display-control review categories | does not show: validation or approval | display controls only | policy_reviewer, statistical_methods_reviewer | 20 |
| reports/secure_ingestion_controls.json | secure_ingestion | True | python scripts/run_ingestion_controls.py | ingestion control data | does not show: real secure evidence platform | default-deny prototype only | technical_reviewer | 20 |
| reports/secure_ingestion_controls.md | secure_ingestion | True | python scripts/run_ingestion_controls.py | secure ingestion controls | does not show: real secure evidence platform | default-deny prototype only | privacy_reviewer, cybersecurity_reviewer | 20 |
| reports/calibration_requirements.json | calibration_shell | True | python scripts/run_examples.py | calibration requirement data | does not show: real calibration | calibration shell only | technical_reviewer | 21 |
| reports/calibration_requirements.md | calibration_shell | True | python scripts/run_examples.py | calibration requirement categories | does not show: real calibration | calibration shell only | statistical_methods_reviewer, treasury_methods_reviewer | 21 |
| reports/repo_guardrails.json | repo_guardrails | True | python scripts/run_repo_guardrails.py | repository guardrail scan data | does not show: complete DLP or cybersecurity validation | prototype repo guardrails only | technical_reviewer | 22 |
| reports/repo_guardrails.md | repo_guardrails | True | python scripts/run_repo_guardrails.py | repository guardrail scan | does not show: complete DLP or cybersecurity validation | prototype repo guardrails only | technical_reviewer, privacy_reviewer | 22 |

## G. Release Documents

| Document | Type | Exists | Purpose | Contains Non-Claims |
| --- | --- | --- | --- | --- |
| release/v1_5_rc/CALIBRATION_BLOCKERS.md | calibration_blockers | True | Consolidated calibration blocker summary. | True |
| release/v1_5_rc/EXTERNAL_REVIEW_ROUTING.md | external_review_routing | True | Suggested external reviewer routing. | True |
| release/v1_5_rc/NON_CLAIM_BOUNDARIES.md | non_claim_boundaries | True | Consolidated boundaries and prohibited inferences. | True |
| release/v1_5_rc/RELEASE_MANIFEST.json | release_manifest_snapshot | True | Static release manifest summary for reviewers. | True |
| release/v1_5_rc/RELEASE_NOTES.md | release_notes | True | Summary of V1.5 release-candidate contents and boundaries. | True |
| release/v1_5_rc/REPORT_MAP.md | report_map | True | Map of generated reports | True |
| release/v1_5_rc/REVIEWER_BRIEFING.md | reviewer_briefing | True | Reviewer-specific reading guide and risks. | True |

## H. Suggested Reviewer Routing

| Reviewer | Layers | Reports | Release Documents | Official Process | Main Reason |
| --- | --- | --- | --- | --- | --- |
| ato_methods_reviewer | administrative_workflow, evidence_workflow, secure_ingestion, repo_guardrails | reports/administrative_compliance_workflow.md, reports/mock_evidence_workflow.md, reports/secure_ingestion_controls.md | release/v1_5_rc/EXTERNAL_REVIEW_ROUTING.md | False | ATO methods reviewers should inspect workflow boundaries without treating them as guidance. |
| economic_methods_reviewer | investment_incidence, sector_stress_matrix, fiscal_trajectory | reports/investment_guardrails.md, reports/sector_stress_matrix.md | release/v1_5_rc/CALIBRATION_BLOCKERS.md | False | Economic reviewers should attack incidence, sector stress, and fiscal assumptions. |
| hostile_red_team_reviewer | behavioural_response, reviewed_scenarios, sector_stress_matrix, repo_guardrails, status_risks_docs | reports/behavioural_response_simulation.md, reports/reviewed_scenarios.md, reports/repo_guardrails.md | release/v1_5_rc/REVIEWER_BRIEFING.md | False | Red-team review should challenge overclaims, stale manifests, and missing blockers. |
| legal_reviewer | legislative_architecture, administrative_workflow, payment_interactions, behavioural_response | reports/legislative_architecture.md, reports/administrative_compliance_workflow.md | release/v1_5_rc/NON_CLAIM_BOUNDARIES.md, release/v1_5_rc/EXTERNAL_REVIEW_ROUTING.md | False | Legal reviewers should attack non-operative boundaries, powers, obligations, and attribution issues. |
| parliamentary_counsel_reviewer | legislative_architecture, working_paper | reports/legislative_architecture.md | release/v1_5_rc/NON_CLAIM_BOUNDARIES.md, release/v1_5_rc/EXTERNAL_REVIEW_ROUTING.md | False | Parliamentary Counsel review is external and the skeleton is non-operative only. |
| policy_reviewer | release_candidate_pack, working_paper, executive_dashboard, reviewed_scenarios, status_risks_docs | reports/v1_5_release_candidate_pack.md, reports/executive_dashboard.md, reports/reviewed_scenarios.md | release/v1_5_rc/RELEASE_NOTES.md, release/v1_5_rc/REVIEWER_BRIEFING.md | False | Policy reviewers should start with scope, boundaries, and display controls. |
| privacy_reviewer | secure_ingestion, evidence_workflow, administrative_workflow, household_distributional | reports/secure_ingestion_controls.md, reports/mock_evidence_workflow.md | release/v1_5_rc/NON_CLAIM_BOUNDARIES.md | False | Privacy reviewers should attack data boundaries and real-data exclusion. |
| statistical_methods_reviewer | household_distributional, household_weighting, uncertainty_ranges, reviewed_scenarios | reports/uncertainty_ranges.md, reports/reviewed_scenarios.md | release/v1_5_rc/CALIBRATION_BLOCKERS.md | False | Statistical reviewers should attack representativeness, uncertainty, and suppression logic. |
| tax_reviewer | core_formula_model, sector_schedules, worked_examples, behavioural_response | reports/transfer_pricing_results.md, reports/sector_schedule_expansion.md | release/v1_5_rc/CALIBRATION_BLOCKERS.md | False | Tax reviewers should focus on AAVA, addback previews, grouping, schedules, and liability boundaries. |
| technical_reviewer | core_formula_model, worked_examples, secure_ingestion, repo_guardrails, executive_dashboard | reports/example_results.md, reports/repo_guardrails.md, reports/executive_dashboard.md | release/v1_5_rc/REPORT_MAP.md | False | Technical reviewers should inspect reproducibility, runners, report schemas, and guardrails. |
| treasury_methods_reviewer | fiscal_trajectory, transition_funding, investment_incidence, calibration_shell | reports/fiscal_trajectory.md, reports/transition_funding.md, reports/investment_guardrails.md | release/v1_5_rc/CALIBRATION_BLOCKERS.md | False | Treasury methods reviewers should attack fiscal, incidence, and funding assumptions. |
| welfare_policy_reviewer | transition_funding, payment_interactions, household_distributional, household_weighting | reports/payment_interactions.md, reports/distributional_scenarios.md | release/v1_5_rc/CALIBRATION_BLOCKERS.md | False | Welfare reviewers should inspect payment interactions, eligibility boundaries, and household synthetic status. |

## I. Calibration Blockers

| Layer ID | Blocker Type | Blocker | Review Needed | Main Reason |
| --- | --- | --- | --- | --- |
| release_candidate_pack | calibration | Release-candidate pack does not calibrate any model or validate any report. | calibration | Release pack consolidates existing materials only. |
| core_formula_model | calibration | OPFTE, FRV, AII, QLC, cap, credit, and rent-rate parameters require external calibration. | calibration | Core formula outputs remain prototype calculations and do not determine tax payable. |
| worked_examples | calibration | Example values are illustrative placeholders and not calibrated firm data. | calibration | Worked examples demonstrate plumbing only. |
| sector_schedules | calibration | Sector output units, OPFTE, FRV, caps, QLC weights, and AII weights are uncalibrated. | calibration | Schedules are placeholders and not legal schedules. |
| sector_schedule_expansion | calibration | Schedule coverage and settings require external calibration and legal attribution review. | calibration | Expansion report checks placeholders only. |
| sector_stress_matrix | calibration | Stress bands are metadata-only and require sector, legal, tax, Treasury, ATO, and methods review. | calibration | Matrix helps review fragility but does not rank sectors. |
| behavioural_response | calibration | Behavioural elasticity, response prevalence, and compliance effects are uncalibrated. | calibration | Pathways are synthetic review prompts only. |
| administrative_workflow | calibration | Workflow thresholds and evidence sufficiency are not calibrated or operationally reviewed. | calibration | Workflow routing organises synthetic cases only. |
| legislative_architecture | calibration | Legislative structure cannot be used without legal, tax, Treasury, ATO, privacy, and policy review. | calibration | Architecture maps conceptual locations only. |
| executive_dashboard | calibration | Dashboard must be updated whenever reports, blockers, or pages change. | calibration | Dashboard is navigation only. |
| evidence_workflow | calibration | Evidence requirements are not tied to real statutory powers or operational systems. | calibration | Mock evidence workflow uses synthetic packets only. |
| secure_ingestion | calibration | Real secure storage, IAM, deletion, DLP, malware scanning, and audit tooling are out of repo. | calibration | Ingestion controls prevent real data from entering the repo. |
| repo_guardrails | calibration | Guardrails require external DLP, sensitive-marker scanning, privacy, legal, and cybersecurity review before real use. | calibration | Guardrails are repository safety checks only. |
| investment_incidence | calibration | Incidence, elasticity, pass-through, and normal-return assumptions are uncalibrated. | calibration | Guardrails flag sensitivity only. |
| fiscal_trajectory | calibration | PAYG, support, superannuation, HELP, GST, company tax, and state effects are uncalibrated. | calibration | Fiscal trajectory is placeholder accounting only. |
| transition_funding | calibration | Population, payment, duration, administration, and participation settings are uncalibrated. | calibration | Transition funding is illustrative only. |
| payment_interactions | calibration | Eligibility, income/household tests, phase rules, double-counting, offsets, and support incidence are uncalibrated. | calibration | Payment interaction outputs are placeholders only. |
| household_distributional | calibration | Household composition, income, cost, welfare, labour-market, and regional parameters are uncalibrated. | calibration | Household cases are synthetic only. |
| household_weighting | calibration | Synthetic weights are not survey weights and require external microdata and weighting review. | calibration | Weighting shell is synthetic and not representative. |
| uncertainty_ranges | calibration | Ranges and stability thresholds are deterministic placeholders. | calibration | Ranges prevent false precision but are not calibrated uncertainty. |
| reviewed_scenarios | calibration | Review categories require external calibration and methods review. | calibration | Reviewed scenarios control display only. |
| calibration_shell | calibration | Real calibration requires authorised external datasets and methods review. | calibration | Shell lists unresolved data needs only. |
| working_paper | calibration | Working paper remains a concept paper and is not calibrated or validated. | calibration | Paper explains the concept but does not make operative claims. |
| status_risks_docs | calibration | Documentation must remain aligned with generated reports and blockers. | calibration | Documentation records blockers and should not be read as approval. |

## J. External Review Blockers

| Layer ID | Blocker Type | Blocker | Review Needed | Main Reason |
| --- | --- | --- | --- | --- |
| release_candidate_pack | external_review | All release contents require external review before any real policy, legal, tax, administrative, economic, welfare, or statistical use. | external_review | Release pack consolidates existing materials only. |
| core_formula_model | external_review | Formula architecture requires legal, tax, Treasury, ATO methods, and economic review. | external_review | Core formula outputs remain prototype calculations and do not determine tax payable. |
| worked_examples | external_review | Example interpretations require technical, policy, legal, tax, and methods review. | external_review | Worked examples demonstrate plumbing only. |
| sector_schedules | external_review | Sector attribution requires legal, tax, Treasury, ATO methods, ABS, and industry review. | external_review | Schedules are placeholders and not legal schedules. |
| sector_schedule_expansion | external_review | Software and digital platform capital-base treatment remains unresolved. | external_review | Expansion report checks placeholders only. |
| sector_stress_matrix | external_review | Do-not-rank treatment must remain visible before wider review. | external_review | Matrix helps review fragility but does not rank sectors. |
| behavioural_response | external_review | Legal, tax, ATO methods, Treasury methods, and behavioural research review are required. | external_review | Pathways are synthetic review prompts only. |
| administrative_workflow | external_review | Legal, tax, ATO methods, privacy, Treasury, and administrative-design review are required. | external_review | Workflow routing organises synthetic cases only. |
| legislative_architecture | external_review | Parliamentary Counsel and constitutional/legal review remain unresolved. | external_review | Architecture maps conceptual locations only. |
| executive_dashboard | external_review | Reviewer routing is a convenience only and does not replace external review. | external_review | Dashboard is navigation only. |
| evidence_workflow | external_review | Legal, privacy, secrecy, ATO methods, and administrative-design review are required. | external_review | Mock evidence workflow uses synthetic packets only. |
| secure_ingestion | external_review | Cybersecurity, privacy, legal, and data-owner review are required. | external_review | Ingestion controls prevent real data from entering the repo. |
| repo_guardrails | external_review | Repository controls are not complete evidence governance. | external_review | Guardrails are repository safety checks only. |
| investment_incidence | external_review | Economic, Treasury, tax, and investment-incidence review are required. | external_review | Guardrails flag sensitivity only. |
| fiscal_trajectory | external_review | Treasury, ATO, PBO, ABS, DSS, and fiscal methods review are required. | external_review | Fiscal trajectory is placeholder accounting only. |
| transition_funding | external_review | DSS, Services Australia, Treasury, PBO, legal, and welfare-policy review are required. | external_review | Transition funding is illustrative only. |
| payment_interactions | external_review | Welfare, DSS, Services Australia, Treasury, PBO, legal, privacy, and tax review are required. | external_review | Payment interaction outputs are placeholders only. |
| household_distributional | external_review | ABS, HILDA, Census, DSS, Services Australia, Treasury, PBO, privacy, welfare, and statistical review are required. | external_review | Household cases are synthetic only. |
| household_weighting | external_review | Statistical, privacy, ABS/HILDA/Census, DSS, Treasury, PBO, welfare, and legal review are required. | external_review | Weighting shell is synthetic and not representative. |
| uncertainty_ranges | external_review | Statistical methods, calibration, data-governance, and policy review are required. | external_review | Ranges prevent false precision but are not calibrated uncertainty. |
| reviewed_scenarios | external_review | Legal, policy, statistical, welfare, and display-control review are required. | external_review | Reviewed scenarios control display only. |
| calibration_shell | external_review | Data-owner, privacy, legal, tax, Treasury, ATO, economic, statistical, welfare, and Parliamentary Counsel review are required. | external_review | Shell lists unresolved data needs only. |
| working_paper | external_review | Legal, tax, Treasury, ATO, Parliamentary Counsel, privacy, statistical, economic, welfare, and policy review are required. | external_review | Paper explains the concept but does not make operative claims. |
| status_risks_docs | external_review | Risk documentation requires hostile, legal, tax, privacy, policy, and methods review. | external_review | Documentation records blockers and should not be read as approval. |

## K. Guardrail / Safety Status

- Source report: reports/repo_guardrails.json
- Exists: True
- Clean: True
- Denied findings: 0
- Warning findings: 52
- Interpretation warning: Guardrail status is a prototype repository-safety signal only, not validation or operational readiness.

## L. Legislative / Legal Boundary

- Legislative architecture material is non-operative and does not create rights, obligations, statutory powers, notices, penalties, enforcement, legal sufficiency, or legislative readiness.
- Legal and Parliamentary Counsel review remain external blockers before any operative drafting.

## M. Tax / ATO / Treasury Boundary

- Formula, schedule, administrative, behavioural, and evidence layers are not ATO guidance, Treasury modelling, tax advice, compliance scoring, or actual-tax-payable analysis.
- Tax, Treasury, ATO methods, transfer-pricing, offshore-attribution, and schedule-authority review remain unresolved.

## N. Household / Welfare Boundary

- Household, payment, weighting, and reviewed-scenario layers are synthetic or placeholder-only.
- They are not real household modelling, welfare advice, eligibility law, Services Australia modelling, population estimates, or validated support-policy outputs.

## O. Fiscal / Economic Boundary

- Fiscal trajectory, transition funding, investment/incidence, and sector stress outputs are not forecasts, economic validation, investment advice, Treasury modelling, or calibrated public-finance estimates.

## P. Statistical / Uncertainty Boundary

- Uncertainty ranges are deterministic low/base/high placeholders only.
- They are not Monte Carlo, confidence intervals, forecasts, statistical validation, or calibrated uncertainty quantification.

## Q. Missing Items / Release Gaps

- No required release-pack documents or indexed reports are missing.

## R. Suggested Next Review Steps

- Use the executive dashboard first for navigation.
- Read the working paper status note and release documents before interpreting generated reports.
- Route findings to legal, tax, Treasury methods, ATO methods, privacy, statistical, economic, welfare, Parliamentary Counsel, technical, and hostile-review paths as appropriate.
- Treat all recommendations as external-review prompts only, not an official process.

## S. Limitations and Future Work

- Private research prototype only.
- Release-candidate pack only.
- Not legal advice.
- Not tax advice.
- Not ATO guidance.
- Not Treasury modelling.
- Not economic validation.
- Not welfare advice.
- Not statistical validation.
- Not compliance scoring.
- Not enforcement.
- Not operational readiness.
- Not legal sufficiency.
- Not legislative readiness.
- Not a readiness score.
- Not official status.
- Not an official review pathway.
- Does not determine actual tax payable.
- Uses no taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- Does not modify firm-level CARSF liability.
- Only packages existing prototype reports, warnings, navigation, review blockers, and working-paper material for external review.
