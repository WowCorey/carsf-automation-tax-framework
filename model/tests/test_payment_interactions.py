from __future__ import annotations

import yaml

from carsf.payment_interactions import evaluate_payment_interactions


def _interaction(**overrides):
    data = {
        "interaction_id": "interaction_test",
        "year": 2028,
        "baseline": {
            "baseline_id": "baseline",
            "eligible_population": 100,
            "average_existing_support_per_person": 1000,
            "existing_admin_cost_per_person": 100,
            "baseline_program_type": "placeholder",
            "illustrative_placeholder_only": True,
        },
        "target_population": {
            "total_population": 1000,
            "displaced_workers": 200,
            "reabsorbed_workers": 50,
            "retraining_participants": 100,
            "existing_support_recipients": 80,
            "counts_may_overlap": False,
            "criteria": {
                "criteria_id": "direct",
                "target_group": "direct displaced",
                "displaced_worker_required": True,
                "retraining_required": False,
                "income_test_placeholder": False,
                "household_test_placeholder": False,
                "recent_employment_link_required": True,
                "automation_displacement_link_required": True,
                "exclusion_rules": [],
                "illustrative_placeholder_only": True,
            },
        },
        "phase_rule": {
            "rule_id": "full",
            "phase_in_start_year": 2026,
            "phase_in_end_year": 2026,
            "phase_out_start_year": None,
            "phase_out_end_year": None,
            "minimum_payment_multiplier": 1.0,
            "maximum_payment_multiplier": 1.0,
            "taper_rate_placeholder": 0.0,
            "illustrative_placeholder_only": True,
        },
        "stack_components": [
            {
                "component_id": "supplement",
                "component_type": "SUPPLEMENT",
                "eligible_people": 150,
                "payment_per_person": 1000,
                "stack_priority": 1,
                "phase_multiplier": 1.0,
            }
        ],
        "support_incidence_assumption": {
            "household_spend_share": 0.7,
            "gst_recovery_rate_placeholder": 0.04,
            "hardship_offset_rate_placeholder": 0.1,
            "savings_or_debt_repayment_share": 0.2,
            "illustrative_placeholder_only": True,
        },
        "automation_revenue_available": 100000,
        "commonwealth_gap_after_carsf": 50000,
    }
    data.update(overrides)
    return data


def test_payment_interactions_keep_existing_baseline_separate_from_new_stack() -> None:
    result = evaluate_payment_interactions(_interaction())

    assert result.baseline_cost == 110000
    assert result.net_stack_cost == 150000
    assert result.baseline_cost != result.net_stack_cost


def test_payment_interactions_calculate_residual_and_combined_gap() -> None:
    result = evaluate_payment_interactions(_interaction())

    assert result.residual_support_gap == 50000
    assert result.combined_commonwealth_gap == 100000


def test_high_cliff_risk_case_has_higher_risk_than_targeted_case(repo_root) -> None:
    targeted = yaml.safe_load((repo_root / "examples/payment_interactions/displaced_worker_targeted_supplement.yaml").read_text())
    high = yaml.safe_load((repo_root / "examples/payment_interactions/high_cliff_risk_interaction_case.yaml").read_text())

    targeted_result = evaluate_payment_interactions(
        {
            "interaction_id": targeted["example_id"],
            "year": targeted["year"],
            "baseline": targeted["baseline"],
            "target_population": targeted["target_population"],
            "phase_rule": targeted["phase_rule"],
            "stack_components": targeted["stack_components"],
            "support_incidence_assumption": targeted["support_incidence_assumption"],
            "automation_revenue_available": targeted["automation_revenue_available"],
            "commonwealth_gap_after_carsf": targeted["commonwealth_gap_after_carsf"],
        }
    )
    high_result = evaluate_payment_interactions(
        {
            "interaction_id": high["example_id"],
            "year": high["year"],
            "baseline": high["baseline"],
            "target_population": high["target_population"],
            "phase_rule": high["phase_rule"],
            "stack_components": high["stack_components"],
            "support_incidence_assumption": high["support_incidence_assumption"],
            "automation_revenue_available": high["automation_revenue_available"],
            "commonwealth_gap_after_carsf": high["commonwealth_gap_after_carsf"],
        }
    )

    ordering = {"low": 0, "medium": 1, "high": 2, "critical": 3}
    assert ordering[high_result.interaction_risk_band] > ordering[targeted_result.interaction_risk_band]


def test_payment_interactions_do_not_modify_firm_level_liability() -> None:
    result = evaluate_payment_interactions(_interaction())

    assert any("do not modify firm-level CARSF liability" in item for item in result.non_claims)
