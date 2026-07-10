import pandas as pd
import joblib

# Load trained model
model = joblib.load("Models/ddos_final_model.pkl")

print("Model Loaded Successfully")

# Example: simulate one window from your system
# (later we will connect real-time data here)

sample = pd.DataFrame([{

    "Flow Duration":5,

    "Tot Fwd Pkts":400,
    "Tot Bwd Pkts":380,

    "TotLen Fwd Pkts":320000,
    "TotLen Bwd Pkts":280000,

    "Flow Byts/s":500000,

    "Flow Pkts/s":1200,

    "Fwd Pkts/s":620,

    "Bwd Pkts/s":580

}])

# Predict
prediction = model.predict(sample)

if prediction[0] == 0:
    print("Result: BENIGN TRAFFIC")
else:
    print("Result: ⚠ DDOS ATTACK DETECTED")