import joblib
import pandas as pd
import time

# Load final model
model = joblib.load("Models/ddos_final_model.pkl")

print("🚀 LIVE DDOS DETECTOR STARTED")

# -----------------------------
# SIMULATED LIVE STREAM (replace later with PyShark)
# -----------------------------

buffer = []

def get_live_sample():

    """
    This will later be replaced by PyShark live sFlow input
    """

    return {
        "Total_Bytes_per_sec": 500000,
        "Total_Pkts_per_sec": 1200,
        "Total_Packets": 800,
        "Total_Bytes": 600000,
        "Avg_Packet_Size": 500,
        "Flow_Duration": 5
    }

# -----------------------------
# REAL-TIME LOOP
# -----------------------------

WINDOW_SIZE = 5

while True:

    sample = get_live_sample()
    buffer.append(sample)

    if len(buffer) > WINDOW_SIZE:
        buffer.pop(0)

    if len(buffer) == WINDOW_SIZE:

        df = pd.DataFrame(buffer)

        features = pd.DataFrame([{
            col: df[col].mean() for col in df.columns
        }])

        prediction = model.predict(features)[0]

        if prediction == 0:
            print("🟢 BENIGN TRAFFIC")
        else:
            print("🔴 DDOS ATTACK DETECTED!")

    time.sleep(1)