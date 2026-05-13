from __future__ import annotations

from carsf.aggregation import EntityInput, evaluate_group_aggregation


def entity(entity_id: str, unit: str = "tonne_kilometres_or_pallet_movements") -> EntityInput:
    return EntityInput(
        entity_id=entity_id,
        description=f"{entity_id} description",
        revenue=1000.0,
        output_value=100.0,
        qlc=1.0,
        hle=2.0,
        aii=0.50,
        nltg=0.0,
        aava=300.0,
        liability=10.0,
        role="test_entity",
        flags=[],
        canonical_output_unit=unit,
        capital_base=100.0,
        verified_credits=0.0,
        standalone_risk="low",
    )


def group_example() -> dict:
    return {
        "group_id": "test_group",
        "placeholder_notice": "Illustrative placeholder group only.",
        "recompute_parameters": {
            "frv_standard": 47000.0,
            "lambda_sector": 0.20,
            "lambda_combined": 0.27,
            "theta": 0.60,
            "uplift_rate": 1.12,
            "rent_tax_rate": 0.22,
        },
        "capital_base": 200.0,
        "verified_credits": 0.0,
    }


def test_group_aggregation_sums_revenue_qlc_aava_and_liabilities() -> None:
    result = evaluate_group_aggregation(group_example(), [entity("a"), entity("b")])

    assert result.aggregate_revenue == 2000.0
    assert result.aggregate_qlc == 2.0
    assert result.aggregate_aava == 600.0
    assert result.standalone_entity_liability_sum == 20.0


def test_group_aggregation_refuses_blind_output_aggregation_for_mismatched_units() -> None:
    result = evaluate_group_aggregation(group_example(), [entity("a", "jobs"), entity("b", "pallets")])

    assert result.output_units_match is False
    assert result.aggregate_output is None
    assert result.aggregate_hle is None
    assert result.weighted_aii is None
    assert result.aggregate_nltg_preview is None
    assert result.group_recomputed_liability_preview is None
    assert any("not blindly aggregated" in warning for warning in result.warnings)


def test_group_recomputed_nltg_preview_is_non_negative() -> None:
    high_aii = EntityInput(
        entity_id="high_aii",
        description="High automation entity",
        revenue=5000.0,
        output_value=1000.0,
        qlc=1.0,
        hle=10.0,
        aii=0.80,
        nltg=7.0,
        aava=2000.0,
        liability=0.0,
        role="automation_entity",
        flags=["OFFSHORE_AUTOMATION_SERVICE"],
        canonical_output_unit="tonne_kilometres_or_pallet_movements",
        capital_base=1000.0,
        verified_credits=0.0,
        standalone_risk="medium",
    )
    result = evaluate_group_aggregation(group_example(), [high_aii])

    assert result.aggregate_nltg_preview is not None
    assert result.aggregate_nltg_preview >= 0
