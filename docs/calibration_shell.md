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

## Uncertainty Range Calibration

The uncertainty range mechanics require future calibration and methods review before any uncertainty claim:

- household residual gap ranges
- transition support ranges
- re-employment timing ranges
- regional stress ranges
- payment cliff ranges
- weighted subgroup residual gap ranges
- weighted high/critical shock-share ranges
- stability thresholds
- fragile-output thresholds
- confidence or uncertainty methods

Required source categories include ABS, HILDA, Census, DSS / Services Australia, ATO aggregated income/tax data, regional labour-market data, household survey data, Treasury modelling, PBO costing methods, privacy/legal review, and statistical methods review.

No such calibration has occurred in this repository. Low/base/high values are deterministic placeholders, not Monte Carlo, confidence intervals, forecasts, or real uncertainty quantification.

## Reviewed Scenario Calibration and Methods Review

The reviewed scenario comparison layer requires future calibration and methods review before any scenario can be treated as a real policy signal:

- which household uncertainty ranges are required for interpretation
- stability thresholds for discussion, warning, and suppression categories
- rules for hiding fragile or range-sensitive point estimates
- treatment of missing uncertainty ranges
- representativeness review for any future subgroup or household weights
- external review criteria for sector-specific distributional outputs

Required source categories include ABS, HILDA, Census, DSS / Services Australia, ATO aggregated income/tax data, regional labour-market data, household survey data, Treasury modelling, PBO costing methods, privacy/legal review, and statistical methods review.

No such calibration has occurred in this repository. Reviewed scenario outputs are prototype display-control signals only; they are not statistical validation, population estimates, real household modelling, forecasts, confidence intervals, welfare advice, eligibility law, legal advice, tax advice, or economic validation.

The pre-Build 21 hardening pass preserves available subgroup metadata through weighted uncertainty and reviewed-scenario payloads. That metadata remains synthetic and non-representative, and missing metadata still requires prototype warnings rather than inference.

## Expanded Sector Schedule Calibration

The expanded prototype sector schedules require future calibration before any operative schedule or sector comparison could be claimed:

- call centre and customer support output per qualified FTE
- accounting, payroll, document-processing, and administration output units
- retail self-checkout, fulfilment, inventory, and robotic picking measures
- software and digital platform Australian-served transaction or workflow measures
- sector-specific QLC weighting and worker-quality evidence
- sector-specific AII component weights
- OPFTE, FRV, cap, uplift, and rent-tax-rate values
- safe-harbour thresholds and worker-assist treatment
- avoidance and classification-arbitrage rules
- software and digital platform capital-base treatment under AASB 138, tax counsel, and Treasury review

Required source categories include ABS labour and output data, ATO aggregated tax data, DSS / Services Australia transition data, PBO costing methods, Fair Work wage and classification data, industry automation surveys, platform/transaction benchmark data, accounting and support workflow benchmarks, Treasury modelling, ATO review, legal review, and specialist software/intangible-asset accounting review.

No such calibration has occurred in this repository. Expanded sector schedules are prototype placeholders only. They are not calibrated, not legal schedules, not Treasury schedules, not ATO guidance, not ABS/ATO/DSS/PBO analysis, do not contain real industry data, and must not be used to estimate actual tax payable.

## Sector Stress Matrix Calibration and Review

The sector stress matrix requires future calibration and methods review before any stress-band output could be treated as more than a metadata-only display control:

- validated sector automation-exposure measures
- validated QLC erosion and worker-quality measures
- AAVA sensitivity and rent-attribution evidence
- incidence and pass-through evidence
- investment-deterrence and normal-return review
- avoidance / gaming evidence and legal attribution review
- calibration difficulty scoring methods
- treatment of software, intangibles, platform attribution, and AASB 138 issues
- real multi-schedule attribution and apportionment review

Required source categories include ABS labour and output data, ATO aggregated tax data, industry automation surveys, platform/transaction benchmark data, Treasury modelling, PBO costing methods, legal review, tax counsel, accounting review, and external methods review.

No such calibration has occurred in this repository. The sector stress matrix is prototype metadata review only, does not use real industry data, does not rank sectors, does not estimate actual tax payable, and does not modify firm-level CARSF liability logic.

Automation-intensity outputs now show digital, physical, decision, and compute metadata components separately. These components are explanation aids only and are not calibrated sector scores.

## Behavioural Response Calibration and Review

The behavioural response / gaming simulation requires future calibration, legal review, ATO/Treasury methods review, and behavioural research before any response pathway could be used beyond prototype policy discussion:

- behavioural response taxonomy and trigger definitions
- response pressure band thresholds
- evidence requirements for labour relabelling, token oversight, QLC inflation, entity splitting, offshore service routing, related-party fees, cloud/inference relabelling, robotics leasing, customer self-service shifts, schedule arbitrage, artificial low AAVA, platform IP royalty routing, open-source AI treatment, and mixed-unit apportionment gaming
- mapping between response pathways and operative anti-avoidance provisions
- grouped-entity, transfer-pricing, offshore-attribution, AAVA deductibility, capital-base, customer-self-service, and schedule-authority review processes
- external behavioural research and administrative feasibility review

Required source categories include legal review, tax counsel, ATO administrative methods review, Treasury policy review, behavioural research, industry automation surveys, transfer-pricing methods review, grouped-entity review methods, software/intangible accounting review, and secure evidence-governance design.

No such calibration has occurred in this repository. Behavioural response outputs are deterministic synthetic pathway reviews only; they do not predict taxpayer behaviour, estimate behavioural elasticity, create compliance-risk scoring, implement enforcement, implement penalties, estimate actual tax payable, or modify firm-level CARSF liability logic.

Placeholder response-band tuning only improves demonstration spread across moderate, high, critical, and suppressed categories. It does not make any response pathway a behavioural probability or observed conduct signal.

## Administrative Workflow Calibration and Review

The administrative compliance workflow shell requires external legal, tax, ATO-methods, Treasury-methods, privacy, calibration, and administrative-design review before any real use:

- review queue taxonomy and stage definitions;
- evidence request bundle mapping to operative source rules;
- behavioural response links and escalation pathways;
- grouped-entity, transfer-pricing, sector schedule, AAVA deductibility, capital-base, offshore-attribution, and privacy/secrecy routing;
- locked and suppressed status rules;
- methods governance for external calibration review;
- administrative safeguards, taxpayer protections, review rights, and documentation controls;
- secure evidence handling outside this repository.

Required source categories include legal review, tax counsel, privacy and secrecy review, ATO administrative methods review, Treasury policy review, secure evidence-governance design, procedural fairness review, operational feasibility review, and external calibration review.

No such calibration has occurred in this repository. Administrative workflow outputs are deterministic synthetic pathway-organisation reviews only; they are not a workflow endorsed by the ATO, not guidance from the ATO, not audit logic, not enforcement, not compliance scoring, do not create notices or penalties, do not estimate actual tax payable, and do not modify firm-level CARSF liability logic.

Routine and enhanced workflow scenarios are included for demonstration coverage only. They do not create administrative readiness, approval, sufficiency, clearance, or operational status.

## Non-Claims

The calibration shell is not legal, tax, Treasury, ATO, ABS, Fair Work, OECD, BEPS, audit, forensic, or economic validation. It does not prove any model setting is correct.
