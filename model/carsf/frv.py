"""Fiscal Replacement Value related helpers."""

from __future__ import annotations


def net_labour_tax_gap(hle: float, aii: float, qlc: float) -> float:
    """NLTG = max(0, (HLE * AII) - QLC)."""

    if hle < 0:
        raise ValueError("hle cannot be negative")
    if qlc < 0:
        raise ValueError("qlc cannot be negative")
    bounded_aii = max(0.0, min(1.0, float(aii)))
    return max(0.0, (hle * bounded_aii) - qlc)
