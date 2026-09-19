import sys
from PyQt5.QtWidgets import QApplication
from gui import ShellWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ShellWindow()
    w.show()
    sys.exit(app.exec_())