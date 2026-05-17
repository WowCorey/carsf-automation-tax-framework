# Behavioural Response / Gaming Simulation

The behavioural response simulation layer maps synthetic CARSF response pathways to placeholder pressure bands, linked avoidance flags, and review pathways.

It simulates response pathways, not outcomes.

## Synthetic Pathways

The scenario file is `examples/behavioural_response_scenarios.yaml`.

Covered prototype pathways include:

- token human oversight
- fake QLC inflation
- entity splitting
- offshore automation service routing
- related-party AI service fees
- cloud / inference relabelling
- robotics leasing shifts
- customer self-service shifts
- schedule classification arbitrage
- artificial low profit or AAVA
- platform IP royalty routing
- open-source AI treatment gaps
- mixed-unit apportionment gaming

## Review Outputs

The module produces:

- response pressure bands
- linked avoidance flags
- countermeasure categories
- review statuses
- external-review flags
- suppression until calibration where dependencies are unresolved
- calibration blockers

Every result has:

- `do_not_predict: true`
- `do_not_score_real_taxpayer: true`
- `firm_level_liability_logic_modified: false`

## Non-Claims

Behavioural response simulation is prototype-only deterministic placeholder scenario review. It does not predict taxpayer behaviour. It does not estimate behavioural elasticity. It is not ATO audit logic, Treasury modelling, ABS/ATO/DSS/PBO analysis, economic validation, compliance-risk scoring, legal advice, tax advice, or investment advice. It does not estimate actual tax payable, modify firm-level CARSF liability, implement penalties, or implement enforcement.

The simulation does not use firm-level, taxpayer-level, industry, ABS, ATO, DSS, Treasury, PBO, HILDA, or Census data. All response scenarios are synthetic placeholders requiring external calibration, legal review, ATO/Treasury methods review, and behavioural research.

## Run Command

```powershell
python scripts/run_behavioural_response_simulation.py
```

Generated reports:

- `reports/behavioural_response_simulation.md`
- `reports/behavioural_response_simulation.json`

## Future Work

Build 20 should add an ATO / administrative compliance workflow for organising evidence requests, review states, behavioural-response flags, sector schedule review, grouped-entity review, transfer-pricing review, and escalation pathways without claiming real ATO enforcement powers or operational readiness.
