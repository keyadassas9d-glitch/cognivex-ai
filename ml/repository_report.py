
import pandas as pd
import joblib
from pathlib import Path

# Project paths
ml_folder = Path(__file__).parent
data_path = ml_folder / "dataset" / "extracted_features.csv"
model_path = ml_folder / "models" / "bug_prone_model.joblib"

# Load extracted features
data = pd.read_csv(data_path)

# Load trained ML model
saved_data = joblib.load(model_path)
model = saved_data["model"]
features = saved_data["features"]

# Generate predictions
X = data[features]
predictions = model.predict(X)

# Repository statistics
total_files = len(data)
eval_files = int(data["has_eval"].sum())
secret_files = int(data["has_hardcoded_secret"].sum())
bug_prone_files = int((predictions == 1).sum())

total_lines = int(data["lines_of_code"].sum())
total_functions = int(data["function_count"].sum())

print("\n======================================")
print("       COGNIVEX AI")
print("       REPOSITORY HEALTH REPORT")
print("======================================")

print("\nREPOSITORY STATISTICS")
print("--------------------------------------")
print("Python files analysed:", total_files)
print("Total lines of code:", total_lines)
print("Total functions:", total_functions)

print("\nSECURITY ANALYSIS")
print("--------------------------------------")
print("Files containing eval/exec:", eval_files)
print("Files with possible hardcoded secrets:", secret_files)

print("\nMACHINE LEARNING ANALYSIS")
print("--------------------------------------")
print("Files predicted as bug-prone:", bug_prone_files)
print("Files predicted as less likely bug-prone:",
      total_files - bug_prone_files)

print("\n======================================")
print("       REPORT GENERATED")
print("======================================")
