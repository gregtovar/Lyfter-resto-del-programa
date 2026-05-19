#
# Actions
#


from colors import cprint, cinput


import re

# Matches 1–20 followed by exactly one A–Z letter (e.g. 1A, 10B, 20Z).
_SECTION_RE = re.compile(r"^([1-9]|1[0-9]|20)[A-Za-z]$")


def _get_average(student: dict) -> float:
    grades = [
        student["spanish"],
        student["english"],
        student["social_studies"],
        student["science"],
    ]
    return sum(grades) / len(grades)

#  Keep asking until the user enters a number in [0, 100].
def _input_grade(prompt: str) -> float:
    while True:
        raw = cinput(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            cprint("  ✗ Invalid input. Please enter a numeric value.")
            continue
        if 0 <= value <= 100:
            return value
        cprint("  ✗ Grade must be between 0 and 100. Try again.")


def _input_section(prompt: str) -> str:

    while True:
        value = cinput(prompt).strip()
        if not value:
            cprint("  ✗ Section cannot be empty.")
            continue
        if not _SECTION_RE.match(value):
            cprint("  ✗ Invalid section format.")
            cprint("    Expected: a number from 1 to 20 followed by one letter (e.g. 10A, 3B, 20Z).")
            continue
        return value[:-1] + value[-1].upper()    



def _input_name(prompt: str) -> str:

    while True:
        value = cinput(prompt).strip()
        if not value:
            cprint("  ✗ Name cannot be empty. Please try again.")
            continue
        invalid_chars = [ch for ch in value if not (ch.isalpha() or ch == " ")]
        if invalid_chars:
            unique = "".join(dict.fromkeys(invalid_chars))   
            cprint(f"  ✗ Name must contain only letters and spaces.")
            cprint(f"    Invalid character(s) found: {unique!r}")
            continue
        return value


def enter_students(students: list) -> None:

    while True:
        raw = cinput("\nHow many students do you want to add? ").strip()
        try:
            count = int(raw)
            if count <= 0:
                cprint("  ✗ Please enter a positive integer.")
                continue
            break
        except ValueError:
            cprint("  ✗ Invalid input. Please enter a whole number.")

    for i in range(1, count + 1):
        cprint(f"\n── Student {i} of {count} ──────────────────────")

        while True:
            name    = _input_name("  Full name        : ")
            section = _input_section("  Section (e.g. 11B): ")

            duplicate = any(
                s["name"].lower() == name.lower() and s["section"].lower() == section.lower()
                for s in students
            )
            if not duplicate:
                break
            cprint(f"  \u2717 '{name}' in section '{section}' is already registered. Please enter a different student.")

        spanish        = _input_grade("  Spanish grade    : ")
        english        = _input_grade("  English grade    : ")
        social_studies = _input_grade("  Social Studies   : ")
        science        = _input_grade("  Science grade    : ")

        student = {
            "name":           name,
            "section":        section,
            "spanish":        spanish,
            "english":        english,
            "social_studies": social_studies,
            "science":        science,
        }
        students.append(student)
        cprint(f"  ✓ {name} added successfully.")


def view_all_students(students: list) -> None:
    if not students:
        cprint("\n  No students registered yet.")
        return

    header = f"\n{'#':<4} {'Name':<30} {'Section':<10} {'Spanish':>8} {'English':>8} {'Soc.St.':>8} {'Science':>8} {'Average':>8}"
    cprint(header)
    cprint("─" * len(header))

    for idx, s in enumerate(students, start=1):
        avg = _get_average(s)
        cprint(
            f"{idx:<4} {s['name']:<30} {s['section']:<10} "
            f"{s['spanish']:>8.2f} {s['english']:>8.2f} "
            f"{s['social_studies']:>8.2f} {s['science']:>8.2f} "
            f"{avg:>8.2f}"
        )


def view_top3(students: list) -> None:
    if not students:
        cprint("\n  No students registered yet.")
        return

    ranked = sorted(students, key=_get_average, reverse=True)
    top = ranked[:3]

    cprint(f"\n{'Rank':<6} {'Name':<30} {'Section':<10} {'Average':>8}")
    cprint("─" * 58)
    for rank, s in enumerate(top, start=1):
        avg = _get_average(s)
        cprint(f"{rank:<6} {s['name']:<30} {s['section']:<10} {avg:>8.2f}")


def view_overall_average(students: list) -> None:
    """Display the overall (grand) average across all students."""
    if not students:
        cprint("\n  No students registered yet.")
        return

    grand_avg = sum(_get_average(s) for s in students) / len(students)
    cprint(f"\n  Overall average grade ({len(students)} student(s)): {grand_avg:.2f}")



def delete_student(students: list) -> None:
    if not students:
        cprint("\n  No students registered yet.")
        return

    name    = cinput("\n  Full name of student to delete : ").strip()
    section = cinput("  Section                        : ").strip()

    
    matches = [
        s for s in students
        if s["name"].lower() == name.lower()
        and s["section"].lower() == section.lower()
    ]

    if not matches:
        cprint(f"\n  ✗ No student found with name '{name}' in section '{section}'.")
        return

    
    student = matches[0]
    avg = _get_average(student)
    cprint(f"\n  Student found:")
    cprint(f"    Name    : {student['name']}")
    cprint(f"    Section : {student['section']}")
    cprint(f"    Average : {avg:.2f}")

     
    while True:
        confirm = cinput("\n  Are you sure you want to delete this student? (y/n): ").strip().lower()
        if confirm == "y":
            students.remove(student)
            cprint(f"\n  ✓ '{student['name']}' from section '{student['section']}' has been deleted.")
            break
        elif confirm == "n":
            cprint("\n  Deletion cancelled.")
            break
        else:
            cprint("  ✗ Please enter 'y' to confirm or 'n' to cancel.")


 
SUBJECT_LABELS = {
    "spanish":       "Spanish",
    "english":       "English",
    "social_studies": "Social Studies",
    "science":       "Science",
}

PASSING_GRADE = 60



def view_failed_students(students: list) -> None:
    if not students:
        cprint("\n  No students registered yet.")
        return

    failed = [
        (s, {subject: s[subject] for subject in SUBJECT_LABELS if s[subject] < PASSING_GRADE})
        for s in students
    ]
 
    failed = [(s, subjects) for s, subjects in failed if subjects]

    if not failed:
        cprint("\n  ✓ No failed students — everyone passed all subjects!")
        return

    cprint(f"\n  Students with at least one subject below {PASSING_GRADE}:")
    cprint("─" * 55)

    for student, failed_subjects in failed:
        cprint(f"\n  Name    : {student['name']}")
        cprint(f"  Section : {student['section']}")
        cprint(f"  Failed subjects:")
        for subject, grade in failed_subjects.items():
            label = SUBJECT_LABELS[subject]
            cprint(f"    • {label:<16} {grade:.2f}")

    cprint("\n" + "─" * 55)
    cprint(f"  Total failed students: {len(failed)}")


def view_worst_students(students: list) -> None:
    """Display all students sorted from lowest to highest average grade."""
    if not students:
        cprint("\n  No students registered yet.")
        return

    ranked = sorted(students, key=_get_average)   

    cprint(f"\n  All students — worst to best by average ({len(ranked)} total):")
    cprint(f"\n{'Rank':<6} {'Name':<30} {'Section':<10} {'Average':>8}")
    cprint("\u2500" * 58)
    for rank, s in enumerate(ranked, start=1):
        avg = _get_average(s)
        cprint(f"{rank:<6} {s['name']:<30} {s['section']:<10} {avg:>8.2f}")
