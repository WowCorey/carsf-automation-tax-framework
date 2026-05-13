from conftest import example_nltg, load_example


def test_mechanic_ai_admin_is_not_punished_like_robotic_shop() -> None:
    ai_admin = example_nltg("mechanic_ai_admin")
    robotic = example_nltg("mechanic_robotic")

    assert ai_admin == 0
    assert robotic > ai_admin


def test_fully_robotic_shop_has_higher_nltg_than_human_shop() -> None:
    human = example_nltg("mechanic_traditional")
    robotic = example_nltg("mechanic_robotic")

    assert human == 0
    assert robotic > human


def test_logistics_ai_platform_materially_exceeds_hybrid_nltg() -> None:
    hybrid = example_nltg("logistics_hybrid")
    platform = example_nltg("logistics_ai_platform")

    assert platform >= hybrid + 10


def test_entity_splitting_safe_harbour_avoidance_is_flagged() -> None:
    flags = load_example("logistics_ai_platform")["red_team_notes"]["flags"]
    assert "entity_splitting_safe_harbour" in flags


def test_offshore_automation_service_avoidance_is_flagged() -> None:
    flags = load_example("logistics_ai_platform")["red_team_notes"]["flags"]
    assert "offshore_automation_service" in flags
