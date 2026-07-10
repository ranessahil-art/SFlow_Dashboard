import pandas as pd


# ---------------------------------------
# Load CIC Dataset
# ---------------------------------------

file_path = "Dataset/DDOS attack-HOIC.csv"

df = pd.read_csv(file_path)


print("Original Dataset:")
print(df.shape)


# ---------------------------------------
# Separate classes
# ---------------------------------------

benign = df[df["Label"] == "Benign"]

ddos = df[df["Label"] != "Benign"]


print("\nBenign Samples:")
print(len(benign))

print("DDOS Samples:")
print(len(ddos))


# ---------------------------------------
# Select random samples
# ---------------------------------------

# Keep original row numbers
df = df.reset_index()

# Separate classes
benign = df[df["Label"] == "Benign"]
ddos = df[df["Label"] != "Benign"]

# ---------------------------------------
# Select consecutive samples
# ---------------------------------------

# First 100 Benign rows
benign_sample = benign.iloc[:100]

# First 100 DDOS rows
ddos_sample = ddos.iloc[:100]

# Combine while preserving order
test_df = pd.concat([
    benign_sample,
    ddos_sample
])

# ---------------------------------------
# Extract only ML Features
# ---------------------------------------

ml_test = pd.DataFrame()


ml_test["Flow_Duration"] = test_df["Flow Duration"]

ml_test["Tot_Fwd_Pkts"] = test_df["Tot Fwd Pkts"]

ml_test["Tot_Bwd_Pkts"] = test_df["Tot Bwd Pkts"]

ml_test["TotLen_Fwd_Pkts"] = test_df["TotLen Fwd Pkts"]

ml_test["TotLen_Bwd_Pkts"] = test_df["TotLen Bwd Pkts"]

ml_test["Flow_Byts_per_sec"] = test_df["Flow Byts/s"]

ml_test["Flow_Pkts_per_sec"] = test_df["Flow Pkts/s"]

ml_test["Fwd_Pkts_per_sec"] = test_df["Fwd Pkts/s"]

ml_test["Bwd_Pkts_per_sec"] = test_df["Bwd Pkts/s"]


# Actual Label

ml_test["Actual_Label"] = test_df["Label"].apply(
    lambda x: 0 if x == "Benign" else 1
)


print("\nFinal Test Dataset:")
print(ml_test.head())


print("\nLabel Distribution:")
print(
    ml_test["Actual_Label"].value_counts()
)


# Save CSV also for checking

ml_test.to_csv(
    "ml_test_dataset.csv",
    index=False
)


print("\nSaved successfully")