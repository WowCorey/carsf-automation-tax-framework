# Secure Evidence Ingestion

Status: V1.5 prototype governance controls.

## Purpose

The secure-ingestion layer defines a default-deny policy before any non-synthetic evidence could be handled. It exists to protect the repository from accidental ingestion of real personal data, taxpayer data, business records, restricted government data, credentials, or source documents.

## Default Rule

Only synthetic mock evidence may be stored in this repository, and only under `data/mock_evidence/`.

All non-synthetic evidence is denied and must be routed to a future external secure system design.

## Denied Content

The prototype policy denies:

- personal data
- real taxpayer data
- real business records
- restricted government data
- secrets, API keys, tokens, credentials, and private keys
- TFNs, ABNs, ACNs, Medicare numbers, bank details, payslips, invoices, contracts, and employment records

## Storage Boundary

Evidence must not be stored under `reports/`, `docs/`, `paper/`, `model/`, `simulator/`, `scripts/`, the repo root, or likely evidence intake folders. Reports and docs may contain derived synthetic summaries only.

The `.gitignore` blocks likely real-evidence and secret paths such as `data/incoming/`, `data/private/`, `data/restricted/`, `data/real_evidence/`, `evidence_inbox/`, `secure_drop/`, `*.secret`, `*.key`, `*.pem`, `*.p12`, and `*.pfx`.

## Reports

Run:

```powershell
python scripts/run_ingestion_controls.py
```

Generated reports:

- `reports/secure_ingestion_controls.md`
- `reports/secure_ingestion_controls.json`

## Non-Claims

These controls are prototype governance controls only. They do not create legal, privacy, cybersecurity, evidentiary, forensic, Treasury, ATO, tax, or audit validation.

Future real evidence handling requires external secure infrastructure, legal/privacy review, data-owner approval, security review, access controls, retention controls, deletion controls, and formal audit logging.
