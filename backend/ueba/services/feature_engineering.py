import pandas as pd

def extract_features(df: pd.DataFrame):
    grouped = df.groupby("agent_id")

    features = grouped.agg(
        actions=("action_type", "count"),
        avg_latency=("latency_ms", "mean"),
        failure_rate=("success", lambda x: 1 - x.mean()),
        avg_tokens=("tokens_used", "mean"),
        off_hours=("hour", lambda x: sum((x < 8) | (x > 19)))
    ).reset_index()

    return features
