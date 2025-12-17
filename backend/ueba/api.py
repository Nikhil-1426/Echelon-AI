import pandas as pd
from fastapi import FastAPI
from ueba.services.loader import load_logs
from ueba.services.feature_engineering import extract_features
from ueba.services.anomaly import load_model, score_anomalies
from ueba.services.risk import compute_risk
from fastapi import APIRouter

router = APIRouter()

@router.get("/summary")
def summary():
    df = load_logs()
    features = extract_features(df)
    model = load_model()
    scored = score_anomalies(model, features)
    risked = compute_risk(scored)

    top = risked.iloc[0]
    return {
        "highest_risk_agent": top["agent_id"],
        "risk_score": round(top["risk_score"], 2)
    }

@router.get("/risk-ranking")
def ranking():
    df = load_logs()
    features = extract_features(df)
    model = load_model()
    scored = score_anomalies(model, features)
    risked = compute_risk(scored)

    return risked[["agent_id", "risk_score"]].round(2).to_dict(orient="records")

@router.get("/agent/{agent_id}")
def agent_detail(agent_id: str):
    df = load_logs()
    agent_df = df[df["agent_id"] == agent_id]

    if agent_df.empty:
        return {"error": "Agent not found"}

    features = extract_features(agent_df)
    return features.to_dict(orient="records")[0]


@router.get("/risk-trend/{agent_id}")
def agent_risk_trend(agent_id: str):
    df = pd.read_json("ueba/data/agent_logs.jsonl", lines=True)

    # Parse timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Derived UEBA features
    df["failure"] = (~df["success"]).astype(int)
    df["off_hours"] = ((df["hour"] < 9) | (df["hour"] > 18)).astype(int)
    df["tokens"] = df["tokens_used"]

    agent_df = df[df["agent_id"] == agent_id]

    if agent_df.empty:
        return []

    # 👇 Explicit daily aggregation with named column
    daily = (
        agent_df
        .assign(date=agent_df["timestamp"].dt.date)
        .groupby("date")
        .agg({
            "latency_ms": "mean",
            "failure": "mean",
            "tokens": "mean",
            "off_hours": "sum"
        })
        .reset_index()
    )

    # Risk score
    daily["risk"] = (
        daily["latency_ms"] * 0.3 +
        daily["failure"] * 100 * 0.3 +
        daily["tokens"] * 0.2 +
        daily["off_hours"] * 0.2
    )

    return [
        {
            "date": str(row["date"]),
            "risk": round(row["risk"], 2)
        }
        for _, row in daily.iterrows()
    ]





@router.get("/explain/{agent_id}")
def explain_agent_risk(agent_id: str):
    df = load_logs()
    agent_df = df[df["agent_id"] == agent_id]

    if agent_df.empty:
        return {"error": "Agent not found"}

    stats = extract_features(agent_df).iloc[0]

    reasons = []

    if stats["failure_rate"] > 0.08:
        reasons.append("High failure rate compared to baseline")

    if stats["off_hours"] > 30:
        reasons.append("Excessive off-hours activity")

    if stats["avg_tokens"] > 300:
        reasons.append("Unusually high token consumption")

    if stats["avg_latency"] > 500:
        reasons.append("Performance degradation observed")

    if not reasons:
        reasons.append("Agent behavior within acceptable baseline")

    return {
        "agent": agent_id,
        "risk_factors": reasons,
        "stats": {
            "failure_rate": round(stats["failure_rate"], 4),
            "avg_latency": round(stats["avg_latency"], 2),
            "avg_tokens": round(stats["avg_tokens"], 2),
            "off_hours": int(stats["off_hours"])
        }
    }


