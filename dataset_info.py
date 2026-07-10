import pandas as pd

# Change the filename to one of the CSVs you downloaded
df = pd.read_csv("Dataset/DDOS attack-HOIC.csv")

print("\nFirst 5 Rows")
print(df.head())

print("\nDataset Shape")
print(df.shape)

print("\nColumn Names")
print(df.columns.tolist())

print("\nData Types")
print(df.dtypes)

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

print("\nLabel Distribution")
print(df["Label"].value_counts())