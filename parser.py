def parse(line: str):
    parts = line.strip().split()
    if not parts:
        return None, []
    return parts[0], parts[1:]