
# COGNIVEX AI
# Component: ML Dataset Preparation and Validation

import pandas as pd
from pathlib import Path
from sklearn.model_selection import train_test_split

# Locate dataset folder
dataset_folder = Path(__file__).parent / "dataset"

# Load our labelled sample dataset
dataset_file = dataset_folder / "bug_samples.csv"

print("===== COGNIVEX AI DATASET PREPARATION =====")

# Read CSV using Pandas
df = pd.read_csv(dataset_file)

print("\nOriginal dataset shape:", df.shape)

# Required columns
required_columns = [
    "lines_of_code",
    "decision_points",
    "function_count",
    "has_eval",
    "has_hardcoded_secret",
    "bug_prone"
]

# Validate columns
missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

# Keep only the required columns
df = df[required_columns].copy()

# Check missing values
print("\nMissing values:")
print(df.isnull().sum())

# Remove duplicate rows
before = len(df)
df = df.drop_duplicates()
duplicates_removed = before - len(df)

# Remove rows containing missing values
df = df.dropna()

# Validate target labels
if not set(df["bug_prone"].unique()).issubset({0, 1}):
    raise ValueError("Target labels must be 0 or 1.")

# Separate features and target
X = df.drop(columns=["bug_prone"])
y = df["bug_prone"]

# Check class counts
class_counts = y.value_counts()

if len(class_counts) != 2 or class_counts.min() < 2:
    raise ValueError(
        "Need at least two examples of each target class."
    )

# Split into training and testing data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Save prepared datasets
training_data = X_train.copy()
training_data["bug_prone"] = y_train

testing_data = X_test.copy()
testing_data["bug_prone"] = y_test

training_data.to_csv(
    dataset_folder / "training_data.csv",
    index=False
)

testing_data.to_csv(
    dataset_folder / "testing_data.csv",
    index=False
)

# Display results
print("\n===== VALIDATION SUMMARY =====")
print("Rows after cleaning:", len(df))
print("Duplicate rows removed:", duplicates_removed)
print("Features:", list(X.columns))
print("Target column: bug_prone")

print("\n===== DATA SPLIT SUMMARY =====")
print("Training records:", len(X_train))
print("Testing records:", len(X_test))

print("\nTraining class distribution:")
print(y_train.value_counts())

print("\nTesting class distribution:")
print(y_test.value_counts())

print("\nPrepared datasets saved successfully!")
print("Dataset preparation completed!")
