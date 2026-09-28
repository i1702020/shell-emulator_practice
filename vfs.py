import csv

class VFSNode:
    def __init__(self, name, is_dir, content="", mode="755"):
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.mode = mode
        self.children = {}

class VFS:
    def __init__(self):
        self.root = VFSNode("/", True)
        self.cwd = "/"

    def load_from_csv(self, filepath):
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                path = row['path'].strip()
                if path == '/':
                    continue
                parts = [p for p in path.split('/') if p]
                current = self.root
                for i, part in enumerate(parts):
                    is_last = (i == len(parts) - 1)
                    if part not in current.children:
                        is_dir = row['type'] == 'dir' if is_last else True
                        content = row['content'] if is_last and not is_dir else ""
                        mode = row.get('mode', '755')
                        current.children[part] = VFSNode(part, is_dir, content, mode)
                    current = current.children[part]

    def get_node(self, path):
        if path == '/':
            return self.root
        if path.startswith('/'):
            parts = [p for p in path.split('/') if p]
        else:
            parts = [p for p in path.split('/') if p]
        current = self.root
        for part in parts:
            if part == '..':
                continue
            if part not in current.children:
                return None
            current = current.children[part]
        return current

    def resolve_path(self, path):
        if path.startswith('/'):
            return self.get_node(path)
        else:
            base = self.cwd.rstrip('/')
            full = base + '/' + path
            full = full.replace('//', '/')
            return self.get_node(full)