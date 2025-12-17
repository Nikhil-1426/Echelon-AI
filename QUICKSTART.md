# Quick Start Guide

## Running the Complete System

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Start the Python API Server

In one terminal:

```bash
python api_server.py
```

The API server will start on `http://localhost:8000`

### Step 3: Install Frontend Dependencies

In another terminal:

```bash
cd frontend
npm install
```

### Step 4: Start the Next.js Frontend

```bash
npm run dev
```

The frontend will start on `http://localhost:3000`

### Step 5: Open in Browser

Navigate to `http://localhost:3000` to see the dashboard.

## Data Flow

1. **Excel Dataset** → Python backend loads `AgenticAI_Final_Format_Dataset.xlsx`
2. **Python Agents** → LangGraph workflow processes each vehicle:
   - Ingest Agent → loads telemetry
   - Anomaly Agent → LSTM detects anomalies
   - Diagnosis Agent → maps to failing parts
   - Engagement Agent → decides notifications
   - Scheduling Agent → assigns workshops
   - Feedback Agent → collects feedback
   - Manufacturing Agent → creates OEM payloads
3. **FastAPI Server** → Exposes workflow results as REST API
4. **Next.js API Routes** → Proxy requests to Python backend
5. **React Components** → Display real-time data from agents

## Verification

- Check API health: `http://localhost:8000/`
- Check vehicles: `http://localhost:8000/api/vehicles`
- Frontend dashboard: `http://localhost:3000`

## Troubleshooting

- **API not responding**: Ensure `AgenticAI_Final_Format_Dataset.xlsx` is in the project root
- **CORS errors**: Check that API server allows `localhost:3000`
- **No data**: Verify Excel file exists and has valid data
- **Port conflicts**: Change ports in `api_server.py` (8000) or `next.config.js` (3000)

