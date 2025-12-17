# """Manufacturing insights agent producing structured OEM payloads."""

# from __future__ import annotations

# from datetime import datetime, timezone

# from app.config import WorkflowConfig
# from app.state import ManufacturingPayload, SystemState
# from app.utils.logging_utils import append_log


# def manufacturing_insights_agent(
#     state: SystemState, cfg: WorkflowConfig | None = None
# ) -> SystemState:
#     """Build payload for downstream OEM/Neo4j/PostgreSQL sinks."""

#     cfg = cfg or WorkflowConfig()
#     append_log(state, "Manufacturing agent: assembling payload.")

#     diagnosis = state.get("diagnosis") or {}
#     feedback = state.get("feedback") or {}
#     schedule = state.get("schedule") or {}

#     payload: ManufacturingPayload = {
#         "vehicle_id": state.get("vehicle_id", "unknown"),
#         "model": state.get("model", "unknown"),
#         "variant": state.get("variant", "base"),
#         "user_segment": state.get("user_segment", cfg.default_user_segment),
#         "failure_part_id": diagnosis.get("part_id", "P999"),
#         "failure_part_name": diagnosis.get("part_name", "Unknown"),
#         "issue_category": diagnosis.get("issue_category", "unspecified"),
#         "workshop_id": schedule.get("workshop_id", "W-NA"),
#         "repair_time_hours": float(feedback.get("repair_time_hours", 0.0)),
#         "diagnosis_correct": bool(feedback.get("diagnosis_correct", False)),
#         "timestamp": datetime.now(timezone.utc).isoformat(),
#     }

#     state["manufacturing_payload"] = payload
#     append_log(state, f"Manufacturing agent: payload ready for OEM analytics: {payload}.")
#     return state

"""Manufacturing insights agent producing structured OEM payloads."""

from __future__ import annotations

from datetime import datetime, timezone

from app.config import WorkflowConfig
from app.state import ManufacturingPayload, SystemState
from app.utils.logging_utils import append_log


def manufacturing_insights_agent(
    state: SystemState, cfg: WorkflowConfig | None = None
) -> SystemState:
    """Build payload for downstream OEM/Neo4j/PostgreSQL sinks."""

    cfg = cfg or WorkflowConfig()
    append_log(state, "Manufacturing agent: assembling payload.")

    diagnosis = state.get("diagnosis") or {}
    feedback = state.get("feedback") or {}
    schedule = state.get("schedule") or {}

    payload: ManufacturingPayload = {
        # Dataset-aligned identifiers
        "vehicle_id": state.get("vehicle_id", "unknown"),
        "model": state.get("model", "unknown"),
        "supplier_id": state.get("supplier_id", "S-NA"),
        "customer_id": state.get("customer_id", "C-NA"),

        # Failure intelligence
        "failure_part_id": diagnosis.get("part_id", "P999"),
        "failure_part_name": diagnosis.get("part_name", "Unknown"),
        "issue_category": diagnosis.get("issue_category", "unspecified"),

        # Service feedback loop
        "workshop_id": schedule.get("workshop_id", "W-NA"),
        "repair_time_hours": float(feedback.get("repair_time_hours", 0.0)),
        "diagnosis_correct": bool(feedback.get("diagnosis_correct", False)),

        # Meta
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    state["manufacturing_payload"] = payload

    append_log(
        state,
        f"Manufacturing agent: payload ready for OEM analytics: {payload}.",
    )

    return state

