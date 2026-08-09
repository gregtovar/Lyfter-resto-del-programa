"""STACK SYSTEM - Car dealership parking lot - Version 1.0

A pure linked-node Stack implementation.

RULES HONORED IN THIS FILE:
    - No lists, no dicts, no tuples, no sets.
    - No 'collections' module (no deque, no namedtuple, no OrderedDict).
    - No str.split() / str.join() either, because those build lists internally.
    - The only container is CarNode, chained together by the '.next' pointer.
"""

import os
import random
import time
from datetime import datetime


# Managing the Path to avoid problems
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = "cars_stack_hex_ids.csv"


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

    beside_script = os.path.join(BASE_DIR, value)
    if os.path.isfile(beside_script):
        return beside_script

    from_terminal = os.path.abspath(value)
    if os.path.isfile(from_terminal):
        return from_terminal

    # Nothing exists yet, so default to writing next to the script.
    return beside_script


# ANSI color palette.
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


# Node management
class CarNode:

    # Builds a single car node.
    def __init__(self, car_id: str, make: str, model: str,
                 year: str, timestamp: str) -> None:
        self.car_id = car_id
        self.make = make
        self.model = model
        self.year = year
        self.timestamp = timestamp
        self.next = None

    # Row used by the table printer.
    def as_row(self, position: int) -> str:
        return (str(position).rjust(4) + "  "
                + fit(self.car_id, 10)
                + fit(self.make, 15)
                + fit(self.model, 15)
                + fit(self.year, 7)
                + self.timestamp)

    # Short one-line description used in prompts and confirmations.
    def label(self) -> str:
        return self.year + " " + self.make + " " + self.model + " [" + self.car_id + "]"


# ---------------------------------------------------------------------------
# The Stack itself. LIFO: the last car parked is the first car out.
# ---------------------------------------------------------------------------
class CarStack:

    # Initializes an empty structure under a chosen name.
    def __init__(self, name: str) -> None:
        self.name = name
        self.top = None
        self.size = 0
        self.source_path = ""
        self.created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # True when there is nothing parked.
    def is_empty(self) -> bool:
        return self.top is None

    # Adds a node on top of the structure.
    def push(self, node: "CarNode") -> "CarNode":
        node.next = self.top
        self.top = node
        self.size = self.size + 1
        return node

    # Removes and returns the node on top. Returns None when empty.
    def pop(self) -> "CarNode":
        if self.top is None:
            return None
        removed = self.top
        self.top = removed.next
        removed.next = None
        self.size = self.size - 1
        return removed

    # Looks at the top node without removing it.
    def peek(self) -> "CarNode":
        return self.top

    # True when an ID is already parked in the lot.
    def has_id(self, car_id: str) -> bool:
        walker = self.top
        while walker is not None:
            if walker.car_id == car_id:
                return True
            walker = walker.next
        return False

    # Prints the whole structure as a framed table, top of stack first.
    def print_structure(self) -> None:
        title = "STACK: " + self.name
        print(paint("\n   " + title, Color.BOLD + Color.CYAN))
        print(paint("   created " + self.created
                    + "   |   cars parked: " + str(self.size), Color.GREY))

        if self.is_empty():
            print(paint("\n   ╭" + "─" * 74 + "╮", Color.GREY))
            print(paint("   │" + "The stack is empty - nothing parked yet.".center(74) + "│",
                        Color.YELLOW))
            print(paint("   ╰" + "─" * 74 + "╯", Color.GREY))
            return

        header = (" POS".ljust(6) + "ID".ljust(10) + "MAKE".ljust(15)
                  + "MODEL".ljust(15) + "YEAR".ljust(7) + "ADDED ON")

        print(paint("\n   ╭" + "─" * 74 + "╮", Color.CYAN))
        print(paint("   │ ", Color.CYAN) + paint(header.ljust(72), Color.BOLD + Color.WHITE)
              + paint(" │", Color.CYAN))
        print(paint("   ├" + "─" * 74 + "┤", Color.CYAN))

        walker = self.top
        position = 1
        while walker is not None:
            row = walker.as_row(position)
            if position == 1:
                body = paint(row.ljust(72), Color.GREEN + Color.BOLD)
                tag = paint(" │", Color.CYAN)
            else:
                body = paint(row.ljust(72), Color.WHITE)
                tag = paint(" │", Color.CYAN)
            print(paint("   │ ", Color.CYAN) + body + tag)
            walker = walker.next
            position = position + 1

        print(paint("   ╰" + "─" * 74 + "╯", Color.CYAN))
        print(paint("   ▲ position 1 is the TOP of the stack "
                    "(last one in, first one out).", Color.DIM + Color.GREEN))


# Draws the animated-looking rainbow header with the app title.
def draw_header(subtitle: str) -> None:
    width = 74
    print()
    print(paint("   ╔" + "═" * width + "╗", rainbow(0)))

    art_1 = "███████ ███████  █████   ██████ ██   ██"
    art_2 = "██         ██   ██   ██ ██      ██  ██ "
    art_3 = "███████    ██   ███████ ██      █████  "
    art_4 = "     ██    ██   ██   ██ ██      ██  ██ "
    art_5 = "███████    ██   ██   ██  ██████ ██   ██"

    print(paint("   ║" + art_1.center(width) + "║", rainbow(1)))
    print(paint("   ║" + art_2.center(width) + "║", rainbow(2)))
    print(paint("   ║" + art_3.center(width) + "║", rainbow(3)))
    print(paint("   ║" + art_4.center(width) + "║", rainbow(4)))
    print(paint("   ║" + art_5.center(width) + "║", rainbow(5)))
    print(paint("   ║" + " " * width + "║", rainbow(6)))
    print(paint("   ║" + "S Y S T E M".center(width) + "║", Color.BOLD + Color.WHITE))
    print(paint("   ╟" + "─" * width + "╢", Color.PURPLE))
    print(paint("   ║" + "Car dealership parking lot  ·  Version 1.0".center(width) + "║",
                Color.CYAN))
    print(paint("   ║" + "Developed by Greg Tovar".center(width) + "║", Color.DIM + Color.GREY))
    print(paint("   ╚" + "═" * width + "╝", rainbow(0)))

    if subtitle != "":
        print(paint("   ▸ " + subtitle, Color.BOLD + Color.YELLOW))


# Prints one menu entry.
def draw_option(number: str, text: str, enabled: bool) -> None:
    if enabled:
        tag = paint("   [" + number + "] ", Color.BOLD + Color.GREEN)
        body = paint(text, Color.WHITE)
    else:
        tag = paint("   [" + number + "] ", Color.DIM + Color.GREY)
        body = paint(text + "  (needs option 1)", Color.DIM + Color.GREY)
    print(tag + body)


# Draws the main menu, dimming what is not available yet.
def draw_menu(stack: "CarStack") -> None:
    ready = stack is not None

    if ready:
        status = ("Active stack: " + stack.name
                  + "   |   cars parked: " + str(stack.size))
        print(paint("\n   " + status, Color.GREEN))
    else:
        print(paint("\n   No stack initialized yet - start with option 1.", Color.ORANGE))

    print(paint("\n   ─── MENU " + "─" * 65, Color.PURPLE))
    draw_option("1", "Initialize the stack", True)
    draw_option("2", "Upload existing CSV file  (optional)", ready)
    draw_option("3", "Add a car to the stack", ready)
    draw_option("4", "Remove a car (pop the top)", ready)
    draw_option("5", "List the stack", ready)
    draw_option("6", "Update CSV file with the active stack", ready)
    print(paint("   [0] ", Color.BOLD + Color.RED) + paint("Exit", Color.WHITE))
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


# Builds an 8 character hexadecimal ID that is not already in the stack.
def new_hex_id(stack: "CarStack") -> str:
    candidate = ""
    while True:
        candidate = format(random.randint(0, 0xFFFFFFFF), "08X")
        if not stack.has_id(candidate):
            return candidate


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


# Asks for a 4 digit model year inside a sane range.
def ask_year() -> str:
    while True:
        value = input(paint("   Year: ", Color.CYAN)).strip()
        if len(value) == 4 and value.isdigit():
            number = int(value)
            if 1900 <= number <= datetime.now().year + 2:
                return value
        print(paint("   Enter a 4 digit year between 1900 and "
                    + str(datetime.now().year + 2) + ".", Color.RED))


# Prints a green success line.
def success(message: str) -> None:
    print(paint("\n   ✔ " + message, Color.BOLD + Color.GREEN))


# Prints a red failure line.
def failure(message: str) -> None:
    print(paint("\n   ✖ " + message, Color.BOLD + Color.RED))


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
# MENU MANAGEMENT
# ---------------------------------------------------------------------------

# Option 1 - creates the structure and gives it a name.
def option_initialize(stack: "CarStack") -> "CarStack":
    clear_screen()
    draw_header("OPTION 1 - Initialize the stack")

    if stack is not None:
        print(paint("\n   A stack named '" + stack.name + "' is already active with "
                    + str(stack.size) + " car(s).", Color.ORANGE))
        if not confirm("Discard it and start a brand new one?"):
            failure("Initialization cancelled. The current stack is untouched.")
            pause()
            return stack

    print(paint("\n   Give this parking lot a name.", Color.GREY))
    name = ask_text("Stack name")
    fresh = CarStack(name)
    success("Stack '" + fresh.name + "' initialized and ready at " + fresh.created + ".")
    pause()
    return fresh


# Option 2 - loads a CSV file into the structure.
def option_load_csv(stack: "CarStack") -> None:
    clear_screen()
    draw_header("OPTION 2 - Upload existing CSV file")

    print(paint("\n   Program folder: " + BASE_DIR, Color.GREY))
    print(paint("   Leave blank to use " + DEFAULT_CSV + " from that folder.", Color.GREY))
    typed = input(paint("   CSV path: ", Color.CYAN))
    path = resolve_path(typed, DEFAULT_CSV)

    if not os.path.isfile(path):
        failure("No file found at:")
        print(paint("     " + path, Color.RED))
        list_csv_files()
        pause()
        return

    if not stack.is_empty():
        print(paint("\n   The stack already holds " + str(stack.size) + " car(s).",
                    Color.ORANGE))
        if confirm("Clear it before loading the file?"):
            while not stack.is_empty():
                stack.pop()

    # Cars are read top down, but a stack has to be filled bottom up.
    # A second stack reverses the order for free - no list needed.
    buffer_stack = CarStack("buffer")
    loaded = 0
    skipped = 0
    line_number = 0

    try:
        handle = open(path, "r", encoding="utf-8-sig")
    except OSError as error:
        failure("Could not open the file: " + str(error))
        pause()
        return

    for raw_line in handle:
        line_number = line_number + 1
        line = raw_line.rstrip("\r\n")

        if line.strip() == "":
            continue
        if line_number == 1 and line.lower().startswith("stack position"):
            continue

        car_id = read_field(line, 1)
        make = read_field(line, 2)
        model = read_field(line, 3)
        year = read_field(line, 4)
        timestamp = read_field(line, 5)

        if make == "" or model == "":
            skipped = skipped + 1
            continue
        if car_id == "":
            car_id = format(random.randint(0, 0xFFFFFFFF), "08X")
        if timestamp == "":
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        buffer_stack.push(CarNode(car_id, make, model, year, timestamp))
        loaded = loaded + 1

    handle.close()

    # Drain the buffer into the real stack so line 1 ends up on top.
    while not buffer_stack.is_empty():
        stack.push(buffer_stack.pop())

    stack.source_path = path
    success(str(loaded) + " car(s) loaded into '" + stack.name + "'.")
    print(paint("   Source: " + path, Color.GREY))
    if skipped > 0:
        print(paint("   " + str(skipped) + " row(s) skipped - missing make or model.",
                    Color.ORANGE))
    stack.print_structure()
    pause()


# Option 3 - pushes a new car with an automatic timestamp.
def option_add_car(stack: "CarStack") -> None:
    clear_screen()
    draw_header("OPTION 3 - Add a car to the stack")

    print(paint("\n   The timestamp is generated by the system.", Color.GREY))
    make = ask_text("Make")
    model = ask_text("Model")
    year = ask_year()

    car_id = new_hex_id(stack)
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    node = CarNode(car_id, make, model, year, stamp)

    print(paint("\n   About to park: ", Color.WHITE) + paint(node.label(), Color.BOLD + Color.CYAN))
    if not confirm("Push this car onto the stack?"):
        failure("Cancelled. Nothing was added.")
        pause()
        return

    stack.push(node)
    success(node.label() + " parked on top. Stack size is now " + str(stack.size) + ".")
    print(paint("   Timestamp recorded: " + stamp, Color.GREY))
    pause()


# Option 4 - shows the stack and pops the top car after confirmation.
def option_remove_car(stack: "CarStack") -> None:
    clear_screen()
    draw_header("OPTION 4 - Remove a car")

    if stack.is_empty():
        failure("The stack is empty - there is nothing to remove.")
        pause()
        return

    stack.print_structure()

    target = stack.peek()
    print(paint("\n   Only the car on top can leave the lot - "
                "everything else is blocked in.", Color.GREY))
    print(paint("   Car on top: ", Color.WHITE) + paint(target.label(), Color.BOLD + Color.YELLOW))
    print(paint("   Parked since: " + target.timestamp, Color.GREY))
    print()

    if not confirm("Are you sure you want to remove this car?"):
        failure("Cancelled. The car stays parked.")
        pause()
        return

    removed = stack.pop()
    success(removed.label() + " removed from the lot.")
    print(paint("   Cars still parked: " + str(stack.size), Color.GREY))
    pause()


# Option 5 - prints the whole structure.
def option_list_stack(stack: "CarStack") -> None:
    clear_screen()
    draw_header("OPTION 5 - List the stack")
    stack.print_structure()
    pause()


# Option 6 - writes the active stack back out to a CSV file.
def option_save_csv(stack: "CarStack") -> None:
    clear_screen()
    draw_header("OPTION 6 - Update CSV file with active stack")

    if stack.is_empty():
        failure("The stack is empty - there is nothing to write.")
        pause()
        return

    if stack.source_path != "":
        fallback = stack.source_path
    else:
        fallback = os.path.join(BASE_DIR, DEFAULT_CSV)

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

    handle.write("Stack Position,ID,Make,Model,Year,Timestamp When Added\n")

    walker = stack.top
    position = 1
    while walker is not None:
        handle.write(str(position) + ","
                     + escape_field(walker.car_id) + ","
                     + escape_field(walker.make) + ","
                     + escape_field(walker.model) + ","
                     + escape_field(walker.year) + ","
                     + escape_field(walker.timestamp) + "\n")
        walker = walker.next
        position = position + 1

    handle.close()
    stack.source_path = path
    success(str(stack.size) + " car(s) written to:")
    print(paint("     " + path, Color.GREEN))
    print(paint("   Position 1 in the file is the top of the stack.", Color.GREY))
    pause()


# ---------------------------------------------------------------------------
# GOODBYE SCREEN
# ---------------------------------------------------------------------------

# Prints the session timer and signs off.
def goodbye(stack: "CarStack", started_at: float) -> None:
    elapsed = int(time.time() - started_at)
    minutes = elapsed // 60
    seconds = elapsed % 60

    clear_screen()
    width = 74
    print()
    print(paint("   ╔" + "═" * width + "╗", rainbow(3)))
    print(paint("   ║" + "SESSION CLOSED".center(width) + "║", Color.BOLD + Color.GREEN))
    print(paint("   ╟" + "─" * width + "╢", rainbow(3)))

    if stack is None:
        summary = "No stack was initialized this session."
    else:
        summary = ("Stack '" + stack.name + "' ended with "
                   + str(stack.size) + " car(s) parked.")

    timer = "Session time: " + str(minutes) + "m " + str(seconds) + "s"
    print(paint("   ║" + summary.center(width) + "║", Color.WHITE))
    print(paint("   ║" + timer.center(width) + "║", Color.CYAN))
    print(paint("   ║" + " " * width + "║", rainbow(3)))
    print(paint("   ║" + "Thanks for using STACK SYSTEM v1.0".center(width) + "║",
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
    stack = None
    message = ""

    while True:
        clear_screen()
        draw_header("")
        draw_menu(stack)

        if message != "":
            print(paint("   " + message, Color.RED))
            message = ""

        choice = input(paint("\n   Select an option: ", Color.BOLD + Color.CYAN)).strip()

        if choice == "0":
            break

        if choice == "1":
            stack = option_initialize(stack)
            continue

        if choice == "2" or choice == "3" or choice == "4" \
                or choice == "5" or choice == "6":
            if stack is None:
                message = "✖ Initialize the stack first (option 1)."
                continue

            if choice == "2":
                option_load_csv(stack)
            elif choice == "3":
                option_add_car(stack)
            elif choice == "4":
                option_remove_car(stack)
            elif choice == "5":
                option_list_stack(stack)
            else:
                option_save_csv(stack)
            continue

        message = "✖ '" + choice + "' is not a valid option."

    goodbye(stack, started_at)


#
# MAIN PROGRAM
#

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(paint("\n\n   Interrupted. Closing STACK SYSTEM.\n", Color.RED))