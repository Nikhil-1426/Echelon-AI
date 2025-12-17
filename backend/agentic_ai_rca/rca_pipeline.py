import pandas as pd
from neo4j import GraphDatabase

# -----------------------------
# CONFIG
# -----------------------------
CSV_PATH = "data/AgenticAI_Final_Format_Dataset.csv"
NEO4J_URI = "neo4j+s://d7c87b52.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "WIWa9b3z0qhOweiQ9BTYsAzfu0NB4Ce__m1fPLKu6I0"

# -----------------------------
# STEP 1: LOAD & PREPARE DATA
# -----------------------------
print("🔹 Loading dataset...")
df = pd.read_csv(CSV_PATH)

# Keep only DTC rows
dtc_df = df[df["Parameters"] == "DTC_Code"].copy()

# Extract vehicle, model, supplier
dtc_df[["Vehicle", "Model", "Supplier"]] = dtc_df["Details"].str.split(", ", expand=True)

# Melt timestamps into rows
timestamp_cols = [c for c in dtc_df.columns if "-" in c]

events = dtc_df.melt(
    id_vars=["Vehicle", "Model", "Supplier"],
    value_vars=timestamp_cols,
    var_name="Timestamp",
    value_name="DTC"
)

# Remove normal and invalid readings
events = events.dropna(subset=["DTC"])
events = events[events["DTC"] != "None"]
events = events[events["DTC"].astype(str).str.strip() != ""]


# Convert timestamp
events["Timestamp"] = pd.to_datetime(events["Timestamp"], format="%d-%m %H:%M")

# Save RCA events
events.to_csv("rca_events.csv", index=False)
print(f"✅ RCA events generated: {len(events)} records")

# -----------------------------
# STEP 2: KPI SUMMARY
# -----------------------------
summary = {
    "top_risk_supplier": events["Supplier"].value_counts().idxmax(),
    "most_affected_model": events["Model"].value_counts().idxmax(),
    "most_frequent_failure": events["DTC"].value_counts().idxmax(),
    "recurring_defect_percent": round(
        (events.shape[0] / len(events["Vehicle"].unique())) * 100, 2
    )
}

pd.DataFrame([summary]).to_csv("rca_summary.csv", index=False)
print("✅ RCA summary generated")

# -----------------------------
# STEP 3: LOAD INTO NEO4J
# -----------------------------
print("🔹 Connecting to Neo4j...")
driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)

def load_graph(events_df):
    with driver.session() as session:
        for row in events_df.itertuples(index=False):
            session.run("""
            MERGE (s:Supplier {name:$supplier})
            MERGE (m:Model {name:$model})
            MERGE (f:Failure {code:$dtc})

            MERGE (s)-[r1:CAUSES]->(f)
            ON CREATE SET r1.count = 1
            ON MATCH SET r1.count = r1.count + 1

            MERGE (m)-[r2:AFFECTS]->(f)
            ON CREATE SET r2.count = 1
            ON MATCH SET r2.count = r2.count + 1
            """,
            supplier=row.Supplier,
            model=row.Model,
            dtc=row.DTC)


load_graph(events)
driver.close()

print("🎯 RCA Knowledge Graph successfully created in Neo4j")
