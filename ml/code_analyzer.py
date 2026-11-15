

# Component: Python Code Analyzer

import ast
from pathlib import Path

# Locate the sample repository
project_folder = Path(__file__).parent / "sample_repository"

# Find all Python files
python_files = list(project_folder.glob("*.py"))

print("===== COGNIVEX AI CODE ANALYZER =====")

total_files = 0
successful_files = 0
failed_files = 0

# Analyse each Python file
for file_path in python_files:

    print("\n--------------------------------")
    print("Analysing:", file_path.name)

    try:

        # Read the source code
        source_code = file_path.read_text(encoding="utf-8")

        # Convert source code into an AST
        syntax_tree = ast.parse(
            source_code,
            filename=file_path.name
        )

        # Extract functions
        functions = [
            node.name
            for node in ast.walk(syntax_tree)
            if isinstance(node, ast.FunctionDef)
        ]

        # Extract classes
        classes = [
            node.name
            for node in ast.walk(syntax_tree)
            if isinstance(node, ast.ClassDef)
        ]

        # Extract imported libraries
        imports = []

        for node in ast.walk(syntax_tree):

            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)

            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module or "unknown")

        # Display analysis results
        print("Syntax: Valid")
        print("Functions:", functions)
        print("Classes:", classes)
        print("Imports:", imports)

        successful_files += 1

    except SyntaxError as error:

        print("Syntax: Error detected")
        print("Error message:", error.msg)
        print("Error line:", error.lineno)

        failed_files += 1

    except OSError as error:

        print("Unable to read file:", error)

        failed_files += 1

    total_files += 1


# Display final summary
print("\n===== ANALYSIS SUMMARY =====")
print("Total files:", total_files)
print("Successfully analysed:", successful_files)
print("Files with errors:", failed_files)
print("Analysis completed!")
