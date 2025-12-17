"""Central configuration for models and workflow thresholds."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class LSTMAnomalyConfig:
    """Hyperparameters and thresholds for the LSTM anomaly detector."""

    input_dim: int = 4
    hidden_dim: int = 32
    num_layers: int = 1
    learning_rate: float = 1e-3
    epochs: int = 10
    anomaly_threshold: float = 0.05


@dataclass
class WorkflowConfig:
    """Workflow-wide configuration knobs."""

    anomaly: LSTMAnomalyConfig = field(default_factory=LSTMAnomalyConfig)
    medium_severity_threshold: float = 0.4
    high_severity_threshold: float = 0.7
    default_user_segment: str = "retail"


