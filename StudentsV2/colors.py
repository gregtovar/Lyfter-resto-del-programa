
#
#.  Colors.py
#.  Color theme setup and colored print/input helpers.
#
#

# *******Theme definitions *********
_THEMES = {
    "1": ("🔵  Blue",   "\033[94m"),
    "2": ("🟢  Green",  "\033[92m"),
    "3": ("🟣  Purple", "\033[95m"),
    "4": ("🩵  Cyan",   "\033[96m"),
    "0": ("⚪  Default (no color)", ""),
}

_active_code = ""   # set once via choose_theme()

BOLD  = "\033[1m"
DIM   = "\033[2m"
RED   = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def set_theme(key: str) -> None:
    global _active_code
    _, _active_code = _THEMES.get(key, ("", ""))


def get_code() -> str:
    return _active_code


def choose_theme() -> None:

    # Prompt user to pick a color theme.

    print(f"\n  {BOLD}Choose a color theme:{RESET}")
    for key, (label, _) in _THEMES.items():
        print(f"  {DIM}  {key}.{RESET}  {label}")
    while True:
        choice = input(f"\n  Option » ").strip()
        if choice in _THEMES:
            set_theme(choice)
            label, _ = _THEMES[choice]
            cprint(f"\n  ✔  Theme set to {label}\n")
            return
        print(f"  {RED}✖  Invalid option. Try again.{RESET}")


def cprint(text: str = "", **kwargs) -> None:
    #
    # 
    # Print with the active color, reset after.
    #
    #
    code = _active_code
    if code:
        print(f"{code}{text}{RESET}", **kwargs)
    else:
        print(text, **kwargs)


def cinput(prompt: str) -> str:
    """Input with the active color on the prompt."""
    code = _active_code
    if code:
        return input(f"{code}{prompt}{RESET}")
    return input(prompt)
