from __future__ import annotations

from carsf.secure_ingestion import IngestionRequest, evaluate_ingestion_request, get_default_ingestion_policy


def request(**overrides) -> IngestionRequest:
    base = {
        "request_id": "unit_request",
        "evidence_mode": "synthetic_mock",
        "source_description": "Synthetic clean mock description.",
        "intended_use": "unit test",
        "storage_zone": "data/mock_evidence/",
        "synthetic_mock_evidence_only": True,
        "contains_personal_data": False,
        "contains_real_business_data": False,
        "contains_restricted_data": False,
        "contains_secrets": False,
        "declared_sensitivity": "low",
        "requested_by": "pytest",
        "metadata": {"synthetic_fixture_only": True},
    }
    return IngestionRequest(**{**base, **overrides})


def test_default_policy_denies_non_synthetic_evidence() -> None:
    decision = evaluate_ingestion_request(
        request(evidence_mode="external_real", synthetic_mock_evidence_only=False)
    )

    assert decision.allowed is False
    assert decision.decision == "DENY"
    assert "external_secure_system_design" in decision.required_approvals


def test_synthetic_mock_evidence_in_allowed_zone_can_be_allowed() -> None:
    decision = evaluate_ingestion_request(request())

    assert decision.allowed is True
    assert decision.decision == "ALLOW_SYNTHETIC_MOCK_ONLY"


def test_real_personal_data_flags_deny_ingestion() -> None:
    decision = evaluate_ingestion_request(request(contains_personal_data=True))

    assert decision.allowed is False
    assert "privacy_review" in decision.required_approvals


def test_real_business_record_flags_deny_ingestion() -> None:
    decision = evaluate_ingestion_request(request(contains_real_business_data=True))

    assert decision.allowed is False
    assert "legal_tax_review" in decision.required_approvals


def test_secret_markers_deny_ingestion() -> None:
    decision = evaluate_ingestion_request(
        request(source_description="Synthetic FAKE_API_KEY_MARKER", contains_secrets=True)
    )

    assert decision.allowed is False
    assert "security_review" in decision.required_approvals


def test_wrong_storage_zone_denies_ingestion() -> None:
    decision = evaluate_ingestion_request(request(storage_zone="reports/"))

    assert decision.allowed is False
    assert any("storage_zone" in reason for reason in decision.reasons)


def test_high_sensitivity_mock_requires_review() -> None:
    decision = evaluate_ingestion_request(request(declared_sensitivity="high"))

    assert decision.allowed is True
    assert decision.decision == "ALLOW_SYNTHETIC_MOCK_WITH_REVIEW"
    assert "privacy_review" in decision.required_approvals


def test_default_policy_is_default_deny() -> None:
    policy = get_default_ingestion_policy()

    assert policy.default_action == "DENY"
    assert policy.allowed_storage_zones == ["data/mock_evidence/"]
