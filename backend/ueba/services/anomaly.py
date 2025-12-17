from sklearn.ensemble import IsolationForest
import joblib
import numpy as np

MODEL_PATH = "ueba/models/isolation_forest.pkl"

def train_anomaly_model(features):
    X = features.drop(columns=["agent_id"])

    model = IsolationForest(
        n_estimators=200,
        contamination=0.07,
        random_state=42
    )
    model.fit(X)

    joblib.dump(model, MODEL_PATH)
    return model

def load_model():
    return joblib.load(MODEL_PATH)

def score_anomalies(model, features):
    X = features.drop(columns=["agent_id"])
    scores = -model.score_samples(X)  # higher = more anomalous
    features["anomaly_score"] = scores
    return features
