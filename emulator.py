import os
import zipfile
import configparser
import shutil
from pathlib import Path

class ShellEmulator:
    def __init__(self, config_file):
        self.load_config(config_file)
        self.history = []
        self.cwd = Path(self.fs_root)

    def load_config(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        self.user = config['DEFAULT']['Username']
        self.hostname = config['DEFAULT']['Hostname']
        zip_path = config['DEFAULT']['FSZipPath']
        self.fs_root = "/tmp/virtual_fs"

        if os.path.exists(self.fs_root):
            shutil.rmtree(self.fs_root)

        os.makedirs(self.fs_root, exist_ok=True)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.fs_root)

    def prompt(self):
        return f"{self.user}@{self.hostname}:{self.cwd.relative_to(self.fs_root)}$ "

    def ls(self):
        return "\n".join(os.listdir(self.cwd))

    def cd(self, path):
        new_path = self.cwd / path if not Path(path).is_absolute() else Path(path)
        if new_path.exists() and new_path.is_dir():
            self.cwd = new_path
        else:
            return "No such directory"

    def echo(self, *args):
        return " ".join(args)

    def history_cmd(self):
        return "\n".join(self.history)

    def run_command(self, command):
        self.history.append(command)
        parts = command.strip().split()
        if not parts:
            return ""

        cmd, *args = parts
        if cmd == "ls":
            return self.ls()
        elif cmd == "cd":
            return self.cd(args[0]) if args else "No path provided"
        elif cmd == "echo":
            return self.echo(*args)
        elif cmd == "history":
            return self.history_cmd()
        elif cmd == "exit":
            return "exit"
        else:
            return f"Command not found: {cmd}"

    def cleanup(self):
        if os.path.exists(self.fs_root):
            shutil.rmtree(self.fs_root)
