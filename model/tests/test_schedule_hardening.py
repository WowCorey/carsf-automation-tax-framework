from conftest import load_schedule


def test_schedules_include_v15_measurement_controls() -> None:
    for schedule_id in ["automotive_repair", "logistics_warehousing"]:
        schedule = load_schedule(schedule_id)

        assert schedule["calibration_status"] == "illustrative_placeholder_values_only"
        assert "measurement_scope" in schedule
        assert "measurement_controls" in schedule
        assert schedule["measurement_controls"]["aava_deductibility_reference"] == (
            "paper/aava_deductibility_appendix.md"
        )
        assert "avoidance_controls" in schedule


def test_automotive_schedule_controls_token_oversight_and_fake_qlc() -> None:
    controls = load_schedule("automotive_repair")["avoidance_controls"]

    assert "fake_qlc_inflation" in controls
    assert "token_human_oversight_jobs" in controls
    assert "related_party_ai_service_fees" in controls


def test_logistics_schedule_controls_offshore_and_sector_arbitrage() -> None:
    controls = load_schedule("logistics_warehousing")["avoidance_controls"]

    assert "offshore_ai_services" in controls
    assert "sector_classification_arbitrage" in controls
    assert "entity_splitting" in controls


def test_aava_appendix_contains_required_taxonomy(repo_root) -> None:
    appendix = (repo_root / "paper" / "aava_deductibility_appendix.md").read_text(
        encoding="utf-8"
    )

    for term in [
        "Human wages counted in QLC",
        "Ordinary rent/utilities",
        "AI cloud inference",
        "AI licensing",
        "Robotics depreciation",
        "Related-party service charges",
        "Platform fees",
        "Human training",
        "Offshore AI services",
    ]:
        assert term in appendix
