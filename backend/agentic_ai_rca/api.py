from fastapi import FastAPI
from fastapi import APIRouter
from neo4j import GraphDatabase
from fastapi.middleware.cors import CORSMiddleware
# -----------------------------
# CONFIG
# -----------------------------
NEO4J_URI = "neo4j+s://d7c87b52.databases.neo4j.io"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "WIWa9b3z0qhOweiQ9BTYsAzfu0NB4Ce__m1fPLKu6I0"

driver = GraphDatabase.driver(
    NEO4J_URI,
    auth=(NEO4J_USER, NEO4J_PASSWORD)
)


router = APIRouter()

# # Enable frontend access
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# -----------------------------
# 1️⃣ RCA SUMMARY
# -----------------------------
@router.get("/summary")
def rca_summary():
    with driver.session() as session:
        result = session.run("""
        MATCH (s:Supplier)-[r:CAUSES]->(f:Failure)
        RETURN
          s.name AS supplier,
          f.code AS failure,
          SUM(r.count) AS total
        ORDER BY total DESC
        LIMIT 1
        """)

        record = result.single()

        return {
            "top_risk_supplier": record["supplier"],
            "most_frequent_failure": record["failure"],
            "recurring_defect_percent": round(record["total"] / 100, 2)
        }

# -----------------------------
# 2️⃣ RCA GRAPH
# -----------------------------
@router.get("/graph")
def rca_graph():
    with driver.session() as session:
        records = session.run("""
        MATCH (s:Supplier)-[r1:CAUSES]->(f:Failure),
              (m:Model)-[r2:AFFECTS]->(f)
        RETURN
          s.name AS supplier,
          m.name AS model,
          f.code AS failure,
          r1.count + r2.count AS weight
        """)

        nodes = {}
        edges = []

        for r in records:
            for node, t in [
                (r["supplier"], "supplier"),
                (r["model"], "model"),
                (r["failure"], "failure")
            ]:
                if node not in nodes:
                    nodes[node] = {"id": node, "type": t}

            edges.append({
                "source": r["supplier"],
                "target": r["failure"],
                "weight": r["weight"]
            })

            edges.append({
                "source": r["model"],
                "target": r["failure"],
                "weight": r["weight"]
            })

        return {
            "nodes": list(nodes.values()),
            "edges": edges
        }

# -----------------------------
# 3️⃣ SUPPLIER RISK
# -----------------------------
@router.get("/supplier-risk")
def supplier_risk():
    with driver.session() as session:
        records = session.run("""
        MATCH (s:Supplier)-[r:CAUSES]->(f:Failure)
        RETURN s.name AS supplier, SUM(r.count) AS risk
        ORDER BY risk DESC
        """)

        return [
            {
                "supplier": r["supplier"],
                "risk_score": round(r["risk"] / 100, 2)
            }
            for r in records
        ]

# -----------------------------
# 4️⃣ FAILURE HEATMAP
# -----------------------------
@router.get("/heatmap")
def failure_heatmap():
    with driver.session() as session:
        records = session.run("""
        MATCH (f:Failure)<-[r:CAUSES]-()
        RETURN f.code AS failure, SUM(r.count) AS count
        ORDER BY count DESC
        """)

        return [
            {"failure": r["failure"], "count": r["count"]}
            for r in records
        ]
