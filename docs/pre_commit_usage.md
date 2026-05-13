# Pre-Commit Usage

Status: optional local developer guardrail.

## Purpose

`.pre-commit-config.yaml` defines a local hook that runs:

```powershell
python scripts/run_repo_guardrails.py
```

This is optional unless a local developer chooses to install and run pre-commit. CI remains the enforced gate.

## Install Locally

```powershell
python -m pip install pre-commit
pre-commit install
```

Run manually:

```powershell
pre-commit run carsf-repo-guardrails --all-files
```

## Non-Claims

The hook is a prototype convenience guardrail only. It is not complete DLP, secret-scanning, cybersecurity, legal/privacy audit, Treasury control, ATO control, or forensic validation.
