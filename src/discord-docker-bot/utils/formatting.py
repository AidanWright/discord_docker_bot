import re


def remove_ansi_codes(logs: str) -> str:
    """Remove ANSI escape codes from a string."""
    ansi_escape = re.compile(r"(?:\x1B[@-_][0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", logs)
