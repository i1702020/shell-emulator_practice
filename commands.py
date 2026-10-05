"""Built-in commands for the shell emulator."""

import time

from parser import parse

START_TIME = time.time()

EXIT_TOKEN = "exit"
ERR_NOT_LOADED = "VFS not loaded"
ERR_UNKNOWN = "command not found: {cmd}"
ERR_NO_PATH = "{cmd}: {path}: No such file or directory"
ERR_NOT_DIR = "{cmd}: {path}: Not a directory"

_state = {"vfs": None}


def set_vfs(vfs):
    """Register the active VFS instance."""
    _state["vfs"] = vfs


def get_vfs():
    """Return the active VFS instance or None."""
    return _state["vfs"]


def run_command(line: str):
    """Execute one line. Returns (ok, output)."""
    cmd, args = parse(line)
    if cmd is None:
        return True, ""
    if cmd == "exit":
        return True, EXIT_TOKEN
    vfs = get_vfs()
    if vfs is None:
        return False, ERR_NOT_LOADED
    handler = _HANDLERS.get(cmd)
    if handler is None:
        return False, ERR_UNKNOWN.format(cmd=cmd)
    return handler(args)


def _cmd_ls(args):
    """List directory contents; accepts optional path argument."""
    vfs = get_vfs()
    path = args[0] if args else vfs.cwd
    node = vfs.resolve_path(path)
    if node is None:
        return False, ERR_NO_PATH.format(cmd="ls", path=path)
    if not node.is_dir:
        return True, node.name
    return True, "\n".join(sorted(node.children))


def _cmd_cd(args):
    """Change current working directory."""
    vfs = get_vfs()
    if not args:
        vfs.cwd = "/"
        return True, ""
    path = args[0]
    node = vfs.resolve_path(path)
    if node is None:
        return False, ERR_NO_PATH.format(cmd="cd", path=path)
    if not node.is_dir:
        return False, ERR_NOT_DIR.format(cmd="cd", path=path)
    vfs.cwd = vfs.norm_path(path)
    return True, ""


def _cmd_tree(args):
    """Print the subtree rooted at path (or cwd)."""
    vfs = get_vfs()
    path = args[0] if args else vfs.cwd
    node = vfs.resolve_path(path)
    if node is None:
        return False, ERR_NO_PATH.format(cmd="tree", path=path)
    lines = []
    _collect_tree(node, "", lines)
    return True, "\n".join(lines)


def _collect_tree(node, prefix, lines):
    """Recursively append tree lines for node."""
    lines.append(prefix + node.name)
    if not node.is_dir:
        return
    for child in sorted(node.children.values(), key=lambda n: n.name):
        _collect_tree(child, prefix + "  ", lines)


def _cmd_uptime(_args):
    """Report seconds elapsed since emulator start."""
    elapsed = int(time.time() - START_TIME)
    return True, "Uptime: {sec} seconds".format(sec=elapsed)


def _cmd_chmod(args):
    """Change mode of a VFS node (in memory)."""
    if len(args) < 2:
        return False, "Usage: chmod <mode> <path>"
    vfs = get_vfs()
    mode, path = args[0], args[1]
    node = vfs.resolve_path(path)
    if node is None:
        return False, ERR_NO_PATH.format(cmd="chmod", path=path)
    node.mode = mode
    msg = "Mode of {path} changed to {mode}"
    return True, msg.format(path=path, mode=mode)


_HANDLERS = {
    "ls": _cmd_ls,
    "cd": _cmd_cd,
    "tree": _cmd_tree,
    "uptime": _cmd_uptime,
    "chmod": _cmd_chmod,
}