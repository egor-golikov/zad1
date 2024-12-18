import unittest
from emulator import ShellEmulator
import os
import zipfile

class TestShellEmulator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create test ZIP filesystem
        cls.test_zip_path = "test_fs.zip"
        with zipfile.ZipFile(cls.test_zip_path, 'w') as zipf:
            zipf.writestr("home/test_user/file.txt", "Hello, world!")
        cls.config_path = "test_config.ini"
        with open(cls.config_path, 'w') as f:
            f.write(f"""[DEFAULT]
Username = test_user
Hostname = test_host
FSZipPath = {cls.test_zip_path}
""")

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_zip_path)
        os.remove(cls.config_path)

    def setUp(self):
        self.emulator = ShellEmulator(TestShellEmulator.config_path)

    def tearDown(self):
        self.emulator.cleanup()

    def test_ls(self):
        result = self.emulator.ls()
        self.assertIn("home", result)

    def test_cd(self):
        self.emulator.cd("home")
        self.assertIn("test_user", self.emulator.ls())

    def test_echo(self):
        result = self.emulator.echo("Hello,", "world!")
        self.assertEqual(result, "Hello, world!")

    def test_history(self):
        self.emulator.run_command("echo test")
        result = self.emulator.history_cmd()
        self.assertIn("echo test", result)

    def test_invalid_command(self):
        result = self.emulator.run_command("invalid_command")
        self.assertEqual(result, "Command not found: invalid_command")
