"""End-to-end runner for illustrative CARSF worked examples."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from .aii import automation_intensity_index
from .aava import australian_automated_value_added
from .avoidance import AvoidanceResult, evaluate_avoidance_risk
from .coverage import coverage_measures, format_coverage_ratio
from .frv import net_labour_tax_gap
from .grouping import GroupingRiskResult, evaluate_grouping_risk
from .levy import calculate_liability
from .libc import human_labour_equivalent
from .qlc import qualified_labour_contribution_firm
from .safe_harbour import SafeHarbourResult, evaluate_safe_harbour
from .types import AIIWeights, LevyParameters, QLCWeights, Worker


VERSION_LABEL = "CARSF V1.5 prototype"
OUTPUT_STATUS = "illustrative_placeholder_outputs_only"
EXAMPLE_IDS = [
    "mechanic_traditional",
    "mechanic_ai_admin",
    "mechanic_robotic",
    "logistics_human_heavy",
    "logistics_hybrid",
    "logistics_ai_platform",
]
NON_CLAIMS = [
    "Not legal advice.",
    "Not tax advice.",
    "Not Treasury or ATO guidance.",
    "Not economic validation.",
    "Not a real tax-payable calculation.",
    "All outputs use illustrative placeholder values unless explicitly labelled otherwise.",
]


class ExampleRunnerError(RuntimeError):
    """Raised for input, validation, or report-generation failures."""


@dataclass(frozen=True)
class ExampleOutputs:
    qlc: float
    opfte_libc: float
    hle: float
    aii: float
    nltg: float
    aava: float
    ael_raw: float
    ael_payable: float
    shortfall: float
    arl: float
    credits: float
    liability: float
    cars_i: float | None
    coverage_ratio: float | None
    coverage_ratio_display: str


@dataclass(frozen=True)
class ExampleResult:
    id: str
    name: str
    schedule: str
    sector: str
    business_description: str
    inputs: dict[str, Any]
    outputs: ExampleOutputs
    formula_trace: list[str]
    interpretation: str
    safe_harbour_result: SafeHarbourResult
    avoidance_result: AvoidanceResult
    grouping_risk_result: GroupingRiskResult
    warnings: list[str] = field(default_factory=list)
    evidence_labels: list[str] = field(default_factory=list)
    limitation_notes: list[str] = field(default_factory=list)
    red_team_notes: dict[str, Any] = field(default_factory=dict)

    def to_jsonable(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["outputs"] = asdict(self.outputs)
        return payload


def require_mapping(data: Any, label: str) -> dict[str, Any]:
    if not isinstance(data, dict):
        raise ExampleRunnerError(f"{label} must parse to a YAML mapping")
    return data


def load_yaml_file(path: Path, label: str) -> dict[str, Any]:
    if not path.exists():
        raise ExampleRunnerError(f"Missing {label}: {path}")
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ExampleRunnerError(f"YAML parse failed for {label} {path}: {exc}") from exc
    return require_mapping(loaded, f"{label} {path}")


def require_field(data: dict[str, Any], path: str) -> Any:
    current: Any = data
    for part in path.split("."):
        if not isinstance(current, dict) or part not in current:
            raise ExampleRunnerError(f"Required field missing: {path}")
        current = current[part]
    return current


def validate_placeholder_labels(example: dict[str, Any], schedule: dict[str, Any]) -> list[str]:
    labels = [
        f"example.status={require_field(example, 'status')}",
        f"example.placeholder_notice={require_field(example, 'placeholder_notice')}",
        f"schedule.status={require_field(schedule, 'status')}",
        f"schedule.calibration_status={require_field(schedule, 'calibration_status')}",
        f"schedule.opfte_libc.evidence_label={require_field(schedule, 'opfte_libc_placeholder.evidence_label')}",
        f"schedule.frv.evidence_label={require_field(schedule, 'frv.evidence_label')}",
    ]
    if "placeholder" not in str(example["status"]).lower():
        raise ExampleRunnerError("Placeholder assumptions missing label: example.status")
    if "placeholder" not in str(example["placeholder_notice"]).lower():
        raise ExampleRunnerError("Placeholder assumptions missing label: example.placeholder_notice")
    if "placeholder" not in str(schedule["calibration_status"]).lower():
        raise ExampleRunnerError("Placeholder assumptions missing label: schedule.calibration_status")
    if "placeholder" not in str(schedule["opfte_libc_placeholder"]["evidence_label"]).lower():
        raise ExampleRunnerError("Placeholder assumptions missing label: schedule.opfte_libc_placeholder.evidence_label")
    if "placeholder" not in str(schedule["frv"]["evidence_label"]).lower():
        raise ExampleRunnerError("Placeholder assumptions missing label: schedule.frv.evidence_label")
    return labels


def qlc_weights_from_schedule(schedule: dict[str, Any]) -> QLCWeights:
    weights = require_field(schedule, "qlc.weights")
    return QLCWeights(
        alpha=require_field(weights, "alpha_wage_quality"),
        beta=require_field(weights, "beta_job_security"),
        gamma=require_field(weights, "gamma_skill_development"),
        delta=require_field(weights, "delta_australian_nexus"),
        qlc_max_multiplier=require_field(schedule, "qlc.qlc_max_multiplier"),
    )


def aii_weights_from_schedule(schedule: dict[str, Any]) -> AIIWeights:
    weights = require_field(schedule, "aii.weights")
    return AIIWeights(
        compute_ratio=require_field(weights, "compute_ratio"),
        auto_decision_ratio=require_field(weights, "auto_decision_ratio"),
        robotics_capital_ratio=require_field(weights, "robotics_capital_ratio"),
        auto_process_share=require_field(weights, "auto_process_share"),
    )


def levy_params_from_schedule(schedule: dict[str, Any]) -> LevyParameters:
    caps = require_field(schedule, "caps")
    return LevyParameters(
        frv_standard=require_field(schedule, "frv.standard_placeholder"),
        lambda_sector=require_field(caps, "lambda_sector"),
        lambda_combined=require_field(caps, "LAMBDA_sector"),
        theta=require_field(caps, "theta"),
        uplift_rate=require_field(caps, "uplift_rate"),
        rent_tax_rate=require_field(caps, "rent_tax_rate"),
    )


def workers_from_example(example: dict[str, Any]) -> list[Worker]:
    workers = require_field(example, "workers")
    if not isinstance(workers, list) or not workers:
        raise ExampleRunnerError("Required field missing or empty: workers")
    result: list[Worker] = []
    for index, worker in enumerate(workers):
        if not isinstance(worker, dict):
            raise ExampleRunnerError(f"Worker entry {index} must be a mapping")
        result.append(
            Worker(
                annual_hours=require_field(worker, "annual_hours"),
                wage_quality=require_field(worker, "wage_quality"),
                job_security=require_field(worker, "job_security"),
                skill_development=require_field(worker, "skill_development"),
                australian_nexus=require_field(worker, "australian_nexus"),
            )
        )
    return result


def build_inputs_summary(example: dict[str, Any], schedule: dict[str, Any]) -> dict[str, Any]:
    caps = require_field(schedule, "caps")
    return {
        "output": require_field(example, "output"),
        "workers": require_field(example, "workers"),
        "automation_components": require_field(example, "automation_components"),
        "aava_inputs": require_field(example, "aava_inputs"),
        "capital_base": require_field(example, "capital_base"),
        "credits": require_field(example, "credits"),
        "risk_metadata": example.get("risk_metadata", {}),
        "schedule_placeholders": {
            "opfte_libc_placeholder": require_field(schedule, "opfte_libc_placeholder"),
            "frv": require_field(schedule, "frv"),
            "caps": {
                "ael_capacity_cap_rate": require_field(caps, "lambda_sector"),
                "combined_liability_cap_rate": require_field(caps, "LAMBDA_sector"),
                "credit_cap_rate": require_field(caps, "theta"),
                "uplift_rate": require_field(caps, "uplift_rate"),
                "rent_tax_rate": require_field(caps, "rent_tax_rate"),
            },
        },
    }


def interpretation_for_example(example_id: str, outputs: ExampleOutputs) -> str:
    interpretations = {
        "mechanic_traditional": (
            "Traditional mechanic shop: high human labour contribution and low automation "
            "intensity produce low or zero NLTG. This illustrative case should not be "
            "treated as automation-heavy."
        ),
        "mechanic_ai_admin": (
            "AI-admin mechanic shop: AI is mainly supporting booking, compliance, customer "
            "support, and diagnostics while humans still perform core repair work. The "
            "low NLTG relative to the robotic shop illustrates the distinction between "
            "worker-assist/admin AI and labour-substituting robotics."
        ),
        "mechanic_robotic": (
            "Fully robotic mechanic shop: high automation intensity and low QLC relative "
            "to output create a materially higher NLTG than the traditional shop. The "
            "result is a stronger liability or recorded shortfall signal in this prototype."
        ),
        "logistics_human_heavy": (
            "Human-heavy logistics company: a larger human workforce and lower automation "
            "intensity produce lower NLTG than the automated logistics examples."
        ),
        "logistics_hybrid": (
            "Hybrid logistics company: AII is intermediate, but NLTG and liability "
            "remain zero under the current placeholders because QLC remains strong. "
            "This demonstrates that hybrid automation is not automatically penalised. "
            "A later stress variant should test non-zero but intermediate NLTG."
        ),
        "logistics_ai_platform": (
            "AI logistics platform: high automated productive capacity and low QLC relative "
            "to output create the strongest stress case among the six examples."
        ),
        "logistics_hybrid_stress": (
            "Hybrid logistics stress variant: automation is meaningful and NLTG is non-zero, "
            "but the result remains below the thin-labour AI logistics platform because "
            "substantial Australian labour is still present."
        ),
    }
    return interpretations.get(
        example_id,
        f"Prototype interpretation unavailable. NLTG is {outputs.nltg:.2f}.",
    )


def run_example(example: dict[str, Any], schedule: dict[str, Any]) -> ExampleResult:
    """Run one illustrative example through the CARSF formula chain."""

    try:
        example_id = str(require_field(example, "example_id"))
        schedule_id = str(require_field(example, "schedule_used"))
        if schedule_id != require_field(schedule, "schedule_id"):
            raise ExampleRunnerError(
                f"Schedule mismatch for {example_id}: example uses {schedule_id}, "
                f"loaded schedule is {schedule.get('schedule_id')}"
            )
        evidence_labels = validate_placeholder_labels(example, schedule)
        workers = workers_from_example(example)
        qlc = qualified_labour_contribution_firm(workers, qlc_weights_from_schedule(schedule))
        opfte_libc = require_field(schedule, "opfte_libc_placeholder.value")
        hle = human_labour_equivalent(require_field(example, "output.value"), opfte_libc)
        automation = require_field(example, "automation_components")
        aii = automation_intensity_index(
            require_field(automation, "compute_ratio"),
            require_field(automation, "auto_decision_ratio"),
            require_field(automation, "robotics_capital_ratio"),
            require_field(automation, "auto_process_share"),
            aii_weights_from_schedule(schedule),
        )
        nltg = net_labour_tax_gap(hle, aii, qlc)
        aava_inputs = require_field(example, "aava_inputs")
        aava = australian_automated_value_added(
            require_field(aava_inputs, "australian_attributable_revenue"),
            require_field(aava_inputs, "verified_non_automation_input_costs"),
            require_field(aava_inputs, "verified_qlc_wage_cost"),
        )
        levy = calculate_liability(
            nltg=nltg,
            aava=aava,
            capital_base=require_field(example, "capital_base"),
            verified_credits=require_field(example, "credits.verified_credits"),
            params=levy_params_from_schedule(schedule),
        )
        coverage_input = example.get("coverage_inputs")
        if coverage_input:
            coverage = coverage_measures(
                require_field(coverage_input, "national_automation_fiscal_damage"),
                require_field(coverage_input, "automation_revenue_captured"),
            )
            cars_i_value: float | None = coverage.cars_i
            coverage_ratio_value = coverage.coverage_ratio
            coverage_display = format_coverage_ratio(coverage.coverage_ratio)
            coverage_notes = list(coverage.notes)
        else:
            cars_i_value = None
            coverage_ratio_value = None
            coverage_display = "N/A - no national monitoring inputs"
            coverage_notes = ["Coverage metrics not calculated because this example has no national monitoring inputs."]
        outputs = ExampleOutputs(
            qlc=qlc,
            opfte_libc=opfte_libc,
            hle=hle,
            aii=aii,
            nltg=nltg,
            aava=aava,
            ael_raw=levy.ael_raw,
            ael_payable=levy.ael_payable,
            shortfall=levy.shortfall,
            arl=levy.arl,
            credits=levy.credits,
            liability=levy.liability,
            cars_i=cars_i_value,
            coverage_ratio=coverage_ratio_value,
            coverage_ratio_display=coverage_display,
        )
        safe_harbour_result = evaluate_safe_harbour(example, schedule, outputs)
        avoidance_result = evaluate_avoidance_risk(example, schedule, outputs)
        grouping_risk_result = evaluate_grouping_risk(example, outputs)
        warnings = [
            "Illustrative placeholder output only.",
            "Do not use this result to estimate real tax payable.",
            "No legal, tax, Treasury, ATO, or economic validation is implied.",
            "Safe harbour and avoidance outputs are prototype review flags, not legal findings.",
            *coverage_notes,
        ]
        if require_field(example, "status") != "illustrative_placeholder":
            warnings.append("Example status is not the expected illustrative_placeholder label.")
        if require_field(schedule, "calibration_status") != "illustrative_placeholder_values_only":
            warnings.append("Schedule calibration status is not the expected placeholder label.")
        trace = [
            f"QLC = sum capped worker QLC = {outputs.qlc:.4f}",
            f"OPFTE_LIBC = schedule placeholder benchmark = {outputs.opfte_libc:.4f}",
            f"HLE = output / OPFTE_LIBC = {outputs.hle:.4f}",
            f"AII = weighted bounded automation components = {outputs.aii:.4f}",
            f"NLTG = max(0, HLE * AII - QLC) = {outputs.nltg:.4f}",
            f"AAVA = revenue - non-automation costs - QLC wage costs = {outputs.aava:.2f}",
            f"AEL raw = NLTG * FRV standard = {outputs.ael_raw:.2f}",
            f"AEL payable = min(AEL raw, lambda_sector * AAVA) = {outputs.ael_payable:.2f}",
            f"Shortfall = AEL raw - AEL payable = {outputs.shortfall:.2f}",
            f"ARL = PRRT-inspired uplift logic result = {outputs.arl:.2f}",
            f"Credits = capped verified credits = {outputs.credits:.2f}",
            f"Final liability = capped combined liability = {outputs.liability:.2f}",
        ]
        limitation_notes = [
            str(require_field(example, "placeholder_notice")),
            "Schedule values are not calibrated.",
            "AAVA deductibility remains a prototype taxonomy.",
            "Safe harbour, anti-avoidance, and grouping checks are executable review flags only.",
            "Safe harbour classification does not automatically reduce or erase liability in this build.",
            "Related-party, offshore, and sector-classification outputs are not legal or tax conclusions.",
        ]
        return ExampleResult(
            id=example_id,
            name=example_id.replace("_", " ").title(),
            schedule=schedule_id,
            sector=str(require_field(schedule, "schedule_name")),
            business_description=str(require_field(example, "business_description")),
            inputs=build_inputs_summary(example, schedule),
            outputs=outputs,
            formula_trace=trace,
            interpretation=interpretation_for_example(example_id, outputs),
            safe_harbour_result=safe_harbour_result,
            avoidance_result=avoidance_result,
            grouping_risk_result=grouping_risk_result,
            warnings=warnings,
            evidence_labels=evidence_labels,
            limitation_notes=limitation_notes,
            red_team_notes=require_field(example, "red_team_notes"),
        )
    except ValueError as exc:
        raise ExampleRunnerError(f"Model validation failed for {example.get('example_id', '<unknown>')}: {exc}") from exc


def load_examples(repo_root: Path) -> list[tuple[dict[str, Any], dict[str, Any]]]:
    loaded: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for example_id in EXAMPLE_IDS:
        example_path = repo_root / "examples" / f"{example_id}.yaml"
        example = load_yaml_file(example_path, "example file")
        schedule_id = require_field(example, "schedule_used")
        schedule_path = repo_root / "schedules" / f"{schedule_id}.yaml"
        schedule = load_yaml_file(schedule_path, "schedule file")
        loaded.append((example, schedule))
    return loaded


def run_all_examples(repo_root: Path) -> list[ExampleResult]:
    return [run_example(example, schedule) for example, schedule in load_examples(repo_root)]


def report_metadata() -> dict[str, Any]:
    return {
        "generated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "version": VERSION_LABEL,
        "status": OUTPUT_STATUS,
        "non_claims": NON_CLAIMS,
    }
