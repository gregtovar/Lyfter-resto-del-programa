"""BINARY TREE - Car dealership parking lot - Version 1.0

"""

import os
import time
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CSV = "car_binary_tree.csv"


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


# Returns the color used for a given depth of the tree.
def depth_color(depth: int) -> str:
    if depth == 0:
        return Color.BOLD + Color.WHITE
    if depth == 1:
        return Color.BOLD + Color.CYAN
    if depth == 2:
        return Color.GREEN
    if depth == 3:
        return Color.YELLOW
    if depth == 4:
        return Color.ORANGE
    return Color.PINK


# Paints a piece of text and closes the escape sequence.
def paint(text: str, color: str) -> str:
    return color + text + Color.RESET


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
# The Node. One category = one node, with at most two children.
#
#. To be binary - can only have 2 children - no more
# ---------------------------------------------------------------------------
class TreeNode:

    # Builds a single detached node.
    def __init__(self, node_id: str, value: str, parent_id: str,
                 branch: str, path: str) -> None:
        self.node_id = node_id
        self.value = value
        self.parent_id = parent_id
        self.branch = branch
        self.path = path
        self.left = None
        self.right = None

    # Label used by every renderer.
    def label(self) -> str:
        return self.value

    # True when the node has no children at all.
    def is_leaf(self) -> bool:
        return self.left is None and self.right is None


# ---------------------------------------------------------------------------
# A one-way chain used only while loading, so rows can be wired in any order.
# This is the stand-in for the list a normal loader would use.
# ---------------------------------------------------------------------------
class NodeLink:

    # Wraps one TreeNode so it can sit in the temporary chain.
    def __init__(self, node: "TreeNode") -> None:
        self.node = node
        self.next = None


# ---------------------------------------------------------------------------
# The Binary Tree itself.
# ---------------------------------------------------------------------------
class CarTree:

    # Initializes an empty structure under a chosen name.
    def __init__(self, name: str) -> None:
        self.name = name
        self.root = None
        self.size = 0
        self.source_path = ""
        self.created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # True when no nodes have been loaded.
    def is_empty(self) -> bool:
        return self.root is None

    # Finds a node by its ID, searching the whole tree. Returns None if absent.
    def find(self, node_id: str) -> "TreeNode":
        return self.find_from(self.root, node_id)

    # Recursive helper for find().
    def find_from(self, node: "TreeNode", node_id: str) -> "TreeNode":
        if node is None:
            return None
        if node.node_id == node_id:
            return node

        hit = self.find_from(node.left, node_id)
        if hit is not None:
            return hit
        return self.find_from(node.right, node_id)

    # Longest chain of nodes from the root down to a leaf.
    def height(self) -> int:
        return self.height_from(self.root)

    # Recursive helper for height().
    def height_from(self, node: "TreeNode") -> int:
        if node is None:
            return 0
        left_height = self.height_from(node.left)
        right_height = self.height_from(node.right)
        if left_height > right_height:
            return left_height + 1
        return right_height + 1

    # Counts nodes that have no children.
    def count_leaves(self) -> int:
        return self.count_leaves_from(self.root)

    # Recursive helper for count_leaves().
    def count_leaves_from(self, node: "TreeNode") -> int:
        if node is None:
            return 0
        if node.is_leaf():
            return 1
        return (self.count_leaves_from(node.left)
                + self.count_leaves_from(node.right))

    # Counts nodes sitting at one exact depth (root is depth 0).
    def count_at_depth(self, node: "TreeNode", depth: int, wanted: int) -> int:
        if node is None:
            return 0
        if depth == wanted:
            return 1
        return (self.count_at_depth(node.left, depth + 1, wanted)
                + self.count_at_depth(node.right, depth + 1, wanted))

    # True when every level is completely filled.
    def is_perfect(self) -> bool:
        if self.root is None:
            return False
        expected = (2 ** self.height()) - 1
        return expected == self.size

 
    def print_rotated(self) -> None:
        print(paint("\n   ROTATED VIEW - root on the left, branches growing right",
                    Color.BOLD + Color.CYAN))
        print(paint("   Nodes above a parent are its RIGHT child, "
                    "nodes below are its LEFT child.", Color.GREY))
        print()
        self.draw_rotated(self.root, "", 0, 0)

    # Recursive helper. branch: 0 = root, 1 = right child, 2 = left child.
    def draw_rotated(self, node: "TreeNode", prefix: str,
                     branch: int, depth: int) -> None:
        if node is None:
            return

        # The right child is drawn ABOVE this node, so it is visited first.
        if node.right is not None:
            if branch == 2:
                child_prefix = prefix + "│   "
            else:
                child_prefix = prefix + "    "
            self.draw_rotated(node.right, child_prefix, 1, depth + 1)

        if branch == 0:
            connector = ""
        elif branch == 1:
            connector = "┌── "
        else:
            connector = "└── "

        tag = paint(" (" + node.node_id + ")", Color.DIM + Color.GREY)
        print("   " + paint(prefix + connector, Color.GREY)
              + paint(node.label(), depth_color(depth)) + tag)

        if node.left is not None:
            if branch == 1:
                child_prefix = prefix + "│   "
            else:
                child_prefix = prefix + "    "
            self.draw_rotated(node.left, child_prefix, 2, depth + 1)

   
    def print_branches(self) -> None:
        print(paint("\n   BRANCH VIEW - indented outline, left child listed first",
                    Color.BOLD + Color.CYAN))
        print()
        print("   " + paint(self.root.label(), depth_color(0))
              + paint(" (" + self.root.node_id + ")", Color.DIM + Color.GREY))
        self.draw_branches(self.root, "", 1)

    # Recursive helper that draws the children of one node.
    def draw_branches(self, node: "TreeNode", prefix: str, depth: int) -> None:
        if node.left is not None:
            last_one = node.right is None
            self.draw_branch_line(node.left, prefix, last_one, depth, "L")
        if node.right is not None:
            self.draw_branch_line(node.right, prefix, True, depth, "R")

    # Draws one child line and then recurses into that child.
    def draw_branch_line(self, node: "TreeNode", prefix: str,
                         last_one: bool, depth: int, side: str) -> None:
        if last_one:
            connector = "└── "
            extension = "    "
        else:
            connector = "├── "
            extension = "│   "

        if side == "L":
            marker = paint("L", Color.BLUE)
        else:
            marker = paint("R", Color.PINK)

        print("   " + paint(prefix + connector, Color.GREY)
              + marker + " "
              + paint(node.label(), depth_color(depth))
              + paint(" (" + node.node_id + ")", Color.DIM + Color.GREY))

        self.draw_branches(node, prefix + extension, depth + 1)

    # -----------------------------------------------------------------
    # RENDERER 3 - one line per level, so the shape of each generation is
    # obvious at a glance.
    # -----------------------------------------------------------------
    def print_levels(self) -> None:
        print(paint("\n   LEVEL VIEW - every generation on its own line",
                    Color.BOLD + Color.CYAN))
        print()

        total_height = self.height()
        depth = 0
        while depth < total_height:
            count = self.count_at_depth(self.root, 0, depth)
            heading = ("   Level " + str(depth) + "  ("
                       + str(count) + " node" + ("s" if count != 1 else "") + ")")
            print(paint(heading, Color.BOLD + Color.WHITE))
            text = self.level_text(self.root, 0, depth)
            self.wrap_print(text, depth_color(depth))
            depth = depth + 1

    # Builds one level's line by walking the tree and keeping only that depth.
    def level_text(self, node: "TreeNode", depth: int, wanted: int) -> str:
        if node is None:
            return ""
        if depth == wanted:
            return node.label()

        left_text = self.level_text(node.left, depth + 1, wanted)
        right_text = self.level_text(node.right, depth + 1, wanted)

        if left_text == "":
            return right_text
        if right_text == "":
            return left_text
        return left_text + "  ·  " + right_text


    def print_traversals(self) -> None:
        print(paint("\n   TRAVERSAL VIEW - the same tree read three ways",
                    Color.BOLD + Color.CYAN))
        print()

        print(paint("   PRE-ORDER   node → left → right", Color.BOLD + Color.GREEN))
        print(paint("   (top down: a parent is always named before its children)",
                    Color.DIM + Color.GREY))
        self.wrap_print(self.preorder(self.root), Color.GREEN)

        print(paint("\n   IN-ORDER    left → node → right", Color.BOLD + Color.YELLOW))
        print(paint("   (left to right: matches the rotated view read top to bottom)",
                    Color.DIM + Color.GREY))
        self.wrap_print(self.inorder(self.root), Color.YELLOW)

        print(paint("\n   POST-ORDER  left → right → node", Color.BOLD + Color.PINK))
        print(paint("   (bottom up: every child is named before its parent)",
                    Color.DIM + Color.GREY))
        self.wrap_print(self.postorder(self.root), Color.PINK)

    # Prints a long line of values wrapped to fit a normal terminal.
    # Breaks are only allowed at a separator, never inside a value, so a name
    # like "Sport Touring" is never cut in half.
    #
    #

    def wrap_print(self, text: str, color: str) -> None:
        line = ""
        index = 0
        length = len(text)

        while index < length:
            char = text[index]

            if len(line) >= 58 and (char == "·" or char == "→"):
                # The separator stays at the end of the line so it is obvious
                # the sequence continues on the next one.
                print("   " + paint("  " + line.strip() + " " + char, color))
                line = ""
                index = index + 1

                # Swallow the padding that followed the separator.
                while index < length and text[index] == " ":
                    index = index + 1
                continue

            line = line + char
            index = index + 1

        if line.strip() != "":
            print("   " + paint("  " + line.strip(), color))

    # Node, then left subtree, then right subtree.
    def preorder(self, node: "TreeNode") -> str:
        if node is None:
            return ""
        text = node.label()
        left_text = self.preorder(node.left)
        right_text = self.preorder(node.right)
        if left_text != "":
            text = text + " → " + left_text
        if right_text != "":
            text = text + " → " + right_text
        return text

    # Left subtree, then node, then right subtree.
    def inorder(self, node: "TreeNode") -> str:
        if node is None:
            return ""
        text = self.inorder(node.left)
        if text != "":
            text = text + " → "
        text = text + node.label()
        right_text = self.inorder(node.right)
        if right_text != "":
            text = text + " → " + right_text
        return text

    # Left subtree, then right subtree, then node.
    def postorder(self, node: "TreeNode") -> str:
        if node is None:
            return ""
        text = self.postorder(node.left)
        right_text = self.postorder(node.right)
        if right_text != "":
            if text != "":
                text = text + " → "
            text = text + right_text
        if text != "":
            text = text + " → "
        return text + node.label()

    # -----------------------------------------------------------------
    # Statistics panel shared by every view.
    # -----------------------------------------------------------------
    def print_summary(self) -> None:
        print(paint("\n   TREE: " + self.name, Color.BOLD + Color.CYAN))
        print(paint("   created " + self.created
                    + "   |   nodes: " + str(self.size)
                    + "   |   levels: " + str(self.height())
                    + "   |   leaves: " + str(self.count_leaves()), Color.GREY))

        if self.is_perfect():
            print(paint("   Shape: PERFECT - every level is completely filled.",
                        Color.GREEN))
        else:
            print(paint("   Shape: not perfect - at least one level has a gap.",
                        Color.ORANGE))


# ---------------------------------------------------------------------------
# BANNER + MENU DRAWING
# ---------------------------------------------------------------------------

# Draws the rainbow header with the app title.
def draw_header(subtitle: str) -> None:
    width = 74
    print()
    print(paint("   ╔" + "═" * width + "╗", rainbow(0)))

    art_1 = "██████  ███████ ██   ██  █████  ██████  ██   ██"
    art_2 = "██   ██    ██   ███  ██ ██   ██ ██   ██  ██ ██ "
    art_3 = "██████     ██   ██ █ ██ ███████ ██████    ███  "
    art_4 = "██   ██    ██   ██  ███ ██   ██ ██  ██     ██  "
    art_5 = "██████  ███████ ██   ██ ██   ██ ██   ██    ██  "

    print(paint("   ║" + art_1.center(width) + "║", rainbow(1)))
    print(paint("   ║" + art_2.center(width) + "║", rainbow(2)))
    print(paint("   ║" + art_3.center(width) + "║", rainbow(3)))
    print(paint("   ║" + art_4.center(width) + "║", rainbow(4)))
    print(paint("   ║" + art_5.center(width) + "║", rainbow(5)))
    print(paint("   ║" + " " * width + "║", rainbow(6)))
    print(paint("   ║" + "┌─ T R E E ─┐".center(width) + "║", Color.BOLD + Color.WHITE))
    print(paint("   ╟" + "─" * width + "╢", Color.PURPLE))
    print(paint("   ║" + "Car dealership parking lot  ·  Version 1.0".center(width) + "║",
                Color.CYAN))
    print(paint("   ║" + "Developed by Greg Tovar".center(width) + "║", Color.DIM + Color.GREY))
    print(paint("   ╚" + "═" * width + "╝", rainbow(0)))

    if subtitle != "":
        print(paint("   ▸ " + subtitle, Color.BOLD + Color.YELLOW))


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
def draw_menu(tree: "CarTree") -> None:
    ready = tree is not None
    loaded = ready and not tree.is_empty()

    if ready:
        if loaded:
            status = ("Active tree: " + tree.name
                      + "   |   nodes: " + str(tree.size)
                      + "   |   levels: " + str(tree.height()))
            print(paint("\n   " + status, Color.GREEN))
        else:
            status = "Active tree: " + tree.name + "   |   empty - load a CSV with option 2"
            print(paint("\n   " + status, Color.ORANGE))
    else:
        print(paint("\n   No tree initialized yet - start with option 1.", Color.ORANGE))

    print(paint("\n   ─── MENU " + "─" * 65, Color.PURPLE))
    draw_option("1", "Initialize the binary tree", True, "")
    draw_option("2", "Upload existing CSV file", ready, "(needs option 1)")
    draw_option("3", "List the binary tree", loaded, "(needs option 2)")
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


# Finds a node inside the temporary loading chain by its ID.
def find_in_chain(head: "NodeLink", node_id: str) -> "TreeNode":
    walker = head
    while walker is not None:
        if walker.node.node_id == node_id:
            return walker.node
        walker = walker.next
    return None


# Option 1 - creates the structure and gives it a name.
def option_initialize(tree: "CarTree") -> "CarTree":
    clear_screen()
    draw_header("OPTION 1 - Initialize the binary tree")

    if tree is not None:
        print(paint("\n   A tree named '" + tree.name + "' is already active with "
                    + str(tree.size) + " node(s).", Color.ORANGE))
        if not confirm("Discard it and start a brand new one?"):
            failure("Initialization cancelled. The current tree is untouched.")
            pause()
            return tree

    print(paint("\n   Give this catalog tree a name.", Color.GREY))
    name = ask_text("Tree name")
    fresh = CarTree(name)
    success("Tree '" + fresh.name + "' initialized and ready at " + fresh.created + ".")
    print(paint("   The structure is empty - load the CSV with option 2.", Color.GREY))
    pause()
    return fresh


# Option 2 - loads a CSV file into the structure.
def option_load_csv(tree: "CarTree") -> None:
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

    if not tree.is_empty():
        print(paint("\n   The tree already holds " + str(tree.size) + " node(s).",
                    Color.ORANGE))
        if not confirm("Replace it with the contents of this file?"):
            failure("Cancelled. The current tree is untouched.")
            pause()
            return

    try:
        handle = open(path, "r", encoding="utf-8-sig")
    except OSError as error:
        failure("Could not open the file: " + str(error))
        pause()
        return

    # PASS 1 - every row becomes a detached node held in a temporary chain.
    chain_head = None
    chain_tail = None
    created = 0
    skipped = 0
    duplicates = 0
    line_number = 0

    for raw_line in handle:
        line_number = line_number + 1
        line = raw_line.rstrip("\r\n")

        if line.strip() == "":
            continue
        if line_number == 1 and line.lower().startswith("node id"):
            continue

        node_id = read_field(line, 0)
        value = read_field(line, 1)
        parent_id = read_field(line, 2)
        branch = read_field(line, 3)
        node_path = read_field(line, 4)

        if node_id == "" or value == "":
            skipped = skipped + 1
            continue
        if find_in_chain(chain_head, node_id) is not None:
            duplicates = duplicates + 1
            continue

        link = NodeLink(TreeNode(node_id, value, parent_id, branch, node_path))
        if chain_head is None:
            chain_head = link
        else:
            chain_tail.next = link
        chain_tail = link
        created = created + 1

    handle.close()

    if created == 0:
        failure("The file contained no usable rows.")
        pause()
        return

    # PASS 2 - wire every node to its parent by scanning the chain.
    root_node = None
    extra_roots = 0
    orphans = 0
    conflicts = 0

    walker = chain_head
    while walker is not None:
        node = walker.node

        if node.parent_id == "":
            if root_node is None:
                root_node = node
            else:
                extra_roots = extra_roots + 1
        else:
            parent = find_in_chain(chain_head, node.parent_id)
            if parent is None:
                orphans = orphans + 1
            elif node.branch.lower().startswith("l"):
                if parent.left is None:
                    parent.left = node
                else:
                    conflicts = conflicts + 1
            elif node.branch.lower().startswith("r"):
                if parent.right is None:
                    parent.right = node
                else:
                    conflicts = conflicts + 1
            else:
                # No branch given: take whichever side is still free.
                if parent.left is None:
                    parent.left = node
                elif parent.right is None:
                    parent.right = node
                else:
                    conflicts = conflicts + 1

        walker = walker.next

    if root_node is None:
        failure("No root row found - every row lists a Parent ID.")
        pause()
        return

    tree.root = root_node
    tree.source_path = path

    # Count what actually hangs off the root, which may be fewer than the rows
    # created if some rows were orphaned.
    tree.size = count_nodes(tree.root)

    success(str(tree.size) + " node(s) loaded into '" + tree.name + "'.")
    print(paint("   Source: " + path, Color.GREY))
    print(paint("   Root: " + root_node.value + " (" + root_node.node_id + ")", Color.GREY))

    if skipped > 0:
        print(paint("   " + str(skipped) + " row(s) skipped - missing Node ID or Value.",
                    Color.ORANGE))
    if duplicates > 0:
        print(paint("   " + str(duplicates) + " row(s) skipped - duplicated Node ID.",
                    Color.ORANGE))
    if orphans > 0:
        print(paint("   " + str(orphans) + " row(s) orphaned - Parent ID not in the file.",
                    Color.ORANGE))
    if extra_roots > 0:
        print(paint("   " + str(extra_roots) + " extra row(s) had no Parent ID and were "
                    "left out - a tree has one root.", Color.ORANGE))
    if conflicts > 0:
        print(paint("   " + str(conflicts) + " row(s) dropped - that parent already had "
                    "both children.", Color.ORANGE))
    # Rows already explained above should not be counted a second time here.
    explained = orphans + extra_roots + conflicts
    if created - tree.size > explained:
        print(paint("   " + str(created - tree.size - explained)
                    + " node(s) are not reachable from the root.", Color.ORANGE))

    tree.print_summary()
    pause()


# Counts every node hanging off a subtree.
def count_nodes(node: "TreeNode") -> int:
    if node is None:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)


# Option 3 - renders the tree, with a small sub-menu of view styles.
def option_list_tree(tree: "CarTree") -> None:
    view = "1"

    while True:
        clear_screen()
        draw_header("OPTION 3 - List the binary tree")
        tree.print_summary()

        if view == "1":
            tree.print_rotated()
        elif view == "2":
            tree.print_branches()
        elif view == "3":
            tree.print_levels()
        else:
            tree.print_traversals()

        print(paint("\n   ─── VIEW " + "─" * 65, Color.PURPLE))
        print(paint("   [1] Rotated tree   [2] Branch outline   "
                    "[3] By level   [4] Traversals   [0] Back", Color.WHITE))
        choice = input(paint("\n   Choose a view: ", Color.BOLD + Color.CYAN)).strip()

        if choice == "0":
            return
        if choice == "1" or choice == "2" or choice == "3" or choice == "4":
            view = choice
        # Anything else simply redraws the current view.


# ---------------------------------------------------------------------------
# GOODBYE SCREEN
# ---------------------------------------------------------------------------

# Prints the session timer and signs off.
def goodbye(tree: "CarTree", started_at: float) -> None:
    elapsed = int(time.time() - started_at)
    minutes = elapsed // 60
    seconds = elapsed % 60

    clear_screen()
    width = 74
    print()
    print(paint("   ╔" + "═" * width + "╗", rainbow(3)))
    print(paint("   ║" + "SESSION CLOSED".center(width) + "║", Color.BOLD + Color.GREEN))
    print(paint("   ╟" + "─" * width + "╢", rainbow(3)))

    if tree is None:
        summary = "No tree was initialized this session."
    else:
        summary = ("Tree '" + tree.name + "' ended with "
                   + str(tree.size) + " node(s).")

    timer = "Session time: " + str(minutes) + "m " + str(seconds) + "s"
    print(paint("   ║" + summary.center(width) + "║", Color.WHITE))
    print(paint("   ║" + timer.center(width) + "║", Color.CYAN))
    print(paint("   ║" + " " * width + "║", rainbow(3)))
    print(paint("   ║" + "Thanks for using BINARY TREE v1.0".center(width) + "║",
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
    tree = None
    message = ""

    while True:
        clear_screen()
        draw_header("")
        draw_menu(tree)

        if message != "":
            print(paint("   " + message, Color.RED))
            message = ""

        choice = input(paint("\n   Select an option: ", Color.BOLD + Color.CYAN)).strip()

        if choice == "0":
            break

        if choice == "1":
            tree = option_initialize(tree)
            continue

        if choice == "2" or choice == "3":
            if tree is None:
                message = "✖ Initialize the tree first (option 1)."
                continue

            if choice == "2":
                option_load_csv(tree)
            else:
                if tree.is_empty():
                    message = "✖ The tree is empty - load the CSV first (option 2)."
                    continue
                option_list_tree(tree)
            continue

        message = "✖ '" + choice + "' is not a valid option."

    goodbye(tree, started_at)


#
# MAIN MENU
#
#


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(paint("\n\n   Interrupted. Closing BINARY TREE.\n", Color.RED))