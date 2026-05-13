<!-- Converted from CARSF_V1_4_Treasury_Exposure_Draft.pdf on 2026-05-13. -->
<!-- PDF layout artefacts, page headers, and footers were removed. Substantive source notes and disclaimers were retained. -->

# Commonwealth Automation Revenue Stabilisation Framework

**CARSF V1.5 Working Draft - Pre-Consultation Concept Paper**

A distributional stabilisation framework for automation-driven

labour-tax-base risk in Australia

### Status of this document

This is a policy concept paper. It is not draft legislation, legal advice, tax advice, or an official

Commonwealth position. Its purpose is to test whether a future automation-related fiscal framework could

be made mathematically coherent, administratively measurable, legally plausible, and politically

explainable to Treasury, ATO, PBO, Department of Finance, Fair Work, and Parliamentary advisers.

### Version and date

CARSF V1.5 Working Draft - Pre-Consultation Concept Paper. Working copy seeded from V1.4 prepared 12 May 2026. Supersedes V1.3 (12

May 2026), V1.2, V1.1, V1.0.

### Intended readers

Treasury, Australian Taxation Office, Parliamentary Budget Office, Department of Finance, Productivity

Commission, Fair Work Commission, Australian Bureau of Statistics, Department of Industry Science and

Resources, Department of Social Services, state and territory Treasuries, and senior Ministerial advisers.

If productive capacity migrates from labour to capital, the fiscal base must follow it - or the

revenue assumptions supporting Australia's medium-term budget become structurally

fragile.

Concept paper - for policy development and modelling review only

## Changes from V1.3

V1.4 retains the architecture of V1.3 but resolves five structural problems identified in the V1.3 audit. The

framework is now suitable for Treasury exposure review subject to the limitations listed at section 18.

Priority Change Section

Critical Restored explicit Australian Automated Value Added (AAVA) formula that V1.3 section4, section5

silently dropped.

Critical Every Automation Intensity Index (AII) component now formally defined, anchored section4, section5, Appendix C

to AASB and ABS measurement conventions. Removed the circular

LabourIntensityShift term.

Critical Labour-Intensity Benchmark Cohort (LIBC) endogeneity guardrail now specified as section5

an asymmetric ratchet plus a productivity-indexed floor.

Critical Explicit prospective-only commencement clause. No retrospective liability for section6, section16

pre-commencement automation.

Critical Combined AEL + ARL cap relative to AAVA introduced to prevent double-hitting section5

capital-rent and labour-gap liability on the same value base.

Important QLC weights restructured to additive form with floors to prevent zero-collapse. section4

Important Output measure now bound to a single canonical unit per sector schedule. section8

Important Discount rate for LifetimeFiscalDamage tied to long-term Treasury bond yield, section7

Intergenerational-Report-consistent.

Important CARS-I (Commonwealth Automation Revenue Stress Index) formally restored. section14

Important Worker-assist concession now requires objective QLC-percentile test. section9

Important Software firms: imputed CapitalBase methodology (cumulative R&D plus compute section12

spend, amortised) to address AASB 138 intangibles problem.

Important Explicit Pillar Two interaction subsection: CARSF assessed before, not after, Pillar section10

Two top-up; declared as covered tax where appropriate.

Important "Why not just raise company tax?" comparator subsection. section3

Refinement $45,255 national floor moved to appendix only; main text uses sector-conditional section2, Appendix A

vectors.

Refinement Government-AI procurement distortion acknowledged. section15

Refinement Dispute resolution pathway specified (internal review, AAT, Federal Court). section14

Refinement Disclosure overlap with AI Safety Standard mapped. section14

Refinement Deadweight-loss and behavioural-elasticity caveat added. section11

Refinement Acquisition on just terms (s 51(xxxi)) and trade-retaliation risks expanded. section10

## Executive summary

> Working status: V1.5 is a working copy of V1.4 for policy and modelling development. It is not legislation, tax advice, legal advice, or an official Commonwealth position.
>
> TODO(V1.5): Add QLC per-worker cap.
> TODO(V1.5): Add AAVA deductibility appendix.
> TODO(V1.5): Add CoverageRatio alongside CARS-I.
> TODO(V1.5): Rename PRRT-style wording to PRRT-inspired uplift logic throughout.
> TODO(V1.5): Clean up LIBC / labour-intensity terminology.
> TODO(V1.5): Retitle the paper as a Pre-Consultation Concept Paper, not a Treasury Exposure Draft.
> TODO(V1.5): Build Prototype Schedule A - Automotive Repair.
> TODO(V1.5): Build Prototype Schedule B - Logistics / Warehousing.
> TODO(V1.5): Add open-source AI treatment.
> TODO(V1.5): Add R&D Tax Incentive interaction policy position.
>
> V1.5 scope note: V1.5 is V1.4 plus two prototype sector schedules and a measurement appendix. It is not only an examples update.


Australia's medium-term fiscal outlook is heavily dependent on personal income tax. The Parliamentary

Budget Office's 2025-26 Medium-Term Budget Outlook projects personal income tax to rise from 47.7% of

total Commonwealth revenue in 2025-26 to 53.0% by 2035-36. Over the same period, AI, robotics, and

autonomous systems may reduce, compress, or restructure the human labour contribution that the tax

base assumes.

CARSF is a framework for measuring and responding to that risk before a labour-market shock occurs. It

does not tax AI adoption. Liability attaches only where a firm's labour-to-output ratio materially diverges

from a contemporary sector labour-intensity benchmark, and where that divergence creates measurable

Commonwealth fiscal exposure.

V1.4 is framed as distributional stabilisation, not as revenue replacement. Automation may genuinely lower

prices, improve services, raise real wages, and increase consumer surplus. Those gains are not the policy

concern. The concern is that the economic gains from automated productive capacity may concentrate in

capital while Australia's fiscal architecture remains built around labour income, consumption from wages,

superannuation contributions, and HELP repayments.

The framework is staged. Disclosure and shadow assessment precede activation. Liability is prospective

only. Safe harbours apply to small business and startups. A capacity-to-pay cap and a combined liability

cap prevent confiscatory outcomes. The Automation Rent Levy follows PRRT-inspired uplift logic uplift logic, taxing only

above-normal automated returns.

V1.4 does not promise universal basic income. It creates a National Productivity Transition Fund with

staged uses and an explicit affordability gate. UBI is a possible Stage 4 outcome, not a Stage 1 promise.

## Headline architecture

Core issue CARSF V1.4 response

Tax base risk Measures labour-tax-base exposure when output shifts from workers to automated

productive capacity.

Productivity concern Does not tax AI use. Liability depends on benchmark divergence, automation

intensity, and fiscal exposure.

Measurement concern Uses contemporary sector Labour-Intensity Benchmark Cohorts (LIBCs), not historical

productivity baselines.

Avoidance concern Uses destination and activity attribution and Australian Automated Value Added, not

only declared profit.

Equity concern Credits verified Australian qualified labour, training, transition, and apprenticeship

activity.

UBI concern Treats universal payments as a possible Stage 4 outcome subject to an affordability

gate, not an upfront promise.

Retrospectivity concern Liability is prospective only. Pre-commencement automation is subject to disclosure,

not levy.

International tax interaction Designed to operate alongside, not against, OECD Pillar Two. Assessed before Pillar

Two top-up; declared as covered tax where appropriate.

## 1. Why this framework is being considered

The central problem is not that AI may replace some jobs. The central problem is that Australia's public

revenue system assumes a broad base of taxable labour income. If productive capacity migrates from

human labour to AI, robotics, and autonomous capital, then the public revenue base may not automatically

migrate with it.

This creates a distributional-fiscal risk. Productivity gains may accrue to owners of automated capital while

workers experience displacement, reduced hours, wage compression, lower career progression, or

lower-wage re-employment. If left unmanaged, the Commonwealth could face lower income-tax growth

and higher transition and support costs simultaneously.

### 1.1 What the framework is not

- Not a tax on AI adoption. Liability depends on benchmark divergence, automation intensity, and fiscal
exposure, not on use of AI.

- Not anti-productivity. Worker-assist AI, compliance AI, safety AI, accessibility AI, medical AI, and
public-interest AI are concessionally treated.

- Not retrospective. Pre-commencement automation is subject to disclosure only, not levy.
- Not a UBI funding mechanism. Stage 1-3 transition uses are prioritised. UBI is gated on affordability.
- Not a replacement for company tax. CARSF operates alongside the existing company tax
architecture.

## 2. Australian fiscal baseline

The figures below establish scale, not policy parameters. Final modelling requires Treasury, PBO, ABS,

ATO, DSS, HILDA, and superannuation-system data, as well as state and territory revenue data.

Indicator Value Use in CARSF

Personal income tax, 2025-26 $357.8b Anchor for national fiscal exposure scale; not

used in firm-level liability.

Personal income tax share of total 47.7% Demonstrates current dependence on labour

revenue, 2025-26 income tax.

Personal income tax share of total 53.0% Demonstrates projected increase in

revenue, 2035-36 dependence.

Company tax, 2025-26 $143.5b Context for current corporate contribution.

CARSF sits alongside.

GST, 2025-26 $99.3b Relevant to consumption effects and

productivity-dividend analysis.

Employment, March 2026 14,767,700 Used for national illustrative floor only; not for

firm-level FRV.

JobSeeker single, no children, from 20 $808.70 per fortnight Conservative transfer-support floor for national

March 2026 illustration.

Company tax rates, 2025-26 25% base-rate; 30% CARSF sits beside, not in place of, existing

other company tax.

Sources: PBO 2025-26 Medium-Term Budget Outlook; ABS Labour Force Australia March 2026; Services Australia

JobSeeker rates from 20 March 2026; ATO company tax rates 2025-26.

Note. The single-figure national floor of $45,255 (PIT per worker plus annualised JobSeeker single) is

retained in Appendix A for completeness only. It is not used as a firm-level Fiscal Replacement Value in

V1.4. Final assessment uses sector- and occupation-conditional FRV vectors drawn from HILDA, ATO

occupational data, DSS transfer data, and state revenue data.

## 3. Design principles

Principle Meaning

## 1. Tax the labour-tax gap, not AI Use of AI is not sufficient to trigger liability. Liability depends on measurable

use divergence between automated productive output and qualified human labour

contribution.

## 2. Use contemporary benchmarks Human Labour Equivalent is anchored to a current labour-intensity benchmark

cohort with an asymmetric ratchet, not a historical productivity baseline.

## 3. Avoid double-counting Job loss, re-employment loss, wage compression, underemployment, and

career scarring are treated as mutually exclusive worker states or time periods.

## 4. Preserve useful productivity The framework recognises productivity dividends, consumer pass-through, real

price reductions, and quality-of-service gains.

## 5. Capture excess automation rent Where automated systems generate above-normal returns, a separate

PRRT-inspired uplift logic rent levy applies, with a combined cap to prevent stacking.

## 6. Protect small business and Simplified safe harbours exempt small and pre-revenue entities from full

startups assessment.

## 7. Be administrable ATO collects and assesses defined inputs. A specialist Schedules Authority

maintains LIBCs, AII components, and FRV vectors with input from Fair Work,

ABS, and the Productivity Commission.

## 8. Be staged and prospective Disclosure and shadow assessment precede liability. Liability attaches only to

NLTG measured in or after the legislated commencement year.

### 3.1 Why not simply raise company tax?

The simplifying alternative is a higher company tax rate with a broader base. It would be administratively

cheaper and politically clearer. CARSF should be assessed against it honestly.

A higher company tax rate fails on three counts where CARSF is designed to succeed:

- Profit-shifting blind spot. Highly automated digital platforms with low declared Australian profit pay
little company tax even on large Australian revenue. Pillar Two helps but does not solve. CARSF's

destination- and activity-based AAVA captures Australian-facing automated value regardless of where

profit is booked.

- Distributional blind spot. Company tax has no distributional measurement layer. It cannot
distinguish a firm replacing 1,000 workers from a firm maintaining 1,000 workers at the same revenue.

CARSF's NLTG can.

- Signal blind spot. A higher company tax rate gives no information about where labour-tax-base
erosion is concentrating. CARSF's disclosure regime produces a national automation-intensity dataset

usable for monetary, fiscal, and labour-market policy.

CARSF should therefore be presented as complementary to, not in competition with, ordinary company

tax. If the framework cannot be made administrable, the company-tax alternative remains the fallback.

## 4. Core definitions

All definitions in this section are illustrative for a concept paper. Legislated definitions would be settled by

Treasury, Office of Parliamentary Counsel, and tax counsel.

Term Definition

Qualified Labour Contribution Normalised full-time-equivalent Australian labour contribution, weighted additively for wage

(QLC) quality, job security, skill development, and Australian nexus, with each component

bounded below to prevent zero-collapse.

Labour-Intensity Benchmark Sector cohort comprising firms with verified high QLC-per-output ratios, refreshed on a

Cohort (LIBC) rolling three-year basis, subject to an asymmetric ratchet (the cohort labour intensity may

decrease but cannot increase by more than a defined annual percentage) and a

productivity-indexed floor.

Output per FTE benchmark Canonical sector output divided by LIBC QLC. Each sector schedule binds one canonical

(OPFTE) Output unit (transactions, deliveries, units produced, claims processed, etc.) so that

cross-firm comparison is meaningful.

Human Labour Equivalent The qualified human labour that would be expected to produce firm i's output under the

(HLE) LIBC benchmark.

Automation Intensity Index Sector-normalised composite of four observable inputs: compute spend ratio, automated

(AII) decision ratio, robotics capital ratio, and automated process-share ratio. Weights are set by

sector schedule. Bounded between 0 and 1.

Net Labour Tax Gap (NLTG) The non-negative gap between automation-adjusted HLE and QLC.

Fiscal Replacement Value Sector- and occupation-conditional value of public fiscal exposure per net labour-tax-gap

(FRV) unit, in floor, standard, or full layers.

Australian Automated Value Australian-attributable revenue less verified non-automation input costs less verified QLC

Added (AAVA) wage cost. Australian attribution uses destination and activity tests aligned with GST

jurisprudence.

Automation Equilibrium Levy Stabilisation liability attached to measured NLTG.

(AEL)

Automation Rent Levy (ARL) Separate PRRT-inspired uplift logic levy on above-normal automated returns, using an uplift rate above a

defined capital base.

CARS-I Commonwealth Automation Revenue Stress Index: national-level ratio of measured

automation fiscal damage to automation revenue captured.

## 5. Mathematical model

The model produces a firm-level liability from observable inputs. Each equation below is followed by a

plain-English explanation. Notation: i = firm; j = sector schedule; t = assessment period; w = worker.

### 5.1 Qualified Labour Contribution

> TODO(V1.5): Add a schedule-defined per-worker QLC cap and explain why it prevents one token worker from being inflated without bound.


QLC_i = sum over w of [(Hours_w / FullTimeHours_w) * (1 + alpha*WQ_w + beta*JS_w +

gamma*SD_w + delta*AN_w)]

Plain English. For each worker w, take their hours as a share of full-time, then multiply by an additive

weighting that rewards wage quality, job security, skill development, and Australian nexus. Sum across all

workers in the firm. The additive form replaces the multiplicative form in V1.3, which collapsed to zero

whenever any single weight was zero. Each weight is bounded by the sector schedule.

### 5.2 Output-per-FTE benchmark from the LIBC

OPFTE_LIBC,j,t = CanonicalOutput_LIBC,j,t / QLC_LIBC,j,t

subject to:

OPFTE_LIBC,j,t <= OPFTE_LIBC,j,t-1 * (1 + ratchet_j)

OPFTE_LIBC,j,t >= OPFTE_floor,j [productivity-indexed]

Plain English. The benchmark output per qualified FTE in sector j at time t is the canonical output divided

by qualified labour in the benchmark cohort. The asymmetric ratchet caps how fast the benchmark can rise

year-on-year (preventing automation-driven collapse) and the floor pins it to a productivity-indexed

minimum drawn from Productivity Commission MFP data. This is the V1.4 fix to the V1.3 endogeneity

weakness.

### 5.3 Human Labour Equivalent

HLE_i = Output_i / OPFTE_LIBC,j,t

Plain English. If firm i produces a given quantity of canonical sector output, the HLE is the qualified

human labour that the benchmark cohort would normally need to produce that output. Output_i is

measured in the same canonical unit defined by the sector schedule, so HLE is in QLC-equivalent units.

### 5.4 Automation Intensity Index

AII_i = w1*ComputeRatio_i + w2*AutoDecisionRatio_i

+ w3*RoboticsCapitalRatio_i + w4*AutoProcessShare_i

AII_i in [0, 1]; sum of weights = 1

Plain English. AII combines four observable measures of automation. Each is defined formally in

Appendix C with anchored denominators. The circular "LabourIntensityShift" term from V1.3 has been

removed. Weights are set by the sector schedule and tested in shadow assessment.

Note. AII is bounded in [0, 1] so it acts as a fraction of HLE attributable to automation. A firm with AII = 0.3 is

treated as if 30% of its HLE output is automation-driven. This replaces the V1.2 undefined "automation

attribution" scalar.

### 5.5 Net Labour Tax Gap

NLTG_i = max(0, [HLE_i * AII_i] - QLC_i)

Plain English. The labour-tax gap is the automation-attributable share of expected human labour, less the

firm's actual qualified labour contribution. A firm matching benchmark labour intensity has NLTG near zero.

A highly automated firm with thin qualified labour has a large NLTG. Negative gaps are not used (NLTG

cannot be negative).

### 5.6 Australian Automated Value Added

> TODO(V1.5): Add a deductibility appendix separating confirmed deductions, illustrative assumptions, placeholder values, and open research requirements.


AAVA_i = AustralianAttributableRevenue_i

- VerifiedNonAutomationInputCosts_i
- VerifiedQLC_WageCost_i
Plain English. AAVA measures the Australian economic value added by automated productive capacity.

Australian attribution uses destination and activity tests rather than relying on declared profit.

Non-automation input costs and qualified human wage costs are deducted. AAVA is the base for the

capacity-to-pay cap and the rent levy.

### 5.7 Automation Equilibrium Levy

AEL_raw,i = NLTG_i * FRV_standard,j,t

AEL_payable,i = min(AEL_raw,i, lambda_j * AAVA_i)

Shortfall_i = AEL_raw,i - AEL_payable,i [recorded, not collected]

Plain English. The raw liability is the gap multiplied by the fiscal replacement value. The payable liability is

capped at a sector-specific share of AAVA. Any amount above the cap is recorded as an Automation

Fiscal Shortfall for national risk monitoring (CARS-I), not collected from the firm.

### 5.8 Automation Rent Levy

ARL_i = max(0, AAVA_i - UpliftRate_j * CapitalBase_i)

* RentTaxRate_j

Plain English. Following PRRT logic, the firm is allowed a normal risk-adjusted return on its capital base

before any rent is taxed. Only AAVA above that uplift is treated as automation rent. For software firms,

CapitalBase uses an imputed methodology to address AASB 138 intangibles restrictions (see section 12).

### 5.9 Combined cap and total liability

Credits_i = min(VerifiedCredits_i, theta * (AEL_payable,i + ARL_i))

CombinedLiability_i = AEL_payable,i + ARL_i - Credits_i

Liability_i = min(CombinedLiability_i, LAMBDA_j * AAVA_i)

TotalTax_i = BaseCompanyTax_i + Liability_i

[assessed before Pillar Two top-up]

Plain English. Verified employment, training, and transition credits reduce the combined liability, capped

so they cannot eliminate it entirely absent a specific legislated exemption. The combined liability is then

subjected to an outer cap (LAMBDA_j * AAVA_i) to prevent the AEL and ARL stacking onto the same

value base without ceiling. CARSF is assessed before Pillar Two top-up and, where appropriate, declared

as a covered tax under GloBE rules to minimise double taxation.

## 6. Worker-state taxonomy

Worker-level fiscal damage is calibrated at the national level for FRV vector construction, not assessed at

the firm level. This prevents double-counting across job loss, wage compression, underemployment, and

career scarring.

State Description Fiscal treatment

A. Unemployed after Worker displaced and not re-employed in Lost PIT plus transfer/support cost plus relevant

displacement the period. transition costs.

B. Re-employed at lower Worker finds work at a lower annual Tax loss on the wage gap, less re-employment

wage wage. recovery.

C. Underemployed Worker remains employed with materially Tax loss on hours and wage reduction.

reduced hours.

D. Retained, Worker keeps role but wage growth is Wage-compression tax loss only.

wage-suppressed suppressed by automation bargaining

effects.

E. Career-scarring residual Future earnings path is lowered, Discounted future PIT and related fiscal losses

especially where entry-level roles erode. after direct states are accounted for.

### 6.1 National calibration only

These states are used by Treasury to construct FRV vectors. They are not individually attributable to firms.

The firm-level liability flow in section 5 uses FRV as an aggregate sector- and occupation-conditional

value, not as a worker-by-worker calculation.

LifetimeFiscalDamage = sum over t of [StateFiscalLoss_t / (1 + r)^t]

where r = long-term Treasury bond yield consistent with the

Intergenerational Report discount-rate convention.

## 7. Fiscal Replacement Value layers

FRV is a vector, not a single national number. Each sector schedule publishes its own FRV vector at floor,

standard, and full layers.

Layer Components Use

FRV floor Lost PIT plus minimum transfer-support cost. National illustrative

communication only; not used in

firm-level liability under V1.4.

FRV standard FRV floor plus GST effects (symmetrically, including productivity Default firm-level assessment

dividend), average transfer supplements, retraining and layer.

administration, HELP repayment loss, and expected 24-month

re-employment recovery.

FRV full FRV standard plus health, housing, superannuation guarantee Treasury and PBO long-run fiscal

future cost, state payroll tax loss, regional impact, wage scarring, risk analysis and CARS-I

and long-term discounted fiscal damage. calibration.

FRV_j,t = PITLoss_j,t + TransferCost_j,t + GSTNet_j,t

+ RetrainingCost_j,t + HELP_Loss_j,t + SG_FutureCost_j,t

+ StateCost_j,t + ScarringCost_j,t

- ReemploymentRecovery_j,t
- ProductivityDividendFiscalGain_j,t
Plain English. The standard FRV nets the gross fiscal losses against re-employment recoveries and any

GST gains from cheaper goods. The productivity-dividend offset is required for honesty: if automation

lowers consumer prices, the fiscal picture is genuinely better than gross-loss accounting suggests.

Treasury must model this symmetrically.

## 8. Industry schedule architecture

> TODO(V1.5): Attach Prototype Schedule A for automotive repair and Prototype Schedule B for logistics / warehousing, including measurement fields and calibration data requirements.


No single national HLE formula can cover the economy. Each sector requires its own schedule binding

one canonical Output unit, an AII weighting vector, an FRV vector, safe-harbour thresholds, and

concessional categories. The table below is illustrative.

Schedule Canonical Output unit Indicative AII proxies

Automotive repair and Book-hour-equivalent jobs Robotic repair hours, AI diagnostic share, automated

maintenance completed. booking and admin share.

Logistics and delivery Tonne-kilometres delivered. Autonomous routing share, automated dispatches,

driverless kilometres.

Schedule Canonical Output unit Indicative AII proxies

Warehousing Pallet movements. Robotics capital ratio, automated movement share,

machine operating hours.

Call centres and customer support Cases resolved. Automated resolution share, AI agent minutes,

human escalation ratio.

Accounting and administration Filings or transactions lodged. AI document share, automated reconciliations,

automated lodgement support.

Software and digital platforms Australian-served Compute spend ratio, automated decision volume,

transactions. AI-generated workflows.

Retail Customer transactions. Self-checkout share, automated inventory, robotic

fulfilment.

Healthcare admin and support Claims and bookings AI triage and admin share, automated coding,

processed. workflow automation.

Manufacturing and robotics Defect-adjusted units Robotics capital ratio, autonomous production hours,

produced. human supervision ratio.

Agriculture and mining Tonnes or hectares produced Autonomous equipment hours, remote-operation

or serviced. share, AI exploration share.

Note. Multi-schedule firms apportion across schedules using a published methodology determined by the

Schedules Authority. Schedule classification is binding for an assessment period and disputable through the

standard dispute resolution pathway (section 14).

## 9. Liability design and safe harbours

Element V1.4 design

Small business safe harbour Simplified exemption below $10m turnover, unless the firm is part of a larger group or

operates high-scale autonomous production. Threshold reviewed by the Schedules

Authority every three years.

Startup safe harbour Five years from incorporation, or pre-revenue period, whichever ends first. Subject to

anti-avoidance for entity-splitting.

Worker-assist AI concession Objective test. Applies where the firm's QLC-per-output ratio is at or above the 60th

percentile of its sector LIBC. Self-declared worker-assist claims are not sufficient.

Compliance, safety, and Concessional treatment for AI used to improve tax compliance, recordkeeping,

accessibility AI concession workplace safety, accessibility, or public-interest services. Subject to disclosure.

Essential services filter Consumer pass-through review before activation of liability on firms supplying essential

goods and services (utilities, primary healthcare, basic food retail, public transport).

Credit cap (theta) Verified employment, training, and transition credits cannot eliminate liability entirely

absent a specific legislated exemption. Indicative starting cap is theta = 0.6 of AEL +

ARL.

Combined liability cap (LAMBDA) Outer cap on AEL + ARL as a share of AAVA. Indicative starting cap is LAMBDA =

0.25, sector-tunable.

Automation Fiscal Shortfall Where caps reduce payable liability below raw fiscal exposure, the shortfall is recorded

for CARS-I monitoring, not collected.

## 10. Legal feasibility and international interaction

Final design requires constitutional and tax counsel. The notes below identify risks without overclaiming

certainty.

Issue Risk and design response

Commonwealth taxation power (s Probably solid. Taxable event needs to be cleanly defined: carrying on an enterprise in

51(ii)) Australia with reportable automation intensity above a sector threshold, producing a

non-zero NLTG in the assessment period.

Acquisition on just terms (s Live but probably weak argument that retrospective taxation of returns from existing

51(xxxi)) automation amounts to expropriation. V1.4's prospective-only design substantially

reduces this risk.

State preference (s 99) Sector schedules will have regional incidence. Defensible if drawn on sector lines, not

state lines, but tax counsel review required.

Corporations power (s 51(xx)) Relevant for disclosure obligations on foreign-incorporated firms operating in Australia.

OECD Pillar Two CARSF assessed before Pillar Two top-up. Where CARSF qualifies as a covered tax

under GloBE rules, it counts toward the 15% effective rate, minimising double taxation

on multinationals.

Trade and treaty exposure Targeted destination-based levies on digital service providers can attract US trade

pressure. Mitigation: framing as domestic fiscal stabilisation; equal application to

domestic and foreign automated output consumed in Australia; alignment with Pillar

Two.

Privacy and disclosure Disclosure is summary-level (automation intensity, decision volumes, labour ratios).

Source code, training data, customer-level personal data, and proprietary weights are

not disclosed under CARSF absent a separate legal power.

Federal-state interaction Intergovernmental revenue-sharing mechanism for payroll tax loss, TAFE, health,

housing, and regional transition. Comparable in structure to GST distribution; final

design by Heads of Treasuries.

## 11. Tax incidence and productivity dividend

CARSF is honest about economic incidence. A firm pays the liability, but the economic burden may fall on

consumers, workers, shareholders, foreign capital, or suppliers in proportions that vary by sector, market

power, import competition, and capital mobility.

Channel Risk V1.4 response

Consumers Liability passed through as higher Consumer pass-through filter; essential services

prices. concession; phased activation.

Workers Firms offset liability by reducing QLC protection; wage-compression monitoring;

wages or hiring. labour-market safeguards inside FRV calibration.

Domestic capital Reduced returns to shareholders. Acceptable where liability captures rent or labour-tax

gap; combined cap (LAMBDA) limits stacking.

Foreign capital Offshore owners bear part of Destination and activity attribution; treaty review; Pillar

Australian activity liability. Two alignment.

Productivity dividend Automation lowers prices and raises Modelled symmetrically in FRV (subtracted as

real consumption. ProductivityDividendFiscalGain).

### 11.1 Behavioural elasticity and deadweight loss

CARSF will alter firm behaviour. Firms may delay automation, restructure to fall under safe harbours, shift

activity offshore, or accept reduced rents. The deadweight loss depends on the elasticity of automation

investment with respect to expected CARSF liability, which is not yet estimated for Australia. Shadow

assessment in Phase 2 should generate the data required for Treasury to publish an elasticity estimate

before activation.

## 12. Capital base for software and digital firms

AASB 138 restricts capitalisation of internally generated intangibles. Book capital base for pure-software

firms therefore under-represents real productive capital, inflating apparent rent under a naive ARL

calculation. V1.4 specifies an imputed methodology.

ImputedCapitalBase_i =

CumulativeR&D_i * AmortisationFactor_R&D

+ CumulativeComputeSpend_i * AmortisationFactor_Compute

+ RecognisedTangible_i + RecognisedIntangible_i

AmortisationFactor parameters set by the Schedules Authority.

Plain English. For software-sector schedules, R&D and compute spending are imputed into the capital

base on an amortised schedule, in addition to recognised tangible and intangible assets. This avoids

systematically over-taxing software firms relative to robotics-heavy firms.

## 13. Cross-border automation and anti-avoidance

The largest avoidance risk is not a domestic firm hiding a robot. It is an Australian-facing business

consuming automation as an imported service from an offshore related party, or routing Australian

economic activity through low-tax jurisdictions.

CARSF is destination- and activity-based. If automated productive capacity serves

Australian customers, produces Australian-facing value, or substitutes for Australian

qualified labour contribution, the framework measures the Australian nexus regardless of

where the server, software, or IP owner is located.

Avoidance vector V1.4 response

Imported automation service Australian consumption and activity attribution rules; related-party automation service

disclosure; alignment with significant global entity regime.

Token QLC inflation Additive QLC weights with floors; wage, hours, security, skill development, and

Australian nexus all required.

Revenue attribution gaming AAVA based on destination and activity, not on business-unit labels.

Input reclassification Standard automation cost categories and audit trails; integration with Part IVA

anti-avoidance and a CARSF-specific anti-avoidance provision for the dominant

purpose of obtaining a labour-tax-gap benefit.

Sector schedule arbitrage Dominant activity test anchored to ANZSIC classification, with binding determinations

from the Schedules Authority.

Sell-and-leaseback of automation Control- and use-based attribution, not only legal asset ownership.

Avoidance vector V1.4 response

Offshore IP royalty stripping Alignment with transfer pricing, diverted profits tax, significant global entity rules, and

Pillar Two.

Entity splitting for safe harbour Aggregation of grouped entities for safe-harbour thresholds; integrity rule against

splitting solely for CARSF purposes.

## 14. Administrative architecture

V1.4 deliberately separates collection from schedule design and labour-quality standards. The ATO is not

made a labour-market regulator.

Institution Role

Treasury Policy owner. Fiscal modelling. Intergovernmental agreements. Legislative design.

Australian Taxation Office Assessment, collection, anti-avoidance enforcement, disclosure compliance, and

rulings.

CARSF Schedules Authority Specialist statutory body. Maintains LIBCs, AII weights, FRV vectors, sector schedules,

(proposed) and review processes. Draws on Productivity Commission, ABS, Fair Work, and

Treasury expertise.

Australian Bureau of Statistics Labour-market and sector data; statistical infrastructure.

Parliamentary Budget Office Independent costing and medium-term fiscal stress testing on request.

Fair Work Commission Input into labour-quality weights and job-security criteria via the Schedules Authority.

Department of Industry, Science Coordination with the AI Safety Standard and the Voluntary AI Safety Standard to avoid

and Resources duplicate disclosure.

States and territories Revenue-sharing, TAFE, health, housing, payroll-tax replacement, and regional

transition support.

### 14.1 Dispute resolution

Disputes follow the standard tax dispute pathway with one addition. Internal review by the ATO is available

for assessment and credit determinations. The Administrative Review Tribunal (ART) provides merits

review. The Federal Court provides judicial review. Sector-classification and LIBC-cohort determinations

may be reviewed by the Schedules Authority before any ART application.

### 14.2 Data, privacy, and disclosure overlap

- Disclosure is summary-level: automation intensity, automated decisions or actions, labour ratios,
sector schedule inputs, related-party automation services, and AAVA components.

- CARSF does not require routine disclosure of source code, training data, customer-level personal
data, or proprietary model weights. A separate legal power and privacy framework would apply for any

such request.

- Public reporting is aggregated by sector and firm size to protect commercially sensitive information.
- Where firms already report under the AI Safety Standard, the Voluntary AI Safety Standard, the
Modern Slavery Act reporting regime, or significant global entity rules, CARSF disclosure must align to

avoid duplicate burden. The Schedules Authority is responsible for the alignment map.

### 14.3 CARS-I: Commonwealth Automation Revenue Stress Index

> TODO(V1.5): Add CoverageRatio = AutomationRevenueCaptured / NationalAutomationFiscalDamage beside CARS-I and define zero-damage handling.


CARS-I_t = NationalAutomationFiscalDamage_t

/ (AutomationRevenueCaptured_t + epsilon)

where epsilon is a defined small constant preventing divide-by-zero.

CARS-I value Meaning

Less than 0.70 Stable. Automation revenue capture comfortably exceeds measured fiscal damage.

### 0.70 to 1.00 Warning zone. Fiscal pressure is building.

### 1.00 Breakpoint. Automation-related fiscal damage equals automation revenue captured.

Greater than 1.00 Stress zone. Automation costs exceed revenue capture.

## 15. Government use of AI

The Commonwealth does not pay tax to itself. CARSF therefore exempts Commonwealth agencies from

firm-level liability, but tracks public-sector automation in national CARS-I monitoring and applies

CARSF-style disclosure to private contractors delivering automated public services under government

procurement.

Category Treatment

Internal Commonwealth productivity and Recorded in national CARS-I monitoring. Exempt from firm-level liability.

compliance AI

AI replacing public-sector labour Requires workforce transition plan, redeployment plan, and reporting to

Parliament.

Public AI infrastructure Treated as sovereign productivity infrastructure. Outputs tracked for public

dividend and service-delivery gains.

Private contractors delivering automated Subject to CARSF-style disclosure where automation substitutes for Australian

public services labour under government procurement.

Note. Acknowledged distortion. The exemption of internal Commonwealth AI from firm-level liability

creates a small procurement preference for direct government AI delivery over contracted delivery. The

Schedules Authority monitors this and reports to Parliament if the distortion becomes material under

Commonwealth Procurement Rules.

## 16. Implementation roadmap

CARSF is staged. No liability attaches before Phase 3. The legislated commencement year fixes the

prospective baseline for LIBC and forms the earliest date from which NLTG can be assessed for liability.

Phase Timeframe Output

Phase 0: Research and 0-12 months Treasury, ABS, PBO scoping; legal review; sector selection; consultation;

design AAT precedent review.

Phase 1: Disclosure pilot Year 1-2 Voluntary or mandatory reporting for selected high-risk sectors. No liability.

Phase 2: Shadow Year 2-3 Firms receive non-payable indicative CARSF assessments. Schedules

assessment refined. Elasticity estimates produced.

Phase Timeframe Output

Phase 3: Limited activation Year 3-5 Liability activated only for large firms in high-confidence sectors with high

NLTG and AAVA. Commencement year for prospective baseline.

Phase 4: Review and Year 5+ Parliamentary review; possible expansion; safe-harbour adjustment; UBI

expansion affordability gate assessment.

## 17. National Productivity Transition Fund and UBI gate

CARSF revenue is directed into a legally quarantined National Productivity Transition Fund. Universal

payments are not promised. The fund's uses are staged and conditional.

Stage Funding purpose

Stage 1 Displacement support, rapid retraining, wage insurance, and income smoothing for affected workers.

Stage 2 Apprenticeship and entry-level role protection, TAFE capacity, regional transition programs, career

re-skilling.

Stage 3 Targeted automation dividend for cohorts or regions directly affected by measurable automation transition.

Stage 4 Broader universal payment only if revenue, productivity, and fiscal-sustainability tests are met.

UBI_Eligible = (CARSF_Revenue

- TransitionLiabilities
- AdminCost
- StabilisationReserve) >= UBI_Cost

## 18. Red-team objections and responses

Source Strongest attack V1.4 response

Treasury The AII components could still be gamed via Components anchored to AASB and ABS

accounting choices. definitions in Appendix C. Schedules Authority

publishes test cases. Shadow assessment

surfaces gaming patterns before activation.

Treasury Why not just raise company tax? Section 3.1 addresses this directly. Company tax

misses profit-shifted automated platforms, has no

distributional layer, and produces no

automation-intensity dataset. CARSF

complements rather than competes.

ATO Schedules Authority assumes a body that Schedules Authority must be created in

does not exist. ATO will end up doing the legislation, funded, and staffed before Phase 3

work. activation. If it cannot be established, Phase 3

does not commence.

Productivity Anything that taxes productivity will reduce it. CARSF does not tax productivity. It taxes the

Commission labour-tax gap and excess rent. A firm matching

benchmark labour intensity has zero CARSF

liability. The framework is explicitly

pro-productivity in design.

Department of Finance Revenue is uncertain and administratively Phase 2 shadow assessment produces revenue

expensive. Cost-benefit may not favour and cost estimates before activation. If

activation. cost-benefit fails, the framework does not

proceed to Phase 3.

Fair Work Commission Labour-quality weights belong with us, not a Fair Work provides labour-quality input into the

new authority. Schedules Authority. The Schedules Authority

synthesises, ATO administers. Fair Work retains

its labour standards role.

Business lobby (BCA, Triple-tax: company tax, Pillar Two, now this. CARSF is assessed before Pillar Two top-up and

AICD) counts as covered tax where qualifying. Where it

does not stack, the combined cap (LAMBDA)

limits exposure.

Small business Small firms using AI admin tools will be $10m safe harbour, simplified self-assessment,

(COSBOA) punished alongside platforms. worker-assist concession (objective test). The

framework is not designed to reach small

businesses using ordinary AI productivity tools.

Unions (ACTU) The framework rewards firms for buying out $45,255 is a national illustration, not a firm-level

workers at the $45,255 floor. FRV under V1.4. Workplace separation

entitlements and transition payments are set by

other instruments. CARSF measures fiscal

exposure, not compensation.

Economists Tax incidence falls on consumers and Acknowledged. Section 11 models incidence

(academic) immobile labour, not on machines. symmetrically. The framework is presented as

distributional stabilisation, not revenue

replacement.

Civil liberties Mandatory disclosure puts the ATO inside Disclosure is summary-level. Source code,

advocates every firm's tech stack. training data, and personal data are not required.

Aligned with AI Safety Standard to avoid

duplicate burden.

Source Strongest attack V1.4 response

Multinational tech firms Australia goes alone; capital leaves. Destination- and activity-based attribution; Pillar

Two alignment; CARSF reach does not depend

on physical presence. Leaving does not reduce

liability for Australian-facing automated value.

State governments We bear payroll tax loss without revenue Intergovernmental revenue-sharing mechanism

share. for payroll tax, TAFE, health, housing, and

regional transition; final design by Heads of

Treasuries.

Free-market critics Benchmarks are central planning. LIBCs are measurement baselines, not

(IPA, CIS) production rules. Firms may automate freely; the

schedule sets the assessment baseline only.

UBI advocates The affordability gate ensures UBI never Stages 1-3 deliver real income support before

arrives. UBI. Stage 4 is conditional, not impossible.

Promising affordability without conditions

discredits the whole framework.

AI industry and This kills Australian AI before it starts. Five-year startup safe harbour. Worker-assist,

startups compliance, safety, and accessibility AI

concessions. Compute-spend imputed into

capital base for software firms (section 12) to

avoid systematic over-taxation.

## 19. Limitations and required research

V1.4 is a concept paper. Before any legislative drafting, the following work is required.

- Build two worked sector pilots end-to-end: automotive repair and logistics or warehousing.
- Construct sector-conditional FRV vectors using ATO, ABS, DSS, HILDA, HELP, superannuation, and
transfer-system data.

- Test LIBC benchmarks for stability under automation diffusion. Calibrate the asymmetric ratchet
parameter.

- Model consumer pass-through and productivity dividend by sector, including symmetric GST
treatment.

- Estimate the elasticity of automation investment with respect to expected CARSF liability for at least
three sectors.

- Design cross-border automation consumption rules compatible with Australia's international tax and
trade obligations.

- Map interaction with R&D Tax Incentive, instant asset write-off, depreciation rules, digital services
frameworks, transfer pricing, diverted profits tax, and OECD Pillar Two.

- Develop a privacy-preserving automation disclosure regime aligned to the AI Safety Standard.
- Test against small business, startup, multinational, public-sector, and open-source AI cases.
- Develop a Commonwealth-state revenue-sharing model.
- Commission independent tax counsel review on retrospectivity, just-terms acquisition, state
preference, and treaty risk before external circulation.

- Engage Treasury-trained economic review of behavioural elasticity, deadweight loss, and revenue
forecasts.

## 20. Conclusion

CARSF V1.4 rests on a narrow claim: where automated productive capacity materially reduces the

qualified human labour contribution that Australia's existing tax base assumes, the fiscal system should

measure and manage that transition deliberately, with prospective effect, and through a framework that

complements rather than replaces existing company tax.

The framework is not a demand to stop AI, punish productivity, or immediately fund a universal basic

income. It is a proposal to create a measurement architecture before automation makes reactive policy

unavoidable. Its purpose is fiscal resilience, fairer transition cost distribution, and ensuring that productivity

gains do not leave the public revenue system anchored to a shrinking labour base.

Automation should be allowed to increase national productivity. But if productivity migrates

away from taxable labour, the fiscal architecture must migrate with it.

## Appendix A - National illustrative floor calculation

Retained for context only. Not used as a firm-level FRV under V1.4.

Calculation Working Rounded result

PIT per employed worker (national mean) $357.8b / 14,767,700 $24,229 per year

Annualised JobSeeker single, no children $808.70 x 26 $21,026 per year

National illustrative floor (sum) $24,229 + $21,026 $45,255 per net labour-tax-gap

unit per year

Note. This floor uses the national mean PIT per employed worker, which is highly skewed by income

distribution. It excludes GST loss, rent assistance, family payments, HELP repayment loss, superannuation

effects, retraining, health pressure, state payroll tax loss, wage scarring, and regional effects. Firm-level

assessment under V1.4 uses sector-conditional FRV vectors drawn from HILDA, occupational, and

transfer-system data, not this national mean.

## Appendix B - Equation glossary

Symbol Meaning

i, j, t, w Firm; sector schedule; assessment period; worker.

QLC Qualified Labour Contribution.

LIBC Labour-Intensity Benchmark Cohort.

OPFTE Output per qualified full-time equivalent in the LIBC.

HLE Human Labour Equivalent.

AII Automation Intensity Index.

NLTG Net Labour Tax Gap.

FRV Fiscal Replacement Value.

AAVA Australian Automated Value Added.

AEL Automation Equilibrium Levy.

ARL Automation Rent Levy.

lambda_j Sector-specific capacity-to-pay cap (AEL share of AAVA).

LAMBDA_j Sector-specific combined cap (AEL + ARL share of AAVA).

theta Credit cap (share of AEL + ARL above which credits cannot reduce liability).

CARS-I Commonwealth Automation Revenue Stress Index.

r Discount rate; long-term Treasury bond yield, Intergenerational-Report-consistent.

## Appendix C - AII component definitions

AII components are defined as ratios in [0, 1] with anchored denominators. The Schedules Authority

publishes the canonical definitions and updates them as accounting standards or measurement practice

evolve.

Component Numerator Denominator Anchoring

ComputeRatio Audited compute spend (cloud Total operating expenditure. Audited financial statements;

and on-prem inference and reconciled to AASB statements.

training).

AutoDecisionRatio Number of decisions or Total decisions or actions of Defined by sector schedule with

actions executed by comparable kind. binding ontology for "decision".

automated systems without

human-in-the-loop.

RoboticsCapitalRat Recognised value of robotics, Total productive capital AASB 116 and AASB 138;

io autonomous equipment, and (recognised plus imputed for imputed methodology for software

automated production assets. software firms per section 12). firms.

AutoProcessShare Output produced by Total output of the firm in the Process taxonomy defined by

automated processes sector's canonical Output unit. sector schedule.

(sector-defined process

categories).

Note. AII is bounded in [0, 1] with sector-determined weights summing to 1. The circular

"LabourIntensityShift" term from V1.3 has been removed because it conflated the dependent variable

(labour intensity) with the independent measure (automation intensity).

## References and source base

[1] Parliamentary Budget Office, 2025-26 Medium-Term Budget Outlook: Beyond the Budget, published 18 September 2025.

https://www.pbo.gov.au/publications-and-data/publications/2025-26-Medium-term-budget-outlook

[2] Australian Bureau of Statistics, Labour Force, Australia, March 2026.

https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/latest-release

[3] Services Australia, JobSeeker Payment rates from 20 March 2026.

https://www.servicesaustralia.gov.au/how-much-jobseeker-payment-you-can-get?context=51411

[4] Australian Taxation Office, Company tax rates 2025-26.

https://www.ato.gov.au/tax-rates-and-codes/company-tax-rates/tax-rates-2025-26

[5] Australian Taxation Office, Global and domestic minimum tax: Pillar Two implementation. https://www.ato.gov.au/businesses-and

-organisations/international-tax-for-business/in-detail/multinationals/global-and-domestic-minimum-tax

[6] OECD, AI and work. https://www.oecd.org/en/topics/ai-and-work.html

[7] OECD, The impact of Artificial Intelligence on productivity, distribution and growth, 2024.

https://www.oecd.org/en/publications/the-impact-of-artificial-intelligence-on-productivity-distribution-and-growth_8d900037-en.html

[8] IMF, Broadening the Gains from Generative AI: The Role of Fiscal Policies, Staff Discussion Note SDN/2024/002. https://www.imf

.org/en/publications/staff-discussion-notes/issues/2024/06/11/broadening-the-gains-from-generative-ai-the-role-of-fiscal-policies-549

639

[9] Australian Government, Policy for the responsible use of AI in government, v2.0 effective 15 December 2025.

https://www.digital.gov.au/ai/ai-in-government-policy

[10] Australian Government, AI Plan for the Australian Public Service 2025.

https://www.digital.gov.au/policy/ai/australian-public-service-ai-plan-2025

[11] Australian Accounting Standards Board, AASB 116 Property, Plant and Equipment.

[12] Australian Accounting Standards Board, AASB 138 Intangible Assets.

[13] Petroleum Resource Rent Tax Assessment Act 1987 (Cth) and associated regulations (uplift-rate framework).

[14] Department of Industry, Science and Resources, Voluntary AI Safety Standard (2024).
