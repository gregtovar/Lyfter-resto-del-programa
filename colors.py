#
#colors.py
#Manages the console color theme for the application.
#
#Uses ANSI escape codes — supported on macOS, Linux, and Windows 10+.
#The chosen color is stored in a module-level variable so every other
# module can import `c` and call c.print() / c.input() transparently.
#

from typography import fprint_transform

# ── ANSI codes ────────────────────────────────────────────────────────────────
_RESET  = "\033[0m"

_THEMES = {
    "0": ("Default", ""),           # no colour code → terminal default
    "1": ("Green",   "\033[32m"),
    "3": ("Yellow",  "\033[33m"),
    "4": ("Purple",  "\033[35m"),
    "5": ("Blue",    "\033[34m"),
}

# Active colour code (empty string = default)
_active_code: str = ""



def set_theme(key: str) -> None:
    """Activate the theme identified by *key* (e.g. '1' for Green)."""
    global _active_code
    _active_code = _THEMES[key][1]


def cprint(text: str = "") -> None:
    """print() wrapper that applies typography then the active colour."""
    text = fprint_transform(text)
    if _active_code:
        print(f"{_active_code}{text}{_RESET}")
    else:
        print(text)


def cinput(prompt: str = "") -> str:
    """input() wrapper that applies typography then the active colour."""
    prompt = fprint_transform(prompt)
    if _active_code:
        return input(f"{_active_code}{prompt}{_RESET}")
    return input(prompt)




def choose_theme() -> None:
    print("\n" + "─" * 45)
    print(" ")
    print("Application Configuration")
    print(" ")
    print("  Choose a colour theme for this session:")
    print("─" * 45)
    for key, (name, _) in _THEMES.items():
        print(f"  [{key}]  {name}")
    print("─" * 45)

    valid = set(_THEMES.keys())
    while True:
        print(" ")
        print("Application Configuration - Theme")
        print(" ")
        choice = input("  Select a theme: ").strip()
        if choice in valid:
            set_theme(choice)
            name = _THEMES[choice][0]
            # Print the confirmation in the chosen colour
            cprint(f"\n  ✓ Theme set to: {name}")
            break
        print(f"  ✗ '{choice}' is not valid. Choose from: {', '.join(sorted(valid))}.")
