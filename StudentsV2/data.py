
#
#
# Data.py
#
# All logic related to exporting and importing student data as CSV.
#Students are stored as objects; this module converts them to/from dicts
#so the CSV layer never touches object internals.
#

import csv
import os

from student import Student
from colors  import cprint, DIM, RED, RESET

CSV_FILE   = os.path.join(os.path.dirname(__file__), "students.csv")
FIELDNAMES = ["name", "section", "spanish", "english", "social_studies", "science"]


def export_to_csv(students: list) -> None:
    
    # Convert each Student object → dict, then write all records to CSV.
    
    if not students:
        cprint(f"\n  {DIM}  No students to export.{RESET}\n")
        return

    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for student in students:
            writer.writerow(student.to_dict())   # ← object → dict

    cprint(f"\n  ✔  {len(students)} student(s) exported to:\n"
           f"  {DIM}  {CSV_FILE}{RESET}\n")


def import_from_csv(students: list) -> None:
    #
    # Read CSV rows (plain dicts) and convert each one → Student object,
    # then append to the students list.
    #
    
    if not os.path.exists(CSV_FILE):
        cprint(f"\n  {DIM}  No CSV file found. Export data first.{RESET}\n")
        return

    imported = 0
    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                student = Student.from_dict(row)   # ← dict → object
                students.append(student)
                imported += 1
            except (KeyError, ValueError) as e:
                print(f"  {RED}✖  Skipped invalid row: {e}{RESET}")

    if imported:
        cprint(f"\n  ✔  {imported} student(s) imported from CSV.\n")
    else:
        cprint(f"\n  {DIM}  No valid records found in the CSV file.{RESET}\n")
