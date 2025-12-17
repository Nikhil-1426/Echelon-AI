# """Feedback agent simulating post-service signals."""

# from __future__ import annotations

# import random
# from typing import Any

# from app.state import FeedbackInfo, ScheduleInfo, SystemState
# from app.utils.logging_utils import append_log


# def feedback_agent(state: SystemState) -> SystemState:
#     """Simulate feedback collection for visualization and meta-learning."""

#     append_log(state, "Feedback agent: collecting simulated feedback.")
#     schedule: ScheduleInfo | None = state.get("schedule")
#     random.seed(state.get("vehicle_id", "seed"))

#     feedback: FeedbackInfo = {
#         "customer_rating": round(random.uniform(3.5, 5.0), 2),
#         "customer_comments": "Service completed. Vehicle performance improved.",
#         "workshop_comments": "Replaced suspected component; validated with test drive.",
#         "repair_time_hours": round(random.uniform(2.0, 5.0), 1),
#         "diagnosis_correct": random.choice([True, True, False]),
#     }

#     state["feedback"] = feedback
#     append_log(
#         state,
#         f"Feedback agent: captured rating {feedback['customer_rating']} with correctness={feedback['diagnosis_correct']}.",
#     )
#     return state


"""Feedback agent simulating post-service signals."""

from __future__ import annotations

import random
from typing import Any

from app.state import FeedbackInfo, ScheduleInfo, SystemState
from app.utils.logging_utils import append_log


def feedback_agent(state: SystemState) -> SystemState:
    """Simulate feedback collection for visualization and meta-learning."""

    append_log(state, "Feedback agent: collecting simulated feedback.")

    schedule: ScheduleInfo | None = state.get("schedule")

    # Dataset-aligned identifiers
    vehicle_id = state.get("vehicle_id", "vehicle")
    customer_id = state.get("customer_id", "customer")
    diagnosis = state.get("diagnosis", {})

    # Stable randomness per vehicle (important for reproducibility)
    random.seed(vehicle_id)

    part_name = diagnosis.get("part_name", "component")

    feedback: FeedbackInfo = {
        "customer_rating": round(random.uniform(3.5, 5.0), 2),
        "customer_comments": (
            f"Service completed for {vehicle_id}. "
            f"Performance improved after {part_name} servicing."
        ),
        "workshop_comments": (
            f"Inspected and addressed {part_name}. "
            f"Post-repair diagnostics within normal range."
        ),
        "repair_time_hours": round(random.uniform(2.0, 5.0), 1),
        "diagnosis_correct": random.choice([True, True, False]),
    }

    state["feedback"] = feedback

    append_log(
        state,
        f"Feedback agent: captured rating {feedback['customer_rating']} "
        f"for {customer_id}/{vehicle_id} with correctness={feedback['diagnosis_correct']}.",
    )

    return state
