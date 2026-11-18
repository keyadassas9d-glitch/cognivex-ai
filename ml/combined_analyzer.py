
import pandas as pd
import joblib
from pathlib import Path

# Locate project directory
ml_folder = Path(__file__).parent

# Load trained ML model
model_path = ml_folder / "models" / "bug_prone_model.joblib"
saved_data = joblib.load(model_path)

model = saved_data["model"]
features = saved_data["features"]

# Load extracted code features
data_path = ml_folder / "dataset" / "extracted_features.csv"
data = pd.read_csv(data_path)

# Prepare input for ML model
X = data[features]

# Generate ML predictions
predictions = model.predict(X)

print("\n========== COGNIVEX AI ==========")
print("     COMBINED CODE ANALYSIS")
print("=================================")

for index, prediction in enumerate(predictions):

    filename = data.iloc[index]["file_name"]

    print(f"\nFile: {filename}")
    print("---------------------------------")

    # Security analysis results
    if data.iloc[index]["has_eval"] == 1:
        print("[SECURITY WARNING] eval() detected")

    if data.iloc[index]["has_hardcoded_secret"] == 1:
        print("[SECURITY WARNING] Possible hardcoded secret detected")

    if (
        data.iloc[index]["has_eval"] == 0
        and data.iloc[index]["has_hardcoded_secret"] == 0
    ):
        print("[SECURITY] No selected risky patterns detected")

    # ML prediction
    if prediction == 1:
        print("[ML PREDICTION] Likely Bug-Prone")
    else:
        print("[ML PREDICTION] Less Likely Bug-Prone")

print("\n=================================")
print("       ANALYSIS COMPLETED")
print("=================================")
