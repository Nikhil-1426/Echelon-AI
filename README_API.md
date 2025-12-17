# API Server Setup

## Python Backend API Server

The FastAPI server exposes the LangGraph workflow as REST endpoints.

### Installation

```bash
pip install -r requirements.txt
```

### Running the API Server

```bash
python api_server.py
```

The server will start on `http://localhost:8000`

### API Endpoints

- `GET /` - Health check
- `GET /api/vehicles` - Get all vehicles with workflow execution results
- `GET /api/vehicles/{vehicle_id}` - Get specific vehicle details
- `POST /api/workflow/run/{vehicle_id}` - Manually trigger workflow for a vehicle
- `GET /api/stats` - Get aggregated statistics
- `GET /api/manufacturing` - Get manufacturing insights payloads

### CORS

The API server is configured to allow requests from:
- `http://localhost:3000` (Next.js dev server)
- `http://127.0.0.1:3000`

### Data Flow

1. API server loads Excel dataset (`AgenticAI_Final_Format_Dataset.xlsx`)
2. For each vehicle, runs the complete LangGraph workflow:
   - Ingest → Anomaly Detection → Diagnosis → Engagement → Scheduling → Feedback → Manufacturing
3. Returns transformed data in frontend-friendly format

### Environment Variables

Set `API_BASE_URL` in Next.js frontend to point to your API server if different from default.

