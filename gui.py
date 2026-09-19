import socket, getpass
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget
from parser import parse
from commands import run_command

class ShellWindow(QMainWindow):
    def __init__(self):
        super().__init__()
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

    def on_enter(self):
        text = self.input.text()
        self.input.clear()
        self.output.append(f"$ {text}")
        result = run_command(text)
        self.output.append(result)