from __future__ import annotations

from carsf.mixed_units import evaluate_mixed_unit_exposure, evaluate_unit_compatibility


def entity(entity_id: str, unit: str, liability: float = 0.0, revenue: float = 100.0, risk_level: str = "low") -> dict:
    return {
        "entity_id": entity_id,
        "schedule_id": "test_schedule",
        "canonical_output_unit": unit,
        "liability": liability,
        "revenue": revenue,
        "aava": revenue / 2,
        "risk_level": risk_level,
    }


def test_unit_compatibility_true_when_units_match() -> None:
    result = evaluate_unit_compatibility(
        [
            entity("a", "tonne_kilometres_or_pallet_movements"),
            entity("b", "tonne_kilometres_or_pallet_movements"),
        ]
    )

    assert result.compatible is True
    assert result.comparable_unit == "tonne_kilometres_or_pallet_movements"


def test_unit_compatibility_false_when_units_differ() -> None:
    result = evaluate_unit_compatibility(
        [
            entity("a", "tonne_kilometres_or_pallet_movements"),
            entity("b", "book_hour_equivalent_jobs_completed"),
        ]
    )

    assert result.compatible is False
    assert result.review_required is True
    assert "direct output/HLE aggregation is prohibited" in result.reason


def test_mixed_unit_handling_prohibits_direct_hle_and_output_aggregation() -> None:
    result = evaluate_mixed_unit_exposure(
        [
            entity("a", "tonne_kilometres_or_pallet_movements"),
            entity("b", "book_hour_equivalent_jobs_completed"),
        ]
    )

    assert result.method == "mixed_units_no_direct_output_or_hle_aggregation"
    assert any("direct output/HLE aggregation is not" in warning for warning in result.warnings)


def test_mixed_unit_exposure_sums_standalone_liabilities() -> None:
    result = evaluate_mixed_unit_exposure(
        [
            entity("a", "tonne_kilometres_or_pallet_movements", liability=100.0),
            entity("b", "book_hour_equivalent_jobs_completed", liability=25.0),
        ]
    )

    assert result.standalone_liability_sum == 125.0


def test_value_weighted_exposure_index_is_labelled_non_tax_base() -> None:
    result = evaluate_mixed_unit_exposure(
        [
            entity("a", "tonne_kilometres_or_pallet_movements", revenue=100.0, risk_level="low"),
            entity("b", "book_hour_equivalent_jobs_completed", revenue=300.0, risk_level="high"),
        ]
    )
    combined = " ".join(result.warnings + result.non_claims).lower()

    assert result.value_weighted_exposure_index is not None
    assert "not a tax base" in combined
    assert "prototype-only" in combined
