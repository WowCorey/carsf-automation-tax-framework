# CARSF V1.5 Executive Dashboard Consolidation

Generated at: `2026-05-20T02:07:18+00:00`

## A. Purpose

This dashboard consolidates existing CARSF V1.5 prototype layers, generated reports, Streamlit pages, non-claim profiles, calibration blockers, external-review blockers, suggested review navigation, and reviewer routing.

## B. Non-Claims

- This is a prototype dashboard and report index only. It is not legal advice, tax advice, ATO guidance, Treasury modelling, economic validation, welfare advice, compliance scoring, enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, and not an official review pathway. It does not determine actual tax payable, does not use taxpayer-level data, firm-level confidential data, household microdata, restricted government data, confidential Treasury/PBO material, or unauthorised data, and does not modify firm-level CARSF liability.
- The dashboard only consolidates existing prototype reports, warnings, navigation, and review blockers.
- Suggested review navigation is a reviewer convenience only and is not an official process.
- It creates no readiness score, maturity score, official review status, validation claim, enforcement pathway, or firm-level liability change.

## C. How to Read This Dashboard

Use this as a review navigation index. Read order is suggested review navigation only and is not an official process. Each linked report keeps its own non-claim boundaries.

## D. Prototype Stack Overview

- Total layers: 26
- Total reports indexed: 46
- Reports present: 46
- Reports missing: 0
- Layers with generated reports: 25
- Synthetic-only layers: 10
- Placeholder-only layers: 22
- Non-operative layers: 3
- External-review-required layers: 23
- Calibration-required layers: 19
- Legal-review-required layers: 13
- Tax-review-required layers: 10
- ATO-methods-review-required layers: 13
- Treasury-methods-review-required layers: 17
- Privacy-review-required layers: 12
- Statistical-methods-review-required layers: 8
- real_data_used: False
- readiness_score_created: False
- operational_readiness_claimed: False
- legal_sufficiency_claimed: False
- economic_validation_claimed: False
- firm_level_liability_logic_modified: False

## E. Suggested Review Navigation

| Read Order | Layer ID | Layer Name | Purpose | Official Process | Main Reason |
| ---: | --- | --- | --- | --- | --- |
| 1 | executive_dashboard | Executive Dashboard | Consolidated navigation and report index for the CARSF V1.5 prototype stack. | False | Suggested review navigation only; not an official process. |
| 2 | working_paper | CARSF V1.5 Working Paper | Working paper, formula reference, glossary, and supporting documentation. | False | Suggested review navigation only; not an official process. |
| 3 | status_risks_docs | Current Status and Known Risks | Status, risk, limitation, and implementation documentation for reviewer orientation. | False | Suggested review navigation only; not an official process. |
| 5 | core_formula_model | Core Formula Model | Core placeholder formula mechanics for QLC, HLE, AII, AAVA, levies, caps, and coverage. | False | Suggested review navigation only; not an official process. |
| 5 | worked_examples | Worked Examples | Synthetic worked examples showing formula traces, evidence labels, and limitation notes. | False | Suggested review navigation only; not an official process. |
| 6 | sector_schedule_expansion | Sector Schedule Expansion | Validates schedule coverage, placeholder weights, calibration labels, and non-claim language. | False | Suggested review navigation only; not an official process. |
| 6 | sector_schedules | Sector Schedules | Prototype sector schedule YAML files and canonical output unit metadata. | False | Suggested review navigation only; not an official process. |
| 7 | sector_stress_matrix | Sector Stress Matrix | Metadata-only cross-sector stress matrix with do-not-rank display controls. | False | Suggested review navigation only; not an official process. |
| 8 | behavioural_response | Behavioural Response Simulation | Synthetic behavioural pathway review mapped to pressure bands and countermeasure categories. | False | Suggested review navigation only; not an official process. |
| 9 | administrative_workflow | Administrative Compliance Workflow | Synthetic administrative pathway organisation across evidence bundles, queues, and locked review states. | False | Suggested review navigation only; not an official process. |
| 10 | legislative_architecture | Legislative Architecture Skeleton | Non-operative legislative-style architecture map for Parts, Divisions, definitions, schedules, powers placeholders, safeguards, and blockers. | False | Suggested review navigation only; not an official process. |
| 11 | fiscal_trajectory | Fiscal Trajectory | Placeholder national fiscal trajectory engine for displacement, PAYG erosion, transfer pressure, and residual gaps. | False | Suggested review navigation only; not an official process. |
| 12 | transition_funding | Transition Funding | Placeholder transition-payment funding comparison against automation revenue. | False | Suggested review navigation only; not an official process. |
| 13 | payment_interactions | Payment Interactions | Placeholder baseline separation, targeting, phase rules, stack interactions, and support incidence. | False | Suggested review navigation only; not an official process. |
| 14 | household_distributional | Household Distributional Scenarios | Synthetic household budget stress, re-employment, regional stress, cliff, and shock-band scenarios. | False | Suggested review navigation only; not an official process. |
| 15 | household_weighting | Household Weighting | Synthetic subgroup weighting and aggregation shell with representativeness warnings. | False | Suggested review navigation only; not an official process. |
| 16 | uncertainty_ranges | Uncertainty Ranges | Deterministic low/base/high placeholder ranges and stability checks. | False | Suggested review navigation only; not an official process. |
| 17 | reviewed_scenarios | Reviewed Scenarios | Display-control layer for stable, fragile, range-sensitive, missing-range, or non-interpretable synthetic outputs. | False | Suggested review navigation only; not an official process. |
| 18 | evidence_workflow | Evidence Workflow | Prototype evidence requirements and synthetic mock evidence workflow. | False | Suggested review navigation only; not an official process. |
| 19 | secure_ingestion | Secure Ingestion Controls | Default-deny synthetic evidence ingestion controls and storage-zone checks. | False | Suggested review navigation only; not an official process. |
| 20 | investment_incidence | Investment / Incidence Guardrails | Placeholder investment and incidence guardrails that do not alter final liability. | False | Suggested review navigation only; not an official process. |
| 20 | repo_guardrails | Repository Guardrails | Prototype repository-level scans for prohibited paths, markers, and generated-report non-claims. | False | Suggested review navigation only; not an official process. |
| 21 | calibration_shell | Calibration Shell | Calibration requirements registry and external-data readiness shell. | False | Suggested review navigation only; not an official process. |
| 26 | real_data_feasibility | Real Data Feasibility and Calibration Intake Map | Feasibility map for public aggregate data candidates, restricted-data requirements, realistic placeholders, forbidden repo data, module needs, and Build 27 pilot candidates. | False | Suggested review navigation only; not an official process. |
| 27 | public_data_pilot | Public Data Pilot and Placeholder Anchor Layer | Small public aggregate/source-reference pilot that anchors realistic placeholders while keeping calibration incomplete and restricted data excluded. | False | Suggested review navigation only; not an official process. |
| 28 | public_data_evidence_map | Public Data Pilot Reviewer Evidence Map | Reviewer-facing evidence map over Build 27 public-data pilot outputs without loading new data. | False | Suggested review navigation only; not an official process. |

## F. Layer Index

| Layer ID | Layer Name | Group | Purpose | Status Labels | Primary Reports | Streamlit Pages | Recommended Reviewer | Read Order | Main Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | ---: | --- |
| executive_dashboard | Executive Dashboard | overview | Consolidated navigation and report index for the CARSF V1.5 prototype stack. | implemented_prototype, placeholder_only, not_for_real_world_use | None | simulator/pages/25_Executive_Dashboard.py | policy_reviewer, technical_reviewer | 1 | Reviewers should start with the dashboard to find reports and boundary warnings. |
| working_paper | CARSF V1.5 Working Paper | documentation | Working paper, formula reference, glossary, and supporting documentation. | implemented_prototype, placeholder_only, external_review_required | paper/CARSF_V1_5_WORKING.md, paper/formula_reference.md | simulator/pages/1_Policy_Paper.py | policy_reviewer, legal_reviewer, tax_reviewer, treasury_methods_reviewer, ato_methods_reviewer | 2 | Working paper provides the main concept narrative before detailed reports. |
| status_risks_docs | Current Status and Known Risks | documentation | Status, risk, limitation, and implementation documentation for reviewer orientation. | implemented_prototype, placeholder_only, external_review_required | docs/current_status.md, docs/known_risks.md | simulator/app.py | policy_reviewer, technical_reviewer, legal_reviewer, tax_reviewer | 3 | Status and risks docs should be read before interpreting outputs. |
| core_formula_model | Core Formula Model | formula_core | Core placeholder formula mechanics for QLC, HLE, AII, AAVA, levies, caps, and coverage. | implemented_prototype, placeholder_only, calibration_required, not_for_real_world_use | reports/example_results.md, reports/example_results.json | simulator/pages/2_Tax_Model.py | legal_reviewer, tax_reviewer, treasury_methods_reviewer, ato_methods_reviewer | 5 | Formula concepts are central but remain placeholder and non-operative. |
| worked_examples | Worked Examples | worked_examples | Synthetic worked examples showing formula traces, evidence labels, and limitation notes. | implemented_prototype, generated_report_available, synthetic_only, placeholder_only | reports/example_results.md, reports/example_results.json | simulator/pages/3_Worked_Examples.py | policy_reviewer, technical_reviewer | 5 | Examples help reviewers follow the model but cannot be read as real cases. |
| sector_schedule_expansion | Sector Schedule Expansion | sector_schedules | Validates schedule coverage, placeholder weights, calibration labels, and non-claim language. | implemented_prototype, generated_report_available, placeholder_only, calibration_required | reports/sector_schedule_expansion.md, reports/sector_schedule_expansion.json | simulator/pages/20_Sector_Schedules.py | legal_reviewer, tax_reviewer, treasury_methods_reviewer, ato_methods_reviewer | 6 | Review schedule coverage before sector stress or behavioural layers. |
| sector_schedules | Sector Schedules | sector_schedules | Prototype sector schedule YAML files and canonical output unit metadata. | implemented_prototype, placeholder_only, calibration_required, legal_review_required | reports/sector_schedule_expansion.md, reports/sector_schedule_expansion.json | simulator/pages/20_Sector_Schedules.py | legal_reviewer, tax_reviewer, treasury_methods_reviewer, ato_methods_reviewer | 6 | Schedules frame sector examples but are not official or calibrated. |
| sector_stress_matrix | Sector Stress Matrix | sector_stress | Metadata-only cross-sector stress matrix with do-not-rank display controls. | implemented_prototype, generated_report_available, placeholder_only, external_review_required | reports/sector_stress_matrix.md, reports/sector_stress_matrix.json | simulator/pages/21_Sector_Stress_Matrix.py | legal_reviewer, tax_reviewer, treasury_methods_reviewer, ato_methods_reviewer | 7 | Stress matrix helps target review without creating real sector scores. |
| behavioural_response | Behavioural Response Simulation | behavioural_response | Synthetic behavioural pathway review mapped to pressure bands and countermeasure categories. | implemented_prototype, generated_report_available, synthetic_only, placeholder_only, external_review_required | reports/behavioural_response_simulation.md, reports/behavioural_response_simulation.json | simulator/pages/22_Behavioural_Response.py | policy_reviewer, legal_reviewer, tax_reviewer, ato_methods_reviewer, economic_methods_reviewer | 8 | Behavioural layer identifies review pathways without predicting behaviour. |
| administrative_workflow | Administrative Compliance Workflow | administrative_workflow | Synthetic administrative pathway organisation across evidence bundles, queues, and locked review states. | implemented_prototype, generated_report_available, synthetic_only, non_operative, external_review_required | reports/administrative_compliance_workflow.md, reports/administrative_compliance_workflow.json | simulator/pages/23_Administrative_Workflow.py | ato_methods_reviewer, legal_reviewer, tax_reviewer, privacy_reviewer | 9 | Administrative workflow must be read before legislative architecture boundaries. |
| legislative_architecture | Legislative Architecture Skeleton | legislative_architecture | Non-operative legislative-style architecture map for Parts, Divisions, definitions, schedules, powers placeholders, safeguards, and blockers. | implemented_prototype, generated_report_available, non_operative, legal_review_required, external_review_required | reports/legislative_architecture.md, reports/legislative_architecture.json | simulator/pages/24_Legislative_Architecture.py | legal_reviewer, tax_reviewer, parliamentary_counsel_reviewer, treasury_methods_reviewer, ato_methods_reviewer, privacy_reviewer | 10 | Legislative skeleton is non-operative and reserved for external review. |
| fiscal_trajectory | Fiscal Trajectory | fiscal_trajectory | Placeholder national fiscal trajectory engine for displacement, PAYG erosion, transfer pressure, and residual gaps. | implemented_prototype, generated_report_available, placeholder_only, calibration_required | reports/fiscal_trajectory.md, reports/fiscal_trajectory.json | simulator/pages/13_Fiscal_Trajectory.py | treasury_methods_reviewer, economic_methods_reviewer, policy_reviewer | 11 | Fiscal trajectory sets context for support and funding layers. |
| transition_funding | Transition Funding | transition_funding | Placeholder transition-payment funding comparison against automation revenue. | implemented_prototype, generated_report_available, placeholder_only, calibration_required | reports/transition_funding.md, reports/transition_funding.json | simulator/pages/14_Transition_Funding.py | welfare_policy_reviewer, treasury_methods_reviewer, policy_reviewer | 12 | Transition funding connects fiscal trajectory to support costs. |
| payment_interactions | Payment Interactions | payment_interactions | Placeholder baseline separation, targeting, phase rules, stack interactions, and support incidence. | implemented_prototype, generated_report_available, synthetic_only, placeholder_only, calibration_required | reports/payment_interactions.md, reports/payment_interactions.json | simulator/pages/15_Payment_Interactions.py | welfare_policy_reviewer, treasury_methods_reviewer, legal_reviewer | 13 | Payment interactions explain support-stack caveats before household scenarios. |
| household_distributional | Household Distributional Scenarios | household_distributional | Synthetic household budget stress, re-employment, regional stress, cliff, and shock-band scenarios. | implemented_prototype, generated_report_available, synthetic_only, placeholder_only, calibration_required | reports/distributional_scenarios.md, reports/distributional_scenarios.json | simulator/pages/16_Distributional_Scenarios.py | welfare_policy_reviewer, statistical_methods_reviewer, privacy_reviewer | 14 | Synthetic households illustrate possible stress mechanics only. |
| household_weighting | Household Weighting | household_weighting | Synthetic subgroup weighting and aggregation shell with representativeness warnings. | implemented_prototype, generated_report_available, synthetic_only, placeholder_only, calibration_required | reports/household_weighting.md, reports/household_weighting.json | simulator/pages/17_Household_Weighting.py | statistical_methods_reviewer, privacy_reviewer, policy_reviewer | 15 | Weighting layer is not representative and must be read with warnings. |
| uncertainty_ranges | Uncertainty Ranges | uncertainty_ranges | Deterministic low/base/high placeholder ranges and stability checks. | implemented_prototype, generated_report_available, synthetic_only, placeholder_only, calibration_required | reports/uncertainty_ranges.md, reports/uncertainty_ranges.json | simulator/pages/18_Uncertainty_Ranges.py | statistical_methods_reviewer, policy_reviewer | 16 | Uncertainty ranges should be read before reviewed scenario classifications. |
| reviewed_scenarios | Reviewed Scenarios | reviewed_scenarios | Display-control layer for stable, fragile, range-sensitive, missing-range, or non-interpretable synthetic outputs. | implemented_prototype, generated_report_available, synthetic_only, non_operative, external_review_required | reports/reviewed_scenarios.md, reports/reviewed_scenarios.json | simulator/pages/19_Reviewed_Scenarios.py | statistical_methods_reviewer, policy_reviewer, technical_reviewer | 17 | Reviewed scenarios tell reviewers which point estimates to suppress. |
| evidence_workflow | Evidence Workflow | evidence_workflow | Prototype evidence requirements and synthetic mock evidence workflow. | implemented_prototype, generated_report_available, synthetic_only, placeholder_only | reports/evidence_requirements.md, reports/evidence_requirements.json, reports/mock_evidence_workflow.md, reports/mock_evidence_workflow.json | simulator/pages/8_Evidence_and_Calibration.py, simulator/pages/9_Mock_Evidence_Workflow.py | ato_methods_reviewer, privacy_reviewer, legal_reviewer, technical_reviewer | 18 | Evidence workflow is needed to understand data boundaries. |
| secure_ingestion | Secure Ingestion Controls | secure_ingestion | Default-deny synthetic evidence ingestion controls and storage-zone checks. | implemented_prototype, generated_report_available, synthetic_only, external_review_required | reports/secure_ingestion_controls.md, reports/secure_ingestion_controls.json | simulator/pages/10_Secure_Ingestion_Controls.py | privacy_reviewer, technical_reviewer, legal_reviewer | 19 | Ingestion controls protect no-real-data boundaries. |
| investment_incidence | Investment / Incidence Guardrails | investment_incidence | Placeholder investment and incidence guardrails that do not alter final liability. | implemented_prototype, generated_report_available, placeholder_only, calibration_required | reports/investment_guardrails.md, reports/investment_guardrails.json | simulator/pages/12_Investment_and_Incidence_Guardrails.py | economic_methods_reviewer, treasury_methods_reviewer, tax_reviewer | 20 | Incidence and investment warnings frame interpretation boundaries. |
| repo_guardrails | Repository Guardrails | repo_guardrails | Prototype repository-level scans for prohibited paths, markers, and generated-report non-claims. | implemented_prototype, generated_report_available, placeholder_only | reports/repo_guardrails.md, reports/repo_guardrails.json | simulator/pages/11_Repository_Guardrails.py | technical_reviewer, privacy_reviewer, legal_reviewer | 20 | Guardrails help verify no-real-data discipline. |
| calibration_shell | Calibration Shell | calibration | Calibration requirements registry and external-data readiness shell. | implemented_prototype, generated_report_available, placeholder_only, calibration_required, external_review_required | reports/calibration_requirements.md, reports/calibration_requirements.json | simulator/pages/8_Evidence_and_Calibration.py | statistical_methods_reviewer, treasury_methods_reviewer, ato_methods_reviewer, privacy_reviewer | 21 | Calibration shell summarises unresolved data and methods needs. |
| real_data_feasibility | Real Data Feasibility and Calibration Intake Map | calibration | Feasibility map for public aggregate data candidates, restricted-data requirements, realistic placeholders, forbidden repo data, module needs, and Build 27 pilot candidates. | implemented_prototype, generated_report_available, placeholder_only, calibration_required, external_review_required, not_for_real_world_use | reports/real_data_feasibility.md, reports/real_data_feasibility.json | None | technical_reviewer, privacy_reviewer, statistical_methods_reviewer, treasury_methods_reviewer, ato_methods_reviewer | 26 | Build 26 prepares a safe public-data pilot boundary without loading data. |
| public_data_pilot | Public Data Pilot and Placeholder Anchor Layer | calibration | Small public aggregate/source-reference pilot that anchors realistic placeholders while keeping calibration incomplete and restricted data excluded. | implemented_prototype, generated_report_available, placeholder_only, calibration_required, external_review_required, not_for_real_world_use | reports/public_data_pilot.md, reports/public_data_pilot.json | None | technical_reviewer, privacy_reviewer, statistical_methods_reviewer, treasury_methods_reviewer, ato_methods_reviewer | 27 | Build 27 tests safe public aggregate intake and placeholder anchoring without real calibration. |
| public_data_evidence_map | Public Data Pilot Reviewer Evidence Map | calibration | Reviewer-facing evidence map over Build 27 public-data pilot outputs without loading new data. | implemented_prototype, generated_report_available, placeholder_only, calibration_required, external_review_required, not_for_real_world_use | reports/public_data_evidence_map.md, reports/public_data_evidence_map.json | simulator/pages/29_Public_Data_Evidence_Map.py | technical_reviewer, privacy_reviewer, statistical_methods_reviewer, treasury_methods_reviewer, ato_methods_reviewer | 28 | Build 28 makes the public-data pilot reviewable without adding data or calibration claims. |

## G. Report Index

| Report | Layer ID | Exists | Generated By | Interpretation Warning | Must Not Be Used For | Suggested Read Order |
| --- | --- | --- | --- | --- | --- | ---: |
| reports/executive_dashboard.json | executive_dashboard | True | scripts/run_executive_dashboard.py | This dashboard is generated by the current runner and is navigation only. | must not use for: readiness score, validation, official process | 1 |
| reports/executive_dashboard.md | executive_dashboard | True | scripts/run_executive_dashboard.py | This dashboard is generated by the current runner and is navigation only. | must not use for: readiness score, validation, official process | 1 |
| reports/example_results.json | worked_examples | True | scripts/run_examples.py | Synthetic examples only; not actual tax payable. | must not use for: actual tax payable, legal advice, tax advice, ATO guidance, Treasury modelling, economic validation, operational readiness | 5 |
| reports/example_results.md | worked_examples | True | scripts/run_examples.py | Synthetic examples only; not actual tax payable. | must not use for: actual tax payable, legal advice, tax advice, ATO guidance, Treasury modelling, economic validation, operational readiness | 5 |
| reports/sector_schedule_expansion.json | sector_schedule_expansion | True | scripts/run_sector_schedule_expansion.py | Prototype schedule validation only; not calibrated. | must not use for: actual tax payable, legal advice, tax advice, ATO guidance, Treasury modelling, economic validation, operational readiness | 6 |
| reports/sector_schedule_expansion.md | sector_schedule_expansion | True | scripts/run_sector_schedule_expansion.py | Prototype schedule validation only; not calibrated. | must not use for: actual tax payable, legal advice, tax advice, ATO guidance, Treasury modelling, economic validation, operational readiness | 6 |
| reports/sector_stress_matrix.json | sector_stress_matrix | True | scripts/run_sector_stress_matrix.py | Metadata-only stress bands; not sector rankings. | must not use for: sector ranking, economic validation, actual tax payable | 7 |
| reports/sector_stress_matrix.md | sector_stress_matrix | True | scripts/run_sector_stress_matrix.py | Metadata-only stress bands; not sector rankings. | must not use for: sector ranking, economic validation, actual tax payable | 7 |
| reports/behavioural_response_simulation.json | behavioural_response | True | scripts/run_behavioural_response_simulation.py | Synthetic pathways only; no conduct prediction. | must not use for: behavioural prediction, behavioural elasticity, compliance scoring | 8 |
| reports/behavioural_response_simulation.md | behavioural_response | True | scripts/run_behavioural_response_simulation.py | Synthetic pathways only; no conduct prediction. | must not use for: behavioural prediction, behavioural elasticity, compliance scoring | 8 |
| reports/administrative_compliance_workflow.json | administrative_workflow | True | scripts/run_administrative_compliance_workflow.py | Synthetic pathway organisation only; no real action. | must not use for: enforcement, notices, penalties, compliance scoring, official review pathway | 9 |
| reports/administrative_compliance_workflow.md | administrative_workflow | True | scripts/run_administrative_compliance_workflow.py | Synthetic pathway organisation only; no real action. | must not use for: enforcement, notices, penalties, compliance scoring, official review pathway | 9 |
| reports/legislative_architecture.json | legislative_architecture | True | scripts/run_legislative_architecture.py | Non-operative architecture only; not legal drafting. | must not use for: operative law, legal sufficiency, statutory powers | 10 |
| reports/legislative_architecture.md | legislative_architecture | True | scripts/run_legislative_architecture.py | Non-operative architecture only; not legal drafting. | must not use for: operative law, legal sufficiency, statutory powers | 10 |
| reports/fiscal_trajectory.json | fiscal_trajectory | True | scripts/run_fiscal_trajectory.py | Placeholder fiscal trajectory only; not a forecast. | must not use for: Treasury modelling, forecast, budget costing | 11 |
| reports/fiscal_trajectory.md | fiscal_trajectory | True | scripts/run_fiscal_trajectory.py | Placeholder fiscal trajectory only; not a forecast. | must not use for: Treasury modelling, forecast, budget costing | 11 |
| reports/transition_funding.json | transition_funding | True | scripts/run_transition_funding.py | Placeholder transition-payment funding only. | must not use for: UBI policy, welfare advice, Treasury costing | 12 |
| reports/transition_funding.md | transition_funding | True | scripts/run_transition_funding.py | Placeholder transition-payment funding only. | must not use for: UBI policy, welfare advice, Treasury costing | 12 |
| reports/payment_interactions.json | payment_interactions | True | scripts/run_payment_interactions.py | Placeholder payment interaction mechanics only. | must not use for: welfare eligibility, welfare advice, validated savings | 13 |
| reports/payment_interactions.md | payment_interactions | True | scripts/run_payment_interactions.py | Placeholder payment interaction mechanics only. | must not use for: welfare eligibility, welfare advice, validated savings | 13 |
| reports/distributional_scenarios.json | household_distributional | True | scripts/run_distributional_scenarios.py | Synthetic household scenarios only. | must not use for: real household modelling, population estimate, welfare advice, eligibility law, statistical validation | 14 |
| reports/distributional_scenarios.md | household_distributional | True | scripts/run_distributional_scenarios.py | Synthetic household scenarios only. | must not use for: real household modelling, population estimate, welfare advice, eligibility law, statistical validation | 14 |
| reports/household_weighting.json | household_weighting | True | scripts/run_household_weighting.py | Synthetic weight-record aggregation only. | must not use for: real household modelling, population estimate, welfare advice, eligibility law, statistical validation | 15 |
| reports/household_weighting.md | household_weighting | True | scripts/run_household_weighting.py | Synthetic weight-record aggregation only. | must not use for: real household modelling, population estimate, welfare advice, eligibility law, statistical validation | 15 |
| reports/uncertainty_ranges.json | uncertainty_ranges | True | scripts/run_uncertainty_ranges.py | Deterministic placeholder ranges only. | must not use for: confidence intervals, forecast, statistical validation | 16 |
| reports/uncertainty_ranges.md | uncertainty_ranges | True | scripts/run_uncertainty_ranges.py | Deterministic placeholder ranges only. | must not use for: confidence intervals, forecast, statistical validation | 16 |
| reports/reviewed_scenarios.json | reviewed_scenarios | True | scripts/run_reviewed_scenarios.py | Display-control classifications only. | must not use for: validation, population estimates, official review pathway | 17 |
| reports/reviewed_scenarios.md | reviewed_scenarios | True | scripts/run_reviewed_scenarios.py | Display-control classifications only. | must not use for: validation, population estimates, official review pathway | 17 |
| reports/evidence_requirements.json | evidence_workflow | True | scripts/run_examples.py | Evidence requirements are prototype-only. | must not use for: information-gathering powers, notices, enforcement | 18 |
| reports/evidence_requirements.md | evidence_workflow | True | scripts/run_examples.py | Evidence requirements are prototype-only. | must not use for: information-gathering powers, notices, enforcement | 18 |
| reports/mock_evidence_workflow.json | evidence_workflow | True | scripts/run_evidence_workflow.py | Mock evidence workflow uses synthetic packets only. | must not use for: real evidence ingestion, notices, enforcement | 18 |
| reports/mock_evidence_workflow.md | evidence_workflow | True | scripts/run_evidence_workflow.py | Mock evidence workflow uses synthetic packets only. | must not use for: real evidence ingestion, notices, enforcement | 18 |
| reports/secure_ingestion_controls.json | secure_ingestion | True | scripts/run_ingestion_controls.py | Prototype default-deny ingestion controls only. | must not use for: secure evidence platform, real access control, privacy compliance | 19 |
| reports/secure_ingestion_controls.md | secure_ingestion | True | scripts/run_ingestion_controls.py | Prototype default-deny ingestion controls only. | must not use for: secure evidence platform, real access control, privacy compliance | 19 |
| reports/investment_guardrails.json | investment_incidence | True | scripts/run_investment_guardrails.py | Placeholder investment and incidence guardrails only. | must not use for: investment advice, economic validation, liability modification | 20 |
| reports/investment_guardrails.md | investment_incidence | True | scripts/run_investment_guardrails.py | Placeholder investment and incidence guardrails only. | must not use for: investment advice, economic validation, liability modification | 20 |
| reports/repo_guardrails.json | repo_guardrails | True | scripts/run_repo_guardrails.py | Prototype repository guardrails only. | must not use for: complete DLP, cybersecurity validation, operational readiness | 20 |
| reports/repo_guardrails.md | repo_guardrails | True | scripts/run_repo_guardrails.py | Prototype repository guardrails only. | must not use for: complete DLP, cybersecurity validation, operational readiness | 20 |
| reports/calibration_requirements.json | calibration_shell | True | scripts/run_examples.py | Calibration requirements are unmet placeholders. | must not use for: calibrated output, real-world validation, external data approval | 21 |
| reports/calibration_requirements.md | calibration_shell | True | scripts/run_examples.py | Calibration requirements are unmet placeholders. | must not use for: calibrated output, real-world validation, external data approval | 21 |
| reports/real_data_feasibility.json | real_data_feasibility | True | scripts/run_real_data_feasibility.py | Machine-readable feasibility map only; public-data candidates are not loaded datasets. | must not use for: real data loaded, calibration completed, validation, official status, actual tax payable | 26 |
| reports/real_data_feasibility.md | real_data_feasibility | True | scripts/run_real_data_feasibility.py | Real-data feasibility is intake mapping only; no real data has been loaded and no calibration has occurred. | must not use for: real data loaded, calibration completed, validation, official status, actual tax payable | 26 |
| reports/public_data_pilot.json | public_data_pilot | True | scripts/run_public_data_pilot.py | Machine-readable public-data pilot registry; source references and placeholders remain separate. | must not use for: calibration completed, validation, official status, actual tax payable, readiness score | 27 |
| reports/public_data_pilot.md | public_data_pilot | True | scripts/run_public_data_pilot.py | Public-data pilot is sanity-check-only and placeholder-anchor-only; it is not calibration. | must not use for: calibration completed, validation, official status, actual tax payable, readiness score | 27 |
| reports/public_data_evidence_map.json | public_data_evidence_map | True | scripts/run_public_data_evidence_map.py | Machine-readable evidence map over Build 27 public-data pilot outputs only. | must not use for: calibration completed, validation, official status, actual tax payable, readiness score | 28 |
| reports/public_data_evidence_map.md | public_data_evidence_map | True | scripts/run_public_data_evidence_map.py | Reviewer evidence map only; no new data is loaded and no calibration is completed. | must not use for: calibration completed, validation, official status, actual tax payable, readiness score | 28 |

## H. Streamlit Page Index

| Streamlit Page |
| --- |
| simulator/app.py |
| simulator/pages/10_Secure_Ingestion_Controls.py |
| simulator/pages/11_Repository_Guardrails.py |
| simulator/pages/12_Investment_and_Incidence_Guardrails.py |
| simulator/pages/13_Fiscal_Trajectory.py |
| simulator/pages/14_Transition_Funding.py |
| simulator/pages/15_Payment_Interactions.py |
| simulator/pages/16_Distributional_Scenarios.py |
| simulator/pages/17_Household_Weighting.py |
| simulator/pages/18_Uncertainty_Ranges.py |
| simulator/pages/19_Reviewed_Scenarios.py |
| simulator/pages/1_Policy_Paper.py |
| simulator/pages/20_Sector_Schedules.py |
| simulator/pages/21_Sector_Stress_Matrix.py |
| simulator/pages/22_Behavioural_Response.py |
| simulator/pages/23_Administrative_Workflow.py |
| simulator/pages/24_Legislative_Architecture.py |
| simulator/pages/25_Executive_Dashboard.py |
| simulator/pages/29_Public_Data_Evidence_Map.py |
| simulator/pages/2_Tax_Model.py |
| simulator/pages/3_Worked_Examples.py |
| simulator/pages/8_Evidence_and_Calibration.py |
| simulator/pages/9_Mock_Evidence_Workflow.py |

## I. Non-Claim Profile by Layer

| Layer ID | Non-Claim Flags | Must Not Be Used For | Not For Real-World Use |
| --- | --- | --- | --- |
| executive_dashboard | not_legal_advice, not_tax_advice, not_ato_guidance, not_treasury_modelling, not_economic_validation, not_operational_readiness, not_legal_sufficiency | must not use for: readiness score, maturity score, official review pathway, validation | True |
| core_formula_model | not_actual_tax_payable, not_tax_advice, not_ato_guidance, not_treasury_modelling | must not use for: actual tax payable, legal advice, tax advice, ATO guidance, Treasury modelling, economic validation, operational readiness | True |
| worked_examples | not_actual_tax_payable, not_real_data, not_tax_advice | must not use for: actual tax payable, legal advice, tax advice, ATO guidance, Treasury modelling, economic validation, operational readiness | True |
| sector_schedules | not_ato_guidance, not_treasury_modelling, not_actual_tax_payable | must not use for: actual tax payable, legal advice, tax advice, ATO guidance, Treasury modelling, economic validation, operational readiness | True |
| sector_schedule_expansion | not_ato_guidance, not_treasury_modelling, not_actual_tax_payable | must not use for: actual tax payable, legal advice, tax advice, ATO guidance, Treasury modelling, economic validation, operational readiness | True |
| sector_stress_matrix | not_economic_validation, not_ato_guidance, not_treasury_modelling, not_actual_tax_payable | must not use for: sector ranking, actual tax payable, economic validation, investment advice | True |
| behavioural_response | not_forecast, not_economic_validation, not_compliance_scoring, not_enforcement | must not use for: taxpayer behaviour prediction, behavioural elasticity, compliance scoring, enforcement | True |
| administrative_workflow | not_compliance_scoring, not_enforcement, not_ato_guidance, not_actual_tax_payable | must not use for: enforcement, notices, penalties, compliance scoring, official review pathway | True |
| legislative_architecture | not_operative_law, not_bill, not_legal_advice, not_tax_advice, not_ato_guidance, not_parliamentary_counsel_drafting | must not use for: operative law, legal drafting, legal sufficiency, rights or obligations, statutory powers | True |
| evidence_workflow | not_ato_guidance, not_enforcement, not_actual_tax_payable, not_real_data | must not use for: real evidence ingestion, enforcement, notices, audit validation | True |
| secure_ingestion | not_real_data, not_enforcement, not_ato_guidance | must not use for: secure evidence platform, real access control, legal or privacy compliance | True |
| repo_guardrails | not_real_data, not_compliance_scoring, not_enforcement | must not use for: cybersecurity validation, complete DLP, operational readiness | True |
| investment_incidence | not_economic_validation, not_forecast, not_tax_advice, not_actual_tax_payable | must not use for: investment advice, economic validation, liability modification | True |
| fiscal_trajectory | not_treasury_modelling, not_economic_validation, not_forecast | must not use for: Treasury modelling, forecasts, budget costing | True |
| transition_funding | not_welfare_advice, not_treasury_modelling, not_economic_validation | must not use for: welfare advice, UBI policy, Treasury costing | True |
| payment_interactions | not_welfare_advice, not_economic_validation, not_actual_tax_payable | must not use for: welfare eligibility, welfare advice, validated savings | True |
| household_distributional | not_population_estimate, not_welfare_advice, not_statistical_validation, not_real_data | must not use for: real household modelling, population estimate, welfare advice, eligibility law, statistical validation | True |
| household_weighting | not_population_estimate, not_statistical_validation, not_real_data | must not use for: real household modelling, population estimate, welfare advice, eligibility law, statistical validation | True |
| uncertainty_ranges | not_confidence_interval, not_forecast, not_statistical_validation, not_population_estimate | must not use for: confidence intervals, forecasts, statistical validation | True |
| reviewed_scenarios | not_population_estimate, not_statistical_validation, not_real_data | must not use for: validation, population estimates, clean point estimates for fragile outputs | True |
| calibration_shell | not_real_data, not_economic_validation, not_statistical_validation | must not use for: calibrated output, real-world validation, external data access approval | True |
| working_paper | not_legal_advice, not_tax_advice, not_treasury_modelling, not_ato_guidance | must not use for: legal advice, tax advice, official policy | True |
| status_risks_docs | not_legal_advice, not_tax_advice, not_economic_validation, not_operational_readiness | must not use for: approval, validation, operational readiness | True |
| real_data_feasibility | not_real_data, not_statistical_validation, not_economic_validation, not_actual_tax_payable, not_operational_readiness | must not use for: real data loaded, calibration completed, validation, official status, actual tax payable | True |
| public_data_pilot | not_statistical_validation, not_economic_validation, not_actual_tax_payable, not_operational_readiness | must not use for: calibration completed, validation, official status, actual tax payable, readiness score | True |
| public_data_evidence_map | not_statistical_validation, not_economic_validation, not_actual_tax_payable, not_operational_readiness | must not use for: calibration completed, validation, official status, actual tax payable, readiness score | True |

## J. Calibration Blockers

| Layer ID | Blocker Type | Blocker | External Review Needed | Main Reason |
| --- | --- | --- | --- | --- |
| core_formula_model | calibration | OPFTE, FRV, caps, rates, and schedule coefficients require external calibration. | False | Formula concepts are central but remain placeholder and non-operative. |
| worked_examples | calibration | Worked examples use synthetic inputs and placeholder schedule values. | False | Examples help reviewers follow the model but cannot be read as real cases. |
| sector_schedules | calibration | Sector schedules require official data, legal attribution, and external calibration. | False | Schedules frame sector examples but are not official or calibrated. |
| sector_schedule_expansion | calibration | Schedule weights and thresholds remain uncalibrated. | False | Review schedule coverage before sector stress or behavioural layers. |
| sector_stress_matrix | calibration | Stress bands are metadata-only and require sector calibration. | False | Stress matrix helps target review without creating real sector scores. |
| behavioural_response | calibration | Behavioural elasticity and response evidence are not calibrated. | False | Behavioural layer identifies review pathways without predicting behaviour. |
| administrative_workflow | calibration | Administrative workflow is not an operational design and requires external process review. | False | Administrative workflow must be read before legislative architecture boundaries. |
| legislative_architecture | calibration | Legislative architecture cannot proceed without external calibration of formula and schedule concepts. | False | Legislative skeleton is non-operative and reserved for external review. |
| evidence_workflow | calibration | Evidence confidence and sufficiency are not calibrated. | False | Evidence workflow is needed to understand data boundaries. |
| secure_ingestion | calibration | Real evidence handling requires external secure environment design. | False | Ingestion controls protect no-real-data boundaries. |
| repo_guardrails | calibration | Guardrails are not a complete DLP or security system. | False | Guardrails help verify no-real-data discipline. |
| investment_incidence | calibration | Incidence, investment, and pass-through assumptions are not calibrated. | False | Incidence and investment warnings frame interpretation boundaries. |
| fiscal_trajectory | calibration | Fiscal, labour-market, transfer, and revenue assumptions require calibration. | False | Fiscal trajectory sets context for support and funding layers. |
| transition_funding | calibration | Payment rates, eligibility, population, and fiscal assumptions are placeholders. | False | Transition funding connects fiscal trajectory to support costs. |
| payment_interactions | calibration | Eligibility, household tests, incidence offsets, and payment interactions are placeholders. | False | Payment interactions explain support-stack caveats before household scenarios. |
| household_distributional | calibration | Household composition, income, regional, support, and re-employment assumptions are synthetic. | False | Synthetic households illustrate possible stress mechanics only. |
| household_weighting | calibration | Weights are synthetic and not representative. | False | Weighting layer is not representative and must be read with warnings. |
| uncertainty_ranges | calibration | Ranges are deterministic placeholders, not statistical uncertainty. | False | Uncertainty ranges should be read before reviewed scenario classifications. |
| reviewed_scenarios | calibration | Missing or fragile ranges require calibration before interpretation. | False | Reviewed scenarios tell reviewers which point estimates to suppress. |
| calibration_shell | calibration | Calibration requirements are listed but unmet. | False | Calibration shell summarises unresolved data and methods needs. |
| working_paper | calibration | Working paper contains unresolved policy and calibration questions. | False | Working paper provides the main concept narrative before detailed reports. |
| status_risks_docs | calibration | Known risks and status docs list unresolved calibration and review gaps. | False | Status and risks docs should be read before interpreting outputs. |
| real_data_feasibility | calibration | No real data has been loaded and no calibration has occurred. | False | Build 26 prepares a safe public-data pilot boundary without loading data. |
| real_data_feasibility | calibration | Restricted-data requirements remain access blockers, not data access. | False | Build 26 prepares a safe public-data pilot boundary without loading data. |
| public_data_pilot | calibration | Public aggregate extracts support sanity checks and placeholder anchors only. | False | Build 27 tests safe public aggregate intake and placeholder anchoring without real calibration. |
| public_data_pilot | calibration | Calibration has not been completed and restricted-data blockers remain. | False | Build 27 tests safe public aggregate intake and placeholder anchoring without real calibration. |
| public_data_evidence_map | calibration | Evidence map exposes Build 27 rows for reviewer inspection only. | False | Build 28 makes the public-data pilot reviewable without adding data or calibration claims. |
| public_data_evidence_map | calibration | No new data is loaded and calibration remains incomplete. | False | Build 28 makes the public-data pilot reviewable without adding data or calibration claims. |

## K. External Review Blockers

| Layer ID | Blocker Type | Blocker | External Review Needed | Main Reason |
| --- | --- | --- | --- | --- |
| executive_dashboard | external_review | Dashboard consolidation requires reviewer judgement and does not replace layer-specific review. | True | Reviewers should start with the dashboard to find reports and boundary warnings. |
| core_formula_model | external_review | Tax, Treasury, ATO methods, and legal review are required before any real use. | True | Formula concepts are central but remain placeholder and non-operative. |
| worked_examples | external_review | External methods review is required before any example interpretation. | True | Examples help reviewers follow the model but cannot be read as real cases. |
| sector_schedules | external_review | Schedule authority, Treasury, ATO methods, tax, and legal review required. | True | Schedules frame sector examples but are not official or calibrated. |
| sector_schedule_expansion | external_review | External schedule, legal, Treasury, and ATO methods review required. | True | Review schedule coverage before sector stress or behavioural layers. |
| sector_stress_matrix | external_review | Sector, legal, tax, Treasury, and ATO methods review required. | True | Stress matrix helps target review without creating real sector scores. |
| behavioural_response | external_review | Legal, tax, Treasury, ATO methods, and behavioural research review required. | True | Behavioural layer identifies review pathways without predicting behaviour. |
| administrative_workflow | external_review | Legal, tax, ATO methods, Treasury methods, privacy, and administrative-design review required. | True | Administrative workflow must be read before legislative architecture boundaries. |
| legislative_architecture | external_review | Legal, tax, Treasury, ATO methods, Parliamentary Counsel, privacy, and administrative-design review required. | True | Legislative skeleton is non-operative and reserved for external review. |
| evidence_workflow | external_review | Legal, privacy, secrecy, ATO methods, and evidence-design review required. | True | Evidence workflow is needed to understand data boundaries. |
| secure_ingestion | external_review | Privacy, secrecy, cybersecurity, legal, and administrative review required. | True | Ingestion controls protect no-real-data boundaries. |
| repo_guardrails | external_review | Security, privacy, legal, and repository governance review required. | True | Guardrails help verify no-real-data discipline. |
| investment_incidence | external_review | Economic, Treasury, tax, and investment methods review required. | True | Incidence and investment warnings frame interpretation boundaries. |
| fiscal_trajectory | external_review | Treasury, economic methods, labour-market, and fiscal review required. | True | Fiscal trajectory sets context for support and funding layers. |
| transition_funding | external_review | Welfare policy, Treasury, legal, tax, and fiscal methods review required. | True | Transition funding connects fiscal trajectory to support costs. |
| payment_interactions | external_review | Welfare policy, legal, fiscal, privacy, and Treasury methods review required. | True | Payment interactions explain support-stack caveats before household scenarios. |
| household_distributional | external_review | Statistical, welfare policy, privacy, and external data review required. | True | Synthetic households illustrate possible stress mechanics only. |
| household_weighting | external_review | Statistical methods, privacy, ABS/HILDA/Census access, and external data review required. | True | Weighting layer is not representative and must be read with warnings. |
| uncertainty_ranges | external_review | Statistical methods and external calibration review required. | True | Uncertainty ranges should be read before reviewed scenario classifications. |
| reviewed_scenarios | external_review | Statistical methods, policy, and external calibration review required. | True | Reviewed scenarios tell reviewers which point estimates to suppress. |
| calibration_shell | external_review | External data governance, statistical methods, Treasury, ATO, legal, privacy, and policy review required. | True | Calibration shell summarises unresolved data and methods needs. |
| working_paper | external_review | Policy, legal, tax, Treasury, ATO methods, and Parliamentary Counsel review required. | True | Working paper provides the main concept narrative before detailed reports. |
| status_risks_docs | external_review | Cross-functional external review required before real use. | True | Status and risks docs should be read before interpreting outputs. |
| real_data_feasibility | external_review | Public source licensing, aggregate-only handling, privacy, statistical methods, legal, tax, Treasury, and ATO-methods review remain required before Build 27 loading. | True | Build 26 prepares a safe public-data pilot boundary without loading data. |
| public_data_pilot | external_review | Source licensing, public-data handling, privacy, statistical methods, legal, tax, Treasury, and ATO-methods review remain required before broader use. | True | Build 27 tests safe public aggregate intake and placeholder anchoring without real calibration. |
| public_data_evidence_map | external_review | Source reconciliation, privacy, statistical methods, legal, tax, Treasury, and ATO-methods review remain required. | True | Build 28 makes the public-data pilot reviewable without adding data or calibration claims. |

## L. Guardrail / Safety Status

| Source Report | Exists | Clean | Denied Findings | Warning Findings | Interpretation Warning |
| --- | --- | --- | ---: | ---: | --- |
| reports/repo_guardrails.json | True | True | 0 | 55 | Guardrail status is a prototype repository-safety signal only, not operational readiness or validation. |
| reports/secure_ingestion_controls.json | True | None | 0 | 0 | Guardrail status is a prototype repository-safety signal only, not operational readiness or validation. |
| reports/investment_guardrails.json | True | None | 0 | 0 | Guardrail status is a prototype repository-safety signal only, not operational readiness or validation. |

## M. Legislative / Administrative Boundary Warnings

- Legislative architecture outputs are non-operative and are not a Bill, legal drafting, legal advice, tax advice, ATO guidance, Treasury modelling, legal sufficiency, or legislative readiness.
- Administrative workflow outputs organise synthetic review pathways only and are not enforcement, notices, penalties, compliance scoring, audit logic, or operational readiness.

## N. Household / Distributional Boundary Warnings

- Household, weighting, uncertainty, and reviewed-scenario layers are synthetic or placeholder outputs only.
- They are not real household modelling, population estimates, statistical validation, confidence intervals, forecasts, welfare advice, or eligibility law.

## O. Fiscal / Economic Boundary Warnings

- Fiscal, transition-funding, payment, investment, incidence, and sector-stress layers are placeholders only.
- They are not Treasury modelling, ATO guidance, economic validation, investment advice, welfare validation, official sector ranking, or actual-tax-payable analysis.

## P. Missing Reports or Navigation Gaps

- No required dashboard report paths are missing.

## Q. Recommended Reviewer Routing

| Reviewer | Layers |
| --- | --- |
| ato_methods_reviewer | working_paper, core_formula_model, sector_schedule_expansion, sector_schedules, sector_stress_matrix, behavioural_response, administrative_workflow, legislative_architecture, evidence_workflow, calibration_shell, real_data_feasibility, public_data_pilot, public_data_evidence_map |
| economic_methods_reviewer | behavioural_response, fiscal_trajectory, investment_incidence |
| legal_reviewer | working_paper, status_risks_docs, core_formula_model, sector_schedule_expansion, sector_schedules, sector_stress_matrix, behavioural_response, administrative_workflow, legislative_architecture, payment_interactions, evidence_workflow, secure_ingestion, repo_guardrails |
| parliamentary_counsel_reviewer | legislative_architecture |
| policy_reviewer | executive_dashboard, working_paper, status_risks_docs, worked_examples, behavioural_response, fiscal_trajectory, transition_funding, household_weighting, uncertainty_ranges, reviewed_scenarios |
| privacy_reviewer | administrative_workflow, legislative_architecture, household_distributional, household_weighting, evidence_workflow, secure_ingestion, repo_guardrails, calibration_shell, real_data_feasibility, public_data_pilot, public_data_evidence_map |
| statistical_methods_reviewer | household_distributional, household_weighting, uncertainty_ranges, reviewed_scenarios, calibration_shell, real_data_feasibility, public_data_pilot, public_data_evidence_map |
| tax_reviewer | working_paper, status_risks_docs, core_formula_model, sector_schedule_expansion, sector_schedules, sector_stress_matrix, behavioural_response, administrative_workflow, legislative_architecture, investment_incidence |
| technical_reviewer | executive_dashboard, status_risks_docs, worked_examples, reviewed_scenarios, evidence_workflow, secure_ingestion, repo_guardrails, real_data_feasibility, public_data_pilot, public_data_evidence_map |
| treasury_methods_reviewer | working_paper, core_formula_model, sector_schedule_expansion, sector_schedules, sector_stress_matrix, legislative_architecture, fiscal_trajectory, transition_funding, payment_interactions, investment_incidence, calibration_shell, real_data_feasibility, public_data_pilot, public_data_evidence_map |
| welfare_policy_reviewer | transition_funding, payment_interactions, household_distributional |

## R. Plain-English Interpretation

The dashboard is a map of what exists, where to find it, how to read it, and what not to infer from it. It makes the prototype easier to review without converting any layer into validation, approval, readiness, legal sufficiency, or tax-payable output.

## S. Limitations and Future Review Needs

- Prototype dashboard only.
- Report index only.
- Not legal advice.
- Not tax advice.
- Not ATO guidance.
- Not Treasury modelling.
- Not economic validation.
- Not welfare advice.
- Not compliance scoring.
- Not enforcement.
- Not operational readiness.
- Not legal sufficiency.
- Not legislative readiness.
- Not a readiness score.
- Not an official review pathway.
- Does not determine actual tax payable.
- Uses no taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- Does not modify firm-level CARSF liability.
- Only consolidates existing prototype reports, warnings, navigation, and review blockers.
