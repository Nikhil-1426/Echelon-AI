def compute_risk(df):
    df["risk_score"] = (
        0.4 * df["anomaly_score"] +
        0.2 * df["failure_rate"] +
        0.2 * df["off_hours"] +
        0.2 * (df["avg_tokens"] / df["avg_tokens"].max())
    )

    df["risk_score"] = (df["risk_score"] / df["risk_score"].max()) * 100
    return df.sort_values("risk_score", ascending=False)
