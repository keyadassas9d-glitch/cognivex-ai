
# COGNIVEX AI
# Component: Automatic ML Feature Extractor

import ast
import csv
from pathlib import Path

# Locate project folders
ml_folder = Path(__file__).parent

project_folder = ml_folder / "sample_repository"

dataset_folder = ml_folder / "dataset"

# Find Python files
python_files = list(project_folder.glob("*.py"))

# Output CSV file
output_file = dataset_folder / "extracted_features.csv"

# Store extracted records
extracted_data = []

print("===== COGNIVEX AI FEATURE EXTRACTOR =====")

# Analyse each Python file
for file_path in python_files:

    print("\nExtracting features:", file_path.name)

    try:

        # Read source code
        source_code = file_path.read_text(encoding="utf-8")

        # Count lines
        lines = source_code.splitlines()

        lines_of_code = sum(
            1 for line in lines if line.strip()
        )

        # Parse source code
        syntax_tree = ast.parse(source_code)

        # Extract functions
        functions = [
            node for node in ast.walk(syntax_tree)
            if isinstance(
                node,
                (ast.FunctionDef, ast.AsyncFunctionDef)
            )
        ]

        function_count = len(functions)

        # Count decision points
        decision_nodes = (
            ast.If,
            ast.For,
            ast.AsyncFor,
            ast.While,
            ast.ExceptHandler
        )

        decision_points = sum(
            isinstance(node, decision_nodes)
            for node in ast.walk(syntax_tree)
        )

        # Count eval() and exec() calls
        has_eval = 0

        for node in ast.walk(syntax_tree):

            if isinstance(node, ast.Call):

                if isinstance(node.func, ast.Name):

                    if node.func.id in {"eval", "exec"}:
                        has_eval = 1

        # Check for hardcoded credential-like strings
        sensitive_names = {
            "password",
            "api_key",
            "secret"
        }

        has_hardcoded_secret = 0

        for node in ast.walk(syntax_tree):

            if isinstance(node, ast.Assign):
                targets = node.targets
                value = node.value

            elif isinstance(node, ast.AnnAssign):
                targets = [node.target]
                value = node.value

            else:
                continue

            if isinstance(value, ast.Constant) and isinstance(value.value, str):

                for target in targets:

                    if isinstance(target, ast.Name):

                        if target.id.lower() in sensitive_names:
                            has_hardcoded_secret = 1

        # Create one feature record per file
        record = {
            "file_name": file_path.name,
            "lines_of_code": lines_of_code,
            "decision_points": decision_points,
            "function_count": function_count,
            "has_eval": has_eval,
            "has_hardcoded_secret": has_hardcoded_secret
        }

        extracted_data.append(record)

        print("Lines of code:", lines_of_code)
        print("Decision points:", decision_points)
        print("Functions:", function_count)
        print("Has eval/exec:", has_eval)
        print("Has hardcoded secret:", has_hardcoded_secret)

    except SyntaxError as error:

        print("Skipped: Invalid Python syntax")
        print("Error:", error.msg)

    except OSError as error:

        print("Unable to read file:", error)


# Save extracted features into CSV
field_names = [
    "file_name",
    "lines_of_code",
    "decision_points",
    "function_count",
    "has_eval",
    "has_hardcoded_secret"
]

with open(output_file, "w", newline="", encoding="utf-8") as csv_file:

    writer = csv.DictWriter(
        csv_file,
        fieldnames=field_names
    )

    writer.writeheader()
    writer.writerows(extracted_data)


# Display summary
print("\n===== FEATURE EXTRACTION SUMMARY =====")
print("Files discovered:", len(python_files))
print("Files successfully processed:", len(extracted_data))
print("Feature records generated:", len(extracted_data))
print("Output file:", output_file)
print("Feature extraction completed!")
