from __future__ import annotations

from carsf.retention import get_access_control_policy, get_retention_policy


def test_retention_policy_denies_retaining_real_evidence_in_repo() -> None:
    policy = get_retention_policy("external_real", "data/mock_evidence/")

    assert policy.retention_action == "deny_repo_retention"
    assert policy.deletion_required is True


def test_retention_policy_allows_clean_synthetic_mock_zone() -> None:
    policy = get_retention_policy("synthetic_mock", "data/mock_evidence/")

    assert policy.retention_action == "retain_in_repo"
    assert policy.deletion_required is False


def test_access_policy_marks_high_sensitivity_as_approval_required() -> None:
    policy = get_access_control_policy("synthetic_mock", "high")

    assert policy.approval_required is True
    assert "public_viewer" in policy.denied_roles


def test_access_policy_routes_non_synthetic_to_external_controls() -> None:
    policy = get_access_control_policy("external_real", "moderate")

    assert policy.approval_required is True
    assert not policy.allowed_roles
