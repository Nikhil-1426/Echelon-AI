"""LangGraph workflow definition for the agentic aftersales ecosystem."""

from __future__ import annotations

from typing import Callable

from langgraph.graph import END, StateGraph

from app.agents import (
    build_anomaly_agent,
    diagnosis_agent,
    engagement_agent,
    feedback_agent,
    ingest_agent,
    manufacturing_insights_agent,
    scheduling_agent,
)
from app.config import WorkflowConfig
from app.models.lstm_anomaly import LSTMAnomalyDetector
from app.state import SystemState
from app.utils.logging_utils import append_log


def _engagement_branch(state: SystemState) -> str:
    """Branching logic after engagement based on severity."""

    diagnosis = state.get("diagnosis")
    if not diagnosis:
        return "feedback"
    severity = diagnosis.get("severity_level", "low")
    if severity in {"medium", "high"}:
        return "schedule"
    return "feedback"


def build_graph(model: LSTMAnomalyDetector, cfg: WorkflowConfig | None = None):
    """Construct and compile the LangGraph StateGraph."""

    cfg = cfg or WorkflowConfig()

    graph = StateGraph(SystemState)

    graph.add_node("ingest_data", ingest_agent)
    graph.add_node("anomaly_agent", build_anomaly_agent(model, cfg))
    graph.add_node("diagnosis_agent", lambda state: diagnosis_agent(state, cfg))
    graph.add_node("engagement_agent", engagement_agent)
    graph.add_node("scheduling_agent", scheduling_agent)
    graph.add_node("feedback_agent", feedback_agent)
    graph.add_node(
        "manufacturing_insights_agent",
        lambda state: manufacturing_insights_agent(state, cfg),
    )

    graph.set_entry_point("ingest_data")
    graph.add_edge("ingest_data", "anomaly_agent")
    graph.add_edge("anomaly_agent", "diagnosis_agent")
    graph.add_edge("diagnosis_agent", "engagement_agent")

    graph.add_conditional_edges(
        "engagement_agent",
        _engagement_branch,
        {
            "schedule": "scheduling_agent",
            "feedback": "feedback_agent",
        },
    )

    graph.add_edge("scheduling_agent", "feedback_agent")
    graph.add_edge("feedback_agent", "manufacturing_insights_agent")
    graph.add_edge("manufacturing_insights_agent", END)

    compiled = graph.compile()
    return compiled


