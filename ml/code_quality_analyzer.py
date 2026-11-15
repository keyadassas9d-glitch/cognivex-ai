
# COGNIVEX AI
# Component: Code Quality Analyzer

import ast
from pathlib import Path

# Locate the sample repository
project_folder = Path(__file__).parent / "sample_repository"

# Find Python files
python_files = list(project_folder.glob("*.py"))

total_files = 0
successful_files = 0
total_functions = 0
total_classes = 0
total_complexity = 0

print("===== COGNIVEX AI CODE QUALITY ANALYZER =====")


# Analyse every Python file
for file_path in python_files:

    print("\n--------------------------------")
    print("File:", file_path.name)

    try:

        # Read source code
        source_code = file_path.read_text(encoding="utf-8")

        # Count total and non-empty lines
        lines = source_code.splitlines()
        total_lines = len(lines)
        non_empty_lines = sum(1 for line in lines if line.strip())

        # Parse source code
        syntax_tree = ast.parse(
            source_code,
            filename=file_path.name
        )

        # Count functions and classes
        functions = [
            node for node in ast.walk(syntax_tree)
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]

        classes = [
            node for node in ast.walk(syntax_tree)
            if isinstance(node, ast.ClassDef)
        ]

        # Calculate approximate complexity
        decision_nodes = (
            ast.If,
            ast.For,
            ast.AsyncFor,
            ast.While,
            ast.ExceptHandler
        )

        decision_count = sum(
            isinstance(node, decision_nodes)
            for node in ast.walk(syntax_tree)
        )

        boolean_count = sum(
            isinstance(node, ast.BoolOp)
            and isinstance(node.op, (ast.And, ast.Or))
            for node in ast.walk(syntax_tree)
        )

        complexity = 1 + decision_count + boolean_count

        # Display file metrics
        print("Total lines:", total_lines)
        print("Non-empty lines:", non_empty_lines)
        print("Functions:", len(functions))
        print("Classes:", len(classes))
        print("Decision points:", decision_count + boolean_count)
        print("Approximate cyclomatic complexity:", complexity)

        # Identify long functions
        for function in functions:

            function_lines = (
                function.end_lineno - function.lineno + 1
            )

            if function_lines > 20:
                print(
                    "Long function warning:",
                    function.name,
                    "-",
                    function_lines,
                    "lines"
                )

        total_functions += len(functions)
        total_classes += len(classes)
        total_complexity += complexity

        successful_files += 1

    except SyntaxError as error:

        print("Cannot analyse invalid Python syntax.")
        print("Syntax error:", error.msg)
        print("Error line:", error.lineno)

    except OSError as error:

        print("Unable to read file:", error)

    total_files += 1


# Display final summary
print("\n===== PROJECT QUALITY SUMMARY =====")
print("Total files:", total_files)
print("Successfully analysed:", successful_files)
print("Total functions:", total_functions)
print("Total classes:", total_classes)
print("Combined file complexity:", total_complexity)
print("Quality analysis completed!")
