import pandas as pd

# Load CIC dataset
df = pd.read_csv("Dataset/DDOS attack-HOIC.csv")

print("Original Shape:", df.shape)

# -----------------------------
# FINAL FEATURES (sFlow-compatible)
# -----------------------------

features = [

    "Flow Duration",

    "Tot Fwd Pkts",
    "Tot Bwd Pkts",

    "TotLen Fwd Pkts",
    "TotLen Bwd Pkts",

    "Flow Byts/s",
    "Flow Pkts/s",

    "Label"
]

df = df[features]

# -----------------------------
# Create sFlow-style mapping
# -----------------------------

df_final = pd.DataFrame()

df_final["Total_Bytes_per_sec"] = df["Flow Byts/s"]
df_final["Total_Pkts_per_sec"] = df["Flow Pkts/s"]

df_final["Total_Packets"] = df["Tot Fwd Pkts"] + df["Tot Bwd Pkts"]
df_final["Total_Bytes"] = df["TotLen Fwd Pkts"] + df["TotLen Bwd Pkts"]

df_final["Avg_Packet_Size"] = df_final["Total_Bytes"] / (df_final["Total_Packets"] + 1)

# Flow duration (safe)
df_final["Flow_Duration"] = df["Flow Duration"]

# -----------------------------
# Label
# -----------------------------

df_final["Label"] = df["Label"].apply(lambda x: 0 if x == "Benign" else 1)

print("\nFinal Dataset Shape:", df_final.shape)

print("\nLabel Distribution:")
print(df_final["Label"].value_counts())

# -----------------------------
# Save final dataset
# -----------------------------

df_final.to_csv("final_training_dataset.csv", index=False)

print("\nFINAL dataset saved successfully!")