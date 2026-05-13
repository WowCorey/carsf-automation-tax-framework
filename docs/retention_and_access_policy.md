# Retention and Access Policy

Status: V1.5 prototype retention/access-control documentation.

## Retention Rule

Synthetic mock evidence may be retained in the repository when it is stored under `data/mock_evidence/`.

Real evidence, restricted evidence, non-synthetic evidence, personal data, taxpayer data, business records, credentials, and source documents must not be retained in the repository.

## Access-Control Rule

The prototype can describe access-control expectations, but it does not enforce real IAM.

High-sensitivity mock scenarios require review before external sharing. Non-synthetic evidence requires an external secure access-control design.

## Out of Scope

The repository does not provide:

- encrypted evidence storage
- role-based access control
- secure upload portals
- retention enforcement
- deletion enforcement
- data-owner approval workflow

## Non-Claims

This is prototype retention/access-control documentation only. It is not real IAM, legal, privacy, cybersecurity, evidentiary, forensic, Treasury, ATO, tax, or audit enforcement.
