"""FastAPI server exposing the LangGraph automotive aftersales workflow."""

from __future__ import annotations

import os
from typing import Dict, List, Optional

import torch
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import WorkflowConfig
from app.graph import build_graph
from app.models.lstm_anomaly import LSTMAnomalyDetector
from app.state import SystemState
from app.utils.data_loader import load_vehicle_timeseries

app = FastAPI(title="EY Agentic AI API", version="1.0.0")

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
_workflow_cache: Optional[object] = None
_model_cache: Optional[LSTMAnomalyDetector] = None
_cfg_cache: Optional[WorkflowConfig] = None
_vehicles_cache: Optional[Dict[str, SystemState]] = None


def _get_workflow():
    """Lazy initialization of workflow and model."""
    global _workflow_cache, _model_cache, _cfg_cache, _vehicles_cache

    if _workflow_cache is None:
        cfg = WorkflowConfig()
        dataset_path = "AgenticAI_Final_Format_Dataset.xlsx"

        # Load vehicles
        if not os.path.exists(dataset_path):
            raise FileNotFoundError(f"Dataset not found: {dataset_path}")

        vehicles = load_vehicle_timeseries(dataset_path)
        if not vehicles:
            raise ValueError("No vehicles loaded from dataset")

        # Determine feature dimension from first vehicle
        first_vehicle = next(iter(vehicles.values()))
        feature_dim = len(first_vehicle["raw_metrics"][0]["metrics"])

        # Initialize model
        model = LSTMAnomalyDetector(
            input_dim=feature_dim,
            hidden_dim=cfg.anomaly.hidden_dim,
            num_layers=cfg.anomaly.num_layers,
        )

        # Build workflow
        workflow = build_graph(model, cfg)

        # Cache
        _workflow_cache = workflow
        _model_cache = model
        _cfg_cache = cfg
        _vehicles_cache = vehicles

    return _workflow_cache, _model_cache, _cfg_cache, _vehicles_cache


class VehicleResponse(BaseModel):
    """Response model for vehicle data."""

    vehicleId: str
    model: str
    customerId: str
    status: str
    anomalies: List[Dict]
    diagnosis: Optional[Dict]
    schedule: Optional[Dict]
    feedback: Optional[Dict]
    manufacturingPayload: Optional[Dict]


def _system_state_to_response(state: SystemState, customer_id: str) -> VehicleResponse:
    """Convert SystemState to frontend-friendly response."""
    anomalies = []
    for anomaly in state.get("anomalies", []):
        anomalies.append({
            "metric": anomaly.get("metric_name", ""),
            "severity": float(anomaly.get("severity", 0.0)),
            "explanation": anomaly.get("explanation", ""),
        })

    diagnosis = state.get("diagnosis")
    diagnosis_dict = None
    if diagnosis:
        diagnosis_dict = {
            "partId": diagnosis.get("part_id", ""),
            "partName": diagnosis.get("part_name", ""),
            "confidence": float(diagnosis.get("confidence", 0.0)),
            "severityLevel": diagnosis.get("severity_level", "low"),
            "estimatedTimeToFailure": float(diagnosis.get("estimated_time_to_failure_days", 0.0)),
        }

    schedule = state.get("schedule")
    schedule_dict = None
    if schedule:
        schedule_dict = {
            "workshopId": schedule.get("workshop_id", ""),
            "workshopName": schedule.get("workshop_name", ""),
            "slotTime": schedule.get("slot_time", ""),
            "priorityTag": schedule.get("priority_tag", "low"),
        }

    feedback = state.get("feedback")
    feedback_dict = None
    if feedback:
        feedback_dict = {
            "customerRating": float(feedback.get("customer_rating", 0.0)),
            "diagnosisCorrect": bool(feedback.get("diagnosis_correct", False)),
            "repairTimeHours": float(feedback.get("repair_time_hours", 0.0)),
        }

    # Determine status
    status = "monitoring"
    if diagnosis:
        severity = diagnosis.get("severity_level", "low")
        if severity in ["medium", "high"]:
            status = "anomaly_detected"
            if schedule:
                status = "scheduled"
                if feedback:
                    status = "serviced"

    return VehicleResponse(
        vehicleId=state.get("vehicle_id", ""),
        model=state.get("model", ""),
        customerId=customer_id,
        status=status,
        anomalies=anomalies,
        diagnosis=diagnosis_dict,
        schedule=schedule_dict,
        feedback=feedback_dict,
        manufacturingPayload=state.get("manufacturing_payload"),
    )


@app.get("/")
def root():
    """Health check endpoint."""
    return {"status": "ok", "service": "EY Agentic AI API"}


@app.get("/api/vehicles")
def get_vehicles():
    """Get all vehicles with their workflow execution results."""
    try:
        workflow, model, cfg, vehicles = _get_workflow()
        results: List[VehicleResponse] = []

        # Run workflow for each vehicle
        for vehicle_id, initial_state in vehicles.items():
            try:
                # Extract customer_id from state if available, otherwise use placeholder
                customer_id = initial_state.get("customer_id", f"CUST_{vehicle_id}")

                # Run workflow
                final_state = workflow.invoke(initial_state)

                # Convert to response format
                vehicle_response = _system_state_to_response(final_state, customer_id)
                results.append(vehicle_response)
            except Exception as e:
                # Skip vehicles that fail, but log the error
                print(f"Error processing vehicle {vehicle_id}: {e}")
                continue

        return {"vehicles": results, "total": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/vehicles/{vehicle_id}")
def get_vehicle(vehicle_id: str):
    """Get a specific vehicle's workflow execution result."""
    try:
        workflow, model, cfg, vehicles = _get_workflow()

        if vehicle_id not in vehicles:
            raise HTTPException(status_code=404, detail=f"Vehicle {vehicle_id} not found")

        initial_state = vehicles[vehicle_id]
        customer_id = initial_state.get("customer_id", f"CUST_{vehicle_id}")

        # Run workflow
        final_state = workflow.invoke(initial_state)

        # Convert to response format
        return _system_state_to_response(final_state, customer_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/workflow/run/{vehicle_id}")
def run_workflow(vehicle_id: str):
    """Manually trigger workflow execution for a vehicle."""
    try:
        workflow, model, cfg, vehicles = _get_workflow()

        if vehicle_id not in vehicles:
            raise HTTPException(status_code=404, detail=f"Vehicle {vehicle_id} not found")

        initial_state = vehicles[vehicle_id]
        customer_id = initial_state.get("customer_id", f"CUST_{vehicle_id}")

        # Run workflow
        final_state = workflow.invoke(initial_state)

        # Convert to response format
        return _system_state_to_response(final_state, customer_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/stats")
def get_stats():
    """Get aggregated statistics from all vehicles."""
    try:
        workflow, model, cfg, vehicles = _get_workflow()
        results: List[VehicleResponse] = []

        # Run workflow for all vehicles
        for vehicle_id, initial_state in vehicles.items():
            try:
                customer_id = initial_state.get("customer_id", f"CUST_{vehicle_id}")
                final_state = workflow.invoke(initial_state)
                vehicle_response = _system_state_to_response(final_state, customer_id)
                results.append(vehicle_response)
            except Exception:
                continue

        # Calculate statistics
        total_vehicles = len(results)
        anomalies_detected = sum(1 for v in results if v.anomalies)
        scheduled = sum(1 for v in results if v.schedule)
        serviced = sum(1 for v in results if v.feedback)

        # Diagnosis accuracy
        correct_diagnoses = sum(1 for v in results if v.feedback and v.feedback.get("diagnosisCorrect"))
        total_feedback = sum(1 for v in results if v.feedback)
        diagnosis_accuracy = (correct_diagnoses / total_feedback * 100) if total_feedback > 0 else 0

        # Average rating
        ratings = [v.feedback["customerRating"] for v in results if v.feedback]
        avg_rating = sum(ratings) / len(ratings) if ratings else 0

        # Part failure distribution
        part_failures: Dict[str, int] = {}
        for v in results:
            if v.diagnosis:
                part_name = v.diagnosis.get("partName", "Unknown")
                part_failures[part_name] = part_failures.get(part_name, 0) + 1

        # Severity distribution
        severity_counts = {"high": 0, "medium": 0, "low": 0}
        for v in results:
            if v.diagnosis:
                severity = v.diagnosis.get("severityLevel", "low")
                severity_counts[severity] = severity_counts.get(severity, 0) + 1

        return {
            "totalVehicles": total_vehicles,
            "anomaliesDetected": anomalies_detected,
            "scheduled": scheduled,
            "serviced": serviced,
            "diagnosisAccuracy": round(diagnosis_accuracy, 2),
            "avgRating": round(avg_rating, 2),
            "partFailures": part_failures,
            "severityDistribution": severity_counts,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/manufacturing")
def get_manufacturing_insights():
    """Get manufacturing insights payloads."""
    try:
        workflow, model, cfg, vehicles = _get_workflow()
        insights = []

        # Run workflow for all vehicles and collect manufacturing payloads
        for vehicle_id, initial_state in vehicles.items():
            try:
                final_state = workflow.invoke(initial_state)
                payload = final_state.get("manufacturing_payload")
                if payload:
                    insights.append(payload)
            except Exception:
                continue

        return {"insights": insights, "total": len(insights)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

