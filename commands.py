import time
from parser import parse
from vfs import VFS

start_time = time.time()
vfs = None

def set_vfs(v):
    global vfs
    vfs = v

def run_command(line: str) -> str:
    cmd, args = parse(line)
    if cmd is None:
        return ""
    if cmd == "exit":
        return "exit"
    if vfs is None:
        return "VFS not loaded"
    if cmd == "ls":
        return cmd_ls(args)
    if cmd == "cd":
        return cmd_cd(args)
    if cmd == "tree":
        return cmd_tree(args)
    if cmd == "uptime":
        return cmd_uptime()
    return f"command not found: {cmd}"

def cmd_ls(args):
    node = vfs.get_node(vfs.cwd)
    if not node or not node.is_dir:
        return "Not a directory"
    names = sorted(node.children.keys())
    return "\n".join(names) if names else ""

def cmd_cd(args):
    if not args:
        vfs.cwd = "/"
        return ""
    path = args[0]
    node = vfs.resolve_path(path)
    if node and node.is_dir:
        if path.startswith('/'):
            vfs.cwd = path
        else:
            vfs.cwd = vfs.cwd.rstrip('/') + '/' + path
            vfs.cwd = vfs.cwd.replace('//', '/')
        return ""
    else:
        return f"cd: {path}: No such directory"

def cmd_tree(args):
    node = vfs.get_node(vfs.cwd)
    if not node:
        return ""
    lines = []
    def recurse(n, prefix=""):
        lines.append(prefix + n.name)
        if n.is_dir:
            for child in sorted(n.children.values(), key=lambda x: x.name):
                recurse(child, prefix + "  ")
    recurse(node)
    return "\n".join(lines)

def cmd_uptime():
    elapsed = time.time() - start_time
    return f"Uptime: {int(elapsed)} seconds"

