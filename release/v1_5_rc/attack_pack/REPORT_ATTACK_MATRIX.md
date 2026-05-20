# Report Attack Matrix

This attack document does not mean external review has been completed, does not mean approval has been granted, and does not mean validation has occurred. It is not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not economic validation, not welfare validation, not statistical validation, not compliance scoring, not enforcement, and does not modify firm-level CARSF liability.

## Method

The generated attack-pack report builds the report-by-report matrix from the V1.5 release manifest. Each row should be attacked for overread risk, stale paths, missing blockers, missing non-claims, and missing external review inputs.

## Required Checks

- Report path exists.
- Report runner exists and is in CI where required.
- Report has non-claim language.
- Report says what it must not be used for.
- Report links to calibration or external-review blockers.

## Build 26 Addition

`reports/real_data_feasibility.md` and `reports/real_data_feasibility.json` are attack targets for the real-data feasibility and calibration-intake map. Attack them for public-source overread, restricted-data boundary failure, realistic-placeholder labelling failure, forbidden repo data gaps, and any wording that could imply real data was loaded or calibration occurred.

## Build 27 Addition

`reports/public_data_pilot.md`, `reports/public_data_pilot.json`, and `data/public_pilot/digests/public_data_pilot_digests.json` are attack targets for the public aggregate-data pilot. Attack them for source provenance gaps, source-reference-only counting errors, realistic-placeholder labelling failure, digest self-hash or drift, restricted-data boundary failure, and any wording that could imply completed calibration, model proof, actual tax payable, validation, approval, official status, or firm-level liability modification.

`reports/public_data_evidence_map.md` and `reports/public_data_evidence_map.json` are attack targets for the reviewer evidence map. Attack them for Build 28 new-data leakage, source-reference-only records counted as loaded data, loaded extract rows without source locators or value-review status, missing Fair Work arithmetic representation, ATO/Treasury/Super overread, placeholder anchors labelled as real data, module sanity checks implying calibration, and any wording that could imply completed calibration, model proof, tax-payable use, validation, approval, official status, ATO guidance, Treasury modelling, PBO costing, or firm-level liability modification.

`reports/public_data_consistency_audit.md` and `reports/public_data_consistency_audit.json` are attack targets for internal reconciliation overread. Attack them for source-reference-only counts being treated as loaded data, missing loaded-extract source metadata, stale digest metadata, missing Fair Work arithmetic reconciliation, dashboard/report disagreement, and any wording that could imply external source verification, completed calibration, model proof, tax-payable use, validation, approval, official status, ATO guidance, Treasury modelling, PBO costing, or firm-level liability modification.

## What Not To Infer

The matrix is not validation, not approval, not a readiness metric, and not government endorsement.
