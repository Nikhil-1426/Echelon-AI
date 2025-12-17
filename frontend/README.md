# EY Agentic AI Frontend

Next.js frontend for the Automotive Aftersales Predictive Maintenance system.

## Features

- **Vehicle Dashboard**: Real-time monitoring of vehicle fleet with anomaly detection status
- **Workflow Visualization**: Interactive LangGraph workflow pipeline visualization
- **Analytics & Insights**: Manufacturing intelligence with charts and metrics
- **EY Branding**: Black and yellow theme matching EY company colors

## Getting Started

### Install Dependencies

```bash
npm install
# or
yarn install
```

### Run Development Server

```bash
npm run dev
# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Main dashboard page
│   └── globals.css         # Global styles with EY theme
├── components/
│   ├── VehicleDashboard.tsx      # Vehicle fleet overview
│   ├── VehicleCard.tsx           # Individual vehicle card
│   ├── WorkflowVisualization.tsx # LangGraph workflow visualization
│   └── StatsOverview.tsx         # Analytics and charts
├── types/
│   └── index.ts            # TypeScript type definitions
└── package.json
```

## Integration with Backend

Currently uses mock data. To connect to the Python backend:

1. Create API routes in `app/api/` directory
2. Update components to fetch from API endpoints
3. Set up CORS on Python backend (FastAPI recommended)

Example API route structure:
- `GET /api/vehicles` - Get all vehicles
- `GET /api/vehicles/:id` - Get specific vehicle details
- `POST /api/workflow/run` - Trigger workflow execution

## Theme Colors

- **EY Black**: `#000000`
- **EY Yellow**: `#FFBE00`
- **EY Yellow Dark**: `#E6A800`
- **Gray**: `#1A1A1A`
- **Gray Light**: `#2A2A2A`

## Build for Production

```bash
npm run build
npm start
```

