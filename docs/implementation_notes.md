# Implementation Notes

The Python model intentionally implements only concept-level formulas.

## Current Choices

- Inputs are validated for obvious negative values.
- Worker-level QLC scores and AII components are bounded in `[0, 1]`.
- AII weights must sum to 1.
- AAVA is calculated as specified, while caps use a non-negative AAVA base.
- ARL uses "PRRT-inspired uplift logic" and is not a full PRRT model.
- CoverageRatio is `None` when measured fiscal damage is zero, so UI can display `N/A - no measured damage` instead of implying 100% coverage.
- CARS-I uses epsilon to avoid divide-by-zero when captured revenue is zero.
- The end-to-end example runner uses the same formula modules as the simulator and writes illustrative reports to `reports/example_results.md` and `reports/example_results.json`.
- Safe-harbour classification is executable as a prototype review layer in `model/carsf/safe_harbour.py`.
- Anti-avoidance checks are executable prototype heuristics in `model/carsf/avoidance.py`.
- Grouping checks are executable review flags in `model/carsf/grouping.py`, not full legal grouping logic.
- Safe-harbour outputs do not modify AEL, ARL, credits, caps, or final liability.
- Risk flags are emitted into the example runner, Markdown reports, JSON reports, and Streamlit worked examples page.

## Not Implemented Yet

- Real schedule calibration.
- Safe-harbour rules that legally alter liability.
- Multi-schedule apportionment.
- Full grouped-entity aggregation.
- Related-party pricing adjustments.
- International tax treaty logic.
- Privacy-preserving disclosure schema.
- Behavioural elasticity and deadweight-loss modelling.
- Calibrated thresholds for safe-harbour, grouping, offshore attribution, and related-party review.

## Example Runner

Run from the repository root:

```powershell
python scripts/run_examples.py
```

Then view:

- `reports/example_results.md`
- `reports/example_results.json`

Run the simulator:

```powershell
python -m streamlit run simulator/app.py
```
