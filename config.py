"""Command-line argument parsing and debug output."""

import argparse


def parse_args(argv=None):
    """Parse CLI arguments for the emulator."""
    parser = argparse.ArgumentParser(
        description="Shell emulator with in-memory VFS"
    )
    parser.add_argument("--vfs", help="Путь к CSV с VFS")
    parser.add_argument("--script", help="Путь к стартовому скрипту")
    return parser.parse_args(argv)


def dump_config(args):
    """Return key-value debug string for all provided options."""
    lines = [
        "=== Configuration ===",
        "vfs    = {0}".format(args.vfs),
        "script = {0}".format(args.script),
        "=====================",
    ]
    return "\n".join(lines)