from services.baseline import build_baseline
from services.anomaly import train_anomaly_model

if __name__ == "__main__":
    print("🔹 Building UEBA baseline...")
    features = build_baseline()

    print("🔹 Training UEBA anomaly model...")
    train_anomaly_model(features)

    print("✅ UEBA model trained successfully.")
