import pandas as pd
import joblib

# -------------------------------
# LOAD DATA
# -------------------------------

df = pd.read_csv("final_training_dataset.csv")

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

    "Flow Duration",

    "Tot Fwd Pkts",
    "Tot Bwd Pkts",

    "TotLen Fwd Pkts",
    "TotLen Bwd Pkts",

    "Flow Byts/s",
    "Flow Pkts/s",

    "Fwd Pkts/s",
    "Bwd Pkts/s"

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