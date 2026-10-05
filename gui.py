"""PyQt5 GUI shell window."""

import getpass
import socket

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import (
    QApplication,
    QLineEdit,
    QMainWindow,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from commands import EXIT_TOKEN, run_command, set_vfs


class ShellWindow(QMainWindow):
    """Main window providing REPL over the VFS."""

    def __init__(self, vfs=None, script_path=None, debug_text=""):
        super().__init__()
        set_vfs(vfs)
        self._build_title()
        self.resize(800, 500)
        self._build_widgets()
        if debug_text:
            self.output.append(debug_text)
        if script_path:
            QTimer.singleShot(
                0, lambda: self.run_script(script_path)
            )

    def _build_title(self):
        """Set window title from real OS data."""
        user = getpass.getuser()
        host = socket.gethostname()
        title = "Эмулятор - [{0}@{1}]".format(user, host)
        self.setWindowTitle(title)

    def _build_widgets(self):
        """Create output area and input line."""
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.input = QLineEdit()
        self.input.returnPressed.connect(self._on_enter)
        layout = QVBoxLayout()
        layout.addWidget(self.output)
        layout.addWidget(self.input)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def _on_enter(self):
        """Handle Enter in the input line."""
        text = self.input.text()
        self.input.clear()
        self.execute_command(text)

    def execute_command(self, text):
        """Execute one command and display the result."""
        self.output.append("$ " + text)
        ok, result = run_command(text)
        if result == EXIT_TOKEN:
            self.close()
            return ok
        if result:
            self.output.append(result)
        return ok

    def run_script(self, script_path):
        """Run startup script; stop at the first failed command."""
        try:
            with open(script_path, encoding="utf-8") as handle:
                for raw in handle:
                    line = raw.strip()
                    if not line or line.startswith("#"):
                        continue
                    ok = self.execute_command(line)
                    QApplication.processEvents()
                    if not ok or not self.isVisible():
                        break
        except OSError as err:
            self.output.append("Script error: {0}".format(err))