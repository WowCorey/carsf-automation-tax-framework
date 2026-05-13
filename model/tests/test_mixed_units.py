from __future__ import annotations

from math import inf, isfinite, nan

import pytest

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


@pytest.mark.parametrize("value", [nan, inf, -inf])
def test_non_finite_liability_fails_closed(value: float) -> None:
    row = entity("a", "tonne_kilometres_or_pallet_movements", liability=value)

    with pytest.raises(ValueError, match="liability must be finite"):
        evaluate_mixed_unit_exposure([row])


@pytest.mark.parametrize("value", [nan, inf, -inf])
def test_non_finite_outputs_liability_fails_closed(value: float) -> None:
    row = entity("a", "tonne_kilometres_or_pallet_movements")
    row.pop("liability")
    row["outputs"] = {"liability": value}

    with pytest.raises(ValueError, match="outputs.liability must be finite"):
        evaluate_mixed_unit_exposure([row])


@pytest.mark.parametrize("field", ["revenue", "reported_revenue"])
@pytest.mark.parametrize("value", [nan, inf, -inf])
def test_non_finite_revenue_fields_fail_closed(field: str, value: float) -> None:
    row = entity("a", "tonne_kilometres_or_pallet_movements")
    row.pop("revenue")
    row[field] = value

    with pytest.raises(ValueError, match=f"{field} must be finite"):
        evaluate_mixed_unit_exposure([row])


@pytest.mark.parametrize("value", [nan, inf, -inf])
def test_non_finite_aava_fails_closed(value: float) -> None:
    row = entity("a", "tonne_kilometres_or_pallet_movements")
    row["aava"] = value

    with pytest.raises(ValueError, match="aava must be finite"):
        evaluate_mixed_unit_exposure([row])


@pytest.mark.parametrize("value", [nan, inf, -inf])
def test_non_finite_outputs_aava_fails_closed(value: float) -> None:
    row = entity("a", "tonne_kilometres_or_pallet_movements")
    row.pop("aava")
    row["outputs"] = {"aava": value}

    with pytest.raises(ValueError, match="outputs.aava must be finite"):
        evaluate_mixed_unit_exposure([row])


@pytest.mark.parametrize("value", [nan, inf, -inf])
def test_non_finite_risk_score_fails_closed(value: float) -> None:
    row = entity("a", "tonne_kilometres_or_pallet_movements")
    row["risk_score"] = value

    with pytest.raises(ValueError, match="risk_score must be finite"):
        evaluate_mixed_unit_exposure([row])


@pytest.mark.parametrize("value", [nan, inf, -inf])
def test_non_finite_outputs_aii_fails_closed(value: float) -> None:
    row = entity("a", "tonne_kilometres_or_pallet_movements")
    row.pop("risk_level")
    row["outputs"] = {"aii": value}

    with pytest.raises(ValueError, match="outputs.aii must be finite"):
        evaluate_mixed_unit_exposure([row])


def test_negative_liability_fails_closed() -> None:
    with pytest.raises(ValueError, match="liability cannot be negative"):
        evaluate_mixed_unit_exposure([entity("a", "tonne_kilometres_or_pallet_movements", liability=-0.01)])


def test_negative_revenue_fails_closed() -> None:
    with pytest.raises(ValueError, match="revenue cannot be negative"):
        evaluate_mixed_unit_exposure([entity("a", "tonne_kilometres_or_pallet_movements", revenue=-0.01)])


def test_negative_aava_without_metadata_fails_closed() -> None:
    row = entity("a", "tonne_kilometres_or_pallet_movements")
    row["aava"] = -0.01

    with pytest.raises(ValueError, match="aava cannot be negative"):
        evaluate_mixed_unit_exposure([row])


def test_negative_aava_with_metadata_is_excluded_from_weighting() -> None:
    row = entity("a", "tonne_kilometres_or_pallet_movements", revenue=0.0)
    row["aava"] = -50.0
    row["allow_negative_aava"] = True

    result = evaluate_mixed_unit_exposure([row])

    assert result.value_weighted_exposure_index is None
    assert any("Negative AAVA was explicitly allowed" in warning for warning in result.warnings)


@pytest.mark.parametrize("risk_score", [-0.01, 1.01])
def test_risk_score_outside_zero_to_one_fails_closed(risk_score: float) -> None:
    row = entity("a", "tonne_kilometres_or_pallet_movements")
    row["risk_score"] = risk_score

    with pytest.raises(ValueError, match="risk_score must be between 0 and 1"):
        evaluate_mixed_unit_exposure([row])


@pytest.mark.parametrize("aii", [-0.01, 1.01])
def test_aii_derived_risk_outside_zero_to_one_fails_closed(aii: float) -> None:
    row = entity("a", "tonne_kilometres_or_pallet_movements")
    row.pop("risk_level")
    row["outputs"] = {"aii": aii}

    with pytest.raises(ValueError, match="outputs.aii must be between 0 and 1"):
        evaluate_mixed_unit_exposure([row])


def test_mixed_unit_exposure_index_cannot_be_nan_or_infinity() -> None:
    result = evaluate_mixed_unit_exposure(
        [
            entity("a", "tonne_kilometres_or_pallet_movements", revenue=100.0, risk_level="low"),
            entity("b", "book_hour_equivalent_jobs_completed", revenue=200.0, risk_level="high"),
        ]
    )

    assert result.value_weighted_exposure_index is not None
    assert isfinite(result.value_weighted_exposure_index)
