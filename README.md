# CARSF Automation Tax Framework

Private research/prototype repository for the Commonwealth Automation Revenue Stabilisation Framework (CARSF).

CARSF is a proposed Australian government-facing policy framework for measuring and responding to automation-driven labour-tax-base risk. Its core principle is:

> If productive capacity migrates from labour to capital, the fiscal base must follow it.

This repository does not contain law, tax advice, Treasury advice, ATO guidance, or calibrated Australian liability settings. It separates the policy paper track from a small Python modelling track so the framework can be tested, criticised, revised, and eventually exported into formal policy materials.

## Status

Current status: private research/prototype.

All sector values, schedule values, examples, caps, Fiscal Replacement Value values, AAVA settings, and behavioural assumptions are placeholders unless explicitly labelled as confirmed baseline figures from official sources.

## Repository Structure

- `paper/` - Markdown policy paper, V1.5 working draft, formulas, glossary, references, and export notes.
- `audits/` - review notes, responses, and red-team register.
- `model/carsf/` - minimal Python concept model for QLC, LIBC/HLE, AII, AAVA, levies, caps, coverage, safe-harbour classification, anti-avoidance heuristics, and grouping review flags.
- `model/tests/` - pytest coverage for formula bounds, caps, examples, and avoidance flags.
- `schedules/` - prototype sector schedules for automotive repair and logistics / warehousing.
- `examples/` - illustrative placeholder firm cases.
- `simulator/` - Streamlit interface for policy review, tax model inputs, worked examples, red-team tests, and audit log.
- `docs/` - data requirements, limitations, implementation notes, known risks, and V1.5 plan.

## Run Tests

```powershell
python -m pip install -r requirements.txt
python -m pytest
```

## Run Worked Examples

```powershell
python scripts/run_examples.py
```

Generated reports:

- `reports/example_results.md`
- `reports/example_results.json`

The reports are illustrative placeholder outputs only. They are not legal, tax, Treasury, ATO, economic, or real liability calculations.

## Run the Simulator

```powershell
python -m streamlit run simulator/app.py
```

The simulator is a prototype interface only. It must not be used to estimate actual tax payable.

## What V1.5 Is Trying To Prove

V1.5 is not just an examples update. It is V1.4 plus two prototype sector schedules and a measurement appendix. The working target is to test whether CARSF can:

- prevent QLC inflation through a per-worker cap;
- measure AAVA without treating unverified deductions as settled policy;
- report CoverageRatio alongside CARS-I;
- distinguish worker-assist AI from labour-substituting automation;
- handle automotive repair and logistics / warehousing as prototype schedules;
- classify prototype safe-harbour, anti-avoidance, and grouped-entity review signals without changing liability;
- identify open-source AI and R&D Tax Incentive interaction questions without overclaiming.

## Not Yet Solved

The model still needs real Treasury, ATO, ABS, DSS, HILDA, HELP, superannuation, state payroll tax, industry, and legal data. It also needs calibrated safe-harbour thresholds, apportionment, grouped-entity aggregation, related-party adjustments, behavioural elasticity estimates, tax incidence modelling, anti-avoidance drafting, privacy review, and independent tax counsel review before any external policy use.

Safe-harbour outputs are prototype classification only. They do not reduce, cap, or erase calculated liability in this build.
