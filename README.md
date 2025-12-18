# EY Agentic AI — Automotive Aftersales Predictive Maintenance

Production-grade, multi-agent LangGraph workflow with an LSTM anomaly detector for automotive aftersales. Includes a FastAPI backend serving real vehicle insights from the provided Excel telemetry dataset and a Next.js + Tailwind (EY black/yellow theme) frontend for monitoring, workflow visualization, and analytics.

## High-Level Overview

- **Agents (LangGraph nodes)**: ingest → anomaly detection (LSTM) → diagnosis → engagement → scheduling → feedback → manufacturing insights.
- **Model**: PyTorch LSTM autoencoder for reconstruction-error–based temporal anomaly detection (configurable thresholds).
- **Data**: `AgenticAI_Final_Format_Dataset.xlsx` (7-day, 30-minute telemetry; 7 parameters per vehicle).
- **Backend**: FastAPI server (`api_server.py`) that loads the dataset, runs the LangGraph workflow per vehicle, and exposes REST APIs.
- **Frontend**: Next.js + Tailwind dashboard (EY black/yellow theme) consuming backend APIs via Next.js route proxies.

## Repository Layout

- `app/` — Core Python backend logic
  - `state.py` — Typed system state for LangGraph
  - `config.py` — Hyperparameters and thresholds
  - `graph.py` — LangGraph StateGraph wiring all agents
  - `agents/` — Six worker agents + ingest
  - `models/lstm_anomaly.py` — PyTorch LSTM autoencoder + train/infer stubs
  - `utils/data_loader.py` — Excel loader → per-vehicle telemetry (`raw_metrics`)
- `api_server.py` — FastAPI server exposing workflow results
- `requirements.txt` — Python dependencies
- `frontend/` — Next.js + Tailwind UI
  - `app/` — Next.js App Router pages and API route proxies
  - `components/` — Dashboard, workflow viz, stats
  - `types/` — Shared TS interfaces
- `QUICKSTART.md` — One-page run instructions
- `README_API.md` — Backend API details

## How It Works

1) **Data ingest**: Excel → `load_vehicle_timeseries` → `raw_metrics` per vehicle  
2) **Workflow (LangGraph)**: ingest → anomaly (LSTM) → diagnosis (rule map) → engagement → scheduling → feedback → manufacturing payload  
3) **API**: FastAPI runs workflow per vehicle and serves `/api/vehicles`, `/api/stats`, `/api/manufacturing`  
4) **Frontend**: Next.js calls its own `/api/*` routes (proxying to Python API) and renders dashboards (fleet, workflow, analytics)

## Run the System

1. **Backend**
   ```bash
   pip install -r requirements.txt
   python api_server.py
   ```
   - Serves at `http://localhost:8000`
   - Requires `AgenticAI_Final_Format_Dataset.xlsx` in project root

2. **Frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```
   - Opens at `http://localhost:3000`
   - Proxies to backend via Next.js API routes; set `API_BASE_URL` env if backend URL differs

## Key Endpoints (Backend)

- `GET /` — Health
- `GET /api/vehicles` — Workflow results for all vehicles
- `GET /api/vehicles/{vehicle_id}` — Single vehicle
- `GET /api/stats` — Aggregated stats (anomalies, schedules, accuracy, ratings)
- `GET /api/manufacturing` — Manufacturing/OEM payloads

## Frontend Screens

- **Vehicle Dashboard** — Fleet cards showing anomalies, diagnosis, schedule, feedback
- **Workflow Visualization** — LangGraph pipeline with step status
- **Analytics & Insights** — Charts (Recharts) + manufacturing insights table



