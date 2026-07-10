import pandas as pd
import psycopg2
import joblib
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# =====================================================
# LOAD MODEL
# =====================================================

model = joblib.load("Models/ddos_final_model.pkl")
print("Random Forest Model Loaded Successfully")

# =====================================================
# DATABASE CONNECTION
# =====================================================

conn = psycopg2.connect(
    host="localhost",
    database="Sflow_db",
    user="postgres",
    password="Sahil",
    port="5432"
)

query = """
SELECT
flow_duration,
tot_fwd_pkts,
tot_bwd_pkts,
totlen_fwd_pkts,
totlen_bwd_pkts,
flow_byts_per_sec,
flow_pkts_per_sec,
fwd_pkts_per_sec,
bwd_pkts_per_sec,
actual_label
FROM ml_test_dataset
ORDER BY id;
"""

df = pd.read_sql(query, conn)
conn.close()

print("\nRows Loaded :", len(df))

WINDOW_SIZE = 5

# =====================================================
# PREPARE FEATURES
# =====================================================

def prepare_features(data):
    X = pd.DataFrame()
    X["Flow Duration"] = data["flow_duration"]
    X["Tot Fwd Pkts"] = data["tot_fwd_pkts"]
    X["Tot Bwd Pkts"] = data["tot_bwd_pkts"]
    X["TotLen Fwd Pkts"] = data["totlen_fwd_pkts"]
    X["TotLen Bwd Pkts"] = data["totlen_bwd_pkts"]
    X["Flow Byts/s"] = data["flow_byts_per_sec"]
    X["Flow Pkts/s"] = data["flow_pkts_per_sec"]
    X["Fwd Pkts/s"] = data["fwd_pkts_per_sec"]
    X["Bwd Pkts/s"] = data["bwd_pkts_per_sec"]
    return X

# =====================================================
# WINDOW EVALUATION
# =====================================================

def evaluate_dataset(dataframe, expected_label, dataset_name):

    X = prepare_features(dataframe)

    predictions = []
    actuals = []
    confidences = []

    print("\n" + "#" * 120)
    print(f"{dataset_name} DATASET")
    print("#" * 120)

    for i in range(len(X) - WINDOW_SIZE + 1):

        window = X.iloc[i:i+WINDOW_SIZE]
        sample = pd.DataFrame([window.mean()])

        pred = model.predict(sample)[0]
        prob = model.predict_proba(sample)[0]
        conf = max(prob) * 100

        predictions.append(pred)
        actuals.append(expected_label)
        confidences.append(conf)

        print("\n" + "=" * 100)
        print(f"{dataset_name} WINDOW {i+1}")
        print("=" * 100)

        print("\nWINDOW DATA")
        print(window.to_string(index=False))

        print("\nWINDOW MEAN")
        print(sample.to_string(index=False))

        print()
        print(f"Actual      : {'DDOS' if expected_label else 'BENIGN'}")
        print(f"Prediction  : {'DDOS' if pred else 'BENIGN'}")
        print(f"Confidence  : {conf:.2f}%")
        print(f"Status      : {'Correct' if pred==expected_label else 'Wrong'}")

    print("\n" + "-" * 100)
    print(f"{dataset_name} PERFORMANCE")
    print("-" * 100)

    acc = accuracy_score(actuals, predictions)
    print(f"Accuracy : {acc*100:.2f}%")
    print("\nConfusion Matrix:")
    print(confusion_matrix(actuals, predictions))
    print("\nClassification Report:")
    print(classification_report(actuals, predictions, zero_division=0))

    results = pd.DataFrame({
        "Window": range(1, len(predictions)+1),
        "Actual": ["DDOS" if expected_label else "BENIGN"]*len(predictions),
        "Prediction": ["DDOS" if x else "BENIGN" for x in predictions],
        "Confidence (%)": [round(x,2) for x in confidences]
    })

    return results, actuals, predictions

# =====================================================
# SPLIT DATA
# =====================================================

benign_df = df[df["actual_label"] == 0].reset_index(drop=True)
ddos_df = df[df["actual_label"] == 1].reset_index(drop=True)

benign_results, benign_actual, benign_pred = evaluate_dataset(
    benign_df, 0, "BENIGN"
)

ddos_results, ddos_actual, ddos_pred = evaluate_dataset(
    ddos_df, 1, "DDOS"
)

# =====================================================
# OVERALL PERFORMANCE
# =====================================================

overall_actual = benign_actual + ddos_actual
overall_pred = benign_pred + ddos_pred

print("\n" + "#" * 120)
print("OVERALL MODEL PERFORMANCE")
print("#" * 120)

print(f"Accuracy : {accuracy_score(overall_actual, overall_pred)*100:.2f}%")
print("\nConfusion Matrix:")
print(confusion_matrix(overall_actual, overall_pred))
print("\nClassification Report:")
print(classification_report(overall_actual, overall_pred, zero_division=0))

print("\nFINAL BENIGN RESULTS")
print(benign_results.to_string(index=False))

print("\nFINAL DDOS RESULTS")
print(ddos_results.to_string(index=False))
