# EY Agentic AI — Automotive Aftersales Predictive Maintenance

---

## 📑 Table of Contents
- [Introduction](#-introduction)
- [Project Overview](#-project-overview)
- [Repository Structure](#-repository-structure)
- [System Architecture & Workflow](#-system-architecture--workflow)
- [Architecture Diagram](#-architecture-diagram)
- [Flow Chart](#-flow-chart)
- [Screenshots](#-screenshots)
- [Getting Started](#-getting-started)
- [Backend APIs](#-backend-apis)
- [Frontend Dashboard](#-frontend-dashboard)
- [Tech Stack](#-tech-stack)
- [About Us](#-about-us)

---

## 💡 Introduction

### **Problem Statement**
Automotive aftersales maintenance is largely **reactive**. Vehicles are serviced only after failures occur, leading to:
- Unexpected breakdowns  
- Customer dissatisfaction  
- Inefficient service center workloads  
- Delayed feedback to manufacturing teams  

### **Solution**
**EY Agentic AI — Automotive Aftersales Predictive Maintenance** introduces a **production-grade, multi-agent AI system** that:
- Continuously monitors vehicle telemetry  
- Detects anomalies *before* failures occur  
- Diagnoses root causes  
- Schedules service actions  
- Collects feedback  
- Generates actionable manufacturing insights  

All powered through an **autonomous LangGraph-driven workflow**.

---

## 🚗 Project Overview

### **Agents (LangGraph nodes)**
ingest → anomaly detection (LSTM) → diagnosis → engagement → scheduling → feedback → manufacturing insights

yaml
Copy code

### **Model**
- **PyTorch LSTM Autoencoder**
- Reconstruction-error–based **temporal anomaly detection**
- Configurable thresholds for production tuning

### **Data**
**AgenticAI_Final_Format_Dataset.xlsx**
- 7-day telemetry window  
- 30-minute intervals  
- 7 parameters per vehicle  

### **Backend**
- **FastAPI** server
- Executes LangGraph workflow **per vehicle**
- Exposes REST APIs for fleet-level insights

### **Frontend**
- **Next.js + Tailwind CSS**
- EY black/yellow theme
- Dashboards for monitoring, workflow visualization, and analytics

---

## 🗂 Repository Structure

```text
app/
 ├─ state.py                  # Typed system state for LangGraph
 ├─ config.py                 # Hyperparameters and thresholds
 ├─ graph.py                  # LangGraph StateGraph wiring all agents
 ├─ agents/                   # Ingest + six worker agents
 ├─ models/
 │   └─ lstm_anomaly.py        # LSTM autoencoder (train / infer stubs)
 ├─ utils/
 │   └─ data_loader.py        # Excel loader → per-vehicle telemetry
api_server.py                 # FastAPI server
requirements.txt              # Python dependencies
frontend/
 ├─ app/                      # Next.js App Router + API proxies
 ├─ components/               # Dashboard, workflow viz, stats
 └─ types/                    # Shared TypeScript interfaces
QUICKSTART.md                 # One-page run instructions
README_API.md                 # Backend API documentation
```
## 🔁 **System Architecture & Workflow**

## **How It Works**

### **1. Data Ingest**
- **Excel telemetry**
- **load_vehicle_timeseries()**
- Converted into **raw_metrics** per vehicle

### **2. LangGraph Workflow Execution**
- **ingest → anomaly detection → diagnosis → customer engagement → service scheduling → feedback → manufacturing insights**

### **3. Backend APIs**
- **FastAPI** runs workflows
- Exposes **vehicle-level** and **fleet-level** insights

### **4. Frontend Visualization**
- **Next.js dashboard** consumes APIs via proxy routes
- Renders **fleet status**, **workflows**, and **analytics**

---

## 🏗 **Architecture Diagram**
<img width="512" height="371" alt="flow chart" src="https://github.com/user-attachments/assets/3bfcc89f-fa47-484b-a956-b086226f022d" />

---

## 🔄 **Flow Chart**
<img width="512" height="339" alt="flow_chart" src="https://github.com/user-attachments/assets/e1b92427-75f5-40ee-b74f-3794931b4b50" />

---

## 🖥 **Screenshots**
<img width="512" height="232" alt="unamed" src="https://github.com/user-attachments/assets/b09bf875-eabd-4bec-966f-f48dbbaf5d64" />
<img width="512" height="232" alt="unamed" src="https://github.com/user-attachments/assets/17a1257b-1a99-4671-9bb4-dd7013193cdc" />


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

---

## 🧠 **Tech Stack**
- **Python / FastAPI** — Backend APIs and orchestration
- **LangGraph** — Multi-agent workflow framework
- **PyTorch** — LSTM autoencoder for anomaly detection
- **Pandas / NumPy** — Telemetry data processing
- **Next.js** — Frontend framework
- **Tailwind CSS** — EY black/yellow UI theme
- **Recharts** — Data visualization

---

## 👋 **Hi, We are the makers of EY Agentic AI!**

## **About Us**
- Meet the creators behind **EY Agentic AI — Automotive Aftersales Predictive Maintenance**
- **Aditi A, Aditi B, Arnav, and Nikhil**

We are a passionate team focused on building **intelligent, production-grade AI systems** that solve real-world industry problems. This project reflects our interest in **agentic AI**, **predictive analytics**, and **scalable system design**, combining multi-agent orchestration, deep learning, and modern full-stack development.

Our goal is to move beyond **reactive workflows** and enable **proactive, explainable, and data-driven decision-making** for enterprises. Through this project, we explore how **autonomous agents** and **temporal intelligence** can transform traditional automotive aftersales into a smarter, connected ecosystem.

- **Aditi — Aditi Agale**
- **Aditi — Aditi Bambal**
- **Arnav — Arnav Parekar**
- **Nikhil — Nikhil Parkar**

---

## 💯 **Happy Coding**
**Made with love ❤️**
