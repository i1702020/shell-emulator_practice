from parser import parse

def run_command(line: str) -> str:
    cmd, args = parse(line)
    if cmd is None:
        return ""
    if cmd == "exit":
        raise SystemExit
    if cmd == "ls":
        return f"ls: {args}"
    if cmd == "cd":
        return f"cd: {args}"
    return f"command not found: {cmd}"