# Sector Schedule Expansion

This build expands the CARSF V1.5 prototype sector schedule library beyond automotive repair and logistics / warehousing.

New prototype schedules:

- `call_centres_customer_support`
- `accounting_administration`
- `retail_self_checkout_fulfilment`
- `software_digital_platforms`

Each schedule includes a placeholder canonical output unit, measurement scope, QLC weights, AII weights, OPFTE placeholder, FRV placeholders, cap placeholders, safe-harbour notes, measurement controls, avoidance controls, assumptions, and data required for future calibration.

## Non-Claims

Sector schedules are prototype placeholders only. They are not calibrated. They are not legal schedules. They are not Treasury schedules. They are not ATO guidance. They are not ABS/ATO/DSS/PBO analysis. They do not contain real industry data. They must not be used to estimate actual tax payable.

The schedules do not modify firm-level CARSF liability logic, do not implement real multi-schedule attribution, and do not validate OPFTE, FRV, caps, or safe-harbour thresholds.

## Software / Digital Platforms

The software / digital platforms schedule includes a specific warning that capital-base treatment for software firms remains unresolved and subject to AASB 138, tax counsel, and Treasury review.

## Run Command

```powershell
python scripts/run_sector_schedule_expansion.py
```

Generated reports:

- `reports/sector_schedule_expansion.md`
- `reports/sector_schedule_expansion.json`

## Future Work

Build 18 should add a sector stress matrix comparing prototype sectors across automation intensity, QLC vulnerability, AAVA sensitivity, incidence risk, investment risk, avoidance risk, calibration difficulty, and display-control status without claiming real sector rankings.
