# CARSF V1.5 Sector Schedule Expansion

Generated at: `2026-05-19T00:02:02+00:00`

## A. Purpose

This report validates and summarises the expanded prototype sector schedule library for CARSF V1.5.

## B. Non-Claims

- Sector schedules are prototype placeholders only. They are not calibrated. They are not legal schedules. They are not Treasury schedules. They are not ATO guidance. They are not ABS/ATO/DSS/PBO analysis. They do not contain real industry data. They must not be used to estimate actual tax payable.
- Sector schedules do not modify firm-level CARSF liability logic.
- Sector schedules do not implement real multi-schedule attribution.
- Sector schedules do not validate OPFTE, FRV, caps, or safe-harbour thresholds.
- Sector schedules are not legal schedules, Treasury schedules, ATO guidance, ABS/ATO/DSS/PBO analysis, or real industry data.
- Sector schedules must not be used to estimate actual tax payable.

## C. Schedule Coverage Summary

| Schedule | New In This Build | Canonical Output Unit | Calibration Status |
| --- | --- | --- | --- |
| Prototype Schedule D - Accounting / Administration | True | standardised_transactions_or_filings_processed | illustrative_placeholder_values_only |
| Prototype Schedule A - Automotive Repair | False | book_hour_equivalent_jobs_completed | illustrative_placeholder_values_only |
| Prototype Schedule C - Call Centres / Customer Support | True | resolved_customer_support_cases | illustrative_placeholder_values_only |
| Prototype Schedule B - Logistics / Warehousing | False | tonne_kilometres_or_pallet_movements | illustrative_placeholder_values_only |
| Prototype Schedule E - Retail Self-Checkout / Fulfilment | True | customer_transactions_or_order_fulfilments | illustrative_placeholder_values_only |
| Prototype Schedule F - Software / Digital Platforms | True | australian_served_platform_transactions_or_workflows | illustrative_placeholder_values_only |

## D. New Prototype Schedules

### Prototype Schedule D - Accounting / Administration

- Schedule ID: `accounting_administration`
- Canonical output unit: `standardised_transactions_or_filings_processed`
- OPFTE placeholder: `12000.0`
- Calibration status: `illustrative_placeholder_values_only`

### Prototype Schedule C - Call Centres / Customer Support

- Schedule ID: `call_centres_customer_support`
- Canonical output unit: `resolved_customer_support_cases`
- OPFTE placeholder: `8500.0`
- Calibration status: `illustrative_placeholder_values_only`

### Prototype Schedule E - Retail Self-Checkout / Fulfilment

- Schedule ID: `retail_self_checkout_fulfilment`
- Canonical output unit: `customer_transactions_or_order_fulfilments`
- OPFTE placeholder: `18000.0`
- Calibration status: `illustrative_placeholder_values_only`

### Prototype Schedule F - Software / Digital Platforms

- Schedule ID: `software_digital_platforms`
- Canonical output unit: `australian_served_platform_transactions_or_workflows`
- OPFTE placeholder: `25000.0`
- Calibration status: `illustrative_placeholder_values_only`

## E. Canonical Output Units

- `accounting_administration`: `standardised_transactions_or_filings_processed`
- `automotive_repair`: `book_hour_equivalent_jobs_completed`
- `call_centres_customer_support`: `resolved_customer_support_cases`
- `logistics_warehousing`: `tonne_kilometres_or_pallet_movements`
- `retail_self_checkout_fulfilment`: `customer_transactions_or_order_fulfilments`
- `software_digital_platforms`: `australian_served_platform_transactions_or_workflows`

## F. AII Weight Comparison

| Schedule | Compute | Auto Decision | Robotics Capital | Auto Process | Total |
| --- | ---: | ---: | ---: | ---: | ---: |
| accounting_administration | 0.25 | 0.25 | 0.05 | 0.45 | 1.00 |
| automotive_repair | 0.15 | 0.25 | 0.35 | 0.25 | 1.00 |
| call_centres_customer_support | 0.25 | 0.30 | 0.05 | 0.40 | 1.00 |
| logistics_warehousing | 0.20 | 0.30 | 0.20 | 0.30 | 1.00 |
| retail_self_checkout_fulfilment | 0.15 | 0.25 | 0.25 | 0.35 | 1.00 |
| software_digital_platforms | 0.30 | 0.30 | 0.05 | 0.35 | 1.00 |

## G. QLC Weight Comparison

| Schedule | Wage Quality | Job Security | Skill Development | Australian Nexus | QLC Max Multiplier |
| --- | ---: | ---: | ---: | ---: | ---: |
| accounting_administration | 0.20 | 0.18 | 0.18 | 0.16 | 1.25 |
| automotive_repair | 0.20 | 0.20 | 0.15 | 0.15 | 1.25 |
| call_centres_customer_support | 0.18 | 0.18 | 0.14 | 0.20 | 1.25 |
| logistics_warehousing | 0.18 | 0.20 | 0.12 | 0.20 | 1.25 |
| retail_self_checkout_fulfilment | 0.18 | 0.20 | 0.12 | 0.20 | 1.25 |
| software_digital_platforms | 0.22 | 0.16 | 0.20 | 0.14 | 1.25 |

## H. Schedule Measurement Risks

### accounting_administration
- Automated accounting workflows should not be routed into a low-intensity generic administration label.
- Related software, offshore processing, and employer entities require grouped review where Australian output is served.

### automotive_repair
- Dominant activity test should prevent a robotic repair facility from selecting a lower-intensity administrative schedule.
- Mixed businesses require schedule apportionment rather than choosing the most favourable schedule.

### call_centres_customer_support
- Support entities should not avoid this schedule by describing chatbot case resolution as ordinary software administration.
- Outsourced or offshore support structures require grouped-entity and related-party review.

### logistics_warehousing
- Platform dispatch, warehouse robotics, and transport operations require apportionment where multiple activities are present.
- A firm cannot avoid the schedule by describing automated dispatch as software administration when it controls Australian logistics output.

### retail_self_checkout_fulfilment
- Retail, online fulfilment, and logistics outputs require apportionment where multiple activities are present.
- Automated fulfilment cannot avoid this schedule by moving into a separate low-labour related entity without grouped review.

### software_digital_platforms
- Platform matching, ranking, pricing, workflow allocation, and recommendation systems require apportionment where mixed with retail, logistics, or support output.
- Offshore IP ownership, model access, or cloud infrastructure should not determine schedule classification alone.

## I. Avoidance / Gaming Risks

- `accounting_administration`: offshore_document_processing_services, ordinary_admin_relabelling, related_party_software_fees, token_reviewer_qlc_inflation
- `automotive_repair`: entity_splitting, fake_qlc_inflation, offshore_ai_services, related_party_ai_service_fees, token_human_oversight_jobs
- `call_centres_customer_support`: offshore_chatbot_service_fees, outsourced_support_entity_splitting, relabelled_ai_resolution, token_human_escalation_roles
- `logistics_warehousing`: entity_splitting, fake_qlc_inflation, offshore_ai_services, related_party_ai_service_fees, sector_classification_arbitrage, token_human_oversight_jobs
- `retail_self_checkout_fulfilment`: customer_labour_relabelling, fulfilment_entity_splitting, robotics_leasing_relabelling, underreported_automated_transaction_share
- `software_digital_platforms`: cloud_inference_relabelling, low_declared_australian_profit, offshore_ip_platform_royalties, open_source_ai_unresolved, related_party_model_access_fees

## J. Calibration Data Requirements

### accounting_administration
- ABS and ATO data separating accounting, bookkeeping, payroll, administration, and professional-services activities.
- Professional-services and administration workforce wage and output data.
- Fair Work award, classification, and job-security data for clerical and accounting-support roles.
- Accounting platform transaction volumes, workflow automation adoption, and document-processing data.
- HILDA, DSS, and labour-market transition data for displaced administrative and accounting-support workers.
- Legal and tax review of professional judgement, advice, audit, and lodgement boundaries.

### automotive_repair
- ATO small-business and company tax data by automotive repair ANZSIC class.
- ABS labour force and output measures for repair and maintenance.
- Fair Work occupational classifications, wage distributions, and casualisation measures.
- HILDA income-transition and wage-scarring data for displaced mechanics and apprentices.
- DSS transfer-system data and HELP repayment loss assumptions.
- Workshop robotics and AI diagnostic adoption data from industry surveys.

### call_centres_customer_support
- ABS and industry customer-service workforce and output data.
- ATO aggregated tax data for customer support and contact-centre entities.
- CRM/ticketing benchmark data for resolved support cases per qualified FTE.
- Fair Work wage, award, casualisation, and job-security data for support workers.
- AI agent, chatbot, and automated triage adoption data from industry surveys.
- DSS, HILDA, and labour-market transition data for displaced customer support workers.

### logistics_warehousing
- ATO, ABS, and industry data separating freight, last-mile delivery, warehousing, and platform dispatch.
- State payroll tax exposure and regional employment concentration.
- HILDA and DSS data on driver, picker, packer, dispatcher, and warehouse transition outcomes.
- Autonomous vehicle kilometres, automated dispatch share, and warehouse robotics adoption data.
- Transfer pricing, diverted profits tax, and significant global entity interaction analysis.

### retail_self_checkout_fulfilment
- ABS, ATO, and industry data separating store retail, online retail, fulfilment, and marketplace activities.
- POS, self-checkout, fulfilment, and inventory automation benchmark data.
- Fair Work retail, warehouse, and fulfilment wage and employment data.
- State payroll tax and regional employment data for retail and fulfilment sites.
- HILDA, DSS, and labour-market transition data for displaced retail and fulfilment workers.
- Legal review of customer self-service, contractor labour, platform retail, and fulfilment attribution.

### software_digital_platforms
- ABS, ATO, and industry data separating software, platform, marketplace, digital services, and AI workflow activities.
- Platform transaction, workflow, recommendation, matching, and automated decision volume data.
- Cloud, inference, model, and data-access cost data with Australian-facing attribution.
- Fair Work and labour-market data for Australian software, moderation, support, and operations workforces.
- HILDA, DSS, and labour-market transition data for displaced administrative, platform, support, and digital-service workers.
- AASB 138, tax counsel, Treasury, and ATO review of intangible assets, capital base, IP royalties, and Australian value attribution.

## K. Multi-Schedule Blending Status

Additional prototype schedules improve demonstration coverage, but they do not implement real multi-schedule legal attribution. True multi-schedule blending still requires calibrated sector schedules, legal attribution rules, evidence standards, and Schedules Authority review.

## L. Limitations and Future Review Needs

- Values are prototype placeholders only.
- No real sector, ABS, ATO, DSS, PBO, Treasury, or industry calibration data has been added.
- OPFTE, FRV, caps, safe-harbour thresholds, and measurement controls are not validated.
- Software / digital platform capital-base treatment remains unresolved and subject to AASB 138, tax counsel, and Treasury review.
- Firm-level CARSF liability logic is not modified.
