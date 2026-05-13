"""Prototype investment and automation-burden guardrails.

This module is a non-operative review layer. It does not change CARSF
liability and does not provide economic, investment, tax, Treasury, ATO, legal,
or market validation.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any


INVESTMENT_NON_CLAIMS = [
    "These are prototype investment and tax-incidence guardrails only.",
    "They are not economic validation, investment advice, Treasury modelling, ATO guidance, legal advice, market forecasting, or tax advice.",
    "Guardrail outputs do not automatically modify final liability.",
]


@dataclass(frozen=True)
class InvestmentGuardrailInput:
    example_id: str
    aava: float
    final_liability: float
    capital_base: float
    uplift_rate: float
    revenue: float
    normal_return_proxy: float | None
    sector: str
    placeholder_basis: list[str] = field(default_factory=list)
    allow_negative_aava: bool = False

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InvestmentGuardrailResult:
    effective_burden_rate: float | None
    liability_to_revenue_rate: float | None
    liability_to_aava_rate: float | None
    normal_return_preserved: bool | None
    preserved_return_amount: float | None
    investment_risk_band: str
    over_capture_warning: bool
    under_capture_warning: bool
    reasons: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(INVESTMENT_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def _finite_number(value: Any, field_name: str) -> float:
    numeric = float(value)
    if not isfinite(numeric):
        raise ValueError(f"{field_name} must be finite")
    return numeric


def _non_negative_number(value: Any, field_name: str) -> float:
    numeric = _finite_number(value, field_name)
    if numeric < 0:
        raise ValueError(f"{field_name} cannot be negative")
    return numeric


def _input_from_mapping(source: dict[str, Any]) -> InvestmentGuardrailInput:
    return InvestmentGuardrailInput(
        example_id=str(source.get("example_id", "")),
        aava=source.get("aava", 0.0),
        final_liability=source.get("final_liability", source.get("liability", 0.0)),
        capital_base=source.get("capital_base", 0.0),
        uplift_rate=source.get("uplift_rate", 0.0),
        revenue=source.get("revenue", source.get("reported_revenue", 0.0)),
        normal_return_proxy=source.get("normal_return_proxy"),
        sector=str(source.get("sector", "")),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
        allow_negative_aava=bool(source.get("allow_negative_aava", False)),
    )


def _normal_return_proxy(inputs: InvestmentGuardrailInput) -> float:
    if inputs.normal_return_proxy is not None:
        return _non_negative_number(inputs.normal_return_proxy, "normal_return_proxy")
    return _non_negative_number(inputs.capital_base, "capital_base") * _non_negative_number(inputs.uplift_rate, "uplift_rate")


def evaluate_investment_guardrail(inputs: InvestmentGuardrailInput | dict[str, Any]) -> InvestmentGuardrailResult:
    """Assess non-operative investment and burden review signals."""

    if isinstance(inputs, dict):
        inputs = _input_from_mapping(inputs)

    final_liability = _non_negative_number(inputs.final_liability, "final_liability")
    revenue = _non_negative_number(inputs.revenue, "revenue")
    capital_base = _non_negative_number(inputs.capital_base, "capital_base")
    uplift_rate = _non_negative_number(inputs.uplift_rate, "uplift_rate")
    aava = _finite_number(inputs.aava, "aava")
    normal_return_proxy = _normal_return_proxy(inputs)
    warnings = [
        "Investment guardrail thresholds are illustrative placeholders only.",
        "This guardrail does not change final liability.",
    ]
    reasons: list[str] = []

    liability_to_revenue = final_liability / revenue if revenue > 0 else None
    if revenue == 0 and final_liability > 0:
        reasons.append("Positive liability with zero revenue requires critical review.")
        return InvestmentGuardrailResult(
            effective_burden_rate=None,
            liability_to_revenue_rate=None,
            liability_to_aava_rate=None,
            normal_return_preserved=None,
            preserved_return_amount=None,
            investment_risk_band="critical",
            over_capture_warning=True,
            under_capture_warning=False,
            reasons=reasons,
            warnings=warnings,
        )

    if aava < 0:
        if not inputs.allow_negative_aava:
            warnings.append("AAVA is negative without explicit allow_negative_aava metadata; investment burden is not assessable.")
            return InvestmentGuardrailResult(
                effective_burden_rate=None,
                liability_to_revenue_rate=liability_to_revenue,
                liability_to_aava_rate=None,
                normal_return_preserved=None,
                preserved_return_amount=None,
                investment_risk_band="not_assessable",
                over_capture_warning=False,
                under_capture_warning=False,
                reasons=["Negative AAVA prevents meaningful burden-rate assessment under prototype rules."],
                warnings=warnings,
            )
        warnings.append("Negative AAVA was explicitly allowed for review, but burden-rate assessment remains not assessable.")
        return InvestmentGuardrailResult(
            effective_burden_rate=None,
            liability_to_revenue_rate=liability_to_revenue,
            liability_to_aava_rate=None,
            normal_return_preserved=None,
            preserved_return_amount=None,
            investment_risk_band="not_assessable",
            over_capture_warning=False,
            under_capture_warning=False,
            reasons=["Negative AAVA requires manual review rather than automated burden scoring."],
            warnings=warnings,
        )

    if aava == 0:
        if final_liability > 0:
            reasons.append("Positive liability with zero AAVA suggests possible over-capture or cap failure.")
            return InvestmentGuardrailResult(
                effective_burden_rate=None,
                liability_to_revenue_rate=liability_to_revenue,
                liability_to_aava_rate=None,
                normal_return_preserved=False,
                preserved_return_amount=None,
                investment_risk_band="critical",
                over_capture_warning=True,
                under_capture_warning=False,
                reasons=reasons,
                warnings=warnings,
            )
        return InvestmentGuardrailResult(
            effective_burden_rate=0.0,
            liability_to_revenue_rate=liability_to_revenue,
            liability_to_aava_rate=0.0,
            normal_return_preserved=True,
            preserved_return_amount=0.0,
            investment_risk_band="low",
            over_capture_warning=False,
            under_capture_warning=False,
            reasons=["No AAVA and no liability under placeholder inputs."],
            warnings=warnings,
        )

    effective_burden = final_liability / aava
    preserved_return_amount = aava - final_liability
    normal_return_preserved = preserved_return_amount >= normal_return_proxy
    liability_to_aava = effective_burden
    under_capture_warning = final_liability == 0 and aava > 0
    over_capture_warning = effective_burden > 0.50 or final_liability > aava

    if effective_burden > 0.80 or (liability_to_revenue is not None and liability_to_revenue > 0.25):
        risk_band = "critical"
        reasons.append("Placeholder effective burden is very high relative to AAVA or revenue.")
    elif effective_burden > 0.50 or (liability_to_revenue is not None and liability_to_revenue > 0.15):
        risk_band = "high"
        reasons.append("Placeholder effective burden may warrant investment-deterrence review.")
    elif effective_burden > 0.25 or (liability_to_revenue is not None and liability_to_revenue > 0.05):
        risk_band = "medium"
        reasons.append("Placeholder burden is material but below high-review thresholds.")
    else:
        risk_band = "low"
        reasons.append("Placeholder burden is low under illustrative thresholds.")

    if not normal_return_preserved:
        warnings.append("Normal return proxy is not preserved under illustrative placeholder inputs.")
        if risk_band == "low":
            risk_band = "medium"
    if under_capture_warning:
        warnings.append("Positive AAVA with zero liability may indicate under-capture under placeholder rules.")

    # Keep local variables referenced so static reviewers can see validation occurred.
    _ = capital_base, uplift_rate
    return InvestmentGuardrailResult(
        effective_burden_rate=effective_burden,
        liability_to_revenue_rate=liability_to_revenue,
        liability_to_aava_rate=liability_to_aava,
        normal_return_preserved=normal_return_preserved,
        preserved_return_amount=preserved_return_amount,
        investment_risk_band=risk_band,
        over_capture_warning=over_capture_warning,
        under_capture_warning=under_capture_warning,
        reasons=reasons,
        warnings=warnings,
    )
