"""Prototype metadata-only sector stress matrix for CARSF schedules."""

from __future__ import annotations

import json
import math
from dataclasses import asdict, dataclass, field
from typing import Any


SECTOR_STRESS_WARNING = (
    "The sector stress matrix is prototype metadata review only. It is not calibrated. "
    "It is not a real-world ranking of sectors. It is not Treasury modelling. It is not ATO guidance. "
    "It is not ABS/ATO/DSS/PBO analysis. It does not use real industry data. "
    "It does not estimate actual tax payable."
)
SECTOR_STRESS_NON_CLAIMS = [
    SECTOR_STRESS_WARNING,
    "The sector stress matrix does not modify firm-level CARSF liability logic.",
    "The sector stress matrix does not implement legal sector attribution or real multi-schedule blending.",
    "The sector stress matrix is not economic validation, investment advice, legal advice, or tax advice.",
    "All schedules remain placeholder-only and subject to external calibration, legal review, and methods review.",
]

STRESS_DIMENSIONS = [
    "automation_intensity_placeholder",
    "qlc_vulnerability_placeholder",
    "aava_sensitivity_placeholder",
    "incidence_risk_placeholder",
    "investment_deterrence_risk_placeholder",
    "avoidance_gaming_risk_placeholder",
    "calibration_difficulty_placeholder",
    "legal_attribution_difficulty_placeholder",
]

STRESS_BANDS = [
    "low_placeholder_stress",
    "moderate_placeholder_stress",
    "high_placeholder_stress",
    "critical_review_required",
    "not_assessable",
]


@dataclass(frozen=True)
class SectorStressInput:
    schedule: dict[str, Any]
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SectorStressResult:
    schedule_id: str
    schedule_name: str
    canonical_output_unit: str
    automation_intensity_placeholder: str
    qlc_vulnerability_placeholder: str
    aava_sensitivity_placeholder: str
    incidence_risk_placeholder: str
    investment_deterrence_risk_placeholder: str
    avoidance_gaming_risk_placeholder: str
    calibration_difficulty_placeholder: str
    legal_attribution_difficulty_placeholder: str
    display_control_status: str
    do_not_rank: bool
    main_reason: str
    dimension_scores: dict[str, float | None]
    stress_reasons: list[str]
    calibration_blockers: list[str]
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(SECTOR_STRESS_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SectorStressSummary:
    schedule_count: int
    stress_band_counts: dict[str, int]
    display_status_counts: dict[str, int]
    external_review_required_count: int
    strong_warning_required_count: int
    do_not_rank_all: bool
    calibration_blockers: list[str]
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(SECTOR_STRESS_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _input_from_mapping(source: SectorStressInput | dict[str, Any]) -> SectorStressInput:
    if isinstance(source, SectorStressInput):
        return source
    return SectorStressInput(
        schedule=dict(source["schedule"]),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def _finite(value: Any, label: str) -> float:
    number = float(value)
    if not math.isfinite(number):
        raise ValueError(f"{label} must be finite")
    return number


def _band(score: float | None) -> str:
    if score is None:
        return "not_assessable"
    if score < 0.25:
        return "low_placeholder_stress"
    if score < 0.45:
        return "moderate_placeholder_stress"
    if score < 0.65:
        return "high_placeholder_stress"
    return "critical_review_required"


def _rank_band(band: str) -> int:
    return {
        "low_placeholder_stress": 1,
        "moderate_placeholder_stress": 2,
        "high_placeholder_stress": 3,
        "critical_review_required": 4,
        "not_assessable": 4,
    }.get(band, 4)


def _text(schedule: dict[str, Any]) -> str:
    return json.dumps({key: value for key, value in schedule.items() if key != "_path"}, sort_keys=True).lower()


def _contains_any(text: str, terms: list[str]) -> bool:
    return any(term in text for term in terms)


def _term_count(text: str, terms: list[str]) -> int:
    return sum(1 for term in terms if term in text)


def _score_cap(value: float) -> float:
    return max(0.0, min(1.0, value))


def _validate_schedule_basics(schedule: dict[str, Any]) -> None:
    if schedule.get("calibration_status") != "illustrative_placeholder_values_only":
        raise ValueError(f"{schedule.get('schedule_id', 'schedule')} missing illustrative placeholder calibration_status")
    if schedule.get("status") != "placeholder_prototype_for_v1_5":
        raise ValueError(f"{schedule.get('schedule_id', 'schedule')} missing placeholder prototype status")
    for field in ["schedule_id", "schedule_name", "canonical_output_unit", "aii", "qlc", "caps", "avoidance_controls"]:
        if field not in schedule:
            raise ValueError(f"schedule missing required field for stress matrix: {field}")


def _automation_score(schedule: dict[str, Any], text: str) -> tuple[float, list[str]]:
    del text
    weights = schedule["aii"]["weights"]
    compute = _finite(weights["compute_ratio"], "compute_ratio")
    auto_decision = _finite(weights["auto_decision_ratio"], "auto_decision_ratio")
    robotics = _finite(weights["robotics_capital_ratio"], "robotics_capital_ratio")
    auto_process = _finite(weights["auto_process_share"], "auto_process_share")
    emphasis = compute + auto_decision + auto_process + (0.25 * robotics)
    reasons = [f"automation emphasis uses AII metadata only ({emphasis:.2f})"]
    if robotics >= 0.25:
        reasons.append("robotics placeholder weight adds physical-automation review note")
    return _score_cap(emphasis / 1.25), reasons


def _qlc_score(schedule: dict[str, Any], text: str) -> tuple[float, list[str]]:
    weights = schedule["qlc"]["weights"]
    skill = _finite(weights["gamma_skill_development"], "gamma_skill_development")
    job_security = _finite(weights["beta_job_security"], "beta_job_security")
    australian = _finite(weights["delta_australian_nexus"], "delta_australian_nexus")
    vulnerability = (0.35 * (1.0 - skill)) + (0.25 * job_security) + (0.20 * australian)
    term_hits = _term_count(text, ["token", "self-service", "offshore", "outsourced", "escalation", "customer self"])
    vulnerability += min(0.25, term_hits * 0.05)
    reasons = ["QLC vulnerability uses placeholder QLC weights and schedule text only"]
    if term_hits:
        reasons.append("token, self-service, offshore, outsourced, or escalation terms increase review pressure")
    return _score_cap(vulnerability), reasons


def _aava_score(schedule: dict[str, Any], text: str) -> tuple[float, list[str]]:
    caps = schedule["caps"]
    cap_pressure = (
        _finite(caps["lambda_sector"], "lambda_sector")
        + _finite(caps["LAMBDA_sector"], "LAMBDA_sector")
        + _finite(caps["rent_tax_rate"], "rent_tax_rate")
    ) / 3.0
    terms = [
        "cloud",
        "inference",
        "royalt",
        " ip",
        "robotics lease",
        "related-party",
        "platform fee",
        "offshore",
        "model access",
        "data access",
        "licence",
        "license",
        "open-source",
    ]
    hits = _term_count(text, terms)
    score = cap_pressure + min(0.45, hits * 0.045)
    reasons = ["AAVA sensitivity uses cap placeholders and AAVA-adjacent schedule terms only"]
    if hits:
        reasons.append("AAVA-adjacent offshore, related-party, IP, cloud, model, data, or licence terms are present")
    return _score_cap(score), reasons


def _incidence_score(schedule: dict[str, Any], text: str) -> tuple[float, list[str]]:
    consumer_terms = [
        "customer",
        "retail",
        "support",
        "logistics",
        "delivery",
        "platform",
        "transaction",
        "fulfilment",
        "pricing",
    ]
    hits = _term_count(text, consumer_terms)
    score = 0.20 + min(0.60, hits * 0.06)
    reasons = ["Incidence risk uses consumer-facing and transaction-facing wording only"]
    if hits:
        reasons.append("consumer, support, retail, logistics, platform, or transaction terms increase review pressure")
    return _score_cap(score), reasons


def _investment_score(schedule: dict[str, Any], text: str) -> tuple[float, list[str]]:
    caps = schedule["caps"]
    cap_pressure = (
        _finite(caps["lambda_sector"], "lambda_sector")
        + _finite(caps["LAMBDA_sector"], "LAMBDA_sector")
        + _finite(caps["rent_tax_rate"], "rent_tax_rate")
    ) / 3.0
    unresolved = _contains_any(text, ["capital-base treatment", "aasb 138", "intangible", "unresolved"])
    score = cap_pressure + (0.35 if unresolved else 0.0)
    reasons = ["Investment risk uses cap placeholders and unresolved capital/intangible wording only"]
    if unresolved:
        reasons.append("unresolved software, intangible, or AASB 138 capital-base treatment requires review")
    return _score_cap(score), reasons


def _avoidance_score(schedule: dict[str, Any], text: str) -> tuple[float, list[str]]:
    controls = schedule.get("avoidance_controls", {})
    score = min(0.45, len(controls) * 0.07)
    terms = [
        "related-party",
        "offshore",
        "entity splitting",
        "royalt",
        "platform",
        " ip",
        "cloud",
        "inference",
        "token",
        "self-checkout",
        "self-service",
        "relabel",
        "model access",
    ]
    hits = _term_count(text, terms)
    score += min(0.45, hits * 0.04)
    reasons = ["Avoidance risk uses number and type of avoidance controls only"]
    if controls:
        reasons.append(f"{len(controls)} avoidance controls are listed")
    if hits:
        reasons.append("related-party, offshore, IP, platform, cloud, token-worker, or self-service terms are present")
    return _score_cap(score), reasons


def _calibration_score(schedule: dict[str, Any], text: str) -> tuple[float, list[str]]:
    requirements = schedule.get("data_required_for_real_calibration", [])
    score = min(0.50, len(requirements) * 0.07)
    terms = [
        "legal",
        "tax",
        "treasury",
        "aasb",
        "intangible",
        "platform",
        "cross-border",
        "attribution",
        "professional judgement",
        "customer self",
    ]
    hits = _term_count(text, terms)
    score += min(0.45, hits * 0.05)
    reasons = ["Calibration difficulty uses listed data requirements and review dependencies only"]
    if hits:
        reasons.append("legal, tax, Treasury, AASB, intangible, platform, cross-border, or attribution terms are present")
    return _score_cap(score), reasons


def _legal_attribution_score(schedule: dict[str, Any], text: str) -> tuple[float, list[str]]:
    terms = [
        "offshore",
        "related-party",
        " ip",
        "royalt",
        "platform",
        "mixed",
        "apportion",
        "professional judgement",
        "customer self",
        "legal review",
        "aasb 138",
        "attribution",
    ]
    hits = _term_count(text, terms)
    score = min(1.0, 0.12 + hits * 0.08)
    reasons = ["Legal attribution difficulty uses schedule attribution and review wording only"]
    if hits:
        reasons.append("offshore, related-party, IP, platform, mixed-activity, customer self-service, legal review, or AASB terms are present")
    return _score_cap(score), reasons


def _display_status(bands: dict[str, str]) -> str:
    band_values = list(bands.values())
    critical_count = sum(1 for value in band_values if value == "critical_review_required")
    high_count = sum(1 for value in band_values if value == "high_placeholder_stress")
    if critical_count:
        return "external_review_required"
    if high_count >= 3:
        return "strong_warning_required"
    if high_count or any(value == "moderate_placeholder_stress" for value in band_values):
        return "show_with_warning"
    return "prototype_discussion_only"


def evaluate_sector_stress(inputs: SectorStressInput | dict[str, Any]) -> SectorStressResult:
    """Evaluate one sector schedule using placeholder metadata only."""

    input_obj = _input_from_mapping(inputs)
    schedule = input_obj.schedule
    _validate_schedule_basics(schedule)
    text = _text(schedule)
    score_builders = {
        "automation_intensity_placeholder": _automation_score,
        "qlc_vulnerability_placeholder": _qlc_score,
        "aava_sensitivity_placeholder": _aava_score,
        "incidence_risk_placeholder": _incidence_score,
        "investment_deterrence_risk_placeholder": _investment_score,
        "avoidance_gaming_risk_placeholder": _avoidance_score,
        "calibration_difficulty_placeholder": _calibration_score,
        "legal_attribution_difficulty_placeholder": _legal_attribution_score,
    }
    scores: dict[str, float | None] = {}
    bands: dict[str, str] = {}
    reasons: list[str] = []
    for dimension, builder in score_builders.items():
        score, dimension_reasons = builder(schedule, text)
        scores[dimension] = score
        bands[dimension] = _band(score)
        reasons.extend(dimension_reasons)

    display_status = _display_status(bands)
    max_dimension = sorted(bands, key=lambda key: (-_rank_band(bands[key]), key))[0]
    blockers = list(schedule.get("data_required_for_real_calibration", []))
    warnings = [
        "Sector stress matrix row is metadata-only and must not be treated as a sector rank.",
        "Do not rank this schedule against other schedules using placeholder stress bands.",
        "Firm-level CARSF liability logic is not modified.",
    ]
    if schedule["schedule_id"] == "software_digital_platforms":
        warnings.append("Software / digital platform capital-base treatment remains unresolved and requires AASB 138, tax counsel, and Treasury review.")

    return SectorStressResult(
        schedule_id=str(schedule["schedule_id"]),
        schedule_name=str(schedule["schedule_name"]),
        canonical_output_unit=str(schedule["canonical_output_unit"]),
        automation_intensity_placeholder=bands["automation_intensity_placeholder"],
        qlc_vulnerability_placeholder=bands["qlc_vulnerability_placeholder"],
        aava_sensitivity_placeholder=bands["aava_sensitivity_placeholder"],
        incidence_risk_placeholder=bands["incidence_risk_placeholder"],
        investment_deterrence_risk_placeholder=bands["investment_deterrence_risk_placeholder"],
        avoidance_gaming_risk_placeholder=bands["avoidance_gaming_risk_placeholder"],
        calibration_difficulty_placeholder=bands["calibration_difficulty_placeholder"],
        legal_attribution_difficulty_placeholder=bands["legal_attribution_difficulty_placeholder"],
        display_control_status=display_status,
        do_not_rank=True,
        main_reason=f"{max_dimension} is {bands[max_dimension]} using placeholder metadata only.",
        dimension_scores=scores,
        stress_reasons=sorted(set(reasons)),
        calibration_blockers=blockers,
        warnings=warnings,
    )


def build_sector_stress_matrix(schedules: list[dict[str, Any]]) -> list[SectorStressResult]:
    """Evaluate all sector schedules in deterministic schedule_id order."""

    if not schedules:
        raise ValueError("sector stress matrix requires at least one schedule")
    results = [
        evaluate_sector_stress({"schedule": schedule, "placeholder_basis": ["sector stress matrix"]})
        for schedule in schedules
    ]
    return sorted(results, key=lambda item: item.schedule_id)


def summarise_sector_stress(results: list[SectorStressResult | dict[str, Any]]) -> SectorStressSummary:
    """Summarise sector stress matrix outputs without ranking sectors."""

    if not results:
        raise ValueError("sector stress summary requires at least one result")
    rows = [
        result if isinstance(result, SectorStressResult) else SectorStressResult(**result)
        for result in results
    ]
    stress_counts = {band: 0 for band in STRESS_BANDS}
    display_counts: dict[str, int] = {}
    blockers: list[str] = []
    for row in rows:
        for dimension in STRESS_DIMENSIONS:
            band = getattr(row, dimension)
            stress_counts[band] = stress_counts.get(band, 0) + 1
        display_counts[row.display_control_status] = display_counts.get(row.display_control_status, 0) + 1
        blockers.extend(f"{row.schedule_id}: {item}" for item in row.calibration_blockers)
    return SectorStressSummary(
        schedule_count=len(rows),
        stress_band_counts=dict(sorted(stress_counts.items())),
        display_status_counts=dict(sorted(display_counts.items())),
        external_review_required_count=sum(1 for row in rows if row.display_control_status == "external_review_required"),
        strong_warning_required_count=sum(1 for row in rows if row.display_control_status == "strong_warning_required"),
        do_not_rank_all=all(row.do_not_rank for row in rows),
        calibration_blockers=sorted(set(blockers)),
        warnings=[
            "Summary counts are metadata review counts only, not sector ranks.",
            "All rows are marked do_not_rank.",
            "All schedules remain subject to external calibration, legal review, and methods review.",
        ],
    )
