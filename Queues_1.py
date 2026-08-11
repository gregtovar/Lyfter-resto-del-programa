"""THE ZOO - A basic Queue built from linked objects - Version 1.0

Greg Tovar - 8/11/2026

A queue is FIFO: First In, First Out. The first animal to arrive is the first
one to leave, exactly like a line at the zoo entrance.

"""

import os
import time
from datetime import datetime

 
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = "animals.csv"


# Color Management

class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    RED = "\033[38;5;203m"
    ORANGE = "\033[38;5;215m"
    YELLOW = "\033[38;5;222m"
    GREEN = "\033[38;5;114m"
    CYAN = "\033[38;5;80m"
    BLUE = "\033[38;5;75m"
    PURPLE = "\033[38;5;141m"
    PINK = "\033[38;5;211m"
    GREY = "\033[38;5;245m"
    WHITE = "\033[38;5;255m"


# Returns the rainbow color that belongs to a given row index.
def rainbow(index: int) -> str:
    step = index % 7
    if step == 0:
        return Color.RED
    if step == 1:
        return Color.ORANGE
    if step == 2:
        return Color.YELLOW
    if step == 3:
        return Color.GREEN
    if step == 4:
        return Color.CYAN
    if step == 5:
        return Color.BLUE
    return Color.PURPLE


# Paints a piece of text and closes the escape sequence.
def paint(text: str, color: str) -> str:
    return color + text + Color.RESET


# Pads a value to a fixed column width, trimming anything too long.
def fit(text: str, width: int) -> str:
    if len(text) > width - 1:
        return text[:width - 2] + "… "
    return text.ljust(width)


# Clears the terminal screen.
def clear_screen() -> None:
    print("\033[2J\033[H", end="")


# Waits for the user before redrawing the screen.
def pause() -> None:
    input(paint("\n   Press ENTER to continue... ", Color.GREY))



# Cleans a path that was typed, pasted, or dragged into the terminal.
def clean_path(raw: str) -> str:
    value = raw.strip()

    if len(value) >= 2:
        first = value[0]
        last = value[-1]
        if (first == '"' and last == '"') or (first == "'" and last == "'"):
            value = value[1:len(value) - 1]

    # Finder drag-and-drop escapes spaces with a backslash.
    value = value.replace("\\ ", " ")
    return os.path.expanduser(value.strip())


# Turns whatever the user typed into one absolute path.
def resolve_path(raw: str, fallback: str) -> str:
    value = clean_path(raw)
    if value == "":
        value = fallback

    if os.path.isabs(value):
        return value

    beside_script = BASE_DIR + os.sep + value
    if os.path.isfile(beside_script):
        return beside_script

    from_terminal = os.path.abspath(value)
    if os.path.isfile(from_terminal):
        return from_terminal

    # Nothing exists yet, so default to writing next to the script.
    return beside_script


# Shows which CSV files actually sit next to the script, to debug bad paths.
def list_csv_files() -> None:
    print(paint("\n   CSV files found in the program folder:", Color.YELLOW))
    found = 0
    try:
        scanner = os.scandir(BASE_DIR)
    except OSError:
        return

    for entry in scanner:
        if entry.is_file() and entry.name.lower().endswith(".csv"):
            print(paint("     · " + entry.name, Color.CYAN))
            found = found + 1

    if found == 0:
        print(paint("     (none - the folder has no .csv files at all)", Color.RED))


# ---------------------------------------------------------------------------
# The Node. One animal = one node, pointing at whoever is behind it in line.
# ---------------------------------------------------------------------------
class AnimalNode:

    # Builds a single animal node, not yet attached to any queue.
    def __init__(self, data: str) -> None:
        self.data = data
        self.added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.next = None


# ---------------------------------------------------------------------------
# The Queue. FIFO: animals join at the rear and leave from the front.
# ---------------------------------------------------------------------------
class AnimalQueue:

    # Initializes an empty queue.
    def __init__(self, name: str) -> None:
        self.name = name
        self.front = None
        self.rear = None
        self.size = 0
        self.source_path = ""
        self.created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # True when no animals are waiting.
    def is_empty(self) -> bool:
        return self.front is None

    # REQUIRED METHOD - adds a node to the END of the queue.
    def enqueue(self, data: str) -> "AnimalNode":
        node = AnimalNode(data)

        if self.rear is None:
            # First animal in line: it is both the front and the rear.
            self.front = node
        else:
            self.rear.next = node

        self.rear = node
        self.size = self.size + 1
        return node

    # REQUIRED METHOD - removes and returns the node at the BEGINNING.
    # Returns None when the queue is empty, so callers can react instead of
    # crashing.
    def dequeue(self) -> str:
        if self.front is None:
            return None

        removed = self.front
        self.front = removed.next

        if self.front is None:
            # The queue just emptied, so the rear pointer must clear too or it
            # would keep pointing at an animal that already left.
            self.rear = None

        removed.next = None
        self.size = self.size - 1
        return removed.data

    # REQUIRED METHOD - prints every element in order, front to rear.
    def print_all(self) -> None:
        if self.is_empty():
            print(paint("   (the queue is empty)", Color.YELLOW))
            return

        line = ""
        walker = self.front
        while walker is not None:
            if line == "":
                line = walker.data
            else:
                line = line + " -> " + walker.data
            walker = walker.next

        wrap_print(line, Color.WHITE)

    # Looks at the animal at the front without removing it.
    def peek(self) -> "AnimalNode":
        return self.front

    # True when a name is already waiting in line (case insensitive).
    def contains(self, data: str) -> bool:
        wanted = data.lower()
        walker = self.front
        while walker is not None:
            if walker.data.lower() == wanted:
                return True
            walker = walker.next
        return False

    # Prints the queue as a framed table with positions and arrival times.
    def print_table(self) -> None:
        print(paint("\n   QUEUE: " + self.name, Color.BOLD + Color.CYAN))
        print(paint("   created " + self.created
                    + "   |   animals in line: " + str(self.size), Color.GREY))

        if self.is_empty():
            print(paint("\n   ╭" + "─" * 74 + "╮", Color.GREY))
            print(paint("   │" + "The zoo is empty - no animals in the queue.".center(74)
                        + "│", Color.YELLOW))
            print(paint("   ╰" + "─" * 74 + "╯", Color.GREY))
            return

        header = (" POS".ljust(8) + "ANIMAL".ljust(22)
                  + "ROLE".ljust(20) + "ADDED ON")

        top_label = "─ ◀ FRONT (next to leave) "
        bottom_label = "─ ▶ REAR (last to arrive) "

        print(paint("\n   ╭" + top_label + "─" * (74 - len(top_label)) + "╮", Color.GREEN))
        print(paint("   │ ", Color.CYAN) + paint(header.ljust(72), Color.BOLD + Color.WHITE)
              + paint(" │", Color.CYAN))
        print(paint("   ├" + "─" * 74 + "┤", Color.CYAN))

        walker = self.front
        position = 1
        while walker is not None:
            if walker is self.front and walker is self.rear:
                role = "front + rear"
                shade = Color.PINK + Color.BOLD
            elif walker is self.front:
                role = "front"
                shade = Color.GREEN + Color.BOLD
            elif walker is self.rear:
                role = "rear"
                shade = Color.YELLOW + Color.BOLD
            else:
                role = ""
                shade = Color.WHITE

            row = (str(position).rjust(4) + "    "
                   + fit(walker.data, 22)
                   + fit(role, 20)
                   + walker.added)

            print(paint("   │ ", Color.CYAN) + paint(row.ljust(72), shade)
                  + paint(" │", Color.CYAN))
            walker = walker.next
            position = position + 1

        print(paint("   ╰" + bottom_label + "─" * (74 - len(bottom_label)) + "╯",
                    Color.YELLOW))
        print(paint("   FIFO - the animal at the front is the next one dequeue() "
                    "will return.", Color.DIM + Color.GREY))


# Prints a long chain wrapped to fit a terminal, breaking only at an arrow so
# an animal name is never cut in half.
def wrap_print(text: str, color: str) -> None:
    line = ""
    index = 0
    length = len(text)

    while index < length:
        char = text[index]

        # An arrow is the two characters '-' and '>' with spaces around it.
        if (len(line) >= 58 and char == "-"
                and index + 1 < length and text[index + 1] == ">"):
            print("   " + paint(line.strip() + " ->", color))
            line = ""
            index = index + 2

            while index < length and text[index] == " ":
                index = index + 1
            continue

        line = line + char
        index = index + 1

    if line.strip() != "":
        print("   " + paint(line.strip(), color))


# ---------------------------------------------------------------------------
# BANNER + MENU DRAWING
# ---------------------------------------------------------------------------

# Draws the rainbow header with the app title.
def draw_header(subtitle: str) -> None:
    width = 74
    print()
    print(paint("   ╔" + "═" * width + "╗", rainbow(0)))

    art_1 = "████████ ██   ██ ███████     ███████  ██████   ██████ "
    art_2 = "   ██    ██   ██ ██             ███  ██    ██ ██    ██"
    art_3 = "   ██    ███████ █████        ███    ██    ██ ██    ██"
    art_4 = "   ██    ██   ██ ██          ███     ██    ██ ██    ██"
    art_5 = "   ██    ██   ██ ███████    ███████   ██████   ██████ "

    print(paint("   ║" + art_1.center(width) + "║", rainbow(1)))
    print(paint("   ║" + art_2.center(width) + "║", rainbow(2)))
    print(paint("   ║" + art_3.center(width) + "║", rainbow(3)))
    print(paint("   ║" + art_4.center(width) + "║", rainbow(4)))
    print(paint("   ║" + art_5.center(width) + "║", rainbow(5)))
    print(paint("   ║" + " " * width + "║", rainbow(6)))
    print(paint("   ║" + "◀  A Q U E U E   O F   A N I M A L S  ▶".center(width) + "║",
                Color.BOLD + Color.WHITE))
    print(paint("   ╟" + "─" * width + "╢", Color.PURPLE))
    print(paint("   ║" + "First In, First Out  ·  Version 1.0".center(width) + "║",
                Color.CYAN))
    print(paint("   ║" + "Developed by Greg Tovar".center(width) + "║",
                Color.DIM + Color.GREY))
    print(paint("   ╚" + "═" * width + "╝", rainbow(0)))

    if subtitle != "":
        print(paint("   ▸ " + subtitle, Color.BOLD + Color.YELLOW))


# Prints one menu entry.
def draw_option(letter: str, text: str, enabled: bool) -> None:
    if enabled:
        tag = paint("   [" + letter + "] ", Color.BOLD + Color.GREEN)
        body = paint(text, Color.WHITE)
    else:
        tag = paint("   [" + letter + "] ", Color.DIM + Color.GREY)
        body = paint(text + "  (load the CSV first)", Color.DIM + Color.GREY)
    print(tag + body)


# Draws the main menu, dimming what is not available yet.
def draw_menu(queue: "AnimalQueue") -> None:
    ready = queue is not None

    if ready:
        status = "Queue loaded   |   animals in line: " + str(queue.size)
        if not queue.is_empty():
            status = status + "   |   next out: " + queue.peek().data
        print(paint("\n   " + status, Color.GREEN))
    else:
        print(paint("\n   No queue yet - start with option A.", Color.ORANGE))

    print(paint("\n   ─── MENU " + "─" * 65, Color.PURPLE))
    draw_option("A", "Load CSV file", True)
    draw_option("B", "Add animal            → enqueue(data)", ready)
    draw_option("C", "Remove animal         → dequeue()", ready)
    draw_option("D", "Print list            → print_all()", ready)
    draw_option("E", "Update the CSV file", ready)
    print(paint("   [F] ", Color.BOLD + Color.RED) + paint("Exit", Color.WHITE))
    print(paint("   " + "─" * 74, Color.PURPLE))


 

# Returns the field found at 'wanted' (zero based) inside a CSV line.
def read_field(line: str, wanted: int) -> str:
    field = ""
    index = 0
    current = 0
    inside_quotes = False
    length = len(line)

    while index < length:
        char = line[index]

        if inside_quotes:
            if char == '"':
                if index + 1 < length and line[index + 1] == '"':
                    if current == wanted:
                        field = field + '"'
                    index = index + 1
                else:
                    inside_quotes = False
            else:
                if current == wanted:
                    field = field + char
        else:
            if char == '"':
                inside_quotes = True
            elif char == ",":
                if current == wanted:
                    return field.strip()
                current = current + 1
            else:
                if current == wanted:
                    field = field + char

        index = index + 1

    if current == wanted:
        return field.strip()
    return ""


# Counts how many fields a CSV line holds.
def count_fields(line: str) -> int:
    total = 1
    index = 0
    inside_quotes = False

    while index < len(line):
        char = line[index]
        if char == '"':
            inside_quotes = not inside_quotes
        elif char == "," and not inside_quotes:
            total = total + 1
        index = index + 1

    return total


# Wraps a value in quotes only when the value would break the CSV format.
def escape_field(value: str) -> str:
    needs_quotes = False
    index = 0
    while index < len(value):
        char = value[index]
        if char == "," or char == '"' or char == "\n":
            needs_quotes = True
        index = index + 1

    if not needs_quotes:
        return value

    escaped = '"'
    index = 0
    while index < len(value):
        if value[index] == '"':
            escaped = escaped + '""'
        else:
            escaped = escaped + value[index]
        index = index + 1
    return escaped + '"'


 

# Asks a yes/no question and keeps asking until the answer is clear.
def confirm(question: str) -> bool:
    while True:
        answer = input(paint("   " + question + " (y/n): ", Color.YELLOW)).strip().lower()
        if answer == "y" or answer == "yes":
            return True
        if answer == "n" or answer == "no":
            return False
        print(paint("   Please answer with y or n.", Color.RED))


# Asks for a non empty piece of text.
def ask_text(label: str) -> str:
    while True:
        value = input(paint("   " + label + ": ", Color.CYAN)).strip()
        if value != "":
            return value
        print(paint("   This field cannot be empty.", Color.RED))


# Prints a green success line.
def success(message: str) -> None:
    print(paint("\n   ✔ " + message, Color.BOLD + Color.GREEN))


# Prints a red failure line.
def failure(message: str) -> None:
    print(paint("\n   ✖ " + message, Color.BOLD + Color.RED))


# ---------------------------------------------------------------------------
# MENU ACTIONS
# ---------------------------------------------------------------------------

# Option A - loads the CSV file and builds the queue from it.
def option_load_csv(queue: "AnimalQueue") -> "AnimalQueue":
    clear_screen()
    draw_header("OPTION A - Load CSV file")

    print(paint("\n   Program folder: " + BASE_DIR, Color.GREY))
    print(paint("   Leave blank to use " + DEFAULT_CSV + " from that folder.", Color.GREY))
    typed = input(paint("   CSV path: ", Color.CYAN))
    path = resolve_path(typed, DEFAULT_CSV)

    if not os.path.isfile(path):
        failure("No file found at:")
        print(paint("     " + path, Color.RED))
        list_csv_files()
        pause()
        return queue

    if queue is not None and not queue.is_empty():
        print(paint("\n   A queue with " + str(queue.size)
                    + " animal(s) is already loaded.", Color.ORANGE))
        if not confirm("Replace it with the contents of this file?"):
            failure("Cancelled. The current queue is untouched.")
            pause()
            return queue

    try:
        handle = open(path, "r", encoding="utf-8-sig")
    except OSError as error:
        failure("Could not open the file: " + str(error))
        pause()
        return queue

    fresh = AnimalQueue("The Zoo")
    loaded = 0
    skipped = 0
    duplicates = 0
    line_number = 0

    for raw_line in handle:
        line_number = line_number + 1
        line = raw_line.rstrip("\r\n")

        if line.strip() == "":
            continue

        # The file has no header, but a header is tolerated if one shows up.
        if line_number == 1:
            lowered = line.lower()
            if lowered.startswith("id,") or lowered.startswith("position,") \
                    or lowered.startswith("#,") or lowered.startswith("number,"):
                continue

        # One column means the whole line is the animal. Two or more means the
        # first column is a position and the animal sits in the second.
        # read_field is used either way so a quoted name like "Bee, Honey"
        # loses its quotes instead of keeping them as part of the name.
        if count_fields(line) == 1:
            animal = read_field(line, 0)
        else:
            animal = read_field(line, 1)

        if animal == "":
            skipped = skipped + 1
            continue
        if fresh.contains(animal):
            duplicates = duplicates + 1
            continue

        # Rows are read top to bottom and enqueued, so line 1 ends up at the
        # front of the queue - the same order the file lists them in.
        fresh.enqueue(animal)
        loaded = loaded + 1

    handle.close()

    if loaded == 0:
        failure("The file contained no usable rows.")
        pause()
        return queue

    fresh.source_path = path
    success(str(loaded) + " animal(s) loaded into the queue.")
    print(paint("   Source: " + path, Color.GREY))
    if skipped > 0:
        print(paint("   " + str(skipped) + " row(s) skipped - no animal name.",
                    Color.ORANGE))
    if duplicates > 0:
        print(paint("   " + str(duplicates) + " row(s) skipped - already in the queue.",
                    Color.ORANGE))

    fresh.print_table()
    pause()
    return fresh


# Option B - asks for an animal and enqueues it at the rear.
def option_add_animal(queue: "AnimalQueue") -> None:
    clear_screen()
    draw_header("OPTION B - Add animal  →  enqueue(data)")

    print(paint("\n   The new animal joins at the REAR of the line.", Color.GREY))
    animal = ask_text("Animal")

    if queue.contains(animal):
        print(paint("\n   '" + animal + "' is already in the queue.", Color.ORANGE))
        if not confirm("Add it anyway?"):
            failure("Cancelled. Nothing was added.")
            pause()
            return

    queue.enqueue(animal)

    success("'" + animal + "' joined the line at position " + str(queue.size) + ".")
    print(paint("   Animals in line: " + str(queue.size), Color.GREY))
    print(paint("\n   Queue is now:", Color.BOLD + Color.WHITE))
    queue.print_all()
    pause()


# Option C - dequeues the animal at the front and shows what left.
def option_remove_animal(queue: "AnimalQueue") -> None:
    clear_screen()
    draw_header("OPTION C - Remove animal  →  dequeue()")

    if queue.is_empty():
        failure("The queue is empty - there is nothing to remove.")
        print(paint("   dequeue() returned None instead of crashing.", Color.GREY))
        pause()
        return

    queue.print_table()

    target = queue.peek()
    print(paint("\n   Animal at the FRONT: ", Color.WHITE)
          + paint(target.data, Color.BOLD + Color.YELLOW))
    print(paint("   In line since: " + target.added, Color.GREY))
    print(paint("   A queue only releases from the front - "
                "everyone else keeps waiting.", Color.GREY))
    print()

    if not confirm("Remove this animal from the zoo?"):
        failure("Cancelled. The animal stays in line.")
        pause()
        return

    removed = queue.dequeue()

    success("dequeue() returned: " + removed)
    print(paint("   Animals still in line: " + str(queue.size), Color.GREY))

    print(paint("\n   Queue is now:", Color.BOLD + Color.WHITE))
    queue.print_all()

    if not queue.is_empty():
        print(paint("\n   Next to leave: " + queue.peek().data, Color.CYAN))

    pause()


# Option D - prints the queue, both as a chain and as a table.
def option_print_all(queue: "AnimalQueue") -> None:
    clear_screen()
    draw_header("OPTION D - Print list  →  print_all()")

    print(paint("\n   print_all() output:", Color.BOLD + Color.WHITE))
    print()
    queue.print_all()

    queue.print_table()
    pause()


# Option E - writes the active queue back out to a CSV file.
def option_save_csv(queue: "AnimalQueue") -> None:
    clear_screen()
    draw_header("OPTION E - Update the CSV file")

    if queue.is_empty():
        failure("The queue is empty - there is nothing to write.")
        pause()
        return

    if queue.source_path != "":
        fallback = queue.source_path
    else:
        fallback = BASE_DIR + os.sep + DEFAULT_CSV

    print(paint("\n   Program folder: " + BASE_DIR, Color.GREY))
    print(paint("   Leave blank to update: " + fallback, Color.GREY))
    typed = input(paint("   CSV path: ", Color.CYAN))
    path = resolve_path(typed, fallback)

    if os.path.isfile(path):
        print(paint("\n   This file already exists and will be overwritten:", Color.ORANGE))
        print(paint("     " + path, Color.ORANGE))
        if not confirm("Continue?"):
            failure("Cancelled. The file was not modified.")
            pause()
            return
    else:
        print(paint("\n   A new file will be created at:", Color.YELLOW))
        print(paint("     " + path, Color.YELLOW))
        if not confirm("Continue?"):
            failure("Cancelled. Nothing was written.")
            pause()
            return

    try:
        handle = open(path, "w", encoding="utf-8", newline="")
    except OSError as error:
        failure("Could not write the file: " + str(error))
        pause()
        return

    # The original file has no header and uses 'position,animal', so the same
    # shape is written back. Positions are renumbered from the front.
    walker = queue.front
    position = 1
    while walker is not None:
        handle.write(str(position) + "," + escape_field(walker.data) + "\n")
        walker = walker.next
        position = position + 1

    handle.close()
    queue.source_path = path

    success(str(queue.size) + " animal(s) written to:")
    print(paint("     " + path, Color.GREEN))
    print(paint("   Row 1 is the front of the queue.", Color.GREY))
    pause()


# ---------------------------------------------------------------------------
# GOODBYE SCREEN
# ---------------------------------------------------------------------------

# Prints the session timer and signs off.
def goodbye(queue: "AnimalQueue", started_at: float) -> None:
    elapsed = int(time.time() - started_at)
    minutes = elapsed // 60
    seconds = elapsed % 60

    clear_screen()
    width = 74
    print()
    print(paint("   ╔" + "═" * width + "╗", rainbow(3)))
    print(paint("   ║" + "SESSION CLOSED".center(width) + "║", Color.BOLD + Color.GREEN))
    print(paint("   ╟" + "─" * width + "╢", rainbow(3)))

    if queue is None:
        summary = "No queue was loaded this session."
    else:
        summary = "The zoo ended with " + str(queue.size) + " animal(s) in line."

    timer = "Session time: " + str(minutes) + "m " + str(seconds) + "s"
    print(paint("   ║" + summary.center(width) + "║", Color.WHITE))
    print(paint("   ║" + timer.center(width) + "║", Color.CYAN))
    print(paint("   ║" + " " * width + "║", rainbow(3)))
    print(paint("   ║" + "Thanks for visiting THE ZOO v1.0".center(width) + "║",
                Color.YELLOW))
    print(paint("   ║" + "Developed by Greg Tovar".center(width) + "║",
                Color.DIM + Color.GREY))
    print(paint("   ╚" + "═" * width + "╝", rainbow(3)))
    print()


# ---------------------------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------------------------

# Runs the menu until the user exits.
def main() -> None:
    started_at = time.time()
    queue = None
    message = ""

    while True:
        clear_screen()
        draw_header("")
        draw_menu(queue)

        if message != "":
            print(paint("   " + message, Color.RED))
            message = ""

        choice = input(paint("\n   Select an option: ", Color.BOLD + Color.CYAN)).strip().upper()

        if choice == "F":
            break

        if choice == "A":
            queue = option_load_csv(queue)
            continue

        if choice == "B" or choice == "C" or choice == "D" or choice == "E":
            if queue is None:
                message = "✖ Load the CSV file first (option A)."
                continue

            if choice == "B":
                option_add_animal(queue)
            elif choice == "C":
                option_remove_animal(queue)
            elif choice == "D":
                option_print_all(queue)
            else:
                option_save_csv(queue)
            continue

        message = "✖ '" + choice + "' is not a valid option."

    goodbye(queue, started_at)


#
#
#    MAIN PROGRAM
#
#


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(paint("\n\n   Interrupted. Closing THE ZOO.\n", Color.RED))