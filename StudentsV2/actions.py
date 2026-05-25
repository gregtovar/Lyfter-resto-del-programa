
#
# actions.py 
# All logic for student-related menu actions (except import/export).
#. Students are stored and handled as Student objects.
#
#
#


from student import Student
from colors  import cprint, cinput, BOLD, DIM, RED, YELLOW, RESET


# ── Input helpers ──────────────────────────────────────

def _input_grade(prompt: str) -> float:
    """Keep asking until the user enters a number in [0, 100]."""
    while True:
        raw = cinput(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print(f"  {RED}✖  Invalid input. Please enter a numeric value.{RESET}")
            continue
        if 0 <= value <= 100:
            return value
        print(f"  {RED}✖  Grade must be between 0 and 100. Try again.{RESET}")


def _section_bar(label: str) -> None:
    cprint(f"\n  {'─' * 44}")
    cprint(f"  {BOLD}  {label}{RESET}")
    cprint(f"  {'─' * 44}")


#
#.   ***** MENU *********
#


def add_student(students: list) -> None:
    """Prompt user for one student's data and append a Student object."""
    _section_bar("➕  Add Student")
    print()

    name    = cinput("  👤  Full name    » ").strip()
    section = cinput("  🏫  Section      » ").strip().upper()

    print()
    cprint(f"  {DIM}  Enter grades (0 – 100):{RESET}")
    spanish       = _input_grade("  📘  Spanish       » ")
    english       = _input_grade("  📗  English       » ")
    social_studies = _input_grade("  📙  Social Studies » ")
    science       = _input_grade("  📕  Science       » ")

    student = Student(name, section, spanish, english, social_studies, science)
    students.append(student)

    print()
    cprint(f"  ✔  {student.name} added successfully.  "
           f"{DIM}Avg: {student.get_average():.2f}{RESET}")


def view_all_students(students: list) -> None:
    """Display every student in a formatted table."""
    _section_bar("📋  All Students")

    if not students:
        cprint(f"\n  {DIM}  No students registered yet.{RESET}\n")
        return

    header = (f"  {'#':<4} {'Name':<22} {'Sec':<6} "
              f"{'ES':>6} {'EN':>6} {'SS':>6} {'SC':>6}  {'Avg':>7}")
    print()
    cprint(header)
    cprint(f"  {'─' * 64}")

    for i, s in enumerate(students, 1):
        row = (f"  {i:<4} {s.name:<22} {s.section:<6} "
               f"{s.spanish:>6.1f} {s.english:>6.1f} "
               f"{s.social_studies:>6.1f} {s.science:>6.1f}  "
               f"{s.get_average():>7.2f}")
        cprint(row)

    cprint(f"  {'─' * 64}")
    cprint(f"  {DIM}  Total students: {len(students)}{RESET}\n")


def view_top3(students: list) -> None:
    """Display the top 3 students by average grade."""
    _section_bar("🏆  Top 3 Students")

    if not students:
        cprint(f"\n  {DIM}  No students registered yet.{RESET}\n")
        return

    ranked = sorted(students, key=lambda s: s.get_average(), reverse=True)
    medals = ["🥇", "🥈", "🥉"]

    print()
    for i, s in enumerate(ranked[:3]):
        medal = medals[i] if i < len(medals) else f"  {i+1}."
        cprint(f"  {medal}  {BOLD}{s.name}{RESET}  "
               f"{DIM}({s.section})  Avg: {s.get_average():.2f}{RESET}")
    print()


def view_overall_average(students: list) -> None:
    """Display the overall average grade across all students."""
    _section_bar("📊  Overall Class Average")

    if not students:
        cprint(f"\n  {DIM}  No students registered yet.{RESET}\n")
        return

    total_avg = sum(s.get_average() for s in students) / len(students)
    print()
    cprint(f"  {BOLD}  Class average:  {total_avg:.2f} / 100{RESET}\n")


def view_worst_students(students: list) -> None:
    """Display students sorted from lowest to highest average."""
    _section_bar("📉  Students by Lowest Average")

    if not students:
        cprint(f"\n  {DIM}  No students registered yet.{RESET}\n")
        return

    ranked = sorted(students, key=lambda s: s.get_average())

    print()
    for i, s in enumerate(ranked, 1):
        cprint(f"  {DIM}{i}.{RESET}  {s.name:<22} "
               f"{DIM}({s.section})  Avg: {s.get_average():.2f}{RESET}")
    print()
