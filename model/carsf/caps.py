"""Credit and AAVA cap helpers."""

from __future__ import annotations

from math import isfinite


def _finite_number(value: float, field_name: str) -> float:
    numeric = float(value)
    if not isfinite(numeric):
        raise ValueError(f"{field_name} must be finite")
    return numeric


def positive_aava(aava: float) -> float:
    """Return the non-negative AAVA base used for caps."""

    numeric = _finite_number(aava, "aava")
    return max(0.0, numeric)


def cap_by_aava(amount: float, cap_rate: float, aava: float) -> float:
    """Cap an amount by a schedule-defined share of non-negative AAVA."""

    amount = _finite_number(amount, "amount")
    cap_rate = _finite_number(cap_rate, "cap_rate")
    if amount < 0:
        raise ValueError("amount cannot be negative")
    if not isfinite(amount) or not isfinite(cap_rate):
        raise ValueError("amount and cap_rate must be finite")
    if not 0 <= cap_rate <= 1:
        raise ValueError("cap_rate must be in [0, 1]")
    return min(amount, cap_rate * positive_aava(aava))


def capped_credits(verified_credits: float, theta: float, ael_payable: float, arl: float) -> float:
    """Credits = min(VerifiedCredits, theta * (AEL_payable + ARL))."""

    verified_credits = _finite_number(verified_credits, "verified_credits")
    theta = _finite_number(theta, "theta")
    ael_payable = _finite_number(ael_payable, "ael_payable")
    arl = _finite_number(arl, "arl")
    if verified_credits < 0:
        raise ValueError("verified_credits cannot be negative")
    if not 0 <= theta <= 1:
        raise ValueError("theta must be in [0, 1]")
    if ael_payable < 0 or arl < 0:
        raise ValueError("liability components cannot be negative")
    return min(verified_credits, theta * (ael_payable + arl))
