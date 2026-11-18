
import ast
import pandas as pd
from pathlib import Path

# Project directories
ml_folder = Path(__file__).parent
repository = ml_folder / "sample_repository"
output_file = ml_folder / "dataset" / "extracted_features.csv"

# Find Python files in all folders
python_files = list(repository.rglob("*.py"))

features_list = []

for file in python_files:

    try:
        source_code = file.read_text(encoding="utf-8")
        tree = ast.parse(source_code)

        lines = source_code.splitlines()

        function_count = 0
        decision_points = 0
        has_eval = 0
        has_hardcoded_secret = 0

        for node in ast.walk(tree):

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_count += 1

            if isinstance(node, (ast.If, ast.For, ast.While)):
                decision_points += 1

            if isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    if node.func.id in ["eval", "exec"]:
                        has_eval = 1

            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        if target.id.lower() in [
                            "password", "api_key", "secret"
                        ]:
                            if isinstance(node.value, ast.Constant):
                                if isinstance(node.value.value, str):
                                    has_hardcoded_secret = 1

        features_list.append({
            "file_name": str(file.relative_to(repository)),
            "lines_of_code": len(lines),
            "decision_points": decision_points,
            "function_count": function_count,
            "has_eval": has_eval,
            "has_hardcoded_secret": has_hardcoded_secret
        })

        print("Analysed:", file.relative_to(repository))

    except SyntaxError:
        print("Skipped syntax error:", file.name)

    except Exception as error:
        print("Could not analyse:", file.name, error)

# Save extracted features
df = pd.DataFrame(features_list)

output_file.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(output_file, index=False)

print("\nCOGNIVEX AI - FEATURE EXTRACTION")
print("--------------------------------")
print("Total Python files found:", len(python_files))
print("Successfully analysed:", len(df))
print("Features saved to:", output_file)
