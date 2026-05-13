"""Labour-Intensity Benchmark Cohort helpers."""

from __future__ import annotations


def output_per_fte_benchmark(canonical_output_libc: float, qlc_libc: float) -> float:
    """OPFTE_LIBC = CanonicalOutput_LIBC / QLC_LIBC."""

    if canonical_output_libc < 0:
        raise ValueError("canonical_output_libc cannot be negative")
    if qlc_libc <= 0:
        raise ValueError("qlc_libc must be positive")
    return canonical_output_libc / qlc_libc


def apply_libc_guardrails(
    proposed_opfte: float,
    previous_opfte: float,
    ratchet: float,
    productivity_indexed_floor: float,
) -> float:
    """Apply V1.4's asymmetric ratchet and productivity-indexed floor."""

    if previous_opfte <= 0:
        raise ValueError("previous_opfte must be positive")
    if ratchet < 0:
        raise ValueError("ratchet cannot be negative")
    if productivity_indexed_floor < 0:
        raise ValueError("productivity_indexed_floor cannot be negative")
    ratcheted = min(proposed_opfte, previous_opfte * (1.0 + ratchet))
    return max(ratcheted, productivity_indexed_floor)


def human_labour_equivalent(output_firm: float, opfte_libc: float) -> float:
    """HLE = Output_firm / OPFTE_LIBC."""

    if output_firm < 0:
        raise ValueError("output_firm cannot be negative")
    if opfte_libc <= 0:
        raise ValueError("opfte_libc must be positive")
    return output_firm / opfte_libc
