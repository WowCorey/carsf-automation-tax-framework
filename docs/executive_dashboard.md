# Executive Dashboard Consolidation

Status: V1.5 prototype dashboard and report index only.

## Purpose

The executive dashboard consolidates the existing CARSF V1.5 prototype stack into a single navigation layer. It indexes major model layers, generated reports, Streamlit pages, non-claim profiles, calibration blockers, external-review blockers, suggested review navigation, and reviewer routing.

It does not add a new tax, fiscal, household, behavioural, legislative, or welfare model.

## Non-Claims

- This is a prototype dashboard and report index only.
- It is not legal advice.
- It is not tax advice.
- It is not ATO guidance.
- It is not Treasury modelling.
- It is not economic validation.
- It is not welfare advice.
- It is not compliance scoring.
- It is not enforcement.
- It is not operational readiness.
- It is not legal sufficiency.
- It is not legislative readiness.
- It is not a readiness score.
- It is not an official review pathway.
- It does not determine actual tax payable.
- It does not use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data.
- It does not modify firm-level CARSF liability.

## Manifest

Dashboard metadata lives in:

- `data/dashboard/executive_dashboard_manifest.yaml`

The manifest lists prototype layers, primary files, generated reports, Streamlit pages, status labels, non-claim flags, calibration blockers, external-review blockers, reviewer categories, suggested read order, and prohibited uses.

## Reports

Generate dashboard reports with:

```powershell
python scripts/run_executive_dashboard.py
```

Generated reports:

- `reports/executive_dashboard.md`
- `reports/executive_dashboard.json`

## Streamlit

The dashboard page is:

- `simulator/pages/25_Executive_Dashboard.py`

The main simulator landing page points reviewers toward the dashboard before the deeper pages.

## Review Boundaries

The suggested read order is review navigation only. It is not an official process, approval route, implementation pathway, or readiness finding. Each linked layer keeps its own non-claim warnings and blockers.

Future work should update this dashboard whenever a new generated report, Streamlit page, or major documentation layer is added.

Build 26 adds `reports/real_data_feasibility.md` as a feasibility and calibration-intake map. It does not load real data, complete calibration, validate the model, or change firm-level liability. Dashboard and release indexes should treat it as a data-governance and pilot-planning layer only.

## Relationship to Release Candidate Pack

Build 23 adds `release/v1_5_rc/` and `reports/v1_5_release_candidate_pack.*`. The executive dashboard remains the navigation entry point; the release-candidate pack packages the working paper, release notes, reviewer briefing, report map, calibration blockers, non-claim boundaries, and external-review routing for external review.

The release-candidate pack is not legal advice, tax advice, ATO guidance, Treasury modelling, economic validation, welfare advice, statistical validation, compliance scoring, enforcement, operational readiness, legal sufficiency, legislative readiness, a readiness score, or an official review pathway. It does not determine actual tax payable, does not use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, and does not modify firm-level CARSF liability.
