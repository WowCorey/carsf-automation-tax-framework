"""Automation levy formulas."""

from __future__ import annotations

from math import isfinite

from .caps import cap_by_aava, capped_credits
from .types import LevyParameters, LevyResult


def _finite_number(value: float, field_name: str) -> float:
    numeric = float(value)
    if not isfinite(numeric):
        raise ValueError(f"{field_name} must be finite")
    return numeric


def automation_equilibrium_levy(
    nltg: float,
    frv_standard: float,
    lambda_sector: float,
    aava: float,
) -> tuple[float, float, float]:
    """Return AEL_raw, AEL_payable, and shortfall."""

    nltg = _finite_number(nltg, "nltg")
    frv_standard = _finite_number(frv_standard, "frv_standard")
    aava = _finite_number(aava, "aava")
    if nltg < 0:
        raise ValueError("nltg cannot be negative")
    if frv_standard < 0:
        raise ValueError("frv_standard cannot be negative")
    ael_raw = _finite_number(nltg * frv_standard, "ael_raw")
    ael_payable = cap_by_aava(ael_raw, lambda_sector, aava)
    shortfall = _finite_number(max(0.0, ael_raw - ael_payable), "shortfall")
    return ael_raw, ael_payable, shortfall


def automation_rent_levy(
    aava: float,
    uplift_rate: float,
    capital_base: float,
    rent_tax_rate: float,
) -> float:
    """ARL under PRRT-inspired uplift logic, not a full PRRT model."""

    aava = _finite_number(aava, "aava")
    uplift_rate = _finite_number(uplift_rate, "uplift_rate")
    capital_base = _finite_number(capital_base, "capital_base")
    rent_tax_rate = _finite_number(rent_tax_rate, "rent_tax_rate")
    if uplift_rate < 0:
        raise ValueError("uplift_rate cannot be negative")
    if capital_base < 0:
        raise ValueError("capital_base cannot be negative")
    if not 0 <= rent_tax_rate <= 1:
        raise ValueError("rent_tax_rate must be in [0, 1]")
    uplifted_capital_base = _finite_number(
        uplift_rate * capital_base,
        "uplifted_capital_base",
    )
    arl_base = _finite_number(max(0.0, aava - uplifted_capital_base), "arl_base")
    return _finite_number(arl_base * rent_tax_rate, "arl")


def calculate_liability(
    nltg: float,
    aava: float,
    capital_base: float,
    verified_credits: float,
    params: LevyParameters,
) -> LevyResult:
    """Calculate AEL, ARL, capped credits, combined cap, and final liability."""

    nltg = _finite_number(nltg, "nltg")
    aava = _finite_number(aava, "aava")
    capital_base = _finite_number(capital_base, "capital_base")
    verified_credits = _finite_number(verified_credits, "verified_credits")
    _finite_number(params.frv_standard, "frv_standard")
    _finite_number(params.lambda_sector, "lambda_sector")
    _finite_number(params.lambda_combined, "lambda_combined")
    _finite_number(params.theta, "theta")
    _finite_number(params.uplift_rate, "uplift_rate")
    _finite_number(params.rent_tax_rate, "rent_tax_rate")
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
    combined_liability = _finite_number(
        max(0.0, ael_payable + arl - credits),
        "combined_liability",
    )
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
