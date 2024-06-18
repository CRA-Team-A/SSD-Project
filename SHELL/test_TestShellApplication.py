from unittest import TestCase, skip

from unittest.mock import Mock

from SHELL.TestShellApplication import TestShellApplication


class TestShellValidCommandCheck(TestCase):
    def setUp(self):
        self.mk_ssd = Mock()
        self.sut = TestShellApplication(self.mk_ssd)

    def is_valid(self, command):
        return self.sut.is_valid_command(command.split())

    def test_verify_correct_write_command(self):
        self.assertEqual(True, self.is_valid("write 3 0xAAAABBBB"))

    def test_verify_correct_fullwrite_command(self):
        self.assertEqual(True, self.is_valid("fullwrite 0xAAAABBBB"))

    def test_verify_correct_read_command(self):
        self.assertEqual(True, self.is_valid("read 3"))

    def test_verify_correct_fullread_command(self):
        self.assertEqual(True, self.is_valid("fullread"))

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

    def test_verify_read_incorrect_address(self):
        input_commands = ["read 100", "read -1", "read"]

        for input_command in input_commands:
            self.assertEqual(False, self.is_valid(input_command))

    def test_verify_fullwrite_incorrect_address(self):
        input_commands = ["fullwrite 50 OxAAAABBBB", "fullwrite", "fullwrite 0x11", "fullwrite 0xAABBFFTT"]

        for input_command in input_commands:
            self.assertEqual(False, self.is_valid(input_command))

    def test_verify_fullread_incorrect_address(self):
        input_commands = ["fullread 10", "fullread 0x111100000"]

        for input_command in input_commands:
            self.assertEqual(False, self.is_valid(input_command))

    def test_verify_help_incorrect_command(self):
        input_commands = ["help 10", "help 10 0x11110000"]

        for input_command in input_commands:
            self.assertEqual(False, self.is_valid(input_command))

class TestTestShellApplication(TestCase):
    def setUp(self):
        super().setUp()
        self.mk_ssd = Mock()

    def test_call_ssd_read_when_shell_read(self):
        self.mk_ssd.read.return_value = '1'
        shell = TestShellApplication(self.mk_ssd)
        shell.read(3)

        self.assertEqual(1, self.mk_ssd.read.call_count)

    def test_call_ssd_read_when_shell_fullread(self):
        self.mk_ssd.read.return_value = '1'
        shell = TestShellApplication(self.mk_ssd)
        shell.fullread()

        self.assertEqual(100, self.mk_ssd.read.call_count)

    def test_call_ssd_write_when_shell_write(self):
        self.mk_ssd.write.return_value = '1'
        shell = TestShellApplication(self.mk_ssd)
        shell.write(3, '0xAAAABBBB')

        self.assertEqual(1, self.mk_ssd.write.call_count)

    def test_call_ssd_write_100_when_shell_fullwrite(self):
        self.mk_ssd.write.return_value = '1'
        shell = TestShellApplication(self.mk_ssd)
        shell.fullwrite('0xAAAABBBB')

        self.assertEqual(100, self.mk_ssd.write.call_count)
