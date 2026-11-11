
# COGNIVEX AI
# Mini Component: Repository File Scanner

files = [
    "main.py",
    "login.py",
    "database.py",
    "security.py",
    "readme.txt",
    "model.py"
]

total_scanned = 0
invalid_files = 0

print("===== COGNIVEX AI SCANNER =====")

for file in files:

    if file.endswith(".py"):
        print("Scanning:", file)
        total_scanned += 1

    else:
        print("Skipping invalid file:", file)
        invalid_files += 1

print("\n===== SCAN SUMMARY =====")
print("Total Python files scanned:", total_scanned)
print("Invalid files skipped:", invalid_files)
print("Scan completed!")
