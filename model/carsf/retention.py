"""Prototype retention and access-control policy helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


RETENTION_NON_CLAIMS = [
    "This is prototype retention/access-control documentation only.",
    "It is not real IAM, legal, privacy, cybersecurity, evidentiary, forensic, Treasury, ATO, tax, or audit enforcement.",
]


@dataclass(frozen=True)
class RetentionPolicy:
    policy_id: str
    evidence_mode: str
    storage_zone: str
    retention_action: str
    retention_period: str
    deletion_required: bool
    reason: str
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(RETENTION_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AccessControlPolicy:
    policy_id: str
    allowed_roles: list[str]
    denied_roles: list[str]
    approval_required: bool
    notes: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(RETENTION_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def get_retention_policy(evidence_mode: str, storage_zone: str) -> RetentionPolicy:
    zone = str(storage_zone).replace("\\", "/")
    if evidence_mode == "synthetic_mock" and zone.rstrip("/") == "data/mock_evidence":
        return RetentionPolicy(
            policy_id="retain-synthetic-mock-evidence",
            evidence_mode=evidence_mode,
            storage_zone=storage_zone,
            retention_action="retain_in_repo",
            retention_period="repository lifecycle",
            deletion_required=False,
            reason="Synthetic mock evidence is allowed in the repo for workflow tests.",
            warnings=["Confirm fixtures remain synthetic and contain no real evidence before commit."],
        )
    return RetentionPolicy(
        policy_id="deny-real-evidence-retention",
        evidence_mode=evidence_mode,
        storage_zone=storage_zone,
        retention_action="deny_repo_retention",
        retention_period="none",
        deletion_required=True,
        reason="Real or non-approved evidence must not be retained in this repository.",
        warnings=["Use an external secure system design for any non-synthetic evidence."],
    )


def get_access_control_policy(evidence_mode: str, sensitivity: str) -> AccessControlPolicy:
    high = sensitivity in {"high", "restricted_placeholder"}
    if evidence_mode != "synthetic_mock":
        return AccessControlPolicy(
            policy_id="external-secure-access-required",
            allowed_roles=[],
            denied_roles=["repo_reader", "repo_writer", "public_viewer", "prototype_user"],
            approval_required=True,
            notes=["Non-synthetic evidence requires external secure access-control design."],
        )
    return AccessControlPolicy(
        policy_id="synthetic-mock-access-review" if high else "synthetic-mock-repo-access",
        allowed_roles=["prototype_maintainer", "policy_reviewer"],
        denied_roles=["public_viewer"],
        approval_required=high,
        notes=[
            "Synthetic mock evidence only.",
            "High-sensitivity mock scenarios require review before external sharing." if high else "No real IAM enforcement is implemented.",
        ],
    )
