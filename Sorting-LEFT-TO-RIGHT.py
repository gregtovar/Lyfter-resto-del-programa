"""BUBBLE SORT - Watch the algorithm work - Version 1.0

LEFT TO RIGHT

"""

import os
import random
import time

#
# Color Management
#

class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    REVERSE = "\033[7m"

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


# Limits for the size of the array.
MIN_ELEMENTS = 10
MAX_ELEMENTS = 100

# Range the random values are drawn from.
MIN_VALUE = 1
MAX_VALUE = 999


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


# Clears the terminal screen.
def clear_screen() -> None:
    print("\033[2J\033[H", end="")


# Moves the cursor to the top left without wiping the screen, so an animated
# frame overwrites the previous one instead of making the whole screen blink.
def cursor_home() -> None:
    print("\033[H", end="")


# Waits for the user before redrawing the screen.
def pause() -> None:
    input(paint("\n   Press ENTER to continue... ", Color.GREY))


# Returns the block character that represents a value on an eight step scale.
def block_for(value: int, highest: int) -> str:
    if highest <= 0:
        return "▁"

    level = (value * 8) // highest
    if level < 1:
        level = 1
    if level > 8:
        level = 8

    if level == 1:
        return "▁"
    if level == 2:
        return "▂"
    if level == 3:
        return "▃"
    if level == 4:
        return "▄"
    if level == 5:
        return "▅"
    if level == 6:
        return "▆"
    if level == 7:
        return "▇"
    return "█"


# ---------------------------------------------------------------------------
# The Node. One number = one node.
# ---------------------------------------------------------------------------
class NumberNode:

    # Builds a single node holding one integer.
    # '.prev' exists so a pass can walk from the tail back toward the head.
    def __init__(self, value: int) -> None:
        self.value = value
        self.prev = None
        self.next = None


# ---------------------------------------------------------------------------
# The Array. A chain of NumberNode, with the capacity chosen by the user.
# ---------------------------------------------------------------------------
class NumberArray:

    # Sets up an empty array with a fixed capacity.
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.head = None
        self.tail = None
        self.size = 0
        self.is_sorted = False

        # Statistics from the most recent run of the algorithm.
        self.passes = 0
        self.comparisons = 0
        self.swaps = 0
        self.seconds = 0.0

    # True when no numbers have been generated yet.
    def is_empty(self) -> bool:
        return self.head is None

    # Adds one value at the end of the chain, linking it in both directions.
    def append(self, value: int) -> None:
        node = NumberNode(value)
        node.prev = self.tail

        if self.tail is None:
            self.head = node
        else:
            self.tail.next = node

        self.tail = node
        self.size = self.size + 1

    # Throws away every node so the array can be filled again.
    def clear(self) -> None:
        self.head = None
        self.tail = None
        self.size = 0
        self.is_sorted = False
        self.passes = 0
        self.comparisons = 0
        self.swaps = 0
        self.seconds = 0.0

    # Fills the array with random values up to its capacity.
    def generate(self) -> None:
        self.clear()
        count = 0
        while count < self.capacity:
            self.append(random.randint(MIN_VALUE, MAX_VALUE))
            count = count + 1

    # Largest value currently stored, used to scale the bar chart.
    def highest(self) -> int:
        best = 0
        walker = self.head
        while walker is not None:
            if walker.value > best:
                best = walker.value
            walker = walker.next
        return best

    # Smallest value currently stored.
    def lowest(self) -> int:
        best = -1
        walker = self.head
        while walker is not None:
            if best < 0 or walker.value < best:
                best = walker.value
            walker = walker.next
        return best

    # Sum of every value, used for the average.
    def total(self) -> int:
        running = 0
        walker = self.head
        while walker is not None:
            running = running + walker.value
            walker = walker.next
        return running

    # True when every value is less than or equal to the one after it.
    def check_ordered(self) -> bool:
        walker = self.head
        while walker is not None and walker.next is not None:
            if walker.value > walker.next.value:
                return False
            walker = walker.next
        return True

    # -----------------------------------------------------------------
    # RENDERING
    # -----------------------------------------------------------------


    def draw_chart(self, left: int, right: int, locked_upto: int) -> None:
        highest = self.highest()
        row_width = 74

        line = "   "
        drawn = 0
        walker = self.head
        index = 0

        while walker is not None:
            block = block_for(walker.value, highest)

            if index == left or index == right:
                line = line + paint(block, Color.BOLD + Color.RED)
            elif index < locked_upto:
                line = line + paint(block, Color.GREEN)
            else:
                line = line + paint(block, Color.CYAN)

            walker = walker.next
            index = index + 1
            drawn = drawn + 1

            if drawn % row_width == 0:
                print(line + "\033[K")
                line = "   "

        if drawn % row_width != 0:
            print(line + "\033[K")

    # Draws the numbers themselves in a grid, ten per row.
    def draw_grid(self, left: int, right: int, locked_upto: int) -> None:
        walker = self.head
        index = 0
        line = "   "

        while walker is not None:
            text = str(walker.value).rjust(4)

            if index == left or index == right:
                cell = paint(text, Color.BOLD + Color.RED + Color.REVERSE)
            elif index < locked_upto:
                cell = paint(text, Color.GREEN)
            else:
                cell = paint(text, Color.WHITE)

            line = line + cell + "  "
            index = index + 1

            if index % 10 == 0:
                print(line + "\033[K")
                line = "   "

            walker = walker.next

        if line.strip() != "":
            print(line + "\033[K")

    # One full frame of the animation: stats, chart, then the grid.
    def draw_frame(self, left: int, right: int, locked_upto: int,
                   heading: str) -> None:
        cursor_home()
        draw_header("")

        print(paint("   " + heading, Color.BOLD + Color.YELLOW) + "\033[K")
        print(paint("   pass " + str(self.passes)
                    + "   ·   comparisons " + str(self.comparisons)
                    + "   ·   swaps " + str(self.swaps), Color.GREY) + "\033[K")
        print("\033[K")

        self.draw_chart(left, right, locked_upto)
        print("\033[K")
        self.draw_grid(left, right, locked_upto)

        print("\033[K")
        print(paint("   red = being swapped   ·   green = settled at the front   "
                    "·   cyan = still unsorted", Color.DIM + Color.GREY) + "\033[K")

        # Wipe anything left over from a taller previous frame.
        print("\033[J", end="")

    # Prints the array as a plain grid with no highlighting.
    def display(self) -> None:
        if self.is_empty():
            print(paint("\n   The array is empty - generate the numbers first.",
                        Color.YELLOW))
            return

        print(paint("\n   Values in current order:", Color.BOLD + Color.WHITE))
        print()
        self.draw_chart(-1, -1, 0)
        print()
        self.draw_grid(-1, -1, 0)

    # Prints the min, max, sum and average.
    def print_stats(self) -> None:
        if self.is_empty():
            return

        average = self.total() / self.size

        print(paint("\n   elements " + str(self.size)
                    + "   ·   lowest " + str(self.lowest())
                    + "   ·   highest " + str(self.highest())
                    + "   ·   sum " + str(self.total())
                    + "   ·   average " + str(round(average, 2)), Color.CYAN))

    # -----------------------------------------------------------------
    # THE ALGORITHM
    # -----------------------------------------------------------------


    def bubble_sort(self, delay: float) -> bool:
        self.passes = 0
        self.comparisons = 0
        self.swaps = 0

        started = time.time()
        locked = 0
        swapped_any = True
        completed = True

        clear_screen()

        try:

            while swapped_any:
                swapped_any = False
                self.passes = self.passes + 1

                walker = self.tail
                index = self.size - 1

                # Stop once the walk reaches the settled block at the front.
                while index > locked:
                    self.comparisons = self.comparisons + 1

                    if walker.prev.value > walker.value:
                        # Swap the two VALUES. A temporary variable is used
                        # because the usual 'a, b = b, a' shortcut builds a
                        # tuple, which is not allowed here.
                        temp = walker.prev.value
                        walker.prev.value = walker.value
                        walker.value = temp

                        self.swaps = self.swaps + 1
                        swapped_any = True

                        if delay > 0:
                            self.draw_frame(index - 1, index, locked,
                                            "SWAPPING position " + str(index)
                                            + " with position " + str(index + 1))
                            time.sleep(delay)

                    walker = walker.prev
                    index = index - 1

                locked = locked + 1

                if delay == 0:
                    self.draw_frame(-1, -1, locked,
                                    "PASS " + str(self.passes) + " complete")

                # Refinement 2: a clean pass means the data is already ordered.
                if not swapped_any:
                    break

        except KeyboardInterrupt:
            completed = False

        self.seconds = time.time() - started

        if completed:
            self.is_sorted = True

        return completed



# Draws the rainbow header with the app title.
def draw_header(subtitle: str) -> None:
    width = 74
    print("\033[K")
    print(paint("   ╔" + "═" * width + "╗", rainbow(0)) + "\033[K")

    art_1 = "██████  ██    ██ ██████  ██████  ██      ███████"
    art_2 = "██   ██ ██    ██ ██   ██ ██   ██ ██      ██     "
    art_3 = "██████  ██    ██ ██████  ██████  ██      █████  "
    art_4 = "██   ██ ██    ██ ██   ██ ██   ██ ██      ██     "
    art_5 = "██████   ██████  ██████  ██████  ███████ ███████"

    print(paint("   ║" + art_1.center(width) + "║", rainbow(1)) + "\033[K")
    print(paint("   ║" + art_2.center(width) + "║", rainbow(2)) + "\033[K")
    print(paint("   ║" + art_3.center(width) + "║", rainbow(3)) + "\033[K")
    print(paint("   ║" + art_4.center(width) + "║", rainbow(4)) + "\033[K")
    print(paint("   ║" + art_5.center(width) + "║", rainbow(5)) + "\033[K")
    print(paint("   ║" + " " * width + "║", rainbow(6)) + "\033[K")
    print(paint("   ║" + "▁▂▃▄▅▆▇█   S O R T   █▇▆▅▄▃▂▁".center(width) + "║",
                Color.BOLD + Color.WHITE) + "\033[K")
    print(paint("   ╟" + "─" * width + "╢", Color.PURPLE) + "\033[K")
    print(paint("   ║" + "Watch the algorithm work  ·  Version 1.0".center(width) + "║",
                Color.CYAN) + "\033[K")
    print(paint("   ║" + "Developed by Greg Tovar".center(width) + "║",
                Color.DIM + Color.GREY) + "\033[K")
    print(paint("   ╚" + "═" * width + "╝", rainbow(0)) + "\033[K")

    if subtitle != "":
        print(paint("   ▸ " + subtitle, Color.BOLD + Color.YELLOW) + "\033[K")


# Prints one menu entry.
def draw_option(number: str, text: str, enabled: bool, note: str) -> None:
    if enabled:
        tag = paint("   [" + number + "] ", Color.BOLD + Color.GREEN)
        body = paint(text, Color.WHITE)
    else:
        tag = paint("   [" + number + "] ", Color.DIM + Color.GREY)
        body = paint(text + "  " + note, Color.DIM + Color.GREY)
    print(tag + body)


# Draws the main menu, dimming what is not available yet.
def draw_menu(array: "NumberArray") -> None:
    ready = array is not None
    filled = ready and not array.is_empty()

    if not ready:
        print(paint("\n   No array yet - start with option 1.", Color.ORANGE))
    elif not filled:
        print(paint("\n   Array set up for " + str(array.capacity)
                    + " elements   |   empty - generate the numbers with option 2.",
                    Color.ORANGE))
    else:
        state = "UNSORTED"
        shade = Color.ORANGE
        if array.is_sorted:
            state = "SORTED"
            shade = Color.GREEN
        print(paint("\n   Array of " + str(array.size) + " elements   |   ", Color.GREEN)
              + paint(state, Color.BOLD + shade))

    print(paint("\n   ─── MENU " + "─" * 65, Color.PURPLE))
    draw_option("1", "Setup Array of Elements", True, "")
    draw_option("2", "Generate Numbers", ready, "(needs option 1)")
    draw_option("3", "Display Array", filled, "(needs option 2)")
    draw_option("4", "Execute Bubble Sort Algorithm", filled, "(needs option 2)")
    print(paint("   [0] ", Color.BOLD + Color.RED) + paint("Exit", Color.WHITE))
    print(paint("   " + "─" * 74, Color.PURPLE))



# Asks a yes/no question and keeps asking until the answer is clear.
def confirm(question: str) -> bool:
    while True:
        answer = input(paint("   " + question + " (y/n): ", Color.YELLOW)).strip().lower()
        if answer == "y" or answer == "yes":
            return True
        if answer == "n" or answer == "no":
            return False
        print(paint("   Please answer with y or n.", Color.RED))


# Asks for a whole number inside a range, refusing anything else.
def ask_number(label: str, lowest: int, highest: int) -> int:
    while True:
        value = input(paint("   " + label + ": ", Color.CYAN)).strip()

        if value == "":
            print(paint("   Please type a number.", Color.RED))
            continue

        # A leading minus is allowed so a negative answer gets the range
        # message rather than the digits message.
        body = value
        if body[0] == "-" or body[0] == "+":
            body = body[1:]

        if not body.isdigit():
            print(paint("   '" + value + "' is not a whole number.", Color.RED))
            continue

        number = int(value)
        if number < lowest or number > highest:
            print(paint("   Enter a number between " + str(lowest)
                        + " and " + str(highest) + ".", Color.RED))
            continue

        return number


# Prints a green success line.
def success(message: str) -> None:
    print(paint("\n   ✔ " + message, Color.BOLD + Color.GREEN))


# Prints a red failure line.
def failure(message: str) -> None:
    print(paint("\n   ✖ " + message, Color.BOLD + Color.RED))


# ---------------------------------------------------------------------------
# MENU ACTIONS
# ---------------------------------------------------------------------------

# Option 1 - asks how many elements the array should hold.
def option_setup(array: "NumberArray") -> "NumberArray":
    clear_screen()
    draw_header("OPTION 1 - Setup Array of Elements")

    if array is not None:
        print(paint("\n   An array is already set up for " + str(array.capacity)
                    + " elements.", Color.ORANGE))
        if not confirm("Set up a new one? The current numbers are discarded."):
            failure("Cancelled. The current array is untouched.")
            pause()
            return array

    print(paint("\n   How many elements should the array hold?", Color.GREY))
    print(paint("   Minimum " + str(MIN_ELEMENTS)
                + ", maximum " + str(MAX_ELEMENTS) + ".", Color.GREY))

    capacity = ask_number("Number of elements", MIN_ELEMENTS, MAX_ELEMENTS)
    fresh = NumberArray(capacity)

    success("Array set up for " + str(capacity) + " elements.")
    print(paint("   It is still empty - use option 2 to fill it with numbers.",
                Color.GREY))
    pause()
    return fresh


# Option 2 - fills the array with random numbers.
def option_generate(array: "NumberArray") -> None:
    clear_screen()
    draw_header("OPTION 2 - Generate Numbers")

    if not array.is_empty():
        print(paint("\n   The array already holds " + str(array.size)
                    + " number(s).", Color.ORANGE))
        if not confirm("Replace them with a fresh set?"):
            failure("Cancelled. The current numbers are untouched.")
            pause()
            return

    array.generate()

    success(str(array.size) + " random number(s) generated.")
    print(paint("   Each value is between " + str(MIN_VALUE)
                + " and " + str(MAX_VALUE) + ".", Color.GREY))

    if array.check_ordered():
        print(paint("   By pure chance these came out already in order.",
                    Color.YELLOW))

    array.display()
    array.print_stats()
    pause()


# Option 3 - shows the array as it currently stands.
def option_display(array: "NumberArray") -> None:
    clear_screen()
    draw_header("OPTION 3 - Display Array")

    if array.is_sorted:
        print(paint("\n   This array has been sorted.", Color.GREEN))
    else:
        print(paint("\n   This array has NOT been sorted yet.", Color.ORANGE))

    array.display()
    array.print_stats()
    pause()


# Option 4 - runs the algorithm with a live animation.
def option_sort(array: "NumberArray") -> None:
    clear_screen()
    draw_header("OPTION 4 - Execute Bubble Sort Algorithm")

    if array.is_sorted:
        print(paint("\n   This array is already sorted.", Color.ORANGE))
        print(paint("   Running again is still interesting: bubble sort needs "
                    "one clean pass to prove it.", Color.GREY))
        if not confirm("Run it anyway?"):
            failure("Cancelled.")
            pause()
            return

    print(paint("\n   How fast should the animation run?", Color.GREY))
    print(paint("   [1] Slow      0.20s per swap - good for explaining", Color.WHITE))
    print(paint("   [2] Normal    0.06s per swap", Color.WHITE))
    print(paint("   [3] Fast      0.01s per swap", Color.WHITE))
    print(paint("   [4] Instant   draw once per pass, no delay", Color.WHITE))

    speed = ask_number("Speed", 1, 4)

    if speed == 1:
        delay = 0.20
    elif speed == 2:
        delay = 0.06
    elif speed == 3:
        delay = 0.01
    else:
        delay = 0.0

    # Warn when the chosen combination would take a long time. The average
    # number of swaps for random data is about a quarter of n squared.
    if delay > 0:
        estimate = int((array.size * array.size) / 4 * delay)
        if estimate > 45:
            print(paint("\n   Heads up: " + str(array.size) + " elements at this "
                        "speed could take around " + str(estimate)
                        + " seconds.", Color.ORANGE))
            print(paint("   Ctrl+C stops the animation at any time.", Color.GREY))
            if not confirm("Continue anyway?"):
                failure("Cancelled. Try a faster speed.")
                pause()
                return

    print(paint("\n   Starting... Ctrl+C interrupts.", Color.GREY))
    time.sleep(0.6)

    completed = array.bubble_sort(delay)

    clear_screen()
    draw_header("OPTION 4 - Execute Bubble Sort Algorithm")

    if not completed:
        failure("Interrupted before finishing - the array is partly sorted.")
        array.display()
        array.print_stats()
        pause()
        return

    print(paint("\n   ╔" + "═" * 74 + "╗", Color.GREEN))
    print(paint("   ║" + "SORT COMPLETE".center(74) + "║", Color.BOLD + Color.GREEN))
    print(paint("   ╚" + "═" * 74 + "╝", Color.GREEN))

    print(paint("\n   passes       " + str(array.passes), Color.WHITE))
    print(paint("   comparisons  " + str(array.comparisons), Color.WHITE))
    print(paint("   swaps        " + str(array.swaps), Color.WHITE))
    print(paint("   time         " + str(round(array.seconds, 3)) + "s", Color.WHITE))

    # The theoretical worst case, for comparison against what actually ran.
    worst = (array.size * (array.size - 1)) // 2
    print(paint("   worst case   " + str(worst)
                + " comparisons for " + str(array.size) + " elements",
                Color.DIM + Color.GREY))

    print(paint("\n   Final sorted array:", Color.BOLD + Color.GREEN))
    print()
    array.draw_chart(-1, -1, array.size)
    print()
    array.draw_grid(-1, -1, array.size)

    array.print_stats()

    # Prove the result rather than just claiming it.
    if array.check_ordered():
        print(paint("\n   Verified: every value is less than or equal to the next.",
                    Color.BOLD + Color.GREEN))
        print(paint("   Lowest value  " + str(array.head.value)
                    + "   ·   Highest value " + str(array.tail.value), Color.GREEN))
    else:
        failure("Verification FAILED - the array is not in order.")

    pause()



# Prints the session timer and signs off.
def goodbye(array: "NumberArray", started_at: float) -> None:
    elapsed = int(time.time() - started_at)
    minutes = elapsed // 60
    seconds = elapsed % 60

    clear_screen()
    width = 74
    print()
    print(paint("   ╔" + "═" * width + "╗", rainbow(3)))
    print(paint("   ║" + "SESSION CLOSED".center(width) + "║", Color.BOLD + Color.GREEN))
    print(paint("   ╟" + "─" * width + "╢", rainbow(3)))

    if array is None:
        summary = "No array was set up this session."
    elif array.is_empty():
        summary = "Array set up for " + str(array.capacity) + " elements, never filled."
    elif array.is_sorted:
        summary = ("Sorted " + str(array.size) + " elements in "
                   + str(array.swaps) + " swaps.")
    else:
        summary = str(array.size) + " elements generated, left unsorted."

    timer = "Session time: " + str(minutes) + "m " + str(seconds) + "s"
    print(paint("   ║" + summary.center(width) + "║", Color.WHITE))
    print(paint("   ║" + timer.center(width) + "║", Color.CYAN))
    print(paint("   ║" + " " * width + "║", rainbow(3)))
    print(paint("   ║" + "Thanks for using BUBBLE SORT v1.0".center(width) + "║",
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
    array = None
    message = ""

    while True:
        clear_screen()
        draw_header("")
        draw_menu(array)

        if message != "":
            print(paint("   " + message, Color.RED))
            message = ""

        choice = input(paint("\n   Select an option: ", Color.BOLD + Color.CYAN)).strip()

        if choice == "0":
            break

        if choice == "1":
            array = option_setup(array)
            continue

        if choice == "2" or choice == "3" or choice == "4":
            if array is None:
                message = "✖ Set up the array first (option 1)."
                continue

            if choice == "2":
                option_generate(array)
                continue

            if array.is_empty():
                message = "✖ Generate the numbers first (option 2)."
                continue

            if choice == "3":
                option_display(array)
            else:
                option_sort(array)
            continue

        message = "✖ '" + choice + "' is not a valid option."

    goodbye(array, started_at)


#
#
# Main Program
#
#

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(paint("\n\n   Interrupted. Closing BUBBLE SORT.\n", Color.RED))