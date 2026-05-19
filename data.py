#
# Data
#


# Import

import csv
from colors import cprint, cinput
import os

# Variables 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_FILE = os.path.join(BASE_DIR, "students.csv")
FIELDNAMES = ["name", "section", "spanish", "english", "social_studies", "science"]


def export_to_csv(students: list) -> None:
    if not students:
        cprint("\n  No students to export.")
        return

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(students)

    cprint(f"\n  ✓ {len(students)} student(s) exported to '{CSV_FILE}'.")


#   
#   Load student records from the CSV file into the current list.
#    Existing records are replaced with the imported ones.
#    Informs the user if no exported file exists yet.
#
# 
def import_from_csv(students: list) -> None:
    if not os.path.exists(CSV_FILE):
        cprint(f"\n  ✗ No exported file found ('{CSV_FILE}' does not exist).")
        cprint("    Use the export option first to create one.")
        return

    imported = []
    try:
        with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            # Validate the file has the expected columns
            if reader.fieldnames is None or not all(
                field in reader.fieldnames for field in FIELDNAMES
            ):
                cprint("\n  ✗ The CSV file has an unexpected format and cannot be imported.")
                return

            for row in reader:
                try:
                    student = {
                        "name":           row["name"],
                        "section":        row["section"],
                        "spanish":        float(row["spanish"]),
                        "english":        float(row["english"]),
                        "social_studies": float(row["social_studies"]),
                        "science":        float(row["science"]),
                    }
                    imported.append(student)
                except (ValueError, KeyError) as exc:
                    cprint(f"\n  ✗ Skipping a row due to invalid data: {exc}")

    except OSError as exc:
        cprint(f"\n  ✗ Could not read the file: {exc}")
        return

    if not imported:
        cprint("\n  ✗ The CSV file contained no valid student records.")
        return

    # Replace current list contents with the imported records
    students.clear()
    students.extend(imported)
    cprint(f"\n  ✓ {len(students)} student(s) imported from '{CSV_FILE}'.")
