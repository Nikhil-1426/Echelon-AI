# """Preprocessing node to normalize incoming telemetry."""

# from __future__ import annotations

# from typing import List

# from app.state import SystemState, VehicleMetricPoint
# from app.utils.logging_utils import append_log


# def ingest_agent(state: SystemState) -> SystemState:
#     """Ensure telemetry is sorted and ready for downstream processing."""

#     append_log(state, "Ingest agent: starting preprocessing of telemetry.")
#     raw_points: List[VehicleMetricPoint] = state.get("raw_metrics", []) or []
#     sorted_points = sorted(raw_points, key=lambda p: p["timestamp"])
#     state["raw_metrics"] = sorted_points
#     append_log(
#         state,
#         f"Ingest agent: normalized telemetry ordering, points={len(sorted_points)}.",
#     )
#     return state

"""Preprocessing node to normalize incoming telemetry."""

from __future__ import annotations

from typing import List

from app.state import SystemState, VehicleMetricPoint
from app.utils.logging_utils import append_log


def ingest_agent(state: SystemState) -> SystemState:
    """Ensure telemetry is sorted and ready for downstream processing."""

    append_log(state, "Ingest agent: starting preprocessing of telemetry.")

    raw_points: List[VehicleMetricPoint] = state.get("raw_metrics", []) or []

    # Dataset-aligned safeguard:
    # CSV-derived telemetry may not contain explicit timestamps
    if raw_points and "timestamp" in raw_points[0]:
        sorted_points = sorted(raw_points, key=lambda p: p.get("timestamp", 0))
    else:
        sorted_points = raw_points  # preserve column-order time sequence

    state["raw_metrics"] = sorted_points

    append_log(
        state,
        f"Ingest agent: normalized telemetry ordering, points={len(sorted_points)}.",
    )

    return state

