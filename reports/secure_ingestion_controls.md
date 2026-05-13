# CARSF V1.5 Secure Evidence Ingestion Controls

Generated at: `2026-05-13T09:38:46+00:00`

## A. Purpose

This report previews default-deny ingestion controls before any non-synthetic evidence is ever handled.

## B. Non-Claims

- These controls are prototype governance controls only. They do not create legal, privacy, cybersecurity, evidentiary, forensic, Treasury, ATO, tax, or audit validation.
- This is a prototype ingestion-control decision only. It is not a legal, privacy, cybersecurity, tax, ATO, Treasury, evidentiary, forensic, or audit determination.
- These controls are governance scaffolding only and do not implement secure storage or real access control.

## C. Default-Deny Policy

- Policy: `carsf-v1.5-default-deny-ingestion`
- Default action: `DENY`
- Allowed modes: synthetic_mock
- Only synthetic mock evidence is allowed in this repository.
- Any real personal, taxpayer, business, restricted, credential, or non-synthetic evidence is denied.

## D. Storage Zones

- Allowed evidence storage zones: data/mock_evidence/
- Prohibited evidence storage zones: reports/, docs/, paper/, model/, simulator/, scripts/, ./, data/incoming/, data/private/, data/restricted/, data/real_evidence/, evidence_inbox/, secure_drop/
- Reports and docs may contain derived synthetic summary text only; they must not contain evidence payloads.

## E. Ingestion Request Table

| Request | Mode | Storage Zone | Synthetic Only | Sensitivity | Decision | Allowed | Required Approvals |
| --- | --- | --- | --- | --- | --- | --- | --- |
| allowed_mock_evidence_request | synthetic_mock | data/mock_evidence/ | true | low | ALLOW_SYNTHETIC_MOCK_ONLY | true | none |
| denied_non_synthetic_evidence_request | external_real | data/mock_evidence/ | false | moderate | DENY | false | external_secure_system_design |
| denied_real_business_record_request | synthetic_mock | data/mock_evidence/ | true | high | DENY | false | legal_tax_review, privacy_review |
| denied_real_taxpayer_data_request | synthetic_mock | data/mock_evidence/ | true | restricted_placeholder | DENY | false | privacy_review |
| denied_secret_marker_request | synthetic_mock | data/mock_evidence/ | true | restricted_placeholder | DENY | false | privacy_review, security_review |
| denied_wrong_storage_zone_request | synthetic_mock | reports/ | true | low | DENY | false | none |
| review_required_high_sensitivity_mock_request | synthetic_mock | data/mock_evidence/ | true | high | ALLOW_SYNTHETIC_MOCK_WITH_REVIEW | true | privacy_review |

## F. Sensitive Scan Results

| Request | Clean | Severity | Markers Found | Deny Ingestion |
| --- | --- | --- | --- | --- |
| allowed_mock_evidence_request | true | none | none | false |
| denied_non_synthetic_evidence_request | true | none | none | false |
| denied_real_business_record_request | false | high | ABN | true |
| denied_real_taxpayer_data_request | false | critical | REAL_TAXPAYER, TFN | true |
| denied_secret_marker_request | false | critical | ACCESS_TOKEN, API_KEY, SECRET | true |
| denied_wrong_storage_zone_request | true | none | none | false |
| review_required_high_sensitivity_mock_request | true | none | none | false |

## G. Redaction Handling

- Sensitive markers deny repo ingestion rather than creating redacted copies inside the repository.
- Redaction plans describe external secure-system handling only and do not output original sensitive values.

| Request | Redaction Required | Denied Fields | Main Warning |
| --- | --- | --- | --- |
| allowed_mock_evidence_request | false | none | No redaction required for clean synthetic mock metadata. |
| denied_non_synthetic_evidence_request | true | none | Non-synthetic evidence requires external secure-system design before any redaction workflow. |
| denied_real_business_record_request | true | ABN | Sensitive markers were found; repo ingestion must be denied rather than creating a redacted repo copy. |
| denied_real_taxpayer_data_request | true | REAL_TAXPAYER, TFN | Sensitive markers were found; repo ingestion must be denied rather than creating a redacted repo copy. |
| denied_secret_marker_request | true | ACCESS_TOKEN, API_KEY, SECRET | Sensitive markers were found; repo ingestion must be denied rather than creating a redacted repo copy. |
| denied_wrong_storage_zone_request | false | none | No redaction required for clean synthetic mock metadata. |
| review_required_high_sensitivity_mock_request | false | none | No redaction required for clean synthetic mock metadata. |

## H. Retention/Access-Control Policy

| Request | Retention Action | Deletion Required | Access Policy | Approval Required |
| --- | --- | --- | --- | --- |
| allowed_mock_evidence_request | retain_in_repo | false | synthetic-mock-repo-access | false |
| denied_non_synthetic_evidence_request | deny_repo_retention | true | external-secure-access-required | true |
| denied_real_business_record_request | deny_repo_retention | true | synthetic-mock-access-review | true |
| denied_real_taxpayer_data_request | deny_repo_retention | true | synthetic-mock-access-review | true |
| denied_secret_marker_request | deny_repo_retention | true | synthetic-mock-access-review | true |
| denied_wrong_storage_zone_request | deny_repo_retention | true | synthetic-mock-repo-access | false |
| review_required_high_sensitivity_mock_request | retain_in_repo | false | synthetic-mock-access-review | true |

## I. Audit-Record Preview

| Request | Record ID | Allowed | Previous Hash | Record Hash |
| --- | --- | --- | --- | --- |
| allowed_mock_evidence_request | ingestion-audit-a98d8c465756cc49 | true | none | a98d8c465756cc49b55bd694b460874be01ebc850245549f43478d1e97a8e553 |
| denied_non_synthetic_evidence_request | ingestion-audit-b0da21e1d7975a5b | false | a98d8c465756cc49b55bd694b460874be01ebc850245549f43478d1e97a8e553 | b0da21e1d7975a5bc77d8bb7405ebed93694d7b19831fe137c93f15e3deaf700 |
| denied_real_business_record_request | ingestion-audit-1e6a58a2c91550d4 | false | b0da21e1d7975a5bc77d8bb7405ebed93694d7b19831fe137c93f15e3deaf700 | 1e6a58a2c91550d47edd4f2c597b45a4deb9396231f9214c8d1aac4ed4f7d099 |
| denied_real_taxpayer_data_request | ingestion-audit-1b19c840166866c6 | false | 1e6a58a2c91550d47edd4f2c597b45a4deb9396231f9214c8d1aac4ed4f7d099 | 1b19c840166866c6803200dd25744f994aeb101feb0314b557da3138c41372e5 |
| denied_secret_marker_request | ingestion-audit-5e0062a58f38241b | false | 1b19c840166866c6803200dd25744f994aeb101feb0314b557da3138c41372e5 | 5e0062a58f38241b4683afcb12070085dbd650d10e4b82bc6cbe24124687c6c4 |
| denied_wrong_storage_zone_request | ingestion-audit-95b4021a0d3e36bb | false | 5e0062a58f38241b4683afcb12070085dbd650d10e4b82bc6cbe24124687c6c4 | 95b4021a0d3e36bbbf6bcc808d965a074c948f20f5a905bdb502c8d9ab46cc22 |
| review_required_high_sensitivity_mock_request | ingestion-audit-10dec2619fbf0878 | true | 95b4021a0d3e36bbbf6bcc808d965a074c948f20f5a905bdb502c8d9ab46cc22 | 10dec2619fbf08780bf98d5952deeab44b91edc894583d20dde00b66e0735ec9 |

## J. Denied Request Explanations

### denied_non_synthetic_evidence_request
- Default action is DENY; request must satisfy every allow condition.
- evidence_mode `external_real` is not allowed in this repo.
- non-synthetic evidence is denied and must be handled outside this repo.

### denied_real_business_record_request
- Default action is DENY; request must satisfy every allow condition.
- declared real taxpayer/business data is denied.
- sensitive scanner found prohibited markers: ABN.

### denied_real_taxpayer_data_request
- Default action is DENY; request must satisfy every allow condition.
- declared personal data is denied.
- sensitive scanner found prohibited markers: REAL_TAXPAYER, TFN.

### denied_secret_marker_request
- Default action is DENY; request must satisfy every allow condition.
- declared secrets or credentials are denied.
- sensitive scanner found prohibited markers: ACCESS_TOKEN, API_KEY, SECRET.

### denied_wrong_storage_zone_request
- Default action is DENY; request must satisfy every allow condition.
- storage_zone `reports/` is not an allowed evidence storage zone.
- storage_zone `reports/` is explicitly prohibited for evidence storage.

## K. Why Real Evidence Must Not Enter This Repo

- The repository is a policy-modelling prototype, not a secure evidence platform.
- Git history is not an appropriate storage mechanism for real personal, taxpayer, restricted, credential, payroll, invoice, contract, or transfer-pricing evidence.
- Any future real evidence workflow requires external secure storage, access controls, legal/privacy review, retention controls, and audit procedures.

## L. Future Secure-System Requirements

- External secure evidence store with encryption and access control.
- Intake quarantine, malware scanning, DLP controls, and redaction tooling.
- Role-based approval workflow for legal, tax, privacy, data-owner, and security review.
- Immutable audit logs with retention and deletion controls.
- Clear ban on committing real evidence or secrets to this repository.
