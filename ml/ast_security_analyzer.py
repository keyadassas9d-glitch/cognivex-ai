
# COGNIVEX AI
# Component: AST-Based Security Analyzer

import ast
from pathlib import Path

# Locate the sample repository
project_folder = Path(__file__).parent / "sample_repository"

# Find all Python files
python_files = list(project_folder.glob("*.py"))

# Names that may indicate hardcoded credentials
sensitive_names = {
    "password",
    "api_key",
    "secret"
}

total_files = 0
successful_files = 0
failed_files = 0
total_issues = 0

print("===== COGNIVEX AI AST SECURITY ANALYZER =====")


# Analyse each Python file
for file_path in python_files:

    print("\n--------------------------------")
    print("Analysing:", file_path.name)

    try:

        # Read source code
        source_code = file_path.read_text(encoding="utf-8")

        # Convert source code into AST
        syntax_tree = ast.parse(
            source_code,
            filename=file_path.name
        )

        file_issues = 0

        # Inspect every AST node
        for node in ast.walk(syntax_tree):

            # Rule 1: Detect eval() and exec()
            if isinstance(node, ast.Call):

                if isinstance(node.func, ast.Name):

                    if node.func.id in {"eval", "exec"}:

                        print(
                            "Potential security issue:",
                            node.func.id,
                            "usage"
                        )

                        print("Line:", node.lineno)

                        file_issues += 1
                        total_issues += 1

            # Rule 2: Detect hardcoded string credentials
            if isinstance(node, ast.Assign):

                targets = node.targets
                value = node.value

            elif isinstance(node, ast.AnnAssign):

                targets = [node.target]
                value = node.value

            else:
                continue

            # Only inspect string values
            if isinstance(value, ast.Constant) and isinstance(value.value, str):

                for target in targets:

                    if isinstance(target, ast.Name):

                        variable_name = target.id.lower()

                        if variable_name in sensitive_names:

                            print(
                                "Potential hardcoded credential:",
                                variable_name
                            )

                            print("Line:", node.lineno)

                            file_issues += 1
                            total_issues += 1

        if file_issues == 0:
            print("No matching security patterns found.")

        else:
            print("Potential issues in this file:", file_issues)

        successful_files += 1

    except SyntaxError as error:

        print("Syntax error:", error.msg)
        print("Error line:", error.lineno)

        failed_files += 1

    except OSError as error:

        print("Unable to read file:", error)

        failed_files += 1

    total_files += 1


# Display final report
print("\n===== SECURITY ANALYSIS SUMMARY =====")
print("Total files:", total_files)
print("Successfully analysed:", successful_files)
print("Files with errors:", failed_files)
print("Potential issues detected:", total_issues)
print("Analysis completed!")
