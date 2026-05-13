from __future__ import annotations

import yaml

from carsf.fiscal_trajectory import run_fiscal_trajectory
from carsf.transition_funding import run_transition_funding


RISK_ORDER = {"not_assessable": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}


def _load_transition_example(repo_root, name: str) -> dict:
    return yaml.safe_load((repo_root / "examples" / "transition_payments" / f"{name}.yaml").read_text(encoding="utf-8"))


def _load_fiscal(repo_root, name: str) -> dict:
    return yaml.safe_load((repo_root / "examples" / "fiscal_trajectory" / f"{name}.yaml").read_text(encoding="utf-8"))


def _funding_from_example(repo_root, example_name: str):
    example = _load_transition_example(repo_root, example_name)
    fiscal = run_fiscal_trajectory(_load_fiscal(repo_root, example["fiscal_trajectory_example"]))
    return run_transition_funding(
        {
            "funding_id": example["example_id"],
            "fiscal_trajectory": fiscal.to_jsonable(),
            "payment_designs_by_year": {0: example["payment_designs"]},
            "population_base_by_year": {0: example["population_base"]},
        }
    )


def test_transition_funding_consumes_fiscal_trajectory_outputs(repo_root) -> None:
    result = _funding_from_example(repo_root, "displaced_worker_supplement_placeholder")

    assert result.years
    assert result.years[0].net_displaced_workers > 0
    assert result.years[0].automation_revenue_captured > 0


def test_high_displacement_payment_stress_has_higher_cliff_risk_than_low_stress_design(repo_root) -> None:
    high = _funding_from_example(repo_root, "high_displacement_payment_stress")
    low = _funding_from_example(repo_root, "transition_income_retraining_placeholder")
    high_peak = max(RISK_ORDER[year.cliff_risk_band] for year in high.years)
    low_peak = max(RISK_ORDER[year.cliff_risk_band] for year in low.years)

    assert high_peak > low_peak


def test_transition_funding_does_not_modify_firm_level_liability(repo_root) -> None:
    result = _funding_from_example(repo_root, "displaced_worker_supplement_placeholder")

    assert result.non_claims
    assert all("liability" in claim.lower() for claim in [result.non_claims[-1]])
