from __future__ import annotations

import yaml
import pytest

from carsf.fiscal_trajectory import run_fiscal_trajectory


def _load(repo_root, name: str) -> dict:
    return yaml.safe_load((repo_root / "examples" / "fiscal_trajectory" / f"{name}.yaml").read_text(encoding="utf-8"))


def test_fiscal_trajectory_runs_all_fiscal_examples(repo_root) -> None:
    paths = sorted((repo_root / "examples" / "fiscal_trajectory").glob("*.yaml"))
    assert len(paths) >= 5

    for path in paths:
        example = yaml.safe_load(path.read_text(encoding="utf-8"))
        result = run_fiscal_trajectory(example)
        assert result.years
        assert result.non_claims
        assert result.cumulative_total_public_sector_gap >= 0


def test_fiscal_trajectory_coverage_ratio_is_none_when_denominator_zero() -> None:
    example = {
        "trajectory_id": "zero_denominator",
        "workforce": {
            "start_year": 2026,
            "end_year": 2026,
            "baseline_employed_workers": 100,
            "annual_displacement_rate": 0.0,
            "annual_reabsorption_rate": 0.0,
            "labour_force_growth_rate": 0.0,
            "average_taxable_income": 0,
            "average_payg_tax_per_worker": 0,
            "average_super_contribution_per_worker": 0,
            "average_help_repayment_per_worker": 0,
        },
        "average_support_payment_per_person": 0,
        "transition_support_share": 0,
        "retraining_support_share": 0,
        "administrative_cost_per_person": 0,
        "automation_revenue_captured_by_year": {2026: 0},
    }
    result = run_fiscal_trajectory(example)

    assert result.years[0].coverage_ratio is None
    assert result.years[0].warning_band == "not_assessable"


def test_fiscal_trajectory_coverage_ratio_calculates_when_denominator_positive(repo_root) -> None:
    example = _load(repo_root, "baseline_placeholder_2026_2034")
    result = run_fiscal_trajectory(example)
    first = result.years[0]

    assert first.coverage_ratio == first.automation_revenue_captured / (
        first.payg_revenue_loss + first.transfer_pressure
    )


def test_high_displacement_produces_higher_gap_than_low_displacement(repo_root) -> None:
    high = run_fiscal_trajectory(_load(repo_root, "high_displacement_low_reabsorption"))
    low = run_fiscal_trajectory(_load(repo_root, "low_displacement_high_reabsorption"))

    assert high.cumulative_total_public_sector_gap > low.cumulative_total_public_sector_gap


def test_weak_capture_produces_higher_residual_gap_than_stronger_capture(repo_root) -> None:
    weak = run_fiscal_trajectory(_load(repo_root, "weak_automation_revenue_capture"))
    strong = run_fiscal_trajectory(_load(repo_root, "stronger_automation_revenue_capture"))

    assert weak.cumulative_commonwealth_gap_after_carsf > strong.cumulative_commonwealth_gap_after_carsf


def test_first_warning_years_are_deterministic(repo_root) -> None:
    example = _load(repo_root, "high_displacement_low_reabsorption")
    first = run_fiscal_trajectory(example)
    second = run_fiscal_trajectory(example)

    assert first.first_high_warning_year == second.first_high_warning_year
    assert first.first_critical_warning_year == second.first_critical_warning_year


def test_fiscal_trajectory_tracks_super_as_retirement_pressure_not_commonwealth_revenue(repo_root) -> None:
    example = _load(repo_root, "baseline_placeholder_2026_2034")
    with_super = run_fiscal_trajectory(example)
    no_super_example = dict(example)
    no_super_example["workforce"] = dict(example["workforce"], average_super_contribution_per_worker=0)
    without_super = run_fiscal_trajectory(no_super_example)

    assert with_super.cumulative_commonwealth_gap_after_carsf == without_super.cumulative_commonwealth_gap_after_carsf
    assert with_super.cumulative_total_public_sector_gap == without_super.cumulative_total_public_sector_gap
    assert with_super.cumulative_retirement_contribution_pressure > 0
    assert with_super.cumulative_broader_labour_linked_pressure > without_super.cumulative_broader_labour_linked_pressure


@pytest.mark.parametrize("field", ["company_tax_change_by_year", "gst_consumption_change_by_year", "other_revenue_change_by_year"])
def test_negative_revenue_changes_fail_without_explicit_gain_flag(repo_root, field: str) -> None:
    example = _load(repo_root, "baseline_placeholder_2026_2034")
    example[field] = {2026: -1}

    with pytest.raises(ValueError, match="cannot be negative"):
        run_fiscal_trajectory(example)


@pytest.mark.parametrize("field", ["company_tax_change_by_year", "gst_consumption_change_by_year", "other_revenue_change_by_year"])
def test_negative_revenue_changes_allowed_with_explicit_gain_flag(repo_root, field: str) -> None:
    example = _load(repo_root, "baseline_placeholder_2026_2034")
    base = run_fiscal_trajectory(example)
    gain_example = dict(example)
    gain_example["allow_revenue_gains"] = True
    gain_example[field] = dict(example[field])
    gain_example[field][2026] = -1000000
    gain = run_fiscal_trajectory(gain_example)

    assert gain.cumulative_commonwealth_gap_after_carsf < base.cumulative_commonwealth_gap_after_carsf


def test_negative_state_or_automation_values_still_fail_when_gain_flag_set(repo_root) -> None:
    example = _load(repo_root, "baseline_placeholder_2026_2034")
    example["allow_revenue_gains"] = True
    example["automation_revenue_captured_by_year"] = {2026: -1}

    with pytest.raises(ValueError, match="cannot be negative"):
        run_fiscal_trajectory(example)
