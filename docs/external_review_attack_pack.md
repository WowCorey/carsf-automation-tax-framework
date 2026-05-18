# External Review Attack Pack

This is an attack pack for external review. It does not mean external review has been completed, does not mean approval has been granted, and does not mean validation has occurred. It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare validation, not statistical validation, not compliance scoring, not enforcement, not operational readiness, not legal sufficiency, not legislative readiness, not a readiness score, not official status, and not an official review pathway. It does not determine actual tax payable, does not use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, and does not modify firm-level CARSF liability.

## Purpose

Build 24 adds a structured reviewer challenge layer for the V1.5 release candidate. It turns known limitations, release routes, generated reports, and prototype layers into discipline-specific attack questions, likely failure modes, evidence requests, boundary checks, and locked-until-review items.

## Review Tracks

- Policy review.
- Technical review.
- Legal review.
- Tax review.
- ATO methods review.
- Treasury methods review.
- Privacy / secrecy review.
- Statistical methods review.
- Economic methods review.
- Welfare policy review.
- Parliamentary Counsel review.
- Hostile / red-team review.

## Generated Reports

Run:

```powershell
python scripts/run_external_review_attack_pack.py
```

Generated reports:

- `reports/external_review_attack_pack.md`
- `reports/external_review_attack_pack.json`

## Release Documents

The release-facing attack pack is under:

- `release/v1_5_rc/attack_pack/`

It includes reviewer-specific attack documents, report and layer matrices, boundary checks, and a manifest snapshot.

## Boundaries

The attack pack is challenge material only. Severity labels are challenge labels, not risk scores, validation outcomes, approval statuses, readiness ratings, or official review outcomes.

