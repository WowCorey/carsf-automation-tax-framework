# CARSF V1.5 External Review Attack Pack

Generated at: `2026-05-20T02:07:19+00:00`

## A. Purpose

This report turns V1.5 release-candidate limitations into reviewer challenge questions, failure modes, boundary checks, report attack rows, and layer attack rows.

## B. Non-Claims

- This is an attack pack for external review. It does not mean external review has been completed, does not mean approval has been granted, does not mean validation has occurred, is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare validation, not statistical validation, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, not official status, and not an official review pathway. It does not determine actual tax payable, does not use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, and does not modify firm-level CARSF liability.
- The attack pack only structures questions, challenges, failure modes, boundary checks, and review routes for external reviewers.
- Challenge severity labels are not risk scores, not validation outcomes, not approval statuses, and not readiness ratings.
- review_completed: False
- approval_claimed: False
- validation_claimed: False
- readiness_score_created: False
- legal_sufficiency_claimed: False
- operational_readiness_claimed: False
- legislative_readiness_claimed: False
- official_status_claimed: False
- real_data_used: False
- firm_level_liability_logic_modified: False

## C. How to Use the Attack Pack

Use this as a challenge map. Reviewers should record issues, missing evidence, and required follow-up; they should not treat challenge severity as validation, approval, readiness, or a score.

- Total review tracks: 12
- Total attack questions: 126
- Total failure modes: 60
- Total boundary checks: 18
- Total report attack rows: 52
- Total layer attack rows: 27
- Total release documents: 17
- Release documents present: 17
- Release documents missing: 0
- Reports referenced: 52
- Reports missing: 0
- Layers referenced: 27
- Unknown layers: 0
- Tracks with required question count: 12
- Tracks missing required question count: 0
- review_completed: False
- approval_claimed: False
- validation_claimed: False
- readiness_score_created: False
- legal_sufficiency_claimed: False
- operational_readiness_claimed: False
- legislative_readiness_claimed: False
- official_status_claimed: False
- real_data_used: False
- firm_level_liability_logic_modified: False

## D. Review Track Index

| Track | Reviewer Type | Inspect First | Layers | Reports | Questions | Failure Modes |
| --- | --- | --- | --- | --- | ---: | ---: |
| ATO Methods Reviewer | ato_methods_reviewer | reports/administrative_compliance_workflow.md, reports/mock_evidence_workflow.md, reports/secure_ingestion_controls.md | administrative_workflow, evidence_workflow, secure_ingestion, behavioural_response | reports/administrative_compliance_workflow.md, reports/mock_evidence_workflow.md, reports/secure_ingestion_controls.md, reports/behavioural_response_simulation.md | 10 | 5 |
| Economic Methods Reviewer | economic_methods_reviewer | reports/investment_guardrails.md, reports/sector_stress_matrix.md, reports/behavioural_response_simulation.md | investment_incidence, sector_stress_matrix, behavioural_response, fiscal_trajectory | reports/investment_guardrails.md, reports/sector_stress_matrix.md, reports/behavioural_response_simulation.md, reports/fiscal_trajectory.md | 10 | 5 |
| Hostile / Red-Team Reviewer | hostile_red_team_reviewer | release/v1_5_rc/NON_CLAIM_BOUNDARIES.md, reports/executive_dashboard.md, reports/v1_5_release_candidate_pack.md | release_candidate_pack, executive_dashboard, legislative_architecture, administrative_workflow, behavioural_response, household_weighting, sector_stress_matrix, public_data_evidence_map | reports/v1_5_release_candidate_pack.md, reports/executive_dashboard.md, reports/legislative_architecture.md, reports/administrative_compliance_workflow.md, reports/behavioural_response_simulation.md, reports/sector_stress_matrix.md, reports/public_data_evidence_map.md | 10 | 5 |
| Legal Reviewer | legal_reviewer | reports/legislative_architecture.md, docs/legislative_architecture.md, release/v1_5_rc/NON_CLAIM_BOUNDARIES.md | legislative_architecture, administrative_workflow, evidence_workflow, release_candidate_pack | reports/legislative_architecture.md, reports/administrative_compliance_workflow.md, reports/mock_evidence_workflow.md, reports/v1_5_release_candidate_pack.md | 10 | 5 |
| Parliamentary Counsel Reviewer | parliamentary_counsel_reviewer | reports/legislative_architecture.md, data/legislative_architecture/legislative_architecture_skeleton.yaml, docs/legislative_architecture.md | legislative_architecture, sector_schedules, administrative_workflow, release_candidate_pack | reports/legislative_architecture.md, reports/sector_schedule_expansion.md, reports/administrative_compliance_workflow.md, reports/v1_5_release_candidate_pack.md | 10 | 5 |
| Policy Reviewer | policy_reviewer | release/v1_5_rc/RELEASE_NOTES.md, release/v1_5_rc/REVIEWER_BRIEFING.md, reports/v1_5_release_candidate_pack.md | release_candidate_pack, executive_dashboard, working_paper, status_risks_docs, transition_funding, payment_interactions | reports/v1_5_release_candidate_pack.md, reports/executive_dashboard.md, reports/transition_funding.md, reports/payment_interactions.md | 10 | 5 |
| Privacy / Secrecy Reviewer | privacy_secrecy_reviewer | reports/secure_ingestion_controls.md, reports/repo_guardrails.md, docs/privacy_and_secrecy_classification.md | secure_ingestion, repo_guardrails, evidence_workflow, household_weighting, real_data_feasibility, public_data_pilot, public_data_evidence_map | reports/secure_ingestion_controls.md, reports/repo_guardrails.md, reports/mock_evidence_workflow.md, reports/household_weighting.md, reports/real_data_feasibility.md, reports/public_data_pilot.md, reports/public_data_evidence_map.md | 10 | 5 |
| Statistical Methods Reviewer | statistical_methods_reviewer | reports/uncertainty_ranges.md, reports/household_weighting.md, reports/reviewed_scenarios.md | uncertainty_ranges, household_weighting, reviewed_scenarios, household_distributional, real_data_feasibility, public_data_pilot, public_data_evidence_map | reports/uncertainty_ranges.md, reports/household_weighting.md, reports/reviewed_scenarios.md, reports/distributional_scenarios.md, reports/real_data_feasibility.md, reports/public_data_pilot.md, reports/public_data_evidence_map.md | 10 | 5 |
| Tax Reviewer | tax_reviewer | reports/example_results.md, reports/transfer_pricing_results.md, reports/sector_schedule_expansion.md | core_formula_model, worked_examples, sector_schedules, administrative_workflow, legislative_architecture | reports/example_results.md, reports/transfer_pricing_results.md, reports/grouped_entity_results.md, reports/sector_schedule_expansion.md | 10 | 5 |
| Technical Reviewer | technical_reviewer | data/release/v1_5_release_manifest.yaml, data/dashboard/executive_dashboard_manifest.yaml, .github/workflows/ci.yml | repo_guardrails, executive_dashboard, release_candidate_pack, evidence_workflow, secure_ingestion, real_data_feasibility, public_data_pilot, public_data_evidence_map | reports/repo_guardrails.md, reports/executive_dashboard.md, reports/v1_5_release_candidate_pack.md, reports/secure_ingestion_controls.md, reports/real_data_feasibility.md, reports/public_data_pilot.md, reports/public_data_evidence_map.md | 10 | 5 |
| Treasury Methods Reviewer | treasury_methods_reviewer | reports/fiscal_trajectory.md, reports/investment_guardrails.md, reports/transition_funding.md | fiscal_trajectory, investment_incidence, transition_funding, core_formula_model | reports/fiscal_trajectory.md, reports/investment_guardrails.md, reports/transition_funding.md, reports/example_results.md | 10 | 5 |
| Welfare Policy Reviewer | welfare_policy_reviewer | reports/payment_interactions.md, reports/transition_funding.md, reports/distributional_scenarios.md | payment_interactions, transition_funding, household_distributional, household_weighting | reports/payment_interactions.md, reports/transition_funding.md, reports/distributional_scenarios.md, reports/household_weighting.md | 10 | 5 |

## E. Cross-Cutting Boundary Checks

| Boundary ID | Boundary Question | Prohibited Claims | Allowed Negative Warnings | Affected Layers | Fail Closed |
| --- | --- | --- | --- | --- | --- |
| ato_guidance_boundary | Does any output imply ATO guidance? | ATO guidance, ATO validated, ready for ATO | not ATO guidance, not ATO validated, not ready for ATO | administrative_workflow, evidence_workflow | True |
| compliance_scoring_boundary | Does any output imply compliance scoring? | compliance score, real compliance score | not compliance scoring, no compliance scoring | behavioural_response, administrative_workflow | True |
| confidence_interval_boundary | Does any output imply confidence intervals? | confidence interval | not confidence intervals, no confidence intervals | uncertainty_ranges, reviewed_scenarios | True |
| economic_validation_boundary | Does any output imply economic validation? | economic validation is complete, validated | not economic validation, no economic validation | investment_incidence, sector_stress_matrix | True |
| enforcement_boundary | Does any output imply enforcement, notices, or penalties? | notice is issued, penalty applies, enforceable | not enforcement, no notices, no penalties | administrative_workflow, legislative_architecture | True |
| forecast_boundary | Does any output imply forecasts? | forecast | not forecasts, no forecasts | fiscal_trajectory, uncertainty_ranges | True |
| legal_sufficiency_boundary | Does any output imply legal sufficiency? | legally sufficient, legal review complete | not legal sufficiency, not legally sufficient, legal_sufficiency_claimed false | legislative_architecture, release_candidate_pack | True |
| legislative_readiness_boundary | Does any output imply legislative readiness? | legislative-ready, bill-ready, parliament-ready | not legislative readiness, not a Bill, not drafting | legislative_architecture | True |
| liability_modification_boundary | Does any output imply firm-level liability was modified? | firm-level liability change | does not modify firm-level CARSF liability, firm_level_liability_logic_modified false | core_formula_model, release_candidate_pack | True |
| official_status_boundary | Does any output imply official status? | official status, official policy, official review pathway | not official status, not official policy, not an official review pathway | release_candidate_pack, executive_dashboard | True |
| operational_readiness_boundary | Does any output imply operational readiness? | operationally ready, operational validation is complete | not operational readiness, operational_readiness_claimed false | administrative_workflow, executive_dashboard | True |
| operative_law_boundary | Does any output imply operative law? | operative law, enforceable provision | not operative law, non-operative | legislative_architecture | True |
| population_estimate_boundary | Does any output imply population estimates? | population estimate, real household estimate | not population estimates, not real household modelling | household_weighting, household_distributional | True |
| real_data_boundary | Does any output imply real data was used? | taxpayer-level real data, firm-level real data, industry real data | no taxpayer-level real data, no firm-level real data, no industry real data | secure_ingestion, repo_guardrails, real_data_feasibility, public_data_pilot, public_data_evidence_map | True |
| statistical_validation_boundary | Does any output imply statistical validation? | statistical validation is complete | not statistical validation, no statistical validation | uncertainty_ranges, household_weighting | True |
| tax_payable_boundary | Does any output imply actual tax payable? | actual tax payable | does not determine actual tax payable, not actual tax payable | core_formula_model, worked_examples | True |
| treasury_validation_boundary | Does any output imply Treasury validation? | Treasury validated, Treasury modelling | not Treasury modelling, not Treasury validated | fiscal_trajectory, release_candidate_pack | True |
| welfare_validation_boundary | Does any output imply welfare validation? | welfare validation is complete | not welfare validation, no welfare validation | payment_interactions, household_distributional | True |

## F. Policy Review Attacks

### Policy Reviewer

Purpose: Attack policy framing, reader overread, public-language risk, equity gaps, and transition framing.

Inspect first: release/v1_5_rc/RELEASE_NOTES.md, release/v1_5_rc/REVIEWER_BRIEFING.md, reports/v1_5_release_candidate_pack.md

Attack questions:

| Question ID | Category | Severity | Question | Targets | What Would Fail | Required Evidence / Review |
| --- | --- | --- | --- | --- | --- | --- |
| common_overclaim_boundary | overclaiming_risk | critical_blocker | Could a reader overread this layer as more than a private prototype? | release_candidate_pack, executive_dashboard, legislative_architecture | Any wording that implies completed review, approval, validation, readiness, government endorsement, or legal adequacy. | Red-team language review and explicit non-claim retention. |
| common_calibration_gap | calibration_gap | material_issue | Are calibration blockers visible before numerical outputs are interpreted? | core_formula_model, sector_schedules, uncertainty_ranges, calibration_shell, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any report path where placeholders are easier to see than the missing calibration basis. | Calibration-methods review, source-data plan, and blocker prominence review. |
| common_real_data_boundary | data_access_gap | critical_blocker | Does any path imply taxpayer-level, firm-level, industry, welfare, or government data was used? | secure_ingestion, repo_guardrails, household_weighting, household_distributional, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any committed artefact that looks like real evidence, restricted data, or government microdata. | Repository guardrail review, secure-ingestion review, and privacy review. |
| common_false_precision | false_precision_gap | material_issue | Do ranges, bands, or matrices create false precision? | sector_stress_matrix, behavioural_response, uncertainty_ranges, reviewed_scenarios | Any phrasing that turns placeholder bands into empirical findings, forecasts, or confidence claims. | Statistical, economic, and red-team review of band language. |
| common_manifest_drift | manifest_drift_gap | material_issue | Do manifests, reports, docs, runners, and CI steps refer to the same artefacts? | executive_dashboard, release_candidate_pack, repo_guardrails | Any missing report, untracked runner, stale document path, or CI ordering mismatch. | Technical manifest trace and CI review. |
| common_power_boundary | administrative_power_gap | locked_until_external_review | Could evidence, workflow, or architecture language be mistaken for a real power or process? | administrative_workflow, legislative_architecture, evidence_workflow | Any path that reads like operative law, a statutory notice, enforcement step, penalty, or endorsed administrative process. | Legal, ATO-methods, administrative-law, and Parliamentary Counsel review. |
| policy_public_language | reader_misinterpretation_gap | material_issue | Could public-facing language make the prototype sound like final policy design? | working_paper, release_candidate_pack | Language that suppresses uncertainty, blockers, or external-review needs. | Policy and communications review of release material. |
| policy_social_licence_gap | hidden_assumption_risk | material_issue | Are social licence, equity, transition, and business-impact questions underdeveloped? | transition_funding, payment_interactions, household_distributional | Missing notes on distributional, business, or transition-design uncertainty. | Policy review and stakeholder impact review outside this repo. |
| policy_blocker_prominence | overclaiming_risk | material_issue | Are calibration and review blockers visible enough in the reading path? | executive_dashboard, release_candidate_pack | A reader can reach outputs before seeing hard limitations. | Navigation review and hostile-reader review. |
| policy_coherence_overstatement | hidden_assumption_risk | review_note | Does the release pack overstate stack coherence across unrelated review layers? | release_candidate_pack, executive_dashboard | Missing caveats that layer consistency has not been externally reviewed. | Independent policy synthesis review. |

Failure modes:

| Failure ID | Severity | Failure Mode | Affected Layers | Boundary At Risk | Required Follow-Up | Not Actual Error Finding |
| --- | --- | --- | --- | --- | --- | --- |
| common_failure_overclaim | material_issue | Non-claim warnings are less prominent than prototype outputs. | release_candidate_pack, executive_dashboard | Reader misinterpretation. | Increase warning prominence and add report-specific caveats. | True |
| common_failure_missing_blocker | critical_blocker | A report omits the blocker that controls interpretation. | calibration_shell, sector_schedules, uncertainty_ranges | Calibration gap. | Add blocker to the source manifest and generated report. | True |
| common_failure_stale_manifest | material_issue | Manifest and generated report indexes drift apart. | executive_dashboard, release_candidate_pack | Manifest drift. | Regenerate reports and update manifest references. | True |
| policy_failure_final_design_tone | material_issue | Release text sounds like settled design rather than challenge material. | working_paper, release_candidate_pack | Reader overread. | Reframe as critique-ready and add stronger blockers. | True |
| policy_failure_transition_gap | material_issue | Transition and equity constraints are not visible near fiscal or payment outputs. | transition_funding, payment_interactions, household_distributional | Hidden assumption. | Add policy-risk cross-links and reviewer prompts. | True |

Required external inputs or reviews:

- Independent review memo with assumptions challenged.
- Source-report trace from manifest entry to generated report.
- Non-claim boundary check against the relevant report.
- Calibration blocker list for the layer.
- External reviewer note separating challenge from validation.
- social licence review
- transition policy review
- business-impact review
- stakeholder challenge memo
- equity framing review

Must not infer:

- Do not infer completed external review.
- Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.
- Do not infer that any output determines actual tax payable.
- Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- Do not infer any firm-level CARSF liability change.

Suggested reviewer output format: Findings table with overclaim risk, missing policy evidence, required external review, and suggested wording change.


## G. Technical Review Attacks

### Technical Reviewer

Purpose: Attack manifests, runners, generated artefacts, CI coverage, fail-closed tests, and guardrail bypasses.

Inspect first: data/release/v1_5_release_manifest.yaml, data/dashboard/executive_dashboard_manifest.yaml, .github/workflows/ci.yml

Attack questions:

| Question ID | Category | Severity | Question | Targets | What Would Fail | Required Evidence / Review |
| --- | --- | --- | --- | --- | --- | --- |
| common_overclaim_boundary | overclaiming_risk | critical_blocker | Could a reader overread this layer as more than a private prototype? | release_candidate_pack, executive_dashboard, legislative_architecture | Any wording that implies completed review, approval, validation, readiness, government endorsement, or legal adequacy. | Red-team language review and explicit non-claim retention. |
| common_calibration_gap | calibration_gap | material_issue | Are calibration blockers visible before numerical outputs are interpreted? | core_formula_model, sector_schedules, uncertainty_ranges, calibration_shell, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any report path where placeholders are easier to see than the missing calibration basis. | Calibration-methods review, source-data plan, and blocker prominence review. |
| common_real_data_boundary | data_access_gap | critical_blocker | Does any path imply taxpayer-level, firm-level, industry, welfare, or government data was used? | secure_ingestion, repo_guardrails, household_weighting, household_distributional, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any committed artefact that looks like real evidence, restricted data, or government microdata. | Repository guardrail review, secure-ingestion review, and privacy review. |
| common_false_precision | false_precision_gap | material_issue | Do ranges, bands, or matrices create false precision? | sector_stress_matrix, behavioural_response, uncertainty_ranges, reviewed_scenarios | Any phrasing that turns placeholder bands into empirical findings, forecasts, or confidence claims. | Statistical, economic, and red-team review of band language. |
| common_manifest_drift | manifest_drift_gap | material_issue | Do manifests, reports, docs, runners, and CI steps refer to the same artefacts? | executive_dashboard, release_candidate_pack, repo_guardrails | Any missing report, untracked runner, stale document path, or CI ordering mismatch. | Technical manifest trace and CI review. |
| common_power_boundary | administrative_power_gap | locked_until_external_review | Could evidence, workflow, or architecture language be mistaken for a real power or process? | administrative_workflow, legislative_architecture, evidence_workflow | Any path that reads like operative law, a statutory notice, enforcement step, penalty, or endorsed administrative process. | Legal, ATO-methods, administrative-law, and Parliamentary Counsel review. |
| technical_ci_runner_gap | guardrail_coverage_gap | material_issue | Does CI run every report runner in the intended order? | repo_guardrails, release_candidate_pack | Missing CI step or report runner after its dependencies. | CI workflow trace and local runner reproduction. |
| technical_fail_closed | guardrail_coverage_gap | critical_blocker | Do invalid manifests and report paths fail closed? | executive_dashboard, release_candidate_pack, repo_guardrails | Mutated missing paths pass tests or runners. | Negative tests for missing reports, layers, documents, and warnings. |
| technical_allowlist_scope | guardrail_coverage_gap | material_issue | Are guardrail allowlists too broad for release and attack-pack documents? | repo_guardrails, secure_ingestion | A non-document artefact can pass under a documentation exception. | Guardrail fixture review and path allowlist review. |
| technical_report_json_trace | report_staleness_gap | material_issue | Does each Markdown report trace to its JSON payload and runner? | executive_dashboard, release_candidate_pack | Report text diverges from JSON or source manifest. | Runner output diff and generated report trace. |

Failure modes:

| Failure ID | Severity | Failure Mode | Affected Layers | Boundary At Risk | Required Follow-Up | Not Actual Error Finding |
| --- | --- | --- | --- | --- | --- | --- |
| common_failure_overclaim | material_issue | Non-claim warnings are less prominent than prototype outputs. | release_candidate_pack, executive_dashboard | Reader misinterpretation. | Increase warning prominence and add report-specific caveats. | True |
| common_failure_missing_blocker | critical_blocker | A report omits the blocker that controls interpretation. | calibration_shell, sector_schedules, uncertainty_ranges | Calibration gap. | Add blocker to the source manifest and generated report. | True |
| common_failure_stale_manifest | material_issue | Manifest and generated report indexes drift apart. | executive_dashboard, release_candidate_pack | Manifest drift. | Regenerate reports and update manifest references. | True |
| technical_failure_ci_gap | critical_blocker | New runner is absent from CI or ordered before its dependencies. | release_candidate_pack, repo_guardrails | Guardrail coverage. | Add CI step and ordering test. | True |
| technical_failure_report_drift | material_issue | Report text and JSON payload disagree. | executive_dashboard, release_candidate_pack | Report staleness. | Regenerate and add stable test assertions. | True |

Required external inputs or reviews:

- Independent review memo with assumptions challenged.
- Source-report trace from manifest entry to generated report.
- Non-claim boundary check against the relevant report.
- Calibration blocker list for the layer.
- External reviewer note separating challenge from validation.
- CI run log
- manifest diff review
- guardrail fixture review
- report regeneration trace

Must not infer:

- Do not infer completed external review.
- Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.
- Do not infer that any output determines actual tax payable.
- Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- Do not infer any firm-level CARSF liability change.

Suggested reviewer output format: Technical findings with file path, reproduction command, expected fail-closed behavior, and required test.


## H. Legal Review Attacks

### Legal Reviewer

Purpose: Attack legal overread, powers, safeguards, review placeholders, rights, obligations, penalties, and legal-sufficiency language.

Inspect first: reports/legislative_architecture.md, docs/legislative_architecture.md, release/v1_5_rc/NON_CLAIM_BOUNDARIES.md

Attack questions:

| Question ID | Category | Severity | Question | Targets | What Would Fail | Required Evidence / Review |
| --- | --- | --- | --- | --- | --- | --- |
| common_overclaim_boundary | overclaiming_risk | critical_blocker | Could a reader overread this layer as more than a private prototype? | release_candidate_pack, executive_dashboard, legislative_architecture | Any wording that implies completed review, approval, validation, readiness, government endorsement, or legal adequacy. | Red-team language review and explicit non-claim retention. |
| common_calibration_gap | calibration_gap | material_issue | Are calibration blockers visible before numerical outputs are interpreted? | core_formula_model, sector_schedules, uncertainty_ranges, calibration_shell, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any report path where placeholders are easier to see than the missing calibration basis. | Calibration-methods review, source-data plan, and blocker prominence review. |
| common_real_data_boundary | data_access_gap | critical_blocker | Does any path imply taxpayer-level, firm-level, industry, welfare, or government data was used? | secure_ingestion, repo_guardrails, household_weighting, household_distributional, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any committed artefact that looks like real evidence, restricted data, or government microdata. | Repository guardrail review, secure-ingestion review, and privacy review. |
| common_false_precision | false_precision_gap | material_issue | Do ranges, bands, or matrices create false precision? | sector_stress_matrix, behavioural_response, uncertainty_ranges, reviewed_scenarios | Any phrasing that turns placeholder bands into empirical findings, forecasts, or confidence claims. | Statistical, economic, and red-team review of band language. |
| common_manifest_drift | manifest_drift_gap | material_issue | Do manifests, reports, docs, runners, and CI steps refer to the same artefacts? | executive_dashboard, release_candidate_pack, repo_guardrails | Any missing report, untracked runner, stale document path, or CI ordering mismatch. | Technical manifest trace and CI review. |
| common_power_boundary | administrative_power_gap | locked_until_external_review | Could evidence, workflow, or architecture language be mistaken for a real power or process? | administrative_workflow, legislative_architecture, evidence_workflow | Any path that reads like operative law, a statutory notice, enforcement step, penalty, or endorsed administrative process. | Legal, ATO-methods, administrative-law, and Parliamentary Counsel review. |
| legal_powers_overread | legal_power_gap | locked_until_external_review | Could evidence placeholders be read as powers, notices, or obligations? | legislative_architecture, evidence_workflow, administrative_workflow | Any provision placeholder that looks like a legal test, binding-sounding request, or obligation. | Legal review, administrative-law review, and drafting counsel review. |
| legal_safeguard_gap | legal_power_gap | critical_blocker | Are review rights, reasons, privacy, secrecy, and administrative protections only placeholders? | legislative_architecture, administrative_workflow | Any language suggesting real rights, appeals, objections, or statutory safeguards exist. | Administrative-law and privacy/secrecy review. |
| legal_constitutional_gap | legal_power_gap | locked_until_external_review | Are constitutional and taxing-power assumptions explicitly unresolved? | legislative_architecture, working_paper | Any implication that constitutional review has occurred. | External constitutional and tax-law review. |
| legal_drafting_boundary | legal_power_gap | locked_until_external_review | Does any text cross from architecture into operative drafting? | legislative_architecture | Mandatory wording, legal tests, rights, obligations, powers, penalties, or commencement effect. | Parliamentary Counsel and legal drafting review. |

Failure modes:

| Failure ID | Severity | Failure Mode | Affected Layers | Boundary At Risk | Required Follow-Up | Not Actual Error Finding |
| --- | --- | --- | --- | --- | --- | --- |
| common_failure_overclaim | material_issue | Non-claim warnings are less prominent than prototype outputs. | release_candidate_pack, executive_dashboard | Reader misinterpretation. | Increase warning prominence and add report-specific caveats. | True |
| common_failure_missing_blocker | critical_blocker | A report omits the blocker that controls interpretation. | calibration_shell, sector_schedules, uncertainty_ranges | Calibration gap. | Add blocker to the source manifest and generated report. | True |
| common_failure_stale_manifest | material_issue | Manifest and generated report indexes drift apart. | executive_dashboard, release_candidate_pack | Manifest drift. | Regenerate reports and update manifest references. | True |
| legal_failure_operative_tone | locked_until_external_review | A placeholder reads like operative drafting. | legislative_architecture | Legal power gap. | Rewrite as conceptual location only and lock for counsel review. | True |
| legal_failure_safeguard_overread | critical_blocker | Safeguard placeholders could be mistaken for real review protections. | legislative_architecture, administrative_workflow | Administrative-law safeguard gap. | Add stronger non-operative warnings and legal-review blocker. | True |

Required external inputs or reviews:

- Independent review memo with assumptions challenged.
- Source-report trace from manifest entry to generated report.
- Non-claim boundary check against the relevant report.
- Calibration blocker list for the layer.
- External reviewer note separating challenge from validation.
- legal review
- administrative-law review
- constitutional review
- Parliamentary Counsel review
- privacy/secrecy legal review

Must not infer:

- Do not infer completed external review.
- Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.
- Do not infer that any output determines actual tax payable.
- Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- Do not infer any firm-level CARSF liability change.

Suggested reviewer output format: Legal issue list separating power implication, drafting risk, safeguard gap, and required counsel review.


## I. Tax Review Attacks

### Tax Reviewer

Purpose: Attack AAVA, deductibility, transfer-pricing, grouped-entity, safe-harbour, cap, credit, and tax-base ambiguities.

Inspect first: reports/example_results.md, reports/transfer_pricing_results.md, reports/sector_schedule_expansion.md

Attack questions:

| Question ID | Category | Severity | Question | Targets | What Would Fail | Required Evidence / Review |
| --- | --- | --- | --- | --- | --- | --- |
| common_overclaim_boundary | overclaiming_risk | critical_blocker | Could a reader overread this layer as more than a private prototype? | release_candidate_pack, executive_dashboard, legislative_architecture | Any wording that implies completed review, approval, validation, readiness, government endorsement, or legal adequacy. | Red-team language review and explicit non-claim retention. |
| common_calibration_gap | calibration_gap | material_issue | Are calibration blockers visible before numerical outputs are interpreted? | core_formula_model, sector_schedules, uncertainty_ranges, calibration_shell, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any report path where placeholders are easier to see than the missing calibration basis. | Calibration-methods review, source-data plan, and blocker prominence review. |
| common_real_data_boundary | data_access_gap | critical_blocker | Does any path imply taxpayer-level, firm-level, industry, welfare, or government data was used? | secure_ingestion, repo_guardrails, household_weighting, household_distributional, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any committed artefact that looks like real evidence, restricted data, or government microdata. | Repository guardrail review, secure-ingestion review, and privacy review. |
| common_false_precision | false_precision_gap | material_issue | Do ranges, bands, or matrices create false precision? | sector_stress_matrix, behavioural_response, uncertainty_ranges, reviewed_scenarios | Any phrasing that turns placeholder bands into empirical findings, forecasts, or confidence claims. | Statistical, economic, and red-team review of band language. |
| common_manifest_drift | manifest_drift_gap | material_issue | Do manifests, reports, docs, runners, and CI steps refer to the same artefacts? | executive_dashboard, release_candidate_pack, repo_guardrails | Any missing report, untracked runner, stale document path, or CI ordering mismatch. | Technical manifest trace and CI review. |
| common_power_boundary | administrative_power_gap | locked_until_external_review | Could evidence, workflow, or architecture language be mistaken for a real power or process? | administrative_workflow, legislative_architecture, evidence_workflow | Any path that reads like operative law, a statutory notice, enforcement step, penalty, or endorsed administrative process. | Legal, ATO-methods, administrative-law, and Parliamentary Counsel review. |
| tax_aava_deductibility | tax_law_gap | critical_blocker | Are AAVA and deductibility treatments clearly unresolved? | core_formula_model, administrative_workflow | Any language that turns a deductibility preview into a tax-law conclusion. | Tax counsel and Treasury methods review. |
| tax_transfer_pricing | transfer_pricing_gap | locked_until_external_review | Do transfer-pricing and offshore attribution previews avoid addback conclusions? | worked_examples, administrative_workflow | Any wording that implies a real addback or accepted attribution method. | International tax and transfer-pricing review. |
| tax_grouping | tax_law_gap | critical_blocker | Are grouped-entity previews clearly non-legal and non-aggregation for real tax? | worked_examples, administrative_workflow | Any implied real grouping, attribution, or liability aggregation. | Legal and tax grouping review. |
| tax_caps_safe_harbours | calibration_gap | material_issue | Are cap, credit, and safe-harbour values explicitly placeholders? | core_formula_model, sector_schedules | Missing cap, credit, FRV, OPFTE, or safe-harbour non-claims. | Tax, Treasury, ATO methods, and calibration review. |

Failure modes:

| Failure ID | Severity | Failure Mode | Affected Layers | Boundary At Risk | Required Follow-Up | Not Actual Error Finding |
| --- | --- | --- | --- | --- | --- | --- |
| common_failure_overclaim | material_issue | Non-claim warnings are less prominent than prototype outputs. | release_candidate_pack, executive_dashboard | Reader misinterpretation. | Increase warning prominence and add report-specific caveats. | True |
| common_failure_missing_blocker | critical_blocker | A report omits the blocker that controls interpretation. | calibration_shell, sector_schedules, uncertainty_ranges | Calibration gap. | Add blocker to the source manifest and generated report. | True |
| common_failure_stale_manifest | material_issue | Manifest and generated report indexes drift apart. | executive_dashboard, release_candidate_pack | Manifest drift. | Regenerate reports and update manifest references. | True |
| tax_failure_addback_overread | critical_blocker | Transfer-pricing preview reads like an actual addback mechanism. | worked_examples, administrative_workflow | Tax law gap. | Reword preview as challenge-only and add tax-review blocker. | True |
| tax_failure_tax_base_overread | critical_blocker | AAVA or cap output appears as settled tax-base treatment. | core_formula_model | Tax base ambiguity. | Strengthen AAVA and deductibility caveats. | True |

Required external inputs or reviews:

- Independent review memo with assumptions challenged.
- Source-report trace from manifest entry to generated report.
- Non-claim boundary check against the relevant report.
- Calibration blocker list for the layer.
- External reviewer note separating challenge from validation.
- tax counsel review
- transfer-pricing review
- AAVA deductibility review
- grouping-law review
- safe-harbour threshold review

Must not infer:

- Do not infer completed external review.
- Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.
- Do not infer that any output determines actual tax payable.
- Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- Do not infer any firm-level CARSF liability change.

Suggested reviewer output format: Tax issue register with affected formula, relevant report, tax-law gap, and required external review.


## J. ATO Methods Review Attacks

### ATO Methods Reviewer

Purpose: Attack administrative workflow overread, evidence bundles, queue labels, audit-logic risk, and operational boundary discipline.

Inspect first: reports/administrative_compliance_workflow.md, reports/mock_evidence_workflow.md, reports/secure_ingestion_controls.md

Attack questions:

| Question ID | Category | Severity | Question | Targets | What Would Fail | Required Evidence / Review |
| --- | --- | --- | --- | --- | --- | --- |
| common_overclaim_boundary | overclaiming_risk | critical_blocker | Could a reader overread this layer as more than a private prototype? | release_candidate_pack, executive_dashboard, legislative_architecture | Any wording that implies completed review, approval, validation, readiness, government endorsement, or legal adequacy. | Red-team language review and explicit non-claim retention. |
| common_calibration_gap | calibration_gap | material_issue | Are calibration blockers visible before numerical outputs are interpreted? | core_formula_model, sector_schedules, uncertainty_ranges, calibration_shell, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any report path where placeholders are easier to see than the missing calibration basis. | Calibration-methods review, source-data plan, and blocker prominence review. |
| common_real_data_boundary | data_access_gap | critical_blocker | Does any path imply taxpayer-level, firm-level, industry, welfare, or government data was used? | secure_ingestion, repo_guardrails, household_weighting, household_distributional, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any committed artefact that looks like real evidence, restricted data, or government microdata. | Repository guardrail review, secure-ingestion review, and privacy review. |
| common_false_precision | false_precision_gap | material_issue | Do ranges, bands, or matrices create false precision? | sector_stress_matrix, behavioural_response, uncertainty_ranges, reviewed_scenarios | Any phrasing that turns placeholder bands into empirical findings, forecasts, or confidence claims. | Statistical, economic, and red-team review of band language. |
| common_manifest_drift | manifest_drift_gap | material_issue | Do manifests, reports, docs, runners, and CI steps refer to the same artefacts? | executive_dashboard, release_candidate_pack, repo_guardrails | Any missing report, untracked runner, stale document path, or CI ordering mismatch. | Technical manifest trace and CI review. |
| common_power_boundary | administrative_power_gap | locked_until_external_review | Could evidence, workflow, or architecture language be mistaken for a real power or process? | administrative_workflow, legislative_architecture, evidence_workflow | Any path that reads like operative law, a statutory notice, enforcement step, penalty, or endorsed administrative process. | Legal, ATO-methods, administrative-law, and Parliamentary Counsel review. |
| ato_workflow_overread | administrative_power_gap | locked_until_external_review | Could queue labels be mistaken for operational workflow? | administrative_workflow | Any text that sounds like a real case path, audit step, notice path, or enforcement action. | ATO methods and administrative design review. |
| ato_evidence_bundle_overread | evidence_sufficiency_gap | critical_blocker | Could evidence request bundles be mistaken for real information requests? | evidence_workflow, administrative_workflow | Any evidence label that looks sufficient for administration or powers. | ATO methods, legal, privacy, and evidence-governance review. |
| ato_compliance_scoring_risk | administrative_power_gap | critical_blocker | Do behavioural flags avoid becoming compliance scoring? | behavioural_response, administrative_workflow | Any score, status, or label that reads as compliance assessment. | ATO methods and red-team review. |
| ato_notice_power_boundary | administrative_power_gap | locked_until_external_review | Are notices, powers, penalties, and enforcement explicitly absent? | administrative_workflow, legislative_architecture | Any command-like wording or implied statutory process. | Legal and ATO methods review. |

Failure modes:

| Failure ID | Severity | Failure Mode | Affected Layers | Boundary At Risk | Required Follow-Up | Not Actual Error Finding |
| --- | --- | --- | --- | --- | --- | --- |
| common_failure_overclaim | material_issue | Non-claim warnings are less prominent than prototype outputs. | release_candidate_pack, executive_dashboard | Reader misinterpretation. | Increase warning prominence and add report-specific caveats. | True |
| common_failure_missing_blocker | critical_blocker | A report omits the blocker that controls interpretation. | calibration_shell, sector_schedules, uncertainty_ranges | Calibration gap. | Add blocker to the source manifest and generated report. | True |
| common_failure_stale_manifest | material_issue | Manifest and generated report indexes drift apart. | executive_dashboard, release_candidate_pack | Manifest drift. | Regenerate reports and update manifest references. | True |
| ato_failure_queue_overread | critical_blocker | Queue label looks like a real administrative queue. | administrative_workflow | Operational overread. | Rename or caveat queue labels as synthetic review labels. | True |
| ato_failure_evidence_power | locked_until_external_review | Evidence bundle text looks like a real information request. | evidence_workflow, administrative_workflow | Information-power implication. | Add no-power warning and legal review blocker. | True |

Required external inputs or reviews:

- Independent review memo with assumptions challenged.
- Source-report trace from manifest entry to generated report.
- Non-claim boundary check against the relevant report.
- Calibration blocker list for the layer.
- External reviewer note separating challenge from validation.
- ATO methods review
- administrative design review
- legal powers review
- evidence governance review
- workflow language red-team

Must not infer:

- Do not infer completed external review.
- Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.
- Do not infer that any output determines actual tax payable.
- Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- Do not infer any firm-level CARSF liability change.

Suggested reviewer output format: ATO-methods challenge sheet with overread risk, evidence concern, queue concern, and required methods review.


## K. Treasury Methods Review Attacks

### Treasury Methods Reviewer

Purpose: Attack fiscal trajectory, incidence, investment, transition, macro boundary, and costing overread.

Inspect first: reports/fiscal_trajectory.md, reports/investment_guardrails.md, reports/transition_funding.md

Attack questions:

| Question ID | Category | Severity | Question | Targets | What Would Fail | Required Evidence / Review |
| --- | --- | --- | --- | --- | --- | --- |
| common_overclaim_boundary | overclaiming_risk | critical_blocker | Could a reader overread this layer as more than a private prototype? | release_candidate_pack, executive_dashboard, legislative_architecture | Any wording that implies completed review, approval, validation, readiness, government endorsement, or legal adequacy. | Red-team language review and explicit non-claim retention. |
| common_calibration_gap | calibration_gap | material_issue | Are calibration blockers visible before numerical outputs are interpreted? | core_formula_model, sector_schedules, uncertainty_ranges, calibration_shell, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any report path where placeholders are easier to see than the missing calibration basis. | Calibration-methods review, source-data plan, and blocker prominence review. |
| common_real_data_boundary | data_access_gap | critical_blocker | Does any path imply taxpayer-level, firm-level, industry, welfare, or government data was used? | secure_ingestion, repo_guardrails, household_weighting, household_distributional, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any committed artefact that looks like real evidence, restricted data, or government microdata. | Repository guardrail review, secure-ingestion review, and privacy review. |
| common_false_precision | false_precision_gap | material_issue | Do ranges, bands, or matrices create false precision? | sector_stress_matrix, behavioural_response, uncertainty_ranges, reviewed_scenarios | Any phrasing that turns placeholder bands into empirical findings, forecasts, or confidence claims. | Statistical, economic, and red-team review of band language. |
| common_manifest_drift | manifest_drift_gap | material_issue | Do manifests, reports, docs, runners, and CI steps refer to the same artefacts? | executive_dashboard, release_candidate_pack, repo_guardrails | Any missing report, untracked runner, stale document path, or CI ordering mismatch. | Technical manifest trace and CI review. |
| common_power_boundary | administrative_power_gap | locked_until_external_review | Could evidence, workflow, or architecture language be mistaken for a real power or process? | administrative_workflow, legislative_architecture, evidence_workflow | Any path that reads like operative law, a statutory notice, enforcement step, penalty, or endorsed administrative process. | Legal, ATO-methods, administrative-law, and Parliamentary Counsel review. |
| treasury_costing_overread | economic_incidence_gap | critical_blocker | Could fiscal outputs be mistaken for a costing or revenue estimate? | fiscal_trajectory, transition_funding | Any wording that implies budget forecasting, official costing, or revenue validation. | Treasury methods, fiscal, and PBO-style review outside the repo. |
| treasury_incidence_gap | economic_incidence_gap | material_issue | Are incidence and investment assumptions clearly uncalibrated? | investment_incidence | Pass-through or deterrence text presented as observed behavior. | Economic and Treasury methods review. |
| treasury_transition_interaction | welfare_interaction_gap | material_issue | Are transition funding and revenue capture kept separate from welfare design? | transition_funding, payment_interactions | Combined fiscal and welfare outputs without blocker language. | Treasury, DSS/Services Australia policy, and welfare review. |
| treasury_macro_boundary | hidden_assumption_risk | material_issue | Are macro, labour-market, pass-through, and revenue-capture assumptions explicitly placeholders? | fiscal_trajectory, investment_incidence | Hidden rates or behavioural assumptions without calibration blocker. | Treasury methods and economic review. |

Failure modes:

| Failure ID | Severity | Failure Mode | Affected Layers | Boundary At Risk | Required Follow-Up | Not Actual Error Finding |
| --- | --- | --- | --- | --- | --- | --- |
| common_failure_overclaim | material_issue | Non-claim warnings are less prominent than prototype outputs. | release_candidate_pack, executive_dashboard | Reader misinterpretation. | Increase warning prominence and add report-specific caveats. | True |
| common_failure_missing_blocker | critical_blocker | A report omits the blocker that controls interpretation. | calibration_shell, sector_schedules, uncertainty_ranges | Calibration gap. | Add blocker to the source manifest and generated report. | True |
| common_failure_stale_manifest | material_issue | Manifest and generated report indexes drift apart. | executive_dashboard, release_candidate_pack | Manifest drift. | Regenerate reports and update manifest references. | True |
| treasury_failure_costing_overread | critical_blocker | Fiscal trajectory reads like a costing or forecast. | fiscal_trajectory | Fiscal boundary. | Add costing and forecast non-claims near fiscal tables. | True |
| treasury_failure_incidence_assumption | material_issue | Pass-through or investment response assumptions are too hidden. | investment_incidence | Economic incidence gap. | Surface assumptions and external review blockers. | True |

Required external inputs or reviews:

- Independent review memo with assumptions challenged.
- Source-report trace from manifest entry to generated report.
- Non-claim boundary check against the relevant report.
- Calibration blocker list for the layer.
- External reviewer note separating challenge from validation.
- Treasury methods review
- fiscal costing methods review
- incidence study review
- macro assumption review
- transition funding policy review

Must not infer:

- Do not infer completed external review.
- Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.
- Do not infer that any output determines actual tax payable.
- Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- Do not infer any firm-level CARSF liability change.

Suggested reviewer output format: Treasury-methods blocker table with assumption, report location, missing evidence, and required external method.


## L. Privacy / Secrecy Review Attacks

### Privacy / Secrecy Reviewer

Purpose: Attack synthetic-only controls, secure ingestion, privacy/secrecy classification, retention, redaction, and restricted-data boundaries.

Inspect first: reports/secure_ingestion_controls.md, reports/repo_guardrails.md, docs/privacy_and_secrecy_classification.md

Attack questions:

| Question ID | Category | Severity | Question | Targets | What Would Fail | Required Evidence / Review |
| --- | --- | --- | --- | --- | --- | --- |
| common_overclaim_boundary | overclaiming_risk | critical_blocker | Could a reader overread this layer as more than a private prototype? | release_candidate_pack, executive_dashboard, legislative_architecture | Any wording that implies completed review, approval, validation, readiness, government endorsement, or legal adequacy. | Red-team language review and explicit non-claim retention. |
| common_calibration_gap | calibration_gap | material_issue | Are calibration blockers visible before numerical outputs are interpreted? | core_formula_model, sector_schedules, uncertainty_ranges, calibration_shell, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any report path where placeholders are easier to see than the missing calibration basis. | Calibration-methods review, source-data plan, and blocker prominence review. |
| common_real_data_boundary | data_access_gap | critical_blocker | Does any path imply taxpayer-level, firm-level, industry, welfare, or government data was used? | secure_ingestion, repo_guardrails, household_weighting, household_distributional, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any committed artefact that looks like real evidence, restricted data, or government microdata. | Repository guardrail review, secure-ingestion review, and privacy review. |
| common_false_precision | false_precision_gap | material_issue | Do ranges, bands, or matrices create false precision? | sector_stress_matrix, behavioural_response, uncertainty_ranges, reviewed_scenarios | Any phrasing that turns placeholder bands into empirical findings, forecasts, or confidence claims. | Statistical, economic, and red-team review of band language. |
| common_manifest_drift | manifest_drift_gap | material_issue | Do manifests, reports, docs, runners, and CI steps refer to the same artefacts? | executive_dashboard, release_candidate_pack, repo_guardrails | Any missing report, untracked runner, stale document path, or CI ordering mismatch. | Technical manifest trace and CI review. |
| common_power_boundary | administrative_power_gap | locked_until_external_review | Could evidence, workflow, or architecture language be mistaken for a real power or process? | administrative_workflow, legislative_architecture, evidence_workflow | Any path that reads like operative law, a statutory notice, enforcement step, penalty, or endorsed administrative process. | Legal, ATO-methods, administrative-law, and Parliamentary Counsel review. |
| privacy_real_data_exclusion | privacy_secrecy_gap | critical_blocker | Can any workflow accidentally permit taxpayer-level, firm-level, welfare, or restricted data? | secure_ingestion, repo_guardrails, evidence_workflow | Any path that accepts, stores, or reports real or restricted data. | Privacy, secrecy, secure ingestion, and repository-control review. |
| privacy_classification_overread | privacy_secrecy_gap | material_issue | Could privacy/secrecy labels be mistaken for formal government markings? | evidence_workflow, administrative_workflow | Any implication that classification is authoritative or operational. | Privacy/secrecy classification review. |
| privacy_retention_iam_absence | privacy_secrecy_gap | critical_blocker | Are redaction, retention, IAM, secure storage, and audit logging limitations explicit? | secure_ingestion, repo_guardrails | Any suggestion that repo controls replace external secure systems. | Privacy, cybersecurity, DLP, retention, and IAM review. |
| privacy_household_overread | data_access_gap | material_issue | Are household layers explicit that no real household or welfare records are present? | household_distributional, household_weighting | Any missing warning about synthetic data and no population representation. | Privacy and statistical methods review. |

Failure modes:

| Failure ID | Severity | Failure Mode | Affected Layers | Boundary At Risk | Required Follow-Up | Not Actual Error Finding |
| --- | --- | --- | --- | --- | --- | --- |
| common_failure_overclaim | material_issue | Non-claim warnings are less prominent than prototype outputs. | release_candidate_pack, executive_dashboard | Reader misinterpretation. | Increase warning prominence and add report-specific caveats. | True |
| common_failure_missing_blocker | critical_blocker | A report omits the blocker that controls interpretation. | calibration_shell, sector_schedules, uncertainty_ranges | Calibration gap. | Add blocker to the source manifest and generated report. | True |
| common_failure_stale_manifest | material_issue | Manifest and generated report indexes drift apart. | executive_dashboard, release_candidate_pack | Manifest drift. | Regenerate reports and update manifest references. | True |
| privacy_failure_real_data_path | critical_blocker | A path appears capable of accepting real or restricted data. | secure_ingestion, repo_guardrails | Real data exclusion. | Tighten deny rules and document external-system-only path. | True |
| privacy_failure_official_marking | material_issue | Prototype classification label resembles a formal marking. | evidence_workflow, administrative_workflow | Classification overread. | Add label caveat and privacy/secrecy review blocker. | True |

Required external inputs or reviews:

- Independent review memo with assumptions challenged.
- Source-report trace from manifest entry to generated report.
- Non-claim boundary check against the relevant report.
- Calibration blocker list for the layer.
- External reviewer note separating challenge from validation.
- privacy impact review
- secrecy review
- DLP review
- secure storage review
- retention and IAM review

Must not infer:

- Do not infer completed external review.
- Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.
- Do not infer that any output determines actual tax payable.
- Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- Do not infer any firm-level CARSF liability change.

Suggested reviewer output format: Privacy/secrecy challenge table with data path, classification overread, control gap, and required external system review.


## M. Statistical Methods Review Attacks

### Statistical Methods Reviewer

Purpose: Attack uncertainty ranges, weighting, subgroup metadata, reviewed-scenario suppression, and synthetic representativeness boundaries.

Inspect first: reports/uncertainty_ranges.md, reports/household_weighting.md, reports/reviewed_scenarios.md

Attack questions:

| Question ID | Category | Severity | Question | Targets | What Would Fail | Required Evidence / Review |
| --- | --- | --- | --- | --- | --- | --- |
| common_overclaim_boundary | overclaiming_risk | critical_blocker | Could a reader overread this layer as more than a private prototype? | release_candidate_pack, executive_dashboard, legislative_architecture | Any wording that implies completed review, approval, validation, readiness, government endorsement, or legal adequacy. | Red-team language review and explicit non-claim retention. |
| common_calibration_gap | calibration_gap | material_issue | Are calibration blockers visible before numerical outputs are interpreted? | core_formula_model, sector_schedules, uncertainty_ranges, calibration_shell, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any report path where placeholders are easier to see than the missing calibration basis. | Calibration-methods review, source-data plan, and blocker prominence review. |
| common_real_data_boundary | data_access_gap | critical_blocker | Does any path imply taxpayer-level, firm-level, industry, welfare, or government data was used? | secure_ingestion, repo_guardrails, household_weighting, household_distributional, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any committed artefact that looks like real evidence, restricted data, or government microdata. | Repository guardrail review, secure-ingestion review, and privacy review. |
| common_false_precision | false_precision_gap | material_issue | Do ranges, bands, or matrices create false precision? | sector_stress_matrix, behavioural_response, uncertainty_ranges, reviewed_scenarios | Any phrasing that turns placeholder bands into empirical findings, forecasts, or confidence claims. | Statistical, economic, and red-team review of band language. |
| common_manifest_drift | manifest_drift_gap | material_issue | Do manifests, reports, docs, runners, and CI steps refer to the same artefacts? | executive_dashboard, release_candidate_pack, repo_guardrails | Any missing report, untracked runner, stale document path, or CI ordering mismatch. | Technical manifest trace and CI review. |
| common_power_boundary | administrative_power_gap | locked_until_external_review | Could evidence, workflow, or architecture language be mistaken for a real power or process? | administrative_workflow, legislative_architecture, evidence_workflow | Any path that reads like operative law, a statutory notice, enforcement step, penalty, or endorsed administrative process. | Legal, ATO-methods, administrative-law, and Parliamentary Counsel review. |
| stats_confidence_overread | statistical_validity_gap | critical_blocker | Could deterministic ranges be mistaken for confidence intervals? | uncertainty_ranges, reviewed_scenarios | Any wording that suggests probability, confidence, or statistical inference. | Statistical methods and uncertainty review. |
| stats_population_overread | statistical_validity_gap | critical_blocker | Could household weights be mistaken for population estimates? | household_weighting, household_distributional | Missing not-population-estimate warnings or representative wording. | Statistical methods and household survey calibration review. |
| stats_suppression_rules | false_precision_gap | material_issue | Are reviewed-scenario suppression rules strong enough for fragile outputs? | reviewed_scenarios, uncertainty_ranges | Point estimates shown where ranges are missing, unstable, or non-interpretable. | Statistical and policy display-control review. |
| stats_forecast_boundary | statistical_validity_gap | material_issue | Are forecasts and probability claims explicitly absent? | uncertainty_ranges, fiscal_trajectory | Any forecast or probability language without external method. | Statistical and forecasting-method review outside this repo. |

Failure modes:

| Failure ID | Severity | Failure Mode | Affected Layers | Boundary At Risk | Required Follow-Up | Not Actual Error Finding |
| --- | --- | --- | --- | --- | --- | --- |
| common_failure_overclaim | material_issue | Non-claim warnings are less prominent than prototype outputs. | release_candidate_pack, executive_dashboard | Reader misinterpretation. | Increase warning prominence and add report-specific caveats. | True |
| common_failure_missing_blocker | critical_blocker | A report omits the blocker that controls interpretation. | calibration_shell, sector_schedules, uncertainty_ranges | Calibration gap. | Add blocker to the source manifest and generated report. | True |
| common_failure_stale_manifest | material_issue | Manifest and generated report indexes drift apart. | executive_dashboard, release_candidate_pack | Manifest drift. | Regenerate reports and update manifest references. | True |
| stats_failure_population_overread | critical_blocker | Synthetic household weights look representative. | household_weighting | Synthetic representativeness overread. | Increase not-population-estimate warnings and metadata fields. | True |
| stats_failure_confidence_overread | critical_blocker | Low/base/high range looks like statistical confidence. | uncertainty_ranges | Statistical validity gap. | Add deterministic-only caveats near range tables. | True |

Required external inputs or reviews:

- Independent review memo with assumptions challenged.
- Source-report trace from manifest entry to generated report.
- Non-claim boundary check against the relevant report.
- Calibration blocker list for the layer.
- External reviewer note separating challenge from validation.
- statistical methods review
- survey weight calibration review
- uncertainty method review
- suppression-rule review
- forecast boundary review

Must not infer:

- Do not infer completed external review.
- Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.
- Do not infer that any output determines actual tax payable.
- Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- Do not infer any firm-level CARSF liability change.

Suggested reviewer output format: Statistical challenge memo with inference risk, missing data/method, suppression concern, and required external calibration.


## N. Economic Methods Review Attacks

### Economic Methods Reviewer

Purpose: Attack incidence, investment, pass-through, normal-return preservation, behavioural pathways, and economic-validation boundaries.

Inspect first: reports/investment_guardrails.md, reports/sector_stress_matrix.md, reports/behavioural_response_simulation.md

Attack questions:

| Question ID | Category | Severity | Question | Targets | What Would Fail | Required Evidence / Review |
| --- | --- | --- | --- | --- | --- | --- |
| common_overclaim_boundary | overclaiming_risk | critical_blocker | Could a reader overread this layer as more than a private prototype? | release_candidate_pack, executive_dashboard, legislative_architecture | Any wording that implies completed review, approval, validation, readiness, government endorsement, or legal adequacy. | Red-team language review and explicit non-claim retention. |
| common_calibration_gap | calibration_gap | material_issue | Are calibration blockers visible before numerical outputs are interpreted? | core_formula_model, sector_schedules, uncertainty_ranges, calibration_shell, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any report path where placeholders are easier to see than the missing calibration basis. | Calibration-methods review, source-data plan, and blocker prominence review. |
| common_real_data_boundary | data_access_gap | critical_blocker | Does any path imply taxpayer-level, firm-level, industry, welfare, or government data was used? | secure_ingestion, repo_guardrails, household_weighting, household_distributional, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any committed artefact that looks like real evidence, restricted data, or government microdata. | Repository guardrail review, secure-ingestion review, and privacy review. |
| common_false_precision | false_precision_gap | material_issue | Do ranges, bands, or matrices create false precision? | sector_stress_matrix, behavioural_response, uncertainty_ranges, reviewed_scenarios | Any phrasing that turns placeholder bands into empirical findings, forecasts, or confidence claims. | Statistical, economic, and red-team review of band language. |
| common_manifest_drift | manifest_drift_gap | material_issue | Do manifests, reports, docs, runners, and CI steps refer to the same artefacts? | executive_dashboard, release_candidate_pack, repo_guardrails | Any missing report, untracked runner, stale document path, or CI ordering mismatch. | Technical manifest trace and CI review. |
| common_power_boundary | administrative_power_gap | locked_until_external_review | Could evidence, workflow, or architecture language be mistaken for a real power or process? | administrative_workflow, legislative_architecture, evidence_workflow | Any path that reads like operative law, a statutory notice, enforcement step, penalty, or endorsed administrative process. | Legal, ATO-methods, administrative-law, and Parliamentary Counsel review. |
| econ_incidence_placeholder | economic_incidence_gap | material_issue | Are incidence and pass-through labels visibly placeholders? | investment_incidence, fiscal_trajectory | Any burden or pass-through wording that implies observed economic behavior. | Economic methods review and incidence evidence plan. |
| econ_behavioural_pathway | behavioural_elasticity_gap | critical_blocker | Do behavioural pathways avoid prediction or elasticity language? | behavioural_response | Any pathway presented as expected conduct, probability, or elasticity. | Behavioural economics and tax-compliance research review. |
| econ_sector_bands | economic_incidence_gap | critical_blocker | Could sector stress bands be read as economic rankings? | sector_stress_matrix | Any ordinal or real-world sector ranking wording. | Economic and sector methods review. |
| econ_normal_return | economic_incidence_gap | material_issue | Is normal-return preservation a placeholder guardrail, not an empirical investment result? | investment_incidence | Any output implying investment effects have been measured. | Investment and incidence methods review. |

Failure modes:

| Failure ID | Severity | Failure Mode | Affected Layers | Boundary At Risk | Required Follow-Up | Not Actual Error Finding |
| --- | --- | --- | --- | --- | --- | --- |
| common_failure_overclaim | material_issue | Non-claim warnings are less prominent than prototype outputs. | release_candidate_pack, executive_dashboard | Reader misinterpretation. | Increase warning prominence and add report-specific caveats. | True |
| common_failure_missing_blocker | critical_blocker | A report omits the blocker that controls interpretation. | calibration_shell, sector_schedules, uncertainty_ranges | Calibration gap. | Add blocker to the source manifest and generated report. | True |
| common_failure_stale_manifest | material_issue | Manifest and generated report indexes drift apart. | executive_dashboard, release_candidate_pack | Manifest drift. | Regenerate reports and update manifest references. | True |
| econ_failure_prediction_overread | critical_blocker | Behavioural pathway reads like predicted behavior. | behavioural_response | Behavioural elasticity gap. | Reword as hypothetical challenge and add research blocker. | True |
| econ_failure_sector_ranking | critical_blocker | Sector stress band could be read as economic ranking. | sector_stress_matrix | Sector comparison overread. | Strengthen do-not-rank language. | True |

Required external inputs or reviews:

- Independent review memo with assumptions challenged.
- Source-report trace from manifest entry to generated report.
- Non-claim boundary check against the relevant report.
- Calibration blocker list for the layer.
- External reviewer note separating challenge from validation.
- incidence methods review
- behavioural elasticity research
- investment response review
- sector economic review
- pass-through evidence review

Must not infer:

- Do not infer completed external review.
- Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.
- Do not infer that any output determines actual tax payable.
- Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- Do not infer any firm-level CARSF liability change.

Suggested reviewer output format: Economic methods challenge table with assumption, empirical gap, overread risk, and required external study.


## O. Welfare Policy Review Attacks

### Welfare Policy Reviewer

Purpose: Attack payment interactions, household hardship, payment cliffs, eligibility-law overread, DSS/Services Australia boundaries, and welfare-validation claims.

Inspect first: reports/payment_interactions.md, reports/transition_funding.md, reports/distributional_scenarios.md

Attack questions:

| Question ID | Category | Severity | Question | Targets | What Would Fail | Required Evidence / Review |
| --- | --- | --- | --- | --- | --- | --- |
| common_overclaim_boundary | overclaiming_risk | critical_blocker | Could a reader overread this layer as more than a private prototype? | release_candidate_pack, executive_dashboard, legislative_architecture | Any wording that implies completed review, approval, validation, readiness, government endorsement, or legal adequacy. | Red-team language review and explicit non-claim retention. |
| common_calibration_gap | calibration_gap | material_issue | Are calibration blockers visible before numerical outputs are interpreted? | core_formula_model, sector_schedules, uncertainty_ranges, calibration_shell, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any report path where placeholders are easier to see than the missing calibration basis. | Calibration-methods review, source-data plan, and blocker prominence review. |
| common_real_data_boundary | data_access_gap | critical_blocker | Does any path imply taxpayer-level, firm-level, industry, welfare, or government data was used? | secure_ingestion, repo_guardrails, household_weighting, household_distributional, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any committed artefact that looks like real evidence, restricted data, or government microdata. | Repository guardrail review, secure-ingestion review, and privacy review. |
| common_false_precision | false_precision_gap | material_issue | Do ranges, bands, or matrices create false precision? | sector_stress_matrix, behavioural_response, uncertainty_ranges, reviewed_scenarios | Any phrasing that turns placeholder bands into empirical findings, forecasts, or confidence claims. | Statistical, economic, and red-team review of band language. |
| common_manifest_drift | manifest_drift_gap | material_issue | Do manifests, reports, docs, runners, and CI steps refer to the same artefacts? | executive_dashboard, release_candidate_pack, repo_guardrails | Any missing report, untracked runner, stale document path, or CI ordering mismatch. | Technical manifest trace and CI review. |
| common_power_boundary | administrative_power_gap | locked_until_external_review | Could evidence, workflow, or architecture language be mistaken for a real power or process? | administrative_workflow, legislative_architecture, evidence_workflow | Any path that reads like operative law, a statutory notice, enforcement step, penalty, or endorsed administrative process. | Legal, ATO-methods, administrative-law, and Parliamentary Counsel review. |
| welfare_eligibility_overread | welfare_interaction_gap | critical_blocker | Could payment interactions be mistaken for eligibility law or Services Australia administration? | payment_interactions, transition_funding | Any implication of eligibility determination, payment entitlement, or administrative feasibility. | Welfare policy, legal, and Services Australia/DSS methods review outside this repo. |
| welfare_household_hardship | welfare_interaction_gap | critical_blocker | Are household hardship rows clearly synthetic and not real welfare evidence? | household_distributional, household_weighting | Missing synthetic-only and not-population-estimate caveats. | Welfare, statistical, and privacy review. |
| welfare_payment_cliffs | welfare_interaction_gap | material_issue | Are payment cliffs and baseline transfer interactions explicitly placeholders? | payment_interactions, household_distributional | Any cliff result presented as validated welfare effect. | Welfare policy and statistical methods review. |
| welfare_baseline_transfer | hidden_assumption_risk | material_issue | Are baseline transfer and new support concepts kept separate? | payment_interactions, transition_funding | Combined transfer and transition support without caveats. | Welfare policy and fiscal methods review. |

Failure modes:

| Failure ID | Severity | Failure Mode | Affected Layers | Boundary At Risk | Required Follow-Up | Not Actual Error Finding |
| --- | --- | --- | --- | --- | --- | --- |
| common_failure_overclaim | material_issue | Non-claim warnings are less prominent than prototype outputs. | release_candidate_pack, executive_dashboard | Reader misinterpretation. | Increase warning prominence and add report-specific caveats. | True |
| common_failure_missing_blocker | critical_blocker | A report omits the blocker that controls interpretation. | calibration_shell, sector_schedules, uncertainty_ranges | Calibration gap. | Add blocker to the source manifest and generated report. | True |
| common_failure_stale_manifest | material_issue | Manifest and generated report indexes drift apart. | executive_dashboard, release_candidate_pack | Manifest drift. | Regenerate reports and update manifest references. | True |
| welfare_failure_eligibility_overread | critical_blocker | Payment interaction row looks like eligibility analysis. | payment_interactions | Welfare law overread. | Add no-eligibility-law caveat near outputs. | True |
| welfare_failure_household_validation | critical_blocker | Household scenario looks like real welfare validation. | household_distributional, household_weighting | Welfare validation overread. | Increase synthetic-only warnings and external review blockers. | True |

Required external inputs or reviews:

- Independent review memo with assumptions challenged.
- Source-report trace from manifest entry to generated report.
- Non-claim boundary check against the relevant report.
- Calibration blocker list for the layer.
- External reviewer note separating challenge from validation.
- welfare policy review
- eligibility-law review
- DSS/Services Australia methods review
- household microsimulation review
- payment cliff review

Must not infer:

- Do not infer completed external review.
- Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.
- Do not infer that any output determines actual tax payable.
- Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- Do not infer any firm-level CARSF liability change.

Suggested reviewer output format: Welfare review challenge list with payment interaction, household risk, eligibility boundary, and required external method.


## P. Parliamentary Counsel Review Attacks

### Parliamentary Counsel Reviewer

Purpose: Attack Parts, Divisions, definitions, schedules, regulation placeholders, evidence placeholders, commencement, and reserved-for-counsel boundaries.

Inspect first: reports/legislative_architecture.md, data/legislative_architecture/legislative_architecture_skeleton.yaml, docs/legislative_architecture.md

Attack questions:

| Question ID | Category | Severity | Question | Targets | What Would Fail | Required Evidence / Review |
| --- | --- | --- | --- | --- | --- | --- |
| common_overclaim_boundary | overclaiming_risk | critical_blocker | Could a reader overread this layer as more than a private prototype? | release_candidate_pack, executive_dashboard, legislative_architecture | Any wording that implies completed review, approval, validation, readiness, government endorsement, or legal adequacy. | Red-team language review and explicit non-claim retention. |
| common_calibration_gap | calibration_gap | material_issue | Are calibration blockers visible before numerical outputs are interpreted? | core_formula_model, sector_schedules, uncertainty_ranges, calibration_shell, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any report path where placeholders are easier to see than the missing calibration basis. | Calibration-methods review, source-data plan, and blocker prominence review. |
| common_real_data_boundary | data_access_gap | critical_blocker | Does any path imply taxpayer-level, firm-level, industry, welfare, or government data was used? | secure_ingestion, repo_guardrails, household_weighting, household_distributional, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any committed artefact that looks like real evidence, restricted data, or government microdata. | Repository guardrail review, secure-ingestion review, and privacy review. |
| common_false_precision | false_precision_gap | material_issue | Do ranges, bands, or matrices create false precision? | sector_stress_matrix, behavioural_response, uncertainty_ranges, reviewed_scenarios | Any phrasing that turns placeholder bands into empirical findings, forecasts, or confidence claims. | Statistical, economic, and red-team review of band language. |
| common_manifest_drift | manifest_drift_gap | material_issue | Do manifests, reports, docs, runners, and CI steps refer to the same artefacts? | executive_dashboard, release_candidate_pack, repo_guardrails | Any missing report, untracked runner, stale document path, or CI ordering mismatch. | Technical manifest trace and CI review. |
| common_power_boundary | administrative_power_gap | locked_until_external_review | Could evidence, workflow, or architecture language be mistaken for a real power or process? | administrative_workflow, legislative_architecture, evidence_workflow | Any path that reads like operative law, a statutory notice, enforcement step, penalty, or endorsed administrative process. | Legal, ATO-methods, administrative-law, and Parliamentary Counsel review. |
| counsel_parts_architecture | legal_power_gap | locked_until_external_review | Does the Parts and Divisions map stay conceptual and non-operative? | legislative_architecture | Any provision type that looks ready to be enacted. | Parliamentary Counsel and legal drafting review. |
| counsel_definitions | legal_power_gap | critical_blocker | Are definition placeholders barred from operative use? | legislative_architecture | Any term that appears usable as a legal definition without review. | Drafting counsel, legal, and tax review. |
| counsel_regulation_placeholders | legal_power_gap | locked_until_external_review | Do regulation-making placeholders avoid creating any real power? | legislative_architecture | Any placeholder that sounds like an available regulation power. | Parliamentary Counsel, legal, Treasury, and ATO methods review. |
| counsel_schedule_placeholders | sector_attribution_gap | critical_blocker | Are sector schedules locked away from official schedule treatment? | sector_schedules, legislative_architecture | Any schedule row that appears official or calibrated. | Sector, legal, tax, and drafting counsel review. |

Failure modes:

| Failure ID | Severity | Failure Mode | Affected Layers | Boundary At Risk | Required Follow-Up | Not Actual Error Finding |
| --- | --- | --- | --- | --- | --- | --- |
| common_failure_overclaim | material_issue | Non-claim warnings are less prominent than prototype outputs. | release_candidate_pack, executive_dashboard | Reader misinterpretation. | Increase warning prominence and add report-specific caveats. | True |
| common_failure_missing_blocker | critical_blocker | A report omits the blocker that controls interpretation. | calibration_shell, sector_schedules, uncertainty_ranges | Calibration gap. | Add blocker to the source manifest and generated report. | True |
| common_failure_stale_manifest | material_issue | Manifest and generated report indexes drift apart. | executive_dashboard, release_candidate_pack | Manifest drift. | Regenerate reports and update manifest references. | True |
| counsel_failure_drafting_overread | locked_until_external_review | Architecture text looks like enactable drafting. | legislative_architecture | Drafting boundary. | Rewrite as reserved-for-counsel placeholder. | True |
| counsel_failure_schedule_status | critical_blocker | Sector schedule placeholder looks official. | sector_schedules, legislative_architecture | Schedule authority overread. | Add not-official schedule warning and legal review blocker. | True |

Required external inputs or reviews:

- Independent review memo with assumptions challenged.
- Source-report trace from manifest entry to generated report.
- Non-claim boundary check against the relevant report.
- Calibration blocker list for the layer.
- External reviewer note separating challenge from validation.
- Parliamentary Counsel review
- legal drafting review
- legislative architecture review
- regulation-making review
- schedule-authority design review

Must not infer:

- Do not infer completed external review.
- Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.
- Do not infer that any output determines actual tax payable.
- Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- Do not infer any firm-level CARSF liability change.

Suggested reviewer output format: Drafting-boundary memo with provision-like text, reason it must remain locked, and counsel review needed.


## Q. Hostile / Red-Team Attacks

### Hostile / Red-Team Reviewer

Purpose: Attack every non-claim boundary, hidden validation language, stale artefacts, false precision, quoted-out-of-context risk, and blocker omissions.

Inspect first: release/v1_5_rc/NON_CLAIM_BOUNDARIES.md, reports/executive_dashboard.md, reports/v1_5_release_candidate_pack.md

Attack questions:

| Question ID | Category | Severity | Question | Targets | What Would Fail | Required Evidence / Review |
| --- | --- | --- | --- | --- | --- | --- |
| common_overclaim_boundary | overclaiming_risk | critical_blocker | Could a reader overread this layer as more than a private prototype? | release_candidate_pack, executive_dashboard, legislative_architecture | Any wording that implies completed review, approval, validation, readiness, government endorsement, or legal adequacy. | Red-team language review and explicit non-claim retention. |
| common_calibration_gap | calibration_gap | material_issue | Are calibration blockers visible before numerical outputs are interpreted? | core_formula_model, sector_schedules, uncertainty_ranges, calibration_shell, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any report path where placeholders are easier to see than the missing calibration basis. | Calibration-methods review, source-data plan, and blocker prominence review. |
| common_real_data_boundary | data_access_gap | critical_blocker | Does any path imply taxpayer-level, firm-level, industry, welfare, or government data was used? | secure_ingestion, repo_guardrails, household_weighting, household_distributional, real_data_feasibility, public_data_pilot, public_data_evidence_map | Any committed artefact that looks like real evidence, restricted data, or government microdata. | Repository guardrail review, secure-ingestion review, and privacy review. |
| common_false_precision | false_precision_gap | material_issue | Do ranges, bands, or matrices create false precision? | sector_stress_matrix, behavioural_response, uncertainty_ranges, reviewed_scenarios | Any phrasing that turns placeholder bands into empirical findings, forecasts, or confidence claims. | Statistical, economic, and red-team review of band language. |
| common_manifest_drift | manifest_drift_gap | material_issue | Do manifests, reports, docs, runners, and CI steps refer to the same artefacts? | executive_dashboard, release_candidate_pack, repo_guardrails | Any missing report, untracked runner, stale document path, or CI ordering mismatch. | Technical manifest trace and CI review. |
| common_power_boundary | administrative_power_gap | locked_until_external_review | Could evidence, workflow, or architecture language be mistaken for a real power or process? | administrative_workflow, legislative_architecture, evidence_workflow | Any path that reads like operative law, a statutory notice, enforcement step, penalty, or endorsed administrative process. | Legal, ATO-methods, administrative-law, and Parliamentary Counsel review. |
| redteam_quote_out_of_context | reader_misinterpretation_gap | critical_blocker | Which sentence could be quoted without its non-claim boundary? | release_candidate_pack, executive_dashboard, working_paper | Any standalone sentence that sounds validated, official, ready, or legally adequate. | Hostile quote review and warning proximity review. |
| redteam_title_overread | overclaiming_risk | material_issue | Do report titles or section headings sound more official than the contents? | executive_dashboard, release_candidate_pack | Any title that suggests endorsement, completion, or official pathway. | Red-team naming review. |
| redteam_boundary_missing | overclaiming_risk | material_issue | Is every hard boundary repeated in reports, docs, and release materials? | release_candidate_pack, executive_dashboard, status_risks_docs | A required non-claim appears in one report but not the related document. | Boundary coverage diff across release documents and reports. |
| redteam_false_authority | reader_misinterpretation_gap | critical_blocker | Could reviewer routing itself be mistaken for an official process? | release_candidate_pack, executive_dashboard | Routing language that implies formal review, authority, or approval status. | Red-team review of routing language and headings. |

Failure modes:

| Failure ID | Severity | Failure Mode | Affected Layers | Boundary At Risk | Required Follow-Up | Not Actual Error Finding |
| --- | --- | --- | --- | --- | --- | --- |
| common_failure_overclaim | material_issue | Non-claim warnings are less prominent than prototype outputs. | release_candidate_pack, executive_dashboard | Reader misinterpretation. | Increase warning prominence and add report-specific caveats. | True |
| common_failure_missing_blocker | critical_blocker | A report omits the blocker that controls interpretation. | calibration_shell, sector_schedules, uncertainty_ranges | Calibration gap. | Add blocker to the source manifest and generated report. | True |
| common_failure_stale_manifest | material_issue | Manifest and generated report indexes drift apart. | executive_dashboard, release_candidate_pack | Manifest drift. | Regenerate reports and update manifest references. | True |
| redteam_failure_quote | critical_blocker | A sentence can be quoted as endorsement without caveat. | release_candidate_pack, executive_dashboard | Reader misinterpretation. | Move warning closer to the sentence or rewrite it. | True |
| redteam_failure_false_authority | material_issue | Reviewer routing looks formal rather than suggested. | release_candidate_pack, executive_dashboard | Official-process overread. | Add suggested-navigation-only wording. | True |

Required external inputs or reviews:

- Independent review memo with assumptions challenged.
- Source-report trace from manifest entry to generated report.
- Non-claim boundary check against the relevant report.
- Calibration blocker list for the layer.
- External reviewer note separating challenge from validation.
- hostile quote review
- forbidden phrase scan
- heading review
- blocker coverage diff
- stale report trace

Must not infer:

- Do not infer completed external review.
- Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.
- Do not infer that any output determines actual tax payable.
- Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- Do not infer any firm-level CARSF liability change.

Suggested reviewer output format: Hostile red-team log with quote, overread risk, violated boundary, and rewrite proposal.


## R. Report-by-Report Attack Matrix

| Report | Layer | Reviewer Tracks | Attack Questions | Likely Overread Risk | Blockers | Must Not Be Used For | Required Follow-Up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| reports/administrative_compliance_workflow.json | administrative_workflow | ato_methods_review, hostile_red_team_review, legal_review, parliamentary_counsel_review, tax_review | ato_compliance_scoring_risk, ato_evidence_bundle_overread, ato_notice_power_boundary, ato_workflow_overread, common_power_boundary, legal_powers_overread, legal_safeguard_gap, privacy_classification_overread, tax_aava_deductibility, tax_grouping, tax_transfer_pricing | does not show: ATO enforcement or audit logic | Workflow thresholds and evidence sufficiency are not calibrated or operationally reviewed., Legal, tax, ATO methods, privacy, Treasury, and administrative-design review are required. | must not be used for: official workflow; must not be used for: audit logic; must not be used for: enforcement; must not be used for: notices | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/administrative_compliance_workflow.md | administrative_workflow | ato_methods_review, hostile_red_team_review, legal_review, parliamentary_counsel_review, tax_review | ato_compliance_scoring_risk, ato_evidence_bundle_overread, ato_notice_power_boundary, ato_workflow_overread, common_power_boundary, legal_powers_overread, legal_safeguard_gap, privacy_classification_overread, tax_aava_deductibility, tax_grouping, tax_transfer_pricing | does not show: ATO enforcement or audit logic | Workflow thresholds and evidence sufficiency are not calibrated or operationally reviewed., Legal, tax, ATO methods, privacy, Treasury, and administrative-design review are required. | must not be used for: official workflow; must not be used for: audit logic; must not be used for: enforcement; must not be used for: notices | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/behavioural_response_simulation.json | behavioural_response | ato_methods_review, economic_methods_review, hostile_red_team_review | ato_compliance_scoring_risk, common_false_precision, econ_behavioural_pathway | does not show: behaviour prediction | Behavioural elasticity, response prevalence, and compliance effects are uncalibrated., Legal, tax, ATO methods, Treasury methods, and behavioural research review are required. | must not be used for: taxpayer behaviour prediction; must not be used for: compliance score; must not be used for: enforcement | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/behavioural_response_simulation.md | behavioural_response | ato_methods_review, economic_methods_review, hostile_red_team_review | ato_compliance_scoring_risk, common_false_precision, econ_behavioural_pathway | does not show: behaviour prediction | Behavioural elasticity, response prevalence, and compliance effects are uncalibrated., Legal, tax, ATO methods, Treasury methods, and behavioural research review are required. | must not be used for: taxpayer behaviour prediction; must not be used for: compliance score; must not be used for: enforcement | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/calibration_requirements.json | calibration_shell | hostile_red_team_review | common_calibration_gap | does not show: real calibration | Real calibration requires authorised external datasets and methods review., Data-owner, privacy, legal, tax, Treasury, ATO, economic, statistical, welfare, and Parliamentary Counsel review are required. | must not be used for: calibrated setting; must not be used for: official source registry; must not be used for: validation | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/calibration_requirements.md | calibration_shell | hostile_red_team_review | common_calibration_gap | does not show: real calibration | Real calibration requires authorised external datasets and methods review., Data-owner, privacy, legal, tax, Treasury, ATO, economic, statistical, welfare, and Parliamentary Counsel review are required. | must not be used for: calibrated setting; must not be used for: official source registry; must not be used for: validation | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/distributional_scenarios.json | household_distributional | statistical_methods_review, welfare_policy_review | common_real_data_boundary, policy_social_licence_gap, privacy_household_overread, stats_population_overread, welfare_household_hardship, welfare_payment_cliffs | does not show: real household modelling | Household composition, income, cost, welfare, labour-market, and regional parameters are uncalibrated., ABS, HILDA, Census, DSS, Services Australia, Treasury, PBO, privacy, welfare, and statistical review are required. | must not be used for: real household estimate; must not be used for: population estimate; must not be used for: welfare validation | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/distributional_scenarios.md | household_distributional | statistical_methods_review, welfare_policy_review | common_real_data_boundary, policy_social_licence_gap, privacy_household_overread, stats_population_overread, welfare_household_hardship, welfare_payment_cliffs | does not show: real household modelling | Household composition, income, cost, welfare, labour-market, and regional parameters are uncalibrated., ABS, HILDA, Census, DSS, Services Australia, Treasury, PBO, privacy, welfare, and statistical review are required. | must not be used for: real household estimate; must not be used for: population estimate; must not be used for: welfare validation | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/evidence_requirements.json | evidence_workflow | ato_methods_review, legal_review, privacy_review, technical_review | ato_evidence_bundle_overread, common_power_boundary, legal_powers_overread, privacy_classification_overread, privacy_real_data_exclusion | does not show: statutory powers or sufficiency | Evidence requirements are not tied to real statutory powers or operational systems., Legal, privacy, secrecy, ATO methods, and administrative-design review are required. | must not be used for: evidence sufficiency; must not be used for: real evidence review; must not be used for: statutory powers | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/evidence_requirements.md | evidence_workflow | ato_methods_review, legal_review, privacy_review, technical_review | ato_evidence_bundle_overread, common_power_boundary, legal_powers_overread, privacy_classification_overread, privacy_real_data_exclusion | does not show: statutory powers or sufficiency | Evidence requirements are not tied to real statutory powers or operational systems., Legal, privacy, secrecy, ATO methods, and administrative-design review are required. | must not be used for: evidence sufficiency; must not be used for: real evidence review; must not be used for: statutory powers | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/example_results.json | worked_examples | tax_review | tax_grouping, tax_transfer_pricing | does not show: calibrated firm outcomes | Example values are illustrative placeholders and not calibrated firm data., Example interpretations require technical, policy, legal, tax, and methods review. | must not be used for: real firm estimate; must not be used for: actual tax payable; must not be used for: official benchmark | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/example_results.md | worked_examples | tax_review, treasury_methods_review | common_calibration_gap, tax_aava_deductibility, tax_caps_safe_harbours, tax_grouping, tax_transfer_pricing | does not show: calibrated firm outcomes | Example values are illustrative placeholders and not calibrated firm data., Example interpretations require technical, policy, legal, tax, and methods review. | must not be used for: real firm estimate; must not be used for: actual tax payable; must not be used for: official benchmark | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/executive_dashboard.json | executive_dashboard | hostile_red_team_review, policy_review, technical_review | common_manifest_drift, common_overclaim_boundary, policy_blocker_prominence, policy_coherence_overstatement, redteam_boundary_missing, redteam_false_authority, redteam_quote_out_of_context, redteam_title_overread, technical_fail_closed, technical_report_json_trace | does not show: readiness score | Dashboard must be updated whenever reports, blockers, or pages change., Reviewer routing is a convenience only and does not replace external review. | must not be used for: readiness score; must not be used for: official review pathway; must not be used for: validation | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/executive_dashboard.md | executive_dashboard | hostile_red_team_review, policy_review, technical_review | common_manifest_drift, common_overclaim_boundary, policy_blocker_prominence, policy_coherence_overstatement, policy_public_language, redteam_boundary_missing, redteam_false_authority, redteam_quote_out_of_context, redteam_title_overread, technical_fail_closed, technical_report_json_trace | does not show: readiness score | Dashboard must be updated whenever reports, blockers, or pages change., Reviewer routing is a convenience only and does not replace external review. | must not be used for: readiness score; must not be used for: official review pathway; must not be used for: validation | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/fiscal_trajectory.json | fiscal_trajectory | economic_methods_review, treasury_methods_review | econ_incidence_placeholder, stats_forecast_boundary, treasury_costing_overread, treasury_macro_boundary | does not show: fiscal forecasts | PAYG, support, superannuation, HELP, GST, company tax, and state effects are uncalibrated., Treasury, ATO, PBO, ABS, DSS, and fiscal methods review are required. | must not be used for: forecast; must not be used for: budget costing; must not be used for: revenue estimate | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/fiscal_trajectory.md | fiscal_trajectory | economic_methods_review, treasury_methods_review | econ_incidence_placeholder, stats_forecast_boundary, treasury_costing_overread, treasury_macro_boundary | does not show: fiscal forecasts | PAYG, support, superannuation, HELP, GST, company tax, and state effects are uncalibrated., Treasury, ATO, PBO, ABS, DSS, and fiscal methods review are required. | must not be used for: forecast; must not be used for: budget costing; must not be used for: revenue estimate | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/grouped_entity_results.json | worked_examples | tax_review | tax_grouping, tax_transfer_pricing | does not show: legal grouping results | Example values are illustrative placeholders and not calibrated firm data., Example interpretations require technical, policy, legal, tax, and methods review. | must not be used for: real firm estimate; must not be used for: actual tax payable; must not be used for: official benchmark | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/grouped_entity_results.md | worked_examples | tax_review | tax_grouping, tax_transfer_pricing | does not show: legal grouping results | Example values are illustrative placeholders and not calibrated firm data., Example interpretations require technical, policy, legal, tax, and methods review. | must not be used for: real firm estimate; must not be used for: actual tax payable; must not be used for: official benchmark | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/household_weighting.json | household_weighting | hostile_red_team_review, privacy_review, statistical_methods_review, welfare_policy_review | common_real_data_boundary, privacy_household_overread, stats_population_overread, welfare_household_hardship | does not show: representative population estimates | Synthetic weights are not survey weights and require external microdata and weighting review., Statistical, privacy, ABS/HILDA/Census, DSS, Treasury, PBO, welfare, and legal review are required. | must not be used for: population weighting; must not be used for: representative estimate; must not be used for: subgroup prevalence | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/household_weighting.md | household_weighting | hostile_red_team_review, privacy_review, statistical_methods_review, welfare_policy_review | common_real_data_boundary, privacy_household_overread, stats_population_overread, welfare_household_hardship | does not show: representative population estimates | Synthetic weights are not survey weights and require external microdata and weighting review., Statistical, privacy, ABS/HILDA/Census, DSS, Treasury, PBO, welfare, and legal review are required. | must not be used for: population weighting; must not be used for: representative estimate; must not be used for: subgroup prevalence | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/investment_guardrails.json | investment_incidence | economic_methods_review, treasury_methods_review | econ_incidence_placeholder, econ_normal_return, treasury_incidence_gap, treasury_macro_boundary | does not show: economic validation | Incidence, elasticity, pass-through, and normal-return assumptions are uncalibrated., Economic, Treasury, tax, and investment-incidence review are required. | must not be used for: economic validation; must not be used for: investment advice; must not be used for: market forecast | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/investment_guardrails.md | investment_incidence | economic_methods_review, treasury_methods_review | econ_incidence_placeholder, econ_normal_return, treasury_incidence_gap, treasury_macro_boundary | does not show: economic validation | Incidence, elasticity, pass-through, and normal-return assumptions are uncalibrated., Economic, Treasury, tax, and investment-incidence review are required. | must not be used for: economic validation; must not be used for: investment advice; must not be used for: market forecast | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/legislative_architecture.json | legislative_architecture | hostile_red_team_review, legal_review, parliamentary_counsel_review, tax_review | ato_notice_power_boundary, common_overclaim_boundary, common_power_boundary, counsel_definitions, counsel_parts_architecture, counsel_regulation_placeholders, counsel_schedule_placeholders, legal_constitutional_gap, legal_drafting_boundary, legal_powers_overread, legal_safeguard_gap | does not show: operative law or legal sufficiency | Legislative structure cannot be used without legal, tax, Treasury, ATO, privacy, and policy review., Parliamentary Counsel and constitutional/legal review remain unresolved. | must not be used for: operative law; must not be used for: Bill drafting; must not be used for: legal sufficiency | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/legislative_architecture.md | legislative_architecture | hostile_red_team_review, legal_review, parliamentary_counsel_review, tax_review | ato_notice_power_boundary, common_overclaim_boundary, common_power_boundary, counsel_definitions, counsel_parts_architecture, counsel_regulation_placeholders, counsel_schedule_placeholders, legal_constitutional_gap, legal_drafting_boundary, legal_powers_overread, legal_safeguard_gap | does not show: operative law or legal sufficiency | Legislative structure cannot be used without legal, tax, Treasury, ATO, privacy, and policy review., Parliamentary Counsel and constitutional/legal review remain unresolved. | must not be used for: operative law; must not be used for: Bill drafting; must not be used for: legal sufficiency | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/mock_evidence_workflow.json | evidence_workflow | ato_methods_review, legal_review, privacy_review, technical_review | ato_evidence_bundle_overread, common_power_boundary, legal_powers_overread, privacy_classification_overread, privacy_real_data_exclusion | does not show: real evidence sufficiency | Evidence requirements are not tied to real statutory powers or operational systems., Legal, privacy, secrecy, ATO methods, and administrative-design review are required. | must not be used for: evidence sufficiency; must not be used for: real evidence review; must not be used for: statutory powers | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/mock_evidence_workflow.md | evidence_workflow | ato_methods_review, legal_review, privacy_review, technical_review | ato_evidence_bundle_overread, common_power_boundary, legal_powers_overread, privacy_classification_overread, privacy_real_data_exclusion | does not show: real evidence sufficiency | Evidence requirements are not tied to real statutory powers or operational systems., Legal, privacy, secrecy, ATO methods, and administrative-design review are required. | must not be used for: evidence sufficiency; must not be used for: real evidence review; must not be used for: statutory powers | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/payment_interactions.json | payment_interactions | policy_review, welfare_policy_review | policy_social_licence_gap, treasury_transition_interaction, welfare_baseline_transfer, welfare_eligibility_overread, welfare_payment_cliffs | does not show: welfare advice or eligibility law | Eligibility, income/household tests, phase rules, double-counting, offsets, and support incidence are uncalibrated., Welfare, DSS, Services Australia, Treasury, PBO, legal, privacy, and tax review are required. | must not be used for: eligibility law; must not be used for: welfare advice; must not be used for: payment costing | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/payment_interactions.md | payment_interactions | policy_review, welfare_policy_review | policy_social_licence_gap, treasury_transition_interaction, welfare_baseline_transfer, welfare_eligibility_overread, welfare_payment_cliffs | does not show: welfare advice or eligibility law | Eligibility, income/household tests, phase rules, double-counting, offsets, and support incidence are uncalibrated., Welfare, DSS, Services Australia, Treasury, PBO, legal, privacy, and tax review are required. | must not be used for: eligibility law; must not be used for: welfare advice; must not be used for: payment costing | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/public_data_evidence_map.json | public_data_evidence_map | hostile_red_team_review, privacy_review, statistical_methods_review, technical_review | common_calibration_gap, common_real_data_boundary | does not show: new data loaded calibration completed validation official status or tax-payable use | Evidence map exposes public-pilot records for reviewer inspection only., No new data is loaded and calibration remains incomplete., Source reconciliation, privacy, statistical, legal, tax, Treasury-methods, and ATO-methods review remain required. | must not be used for: calibration completed; must not be used for: validation; must not be used for: official status; must not be used for: actual tax payable; must not be used for: readiness score | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/public_data_evidence_map.md | public_data_evidence_map | hostile_red_team_review, privacy_review, statistical_methods_review, technical_review | common_calibration_gap, common_real_data_boundary | does not show: new data loaded calibration completed validation official status or tax-payable use | Evidence map exposes public-pilot records for reviewer inspection only., No new data is loaded and calibration remains incomplete., Source reconciliation, privacy, statistical, legal, tax, Treasury-methods, and ATO-methods review remain required. | must not be used for: calibration completed; must not be used for: validation; must not be used for: official status; must not be used for: actual tax payable; must not be used for: readiness score | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/public_data_pilot.json | public_data_pilot | privacy_review, statistical_methods_review, technical_review | common_calibration_gap, common_real_data_boundary | does not show: calibration completed validation official status tax-payable use or proof that CARSF works | Public aggregate extracts support sanity checks and placeholder anchors only., Calibration has not been completed and restricted-data blockers remain., Technical, privacy, statistical, legal, tax, Treasury-methods, and ATO-methods review remain required. | must not be used for: calibration completed; must not be used for: validation; must not be used for: official status; must not be used for: actual tax payable; must not be used for: readiness score | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/public_data_pilot.md | public_data_pilot | privacy_review, statistical_methods_review, technical_review | common_calibration_gap, common_real_data_boundary | does not show: calibration completed validation official status tax-payable use or proof that CARSF works | Public aggregate extracts support sanity checks and placeholder anchors only., Calibration has not been completed and restricted-data blockers remain., Technical, privacy, statistical, legal, tax, Treasury-methods, and ATO-methods review remain required. | must not be used for: calibration completed; must not be used for: validation; must not be used for: official status; must not be used for: actual tax payable; must not be used for: readiness score | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/real_data_feasibility.json | real_data_feasibility | privacy_review, statistical_methods_review, technical_review | common_calibration_gap, common_real_data_boundary | does not show: real data loaded calibration completed validation official status or tax model proof | No real data has been loaded and no calibration has occurred., Public-data candidates require licence, provenance, and aggregate-only review before any Build 27 pilot., Technical, privacy, statistical, legal, tax, Treasury-methods, and ATO-methods review remain required. | must not be used for: real data loaded; must not be used for: calibration completed; must not be used for: validation; must not be used for: official status; must not be used for: actual tax payable | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/real_data_feasibility.md | real_data_feasibility | privacy_review, statistical_methods_review, technical_review | common_calibration_gap, common_real_data_boundary | does not show: real data loaded calibration completed validation official status or tax model proof | No real data has been loaded and no calibration has occurred., Public-data candidates require licence, provenance, and aggregate-only review before any Build 27 pilot., Technical, privacy, statistical, legal, tax, Treasury-methods, and ATO-methods review remain required. | must not be used for: real data loaded; must not be used for: calibration completed; must not be used for: validation; must not be used for: official status; must not be used for: actual tax payable | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/repo_guardrails.json | repo_guardrails | privacy_review, technical_review | common_manifest_drift, common_real_data_boundary, privacy_real_data_exclusion, privacy_retention_iam_absence, technical_allowlist_scope, technical_ci_runner_gap, technical_fail_closed | does not show: complete DLP or cybersecurity validation | Guardrails require external DLP, sensitive-marker scanning, privacy, legal, and cybersecurity review before real use., Repository controls are not complete evidence governance. | must not be used for: complete sensitive-data proof; must not be used for: cybersecurity validation; must not be used for: privacy compliance | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/repo_guardrails.md | repo_guardrails | privacy_review, technical_review | common_manifest_drift, common_real_data_boundary, privacy_real_data_exclusion, privacy_retention_iam_absence, technical_allowlist_scope, technical_ci_runner_gap, technical_fail_closed | does not show: complete DLP or cybersecurity validation | Guardrails require external DLP, sensitive-marker scanning, privacy, legal, and cybersecurity review before real use., Repository controls are not complete evidence governance. | must not be used for: complete sensitive-data proof; must not be used for: cybersecurity validation; must not be used for: privacy compliance | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/reviewed_scenarios.json | reviewed_scenarios | statistical_methods_review | common_false_precision, stats_confidence_overread, stats_suppression_rules | does not show: validation or approval | Review categories require external calibration and methods review., Legal, policy, statistical, welfare, and display-control review are required. | must not be used for: validation; must not be used for: approval; must not be used for: clean point estimate | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/reviewed_scenarios.md | reviewed_scenarios | statistical_methods_review | common_false_precision, stats_confidence_overread, stats_suppression_rules | does not show: validation or approval | Review categories require external calibration and methods review., Legal, policy, statistical, welfare, and display-control review are required. | must not be used for: validation; must not be used for: approval; must not be used for: clean point estimate | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/sector_schedule_expansion.json | sector_schedule_expansion | hostile_red_team_review | None | does not show: official schedule calibration | Schedule coverage and settings require external calibration and legal attribution review., Software and digital platform capital-base treatment remains unresolved. | must not be used for: official schedule validation; must not be used for: sector calibration; must not be used for: actual tax payable | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/sector_schedule_expansion.md | sector_schedule_expansion | parliamentary_counsel_review, tax_review | common_calibration_gap, counsel_schedule_placeholders, tax_caps_safe_harbours | does not show: official schedule calibration | Schedule coverage and settings require external calibration and legal attribution review., Software and digital platform capital-base treatment remains unresolved. | must not be used for: official schedule validation; must not be used for: sector calibration; must not be used for: actual tax payable | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/sector_stress_matrix.json | sector_stress_matrix | economic_methods_review, hostile_red_team_review | common_false_precision, econ_sector_bands | does not show: real sector ranking | Stress bands are metadata-only and require sector, legal, tax, Treasury, ATO, and methods review., Do-not-rank treatment must remain visible before wider review. | must not be used for: sector ranking; must not be used for: official sector score; must not be used for: economic validation | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/sector_stress_matrix.md | sector_stress_matrix | economic_methods_review, hostile_red_team_review | common_false_precision, econ_sector_bands | does not show: real sector ranking | Stress bands are metadata-only and require sector, legal, tax, Treasury, ATO, and methods review., Do-not-rank treatment must remain visible before wider review. | must not be used for: sector ranking; must not be used for: official sector score; must not be used for: economic validation | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/secure_ingestion_controls.json | secure_ingestion | ato_methods_review, privacy_review, technical_review | common_real_data_boundary, privacy_real_data_exclusion, privacy_retention_iam_absence, technical_allowlist_scope | does not show: real secure evidence platform | Real secure storage, IAM, deletion, DLP, malware scanning, and audit tooling are out of repo., Cybersecurity, privacy, legal, and data-owner review are required. | must not be used for: real evidence ingestion; must not be used for: secure storage; must not be used for: complete DLP | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/secure_ingestion_controls.md | secure_ingestion | ato_methods_review, privacy_review, technical_review | common_real_data_boundary, privacy_real_data_exclusion, privacy_retention_iam_absence, technical_allowlist_scope | does not show: real secure evidence platform | Real secure storage, IAM, deletion, DLP, malware scanning, and audit tooling are out of repo., Cybersecurity, privacy, legal, and data-owner review are required. | must not be used for: real evidence ingestion; must not be used for: secure storage; must not be used for: complete DLP | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/transfer_pricing_results.json | worked_examples | tax_review | tax_grouping, tax_transfer_pricing | does not show: legal addbacks | Example values are illustrative placeholders and not calibrated firm data., Example interpretations require technical, policy, legal, tax, and methods review. | must not be used for: real firm estimate; must not be used for: actual tax payable; must not be used for: official benchmark | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/transfer_pricing_results.md | worked_examples | tax_review | tax_grouping, tax_transfer_pricing | does not show: legal addbacks | Example values are illustrative placeholders and not calibrated firm data., Example interpretations require technical, policy, legal, tax, and methods review. | must not be used for: real firm estimate; must not be used for: actual tax payable; must not be used for: official benchmark | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/transition_funding.json | transition_funding | policy_review, treasury_methods_review, welfare_policy_review | policy_social_licence_gap, treasury_costing_overread, treasury_transition_interaction, welfare_baseline_transfer, welfare_eligibility_overread | does not show: welfare policy or costing | Population, payment, duration, administration, and participation settings are uncalibrated., DSS, Services Australia, Treasury, PBO, legal, and welfare-policy review are required. | must not be used for: welfare policy; must not be used for: payment design; must not be used for: costing | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/transition_funding.md | transition_funding | policy_review, treasury_methods_review, welfare_policy_review | policy_social_licence_gap, treasury_costing_overread, treasury_transition_interaction, welfare_baseline_transfer, welfare_eligibility_overread | does not show: welfare policy or costing | Population, payment, duration, administration, and participation settings are uncalibrated., DSS, Services Australia, Treasury, PBO, legal, and welfare-policy review are required. | must not be used for: welfare policy; must not be used for: payment design; must not be used for: costing | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/uncertainty_ranges.json | uncertainty_ranges | statistical_methods_review | common_calibration_gap, common_false_precision, stats_confidence_overread, stats_forecast_boundary, stats_suppression_rules | does not show: confidence intervals or forecasts | Ranges and stability thresholds are deterministic placeholders., Statistical methods, calibration, data-governance, and policy review are required. | must not be used for: confidence interval; must not be used for: forecast; must not be used for: statistical validation | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/uncertainty_ranges.md | uncertainty_ranges | statistical_methods_review | common_calibration_gap, common_false_precision, stats_confidence_overread, stats_forecast_boundary, stats_suppression_rules | does not show: confidence intervals or forecasts | Ranges and stability thresholds are deterministic placeholders., Statistical methods, calibration, data-governance, and policy review are required. | must not be used for: confidence interval; must not be used for: forecast; must not be used for: statistical validation | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/v1_5_release_candidate_pack.json | release_candidate_pack | hostile_red_team_review, legal_review, parliamentary_counsel_review, policy_review, technical_review | common_manifest_drift, common_overclaim_boundary, policy_blocker_prominence, policy_coherence_overstatement, policy_public_language, redteam_boundary_missing, redteam_false_authority, redteam_quote_out_of_context, redteam_title_overread, technical_ci_runner_gap, technical_fail_closed, technical_report_json_trace | does not show: no readiness score or official status | Release-candidate pack does not calibrate any model or validate any report., All release contents require external review before any real policy, legal, tax, administrative, economic, welfare, or statistical use. | must not be used for: readiness score; must not be used for: official status; must not be used for: official review pathway; must not be used for: validation | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |
| reports/v1_5_release_candidate_pack.md | release_candidate_pack | hostile_red_team_review, legal_review, parliamentary_counsel_review, policy_review, technical_review | common_manifest_drift, common_overclaim_boundary, legal_constitutional_gap, policy_blocker_prominence, policy_coherence_overstatement, policy_public_language, redteam_boundary_missing, redteam_false_authority, redteam_quote_out_of_context, redteam_title_overread, technical_ci_runner_gap, technical_fail_closed | does not show: no readiness score or official status | Release-candidate pack does not calibrate any model or validate any report., All release contents require external review before any real policy, legal, tax, administrative, economic, welfare, or statistical use. | must not be used for: readiness score; must not be used for: official status; must not be used for: official review pathway; must not be used for: validation | External reviewer should test the report against its non-claims, blockers, source runner, and generated JSON payload. |

## S. Layer-by-Layer Attack Matrix

| Layer ID | Layer Name | Attack Tracks | Categories | Known Blockers | Missing External Inputs | Failure Modes | Must Not Infer | Locked Until Review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| administrative_workflow | Administrative Compliance Workflow | ato_methods_review, hostile_red_team_review, legal_review, parliamentary_counsel_review, tax_review | administrative_power_gap, evidence_sufficiency_gap, legal_power_gap, privacy_secrecy_gap, tax_law_gap, transfer_pricing_gap | Workflow thresholds and evidence sufficiency are not calibrated or operationally reviewed., Legal, tax, ATO methods, privacy, Treasury, and administrative-design review are required. | AAVA deductibility review, ATO methods review, Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Parliamentary Counsel review, Source-report trace from manifest entry to generated report., administrative design review, administrative-law review, blocker coverage diff, constitutional review | ato_failure_evidence_power, ato_failure_queue_overread, legal_failure_safeguard_overread, privacy_failure_official_marking, tax_failure_addback_overread | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | AAVA deductibility, Parts and Divisions, all external-review claims, all firm-liability implications, all official-status language, all readiness language, all validation language, behavioural flags, cap and credit settings, commencement and transition placeholders, constitutional basis, definitions |
| behavioural_response | Behavioural Response Simulation | ato_methods_review, economic_methods_review, hostile_red_team_review | administrative_power_gap, behavioural_elasticity_gap, false_precision_gap | Behavioural elasticity, response prevalence, and compliance effects are uncalibrated., Legal, tax, ATO methods, Treasury methods, and behavioural research review are required. | ATO methods review, Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., administrative design review, behavioural elasticity research, blocker coverage diff, evidence governance review, forbidden phrase scan, heading review | econ_failure_prediction_overread | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | all external-review claims, all firm-liability implications, all official-status language, all readiness language, all validation language, behavioural elasticity, behavioural flags, escalation pathways, evidence bundles, incidence assumptions, investment response, pass-through |
| calibration_shell | Calibration Shell | hostile_red_team_review | calibration_gap | Real calibration requires authorised external datasets and methods review., Data-owner, privacy, legal, tax, Treasury, ATO, economic, statistical, welfare, and Parliamentary Counsel review are required. | Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., blocker coverage diff, forbidden phrase scan, heading review, hostile quote review, stale report trace | common_failure_missing_blocker | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | all external-review claims, all firm-liability implications, all official-status language, all readiness language, all validation language |
| core_formula_model | Core Formula Model | tax_review, treasury_methods_review | calibration_gap, tax_law_gap | OPFTE, FRV, AII, QLC, cap, credit, and rent-rate parameters require external calibration., Formula architecture requires legal, tax, Treasury, ATO methods, and economic review. | AAVA deductibility review, Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., Treasury methods review, fiscal costing methods review, grouping-law review, incidence study review, macro assumption review, safe-harbour threshold review | tax_failure_tax_base_overread | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | AAVA deductibility, cap and credit settings, fiscal trajectory assumptions, investment deterrence, legal grouping, pass-through, revenue capture, safe-harbour thresholds, transfer-pricing attribution, transition funding feasibility |
| evidence_workflow | Evidence Workflow | ato_methods_review, legal_review, privacy_review, technical_review | administrative_power_gap, evidence_sufficiency_gap, legal_power_gap, privacy_secrecy_gap | Evidence requirements are not tied to real statutory powers or operational systems., Legal, privacy, secrecy, ATO methods, and administrative-design review are required. | ATO methods review, CI run log, Calibration blocker list for the layer., DLP review, External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Parliamentary Counsel review, Source-report trace from manifest entry to generated report., administrative design review, administrative-law review, constitutional review | ato_failure_evidence_power, privacy_failure_official_marking | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | CI coverage completeness, behavioural flags, constitutional basis, escalation pathways, evidence bundles, evidence powers, fail-closed mutation coverage, generated-report traceability, guardrail allowlists, manifest drift controls, operative drafting, privacy classification |
| executive_dashboard | Executive Dashboard | hostile_red_team_review, policy_review, technical_review | guardrail_coverage_gap, hidden_assumption_risk, manifest_drift_gap, overclaiming_risk, reader_misinterpretation_gap, report_staleness_gap | Dashboard must be updated whenever reports, blockers, or pages change., Reviewer routing is a convenience only and does not replace external review. | CI run log, Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., blocker coverage diff, business-impact review, equity framing review, forbidden phrase scan, guardrail fixture review, heading review | common_failure_overclaim, common_failure_stale_manifest, redteam_failure_false_authority, redteam_failure_quote, technical_failure_report_drift | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | CI coverage completeness, all external-review claims, all firm-liability implications, all official-status language, all readiness language, all validation language, equity conclusions, fail-closed mutation coverage, final policy design language, generated-report traceability, guardrail allowlists, manifest drift controls |
| fiscal_trajectory | Fiscal Trajectory | economic_methods_review, treasury_methods_review | economic_incidence_gap, hidden_assumption_risk, statistical_validity_gap | PAYG, support, superannuation, HELP, GST, company tax, and state effects are uncalibrated., Treasury, ATO, PBO, ABS, DSS, and fiscal methods review are required. | Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., Treasury methods review, behavioural elasticity research, fiscal costing methods review, incidence methods review, incidence study review, investment response review, macro assumption review | treasury_failure_costing_overread | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | behavioural elasticity, fiscal trajectory assumptions, incidence assumptions, investment deterrence, investment response, pass-through, revenue capture, sector comparison, transition funding feasibility |
| household_distributional | Household Distributional Scenarios | statistical_methods_review, welfare_policy_review | data_access_gap, hidden_assumption_risk, statistical_validity_gap, welfare_interaction_gap | Household composition, income, cost, welfare, labour-market, and regional parameters are uncalibrated., ABS, HILDA, Census, DSS, Services Australia, Treasury, PBO, privacy, welfare, and statistical review are required. | Calibration blocker list for the layer., DSS/Services Australia methods review, External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., eligibility-law review, forecast boundary review, household microsimulation review, payment cliff review, statistical methods review, suppression-rule review | policy_failure_transition_gap, welfare_failure_household_validation | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | DSS policy interaction, Services Australia administration, confidence treatment, eligibility interactions, household hardship validation, household representativeness, payment cliffs, reviewed-scenario suppression, subgroup inference, uncertainty method |
| household_weighting | Household Weighting | hostile_red_team_review, privacy_review, statistical_methods_review, welfare_policy_review | data_access_gap, statistical_validity_gap, welfare_interaction_gap | Synthetic weights are not survey weights and require external microdata and weighting review., Statistical, privacy, ABS/HILDA/Census, DSS, Treasury, PBO, welfare, and legal review are required. | Calibration blocker list for the layer., DLP review, DSS/Services Australia methods review, External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., blocker coverage diff, eligibility-law review, forbidden phrase scan, forecast boundary review, heading review | stats_failure_population_overread, welfare_failure_household_validation | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | DSS policy interaction, Services Australia administration, all external-review claims, all firm-liability implications, all official-status language, all readiness language, all validation language, confidence treatment, eligibility interactions, household hardship validation, household representativeness, payment cliffs |
| investment_incidence | Investment and Incidence Guardrails | economic_methods_review, treasury_methods_review | economic_incidence_gap, hidden_assumption_risk | Incidence, elasticity, pass-through, and normal-return assumptions are uncalibrated., Economic, Treasury, tax, and investment-incidence review are required. | Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., Treasury methods review, behavioural elasticity research, fiscal costing methods review, incidence methods review, incidence study review, investment response review, macro assumption review | treasury_failure_incidence_assumption | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | behavioural elasticity, fiscal trajectory assumptions, incidence assumptions, investment deterrence, investment response, pass-through, revenue capture, sector comparison, transition funding feasibility |
| legislative_architecture | Legislative Architecture Skeleton | hostile_red_team_review, legal_review, parliamentary_counsel_review, tax_review | administrative_power_gap, legal_power_gap, overclaiming_risk, sector_attribution_gap | Legislative structure cannot be used without legal, tax, Treasury, ATO, privacy, and policy review., Parliamentary Counsel and constitutional/legal review remain unresolved. | AAVA deductibility review, Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Parliamentary Counsel review, Source-report trace from manifest entry to generated report., administrative-law review, blocker coverage diff, constitutional review, forbidden phrase scan, grouping-law review | counsel_failure_drafting_overread, counsel_failure_schedule_status, legal_failure_operative_tone, legal_failure_safeguard_overread | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | AAVA deductibility, Parts and Divisions, all external-review claims, all firm-liability implications, all official-status language, all readiness language, all validation language, cap and credit settings, commencement and transition placeholders, constitutional basis, definitions, evidence powers |
| payment_interactions | Payment Interactions | policy_review, welfare_policy_review | hidden_assumption_risk, welfare_interaction_gap | Eligibility, income/household tests, phase rules, double-counting, offsets, and support incidence are uncalibrated., Welfare, DSS, Services Australia, Treasury, PBO, legal, privacy, and tax review are required. | Calibration blocker list for the layer., DSS/Services Australia methods review, External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., business-impact review, eligibility-law review, equity framing review, household microsimulation review, payment cliff review, social licence review | policy_failure_transition_gap, welfare_failure_eligibility_overread | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | DSS policy interaction, Services Australia administration, eligibility interactions, equity conclusions, final policy design language, household hardship validation, payment cliffs, public-facing policy claims, stakeholder acceptability, transition-policy feasibility |
| public_data_evidence_map | Public Data Pilot Reviewer Evidence Map | hostile_red_team_review, privacy_review, statistical_methods_review, technical_review | calibration_gap, data_access_gap | Evidence map exposes public-pilot records for reviewer inspection only., No new data is loaded and calibration remains incomplete., Source reconciliation, privacy, statistical, legal, tax, Treasury-methods, and ATO-methods review remain required. | CI run log, Calibration blocker list for the layer., DLP review, External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., blocker coverage diff, forbidden phrase scan, forecast boundary review, guardrail fixture review, heading review | None | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | CI coverage completeness, all external-review claims, all firm-liability implications, all official-status language, all readiness language, all validation language, confidence treatment, fail-closed mutation coverage, generated-report traceability, guardrail allowlists, household representativeness, manifest drift controls |
| public_data_pilot | Public Data Pilot and Placeholder Anchor Layer | privacy_review, statistical_methods_review, technical_review | calibration_gap, data_access_gap | Public aggregate extracts support sanity checks and placeholder anchors only., Calibration has not been completed and restricted-data blockers remain., Technical, privacy, statistical, legal, tax, Treasury-methods, and ATO-methods review remain required. | CI run log, Calibration blocker list for the layer., DLP review, External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., forecast boundary review, guardrail fixture review, manifest diff review, privacy impact review, report regeneration trace | None | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | CI coverage completeness, confidence treatment, fail-closed mutation coverage, generated-report traceability, guardrail allowlists, household representativeness, manifest drift controls, privacy classification, real-data ingestion, retention and IAM, reviewed-scenario suppression, secrecy handling |
| real_data_feasibility | Real Data Feasibility and Calibration Intake Map | privacy_review, statistical_methods_review, technical_review | calibration_gap, data_access_gap | No real data has been loaded and no calibration has occurred., Public-data candidates require licence, provenance, and aggregate-only review before any Build 27 pilot., Technical, privacy, statistical, legal, tax, Treasury-methods, and ATO-methods review remain required. | CI run log, Calibration blocker list for the layer., DLP review, External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., forecast boundary review, guardrail fixture review, manifest diff review, privacy impact review, report regeneration trace | None | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | CI coverage completeness, confidence treatment, fail-closed mutation coverage, generated-report traceability, guardrail allowlists, household representativeness, manifest drift controls, privacy classification, real-data ingestion, retention and IAM, reviewed-scenario suppression, secrecy handling |
| release_candidate_pack | V1.5 Release Candidate Pack | hostile_red_team_review, legal_review, parliamentary_counsel_review, policy_review, technical_review | guardrail_coverage_gap, hidden_assumption_risk, manifest_drift_gap, overclaiming_risk, reader_misinterpretation_gap, report_staleness_gap | Release-candidate pack does not calibrate any model or validate any report., All release contents require external review before any real policy, legal, tax, administrative, economic, welfare, or statistical use. | CI run log, Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Parliamentary Counsel review, Source-report trace from manifest entry to generated report., administrative-law review, blocker coverage diff, business-impact review, constitutional review, equity framing review | common_failure_overclaim, common_failure_stale_manifest, policy_failure_final_design_tone, redteam_failure_false_authority, redteam_failure_quote, technical_failure_ci_gap, technical_failure_report_drift | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | CI coverage completeness, Parts and Divisions, all external-review claims, all firm-liability implications, all official-status language, all readiness language, all validation language, commencement and transition placeholders, constitutional basis, definitions, equity conclusions, evidence powers |
| repo_guardrails | Repository Guardrails | privacy_review, technical_review | data_access_gap, guardrail_coverage_gap, manifest_drift_gap, privacy_secrecy_gap | Guardrails require external DLP, sensitive-marker scanning, privacy, legal, and cybersecurity review before real use., Repository controls are not complete evidence governance. | CI run log, Calibration blocker list for the layer., DLP review, External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., guardrail fixture review, manifest diff review, privacy impact review, report regeneration trace, retention and IAM review | privacy_failure_real_data_path, technical_failure_ci_gap | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | CI coverage completeness, fail-closed mutation coverage, generated-report traceability, guardrail allowlists, manifest drift controls, privacy classification, real-data ingestion, retention and IAM, secrecy handling, secure storage |
| reviewed_scenarios | Reviewed Scenarios | statistical_methods_review | false_precision_gap, statistical_validity_gap | Review categories require external calibration and methods review., Legal, policy, statistical, welfare, and display-control review are required. | Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., forecast boundary review, statistical methods review, suppression-rule review, survey weight calibration review, uncertainty method review | None | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | confidence treatment, household representativeness, reviewed-scenario suppression, subgroup inference, uncertainty method |
| sector_schedule_expansion | Sector Schedule Expansion | hostile_red_team_review | overclaiming_risk | Schedule coverage and settings require external calibration and legal attribution review., Software and digital platform capital-base treatment remains unresolved. | Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., blocker coverage diff, forbidden phrase scan, heading review, hostile quote review, stale report trace | None | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | all external-review claims, all firm-liability implications, all official-status language, all readiness language, all validation language |
| sector_schedules | Sector Schedules | parliamentary_counsel_review, tax_review | calibration_gap, sector_attribution_gap | Sector output units, OPFTE, FRV, caps, QLC weights, and AII weights are uncalibrated., Sector attribution requires legal, tax, Treasury, ATO methods, ABS, and industry review. | AAVA deductibility review, Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Parliamentary Counsel review, Source-report trace from manifest entry to generated report., grouping-law review, legal drafting review, legislative architecture review, regulation-making review, safe-harbour threshold review | common_failure_missing_blocker, counsel_failure_schedule_status | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | AAVA deductibility, Parts and Divisions, cap and credit settings, commencement and transition placeholders, definitions, legal grouping, regulation placeholders, safe-harbour thresholds, schedules, transfer-pricing attribution |
| sector_stress_matrix | Sector Stress Matrix | economic_methods_review, hostile_red_team_review | economic_incidence_gap, false_precision_gap | Stress bands are metadata-only and require sector, legal, tax, Treasury, ATO, and methods review., Do-not-rank treatment must remain visible before wider review. | Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., behavioural elasticity research, blocker coverage diff, forbidden phrase scan, heading review, hostile quote review, incidence methods review, investment response review | econ_failure_sector_ranking | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | all external-review claims, all firm-liability implications, all official-status language, all readiness language, all validation language, behavioural elasticity, incidence assumptions, investment response, pass-through, sector comparison |
| secure_ingestion | Secure Ingestion Controls | ato_methods_review, privacy_review, technical_review | data_access_gap, guardrail_coverage_gap, privacy_secrecy_gap | Real secure storage, IAM, deletion, DLP, malware scanning, and audit tooling are out of repo., Cybersecurity, privacy, legal, and data-owner review are required. | ATO methods review, CI run log, Calibration blocker list for the layer., DLP review, External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., administrative design review, evidence governance review, guardrail fixture review, legal powers review | privacy_failure_real_data_path | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | CI coverage completeness, behavioural flags, escalation pathways, evidence bundles, fail-closed mutation coverage, generated-report traceability, guardrail allowlists, manifest drift controls, privacy classification, real-data ingestion, retention and IAM, review states |
| status_risks_docs | Status and Risk Documentation | policy_review | overclaiming_risk | Documentation must remain aligned with generated reports and blockers., Risk documentation requires hostile, legal, tax, privacy, policy, and methods review. | Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., business-impact review, equity framing review, social licence review, stakeholder challenge memo, transition policy review | None | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | equity conclusions, final policy design language, public-facing policy claims, stakeholder acceptability, transition-policy feasibility |
| transition_funding | Transition Funding | policy_review, treasury_methods_review, welfare_policy_review | economic_incidence_gap, hidden_assumption_risk, welfare_interaction_gap | Population, payment, duration, administration, and participation settings are uncalibrated., DSS, Services Australia, Treasury, PBO, legal, and welfare-policy review are required. | Calibration blocker list for the layer., DSS/Services Australia methods review, External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., Treasury methods review, business-impact review, eligibility-law review, equity framing review, fiscal costing methods review, household microsimulation review | policy_failure_transition_gap | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | DSS policy interaction, Services Australia administration, eligibility interactions, equity conclusions, final policy design language, fiscal trajectory assumptions, household hardship validation, investment deterrence, pass-through, payment cliffs, public-facing policy claims, revenue capture |
| uncertainty_ranges | Uncertainty Ranges | statistical_methods_review | calibration_gap, false_precision_gap, statistical_validity_gap | Ranges and stability thresholds are deterministic placeholders., Statistical methods, calibration, data-governance, and policy review are required. | Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., forecast boundary review, statistical methods review, suppression-rule review, survey weight calibration review, uncertainty method review | common_failure_missing_blocker, stats_failure_confidence_overread | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | confidence treatment, household representativeness, reviewed-scenario suppression, subgroup inference, uncertainty method |
| worked_examples | Worked Examples | tax_review | tax_law_gap, transfer_pricing_gap | Example values are illustrative placeholders and not calibrated firm data., Example interpretations require technical, policy, legal, tax, and methods review. | AAVA deductibility review, Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., grouping-law review, safe-harbour threshold review, tax counsel review, transfer-pricing review | tax_failure_addback_overread | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | AAVA deductibility, cap and credit settings, legal grouping, safe-harbour thresholds, transfer-pricing attribution |
| working_paper | V1.5 Working Paper | policy_review | legal_power_gap, reader_misinterpretation_gap | Working paper remains a concept paper and is not calibrated or validated., Legal, tax, Treasury, ATO, Parliamentary Counsel, privacy, statistical, economic, welfare, and policy review are required. | Calibration blocker list for the layer., External reviewer note separating challenge from validation., Independent review memo with assumptions challenged., Non-claim boundary check against the relevant report., Source-report trace from manifest entry to generated report., business-impact review, equity framing review, social licence review, stakeholder challenge memo, transition policy review | policy_failure_final_design_tone | must not be used for: Do not infer any firm-level CARSF liability change.; must not be used for: Do not infer approval, validation, operational readiness, legal sufficiency, or official endorsement.; must not be used for: Do not infer completed external review.; must not be used for: Do not infer that any output determines actual tax payable.; must not be used for: Do not infer use of taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. | equity conclusions, final policy design language, public-facing policy claims, stakeholder acceptability, transition-policy feasibility |

## T. Locked-Until-Review Items

- AAVA deductibility
- CI coverage completeness
- DSS policy interaction
- Parts and Divisions
- Services Australia administration
- all external-review claims
- all firm-liability implications
- all official-status language
- all readiness language
- all validation language
- behavioural elasticity
- behavioural flags
- cap and credit settings
- commencement and transition placeholders
- confidence treatment
- constitutional basis
- definitions
- eligibility interactions
- equity conclusions
- escalation pathways
- evidence bundles
- evidence powers
- fail-closed mutation coverage
- final policy design language
- fiscal trajectory assumptions
- generated-report traceability
- guardrail allowlists
- household hardship validation
- household representativeness
- incidence assumptions
- investment deterrence
- investment response
- legal grouping
- manifest drift controls
- operative drafting
- pass-through
- payment cliffs
- privacy classification
- public-facing policy claims
- real-data ingestion
- regulation placeholders
- retention and IAM
- revenue capture
- review rights
- review states
- reviewed-scenario suppression
- safe-harbour thresholds
- schedules
- secrecy handling
- sector comparison
- secure storage
- stakeholder acceptability
- subgroup inference
- taxing power
- transfer-pricing attribution
- transition funding feasibility
- transition-policy feasibility
- uncertainty method
- workflow queues

## U. Required External Inputs

- AAVA deductibility review
- ATO methods review
- CI run log
- Calibration blocker list for the layer.
- DLP review
- DSS/Services Australia methods review
- External reviewer note separating challenge from validation.
- Independent review memo with assumptions challenged.
- Non-claim boundary check against the relevant report.
- Parliamentary Counsel review
- Source-report trace from manifest entry to generated report.
- Treasury methods review
- administrative design review
- administrative-law review
- behavioural elasticity research
- blocker coverage diff
- business-impact review
- constitutional review
- eligibility-law review
- equity framing review
- evidence governance review
- fiscal costing methods review
- forbidden phrase scan
- forecast boundary review
- grouping-law review
- guardrail fixture review
- heading review
- hostile quote review
- household microsimulation review
- incidence methods review
- incidence study review
- investment response review
- legal drafting review
- legal powers review
- legal review
- legislative architecture review
- macro assumption review
- manifest diff review
- pass-through evidence review
- payment cliff review
- privacy impact review
- privacy/secrecy legal review
- regulation-making review
- report regeneration trace
- retention and IAM review
- safe-harbour threshold review
- schedule-authority design review
- secrecy review
- sector economic review
- secure storage review
- social licence review
- stakeholder challenge memo
- stale report trace
- statistical methods review
- suppression-rule review
- survey weight calibration review
- tax counsel review
- transfer-pricing review
- transition funding policy review
- transition policy review
- uncertainty method review
- welfare policy review
- workflow language red-team

## V. Suggested Reviewer Output Format

Reviewer notes should list challenged claim, affected layer/report, evidence gap, boundary risk, severity label, and required follow-up while stating that the note is not validation or approval.

Attack-pack release documents:

| Document | Exists | Contains Non-Claims |
| --- | --- | --- |
| release/v1_5_rc/attack_pack/ATO_METHODS_REVIEW_ATTACKS.md | True | True |
| release/v1_5_rc/attack_pack/ATTACK_PACK_MANIFEST.json | True | True |
| release/v1_5_rc/attack_pack/ATTACK_PACK_OVERVIEW.md | True | True |
| release/v1_5_rc/attack_pack/BOUNDARY_CHECKS.md | True | True |
| release/v1_5_rc/attack_pack/ECONOMIC_METHODS_REVIEW_ATTACKS.md | True | True |
| release/v1_5_rc/attack_pack/HOSTILE_RED_TEAM_ATTACKS.md | True | True |
| release/v1_5_rc/attack_pack/LAYER_ATTACK_MATRIX.md | True | True |
| release/v1_5_rc/attack_pack/LEGAL_REVIEW_ATTACKS.md | True | True |
| release/v1_5_rc/attack_pack/PARLIAMENTARY_COUNSEL_REVIEW_ATTACKS.md | True | True |
| release/v1_5_rc/attack_pack/POLICY_REVIEW_ATTACKS.md | True | True |
| release/v1_5_rc/attack_pack/PRIVACY_SECRECY_REVIEW_ATTACKS.md | True | True |
| release/v1_5_rc/attack_pack/REPORT_ATTACK_MATRIX.md | True | True |
| release/v1_5_rc/attack_pack/STATISTICAL_METHODS_REVIEW_ATTACKS.md | True | True |
| release/v1_5_rc/attack_pack/TAX_REVIEW_ATTACKS.md | True | True |
| release/v1_5_rc/attack_pack/TECHNICAL_REVIEW_ATTACKS.md | True | True |
| release/v1_5_rc/attack_pack/TREASURY_METHODS_REVIEW_ATTACKS.md | True | True |
| release/v1_5_rc/attack_pack/WELFARE_POLICY_REVIEW_ATTACKS.md | True | True |

## W. Limitations and Future Work

- Attack pack only.
- External review has not been completed.
- Approval has not been granted.
- Validation has not occurred.
- Not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare validation, not statistical validation, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, not official status, and not an official review pathway.
- It does not determine actual tax payable, does not use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, and does not modify firm-level CARSF liability.
