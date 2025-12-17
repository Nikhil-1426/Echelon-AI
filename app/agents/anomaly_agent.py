# """Anomaly detection agent using the LSTM model."""

# from __future__ import annotations

# from typing import Dict, List, Sequence

# import torch

# from app.config import WorkflowConfig
# from app.models import infer_anomalies
# from app.models.lstm_anomaly import LSTMAnomalyDetector
# from app.state import AnomalyInfo, SystemState, VehicleMetricPoint
# from app.utils.logging_utils import append_log


# def _extract_series(raw_points: List[VehicleMetricPoint]) -> tuple[torch.Tensor, Sequence[str]]:
#     """Convert telemetry points into a tensor suitable for the model."""

#     if not raw_points:
#         raise ValueError("No telemetry points provided.")
#     metric_names = sorted(raw_points[0]["metrics"].keys())
#     series = []
#     for point in raw_points:
#         values = [float(point["metrics"].get(name, 0.0)) for name in metric_names]
#         series.append(values)
#     tensor = torch.tensor(series, dtype=torch.float32).unsqueeze(0)  # (1, seq_len, features)
#     return tensor, metric_names


# def build_anomaly_agent(
#     model: LSTMAnomalyDetector, config: WorkflowConfig
# ):  # type: ignore[override]
#     """Factory to build the anomaly detection node with injected model and config."""

#     def node(state: SystemState) -> SystemState:
#         append_log(state, "Anomaly agent: running LSTM-based detection.")
#         raw_points = state.get("raw_metrics", []) or []
#         try:
#             series, metric_names = _extract_series(raw_points)
#         except ValueError as exc:
#             append_log(state, f"Anomaly agent: failed to extract series: {exc}")
#             state["anomalies"] = []
#             return state

#         anomalies_raw = infer_anomalies(
#             model=model,
#             series=series,
#             metric_names=metric_names,
#             threshold=config.anomaly.anomaly_threshold,
#         )

#         anomalies: List[AnomalyInfo] = []
#         for metric_name, severity, error in anomalies_raw:
#             anomalies.append(
#                 {
#                     "metric_name": metric_name,
#                     "severity": severity,
#                     "error": error,
#                     "explanation": f"{metric_name} reconstruction error {error:.4f} exceeds threshold",
#                 }
#             )

#         state["anomalies"] = anomalies
#         append_log(
#             state,
#             f"Anomaly agent: detected {len(anomalies)} anomalies above threshold "
#             f"{config.anomaly.anomaly_threshold}.",
#         )
#         return state

#     return node


"""Anomaly detection agent using the LSTM model."""

from __future__ import annotations

from typing import Dict, List, Sequence

import torch

from app.config import WorkflowConfig
from app.models import infer_anomalies
from app.models.lstm_anomaly import LSTMAnomalyDetector
from app.state import AnomalyInfo, SystemState, VehicleMetricPoint
from app.utils.logging_utils import append_log


def _extract_series(
    raw_points: List[VehicleMetricPoint],
) -> tuple[torch.Tensor, Sequence[str]]:
    """Convert telemetry points into a tensor suitable for the model.
    
    Dataset tweak:
    - Ignore non-numeric parameters (e.g., DTC / error codes)
    """

    if not raw_points:
        raise ValueError("No telemetry points provided.")

    # keep only numeric metrics (dataset has categorical DTCs)
    metric_names = sorted(
        name
        for name, value in raw_points[0]["metrics"].items()
        if isinstance(value, (int, float))
    )

    series = []
    for point in raw_points:
        values = [
            float(point["metrics"].get(name, 0.0))
            for name in metric_names
        ]
        series.append(values)

    tensor = torch.tensor(series, dtype=torch.float32).unsqueeze(0)
    # shape: (1, seq_len, num_features)

    return tensor, metric_names


def build_anomaly_agent(
    model: LSTMAnomalyDetector, config: WorkflowConfig
):  # type: ignore[override]
    """Factory to build the anomaly detection node with injected model and config."""

    def node(state: SystemState) -> SystemState:
        append_log(state, "Anomaly agent: running LSTM-based detection.")

        raw_points = state.get("raw_metrics", []) or []

        try:
            series, metric_names = _extract_series(raw_points)
        except ValueError as exc:
            append_log(state, f"Anomaly agent: failed to extract series: {exc}")
            state["anomalies"] = []
            return state

        anomalies_raw = infer_anomalies(
            model=model,
            series=series,
            metric_names=metric_names,
            threshold=config.anomaly.anomaly_threshold,
        )

        anomalies: List[AnomalyInfo] = []
        for metric_name, severity, error in anomalies_raw:
            anomalies.append(
                {
                    "metric_name": metric_name,
                    "severity": severity,
                    "error": error,
                    "explanation": (
                        f"{metric_name} reconstruction error {error:.4f} "
                        f"exceeds threshold"
                    ),
                }
            )

        state["anomalies"] = anomalies

        append_log(
            state,
            f"Anomaly agent: detected {len(anomalies)} anomalies above threshold "
            f"{config.anomaly.anomaly_threshold}.",
        )

        return state

    return node
