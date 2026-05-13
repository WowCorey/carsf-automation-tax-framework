# Investment and Incidence Guardrails

Status: V1.5 prototype review layer.

## Purpose

The investment and incidence guardrails test whether illustrative CARSF outputs appear too punitive, too weak, likely to be passed through, or insufficiently focused on automation rent rather than ordinary productive investment.

The guardrails are non-operative. They do not change final liability.

## What Exists

- Effective automation burden preview.
- Liability-to-revenue and liability-to-AAVA rates.
- Normal-return preservation proxy.
- Consumer, worker, supplier, and capital incidence allocation preview.
- Under-capture / over-capture burden-balance check.
- Placeholder sensitivity sweeps for pass-through rates, cap rates, and AAVA values.
- Stress examples under `examples/investment_guardrails/`.

## Run

```powershell
python scripts/run_investment_guardrails.py
```

Generated reports:

- `reports/investment_guardrails.md`
- `reports/investment_guardrails.json`

## Non-Claims

These are prototype investment and tax-incidence guardrails only. They are not economic validation, investment advice, Treasury modelling, ATO guidance, legal advice, market forecasting, or tax advice.

All elasticity, pass-through, normal-return, and burden thresholds are illustrative placeholders. Future calibration requires Treasury/economic/tax-incidence modelling, legal/tax review, and real data governance.
