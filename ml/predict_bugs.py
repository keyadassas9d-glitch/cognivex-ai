
import pandas as pd
import joblib
from pathlib import Path

# Locate project folders
ml_folder = Path(__file__).parent

# Load trained model
model_path = ml_folder / "models" / "bug_prone_model.joblib"
saved_data = joblib.load(model_path)

model = saved_data["model"]
features = saved_data["features"]

# Load extracted code features
data_path = ml_folder / "dataset" / "extracted_features.csv"
data = pd.read_csv(data_path)

# Select the same features used during training
X = data[features]

# Predict bug-proneness
predictions = model.predict(X)

print("\nCOGNIVEX AI - BUG PREDICTION REPORT")
print("----------------------------------")

for index, prediction in enumerate(predictions):
    filename = data.iloc[index]["file_name"]

    if prediction == 1:
        result = "Likely Bug-Prone"
    else:
        result = "Less Likely Bug-Prone"

    print(f"{filename}: {result}")

print("\nPrediction completed!")
