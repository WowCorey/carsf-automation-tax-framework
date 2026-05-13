"""Credit and AAVA cap helpers."""

from __future__ import annotations


def positive_aava(aava: float) -> float:
    """Return the non-negative AAVA base used for caps."""

    return max(0.0, float(aava))


def cap_by_aava(amount: float, cap_rate: float, aava: float) -> float:
    """Cap an amount by a schedule-defined share of non-negative AAVA."""

    if amount < 0:
        raise ValueError("amount cannot be negative")
    if cap_rate < 0:
        raise ValueError("cap_rate cannot be negative")
    return min(amount, cap_rate * positive_aava(aava))


def capped_credits(verified_credits: float, theta: float, ael_payable: float, arl: float) -> float:
    """Credits = min(VerifiedCredits, theta * (AEL_payable + ARL))."""

    if verified_credits < 0:
        raise ValueError("verified_credits cannot be negative")
    if not 0 <= theta <= 1:
        raise ValueError("theta must be in [0, 1]")
    if ael_payable < 0 or arl < 0:
        raise ValueError("liability components cannot be negative")
    return min(verified_credits, theta * (ael_payable + arl))
