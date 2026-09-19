import argparse

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--vfs", help="Путь к CSV с VFS")
    p.add_argument("--script", help="Путь к стартовому скрипту")
    return p.parse_args()