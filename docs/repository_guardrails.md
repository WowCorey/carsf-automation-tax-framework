# Repository Guardrails

Status: V1.5 prototype repository enforcement gates.

## Purpose

Repository guardrails provide a fail-closed scan for likely evidence leaks, secret markers, prohibited storage zones, unsafe generated report content, and accidental real-data commits.

They are deliberately conservative. Synthetic mock fixtures are allowlisted only in controlled paths and only when they are explicitly marked as synthetic.

## What Is Enforced

- Prohibited evidence and secret storage paths such as `data/incoming/`, `data/private/`, `data/restricted/`, `data/real_evidence/`, `evidence_inbox/`, `secure_drop/`, `secrets/`, and `private/`.
- Prohibited secret or database file extensions such as `.pem`, `.key`, `.p12`, `.pfx`, `.secret`, `.crt`, `.cer`, `.der`, `.sqlite`, `.db`, `.mdb`, and `.accdb`.
- Sensitive-marker findings outside allowlisted synthetic fixtures, documentation, tests, and governance implementation files.
- Synthetic mock fixtures under `data/mock_evidence/` and `data/mock_ingestion_requests/` must include `synthetic_mock_evidence_only: true`.
- Generated reports must include prototype/non-claim language and must not contain raw evidence packet payload markers.

## Run

```powershell
python scripts/run_repo_guardrails.py
```

Generated reports:

- `reports/repo_guardrails.md`
- `reports/repo_guardrails.json`

The script exits with a non-zero code when denied findings exist.

## Non-Claims

These are prototype repository guardrails only. They are not a complete DLP system, secret scanner, cybersecurity control, legal/privacy audit, Treasury control, ATO control, or forensic validation.

Passing the scan does not prove that the repository is free of sensitive content. Real evidence must not enter this repository.
