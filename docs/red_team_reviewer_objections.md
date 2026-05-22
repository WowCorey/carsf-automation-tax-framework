# CARSF V1.5 Red-Team Reviewer Objections Pack

This is a red-team reviewer objections pack only. No new data is loaded by this build. It does not externally verify source values, does not scrape public sources, and does not call external APIs.

Objections being acknowledged does not mean they are resolved. Partially mitigated does not mean solved. This is not calibration; calibration has not been completed. Public data does not prove the model works. Realistic placeholders remain placeholders, are not real data, and are not calibrated. Source references are not loaded datasets. Restricted-data requirements are not data access.

This is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, and not official status. It does not determine actual tax payable, does not use taxpayer-level data, firm-level confidential data, household microdata, ABS DataLab, HILDA microdata, DSS/Services Australia records, ATO taxpayer records, Treasury/PBO confidential material, or restricted government data, and does not modify firm-level CARSF liability.

## What It Adds

- Objection status taxonomy.
- Severity taxonomy.
- Objection category taxonomy.
- A 41-item reviewer objection catalogue.
- Per-objection explanations for why each concern is valid.
- Current project response text bounded by non-claim warnings.
- What the project can say.
- What the project must not claim.
- Unresolved blocker mapping.
- Evidence needed to resolve each objection.
- Build 30 handoff route.

## Generated Reports

- `reports/red_team_reviewer_objections.md`
- `reports/red_team_reviewer_objections.json`

## Runner

Run:

```bash
python scripts/run_red_team_reviewer_objections.py
```

The runner validates required categories, required fields, objection counts, unresolved blockers, future evidence needs, forbidden affirmative claims, and false readiness/legal/validation flags.

## Dashboard

The existing public-data evidence dashboard can display the red-team objection summary if `reports/red_team_reviewer_objections.json` exists. The section is reviewer-navigation only and does not create any score, validation outcome, approval, external source check, legal sufficiency, operational readiness, official status, or tax-payable result.

## Current Limits

The pack is intentionally an objections catalogue, not a defence brief. It does not resolve objections and does not add evidence. A future reviewer handoff pack can use it to show external reviewers what to inspect first and what remains unresolved.

Build 31 adds a controlled public real aggregate-data loader over existing source-located public-pilot values. It does not resolve the objections in this pack. Public aggregate data does not equal calibration, does not prove the model works, does not determine actual tax payable, does not create official status, and does not modify firm-level CARSF liability.
## Build 32 Placeholder Replacement Objection Boundary

Build 32 may make public aggregate anchors look more concrete, but it remains a placeholder replacement map only. No new data is loaded, no objection is resolved, public aggregate replacement does not mean validation, public aggregate narrowing does not mean statistical estimation, and the map does not complete calibration, prove the model works, determine actual tax payable, create official status, or modify firm-level CARSF liability.

## Build 33 Calibration Boundary Objection Boundary

Build 33 may make allowed-use labels look more settled than they are, but it remains a boundary map only. No new data is loaded, no objection is resolved, public aggregate boundary mapping does not mean validation or statistical estimation, and the map does not complete calibration, prove the model works, determine actual tax payable, create legal sufficiency, create official status, or modify firm-level CARSF liability.
Build 34 turns several red-team risks into explicit scenario constraints. Outputs that could be mistaken for calibration, validation, tax payable, firm liability, legal sufficiency, official status, statistical estimation, economic validation, welfare validation, or implementation readiness are marked non-interpretable, hidden, downgraded, or fail-closed.

## Build 34.5 Integrity Audit Link

Build 34.5 adds a full repo integrity audit that carries red-team concerns into missing-factor, data-dependency, external-review dependency, guardrail, and non-claim coverage registers. The audit loads no new data, does not resolve objections, does not calibrate or validate the model, does not determine actual tax payable, and does not modify firm-level CARSF liability.
