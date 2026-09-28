import sys
from PyQt5.QtWidgets import QApplication
from gui import ShellWindow
from config import parse_args
from vfs import VFS

if __name__ == "__main__":
    args = parse_args()
    vfs = None
    if args.vfs:
        vfs = VFS()
        try:
            vfs.load_from_csv(args.vfs)
        except Exception as e:
            print(f"Error loading VFS: {e}")
            sys.exit(1)
    app = QApplication(sys.argv)
    w = ShellWindow(vfs=vfs, script_path=args.script)
    w.show()
    sys.exit(app.exec_())