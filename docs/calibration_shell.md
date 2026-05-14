# Calibration Shell

Status: V1.5 prototype calibration scaffolding.

## Purpose

The calibration shell identifies the datasets and review pathways needed before CARSF parameters could be calibrated. It does not contain real calibration values.

## Required Data Categories

Future calibration would require source categories including:

- ABS labour force and industry data
- ATO aggregated tax data
- PBO fiscal projections
- DSS / Services Australia payment data
- Fair Work / wage award data
- HILDA longitudinal labour data
- superannuation guarantee data
- HELP/HECS repayment data
- state payroll tax datasets
- industry productivity datasets
- business survey data
- Treasury modelling
- independent legal/tax review

## Placeholder-Only Fields

The calibration registry marks OPFTE_LIBC, FRV, QLC weights, AII weights, AAVA deductibility, caps, credit caps, uplift and rent-tax rates, safe-harbour thresholds, avoidance thresholds, transfer-pricing review shares, mixed-unit weighting, labour-market impacts, GST effects, superannuation and HELP/HECS effects, state payroll tax effects, regional weighting, public-sector automation, and investment deterrence as unresolved placeholder areas.

## Relationship to Mock Evidence

Synthetic mock evidence can test workflow states and confidence handling, but it cannot calibrate model values. A mock packet may demonstrate that a prototype requirement can be marked `partial` or `sufficient_for_prototype`; it does not provide a real OPFTE, FRV, cap rate, transfer-pricing share, or schedule setting.

## Investment and Incidence Calibration

The investment and incidence guardrails require future calibration before any policy claim:

- pass-through elasticities by sector and market structure
- worker wage or underemployment pressure estimates
- supplier pressure and capital absorption assumptions
- normal-return proxies by capital intensity and sector risk
- public-revenue coverage sensitivity and national automation fiscal damage
- over-capture and under-capture tolerances

No such calibration has occurred in this repository.

## Fiscal Trajectory Calibration

The national fiscal trajectory engine also requires future calibration before any policy claim:

- labour displacement and reabsorption rates by sector and region
- PAYG tax loss per displaced worker
- superannuation contribution loss
- HELP/HECS repayment loss
- support-payment and retraining pressure
- administrative cost assumptions
- GST consumption effects
- company tax changes
- state payroll-tax pressure
- automation revenue captured
- public-revenue coverage thresholds

Required source categories include Treasury modelling, ATO aggregated tax data, ABS labour force and industry data, DSS / Services Australia payment data, PBO costing methods, state payroll-tax datasets, superannuation data, HELP/HECS repayment data, and labour-market transition datasets.

No such calibration has occurred in this repository, and fiscal trajectory outputs are not forecasts.

## Transition Funding Calibration

The transition funding module requires future calibration before any policy claim:

- eligible population definitions
- displaced-worker supplement rates
- UBI-lite or automation-dividend payment levels
- participation rates and take-up assumptions
- retraining grant costs
- administrative delivery costs
- duration and phase-out settings
- interaction with existing welfare, tax, and labour-market programs
- automation revenue coverage assumptions
- cliff-risk thresholds

Required source categories include DSS / Services Australia program data, Treasury costing methods, PBO costing methods, ABS population and labour data, ATO aggregated tax data, labour-market transition datasets, and legal/privacy review.

No such calibration has occurred in this repository, and transition-funding outputs are not UBI policy or welfare advice.

## Payment Interaction Calibration

Payment interaction and targeting mechanics require future calibration and legal review before any policy claim:

- existing transfer baseline definitions
- displaced-worker and retraining eligibility rules
- income and household test thresholds
- overlap rules between universal and targeted payments
- phase-in, taper, and phase-out mechanics
- person-level double-counting prevention rules
- support-payment consumption flow and GST recovery assumptions
- hardship-offset assumptions
- inclusion, exclusion, leakage, and cliff-risk thresholds

Required source categories include DSS / Services Australia program data, Treasury costing methods, PBO costing methods, ABS household and labour data, ATO aggregated tax data, privacy/legal review, and welfare-administration design review.

No such calibration has occurred in this repository, and payment-interaction outputs are not eligibility law, welfare advice, Centrelink/DSS/Services Australia modelling, or validated fiscal savings.

## Synthetic Household Distributional Calibration

Synthetic household distributional scenarios require future calibration and privacy/legal review before any policy claim:

- household composition and income-band distributions
- housing, essential cost, debt-pressure, and savings-buffer distributions
- existing transfer baseline interactions by household type
- re-employment timing and income recovery by sector, age, region, skill profile, and retraining access
- payment cliff, inclusion, exclusion, leakage, and support adequacy thresholds
- regional labour-market depth, retraining access, transport access, and housing-cost pressure
- household shock-band thresholds and residual hardship measures

Required source categories include ABS household and labour data, HILDA longitudinal data, Census and regional datasets, DSS / Services Australia program data, ATO aggregated income/tax data, labour-market transition datasets, privacy/legal review, Treasury modelling, PBO costing methods, and welfare-administration design review.

No such calibration has occurred in this repository, and distributional scenario outputs are not real household modelling, welfare advice, eligibility law, DSS / Services Australia modelling, ABS analysis, Treasury modelling, PBO costing, legal advice, tax advice, or economic validation.

## Household Weighting Calibration

Synthetic household weighting and subgroup aggregation require future calibration and privacy/legal review before any representativeness claim:

- household composition distributions
- income-band distributions
- displacement incidence by household type, sector, and region
- regional labour-market depth and transition capacity
- housing, essential cost, savings, and debt-buffer distributions
- existing transfer baseline interactions
- re-employment timing and income recovery distributions
- payment eligibility, inclusion, exclusion, leakage, and cliff-risk parameters
- survey weights or population weights
- uncertainty and confidence interval methods

Required source categories include ABS, HILDA, Census, DSS / Services Australia, ATO aggregated income/tax data, regional labour-market data, household survey data, Treasury modelling, PBO costing methods, privacy/legal review, and welfare-administration review.

No such calibration has occurred in this repository, real household data is not allowed in the repo, and household weighting outputs are not population estimates or real distributional modelling.

## Non-Claims

The calibration shell is not legal, tax, Treasury, ATO, ABS, Fair Work, OECD, BEPS, audit, forensic, or economic validation. It does not prove any model setting is correct.
