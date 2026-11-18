
import ast
import joblib
import pandas as pd

from pathlib import Path


def analyze_python_file(source_code):

    # Parse Python source code
    try:
        tree = ast.parse(source_code)
    except SyntaxError as error:
        return {
            "syntax_valid": False,
            "syntax_error": str(error),
            "line": error.lineno
        }

    # Initialise analysis features
    function_count = 0
    class_count = 0
    decision_points = 0
    has_eval = 0
    has_hardcoded_secret = 0
    security_warnings = []
    imports = []

    lines = source_code.splitlines()

    # Inspect code structure
    for node in ast.walk(tree):

        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            function_count += 1

        if isinstance(node, ast.ClassDef):
            class_count += 1

        if isinstance(node, (ast.If, ast.For, ast.While)):
            decision_points += 1

        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))

        # Check eval() and exec()
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in ["eval", "exec"]:
                    has_eval = 1
                    security_warnings.append(
                        f"Potentially unsafe {node.func.id}() call "
                        f"at line {node.lineno}"
                    )

        # Check possible hardcoded secrets
        if isinstance(node, ast.Assign):
            for target in node.targets:

                if isinstance(target, ast.Name):
                    if target.id.lower() in [
                        "password", "api_key", "secret"
                    ]:
                        if isinstance(node.value, ast.Constant):
                            if isinstance(node.value.value, str):

                                has_hardcoded_secret = 1
                                security_warnings.append(
                                    f"Possible hardcoded secret in "
                                    f"{target.id}"
                                )

    # Extract ML features
    feature_values = {
        "lines_of_code": len(lines),
        "decision_points": decision_points,
        "function_count": function_count,
        "has_eval": has_eval,
        "has_hardcoded_secret": has_hardcoded_secret
    }

    # Locate saved model
    project_root = Path(__file__).resolve().parents[2]

    model_path = (
        project_root / "ml" / "models" / "bug_prone_model.joblib"
    )

    if not model_path.exists():
        raise FileNotFoundError("Trained ML model not found")

    # Load trained Random Forest model
    saved_data = joblib.load(model_path)

    model = saved_data["model"]
    model_features = saved_data["features"]

    # Arrange features in the model's expected order
    input_data = pd.DataFrame(
        [[feature_values[name] for name in model_features]],
        columns=model_features
    )

    # Predict bug-proneness
    prediction = int(model.predict(input_data)[0])

    return {
        "syntax_valid": True,
        "functions": function_count,
        "classes": class_count,
        "imports": imports,
        "code_metrics": feature_values,
        "security_warnings": security_warnings,
        "ml_prediction": (
            "Likely Bug-Prone"
            if prediction == 1
            else "Less Likely Bug-Prone"
        )
    }
