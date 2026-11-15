
# COGNIVEX AI
# Component: Python Source Code Reader

from pathlib import Path

# 1. Locate the sample repository
project_folder = Path(__file__).parent / "sample_repository"

# 2. Find all Python files
python_files = list(project_folder.glob("*.py"))

# 3. Initialize counter
total_files = 0

print("===== COGNIVEX AI FILE READER =====")

# 4. Read every Python file
for file_path in python_files:

    try:
        with open(file_path, "r", encoding="utf-8") as file:

            code = file.read()

            print("\nFile Name:", file_path.name)

            print("Source Code:")
            print(code)

            total_files += 1

    except OSError as error:
        print("Unable to read file:", file_path.name)
        print("Error:", error)

# 5. Display summary
print("\n===== SCAN SUMMARY =====")
print("Total files read:", total_files)
print("Reading completed!")
