# CARSF V1.5 Full Repo Integrity Upgrade / Bug Check / Gap Audit

Generated at: `2026-05-22T02:27:02+00:00`

## A. Purpose

Build 34.5 audits the repository-wide runner, report, manifest, dashboard, documentation, data-boundary, placeholder-boundary, calibration-boundary, scenario-constraint, guardrail, and non-claim state before the next reviewer handoff pack.

## B. Non-Claims

- This is a full repo integrity audit only.
- No new data is loaded by this build.
- This does not fake missing data.
- This does not calibrate the model.
- This does not validate the model.
- This does not prove the model works.
- This does not determine actual tax payable.
- This does not modify firm-level CARSF liability.
- Missing factors requiring data or review remain blocked.
- Public aggregate values remain boundary-limited.
- Placeholders remain placeholders unless already mapped otherwise.
- Scenario constraints remain constraints, not validation.

## C. Audit Scope

- repo structure
- Python modules
- runners
- reports
- JSON outputs
- manifests
- dashboards
- CI
- tests
- guardrails
- missing factors

## D. Repo-Wide Build Coverage Matrix

| Build or Layer | Runner Exists | CI Referenced | Markdown | JSON | Status |
| --- | --- | --- | --- | --- | --- |
| example_results | True | True | True | True | covered |
| grouped_entity_results | True | True | True | True | covered |
| transfer_pricing_results | True | True | True | True | covered |
| evidence_requirements | True | True | True | True | covered |
| calibration_requirements | True | True | True | True | covered |
| sector_schedule_expansion | True | True | True | True | covered |
| sector_stress_matrix | True | True | True | True | covered |
| behavioural_response_simulation | True | True | True | True | covered |
| administrative_compliance_workflow | True | True | True | True | covered |
| legislative_architecture | True | True | True | True | covered |
| executive_dashboard | True | True | True | True | covered |
| v1_5_release_candidate_pack | True | True | True | True | covered |
| external_review_attack_pack | True | True | True | True | covered |
| v1_5_final_rc_integrity_seal | True | True | True | True | covered |
| real_data_feasibility | True | True | True | True | covered |
| public_data_pilot | True | True | True | True | covered |
| public_data_evidence_map | True | True | True | True | covered |
| public_data_consistency_audit | True | True | True | True | covered |
| source_locator_verification_pack | True | True | True | True | covered |
| red_team_reviewer_objections | True | True | True | True | covered |
| public_real_data_loader | True | True | True | True | covered |
| public_data_placeholder_replacement_map | True | True | True | True | covered |
| public_aggregate_calibration_boundary_map | True | True | True | True | covered |
| public_aggregate_scenario_constraint_layer | True | True | True | True | covered |
| full_repo_integrity_upgrade_audit | True | True | True | True | covered |
| mock_evidence_workflow | True | True | True | True | covered |
| secure_ingestion_controls | True | True | True | True | covered |
| investment_guardrails | True | True | True | True | covered |
| fiscal_trajectory | True | True | True | True | covered |
| transition_funding | True | True | True | True | covered |
| payment_interactions | True | True | True | True | covered |
| distributional_scenarios | True | True | True | True | covered |
| household_weighting | True | True | True | True | covered |
| uncertainty_ranges | True | True | True | True | covered |
| reviewed_scenarios | True | True | True | True | covered |
| repo_guardrails | True | True | True | True | covered |

## E. Runner Coverage Matrix

| runner_path | exists | ci_referenced | status |
| --- | --- | --- | --- |
| scripts/run_examples.py | True | True | covered |
| scripts/run_sector_schedule_expansion.py | True | True | covered |
| scripts/run_sector_stress_matrix.py | True | True | covered |
| scripts/run_behavioural_response_simulation.py | True | True | covered |
| scripts/run_administrative_compliance_workflow.py | True | True | covered |
| scripts/run_legislative_architecture.py | True | True | covered |
| scripts/run_executive_dashboard.py | True | True | covered |
| scripts/run_v1_5_release_candidate_pack.py | True | True | covered |
| scripts/run_external_review_attack_pack.py | True | True | covered |
| scripts/run_v1_5_final_rc_integrity_seal.py | True | True | covered |
| scripts/run_real_data_feasibility.py | True | True | covered |
| scripts/run_public_data_pilot.py | True | True | covered |
| scripts/run_public_data_evidence_map.py | True | True | covered |
| scripts/run_public_data_consistency_audit.py | True | True | covered |
| scripts/run_source_locator_verification_pack.py | True | True | covered |
| scripts/run_red_team_reviewer_objections.py | True | True | covered |
| scripts/run_public_real_data_loader.py | True | True | covered |
| scripts/run_public_data_placeholder_replacement_map.py | True | True | covered |
| scripts/run_public_aggregate_calibration_boundary_map.py | True | True | covered |
| scripts/run_public_aggregate_scenario_constraint_layer.py | True | True | covered |
| scripts/run_full_repo_integrity_upgrade_audit.py | True | True | covered |
| scripts/run_evidence_workflow.py | True | True | covered |
| scripts/run_ingestion_controls.py | True | True | covered |
| scripts/run_investment_guardrails.py | True | True | covered |
| scripts/run_fiscal_trajectory.py | True | True | covered |
| scripts/run_transition_funding.py | True | True | covered |
| scripts/run_payment_interactions.py | True | True | covered |
| scripts/run_distributional_scenarios.py | True | True | covered |
| scripts/run_household_weighting.py | True | True | covered |
| scripts/run_uncertainty_ranges.py | True | True | covered |
| scripts/run_reviewed_scenarios.py | True | True | covered |
| scripts/run_repo_guardrails.py | True | True | covered |

## F. Report Coverage Matrix

| report_stem | markdown_report | json_report | markdown_exists | json_exists | status |
| --- | --- | --- | --- | --- | --- |
| example_results | reports/example_results.md | reports/example_results.json | True | True | covered |
| grouped_entity_results | reports/grouped_entity_results.md | reports/grouped_entity_results.json | True | True | covered |
| transfer_pricing_results | reports/transfer_pricing_results.md | reports/transfer_pricing_results.json | True | True | covered |
| evidence_requirements | reports/evidence_requirements.md | reports/evidence_requirements.json | True | True | covered |
| calibration_requirements | reports/calibration_requirements.md | reports/calibration_requirements.json | True | True | covered |
| sector_schedule_expansion | reports/sector_schedule_expansion.md | reports/sector_schedule_expansion.json | True | True | covered |
| sector_stress_matrix | reports/sector_stress_matrix.md | reports/sector_stress_matrix.json | True | True | covered |
| behavioural_response_simulation | reports/behavioural_response_simulation.md | reports/behavioural_response_simulation.json | True | True | covered |
| administrative_compliance_workflow | reports/administrative_compliance_workflow.md | reports/administrative_compliance_workflow.json | True | True | covered |
| legislative_architecture | reports/legislative_architecture.md | reports/legislative_architecture.json | True | True | covered |
| executive_dashboard | reports/executive_dashboard.md | reports/executive_dashboard.json | True | True | covered |
| v1_5_release_candidate_pack | reports/v1_5_release_candidate_pack.md | reports/v1_5_release_candidate_pack.json | True | True | covered |
| external_review_attack_pack | reports/external_review_attack_pack.md | reports/external_review_attack_pack.json | True | True | covered |
| v1_5_final_rc_integrity_seal | reports/v1_5_final_rc_integrity_seal.md | reports/v1_5_final_rc_integrity_seal.json | True | True | covered |
| real_data_feasibility | reports/real_data_feasibility.md | reports/real_data_feasibility.json | True | True | covered |
| public_data_pilot | reports/public_data_pilot.md | reports/public_data_pilot.json | True | True | covered |
| public_data_evidence_map | reports/public_data_evidence_map.md | reports/public_data_evidence_map.json | True | True | covered |
| public_data_consistency_audit | reports/public_data_consistency_audit.md | reports/public_data_consistency_audit.json | True | True | covered |
| source_locator_verification_pack | reports/source_locator_verification_pack.md | reports/source_locator_verification_pack.json | True | True | covered |
| red_team_reviewer_objections | reports/red_team_reviewer_objections.md | reports/red_team_reviewer_objections.json | True | True | covered |
| public_real_data_loader | reports/public_real_data_loader.md | reports/public_real_data_loader.json | True | True | covered |
| public_data_placeholder_replacement_map | reports/public_data_placeholder_replacement_map.md | reports/public_data_placeholder_replacement_map.json | True | True | covered |
| public_aggregate_calibration_boundary_map | reports/public_aggregate_calibration_boundary_map.md | reports/public_aggregate_calibration_boundary_map.json | True | True | covered |
| public_aggregate_scenario_constraint_layer | reports/public_aggregate_scenario_constraint_layer.md | reports/public_aggregate_scenario_constraint_layer.json | True | True | covered |
| full_repo_integrity_upgrade_audit | reports/full_repo_integrity_upgrade_audit.md | reports/full_repo_integrity_upgrade_audit.json | True | True | covered |
| mock_evidence_workflow | reports/mock_evidence_workflow.md | reports/mock_evidence_workflow.json | True | True | covered |
| secure_ingestion_controls | reports/secure_ingestion_controls.md | reports/secure_ingestion_controls.json | True | True | covered |
| investment_guardrails | reports/investment_guardrails.md | reports/investment_guardrails.json | True | True | covered |
| fiscal_trajectory | reports/fiscal_trajectory.md | reports/fiscal_trajectory.json | True | True | covered |
| transition_funding | reports/transition_funding.md | reports/transition_funding.json | True | True | covered |
| payment_interactions | reports/payment_interactions.md | reports/payment_interactions.json | True | True | covered |
| distributional_scenarios | reports/distributional_scenarios.md | reports/distributional_scenarios.json | True | True | covered |
| household_weighting | reports/household_weighting.md | reports/household_weighting.json | True | True | covered |
| uncertainty_ranges | reports/uncertainty_ranges.md | reports/uncertainty_ranges.json | True | True | covered |
| reviewed_scenarios | reports/reviewed_scenarios.md | reports/reviewed_scenarios.json | True | True | covered |
| repo_guardrails | reports/repo_guardrails.md | reports/repo_guardrails.json | True | True | covered |

## G. JSON/Markdown Result Coverage

| report_path | false_flags_clean | status |
| --- | --- | --- |
| reports/public_real_data_loader.json | True | clean |
| reports/public_data_placeholder_replacement_map.json | True | clean |
| reports/public_aggregate_calibration_boundary_map.json | True | clean |
| reports/public_aggregate_scenario_constraint_layer.json | True | clean |

## H. CI Coverage

- CI references the full repo audit runner after the public aggregate scenario constraint layer and before repository guardrails.
- CI YAML parsing now covers schedules, examples, data, and release.

## I. Dashboard Coverage

| artifact | expected_reference | reference_present | status |
| --- | --- | --- | --- |
| data/dashboard/executive_dashboard_manifest.yaml | full_repo_integrity_upgrade_audit | True | covered |
| data/dashboard/executive_dashboard_manifest.yaml | reports/full_repo_integrity_upgrade_audit.md | True | covered |
| data/dashboard/executive_dashboard_manifest.yaml | reports/full_repo_integrity_upgrade_audit.json | True | covered |

## J. Release Manifest Coverage

| artifact | expected_reference | reference_present | status |
| --- | --- | --- | --- |
| data/release/v1_5_release_manifest.yaml | full_repo_integrity_upgrade_audit | True | covered |
| data/release/v1_5_release_manifest.yaml | reports/full_repo_integrity_upgrade_audit.md | True | covered |
| data/release/v1_5_release_manifest.yaml | reports/full_repo_integrity_upgrade_audit.json | True | covered |
| release/v1_5_rc/REPORT_MAP.md | reports/full_repo_integrity_upgrade_audit.md | True | covered |
| release/v1_5_rc/REPORT_MAP.md | run_full_repo_integrity_upgrade_audit.py | True | covered |

## K. Documentation Coverage

| artifact | expected_reference | reference_present | status |
| --- | --- | --- | --- |
| README.md | file exists | True | covered |
| BUILD_LOG.md | file exists | True | covered |
| docs/current_status.md | file exists | True | covered |
| docs/known_risks.md | file exists | True | covered |
| docs/calibration_shell.md | file exists | True | covered |
| docs/v1_5_plan.md | file exists | True | covered |
| docs/public_data_pilot.md | file exists | True | covered |
| docs/public_real_data_loader.md | file exists | True | covered |
| docs/public_data_placeholder_replacement_map.md | file exists | True | covered |
| docs/public_aggregate_calibration_boundary_map.md | file exists | True | covered |
| docs/public_aggregate_scenario_constraint_layer.md | file exists | True | covered |
| docs/full_repo_integrity_upgrade_audit.md | file exists | True | covered |
| release/v1_5_rc/RELEASE_NOTES.md | file exists | True | covered |
| release/v1_5_rc/CALIBRATION_BLOCKERS.md | file exists | True | covered |
| release/v1_5_rc/NON_CLAIM_BOUNDARIES.md | file exists | True | covered |
| release/v1_5_rc/REPORT_MAP.md | file exists | True | covered |
| release/v1_5_rc/RELEASE_MANIFEST.json | file exists | True | covered |

## L. Public Data Boundary Audit

| guardrail_id | category | covered | evidence | status |
| --- | --- | --- | --- | --- |
| public_value_source_url | public_data_boundary | True | source_url | clean |
| public_value_source_locator | public_data_boundary | True | source_locator | clean |
| public_value_unit | public_data_boundary | True | unit | clean |
| public_value_period | public_data_boundary | True | period | clean |
| public_value_geography | public_data_boundary | True | geography | clean |
| public_value_must_not_infer | public_data_boundary | True | must_not_infer | clean |
| public_values_forbidden_flags | public_data_boundary | True | loaded public aggregate values keep restricted/private flags false | clean |

## M. Placeholder Boundary Audit

| guardrail_id | category | covered | evidence | status |
| --- | --- | --- | --- | --- |
| placeholders_are_realistic_placeholder | placeholder_boundary | True | placeholders_are_realistic_placeholder | clean |
| placeholders_not_real_data | placeholder_boundary | True | placeholders_not_real_data | clean |
| placeholders_not_calibrated | placeholder_boundary | True | placeholders_not_calibrated | clean |

## N. Calibration Boundary Audit

| guardrail_id | category | covered | evidence | status |
| --- | --- | --- | --- | --- |
| calibration_boundary_new_data_loaded | calibration_boundary | True | new_data_loaded | clean |
| calibration_boundary_calibration_completed | calibration_boundary | True | calibration_completed | clean |
| calibration_boundary_validation_claimed | calibration_boundary | True | validation_claimed | clean |
| calibration_boundary_actual_tax_payable_determined | calibration_boundary | True | actual_tax_payable_determined | clean |
| calibration_boundary_official_status_claimed | calibration_boundary | True | official_status_claimed | clean |
| calibration_boundary_firm_level_liability_logic_modified | calibration_boundary | True | firm_level_liability_logic_modified | clean |

## O. Scenario Constraint Audit

| guardrail_id | category | covered | evidence | status |
| --- | --- | --- | --- | --- |
| scenario_constraint_new_data_loaded | scenario_constraint | True | new_data_loaded | clean |
| scenario_constraint_calibration_completed | scenario_constraint | True | calibration_completed | clean |
| scenario_constraint_validation_claimed | scenario_constraint | True | validation_claimed | clean |
| scenario_constraint_actual_tax_payable_determined | scenario_constraint | True | actual_tax_payable_determined | clean |
| scenario_constraint_official_status_claimed | scenario_constraint | True | official_status_claimed | clean |
| scenario_constraint_firm_level_liability_logic_modified | scenario_constraint | True | firm_level_liability_logic_modified | clean |

## P. Guardrail Audit

| guardrail_id | category | covered | evidence | status |
| --- | --- | --- | --- | --- |
| guardrail_1 | guardrail_boundary | True | restricted data | clean |
| guardrail_2 | guardrail_boundary | True | personal data | clean |
| guardrail_3 | guardrail_boundary | True | taxpayer-level data | clean |
| guardrail_4 | guardrail_boundary | True | firm-confidential data | clean |
| guardrail_5 | guardrail_boundary | True | household microdata | clean |
| guardrail_6 | guardrail_boundary | True | ABS DataLab microdata | clean |
| guardrail_7 | guardrail_boundary | True | HILDA microdata | clean |
| guardrail_8 | guardrail_boundary | True | DSS / Services Australia records | clean |
| guardrail_9 | guardrail_boundary | True | ATO taxpayer records | clean |
| guardrail_10 | guardrail_boundary | True | confidential Treasury / PBO material | clean |
| guardrail_11 | guardrail_boundary | True | bank records | clean |
| guardrail_12 | guardrail_boundary | True | pay-record documents | clean |
| guardrail_13 | guardrail_boundary | True | tax-file identifiers | clean |
| guardrail_14 | guardrail_boundary | True | calibration-complete claims | clean |
| guardrail_15 | guardrail_boundary | True | validation claims | clean |
| guardrail_16 | guardrail_boundary | True | actual tax payable claims | clean |
| guardrail_17 | guardrail_boundary | True | firm liability claims | clean |
| guardrail_18 | guardrail_boundary | True | official status claims | clean |
| guardrail_19 | guardrail_boundary | True | readiness or maturity scores | clean |

## Q. Non-Claim Boundary Audit

| artifact | required_phrases_present | missing_phrases | status |
| --- | --- | --- | --- |
| reports/public_aggregate_scenario_constraint_layer.md | True | [] | clean |
| reports/public_aggregate_calibration_boundary_map.md | True | [] | clean |
| reports/public_data_placeholder_replacement_map.md | True | [] | clean |
| release/v1_5_rc/NON_CLAIM_BOUNDARIES.md | True | [] | clean |
| docs/full_repo_integrity_upgrade_audit.md | True | [] | clean |

## R. Safe Fixes Applied

| fix_id | description | files_changed | status |
| --- | --- | --- | --- |
| safe_fix_ci_release_yaml_parse | Extended CI YAML parsing to include release YAML files. | ['.github/workflows/ci.yml'] | fixed |
| safe_fix_full_audit_runner_wiring | Added full repo audit runner, manifest, reports, CI entry, and report/release/dashboard references. | ['scripts/run_full_repo_integrity_upgrade_audit.py', 'data/audit/full_repo_integrity_upgrade_manifest.yaml', 'reports/full_repo_integrity_upgrade_audit.md', 'reports/full_repo_integrity_upgrade_audit.json'] | fixed |
| safe_fix_handoff_docs | Added Build 34.5 documentation and release references without changing data or liability logic. | ['docs/full_repo_integrity_upgrade_audit.md', 'release/v1_5_rc/REPORT_MAP.md'] | fixed |

## S. Bugs Fixed

| finding_id | severity | category | title | details |
| --- | --- | --- | --- | --- |
| ci_release_yaml_parse_gap | low | ci_gap | CI YAML parse did not include release YAML files. | The parse step now covers schedules, examples, data, and release. |
| full_repo_audit_missing_before_build_34_5 | medium | runner_gap | No whole-repo integrity/gap audit runner existed before this build. | Build 34.5 adds the runner, report, manifest, tests, and CI entry. |

## T. Missing Factors Identified

| missing_factor_id | factor_name | category | gap_description | blocking_status |
| --- | --- | --- | --- | --- |
| missing_factor_01_labour_cost_anchors | Labour cost anchors | public_data | Fair Work anchors exist but do not represent all labour costs. | requires_data |
| missing_factor_02_wage_variation | Wage variation | data_gap | Public wage anchors do not cover occupation, region, award, enterprise agreement, or hours variation. | requires_data |
| missing_factor_03_casual_loading | Casual loading | public_data | Casual loading is represented as a public anchor but not full casual employment cost. | requires_data |
| missing_factor_04_super_pressure | Superannuation contribution pressure | public_data | Super guarantee rate is loaded but employer behaviour remains unknown. | requires_data |
| missing_factor_05_payg_erosion | PAYG erosion assumptions | calibration_gap | PAYG erosion cannot be estimated from the current public aggregate set. | requires_data |
| missing_factor_06_corporate_tax_scale | Corporate tax scale | public_data | ATO public aggregate values provide scale context only. | documented |
| missing_factor_07_fiscal_context | Fiscal trajectory context | public_data | Budget aggregates provide context and bounds only. | documented |
| missing_factor_08_transition_funding | Transition funding context | public_data | Transition funding remains placeholder/context-only. | requires_data |
| missing_factor_09_household_limits | Household distributional limits | restricted_data | Household outputs remain synthetic without microdata. | requires_data |
| missing_factor_10_payment_limits | Welfare/payment interaction limits | restricted_data | Payment interactions need welfare records and policy review. | requires_data |
| missing_factor_11_sector_schedule_limits | Sector schedule limits | external_review | Sector schedules remain placeholder and need sector review. | requires_data |
| missing_factor_12_sector_stress_limits | Sector stress limits | external_review | Stress bands are metadata-only. | requires_data |
| missing_factor_13_behavioural_response | Behavioural response/gaming risks | calibration_gap | Behavioural pathways remain synthetic. | requires_data |
| missing_factor_14_admin_limits | Administrative compliance limits | legal_review | Workflow is synthetic and not ATO process. | requires_data |
| missing_factor_15_legislative_limits | Legislative architecture limits | legal_review | Legislative skeleton is non-operative. | requires_data |
| missing_factor_16_data_provenance | Data provenance | public_data | Public aggregate provenance is recorded; external verification remains absent. | documented |
| missing_factor_17_source_locators | Source locators | public_data | Locators are recorded for loaded values but not externally verified. | documented |
| missing_factor_18_real_public_values | Real public aggregate values | public_data | Ten public aggregate values are loaded but boundary-limited. | documented |
| missing_factor_19_placeholder_replacement | Placeholder replacement | placeholder_boundary | Some placeholders are replaced or narrowed by anchors but not calibrated. | requires_data |
| missing_factor_20_calibration_boundaries | Calibration boundaries | calibration_gap | Boundaries are mapped but calibration remains absent. | requires_data |
| missing_factor_21_scenario_constraints | Scenario constraints | scenario_constraint | Scenario outputs are constrained but not validated. | requires_data |
| missing_factor_22_non_interpretable | Non-interpretable outputs | scenario_constraint | Non-interpretable treatment is present but needs reviewer handoff clarity. | documented |
| missing_factor_23_hidden_dashboard | Hidden dashboard outputs | dashboard_gap | Hidden outputs are documented but should be packaged for reviewers. | documented |
| missing_factor_24_external_review | External review dependencies | external_review | External review remains unresolved. | requires_data |
| missing_factor_25_legal_review | Legal review dependencies | legal_review | Legal sufficiency is out of repo. | requires_data |
| missing_factor_26_tax_review | Tax review dependencies | tax_review | Tax treatment and ATO methods remain external. | requires_data |
| missing_factor_27_economic_review | Economic review dependencies | economic_review | Incidence, pass-through, and sufficiency remain external. | requires_data |
| missing_factor_28_statistical_review | Statistical review dependencies | statistical_review | Representativeness and uncertainty remain external. | requires_data |
| missing_factor_29_restricted_blockers | Restricted-data blockers | data_gap | Taxpayer, firm, household, and welfare microdata remain unavailable in repo. | requires_data |
| missing_factor_30_reviewer_handoff | Reviewer handoff readiness | docs_gap | A next handoff pack should package audit outputs for reviewers. | documented |

## U. Missing Data Dependencies

| dependency_id | data_needed | current_status | restricted_data_required | can_be_loaded_now | why_not_loaded |
| --- | --- | --- | --- | --- | --- |
| restricted_ato_taxpayer | ATO taxpayer-level records | not loaded | True | False | Out of repo scope or requires authorised access and review. |
| firm_confidential | Firm confidential revenue/cost records | not loaded | True | False | Out of repo scope or requires authorised access and review. |
| household_microdata | Household microdata | not loaded | True | False | Out of repo scope or requires authorised access and review. |
| welfare_records | DSS / Services Australia payment records | not loaded | True | False | Out of repo scope or requires authorised access and review. |
| abs_datalab | ABS DataLab labour and industry microdata | not loaded | True | False | Out of repo scope or requires authorised access and review. |
| hilda | HILDA microdata | not loaded | True | False | Out of repo scope or requires authorised access and review. |
| treasury_pbo | Confidential Treasury / PBO material | not loaded | True | False | Out of repo scope or requires authorised access and review. |
| behavioural | Behavioural elasticity evidence | not loaded | False | False | Out of repo scope or requires authorised access and review. |

## V. External Review Dependencies

| review_id | review_type | why_required | blocking_status | recommended_reviewer_profile |
| --- | --- | --- | --- | --- |
| review_legal | legal | Legal review is required for legislative architecture, powers, attribution, safeguards, and boundaries. | requires_external_review | legal reviewer with CARSF boundary brief |
| review_tax | tax | Tax review is required for attribution, deductibility, PAYG, company tax, and ATO-methods boundaries. | requires_external_review | tax reviewer with CARSF boundary brief |
| review_economic | economic | Economic review is required for incidence, pass-through, labour displacement, and fiscal interpretation. | requires_external_review | economic reviewer with CARSF boundary brief |
| review_statistical | statistical | Statistical review is required for representativeness, uncertainty, weighting, and scenario interpretation. | requires_external_review | statistical reviewer with CARSF boundary brief |
| review_administrative | administrative | Administrative review is required for workflow feasibility and evidence process boundaries. | requires_external_review | administrative reviewer with CARSF boundary brief |
| review_domain | domain | Domain review is required for sector schedules and sector stress assumptions. | requires_external_review | domain reviewer with CARSF boundary brief |
| review_public_finance | public finance | Public finance review is required before fiscal context can be interpreted beyond public aggregate bounds. | requires_external_review | public finance reviewer with CARSF boundary brief |
| review_welfare | welfare | Welfare review is required for payment interactions, support adequacy, and household pressure boundaries. | requires_external_review | welfare reviewer with CARSF boundary brief |
| review_data_governance | data governance | Data governance review is required before any restricted or confidential source could be considered. | requires_external_review | data governance reviewer with CARSF boundary brief |

## W. Items Blocked Inside Repo

| gap_id | category | description | status | recommended_action |
| --- | --- | --- | --- | --- |
| gap_restricted_data | data_gap | Restricted administrative and microdata dependencies remain outside repo scope. | blocked | Carry into data dependency register. |
| gap_external_review | external_review_gap | Legal, tax, economic, statistical, welfare, data governance, and domain review remain unresolved. | requires_external_review | Carry into reviewer handoff. |
| gap_calibration | calibration_gap | Calibration has not been performed and cannot be performed from current public aggregate data alone. | blocked | Preserve boundary maps and do not overclaim. |

## X. What The Repo Can Currently Claim

- The repo contains prototype reports, manifests, guardrails, and public aggregate boundary maps for reviewer inspection.
- Build 31 public aggregate values are source-located and boundary-limited.
- Builds 32-34 map placeholder, calibration-boundary, and scenario-display constraints without loading new data.
- Repository guardrails currently report no denied findings.

## Y. What The Repo Must Not Claim

- calibration
- validation
- actual tax payable
- firm-level CARSF liability
- official status
- legal sufficiency
- operational readiness
- ATO guidance
- Treasury modelling
- PBO costing
- readiness score
- maturity score

## Z. Recommended Next Builds

- Option A: Build 35 - Public Data Reviewer Handoff Pack V2.
- Option B: Build 35 - Gap Closure Sprint 1 for safe, internal, non-data, non-claim gaps.

## Summary Flags

- full_repo_integrity_audit_created: True
- safe_fixes_applied: True
- critical_findings_total: 0
- critical_findings_fixed: 0
- critical_findings_remaining: 0
- high_findings_total: 0
- high_findings_fixed: 0
- high_findings_remaining: 0
- medium_findings_total: 1
- medium_findings_fixed: 1
- medium_findings_remaining: 0
- runner_coverage_complete: True
- report_coverage_complete: True
- json_report_coverage_complete: True
- dashboard_coverage_complete: True
- release_manifest_coverage_complete: True
- docs_coverage_complete: True
- public_data_boundary_clean: True
- placeholder_boundary_clean: True
- calibration_boundary_clean: True
- scenario_constraint_boundary_clean: True
- guardrails_clean: True
- non_claim_boundaries_clean: True
- forbidden_claim_findings: 0
- new_data_loaded: False
- restricted_data_loaded: False
- personal_data_loaded: False
- taxpayer_level_data_loaded: False
- firm_confidential_data_loaded: False
- household_microdata_loaded: False
- calibration_completed: False
- validation_claimed: False
- actual_tax_payable_determined: False
- official_status_claimed: False
- firm_level_liability_logic_modified: False
