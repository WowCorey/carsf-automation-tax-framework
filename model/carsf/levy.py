"""Automation levy formulas."""

from __future__ import annotations

from .caps import cap_by_aava, capped_credits
from .types import LevyParameters, LevyResult


def automation_equilibrium_levy(
    nltg: float,
    frv_standard: float,
    lambda_sector: float,
    aava: float,
) -> tuple[float, float, float]:
    """Return AEL_raw, AEL_payable, and shortfall."""

    if nltg < 0:
        raise ValueError("nltg cannot be negative")
    if frv_standard < 0:
        raise ValueError("frv_standard cannot be negative")
    ael_raw = nltg * frv_standard
    ael_payable = cap_by_aava(ael_raw, lambda_sector, aava)
    shortfall = max(0.0, ael_raw - ael_payable)
    return ael_raw, ael_payable, shortfall


def automation_rent_levy(
    aava: float,
    uplift_rate: float,
    capital_base: float,
    rent_tax_rate: float,
) -> float:
    """ARL under PRRT-inspired uplift logic, not a full PRRT model."""

    if uplift_rate < 0:
        raise ValueError("uplift_rate cannot be negative")
    if capital_base < 0:
        raise ValueError("capital_base cannot be negative")
    if not 0 <= rent_tax_rate <= 1:
        raise ValueError("rent_tax_rate must be in [0, 1]")
    return max(0.0, aava - (uplift_rate * capital_base)) * rent_tax_rate


def calculate_liability(
    nltg: float,
    aava: float,
    capital_base: float,
    verified_credits: float,
    params: LevyParameters,
) -> LevyResult:
    """Calculate AEL, ARL, capped credits, combined cap, and final liability."""

    ael_raw, ael_payable, shortfall = automation_equilibrium_levy(
        nltg=nltg,
        frv_standard=params.frv_standard,
        lambda_sector=params.lambda_sector,
        aava=aava,
    )
    arl = automation_rent_levy(
        aava=aava,
        uplift_rate=params.uplift_rate,
        capital_base=capital_base,
        rent_tax_rate=params.rent_tax_rate,
    )
    credits = capped_credits(
        verified_credits=verified_credits,
        theta=params.theta,
        ael_payable=ael_payable,
        arl=arl,
    )
    combined_liability = max(0.0, ael_payable + arl - credits)
    liability = cap_by_aava(combined_liability, params.lambda_combined, aava)
    return LevyResult(
        ael_raw=ael_raw,
        ael_payable=ael_payable,
        shortfall=shortfall,
        arl=arl,
        credits=credits,
        combined_liability=combined_liability,
        liability=liability,
    )
