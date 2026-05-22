# Public Aggregate Calibration Boundary Map

Build 33 defines how loaded public aggregate values may be used across the CARSF V1.5 prototype. It uses Build 31 public aggregate values and Build 32 placeholder replacement decisions only.

Generated reports:

- `reports/public_aggregate_calibration_boundary_map.md`
- `reports/public_aggregate_calibration_boundary_map.json`

The map separates allowed uses from forbidden uses. Allowed uses are limited to sanity checks, public aggregate anchors, public aggregate bounds, contextual references, placeholder narrowing, and reviewer traceability.

This is a calibration-boundary map only. No new data is loaded. Public aggregate data does not calibrate the model, calibration has not been completed, public data does not prove the model works, boundary mapping does not mean validation, and boundary mapping does not mean statistical estimation, legal sufficiency, implementation readiness, official status, or actual tax payable.

Source candidates not loaded remain not loaded. Restricted-data blockers remain blockers. The map is not legal advice, tax advice, ATO guidance, Treasury modelling, PBO costing, economic validation, welfare validation, statistical validation, operational readiness, legal sufficiency, or official status, and it does not modify firm-level CARSF liability.

The report section titled “Modules Requiring External Review” lists modules that need external review before calibration claims could be considered. It does not imply every boundary-limited use is fully blocked.
Build 34 uses this boundary map to constrain scenario outputs. Public aggregate values can appear in scenario-facing outputs only as sanity checks, anchors, bounds, context, placeholder narrowing, or reviewer traceability. Outputs that would imply calibration, validation, tax payable, firm liability, legal sufficiency, official status, statistical estimation, economic validation, welfare validation, or implementation readiness are marked non-interpretable, hidden, downgraded, or fail-closed.

Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-34 are included in a later sealed RC.
