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

        "Flow Duration": 5,

        "Tot Fwd Pkts": 400,
        "Tot Bwd Pkts": 380,

        "TotLen Fwd Pkts": 320000,
        "TotLen Bwd Pkts": 280000,

        "Flow Byts/s": 500000,

        "Flow Pkts/s": 1200,

        "Fwd Pkts/s": 620,

        "Bwd Pkts/s": 580

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