import pandas as pd

# Load CIC Dataset
df = pd.read_csv("Dataset/DDOS attack-HOIC.csv")

print("Original Shape:", df.shape)

# -----------------------------------
# Final Reliable Features
# -----------------------------------

features = [

    "Flow Duration",

    "Tot Fwd Pkts",
    "Tot Bwd Pkts",

    "TotLen Fwd Pkts",
    "TotLen Bwd Pkts",

    "Flow Byts/s",
    "Flow Pkts/s",

    "Fwd Pkts/s",
    "Bwd Pkts/s",

    "Label"

]

# Select only required columns
df_final = df[features].copy()

# -----------------------------------
# Convert Label
# -----------------------------------

df_final["Label"] = df_final["Label"].apply(
    lambda x: 0 if x == "Benign" else 1
)

print("\nFinal Dataset Shape:", df_final.shape)

print("\nLabel Distribution:")
print(df_final["Label"].value_counts())

# -----------------------------------
# Save Final Dataset
# -----------------------------------

df_final.to_csv(
    "final_training_dataset.csv",
    index=False
)

print("\nFinal Training Dataset Saved Successfully!")