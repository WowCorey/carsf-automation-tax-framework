"""Runner for transfer-pricing and mixed-unit preview examples."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .example_runner import ExampleRunnerError, load_yaml_file
from .group_runner import load_schedules_by_id
from .mixed_units import (
    MixedUnitExposureResult,
    UnitCompatibilityResult,
    evaluate_mixed_unit_exposure,
    evaluate_unit_compatibility,
)
from .transfer_pricing import (
    AdjustedAAVAPreview,
    LiabilityAdjustmentPreview,
    TransferPricingPreviewResult,
    evaluate_transfer_pricing_preview,
    preview_adjusted_aava,
    preview_liability_with_adjusted_aava,
)


RELATED_PARTY_AI_FEE_ID = "related_party_ai_fee_structure"
ROBOTICS_LEASING_ID = "robotics_leasing_structure"
MIXED_UNIT_PLATFORM_ID = "mixed_unit_platform_group"
TRANSFER_PRICING_REPORT_STATUS = "illustrative_transfer_pricing_and_mixed_unit_previews_only"
TRANSFER_PRICING_REPORT_WARNING = (
    "These outputs are prototype review previews only. They are not transfer-pricing adjustments, "
    "ATO findings, legal findings, Treasury guidance, OECD/BEPS analysis, or economic validation."
)
TRANSFER_PRICING_NON_CLAIMS = [
    "Not transfer-pricing adjustments.",
    "Not ATO findings.",
    "Not legal findings.",
    "Not Treasury guidance.",
    "Not OECD/BEPS analysis.",
    "Not economic validation.",
    "Not real tax assessments.",
    "Adjusted AAVA is preview-only and does not replace reported AAVA.",
    "Value-weighted exposure index is not a tax base.",
]


@dataclass(frozen=True)
class TransferPricingScenarioResult:
    """Transfer-pricing preview result for one illustrative scenario."""

    scenario_id: str
    title: str
    schedule_id: str
    source: dict[str, Any]
    reported_aava: float
    transfer_pricing_result: TransferPricingPreviewResult
    adjusted_aava_preview: AdjustedAAVAPreview
    liability_preview: LiabilityAdjustmentPreview

    def to_jsonable(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class TransferPricingPreviewReport:
    """Combined transfer-pricing and mixed-unit preview output."""

    related_party_ai_fee: TransferPricingScenarioResult
    robotics_leasing: TransferPricingScenarioResult
    mixed_unit_group: dict[str, Any]
    unit_compatibility: UnitCompatibilityResult
    mixed_unit_exposure: MixedUnitExposureResult

    def to_jsonable(self) -> dict[str, Any]:
        return {
            "related_party_ai_fee": self.related_party_ai_fee.to_jsonable(),
            "robotics_leasing": self.robotics_leasing.to_jsonable(),
            "mixed_unit_group": self.mixed_unit_group,
            "unit_compatibility": asdict(self.unit_compatibility),
            "mixed_unit_exposure": asdict(self.mixed_unit_exposure),
        }


def _load_group_yaml(repo_root: Path, group_id: str) -> dict[str, Any]:
    return load_yaml_file(repo_root / "examples" / "groups" / f"{group_id}.yaml", "group example file")


def _reported_aava(source: dict[str, Any]) -> float:
    if "reported_aava" in source:
        return float(source["reported_aava"])
    outputs = source.get("existing_outputs", {})
    if isinstance(outputs, dict) and "aava" in outputs:
        return float(outputs["aava"])
    raise ExampleRunnerError(f"Missing reported_aava for {source.get('group_id', '<unknown>')}")


def _existing_outputs(source: dict[str, Any]) -> dict[str, Any]:
    outputs = source.get("existing_outputs", {})
    if not isinstance(outputs, dict):
        raise ExampleRunnerError(f"existing_outputs must be a mapping for {source.get('group_id', '<unknown>')}")
    return {
        **outputs,
        "capital_base": source.get("capital_base", outputs.get("capital_base", 0.0)),
        "verified_credits": source.get("verified_credits", outputs.get("verified_credits", 0.0)),
    }


def _run_transfer_scenario(
    source: dict[str, Any],
    schedules_by_id: dict[str, dict[str, Any]],
) -> TransferPricingScenarioResult:
    schedule_id = str(source.get("schedule_used", ""))
    if schedule_id not in schedules_by_id:
        raise ExampleRunnerError(f"Unknown schedule for transfer-pricing scenario: {schedule_id}")
    reported_aava = _reported_aava(source)
    transfer_result = evaluate_transfer_pricing_preview(source, reported_aava)
    adjusted_preview = preview_adjusted_aava(reported_aava, transfer_result)
    liability_preview = preview_liability_with_adjusted_aava(
        _existing_outputs(source),
        adjusted_preview.adjusted_aava_preview,
        schedules_by_id[schedule_id],
        capital_base=float(source.get("capital_base", 0.0)),
        verified_credits=float(source.get("verified_credits", 0.0)),
    )
    return TransferPricingScenarioResult(
        scenario_id=str(source["group_id"]),
        title=str(source["title"]),
        schedule_id=schedule_id,
        source=source,
        reported_aava=reported_aava,
        transfer_pricing_result=transfer_result,
        adjusted_aava_preview=adjusted_preview,
        liability_preview=liability_preview,
    )


def run_transfer_pricing_previews(repo_root: Path) -> TransferPricingPreviewReport:
    """Run transfer-pricing and mixed-unit preview scenarios."""

    schedules_by_id = load_schedules_by_id(repo_root)
    related_party_ai_fee = _load_group_yaml(repo_root, RELATED_PARTY_AI_FEE_ID)
    robotics_leasing = _load_group_yaml(repo_root, ROBOTICS_LEASING_ID)
    mixed_unit_group = _load_group_yaml(repo_root, MIXED_UNIT_PLATFORM_ID)
    entities = mixed_unit_group.get("entities")
    if not isinstance(entities, list):
        raise ExampleRunnerError("mixed_unit_platform_group entities must be a list")

    return TransferPricingPreviewReport(
        related_party_ai_fee=_run_transfer_scenario(related_party_ai_fee, schedules_by_id),
        robotics_leasing=_run_transfer_scenario(robotics_leasing, schedules_by_id),
        mixed_unit_group=mixed_unit_group,
        unit_compatibility=evaluate_unit_compatibility(entities),
        mixed_unit_exposure=evaluate_mixed_unit_exposure(entities),
    )
