"""THE ZOO - A Doubly Linked List - Version 1.0

Every node holds TWO references: '.next' points at the node behind it and
'.prev' points at the node in front of it. That is the whole difference from
a singly linked list, and it is what makes print_backward() and delete()
cheap instead of painful.

"""

import os
import time
from datetime import datetime



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = "animals.csv"



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
# The Node. One animal, holding a reference in BOTH directions.
# ---------------------------------------------------------------------------
class AnimalNode:

    # Builds a single detached node.
    def __init__(self, data: str) -> None:
        self.data = data
        self.added = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.prev = None
        self.next = None


# ---------------------------------------------------------------------------
# The Doubly Linked List.
# 'head' is the first animal, 'tail' is the last.
# ---------------------------------------------------------------------------
class AnimalList:

    # Initializes an empty list.
    def __init__(self, name: str) -> None:
        self.name = name
        self.head = None
        self.tail = None
        self.size = 0
        self.source_path = ""
        self.created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # True when the list holds no animals.
    def is_empty(self) -> bool:
        return self.head is None

    # -----------------------------------------------------------------
    # REQUIRED METHOD 1 - append(data): adds a node at the END.
    # -----------------------------------------------------------------
    def append(self, data: str) -> "AnimalNode":
        node = AnimalNode(data)
        node.prev = self.tail
        node.next = None

        if self.tail is None:
            # First animal ever: it is both the head and the tail.
            self.head = node
        else:
            self.tail.next = node

        self.tail = node
        self.size = self.size + 1
        return node

    # -----------------------------------------------------------------
    # REQUIRED METHOD 2 - prepend(data): adds a node at the BEGINNING.
    # -----------------------------------------------------------------
    def prepend(self, data: str) -> "AnimalNode":
        node = AnimalNode(data)
        node.prev = None
        node.next = self.head

        if self.head is None:
            self.tail = node
        else:
            self.head.prev = node

        self.head = node
        self.size = self.size + 1
        return node

    # -----------------------------------------------------------------
    # REQUIRED METHOD 3 - delete(data): finds an animal by name and
    # unlinks it. Returns True when something was removed, False when the
    # name was not in the list.
    #
    # This is where the backward pointer pays off. The node already knows
    # both of its neighbours, so it can step out of the chain by simply
    # pointing them at each other - no second walk to find the previous
    # node, the way a singly linked list would need.
    # -----------------------------------------------------------------
    def delete(self, data: str) -> bool:
        node = self.find(data)
        if node is None:
            return False

        if node.prev is None:
            # Removing the head: the next node becomes the new head.
            self.head = node.next
        else:
            node.prev.next = node.next

        if node.next is None:
            # Removing the tail: the previous node becomes the new tail.
            self.tail = node.prev
        else:
            node.next.prev = node.prev

        # Detach the node completely so it does not keep the chain alive.
        node.prev = None
        node.next = None
        self.size = self.size - 1
        return True

    # -----------------------------------------------------------------
    # REQUIRED METHOD 4 - print_forward(): head to tail.
    # -----------------------------------------------------------------
    def print_forward(self) -> None:
        if self.is_empty():
            print(paint("   (the list is empty)", Color.YELLOW))
            return

        line = ""
        walker = self.head
        while walker is not None:
            if line == "":
                line = walker.data
            else:
                line = line + " <-> " + walker.data
            walker = walker.next

        wrap_print(line, Color.GREEN)

    # -----------------------------------------------------------------
    # REQUIRED METHOD 5 - print_backward(): tail to head.
    # Note this walks '.prev', which only exists because the list is
    # doubly linked. A singly linked list could not do this directly.
    # -----------------------------------------------------------------
    def print_backward(self) -> None:
        if self.is_empty():
            print(paint("   (the list is empty)", Color.YELLOW))
            return

        line = ""
        walker = self.tail
        while walker is not None:
            if line == "":
                line = walker.data
            else:
                line = line + " <-> " + walker.data
            walker = walker.prev

        wrap_print(line, Color.PINK)

    # -----------------------------------------------------------------
    # SUPPORTING METHODS
    # -----------------------------------------------------------------

    # Finds a node by name, ignoring case. Returns None when absent.
    def find(self, data: str) -> "AnimalNode":
        wanted = data.strip().lower()
        walker = self.head
        while walker is not None:
            if walker.data.lower() == wanted:
                return walker
            walker = walker.next
        return None

    # Returns the 1 based position of a node, or 0 when it is not present.
    def position_of(self, node: "AnimalNode") -> int:
        walker = self.head
        position = 1
        while walker is not None:
            if walker is node:
                return position
            walker = walker.next
            position = position + 1
        return 0

    # True when a name is already in the list.
    def contains(self, data: str) -> bool:
        return self.find(data) is not None

    # Prints both directions together, the way options B and C need.
    def print_both(self) -> None:
        print(paint("\n   FORWARD   (head → tail)  print_forward()",
                    Color.BOLD + Color.GREEN))
        self.print_forward()
        print(paint("\n   BACKWARD  (tail → head)  print_backward()",
                    Color.BOLD + Color.PINK))
        self.print_backward()

    # Prints the list as a framed table with positions and neighbours.
    def print_table(self) -> None:
        print(paint("\n   LIST: " + self.name, Color.BOLD + Color.CYAN))
        print(paint("   created " + self.created
                    + "   |   animals: " + str(self.size), Color.GREY))

        if self.is_empty():
            print(paint("\n   ╭" + "─" * 74 + "╮", Color.GREY))
            print(paint("   │" + "The zoo is empty - no animals in the list.".center(74)
                        + "│", Color.YELLOW))
            print(paint("   ╰" + "─" * 74 + "╯", Color.GREY))
            return

        header = (" POS".ljust(7) + "◀ PREV".ljust(17) + "ANIMAL".ljust(17)
                  + "NEXT ▶".ljust(17) + "ROLE")

        top_label = "─ ◀ HEAD "
        bottom_label = "─ ▶ TAIL "

        print(paint("\n   ╭" + top_label + "─" * (74 - len(top_label)) + "╮", Color.GREEN))
        print(paint("   │ ", Color.CYAN) + paint(header.ljust(72), Color.BOLD + Color.WHITE)
              + paint(" │", Color.CYAN))
        print(paint("   ├" + "─" * 74 + "┤", Color.CYAN))

        walker = self.head
        position = 1
        while walker is not None:
            if walker.prev is None:
                prev_text = "· none ·"
            else:
                prev_text = walker.prev.data

            if walker.next is None:
                next_text = "· none ·"
            else:
                next_text = walker.next.data

            if walker is self.head and walker is self.tail:
                role = "head + tail"
                shade = Color.PINK + Color.BOLD
            elif walker is self.head:
                role = "head"
                shade = Color.GREEN + Color.BOLD
            elif walker is self.tail:
                role = "tail"
                shade = Color.YELLOW + Color.BOLD
            else:
                role = ""
                shade = Color.WHITE

            row = (str(position).rjust(4) + "   "
                   + fit(prev_text, 17)
                   + fit(walker.data, 17)
                   + fit(next_text, 17)
                   + role)

            print(paint("   │ ", Color.CYAN) + paint(row.ljust(72), shade)
                  + paint(" │", Color.CYAN))
            walker = walker.next
            position = position + 1

        print(paint("   ╰" + bottom_label + "─" * (74 - len(bottom_label)) + "╯",
                    Color.YELLOW))
        print(paint("   Every node stores both neighbours, so the chain can be read "
                    "either way.", Color.DIM + Color.GREY))


# Prints a long chain wrapped to fit a terminal, breaking only at an arrow so
# an animal name is never cut in half.
def wrap_print(text: str, color: str) -> None:
    line = ""
    index = 0
    length = len(text)

    while index < length:
        char = text[index]

        # The arrow is '<->' surrounded by spaces.
        if (len(line) >= 56 and char == "<"
                and index + 2 < length and text[index + 1] == "-"
                and text[index + 2] == ">"):
            print("   " + paint(line.strip() + " <->", color))
            line = ""
            index = index + 3

            while index < length and text[index] == " ":
                index = index + 1
            continue

        line = line + char
        index = index + 1

    if line.strip() != "":
        print("   " + paint(line.strip(), color))

 

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
    print(paint("   ║" + "◀-▶  D O U B L Y   L I N K E D   L I S T  ◀-▶".center(width)
                + "║", Color.BOLD + Color.WHITE))
    print(paint("   ╟" + "─" * width + "╢", Color.PURPLE))
    print(paint("   ║" + "Every node knows both neighbours  ·  Version 1.0".center(width)
                + "║", Color.CYAN))
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
def draw_menu(animals: "AnimalList") -> None:
    ready = animals is not None

    if ready:
        status = "List loaded   |   animals: " + str(animals.size)
        if not animals.is_empty():
            status = (status + "   |   head: " + animals.head.data
                      + "   |   tail: " + animals.tail.data)
        print(paint("\n   " + status, Color.GREEN))
    else:
        print(paint("\n   No list yet - start with option A.", Color.ORANGE))

    print(paint("\n   ─── MENU " + "─" * 65, Color.PURPLE))
    draw_option("A", "Load CSV file", True)
    draw_option("B", "Add animal          → prepend(data)", ready)
    draw_option("C", "Remove animal       → delete(data)", ready)
    draw_option("D", "Print list forward  → print_forward()", ready)
    draw_option("E", "Print list backward → print_backward()", ready)
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

# Option A - loads the CSV file and builds the list from it.
def option_load_csv(animals: "AnimalList") -> "AnimalList":
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
        return animals

    if animals is not None and not animals.is_empty():
        print(paint("\n   A list with " + str(animals.size)
                    + " animal(s) is already loaded.", Color.ORANGE))
        if not confirm("Replace it with the contents of this file?"):
            failure("Cancelled. The current list is untouched.")
            pause()
            return animals

    try:
        handle = open(path, "r", encoding="utf-8-sig")
    except OSError as error:
        failure("Could not open the file: " + str(error))
        pause()
        return animals

    fresh = AnimalList("The Zoo")
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

        # Rows are read top to bottom and appended, so line 1 becomes the head
        # and the file order is preserved exactly.
        fresh.append(animal)
        loaded = loaded + 1

    handle.close()

    if loaded == 0:
        failure("The file contained no usable rows.")
        pause()
        return animals

    fresh.source_path = path
    success(str(loaded) + " animal(s) loaded into the list.")
    print(paint("   Source: " + path, Color.GREY))
    print(paint("   Built with append(), so the file order is preserved.", Color.GREY))
    if skipped > 0:
        print(paint("   " + str(skipped) + " row(s) skipped - no animal name.",
                    Color.ORANGE))
    if duplicates > 0:
        print(paint("   " + str(duplicates) + " row(s) skipped - already in the list.",
                    Color.ORANGE))

    fresh.print_table()
    pause()
    return fresh


# Option B - asks for an animal and prepends it at the head.
def option_add_animal(animals: "AnimalList") -> None:
    clear_screen()
    draw_header("OPTION B - Add animal  →  prepend(data)")

    print(paint("\n   prepend() puts the new animal at the BEGINNING of the list.",
                Color.GREY))
    animal = ask_text("Animal")

    if animals.contains(animal):
        print(paint("\n   '" + animal + "' is already in the list.", Color.ORANGE))
        if not confirm("Add it anyway?"):
            failure("Cancelled. Nothing was added.")
            pause()
            return

    animals.prepend(animal)

    success("'" + animal + "' added at the head. Animals: " + str(animals.size) + ".")
    animals.print_both()
    pause()


# Option C - asks for an animal and deletes it if present.
def option_remove_animal(animals: "AnimalList") -> None:
    clear_screen()
    draw_header("OPTION C - Remove animal  →  delete(data)")

    if animals.is_empty():
        failure("The list is empty - there is nothing to remove.")
        pause()
        return

    animals.print_table()

    print(paint("\n   Any animal can be removed, not just the ends.", Color.GREY))
    animal = ask_text("Animal to remove")

    target = animals.find(animal)

    if target is None:
        failure("'" + animal + "' was NOT FOUND in the list.")
        print(paint("   delete() returned False - nothing was changed.", Color.GREY))
        print(paint("   Check the spelling against the table above.", Color.GREY))
        pause()
        return

    # Describe the neighbours before the unlink, so the reconnection is visible.
    position = animals.position_of(target)

    if target.prev is None:
        before = "· nothing ·"
    else:
        before = target.prev.data

    if target.next is None:
        after = "· nothing ·"
    else:
        after = target.next.data

    print(paint("\n   Found '" + target.data + "' at position "
                + str(position) + " of " + str(animals.size) + ".",
                Color.BOLD + Color.GREEN))
    print(paint("   Currently linked:  " + before + "  ◀-▶  " + target.data
                + "  ◀-▶  " + after, Color.CYAN))
    print()

    if not confirm("Remove '" + target.data + "' from the list?"):
        failure("Cancelled. The animal stays in the list.")
        pause()
        return

    removed_name = target.data
    was_removed = animals.delete(removed_name)

    if not was_removed:
        failure("Nothing was removed.")
        pause()
        return

    success("delete('" + removed_name + "') returned True - animal removed.")
    print(paint("   Now linked:  " + before + "  ◀-▶  " + after, Color.CYAN))
    print(paint("   Animals left: " + str(animals.size), Color.GREY))

    animals.print_both()
    pause()


# Option D - prints the list from head to tail.
def option_print_forward(animals: "AnimalList") -> None:
    clear_screen()
    draw_header("OPTION D - Print list forward  →  print_forward()")

    print(paint("\n   Walking '.next' from the head:", Color.BOLD + Color.GREEN))
    print()
    animals.print_forward()

    animals.print_table()
    pause()


# Option E - prints the list from tail to head.
def option_print_backward(animals: "AnimalList") -> None:
    clear_screen()
    draw_header("OPTION E - Print list backward  →  print_backward()")

    print(paint("\n   Walking '.prev' from the tail:", Color.BOLD + Color.PINK))
    print()
    animals.print_backward()

    print(paint("\n   This is only possible because every node stores a backward "
                "reference.", Color.DIM + Color.GREY))

    animals.print_table()
    pause()


# ---------------------------------------------------------------------------
# GOODBYE SCREEN
# ---------------------------------------------------------------------------

# Prints the session timer and signs off.
def goodbye(animals: "AnimalList", started_at: float) -> None:
    elapsed = int(time.time() - started_at)
    minutes = elapsed // 60
    seconds = elapsed % 60

    clear_screen()
    width = 74
    print()
    print(paint("   ╔" + "═" * width + "╗", rainbow(3)))
    print(paint("   ║" + "SESSION CLOSED".center(width) + "║", Color.BOLD + Color.GREEN))
    print(paint("   ╟" + "─" * width + "╢", rainbow(3)))

    if animals is None:
        summary = "No list was loaded this session."
    else:
        summary = "The zoo ended with " + str(animals.size) + " animal(s) in the list."

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
    animals = None
    message = ""

    while True:
        clear_screen()
        draw_header("")
        draw_menu(animals)

        if message != "":
            print(paint("   " + message, Color.RED))
            message = ""

        choice = input(paint("\n   Select an option: ",
                             Color.BOLD + Color.CYAN)).strip().upper()

        if choice == "F":
            break

        if choice == "A":
            animals = option_load_csv(animals)
            continue

        if choice == "B" or choice == "C" or choice == "D" or choice == "E":
            if animals is None:
                message = "✖ Load the CSV file first (option A)."
                continue

            if choice == "B":
                option_add_animal(animals)
            elif choice == "C":
                option_remove_animal(animals)
            elif choice == "D":
                option_print_forward(animals)
            else:
                option_print_backward(animals)
            continue

        message = "✖ '" + choice + "' is not a valid option."

    goodbye(animals, started_at)

#
#
# MAIN PROGRAM
#
#


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(paint("\n\n   Interrupted. Closing THE ZOO.\n", Color.RED))