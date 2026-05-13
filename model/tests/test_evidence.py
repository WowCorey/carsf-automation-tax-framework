from __future__ import annotations

from carsf.evidence import assess_evidence, get_default_evidence_requirements


def test_evidence_requirements_load() -> None:
    requirements = get_default_evidence_requirements()

    assert requirements
    assert all(requirement.requirement_id for requirement in requirements)


def test_evidence_assessment_returns_placeholder_only_without_real_evidence() -> None:
    assessment = assess_evidence(
        {
            "status": "illustrative_placeholder",
            "placeholder_notice": "illustrative placeholder only",
        },
        ["core_formula", "safe_harbour"],
    )

    assert assessment.status == "placeholder_only"
    assert assessment.review_required is True
    assert assessment.missing_requirements


def test_evidence_assessment_includes_non_claim_wording() -> None:
    assessment = assess_evidence({"status": "illustrative_placeholder"}, "core_formula")
    combined = " ".join(assessment.non_claims)

    assert "prototype evidence assessment only" in combined
    assert "not legal, tax, Treasury, ATO" in combined


def test_required_categories_cover_all_review_layers() -> None:
    categories = {requirement.category for requirement in get_default_evidence_requirements()}

    assert {
        "core_formula",
        "safe_harbour",
        "avoidance",
        "grouping",
        "transfer_pricing",
        "mixed_units",
    }.issubset(categories)
