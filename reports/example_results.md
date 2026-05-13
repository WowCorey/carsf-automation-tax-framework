# CARSF V1.5 Worked Example Results

Generated at: `2026-05-13T08:32:02+00:00`

Version: CARSF V1.5 prototype

Status: `illustrative_placeholder_outputs_only`

These outputs are illustrative placeholders only. They are not legal, tax, Treasury, ATO, economic, or real liability calculations.

## Summary Comparison

| Example | Sector | QLC | HLE | AII | NLTG | AAVA | AEL Payable | ARL | Final Liability | Main Interpretation |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Mechanic Traditional | automotive_repair | 5.88 | 4.67 | 0.02 | 0.00 | 70,000.00 | 0.00 | 0.00 | 0.00 | Traditional mechanic shop: high human labour contribution and low automation intensity produce low or zero NLTG. This illustrative case should not be treated as automation-heavy. |
| Mechanic Ai Admin | automotive_repair | 4.85 | 5.33 | 0.11 | 0.00 | 170,000.00 | 0.00 | 0.00 | 0.00 | AI-admin mechanic shop: AI is mainly supporting booking, compliance, customer support, and diagnostics while humans still perform core repair work. The low NLTG relative to the robotic shop illustrates the distinction between worker-assist/admin AI and labour-substituting robotics. |
| Mechanic Robotic | automotive_repair | 1.73 | 8.00 | 0.81 | 4.74 | 880,000.00 | 158,400.00 | 0.00 | 148,400.00 | Fully robotic mechanic shop: high automation intensity and low QLC relative to output create a materially higher NLTG than the traditional shop. The result is a stronger liability or recorded shortfall signal in this prototype. |
| Logistics Human Heavy | logistics_warehousing | 11.10 | 9.00 | 0.05 | 0.00 | 150,000.00 | 0.00 | 0.00 | 0.00 | Human-heavy logistics company: a larger human workforce and lower automation intensity produce lower NLTG than the automated logistics examples. |
| Logistics Hybrid | logistics_warehousing | 11.10 | 20.00 | 0.27 | 0.00 | 800,000.00 | 0.00 | 0.00 | 0.00 | Hybrid logistics company: AII is intermediate, but NLTG and liability remain zero under the current placeholders because QLC remains strong. This demonstrates that hybrid automation is not automatically penalised. A later stress variant should test non-zero but intermediate NLTG. |
| Logistics Ai Platform | logistics_warehousing | 3.32 | 40.00 | 0.73 | 25.96 | 3,840,000.00 | 768,000.00 | 204,160.00 | 922,160.00 | AI logistics platform: high automated productive capacity and low QLC relative to output create the strongest stress case among the six examples. |

The comparison should be read directionally only: AI-admin repair is not treated like robotic repair, robotic repair is higher-risk than traditional repair, and the AI logistics platform is higher-risk than hybrid logistics under these placeholders.

## Safe Harbour and Review Flags

These are prototype review flags, not legal findings. Safe harbour classification does not reduce or erase liability in this build.

| Example | Safe Harbour Category | Avoidance Risk | Grouping Risk | Review Required | Main Reason |
| --- | --- | --- | --- | --- | --- |
| Mechanic Traditional | SMALL_BUSINESS_PLACEHOLDER | low | low | no | Revenue is below the schedule placeholder small-business threshold. |
| Mechanic Ai Admin | WORKER_ASSIST_OR_ADMIN_AI | low | low | no | Metadata identifies worker-assist/admin AI rather than labour-substituting automation. |
| Mechanic Robotic | NO_SAFE_HARBOUR_REVIEW | medium | low | yes | High-risk avoidance metadata or red-team flags require review before any safe harbour. |
| Logistics Human Heavy | SMALL_BUSINESS_PLACEHOLDER | low | low | no | Revenue is below the schedule placeholder small-business threshold. |
| Logistics Hybrid | SMALL_BUSINESS_PLACEHOLDER | low | low | no | Revenue is below the schedule placeholder small-business threshold. |
| Logistics Ai Platform | NO_SAFE_HARBOUR_REVIEW | high | high | yes | High-risk avoidance metadata or red-team flags require review before any safe harbour. |

## Evidence and Decision-Log Summary

Evidence assessments are prototype-only and do not validate liability, legal positions, tax positions, or audit findings.

| Example | Evidence Status | Missing Requirements | Decision-Log Entries | Review Required |
| --- | --- | ---: | ---: | --- |
| Mechanic Traditional | placeholder_only | 33 | 12 | true |
| Mechanic Ai Admin | placeholder_only | 33 | 12 | true |
| Mechanic Robotic | placeholder_only | 33 | 12 | true |
| Logistics Human Heavy | placeholder_only | 33 | 12 | true |
| Logistics Hybrid | placeholder_only | 33 | 12 | true |
| Logistics Ai Platform | placeholder_only | 33 | 12 | true |

## Mechanic Traditional

### A. Business Description

Traditional suburban automotive repair workshop with human mechanics and low automation.

### B. Key Input Assumptions

- Output: 4,200.00 book_hour_equivalent_jobs_completed
- Workers: 5
- Automation components: compute=0.03, auto_decision=0.02, robotics_capital=0.01, auto_process=0.03
- AAVA inputs: revenue=850,000.00, non_automation_costs=420,000.00, qlc_wage_cost=360,000.00
- Capital base: 180,000.00
- Verified credits: 15,000.00
- Caps: lambda=0.18, LAMBDA=0.25, theta=0.6

### C. Formula Trace

- QLC = sum capped worker QLC = 5.8791
- OPFTE_LIBC = schedule placeholder benchmark = 900.0000
- HLE = output / OPFTE_LIBC = 4.6667
- AII = weighted bounded automation components = 0.0205
- NLTG = max(0, HLE * AII - QLC) = 0.0000
- AAVA = revenue - non-automation costs - QLC wage costs = 70000.00
- AEL raw = NLTG * FRV standard = 0.00
- AEL payable = min(AEL raw, lambda_sector * AAVA) = 0.00
- Shortfall = AEL raw - AEL payable = 0.00
- ARL = PRRT-inspired uplift logic result = 0.00
- Credits = capped verified credits = 0.00
- Final liability = capped combined liability = 0.00

### D. Calculated Output Table

| Output | Value |
| --- | ---: |
| QLC | 5.8791 |
| OPFTE_LIBC | 900.0000 |
| HLE | 4.6667 |
| AII | 0.0205 |
| NLTG | 0.0000 |
| AAVA | 70,000.00 |
| AEL raw | 0.00 |
| AEL payable | 0.00 |
| AEL shortfall | 0.00 |
| ARL | 0.00 |
| Credits | 0.00 |
| Final liability (placeholder) | 0.00 |
| CARS-I | N/A |
| CoverageRatio | N/A - no national monitoring inputs |

### E. Plain-English Interpretation

Traditional mechanic shop: high human labour contribution and low automation intensity produce low or zero NLTG. This illustrative case should not be treated as automation-heavy.

### F. Red-Team / Limitation Notes

**Warnings**

- Illustrative placeholder output only.
- Do not use this result to estimate real tax payable.
- No legal, tax, Treasury, ATO, or economic validation is implied.
- Safe harbour and avoidance outputs are prototype review flags, not legal findings.
- Coverage metrics not calculated because this example has no national monitoring inputs.

**Evidence labels**

- `example.status=illustrative_placeholder`
- `example.placeholder_notice=Numbers are illustrative placeholders and are not Australian industry data.`
- `schedule.status=placeholder_prototype_for_v1_5`
- `schedule.calibration_status=illustrative_placeholder_values_only`
- `schedule.opfte_libc.evidence_label=illustrative_placeholder`
- `schedule.frv.evidence_label=illustrative_placeholder`

**Limitations**

- Numbers are illustrative placeholders and are not Australian industry data.
- Schedule values are not calibrated.
- AAVA deductibility remains a prototype taxonomy.
- Safe harbour, anti-avoidance, and grouping checks are executable review flags only.
- Safe harbour classification does not automatically reduce or erase liability in this build.
- Related-party, offshore, and sector-classification outputs are not legal or tax conclusions.

**Red-team notes**

- Flags: none
- Serves as the human-heavy comparator.

### G. Safe Harbour Assessment

- Eligible: true
- Category: SMALL_BUSINESS_PLACEHOLDER
- Review required: false
- Reasons:
  - Revenue is below the schedule placeholder small-business threshold.
  - No high-risk avoidance metadata is present.
  - NLTG is zero or near-zero and human labour remains substantial.
- Warnings:
  - Prototype classification only; not legal advice, tax advice, Treasury guidance, or ATO guidance.
  - This result does not constitute legal validation of any actual safe harbour.
- Placeholder basis:
  - Prototype safe-harbour checks use illustrative placeholder thresholds only.
  - low_nltg_threshold_placeholder=0.25
  - substantial_human_labour_qlc_hle_ratio_placeholder=0.35
  - small_business_revenue_threshold_placeholder=10000000.0
  - Safe-harbour classification does not alter liability in this build.

### H. Avoidance / Gaming Risk Assessment

- Risk level: low
- Flags: none
- Reasons:
  - No executable prototype avoidance flags were triggered.
- Recommended review:
  - Prototype review flags only; no legal, tax, Treasury, or ATO validation is provided.
- Placeholder basis:
  - Avoidance checks are prototype heuristics only.
  - Thresholds are illustrative placeholders and not calibrated enforcement rules.
  - No result constitutes legal, tax, Treasury, or ATO validation.

### I. Grouped-Entity Review Flag

- Risk level: low
- Flags: none
- Reasons:
  - No grouped-entity review flags were triggered.
- Recommended review:
  - Prototype grouping review only; this is not legal grouping analysis or tax-law validation.
- Placeholder basis:
  - Grouping checks are prototype review flags only.
  - No full legal grouping, transfer-pricing, or attribution rule is implemented.

### J. Evidence and Decision Log

- Evidence status: placeholder_only
- Missing evidence requirements: 33
- Decision-log entries: 12
- Decision-log steps: evidence_assessment, qlc, hle, aii, nltg, aava, ael, arl, caps, safe_harbour, avoidance, grouping
- Evidence assessment is prototype-only and does not validate any liability, legal position, tax position, or audit finding.
- Evidence remains insufficient for real calibration, legal use, or actual tax-payable claims.

## Mechanic Ai Admin

### A. Business Description

Human workshop using AI for booking, invoicing, reminders, and diagnostic support with mechanics still doing repair work.

### B. Key Input Assumptions

- Output: 4,800.00 book_hour_equivalent_jobs_completed
- Workers: 4
- Automation components: compute=0.12, auto_decision=0.18, robotics_capital=0.02, auto_process=0.16
- AAVA inputs: revenue=940,000.00, non_automation_costs=440,000.00, qlc_wage_cost=330,000.00
- Capital base: 220,000.00
- Verified credits: 22,000.00
- Caps: lambda=0.18, LAMBDA=0.25, theta=0.6

### C. Formula Trace

- QLC = sum capped worker QLC = 4.8489
- OPFTE_LIBC = schedule placeholder benchmark = 900.0000
- HLE = output / OPFTE_LIBC = 5.3333
- AII = weighted bounded automation components = 0.1100
- NLTG = max(0, HLE * AII - QLC) = 0.0000
- AAVA = revenue - non-automation costs - QLC wage costs = 170000.00
- AEL raw = NLTG * FRV standard = 0.00
- AEL payable = min(AEL raw, lambda_sector * AAVA) = 0.00
- Shortfall = AEL raw - AEL payable = 0.00
- ARL = PRRT-inspired uplift logic result = 0.00
- Credits = capped verified credits = 0.00
- Final liability = capped combined liability = 0.00

### D. Calculated Output Table

| Output | Value |
| --- | ---: |
| QLC | 4.8489 |
| OPFTE_LIBC | 900.0000 |
| HLE | 5.3333 |
| AII | 0.1100 |
| NLTG | 0.0000 |
| AAVA | 170,000.00 |
| AEL raw | 0.00 |
| AEL payable | 0.00 |
| AEL shortfall | 0.00 |
| ARL | 0.00 |
| Credits | 0.00 |
| Final liability (placeholder) | 0.00 |
| CARS-I | N/A |
| CoverageRatio | N/A - no national monitoring inputs |

### E. Plain-English Interpretation

AI-admin mechanic shop: AI is mainly supporting booking, compliance, customer support, and diagnostics while humans still perform core repair work. The low NLTG relative to the robotic shop illustrates the distinction between worker-assist/admin AI and labour-substituting robotics.

### F. Red-Team / Limitation Notes

**Warnings**

- Illustrative placeholder output only.
- Do not use this result to estimate real tax payable.
- No legal, tax, Treasury, ATO, or economic validation is implied.
- Safe harbour and avoidance outputs are prototype review flags, not legal findings.
- Coverage metrics not calculated because this example has no national monitoring inputs.

**Evidence labels**

- `example.status=illustrative_placeholder`
- `example.placeholder_notice=Numbers are illustrative placeholders and are not Australian industry data.`
- `schedule.status=placeholder_prototype_for_v1_5`
- `schedule.calibration_status=illustrative_placeholder_values_only`
- `schedule.opfte_libc.evidence_label=illustrative_placeholder`
- `schedule.frv.evidence_label=illustrative_placeholder`

**Limitations**

- Numbers are illustrative placeholders and are not Australian industry data.
- Schedule values are not calibrated.
- AAVA deductibility remains a prototype taxonomy.
- Safe harbour, anti-avoidance, and grouping checks are executable review flags only.
- Safe harbour classification does not automatically reduce or erase liability in this build.
- Related-party, offshore, and sector-classification outputs are not legal or tax conclusions.

**Red-team notes**

- Flags: none
- Tests the worker-assist concession boundary.

### G. Safe Harbour Assessment

- Eligible: true
- Category: WORKER_ASSIST_OR_ADMIN_AI
- Review required: false
- Reasons:
  - Metadata identifies worker-assist/admin AI rather than labour-substituting automation.
  - QLC remains substantial relative to HLE under placeholder rules.
  - NLTG is zero or near-zero under placeholder rules.
- Warnings:
  - Prototype classification only; not legal advice, tax advice, Treasury guidance, or ATO guidance.
  - This result does not constitute legal validation of any actual safe harbour.
- Placeholder basis:
  - Prototype safe-harbour checks use illustrative placeholder thresholds only.
  - low_nltg_threshold_placeholder=0.25
  - substantial_human_labour_qlc_hle_ratio_placeholder=0.35
  - small_business_revenue_threshold_placeholder=10000000.0
  - Safe-harbour classification does not alter liability in this build.

### H. Avoidance / Gaming Risk Assessment

- Risk level: low
- Flags: none
- Reasons:
  - No executable prototype avoidance flags were triggered.
- Recommended review:
  - Prototype review flags only; no legal, tax, Treasury, or ATO validation is provided.
- Placeholder basis:
  - Avoidance checks are prototype heuristics only.
  - Thresholds are illustrative placeholders and not calibrated enforcement rules.
  - No result constitutes legal, tax, Treasury, or ATO validation.

### I. Grouped-Entity Review Flag

- Risk level: low
- Flags: none
- Reasons:
  - No grouped-entity review flags were triggered.
- Recommended review:
  - Prototype grouping review only; this is not legal grouping analysis or tax-law validation.
- Placeholder basis:
  - Grouping checks are prototype review flags only.
  - No full legal grouping, transfer-pricing, or attribution rule is implemented.

### J. Evidence and Decision Log

- Evidence status: placeholder_only
- Missing evidence requirements: 33
- Decision-log entries: 12
- Decision-log steps: evidence_assessment, qlc, hle, aii, nltg, aava, ael, arl, caps, safe_harbour, avoidance, grouping
- Evidence assessment is prototype-only and does not validate any liability, legal position, tax position, or audit finding.
- Evidence remains insufficient for real calibration, legal use, or actual tax-payable claims.

## Mechanic Robotic

### A. Business Description

Highly automated repair facility using robotic inspection, automated quoting, and limited human supervision.

### B. Key Input Assumptions

- Output: 7,200.00 book_hour_equivalent_jobs_completed
- Workers: 2
- Automation components: compute=0.58, auto_decision=0.78, robotics_capital=0.92, auto_process=0.82
- AAVA inputs: revenue=1,550,000.00, non_automation_costs=520,000.00, qlc_wage_cost=150,000.00
- Capital base: 900,000.00
- Verified credits: 10,000.00
- Caps: lambda=0.18, LAMBDA=0.25, theta=0.6

### C. Formula Trace

- QLC = sum capped worker QLC = 1.7308
- OPFTE_LIBC = schedule placeholder benchmark = 900.0000
- HLE = output / OPFTE_LIBC = 8.0000
- AII = weighted bounded automation components = 0.8090
- NLTG = max(0, HLE * AII - QLC) = 4.7412
- AAVA = revenue - non-automation costs - QLC wage costs = 880000.00
- AEL raw = NLTG * FRV standard = 213355.38
- AEL payable = min(AEL raw, lambda_sector * AAVA) = 158400.00
- Shortfall = AEL raw - AEL payable = 54955.38
- ARL = PRRT-inspired uplift logic result = 0.00
- Credits = capped verified credits = 10000.00
- Final liability = capped combined liability = 148400.00

### D. Calculated Output Table

| Output | Value |
| --- | ---: |
| QLC | 1.7308 |
| OPFTE_LIBC | 900.0000 |
| HLE | 8.0000 |
| AII | 0.8090 |
| NLTG | 4.7412 |
| AAVA | 880,000.00 |
| AEL raw | 213,355.38 |
| AEL payable | 158,400.00 |
| AEL shortfall | 54,955.38 |
| ARL | 0.00 |
| Credits | 10,000.00 |
| Final liability (placeholder) | 148,400.00 |
| CARS-I | N/A |
| CoverageRatio | N/A - no national monitoring inputs |

### E. Plain-English Interpretation

Fully robotic mechanic shop: high automation intensity and low QLC relative to output create a materially higher NLTG than the traditional shop. The result is a stronger liability or recorded shortfall signal in this prototype.

### F. Red-Team / Limitation Notes

**Warnings**

- Illustrative placeholder output only.
- Do not use this result to estimate real tax payable.
- No legal, tax, Treasury, ATO, or economic validation is implied.
- Safe harbour and avoidance outputs are prototype review flags, not legal findings.
- Coverage metrics not calculated because this example has no national monitoring inputs.

**Evidence labels**

- `example.status=illustrative_placeholder`
- `example.placeholder_notice=Numbers are illustrative placeholders and are not Australian industry data.`
- `schedule.status=placeholder_prototype_for_v1_5`
- `schedule.calibration_status=illustrative_placeholder_values_only`
- `schedule.opfte_libc.evidence_label=illustrative_placeholder`
- `schedule.frv.evidence_label=illustrative_placeholder`

**Limitations**

- Numbers are illustrative placeholders and are not Australian industry data.
- Schedule values are not calibrated.
- AAVA deductibility remains a prototype taxonomy.
- Safe harbour, anti-avoidance, and grouping checks are executable review flags only.
- Safe harbour classification does not automatically reduce or erase liability in this build.
- Related-party, offshore, and sector-classification outputs are not legal or tax conclusions.

**Red-team notes**

- Flags: token_human_oversight_jobs, fake_qlc_inflation
- Tests whether nominal supervision roles are enough to suppress NLTG.

### G. Safe Harbour Assessment

- Eligible: false
- Category: NO_SAFE_HARBOUR_REVIEW
- Review required: true
- Reasons:
  - High-risk avoidance metadata or red-team flags require review before any safe harbour.
- Warnings:
  - Prototype classification only; not legal advice, tax advice, Treasury guidance, or ATO guidance.
  - This result does not constitute legal validation of any actual safe harbour.
- Placeholder basis:
  - Prototype safe-harbour checks use illustrative placeholder thresholds only.
  - low_nltg_threshold_placeholder=0.25
  - substantial_human_labour_qlc_hle_ratio_placeholder=0.35
  - small_business_revenue_threshold_placeholder=10000000.0
  - Safe-harbour classification does not alter liability in this build.

### H. Avoidance / Gaming Risk Assessment

- Risk level: medium
- Flags: TOKEN_HUMAN_OVERSIGHT, FAKE_QLC_INFLATION
- Reasons:
  - High automation with low QLC/HLE and a small workforce may indicate nominal human oversight.
  - QLC scoring may be inflated or concentrated in too few roles relative to automated output.
- Recommended review:
  - Prototype review flags only; no legal, tax, Treasury, or ATO validation is provided.
  - Review whether human roles are substantive, verified, and appropriately scored for QLC.
  - Review payroll, hours, wage quality, security, training, and Australian nexus evidence.
- Placeholder basis:
  - Avoidance checks are prototype heuristics only.
  - Thresholds are illustrative placeholders and not calibrated enforcement rules.
  - No result constitutes legal, tax, Treasury, or ATO validation.

### I. Grouped-Entity Review Flag

- Risk level: low
- Flags: none
- Reasons:
  - No grouped-entity review flags were triggered.
- Recommended review:
  - Prototype grouping review only; this is not legal grouping analysis or tax-law validation.
- Placeholder basis:
  - Grouping checks are prototype review flags only.
  - No full legal grouping, transfer-pricing, or attribution rule is implemented.

### J. Evidence and Decision Log

- Evidence status: placeholder_only
- Missing evidence requirements: 33
- Decision-log entries: 12
- Decision-log steps: evidence_assessment, qlc, hle, aii, nltg, aava, ael, arl, caps, safe_harbour, avoidance, grouping
- Evidence assessment is prototype-only and does not validate any liability, legal position, tax position, or audit finding.
- Evidence remains insufficient for real calibration, legal use, or actual tax-payable claims.

## Logistics Human Heavy

### A. Business Description

Human-heavy logistics operator with drivers, dispatchers, and warehouse workers.

### B. Key Input Assumptions

- Output: 900,000.00 tonne_kilometres_or_pallet_movements
- Workers: 9
- Automation components: compute=0.05, auto_decision=0.05, robotics_capital=0.02, auto_process=0.06
- AAVA inputs: revenue=2,100,000.00, non_automation_costs=1,300,000.00, qlc_wage_cost=650,000.00
- Capital base: 600,000.00
- Verified credits: 30,000.00
- Caps: lambda=0.2, LAMBDA=0.27, theta=0.6

### C. Formula Trace

- QLC = sum capped worker QLC = 11.0989
- OPFTE_LIBC = schedule placeholder benchmark = 100000.0000
- HLE = output / OPFTE_LIBC = 9.0000
- AII = weighted bounded automation components = 0.0470
- NLTG = max(0, HLE * AII - QLC) = 0.0000
- AAVA = revenue - non-automation costs - QLC wage costs = 150000.00
- AEL raw = NLTG * FRV standard = 0.00
- AEL payable = min(AEL raw, lambda_sector * AAVA) = 0.00
- Shortfall = AEL raw - AEL payable = 0.00
- ARL = PRRT-inspired uplift logic result = 0.00
- Credits = capped verified credits = 0.00
- Final liability = capped combined liability = 0.00

### D. Calculated Output Table

| Output | Value |
| --- | ---: |
| QLC | 11.0989 |
| OPFTE_LIBC | 100,000.0000 |
| HLE | 9.0000 |
| AII | 0.0470 |
| NLTG | 0.0000 |
| AAVA | 150,000.00 |
| AEL raw | 0.00 |
| AEL payable | 0.00 |
| AEL shortfall | 0.00 |
| ARL | 0.00 |
| Credits | 0.00 |
| Final liability (placeholder) | 0.00 |
| CARS-I | N/A |
| CoverageRatio | N/A - no national monitoring inputs |

### E. Plain-English Interpretation

Human-heavy logistics company: a larger human workforce and lower automation intensity produce lower NLTG than the automated logistics examples.

### F. Red-Team / Limitation Notes

**Warnings**

- Illustrative placeholder output only.
- Do not use this result to estimate real tax payable.
- No legal, tax, Treasury, ATO, or economic validation is implied.
- Safe harbour and avoidance outputs are prototype review flags, not legal findings.
- Coverage metrics not calculated because this example has no national monitoring inputs.

**Evidence labels**

- `example.status=illustrative_placeholder`
- `example.placeholder_notice=Numbers are illustrative placeholders and are not Australian logistics data.`
- `schedule.status=placeholder_prototype_for_v1_5`
- `schedule.calibration_status=illustrative_placeholder_values_only`
- `schedule.opfte_libc.evidence_label=illustrative_placeholder`
- `schedule.frv.evidence_label=illustrative_placeholder`

**Limitations**

- Numbers are illustrative placeholders and are not Australian logistics data.
- Schedule values are not calibrated.
- AAVA deductibility remains a prototype taxonomy.
- Safe harbour, anti-avoidance, and grouping checks are executable review flags only.
- Safe harbour classification does not automatically reduce or erase liability in this build.
- Related-party, offshore, and sector-classification outputs are not legal or tax conclusions.

**Red-team notes**

- Flags: none
- Human-heavy comparator for logistics schedule.

### G. Safe Harbour Assessment

- Eligible: true
- Category: SMALL_BUSINESS_PLACEHOLDER
- Review required: false
- Reasons:
  - Revenue is below the schedule placeholder small-business threshold.
  - No high-risk avoidance metadata is present.
  - NLTG is zero or near-zero and human labour remains substantial.
- Warnings:
  - Prototype classification only; not legal advice, tax advice, Treasury guidance, or ATO guidance.
  - This result does not constitute legal validation of any actual safe harbour.
- Placeholder basis:
  - Prototype safe-harbour checks use illustrative placeholder thresholds only.
  - low_nltg_threshold_placeholder=0.25
  - substantial_human_labour_qlc_hle_ratio_placeholder=0.35
  - small_business_revenue_threshold_placeholder=10000000.0
  - Safe-harbour classification does not alter liability in this build.

### H. Avoidance / Gaming Risk Assessment

- Risk level: low
- Flags: none
- Reasons:
  - No executable prototype avoidance flags were triggered.
- Recommended review:
  - Prototype review flags only; no legal, tax, Treasury, or ATO validation is provided.
- Placeholder basis:
  - Avoidance checks are prototype heuristics only.
  - Thresholds are illustrative placeholders and not calibrated enforcement rules.
  - No result constitutes legal, tax, Treasury, or ATO validation.

### I. Grouped-Entity Review Flag

- Risk level: low
- Flags: none
- Reasons:
  - No grouped-entity review flags were triggered.
- Recommended review:
  - Prototype grouping review only; this is not legal grouping analysis or tax-law validation.
- Placeholder basis:
  - Grouping checks are prototype review flags only.
  - No full legal grouping, transfer-pricing, or attribution rule is implemented.

### J. Evidence and Decision Log

- Evidence status: placeholder_only
- Missing evidence requirements: 33
- Decision-log entries: 12
- Decision-log steps: evidence_assessment, qlc, hle, aii, nltg, aava, ael, arl, caps, safe_harbour, avoidance, grouping
- Evidence assessment is prototype-only and does not validate any liability, legal position, tax position, or audit finding.
- Evidence remains insufficient for real calibration, legal use, or actual tax-payable claims.

## Logistics Hybrid

### A. Business Description

Logistics operator using route optimisation and warehouse scanning while retaining substantial human driving and warehouse labour.

### B. Key Input Assumptions

- Output: 2,000,000.00 tonne_kilometres_or_pallet_movements
- Workers: 9
- Automation components: compute=0.22, auto_decision=0.35, robotics_capital=0.18, auto_process=0.28
- AAVA inputs: revenue=4,200,000.00, non_automation_costs=2,500,000.00, qlc_wage_cost=900,000.00
- Capital base: 1,600,000.00
- Verified credits: 65,000.00
- Caps: lambda=0.2, LAMBDA=0.27, theta=0.6

### C. Formula Trace

- QLC = sum capped worker QLC = 11.0989
- OPFTE_LIBC = schedule placeholder benchmark = 100000.0000
- HLE = output / OPFTE_LIBC = 20.0000
- AII = weighted bounded automation components = 0.2690
- NLTG = max(0, HLE * AII - QLC) = 0.0000
- AAVA = revenue - non-automation costs - QLC wage costs = 800000.00
- AEL raw = NLTG * FRV standard = 0.00
- AEL payable = min(AEL raw, lambda_sector * AAVA) = 0.00
- Shortfall = AEL raw - AEL payable = 0.00
- ARL = PRRT-inspired uplift logic result = 0.00
- Credits = capped verified credits = 0.00
- Final liability = capped combined liability = 0.00

### D. Calculated Output Table

| Output | Value |
| --- | ---: |
| QLC | 11.0989 |
| OPFTE_LIBC | 100,000.0000 |
| HLE | 20.0000 |
| AII | 0.2690 |
| NLTG | 0.0000 |
| AAVA | 800,000.00 |
| AEL raw | 0.00 |
| AEL payable | 0.00 |
| AEL shortfall | 0.00 |
| ARL | 0.00 |
| Credits | 0.00 |
| Final liability (placeholder) | 0.00 |
| CARS-I | N/A |
| CoverageRatio | N/A - no national monitoring inputs |

### E. Plain-English Interpretation

Hybrid logistics company: AII is intermediate, but NLTG and liability remain zero under the current placeholders because QLC remains strong. This demonstrates that hybrid automation is not automatically penalised. A later stress variant should test non-zero but intermediate NLTG.

### F. Red-Team / Limitation Notes

**Warnings**

- Illustrative placeholder output only.
- Do not use this result to estimate real tax payable.
- No legal, tax, Treasury, ATO, or economic validation is implied.
- Safe harbour and avoidance outputs are prototype review flags, not legal findings.
- Coverage metrics not calculated because this example has no national monitoring inputs.

**Evidence labels**

- `example.status=illustrative_placeholder`
- `example.placeholder_notice=Numbers are illustrative placeholders and are not Australian logistics data.`
- `schedule.status=placeholder_prototype_for_v1_5`
- `schedule.calibration_status=illustrative_placeholder_values_only`
- `schedule.opfte_libc.evidence_label=illustrative_placeholder`
- `schedule.frv.evidence_label=illustrative_placeholder`

**Limitations**

- Numbers are illustrative placeholders and are not Australian logistics data.
- Schedule values are not calibrated.
- AAVA deductibility remains a prototype taxonomy.
- Safe harbour, anti-avoidance, and grouping checks are executable review flags only.
- Safe harbour classification does not automatically reduce or erase liability in this build.
- Related-party, offshore, and sector-classification outputs are not legal or tax conclusions.

**Red-team notes**

- Flags: none
- Tests useful productivity where QLC remains substantial.

### G. Safe Harbour Assessment

- Eligible: true
- Category: SMALL_BUSINESS_PLACEHOLDER
- Review required: false
- Reasons:
  - Revenue is below the schedule placeholder small-business threshold.
  - No high-risk avoidance metadata is present.
  - NLTG is zero or near-zero and human labour remains substantial.
- Warnings:
  - Prototype classification only; not legal advice, tax advice, Treasury guidance, or ATO guidance.
  - This result does not constitute legal validation of any actual safe harbour.
- Placeholder basis:
  - Prototype safe-harbour checks use illustrative placeholder thresholds only.
  - low_nltg_threshold_placeholder=0.25
  - substantial_human_labour_qlc_hle_ratio_placeholder=0.35
  - small_business_revenue_threshold_placeholder=10000000.0
  - Safe-harbour classification does not alter liability in this build.

### H. Avoidance / Gaming Risk Assessment

- Risk level: low
- Flags: none
- Reasons:
  - No executable prototype avoidance flags were triggered.
- Recommended review:
  - Prototype review flags only; no legal, tax, Treasury, or ATO validation is provided.
- Placeholder basis:
  - Avoidance checks are prototype heuristics only.
  - Thresholds are illustrative placeholders and not calibrated enforcement rules.
  - No result constitutes legal, tax, Treasury, or ATO validation.

### I. Grouped-Entity Review Flag

- Risk level: low
- Flags: none
- Reasons:
  - No grouped-entity review flags were triggered.
- Recommended review:
  - Prototype grouping review only; this is not legal grouping analysis or tax-law validation.
- Placeholder basis:
  - Grouping checks are prototype review flags only.
  - No full legal grouping, transfer-pricing, or attribution rule is implemented.

### J. Evidence and Decision Log

- Evidence status: placeholder_only
- Missing evidence requirements: 33
- Decision-log entries: 12
- Decision-log steps: evidence_assessment, qlc, hle, aii, nltg, aava, ael, arl, caps, safe_harbour, avoidance, grouping
- Evidence assessment is prototype-only and does not validate any liability, legal position, tax position, or audit finding.
- Evidence remains insufficient for real calibration, legal use, or actual tax-payable claims.

## Logistics Ai Platform

### A. Business Description

AI logistics platform using automated dispatch, offshore optimisation services, and contracted fulfilment with thin Australian QLC.

### B. Key Input Assumptions

- Output: 4,000,000.00 tonne_kilometres_or_pallet_movements
- Workers: 3
- Automation components: compute=0.7, auto_decision=0.88, robotics_capital=0.35, auto_process=0.86
- AAVA inputs: revenue=8,500,000.00, non_automation_costs=4,300,000.00, qlc_wage_cost=360,000.00
- Capital base: 2,600,000.00
- Verified credits: 50,000.00
- Caps: lambda=0.2, LAMBDA=0.27, theta=0.6

### C. Formula Trace

- QLC = sum capped worker QLC = 3.3242
- OPFTE_LIBC = schedule placeholder benchmark = 100000.0000
- HLE = output / OPFTE_LIBC = 40.0000
- AII = weighted bounded automation components = 0.7320
- NLTG = max(0, HLE * AII - QLC) = 25.9558
- AAVA = revenue - non-automation costs - QLC wage costs = 3840000.00
- AEL raw = NLTG * FRV standard = 1219923.74
- AEL payable = min(AEL raw, lambda_sector * AAVA) = 768000.00
- Shortfall = AEL raw - AEL payable = 451923.74
- ARL = PRRT-inspired uplift logic result = 204160.00
- Credits = capped verified credits = 50000.00
- Final liability = capped combined liability = 922160.00

### D. Calculated Output Table

| Output | Value |
| --- | ---: |
| QLC | 3.3242 |
| OPFTE_LIBC | 100,000.0000 |
| HLE | 40.0000 |
| AII | 0.7320 |
| NLTG | 25.9558 |
| AAVA | 3,840,000.00 |
| AEL raw | 1,219,923.74 |
| AEL payable | 768,000.00 |
| AEL shortfall | 451,923.74 |
| ARL | 204,160.00 |
| Credits | 50,000.00 |
| Final liability (placeholder) | 922,160.00 |
| CARS-I | N/A |
| CoverageRatio | N/A - no national monitoring inputs |

### E. Plain-English Interpretation

AI logistics platform: high automated productive capacity and low QLC relative to output create the strongest stress case among the six examples.

### F. Red-Team / Limitation Notes

**Warnings**

- Illustrative placeholder output only.
- Do not use this result to estimate real tax payable.
- No legal, tax, Treasury, ATO, or economic validation is implied.
- Safe harbour and avoidance outputs are prototype review flags, not legal findings.
- Coverage metrics not calculated because this example has no national monitoring inputs.

**Evidence labels**

- `example.status=illustrative_placeholder`
- `example.placeholder_notice=Numbers are illustrative placeholders and are not Australian logistics data.`
- `schedule.status=placeholder_prototype_for_v1_5`
- `schedule.calibration_status=illustrative_placeholder_values_only`
- `schedule.opfte_libc.evidence_label=illustrative_placeholder`
- `schedule.frv.evidence_label=illustrative_placeholder`

**Limitations**

- Numbers are illustrative placeholders and are not Australian logistics data.
- Schedule values are not calibrated.
- AAVA deductibility remains a prototype taxonomy.
- Safe harbour, anti-avoidance, and grouping checks are executable review flags only.
- Safe harbour classification does not automatically reduce or erase liability in this build.
- Related-party, offshore, and sector-classification outputs are not legal or tax conclusions.

**Red-team notes**

- Flags: entity_splitting_safe_harbour, offshore_automation_service, related_party_ai_service_fees, sector_classification_arbitrage
- Tests grouped-entity aggregation for safe-harbour avoidance.
- Tests destination and activity attribution for offshore automation services.

### G. Safe Harbour Assessment

- Eligible: false
- Category: NO_SAFE_HARBOUR_REVIEW
- Review required: true
- Reasons:
  - High-risk avoidance metadata or red-team flags require review before any safe harbour.
- Warnings:
  - Prototype classification only; not legal advice, tax advice, Treasury guidance, or ATO guidance.
  - This result does not constitute legal validation of any actual safe harbour.
- Placeholder basis:
  - Prototype safe-harbour checks use illustrative placeholder thresholds only.
  - low_nltg_threshold_placeholder=0.25
  - substantial_human_labour_qlc_hle_ratio_placeholder=0.35
  - small_business_revenue_threshold_placeholder=10000000.0
  - Safe-harbour classification does not alter liability in this build.

### H. Avoidance / Gaming Risk Assessment

- Risk level: high
- Flags: TOKEN_HUMAN_OVERSIGHT, FAKE_QLC_INFLATION, OFFSHORE_AUTOMATION_SERVICE, RELATED_PARTY_AI_SERVICE_FEES, ENTITY_SPLITTING, SECTOR_CLASSIFICATION_ARBITRAGE, CLOUD_COST_RELABELING
- Reasons:
  - High automation with low QLC/HLE and a small workforce may indicate nominal human oversight.
  - QLC scoring may be inflated or concentrated in too few roles relative to automated output.
  - Metadata or red-team notes identify offshore automation services serving Australian output.
  - Related-party AI service fees may reduce AAVA without arm's-length support.
  - Metadata or red-team notes indicate potential grouped-entity threshold avoidance.
  - Schedule choice may be material to liability or may not match Australian-facing activity.
  - AI cloud or inference costs may be relabelled as ordinary non-automation input costs.
- Recommended review:
  - Prototype review flags only; no legal, tax, Treasury, or ATO validation is provided.
  - Review whether human roles are substantive, verified, and appropriately scored for QLC.
  - Review payroll, hours, wage quality, security, training, and Australian nexus evidence.
  - Review destination/activity attribution and offshore automation-as-a-service contracts.
  - Review transfer-pricing support, service descriptions, and AAVA deductibility treatment.
  - Review related entities, output ownership, employment entity, IP owner, and platform owner.
  - Review dominant activity, schedule apportionment, and Schedules Authority classification.
  - Review cloud invoices, inference allocation, and AAVA deductibility taxonomy treatment.
- Placeholder basis:
  - Avoidance checks are prototype heuristics only.
  - Thresholds are illustrative placeholders and not calibrated enforcement rules.
  - No result constitutes legal, tax, Treasury, or ATO validation.

### I. Grouped-Entity Review Flag

- Risk level: high
- Flags: ENTITY_SPLITTING_SAFE_HARBOUR, RELATED_OPERATING_ENTITIES, SEPARATED_IP_PLATFORM_EMPLOYER, THIN_AUSTRALIAN_EMPLOYING_ENTITY
- Reasons:
  - Metadata or red-team notes indicate possible entity splitting to access safe harbours or thresholds.
  - Example metadata lists related operating entities relevant to the output or automation chain.
  - Metadata indicates separation of IP, platform, employer, or contractor entities.
  - Thin Australian QLC is paired with high automated Australian-facing output.
- Recommended review:
  - Prototype grouping review only; this is not legal grouping analysis or tax-law validation.
  - Review grouped turnover, output, employment, IP, platform, and contractor entities together.
  - Review whether related entities should be aggregated for schedule thresholds and output attribution.
  - Review whether the split suppresses QLC, hides automation, or shifts AAVA outside the measured firm.
  - Review whether automated productive capacity sits in another related entity or offshore service provider.
- Placeholder basis:
  - Grouping checks are prototype review flags only.
  - No full legal grouping, transfer-pricing, or attribution rule is implemented.

### J. Evidence and Decision Log

- Evidence status: placeholder_only
- Missing evidence requirements: 33
- Decision-log entries: 12
- Decision-log steps: evidence_assessment, qlc, hle, aii, nltg, aava, ael, arl, caps, safe_harbour, avoidance, grouping
- Evidence assessment is prototype-only and does not validate any liability, legal position, tax position, or audit finding.
- Evidence remains insufficient for real calibration, legal use, or actual tax-payable claims.
