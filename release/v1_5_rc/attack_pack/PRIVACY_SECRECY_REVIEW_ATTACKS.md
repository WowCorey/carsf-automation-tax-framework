# Privacy / Secrecy Review Attacks

This attack document does not mean external review has been completed, does not mean approval has been granted, and does not mean validation has occurred. It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare validation, not statistical validation, not compliance scoring, not enforcement, and does not modify firm-level CARSF liability.

## What To Inspect First

- `reports/secure_ingestion_controls.md`
- `reports/repo_guardrails.md`
- `reports/mock_evidence_workflow.md`

## Attack Questions

- Can any path accept real taxpayer, firm, welfare, or restricted data?
- Do privacy/secrecy labels look formal?
- Are redaction, retention, IAM, secure storage, and audit logging limits visible?
- Are synthetic household layers clearly synthetic?
- Are repository guardrails strong enough for data-exclusion boundaries?

## Likely Failure Modes

- A path appears able to store real data.
- Prototype classifications resemble formal markings.
- Secure-ingestion controls look like a secure environment.
- Redaction documentation appears to permit real records in repo.
- Household examples look like real records.

## Required Evidence / External Review

- Privacy impact review.
- Secrecy review.
- DLP review.
- Secure storage review.
- Retention and IAM review.

## What Not To Infer

- Do not infer real-data handling approval, privacy compliance, secrecy compliance, secure storage, validation, approval, or firm-level liability change.

## Locked-Until-Review Items

- Real-data ingestion.
- Privacy classification.
- Secrecy handling.
- Secure storage.
- Retention and IAM.

## Suggested Reviewer Output Format

Use data path, privacy/secrecy boundary, control gap, required external system review, and required repository change.

