"""PyTorch LSTM model and utilities for time-series anomaly detection."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple

import torch
from torch import nn

from app.config import LSTMAnomalyConfig


class LSTMAnomalyDetector(nn.Module):
    """Simple sequence-to-sequence LSTM autoencoder for reconstruction-based anomaly scoring."""

    def __init__(self, input_dim: int, hidden_dim: int, num_layers: int = 1) -> None:
        super().__init__()
        self.encoder = nn.LSTM(
            input_dim, hidden_dim, num_layers=num_layers, batch_first=True
        )
        self.decoder = nn.LSTM(
            hidden_dim, hidden_dim, num_layers=num_layers, batch_first=True
        )
        self.output_layer = nn.Linear(hidden_dim, input_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """Encode the sequence and reconstruct it."""

        enc_out, (hidden, cell) = self.encoder(x)
        dec_out, _ = self.decoder(enc_out, (hidden, cell))
        recon = self.output_layer(dec_out)
        return recon


@dataclass
class TrainingArtifacts:
    """Container for training outputs."""

    model: LSTMAnomalyDetector
    losses: List[float]


def train_lstm_anomaly_model(
    data_loader: Iterable[Tuple[torch.Tensor, torch.Tensor]],
    config: LSTMAnomalyConfig,
    device: torch.device | None = None,
) -> TrainingArtifacts:
    """Train the LSTM anomaly model using reconstruction loss.

    Args:
        data_loader: Iterable yielding (input, target) tensors shaped (batch, seq_len, features).
        config: Hyperparameters.
        device: Optional device override.

    Returns:
        TrainingArtifacts containing the trained model and loss history.

    Note:
        This is a placeholder training loop. Replace the data_loader with a real
        dataset and extend with validation, checkpoints, and early stopping when real data arrives.
    """

    device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = LSTMAnomalyDetector(
        input_dim=config.input_dim,
        hidden_dim=config.hidden_dim,
        num_layers=config.num_layers,
    ).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    criterion = nn.MSELoss()

    loss_history: List[float] = []

    model.train()
    for epoch in range(config.epochs):
        epoch_loss = 0.0
        batches = 0
        for batch_x, batch_y in data_loader:
            batch_x = batch_x.to(device)
            batch_y = batch_y.to(device)

            optimizer.zero_grad()
            recon = model(batch_x)
            loss = criterion(recon, batch_y)
            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
            batches += 1

        if batches:
            avg_loss = epoch_loss / batches
            loss_history.append(avg_loss)

    return TrainingArtifacts(model=model, losses=loss_history)


def compute_reconstruction_error(
    recon: torch.Tensor, original: torch.Tensor
) -> torch.Tensor:
    """Compute mean squared error per feature."""

    # mean over batch and sequence -> per feature
    return torch.mean((recon - original) ** 2, dim=(0, 1))


def infer_anomalies(
    model: LSTMAnomalyDetector,
    series: torch.Tensor,
    metric_names: Sequence[str],
    threshold: float,
    device: torch.device | None = None,
) -> List[Tuple[str, float, float]]:
    """Run inference and produce anomaly scores.

    Args:
        model: Trained LSTMAnomalyDetector.
        series: Tensor shaped (1, seq_len, features).
        metric_names: Ordered names corresponding to feature dimension.
        threshold: Reconstruction error threshold.
        device: Optional device override.

    Returns:
        List of tuples (metric_name, severity, error) for metrics exceeding threshold.
    """

    device = device or torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()
    with torch.no_grad():
        series = series.to(device)
        recon = model(series)
        errors = compute_reconstruction_error(recon, series)  # shape (features,)
        anomalies: List[Tuple[str, float, float]] = []
        for name, err in zip(metric_names, errors):
            error_val = err.item()
            if error_val > threshold:
                severity = min(error_val / (threshold * 2.0), 1.0)
                anomalies.append((name, severity, error_val))
    return anomalies


