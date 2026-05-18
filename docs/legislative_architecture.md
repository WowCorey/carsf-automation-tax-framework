# Legislative Architecture Skeleton

The legislative architecture skeleton is a non-operative map showing where CARSF V1.5 concepts could sit in a future legal architecture for external review.

Run:

```powershell
python scripts/run_legislative_architecture.py
```

Generated reports:

- `reports/legislative_architecture.md`
- `reports/legislative_architecture.json`

## Scope

The skeleton maps:

- proposed Parts and Divisions;
- definition placeholders;
- sector schedule placeholders;
- formula and liability architecture placeholders;
- safe-harbour placeholders;
- anti-avoidance and integrity placeholders;
- grouped-entity and related-party placeholders;
- evidence and information architecture placeholders;
- safeguards and review placeholders;
- privacy, secrecy, and data-handling placeholders;
- regulation-making placeholders;
- commencement and transitional placeholders;
- external-review blockers and areas reserved for counsel.

## Non-Claims

This is a non-operative legislative architecture skeleton only. It is not operative law, not a Bill, not legal drafting, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, and not Parliamentary Counsel drafting. It is not legally sufficient and it has not been constitutionally reviewed.

It creates no rights, obligations, statutory powers, information-gathering powers, notices, penalties, enforcement process, or compliance scoring. It does not determine tax payable, does not use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, and does not modify firm-level CARSF liability.

## Review Requirements

The skeleton is intended to make review blockers explicit before any law-shaped work occurs. It reserves operative definitions, liability architecture, evidence powers, anti-avoidance rules, review rights, regulation-making mechanisms, commencement, and transitional rules for external legal, tax, Treasury, ATO, Parliamentary Counsel, privacy, calibration, administrative-design, and policy review.

## Outputs

The runner validates that:

- all Parts are marked non-operative;
- all Divisions include external-review flags;
- core CARSF definition placeholders exist;
- definition placeholders cannot be used as operative definitions;
- sector schedule placeholders reference existing schedule YAML files and are marked not official;
- evidence-power placeholders create no powers, notices, or real-data ingestion;
- regulation-making placeholders create no real powers;
- anti-avoidance placeholders remain non-operative;
- summary flags for operative law, powers, notices, penalties, enforcement, real data, and firm-level liability changes remain false.

## Release Candidate Cross-Reference

The V1.5 release-candidate pack references this skeleton as one review layer only. The pack does not make the skeleton legal advice, tax advice, ATO guidance, Treasury modelling, economic validation, welfare advice, statistical validation, compliance scoring, enforcement, operational readiness, legal sufficiency, legislative readiness, a readiness score, or an official review pathway. It does not determine actual tax payable, does not use taxpayer-level, firm-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data, and does not modify firm-level CARSF liability.
