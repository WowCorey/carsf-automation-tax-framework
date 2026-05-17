# Administrative Compliance Workflow

The administrative compliance workflow is a prototype shell for organising synthetic CARSF cases into review pathways. It connects evidence request bundles, review queues, behavioural-response links, sector schedule review, grouped-entity review, transfer-pricing review, privacy/secrecy review, legal-policy review, methods review, and external calibration review.

Run:

```powershell
python scripts/run_administrative_compliance_workflow.py
```

Generated reports:

- `reports/administrative_compliance_workflow.md`
- `reports/administrative_compliance_workflow.json`

## Scope

The workflow layer:

- loads synthetic administrative workflow scenarios;
- validates referenced sector schedules;
- validates referenced behavioural response scenarios;
- validates referenced synthetic mock evidence packet IDs;
- maps requested review domains to existing prototype evidence requirement IDs;
- assigns deterministic workflow decision bands and workflow statuses;
- assigns review queues and escalation pathways;
- records locked or suppressed cases;
- includes routine and enhanced synthetic demonstration rows so the workflow spread is visible;
- preserves no-enforcement and no-liability-modification flags.

## Non-Claims

This is a prototype administrative workflow only. It is not a workflow endorsed by the ATO, not guidance from the ATO, not Treasury modelling, not legal advice, not tax advice, not compliance scoring, not audit logic, and not enforcement. It does not create notices, implement penalties, use statutory information-gathering powers, determine non-compliance, estimate actual tax payable, predict taxpayer behaviour, estimate behavioural elasticity, use taxpayer-level data, firm-level data, industry data, ABS data, ATO data, DSS data, Treasury data, PBO data, HILDA data, or Census data, or modify firm-level CARSF liability.

All workflow steps require external legal, tax, ATO-methods, Treasury-methods, privacy, calibration, and administrative-design review before any real use.

## Workflow Outputs

The report includes:

- scenario coverage;
- administrative workflow matrix;
- evidence request bundle summaries;
- review queue assignments;
- escalation pathway summaries;
- behavioural response links;
- privacy and secrecy review notes;
- locked and suppressed cases;
- calibration and administrative-design blockers.

The output is a display and governance shell only. It should not be used as an operational process, compliance workflow, or liability input.

Routine and enhanced rows are demonstration rows only. They do not imply administrative approval, evidence sufficiency, clearance, operational readiness, or any real action.
