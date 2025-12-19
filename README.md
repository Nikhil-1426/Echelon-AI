# 🟡 EY Agentic AI — Automotive Aftersales Predictive Intelligence Platform

---

## 📑 Table of Contents
- [Introduction](#-introduction)
- [Project Overview](#-project-overview)
- [Key Novelties](#-key-novelties)
- [Repository Structure](#-repository-structure)
- [System Architecture & Workflow](#-system-architecture--workflow)
- [RCA — Root Cause Analysis Engine](#-rca--root-cause-analysis-engine)
- [UEBA — User & Entity Behavior Analytics](#-ueba--user--entity-behavior-analytics)
- [Architecture Diagram](#-architecture-diagram)
- [Flow Chart](#-flow-chart)
- [Screenshots](#-screenshots)
- [Getting Started](#-getting-started)
- [Backend APIs](#-backend-apis)
- [Frontend Dashboard](#-frontend-dashboard)
- [Enterprise Considerations](#-enterprise-considerations)
- [Impact Metrics](#-impact-metrics)
- [Tech Stack](#-tech-stack)
- [About Us](#-about-us)

---

## 💡 Introduction

### Problem Statement
Automotive aftersales operations today remain largely **reactive and siloed**. Vehicles are serviced only after failures occur, resulting in:

- 🚧 Unexpected breakdowns and roadside incidents  
- 😟 Poor customer experience and reduced brand trust  
- 🏭 Inefficient service center utilization  
- 🔄 Delayed and fragmented feedback to manufacturing teams  

While vehicle telemetry and service data exist, organizations lack an **autonomous, explainable intelligence layer** that can:
- Predict failures early
- Explain *why* failures happen
- Correlate issues across systems, agents, and processes
- Drive coordinated, auditable actions across the enterprise

---

### Solution
**EY Agentic AI** is a **production-grade, agent-driven predictive intelligence platform** for automotive aftersales.

It unifies:
- **Agentic orchestration (LangGraph)**
- **Predictive anomaly detection**
- **Graph-based Root Cause Analysis (RCA)**
- **User & Entity Behavior Analytics (UEBA)**

to deliver **proactive, explainable, and enterprise-ready decision intelligence**.

The platform continuously monitors telemetry, detects anomalies in advance, explains root causes, schedules service actions, gathers feedback, and generates manufacturing insights — all through an **autonomous yet governed workflow**, aligned with EY’s principles of **trust, transparency, and scalability**.

---

## 🚗 Project Overview

### Agentic Workflow (LangGraph Nodes)
**ingest → anomaly → diagnosis → engagement → scheduling → feedback → manufacturing insights**

Each agent is:
- Purpose-specific
- Independently observable
- Auditable via logs and UEBA analytics

---

### Data
**AgenticAI_Final_Format_Dataset.xlsx**
- 7-day vehicle telemetry  
- 30-minute intervals  
- 7 operational parameters per vehicle  

---

### Backend
- **Unified FastAPI application**
- Modular RCA and UEBA services
- REST APIs for vehicle-level and fleet-level intelligence

---

### Frontend
- **Next.js + Tailwind CSS**
- EY black & yellow design language
- Interactive dashboards, graphs, and explainability views

---

## ✨ Key Novelties

### 1️⃣ Agentic RCA with Knowledge Graph Reasoning
Unlike traditional rule-based diagnostics, our RCA engine:
- Correlates anomalies across **vehicles, components, symptoms, and actions**
- Models relationships using **Neo4j-style knowledge graphs**
- Produces **explainable root cause chains**, similar to enterprise RCA tools

---

### 2️⃣ UEBA for Agent & System Trust
A **novel application of UEBA** in agentic AI systems:
- Detects abnormal agent behavior (latency, failures, token usage, off-hours)
- Assigns risk scores per agent
- Enables governance, trust, and auditability of autonomous workflows

---

### 3️⃣ End-to-End Explainability
Every decision is traceable:
- Why was an anomaly flagged?
- Which agent caused risk escalation?
- What evidence supports the root cause?

This aligns strongly with **EY’s Responsible AI principles**.

---

## 🗂 Repository Structure

```text
backend/
 ├─ agentic_ai_rca/
 │  ├─ data/
 │  │  └─ AgenticAI_Final_Format_Dataset.xlsx
 │  ├─ __init__.py
 │  ├─ api.py
 │  ├─ rca_events.csv
 │  ├─ rca_pipeline.py
 │  ├─ rca_summary.csv
 │  └─ requirements.txt
 ├─ ueba/
 │  ├─ data/
 │  │  └─ agent_logs.jsonl
 │  ├─ models/
 │  │  └─ isolation_forest.pkl
 │  ├─ services/
 │  │  ├─ __init__.py
 │  │  ├─ anomaly.py
 │  │  ├─ baseline.py
 │  │  ├─ feature_engineering.py
 │  │  ├─ loader.py
 │  │  └─ risk.py
 │  ├─ __init__.py
 │  ├─ api.py
 │  ├─ generate_logs.py
 │  ├─ requirements.txt
 │  └─ train_ueba.py
 ├─ generate_vehicle_dataset.py
 ├─ main.py
 └─ script.py
frontend/
 ├─ app/
 ├─ components/
 ├─ types/
 ├─ .gitignore
 ├─ README.md
 ├─ next.config.js
 ├─ package.json
 ├─ tailwind.config.js
 └─ tsconfig.json
app/
.gitignore
AgenticAI_Final_Format_Dataset.xlsx
QUICKSTART.md
README.md
README_API.md
api_server.py
main.py
package.json
requirements.txt
```

## 🔁 **System Architecture & Workflow**

## **How It Works**

### **1. Data Ingest**
- **Excel telemetry**
- **load_vehicle_timeseries()**
- Converted into **raw_metrics** per vehicle

### **2. LangGraph Workflow Execution**
- **ingest → anomaly detection → diagnosis → customer engagement → service scheduling → feedback → manufacturing insights**

### **3. RCA and UEBA Layers**
- RCA **correlates failures** to root causes
- UEBA monitors **agent behavior and risk**

### **4. Backend APIs**
- **FastAPI** runs workflows
- Exposes **vehicle-level** and **fleet-level** insights

### **5. Frontend Visualization**
- **Next.js dashboard** consumes APIs via proxy routes
- Renders **fleet status**, **workflows**, and **analytics**

---

## 🧩 RCA — Root Cause Analysis Engine

### What It Provides
- **Symptom → Component → Process → Manufacturing Insight** causal chains  
- **Fleet-level aggregated RCA summaries** to identify systemic issues  
- **Graph-style cause–effect visualization** for transparent diagnostics  
- Explainable reasoning suitable for **OEM, QA, and manufacturing teams**

### Key Capabilities
- Translates raw anomalies into **actionable root causes**
- Correlates recurring failures across vehicles, parts, and time windows
- Bridges the gap between **aftersales operations and manufacturing feedback loops**

### Key Endpoints
- **GET `/rca/summary`** — Fleet-level RCA aggregation and top failure drivers  
- **GET `/rca/heatmap`** — Failure frequency over time
- **GET `/rca/supplier-risk`** — Supplier risk ranking  
- **GET `/rca/graph`** — Vehicle-specific RCA causal graph  


---

## 🛡 UEBA — User & Entity Behavior Analytics

### What It Provides
- **Agent-level risk scoring** for operational and decision anomalies  
- **Behavioral baselines** derived from historical agent actions  
- **Risk trends over time** for early insider-risk or process deviations  
- **Explainable risk factors** for governance and audit readiness  

### Key Capabilities
- Detects abnormal behavior in **agent workflows, overrides, and decisions**
- Differentiates between **skill gaps, process drift, and malicious patterns**
- Supports **enterprise compliance, trust, and accountability**

### Key Endpoints
- **GET `/ueba/summary`** — Overall UEBA risk posture with highest risk agent and risk score
- **GET `/ueba/risk-ranking`** — Ranked list of agents by risk score
- **GET `/ueba/agent/{agent_id}`** — Shows raw behavioral stats  for selected agent  
- **GET `/ueba/risk-trend/{agent_id}`** — Temporal risk evolution  
- **GET `/ueba/explain/{agent_id}`** — Explainable drivers behind risk score  


---


## 🏗 **Architecture Diagram**
<img width="668" height="449" alt="image" src="https://github.com/user-attachments/assets/e413bac3-f368-4405-be51-9a788136ea92" />


---

## 🔄 **Flow Chart**
<img width="872" height="430" alt="image" src="https://github.com/user-attachments/assets/4146d364-a27a-4b45-ae77-ec1bd1aefadd" />

---

## 🖥 **Screenshots**
<img width="736" height="343" alt="image" src="https://github.com/user-attachments/assets/4da9709c-f75e-499d-ac36-00e98f618837" />

<img width="736" height="343" alt="unamed" src="https://github.com/user-attachments/assets/a9d3986b-7008-4e41-9591-05b27e663a0b" />

---

## 🚀 **Getting Started**

## **Backend Setup**
- `pip install -r requirements.txt`
- `python api_server.py`
- Runs at: **http://localhost:8000**
- Requires **AgenticAI_Final_Format_Dataset.xlsx** in project root

## **Frontend Setup**
- `cd frontend`
- `npm install`
- `npm run dev`
- Runs at: **http://localhost:3000**
- Uses **Next.js API routes** to proxy requests to FastAPI
- Set **API_BASE_URL** if backend URL differs

---

## 🔌 **Backend APIs**
- **GET /** — Health check
- **GET /api/vehicles** — Workflow results for all vehicles
- **GET /api/vehicles/{vehicle_id}** — Single vehicle workflow
- **GET /api/stats** — Aggregated fleet metrics
- **GET /api/manufacturing** — Manufacturing and OEM insights

---

## 📊 **Frontend Dashboard**

## **Available Screens**

### **Vehicle Dashboard**
- Fleet cards showing **anomalies**, **diagnosis**, **service schedules**, and **feedback**

### **Workflow Visualization**
- **LangGraph pipeline** with step-by-step execution status

### **Analytics & Insights**
- **Recharts-based charts**
- Manufacturing insight tables

### Unified One-Page View
- **Fleet anomaly overview** with severity indicators  
- **Interactive RCA graph visualization**  
- **UEBA risk leaderboard** for agents and entities  
- **Explainability panels** (why an alert was triggered)  
- **Trend analytics** for failures, risks, and resolutions  

Designed to give **CXOs, aftersales heads, and risk teams** a single, trusted control plane.

---

## 🏢 Enterprise Considerations

✔ **Modular & microservice-ready architecture**  
✔ **Explainable AI (XAI)** for trust and adoption  
✔ **Governance-ready UEBA layer** (audit & compliance friendly)  
✔ **Extensible to IoT, cloud, and real-time telemetry streams**  
✔ **Neo4j-compatible graph architecture** for large-scale RCA reasoning  


---

## 📈 Impact Metrics

- Reduction in **unplanned vehicle breakdowns**  
- Improved **service scheduling efficiency & workshop utilization**  
- **Faster root cause identification** and resolution cycles  
- Increased **customer satisfaction & retention** through proactive engagement  
- **Agent decision accuracy & confidence scores**  
- Reduced **end-to-end workflow turnaround time**  
- Decrease in **recurring manufacturing and design defects**  


---

## 🧠 **Tech Stack**
| Layer | Technology |
|------|------------|
| Backend APIs | **FastAPI** |
| Core Logic | **Python** |
| Agent Orchestration | **LangGraph** |
| RCA Reasoning | **Neo4j-compatible Graph Model** |
| UEBA Detection | **Isolation Forest** |
| Data Processing | **Pandas / NumPy** |
| Frontend | **Next.js / React / TypeScript** |
| UI | **Tailwind CSS (EY Black & Yellow Theme)** |
| Deployment | **Docker (Extensible)** |

---

## 👋 **Hi, We are the makers of Echelon-AI!**

## **About Us**
- Meet the creators behind **Echelon-AI — Automotive Aftersales Predictive Maintenance**
- **Aditi A, Aditi B, Arnav, and Nikhil**

We are a passionate team focused on building **intelligent, production-grade AI systems** that solve real-world industry problems. This project reflects our interest in **agentic AI**, **predictive analytics**, and **scalable system design**, combining multi-agent orchestration, deep learning, and modern full-stack development.

Our goal is to move beyond **reactive workflows** and enable **proactive, explainable, and data-driven decision-making** for enterprises. Through this project, we explore how **autonomous agents** and **temporal intelligence** can transform traditional automotive aftersales into a smarter, connected ecosystem.

- Aditi - [Aditi Agale](https://www.linkedin.com/in/aditi-agale-981372289/) 
- Aditi - [Aditi Bambal](https://www.linkedin.com/in/aditi-bambal-06640328b/) 
- Arnav - [Arnav Parekar](https://linkedin.com/in/arnav-parekar-b55786287/)
- Nikhil - [Nikhil Parkar](https://www.linkedin.com/in/nikhil-parkar-49b600274/)

---

## 💯 **Happy Coding**
**Made with love ❤️**
