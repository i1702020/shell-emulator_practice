"""Virtual file system loaded from CSV, kept entirely in memory."""

import csv
import posixpath

DEFAULT_MODE = "755"


class VFSNode:
    """Single node (file or directory) of the virtual file system."""

    def __init__(self, name, is_dir, content="", mode=DEFAULT_MODE):
        self.name = name
        self.is_dir = is_dir
        self.content = content
        self.mode = mode
        self.children = {}


class VFS:
    """In-memory virtual file system with a current working directory."""

    def __init__(self, source_name="default"):
        self.root = VFSNode("/", True)
        self.cwd = "/"
        self.source_name = source_name

    def load_from_csv(self, filepath):
        """Populate the VFS tree from a CSV file at filepath."""
        with open(filepath, newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            if reader.fieldnames is None:
                raise ValueError("empty CSV")
            for row in reader:
                self._insert_row(row)

    def _insert_row(self, row):
        """Insert a single CSV row into the tree."""
        path = row["path"].strip()
        if path == "/":
            return
        parts = [part for part in path.split("/") if part]
        current = self.root
        for index, part in enumerate(parts):
            is_last = index == len(parts) - 1
            if part not in current.children:
                current.children[part] = self._make_node(
                    part, row, is_last
                )
            current = current.children[part]

    @staticmethod
    def _make_node(name, row, is_last):
        """Create a VFSNode from a CSV row."""
        is_dir = row["type"] == "dir" if is_last else True
        content = ""
        if is_last and not is_dir:
            content = row.get("content", "")
        mode = row.get("mode") or DEFAULT_MODE
        return VFSNode(name, is_dir, content, mode)

    def get_node(self, path):
        """Return the node at an absolute path or None."""
        if not path or path == "/":
            return self.root
        parts = [part for part in path.split("/") if part]
        current = self.root
        for part in parts:
            if part not in current.children:
                return None
            current = current.children[part]
        return current

    def norm_path(self, path):
        """Return canonical absolute path for path relative to cwd."""
        if path.startswith("/"):
            full = path
        else:
            full = posixpath.join(self.cwd, path)
        return posixpath.normpath(full)

    def resolve_path(self, path):
        """Resolve absolute or relative path against cwd."""
        return self.get_node(self.norm_path(path))