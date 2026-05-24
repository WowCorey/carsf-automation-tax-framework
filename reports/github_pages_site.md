# CARSF V1.5 GitHub Pages Project Website

## A. Purpose

This report validates the static GitHub Pages-ready project website for the CARSF Automation Tax Framework.
The website is reviewer-facing only and packages existing generated report outputs without loading new data.

## B. Non-Claims

- CARSF is a private research/prototype policy and modelling framework.
- This site is static and reviewer-facing only.
- This site does not load private, restricted, personal, taxpayer-level, firm-confidential, or household microdata.
- This site does not scrape sources or call external APIs.
- CARSF is not law.
- CARSF is not legal advice.
- CARSF is not tax advice.
- CARSF is not ATO guidance.
- CARSF is not Treasury modelling.
- CARSF is not PBO costing.
- CARSF is not official policy.
- CARSF is not calibrated modelling.
- CARSF is not validated modelling.
- CARSF does not determine actual tax payable.
- CARSF does not determine firm-level liability.
- CARSF does not claim economic validation, welfare validation, statistical validation, legal sufficiency, operational readiness, or implementation readiness.

## C. Static Site Files

| File | Exists |
| --- | --- |
| `site/index.html` | True |
| `site/styles.css` | True |
| `site/app.js` | True |
| `site/assets/carsf-logo.svg` | True |
| `site/site_manifest.json` | True |
| `site/README.md` | True |

## D. Required Content Sections

| Section | Present |
| --- | --- |
| hero | True |
| what_carsf_is | True |
| what_problem_it_tests | True |
| what_the_model_currently_does | True |
| what_is_calculated | True |
| what_is_not_calculated | True |
| public_aggregate_data_loaded | True |
| placeholder_replacement_map | True |
| calibration_boundary_map | True |
| scenario_constraint_layer | True |
| full_repo_integrity_gap_audit | True |
| missing_data | True |
| how_to_test_the_model | True |
| how_to_read_reports | True |
| reviewer_pathway | True |
| github_pages_setup | True |

## E. Source Report Inputs

| Report | Path | Exists |
| --- | --- | --- |
| public_real_data_loader | `reports/public_real_data_loader.json` | True |
| public_data_placeholder_replacement_map | `reports/public_data_placeholder_replacement_map.json` | True |
| public_aggregate_calibration_boundary_map | `reports/public_aggregate_calibration_boundary_map.json` | True |
| public_aggregate_scenario_constraint_layer | `reports/public_aggregate_scenario_constraint_layer.json` | True |
| full_repo_integrity_upgrade_audit | `reports/full_repo_integrity_upgrade_audit.json` | True |
| repo_guardrails | `reports/repo_guardrails.json` | True |

## F. Source Summary Counts

| Count | Value |
| --- | ---: |
| loaded_public_aggregate_sources | 5 |
| loaded_public_aggregate_values | 10 |
| source_candidates_not_loaded | 3 |
| placeholders_mapped | 11 |
| placeholders_replaced_by_public_anchor | 2 |
| placeholders_narrowed_by_public_anchor | 3 |
| placeholders_informed_by_public_anchor | 3 |
| placeholders_blocked_until_restricted_data | 1 |
| placeholders_blocked_until_external_review | 1 |
| module_boundaries_mapped | 19 |
| field_boundaries_mapped | 11 |
| module_scenario_constraints | 20 |
| field_scenario_constraints | 11 |
| full_repo_critical_findings_remaining | 0 |

## G. Report Count Reconciliation

| Count | Site Manifest | Source Report | Reconciled |
| --- | ---: | ---: | --- |
| loaded_public_aggregate_sources | 5 | 5 | True |
| loaded_public_aggregate_values | 10 | 10 | True |
| source_candidates_not_loaded | 3 | 3 | True |
| placeholders_mapped | 11 | 11 | True |
| placeholders_replaced_by_public_anchor | 2 | 2 | True |
| placeholders_narrowed_by_public_anchor | 3 | 3 | True |
| placeholders_informed_by_public_anchor | 3 | 3 | True |
| placeholders_blocked_until_restricted_data | 1 | 1 | True |
| placeholders_blocked_until_external_review | 1 | 1 | True |
| module_boundaries_mapped | 19 | 19 | True |
| field_boundaries_mapped | 11 | 11 | True |
| module_scenario_constraints | 20 | 20 | True |
| field_scenario_constraints | 11 | 11 | True |
| full_repo_critical_findings_remaining | 0 | 0 | True |

## H. External Dependency Check

- No external dependencies: True
- Scope: external scripts, stylesheets, images, fonts, analytics, tracking, fetch calls, and XMLHttpRequest

## I. Non-Claim Boundary Check

| Required text | Present |
| --- | --- |
| private research/prototype | True |
| not law | True |
| not legal advice | True |
| not tax advice | True |
| not ATO guidance | True |
| not Treasury modelling | True |
| not PBO costing | True |
| not official policy | True |
| not calibrated | True |
| not validated | True |
| No tax payable estimate | True |
| No firm liability calculation | True |
| does not determine actual tax payable | True |
| does not determine firm-level liability | True |

## J. Forbidden Claim Scan

- Forbidden affirmative claim findings: 0

## K. GitHub Pages Setup

1. Go to repository Settings.
2. Open Pages.
3. Set the source to GitHub Actions or deploy from a branch/folder.
4. If using branch/folder, choose main and the site folder if GitHub Pages exposes that folder option for this repository.
5. Save.
6. Open the repository Pages URL shown by GitHub.

## L. What The Site Can Claim

- The repo contains a structured private research prototype.
- The repo contains public aggregate-data anchors and source-locator metadata.
- The repo contains placeholder replacement mapping, calibration-boundary mapping, scenario-output constraints, and a full repo integrity/gap audit.
- The repo can be reviewed and tested locally.

## M. What The Site Must Not Claim

- law
- legal advice
- tax advice
- ATO guidance
- Treasury modelling
- PBO costing
- official policy
- calibrated modelling
- validated modelling
- actual tax payable calculation
- firm-level liability determination
- economic validation
- welfare validation
- statistical validation
- implementation readiness

## N. Summary Flags

| Flag | Value |
| --- | --- |
| github_pages_site_created | True |
| static_site_only | True |
| backend_required | False |
| external_api_calls | False |
| scraping | False |
| analytics_or_tracking | False |
| external_cdn_dependencies | False |
| required_site_files_present | True |
| required_sections_present | True |
| source_reports_available | True |
| source_report_counts_reconciled | True |
| non_claim_boundaries_visible | True |
| forbidden_claim_findings | 0 |
| loaded_public_aggregate_values_displayed | 10 |
| source_candidates_not_loaded_displayed | 3 |
| placeholders_mapped_displayed | 11 |
| module_boundaries_mapped_displayed | 19 |
| scenario_constraints_mapped_displayed | 20 |
| full_repo_audit_referenced | True |
| github_pages_workflow_added | False |
| new_data_loaded | False |
| restricted_data_loaded | False |
| personal_data_loaded | False |
| taxpayer_level_data_loaded | False |
| firm_confidential_data_loaded | False |
| household_microdata_loaded | False |
| calibration_completed | False |
| validation_claimed | False |
| actual_tax_payable_determined | False |
| official_status_claimed | False |
| firm_level_liability_logic_modified | False |

## O. Limitations and Future Work

This is a static project website only. It does not enable GitHub Pages from code, does not load new data, and does not change model calculations.
Repository settings must still be configured before the site is published through GitHub Pages.
