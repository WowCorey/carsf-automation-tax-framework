"""Runner for grouped-entity and apportionment preview examples."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .aggregation import AggregationResult, EntityInput, evaluate_group_aggregation, risk_rank
from .apportionment import ApportionmentResult, evaluate_apportionment
from .example_runner import ExampleResult, load_yaml_file, run_example


SPLIT_STRUCTURE_ID = "logistics_split_structure"
MIXED_APPORTIONMENT_ID = "mixed_logistics_warehousing_platform"
HYBRID_STRESS_ID = "logistics_hybrid_stress"
GROUPED_REPORT_STATUS = "illustrative_grouped_entity_and_apportionment_previews_only"
GROUPED_NON_CLAIMS = [
    "Not legal grouping analysis.",
    "Not tax-law attribution.",
    "Not Treasury or ATO guidance.",
    "Not economic validation.",
    "Not a real tax assessment.",
    "All grouped and apportioned values use illustrative placeholder inputs.",
]
APPORTIONMENT_SCOPE_NOTE = (
    "This example currently uses the combined logistics_warehousing prototype schedule for all activity slices. "
    "It tests apportionment plumbing and share-validation logic, not final cross-sector schedule blending. "
    "True multi-schedule blending requires additional calibrated sector schedules."
)


@dataclass(frozen=True)
class GroupedPreviewResult:
    """Combined output for grouped/apportionment preview reporting."""

    split_structure: dict[str, Any]
    split_entities: list[EntityInput]
    aggregation_result: AggregationResult
    mixed_apportionment: dict[str, Any]
    apportionment_result: ApportionmentResult
    hybrid_stress_result: ExampleResult

    def to_jsonable(self) -> dict[str, Any]:
        return {
            "split_structure": self.split_structure,
            "split_entities": [asdict(entity) for entity in self.split_entities],
            "aggregation_result": asdict(self.aggregation_result),
            "mixed_apportionment": self.mixed_apportionment,
            "apportionment_result": asdict(self.apportionment_result),
            "hybrid_stress_result": self.hybrid_stress_result.to_jsonable(),
        }


def load_schedules_by_id(repo_root: Path) -> dict[str, dict[str, Any]]:
    schedules: dict[str, dict[str, Any]] = {}
    for path in sorted((repo_root / "schedules").glob("*.yaml")):
        data = load_yaml_file(path, "schedule file")
        schedule_id = data.get("schedule_id")
        if schedule_id:
            schedules[str(schedule_id)] = data
    return schedules


def _load_group_yaml(repo_root: Path, group_id: str) -> dict[str, Any]:
    return load_yaml_file(repo_root / "examples" / "groups" / f"{group_id}.yaml", "group example file")


def _load_hybrid_stress(repo_root: Path, schedules_by_id: dict[str, dict[str, Any]]) -> ExampleResult:
    example = load_yaml_file(repo_root / "examples" / f"{HYBRID_STRESS_ID}.yaml", "hybrid stress example file")
    schedule_id = str(example["schedule_used"])
    return run_example(example, schedules_by_id[schedule_id])


def run_grouped_previews(repo_root: Path) -> GroupedPreviewResult:
    schedules_by_id = load_schedules_by_id(repo_root)
    split_structure = _load_group_yaml(repo_root, SPLIT_STRUCTURE_ID)
    mixed_apportionment = _load_group_yaml(repo_root, MIXED_APPORTIONMENT_ID)
    aggregation_result = evaluate_group_aggregation(split_structure, split_structure["entities"])
    split_entities = [EntityInput(**entity) for entity in split_structure["entities"]]
    apportionment_result = evaluate_apportionment(mixed_apportionment, schedules_by_id)
    hybrid_stress_result = _load_hybrid_stress(repo_root, schedules_by_id)
    return GroupedPreviewResult(
        split_structure=split_structure,
        split_entities=split_entities,
        aggregation_result=aggregation_result,
        mixed_apportionment=mixed_apportionment,
        apportionment_result=apportionment_result,
        hybrid_stress_result=hybrid_stress_result,
    )


def standalone_max_risk(entities: list[EntityInput]) -> str:
    return max((entity.standalone_risk for entity in entities), key=risk_rank, default="low")
