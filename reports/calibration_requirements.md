# CARSF V1.5 Calibration Requirements Report

Generated at: `2026-05-13T10:04:04+00:00`

## A. Purpose

This report defines the calibration shell for future CARSF modelling. It does not include real calibration values.

## B. Calibration Registry

- Version: CARSF V1.5 calibration shell
- Requirement count: 20
- No fake calibration values detected: true

## C. Required Datasets

| Component | Required Dataset | Preferred Source | Fallback Source | Status |
| --- | --- | --- | --- | --- |
| OPFTE_LIBC benchmarks | OPFTE_LIBC benchmarks calibration dataset placeholder | ABS labour force / industry data | industry productivity datasets | not_collected |
| FRV floor/standard/full | FRV floor/standard/full calibration dataset placeholder | ATO aggregated tax data | PBO fiscal projections | not_collected |
| QLC weights and QLCMaxMultiplier | QLC weights and QLCMaxMultiplier calibration dataset placeholder | Fair Work / wage award data | HILDA longitudinal labour data | not_collected |
| AII component weights | AII component weights calibration dataset placeholder | business survey data | industry productivity datasets | not_collected |
| AAVA deductibility categories | AAVA deductibility categories calibration dataset placeholder | independent legal/tax review | Treasury modelling | not_collected |
| cap rates lambda_sector / LAMBDA_sector | cap rates lambda_sector / LAMBDA_sector calibration dataset placeholder | Treasury modelling | business survey data | not_collected |
| theta credit cap | theta credit cap calibration dataset placeholder | Treasury modelling | business survey data | not_collected |
| uplift rate and rent tax rate | uplift rate and rent tax rate calibration dataset placeholder | ATO aggregated tax data | PBO fiscal projections | not_collected |
| safe-harbour thresholds | safe-harbour thresholds calibration dataset placeholder | Treasury modelling | business survey data | not_collected |
| avoidance risk thresholds | avoidance risk thresholds calibration dataset placeholder | Treasury modelling | business survey data | not_collected |
| transfer-pricing review shares | transfer-pricing review shares calibration dataset placeholder | independent legal/tax review | Treasury modelling | not_collected |
| mixed-unit exposure weighting | mixed-unit exposure weighting calibration dataset placeholder | business survey data | industry productivity datasets | not_collected |
| labour-market absorption rates | labour-market absorption rates calibration dataset placeholder | DSS / Services Australia payment data | HILDA longitudinal labour data | not_collected |
| wage compression / underemployment modules | wage compression / underemployment modules calibration dataset placeholder | Fair Work / wage award data | HILDA longitudinal labour data | not_collected |
| GST consumption effects | GST consumption effects calibration dataset placeholder | Treasury modelling | business survey data | not_collected |
| superannuation and HELP/HECS effects | superannuation and HELP/HECS effects calibration dataset placeholder | ATO aggregated tax data | PBO fiscal projections | not_collected |
| state payroll tax effects | state payroll tax effects calibration dataset placeholder | ATO aggregated tax data | PBO fiscal projections | not_collected |
| regional weighting | regional weighting calibration dataset placeholder | Treasury modelling | business survey data | not_collected |
| public-sector automation | public-sector automation calibration dataset placeholder | Treasury modelling | business survey data | not_collected |
| investment deterrence / tax incidence parameters | investment deterrence / tax incidence parameters calibration dataset placeholder | ATO aggregated tax data | PBO fiscal projections | not_collected |

## D. Placeholder-Only Fields

- OPFTE_LIBC benchmarks
- FRV floor/standard/full
- QLC weights and QLCMaxMultiplier
- AII component weights
- AAVA deductibility categories
- cap rates lambda_sector / LAMBDA_sector
- theta credit cap
- uplift rate and rent tax rate
- safe-harbour thresholds
- avoidance risk thresholds
- transfer-pricing review shares
- mixed-unit exposure weighting
- labour-market absorption rates
- wage compression / underemployment modules
- GST consumption effects
- superannuation and HELP/HECS effects
- state payroll tax effects
- regional weighting
- public-sector automation
- investment deterrence / tax incidence parameters

## E. Unresolved Dependencies

- Treasury/ATO-style data access and modelling governance
- Privacy and secrecy review for restricted datasets
- Independent legal/tax review
- Sector-specific calibration methodology
- Economic incidence and behavioural response modelling

## F. Components That Cannot Be Validated Yet

All listed calibration components remain `not_collected` and cannot be validated until authorised source data, privacy review, legal/tax review, and policy methodology are supplied.

## G. Non-Claims

- This calibration registry is a prototype shell only.
- No real calibration values, official data, legal validation, tax validation, Treasury validation, ATO validation, ABS validation, Fair Work validation, or economic validation are included.
- All calibration statuses remain not_collected or placeholder until authorised data and review are supplied.
