# CARSF V1.5 Sector Stress Matrix

Generated at: `2026-05-17T06:11:15+00:00`

## A. Purpose

This report compares prototype CARSF schedules across metadata-only review dimensions so reviewers can see where placeholder schedules are fragile, sensitive, or governance-heavy.

## B. Non-Claims

- The sector stress matrix is prototype metadata review only. It is not calibrated. It is not a real-world ranking of sectors. It is not Treasury modelling. It is not ATO guidance. It is not ABS/ATO/DSS/PBO analysis. It does not use real industry data. It does not estimate actual tax payable.
- The sector stress matrix does not modify firm-level CARSF liability logic.
- The sector stress matrix does not implement legal sector attribution or real multi-schedule blending.
- The sector stress matrix is not economic validation, investment advice, legal advice, or tax advice.
- All schedules remain placeholder-only and subject to external calibration, legal review, and methods review.
- Do not rank schedules using this matrix.

## C. Method - Placeholder Metadata Only

Scores are deterministic placeholders derived only from schedule metadata such as AII weights, QLC weights, cap placeholders, avoidance controls, calibration requirements, attribution wording, and unresolved review notes. No real sector data is used.

## D. Sector Coverage

- `accounting_administration`: Prototype Schedule D - Accounting / Administration
- `automotive_repair`: Prototype Schedule A - Automotive Repair
- `call_centres_customer_support`: Prototype Schedule C - Call Centres / Customer Support
- `logistics_warehousing`: Prototype Schedule B - Logistics / Warehousing
- `retail_self_checkout_fulfilment`: Prototype Schedule E - Retail Self-Checkout / Fulfilment
- `software_digital_platforms`: Prototype Schedule F - Software / Digital Platforms

## E. Stress Band Definitions

- `low_placeholder_stress`: low metadata review pressure.
- `moderate_placeholder_stress`: moderate metadata review pressure.
- `high_placeholder_stress`: high metadata review pressure.
- `critical_review_required`: critical placeholder review pressure before policy discussion.
- `not_assessable`: missing or non-interpretable metadata.

## F. Sector Stress Matrix

| Schedule ID | Schedule Name | Canonical Output Unit | Automation Intensity | QLC Vulnerability | AAVA Sensitivity | Incidence Risk | Investment Risk | Avoidance / Gaming Risk | Calibration Difficulty | Legal Attribution Difficulty | Display Status | Do Not Rank | Main Reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| accounting_administration | Prototype Schedule D - Accounting / Administration | standardised_transactions_or_filings_processed | critical_review_required | high_placeholder_stress | moderate_placeholder_stress | moderate_placeholder_stress | low_placeholder_stress | high_placeholder_stress | critical_review_required | high_placeholder_stress | external_review_required | True | automation_intensity_placeholder is critical_review_required using placeholder metadata only. |
| automotive_repair | Prototype Schedule A - Automotive Repair | book_hour_equivalent_jobs_completed | high_placeholder_stress | high_placeholder_stress | moderate_placeholder_stress | moderate_placeholder_stress | low_placeholder_stress | high_placeholder_stress | high_placeholder_stress | high_placeholder_stress | strong_warning_required | True | automation_intensity_placeholder is high_placeholder_stress using placeholder metadata only. |
| call_centres_customer_support | Prototype Schedule C - Call Centres / Customer Support | resolved_customer_support_cases | critical_review_required | high_placeholder_stress | moderate_placeholder_stress | moderate_placeholder_stress | low_placeholder_stress | high_placeholder_stress | high_placeholder_stress | moderate_placeholder_stress | external_review_required | True | automation_intensity_placeholder is critical_review_required using placeholder metadata only. |
| logistics_warehousing | Prototype Schedule B - Logistics / Warehousing | tonne_kilometres_or_pallet_movements | critical_review_required | high_placeholder_stress | moderate_placeholder_stress | critical_review_required | low_placeholder_stress | high_placeholder_stress | high_placeholder_stress | high_placeholder_stress | external_review_required | True | automation_intensity_placeholder is critical_review_required using placeholder metadata only. |
| retail_self_checkout_fulfilment | Prototype Schedule E - Retail Self-Checkout / Fulfilment | customer_transactions_or_order_fulfilments | critical_review_required | high_placeholder_stress | moderate_placeholder_stress | high_placeholder_stress | low_placeholder_stress | high_placeholder_stress | critical_review_required | high_placeholder_stress | external_review_required | True | automation_intensity_placeholder is critical_review_required using placeholder metadata only. |
| software_digital_platforms | Prototype Schedule F - Software / Digital Platforms | australian_served_platform_transactions_or_workflows | critical_review_required | moderate_placeholder_stress | critical_review_required | high_placeholder_stress | high_placeholder_stress | critical_review_required | critical_review_required | critical_review_required | external_review_required | True | aava_sensitivity_placeholder is critical_review_required using placeholder metadata only. |

## G. Automation Intensity Placeholder Bands

- `high placeholder stress`: automotive_repair
- `critical review required`: accounting_administration, call_centres_customer_support, logistics_warehousing, retail_self_checkout_fulfilment, software_digital_platforms

## H. QLC Vulnerability Placeholder Bands

- `moderate placeholder stress`: software_digital_platforms
- `high placeholder stress`: accounting_administration, automotive_repair, call_centres_customer_support, logistics_warehousing, retail_self_checkout_fulfilment

## I. AAVA Sensitivity Placeholder Bands

- `moderate placeholder stress`: accounting_administration, automotive_repair, call_centres_customer_support, logistics_warehousing, retail_self_checkout_fulfilment
- `critical review required`: software_digital_platforms

## J. Avoidance / Gaming Risk Placeholder Bands

- `high placeholder stress`: accounting_administration, automotive_repair, call_centres_customer_support, logistics_warehousing, retail_self_checkout_fulfilment
- `critical review required`: software_digital_platforms

## K. Calibration Difficulty Placeholder Bands

- `high placeholder stress`: automotive_repair, call_centres_customer_support, logistics_warehousing
- `critical review required`: accounting_administration, retail_self_checkout_fulfilment, software_digital_platforms

## L. Legal Attribution Difficulty Placeholder Bands

- `moderate placeholder stress`: call_centres_customer_support
- `high placeholder stress`: accounting_administration, automotive_repair, logistics_warehousing, retail_self_checkout_fulfilment
- `critical review required`: software_digital_platforms

## M. Display-Control Status

- `external_review_required`: accounting_administration, call_centres_customer_support, logistics_warehousing, retail_self_checkout_fulfilment, software_digital_platforms
- `strong_warning_required`: automotive_repair

## N. Cross-Sector Observations Without Rankings

- This matrix groups schedules by placeholder metadata stress bands only.
- A schedule with stronger warnings is not described as better or worse than another schedule.
- Rows with external-review status require calibration, legal attribution review, and methods review before policy use.
- Every row remains marked `do_not_rank: true`.
- `software_digital_platforms` carries software/intangible capital-base review warnings, including unresolved AASB 138 treatment.

## O. Calibration and External Review Blockers

- accounting_administration: ABS and ATO data separating accounting, bookkeeping, payroll, administration, and professional-services activities.
- accounting_administration: Accounting platform transaction volumes, workflow automation adoption, and document-processing data.
- accounting_administration: Fair Work award, classification, and job-security data for clerical and accounting-support roles.
- accounting_administration: HILDA, DSS, and labour-market transition data for displaced administrative and accounting-support workers.
- accounting_administration: Legal and tax review of professional judgement, advice, audit, and lodgement boundaries.
- accounting_administration: Professional-services and administration workforce wage and output data.
- automotive_repair: ABS labour force and output measures for repair and maintenance.
- automotive_repair: ATO small-business and company tax data by automotive repair ANZSIC class.
- automotive_repair: DSS transfer-system data and HELP repayment loss assumptions.
- automotive_repair: Fair Work occupational classifications, wage distributions, and casualisation measures.
- automotive_repair: HILDA income-transition and wage-scarring data for displaced mechanics and apprentices.
- automotive_repair: Workshop robotics and AI diagnostic adoption data from industry surveys.
- call_centres_customer_support: ABS and industry customer-service workforce and output data.
- call_centres_customer_support: AI agent, chatbot, and automated triage adoption data from industry surveys.
- call_centres_customer_support: ATO aggregated tax data for customer support and contact-centre entities.
- call_centres_customer_support: CRM/ticketing benchmark data for resolved support cases per qualified FTE.
- call_centres_customer_support: DSS, HILDA, and labour-market transition data for displaced customer support workers.
- call_centres_customer_support: Fair Work wage, award, casualisation, and job-security data for support workers.
- logistics_warehousing: ATO, ABS, and industry data separating freight, last-mile delivery, warehousing, and platform dispatch.
- logistics_warehousing: Autonomous vehicle kilometres, automated dispatch share, and warehouse robotics adoption data.
- logistics_warehousing: HILDA and DSS data on driver, picker, packer, dispatcher, and warehouse transition outcomes.
- logistics_warehousing: State payroll tax exposure and regional employment concentration.
- logistics_warehousing: Transfer pricing, diverted profits tax, and significant global entity interaction analysis.
- retail_self_checkout_fulfilment: ABS, ATO, and industry data separating store retail, online retail, fulfilment, and marketplace activities.
- retail_self_checkout_fulfilment: Fair Work retail, warehouse, and fulfilment wage and employment data.
- retail_self_checkout_fulfilment: HILDA, DSS, and labour-market transition data for displaced retail and fulfilment workers.
- retail_self_checkout_fulfilment: Legal review of customer self-service, contractor labour, platform retail, and fulfilment attribution.
- retail_self_checkout_fulfilment: POS, self-checkout, fulfilment, and inventory automation benchmark data.
- retail_self_checkout_fulfilment: State payroll tax and regional employment data for retail and fulfilment sites.
- software_digital_platforms: AASB 138, tax counsel, Treasury, and ATO review of intangible assets, capital base, IP royalties, and Australian value attribution.
- software_digital_platforms: ABS, ATO, and industry data separating software, platform, marketplace, digital services, and AI workflow activities.
- software_digital_platforms: Cloud, inference, model, and data-access cost data with Australian-facing attribution.
- software_digital_platforms: Fair Work and labour-market data for Australian software, moderation, support, and operations workforces.
- software_digital_platforms: HILDA, DSS, and labour-market transition data for displaced administrative, platform, support, and digital-service workers.
- software_digital_platforms: Platform transaction, workflow, recommendation, matching, and automated decision volume data.

## P. Limitations and Future Review Needs

### Stress Band Counts

- `low_placeholder_stress`: 5
- `moderate_placeholder_stress`: 10
- `high_placeholder_stress`: 21
- `critical_review_required`: 12
- `not_assessable`: 0

### Display-Control Counts

- `external_review_required`: 5
- `strong_warning_required`: 1

- External-review-required rows: 5
- Strong-warning rows: 1
- All rows marked do-not-rank: True

- Prototype only.
- Placeholder only.
- Metadata-only.
- Not calibrated.
- Not a real-world ranking of sectors.
- Not Treasury modelling, ATO guidance, ABS/ATO/DSS/PBO analysis, economic validation, investment advice, legal advice, or tax advice.
- No real industry data is used.
- Firm-level CARSF liability logic is not modified.
- Legal sector attribution and real multi-schedule blending are not implemented.
