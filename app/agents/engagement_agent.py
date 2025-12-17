# """Engagement agent deciding customer notification strategy."""

# from __future__ import annotations

# from app.state import DiagnosisInfo, SystemState
# from app.utils.logging_utils import append_log


# def engagement_agent(state: SystemState) -> SystemState:
#     """Decide whether to notify customer and craft the message."""

#     append_log(state, "Engagement agent: evaluating notification need.")
#     diagnosis: DiagnosisInfo | None = state.get("diagnosis")
#     if not diagnosis:
#         append_log(state, "Engagement agent: no diagnosis available; skipping notification.")
#         state["customer_notified"] = False
#         state["notification_message"] = ""
#         return state

#     severity = diagnosis.get("severity_level", "low")
#     notify = severity in {"medium", "high"}
#     message = ""
#     if notify:
#         message = (
#             f"Detected potential issue with {diagnosis.get('part_name','component')} "
#             f"(severity: {severity}). Recommended action: schedule service within "
#             f"{max(1, int(diagnosis.get('estimated_time_to_failure_days', 30)))} days."
#         )
#         append_log(state, f"Engagement agent: customer will be notified. Message='{message}'")
#     else:
#         append_log(state, "Engagement agent: severity low; monitoring without notification.")

#     state["customer_notified"] = notify
#     state["notification_message"] = message
#     return state


"""Engagement agent deciding customer notification strategy."""

from __future__ import annotations

from app.state import DiagnosisInfo, SystemState
from app.utils.logging_utils import append_log


def engagement_agent(state: SystemState) -> SystemState:
    """Decide whether to notify customer and craft the message."""

    append_log(state, "Engagement agent: evaluating notification need.")

    diagnosis: DiagnosisInfo | None = state.get("diagnosis")
    if not diagnosis:
        append_log(state, "Engagement agent: no diagnosis available; skipping notification.")
        state["customer_notified"] = False
        state["notification_message"] = ""
        return state

    severity = diagnosis.get("severity_level", "low")
    notify = severity in {"medium", "high"}

    # Dataset-aligned fields (optional)
    customer_id = state.get("customer_id", "Customer")
    vehicle_id = state.get("vehicle_id", "your vehicle")

    message = ""
    if notify:
        message = (
            f"{customer_id}, we detected a potential issue with {vehicle_id} "
            f"related to {diagnosis.get('part_name', 'a vehicle component')} "
            f"(severity: {severity}). Recommended action: schedule service within "
            f"{max(1, int(diagnosis.get('estimated_time_to_failure_days', 30)))} days."
        )
        append_log(state, f"Engagement agent: customer will be notified. Message='{message}'")
    else:
        append_log(state, "Engagement agent: severity low; monitoring without notification.")

    state["customer_notified"] = notify
    state["notification_message"] = message
    return state
