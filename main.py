"""Demo entry point for the LangGraph automotive aftersales workflow."""

from __future__ import annotations

from pprint import pprint
from typing import List

import torch

from app.config import WorkflowConfig
from app.graph import build_graph
from app.models.lstm_anomaly import LSTMAnomalyDetector
from app.state import SystemState, VehicleMetricPoint
from app.utils.data_loader import load_vehicle_timeseries


def _build_dummy_time_series() -> List[VehicleMetricPoint]:
    """Create a dummy multi-metric time-series for fallback demonstration."""

    data: List[VehicleMetricPoint] = []
    for t in range(30):
        data.append(
            {
                "timestamp": float(t),
                "metrics": {
                    "Engine_Temperature": 80.0 + 0.2 * t,
                    "Odometer": 70000 + 5 * t,
                    "Battery_SoC": max(0, 90 - t),
                    "Speed": 60 + (t % 10),
                    "Brake_Pressure": 30 + (t % 5),
                    "Fuel_Status": max(0, 70 - 2 * t),
                    "DTC_Code": 0.0,
                },
            }
        )
    return data


def main() -> None:
    cfg = WorkflowConfig()
    dataset_path = "AgenticAI_Final_Format_Dataset.xlsx"

    # Prefer real dataset if present; otherwise fall back to synthetic telemetry.
    try:
        vehicles = load_vehicle_timeseries(dataset_path)
    except Exception as exc:  # noqa: BLE001
        vehicles = {}
        print(f"Dataset load failed ({exc}); using dummy telemetry instead.")

    if vehicles:
        # Take first vehicle for the demo run.
        initial_state = next(iter(vehicles.values()))
        feature_dim = len(initial_state["raw_metrics"][0]["metrics"])
    else:
        initial_state = {
            "vehicle_id": "V-12345",
            "model": "Sedan-X",
            "variant": "premium",
            "user_segment": cfg.default_user_segment,
            "raw_metrics": _build_dummy_time_series(),
            "logs": [],
        }
        feature_dim = len(initial_state["raw_metrics"][0]["metrics"])

    # Initialize model with random weights (placeholder until trained weights are available).
    model = LSTMAnomalyDetector(
        input_dim=feature_dim,
        hidden_dim=cfg.anomaly.hidden_dim,
        num_layers=cfg.anomaly.num_layers,
    )

    workflow = build_graph(model, cfg)

    final_state = workflow.invoke(initial_state)

    print("\n=== Final State (truncated) ===")
    pprint({k: v for k, v in final_state.items() if k != "logs"})

    print("\n=== Logs ===")
    for entry in final_state.get("logs", []):
        print(entry)


if __name__ == "__main__":
    main()


