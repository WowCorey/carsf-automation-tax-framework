# V1.5 Release Candidate Pack

Status: private research prototype release-candidate packaging.

## Purpose

The V1.5 release-candidate pack consolidates the current CARSF prototype stack into a working-paper and reviewer-navigation package. It indexes prototype layers, generated reports, release notes, reviewer briefing, report map, calibration blockers, non-claim boundaries, external-review routing, and release manifest metadata.

## Non-Claims

- This is a private research prototype and release-candidate pack only.
- It is not legal advice.
- It is not tax advice.
- It is not ATO guidance.
- It is not Treasury modelling.
- It is not economic validation.
- It is not welfare advice.
- It is not statistical validation.
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

## Files

- `data/release/v1_5_release_manifest.yaml`
- `release/v1_5_rc/RELEASE_NOTES.md`
- `release/v1_5_rc/REVIEWER_BRIEFING.md`
- `release/v1_5_rc/REPORT_MAP.md`
- `release/v1_5_rc/CALIBRATION_BLOCKERS.md`
- `release/v1_5_rc/NON_CLAIM_BOUNDARIES.md`
- `release/v1_5_rc/EXTERNAL_REVIEW_ROUTING.md`
- `release/v1_5_rc/RELEASE_MANIFEST.json`

## Runner

Generate release-candidate pack reports with:

```powershell
python scripts/run_v1_5_release_candidate_pack.py
```

Generated reports:

- `reports/v1_5_release_candidate_pack.md`
- `reports/v1_5_release_candidate_pack.json`

## Working Paper Link

The V1.5 working paper remains `paper/CARSF_V1_5_WORKING.md`. The release-candidate update adds a stack map and cross-references to current prototype layers; it does not convert the paper into legal drafting, official policy, or validation.

## Review Use

Use the release pack after the executive dashboard. The pack is useful for routing external review, identifying calibration blockers, and checking report boundaries. It must not be used as a readiness finding, official review pathway, legal sufficiency claim, operational readiness claim, economic validation, welfare validation, statistical validation, or actual-tax-payable analysis.
