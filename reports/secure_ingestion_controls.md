# CARSF V1.5 Secure Evidence Ingestion Controls

Generated at: `2026-05-13T11:46:05+00:00`

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
| denied_non_synthetic_evidence_request | external_real | data/mock_evidence/ | true | moderate | DENY | false | none |
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
| denied_non_synthetic_evidence_request | ingestion-audit-d56b971430485e7f | false | a98d8c465756cc49b55bd694b460874be01ebc850245549f43478d1e97a8e553 | d56b971430485e7f9266466b3403a353e3649c184729591d08011d2a8f61a3f9 |
| denied_real_business_record_request | ingestion-audit-04104f9d5f47b20a | false | d56b971430485e7f9266466b3403a353e3649c184729591d08011d2a8f61a3f9 | 04104f9d5f47b20aa66f117a4533fe19779e69736be6978f7015f158bcb2d60f |
| denied_real_taxpayer_data_request | ingestion-audit-b137b54714d72ca2 | false | 04104f9d5f47b20aa66f117a4533fe19779e69736be6978f7015f158bcb2d60f | b137b54714d72ca2a16f84bf9db88b68271ebc0dfebb3a3a5258b0fd582f7d8e |
| denied_secret_marker_request | ingestion-audit-1e03ff8b44f7aee0 | false | b137b54714d72ca2a16f84bf9db88b68271ebc0dfebb3a3a5258b0fd582f7d8e | 1e03ff8b44f7aee0bc9a80a8ba5a18bbd0ba4f342d2e4da4aed13604a0816a53 |
| denied_wrong_storage_zone_request | ingestion-audit-4e94b06fb6f6bfb5 | false | 1e03ff8b44f7aee0bc9a80a8ba5a18bbd0ba4f342d2e4da4aed13604a0816a53 | 4e94b06fb6f6bfb5a4f762fbda8d07c18181efe438c249d3f8ab654446439109 |
| review_required_high_sensitivity_mock_request | ingestion-audit-a21526dcac3151ac | true | 4e94b06fb6f6bfb5a4f762fbda8d07c18181efe438c249d3f8ab654446439109 | a21526dcac3151ac1fc7daf253c6c1f58b52f38ed69c5857e3d2f42e74a0147c |

## J. Denied Request Explanations

### denied_non_synthetic_evidence_request
- Default action is DENY; request must satisfy every allow condition.
- evidence_mode `external_real` is not allowed in this repo.

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
