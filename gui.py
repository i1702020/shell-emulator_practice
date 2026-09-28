import socket, getpass, sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget, QApplication
from parser import parse
from commands import run_command, set_vfs

class ShellWindow(QMainWindow):
    def __init__(self, vfs=None, script_path=None):
        super().__init__()
        set_vfs(vfs)
        user = getpass.getuser()
        host = socket.gethostname()
        self.setWindowTitle(f"Эмулятор - {user}@{host}")
        self.resize(800, 500)

        self.output = QTextEdit(); self.output.setReadOnly(True)
        self.input = QLineEdit()
        self.input.returnPressed.connect(self.on_enter)

        layout = QVBoxLayout()
        layout.addWidget(self.output)
        layout.addWidget(self.input)
        c = QWidget(); c.setLayout(layout); self.setCentralWidget(c)

        if script_path:
            self.run_script(script_path)

    def on_enter(self):
        text = self.input.text()
        self.input.clear()
        self.execute_command(text)

    def execute_command(self, text):
        self.output.append(f"$ {text}")
        result = run_command(text)
        if result == "exit":
            self.close()
            return
        if result:
            self.output.append(result)

    def run_script(self, script_path):
        try:
            with open(script_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        self.execute_command(line)
                        QApplication.processEvents()
        except Exception as e:
            self.output.append(f"Error running script: {e}")