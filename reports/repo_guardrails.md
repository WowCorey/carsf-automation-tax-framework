# CARSF V1.5 Repository Guardrails

Generated at: `2026-05-22T02:25:45+00:00`

## A. Purpose

This report runs prototype repository-level guardrails for likely evidence leaks, secret markers, wrong storage zones, generated-report non-claims, and accidental real-data commits.

## B. Non-Claims

- These are prototype repository guardrails only. They are not a complete DLP system, secret scanner, cybersecurity control, legal/privacy audit, Treasury control, ATO control, or forensic validation.
- These are prototype repository guardrails only.
- They are not a complete DLP system, secret scanner, cybersecurity control, legal/privacy audit, Treasury control, ATO control, or forensic validation.

## C. Files Scanned/Skipped

- Files scanned: 542
- Files skipped: 1421
- Clean: true

## D. Denied Findings

| Path | Severity | Type | Line | Message |
| --- | --- | --- | --- | --- |
| none | none | none | none | none |

## E. Warning Findings

| Path | Severity | Type | Line | Message |
| --- | --- | --- | --- | --- |
| BUILD_LOG.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: SECRET. |
| CONTRIBUTING.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: API_KEY. |
| README.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: REAL_TAXPAYER, SECRET. |
| data/README.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: REAL_BUSINESS_RECORD, REAL_TAXPAYER, TAX_FILE_NUMBER. |
| data/calibration/real_data_feasibility_map.yaml | low | documented_marker_example | N/A | Documentation/test file contains marker examples: ABN, PAYSLIP, SECRET, TAX_FILE_NUMBER, TFN. |
| data/mock_ingestion_requests/allowed_mock_evidence_request.yaml | low | allowlisted_synthetic_marker | N/A | Synthetic mock fixture contains controlled marker terms: SECRET. |
| data/mock_ingestion_requests/denied_non_synthetic_evidence_request.yaml | low | allowlisted_synthetic_marker | N/A | Synthetic mock fixture contains controlled marker terms: SECRET. |
| data/mock_ingestion_requests/denied_real_business_record_request.yaml | low | allowlisted_synthetic_marker | N/A | Synthetic mock fixture contains controlled marker terms: ABN, SECRET. |
| data/mock_ingestion_requests/denied_real_taxpayer_data_request.yaml | low | allowlisted_synthetic_marker | N/A | Synthetic mock fixture contains controlled marker terms: REAL_TAXPAYER, SECRET, TFN. |
| data/mock_ingestion_requests/denied_secret_marker_request.yaml | low | allowlisted_synthetic_marker | N/A | Synthetic mock fixture contains controlled marker terms: ACCESS_TOKEN, API_KEY, SECRET. |
| data/mock_ingestion_requests/denied_wrong_storage_zone_request.yaml | low | allowlisted_synthetic_marker | N/A | Synthetic mock fixture contains controlled marker terms: SECRET. |
| data/mock_ingestion_requests/review_required_high_sensitivity_mock_request.yaml | low | allowlisted_synthetic_marker | N/A | Synthetic mock fixture contains controlled marker terms: SECRET. |
| docs/ci_enforcement.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: SECRET. |
| docs/current_status.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: SECRET. |
| docs/decision_log_design.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: SECRET. |
| docs/evidence_requirements.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: INVOICE. |
| docs/known_risks.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: REAL_BUSINESS_RECORD, SECRET. |
| docs/mock_evidence_workflow.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: INVOICE, PAYSLIP, REAL_BUSINESS_RECORD, REAL_TAXPAYER, SECRET. |
| docs/pre_commit_usage.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: SECRET. |
| docs/privacy_and_secrecy_classification.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: ABN, API_KEY, MEDICARE_NUMBER, PASSWORD, PRIVATE_KEY, REAL_TAXPAYER, TAX_FILE_NUMBER, TFN. |
| docs/repository_guardrails.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: SECRET. |
| docs/secure_evidence_ingestion.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: ABN, ACN, API_KEY, INVOICE, MEDICARE_NUMBER, PAYSLIP, PRIVATE_KEY, REAL_BUSINESS_RECORD, REAL_TAXPAYER, SECRET, TFN. |
| docs/v1_5_plan.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: SECRET. |
| examples/groups/robotics_leasing_structure.yaml | low | documented_marker_example | N/A | Documentation/test file contains marker examples: INVOICE. |
| gitignore | low | documented_marker_example | N/A | Documentation/test file contains marker examples: SECRET. |
| model/carsf/avoidance.py | low | documented_model_marker_reference | N/A | Model file contains narrowly documented marker vocabulary: INVOICE. |
| model/carsf/classification.py | low | policy_marker_definition | N/A | Guardrail implementation contains policy marker definitions: ABN, API_KEY, BANK_ACCOUNT, INVOICE, MEDICARE_NUMBER, PASSWORD, PRIVATE_KEY, REAL_TAXPAYER, SECRET, TAX_FILE_NUMBER, TFN. |
| model/carsf/decision_log.py | low | documented_model_marker_reference | N/A | Model file contains narrowly documented marker vocabulary: API_KEY, PASSWORD, TFN. |
| model/carsf/evidence.py | low | documented_model_marker_reference | N/A | Model file contains narrowly documented marker vocabulary: EMPLOYMENT_CONTRACT, INVOICE. |
| model/carsf/evidence_packet.py | low | policy_marker_definition | N/A | Guardrail implementation contains policy marker definitions: ABN, API_KEY, BANK_ACCOUNT, MEDICARE_NUMBER, PASSWORD, PRIVATE_KEY, REAL_TAXPAYER, SECRET, TAX_FILE_NUMBER, TFN. |
| model/carsf/repo_guardrails.py | low | policy_marker_definition | N/A | Guardrail implementation contains policy marker definitions: API_KEY, INVOICE, PASSWORD, SECRET, TFN. |
| model/carsf/secure_ingestion.py | low | policy_marker_definition | N/A | Guardrail implementation contains policy marker definitions: ABN, ACN, API_KEY, INVOICE, MEDICARE_NUMBER, PAYSLIP, PRIVATE_KEY, REAL_BUSINESS_RECORD, REAL_TAXPAYER, SECRET, TFN. |
| model/carsf/sensitive_scan.py | low | policy_marker_definition | N/A | Guardrail implementation contains policy marker definitions: ABN, ACCESS_TOKEN, ACN, API_KEY, BANK_ACCOUNT, BSB, CREDIT_CARD, DATE_OF_BIRTH, EMPLOYMENT_CONTRACT, INVOICE, MEDICARE_NUMBER, PASSPHRASE, PASSWORD, PAYSLIP, PRIVATE_KEY, REAL_BUSINESS_RECORD, REAL_TAXPAYER, RESIDENTIAL_ADDRESS, SECRET, TAX_FILE_NUMBER, TFN. |
| model/tests/test_classification.py | low | documented_marker_example | N/A | Documentation/test file contains marker examples: PRIVATE_KEY. |
| model/tests/test_decision_log.py | low | documented_marker_example | N/A | Documentation/test file contains marker examples: API_KEY, PASSWORD, SECRET. |
| model/tests/test_evidence_packet.py | low | documented_marker_example | N/A | Documentation/test file contains marker examples: SECRET, TFN. |
| model/tests/test_ingestion_audit.py | low | documented_marker_example | N/A | Documentation/test file contains marker examples: API_KEY. |
| model/tests/test_public_data_pilot.py | low | documented_marker_example | N/A | Documentation/test file contains marker examples: PAYSLIP, TFN. |
| model/tests/test_redaction.py | low | documented_marker_example | N/A | Documentation/test file contains marker examples: API_KEY. |
| model/tests/test_repo_guardrail_script.py | low | documented_marker_example | N/A | Documentation/test file contains marker examples: SECRET. |
| model/tests/test_repo_guardrails.py | low | documented_marker_example | N/A | Documentation/test file contains marker examples: SECRET. |
| model/tests/test_secure_ingestion.py | low | documented_marker_example | N/A | Documentation/test file contains marker examples: API_KEY, SECRET. |
| model/tests/test_sensitive_scan.py | low | documented_marker_example | N/A | Documentation/test file contains marker examples: BANK_ACCOUNT, MEDICARE_NUMBER, SECRET, TFN. |
| paper/CARSF_V1_5_WORKING.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: REAL_TAXPAYER. |
| paper/aava_deductibility_appendix.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: INVOICE. |
| paper/export_notes.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: REAL_TAXPAYER. |
| release/v1_5_rc/NON_CLAIM_BOUNDARIES.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: REAL_TAXPAYER. |
| release/v1_5_rc/attack_pack/PRIVACY_SECRECY_REVIEW_ATTACKS.md | low | documented_marker_example | N/A | Documentation/test file contains marker examples: REAL_TAXPAYER. |
| schedules/accounting_administration.yaml | low | documented_marker_example | N/A | Documentation/test file contains marker examples: INVOICE. |
| schedules/automotive_repair.yaml | low | documented_marker_example | N/A | Documentation/test file contains marker examples: INVOICE. |
| scripts/run_evidence_workflow.py | low | policy_marker_definition | N/A | Guardrail implementation contains policy marker definitions: INVOICE, REAL_TAXPAYER, SECRET. |
| scripts/run_ingestion_controls.py | low | policy_marker_definition | N/A | Guardrail implementation contains policy marker definitions: INVOICE, SECRET. |
| scripts/run_repo_guardrails.py | low | policy_marker_definition | N/A | Guardrail implementation contains policy marker definitions: SECRET. |
| simulator/pages/10_Secure_Ingestion_Controls.py | low | policy_marker_definition | N/A | Guardrail implementation contains policy marker definitions: SECRET. |
| simulator/pages/11_Repository_Guardrails.py | low | policy_marker_definition | N/A | Guardrail implementation contains policy marker definitions: SECRET. |

## F. Allowlisted Synthetic Fixture Findings

| Path | Severity | Type | Line | Message |
| --- | --- | --- | --- | --- |
| data/mock_ingestion_requests/allowed_mock_evidence_request.yaml | low | allowlisted_synthetic_marker | N/A | Synthetic mock fixture contains controlled marker terms: SECRET. |
| data/mock_ingestion_requests/denied_non_synthetic_evidence_request.yaml | low | allowlisted_synthetic_marker | N/A | Synthetic mock fixture contains controlled marker terms: SECRET. |
| data/mock_ingestion_requests/denied_real_business_record_request.yaml | low | allowlisted_synthetic_marker | N/A | Synthetic mock fixture contains controlled marker terms: ABN, SECRET. |
| data/mock_ingestion_requests/denied_real_taxpayer_data_request.yaml | low | allowlisted_synthetic_marker | N/A | Synthetic mock fixture contains controlled marker terms: REAL_TAXPAYER, SECRET, TFN. |
| data/mock_ingestion_requests/denied_secret_marker_request.yaml | low | allowlisted_synthetic_marker | N/A | Synthetic mock fixture contains controlled marker terms: ACCESS_TOKEN, API_KEY, SECRET. |
| data/mock_ingestion_requests/denied_wrong_storage_zone_request.yaml | low | allowlisted_synthetic_marker | N/A | Synthetic mock fixture contains controlled marker terms: SECRET. |
| data/mock_ingestion_requests/review_required_high_sensitivity_mock_request.yaml | low | allowlisted_synthetic_marker | N/A | Synthetic mock fixture contains controlled marker terms: SECRET. |

## G. Storage Boundary Checks

- Prohibited paths: data/incoming/, data/private/, data/restricted/, data/real_evidence/, evidence_inbox/, secure_drop/, .env, .env., secrets/, private/
- Allowed mock paths: data/mock_evidence/, data/mock_ingestion_requests/

| Path | Severity | Type | Line | Message |
| --- | --- | --- | --- | --- |
| none | none | none | none | none |

## H. Generated Report Checks

- Generated reports must include prototype/non-claim language.
- Generated reports must not include raw evidence packet payload markers.

| Path | Severity | Type | Line | Message |
| --- | --- | --- | --- | --- |
| none | none | none | none | none |

## I. Secret/Evidence Path Checks

- Prohibited extensions: .pem, .key, .p12, .pfx, .secret, .crt, .cer, .der, .sqlite, .db, .mdb, .accdb

| Path | Severity | Type | Line | Message |
| --- | --- | --- | --- | --- |
| none | none | none | none | none |

## J. Required Non-Claim Checks

Required non-claim patterns are intentionally broad and prototype-only:

- `not legal`
- `not a legal`
- `not legal, tax`
- `prototype`
- `not a complete dlp`
- `not a tax`
- `not a tax calculator`
- `not a secure evidence platform`
- `not transfer-pricing adjustments`

## K. Limitations

- These guardrails are over-blocking by design.
- They are not a complete DLP, secret scanner, cybersecurity product, legal/privacy audit, Treasury control, ATO control, or forensic validation.
- Passing this scan does not prove that the repository is free of sensitive content.
- Real evidence must not enter this repository.
