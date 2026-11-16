
# COGNIVEX AI
# Component: Random Forest Bug-Proneness Model

import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix
)

# Locate project folders
ml_folder = Path(__file__).parent

dataset_file = ml_folder / "dataset" / "bug_samples.csv"

model_folder = ml_folder / "models"
model_folder.mkdir(parents=True, exist_ok=True)

model_file = model_folder / "bug_prone_model.joblib"

print("===== COGNIVEX AI ML TRAINING =====")

# Load labelled dataset
df = pd.read_csv(dataset_file)

# Define input features
feature_columns = [
    "lines_of_code",
    "decision_points",
    "function_count",
    "has_eval",
    "has_hardcoded_secret"
]

# Validate dataset
required_columns = feature_columns + ["bug_prone"]

if not set(required_columns).issubset(df.columns):
    raise ValueError("Dataset is missing required columns.")

df = df[required_columns].dropna()

if not set(df["bug_prone"].unique()).issubset({0, 1}):
    raise ValueError("Labels must contain only 0 or 1.")

if df["bug_prone"].nunique() != 2:
    raise ValueError("Dataset must contain both classes.")

if df["bug_prone"].value_counts().min() < 2:
    raise ValueError("Need at least two records per class.")

# Separate features and labels
X = df[feature_columns]
y = df["bug_prone"].astype(int)

print("Total training examples available:", len(df))

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training records:", len(X_train))
print("Testing records:", len(X_test))

# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

# Train the model
model.fit(X_train, y_train)

print("\nModel training completed!")

# Predict test records
predictions = model.predict(X_test)

# Evaluate model
accuracy = accuracy_score(y_test, predictions)

print("\n===== MODEL EVALUATION =====")

print("Test accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions,
        labels=[0, 1],
        target_names=["Not Bug-Prone", "Bug-Prone"],
        zero_division=0
    )
)

print("Confusion Matrix:")
print(confusion_matrix(y_test, predictions, labels=[0, 1]))

# Display feature importance
print("\n===== FEATURE IMPORTANCE =====")

for name, importance in zip(
    feature_columns,
    model.feature_importances_
):
    print(name, ":", round(importance, 4))

# Save trained model and feature order
model_data = {
    "model": model,
    "features": feature_columns
}

joblib.dump(model_data, model_file)

print("\nModel saved at:", model_file)
print("ML training pipeline completed!")
