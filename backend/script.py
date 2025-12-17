import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Configuration
NUM_CUSTOMERS = 100
START_DATE = datetime(2025, 1, 1)
DAYS = 7
INTERVAL_MINUTES = 30

# Choices
vehicle_models = ["Model-X", "Model-Y", "Model-Z"]
suppliers = ["Supplier-A", "Supplier-B", "Supplier-C"]
dtc_codes = ["None", "P0135", "P0420", "P0300", "P0455", "U0121"]
dtc_prob = [0.80, 0.05, 0.05, 0.04, 0.03, 0.03]

# Timestamp generation
timestamps = []
current = START_DATE
for _ in range(int((24 * 60 / INTERVAL_MINUTES) * DAYS)):
    timestamps.append(current.strftime("%d-%m %H:%M"))
    current += timedelta(minutes=INTERVAL_MINUTES)

# Table structure
columns = ["Sr_No", "Customer", "Details", "Parameters"] + timestamps
final_df = pd.DataFrame(columns=columns)

# Data generation
sr_no = 1
for i in range(NUM_CUSTOMERS):
    cust = f"CUST{i+1:03d}"
    vehicle_id = f"VH{i+1:03d}"
    model = np.random.choice(vehicle_models)
    supplier = np.random.choice(suppliers)

    details = f"{vehicle_id}, {model}, {supplier}"

    parameters = [
        "Engine_Temperature",
        "Odometer",
        "Battery_SoC",
        "Speed",
        "Brake_Pressure",
        "Fuel_Status",
        "DTC_Code"
    ]

    odometer = np.random.randint(10000, 90000)

    for param in parameters:
        row = [sr_no, cust, details, param]

        for ts in timestamps:

            if param == "Engine_Temperature":
                val = round(np.clip(np.random.normal(85, 7), 60, 130), 2)
            elif param == "Battery_SoC":
                val = np.random.randint(20, 100)
            elif param == "Speed":
                val = np.random.randint(0, 120)
            elif param == "Brake_Pressure":
                val = np.random.randint(10, 90)
            elif param == "Odometer":
                odometer += np.random.randint(0, 5)
                val = odometer
            elif param == "Fuel_Status":
                val = np.random.randint(0, 100)
            elif param == "DTC_Code":
                val = np.random.choice(dtc_codes, p=dtc_prob)
            else:
                val = None

            row.append(val)

        final_df.loc[len(final_df)] = row

    sr_no += 1

# Save CSV
final_df.to_csv("AgenticAI_Final_Format_Dataset.csv", index=False)
print("🎯 Dataset saved as AgenticAI_Final_Format_Dataset.csv")