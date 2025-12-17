import pandas as pd

def load_logs(path="ueba/data/agent_logs.jsonl"):
    return pd.read_json(path, lines=True)
