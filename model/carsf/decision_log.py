"""Deterministic decision-log helpers for CARSF prototype runs."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any


DECISION_LOG_NON_CLAIMS = [
    "Decision logs are prototype audit trails only.",
    "Decision logs do not create legal findings, tax findings, Treasury guidance, ATO guidance, or economic validation.",
    "Decision logs must not contain raw sensitive identifiers or personal records.",
]
FORBIDDEN_MARKERS = ["password", "api_key", "personal_data", "tax_file_number", "tfn"]


@dataclass(frozen=True)
class DecisionLogEntry:
    step_id: str
    step_name: str
    input_summary: dict[str, Any]
    output_summary: dict[str, Any]
    decision: str
    reasons: list[str] = field(default_factory=list)
    evidence_status: str = "placeholder_only"
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(DECISION_LOG_NON_CLAIMS))


@dataclass
class DecisionLog:
    run_id: str
    example_id: str
    generated_at: str
    entries: list[DecisionLogEntry] = field(default_factory=list)
    final_warnings: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)


def create_decision_log(example_id: str) -> DecisionLog:
    """Create a deterministic log shell, except for generated_at."""

    safe_id = str(example_id).replace(" ", "_").lower()
    return DecisionLog(
        run_id=f"carsf-v1.5-{safe_id}",
        example_id=str(example_id),
        generated_at=datetime.now(UTC).replace(microsecond=0).isoformat(),
        final_warnings=[
            "Prototype decision log only.",
            "No legal, tax, Treasury, ATO, audit, forensic, or economic validation is implied.",
        ],
        limitations=[
            "Inputs are illustrative placeholders unless separately verified.",
            "Decision entries record model flow and review signals only.",
        ],
    )


def _assert_no_forbidden_markers(payload: Any) -> None:
    text = str(payload).lower()
    for marker in FORBIDDEN_MARKERS:
        if marker in text:
            raise ValueError(f"decision log payload contains forbidden marker: {marker}")


def add_decision_entry(
    log: DecisionLog,
    step_id: str,
    step_name: str,
    input_summary: dict[str, Any],
    output_summary: dict[str, Any],
    decision: str,
    reasons: list[str] | None = None,
    evidence_status: str = "placeholder_only",
    warnings: list[str] | None = None,
    non_claims: list[str] | None = None,
) -> DecisionLog:
    entry = DecisionLogEntry(
        step_id=str(step_id),
        step_name=str(step_name),
        input_summary=input_summary,
        output_summary=output_summary,
        decision=str(decision),
        reasons=reasons or [],
        evidence_status=str(evidence_status),
        warnings=warnings or [],
        non_claims=non_claims or list(DECISION_LOG_NON_CLAIMS),
    )
    _assert_no_forbidden_markers(asdict(entry))
    log.entries.append(entry)
    return log


def summarise_decision_log(log: DecisionLog) -> dict[str, Any]:
    payload = {
        "run_id": log.run_id,
        "example_id": log.example_id,
        "generated_at": log.generated_at,
        "entry_count": len(log.entries),
        "steps": [entry.step_id for entry in log.entries],
        "decisions": {entry.step_id: entry.decision for entry in log.entries},
        "evidence_status_by_step": {entry.step_id: entry.evidence_status for entry in log.entries},
        "warnings": list(log.final_warnings),
        "limitations": list(log.limitations),
        "non_claims": list(DECISION_LOG_NON_CLAIMS),
    }
    _assert_no_forbidden_markers(payload)
    return payload


def build_standard_decision_log(
    example_id: str,
    evidence_status: str,
    step_outputs: dict[str, Any],
    extra_steps: list[tuple[str, str, dict[str, Any], dict[str, Any], str]] | None = None,
) -> DecisionLog:
    """Build a compact standard decision log for example/report outputs."""

    log = create_decision_log(example_id)
    add_decision_entry(
        log,
        "evidence_assessment",
        "Evidence assessment",
        {"example_id": example_id},
        {"status": evidence_status},
        "Evidence reviewed as prototype-only input governance.",
        evidence_status=evidence_status,
    )
    for step_id, step_name, inputs, outputs, decision in extra_steps or []:
        add_decision_entry(
            log,
            step_id,
            step_name,
            inputs,
            outputs,
            decision,
            evidence_status=evidence_status,
        )
    for step_id in (
        "qlc",
        "hle",
        "aii",
        "nltg",
        "aava",
        "ael",
        "arl",
        "caps",
        "safe_harbour",
        "avoidance",
        "grouping",
    ):
        if step_id in step_outputs:
            add_decision_entry(
                log,
                step_id,
                step_id.upper().replace("_", " "),
                {"source": "model pipeline"},
                {"value": step_outputs[step_id]},
                f"Recorded {step_id} prototype model step.",
                evidence_status=evidence_status,
            )
    return log
