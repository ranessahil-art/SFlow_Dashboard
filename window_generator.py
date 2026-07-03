import pandas as pd
import joblib

# -------------------------------
# LOAD DATA
# -------------------------------

df = pd.read_csv("aligned_training_dataset.csv")

print("Dataset Loaded:", df.shape)

# -------------------------------
# LOAD MODEL
# -------------------------------

model = joblib.load("Models/ddos_rf_model.pkl")

print("Model Loaded Successfully")

# -------------------------------
# FEATURES (same as training)
# -------------------------------

feature_cols = [

    "Total_Bytes_per_sec",
    "Total_Pkts_per_sec",
    "Total_Packets",
    "Total_Bytes",
    "Avg_Packet_Size",
    "Flow_Duration",
    "Pkt_Size_Mean",
    "Pkt_Size_Std",
    "Pkt_Size_Max",
    "Pkt_Size_Min"

]

# -------------------------------
# WINDOW SIZE
# -------------------------------

WINDOW_SIZE = 5

print("Total Records:", len(df))

# -------------------------------
# WINDOW PROCESSING
# -------------------------------

for i in range(len(df) - WINDOW_SIZE + 1):

    window = df.iloc[i:i+WINDOW_SIZE]

    # create feature vector from window mean
    sample = pd.DataFrame([{

        col: window[col].mean() for col in feature_cols

    }])

    pred = model.predict(sample)[0]

    if pred == 0:
        print(f"Window {i}: 🟢 BENIGN")
    else:
        print(f"Window {i}: 🔴 DDOS DETECTED")

print("\nProcessing Completed")