"""Typed state definitions for the LangGraph automotive aftersales workflow."""

from __future__ import annotations

from typing import Dict, List, Literal, Optional, TypedDict


class VehicleMetricPoint(TypedDict):
    """Single telemetry measurement for a vehicle."""

    timestamp: float  # seconds since epoch or relative time
    metrics: Dict[str, float]


class AnomalyInfo(TypedDict, total=False):
    """Detected anomaly for a specific metric."""

    metric_name: str
    severity: float  # 0.0 - 1.0
    explanation: str
    error: float  # reconstruction/forecast error


class DiagnosisInfo(TypedDict, total=False):
    """Diagnosis outcome derived from anomalies."""

    part_id: str
    part_name: str
    confidence: float
    estimated_time_to_failure_days: float
    severity_level: Literal["low", "medium", "high"]
    issue_category: str
    supporting_metrics: List[str]


class ScheduleInfo(TypedDict, total=False):
    """Workshop scheduling details."""

    workshop_id: str
    workshop_name: str
    slot_time: str
    mechanic_id: str
    priority_tag: Literal["low", "medium", "high"]


class FeedbackInfo(TypedDict, total=False):
    """Feedback collected after service."""

    customer_rating: float
    customer_comments: str
    workshop_comments: str
    repair_time_hours: float
    diagnosis_correct: bool


class ManufacturingPayload(TypedDict, total=False):
    """Structured payload destined for OEM/manufacturing analytics."""

    vehicle_id: str
    model: str
    variant: str
    user_segment: str
    failure_part_id: str
    failure_part_name: str
    issue_category: str
    workshop_id: str
    repair_time_hours: float
    diagnosis_correct: bool
    timestamp: str


class SystemState(TypedDict, total=False):
    """Shared graph state passed between LangGraph nodes."""

    vehicle_id: str
    model: str
    variant: str
    user_segment: str
    raw_metrics: List[VehicleMetricPoint]
    anomalies: List[AnomalyInfo]
    diagnosis: Optional[DiagnosisInfo]
    customer_notified: bool
    notification_message: str
    schedule: Optional[ScheduleInfo]
    feedback: Optional[FeedbackInfo]
    manufacturing_payload: Optional[ManufacturingPayload]
    logs: List[str]


