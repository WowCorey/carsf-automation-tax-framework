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

## What Not To Infer

The matrix is not validation, not approval, not a readiness metric, and not government endorsement.
