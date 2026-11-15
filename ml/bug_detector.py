
# COGNIVEX AI
# Component: Rule-Based Bug and Security Detector

from pathlib import Path

# Locate the sample repository
project_folder = Path(__file__).parent / "sample_repository"

# Find Python files
python_files = list(project_folder.glob("*.py"))

# Define detection rules
detection_rules = {
    "eval(": "Potentially unsafe use of eval()",
    "exec(": "Potentially unsafe use of exec()",
    "password =": "Possible hardcoded password",
    "api_key =": "Possible hardcoded API key",
    "secret =": "Possible hardcoded secret"
}

total_files = 0
total_issues = 0

print("===== COGNIVEX AI BUG DETECTOR =====")

# Examine each Python file
for file_path in python_files:

    print("\n--------------------------------")
    print("Checking:", file_path.name)

    try:

        # Read the file
        source_code = file_path.read_text(encoding="utf-8")

        # Examine each line separately
        lines = source_code.splitlines()

        file_issues = 0

        for line_number, line in enumerate(lines, start=1):

            # Convert the line to lowercase
            clean_line = line.lower()

            # Check every detection rule
            for pattern, description in detection_rules.items():

                if pattern in clean_line:

                    print("Potential issue:", description)
                    print("Line number:", line_number)
                    print("Code:", line.strip())

                    file_issues += 1
                    total_issues += 1

        if file_issues == 0:
            print("No matching suspicious patterns found.")

        else:
            print("Issues found in this file:", file_issues)

        total_files += 1

    except OSError as error:

        print("Unable to read file:", error)


# Display final report
print("\n===== DETECTION SUMMARY =====")
print("Files checked:", total_files)
print("Potential issues detected:", total_issues)
print("Detection completed!")
