# Public Aggregate Scenario Constraint Layer

Build 34 adds a public aggregate scenario constraint layer over the Build 33 calibration-boundary map. It uses existing Build 31 public aggregate values and Build 32 placeholder replacement decisions only.

This is a scenario constraint layer only. No new data is loaded. Scenario constraints do not calibrate the model, do not validate the model, and do not determine actual tax payable. Public aggregate data can appear only as sanity checks, public aggregate anchors, public aggregate bounds, context, placeholder narrowing, or reviewer traceability.

Outputs that would imply calibration, validation, tax payable, firm liability, official status, legal sufficiency, statistical estimation, economic validation, welfare validation, or implementation readiness are marked non-interpretable, hidden, downgraded, or fail-closed.

The generated reports are:

- `reports/public_aggregate_scenario_constraint_layer.md`
- `reports/public_aggregate_scenario_constraint_layer.json`

The Streamlit public-data evidence page can show the scenario constraint summary, module constraints, field constraints, outputs marked non-interpretable, outputs hidden from reviewer dashboards, forbidden implications, and evidence needed to lift constraints.

This is not validation, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not economic validation, not welfare validation, not statistical validation, not operational readiness, not legal sufficiency, and not official status. It does not modify firm-level CARSF liability.

Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-34 are included in a later sealed RC.

## Build 34.5 Follow-On Audit

Build 34.5 adds a full repo integrity upgrade and gap audit over this scenario constraint layer and the wider CARSF V1.5 repository. It checks report, runner, dashboard, manifest, non-claim, public-data boundary, placeholder boundary, calibration boundary, and scenario-constraint coverage without loading new data.

The follow-on audit is not calibration, not validation, not legal advice, not tax advice, not ATO guidance, not Treasury modelling, not PBO costing, not operational readiness, not legal sufficiency, not official status, and does not determine actual tax payable or modify firm-level CARSF liability. Build 25 sealed the earlier RC state. A new integrity seal must be regenerated if Builds 26-34.5 are included in a later sealed RC.
