"""Deterministic placeholder uncertainty range helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from math import isfinite
from typing import Any


UNCERTAINTY_WARNING = (
    "These are deterministic placeholder uncertainty ranges only. They are not statistical confidence "
    "intervals, forecasts, real uncertainty quantification, population estimates, ABS/HILDA/Census analysis, "
    "DSS/Services Australia modelling, Treasury modelling, PBO costing, welfare advice, eligibility law, legal "
    "advice, tax advice, or economic validation."
)
UNCERTAINTY_NON_CLAIMS = [
    UNCERTAINTY_WARNING,
    "This is a prototype deterministic range wrapper only; it is not Monte Carlo, calibration, forecasting, or statistical inference.",
    "Uncertainty range outputs do not modify firm-level CARSF liability.",
]


@dataclass(frozen=True)
class UncertaintyRange:
    range_id: str
    metric_name: str
    low: float
    base: float
    high: float
    confidence_placeholder: str
    calibration_status: str
    uncertainty_drivers: list[str] = field(default_factory=list)
    illustrative_placeholder_only: bool = True
    placeholder_basis: list[str] = field(default_factory=list)

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class UncertaintyRangeResult:
    range_id: str
    metric_name: str
    low: float
    base: float
    high: float
    absolute_range_width: float
    relative_range_width: float | None
    ordered_correctly: bool
    confidence_placeholder: str
    calibration_status: str
    uncertainty_drivers: list[str]
    stability_band: str
    warnings: list[str] = field(default_factory=list)
    non_claims: list[str] = field(default_factory=lambda: list(UNCERTAINTY_NON_CLAIMS))

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


def uncertainty_range_from_mapping(source: UncertaintyRange | dict[str, Any]) -> UncertaintyRange:
    if isinstance(source, UncertaintyRange):
        return source
    return UncertaintyRange(
        range_id=str(source["range_id"]),
        metric_name=str(source["metric_name"]),
        low=source["low"],
        base=source["base"],
        high=source["high"],
        confidence_placeholder=str(source.get("confidence_placeholder", "placeholder_confidence_not_statistical")),
        calibration_status=str(source.get("calibration_status", "not_calibrated")),
        uncertainty_drivers=[str(item) for item in source.get("uncertainty_drivers", [])],
        illustrative_placeholder_only=bool(source.get("illustrative_placeholder_only", True)),
        placeholder_basis=[str(item) for item in source.get("placeholder_basis", [])],
    )


def _finite_number(value: Any, field_name: str) -> float:
    numeric = float(value)
    if not isfinite(numeric):
        raise ValueError(f"{field_name} must be finite")
    return numeric


def _signed_allowed(input_range: UncertaintyRange) -> bool:
    basis = " ".join(input_range.placeholder_basis).lower()
    return "allow_signed" in basis or "signed_metric_allowed" in basis


def _stability_band(relative_range_width: float | None, absolute_range_width: float, base: float) -> str:
    if base == 0 and absolute_range_width > 0:
        return "not_assessable"
    if relative_range_width is None:
        return "stable" if absolute_range_width == 0 else "not_assessable"
    if relative_range_width <= 0.20:
        return "stable"
    if relative_range_width <= 0.60:
        return "moderately_sensitive"
    return "fragile"


def evaluate_uncertainty_range(input_range: UncertaintyRange | dict[str, Any]) -> UncertaintyRangeResult:
    """Validate one deterministic placeholder low/base/high range."""

    range_obj = uncertainty_range_from_mapping(input_range)
    if range_obj.illustrative_placeholder_only is not True:
        raise ValueError("uncertainty range must be illustrative_placeholder_only")
    low = _finite_number(range_obj.low, "low")
    base = _finite_number(range_obj.base, "base")
    high = _finite_number(range_obj.high, "high")
    if not _signed_allowed(range_obj) and min(low, base, high) < 0:
        raise ValueError("low/base/high must be non-negative unless signed values are explicitly allowed")
    if low > base or base > high:
        raise ValueError("uncertainty range must satisfy low <= base <= high")
    absolute_width = high - low
    relative_width = None if base == 0 else absolute_width / base
    stability = _stability_band(relative_width, absolute_width, base)
    warnings = [
        "Range thresholds are illustrative placeholders and not calibrated uncertainty bands.",
        "Confidence placeholder is descriptive only and is not statistical confidence.",
    ]
    if stability == "not_assessable":
        warnings.append("Range stability is not assessable because the base value is zero or the range cannot be interpreted.")
    if range_obj.calibration_status != "calibrated_external_reviewed":
        warnings.append("Calibration status does not support real uncertainty quantification.")
    return UncertaintyRangeResult(
        range_id=range_obj.range_id,
        metric_name=range_obj.metric_name,
        low=low,
        base=base,
        high=high,
        absolute_range_width=absolute_width,
        relative_range_width=relative_width,
        ordered_correctly=True,
        confidence_placeholder=range_obj.confidence_placeholder,
        calibration_status=range_obj.calibration_status,
        uncertainty_drivers=list(range_obj.uncertainty_drivers),
        stability_band=stability,
        warnings=warnings,
    )
