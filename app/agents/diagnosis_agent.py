# """Diagnosis agent mapping anomalies to likely failing parts."""

# from __future__ import annotations

# from typing import Dict, List

# from app.config import WorkflowConfig
# from app.state import AnomalyInfo, DiagnosisInfo, SystemState
# from app.utils.logging_utils import append_log


# METRIC_PART_MAP: Dict[str, Dict[str, str]] = {
#     "battery_voltage": {"part_id": "P001", "part_name": "Battery"},
#     "alternator_output": {"part_id": "P002", "part_name": "Alternator"},
#     "coolant_temp": {"part_id": "P003", "part_name": "Cooling System"},
#     "brake_pad_wear": {"part_id": "P004", "part_name": "Brake Pads"},
# }


# def _severity_level(severity: float, cfg: WorkflowConfig) -> str:
#     if severity >= cfg.high_severity_threshold:
#         return "high"
#     if severity >= cfg.medium_severity_threshold:
#         return "medium"
#     return "low"


# def diagnosis_agent(state: SystemState, cfg: WorkflowConfig | None = None) -> SystemState:
#     """Create a diagnosis record from detected anomalies."""

#     cfg = cfg or WorkflowConfig()
#     append_log(state, "Diagnosis agent: evaluating anomalies.")
#     anomalies: List[AnomalyInfo] = state.get("anomalies", []) or []
#     if not anomalies:
#         append_log(state, "Diagnosis agent: no anomalies present; skipping diagnosis.")
#         state["diagnosis"] = None
#         return state

#     # Pick the most severe anomaly for prioritization.
#     primary = max(anomalies, key=lambda a: a.get("severity", 0.0))
#     metric_name = primary.get("metric_name", "unknown_metric")
#     mapping = METRIC_PART_MAP.get(
#         metric_name,
#         {"part_id": "P999", "part_name": "Unknown/General Inspection"},
#     )
#     severity = float(primary.get("severity", 0.0))
#     severity_level = _severity_level(severity, cfg)

#     diagnosis: DiagnosisInfo = {
#         "part_id": mapping["part_id"],
#         "part_name": mapping["part_name"],
#         "confidence": min(0.5 + severity / 2.0, 1.0),
#         "estimated_time_to_failure_days": max(1.0, (1.0 - severity) * 60.0),
#         "severity_level": severity_level,
#         "issue_category": "performance_degradation",
#         "supporting_metrics": [a["metric_name"] for a in anomalies],
#     }
#     state["diagnosis"] = diagnosis
#     append_log(
#         state,
#         f"Diagnosis agent: mapped metric {metric_name} to {mapping['part_name']} with severity {severity_level}.",
#     )
#     return state


"""Diagnosis agent mapping anomalies to likely failing parts."""

from __future__ import annotations

from typing import Dict, List

from app.config import WorkflowConfig
from app.state import AnomalyInfo, DiagnosisInfo, SystemState
from app.utils.logging_utils import append_log


# Dataset-aligned metric → part mapping
METRIC_PART_MAP: Dict[str, Dict[str, str]] = {
    "Battery_Voltage": {"part_id": "P001", "part_name": "Battery"},
    "Battery_SoC": {"part_id": "P001", "part_name": "Battery"},
    "Engine_Temperature": {"part_id": "P003", "part_name": "Cooling System"},
    "Brake_Pressure": {"part_id": "P004", "part_name": "Brake System"},
    "Speed": {"part_id": "P005", "part_name": "Transmission / Powertrain"},
    "Fuel_Status": {"part_id": "P006", "part_name": "Fuel System"},
    "Odometer_Reading": {"part_id": "P007", "part_name": "Wear & Tear Components"},
}


def _severity_level(severity: float, cfg: WorkflowConfig) -> str:
    if severity >= cfg.high_severity_threshold:
        return "high"
    if severity >= cfg.medium_severity_threshold:
        return "medium"
    return "low"


def diagnosis_agent(state: SystemState, cfg: WorkflowConfig | None = None) -> SystemState:
    """Create a diagnosis record from detected anomalies."""

    cfg = cfg or WorkflowConfig()
    append_log(state, "Diagnosis agent: evaluating anomalies.")

    anomalies: List[AnomalyInfo] = state.get("anomalies", []) or []
    if not anomalies:
        append_log(state, "Diagnosis agent: no anomalies present; skipping diagnosis.")
        state["diagnosis"] = None
        return state

    # Pick the most severe anomaly for prioritization
    primary = max(anomalies, key=lambda a: a.get("severity", 0.0))
    metric_name = primary.get("metric_name", "unknown_metric")

    mapping = METRIC_PART_MAP.get(
        metric_name,
        {"part_id": "P999", "part_name": "General Inspection Required"},
    )

    severity = float(primary.get("severity", 0.0))
    severity_level = _severity_level(severity, cfg)

    diagnosis: DiagnosisInfo = {
        "part_id": mapping["part_id"],
        "part_name": mapping["part_name"],
        "confidence": min(0.5 + severity / 2.0, 1.0),
        "estimated_time_to_failure_days": max(1.0, (1.0 - severity) * 60.0),
        "severity_level": severity_level,
        "issue_category": "performance_degradation",
        "supporting_metrics": [a["metric_name"] for a in anomalies],
    }

    state["diagnosis"] = diagnosis

    append_log(
        state,
        f"Diagnosis agent: mapped metric {metric_name} to "
        f"{mapping['part_name']} with severity {severity_level}.",
    )

    return state
