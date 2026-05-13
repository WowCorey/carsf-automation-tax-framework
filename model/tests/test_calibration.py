from __future__ import annotations

from carsf.calibration import REQUIRED_COMPONENTS, get_calibration_registry, list_requirements_by_component, validate_no_fake_calibration_values


def test_calibration_registry_loads() -> None:
    registry = get_calibration_registry()

    assert registry.version == "CARSF V1.5 calibration shell"
    assert registry.requirements


def test_calibration_registry_includes_all_required_components() -> None:
    registry = get_calibration_registry()
    components = {requirement.model_component for requirement in registry.requirements}

    assert set(REQUIRED_COMPONENTS).issubset(components)


def test_validate_no_fake_calibration_values_returns_true() -> None:
    assert validate_no_fake_calibration_values(get_calibration_registry()) is True


def test_calibration_requirements_mark_not_collected_or_placeholder() -> None:
    registry = get_calibration_registry()

    assert all(requirement.calibration_status in {"not_collected", "placeholder", "placeholder_only"} for requirement in registry.requirements)
    assert all("No real value" in " ".join(requirement.notes) for requirement in registry.requirements)


def test_list_requirements_by_component_filters_registry() -> None:
    requirements = list_requirements_by_component("OPFTE")

    assert requirements
    assert all("OPFTE" in requirement.model_component for requirement in requirements)
