
# COGNIVEX AI - First Python Program

# 1. Project information
project_name = "Cognivex AI"
language = "Python"

# 2. Repository files
files = [
    "login.py",
    "register.py",
    "database.py",
    "main.py",
    "security.py"
]

# 3. Analysis results
analysis = {
    "total_files": len(files),
    "bugs_detected": 3,
    "security_issues": 2
}

# 4. Function to display project information
def show_project_details():

    print("===== COGNIVEX AI =====")

    print("Project:", project_name)
    print("Language:", language)

    print("\nRepository Files:")

    for file in files:
        print("-", file)

    print("\nAnalysis Results:")

    print("Total Files:", analysis["total_files"])
    print("Bugs Detected:", analysis["bugs_detected"])
    print("Security Issues:", analysis["security_issues"])


# 5. Run the function
show_project_details()
