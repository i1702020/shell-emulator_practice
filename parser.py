"""Parser for splitting input lines into a command and arguments."""

import shlex


def parse(line: str):
    """Split line into (command, args). Handles quoted arguments."""
    stripped = line.strip()
    if not stripped:
        return None, []
    try:
        parts = shlex.split(stripped)
    except ValueError:
        parts = stripped.split()
    if not parts:
        return None, []
    return parts[0], parts[1:]