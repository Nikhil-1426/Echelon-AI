"""Helper utilities for structured logging within the workflow state."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import List

from app.state import SystemState


def append_log(state: SystemState, message: str) -> None:
    """Append a timestamped log entry to the shared state."""

    timestamp = datetime.now(timezone.utc).isoformat()
    log_entry = f"[{timestamp}] {message}"
    if "logs" not in state or state["logs"] is None:
        state["logs"] = []
    state["logs"].append(log_entry)


def extend_logs(state: SystemState, messages: List[str]) -> None:
    """Append multiple log entries to the shared state."""

    for msg in messages:
        append_log(state, msg)


