"""Australian Automated Value Added formula."""

from __future__ import annotations


def australian_automated_value_added(
    australian_attributable_revenue: float,
    verified_non_automation_input_costs: float,
    verified_qlc_wage_cost: float,
) -> float:
    """Calculate AAVA.

    AAVA = AustralianAttributableRevenue
           - VerifiedNonAutomationInputCosts
           - VerifiedQLC_WageCost

    The deductibility schedule is not final. Callers should separately retain
    evidence labels for confirmed baseline figures, illustrative assumptions,
    placeholder values, and future research requirements.
    """

    if australian_attributable_revenue < 0:
        raise ValueError("australian_attributable_revenue cannot be negative")
    if verified_non_automation_input_costs < 0:
        raise ValueError("verified_non_automation_input_costs cannot be negative")
    if verified_qlc_wage_cost < 0:
        raise ValueError("verified_qlc_wage_cost cannot be negative")
    return (
        australian_attributable_revenue
        - verified_non_automation_input_costs
        - verified_qlc_wage_cost
    )
