"""Utilities to load the AgenticAI_Final_Format_Dataset Excel into model-ready telemetry."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Sequence, Tuple

import pandas as pd

from app.state import SystemState, VehicleMetricPoint


@dataclass
class VehicleMetadata:
    """Metadata parsed from the Details column."""

    vehicle_id: str
    vehicle_model: str
    supplier_id: str


def _parse_details(details: str) -> VehicleMetadata:
    parts = [p.strip() for p in str(details).split(",")]
    while len(parts) < 3:
        parts.append("unknown")
    return VehicleMetadata(vehicle_id=parts[0], vehicle_model=parts[1], supplier_id=parts[2])


def _value_to_float(parameter: str, value) -> float:
    """Convert raw values to float for model ingestion."""

    if parameter == "DTC_Code":
        text = str(value).strip().lower()
        return 0.0 if text in {"none", "", "nan"} else 1.0
    try:
        return float(value)
    except Exception:
        return 0.0


def load_vehicle_timeseries(
    path: str, customer_filter: Optional[str] = None
) -> Dict[str, SystemState]:
    """Load Excel and emit per-vehicle SystemState fragments with raw_metrics populated.

    Args:
        path: Path to AgenticAI_Final_Format_Dataset.xlsx.
        customer_filter: Optional specific customer id to filter to.

    Returns:
        Dict keyed by vehicle_id containing SystemState slices ready for graph invocation.
    """

    df = pd.read_excel(path)
    timestamp_cols = list(df.columns[4:])

    if customer_filter:
        df = df[df["Customer"] == customer_filter]

    vehicles: Dict[str, SystemState] = {}

    for (customer, details), block in df.groupby(["Customer", "Details"]):
        meta = _parse_details(details)
        metrics_per_ts: Dict[str, Dict[str, float]] = {str(ts): {} for ts in timestamp_cols}

        for _, row in block.iterrows():
            parameter = row["Parameters"]
            for ts in timestamp_cols:
                metrics_per_ts[str(ts)][parameter] = _value_to_float(parameter, row[ts])

        raw_points: List[VehicleMetricPoint] = []
        for ts in timestamp_cols:
            ts_str = str(ts)
            point = VehicleMetricPoint(
                timestamp=pd.to_datetime(ts).timestamp(),
                metrics=metrics_per_ts[ts_str],
            )
            raw_points.append(point)

        vehicles[meta.vehicle_id] = {
            "vehicle_id": meta.vehicle_id,
            "model": meta.vehicle_model,
            "variant": "unknown",
            "user_segment": "retail",
            "customer_id": str(customer),  # Include customer ID from Excel
            "supplier_id": meta.supplier_id,
            "raw_metrics": raw_points,
            "logs": [],
        }

    return vehicles


def feature_names_from_dataset(path: str) -> List[str]:
    """Extract ordered feature names based on the first telemetry row."""

    df = pd.read_excel(path, nrows=1)
    return list(df["Parameters"].unique())


