# """Scheduling agent for workshop allocation."""

# from __future__ import annotations

# from datetime import datetime, timedelta
# from typing import List

# from app.state import DiagnosisInfo, ScheduleInfo, SystemState
# from app.utils.logging_utils import append_log


# WORKSHOPS = [
#     {"workshop_id": "W001", "name": "City Central Auto", "location": "central", "capacity": 5},
#     {"workshop_id": "W002", "name": "Northside Motors", "location": "north", "capacity": 3},
#     {"workshop_id": "W003", "name": "Express Auto South", "location": "south", "capacity": 4},
# ]


# def _priority(severity: str) -> str:
#     if severity == "high":
#         return "high"
#     if severity == "medium":
#         return "medium"
#     return "low"


# def scheduling_agent(state: SystemState) -> SystemState:
#     """Allocate a workshop slot using a simple FCFS + priority heuristic."""

#     append_log(state, "Scheduling agent: determining workshop slot.")
#     diagnosis: DiagnosisInfo | None = state.get("diagnosis")
#     if not diagnosis:
#         append_log(state, "Scheduling agent: no diagnosis available; skipping scheduling.")
#         state["schedule"] = None
#         return state

#     severity = diagnosis.get("severity_level", "low")
#     priority_tag = _priority(severity)

#     # Mock FCFS + priority: pick the first workshop; in real flow, order by capacity/priority queue.
#     chosen = WORKSHOPS[0]
#     slot_time = (datetime.utcnow() + timedelta(days=1)).isoformat()
#     schedule: ScheduleInfo = {
#         "workshop_id": chosen["workshop_id"],
#         "workshop_name": chosen["name"],
#         "slot_time": slot_time,
#         "mechanic_id": "M-1001",
#         "priority_tag": priority_tag,  # priority respected at queue level; non-preemptive execution
#     }

#     state["schedule"] = schedule
#     append_log(
#         state,
#         f"Scheduling agent: assigned workshop {chosen['name']} at {slot_time} with priority {priority_tag}.",
#     )
#     return state


"""Scheduling agent for workshop allocation."""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import List

from app.state import DiagnosisInfo, ScheduleInfo, SystemState
from app.utils.logging_utils import append_log


WORKSHOPS = [
    {"workshop_id": "W001", "name": "City Central Auto", "location": "central", "capacity": 5},
    {"workshop_id": "W002", "name": "Northside Motors", "location": "north", "capacity": 3},
    {"workshop_id": "W003", "name": "Express Auto South", "location": "south", "capacity": 4},
]


def _priority(severity: str) -> str:
    if severity == "high":
        return "high"
    if severity == "medium":
        return "medium"
    return "low"


def scheduling_agent(state: SystemState) -> SystemState:
    """Allocate a workshop slot using a simple FCFS + priority heuristic."""

    append_log(state, "Scheduling agent: determining workshop slot.")

    diagnosis: DiagnosisInfo | None = state.get("diagnosis")
    if not diagnosis:
        append_log(state, "Scheduling agent: no diagnosis available; skipping scheduling.")
        state["schedule"] = None
        return state

    severity = diagnosis.get("severity_level", "low")
    priority_tag = _priority(severity)

    # Dataset-aligned identifiers (for traceability only)
    customer_id = state.get("customer_id", "C-NA")
    vehicle_id = state.get("vehicle_id", "V-NA")

    # FCFS mock allocation (dataset has no live capacity feed)
    chosen = WORKSHOPS[0]
    slot_time = (datetime.utcnow() + timedelta(days=1)).isoformat()

    schedule: ScheduleInfo = {
        "workshop_id": chosen["workshop_id"],
        "workshop_name": chosen["name"],
        "slot_time": slot_time,
        "mechanic_id": "M-1001",
        "priority_tag": priority_tag,
    }

    state["schedule"] = schedule

    append_log(
        state,
        f"Scheduling agent: assigned workshop {chosen['name']} "
        f"to {customer_id}/{vehicle_id} at {slot_time} "
        f"with priority {priority_tag}.",
    )

    return state
