
from pathlib import Path

def scan_repository(repository_path):

    repository = Path(repository_path)

    # Find Python files in all folders and subfolders
    python_files = list(repository.rglob("*.py"))

    print("\nCOGNIVEX AI - REPOSITORY SCANNER")
    print("--------------------------------")

    print("Repository:", repository.name)
    print("Python files found:", len(python_files))

    for file in python_files:
        print(file.relative_to(repository))

    return python_files


# Sample repository location
sample_path = Path(__file__).parent / "sample_repository"

scan_repository(sample_path)
