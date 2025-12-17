import numpy as np
import pandas as pd
import random
from datetime import datetime, timedelta

# ------------------------------
# CONFIGURATION
# ------------------------------
NUM_VEHICLES = 1000
DAYS = 90
READINGS_PER_DAY = 24  # hourly
TOTAL_HOURS = DAYS * READINGS_PER_DAY

np.random.seed(42)
random.seed(42)

# ------------------------------
# HELPER FUNCTIONS
# ------------------------------
def random_choice_weighted(options):
    values, weights = zip(*options)
    return random.choices(values, weights=weights, k=1)[0]

def generate_failure_code():
    return random_choice_weighted([
        ("P0300", 0.1), ("P0420", 0.15), ("P0171", 0.2),
        ("P0455", 0.1), ("NONE", 0.45)
    ])

# RCA mapping support
PARTS = ["Engine Pump", "Battery", "Fuel Injector", "Brake Pad", "Alternator"]
SUPPLIERS = ["S1-Motherson", "S2-Bosch", "S3-Delphi", "S4-Denso"]
FAILURE_MODES = ["Leakage", "Wear", "Overheating", "Electrical Fault"]
MODELS = ["A1", "A2", "B1", "B2"]
PLANTS = ["Plant-1", "Plant-2"]

# ------------------------------
# 1️⃣ VEHICLE METADATA (1,000 rows)
# ------------------------------
metadata = pd.DataFrame({
    "vehicle_id": [f"V{i:04d}" for i in range(NUM_VEHICLES)],
    "model": np.random.choice(MODELS, NUM_VEHICLES),
    "variant": np.random.choice(["Base", "Mid", "Top"], NUM_VEHICLES),
    "year": np.random.choice([2020, 2021, 2022, 2023], NUM_VEHICLES),
    "engine_type": np.random.choice(["Petrol", "Diesel", "EV"], NUM_VEHICLES),
    "supplier_id": np.random.choice(SUPPLIERS, NUM_VEHICLES),
    "manufacturing_plant": np.random.choice(PLANTS, NUM_VEHICLES),
})
metadata.to_csv("vehicle_metadata.csv", index=False)

# ------------------------------
# 2️⃣ HOURLY TELEMETRY DATA (2.16 million rows)
# ------------------------------
rows = []
start = datetime(2023, 1, 1)

for vid in metadata["vehicle_id"]:
    ts = start
    for _ in range(TOTAL_HOURS):
        rows.append([
            vid, ts,
            np.random.normal(70, 5),  # engine temp
            np.random.normal(40, 3),  # coolant temp
            np.random.normal(35, 2),  # oil pressure
            np.random.normal(12.5, 0.3),  # battery voltage
            np.random.uniform(10, 100),  # fuel level
            np.random.uniform(28, 35), np.random.uniform(28, 35),
            np.random.uniform(28, 35), np.random.uniform(28, 35),  # tire pressures
            np.random.randint(700, 3000),  # rpm
            np.random.randint(0, 120),  # speed
            np.random.normal(40, 5),  # brake pressure
            np.random.randint(1, 6),  # gear
            np.random.uniform(0, 1),  # ABS sensor
            np.random.uniform(-30, 30),  # steering angle
            generate_failure_code(),  # DTC code
            np.random.uniform(0.8, 1.2),  # MAF
            np.random.uniform(0.85, 1.15),  # O2 sensor
            np.random.uniform(5, 95),  # throttle
            np.random.randint(0, 5),  # misfire
            np.random.uniform(200, 400),  # emissions
            np.random.uniform(50, 100),  # vehicle load
            np.random.uniform(20, 40),  # intake air temp
        ])
        ts += timedelta(hours=1)

telemetry_cols = [
    "vehicle_id", "timestamp", "engine_temp", "coolant_temp", "oil_pressure",
    "battery_voltage", "fuel_level", "tire_fl_psi", "tire_fr_psi",
    "tire_rl_psi", "tire_rr_psi", "rpm", "speed", "brake_pressure",
    "gear_position", "abs_sensor", "steering_angle", "dtc_code",
    "maf", "o2_sensor", "throttle", "misfire", "emissions",
    "vehicle_load", "intake_air_temp"
]

telemetry_df = pd.DataFrame(rows, columns=telemetry_cols)
telemetry_df.to_csv("telemetry.csv", index=False)

# ------------------------------
# 3️⃣ SERVICE HISTORY
# ------------------------------
service_rows = []
for vid in metadata["vehicle_id"]:
    num_repairs = np.random.randint(1, 6)
    for _ in range(num_repairs):
        service_rows.append([
            vid,
            random_choice_weighted([("Routine", 0.6), ("Breakdown", 0.4)]),
            random.choice(PARTS),
            random.choice(FAILURE_MODES),
            random.randint(1, 5),  # severity
            np.random.randint(1, 365),  # days since last service
            np.random.randint(0, 4),  # breakdowns
            np.random.randint(1, 6),  # customer satisfaction
        ])

service_df = pd.DataFrame(service_rows, columns=[
    "vehicle_id","service_type","failed_part","failure_mode",
    "severity","days_since_last_service","prev_breakdowns",
    "customer_satisfaction"
])
service_df.to_csv("service_history.csv", index=False)

# ------------------------------
# 4️⃣ CUSTOMER INTERACTIONS
# ------------------------------
interaction_rows = []
for vid in metadata["vehicle_id"]:
    for _ in range(np.random.randint(5, 15)):
        interaction_rows.append([
            vid,
            random_choice_weighted([("App", 0.5), ("SMS", 0.3), ("Voice", 0.2)]),
            random.choice(["Yes", "No"]),
            random.uniform(1, 24),
            np.random.randint(0, 3),
        ])
customer_df = pd.DataFrame(interaction_rows, columns=[
    "vehicle_id", "channel", "alert_acknowledged", "response_time_hr", "reschedule_count"
])
customer_df.to_csv("customer_interactions.csv", index=False)

# ------------------------------
# 5️⃣ WORKSHOP DATA
# ------------------------------
workshop_df = pd.DataFrame({
    "workshop_id": [f"W{i:03d}" for i in range(20)],
    "capacity_percent": np.random.uniform(40, 100, 20),
    "tech_available": np.random.randint(5, 20, 20),
    "inventory_score": np.random.uniform(0.5, 1.0, 20)
})
workshop_df.to_csv("workshops.csv", index=False)

# ------------------------------
# 6️⃣ AGENT PERFORMANCE LOGS
# ------------------------------
agent_logs = []
agents = ["anomaly", "diagnosis", "scheduling", "engagement", "feedback", "manufacturing"]

for _ in range(5000):
    agent_logs.append([
        random.choice(agents),
        datetime.now() - timedelta(hours=random.randint(1, 500)),
        np.random.uniform(0.7, 0.99),  # accuracy
        np.random.uniform(0.1, 2.0),  # latency
        np.random.uniform(0.5, 1.0)   # satisfaction
    ])
agent_df = pd.DataFrame(agent_logs, columns=[
    "agent", "timestamp", "accuracy", "latency", "satisfaction"
])
agent_df.to_csv("agent_logs.csv", index=False)

# ------------------------------
# 7️⃣ RCA GRAPH DATA
# ------------------------------
rca_rows = []
for _ in range(2000):
    rca_rows.append([
        random.choice(PARTS),
        random.choice(SUPPLIERS),
        random.choice(MODELS),
        random.choice(FAILURE_MODES),
        random.randint(1, 5),
        np.random.randint(1, 1000),
        random.choice(PLANTS)
    ])
rca_df = pd.DataFrame(rca_rows, columns=[
    "part_id","supplier_id","vehicle_model",
    "failure_mode","severity","occurrence_count","plant"
])
rca_df.to_csv("rca_graph.csv", index=False)

# ------------------------------
# 8️⃣ UEBA LOGS
# ------------------------------
ueba_rows = []
actions = ["read", "update", "predict", "write", "alert"]

for _ in range(3000):
    ueba_rows.append([
        random.choice(agents),
        datetime.now() - timedelta(hours=random.randint(1, 300)),
        random.choice(actions),
        np.random.uniform(0, 1),  # risk score
        random.choice(["Normal", "Suspicious"]),
    ])

ueba_df = pd.DataFrame(ueba_rows, columns=[
    "agent_id","timestamp","action","risk_score","status"
])
ueba_df.to_csv("ueba_logs.csv", index=False)

# ------------------------------
# 9️⃣ LABELS (For ML Training)
# ------------------------------
labels = []
for vid in metadata["vehicle_id"]:
    labels.append([
        vid,
        random.choice(["Normal", "Anomaly"]),
        random.choice(FAILURE_MODES),
        np.random.randint(10, 500)  # time to failure
    ])
label_df = pd.DataFrame(labels, columns=[
    "vehicle_id","status","failure_type","time_to_failure_hr"
])
label_df.to_csv("labels.csv", index=False)

print("All datasets generated successfully!")
