from __future__ import annotations

from carsf.household_calibration_shell import get_household_calibration_requirements


def test_household_calibration_shell_returns_unmet_requirements() -> None:
    shell = get_household_calibration_requirements()

    assert shell.requirement_count == 12
    assert shell.unmet_requirement_count == shell.requirement_count
    assert shell.ready_for_real_distributional_claims is False
    assert all(requirement.status == "unmet" for requirement in shell.requirements)


def test_household_calibration_shell_disallows_real_data_in_repo() -> None:
    shell = get_household_calibration_requirements()

    assert all(requirement.real_data_in_repo_allowed is False for requirement in shell.requirements)
    assert any("Real household data is not allowed" in warning for warning in shell.warnings)


def test_household_calibration_shell_includes_required_categories() -> None:
    shell = get_household_calibration_requirements()
    categories = {requirement.category for requirement in shell.requirements}

    assert {
        "household composition",
        "income distribution",
        "employment displacement",
        "regional labour-market depth",
        "housing costs",
        "essential costs",
        "savings/debt buffers",
        "welfare/transfer baseline",
        "re-employment timing",
        "payment eligibility",
        "survey weighting",
        "uncertainty/confidence intervals",
    } <= categories
