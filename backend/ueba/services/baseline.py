from ueba.services.loader import load_logs
from ueba.services.feature_engineering import extract_features

def build_baseline():
    df = load_logs()
    features = extract_features(df)
    return features
