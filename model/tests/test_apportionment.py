from __future__ import annotations

from math import inf

from conftest import load_schedule

from carsf.apportionment import evaluate_apportionment


def schedules_by_id() -> dict[str, dict]:
    return {
        "automotive_repair": load_schedule("automotive_repair"),
        "logistics_warehousing": load_schedule("logistics_warehousing"),
    }


def apportionment_example(activities, normalisation_permitted: bool = False) -> dict:
    return {
        "placeholder_notice": "Apportionment test uses illustrative placeholder values only.",
        "apportionment": {
            "normalisation_permitted": normalisation_permitted,
            "activities": activities,
        },
    }


def activity(schedule_id: str, share: float) -> dict:
    return {
        "activity_id": f"{schedule_id}_{share}",
        "schedule_id": schedule_id,
        "share": share,
        "basis": "audited_placeholder_share",
        "placeholder_basis": "illustrative_placeholder_only",
    }


def test_apportionment_rejects_negative_shares() -> None:
    result = evaluate_apportionment(
        apportionment_example([activity("logistics_warehousing", 1.1), activity("automotive_repair", -0.1)]),
        schedules_by_id(),
    )

    assert result.valid is False
    assert result.review_required is True
    assert "negative" in result.warnings[0].lower()


def test_apportionment_rejects_non_finite_shares() -> None:
    result = evaluate_apportionment(
        apportionment_example([activity("logistics_warehousing", inf)]),
        schedules_by_id(),
    )

    assert result.valid is False
    assert "finite" in result.warnings[0].lower()


def test_apportionment_rejects_shares_not_summing_to_one_without_normalisation() -> None:
    result = evaluate_apportionment(
        apportionment_example([activity("logistics_warehousing", 0.50), activity("automotive_repair", 0.25)]),
        schedules_by_id(),
    )

    assert result.valid is False
    assert "sum to 1.0" in result.warnings[0]


def test_apportionment_allows_explicit_normalisation() -> None:
    result = evaluate_apportionment(
        apportionment_example(
            [activity("logistics_warehousing", 0.50), activity("automotive_repair", 0.25)],
            normalisation_permitted=True,
        ),
        schedules_by_id(),
    )

    assert result.valid is True
    assert sum(item.share for item in result.activities) == 1.0
    assert any("normalised" in warning.lower() for warning in result.warnings)


def test_apportionment_rejects_unknown_schedule_ids() -> None:
    result = evaluate_apportionment(
        apportionment_example([activity("missing_schedule", 1.0)]),
        schedules_by_id(),
    )

    assert result.valid is False
    assert "unknown schedule_id" in result.warnings[0].lower()


def test_weighted_schedule_values_are_deterministic() -> None:
    result = evaluate_apportionment(
        apportionment_example([activity("automotive_repair", 0.25), activity("logistics_warehousing", 0.75)]),
        schedules_by_id(),
    )

    assert result.valid is True
    assert result.weighted_parameters["opfte_libc"] == 0.25 * 900.0 + 0.75 * 100000.0
    assert result.weighted_parameters["frv_standard"] == 0.25 * 45000.0 + 0.75 * 47000.0
    assert result.weighted_parameters["lambda_sector"] == 0.25 * 0.18 + 0.75 * 0.20
    assert result.weighted_parameters["aii_weights"]["compute_ratio"] == 0.25 * 0.15 + 0.75 * 0.20
