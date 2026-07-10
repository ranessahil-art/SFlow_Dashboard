import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    accuracy_score
)

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------

df = pd.read_csv("final_training_dataset.csv")

print("Dataset Loaded Successfully")
print("Dataset Shape :", df.shape)

# --------------------------------------------------
# Features and Labels
# --------------------------------------------------

X = df.drop("Label", axis=1)
y = df["Label"]

print("\nFeatures Used:")

for feature in X.columns:
    print(" -", feature)

print("\nTotal Features :", len(X.columns))

# --------------------------------------------------
# Train Test Split
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=42,
    stratify=y
)

print("\nTraining Samples :", X_train.shape[0])
print("Testing Samples  :", X_test.shape[0])

# --------------------------------------------------
# Random Forest Model
# --------------------------------------------------

model = RandomForestClassifier(

    n_estimators=150,
    random_state=42,
    n_jobs=-1

)

print("\nTraining Random Forest Model...")

model.fit(X_train, y_train)

print("Training Completed Successfully!")

# --------------------------------------------------
# Prediction
# --------------------------------------------------

predictions = model.predict(X_test)

# --------------------------------------------------
# Evaluation
# --------------------------------------------------

print("\nAccuracy : {:.4f}".format(
    accuracy_score(y_test, predictions)
))

print("\nConfusion Matrix:")

print(
    confusion_matrix(
        y_test,
        predictions
    )
)

print("\nClassification Report:\n")

print(
    classification_report(
        y_test,
        predictions
    )
)

# --------------------------------------------------
# Feature Importance
# --------------------------------------------------

importance = pd.DataFrame({

    "Feature": X.columns,
    "Importance": model.feature_importances_

})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\nFeature Importance:\n")

print(importance)

# --------------------------------------------------
# Save Model
# --------------------------------------------------

joblib.dump(
    model,
    "Models/ddos_final_model.pkl"
)

print("\nModel Saved Successfully!")
print("Location : Models/ddos_final_model.pkl")