"""
typography.py
Simulates font size and font type in the terminal.

True font changes aren't possible from Python — the terminal controls that.
We approximate them with two techniques:
  • Size  → vertical padding (blank lines) around printed text and
             a leading indent prefix to give a "roomy" vs "compact" feel.
  • Type  → Unicode Mathematical Alphanumeric Symbols block, which contains
             styled equivalents of A-Z, a-z, 0-9 that render as bold,
             italic/sans-serif, or monospace glyphs in any Unicode-aware terminal.
"""


# ── Font size ─────────────────────────────────────────────────────────────────

_SIZE_OPTIONS = {
    "1": "Small",
    "2": "Medium",
    "3": "Large",
}

# (lines before, lines after, indent spaces)
_SIZE_PADDING = {
    "1": (0, 0, 0),   # compact – no extra whitespace
    "2": (0, 1, 2),   # medium  – one blank line after, slight indent
    "3": (1, 1, 4),   # large   – blank lines before and after, more indent
}

_active_size: str = "2"   # default: Medium


def set_size(key: str) -> None:
    global _active_size
    _active_size = key


def _apply_size(text: str) -> str:
    """Wrap *text* with the padding that corresponds to the active size."""
    before, after, indent = _SIZE_PADDING[_active_size]
    lines  = ("\n" * before) if before else ""
    lines += (" " * indent) + text
    lines += ("\n" * after) if after else ""
    return lines


# ── Font type ─────────────────────────────────────────────────────────────────

_TYPE_OPTIONS = {
    "1": "Normal",
    "2": "Bold",
    "3": "Monospace",
}

_active_type: str = "1"   # default: Normal


def set_type(key: str) -> None:
    global _active_type
    _active_type = key


# Unicode Mathematical Alphanumeric block offsets
# Each entry: (UPPER_base, lower_base, digit_base | None)
# Source: Unicode chart U+1D400
_UNICODE_MAPS = {
    # key: (UPPER offset from A, lower offset from a, digit offset from 0 or None)
    "1": None,                          # Normal — no transformation
    "2": (0x1D400, 0x1D41A, 0x1D7CE),  # Mathematical Bold
    "3": (0x1D670, 0x1D68A, 0x1D7F6),  # Mathematical Monospace
}

def _char_to_styled(ch: str) -> str:
    """Convert a single character to its Unicode styled equivalent."""
    mapping = _UNICODE_MAPS.get(_active_type)
    if mapping is None:
        return ch                          # Normal — pass through unchanged

    upper_base, lower_base, digit_base = mapping

    if "A" <= ch <= "Z":
        return chr(upper_base + ord(ch) - ord("A"))
    if "a" <= ch <= "z":
        return chr(lower_base + ord(ch) - ord("a"))
    if digit_base and "0" <= ch <= "9":
        return chr(digit_base + ord(ch) - ord("0"))
    return ch                              # punctuation / spaces — unchanged


def _apply_type(text: str) -> str:
    """Translate every letter/digit in *text* to the active Unicode style."""
    if _UNICODE_MAPS.get(_active_type) is None:
        return text
    return "".join(_char_to_styled(ch) for ch in text)


# ── Combined helpers (used everywhere instead of print/input) ─────────────────

def fprint(text: str = "") -> None:
    """
    print() wrapper that applies both active size padding and font type.
    Import this alongside cprint from colors and chain them:
        cprint(fprint_transform(text))   ← see tprint() below.
    """
    styled = _apply_type(text)
    print(_apply_size(styled))


def finput(prompt: str = "") -> str:
    """input() wrapper that applies font type to the prompt."""
    styled = _apply_type(prompt)
    return input(_apply_size(styled))


def fprint_transform(text: str) -> str:
    """
    Return the fully transformed string WITHOUT printing it.
    Used by tprint() in main so colors and typography can be combined.
    """
    return _apply_size(_apply_type(text))


# ── Startup prompts ───────────────────────────────────────────────────────────

def _prompt_loop(title: str, options: dict, setter) -> str:
    """Generic selection loop shared by choose_size and choose_type."""
    print("\n" + "─" * 45)
    print(f"  {title}:")
    print("─" * 45)
    for key, label in options.items():
        print(f"  [{key}]  {label}")
    print("─" * 45)

    valid = set(options.keys())
    while True:
        choice = input("  Select an option: ").strip()
        if choice in valid:
            setter(choice)
            print(f"\n  ✓ {title} set to: {options[choice]}")
            return choice
        print(f"  ✗ '{choice}' is not valid. Choose from: {', '.join(sorted(valid))}.")


def choose_size() -> None:
    """Ask the user to pick a font size at startup."""
    _prompt_loop("Choose a font size", _SIZE_OPTIONS, set_size)


def choose_type() -> None:
    """Ask the user to pick a font type at startup."""
    _prompt_loop("Choose a font type", _TYPE_OPTIONS, set_type)
