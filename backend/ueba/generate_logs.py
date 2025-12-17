import json
import random
from datetime import datetime, timedelta

agents = [
    "anomaly_agent",
    "diagnosis_agent",
    "engagement_agent",
    "feedback_agent",
    "ingest_agent",
    "manufacturing_agent",
    "scheduling_agent"
]
tools = ["db_query", "web_fetch", "code_exec", "vector_search"]
resources = ["supplier_db", "logs_db", "user_data"]
roles = ["planner", "executor", "critic"]

logs = []
now = datetime.utcnow()

for i in range(3000):
    agent = random.choice(agents)
    role = random.choice(roles)
    tool = random.choice(tools)

    is_anomalous = random.random() < 0.07  # 7% anomalies

    log = {
        "timestamp": (now - timedelta(minutes=random.randint(0, 1440))).isoformat(),
        "agent_id": agent,
        "agent_role": role,
        "action_type": "tool_call",
        "tool_name": tool,
        "resource": random.choice(resources),
        "success": not is_anomalous,
        "latency_ms": random.randint(200, 400) if not is_anomalous else random.randint(1200, 4000),
        "tokens_used": random.randint(100, 300) if not is_anomalous else random.randint(800, 2000),
        "hour": random.randint(9, 18) if not is_anomalous else random.choice([1, 2, 3, 23])
    }

    logs.append(log)

with open("data/agent_logs.jsonl", "w") as f:
    for log in logs:
        f.write(json.dumps(log) + "\n")

print("Synthetic agent logs generated.")
