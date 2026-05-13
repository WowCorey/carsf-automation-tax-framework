from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from carsf import AIIWeights, QLCWeights, Worker
from carsf.aii import automation_intensity_index
from carsf.frv import net_labour_tax_gap
from carsf.libc import human_labour_equivalent
from carsf.qlc import qualified_labour_contribution_firm


REPO_ROOT = Path(__file__).resolve().parents[2]


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def load_schedule(schedule_id: str) -> dict:
    return load_yaml(REPO_ROOT / "schedules" / f"{schedule_id}.yaml")


def load_example(example_id: str) -> dict:
    return load_yaml(REPO_ROOT / "examples" / f"{example_id}.yaml")


def qlc_weights_from_schedule(schedule: dict) -> QLCWeights:
    weights = schedule["qlc"]["weights"]
    return QLCWeights(
        alpha=weights["alpha_wage_quality"],
        beta=weights["beta_job_security"],
        gamma=weights["gamma_skill_development"],
        delta=weights["delta_australian_nexus"],
        qlc_max_multiplier=schedule["qlc"]["qlc_max_multiplier"],
    )


def aii_weights_from_schedule(schedule: dict) -> AIIWeights:
    weights = schedule["aii"]["weights"]
    return AIIWeights(
        compute_ratio=weights["compute_ratio"],
        auto_decision_ratio=weights["auto_decision_ratio"],
        robotics_capital_ratio=weights["robotics_capital_ratio"],
        auto_process_share=weights["auto_process_share"],
    )


def example_nltg(example_id: str) -> float:
    example = load_example(example_id)
    schedule = load_schedule(example["schedule_used"])
    workers = [
        Worker(**{key: value for key, value in worker.items() if key != "role"})
        for worker in example["workers"]
    ]
    qlc = qualified_labour_contribution_firm(workers, qlc_weights_from_schedule(schedule))
    hle = human_labour_equivalent(
        example["output"]["value"],
        schedule["opfte_libc_placeholder"]["value"],
    )
    automation = example["automation_components"]
    aii = automation_intensity_index(
        automation["compute_ratio"],
        automation["auto_decision_ratio"],
        automation["robotics_capital_ratio"],
        automation["auto_process_share"],
        aii_weights_from_schedule(schedule),
    )
    return net_labour_tax_gap(hle, aii, qlc)


@pytest.fixture
def repo_root() -> Path:
    return REPO_ROOT
