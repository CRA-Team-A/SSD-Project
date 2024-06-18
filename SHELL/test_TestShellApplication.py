from unittest import TestCase, skip
from unittest.mock import Mock

from SHELL.TestShellApplication import TestShellApplication


class TestShellValidCommandCheck(TestCase):
    def setUp(self):
        self.sut = TestShellApplication()

    def is_valid(self, command):
        return self.sut.is_valid_command(command.split())

    def test_verify_correct_write_command(self):
        self.assertEqual(True, self.is_valid("write 3 0xAAAABBBB"))

    @skip
    def test_verify_correct_fullwrite_command(self):
        self.assertEqual(True, self.is_valid("fullwrite 0xAAAABBBB"))

    @skip
    def test_verify_correct_read_command(self):
        self.assertEqual(True, self.is_valid("read 3"))

    @skip
    def test_verify_correct_fullread_command(self):
        self.assertEqual(True, self.is_valid("fullread"))

    @skip
    def test_verify_correct_help(self):
        self.assertEqual(True, self.is_valid("help"))

    def test_verify_write_incorrect_data(self):
        input_commands = ["write 3 OxAAAABBBB", "write 3 0xAABBBB", "write 3 0xAAAABBBBCC"]

        for input_command in input_commands:
            self.assertEqual(False, self.is_valid(input_command))

    def test_verify_write_incorrect_address(self):
        input_commands = ["write 100 OxAAAABBBB", "write -1 OxAAAABBBB", "write 0x11 OxAAAABBBB"]

        for input_command in input_commands:
            self.assertEqual(False, self.is_valid(input_command))
