import pandas as pd
import joblib

# Load trained model
model = joblib.load("Models/ddos_final_model.pkl")

print("Model Loaded Successfully")

# Example: simulate one window from your system
# (later we will connect real-time data here)

sample = pd.DataFrame([{

    "Total_Bytes_per_sec": 500000,
    "Total_Pkts_per_sec": 1200,
    "Total_Packets": 800,
    "Total_Bytes": 600000,
    "Avg_Packet_Size": 500,
    "Flow_Duration": 5,
    "Pkt_Size_Mean": 450,
    "Pkt_Size_Std": 120,
    "Pkt_Size_Max": 900,
    "Pkt_Size_Min": 60

}])

# Predict
prediction = model.predict(sample)

if prediction[0] == 0:
    print("Result: BENIGN TRAFFIC")
else:
    print("Result: ⚠ DDOS ATTACK DETECTED")